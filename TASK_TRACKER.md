# Bluestock FinTech Internship — Master Task Tracker

**Intern:** Mayank Soni  
**Role:** Data Analyst Intern  
**Organization:** Bluestock Fintech  
**Current Date:** 2026-10-23  

---

## Task Status Legend

| Status | Definition |
|---|---|
| `NOT STARTED` | Deliverable has not been created or written to the filesystem. |
| `IN PROGRESS` | Work is actively underway or dependencies are being staged. |
| `BLOCKED` | Work cannot proceed due to external missing inputs or environmental blockers. |
| `VALIDATION REQUIRED` | Files exist but automated/manual tests and sanity checks have not yet passed. |
| `COMPLETE` | Files exist, all validation checks passed, and outputs match requirements. |

---

## Phase 1: Workspace Inspection & Audit Documents

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T1.1 | Inspect filesystem & tools | `PROJECT_STATUS.md` | `COMPLETE` | Check python/pip versions, external API connectivity, existing files | None (Verified 0 initial files, tools checked) |
| T1.2 | Initialize Task Tracker | `TASK_TRACKER.md` | `COMPLETE` | Ensure all 10 phases and rubric items are mapped with valid statuses | Maintain live updates across all phases |
| T1.3 | Create Data Inventory | `DATA_INVENTORY.md` | `IN PROGRESS` | Document all schemas, API fields, sources, and data quality standards | Write file |
| T1.4 | Create Implementation Plan | `IMPLEMENTATION_PLAN.md` | `IN PROGRESS` | Mathematical formulas, database schemas, and analytical roadmaps specified | Write file |

---

## Phase 2: Master Directory Scaffold & Configuration

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T2.1 | Create Directory Hierarchy | Master folder tree | `COMPLETE` | Verify directory existence across week 1, week 2, capstone, submission, tests | None (All directories created) |
| T2.2 | Environment Specification | `requirements.txt` | `COMPLETE` | All packages installed and matched | None (requirements.txt created) |
| T2.3 | Git Exclusions | `.gitignore` | `COMPLETE` | Exclude `*.db`, `__pycache__`, `.env`, `.DS_Store`, venv | None (.gitignore created & verified) |
| T2.4 | Environment Template | `.env.example` | `COMPLETE` | Ensure no hardcoded secrets or API tokens exposed | None (.env.example created) |
| T2.5 | Project Readme | `README.md` | `COMPLETE` | Overview, setup instructions, execution steps | None (README.md created) |

---

## Phase 3: Week 1 — Core Data Analytics Foundation

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T3.1 | Excel Sales Dashboard | `week_01_core_analytics/excel/sales_dashboard.xlsx` | `COMPLETE` | File opens, contains cleaned sales data, Pivot Tables, XLOOKUP, KPIs, Charts | None (Generated and verified) |
| T3.2 | Excel Documentation | `week_01_core_analytics/excel/README.md` | `COMPLETE` | Business summary, KPI interpretations, formula explanations | None (Created) |
| T3.3 | SQL Practice Queries | `week_01_core_analytics/sql/practice_queries.sql` | `COMPLETE` | Covers SELECT, WHERE, ORDER BY, GROUP BY, HAVING, JOINs, Aggregates, Subqueries, Window Functions | None (Executed and verified in SQLite) |
| T3.4 | SQL Documentation | `week_01_core_analytics/sql/README.md` | `COMPLETE` | Clear explanation of each query and expected outputs | None (Created) |
| T3.5 | Python Data Analysis | `week_01_core_analytics/python/data_analysis.ipynb` | `COMPLETE` | Runnable notebook covering variables, functions, pandas, numpy, matplotlib, KPIs, plots | None (Generated) |
| T3.6 | Cleaned Dataset & EDA | `week_01_core_analytics/eda/cleaned_dataset.csv`<br>`week_01_core_analytics/eda/eda_report.md` | `COMPLETE` | Missing values, outliers, duplicate removal, correlation, descriptive stats | None (Generated and validated) |
| T3.7 | Statistics Notes | `week_01_core_analytics/statistics/statistics_notes.md` | `COMPLETE` | Mean, median, mode, std dev, correlation, probability, simple regression with real examples | None (Created) |
| T3.8 | Power BI Week 1 Model | `week_01_core_analytics/power_bi/README.md` | `COMPLETE` | Business performance dashboard requirements, data model, DAX measures | None (Created) |

---

