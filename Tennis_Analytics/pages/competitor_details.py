import streamlit as st
from db_connection import run_query   

def show():
    #st.title("Competitor Details")
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
        <h1>👤 Competitor Details</h1>
    </div>
    """, unsafe_allow_html=True)


    query = """
    SELECT c.name, c.country, r.ranking, r.points, r.movement, r.competitions_played
    FROM Competitors c
    JOIN Competitor_Rankings r 
        ON c.competitor_id = r.competitor_id
    """

    # Use the helper function 
    df = run_query(query)

    competitor = st.selectbox("Select a Competitor", sorted(df["name"].unique()))
    details = df[df["name"] == competitor].iloc[0]


    # === Custom Card for Name + Country ===
    st.markdown("""
    <style>
    .info-card {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        text-align: center;
        color: white;
    }
    .info-card h2 {
        font-size: 1.6rem;
        margin-bottom: 0.5rem;
    }
    .info-card p {
        font-size: 1.1rem;
        margin: 0;
        color: #f1f1f1;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card">
        <h2>{details['name']}</h2>
        <p>{details['country']}</p>
    </div>
    """, unsafe_allow_html=True)

    # === KPI Cards for Stats ===
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
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.4rem;
    }
    .kpi-card p {
        font-size: 1.6rem;
        font-weight: bold;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>📊 Rank</h3>
            <p><b>{details['ranking']}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>🏆 Points</h3>
            <p><b>{details['points']}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>📈 Movement</h3>
            <p><b>{details['movement']}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>🎯 Competitions Played</h3>
            <p><b>{details['competitions_played']}</b></p>
        </div>
        """, unsafe_allow_html=True)


   