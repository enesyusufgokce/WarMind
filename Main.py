from Characters.Knight import Knight
from Characters.Giant import Giant
from Characters.Musketeer import Musketeer
import joblib
import pandas as pd
import numpy as np

bundle = joblib.load("ai_bot_model.pkl")
model = bundle["model"]
encoder = bundle["encoder"]
categorical_features = bundle["categorical_features"]

def options():
    print("Character options")
    print("1-Knight")
    print("2-Giant")
    print("3-Musketeer")

    p1 = input("for player 1, select a character(1/2/3) ")
    p2 = input("for player 2, select a character(1/2/3) ")

    def select(character):
        if character == "1":
            return Knight()
        elif character == "2":
            return Giant()
        elif character == "3":
            return Musketeer()
        else:
            raise Exception("Invalid character")

    player1 = select(p1)
    player2 = select(p2)

    def player1_characters():
        if p1 == "1":
            print("Player 1 is a Knight")
        elif p1 == "2":
            print("Player 1 is a Giant")
        elif p1 == "3":
            print("Player 1 is a Musketeer")

    def player2_characters():
        if p2 == "1":
            print("Player 2 is a Knight")
        elif p2 == "2":
            print("Player 2 is a Giant")
        elif p2 == "3":
            print("Player 2 is a Musketeer")

    player1_characters()
    player2_characters()

    player2.hp += 15

    return player1, player2

def ai_action(bot, player, player_action):
    data = pd.DataFrame([{
        "AI_Name": bot.name,
        "Player_Name": player.name,
        "AI_HP": bot.hp,
        "Player_HP": player.hp,
        "AI_Damage": bot.damage,
        "Player_Damage": player.damage,
        "AI_Shield": bot.shield_uses,
        "Player_Shield": player.shield_uses,
        "AI_Super": bot.super_uses,
        "Player_Super": player.super_uses,
        "Round_Number": np.random.randint(1, 11),
        "AI_HP_Diff": bot.hp - player.hp,
        "AI_Mode": np.random.choice(["aggressive", "defensive", "balanced"]),
        "Player_Action": player_action
    }])
    encoded = encoder.transform(data[categorical_features])
    encoded_cols = encoder.get_feature_names_out(categorical_features)
    encoded_df = pd.DataFrame(encoded, columns=encoded_cols)

    x_encoded = pd.concat(
        [data.drop(categorical_features, axis=1).reset_index(drop=True),
         encoded_df.reset_index(drop=True)],
        axis=1)

    action = model.predict(x_encoded)[0]

    if action == 0:
        dmg = bot.attack()
        player.defend(dmg)
        print(f"[AI {bot.name}] attacked for {dmg:.1f} damage on [Player {player.name}]!")

    elif action == 1 and bot.shield_uses > 0:
        bot.enable_defense()
        print(f"[AI {bot.name}] is defending! ({bot.shield_uses} shields left)")

    elif action == 2 and bot.super_uses > 0:
        dmg = bot.super_attack()
        player.defend(dmg)
        print(f"[AI {bot.name}] used SUPER ATTACK on [Player {player.name}] for {dmg:.1f} damage!")

    else:
        dmg = bot.attack()
        player.defend(dmg)
        print(f"[AI {bot.name}] attacked for {dmg:.1f} damage on [Player {player.name}]!")


def battle(player1, player2):
    while player1.is_alive() and player2.is_alive():
        print(f"\n{player1.name}: {player1.hp:.1f} HP | {player2.name}: {player2.hp:.1f} HP")

        while True:
            move = input("1-Attack  2-Defend  3-Super Attack: ")

            if move == "1":
                player_action = "attack"
                dmg = player1.attack()
                player2.defend(dmg)
                break

            elif move == "2":
                player_action = "defend"
                if player1.enable_defense():
                    print(f"{player1.name} is defending!")
                    break
                else:
                    print(f"{player1.name} has no shields left, choose another move.")

            elif move == "3":
                player_action = "super"
                if player1.super_uses > 0:
                    dmg = player1.super_attack()
                    player2.defend(dmg)
                    print(f"{player1.name} used a Super Attack! ({player1.super_uses} left)")
                    break
                else:
                    print(f"{player1.name} has no super attacks left, choose another move.")

            else:
                print("Invalid choice. Try again.")

        if not player2.is_alive():
            print(f"{player2.name} has been defeated.")
            break

        ai_action(player2, player1, player_action)

        if not player1.is_alive():
            print(f"{player1.name} has been defeated.")
            break


if __name__ == "__main__":
    player1, player2 = options()
    battle(player1, player2)
