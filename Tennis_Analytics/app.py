import streamlit as st
from pages import home, search_filter, compititor_details, country_analysis, leaderboards, sql_queries

st.set_page_config(
    page_title="Tennis Analytics",
    layout="wide",
    page_icon="🎾"
)

# ---------------- Initialize Session State ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"


# ---------------- Custom Navbar Styling ----------------
st.markdown("""
<style>
.navbar {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
}
.nav-item {
    background: #203a43;
    color: white;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    text-align: center;
    cursor: pointer;
    transition: 0.3s;
    font-weight: 500;
}
.nav-item:hover {
    background: #2c5364;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Navbar with Buttons ----------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🏠 Homepage"):
        st.session_state.page = "Home"
with col2:
    if st.button("🔍 Search"):
        st.session_state.page = "Search & Filter"
with col3:
    if st.button("👥 Competitors"):
        st.session_state.page = "Competitor Details"
with col4:
    if st.button("🌍 Country Analysis"):
        st.session_state.page = "Country Analysis"
with col5:
    if st.button("📊 Leaderboards"):
        st.session_state.page = "Leaderboards"
with col6:
    if st.button("📝 SQL Queries"):
        st.session_state.page = "SQL Queries"






# ---------------- ROUTING ----------------
if st.session_state.page in ["Home"]:
    home.show()
elif st.session_state.page == "Search & Filter":
    search_filter.show()
elif st.session_state.page == "Competitor Details":
    compititor_details.show()
elif st.session_state.page == "Country Analysis":
    country_analysis.show()
elif st.session_state.page == "Leaderboards":
    leaderboards.show()
elif st.session_state.page == "SQL Queries":
    sql_queries.show()