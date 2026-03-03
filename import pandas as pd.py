import pandas as pd
import os

class MemoryAgent:
    def __init__(self, memory_file="memory_log.csv"):
        self.memory_file = memory_file
        # create file if it doesn't exist
        if not os.path.exists(self.memory_file):
            df = pd.DataFrame(columns=["total_spent", "budget", "predicted_end_month", "decision", "alert"])
            df.to_csv(self.memory_file, index=False)

    def save_record(self, total_spent, budget, predicted, decision, alert):
        df = pd.read_csv(self.memory_file)
        new_record = {
            "total_spent": total_spent,
            "budget": budget,
            "predicted_end_month": predicted,
            "decision": decision,
            "alert": alert
        }
        df = df.append(new_record, ignore_index=True)
        df.to_csv(self.memory_file, index=False)
