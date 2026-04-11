import streamlit as st
import pandas as pd
import os
import requests
from agents.expense_agent import ExpenseAnalysisAgent
from agents.decision_agent import DecisionAgent
from agents.prediction_agent import PredictionAgent
from agents.alert_agent import AlertAgent
from agents.memory_agent import MemoryAgent

from agents.recurring_agent import RecurringExpenseAgent
from agents.insight_agent import InsightAgent
import time


st.set_page_config(layout="wide")

# --------- FULL SCREEN SPLASH ---------
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if not st.session_state.app_started:

    # Hide sidebar & header
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        section[data-testid="stSidebar"] {display: none;}
        .block-container {
            padding: 0;
        }
        body {
            margin: 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        .splash {
            height: 100vh;
            width: 100vw;
            background: linear-gradient(135deg, #141e30, #243b55);
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            flex-direction: column;
        }
        .title {
            font-size: 70px;
            font-weight: 800;
            letter-spacing: 2px;
            animation: fadeIn 2s ease-in-out;
        }
        .subtitle {
            font-size: 24px;
            margin-top: 20px;
            opacity: 0.8;
            animation: fadeIn 3s ease-in-out;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(30px);}
            to {opacity: 1; transform: translateY(0);}
        }
        </style>

        <div class="splash">
            <div class="title">SmartFin AI</div>
            <div class="subtitle">Smarter Budgeting. Better Decisions.</div>
        </div>
    """, unsafe_allow_html=True)

    time.sleep(3)

    st.session_state.app_started = True
    st.rerun()

st.set_page_config(page_title="Agentic AI Finance Manager", layout="wide")
st.title("💸 Agentic AI Personal Finance Manager")

DATA_PATH = "data/transactions.csv"
# ---------------- BUDGET PERSISTENCE ----------------

BUDGET_PATH = "data/budget.csv"

# If file does not exist OR is empty → recreate it
if not os.path.exists(BUDGET_PATH) or os.path.getsize(BUDGET_PATH) == 0:
    pd.DataFrame({"budget": [3000]}).to_csv(BUDGET_PATH, index=False)

# Now safely read
budget_df = pd.read_csv(BUDGET_PATH)

# Extra safety in case structure breaks
if "budget" not in budget_df.columns:
    pd.DataFrame({"budget": [3000]}).to_csv(BUDGET_PATH, index=False)
    budget_df = pd.read_csv(BUDGET_PATH)

current_budget = int(budget_df.loc[0, "budget"])

# ---------------- SIDEBAR ----------------
budget = st.sidebar.number_input(
    "Set Monthly Budget",
    min_value=0,
    value=current_budget,
    step=500
)


st.sidebar.markdown("### ➕ Add Daily Expense")

with st.sidebar.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox(
        "Category",
        ["Food", "Rent", "Transport", "Shopping", "Other"]
    )
    amount = st.number_input("Amount", min_value=1)
    if budget != current_budget:
        pd.DataFrame({"budget": [budget]}).to_csv(BUDGET_PATH, index=False)
    submit = st.form_submit_button("Add Expense")

# -------- RESET BUTTON (RUNS FIRST) --------
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

recurring_agent = RecurringExpenseAgent(DATA_PATH)

insight_agent = InsightAgent(DATA_PATH)

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
insights = insight_agent.generate_insights()

# ---------------- DISPLAY ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Spent", total_spent)
col2.metric("Budget", budget)
col3.metric("Predicted Month End", int(predicted))

if "⚠️" in alert:
    st.error(alert)
else:
    st.success(alert)
    st.markdown("---")
# -------- AI INSIGHT EXPLAINER --------
def explain_insight(insight):

    text = insight.lower()

    if "highest spending category" in text:
        return "This means a large portion of your money is going into one category. You should check if this expense is necessary or can be reduced."

    elif "average daily spending" in text:
        return "This shows how much you spend daily. If this number is high, you may run out of budget before month end."

    elif "warning" in text:
        return "This is a risk signal. You are overspending in one category which can affect your savings."

    elif "not enough data" in text:
        return "You need more transactions for better analysis. Keep adding expenses daily."

    else:
        return "This insight highlights a pattern in your spending. Use it to improve your financial habits."
st.subheader("📊 Smart Insights")

# Track open card
if "open_card" not in st.session_state:
    st.session_state.open_card = -1


# PREMIUM CSS
st.markdown("""
<style>

.card {
    background: linear-gradient(145deg, #1f2937, #111827);
    padding: 18px;
    border-radius: 16px;
    color: white;
    font-size: 15px;
    font-weight: 500;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
    margin-bottom: 15px;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.05);
}

.card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 35px rgba(79,70,229,0.4);
    border: 1px solid rgba(79,70,229,0.5);
}

