import pandas as pd
import os

class MemoryAgent:
    def __init__(self, file_path="data/transactions.csv"):
        self.file_path = file_path

    def save_expense(self, date, category, amount):
        new_row = pd.DataFrame([{
            "date": date,
            "category": category,
            "amount": amount
        }])

        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row

        df.to_csv(self.file_path, index=False)


