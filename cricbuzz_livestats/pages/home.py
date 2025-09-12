import streamlit as st

def show():
    st.set_page_config(page_title="🏏 Cricbuzz Dashboard", layout="wide")

    st.title("🏏 Cricbuzz Live Dashboard")
    st.markdown("""
    Welcome to the Cricbuzz Dashboard!  
    Use the sidebar to navigate between **Live Matches** and **Top Players**.
    """)
