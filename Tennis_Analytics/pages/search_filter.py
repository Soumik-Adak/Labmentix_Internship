import streamlit as st
from db_connection import run_query

def show():
    #st.title("🔍 Search & Filter Competitors")

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
        <h1>🔍 Search & Filter Competitors</h1>
    </div>
    """, unsafe_allow_html=True)

    
    # ---------- Filter Section ----------
    st.markdown("### Filters")

    # Row 1: Name + Country
    c1, c2 = st.columns([2, 1])
    with c1:
        search_name = st.text_input("👤 Competitor Name")
    countries_df = run_query("SELECT DISTINCT country FROM Competitors WHERE country IS NOT NULL ORDER BY country")
    country_list = ["All"] + countries_df["country"].dropna().tolist()
    with c2:
        country = st.selectbox("🌍 Country", country_list)

    # Row 2: Rank Range + Points
    c3, c4 = st.columns([1, 1])
    with c3:
        rank_range = st.slider("🏆 Ranking Range", 1, 500, (1, 100))
    with c4:
        min_points = st.slider("📊 Minimum Points", 0, 5000, 0)

    # Row 3: Movement
    movement_type = st.selectbox("📈 Movement", ["All", "Rising", "Falling"])

    # ---------- Build Query ----------
    query = """
    SELECT 
        c.name,
        c.country,
        r.ranking,
        r.points,
        r.movement,
        r.competitions_played
    FROM Competitors c
    JOIN Competitor_Rankings r
        ON c.competitor_id = r.competitor_id
    WHERE 1=1
    """
    params = []

    if search_name:
        query += " AND c.name LIKE %s"
        params.append(f"%{search_name}%")

    if country != "All":
        query += " AND c.country = %s"
        params.append(country)

    query += " AND r.points >= %s"
    params.append(min_points)

    query += " AND r.ranking BETWEEN %s AND %s"
    params.extend(rank_range)

    if movement_type == "Rising":
        query += " AND r.movement > 0"
    elif movement_type == "Falling":
        query += " AND r.movement < 0"

    query += " ORDER BY r.ranking"

    df = run_query(query, params)

    # ---------- Styled Data Table ----------
    st.markdown("""
    <style>
    .dataframe th {
        background-color: #283c86;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True)
