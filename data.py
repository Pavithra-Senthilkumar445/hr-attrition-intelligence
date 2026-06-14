# data.py
# Reads REAL data from Unity Catalog Volume using Databricks SDK
# Silver CSV → role based filtering (1470 individual rows)
# Gold CSVs  → overall KPI cards (pre-aggregated)
# Official Databricks doc confirms SDK is required for Apps
# Source: kb.databricks.com/unity-catalog/queries-to-access-files

import pandas as pd
from io import BytesIO

VOLUME_BASE = "/Volumes/workspace/default/hr_files"

def _read_csv(filename: str) -> pd.DataFrame:
    """
    Downloads CSV from Unity Catalog Volume using Databricks SDK.
    Required for Databricks Apps — direct path access not supported.
    """
    try:
        from databricks.sdk import WorkspaceClient
        w   = WorkspaceClient()
        res = w.files.download(f"{VOLUME_BASE}/{filename}")
        return pd.read_csv(BytesIO(res.contents.read()))
    except Exception as e:
        print(f"ERROR reading {filename}: {e}")
        return pd.DataFrame()

# Load at app startup — real data from Volume
SILVER       = _read_csv("silver.csv")
GOLD_OVERVIEW = _read_csv("gold_overview.csv")
GOLD_DEPT    = _read_csv("gold_dept.csv")

print(f"Silver loaded    : {len(SILVER)} rows")
print(f"Gold overview    : {len(GOLD_OVERVIEW)} rows")
print(f"Gold dept        : {len(GOLD_DEPT)} rows")


def get_data_for_role(role: str, department: str) -> dict:
    """
    Filters Silver table by role/department.
    Calculates real KPIs from filtered rows.
    Gold overview used for HR Admin overall KPIs only.
    """
    # Filter Silver by department
    if department == "All":
        df = SILVER.copy()
    else:
        df = SILVER[
            SILVER["department"].str.strip() == department.strip()
        ].copy()

    # Calculate KPIs from real Silver data
    total_employees    = len(df)
    total_attrition    = int(df["attrition_flag"].sum())
    attrition_rate     = round((total_attrition / total_employees) * 100, 2) if total_employees > 0 else 0
    avg_monthly_income = round(df["monthlyincome"].mean(), 0)
    avg_tenure         = round(df["yearsatcompany"].mean(), 1)
    avg_age            = round(df["age"].mean(), 1)

    # Attrition by department (from filtered Silver)
    dept_analysis = df.groupby("department").agg(
        total_employees  = ("employeenumber", "count"),
        attrition_count  = ("attrition_flag", "sum")
    ).reset_index()
    dept_analysis["attrition_rate"] = round(
        dept_analysis["attrition_count"] / dept_analysis["total_employees"] * 100, 2
    )

    # Attrition by age group
    df["age_group"] = pd.cut(
        df["age"],
        bins   = [17, 25, 35, 45, 55, 100],
        labels = ["18-25", "26-35", "36-45", "46-55", "55+"]
    )
    age_analysis = df.groupby("age_group", observed=True).agg(
        total_employees = ("employeenumber", "count"),
        attrition_count = ("attrition_flag", "sum")
    ).reset_index()
    age_analysis["attrition_rate"] = round(
        age_analysis["attrition_count"] / age_analysis["total_employees"] * 100, 2
    )

    # Attrition by income band
    df["income_band"] = pd.cut(
        df["monthlyincome"],
        bins   = [0, 3000, 6000, 10000, 999999],
        labels = ["1k-3k", "3k-6k", "6k-10k", "10k+"]
    )
    income_analysis = df.groupby("income_band", observed=True).agg(
        total_employees = ("employeenumber", "count"),
        attrition_count = ("attrition_flag", "sum")
    ).reset_index()
    income_analysis["attrition_rate"] = round(
        income_analysis["attrition_count"] / income_analysis["total_employees"] * 100, 2
    )

    # Attrition by job satisfaction
    sat_map = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
    df["satisfaction_label"] = df["jobsatisfaction"].map(sat_map)
    sat_analysis = df.groupby("satisfaction_label").agg(
        total_employees = ("employeenumber", "count"),
        attrition_count = ("attrition_flag", "sum")
    ).reset_index()
    sat_analysis["attrition_rate"] = round(
        sat_analysis["attrition_count"] / sat_analysis["total_employees"] * 100, 2
    )
    sat_order = ["Low", "Medium", "High", "Very High"]
    sat_analysis["satisfaction_label"] = pd.Categorical(
        sat_analysis["satisfaction_label"], categories=sat_order, ordered=True
    )
    sat_analysis = sat_analysis.sort_values("satisfaction_label")

    # Key insights
    top_dept    = dept_analysis.sort_values("attrition_rate", ascending=False).iloc[0]
    top_age     = age_analysis.sort_values("attrition_rate",  ascending=False).iloc[0]
    top_income  = income_analysis.sort_values("attrition_rate", ascending=False).iloc[0]
    top_sat     = sat_analysis.sort_values("attrition_rate",  ascending=False).iloc[0]

    insights = [
        f"🔴 {top_dept['department']} has the highest attrition rate at {top_dept['attrition_rate']}%",
        f"👥 Employees aged {top_age['age_group']} have the highest turnover at {top_age['attrition_rate']}%",
        f"💰 Employees earning {top_income['income_band']} leave most at {top_income['attrition_rate']}%",
        f"😞 {top_sat['satisfaction_label']} job satisfaction has highest attrition at {top_sat['attrition_rate']}%",
    ]

    return {
        "total_employees"    : total_employees,
        "total_attrition"    : total_attrition,
        "attrition_rate"     : attrition_rate,
        "avg_monthly_income" : avg_monthly_income,
        "avg_tenure"         : avg_tenure,
        "avg_age"            : avg_age,
        "dept_analysis"      : dept_analysis,
        "age_analysis"       : age_analysis,
        "income_analysis"    : income_analysis,
        "sat_analysis"       : sat_analysis,
        "show_salary"        : role in ["HR Admin", "Sales Manager", "R&D Manager"],
        "insights"           : insights,
        "filtered_df"        : df,
    }
