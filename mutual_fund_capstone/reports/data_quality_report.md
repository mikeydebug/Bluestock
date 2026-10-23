# Mutual Fund Analytics Capstone — Data Quality & Integrity Audit

**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Document:** Data Quality Audit & Cleaning Policy  
**Status:** Audit Completed & Certified  

---

## 1. Executive Summary

This report establishes the data quality baseline, validation procedures, and cleaning decisions applied across the mutual fund data pipeline. All raw JSON files received from AMFI (`api.mfapi.in`) have been archived without modification in `mutual_fund_capstone/data/raw/` to preserve complete auditability.

---

## 2. Ingestion & Scheme Resolution Audit

A critical finding was uncovered during live network resolution of the 6 supplied AMFI scheme codes:

| Supplied Code | Reference Name in Instruction | Actual Resolved Legal Title from AMFI API | AMC / Fund House | Category | Discrepancy Analysis |
|---|---|---|---|---|---|
| **125497** | HDFC Top 100 Direct | SBI SMALL CAP FUND - Direct Plan - Growth | SBI Mutual Fund | Small Cap Fund | Mapped to Small Cap instead of Large Cap |
| **119551** | SBI Bluechip | Aditya Birla Sun Life Banking & PSU Debt - IDCW | Aditya Birla Sun Life | Debt Scheme | Mapped to Banking & PSU Debt |
| **120503** | ICICI Bluechip | Axis ELSS- Tax Saver Fund - Direct Plan - Growth | Axis Mutual Fund | ELSS Tax Saver | Mapped to Tax-Saver ELSS |
| **118632** | Nippon Large Cap | Nippon India Large Cap Fund - Direct Plan - Growth | Nippon India MF | Large Cap Fund | **Exact Verified Match** |
| **119092** | Axis Bluechip | HDFC Money Market Fund - Direct Plan - Growth | HDFC Mutual Fund | Money Market Debt | Mapped to Money Market Debt |
| **120841** | Kotak Bluechip | Quant Mid Cap Fund - Direct Plan - Growth | quant Mutual Fund | Mid Cap Fund | Mapped to Mid Cap Equity |

*Governance Decision:* As mandated by project guidelines, the pipeline ingests the authentic data returned by the official API, retains both the configured reference names and resolved fund names, and leverages this multi-category universe (Large Cap, Mid Cap, Small Cap, ELSS, Debt, Money Market) to demonstrate robust cross-asset risk analysis.

---

## 3. Data Transformation & Cleaning Decisions

### 3.1 Non-Trading Days vs. Missing Observations Policy
- **Market Context:** Indian mutual funds only calculate and publish daily closing NAVs on active trading days (excluding Saturdays, Sundays, and official exchange holidays declared by NSE/BSE).
- **Integrity Rule:** Non-trading days are **NOT** imputed via forward-fill in the primary NAV table. Forward-filling artificially suppresses daily return variance and generates zero-return artifacts that distort standard deviation and Sharpe ratios.
- **Return Computation:** Daily arithmetic returns are computed strictly across consecutive observed trading days:
  $$R_t = \frac{NAV_t}{NAV_{t-1}} - 1$$

### 3.2 Row Counts & Data Hygiene Reconciliation

| Dataset Entity | Raw Records Ingested | Duplicates Dropped | Invalid / Non-Positive Records Removed | Clean Records Loaded to SQLite | Data Quality Score |
|---|---|---|---|---|---|
| **NAV Fact (`fact_nav`)** | 20,390 | 0 | 1 ($NAV \le 0$ check) | **20,389** | 99.99% |
| **Investor Transactions** | 5,000 | 0 | 0 | **5,000** | 100.00% |
| **AUM History (`fact_aum`)** | 162 | 0 | 0 | **162** | 100.00% |
| **Fund Master (`dim_fund`)** | 6 | 0 | 0 | **6** | 100.00% |
| **Date Master (`dim_date`)** | 4,330 | 0 | 0 | **4,330** | 100.00% |

---

## 4. Key Data Validation Checks Passed

1. **NAV Positivity Enforcement:** All 20,389 NAV observations satisfy $NAV > 0$. Zero negative or zero-value records permitted.
2. **Key Uniqueness & Foreign Key Constraints:** SQLite `PRAGMA foreign_keys = ON` executed with zero constraint violations. Every transaction and NAV observation maps to a valid `fund_id` and `date_id`.
3. **Transaction Amount Sanity:** All 5,000 transactions have positive amounts ($₹1,000 \le \text{amount} \le ₹500,000$).
4. **Expense Ratio Boundary:** All expense ratios fall within statutory SEBI ceilings ($0.22\% \le \text{TER} \le 0.82\%$).
5. **Finite Metric Values:** All calculated quant metrics (CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown) evaluated to finite real numbers with zero `NaN` or `Inf` errors.
