import streamlit as st
from agents.expense_agent import ExpenseAnalysisAgent

DATA_PATH = "data/transactions.csv"

st.set_page_config(page_title="Category Spending", layout="wide")
st.title("📊 Category-wise Spending")

expense_agent = ExpenseAnalysisAgent(DATA_PATH)

total_spent, category_spend = expense_agent.analyze()

# ✅ CORRECT CHECK
if not category_spend.empty:
    st.bar_chart(category_spend)

    st.subheader("📋 Category Breakdown")
    st.dataframe(
        category_spend.reset_index().rename(
            columns={"index": "Category", 0: "Amount"}
        ),
        use_container_width=True
    )
else:
    st.info("No expenses added yet")
