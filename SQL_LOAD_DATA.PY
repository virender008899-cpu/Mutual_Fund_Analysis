import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from getpass import getpass

# ==========================================
# 1. PROJECT SETTINGS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "CLEAN"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

DATABASE = "MF_DB"
HOST = "localhost"
PORT = 5432
USERNAME = "postgres"

# ==========================================
# 2. FILE AND TABLE MAPPING
# ==========================================

files = {
    "01_fund_master.csv": "src_fund_master",
    "02_nav_history.csv": "src_nav_history",
    "03_aum_by_fund_house.csv": "src_aum_by_fund_house",
    "04_monthly_sip_inflows.csv": "src_monthly_sip_inflows",
    "05_category_inflows.csv": "src_category_inflows",
    "06_industry_folio_count.csv": "src_industry_folio_count",
    "07_scheme_performance.csv": "src_scheme_performance",
    "08_investor_transactions.csv": "src_investor_transactions",
    "09_portfolio_holdings.csv": "src_portfolio_holdings",
    "10_benchmark_indices.csv": "src_benchmark_indices"
}

# ==========================================
# 3. CONNECT TO POSTGRESQL
# ==========================================

password = getpass("Enter PostgreSQL password: ")

url = URL.create(
    drivername="postgresql+psycopg2",
    username=USERNAME,
    password=password,
    host=HOST,
    port=PORT,
    database=DATABASE
)

engine = create_engine(url)

print("\nConnecting to PostgreSQL...")

# ==========================================
# 4. LOAD DATASETS
# ==========================================

results = []

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("Database connection successful!")

    for filename, table_name in files.items():

        file_path = DATA_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

        print(f"\nLoading: {filename}")

        df = pd.read_csv(file_path)

        source_rows = len(df)

        if df.columns.duplicated().any():
            raise ValueError(
                f"Duplicate column names in {filename}"
            )

        # Load CSV into PostgreSQL
        df.to_sql(
            name=table_name,
            con=engine,
            schema="public",
            if_exists="replace",
            index=False,
            chunksize=5000,
            method="multi"
        )

        # Verify PostgreSQL row count
        with engine.connect() as connection:
            database_rows = connection.execute(
                text(f'SELECT COUNT(*) FROM public."{table_name}"')
            ).scalar_one()

        status = (
            "PASS"
            if source_rows == database_rows
            else "FAIL"
        )

        results.append({
            "file": filename,
            "table": table_name,
            "source_rows": source_rows,
            "database_rows": database_rows,
            "status": status
        })

        print("Source rows:", source_rows)
        print("Database rows:", database_rows)
        print("Status:", status)

        if status == "FAIL":
            raise RuntimeError(
                f"Row count mismatch in {table_name}"
            )

    # ======================================
    # 5. SAVE LOADING REPORT
    # ======================================

    report = pd.DataFrame(results)

    report.to_csv(
        REPORT_DIR / "postgres_load_report.csv",
        index=False
    )

    print("\n" + "=" * 55)
    print("POSTGRESQL DATA LOADING REPORT")
    print("=" * 55)

    print(report.to_string(index=False))

    print("\nTotal datasets:", len(results))
    print("Total source rows:", report["source_rows"].sum())
    print("Total database rows:", report["database_rows"].sum())

    if (report["status"] == "PASS").all():
        print("\nALL DATASETS LOADED AND VERIFIED SUCCESSFULLY!")

except Exception as error:
    print("\nERROR:", error)
    print("Please check the error before continuing.")

finally:
    engine.dispose()
    