class DecisionAgent:
    def decide(self, total_spent, budget):
        if total_spent > budget:
            return "⚠️ Warning: You are over budget! Reduce spending."
        else:
            return "✅ You are within the budget. Good job!"
