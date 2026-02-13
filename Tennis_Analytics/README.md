# 🎾 Tennis Analytics Dashboard  

![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white)  
![SQLite](https://img.shields.io/badge/Database-MySQL-07405E?logo=sqlite&logoColor=white)  
![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)  
![API](https://img.shields.io/badge/API-Tennis%20(SportsRaderAPI)-0096FF?logo=cricket&logoColor=white)  

An end-to-end data analytics project that transforms raw tennis data from the SportRadar API into a structured MySQL database and an interactive Streamlit dashboard. This project demonstrates real-world data engineering, SQL analytics, and visualization workflow — from extraction to insight.

---

## 🚀 Project Overview

The Tennis Analytics Dashboard is built to collect, structure, analyze, and visualize professional tennis competition and ranking data. Raw JSON data is fetched from an external API, cleaned and normalized into relational tables, and then explored through an interactive multi-page dashboard.

The goal is not just visualization — but building a **complete analytics pipeline**:  
**API → Data Cleaning → Schema Design → SQL Analytics → Interactive Dashboard → Insights**

---

## 🧱 Tech Stack

- **Python** — Data extraction & processing  
- **MySQL** — Relational database & analytics queries  
- **SQL Views** — Reusable analytical layer  
- **Streamlit** — Interactive dashboard UI  
- **Pandas** — Data handling  
- **Plotly** — Interactive charts  
- **Requests** — API integration  

---

## 📂 Project Features

### ✅ Data Engineering
- API data extraction scripts  
- JSON parsing with null-safe handling  
- Clean field mapping  
- Deduplication using keys  
- Normalized relational schema  
- Foreign key relationships  

### ✅ Database Design
- Competitors table  
- Rankings table  
- Competitions hierarchy  
- Categories mapping  
- Complexes & venues structure  
- Analytical SQL views for dashboard queries  

### ✅ Dashboard Modules
- 🏠 **Homepage** → KPIs, overview metrics  
- 👤 **Competitor Details** → Player drill-down view  
- 🌍 **Country Analysis** → Competitor count, avg points, scatter plots, share distribution  
- 🏆 **Leaderboards** → Medal-style Top 3, Top N chart, rising players, country strength  
- 🔍 **Search & Filter** → Search by name, country, ranking range, points, movement  
- 🧾 **SQL Query Explorer** → Prebuilt queries, results preview, learning support  

---

## 🗄️ Database Schema Highlights
- Fully normalized relational design  
- One-to-many and self-join relationships  
- Ranking separated from competitor identity  
- Competition parent–child hierarchy  
- Lookup tables for categories  
- Views created for dashboard consumption  

---
## 📂 Project Structure  

tennis_analytics/
├── app.py # Streamlit entry point
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

---

## 📊 Key Analytical Insights
- Ranking points distribution is highly skewed  
- Country depth ≠ country performance strength  
- Few elite players heavily influence averages  
- Ranking movement is a strong momentum indicator  
- Participation volume does not guarantee high points  
- Performance efficiency varies widely by country  

---

## ⚠️ Challenges Solved
- Inconsistent API field structures  
- Missing nested JSON values  
- SQL reserved keyword conflicts  
- Duplicate record handling  
- Join row count mismatches  
- View vs query architecture refactor  
- UI readability vs chart density balance


---

## 🛠️ Installation & Setup

### 1️⃣ Clone Project
```bash
git clone <your-repo-url>
cd tennis-analytics-dashboard



