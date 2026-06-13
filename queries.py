from databricks import sql
import pandas as pd
import os

def get_connection():
    return sql.connect(
        server_hostname = os.getenv("DATABRICKS_HOST", "community.cloud.databricks.com"),
        http_path       = os.getenv("DATABRICKS_HTTP_PATH", "/sql/1.0/warehouses/auto"),
        access_token    = os.getenv("DATABRICKS_TOKEN")
    )

def run_query(query: str) -> pd.DataFrame:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()

CATALOG = "workspace"
SCHEMA  = "default"

def get_overview():
    return run_query(f"SELECT * FROM {CATALOG}.{SCHEMA}.gold_attrition_overview")

def get_dept_analysis():
    return run_query(f"SELECT * FROM {CATALOG}.{SCHEMA}.gold_dept_analysis")

def get_age_analysis():
    return run_query(f"SELECT * FROM {CATALOG}.{SCHEMA}.gold_age_analysis")

def get_income_analysis():
    return run_query(f"SELECT * FROM {CATALOG}.{SCHEMA}.gold_income_analysis")

def get_satisfaction_analysis():
    return run_query(f"SELECT * FROM {CATALOG}.{SCHEMA}.gold_satisfaction_analysis")

def get_users():
    return run_query(f"SELECT * FROM {CATALOG}.{SCHEMA}.app_users WHERE is_active = true")

def validate_user(email: str, password_hash: str):
    df = run_query(f"""
        SELECT * FROM {CATALOG}.{SCHEMA}.app_users
        WHERE email = '{email}'
        AND password = '{password_hash}'
        AND is_active = true
    """)
    return df.iloc[0] if len(df) > 0 else None
