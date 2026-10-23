# Bluestock FinTech Internship — Master Technical Implementation Plan

**Intern:** Mayank Soni (B.Tech Computer Science)  
**Organization:** Bluestock Fintech  
**Document:** Master Technical Architecture & Implementation Plan  
**Target Submission:** Fully Validated End-to-End Project  

---

## 1. System Architecture Overview

The system implements an enterprise-grade analytics pipeline following modern data engineering and quantitative finance best practices:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION LAYER                            │
│  - AMFI REST API (mfapi.in) for historical daily mutual fund NAVs       │
│  - National Stock Exchange (NSE) historical benchmark index feeds     │
│  - Retail & HNI transactional behavioral simulation engine             │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Raw JSON & CSVs
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA CLEANING & ETL LAYER                       │
│  - Schema validation, type coercion, date normalization (ISO 8601)     │
│  - Anomaly filtering (NAV > 0, duplicate dropping, outlier audits)     │
│  - Multi-tier storage: raw/ -> processed/                              │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Cleaned relational tables
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        RELATIONAL DATABASE LAYER                       │
│  - SQLite 3 Star Schema: dim_fund, dim_date, fact_nav,                 │
│    fact_transactions, fact_performance, fact_aum                       │
│  - Enforced primary keys, foreign keys, and B-tree indexes             │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ SQL Queries & DataFrames
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        ANALYTICS & QUANT ENGINE                        │
│  - Returns, CAGR (1Y, 3Y, 5Y), Sharpe, Sortino, Alpha, Beta, Max DD    │
│  - 0–100 Weighted Fund Scorecard, Tracking Error                       │
│  - Downside Risk: 95% Historical VaR, CVaR, Rolling 90-Day Sharpe     │
│  - Cohort analysis, SIP continuity, Herfindahl-Hirschman Index (HHI)   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Exported Datasets, Visuals & Schematics
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   PRESENTATION & REPORTING LAYER                       │
│  - 4-Page Power BI Star Schema Model, Slicers & Comprehensive DAX      │
│  - 15–20 Page Formal Comprehensive PDF Report (ReportLab)              │
│  - 12-Slide High-Impact Executive Presentation (python-pptx)           │
│  - Automated Test Suite with pytest                                    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Quantitative Methodology & Mathematical Formulations

### 2.1 Daily Arithmetic Returns
For each individual mutual fund scheme $i$, sorted strictly in ascending chronological order:
$$R_{i, t} = \frac{NAV_{i, t}}{NAV_{i, t-1}} - 1$$
*Rule:* Daily returns are calculated within fund boundaries; no cross-fund boundary calculations.

### 2.2 Compound Annual Growth Rate (CAGR)
For multi-year holding periods (1-Year, 3-Year, 5-Year):
$$\text{CAGR} = \left(\frac{NAV_{\text{end}}}{NAV_{\text{start}}}\right)^{\frac{1}{Y}} - 1$$
where $Y$ is the exact elapsed time in years:
$$Y = \frac{\text{Calendar Days Between End and Start}}{365.25}$$
*Sanity Constraint:* If available history $N < 252 \times Y$, the corresponding multi-year metric is marked `NaN` rather than extrapolating artificially.

### 2.3 Annualised Volatility
$$\sigma_{\text{ann}} = \sigma_{\text{daily}} \times \sqrt{252}$$
where $\sigma_{\text{daily}}$ is the sample standard deviation of daily arithmetic returns:
$$\sigma_{\text{daily}} = \sqrt{\frac{1}{N-1} \sum_{t=1}^N (R_t - \bar{R})^2}$$

### 2.4 Sharpe Ratio
Measures excess risk-adjusted return over the risk-free benchmark:
$$\text{Sharpe Ratio} = \frac{R_{\text{ann}} - R_f}{\sigma_{\text{ann}}}$$
- **Benchmark Risk-Free Rate:** $R_f = 6.5\%$ (0.065 annualised), as mandated by project requirements.
- **Annualised Return:** $R_{\text{ann}} = (1 + \bar{R}_{\text{daily}})^{252} - 1$ (or arithmetic $\bar{R}_{\text{daily}} \times 252$, documented consistently).

