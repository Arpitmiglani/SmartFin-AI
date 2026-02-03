class AlertAgent:
    def generate_alert(self, predicted, budget):
        if predicted > budget:
            return f"⚠️ Alert! You may exceed budget by {int(predicted - budget)}"
        else:
            return "✅ Spending looks safe"
