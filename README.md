# Bluestock FinTech Internship — Master Project Repository

**Intern:** Mayank Soni (B.Tech Computer Science)  
**Organization:** Bluestock Fintech  
**Role:** Data Analyst Intern  
**Project:** Mutual Fund Analytics Capstone & FinTech Engineering  
**Academic Year:** 2026  

---

## 1. Project Overview

This repository contains the complete portfolio of work for the **Bluestock FinTech Data Analytics Internship**, encompassing:
1. **Week 1 — Core Data Analytics Foundation:** Advanced Excel modeling, SQL analytics suite, Python numerical processing, exploratory data analysis, and statistical theory.
2. **Week 2 — FinTech Fundamentals & Software Engineering:** Capital markets mechanisms, real audited financial statement analysis (Reliance Industries), robust REST API extraction, modular software architecture design, and FinTech industry research.
3. **Mutual Fund Analytics Capstone Project:** End-to-end quantitative analytics engine featuring:
   - Automated ingestion of historical daily NAVs from AMFI (`api.mfapi.in`) across equity, debt, and hybrid funds.
   - Robust ETL pipelines with schema enforcement and anomaly filtering.
   - Relational star schema database in SQLite with primary/foreign keys and indexing.
   - Comprehensive exploratory data analysis (EDA) with 15+ visualizations.
   - Financial quantitative analytics: CAGR (1Y, 3Y, 5Y), Sharpe, Sortino, Alpha, Beta, Maximum Drawdown, and a 0–100 Multi-Factor Fund Scorecard.
   - Downside risk modeling: Historical 95% VaR, Conditional VaR (CVaR), and Rolling 90-Day Sharpe ratios.
   - Behavioral analytics: Investor cohort analysis, SIP continuity tracking, and Sector HHI concentration.
4. **Interactive Power BI Business Intelligence:** 4-page executive dashboard data model, DAX calculation library, visual exports, and presentation pack.
5. **Executive Deliverables & Verification:** 15–20 page comprehensive PDF report, 12-slide executive presentation (`.pptx`), automated `pytest` test suite, and structured submission checklist.

---

## 2. Master Repository Structure

```
Bluestock_FinTech/
├── README.md                           # Master Project Documentation
├── requirements.txt                    # Python Dependencies
├── .gitignore                          # Git Exclusions (including *.db)
├── .env.example                        # Environment Configuration Template
├── PROJECT_STATUS.md                   # Real-time Project Status Audit
├── TASK_TRACKER.md                     # Comprehensive Task & Deliverable Tracker
├── DATA_INVENTORY.md                   # Datasets, API Endpoints, and Schema Specs
├── IMPLEMENTATION_PLAN.md              # Technical Architecture & Math Formulations
│
├── week_01_core_analytics/             # Week 1: Foundations
│   ├── excel/
│   │   ├── sales_dashboard.xlsx        # Excel Sales Model with Pivot Tables & Formulas
│   │   └── README.md                   # Excel Workbook Documentation
│   ├── sql/
│   │   ├── practice_queries.sql        # Advanced SQL Practice Suite
│   │   └── README.md                   # SQL Exercises Guide & Query Explanations
│   ├── python/
│   │   └── data_analysis.ipynb         # Python Data Analysis Jupyter Notebook
│   ├── eda/
│   │   ├── cleaned_dataset.csv         # Cleaned Sales & Customer Dataset
│   │   └── eda_report.md               # Empirical EDA Findings Report
│   ├── power_bi/
│   │   └── README.md                   # Power BI Business Performance Requirements
│   └── statistics/
│       └── statistics_notes.md         # Descriptive & Inferential Statistics Guide
│
├── week_02_fintech_fundamentals/       # Week 2: FinTech Domain & Engineering
│   ├── stock_market_summary.md         # Capital Markets & Valuation Fundamentals
│   ├── financial_statement_analysis.md # Audited Statement Analysis of Reliance Industries
│   ├── api_extraction/
│   │   ├── api_extraction.py           # Resilient REST API Data Ingestion Script
│   │   └── README.md                   # API Script Documentation
│   ├── software_architecture/
│   │   ├── architecture_diagram.md     # System Flow Architecture & Mermaid Diagram
│   │   └── README.md                   # Architecture Component Explanations
│   ├── fintech_research_report.md      # In-Depth FinTech Platform Research Report
│   └── github_workflow.md              # Git & GitHub Team Collaboration Guide
│
├── mutual_fund_capstone/               # Capstone: Mutual Fund Analytics Engine
│   ├── data/
│   │   ├── raw/                        # Raw Ingested API Data & Source CSVs
│   │   ├── processed/                  # Cleaned, Validated CSV Datasets
│   │   ├── external/                   # Market Benchmarks (Nifty 50, Nifty 100)
│   │   └── db/                         # SQLite Database (git-ignored)
│   ├── notebooks/
│   │   ├── 01_data_ingestion.ipynb     # Ingestion & API Extraction Notebook
│   │   ├── 02_data_cleaning.ipynb      # ETL & Database Loading Notebook
│   │   ├── 03_eda_analysis.ipynb       # 15+ Visual EDA Analyses
│   │   ├── 04_performance_analytics.ipynb # Quantitative Metrics & Scorecard
│   │   └── 05_advanced_analytics.ipynb # Downside Risk (VaR/CVaR, Rolling Sharpe)
│   ├── scripts/
│   │   ├── data_ingestion.py           # Automated NAV & Benchmark Fetcher
│   │   ├── etl_pipeline.py             # Data Transformation & DB Loader
│   │   ├── compute_metrics.py          # Quant Metric & Scorecard Engine
│   │   ├── recommender.py              # Risk-Profile Fund Recommendation Engine
│   │   └── run_pipeline.py             # Master End-to-End Execution CLI
│   ├── sql/
│   │   ├── schema.sql                  # Relational Star Schema DDL
│   │   └── queries.sql                 # Production Analytical SQL Queries
│   ├── reports/
│   │   ├── data_dictionary.md          # Comprehensive Data Dictionary
│   │   ├── data_quality_report.md      # Data Validation & Quality Audit
│   │   ├── eda_findings.md             # 10+ Evidence-Based EDA Findings
│   │   └── methodology.md              # Mathematical Methodology & Assumptions
│   ├── outputs/
│   │   ├── csv/                        # Exported Scorecards & Metric Reports
│   │   ├── charts/                     # Generated High-Resolution Visualizations
│   │   └── tables/                     # Formatted Markdown/HTML Summary Tables
│   └── dashboard/
│       ├── dashboard_requirements.md   # 4-Page Power BI Specification
│       └── power_bi/                   # Prepared BI CSVs, DAX Library, Exports
│
├── final_submission/                   # Submission Package & Executive Artifacts
│   ├── report/
│   │   └── Final_Report.pdf            # 15–20 Page Formal Capstone Report
│   ├── presentation/
│   │   └── Bluestock_MF_Presentation.pptx # 12-Slide Executive PowerPoint Deck
│   ├── dashboard_exports/              # High-Res Dashboard Page Renders
│   ├── submission_checklist.md         # Final Verification & Audit Checklist
│   └── ...                             # Source code & documentation bundles
│
└── tests/                              # Automated Verification Suite
    ├── test_data_cleaning.py           # Unit Tests for ETL & Cleaners
    ├── test_performance_metrics.py     # Unit Tests for CAGR, Sharpe, Alpha, etc.
    └── test_sql_database.py            # Unit Tests for SQLite Schema & Constraints
```

