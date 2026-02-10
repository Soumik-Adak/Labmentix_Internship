import requests
import mysql.connector

API_KEY = "MjBXAcvFJZqa0NrmHEduG6oDpeUf7h0Tzg8qOIuw"
URL = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Soumik@123_mysql",
    database="tennis"
)
cursor = conn.cursor()

response = requests.get(URL, params={"api_key": API_KEY})
data = response.json()

for comp in data["competitions"]:
    cat = comp["category"]

    cursor.execute("""
        INSERT IGNORE INTO Categories VALUES (%s, %s)
    """, (cat["id"], cat["name"]))

    cursor.execute("""
        INSERT IGNORE INTO Competitions VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        comp["id"],
        comp["name"],
        comp.get("parent_id"),
        comp.get("type"),
        comp.get("gender"),
        cat["id"]
    ))

conn.commit()
cursor.close()
conn.close()
print("Competitions data inserted successfully")