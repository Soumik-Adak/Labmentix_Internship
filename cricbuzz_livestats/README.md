# 🏏 Cricbuzz Live Stats  

![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white)  
![SQLite](https://img.shields.io/badge/Database-SQLite-07405E?logo=sqlite&logoColor=white)  
![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)  
![API](https://img.shields.io/badge/API-Cricbuzz%20(RapidAPI)-0096FF?logo=cricket&logoColor=white)  

A **Streamlit-based cricket analytics dashboard** that connects with **Cricbuzz API** and a **SQLite database** to provide:  
✅ Live Matches & Scores  
✅ Player & Team Stats  
✅ SQL Query Execution  
✅ Venue & Series Analysis  
✅ CRUD Operations  

---

## ✨ Features  
- 📡 **Live Matches** → Real-time updates on scores & match states  
- 🏆 **Top Players** → Most runs, wickets, centuries & more  
- 🗂 **SQL Queries** → Predefined cricket-related queries with results  
- ✏️ **CRUD Operations** → Manage records directly from the dashboard  
- 🏟 **Venues & Series** → Explore cricket grounds & tournaments  
- 🏠 **Home Page** → Project overview, tools used & navigation  

---

## 🛠️ Tech Stack  
| Layer        | Technology |
|--------------|------------|
| **Frontend** | Streamlit |
| **Backend**  | Python, SQLite |
| **Data**     | Cricbuzz API (via RapidAPI), JSON |
| **Libraries**| Pandas, Requests, SQLite3 |

---

## 📂 Project Structure  

<details>
<summary>Click to expand 📂</summary>
cricbuzz_livestats/
├── main.py # Streamlit entry point
├── utils.py # Database + API helpers
├── pages/ # Multi-page Streamlit structure
│ ├── home.py
│ ├── live_matches.py
│ ├── top_stats.py
│ ├── sql_queries.py
│ ├── crud_operations.py
├── data/ # JSON data files
│ ├── all_team_players.json
│ ├── all_venues.json
│ ├── recent_matches.json
│ ├── player_stats.json
├── cricket.db # SQLite database
└── Project_report.pdf # Full project report