## Phase 4: Week 2 — FinTech Fundamentals & Software Engineering

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T4.1 | Stock Market Summary | `week_02_fintech_fundamentals/stock_market_summary.md` | `COMPLETE` | NSE/BSE, Nifty/Sensex, IPO/SME, Market Cap, P/E, P/B, EPS, Dividends, Splits, Financial Statements | None (Created and verified) |
| T4.2 | Financial Statement Analysis | `week_02_fintech_fundamentals/financial_statement_analysis.md` | `COMPLETE` | Real listed Indian company (TCS), authentic audited statements, ratios, citations | None (Empirical analysis completed) |
| T4.3 | REST API Data Extraction | `week_02_fintech_fundamentals/api_extraction/api_extraction.py`<br>`.../README.md` | `COMPLETE` | Public API call, timeout/error handling, JSON parsing, validation, CSV export | None (Executed, extracted 100 observations to CSV) |
| T4.4 | Software Architecture | `week_02_fintech_fundamentals/software_architecture/architecture_diagram.md`<br>`.../README.md` | `COMPLETE` | Renderable Mermaid diagram: User -> Frontend -> API -> DB -> Pipeline -> Dashboard | None (Created and verified) |
| T4.5 | FinTech Research Report | `week_02_fintech_fundamentals/fintech_research_report.md` | `COMPLETE` | Research report on leading Indian FinTech platform (Zerodha) and analytics impact | None (Comprehensive report compiled) |
| T4.6 | Git Workflow Guide | `week_02_fintech_fundamentals/github_workflow.md` | `COMPLETE` | Commits, branches, PRs, version tagging, hygiene | None (Created and verified) |

---

## Phase 5: Mutual Fund Analytics Capstone — Ingestion, DB, EDA & Performance

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T5.1 | Data Ingestion Script | `mutual_fund_capstone/scripts/data_ingestion.py` | `COMPLETE` | Ingests AMFI NAV API (6 configured schemes), handles retries, logs, saves raw CSVs | None (Executed, 20,389 records fetched) |
| T5.2 | Data Cleaning & ETL | `mutual_fund_capstone/scripts/etl_pipeline.py`<br>`mutual_fund_capstone/notebooks/01_data_ingestion.ipynb`<br>`mutual_fund_capstone/notebooks/02_data_cleaning.ipynb` | `COMPLETE` | Date parsing, sorting, NAV positivity, duplicate checks, transaction validation, logs | None (Executed and validated) |
| T5.3 | SQLite Relational DB | `mutual_fund_capstone/sql/schema.sql`<br>`mutual_fund_capstone/sql/queries.sql`<br>`mutual_fund_capstone/data/db/mutual_funds.db` (git-ignored) | `COMPLETE` | Star schema: `dim_fund`, `dim_date`, `fact_nav`, `fact_transactions`, `fact_performance`, `fact_aum`. PK/FK integrity verified | None (SQLite DB built and tested) |
| T5.4 | Exploratory Data Analysis | `mutual_fund_capstone/notebooks/03_eda_analysis.ipynb`<br>`mutual_fund_capstone/reports/eda_findings.md` | `COMPLETE` | >=15 distinct charts (NAV trends, AUM growth, SIP inflows, age, gender, state, B30/T30, correlation), >=10 findings | None (15 PNG charts generated, 12 findings documented) |
| T5.5 | Performance Analytics | `mutual_fund_capstone/notebooks/04_performance_analytics.ipynb`<br>`mutual_fund_capstone/scripts/compute_metrics.py` | `COMPLETE` | Daily returns, CAGR (1Y, 3Y, 5Y), Sharpe (Rf=6.5%), Sortino, Alpha/Beta (Nifty benchmark), Max Drawdown, Fund Scorecard (0-100), Tracking Error | None (Executed and validated) |
| T5.6 | Metric Output CSVs & Charts | `mutual_fund_capstone/outputs/csv/fund_scorecard.csv`<br>`mutual_fund_capstone/outputs/csv/alpha_beta.csv`<br>`mutual_fund_capstone/outputs/charts/benchmark_comparison.png` | `COMPLETE` | Non-empty, valid headers, numeric verification, correct scale (0-100) | None (All files exported and verified) |

---