.card-expanded {
    background: linear-gradient(145deg, #1f2937, #111827);
    padding: 18px;
    border-radius: 16px;
    color: white;
    box-shadow: 0 12px 35px rgba(79,70,229,0.5);
    border: 1px solid rgba(79,70,229,0.6);
    margin-bottom: 15px;
}

.ai-text {
    margin-top: 10px;
    font-size: 14px;
    color: #d1d5db;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 10px;
}

</style>
""", unsafe_allow_html=True)


if insights:

    col1, col2 = st.columns(2)

    for i, insight in enumerate(insights):

        col = col1 if i % 2 == 0 else col2

        with col:

            # Handle click
            if st.button("", key=f"card_click_{i}"):
                if st.session_state.open_card == i:
                    st.session_state.open_card = -1
                else:
                    st.session_state.open_card = i

            # EXPANDED CARD
            if st.session_state.open_card == i:

                explanation = explain_insight(insight)

                st.markdown(f"""
                <div class="card-expanded">
                    💡 {insight}
                    <div class="ai-text">
                        🤖 {explanation}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # NORMAL CARD
            else:

                st.markdown(f"""
                <div class="card">
                    💡 {insight}
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("No insights available yet.")

# ---------------- WORKING PREMIUM ASSISTANT ----------------

# STATE
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# CSS
st.markdown("""
<style>

/* Avatar */
.avatar {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 65px;
    height: 65px;
    border-radius: 50%;
    background: url('https://cdn-icons-png.flaticon.com/512/4712/4712109.png');
    background-size: cover;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.5);
    z-index: 999;
}

/* Bubble */
.chat-bubble {
    position: fixed;
    bottom: 95px;
    right: 20px;
    background: #4F46E5;
    color: white;
    padding: 8px 12px;
    border-radius: 15px;
    font-size: 12px;
    z-index: 999;
}

/* Chat window */
.chat-window {
    position: fixed;
    bottom: 110px;
    right: 20px;
    width: 300px;
    height: 400px;
    background: #111827;
    border-radius: 15px;
    padding: 10px;
    overflow-y: auto;
    z-index: 999;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.6);
}

/* Input box fix */
.chat-input input {
    width: 100% !important;
}

</style>
""", unsafe_allow_html=True)


# CLICKABLE BUTTON (REAL FUNCTIONAL BUTTON)
btn_col = st.columns([9,1])[1]

with btn_col:
    if st.button("🤖", key="avatar_click"):
        st.session_state.chat_open = not st.session_state.chat_open


# Visual avatar + bubble
st.markdown('<div class="avatar"></div>', unsafe_allow_html=True)
st.markdown('<div class="chat-bubble">Ask me anything 💬</div>', unsafe_allow_html=True)


# CHAT WINDOW
if st.session_state.chat_open:

    st.markdown('<div class="chat-window">', unsafe_allow_html=True)

    st.markdown("### 🤖 SmartFin Assistant")

    # INPUT
    user_q = st.text_input("Type here...", key="chat_input")

    if st.button("Send", key="send_msg"):

        if user_q.strip() != "":
            reply = smartfin_chatbot(user_q)

            st.session_state.chat_history.append(("You", user_q))
            st.session_state.chat_history.append(("AI", reply))


    # DISPLAY CHAT
    for sender, msg in st.session_state.chat_history:

        if sender == "You":
            st.markdown(f"🧑 **You:** {msg}")
        else:
            st.markdown(f"🤖 **AI:** {msg}")

    st.markdown("</div>", unsafe_allow_html=True)