-- ============================================
-- BLUESTOCK MUTUAL FUND CAPSTONE PROJECT
-- DATABASE: MF_DB
-- STAR SCHEMA DESIGN
-- ============================================

-- 1. DIMENSION: FUND
CREATE TABLE IF NOT EXISTS dim_fund (
    fund_key SERIAL PRIMARY KEY,
    amfi_code VARCHAR(20) UNIQUE NOT NULL,
    fund_house VARCHAR(150),
    scheme_name VARCHAR(250) NOT NULL
);

-- 2. DIMENSION: DATE
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER,
    year INTEGER,
    day_of_week VARCHAR(20)
);

-- 3. FACT: NAV
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    nav NUMERIC(18,4) NOT NULL CHECK (nav > 0),
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    UNIQUE (fund_key, date_key)
);

-- 4. FACT: INVESTOR TRANSACTIONS
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL
        CHECK (transaction_type IN ('SIP', 'Lumpsum', 'Redemption')),
    amount NUMERIC(18,2) NOT NULL CHECK (amount > 0),
    state VARCHAR(100),
    kyc_status VARCHAR(20) NOT NULL
        CHECK (kyc_status IN ('Verified', 'Pending')),
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- 5. FACT: SCHEME PERFORMANCE
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    return_1yr_pct NUMERIC(12,4),
    return_3yr_pct NUMERIC(12,4),
    return_5yr_pct NUMERIC(12,4),
    benchmark_3yr_pct NUMERIC(12,4),
    alpha NUMERIC(12,4),
    beta NUMERIC(12,4),
    sharpe_ratio NUMERIC(12,4),
    sortino_ratio NUMERIC(12,4),
    std_dev_ann_pct NUMERIC(12,4),
    max_drawdown_pct NUMERIC(12,4),
    aum_crore NUMERIC(18,2),
    expense_ratio_pct NUMERIC(8,4)
        CHECK (expense_ratio_pct IS NULL OR
               expense_ratio_pct BETWEEN 0.1 AND 2.5),
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    UNIQUE (fund_key, date_key)
);

-- 6. FACT: AUM
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    aum_crore NUMERIC(18,2) NOT NULL CHECK (aum_crore >= 0),
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    UNIQUE (fund_key, date_key)
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_nav_fund
ON fact_nav(fund_key);

CREATE INDEX IF NOT EXISTS idx_nav_date
ON fact_nav(date_key);

CREATE INDEX IF NOT EXISTS idx_transactions_fund
ON fact_transactions(fund_key);

CREATE INDEX IF NOT EXISTS idx_transactions_date
ON fact_transactions(date_key);

CREATE INDEX IF NOT EXISTS idx_performance_fund
ON fact_performance(fund_key);

CREATE INDEX IF NOT EXISTS idx_aum_fund
ON fact_aum(fund_key);

-- ============================================
-- VERIFICATION
-- ============================================

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- ============================================
-- END OF SCHEMA
-- ============================================