### 2.5 Sortino Ratio
Penalises only harmful downside volatility below the Minimum Acceptable Return (MAR = $R_{f, \text{daily}}$):
$$\text{Sortino Ratio} = \frac{R_{\text{ann}} - R_f}{\sigma_{\text{downside, ann}}}$$
where downside deviation is defined over all observations $N$:
$$\sigma_{\text{downside, daily}} = \sqrt{\frac{1}{N} \sum_{t=1}^N \min(0, R_t - \text{MAR})^2}, \quad \sigma_{\text{downside, ann}} = \sigma_{\text{downside, daily}} \times \sqrt{252}$$

### 2.6 Alpha ($\alpha$) and Beta ($\beta$) via CAPM Linear Regression
Using Ordinary Least Squares (OLS) via `scipy.stats.linregress` on aligned fund and market benchmark daily returns:
$$R_{\text{fund}, t} = \alpha_{\text{daily}} + \beta \times R_{\text{market}, t} + \epsilon_t$$
- **Beta ($\beta$):** Measures systematic market risk (slope of the regression line).
- **Annualised Jensen's Alpha:** Arithmetic conversion:
  $$\alpha_{\text{ann}} = \alpha_{\text{daily}} \times 252 \times 100 \quad (\text{expressed as percentage})$$

### 2.7 Maximum Drawdown (MDD)
Evaluates peak-to-trough capital impairment over the observation horizon:
$$\text{Drawdown}_t = \frac{NAV_t}{\max_{\tau \le t} (NAV_\tau)} - 1$$
$$\text{Max Drawdown} = \min_{t} (\text{Drawdown}_t)$$
The algorithm tracks:
- **Peak Date:** Date when the historical running maximum was set prior to the trough.
- **Trough Date:** Date when the minimum drawdown occurred.

### 2.8 Tracking Error (TE)
Measures the consistency of excess returns relative to the benchmark:
$$\text{Tracking Error} = \sqrt{\frac{1}{N-1} \sum_{t=1}^N \left( (R_{\text{fund}, t} - R_{\text{benchmark}, t}) - \overline{\Delta R} \right)^2} \times \sqrt{252}$$

### 2.9 Multi-Factor Fund Scorecard (0–100 Composite)
Implements the rubric's weighted multi-attribute ranking:
$$\text{Raw Score} = 0.30 \times \text{Rank}_{3Y} + 0.25 \times \text{Rank}_{\text{Sharpe}} + 0.20 \times \text{Rank}_{\text{Alpha}} + 0.15 \times \text{Rank}_{\text{ExpRatio}}^{-1} + 0.10 \times \text{Rank}_{\text{MaxDD}}^{-1}$$
- Ranks are normalised across the fund universe to a percentile scale $P \in [0, 100]$.
- Higher return, higher Sharpe, and higher Alpha receive higher ranks (better).
- Lower expense ratio and shallower maximum drawdown (smaller loss) receive higher inverse ranks (better).
- Final scores are scaled from $0$ to $100$.

### 2.10 Downside Risk: Value at Risk (VaR) & Conditional VaR (CVaR)
- **Historical 95% Daily VaR (Signed Return Quantile):**
  $$\text{VaR}_{95\%} = \text{Percentile}(R, 5)$$
- **Loss Magnitude VaR:**
  $$\text{VaR}_{\text{loss}} = - \text{VaR}_{95\%}$$
- **Conditional Value at Risk (CVaR / Expected Shortfall):**
  $$\text{CVaR}_{95\%} = \mathbb{E}\left[ R \mid R \le \text{VaR}_{95\%} \right]$$

### 2.11 Sector Concentration (Herfindahl-Hirschman Index - HHI)
$$\text{HHI} = \sum_{k=1}^K s_k^2$$
where $s_k$ is the percentage allocation to sector $k$ ($0 \le s_k \le 100$).
- $\text{HHI} < 1500$: Diversified
- $1500 \le \text{HHI} \le 2500$: Moderate concentration
- $\text{HHI} > 2500$: Highly concentrated

---

