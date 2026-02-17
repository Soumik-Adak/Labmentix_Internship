# 🎾 Tennis Analytics Intelligence Platform  

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)  
![MySQL](https://img.shields.io/badge/Database-MySQL-07405E?logo=mysql&logoColor=white)  
![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)  
![API](https://img.shields.io/badge/Data-API%20Integration-0096FF?logo=fastapi&logoColor=white)  
![Analytics](https://img.shields.io/badge/Focus-Data%20Analytics-8A2BE2)

---

## 📌 Executive Summary

The **Tennis Analytics Intelligence Platform** is a full-stack data analytics solution that transforms raw tennis data from an external API into structured, business-ready insights through a scalable database architecture and an interactive dashboard.

This project demonstrates a complete analytics workflow:

> **API → Data Engineering → Relational Modeling → SQL Analytics → Interactive Dashboard → Business Insights**

It simulates a real-world sports analytics use case where stakeholders require structured performance intelligence and competitive insights.

---

# 💼 Business Problem

Raw sports data is:

- Highly nested (JSON format)
- Inconsistent across endpoints
- Not directly usable for analysis
- Difficult to convert into strategic insights

Stakeholders such as:

- Sports Analysts  
- Tournament Organizers  
- Performance Strategists  
- Talent Scouts  

need answers to questions like:

- Which countries dominate rankings?
- Does higher participation mean stronger performance?
- Which players are rapidly improving?
- How competitive is the ranking distribution?

This project bridges the gap between raw data and decision-making insights.

---

# 🚀 Business Outcomes & Impact

## 📊 1. Country Performance Intelligence
- Identified mismatch between participation volume and actual performance strength  
- Highlighted high-efficiency countries (fewer players, higher average points)  
- Enabled comparative performance benchmarking  

## 🏆 2. Competitive Landscape Analysis
- Revealed ranking concentration among elite players  
- Identified dominance clusters  
- Detected performance gaps between tiers  

## 📈 3. Momentum Tracking
- Ranking movement analysis detects rising players  
- Helps identify breakout talent early  

## 🧠 4. Data-Driven Decision Support
- KPI visualization simplifies complex ranking structures  
- Drill-down capability enhances exploratory analysis  
- SQL views provide reusable analytical logic  

## ⚙️ 5. Scalable Data Architecture
- Normalized relational schema  
- Hierarchical competition modeling  
- Modular SQL view layer for abstraction  
- Clean separation between raw and analytical layers  

---

# 🏗️ System Architecture

```
SportRadar API
        ↓
Python ETL (Requests + Pandas)
        ↓
MySQL Relational Database
        ↓
SQL Views (Analytics Layer)
        ↓
Streamlit Interactive Dashboard
        ↓
Business Insights
```

---

# 🧱 Tech Stack

| Layer | Technology |
|--------|------------|
| Data Extraction | Python, Requests |
| Data Processing | Pandas |
| Database | MySQL |
| Query Layer | Advanced SQL + Views |
| Visualization | Streamlit |
| Charts | Plotly |
| Architecture | Normalized Relational Schema |

---

# 🗄️ Database Design Highlights

- Fully normalized schema (3NF principles)
- Separation of static (Competitors) and dynamic (Rankings) entities
- Parent–child hierarchy using self-joins
- Foreign key integrity enforcement
- Analytical SQL views for dashboard queries
- Optimized joins for performance

---

# 📊 Dashboard Modules

## 🏠 Homepage
- Global KPIs
- Summary metrics
- Overview insights

## 👤 Competitor Analysis
- Player drill-down
- Ranking breakdown
- Country mapping
- Performance comparison

## 🌍 Country Intelligence
- Competitor distribution
- Average points by country
- Efficiency vs volume comparison
- Scatter-based performance clustering

## 🏆 Leaderboards
- Medal-style Top 3 display
- Top N ranking visualization
- Ranking movement tracking
- Country dominance insights

## 🔍 Search & Filter Engine
Dynamic filtering by:
- Player name
- Country
- Ranking range
- Points range
- Movement indicator

## 🧾 SQL Query Explorer
- Pre-built analytical queries
- Learning-oriented SQL structure
- Live result preview

---

# 📈 Key Analytical Findings

- Ranking points distribution is highly skewed
- Elite players significantly influence averages
- Participation depth does not equal performance strength
- Country efficiency varies widely
- High participation does not guarantee top ranking
- Competitive dominance is concentrated within small clusters

---

# ⚠️ Technical Challenges & Solutions

| Challenge | Solution |
|------------|-----------|
| Nested API JSON | Structured parsing with safe extraction |
| Missing fields | Null-safe handling |
| Duplicate records | Primary key enforcement |
| SQL keyword conflicts | Aliasing strategy |
| Join inconsistencies | Foreign key validation |
| Query repetition | SQL view abstraction |
| UI clutter | Balanced KPI & visualization design |

---

# 📂 Project Structure

```
tennis_analytics/
├── app.py
├── db_connection.py
├── ranking_api.py
├── pages/
│   ├── home.py
│   ├── competitor.py
│   ├── country.py
│   ├── leaderboards.py
│   ├── search_filter.py
│   ├── sql_explorer.py
├── sql/
│   ├── competition_query.sql
│   ├── competitors_query.sql
│   ├── venues_query.sql
├── requirements.txt
└── README.md
```

---

# 🛠️ Installation & Setup

## 1️⃣ Clone Repository
```bash
git clone <your-repo-url>
cd tennis-analytics-dashboard
```

## 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## 3️⃣ Run Application
```bash
streamlit run app.py
```

---

# 🎯 Skills Demonstrated

✔ API Integration & ETL Design  
✔ Advanced SQL & Query Optimization  
✔ Relational Database Modeling  
✔ Dashboard UI/UX Design  
✔ Business Insight Generation  
✔ Data Cleaning & Validation  
✔ Analytical Thinking  

---

# 💡 Why This Project Stands Out

Unlike basic dashboard projects, this solution:

- Builds the full data pipeline from scratch  
- Uses relational modeling best practices  
- Separates raw, transformed, and analytical layers  
- Focuses on business impact, not just visuals  
- Demonstrates real-world data engineering capability  

This reflects skills required for:

- Data Analyst  
- Business Intelligence Analyst  
- Junior Data Engineer  
- Analytics Consultant  

---

# 👨‍💻 Author

**Soumik Adak**  
M.Sc. in IT(Data Science)  
Skilled in Python, SQL, Power BI & Data Engineering  
  

---

⭐ If you found this project interesting, feel free to explore, fork, or connect!
