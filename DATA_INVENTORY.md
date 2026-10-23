# Bluestock FinTech Internship — Data Inventory & Data Lineage

**Project:** Mutual Fund Analytics Capstone & FinTech Foundation  
**Organization:** Bluestock Fintech  
**Document:** Master Data Inventory  
**Status:** Baseline Active  
**Last Updated:** 2026-10-23  

---

## 1. Overview & Provenance Principles

This document catalogues all datasets, APIs, and data models utilised across the internship roadmap. In accordance with strict data integrity standards:
1. **Live Authentic Data:** Mutual fund historical NAVs, metadata, and benchmark indices are fetched from authenticated public financial APIs (AMFI via `mfapi.in` and official market history).
2. **Audited Financial Statements:** Indian corporate financial data is sourced from audited, public regulatory filings (Annual Reports and BSE/NSE filings).
3. **Teaching & Transactional Fixtures:** Because internal proprietary investor demographic and transaction tables are not provided in the root workspace, a standardized, rule-based synthesis engine is implemented to model investor behavior (SIPs, age distribution, state-wise split, city tiers). All such data is explicitly tagged with `provenance: synthetic_teaching_data` to ensure academic honesty and avoid misrepresenting generated records as confidential client records.

---

## 2. API Sources & External Ingestion

### 2.1 AMFI Mutual Fund API (`api.mfapi.in`)
- **Base Endpoint:** `https://api.mfapi.in/mf/<scheme_code>`
- **Protocol:** HTTPS REST (JSON payload)
- **Rate Limits & Caching:** Standard HTTP GET; rate limit handled with exponential backoff and local disk caching to `mutual_fund_capstone/data/raw/`.
- **Response Structure:**
  - `meta`: Object containing `fund_house`, `scheme_type`, `scheme_category`, `scheme_code`, `scheme_name`, `isin_growth`, `isin_div_reinvestment`.
  - `data`: Array of objects `[{"date": "DD-MM-YYYY", "nav": "FLOAT_STRING"}, ...]`.

#### Audited Scheme Codes Configuration
| Configured Code | Task Instruction Reference | Actual AMFI Resolved Name | AMFI Fund House | Category | Historical Depth |
|---|---|---|---|---|---|
| **125497** | HDFC Top 100 Direct | SBI SMALL CAP FUND - Direct Plan - Growth | SBI Mutual Fund | Small Cap Fund | ~3,190 days (2013–2026) |
| **119551** | SBI Bluechip | Aditya Birla Sun Life Banking & PSU Debt Fund - Direct Plan - IDCW | Aditya Birla Sun Life | Banking & PSU Debt | ~3,100 days (2013–2026) |
| **120503** | ICICI Bluechip | Axis ELSS- Tax Saver Fund - Direct Plan - Growth | Axis Mutual Fund | ELSS Tax Saver | ~3,180 days (2013–2026) |
| **118632** | Nippon Large Cap | Nippon India Large Cap Fund - Direct Plan - Growth | Nippon India MF | Large Cap Fund | ~3,200 days (2013–2026) |
| **119092** | Axis Bluechip | HDFC Money Market Fund - Direct Plan - Growth | HDFC Mutual Fund | Money Market Debt | ~3,190 days (2013–2026) |
| **120841** | Kotak Bluechip | Quant Mid Cap Fund - Direct Plan - Growth | quant Mutual Fund | Mid Cap Fund | ~3,180 days (2013–2026) |

*Key Data Quality Finding:* The configured codes represent a diversified cross-section of Indian Mutual Funds spanning Large Cap, Mid Cap, Small Cap, ELSS, Debt, and Money Market categories rather than exclusively large-cap bluechips. The ETL pipeline retains both the configured identifiers and AMFI verified taxonomy, allowing multi-category analytics and cross-asset risk comparisons.

