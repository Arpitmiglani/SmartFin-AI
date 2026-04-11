import pandas as pd
from datetime import datetime, timedelta

class RecurringExpenseAgent:
    def __init__(self, data_path):
        self.data_path = data_path

    def detect_recurring(self):
        df = pd.read_csv(self.data_path)

        if df.empty:
            return []

        df["date"] = pd.to_datetime(df["date"])
        today = datetime.today()

        reminders = []

        for category in df["category"].unique():

            cat_df = df[df["category"] == category].sort_values("date")

            if len(cat_df) < 3:
                continue

            diffs = cat_df["date"].diff().dropna().dt.days
            avg_gap = int(diffs.mean())

            # Detect monthly pattern
            if 25 <= avg_gap <= 35:

                last_date = cat_df["date"].iloc[-1]
                next_due = last_date + timedelta(days=avg_gap)

                # 🔥 FIX: Keep pushing next_due into future
                while next_due < today:
                    next_due += timedelta(days=avg_gap)

                days_until_due = (next_due - today).days

                # Premium reminder window
                if 0 <= days_until_due <= 0:

                    if days_until_due == 0:
                        message = f"{category} payment is due today."
                    elif days_until_due == 1:
                        message = f"{category} payment is due tomorrow."
                    else:
                        message = f"{category} payment is due in {days_until_due} days."

                    reminders.append({
                        "category": category,
                        "due_date": next_due.strftime("%Y-%m-%d"),
                        "message": message
                    })

        return reminders