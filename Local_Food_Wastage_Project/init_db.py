import sqlite3

DB_PATH = "E:/FOOD_PROJECT_CODE/local_food.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Drop tables if exist (for clean reloads)
cur.execute("DROP TABLE IF EXISTS providers;")
cur.execute("DROP TABLE IF EXISTS receivers;")
cur.execute("DROP TABLE IF EXISTS food_listings;")
cur.execute("DROP TABLE IF EXISTS claims;")

# Create tables
cur.execute("""
CREATE TABLE providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
);
""")

cur.execute("""
CREATE TABLE receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    City TEXT,
    Contact TEXT
);
""")

cur.execute("""
CREATE TABLE food_listings (
    Food_ID INTEGER PRIMARY KEY,
    Food_Name TEXT,
    Quantity INTEGER,
    Expiry_Date DATE,
    Provider_ID INTEGER,
    Provider_Type TEXT,
    Location TEXT,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
);
""")

cur.execute("""
CREATE TABLE claims (
    Claim_ID INTEGER PRIMARY KEY,
    Food_ID INTEGER,
    Receiver_ID INTEGER,
    Status TEXT,
    Timestamp DATETIME,
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
);
""")

conn.commit()
conn.close()

print("Tables created successfully!")

import pandas as pd

# Load CSV files
providers = pd.read_csv("C:/Users/soumi/food_sql_project/data/providers.csv")
receivers = pd.read_csv("C:/Users/soumi/food_sql_project/data/receivers.csv")
food_listings = pd.read_csv("C:/Users/soumi/food_sql_project/data/food_listings.csv")
claims = pd.read_csv("C:/Users/soumi/food_sql_project/data/claims.csv")

# Save into SQLite
conn = sqlite3.connect(DB_PATH)

providers.to_sql("providers", conn, if_exists="append", index=False)
receivers.to_sql("receivers", conn, if_exists="append", index=False)
food_listings.to_sql("food_listings", conn, if_exists="append", index=False)
food_listings["Expiry_Date"] = pd.to_datetime(food_listings["Expiry_Date"], errors="coerce").dt.date
claims.to_sql("claims", conn, if_exists="append", index=False)
claims["Timestamp"] = pd.to_datetime(claims["Timestamp"], errors="coerce")

conn.close()

print("CSVs loaded into SQLite successfully!")

conn = sqlite3.connect(DB_PATH)
print(pd.read_sql("SELECT * FROM providers LIMIT 10;", conn))
#print(pd.read_sql("SELECT * FROM clai LIMIT 5;", conn))
#print(pd.read_sql("SELECT * FROM food_listings LIMIT 5;", conn))
conn.close()
