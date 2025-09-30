import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import plotly.express as px

# ----------------------------
# 1. Page Setup
# ----------------------------
st.set_page_config(page_title="OLA Ride Dashboard", layout="wide")
st.title("🚖 Ola Ride Insights")
st.sidebar.image("logo.png", width=500)

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
    query = "SELECT * FROM ola_rides;"   
    df = pd.read_sql(query, engine)
    # Convert Date column 
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()

# ----------------------------
# 4. Explore Data
# ----------------------------
st.write("### Preview of Data", df.head())

# Page selector
page = st.sidebar.radio("Choose Dashboard", ["Power BI Dashboard", "SQL Queries"])

# ----------------------------
# Power BI Dashboard
# ----------------------------
if page == "Power BI Dashboard":
    st.subheader("📈 Power BI Dashboard")
    # ----------------------------
    # 4a. Interactive Filters
    # ----------------------------
    st.sidebar.header("🔍 Filters")

    # Date filter
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

    # Vehicle type filter
    vehicle_filter = st.sidebar.multiselect(
        "Select Vehicle Type", options=df["Vehicle_Type"].unique()
    )

    # Payment method filter
    payment_filter = st.sidebar.multiselect(
        "Select Payment Method", options=df["Payment_Method"].unique()
    )

    # Booking status filter
    status_filter = st.sidebar.multiselect(
        "Select Booking Status", options=df["Booking_Status"].unique()
    )

    # Apply filters
    filtered_df = df.copy()

    if len(date_range) == 2:
        start_date, end_date = date_range
        # Convert to pandas Timestamps
        start_date = pd.to_datetime(start_date, errors="coerce")
        end_date = pd.to_datetime(end_date, errors="coerce")
        filtered_df = filtered_df[
            (filtered_df["Date"] >= start_date) &
            (filtered_df["Date"] <= end_date)
        ]

    if vehicle_filter:
        filtered_df = filtered_df[filtered_df["Vehicle_Type"].isin(vehicle_filter)]

    if payment_filter:
        filtered_df = filtered_df[filtered_df["Payment_Method"].isin(payment_filter)]

    if status_filter:
        filtered_df = filtered_df[filtered_df["Booking_Status"].isin(status_filter)]


    search_term = st.sidebar.text_input("Search by Customer ID or Driver ID")

    if search_term:
        filtered_df = filtered_df[
            filtered_df["Customer_ID"].astype(str).str.contains(search_term, case=False) |
            filtered_df["Driver_ID"].astype(str).str.contains(search_term, case=False)
        ]


    # KPI Metrics
    total_bookings = len(filtered_df)
    success_bookings = filtered_df[filtered_df["Booking_Status"]=="Success"].shape[0]
    cancelled_bookings = filtered_df[filtered_df["Booking_Status"].isin(["Canceled by Driver","Canceled by Customer"])].shape[0]
    cancellation_rate = round((cancelled_bookings/total_bookings)*100,2) if total_bookings>0 else 0
    total_revenue = filtered_df.loc[filtered_df["Booking_Status"]=="Success", "Booking_Value"].sum()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Bookings", f"{total_bookings:,}")
    col2.metric("Success Bookings", f"{success_bookings:,}")
    col3.metric("Cancelled Bookings", f"{cancelled_bookings:,}")
    col4.metric("Cancellation Rate", f"{cancellation_rate}%")
    col5.metric("Total Revenue", f"{total_revenue:,}")

    # ----------------------------
    # 5. Charts
    # ----------------------------

    # Booking Status Breakdown
    status_counts = filtered_df["Booking_Status"].value_counts().reset_index()
    status_counts.columns = ["Booking_Status", "Count"]
    fig_status = px.pie(status_counts, values="Count", names="Booking_Status", title="Booking Status Breakdown")
    st.plotly_chart(fig_status, use_container_width=True)

    # Rides over time
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
    rides_over_time = filtered_df.groupby("Date").size().reset_index(name="count")
    fig_time = px.line(rides_over_time, x="Date", y="count", title="Rides Over Time")
    st.plotly_chart(fig_time, use_container_width=True)
    # Revenue by Payment Method
    revenue_by_payment = (
        filtered_df.groupby("Payment_Method")["Booking_Value"]
        .sum()
        .reset_index()
        .sort_values(by="Booking_Value", ascending=False)
    )

    fig_payment = px.bar(
        revenue_by_payment,
        x="Payment_Method",
        y="Booking_Value",
        title="Revenue by Payment Method",
        labels={"Payment_Method": "Payment Method", "Booking_Value": "Total Revenue"},
        color="Payment_Method",
        text="Booking_Value"
    )

    fig_payment.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_payment.update_layout(yaxis_title="Total Revenue", xaxis_title="Payment Method")

    st.plotly_chart(fig_payment, use_container_width=True)

    # Driver cancellation reasons
    if "Canceled_Rides_by_Driver" in filtered_df.columns:
        driver_cancel_reasons = (
            filtered_df[filtered_df["Booking_Status"] == "Canceled by Driver"]
            .groupby("Canceled_Rides_by_Driver")
            .size()
            .reset_index(name="Count")
        )

    if not driver_cancel_reasons.empty:
        fig_driver_cancel = px.pie(
            driver_cancel_reasons,
            values="Count",
            names="Canceled_Rides_by_Driver",
            title="Driver Cancellation Reasons"
        )
        st.plotly_chart(fig_driver_cancel, use_container_width=True)

    # Customer cancellation reasons
    if "Canceled_Rides_by_Customer" in filtered_df.columns:
        customer_cancel_reasons = (
            filtered_df[filtered_df["Booking_Status"] == "Canceled by Customer"]
            .groupby("Canceled_Rides_by_Customer")
            .size()
            .reset_index(name="Count")
        )

    if not customer_cancel_reasons.empty:
        fig_customer_cancel = px.pie(
            customer_cancel_reasons,
            values="Count",
            names="Canceled_Rides_by_Customer",
            title="Customer Cancellation Reasons"
        )
        st.plotly_chart(fig_customer_cancel, use_container_width=True)

    # Ride distance distribution per day
    distance_per_day = (
        filtered_df.groupby("Date")["Ride_Distance"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    # Plot bar chart
    fig_distance = px.bar(
        distance_per_day,
        x="Date",
        y="Ride_Distance",
        title="Ride Distance Distribution per Day",
        labels={"Date": "Date", "Ride_Distance": "Total Ride Distance"},
        text="Ride_Distance"
    )

    fig_distance.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_distance.update_layout(xaxis_title="Date", yaxis_title="Total Ride Distance")

    st.plotly_chart(fig_distance, use_container_width=True)

    

    
# ----------------------------
# SQL Queries
# ----------------------------

elif page == "SQL Queries":
    st.subheader("🔎 Explore SQL Queries")

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




