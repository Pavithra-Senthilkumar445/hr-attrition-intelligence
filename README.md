##🏢 IBM HR Attrition Intelligence Portal

   An end-to-end HR analytics platform built on **Databricks Medallion Architecture** with role-based access control, real-time data filtering, and interactive          visualizations using IBM HR Employee Attrition data.

##📌 Project Overview

This project analyses **why employees leave a company** using the IBM HR Analytics Employee Attrition dataset. It is built as a production-grade data pipeline with a live interactive dashboard — demonstrating both **Data Engineering** and **Data Analytics** skills.

The platform allows HR leaders and department managers to explore attrition patterns across departments, age groups, salary bands, and job satisfaction levels — all through a secure role-based login system.

##🎯 Business Problem

> *"We are losing too many employees every year. Can you tell us who is leaving, from which department, and why?"*

This dashboard answers:
- What is the overall employee attrition rate?
- Which department loses the most employees?
- Are younger employees leaving more than older ones?
- Do low-salary employees leave more often?
- Does job satisfaction affect who leaves?

---

## 🏗️ Architecture — Medallion Pipeline
Kaggle CSV (IBM HR Dataset)
            ↓
Unity Catalog Volume (Raw file storage)
            ↓
🥉 Bronze Layer  →  Raw Delta table (audit trail, metadata columns)
            ↓
🥈 Silver Layer  →  Cleaned + typed data (PySpark transformations)
            ↓
🥇 Gold Layer    →  Aggregated KPI tables (Spark SQL)
            ↓
Dash Application →  Role-based interactive dashboard
            ↓
GitHub →  Version controlled codebase

---

## 📊 Dataset

| Property       | Details                                      |
|----------------|----------------------------------------------|
| Source         | IBM HR Analytics Employee Attrition Dataset  |
| Platform       | Kaggle                                       |
| Rows           | 1,470 employees                              |
| Columns        | 35 attributes                                |
| Key Column     | Attrition (Yes = Left, No = Still working)   |
| Departments    | Sales, Human Resources, Research & Development|

---

## 🔐 Role-Based Access Control

| Role           | Email                  | Data Scope                        |
|----------------|------------------------|-----------------------------------|
| HR Admin       | admin@hrapp.com        | All departments, full metrics     |
| HR Manager     | hr@hrapp.com           | Human Resources department only   |
| Sales Manager  | sales@hrapp.com        | Sales department only             |
| R&D Manager    | rd@hrapp.com           | Research & Development only       |

Each role sees **different data** filtered from the Silver table in real time.

---

## 📈 Dashboard Features

- **KPI Cards** — Total Employees, Attrition Rate, Avg Monthly Income, Avg Tenure
- **4 Interactive Charts:**
  - Attrition Rate by Department (Horizontal Bar)
  - Attrition Rate by Age Group (Funnel Chart)
  - Attrition Count by Income Band (Donut Chart)
  - Job Satisfaction vs Attrition (Grouped Bar)
- **Filters** — Department pills + Age Group pills
- **Chart Popup** — Click any chart to expand full detail modal
- **Key Insights** — Auto-generated plain English insights from real data
- **Dark / Light Theme** — Toggle switch in navbar
- **Secure Login** — SHA-256 password hashing

---

## 🛠️ Tech Stack

| Category           | Technology                              |
|--------------------|-----------------------------------------|
| Cloud Platform     | Databricks (Community Edition)          |
| Data Storage       | Delta Lake + Unity Catalog              |
| Pipeline           | Medallion Architecture (Bronze→Silver→Gold) |
| Big Data           | Apache Spark + PySpark                  |
| SQL Engine         | Spark SQL                               |
| Secret Management  | Databricks Secret Scope                 |
| App Framework      | Dash + Plotly                           |
| Styling            | Dash Bootstrap Components               |
| Language           | Python 3.11                             |
| Version Control    | GitHub                                  |
| Deployment         | Databricks Apps                         |

---

## 📁 Project Structure

hr-attrition-intelligence/

│

├── app/

│   ├── app.py              # Main Dash application

│   ├── auth.py             # Login + password hashing

│   ├── data.py             # Data loading + role filtering

│   └── requirements.txt    # Python dependencies

│

├── ingestion/

│   └── 01_ingest_bronze.py # CSV → Bronze Delta table

│

├── processing/

│   ├── 02_silver_clean.py  # Bronze → Silver (PySpark)

│   └── 03_gold_kpis.py     # Silver → Gold (Spark SQL)

│

└── README.md

---

## 🔑 Key Technical Decisions

**Why Medallion Architecture?**
Bronze preserves raw data with audit trail. Silver enforces data quality and types. Gold pre-aggregates for fast dashboard queries. Each layer serves a specific purpose.

**Why Secret Scope instead of hardcoding?**
Databricks Secret Scope stores credentials in an encrypted vault. Code only references key names — never actual values. Safe to push to GitHub.

**Why Silver for role filtering instead of Gold?**
Gold tables are pre-aggregated — all roles would see the same numbers. Silver has 1,470 individual employee rows that can be filtered dynamically by department per role.

**Why Dash instead of SQL Dashboard?**
Dash supports role-based login, dynamic filtering, theme toggling, and chart popups — none of which are possible in a basic SQL dashboard.

---

## 📸 Screenshots

### Landing Page
<!-- Add screenshot here -->
![Landing Page](screenshots/landing.png)

### Login Page
<!-- Add screenshot here -->
![Login Page](screenshots/login.png)

### HR Admin Dashboard
<!-- Add screenshot here -->
![HR Admin Dashboard](screenshots/admin_dashboard.png)

### Sales Manager Dashboard
<!-- Add screenshot here -->
![Sales Manager Dashboard](screenshots/sales_dashboard.png)

### Dark Theme
<!-- Add screenshot here -->
![Dark Theme](screenshots/dark_theme.png)

### Chart Popup Modal
<!-- Add screenshot here -->
![Chart Popup](screenshots/chart_popup.png)

---

## 💡 Key Insights from Data

- **Sales department** has the highest attrition rate at **20.63%**
- **Younger employees (18-25)** leave the most at **35.77%**
- **Low salary employees ($1k-$3k/month)** have **28.61%** attrition rate
- **Low job satisfaction** employees leave at **22.84%** — highest satisfaction group

---

## 📜 Data Source

**IBM HR Analytics Employee Attrition & Performance Dataset**
Available on Kaggle — IBM HR Analytics Employee Attrition Dataset
This dataset was created by IBM data scientists for HR analytics research.

---

*Built with ❤️ on Databricks | IBM HR Analytics Employee Attrition Dataset*
