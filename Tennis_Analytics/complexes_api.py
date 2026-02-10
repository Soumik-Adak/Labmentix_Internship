import requests
import mysql.connector

API_KEY = "MjBXAcvFJZqa0NrmHEduG6oDpeUf7h0Tzg8qOIuw"
URL = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Soumik@123_mysql",
    database="tennis"
)
cursor = conn.cursor()

data = requests.get(URL, params={"api_key": API_KEY}).json()

# ---------------- INSERT DATA ----------------
for complex_ in data.get("complexes", []):

    complex_id = complex_.get("id")
    complex_name = complex_.get("name")

    # ---- insert complex ----
    cursor.execute("""
        INSERT IGNORE INTO Complexes
        (complex_id, complex_name)
        VALUES (%s, %s)
    """, (complex_id, complex_name))

    # ---- insert venues ----
    for venue in complex_.get("venues", []):

        cursor.execute("""
            INSERT IGNORE INTO Venues
            (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            venue.get("id"),
            venue.get("name"),
            venue.get("city_name"),      
            venue.get("country_name"),   
            venue.get("country_code"),   
            venue.get("timezone"),
            complex_id
        ))

# ---------------- COMMIT ----------------
conn.commit()
cursor.close()
conn.close()

print("Complexes and Venues inserted successfully")
