Bluestock Mutual Fund Analysis – Data Dictionary

Project Information

Item	Details
Project	Bluestock Mutual Fund Analysis
Database	MF_DB
Database System	PostgreSQL
Source Format	CSV
Total Source Datasets	10
Data Location	data/CLEAN/

⸻

1. Fund Master

Source: 01_fund_master.csv
Table: src_fund_master

Column	Data Type	Business Definition
amfi_code	BIGINT	Unique AMFI scheme identification code
fund_house	TEXT	Mutual fund company name
scheme_name	TEXT	Name of the mutual fund scheme
category	TEXT	Main fund category
sub_category	TEXT	Specific fund classification
plan	TEXT	Investment plan type
launch_date	TEXT	Scheme launch date
benchmark	TEXT	Benchmark index used for comparison
expense_ratio_pct	DOUBLE PRECISION	Annual fund management expense percentage
exit_load_pct	DOUBLE PRECISION	Exit load percentage
min_sip_amount	BIGINT	Minimum SIP investment amount
min_lumpsum_amount	BIGINT	Minimum lump sum investment
fund_manager	TEXT	Name of fund manager
risk_category	TEXT	Investment risk classification
sebi_category_code	TEXT	SEBI category identification code

2. NAV History

Source: 02_nav_history.csv
Table: src_nav_history

Column	Data Type	Business Definition
amfi_code	BIGINT	AMFI scheme identification code
date	TEXT	NAV record date
nav	DOUBLE PRECISION	Net Asset Value per unit

3. AUM by Fund House

Source: 03_aum_by_fund_house.csv
Table: src_aum_by_fund_house

Column	Data Type	Business Definition
date	TEXT	Reporting date
fund_house	TEXT	Mutual fund company
aum_lakh_crore	DOUBLE PRECISION	Assets under management in lakh crore
aum_crore	BIGINT	Assets under management in crore
num_schemes	BIGINT	Number of schemes managed

4. Monthly SIP Inflows

Source: 04_monthly_sip_inflows.csv
Table: src_monthly_sip_inflows

Column	Data Type	Business Definition
month	TEXT	Reporting month
sip_inflow_crore	BIGINT	Total monthly SIP investment inflow
active_sip_accounts_crore	DOUBLE PRECISION	Number of active SIP accounts in crore
new_sip_accounts_lakh	DOUBLE PRECISION	Newly registered SIP accounts in lakh
sip_aum_lakh_crore	DOUBLE PRECISION	SIP assets under management in lakh crore
yoy_growth_pct	DOUBLE PRECISION	Year-over-year SIP growth percentage

5. Category Inflows

Source: 05_category_inflows.csv
Table: src_category_inflows

Column	Data Type	Business Definition
month	TEXT	Reporting month
category	TEXT	Mutual fund category
net_inflow_crore	DOUBLE PRECISION	Net investment inflow in crore

6. Industry Folio Count

Source: 06_industry_folio_count.csv
Table: src_industry_folio_count

Column	Data Type	Business Definition
month	TEXT	Reporting month
total_folios_crore	DOUBLE PRECISION	Total mutual fund folios in crore
equity_folios_crore	DOUBLE PRECISION	Equity fund folios in crore
debt_folios_crore	DOUBLE PRECISION	Debt fund folios in crore
hybrid_folios_crore	DOUBLE PRECISION	Hybrid fund folios in crore
others_folios_crore	DOUBLE PRECISION	Other category folios in crore

7. Scheme Performance

Source: 07_scheme_performance.csv
Table: src_scheme_performance

