# Mutual Fund Capstone — Comprehensive Exploratory Data Analysis (EDA) Findings

**File:** `mutual_fund_capstone/reports/eda_findings.md`  
**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Topic:** Mutual Fund Capstone — Empirical Findings & Market Insights  
**Charts Generated:** 15 High-Resolution Charts in `mutual_fund_capstone/outputs/charts/`  

---

## 1. Executive Synthesis

This report synthesizes the exploratory data analysis conducted across 20,389 daily NAV observations, 5,000 investor transactions, 162 quarterly AUM snapshots, and detailed equity portfolio sector allocations. All findings are derived directly from the verified SQLite relational database (`mutual_funds.db`) and validated quantitative analytics.

---

## 2. Twelve Evidence-Based Analytical Findings

### Finding 1: Large-Cap Fund Consistency & Benchmark Outperformance
**Nippon India Large Cap Fund** (Scheme 118632) demonstrated the highest risk-adjusted stability among equity funds, generating a **10.39% 3-Year CAGR** with an annualised volatility of **13.70%** and a Sharpe ratio of **0.29**. Its low maximum drawdown (-15.37%) relative to mid/small-cap peers earned it the **#1 rank on the composite Fund Scorecard (95.0/100)**.

### Finding 2: High Alpha and Downside Vulnerability in Small-Cap Funds
**SBI Small Cap Fund** (Scheme 125497) posted a 3-Year CAGR of **10.13%** and an impressive annualised Jensen's Alpha of **+11.76%**. However, this return was accompanied by a severe **Maximum Drawdown of -22.42%** and volatility of **14.34%**, underscoring the necessity of multi-factor risk scoring rather than relying solely on raw trailing returns.

### Finding 3: Capital Preservation in Money Market Funds
**HDFC Money Market Fund** (Scheme 119092) achieved a 3-Year CAGR of **7.29%** with near-zero annualised volatility (**0.43%**) and a negligible maximum drawdown of **-0.15%**. This yielded an exceptional Sharpe ratio of **1.97**, establishing it as the premier capital-preservation instrument in the monitored universe.

### Finding 4: Debt Fund Sensitivity to Interest Rate Cycles
**Aditya Birla Sun Life Banking & PSU Debt Fund** (Scheme 119551) recorded a negative 3-Year CAGR of **-2.39%** and a negative Sharpe ratio (**-0.64**), reflecting duration risks and capital depreciation during RBI monetary policy tightening cycles between 2022 and 2024.

### Finding 5: Retail SIP Dominance in Inflow Velocity
Of the 5,000 recorded investor transactions, Systematic Investment Plans (**SIP**) accounted for **72.1% of total transaction frequency** (3,607 transactions) and ₹2.12 Crores in capital volume, representing the primary recurring cash engine for asset management companies.

### Finding 6: Age Demographic Skew Toward Young Professionals
Investors aged **26–35 years** represent the largest individual cohort (**42.0% of total folios**), followed by the 36–50 age bracket (26.0%). This reflects the rapid digitization of retail investing via smartphone applications (Zerodha Coin, Groww) among urban millennials.

### Finding 7: Ticket Size Elasticity by Age Cohort
While the 26–35 age bracket dominates transaction volume, the **36–50 age cohort** commands significantly higher average monthly SIP ticket sizes (**₹7,420** vs. ₹4,180 for 26–35 and ₹1,950 for 18–25), demonstrating increasing discretionary investable surplus during peak career earning years.

### Finding 8: Geographic Capital Concentration in Western and Southern Tech Hubs
Geographic analysis reveals heavy inflow concentration:
1. **Maharashtra:** 24.2% of total capital inflows (Mumbai financial services center).
2. **Karnataka:** 18.1% of inflows (Bengaluru tech ecosystem).
3. **Delhi NCR:** 14.0% of inflows.  
Together, the top three states generate over **56.3% of aggregate mutual fund investments**.

### Finding 9: Emerging Market Penetration (T30 vs. B30)
Inflows from **Beyond 30 (B30)** cities represent **36.2% of total transaction volume**, reflecting SEBI's regulatory incentives (additional expense ratio allowances) designed to drive mutual fund penetration into Tier-2 and Tier-3 rural/semi-urban geographies.

### Finding 10: Multi-Year AUM Compounding
Aggregate AUM across the monitored fund universe grew from ₹92,000 Crores in Q1 2020 to over **₹198,000 Crores by Q3 2026**, representing an annualised compound growth rate exceeding **13.5%**, supported by steady SIP book inflows.

### Finding 11: Sector Concentration in Equity Portfolios
Sector allocation analysis reveals that **Financial Services** (Banking, NBFCs, Insurance) represents the single largest allocation across equity holdings (**32.4%** in Large Cap, **22.0%** in Mid Cap), followed by **Information Technology** (14.8%) and **Oil & Gas** (12.1%).

### Finding 12: Inter-Fund Return Correlation & Diversification Benefits
Return correlation analysis demonstrates that Large Cap and Mid Cap equity funds have high cross-correlation ($r = 0.82$), providing limited intra-equity diversification. Conversely, the Money Market Fund exhibited near-zero correlation ($r = 0.04$) with equities, proving that cross-asset allocation is essential for drawdown mitigation.

---

## 3. Visual Catalog Reference

All supporting visual charts are stored in `mutual_fund_capstone/outputs/charts/`:
- `chart_01_nav_trends.png`: 3-Year Historical NAV Trajectory
- `chart_02_aum_growth.png`: AUM Expansion by Fund House
- `chart_03_monthly_sip_inflows.png`: Monthly SIP Velocity
- `chart_04_category_inflow_heatmap.png`: Quarterly Category Heatmap
- `chart_05_age_distribution.png`: Investor Demographics Pie Chart
- `chart_06_sip_by_age.png`: Mean vs Median SIP Ticket Sizes
- `chart_07_gender_distribution.png`: Capital Contribution by Gender
- `chart_08_state_distribution.png`: State-Wise Inflows
- `chart_09_t30_vs_b30.png`: Metro vs Emerging Markets Split
- `chart_10_folio_growth.png`: Active Folios Time-Series
- `chart_11_return_correlation.png`: Return Correlation Heatmap
- `chart_12_sector_allocation.png`: Equity Portfolio Sector Weights
- `chart_13_drawdown_curves.png`: Peak-to-Trough Drawdown Curves
- `chart_14_risk_return_scatter.png`: Volatility vs CAGR Scatter Plot
- `chart_15_transaction_composition.png`: Transaction Type Breakdown
- `benchmark_comparison.png`: Rebased Cumulative Growth vs NIFTY 100
