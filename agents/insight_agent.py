import pandas as pd
from datetime import datetime, timedelta

class InsightAgent:
    def __init__(self, file_path):
        self.file_path = file_path

    def generate_insights(self):
        try:
            df = pd.read_csv(self.file_path)
        except:
            return ["No data available yet."]

        if df.empty:
            return ["No expenses recorded yet."]

        insights = []

        # Convert date
        df["date"] = pd.to_datetime(df["date"])

        # 1. Highest spending category
        category_totals = df.groupby("category")["amount"].sum()
        top_category = category_totals.idxmax()
        top_amount = category_totals.max()

        insights.append(
            f"Highest spending category: {top_category} (₹{int(top_amount)})"
        )

        # 2. Average daily spending
        total_spent = df["amount"].sum()
        days = (df["date"].max() - df["date"].min()).days + 1
        avg_daily = total_spent / max(days, 1)

        insights.append(
            f"Average daily spending: ₹{int(avg_daily)}"
        )

        # 3. Weekly comparison
        today = datetime.today()
        last_week = today - timedelta(days=7)

        current_week = df[df["date"] >= last_week]["amount"].sum()

        previous_week = df[
            (df["date"] < last_week) &
            (df["date"] >= last_week - timedelta(days=7))
        ]["amount"].sum()

        if previous_week > 0:
            change = ((current_week - previous_week) / previous_week) * 100
            insights.append(f"Weekly spending change: {round(change,1)}%")
        else:
            insights.append("Not enough data for weekly comparison")

        # 4. Dominant category warning
        if top_amount > 0.5 * total_spent:
            insights.append(f"Warning: Over 50% spending is on {top_category}")

        return insights