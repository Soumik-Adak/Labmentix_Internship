import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ----------------------------
# 1. Page Setup
# ----------------------------
st.set_page_config(page_title="OLA Ride Dashboard", layout="wide")
st.title("🚖 Ola Ride Analytics (MySQL)")

# ----------------------------
# 2. Database Connection
# ----------------------------
# Replace with your MySQL credentials
HOST = "localhost:3306"      # or server IP
USER = "root"
PASSWORD = "Soumik@123_mysql"
DATABASE = "OLA_db"


# Encode the password safely
encoded_password = quote_plus(PASSWORD)

# Create connection string
engine = create_engine(f"mysql+pymysql://{USER}:{encoded_password}@{HOST}/{DATABASE}")

# ----------------------------
# 3. Query Data
# ----------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM ola_rides;"   # table name must match MySQL
    return pd.read_sql(query, engine)

df = load_data()

# ----------------------------
# 4. Explore Data
# ----------------------------
st.write("### Preview of Data", df.head())



# KPI Metrics
total_bookings = len(df)
success_bookings = df[df["Booking_Status"]=="Success"].shape[0]
cancelled_bookings = df[df["Booking_Status"].isin(["Canceled by Driver","Canceled by Customer"])].shape[0]
cancellation_rate = round((cancelled_bookings/total_bookings)*100,2) if total_bookings>0 else 0
total_revenue = df.loc[df["Booking_Status"]=="Success", "Booking_Value"].sum()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Bookings", f"{total_bookings:,}")
col2.metric("Success Bookings", f"{success_bookings:,}")
col3.metric("Cancelled Bookings", f"{cancelled_bookings:,}")
col4.metric("Cancellation Rate", f"{cancellation_rate}%")
col5.metric("Total Revenue", f"{total_revenue:,}")

# ----------------------------
# 5. Charts
# ----------------------------
import plotly.express as px

# Booking Status Breakdown
status_counts = df["Booking_Status"].value_counts().reset_index()
status_counts.columns = ["Booking_Status", "Count"]
fig_status = px.pie(status_counts, values="Count", names="Booking_Status", title="Booking Status Breakdown")
st.plotly_chart(fig_status, use_container_width=True)

# Rides over time
df["Date"] = pd.to_datetime(df["Date"])
rides_over_time = df.groupby("Date").size().reset_index(name="count")
fig_time = px.line(rides_over_time, x="Date", y="count", title="Rides Over Time")
st.plotly_chart(fig_time, use_container_width=True)


# ----------------------------
# SQL Queries
# ----------------------------

st.subheader(" Explore SQL Queries")

queries = {
    "Total Successful Bookings": "select * from ola_rides where Booking_Status = 'Success';",
    "Average Ride Distance by Vehicle Type": "select Vehicle_Type, round(avg(Ride_Distance),2) as avg_ride_distance from ola_rides group by Vehicle_Type order by avg_ride_distance desc;",
    "Total Cancelled Rides by Customers": "select count(*) as total_rides from ola_rides where Booking_status = 'Canceled by Customer';",
    "Top 5 Customers with Highest No of Rides": "select Customer_ID, count(*) as total_rides from ola_rides group by Customer_ID order by total_rides desc limit 5;",
    "Total Rides Cancelled by Drivers due to Personal and Car-related Issues": "select count(*) as total_rides from ola_rides where Canceled_Rides_by_Driver = 'Personal & Car related issue';",
    "Maximum and Minimum Driver Ratings for Prime Sedan": "select Vehicle_Type, round(max(Driver_Ratings),2) as max_ratings, round(min(Driver_Ratings),2) as min_ratings from ola_rides where Vehicle_Type = 'Prime Sedan';",
    "Rides where Payment Method was UPI": "select Payment_Method, count(*) as total_rides from ola_rides where Payment_Method = 'UPI';",
    "Average Customer Rating by Vehicle Type": "select Vehicle_Type, round(avg(Customer_Rating),2) as avg_rating from ola_rides group by Vehicle_Type order by avg_rating desc;",
    "Successfull Rides Booking Value": "select Booking_Status, sum(Booking_Value) as total_booking_value from ola_rides where Booking_Status = 'Success';",
    "Incomplete Rides Reason": "select * from ola_rides where Incomplete_Rides = 'Yes' and Incomplete_Rides_Reason <> 'Unknown';",
}
selected_query = st.selectbox("Choose a query:", list(queries.keys()))
if selected_query:
    sql = queries[selected_query]
    st.code(sql, language="sql")  
    df_sql = pd.read_sql(sql, engine)
    st.write(f"### Results: {selected_query}", df_sql.head())


# View sections
st.subheader("Explore Views Queries")

# 1. Get all views from MySQL
views_query = f"""
SELECT table_name AS view_name
FROM information_schema.views
WHERE table_schema = '{DATABASE}';
"""
views_df = pd.read_sql(views_query, engine)


# 3. Dropdown
selected_view = st.selectbox("Choose a view:", views_df["view_name"])

def get_view_definition(view_name):
    query = f"SHOW CREATE VIEW {view_name};"
    df_view = pd.read_sql(query, engine)
    return df_view["Create View"].iloc[0]

if selected_view:
    view_sql = get_view_definition(selected_view)
    #st.code(view_sql, language="sql")   # show the SQL query


df_view_data = pd.read_sql(f"SELECT * FROM {selected_view};", engine)
st.write(f"### Preview of `{selected_view}`", df_view_data)


