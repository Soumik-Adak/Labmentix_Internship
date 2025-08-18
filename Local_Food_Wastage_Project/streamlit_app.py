# Import libraries
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from PIL import Image
from datetime import datetime


# --------  database helpers ----------

DB_PATH = "local_food.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def run_query_df(query, params=None):
    conn = get_conn()
    try:
        df = pd.read_sql(query, conn, params=params)
    finally:
        conn.close()
    return df

def run_exec(query, params=None, many=False, data=None):
    conn = get_conn()
    cur = conn.cursor()
    try:
        if many and data is not None:
            cur.executemany(query, data)
        else:
            cur.execute(query, params)
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()

# -------- Streamlit App -----------

st.set_page_config(page_title="Local Food Wastage Management", layout="wide")


# Header for the dashboard
try:
    header_image = "food_wastage.png"
    st.image(Image.open(header_image), use_container_width = True)
except Exception:
    st.title("🍲 Local Food Wastage Management System")

st.sidebar.subheader("Select Analysis")


# Sidebar Navigation

menu = [
            "Dashboard",
            "Browse & Filter",
            "Queries",
            "Contacts",
            "CRUD" 
        ]

section = st.sidebar.radio("Navigate", menu)

# ----- SUMMARY METRICS -----
if section == "Dashboard":
    st.subheader("📊 Dashboard Overview")

    # Queries for counts
    providers_count = run_query_df("SELECT COUNT(*) FROM providers").iloc[0][0]
    receivers_count = run_query_df("SELECT COUNT(*) FROM receivers").iloc[0][0]
    food_count = run_query_df("SELECT COUNT(*) FROM food_listings").iloc[0][0]
    claims_count = run_query_df("SELECT COUNT(*) FROM claims").iloc[0][0]

    ## Inject CSS for KPI cards
    st.markdown(
        """
        <style>
        .kpi-card {
            background: linear-gradient(135deg, #f0f4ff, #d6e4ff);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.15);
            transition: 0.3s;
        }
        .kpi-card:hover {
            transform: scale(1.05);
            background: linear-gradient(135deg, #e8f0ff, #cddfff);
        }
        .kpi-value {
            font-size: 32px;
            font-weight: bold;
            color: #2E86C1;
        }
        .kpi-label {
            font-size: 16px;
            font-weight: 600;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display KPI cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{providers_count}</div><div class='kpi-label'>Total Providers</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{receivers_count}</div><div class='kpi-label'>Total Receivers</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{food_count}</div><div class='kpi-label'>Total Food Listings</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{claims_count}</div><div class='kpi-label'>Total Claims</div></div>", unsafe_allow_html=True)

# BROWSE & FILTER
elif section == "Browse & Filter":
    st.subheader("Filter Food Donations")
    # Filters (pulled live from DB)
    cities = run_query_df(
                            """
                                SELECT DISTINCT City
                                FROM providers 
                                ORDER BY City
                            """
                        )["City"].dropna().tolist()
    providers = run_query_df(
                                """
                                    SELECT DISTINCT Name 
                                    FROM providers 
                                    ORDER BY Name
                                """
                            )["Name"].tolist()
    food_types = run_query_df(
                                """
                                    SELECT DISTINCT Food_Type 
                                    FROM food_listings 
                                    ORDER BY Food_Type
                                """
                            )["Food_Type"].dropna().tolist()

    c1, c2, c3 = st.columns(3)

    with c1:
        sel_cities = st.multiselect("City", cities)
    with c2:
        sel_providers = st.multiselect("Provider", providers)
    with c3:
        sel_food_types = st.multiselect("Food Type", food_types)


# Base query
    base_sql =  """
                    SELECT 
                        f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date, 
                        f.Food_Type, f.Meal_Type, p.Name AS Provider, p.Type AS Provider_Type,
                        p.City, p.Address, p.Contact
                    FROM food_listings f
                    JOIN providers p ON f.Provider_ID = p.Provider_ID
                    WHERE 1=1
                """
    params = []
    if sel_cities:
        base_sql += " AND p.City IN (" + ",".join(["?"]*len(sel_cities)) + ")"
        params += sel_cities
    if sel_providers:
        base_sql += " AND p.Name IN (" + ",".join(["?"]*len(sel_providers)) + ")"
        params += sel_providers
    if sel_food_types:
        base_sql += " AND f.Food_Type IN (" + ",".join(["?"]*len(sel_food_types)) + ")"
        params += sel_food_types

    df = run_query_df(base_sql, params)

        # ---- CATEGORY CLEANING ----
    veg_exclude = ["Chicken", "Fish"]
    vegan_exclude = ["Dairy"]
    nonveg_exclude = ["Vegetable", "Bread"]

    def filter_food_type(df):
        return df[
            ((df["Food_Type"] == "Vegetarian") & (~df["Food_Name"].str.contains("|".join(veg_exclude)))) |
            ((df["Food_Type"] == "Vegan") & (~df["Food_Name"].str.contains("|".join(vegan_exclude)))) |
            ((df["Food_Type"] == "Non-Vegetarian") & (~df["Food_Name"].str.contains("|".join(nonveg_exclude))))
        ]

    if not df.empty:
        df = filter_food_type(df)


    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.markdown("#### Quantity by Food Type")
        fig = px.bar(df.groupby("Food_Type", as_index=False)["Quantity"].sum(), x="Food_Type", y="Quantity")
        st.plotly_chart(fig, use_container_width=True)


# QUERIES

elif section == "Queries":
    st.subheader("📚 Prebuilt Insights")


    query_menu = [
        "Providers and Receivers by City",
        "Top Food Provider Type",
        "Provider Information in Specific City",
        "Top Food Claim Receiver",
        "Total Food Quantity by Providers",
        "City with Most Listings",
        "Popular Food Types",
        "Food Claims by Item",
        "Top Successful Provider",
        "Percentage of Claim Status",
        "Average Food Claimed per Receiver",
        "Most Claimed Meal Type",
        "Total Quantity Donated by Provider"

    ]

    choice = st.selectbox("Select a query", query_menu)



    #1
    if choice == "Providers and Receivers by City":
        query = """
                    SELECT all_cities.City,
                        coalesce(p.total_providers, 0) as total_providers,
                            coalesce(r.total_receivers, 0) as total_receivers
                    FROM (
                        SELECT City 
                        FROM providers
                        UNION
                        SELECT City
                        FROM receivers
                    ) AS all_cities
                    LEFT JOIN (
                        SELECT City,
                                COUNT(*) AS total_providers
                        FROM providers
                        GROUP BY City
                    ) AS p ON all_cities.City = p.City
                    LEFT JOIN (
                        SELECT City,
                                COUNT(*) AS total_receivers
                        FROM receivers
                        GROUP BY City
                    ) AS r ON all_cities.City = r.City
                    ORDER BY all_cities.City;
                """
        df = run_query_df(query)
        st.dataframe(df, use_container_width=True)
        if not df.empty:
            fig = px.bar(df, x="City", y=["total_providers", "total_receivers"], barmode="group")
            st.plotly_chart(fig, use_container_width=True)

    #2
    elif choice == "Top Food Provider Type":
        query = """
                    select 
                            p.Type as Provider_Type, sum(f.Quantity) as total_quantity
                    from food_listings f
                    join providers p	
                    on f.Provider_ID = p.Provider_ID
                    group by p.Type
                    order by total_quantity desc
                    limit 1;
                """
        st.dataframe(run_query_df(query))

    #3
    elif choice == "Provider Information in Specific City":
        city = st.text_input("Enter City Name", "")
        if city:
            query = """
                        select
                            Name as provider_name,
                            Type as provider_type,
                            Address,
                            City,
                            Contact
                        from providers
                        where
                            City = "New Jessica";
                    """
            st.dataframe(run_query_df(query, (city,)))

    #4
    elif choice == "Top Food Claim Receiver":
        query = """
                    select
                        r.Name as receiver_name,
                        count(c.Claim_ID) as total_claims
                    from claims c
                    join receivers r 
                    on c.Receiver_ID = r.Receiver_ID
                    group by r.Name 
                    order by total_claims desc;
                """
        st.dataframe(run_query_df(query))

    #5
    elif choice == "Total Food Quantity by Providers":
        query = """
                    select
                        p.Name as provider_name,
                        sum(f.Quantity) as total_quantity
                    from food_listings f
                    join providers p 
                    on f.Provider_ID  = p.Provider_ID
                    group by p.Name 
                    order by total_quantity desc;
                """
        st.dataframe(run_query_df(query))

    #6
    elif choice == "City with Most Listings":
        query = """
                    select
                        p.City, count(*) as total_listings
                    from
                        food_listings f 
                    join
                        providers p 
                    on f.Provider_ID = p.Provider_ID
                    group by p.City
                    order by total_listings desc;
                """
        st.dataframe(run_query_df(query))

    #7
    elif choice == "Popular Food Types":
        query = """
                    select
                        Food_Type,
                        count(*) as total_listings
                    from 
                        food_listings
                    group by Food_Type
                    order by total_listings desc;
                """
        st.dataframe(run_query_df(query))

    #8
    elif choice == "Food Claims by Item":
        query = """
                    select 
                        f.Food_Name,
                        count(c.Claim_ID) as total_claims
                    from
                        claims c 
                    join 
                        food_listings f 
                    on c.Food_ID = f.Food_ID
                    group by f.Food_Name
                    order by total_claims desc;
                """
        st.dataframe(run_query_df(query))

    #9
    elif choice == "Top Successful Provider":
        query = """
                    select
                        p.Name as provider_name,
                        count(c.Claim_ID) as successful_claims
                    from
                        claims c 
                    join 
                        food_listings f 
                    on c.Food_ID = f.Food_ID
                    join
                        providers p 
                    on f.Provider_ID = p.Provider_ID
                    where 
                        c.Status = 'Completed'
                    group by p.Name 
                    order by successful_claims desc
                    limit 1;
                """
        st.dataframe(run_query_df(query))


    #10
    elif choice == "Percentage of Claim Status":
        query = """
                    select
                        Status,
                        count(*) as total_claims,
                        round(count(*) * 100.0 / (select count(*) from claims), 2) as percentage
                    from
                        claims
                    group by Status
                    order by percentage desc;
                """
        st.dataframe(run_query_df(query))

    #11
    elif choice == "Average Food Claimed per Receiver":
        query = """
                    select
                        r.Name as receiver_name,
                        round(avg(f.Quantity), 2) as avg_quantity_claimed
                    from
                        food_listings f 
                    join claims c 
                    on f.Food_ID = c.Food_ID
                    join receivers r 
                    on c.Receiver_ID = r.Receiver_ID
                    group by r.Name 
                    order by avg_quantity_claimed desc;
                """
        st.dataframe(run_query_df(query))

    #12
    elif choice == "Most Claimed Meal Type":
        query = """
                    select
                        f.Meal_Type,
                        count(c.Claim_ID) as total_claims
                    from
                        claims c 
                    join 
                        food_listings f 
                    on c.Food_ID = f.Food_ID
                    group by f.Meal_Type
                    order by total_claims desc
                    limit 1;
                """
        st.dataframe(run_query_df(query))


    #13
    elif choice == "Total Quantity Donated by Provider":
        query = """
                    select
                        p.Name as provider_name,
                        sum(f.Quantity) as total_quantity_donated
                    from 
                        food_listings f 
                    join 
                        providers p 
                    on f.Provider_ID = p.Provider_ID
                    group by p.Name 
                    order by total_quantity_donated desc;
                """
        st.dataframe(run_query_df(query))


# CONTACTS
elif section == "Contacts":
    st.subheader("📞 Contact Providers & Receivers")
    tab1, tab2 = st.tabs(["Providers", "Receivers"])

    with tab1:
        dfp = run_query_df(
                            """
                                SELECT Provider_ID, Name, Type, City, Contact 
                                FROM providers 
                                ORDER BY Name;
                            """
                        )
        st.dataframe(dfp, use_container_width=True)
        st.markdown("Tip: Click a contact to email/call if formatted as email/phone.")

        # Quick City filters
        city = st.selectbox("Filter by City (optional)", [""] + sorted(dfp["City"].dropna().unique().tolist()))
        if city:
            st.dataframe(dfp[dfp["City"] == city])

        # Build contact links
        def linkify(val):
            if pd.isna(val):
                return ""
            s = str(val)
            if "@" in s:
                return f"[Email]({f'mailto:{s}'})"
            digits = "".join([c for c in s if c.isdigit() or c == "+"])
            if len(digits) >= 8:
                return f"[Call]({f'tel:{digits}'})"
            return s

        if not dfp.empty:
            dfp2 = dfp.copy()
            dfp2["Contact Link"] = dfp2["Contact"].map(linkify)
            st.dataframe(dfp2[["Name","Type","City","Contact","Contact Link"]], use_container_width=True)

    with tab2:
        dfr = run_query_df(
                                """
                                    SELECT Receiver_ID, Name, Type, City, Contact 
                                    FROM receivers 
                                    ORDER BY Name;
                                """
                            )
        st.dataframe(dfr, use_container_width=True)
        city2 = st.selectbox("Filter by City (optional) ", [""] + sorted(dfr["City"].dropna().unique().tolist()))
        if city2:
            st.dataframe(dfr[dfr["City"] == city2])

# CRUD Operations
elif section == "CRUD":
    st.subheader("✍️ Create / Update / Delete Records")
    crud_tab = st.selectbox("Choose table", ["providers", "receivers", "food_listings", "claims"])

    # ----- CREATE -----
    st.markdown("#### ➕ Add New Record")
    if crud_tab == "providers":
        with st.form("add_provider"):
            name = st.text_input("Name")
            ptype = st.text_input("Type")
            addr = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Provider")
        if submitted:
            run_exec("INSERT INTO providers (Name, Type, Address, City, Contact) VALUES (%s,%s,%s,%s,%s)",
                     (name, ptype, addr, city, contact))
            st.success("Provider added.")

    elif crud_tab == "receivers":
        with st.form("add_receiver"):
            name = st.text_input("Name")
            rtype = st.text_input("Type")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Receiver")
        if submitted:
            run_exec("INSERT INTO receivers (Name, Type, City, Contact) VALUES (%s,%s,%s,%s)",
                     (name, rtype, city, contact))
            st.success("Receiver added.")

    elif crud_tab == "food_listings":
        with st.form("add_food"):
            fname = st.text_input("Food Name")
            qty = st.number_input("Quantity", min_value=0, step=1)
            exp = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider_ID", min_value=1, step=1)
            provider_type = st.text_input("Provider_Type")
            location = st.text_input("Location")
            ftype = st.text_input("Food_Type")
            mtype = st.text_input("Meal_Type")
            submitted = st.form_submit_button("Add Food Listing")
        if submitted:
            run_exec("""
                INSERT INTO food_listings
                (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (fname, qty, exp.strftime("%Y-%m-%d"), provider_id, provider_type, location, ftype, mtype))
            st.success("Food listing added.")

    else:  # claims
        with st.form("add_claim"):
            food_id = st.number_input("Food_ID", min_value=1, step=1)
            receiver_id = st.number_input("Receiver_ID", min_value=1, step=1)
            status = st.selectbox("Status", ["Pending","Completed","Canceled"])
            ts = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            submitted = st.form_submit_button("Add Claim")
        if submitted:
            run_exec("""
                INSERT INTO claims (Food_ID, Receiver_ID, Status, Timestamp)
                VALUES (%s,%s,%s,%s)
            """, (food_id, receiver_id, status, ts))
            st.success("Claim added.")

    st.divider()

    # ----- UPDATE -----
    st.markdown("#### ✏️ Update (simple examples)")
    if crud_tab == "providers":
        pid = st.number_input("Provider_ID to update", min_value=1, step=1)
        new_contact = st.text_input("New Contact")
        if st.button("Update Provider Contact"):
            run_exec("UPDATE providers SET Contact=%s WHERE Provider_ID=%s", (new_contact, pid))
            st.success("Provider contact updated.")

    if crud_tab == "food_listings":
        fid = st.number_input("Food_ID to update", min_value=1, step=1)
        new_qty = st.number_input("New Quantity", min_value=0, step=1)
        if st.button("Update Food Quantity"):
            run_exec("UPDATE food_listings SET Quantity=%s WHERE Food_ID=%s", (new_qty, fid))
            st.success("Food quantity updated.")

    st.divider()

    # ----- DELETE -----
    st.markdown("#### 🗑️ Delete")
    del_id = st.number_input(f"ID to delete from `{crud_tab}`", min_value=1, step=1, key="del_any")
    if st.button("Delete Row"):
        id_col = {"providers":"Provider_ID", "receivers":"Receiver_ID",
                  "food_listings":"Food_ID", "claims":"Claim_ID"}[crud_tab]
        run_exec(f"DELETE FROM {crud_tab} WHERE {id_col}=%s", (del_id,))
        st.success(f"Deleted from {crud_tab}.")


# # SQL RUNNER
# elif section == "SQL Runner":
#     st.subheader("🧪 Run Any SQL (READ-ONLY recommended)")
#     sql = st.text_area("Write a SELECT query", height=150, value="SELECT * FROM providers LIMIT 10;")
#     if st.button("Run"):
#         try:
#             df = run_query_df(sql)
#             st.dataframe(df, use_container_width=True)
#         except sqlite3.Error as e:
#             st.error(str(e))


