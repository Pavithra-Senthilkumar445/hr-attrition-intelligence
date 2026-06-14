# data.py
# Reads REAL data from Unity Catalog Volume using Databricks SDK
# Silver CSV → role based filtering (1470 individual rows)
# Gold CSVs  → overall KPI cards (pre-aggregated for HR Admin)

import pandas as pd
from io import BytesIO

VOLUME_BASE = "/Volumes/workspace/default/hr_files"

def _read_csv(filename: str) -> pd.DataFrame:
    try:
        from databricks.sdk import WorkspaceClient
        w   = WorkspaceClient()
        res = w.files.download(f"{VOLUME_BASE}/{filename}")
        return pd.read_csv(BytesIO(res.contents.read()))
    except Exception as e:
        print(f"ERROR reading {filename}: {e}")
        return pd.DataFrame()

# Load at app startup — real data from Volume
SILVER        = _read_csv("silver.csv")
GOLD_OVERVIEW = _read_csv("gold_overview.csv")

print(f"Silver loaded     : {len(SILVER)} rows")
print(f"Gold overview     : {len(GOLD_OVERVIEW)} rows")

# All unique job roles for filter dropdown
ALL_JOB_ROLES = sorted(SILVER["jobrole"].dropna().unique().tolist())

# All age groups for filter pills
AGE_GROUPS = ["18-25", "26-35", "36-45", "46-55", "55+"]


def get_data_for_role(
    role       : str,
    department : str,
    age_filter : str  = "All",
    job_filter : str  = "All"
) -> dict:
    """
    Filters Silver table by role + department + age + job role.
    Calculates real KPIs from filtered rows.
    """
    # Step 1 — Department filter
    if department == "All":
        df = SILVER.copy()
    else:
        df = SILVER[
            SILVER["department"].str.strip() == department.strip()
        ].copy()

    # Step 2 — Age group filter
    df["age_group"] = pd.cut(
        df["age"],
        bins   = [17, 25, 35, 45, 55, 100],
        labels = AGE_GROUPS
    )
    if age_filter != "All":
        df = df[df["age_group"].astype(str) == age_filter].copy()

    # Step 3 — Job role filter
    if job_filter != "All":
        df = df[df["jobrole"] == job_filter].copy()

    if len(df) == 0:
        return _empty_data()

    # Step 4 — Calculate KPIs
    total_employees    = len(df)
    total_attrition    = int(df["attrition_flag"].sum())
    attrition_rate     = round((total_attrition / total_employees) * 100, 2)
    avg_monthly_income = round(df["monthlyincome"].mean(), 0)
    avg_tenure         = round(df["yearsatcompany"].mean(), 1)
    avg_age            = round(df["age"].mean(), 1)

    # Step 5 — Attrition by department
    dept_analysis = df.groupby("department").agg(
        total_employees = ("employeenumber", "count"),
        attrition_count = ("attrition_flag",  "sum")
    ).reset_index()
    dept_analysis["attrition_rate"] = round(
        dept_analysis["attrition_count"] / dept_analysis["total_employees"] * 100, 2
    )

    # Step 6 — Attrition by age group
    age_analysis = df.groupby("age_group", observed=True).agg(
        total_employees = ("employeenumber", "count"),
        attrition_count = ("attrition_flag",  "sum")
    ).reset_index()
    age_analysis["age_group"]      = age_analysis["age_group"].astype(str)
    age_analysis["attrition_rate"] = round(
        age_analysis["attrition_count"] / age_analysis["total_employees"] * 100, 2
    )

    # Step 7 — Attrition by income band
    df["income_band"] = pd.cut(
        df["monthlyincome"],
        bins   = [0, 3000, 6000, 10000, 999999],
        labels = ["1k-3k", "3k-6k", "6k-10k", "10k+"]
    )
    income_analysis = df.groupby("income_band", observed=True).agg(
        total_employees = ("employeenumber", "count"),
        attrition_count = ("attrition_flag",  "sum")
    ).reset_index()
    income_analysis["income_band"]     = income_analysis["income_band"].astype(str)
    income_analysis["attrition_rate"]  = round(
        income_analysis["attrition_count"] / income_analysis["total_employees"] * 100, 2
    )

    # Step 8 — Attrition by job satisfaction
    sat_map   = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
    sat_order = ["Low", "Medium", "High", "Very High"]
    df["satisfaction_label"] = df["jobsatisfaction"].map(sat_map)
    sat_analysis = df.groupby("satisfaction_label").agg(
        total_employees = ("employeenumber", "count"),
        attrition_count = ("attrition_flag",  "sum")
    ).reset_index()
    sat_analysis["attrition_rate"] = round(
        sat_analysis["attrition_count"] / sat_analysis["total_employees"] * 100, 2
    )
    sat_analysis["satisfaction_label"] = pd.Categorical(
        sat_analysis["satisfaction_label"],
        categories = sat_order,
        ordered    = True
    )
    sat_analysis = sat_analysis.sort_values("satisfaction_label")

    # Step 9 — Key insights
    insights = []
    if len(dept_analysis) > 0:
        top_dept = dept_analysis.sort_values("attrition_rate", ascending=False).iloc[0]
        insights.append(f"🔴 {top_dept['department']} has highest attrition at {top_dept['attrition_rate']}%")
    if len(age_analysis) > 0:
        top_age = age_analysis.sort_values("attrition_rate", ascending=False).iloc[0]
        insights.append(f"👥 Age group {top_age['age_group']} has highest turnover at {top_age['attrition_rate']}%")
    if len(income_analysis) > 0:
        top_inc = income_analysis.sort_values("attrition_rate", ascending=False).iloc[0]
        insights.append(f"💰 Employees earning {top_inc['income_band']} leave most at {top_inc['attrition_rate']}%")
    if len(sat_analysis) > 0:
        top_sat = sat_analysis.sort_values("attrition_rate", ascending=False).iloc[0]
        insights.append(f"😞 {top_sat['satisfaction_label']} satisfaction employees leave most at {top_sat['attrition_rate']}%")

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
        "insights"           : insights,
    }


def _empty_data() -> dict:
    return {
        "total_employees"    : 0,
        "total_attrition"    : 0,
        "attrition_rate"     : 0.0,
        "avg_monthly_income" : 0.0,
        "avg_tenure"         : 0.0,
        "avg_age"            : 0.0,
        "dept_analysis"      : pd.DataFrame(),
        "age_analysis"       : pd.DataFrame(),
        "income_analysis"    : pd.DataFrame(),
        "sat_analysis"       : pd.DataFrame(),
        "insights"           : ["No data available for selected filters."],
    }
