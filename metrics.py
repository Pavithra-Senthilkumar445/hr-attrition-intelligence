def calculate_kpis(df):
    total_employees = len(df)
    attrition_count = df["Attrition_Flag"].sum()
    attrition_rate = round((attrition_count / total_employees) * 100, 2)

    avg_age = round(df["Age"].mean(), 1)

    return {
        "total_employees": total_employees,
        "attrition_count": attrition_count,
        "attrition_rate": attrition_rate,
        "avg_age": avg_age
    }
