import streamlit as st
from db_connection import run_query
import plotly.express as px

def show():
    # === Title Card ===
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
        <h1>🏆 Leaderboards</h1>
    </div>
    """, unsafe_allow_html=True)

    # Filter Section
    countries_df = run_query("SELECT DISTINCT country FROM Competitors WHERE country IS NOT NULL ORDER BY country")
    country_list = ["All"] + countries_df["country"].dropna().tolist()

    selected_country = st.selectbox("Filter by Country", country_list)

    # ================= TOP PLAYERS QUERY =================

    top_query = """
          SELECT 
              r.ranking,
              c.name,
              c.country,
              r.points,
              r.movement
          FROM Competitor_Rankings r
          JOIN Competitors c
              ON r.competitor_id = c.competitor_id
          Where 1=1
    """

    params = []
    if selected_country != "All":
        top_query += " AND c.country = %s"
        params.append(selected_country)

    top_query += " ORDER BY r.ranking LIMIT 50"

    df = run_query(top_query, params)


    # ================= MEDAL TOP 3 =================

    st.subheader("🥇 Top 3 Players")

    top3 = df.head(3)

    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]

    for i in range(3):
        with cols[i]:
            if i < len(top3):
                st.markdown(f"### {medals[i]} #{top3.iloc[i]['ranking']}")
                st.metric(
                    top3.iloc[i]["name"],
                    f"{top3.iloc[i]['points']} pts",
                    delta=int(top3.iloc[i]["movement"])
                )
                st.caption(top3.iloc[i]["country"])
            else:
                st.markdown(f"### {medals[i]}")
                st.info("No player available for this position")


    st.divider()

    # ================= TOP N INTERACTIVE =================

    st.subheader("📊 Top Players Chart")

    top_n = st.slider("Select Top N", 5, 30, 10)
    chart_df = df.head(top_n)

    fig_bar = px.bar(
        chart_df,
        x="points",
        y="name",
        orientation="h",  
        title=f"Top {top_n} Players by Points",
        text="points",
        color="points",
        color_continuous_scale="viridis"
    )

    # Show labels outside bars
    fig_bar.update_traces(
        texttemplate='%{text}', 
        textposition='inside'
    )

    # Layout tweaks
    fig_bar.update_layout(
        xaxis_title="Points",
        yaxis_title=None, 
    )
    # Side-by-side layout
    col1, col2 = st.columns([1, 1])  

    with col1:
        st.dataframe(chart_df, use_container_width=True)

    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()
        


    # ================= RISING PLAYERS =================

    st.subheader("📈 Biggest Ranking Movers")

    rising_query = """
    SELECT 
        c.name,
        c.country,
        r.movement
    FROM Competitor_Rankings r
    JOIN Competitors c
        ON r.competitor_id = c.competitor_id
    WHERE r.movement > 0
    ORDER BY r.movement DESC
    LIMIT 10
    """

    rising_df = run_query(rising_query)

    fig_rising = px.bar(
        rising_df,
        x="movement",
        y="name",
        orientation="h",  
        title="Top Rising Players by Movement",
        text="movement",
        color="movement",
        color_continuous_scale="viridis"
    )

    # Show labels outside bars
    fig_rising.update_traces(
        texttemplate='%{text}', 
        textposition='outside'
    )

    # Layout tweaks
    fig_rising.update_layout(
        xaxis_title="Movement",
        yaxis_title=None
    )
    # Side-by-side layout
    col1, col2 = st.columns([1, 1])  

    with col1:
        st.dataframe(rising_df, use_container_width=True)

    with col2:
        st.plotly_chart(fig_rising, use_container_width=True)

    st.divider()
        

    # ================= COUNTRY DOMINANCE =================

    st.subheader("🌍 Country Strength")

    country_query = """
    SELECT 
        c.country,
        SUM(r.points) AS total_points
    FROM Competitors c
    JOIN Competitor_Rankings r
        ON c.competitor_id = r.competitor_id
    GROUP BY c.country
    ORDER BY total_points DESC
    LIMIT 10
    """

    country_df = run_query(country_query)

    fig_country = px.bar(
        country_df,
        x="country",
        y="total_points",
        title="Top Rising Players by Movement",
        text="total_points",
        color="total_points",
        color_continuous_scale="teal"
    )

    # Show labels outside bars
    fig_country.update_traces(
        texttemplate='%{text}', 
        textposition='outside'
    )

    # Layout tweaks
    fig_country.update_layout(
        xaxis_title=None,
        yaxis_title="Total Points"
    )
    # Side-by-side layout
    col1, col2 = st.columns([1, 1])  

    with col1:
        st.dataframe(country_df, use_container_width=True)

    with col2:
        st.plotly_chart(fig_country, use_container_width=True)

    