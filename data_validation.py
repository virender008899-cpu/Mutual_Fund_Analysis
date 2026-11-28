import pandas as pd
import os
data_path = "data/RAW"
files = os.listdir(data_path)
print(files)

dataframes = {}

for file in files:
    if file.endswith(".csv"):
        name = file.replace(".csv", "")
        dataframes[name] = pd.read_csv(os.path.join(data_path, file))

        print(name, dataframes[name].shape)

for name, df in dataframes.items():
    print("\n", name)
    print(df.isnull().sum())        

print("\nChecking for duplicates in each dataframe:")
for name, df in dataframes.items():
    print(name, "Duplicates:", df.duplicated().sum())    

for name, df in dataframes.items():
    print("\n", name)
    print(df.dtypes)  


for name, df in dataframes.items():
    print(name, "Rows:", df.shape[0], "Columns:", df.shape[1])

for name, df in dataframes.items():
    print("\n", name)
    print(df.head(5))

date_columns = {
    "01_fund_master": ["launch_date"],
    "02_nav_history": ["date"],
    "03_aum_by_fund_house": ["date"],
    "04_monthly_sip_inflows": ["month"],
    "05_category_inflows": ["month"],
    "06_industry_folio_count": ["month"],
    "08_investor_transactions": ["transaction_date"],
    "09_portfolio_holdings": ["portfolio_date"],
    "10_benchmark_indices": ["date"]
}

for name, columns in date_columns.items():
    for column in columns:
        dataframes[name][column] = pd.to_datetime(
            dataframes[name][column], errors="raise"
        )

print("Date conversion completed.")    

for name, df in dataframes.items():
    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            print(name, column, df[column].dtype)

for name, df in dataframes.items():
    numeric_data = df.select_dtypes(include="number")
    print("\n", name)
    print((numeric_data < 0).sum())

for name, df in dataframes.items():
    print("\n", name)
    print(df.nunique())

for name, df in dataframes.items():
    text_columns = df.select_dtypes(include="object")

    print("\n", name)

    for column in text_columns.columns:
        print(column, text_columns[column].unique()[:10]) 


# data check for cleaning
df = dataframes["04_monthly_sip_inflows"]

print(df[df["yoy_growth_pct"].isna()])


df = dataframes["04_monthly_sip_inflows"]
print("Missing YoY values:", df["yoy_growth_pct"].isna().sum())

df = dataframes["04_monthly_sip_inflows"]

df = df.fillna(0)

print(df.isnull().sum())

# Fill missing values only in 04_monthly_sip_inflows
dataframes["04_monthly_sip_inflows"] = (
    dataframes["04_monthly_sip_inflows"].fillna(0))

# Save all files in CLEAN folder
clean_path = "data/CLEAN"
os.makedirs(clean_path, exist_ok=True)

for name, df in dataframes.items():

    output_file = os.path.join(clean_path, name + ".csv")

    df.to_csv(output_file, index=False)

    print(name, "Saved successfully")

print("All files saved successfully in CLEAN folder.")