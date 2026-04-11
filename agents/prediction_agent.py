import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class PredictionAgent:
    def __init__(self, file_path):
        self.file_path = file_path
        self.model = LinearRegression()

    def train(self):
        df = pd.read_csv(self.file_path)

        if len(df) < 2:
            return False

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["day"] = np.arange(1, len(df) + 1)

        X = df[["day"]]
        y = df["amount"]
        # Remove NaN rows
        data = pd.concat([X, y], axis=1).dropna()

        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]

        self.model.fit(X, y)
        return True

    def predict(self, day):
        return float(self.model.predict([[day]])[0])

