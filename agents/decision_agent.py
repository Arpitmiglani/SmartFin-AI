class DecisionAgent:
    def decide(self, total_spent, budget):
        if total_spent > budget:
            return "❌ You have exceeded your budget"
        else:
            return "✅ You are within your budget"
