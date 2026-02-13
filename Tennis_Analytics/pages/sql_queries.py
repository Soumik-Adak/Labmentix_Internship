import streamlit as st
import pandas as pd
from db_connection import run_query

def show():
    # ---------- Title Card ----------
    st.markdown("""
    <style>
    .title-card {
        background: linear-gradient(135deg, #283c86, #45a247);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
        color: white;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    .title-card h1 {
        font-size: 1.8rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title-card'><h1>📊 Explore SQL Queries</h1></div>", unsafe_allow_html=True)

    # ---------- Tabs for Categories ----------
    tab1, tab2, tab3 = st.tabs(["Categories & Competitions", "Complexes & Venues", "Competitors & Competitors_Rankings"])

    # --- Competitions Queries ---
    with tab1:
        comp_queries = {
            "All Competitions with Category name": """
                SELECT 
	                c.competition_name, 
                    cat.category_name
                FROM competitions c 
                JOIN categories cat 
	                ON c.category_id = cat.category_id;
            """,
            "Competitions per Category": """
                SELECT 
	                cat.category_name, 
                    COUNT(c.competition_id) AS competition_count
                FROM competitions c 
                JOIN categories cat 
	                ON c.category_id = cat.category_id
                GROUP BY cat.category_name
                ORDER BY competition_count DESC;
            """,
            "Doubles Competitions": """
                SELECT 
                    competition_name, 
                    type, 
                    gender
                FROM competitions
                WHERE type ='doubles';
            """,
            "Competitions in ITF Men": """
                SELECT 
	                c.competition_name, 
                    c.type, 
                    c.gender
                FROM competitions c 
                JOIN categories cat 
	                ON c.category_id = cat.category_id
                WHERE cat.category_name = 'ITF Men';
            """,
            "Parent & Sub-Competitions": """
                SELECT 
                    parent.competition_name AS parent_competition,
                    child.competition_name AS sub_competition
                FROM competitions child
                JOIN competitions parent
                    ON child.parent_id = parent.competition_id
                ORDER BY parent_competition;
            """,
            "Competition Type Distribution": """
                SELECT
	                cat.category_name,
                    c.type AS competition_type,
                    COUNT(*) AS competition_count
                FROM competitions c 
                JOIN categories cat 
	                ON c.category_id = cat.category_id
                GROUP BY
	                cat.category_name,
                    c.type
                ORDER BY
	                cat.category_name,
                    competition_count DESC;
            """,
            "Top-Level Competitions": """
                SELECT
	                competition_name, 
                    type,
                    gender
                FROM competitions
                WHERE parent_id IS NULL;
            """,

        }
        selected_comp = st.selectbox("Choose a Competitions or Categories Query:", list(comp_queries.keys()))
        if selected_comp:
            sql_comp = comp_queries[selected_comp]

            # Side-by-side layout
            col1, col2 = st.columns([1, 2])  
            
            with col1:
                st.markdown("#### 🧾 SQL Code")
                st.code(sql_comp, language="sql")

            with col2:
                st.markdown("#### 📊 Query Results")
                df_comp = run_query(sql_comp)
                st.dataframe(df_comp, use_container_width=True)

    # --- Venues Queries ---
    with tab2:
        venue_queries = {
            "Venues with Complex Names": """
                SELECT
	                v.venue_name,
                    c.complex_name
                FROM venues v 
                JOIN complexes c 
	                ON v.complex_id = c.complex_id;
            """,
            "Venues per Complex": """
                SELECT
	                c.complex_name,
                    COUNT(v.venue_id) AS venue_count
                FROM venues v 
                JOIN complexes c 
	                ON v.complex_id = c.complex_id
                GROUP BY c.complex_name
                ORDER BY venue_count DESC;
            """,
            "Venues in Chile": """
                SELECT 
	                v.venue_name,
                    v.city_name,
                    v.country_name,
                    v.country_code,
                    v.timezone,
                    c.complex_name
                FROM venues v 
                JOIN complexes c 
	                ON v.complex_id = c.complex_id
                WHERE country_name = "CHILE";
            """,
            "Venues & Timezones": """
                SELECT
	                venue_name,
                    timezone
                FROM venues;
            """,
            "Complexes with Multiple Venues": """
                SELECT
	                c.complex_name,
                    COUNT(v.venue_id) AS venue_count
                FROM venues v 
                JOIN complexes c 
	                ON v.complex_id = c.complex_id
                GROUP BY c.complex_name
                HAVING COUNT(v.venue_id)>1;
            """,
            "Venues by Country": """
                SELECT
	                country_name,
	                COUNT(venue_id) as venue_count
                FROM venues
                GROUP BY country_name
                ORDER BY venue_count DESC;
            """,
            "Venues in Nacional Complex": """
                SELECT
	                v.venue_name,
                    v.country_name,
                    v.city_name,
                    v.country_code,
                    v.timezone
                FROM venues v 
                JOIN complexes c 
	                ON v.complex_id = c.complex_id
                WHERE c.complex_name = 'Nacional';
            """,
            
        }
        selected_venue = st.selectbox("Choose a Venues or Complexes Query:", list(venue_queries.keys()))
        if selected_venue:
            sql_venue = venue_queries[selected_venue]
            # Side-by-side layout
            col1, col2 = st.columns([1, 2])  

            with col1:
                st.markdown("#### 🧾 SQL Code")
                st.code(sql_venue, language="sql")

            with col2:
                st.markdown("#### 📊 Query Results")
                df_venue = run_query(sql_venue)
                st.dataframe(df_venue, use_container_width=True)

    # --- Competitors Queries ---
    with tab3:
        competitor_queries = {
            "Competitors with Rank & Points": """
                SELECT
	                c.name,
                    r.ranking,
                    r.points
                FROM competitors c 
                JOIN competitor_rankings r 
	                ON c.competitor_id = r.competitor_id
                ORDER BY r.ranking ASC;
            """,
            "Top 5 Competitors": """
                SELECT
	                c.name,
                    r.ranking,
                    r.points
                FROM competitors c 
                JOIN competitor_rankings r 
	                ON c.competitor_id = r.competitor_id
                WHERE r.ranking <= 5
                ORDER BY r.ranking ASC;
            """,
            "Stable Rank Competitors": """
                SELECT
	                c.name,
                    r.ranking,
                    r.movement
                FROM competitors c 
                JOIN competitor_rankings r 
	                ON c.competitor_id = r.competitor_id
                WHERE r.movement = 0;
            """,
            "Total Points by Country (Croatia)": """
                SELECT
	                c.country,
                    SUM(r.points) AS total_points
                FROM competitors c 
                JOIN competitor_rankings r
	                ON c.competitor_id = r.competitor_id
                WHERE c.country = 'Croatia'
                GROUP BY c.country;
            """,
            "Competitors per Country": """
                SELECT
	                country,
	                COUNT(competitor_id) AS competitor_count
                FROM competitors
                GROUP BY country
                ORDER BY competitor_count DESC;
            """,
            "Highest Points Competitors in this Week": """
                SELECT
	                c.name,
                    r.ranking,
                    r.points
                FROM competitors c 
                JOIN competitor_rankings r 
	                ON c.competitor_id = r.competitor_id
                ORDER BY r.points DESC
                LIMIT 1;
            """,
            
        }
        selected_competitor = st.selectbox("Choose a Competitors or Competitors Rankings Query:", list(competitor_queries.keys()))
        if selected_competitor:
            sql_competitor = competitor_queries[selected_competitor]
            # Side-by-side layout
            col1, col2 = st.columns([1, 2])  

            with col1:
                st.markdown("#### 🧾 SQL Code")
                st.code(sql_competitor, language="sql")

            with col2:
                st.markdown("#### 📊 Query Results")
                df_competitor = run_query(sql_competitor)
                st.dataframe(df_competitor, use_container_width=True)