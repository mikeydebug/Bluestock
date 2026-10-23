# Mutual Fund Analytics Capstone — Comprehensive Data Dictionary

**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Target Database:** `mutual_fund_capstone/data/db/mutual_funds.db` (SQLite 3)  
**Status:** Validated  

---

## 1. Table: `dim_fund` (Mutual Fund Master Dimension)
Stores metadata for all mutual fund schemes tracked in the analytics engine.

| Column Name | Data Type | Key Type | Nullable | Description / Business Definition | Valid Example |
|---|---|---|---|---|---|
| `fund_id` | INTEGER | PRIMARY KEY | No | Internal surrogate integer primary key | `1` |
| `scheme_code` | INTEGER | UNIQUE | No | Official AMFI 6-digit unique scheme identifier | `118632` |
| `reference_name` | TEXT | None | No | Label referenced in internship instructions | `Nippon Large Cap` |
| `scheme_name` | TEXT | None | No | Official legal title of the fund from AMFI | `Nippon India Large Cap Fund - Direct Growth` |
| `fund_house` | TEXT | None | No | Asset Management Company (AMC) name | `Nippon India Mutual Fund` |
| `category` | TEXT | None | No | SEBI scheme classification | `Large Cap Fund` |
| `expense_ratio` | REAL | None | No | Total Expense Ratio (TER %) | `0.82` |
| `risk_grade` | TEXT | None | No | Risk-o-meter rating | `High` |
| `launch_year` | INTEGER | None | No | Calendar year fund inception occurred | `2013` |

---

## 2. Table: `dim_date` (Calendar & Trading Day Dimension)
Standardized Kimball calendar dimension supporting time-intelligence slicing.

| Column Name | Data Type | Key Type | Nullable | Description / Business Definition | Valid Example |
|---|---|---|---|---|---|
| `date_id` | TEXT | PRIMARY KEY | No | ISO 8601 calendar date (`YYYY-MM-DD`) | `2024-04-15` |
| `year` | INTEGER | None | No | Four-digit calendar year | `2024` |
| `quarter` | INTEGER | None | No | Calendar quarter (1 to 4) | `2` |
| `month` | INTEGER | None | No | Month of the year (1 to 12) | `4` |
| `month_name` | TEXT | None | No | Full English month name | `April` |
| `day` | INTEGER | None | No | Day of the month (1 to 31) | `15` |
| `day_of_week` | INTEGER | None | No | Day index (0=Monday, 6=Sunday) | `0` |
| `is_trading_day`| INTEGER | None | No | 1 if active trading day, 0 if weekend | `1` |

---

## 3. Table: `fact_nav` (Historical Daily NAV Fact Table)
Contains daily sequential Net Asset Values and returns.

| Column Name | Data Type | Key Type | Nullable | Description / Business Definition | Valid Example |
|---|---|---|---|---|---|
| `nav_id` | INTEGER | PRIMARY KEY | No | Surrogate auto-incrementing key | `1042` |
| `fund_id` | INTEGER | FOREIGN KEY | No | References `dim_fund(fund_id)` | `4` |
| `date_id` | TEXT | FOREIGN KEY | No | References `dim_date(date_id)` | `2024-04-15` |
| `nav` | REAL | None | No | Net Asset Value in INR (enforced $>0$) | `97.4783` |
| `daily_return`| REAL | None | Yes | Arithmetic daily return $\frac{NAV_t}{NAV_{t-1}} - 1$ | `0.00292` |

---

## 4. Table: `fact_transactions` (Investor Retail Transactions Fact)
Records client capital movements, SIP orders, and redemption activity.

