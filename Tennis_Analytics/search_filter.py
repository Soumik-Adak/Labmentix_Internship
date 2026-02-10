import streamlit as st
from db_connection import run_query

def show():
    st.title("🔍 Search & Filter Competitors")

    query = """
    SELECT c.name, c.country, r.ranking, r.points, r.movement, r.competitions_played
    FROM Competitors c
    JOIN Competitor_Rankings r 
      ON c.competitor_id = r.competitor_id
    """

    # Use run_query_df instead of pd.read_sql
    df = run_query(query)

    # Search by name
    search_name = st.text_input("Search Competitor by Name")
    if search_name:
        df = df[df["name"].str.contains(search_name, case=False)]

    # Filter by country
    country = st.selectbox("Select Country", ["All"] + sorted(df["country"].unique()))
    if country != "All":
        df = df[df["country"] == country]

    # Filter by rank range
    rank_range = st.slider(
        "Select Rank Range",
        int(df["ranking"].min()),
        int(df["ranking"].max()),
        (1, 50)
    )
    df = df[(df["ranking"] >= rank_range[0]) & (df["ranking"] <= rank_range[1])]

    # Filter by points threshold
    points_threshold = st.number_input("Minimum Points", min_value=0, value=1000)
    df = df[df["points"] >= points_threshold]

    st.dataframe(df, use_container_width=True)