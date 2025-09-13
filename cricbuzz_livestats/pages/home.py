import streamlit as st

def show():
    # Page setup
    st.set_page_config(page_title="🏏 Cricbuzz Dashboard", layout="wide")

    # Hero Section
    st.title("🏏 Cricbuzz Live Dashboard")
    st.markdown(
        """
        ### Welcome to the Cricbuzz Dashboard!  
        Stay updated with **Live Matches**, explore **Top Players**, run **SQL Queries**,  
        and manage data with **CRUD Operations** – all in one place.
        """
    )

    st.divider()

    # Dashboard Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Live Matches", "⚡ Real-time")
        st.caption("Follow ball-by-ball live scores")

    with col2:
        st.metric("Top Players", "🌟 Stats")
        st.caption("Track batting & bowling leaders")

    with col3:
        st.metric("SQL Queries", "📊 Insights")
        st.caption("Run advanced cricket queries")

    with col4:
        st.metric("CRUD Ops", "⚙️ Manage")
        st.caption("Insert, update & delete records")

    st.divider()

    # Call-to-action Section
    st.subheader("🚀 Get Started")
    st.info("👉 Use the **left sidebar** to navigate between pages.", icon="🧭")

    # Footer
    st.markdown("---")
    st.markdown(
        "<center>📌 Built with ❤️ using Streamlit & Cricbuzz API</center>",
        unsafe_allow_html=True
    )


