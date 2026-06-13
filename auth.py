import streamlit as st

def login_user():
    st.sidebar.header("Login")

    users = {
        "hr_admin": "HR Admin",
        "sales_manager": "Sales",
        "it_manager": "IT"
    }

    username = st.sidebar.selectbox("Select User", list(users.keys()))

    return users[username]