---

## 3. Getting Started & Environment Setup

### 3.1 Prerequisites
- Python 3.9+ (Verified with Python 3.9.6 on macOS)
- `pip` package manager
- SQLite3 (built into Python standard library)

### 3.2 Installation
Clone or navigate to the repository directory and install the required dependencies:
```bash
cd /Users/mayanksoni/Desktop/Bluestock_FinTech
pip install -r requirements.txt
```

### 3.3 Running the End-to-End Capstone Pipeline
Execute the automated master pipeline script to fetch data, perform ETL, load the SQLite database, compute quantitative metrics, and export reports:
```bash
python3 mutual_fund_capstone/scripts/run_pipeline.py
```

### 3.4 Running Automated Tests
Run the verification test suite using `pytest`:
```bash
pytest tests/ -v
```

---

## 4. Key Financial Methodology & Formulas

- **Daily Return:** $R_t = \frac{NAV_t}{NAV_{t-1}} - 1$
- **Compound Annual Growth Rate (CAGR):** $\text{CAGR} = \left(\frac{NAV_{\text{end}}}{NAV_{\text{start}}}\right)^{1/Y} - 1$
- **Sharpe Ratio:** $\frac{R_{\text{ann}} - 6.5\%}{\sigma_{\text{ann}}}$
- **Sortino Ratio:** $\frac{R_{\text{ann}} - 6.5\%}{\sigma_{\text{downside, ann}}}$
- **Alpha & Beta:** Linear regression $R_{\text{fund}} = \alpha + \beta R_{\text{market}} + \epsilon$ using `scipy.stats.linregress`
- **Max Drawdown:** $\min_t \left( \frac{NAV_t}{\max_{\tau \le t} NAV_\tau} - 1 \right)$
- **Fund Scorecard (0–100):** Weighted composite of 3Y Return (30%), Sharpe (25%), Alpha (20%), Inverse Expense Ratio (15%), and Inverse Max Drawdown (10%).

---

## 5. Academic Honesty & Data Governance
- All mutual fund NAVs and market indices are sourced from official public endpoints.
- Corporate financial figures are referenced from audited regulatory filings of listed companies.
- Synthetic retail investor transaction datasets are explicitly identified as educational fixtures to demonstrate scalable database and BI modeling without claiming to be proprietary Bluestock client records.