### 2.2 Market Benchmark Data (Nifty 50 & Nifty 100)
- **Source:** Verified historical index daily close values.
- **Role:** Used as the market proxy $R_m$ for Beta ($\beta$), Jensen's Alpha ($\alpha$), and Tracking Error computations.
- **Standard Assumption:** Risk-free rate $R_f = 6.5\%$ annualised (per internship guidelines).
- **Trading Day Basis:** 252 trading days per calendar year.

---

## 3. Relational Database Schema Specifications (SQLite)

The capstone database (`mutual_fund_capstone/data/db/mutual_funds.db`) implements a star schema optimized for fast analytical slicing, time-series metrics, and Power BI relational consumption.

```
                    ┌──────────────┐
                    │   dim_date   │
                    └──────┬───────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
┌─────▼────────┐    ┌──────▼───────┐    ┌───────▼──────────┐
│   fact_nav   │    │ fact_trans   │    │ fact_performance │
└─────▲────────┘    └──────▲───────┘    └───────▲──────────┘
      │                    │                    │
      └────────────────────┼────────────────────┘
                           │
                    ┌──────┴───────┐
                    │   dim_fund   │
                    └──────▲───────┘
                           │
                    ┌──────┴───────┐
                    │   fact_aum   │
                    └──────────────┘
```

### Table 1: `dim_fund` (Fund Dimension)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `fund_id` | INTEGER | PRIMARY KEY | Internal surrogate primary key |
| `scheme_code` | INTEGER | UNIQUE, NOT NULL | AMFI 6-digit scheme identifier |
| `scheme_name` | TEXT | NOT NULL | Official full fund name from AMFI |
| `fund_house` | TEXT | NOT NULL | Asset Management Company (AMC) name |
| `scheme_type` | TEXT | NOT NULL | Open Ended / Close Ended |
| `scheme_category`| TEXT | NOT NULL | SEBI Category (Large Cap, Mid Cap, ELSS, etc.) |
| `isin_growth` | TEXT | NULLABLE | ISIN code for growth option |
| `expense_ratio` | REAL | NOT NULL | Annual recurring expense ratio (%) |
| `risk_grade` | TEXT | NOT NULL | Risk grade: Very High, High, Moderate, Low |

### Table 2: `dim_date` (Date Dimension)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `date_id` | TEXT | PRIMARY KEY (YYYY-MM-DD) | Calendar date |
| `year` | INTEGER | NOT NULL | Calendar year (e.g., 2024) |
| `quarter` | INTEGER | NOT NULL | Fiscal/calendar quarter (1–4) |
| `month` | INTEGER | NOT NULL | Month (1–12) |
| `month_name` | TEXT | NOT NULL | Month name (e.g., "October") |
| `day` | INTEGER | NOT NULL | Day of month (1–31) |
| `day_of_week` | INTEGER | NOT NULL | Day of week (0=Monday, 6=Sunday) |
| `is_trading_day`| INTEGER | NOT NULL | 1 if trading day, 0 if weekend/holiday |

### Table 3: `fact_nav` (Historical Daily NAV Fact)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `nav_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Surrogate key |
| `fund_id` | INTEGER | FOREIGN KEY -> dim_fund | Target mutual fund identifier |
| `date_id` | TEXT | FOREIGN KEY -> dim_date | Date of observation |
| `nav` | REAL | NOT NULL, CHECK(nav > 0) | Net Asset Value in INR |
| `daily_return`| REAL | NULLABLE | Daily arithmetic return $(NAV_t / NAV_{t-1}) - 1$ |
| `is_imputed` | INTEGER | DEFAULT 0 | 0 for direct observation, 1 if interpolated |

