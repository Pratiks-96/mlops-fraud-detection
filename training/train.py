import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


DATA_PATH = "training/fraud.csv"
MODEL_PATH = "model/model.joblib"


def load_data():
    df = pd.read_csv(DATA_PATH)

    X = df.drop("is_fraud", axis=1)
    y = df["is_fraud"]

    return X, y


def train():

    print("Loading dataset...")

    X, y = load_data()

    print("Splitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    print("Training model...")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    print("Evaluating model...")

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"Accuracy: {accuracy}")

    os.makedirs("model", exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("Model saved at:", MODEL_PATH)


if __name__ == "__main__":
    train()
