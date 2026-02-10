import requests
import mysql.connector

API_KEY = "MjBXAcvFJZqa0NrmHEduG6oDpeUf7h0Tzg8qOIuw"
URL = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Soumik@123_mysql",
    database="tennis"
)
cursor = conn.cursor()

data = requests.get(URL, params={"api_key": API_KEY}).json()

for item in data["rankings"][0]["competitor_rankings"]:
    comp = item["competitor"]

    # ---------- INSERT COMPETITOR ----------
    cursor.execute("""
        INSERT IGNORE INTO Competitors
        (competitor_id, name, country, country_code, abbreviation)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        comp.get("id"),
        comp.get("name"),
        comp.get("country"),
        comp.get("country_code"),
        comp.get("abbreviation")
    ))

    # ---------- INSERT RANKING ----------
    cursor.execute("""
        INSERT INTO Competitor_Rankings
        (ranking, movement, points, competitions_played, competitor_id)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        item.get("rank"),   
        item.get("movement"),
        item.get("points"),
        item.get("competitions_played"),
        comp.get("id")
    ))

conn.commit()
cursor.close()
conn.close()

print("Rankings inserted successfully")
