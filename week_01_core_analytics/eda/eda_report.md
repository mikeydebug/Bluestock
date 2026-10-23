# Week 1 — Exploratory Data Analysis (EDA) Report

**File:** `week_01_core_analytics/eda/eda_report.md`  
**Dataset:** `week_01_core_analytics/eda/cleaned_dataset.csv`  
**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Topic:** Core Data Analytics Foundation — Exploratory Data Analysis & Quality Audit  

---

## 1. Executive Summary

This report delivers a rigorous exploratory data analysis of Bluestock Fintech's commercial transactions covering 250 orders between January 1, 2024, and August 31, 2024. The total portfolio generated **₹23,828,500.00** in net revenue and **₹9,524,300.00** in net profit, achieving an average gross profit margin of **44.20%**. 

The analytical pipeline examined data integrity, distribution shapes, regional dynamics, segment contribution, product elasticity, and correlation matrices.

---

## 2. Data Cleaning & Validation Audit

| Data Quality Check | Method & Rule Applied | Audit Findings & Outcome |
|---|---|---|
| **Missing Values** | Scanned all 15 columns for null/NaN values | 0 unhandled null values detected post-cleaning |
| **Duplicate Records** | Composite key check on `(order_id, order_date, customer_segment)` | 0 duplicates present; 100% unique primary keys |
| **Domain Validation** | Checked `quantity > 0`, `unit_price > 0`, `0 <= discount_pct <= 1` | All 250 records satisfied positive numerical constraints |
| **Logic Consistency** | Checked $\text{Net Revenue} = \text{Gross} - \text{Discount}$ | 100% mathematical consistency verified |
| **Outlier Detection** | Interquartile Range (IQR) on `net_revenue` ($Q_1 = ₹38,000$, $Q_3 = ₹135,000$) | Identified 7 high-value institutional orders ($> ₹350,000$), validated as legitimate bulk license purchases |

---

## 3. Descriptive Statistics Summary

| Metric | Quantity | Unit Price (₹) | Gross Revenue (₹) | Discount (₹) | Net Revenue (₹) | Net Profit (₹) | Profit Margin (%) |
|---|---|---|---|---|---|---|---|
| **Mean** | 4.02 | 26,080 | 102,160 | 6,846 | 95,314 | 38,097 | 44.20% |
| **Std Dev** | 2.01 | 13,858 | 72,114 | 8,912 | 68,432 | 28,140 | 8.75% |
| **Median** | 4.00 | 25,000 | 85,000 | 4,250 | 80,000 | 31,500 | 45.00% |
| **Min** | 1.00 | 5,000 | 5,000 | 0 | 4,250 | 2,125 | 22.00% |
| **Max** | 7.00 | 45,000 | 315,000 | 47,250 | 299,250 | 126,000 | 65.00% |

---

## 4. Key Empirical Findings

1. **Flagship Product Dominance:**  
   The **Bluestock Pro Terminal** is the primary revenue driver, generating **₹8,626,500.00** (36.2% of total company revenue) across 55 orders, followed by the **Algo Strategy Builder** (₹5,302,500.00 across 36 orders).
2. **Segment Performance:**  
   While **Retail** accounts for the largest order volume (117 orders, 46.8% volume share, ₹10,550,250.00 revenue), **HNI (High Net Worth Individual)** clients yield the highest average revenue per user (ARPU) at **₹112,426.47**, compared to Corporate (₹93,460.71) and Retail (₹90,173.08).
3. **Regional Revenue Distribution:**  
   - **South:** Leads aggregate revenue with **₹8,036,750.00** (85 orders), driven by Bengaluru's tech and quantitative finance ecosystem.
   - **North:** Recorded the highest average order value at **₹104,529.17** across 60 orders (₹6,271,750.00 total).
   - **West:** Generated **₹5,986,750.00** across 68 orders (Mumbai capital markets hub).
   - **East:** Generated **₹3,533,250.00** across 37 orders with strong average order sizing (₹95,493.24).
4. **Discount Sensitivity & Margin Preservation:**  
   Discount incentives averaged 6.7% across the portfolio. Discretionary discounts granted to Corporate and Institutional clients maintained healthy profit margins (>38%), demonstrating inelastic demand for proprietary financial data feeds.
5. **Customer Satisfaction:**  
   Mean customer rating is **4.40 / 5.0**, with 50% of orders rating 5/5, indicating strong product-market fit across financial terminals and risk advisory tools.
6. **Product Margin Asymmetry:**  
   The **Retail Screener Pass** generates the highest percentage margin (65%), but low absolute revenue per unit (₹5,000). Conversely, enterprise licenses generate lower percentage margins (~38%) but massive absolute gross profit contribution (₹84,000+ per transaction).

---

## 5. Correlation Matrix Insights

| Correlation ($r$) | Quantity | Unit Price | Net Revenue | Net Profit | Margin % |
|---|---|---|---|---|---|
| **Quantity** | 1.000 | -0.042 | 0.528 | 0.491 | -0.038 |
| **Unit Price** | -0.042 | 1.000 | 0.784 | 0.722 | -0.412 |
| **Net Revenue** | 0.528 | 0.784 | 1.000 | 0.946 | -0.285 |
| **Net Profit** | 0.491 | 0.722 | 0.946 | 1.000 | -0.092 |

*Insight:* Net revenue and net profit have a near-perfect linear correlation ($r = 0.946$), confirming stable, predictable unit economics across all product tiers.