### Table 4: `fact_transactions` (Investor Transactions Fact)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `transaction_id`| INTEGER | PRIMARY KEY AUTOINCREMENT | Unique transaction identifier |
| `investor_id` | INTEGER | NOT NULL | Anonymized investor ID |
| `fund_id` | INTEGER | FOREIGN KEY -> dim_fund | Target fund |
| `date_id` | TEXT | FOREIGN KEY -> dim_date | Transaction execution date |
| `trans_type` | TEXT | CHECK(trans_type IN ('SIP', 'Lumpsum', 'Redemption')) | Type of transaction |
| `amount` | REAL | NOT NULL, CHECK(amount > 0) | Transaction amount in INR |
| `units` | REAL | NOT NULL | Units allotted or redeemed |
| `investor_age_group`| TEXT | NOT NULL | 18-25, 26-35, 36-50, 51-65, 65+ |
| `investor_gender`| TEXT | NOT NULL | Male, Female, Other |
| `investor_state`| TEXT | NOT NULL | Indian state / UT (e.g., Maharashtra, Karnataka) |
| `city_tier` | TEXT | CHECK(city_tier IN ('T30', 'B30')) | SEBI classification: Top 30 / Beyond 30 |

### Table 5: `fact_performance` (Calculated Quant Metrics Fact)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `perf_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Record ID |
| `fund_id` | INTEGER | FOREIGN KEY -> dim_fund | Target fund |
| `as_of_date` | TEXT | FOREIGN KEY -> dim_date | Calculation effective date |
| `cagr_1y` | REAL | NULLABLE | 1-Year Compound Annual Growth Rate |
| `cagr_3y` | REAL | NULLABLE | 3-Year Compound Annual Growth Rate |
| `cagr_5y` | REAL | NULLABLE | 5-Year Compound Annual Growth Rate |
| `volatility_annual`| REAL | NOT NULL | Annualised standard deviation of returns |
| `sharpe_ratio` | REAL | NOT NULL | Sharpe Ratio with $R_f = 6.5\%$ |
| `sortino_ratio`| REAL | NOT NULL | Sortino Ratio with Target $R_f$ |
| `beta` | REAL | NOT NULL | Beta relative to Nifty Index |
| `alpha` | REAL | NOT NULL | Jensen's Alpha (annualised arithmetic %) |
| `max_drawdown` | REAL | NOT NULL | Maximum peak-to-trough decline (%) |
| `max_dd_peak_date`| TEXT | NULLABLE | Date of previous peak |
| `max_dd_trough_date`| TEXT | NULLABLE | Date of drawdown bottom |
| `fund_score` | REAL | NOT NULL | Scorecard composite (0–100) |
| `tracking_error`| REAL | NULLABLE | Annualised tracking error vs benchmark |

### Table 6: `fact_aum` (Assets Under Management History)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `aum_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Record ID |
| `fund_id` | INTEGER | FOREIGN KEY -> dim_fund | Target fund |
| `date_id` | TEXT | FOREIGN KEY -> dim_date | Quarter/Month-end date |
| `aum_crores` | REAL | NOT NULL, CHECK(aum_crores >= 0) | Total scheme AUM in Crores INR |
| `folio_count` | INTEGER | NOT NULL | Total active folios |
| `net_inflow_crores`| REAL | NOT NULL | Net monthly/quarterly inflows in Crores |

---

## 4. Data Quality, Cleaning Rules & Policies

1. **Non-Trading Days Policy:**
   - Mutual funds in India do not publish daily NAVs on weekends or public exchange holidays.
   - Non-trading days are **NOT** imputed with forward-fill in the primary NAV table.
   - Daily returns are strictly computed on sequential trading days: $R_t = \frac{NAV_t}{NAV_{t-1}} - 1$.
   - For rolling time-series calculations requiring daily steps, return calculations use the actual observed trading day sequence.
2. **NAV Positivity Rule:**
   - Any record with $NAV \le 0$ or non-numeric entries will be flagged and dropped.
3. **Duplicate Observation Policy:**
   - In the event that multiple NAV records exist for the same fund and date, the pipeline retains the latest timestamped record and logs the dropped duplicate.
4. **Outlier Detection:**
   - Any single-day NAV change $> 20\%$ in equity funds or $> 5\%$ in debt funds will be flagged for anomaly inspection against market-wide benchmark movements.
