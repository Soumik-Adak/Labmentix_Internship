import streamlit as st
import pandas as pd
from db_connection import run_query


def show():

    # === Custom Title Card ===
    st.markdown("""
    <style>
    .title-card {
        background: linear-gradient(135deg, #283c86, #45a247); 
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
        text-align: center;
        color: white;
    }
    .title-card h1 {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .title-card p {
        margin: 0.3rem 0;
        font-size: 1.1rem;
        color: #f1f1f1;
    }
    </style>
    """, unsafe_allow_html=True)

    # === Welcome Card ===
    st.markdown("""
    <div class="title-card">
        <h1>🎾 Tennis Analytics Dashboard</h1>
        <p>Welcome to the Tennis Analytics application</p>
        <p>This tool is designed to manage, visualize, and analyze tennis competition data using the <b>SportRadar API</b>.</p>
        <p>Explore the world of tennis through dynamic insights and visualizations powered by <b>Python</b>, <b>MySQL</b> and <b>Streamlit</b></p>
    </div>
    """, unsafe_allow_html=True)

    # === Custom CSS for KPI Cards ===
    st.markdown("""
    <style>
    .kpi-card {
        background: linear-gradient(135deg, #1f4037, #99f2c8);
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        text-align: center;
        color: white;
    }
    .kpi-card h3 {
        font-size: 1rem;       /* smaller header */
        font-weight: 500;
        margin-bottom: 0.4rem;
    }
    .kpi-card p {
        font-size: 1.6rem;     /* bigger number */
        font-weight: bold;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # === Query for KPIs ===
    query = """
        SELECT  
            COUNT(DISTINCT c.competitor_id) AS competitors,
            COUNT(DISTINCT c.country) AS countries,
            MAX(r.points) AS max_points
        FROM Competitors c
        JOIN Competitor_Rankings r 
            ON c.competitor_id = r.competitor_id
        WHERE 
            c.country IS NOT NULL AND r.points IS NOT NULL 
    """
    kpi = run_query(query)

    total_competitors = kpi.iloc[0, 0]
    countries = kpi.iloc[0, 1]
    top_points = kpi.iloc[0, 2]

    # === Layout: 3 columns, each with its own card ===
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>👥 Total Competitors</h3>
            <p><b>{total_competitors}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>🌍 Countries Represented</h3>
            <p><b>{countries}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>🏆 Highest Points</h3>
            <p><b>{int(top_points):,}</b></p>
        </div>
        """, unsafe_allow_html=True)


