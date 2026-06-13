import pandas as pd

def load_data():
    df = pd.read_csv("data/ibm_hr_data.csv")

    if "Attrition" in df.columns:
        df["Attrition_Flag"] = df["Attrition"].map({"Yes": 1, "No": 0})

    return df