## 3. Power BI Four-Page Design Architecture

1. **Page 1: Industry & AMC Landscape**
   - KPI Cards: Total Industry AUM (₹ Cr), Monthly SIP Inflows (₹ Cr), Active Folios (Cr), Registered Schemes Count.
   - Area Chart: 5-Year Industry AUM Growth Trend.
   - Bar Chart: Market Share by Top Fund Houses (SBI, ICICI, HDFC, Nippon, Axis, Quant).
   - Slicers: Fiscal Year, AMC, Scheme Type.

2. **Page 2: Scheme Performance & Risk-Return Profiling**
   - Scatter Plot: Risk vs. Return (X-Axis: Annualised Volatility %, Y-Axis: 3-Year CAGR %, Bubble Size: AUM).
   - Dynamic Table / Matrix: Fund Scorecard (Rank, Scheme Name, Category, 3Y Return, Sharpe, Alpha, Expense Ratio, Final Score).
   - Line Chart: Normalized NAV Performance vs. Nifty 50 and Nifty 100 (Rebased to 100).
   - Slicers: Scheme Category, Risk Grade, Fund House.

3. **Page 3: Investor Demographics & Retail Behavior**
   - Map / Clustered Bar: State-wise Investment Distribution (Maharashtra, Gujarat, Karnataka, etc.).
   - Donut Chart: Transaction Type Split (SIP vs. Lumpsum vs. Redemption).
   - Grouped Bar: Average Ticket Size & Monthly Inflow by Age Bracket (18–25, 26–35, 36–50, 51–65, 65+).
   - Split Tile: Geographic Inflows (T30 Metro vs. B30 Emerging Markets).
   - Slicers: State, Age Group, City Tier (T30/B30).

4. **Page 4: SIP Persistence & Market Correlation Dynamics**
   - Dual-Axis Combo Chart: Monthly SIP Inflow (₹ Cr) vs. Nifty 50 Index Close.
   - Inflow Heatmap: Month vs. Category Inflow intensity.
   - Horizontal Bar: Net Inflow by Category (Equity, Hybrid, Debt, Solution-Oriented).
   - Slicers: Calendar Year, Inflow Bracket.

---

## 4. Execution Sequence & Phase Progression

- **Step 1:** Phase 1 — Complete Audit Documents (`PROJECT_STATUS.md`, `TASK_TRACKER.md`, `DATA_INVENTORY.md`, `IMPLEMENTATION_PLAN.md`).
- **Step 2:** Phase 2 — Scaffold master folder tree, generate `requirements.txt`, `.gitignore`, `.env.example`, `README.md`.
- **Step 3:** Phase 3 — Week 1 Core Analytics (Excel dashboard with formulas & charts, SQL practice suite, Python notebook, EDA report, statistics guide, Power BI model).
- **Step 4:** Phase 4 — Week 2 FinTech Fundamentals (Stock market guide, real listed financial statement analysis of Reliance Industries / TCS, REST API extraction script, system architecture diagram, FinTech platform research paper, Git workflow).
- **Step 5:** Phase 5 — Mutual Fund Capstone Data Pipeline (Live ingestion from AMFI, ETL cleaning, SQLite star schema database, EDA notebook with >=15 charts & >=10 findings, quantitative performance engine with scorecard & benchmark comparisons).
- **Step 6:** Phase 6 — Advanced Analytics & Downside Risk (95% VaR, CVaR, Rolling 90-day Sharpe, Investor cohorts, SIP continuity analysis, risk-grade fund recommender, sector HHI).
- **Step 7:** Phase 7 — Interactive Power BI Dashboard Package (Clean star-schema CSV exports, formatted DAX measure catalog, 4-page layout specifications, high-res visual chart exports, and PDF dashboard export).
- **Step 8:** Phase 8 — Comprehensive 15–20 Page Final Technical Report & 12-Slide Executive Presentation.
- **Step 9:** Phase 9 — Automated Testing Suite (`tests/` with pytest) covering data cleaning, quantitative formulas, and SQLite database constraints.
- **Step 10:** Phase 10 — Final Submission Package & Google Drive Delivery Checklist.
