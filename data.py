import pandas as pd

def load_data():
    # Replace later with Databricks connector
    df = pd.read_csv("ibm_hr_data.csv")

    # basic cleanup
    df["Attrition_Flag"] = df["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)

    return df