| Column Name | Data Type | Key Type | Nullable | Description / Business Definition | Valid Example |
|---|---|---|---|---|---|
| `transaction_id`| TEXT | PRIMARY KEY | No | Unique transaction identifier | `TXN-200105` |
| `investor_id` | INTEGER | None | No | Anonymized unique investor identifier | `10452` |
| `fund_id` | INTEGER | FOREIGN KEY | No | References `dim_fund(fund_id)` | `1` |
| `date_id` | TEXT | FOREIGN KEY | No | References `dim_date(date_id)` | `2024-05-10` |
| `trans_type` | TEXT | None | No | Order type: `SIP`, `Lumpsum`, `Redemption` | `SIP` |
| `amount` | REAL | None | No | Transaction value in INR (enforced $>0$) | `5000.00` |
| `units` | REAL | None | No | Mutual fund units allotted or liquidated | `51.2938` |
| `investor_age_group`| TEXT | None | No | Demographic age bracket | `26-35` |
| `investor_gender`| TEXT | None | No | Gender identity: `Male`, `Female`, `Other` | `Female` |
| `investor_state`| TEXT | None | No | State of residence | `Maharashtra` |
| `city_tier` | TEXT | None | No | Market tier: `T30` (Top 30) or `B30` | `T30` |

---

## 5. Table: `fact_aum` (Quarterly AUM and Folio History)
Tracks fund house capital scale and folio expansion over multi-year horizons.

| Column Name | Data Type | Key Type | Nullable | Description / Business Definition | Valid Example |
|---|---|---|---|---|---|
| `aum_id` | INTEGER | PRIMARY KEY | No | Surrogate key | `42` |
| `fund_id` | INTEGER | FOREIGN KEY | No | References `dim_fund(fund_id)` | `3` |
| `date_id` | TEXT | FOREIGN KEY | No | Quarter-end observation date | `2024-06-30` |
| `aum_crores` | REAL | None | No | Total scheme AUM in INR Crores | `24850.50` |
| `folio_count` | INTEGER | None | No | Number of active investor folios | `984500` |
| `net_inflow_crores`| REAL | None | No | Net capital inflows during the quarter | `450.25` |

---

## 6. Table: `fact_performance` (Calculated Quantitative Metrics)
Captures risk-adjusted return attributes and composite scorecard ratings.

| Column Name | Data Type | Key Type | Nullable | Description / Business Definition | Valid Example |
|---|---|---|---|---|---|
| `perf_id` | INTEGER | PRIMARY KEY | No | Surrogate key | `1` |
| `fund_id` | INTEGER | FOREIGN KEY | No | References `dim_fund(fund_id)` | `4` |
| `as_of_date` | TEXT | FOREIGN KEY | No | Calculation effective date | `2026-10-23` |
| `cagr_1y` | REAL | None | Yes | 1-Year Compound Annual Growth Rate (%) | `24.50` |
| `cagr_3y` | REAL | None | Yes | 3-Year Compound Annual Growth Rate (%) | `10.39` |
| `cagr_5y` | REAL | None | Yes | 5-Year Compound Annual Growth Rate (%) | `18.20` |
| `volatility_ann`| REAL | None | No | Annualised standard deviation of returns (%) | `13.70` |
| `sharpe_ratio` | REAL | None | No | Sharpe Ratio ($R_f = 6.5\%$ annualised) | `0.29` |
| `sortino_ratio`| REAL | None | No | Sortino Ratio with downside semideviation | `0.42` |
| `beta` | REAL | None | No | CAPM Beta relative to NIFTY 100 | `-0.035` |
| `alpha` | REAL | None | No | Annualised Jensen's Alpha (%) | `11.84` |
| `max_drawdown` | REAL | None | No | Maximum peak-to-trough decline (%) | `-15.37` |
| `max_dd_peak_date`| TEXT | None | Yes | Date preceding drawdown | `2024-09-27` |
| `max_dd_trough_date`| TEXT | None | Yes | Date of maximum drawdown bottom | `2025-01-14` |
| `fund_score` | REAL | None | No | Composite multi-factor score (0–100) | `95.0` |
| `tracking_error`| REAL | None | Yes | Annualised tracking error vs NIFTY 100 (%) | `13.85` |
