import pandas as pd
from pathlib import Path

# Project folders
base_folder = Path(__file__).resolve().parent
raw_folder = base_folder / "data" / "raw"
clean_folder = base_folder / "data" / "CLEAN"

clean_folder.mkdir(parents=True, exist_ok=True)

# --------------------------------
# 1. NAV HISTORY
# --------------------------------

nav = pd.read_csv(raw_folder / "02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"], errors="coerce")
nav["nav"] = pd.to_numeric(nav["nav"], errors="coerce")

nav = nav.dropna(subset=["amfi_code", "date"])

nav = nav.sort_values(["amfi_code", "date"])

nav = nav.drop_duplicates(
    subset=["amfi_code", "date"],
    keep="last"
)

# Fill missing NAV using previous NAV of the same fund
nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

# Remove rows where NAV is still missing or invalid
nav = nav.dropna(subset=["nav"])
nav = nav[nav["nav"] > 0]

nav.to_csv(clean_folder / "02_nav_history.csv", index=False)


# --------------------------------
# 2. SCHEME PERFORMANCE
# --------------------------------

performance = pd.read_csv(
    raw_folder / "07_scheme_performance.csv"
)

# Convert financial columns to numeric
numeric_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio",
    "std_dev_ann_pct",
    "max_drawdown_pct",
    "aum_crore",
    "expense_ratio_pct"
]

for col in numeric_columns:
    if col in performance.columns:
        performance[col] = pd.to_numeric(
            performance[col], errors="coerce"
        )

# Flag unusual return values instead of deleting them
return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct"
]

for col in return_columns:
    if col in performance.columns:
        q1 = performance[col].quantile(0.25)
        q3 = performance[col].quantile(0.75)
        iqr = q3 - q1

        performance[col + "_anomaly"] = (
            (performance[col] < q1 - 1.5 * iqr) |
            (performance[col] > q3 + 1.5 * iqr)
        )

# Validate expense ratio
performance["expense_ratio_valid"] = (
    performance["expense_ratio_pct"].between(0.1, 2.5)
)

# Do not invent missing performance figures
performance.to_csv(
    clean_folder / "07_scheme_performance.csv",
    index=False
)


# --------------------------------
# 3. INVESTOR TRANSACTIONS
# --------------------------------

transactions = pd.read_csv(
    raw_folder / "08_investor_transactions.csv"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"],
    errors="coerce"
)

# Standardise transaction types
type_mapping = {
    "sip": "SIP",
    "systematic investment plan": "SIP",
    "lumpsum": "Lumpsum",
    "lump sum": "Lumpsum",
    "lump-sum": "Lumpsum",
    "redemption": "Redemption"
}

transactions["transaction_type"] = (
    transactions["transaction_type"]
    .astype("string")
    .str.strip()
    .str.lower()
    .map(type_mapping)
)

# Standardise KYC status
transactions["kyc_status"] = (
    transactions["kyc_status"]
    .astype("string")
    .str.strip()
    .str.title()
)

valid_kyc = [
    "Verified",
    "Pending",
    "Rejected",
    "In Progress"
]

transactions["kyc_status_valid"] = (
    transactions["kyc_status"].isin(valid_kyc)
)

# Remove records without essential transaction information
transactions = transactions.dropna(
    subset=[
        "investor_id",
        "transaction_date",
        "amfi_code",
        "transaction_type",
        "amount_inr"
    ]
)

transactions = transactions[
    transactions["amount_inr"] > 0
]

transactions = transactions.drop_duplicates()

transactions.to_csv(
    clean_folder / "08_investor_transactions.csv",
    index=False
)


# --------------------------------
# 4. GENERAL MISSING VALUE REPORT
# --------------------------------

print("\nDAY 2 MISSING VALUE CLEANING REPORT")

for file in clean_folder.glob("*.csv"):

    df = pd.read_csv(file)

    print("\nFile:", file.name)
    print("Total rows:", len(df))
    print("Total missing values:", df.isnull().sum().sum())

    missing = df.isnull().sum()

    if missing.sum() > 0:
        print("Columns with missing values:")
        print(missing[missing > 0])
    else:
        print("No missing values.")

print("\nCleaning completed.")
print("Cleaned files saved in data/CLEAN/")

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
CLEAN = Path("data/CLEAN")

files = {
    "NAV History": "02_nav_history.csv",
    "Investor Transactions": "08_investor_transactions.csv",
    "Scheme Performance": "07_scheme_performance.csv"
}

def check_file(name, filename):
    print("\n" + "=" * 60)
    print(name.upper())
    print("=" * 60)

    raw_path = RAW / filename
    clean_path = CLEAN / filename

    if not raw_path.exists() or not clean_path.exists():
        print("ERROR: Raw or cleaned file not found.")
        return

    raw = pd.read_csv(raw_path)
    df = pd.read_csv(clean_path)

    print(f"Raw rows: {len(raw)}")
    print(f"Clean rows: {len(df)}")
    print(f"Raw missing values: {raw.isna().sum().sum()}")
    print(f"Clean missing values: {df.isna().sum().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    if name == "NAV History":
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

        print("\nNAV CHECKS")
        print("Invalid dates:", df["date"].isna().sum())
        print("Missing NAV:", df["nav"].isna().sum())
        print("NAV <= 0:", (df["nav"] <= 0).sum())
        print("Duplicate fund-date pairs:",
              df.duplicated(["amfi_code", "date"]).sum())
        print("Sorted by fund and date:",
              df.sort_values(["amfi_code", "date"]).index.equals(df.index))

    elif name == "Investor Transactions":
        df["transaction_date"] = pd.to_datetime(
            df["transaction_date"], errors="coerce"
        )
        df["amount_inr"] = pd.to_numeric(
            df["amount_inr"], errors="coerce"
        )

        print("\nTRANSACTION CHECKS")
        print("Invalid dates:", df["transaction_date"].isna().sum())
        print("Missing amounts:", df["amount_inr"].isna().sum())
        print("Amount <= 0:", (df["amount_inr"] <= 0).sum())

        print("Transaction types:")
        print(df["transaction_type"].value_counts(dropna=False))

        print("KYC values:")
        print(df["kyc_status"].value_counts(dropna=False))

    elif name == "Scheme Performance":
        numeric_columns = [
            "return_1yr_pct",
            "return_3yr_pct",
            "return_5yr_pct",
            "benchmark_3yr_pct",
            "alpha",
            "beta",
            "sharpe_ratio",
            "sortino_ratio",
            "std_dev_ann_pct",
            "max_drawdown_pct",
            "aum_crore",
            "expense_ratio_pct"
        ]

        print("\nPERFORMANCE CHECKS")
        for col in numeric_columns:
            converted = pd.to_numeric(df[col], errors="coerce")
            print(f"{col}: invalid numeric values =",
                  (converted.isna() & df[col].notna()).sum())

        expense = pd.to_numeric(
            df["expense_ratio_pct"], errors="coerce"
        )
        print("Expense ratio below 0.1:",
              (expense < 0.1).sum())
        print("Expense ratio above 2.5:",
              (expense > 2.5).sum())

for name, filename in files.items():
    check_file(name, filename)

print("\n" + "=" * 60)
print("VERIFICATION COMPLETED")
print("No files were modified.")