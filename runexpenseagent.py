from agents.expense_agent import ExpenseAnalysisAgent
from agents.goal_planner_agent import GoalPlannerAgent
from agents.decision_agent import DecisionAgent
from agents.prediction_agent import PredictionAgent
from agents.alert_agent import AlertAgent
from agents.memory_agent import MemoryAgent

# -----------------------------
# CREATE AGENTS
# -----------------------------
expense_agent = ExpenseAnalysisAgent("C:/Users/ACER/Desktop/agentic_finance/data/transactions.csv")
goal_agent = GoalPlannerAgent(monthly_budget=3000)
decision_agent = DecisionAgent()
prediction_agent = PredictionAgent("C:/Users/ACER/Desktop/agentic_finance/data/transactions.csv")
alert_agent = AlertAgent()
memory_agent = MemoryAgent()

# -----------------------------
# RUN AGENTS
# -----------------------------
total_spent, category_spend = expense_agent.analyze()
budget = goal_agent.get_budget()
decision = decision_agent.decide(total_spent, budget)

# Train and predict
prediction_agent.train()
predicted_month_end = prediction_agent.predict(30)

# Generate alert
alert_message = alert_agent.generate_alert(predicted_month_end, budget)

# Save record in memory
memory_agent.save_record(
    total_spent,
    budget,
    round(predicted_month_end,2),
    decision,
    alert_message
)

# -----------------------------
# OUTPUT TO TERMINAL
# -----------------------------
print("Total Spent:", total_spent)
print("Budget:", budget)
print("Decision:", decision)
print("Predicted End-of-Month Spending:", round(predicted_month_end,2))
print("Alert:", alert_message)
print("\nCategory-wise Spending:")
print(category_spend)



