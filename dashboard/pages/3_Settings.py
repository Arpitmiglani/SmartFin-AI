import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Settings")
st.title("⚙️ Settings")

if st.button("🔄 Reset ALL Data"):
    pd.DataFrame(columns=["date", "category", "amount"]).to_csv(
        "data/transactions.csv", index=False
    )

    pd.DataFrame(columns=[
        "total_spent",
        "budget",
        "predicted_end_month",
        "decision",
        "alert"
    ]).to_csv("memory_log.csv", index=False)

    st.success("✅ All data reset")
