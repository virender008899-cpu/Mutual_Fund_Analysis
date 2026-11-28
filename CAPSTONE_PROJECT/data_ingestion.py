import pandas as pd
import os

data_path = "data/raw"

dataframes = {}

files = os.listdir(data_path)

for file in files:

    if file.endswith(".csv") and not file.endswith("_NAV.csv"):

        name = file.replace(".csv", "")

        file_path = os.path.join(data_path, file)

        df = pd.read_csv(file_path)

        dataframes[name] = df

        print("\n")
        print("Dataset:", name)

        # Check rows and columns
        print("\nShape:")
        print(df.shape)

        # Check data types
        print("\nData Types:")
        print(df.dtypes)

        # Display first five records
        print("\nFirst Five Rows:")
        print(df.head())

        # Check column names
        print("\nColumns:")
        print(df.columns.tolist())

        # Check unique values
        print("\nUnique Values:")
        print(df.nunique())

print("\nTotal datasets loaded:", len(dataframes))
print("Data ingestion completed successfully.")

# Explore Fund Master dataset

df = dataframes["01_fund_master"]

print("\nFund Master Exploration")

print("\nAvailable Columns:")
print(df.columns.tolist())

# Check unique values in each column
for column in df.columns:

    if any(word in column.lower() for word in
           ["fund_house", "category", "sub_category", "risk_grade"]):

        print("\n", column)
        print("Unique values:", df[column].nunique())
        print(df[column].dropna().unique())

# AMFI Scheme Code Validation

fund_master = dataframes["01_fund_master"]
nav_history = dataframes["02_nav_history"]

fund_codes = set(fund_master["amfi_code"].dropna())
nav_codes = set(nav_history["amfi_code"].dropna())

missing_codes = fund_codes - nav_codes

print("\nAMFI Scheme Code Validation")

print("Fund Master Codes:", len(fund_codes))
print("NAV History Codes:", len(nav_codes))
print("Missing Codes:", len(missing_codes))

if len(missing_codes) == 0:
    print("All Fund Master codes exist in NAV History.")
else:
    print("Codes missing from NAV History:")
    print(missing_codes)