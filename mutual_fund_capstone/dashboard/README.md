# Mutual Fund Capstone — Executive Power BI Dashboard Suite

**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Topic:** Business Intelligence & Interactive Portfolio Dashboard  

---

## 1. Deliverables Summary

The Power BI dashboard suite provides an end-to-end business intelligence solution modeling mutual fund industry dynamics, quantitative scheme risk-return performance, retail investor demographics, and SIP persistence trends:

1. **`Dashboard.pdf`**: Multi-page high-resolution executive document compiling all four visual views.
2. **Four High-Resolution Page Visuals:**
   - `page_1_industry_overview.png`: Macro AUM expansion, AMC market shares, and key KPI tiles.
   - `page_2_fund_performance.png`: Risk-return scatter plot, rebased benchmark comparison, and interactive Fund Scorecard.
   - `page_3_investor_analytics.png`: Geographic state-wise inflows, ticket sizes by age group, and T30 vs. B30 market penetration.
   - `page_4_sip_market_trends.png`: Dual-axis SIP inflow velocity vs. NIFTY 50 index close, quarterly category heatmaps, and net inflow rankings.
3. **Prepared Star-Schema Datasets (`power_bi/*.csv`):**
   - `Dim_Fund.csv`: Mutual fund master dimension.
   - `Dim_Date.csv`: Standardized date dimension.
   - `Fact_NAV.csv`: 20,389 daily NAV observations with arithmetic returns.
   - `Fact_Transactions.csv`: 5,000 retail and HNI transactions.
   - `Fact_AUM.csv`: 162 quarterly AUM and folio snapshots.
   - `Fact_Scorecard.csv`: 0–100 composite fund scorecard rankings.
   - `Fact_Risk_Metrics.csv`: 95% Historical VaR and CVaR metrics.
4. **`DAX_MEASURES.md`**: Production library containing 10+ formatted DAX measures.
5. **`dashboard_requirements.md`**: Comprehensive architectural and layout specification document.

---

## 2. Step-by-Step Power BI Desktop Build Guide

Follow these steps to import and configure the dashboard in Microsoft Power BI Desktop:

### Step 1: Ingest Data Sources
1. Open **Power BI Desktop**.
2. Click **Get Data** $\to$ **Text/CSV**.
3. Browse to `mutual_fund_capstone/dashboard/power_bi/` and import:
   - `Dim_Fund.csv`
   - `Dim_Date.csv`
   - `Fact_NAV.csv`
   - `Fact_Transactions.csv`
   - `Fact_AUM.csv`
   - `Fact_Scorecard.csv`

### Step 2: Establish Model Relationships
Navigate to the **Model View** and verify single-direction 1-to-many (`1:*`) relationships:
- `Dim_Fund[fund_id]` $\to$ `Fact_NAV[fund_id]`
- `Dim_Fund[fund_id]` $\to$ `Fact_Transactions[fund_id]`
- `Dim_Fund[fund_id]` $\to$ `Fact_AUM[fund_id]`
- `Dim_Fund[scheme_code]` $\to$ `Fact_Scorecard[scheme_code]`
- `Dim_Date[date_id]` $\to$ `Fact_NAV[date_id]`
- `Dim_Date[date_id]` $\to` `Fact_Transactions[date_id]`
- `Dim_Date[date_id]` $\to` `Fact_AUM[date_id]`

### Step 3: Implement DAX Measures
Create a dedicated `_Measures` table and copy the formulas provided in `power_bi/DAX_MEASURES.md`.

### Step 4: Layout the Four Pages
Replicate the exact layouts, slicers, cards, and charts detailed in `dashboard_requirements.md` and verified in `Dashboard.pdf`.
