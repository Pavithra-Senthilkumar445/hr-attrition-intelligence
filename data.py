import pandas as pd

# Real data from Gold tables — IBM HR Attrition dataset
OVERVIEW = pd.DataFrame([{
    "total_employees"    : 1470,
    "total_attrition"    : 237,
    "attrition_rate"     : 16.12,
    "avg_age"            : 36.9,
    "avg_monthly_income" : 6503.0,
    "avg_tenure_years"   : 7.0
}])

DEPT = pd.DataFrame([
    {"department": "Sales",                  "total_employees": 446, "attrition_count": 92,  "attrition_rate": 20.63, "avg_salary": 6959.0},
    {"department": "Human Resources",        "total_employees": 63,  "attrition_count": 12,  "attrition_rate": 19.05, "avg_salary": 6655.0},
    {"department": "Research & Development", "total_employees": 961, "attrition_count": 133, "attrition_rate": 13.84, "avg_salary": 6281.0},
])

AGE = pd.DataFrame([
    {"age_group": "18-25", "total_employees": 123, "attrition_count": 44, "attrition_rate": 35.77},
    {"age_group": "26-35", "total_employees": 606, "attrition_count": 116,"attrition_rate": 19.14},
    {"age_group": "36-45", "total_employees": 468, "attrition_count": 43, "attrition_rate":  9.19},
    {"age_group": "46-55", "total_employees": 226, "attrition_count": 26, "attrition_rate": 11.50},
    {"age_group": "55+",   "total_employees": 47,  "attrition_count": 8,  "attrition_rate": 17.02},
])

INCOME = pd.DataFrame([
    {"income_band": "1k-3k",  "total_employees": 395, "attrition_count": 113, "attrition_rate": 28.61},
    {"income_band": "3k-6k",  "total_employees": 519, "attrition_count": 66,  "attrition_rate": 12.72},
    {"income_band": "6k-10k", "total_employees": 275, "attrition_count": 33,  "attrition_rate": 12.00},
    {"income_band": "10k+",   "total_employees": 281, "attrition_count": 25,  "attrition_rate":  8.90},
])

SATISFACTION = pd.DataFrame([
    {"satisfaction_label": "Low",       "jobsatisfaction": 1, "total_employees": 289, "attrition_count": 66, "attrition_rate": 22.84},
    {"satisfaction_label": "Medium",    "jobsatisfaction": 2, "total_employees": 280, "attrition_count": 46, "attrition_rate": 16.43},
    {"satisfaction_label": "High",      "jobsatisfaction": 3, "total_employees": 442, "attrition_count": 73, "attrition_rate": 16.52},
    {"satisfaction_label": "Very High", "jobsatisfaction": 4, "total_employees": 459, "attrition_count": 52, "attrition_rate": 11.33},
])

def get_dept_for_role(role: str, dept: str) -> pd.DataFrame:
    if role == "Manager":
        return DEPT[DEPT["department"].str.contains(dept, case=False)]
    return DEPT

def get_overview_for_role(role: str, dept: str) -> pd.DataFrame:
    if role == "Manager":
        row = DEPT[DEPT["department"].str.contains(dept, case=False)].iloc[0]
        return pd.DataFrame([{
            "total_employees"    : row["total_employees"],
            "total_attrition"    : row["attrition_count"],
            "attrition_rate"     : row["attrition_rate"],
            "avg_monthly_income" : row["avg_salary"],
            "avg_tenure_years"   : 7.0
        }])
    return OVERVIEW
