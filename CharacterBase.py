class Character:
    def __init__(self, name, hp, damage, shield_uses, super_uses):
        self.name = name
        self.hp = float(hp)
        self.damage = float(damage)
        self.shield_uses = int(shield_uses)
        self.super_uses = int(super_uses)
        self.max_shield = 2
        self.max_supers = 2
        self.defending = False

    def attack(self):
        return self.damage

    def super_attack(self):
        if self.super_uses > 0:
            self.super_uses = self.super_uses - 1
            return self.damage * 1.3
        return self.damage

    def defend(self, incoming_damage):
        if self.defending:
            incoming_damage = incoming_damage * 0.6
            self.defending = False
        self.hp = self.hp - incoming_damage
        return incoming_damage

    def enable_defense(self):
        if self.shield_uses > 0:
            self.shield_uses = self.shield_uses - 1
            self.defending = True
            return True
        return False

    def is_alive(self):
        return self.hp > 0
