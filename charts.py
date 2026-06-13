import streamlit as st
import matplotlib.pyplot as plt

def render_charts(df):

    st.subheader("Attrition by Department")

    dept = df.groupby("Department")["Attrition_Flag"].sum()

    fig, ax = plt.subplots()
    dept.plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Age Distribution")

    fig2, ax2 = plt.subplots()
    ax2.hist(df["Age"], bins=10)
    st.pyplot(fig2)
