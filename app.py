import streamlit as st
from auth import login_user
from data_loader import load_data
from metrics import calculate_kpis
from charts import render_charts

st.set_page_config(page_title="IBM HR Attrition Portal", layout="wide")

# ---------------- Landing Page ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("IBM HR Attrition Intelligence Portal")
    st.image("assets/ibm_logo.png", width=200)

    st.write("""
    An interactive analytics platform to understand employee attrition patterns,
    workforce trends, and department-level insights using IBM HR dataset.
    """)

    if st.button("Login"):
        st.session_state.logged_in = True
        st.rerun()

# ---------------- After Login ----------------
else:
    user_role = login_user()

    df = load_data()

    st.sidebar.success(f"Logged in as: {user_role}")

    # Filter based on role
    if user_role != "HR Admin":
        df = df[df["Department"] == user_role]

    kpis = calculate_kpis(df)

    st.title("Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Employees", kpis["total_employees"])
    col2.metric("Attrition Count", kpis["attrition_count"])
    col3.metric("Attrition Rate (%)", kpis["attrition_rate"])
    col4.metric("Avg Age", kpis["avg_age"])

    render_charts(df)
