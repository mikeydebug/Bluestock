# Mutual Fund Analytics Capstone — Power BI Dashboard Architecture & Specifications

**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Topic:** Interactive Power BI Business Intelligence Architecture  

---

## 1. Executive BI Overview

The **Bluestock Mutual Fund Analytics Dashboard** provides an interactive, executive-grade business intelligence interface designed for wealth managers, portfolio risk committees, and AMC executives. 

The report comprises four specialized analytical views:
1. **Page 1: Industry & AMC Landscape** (Macro market trends, AUM by AMC, active folios)
2. **Page 2: Scheme Performance & Risk Profiling** (Fund scorecard, risk-return scatter, benchmark comparison)
3. **Page 3: Investor Demographics & Retail Behavior** (Geographic maps, age cohort ticket sizes, T30 vs B30)
4. **Page 4: SIP Persistence & Market Correlation** (SIP inflow velocity vs NIFTY 50, category heatmaps)

---

## 2. Dimensional Data Model & Table Relationships

The Power BI data model imports pre-staged star-schema CSV tables from `mutual_fund_capstone/dashboard/power_bi/`:

```
                       ┌──────────────┐
                       │   Dim_Date   │
                       └──────┬───────┘
                              │ 1
                              │
         ┌────────────────────┼────────────────────┐
         │ *                  │ *                  │ *
   ┌─────▼────────┐    ┌──────▼───────┐    ┌───────▼──────────┐
   │   Fact_NAV   │    │Fact_Transact │    │     Fact_AUM     │
   └─────▲────────┘    └──────▲───────┘    └───────▲──────────┘
         │ *                  │ *                  │ *
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │ 1
                       ┌──────┴───────┐
                       │   Dim_Fund   │
                       └──────▲───────┘
                              │ 1
                              │
                              │ 1
                       ┌──────┴───────┐
                       │Fact_Scorecard│
                       └──────────────┘
```

- **Relationships:** Single-direction 1-to-many (`1:*`) relationships with referential integrity enforced.
- **Date Dimension (`Dim_Date`):** Marked as official Date Table in Power BI.

---

## 3. Four-Page Visual Layout Specifications

### Page 1: Industry & AMC Landscape
- **Header:** Bluestock FinTech corporate branding, last-refresh timestamp.
- **Top KPI Cards (4 Tiles):**
  - Total Industry AUM: `₹1,98,420 Cr`
  - Monthly SIP Inflow: `₹21,240 Cr`
  - Total Active Folios: `9.42 Cr`
  - Monitored Schemes: `6`
- **Visual 1 (Stacked Area Chart):** 5-Year Industry AUM Growth Trend by Quarter (2020–2026).
- **Visual 2 (Horizontal Clustered Bar):** Market Share by Top Fund Houses (SBI, Nippon, Axis, HDFC, quant).
- **Visual 3 (Multi-Row Card):** Quarterly Net Inflow Velocity across Asset Classes.
- **Interactive Slicers:** `Calendar Year`, `Fund House (AMC)`, `Scheme Category`.

### Page 2: Scheme Performance & Risk Profiling
- **Visual 1 (Scatter Plot):** Risk-Return Matrix.
  - X-Axis: `Annualised Volatility (%)`
  - Y-Axis: `3-Year CAGR (%)`
  - Bubble Size: `AUM (₹ Cr)`
  - Color Legend: `Risk Grade`
- **Visual 2 (Interactive Matrix / Table):** Fund Scorecard.
  - Columns: Rank, Scheme Name, Category, 3Y Return %, Sharpe, Alpha, TER %, Max Drawdown %, Composite Score (0–100).
- **Visual 3 (Line Chart):** Rebased Cumulative Performance vs NIFTY 100 Benchmark.
- **Interactive Slicers:** `Scheme Category`, `Risk Grade`, `Expense Ratio Bracket`.

### Page 3: Investor Demographics & Retail Behavior
- **Visual 1 (Geographic Clustered Bar / Filled Map):** State-Wise Investment Volume (Maharashtra, Karnataka, Delhi, Gujarat, etc.).
- **Visual 2 (Donut Chart):** Transaction Breakdown by Order Type (SIP: 72.1%, Lumpsum: 20.0%, Redemption: 7.9%).
- **Visual 3 (Grouped Column Chart):** Mean vs. Median SIP Ticket Size across Age Demographics (18–25, 26–35, 36–50, 51–65, 65+).
- **Visual 4 (100% Stacked Bar):** Metro (T30) vs Emerging Market (B30) Contribution Ratio.
- **Interactive Slicers:** `Investor State`, `Age Group`, `City Tier (T30 / B30)`.

### Page 4: SIP Persistence & Market Correlation
- **Visual 1 (Dual-Axis Combo Chart):** Monthly SIP Inflow (₹ Lakhs) vs. NIFTY 50 Index Close. Demonstrates retail SIP stickiness regardless of short-term market corrections.
- **Visual 2 (Matrix Heatmap):** Category Inflow Intensity by Quarter (Equity vs Debt vs Money Market).
- **Visual 3 (Ranked Bar Chart):** Net Inflow Acceleration by SEBI Category.
- **Interactive Slicers:** `Calendar Year`, `Quarter`, `Transaction Inflow Tier`.
