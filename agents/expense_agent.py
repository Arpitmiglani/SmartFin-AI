import pandas as pd

class ExpenseAnalysisAgent:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze(self):
        df = pd.read_csv(self.file_path)

        if df.empty:
            return 0, pd.Series(dtype="float64")

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna()

        total_spent = int(df["amount"].sum())

        # 🔴 IMPORTANT: RETURN A PANDAS SERIES (NOT DICT)
        category_spend = df.groupby("category")["amount"].sum()

        return total_spent, category_spend