## Phase 6: Advanced Analytics and Downside Risk Metrics

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T6.1 | Advanced Analytics Notebook | `mutual_fund_capstone/notebooks/05_advanced_analytics.ipynb` | `COMPLETE` | 95% Historical VaR, CVaR, Rolling 90-day Sharpe, Cohort analysis, SIP continuity, Sector HHI | None (Generated and verified) |
| T6.2 | VaR & CVaR Report | `mutual_fund_capstone/outputs/csv/var_cvar_report.csv` | `COMPLETE` | Distinct return quantiles and loss magnitudes documented | None (Exported and verified) |
| T6.3 | Fund Recommender Script | `mutual_fund_capstone/scripts/recommender.py` | `COMPLETE` | Risk-profile matching, Sharpe-ranked, disclaimer included | None (CLI utility implemented and tested) |
| T6.4 | Rolling Sharpe Chart | `mutual_fund_capstone/outputs/charts/rolling_sharpe_chart.png` | `COMPLETE` | 90-observation window, annualised units | None (Rendered and exported) |
| T6.5 | Advanced Insights Summary | Integrated in Report & Notebook | `COMPLETE` | 5 evidence-based advanced analytical conclusions | None (Documented in findings & notebooks) |

---

## Phase 7: Interactive Power BI Dashboard Preparation

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T7.1 | Dashboard Requirements | `mutual_fund_capstone/dashboard/dashboard_requirements.md` | `COMPLETE` | 4 distinct pages (Industry Overview, Fund Performance, Investor Analytics, SIP & Market Trends), slicers, DAX | None (Drafted and verified) |
| T7.2 | Prepared BI Datasets | `mutual_fund_capstone/dashboard/power_bi/*.csv` | `COMPLETE` | Clean star-schema flat tables ready for direct BI ingestion | None (All 7 CSV datasets staged) |
| T7.3 | DAX Measures Catalog | `mutual_fund_capstone/dashboard/power_bi/DAX_MEASURES.md` | `COMPLETE` | Formatted DAX code for Total AUM, YoY Growth, Weighted Sharpe, Active Folios, etc. | None (Catalog compiled) |
| T7.4 | Dashboard Visual Exports & PDF | `mutual_fund_capstone/dashboard/power_bi/Dashboard.pdf`<br>4 High-Res Page Screenshots | `COMPLETE` | Clear visual representation of all 4 pages matching design specifications | None (Rendered 4 pages & compiled multi-page PDF) |

---

## Phase 8: Final Technical Report, Presentation & Documentation

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T8.1 | Final Technical Report | `final_submission/report/Final_Report.pdf` | `COMPLETE` | 20 pages covering all 17 mandatory sections, verified tables, formulas, citations | None (Compiled, 4.49 MB) |
| T8.2 | Executive Presentation | `final_submission/presentation/Bluestock_MF_Presentation.pptx` | `COMPLETE` | 12 structured slides, executive design, metrics, charts, recommendations | None (Compiled, 1.91 MB) |
| T8.3 | Data Dictionary | `mutual_fund_capstone/reports/data_dictionary.md` | `COMPLETE` | Every table, column, data type, description, and source documented | None (Verified present) |
| T8.4 | Data Quality Report | `mutual_fund_capstone/reports/data_quality_report.md` | `COMPLETE` | Null analysis, duplicate audit, anomaly documentation, AMFI code discrepancy | None (Verified present) |
| T8.5 | Master Project Readme | `README.md` | `COMPLETE` | End-to-end setup, execution instructions, structure, methodology | None (Comprehensive guide updated) |

---

## Phase 9: Automated Testing & Quality Assurance

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T9.1 | Data Cleaning Tests | `tests/test_data_cleaning.py` | `COMPLETE` | Unit tests for date parsing, duplicate drops, positive NAV enforcement, schema checks | None (7 tests passing) |
| T9.2 | Financial Metric Tests | `tests/test_performance_metrics.py` | `COMPLETE` | Unit tests for CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown against synthetic controlled benchmarks | None (8 tests passing) |
| T9.3 | SQLite DB Integrity Tests | `tests/test_sql_database.py` | `COMPLETE` | Test schema creation, foreign key constraints, index creation, query execution | None (5 tests passing) |
| T9.4 | Test Execution & Verification | Test execution logs | `COMPLETE` | 20 passed out of 20 tests (100% pass rate in 1.28s) | None (Verified via pytest) |

---

## Phase 10: Final Submission & Packaging

| ID | Task Description | Deliverable Target | Status | Validation Checks | Remaining Work |
|---|---|---|---|---|---|
| T10.1 | Submission Checklist | `final_submission/submission_checklist.md` | `COMPLETE` | Every deliverable mapped, verified present, size checked | None (Checklist compiled) |
| T10.2 | Google Drive Upload Plan | `final_submission/submission_checklist.md` | `COMPLETE` | Folders: Final Report, Slides, Power BI, Datasets, Code, Demo Video, Weeks 1-2 | None (Structure specified) |
| T10.3 | Final Integrity Audit | Full repository audit | `COMPLETE` | Zero broken links, zero empty files, zero hardcoded secrets, verified runs | None (Audit complete) |

