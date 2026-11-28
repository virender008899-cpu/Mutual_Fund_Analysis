-- BLUESTOCK MUTUAL FUND CAPSTONE PROJECT
-- DATABASE: MF_DB
-- 10 ANALYTICAL SQL QUERIES
-- =====================================================


-- 1. TOP 5 FUNDS BY AUM

SELECT
    scheme_name,
    fund_house,
    aum_crore
FROM src_scheme_performance
WHERE aum_crore IS NOT NULL
ORDER BY aum_crore DESC
LIMIT 5;


-- 2. AVERAGE NAV PER MONTH

SELECT
    DATE_TRUNC('month', date::date)::date AS month,
    ROUND(AVG(nav)::numeric, 4) AS average_nav
FROM src_nav_history
WHERE date IS NOT NULL
  AND nav IS NOT NULL
GROUP BY DATE_TRUNC('month', date::date)
ORDER BY month;


-- 3. SIP YEAR-OVER-YEAR GROWTH

SELECT
    month,
    sip_inflow_crore,
    yoy_growth_pct
FROM src_monthly_sip_inflows
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month;


-- 4. INVESTOR TRANSACTIONS BY STATE

SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_transaction_amount
FROM src_investor_transactions
GROUP BY state
ORDER BY total_transactions DESC;


-- 5. FUNDS WITH EXPENSE RATIO BELOW 1%

SELECT
    amfi_code,
    scheme_name,
    fund_house,
    category,
    expense_ratio_pct
FROM src_fund_master
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct ASC;


-- 6. TOP 5 FUND HOUSES BY AUM

SELECT
    fund_house,
    SUM(aum_crore) AS total_aum_crore
FROM src_aum_by_fund_house
GROUP BY fund_house
ORDER BY total_aum_crore DESC
LIMIT 5;


-- 7. CATEGORY-WISE TOTAL INFLOWS

SELECT
    category,
    ROUND(SUM(net_inflow_crore)::numeric, 2)
        AS total_inflow_crore
FROM src_category_inflows
GROUP BY category
ORDER BY total_inflow_crore DESC;


-- 8. MONTHLY GROWTH IN TOTAL INDUSTRY FOLIOS

SELECT
    month,total_folios_crore,
    ROUND(total_folios_crore -LAG(total_folios_crore) OVER (ORDER BY month),
        4
    ) AS monthly_folio_change
FROM src_industry_folio_count
ORDER BY month;


-- 9. TOP 10 SECTORS BY PORTFOLIO HOLDING VALUE

SELECT
    sector,
    COUNT(*) AS total_holdings,
    ROUND(SUM(market_value_cr)::numeric, 2)
        AS total_market_value_cr
FROM src_portfolio_holdings
GROUP BY sector
ORDER BY total_market_value_cr DESC
LIMIT 10;


-- 10. KYC STATUS ANALYSIS

SELECT
    kyc_status,
    COUNT(*) AS total_investors,
    ROUND(
        COUNT(*) * 100.0 /
        NULLIF((SELECT COUNT(*) FROM src_investor_transactions), 0),
        2
    ) AS percentage
FROM src_investor_transactions
GROUP BY kyc_status
ORDER BY total_investors DESC;


-- =====================================================
-- END OF ANALYTICAL QUERIES
-- =====================================================