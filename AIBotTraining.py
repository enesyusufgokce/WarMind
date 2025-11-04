from xgboost import XGBClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

data = pd.read_csv("ai_smart_behavior.csv")

x = data.drop("Action", axis=1)

categorical_features = x.select_dtypes(include=["object"]).columns

encoder = OneHotEncoder(drop = "first", sparse_output=False)
encoded_categorical = encoder.fit_transform(x[categorical_features])

encoded_columns = encoder.get_feature_names_out(categorical_features)
encoded_categorical_df = pd.DataFrame(encoded_categorical, columns=encoded_columns)

x_encoded = pd.concat([x.drop(categorical_features, axis=1).reset_index(drop=True),
                          encoded_categorical_df.reset_index(drop=True)], axis=1)

y = data["Action"]
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

x_train, x_temp, y_train, y_temp = train_test_split(x_encoded, y_encoded, test_size=0.4, random_state=1)
x_cv, x_test, y_cv, y_test = train_test_split(x_temp, y_temp, test_size=0.5, random_state=1)
del x_temp, y_temp

model = XGBClassifier(n_estimators=2000, learning_rate=0.5, max_depth=4, min_child_weight=5, subsample=0.7, colsample_bytree=0.2, reg_lambda=2.0, reg_alpha=1, gamma=2, random_state=1)
model.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_cv, y_cv)])

prediction = model.predict(x_test)

accuracy = accuracy_score(y_test, prediction)
print("model accuracy is:",accuracy)

import joblib
joblib.dump({
    "model": model,
    "encoder": encoder,
    "categorical_features": categorical_features
}, "ai_bot_model.pkl")
