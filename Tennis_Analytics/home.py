import streamlit as st
import pandas as pd
from db_connection import run_query


def show():
    st.title("🎾 Tennis Analytics Dashboard")

    query = """
    SELECT 
        COUNT(DISTINCT c.competitor_id) AS competitors,
        COUNT(DISTINCT c.country) AS countries,
        MAX(r.points) AS max_points
    FROM Competitors c
    JOIN Competitor_Rankings r 
        ON c.competitor_id = r.competitor_id
    """

    kpi = run_query(query)

    c1, c2, c3 = st.columns(3)
    c1.metric("🏃 Total Competitors", kpi.iloc[0, 0])
    c2.metric("🌍 Countries Represented", kpi.iloc[0, 1])
    c3.metric("🔥 Highest Points", kpi.iloc[0, 2])