Column	Data Type	Business Definition
amfi_code	BIGINT	AMFI scheme identification code
scheme_name	TEXT	Mutual fund scheme name
fund_house	TEXT	Fund management company
category	TEXT	Scheme category
plan	TEXT	Investment plan
return_1yr_pct	DOUBLE PRECISION	One-year investment return
return_3yr_pct	DOUBLE PRECISION	Three-year investment return
return_5yr_pct	DOUBLE PRECISION	Five-year investment return
benchmark_3yr_pct	DOUBLE PRECISION	Three-year benchmark return
alpha	DOUBLE PRECISION	Excess return relative to benchmark
beta	DOUBLE PRECISION	Market sensitivity measurement
sharpe_ratio	DOUBLE PRECISION	Risk-adjusted return measurement
sortino_ratio	DOUBLE PRECISION	Downside risk-adjusted return measurement
std_dev_ann_pct	DOUBLE PRECISION	Annualised standard deviation
max_drawdown_pct	DOUBLE PRECISION	Maximum observed percentage decline
aum_crore	BIGINT	Assets under management in crore
expense_ratio_pct	DOUBLE PRECISION	Annual expense ratio
morningstar_rating	BIGINT	Morningstar scheme rating
risk_grade	TEXT	Scheme risk grade
return_1yr_pct_anomaly	BOOLEAN	One-year return anomaly flag
return_3yr_pct_anomaly	BOOLEAN	Three-year return anomaly flag
return_5yr_pct_anomaly	BOOLEAN	Five-year return anomaly flag
benchmark_3yr_pct_anomaly	BOOLEAN	Benchmark return anomaly flag
expense_ratio_valid	BOOLEAN	Indicates whether expense ratio passes validation

8. Investor Transactions

Source: 08_investor_transactions.csv
Table: src_investor_transactions

Column	Data Type	Business Definition
investor_id	TEXT	Unique investor identification
transaction_date	TEXT	Transaction date
amfi_code	BIGINT	AMFI scheme identification code
transaction_type	TEXT	SIP, Lumpsum or Redemption
amount_inr	BIGINT	Transaction amount in Indian rupees
state	TEXT	Investor’s state
city	TEXT	Investor’s city
city_tier	TEXT	City classification
age_group	TEXT	Investor age group
gender	TEXT	Recorded investor gender
annual_income_lakh	DOUBLE PRECISION	Annual income in lakh
payment_mode	TEXT	Transaction payment method
kyc_status	TEXT	Investor KYC verification status
kyc_status_valid	BOOLEAN	Indicates whether KYC status passes validation

9. Portfolio Holdings

Source: 09_portfolio_holdings.csv
Table: src_portfolio_holdings

Column	Data Type	Business Definition
amfi_code	BIGINT	AMFI scheme identification code
stock_symbol	TEXT	Stock exchange symbol
stock_name	TEXT	Company or stock name
sector	TEXT	Business sector classification
weight_pct	DOUBLE PRECISION	Portfolio allocation percentage
market_value_cr	DOUBLE PRECISION	Holding market value in crore
current_price_inr	DOUBLE PRECISION	Current stock price in rupees
portfolio_date	TEXT	Portfolio reporting date

10. Benchmark Indices

Source: 10_benchmark_indices.csv
Table: src_benchmark_indices

Column	Data Type	Business Definition
date	TEXT	Benchmark reporting date
index_name	TEXT	Benchmark index name
close_value	DOUBLE PRECISION	Index closing value

⸻

Data Sources and References

Dataset	Original File	PostgreSQL Table
Fund Master	01_fund_master.csv	src_fund_master
NAV History	02_nav_history.csv	src_nav_history
AUM by Fund House	03_aum_by_fund_house.csv	src_aum_by_fund_house
Monthly SIP Inflows	04_monthly_sip_inflows.csv	src_monthly_sip_inflows
Category Inflows	05_category_inflows.csv	src_category_inflows
Industry Folio Count	06_industry_folio_count.csv	src_industry_folio_count
Scheme Performance	07_scheme_performance.csv	src_scheme_performance
Investor Transactions	08_investor_transactions.csv	src_investor_transactions
Portfolio Holdings	09_portfolio_holdings.csv	src_portfolio_holdings
Benchmark Indices	10_benchmark_indices.csv	src_benchmark_indices

Technical Notes

* Source datasets are stored in CSV format.
* Data is loaded into PostgreSQL using Python, Pandas and SQLAlchemy.
* Column data types are documented according to the PostgreSQL source tables.
* Date fields are stored as TEXT in the current source tables.
* Percentage fields represent percentage values.
* Monetary values are documented in their respective currencies and units.
* Boolean columns represent validation flags or anomaly indicators.

End of Data Dictionary