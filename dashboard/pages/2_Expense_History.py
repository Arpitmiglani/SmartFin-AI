import streamlit as st
import pandas as pd

DATA_PATH = "data/transactions.csv"

st.title("Expense History")

# ---------------- SESSION STATE ----------------
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)

# ---------------- CLEAN BUTTON CSS ----------------
st.markdown("""
<style>

/* Make action buttons square */
div[data-testid="stButton"] button {
    width: 34px;
    height: 34px;
    border-radius: 6px;
    padding: 0;
}

/* Remove button text */
div[data-testid="stButton"] button span {
    display: none;
}

/* EDIT buttons */
button[id^="edit_"] {
    background-color: #ffffff !important;
    background-image: url("https://cdn-icons-png.flaticon.com/512/1159/1159633.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 16px;
}

/* DELETE buttons */
button[id^="delete_"] {
    background-color: #ffffff !important;
    background-image: url("https://cdn-icons-png.flaticon.com/512/3096/3096687.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TABLE ----------------
st.subheader("Your Expenses")

for i in range(len(df)):
    col1, col2, col3, col4, col5 = st.columns([3, 3, 2, 1, 1])

    col1.write(df.loc[i, "date"])
    col2.write(df.loc[i, "category"])
    col3.write(df.loc[i, "amount"])

   # EDIT BUTTON
with col4:
    if st.button(
        "✏️",
        key=f"edit_{i}",
        type="secondary",
        help="Edit"
    ):
        st.session_state.edit_index = i

# DELETE BUTTON
with col5:
    if st.button(
        "🗑️",
        key=f"delete_{i}",
        type="secondary",
        help="Delete"
    ):
        st.session_state.delete_index = i

# ---------------- DELETE LOGIC ----------------
if st.session_state.delete_index is not None:
    idx = st.session_state.delete_index
    df = df.drop(idx).reset_index(drop=True)
    df.to_csv(DATA_PATH, index=False)
    st.session_state.delete_index = None
    st.rerun()

# ---------------- EDIT FORM ----------------
if st.session_state.edit_index is not None:

    # Always reload fresh data
    df = pd.read_csv(DATA_PATH)

    idx = st.session_state.edit_index

    # Safety check
    if idx >= len(df):
        st.session_state.edit_index = None
        st.rerun()

    row = df.iloc[idx]   # ← VERY IMPORTANT

    st.markdown("---")
    st.subheader("Edit Expense")

    with st.form("edit_form"):

        new_date = st.date_input(
            "Date",
            pd.to_datetime(row["date"])
        )

        categories = ["Food", "Rent", "Transport", "Shopping", "Other"]

        new_category = st.selectbox(
            "Category",
            categories,
            index=categories.index(row["category"])
        )

        new_amount = st.number_input(
            "Amount",
            min_value=1,
            value=int(row["amount"])
        )

        save = st.form_submit_button("Save Changes")
        cancel = st.form_submit_button("Cancel")

    if save:
        df.iloc[idx] = [new_date, new_category, new_amount]
        df.to_csv(DATA_PATH, index=False)
        st.session_state.edit_index = None
        st.rerun()

    if cancel:
        st.session_state.edit_index = None
        st.rerun()


