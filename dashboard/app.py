import streamlit as st
import pandas as pd
import os

from agents.expense_agent import ExpenseAnalysisAgent
from agents.decision_agent import DecisionAgent
from agents.prediction_agent import PredictionAgent
from agents.alert_agent import AlertAgent
from agents.memory_agent import MemoryAgent


st.set_page_config(page_title="Agentic AI Finance Manager", layout="wide")
st.title("💸 Agentic AI Personal Finance Manager")

DATA_PATH = "data/transactions.csv"

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

budget = st.sidebar.number_input(
    "Set Monthly Budget",
    min_value=0,
    value=3000,
    step=500
)

if budget > 13000:
    st.sidebar.error("❌ Budget cannot exceed 13000")
    st.stop()

st.sidebar.markdown("### ➕ Add Daily Expense")

with st.sidebar.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox(
        "Category",
        ["Food", "Rent", "Transport", "Shopping", "Other"]
    )
    amount = st.number_input("Amount", min_value=1)
    submit = st.form_submit_button("Add Expense")

# -------- RESET BUTTON (RUNS FIRST) --------
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All Data"):
    pd.DataFrame(columns=["date", "category", "amount"]).to_csv(
        DATA_PATH, index=False
    )

    if os.path.exists("memory_log.csv"):
        pd.DataFrame(columns=[
            "total_spent",
            "budget",
            "predicted_end_month",
            "decision",
            "alert"
        ]).to_csv("memory_log.csv", index=False)

    st.sidebar.success("✅ All data reset")
    st.rerun()

# ---------------- AGENTS ----------------
expense_agent = ExpenseAnalysisAgent(DATA_PATH)
decision_agent = DecisionAgent()
prediction_agent = PredictionAgent(DATA_PATH)
alert_agent = AlertAgent()
memory_agent = MemoryAgent(DATA_PATH)

# -------- ADD EXPENSE LOGIC --------
if submit:
    memory_agent.save_expense(date, category, amount)
    st.sidebar.success("✅ Expense added")
    st.rerun()

# ---------------- RUN LOGIC ----------------
total_spent, category_spend = expense_agent.analyze()
decision = decision_agent.decide(total_spent, budget)

trained = prediction_agent.train()
predicted = prediction_agent.predict(30) if trained else total_spent

alert = alert_agent.generate_alert(predicted, budget)

# ---------------- DISPLAY ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Spent", total_spent)
col2.metric("Budget", budget)
col3.metric("Predicted Month End", int(predicted))

if "⚠️" in alert:
    st.error(alert)
else:
    st.success(alert)

st.subheader("📊 Category-wise Spending")

if isinstance(category_spend, pd.Series) and not category_spend.empty:
    st.bar_chart(category_spend)
else:
    st.info("No expenses added yet")


st.subheader("📄 Expense History")
df = pd.read_csv(DATA_PATH)
st.dataframe(df, use_container_width=True)
