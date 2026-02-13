import streamlit as st
import plotly.express as px
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
        <h1>🌍 Country-Wise Analysis</h1>
    </div>
    """, unsafe_allow_html=True)

    query = """
        SELECT c.country, 
              COUNT(*) AS competitors, 
              ROUND(AVG(r.points), 2) AS avg_points
        FROM Competitors c
        JOIN Competitor_Rankings r 
          ON c.competitor_id = r.competitor_id
        GROUP BY c.country
        ORDER BY competitors DESC
    """

    df_country = run_query(query)

    # === KPI Calculations ===
    total_countries = df_country["country"].nunique()
    top_nation = df_country.iloc[0]["country"]   # first row after ORDER BY competitors DESC
    avg_points_per_country = round(df_country["avg_points"].mean(), 2)


    # === Custom KPI Cards ===
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

    # === KPI Layout ===
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>🌍 Total Countries</h3>
            <p><b>{total_countries}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>🥇 Leading Nation</h3>
            <p><b>{top_nation}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>📊 Avg Points per Country</h3>
            <p><b>{avg_points_per_country}</b></p>
        </div>
        """, unsafe_allow_html=True)

    # plot charts
    st.subheader("🌍 Top Country Chart")

    fig_bar = px.bar(
        df_country.head(10),
        x="country",
        y="competitors",
        title="Top 10 Countries by Competitor Count",
        color="competitors",
        color_continuous_scale="teal",
        text="competitors"
    )
    # Make labels appear nicely
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')

    # Layout tweaks
    fig_bar.update_layout(
        xaxis_title=None,
        yaxis_title="Competitors"
    )

    # Side-by-side layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(df_country, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()

    # Sort by avg_points
    df_points_top = (
        df_country
        .sort_values("avg_points", ascending=False)
        .head(10)
    )

    # Average Points by Country (Top 10)
    fig_points = px.bar(
          df_points_top,
          x="avg_points",
          y="country",
          orientation="h",
          title="Top 10 Countries by Average Points",
          text="avg_points",
          color="avg_points",
          color_continuous_scale="viridis"
    )
    fig_points.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    # Layout tweaks
    fig_points.update_layout(
        xaxis_title="Average Points",
        yaxis_title=None,
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig_points, use_container_width=True)
    st.divider

    # Competitors vs Average Points (Scatter Plot)
    fig_scatter = px.scatter(
          df_country,
          x="competitors",
          y="avg_points",
          size="competitors",
          color="avg_points",
          hover_name="country",
          title="Competitors vs Average Points by Country"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.divider()

    country_query = """
        SELECT 
            c.country,
            COUNT(*) AS competitors,
            AVG(r.points) AS avg_points
        FROM Competitors c
        JOIN Competitor_Rankings r
            ON c.competitor_id = r.competitor_id
        GROUP BY c.country
        ORDER BY avg_points DESC
        LIMIT 10
    """
    country_df = run_query(country_query)


    # Country share by points 
    fig_donut = px.pie(
            country_df,
            names="country",
            values="avg_points",
            hole=0.4,  # makes it a donut chart
            title="Country Share of Average Points",
            color_discrete_sequence=px.colors.sequential.Viridis_r
    )

    st.plotly_chart(fig_donut, use_container_width=True)
