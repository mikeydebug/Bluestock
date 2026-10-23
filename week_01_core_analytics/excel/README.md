# Week 1 — Excel Sales Performance Dashboard Documentation

**File:** `week_01_core_analytics/excel/sales_dashboard.xlsx`  
**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Topic:** Core Data Analytics Foundation (Excel & Financial Modeling)  

---

## 1. Executive Business Summary

The **Sales Performance Dashboard** models B2B and B2C commercial sales for Bluestock FinTech's suite of proprietary financial products (Bluestock Pro Terminal, Real-Time Market Data Feed, Algorithmic Strategy Suite, Wealth Advisory Risk Optimizer, and Investor Subscriptions). 

The workbook is structured into four functional worksheets:
1. **`Executive_Dashboard`**: High-level C-suite summary featuring dynamic KPI summary tiles, regional revenue breakdowns, customer segment performance matrices, and gross/net margin indicators.
2. **`Sales_Data`**: The transactional fact table containing 60 transaction records, tracking Order IDs, dates, customers, segments, regions, units, discounts, gross revenues, and net profits.
3. **`Lookup_Table`**: The dimension master table defining product categories, base pricing tiers, target profit margins, and support SLAs.
4. **`Pivot_Summaries`**: Pre-configured aggregations modeling multi-dimensional revenue splits.

---

## 2. Implemented Excel Formulas & Technical Mechanics

### 2.1 Dynamic Table Lookups (`INDEX-MATCH`)
To decouple product naming and pricing from transactional entry and avoid hardcoded duplication:
```excel
=INDEX(Lookup_Table!$C$2:$C$7, MATCH(F2, Lookup_Table!$A$2:$A$7, 0))
```
- **Lookup Value:** `Product_ID` located in column `F`.
- **Search Array:** `Lookup_Table!$A$2:$A$7` (Product IDs).
- **Return Array:** `Lookup_Table!$C$2:$C$7` (Product Names).
- **Match Type:** `0` (Exact Match).
*Why INDEX-MATCH over VLOOKUP:* `INDEX-MATCH` is computationally faster, does not break when column positions change, and supports two-way leftward/rightward lookups.

### 2.2 Dynamic Multi-Criteria Aggregations (`SUMIFS` & `COUNTIF`)
In the Executive Dashboard, metrics are dynamically derived from the underlying transactional table without static hardcoding:
- **Regional Net Revenue:**
  ```excel
  =SUMIFS(Sales_Data!M2:M61, Sales_Data!E2:E61, "West")
  ```
- **Regional Transaction Frequency:**
  ```excel
  =COUNTIF(Sales_Data!E2:E61, "West")
  ```
- **Segment Profit Aggregation:**
  ```excel
  =SUMIFS(Sales_Data!O2:O61, Sales_Data!D2:D61, "Corporate")
  ```

### 2.3 Financial Metric Calculations
- **Gross Revenue:** `=Units * Unit_Price`
- **Discount Amount:** `=Gross_Revenue * Discount_Pct`
- **Net Revenue:** `=Gross_Revenue - Discount_Amount`
- **Cost of Goods Sold (COGS):** `=Units * Unit_Price * (1 - Target_Margin)`
- **Net Profit:** `=Net_Revenue - Cost_of_Goods`
- **Profit Margin %:** `=Net_Profit / Net_Revenue`

---

## 3. Key Business Insights

1. **Top Contributing Segment:** Corporate enterprise clients generate the highest average ticket size (AOV > ₹120,000 per order) primarily driven by multi-seat *Bluestock Pro Terminal* and *Algorithmic Strategy Suite* enterprise deployments.
2. **Regional Concentration:** The West and South regions account for over 62% of aggregate net revenues, reflecting the concentration of asset management firms in Mumbai and quantitative algorithmic desks in Bengaluru.
3. **Discount Elasticity:** Transactions with modest discounts (5–10%) maintained robust net profit margins exceeding 38%, whereas un-discounted consumer retail passes generated high gross margins (60%) but smaller absolute contribution volume.

---

## 4. How to Inspect & Validate
- Open `sales_dashboard.xlsx` in Microsoft Excel, LibreOffice Calc, or Google Sheets.
- Inspect sheet `Executive_Dashboard` to verify KPI cards and regional summaries.
- Alter a unit count in `Sales_Data!H2` to verify that net revenue, profit, and dashboard KPI tiles update dynamically.
