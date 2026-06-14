# 🏢 IBM HR Attrition Intelligence Portal

**End-to-end HR Analytics platform built on Databricks Medallion Architecture using Delta Table, PySpark, Spark SQL, and Dash with role-based access control.**

---

## 📌 Project Overview

This project analyzes employee attrition using the IBM HR Analytics Employee Attrition dataset. It is designed as an enterprise-style data platform that demonstrates both Data Engineering and Data Analytics concepts through a complete Bronze → Silver → Gold pipeline and an interactive dashboard.

The platform enables HR leaders and department managers to explore workforce trends, attrition patterns, salary distributions, age-group behavior, and job satisfaction metrics through secure role-based access.

---

## 🎯 Business Problem

> *"We are losing too many employees every year. Can you tell us who is leaving, from which department, and why?"*

This solution helps answer:

* What is the overall employee attrition rate?
* Which department experiences the highest attrition?
* Are younger employees leaving more frequently than older employees?
* Does salary influence employee attrition?
* How does job satisfaction impact employee retention?

---

## 🏗️ Architecture — Medallion Pipeline

```text
Kaggle CSV (IBM HR Dataset)
            ↓
Unity Catalog Volume (Raw File Storage)
            ↓
🥉 Bronze Layer
Raw Delta Table + Audit Metadata
            ↓
🥈 Silver Layer
Cleaned & Standardized Employee Data
            ↓
🥇 Gold Layer
Business KPI & Aggregated Analytics Tables
            ↓
Dash Application
Role-Based Interactive Dashboard
            ↓
GitHub
Version Controlled Repository
```

---

## 📊 Dataset

| Property    | Details                                        |
| ----------- | ---------------------------------------------- |
| Source      | IBM HR Analytics Employee Attrition Dataset    |
| Platform    | Kaggle                                         |
| Rows        | 1,470 Employees                                |
| Columns     | 35 Attributes                                  |
| Key Column  | Attrition (Yes = Left, No = Active Employee)   |
| Departments | Sales, Human Resources, Research & Development |

---

## 🔐 Role-Based Access Control

| Role          | Email                                     | Data Scope                  |
| ------------- | ----------------------------------------- | --------------------------- |
| HR Admin      | [admin@hrapp.com](mailto:admin@hrapp.com) | All Departments             |
| HR Manager    | [hr@hrapp.com](mailto:hr@hrapp.com)       | Human Resources Only        |
| Sales Manager | [sales@hrapp.com](mailto:sales@hrapp.com) | Sales Only                  |
| R&D Manager   | [rd@hrapp.com](mailto:rd@hrapp.com)       | Research & Development Only |

Each user sees only the data relevant to their assigned department through dynamic filtering and access control logic.

---

## 📈 Dashboard Features

### KPI Metrics

* Total Employees
* Overall Attrition Rate
* Average Monthly Income
* Average Employee Tenure

### Interactive Visualizations

* Attrition Rate by Department (Horizontal Bar Chart)
* Attrition Rate by Age Group (Funnel Chart)
* Attrition Count by Income Band (Donut Chart)
* Job Satisfaction vs Attrition (Grouped Bar Chart)

### User Experience

* Department Filters
* Age Group Filters
* Expandable Chart Modal
* Dynamic Business Insights
* Light / Dark Theme Toggle
* Secure Role-Based Login

---

## 🚀 Project Outcomes

* Implemented a complete Medallion Architecture using Delta Table.
* Built Bronze, Silver, and Gold data layers using PySpark and Spark SQL.
* Developed a role-based dashboard for department-level analytics.
* Created interactive visualizations for workforce and attrition analysis.
* Enabled HR stakeholders to identify trends across age, salary, department, and satisfaction levels.
* Demonstrated an end-to-end Data Engineering and Analytics workflow using Databricks and Dash.

---

## 🛠️ Tech Stack

| Category              | Technology                                      |
| --------------------- | ----------------------------------------------- |
| Cloud Platform        | Databricks Community Edition                    |
| Data Storage          | Delta Table                                      |
| Governance            | Unity Catalog                                   |
| Pipeline Architecture | Medallion Architecture (Bronze → Silver → Gold) |
| Processing Engine     | Apache Spark                                    |
| Programming Language  | Python 3.11                                     |
| Data Transformation   | PySpark                                         |
| SQL Engine            | Spark SQL                                       |
| Dashboard Framework   | Dash                                            |
| Visualization         | Plotly                                          |
| UI Components         | Dash Bootstrap Components                       |
| Version Control       | GitHub                                          |
| Deployment            | Databricks Apps                                 |

---

## 📁 Project Structure

```text
hr-attrition-intelligence/

├── app/
│   ├── app.py
│   ├── auth.py
│   ├── data.py
│   └── requirements.txt
│
├── ingestion/
│   └── 01_ingest_bronze.py
│
├── processing/
│   ├── 02_silver_clean.py
│   └── 03_gold_kpis.py
│
└── README.md
```

---

## 🔑 Key Technical Decisions

### Why Medallion Architecture?

Bronze preserves raw source data for traceability, Silver improves data quality through cleansing and standardization, and Gold provides business-ready aggregated datasets optimized for analytics and reporting.

### Why Delta Table?

Delta Table provides ACID transactions, schema enforcement, and reliable data processing across the Medallion layers.

### Why Silver Layer for Role Filtering?

Role-level filtering requires access to employee-level records. Since Gold tables are aggregated, department-based filtering is applied using Silver-layer data.

### Why Dash Instead of Traditional BI Dashboards?

Dash provides greater flexibility for implementing role-based login, custom UI components, dynamic filtering, theme switching, and interactive chart modals.

---

## 📸 Screenshots

### Landing Page

![Landing Page](screenshots/landing.png)

### Login Page

![Login Page](screenshots/login.png)

### HR Admin Dashboard

![HR Admin Dashboard](screenshots/admin_dashboard.png)

### Sales Manager Dashboard

![Sales Manager Dashboard](screenshots/sales_dashboard.png)

### Dark Theme

![Dark Theme](screenshots/dark_theme.png)

### Chart Popup Modal

![Chart Popup](screenshots/chart_popup.png)

---

## 💡 Key Insights from Data

* Sales department shows the highest attrition rate at **20.63%**.
* Employees aged **18–25** have the highest attrition rate at **35.77%**.
* Employees earning between **$1,000–$3,000 per month** show an attrition rate of **28.61%**.
* Employees with low job satisfaction exhibit the highest attrition rate at **22.84%**.

---

## 📜 Data Source

**IBM HR Analytics Employee Attrition & Performance Dataset**

Source: Kaggle

This dataset was created by IBM data scientists and is widely used for HR analytics, workforce planning, and attrition prediction use cases.

---

