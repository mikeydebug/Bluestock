# Week 1 — Advanced SQL Practice Suite Documentation

**File:** `week_01_core_analytics/sql/practice_queries.sql`  
**Author:** Mayank Soni (Data Analyst Intern)  
**Topic:** Core Data Analytics Foundation (Relational SQL & Analytical Querying)  

---

## 1. Schema Overview

The practice environment models a commercial FinTech B2B/B2C transactional database comprising four normalized relational tables:
1. **`customers`**: Demographics and segment classifications (`Corporate`, `Retail`, `HNI`).
2. **`products`**: Catalog of financial software, streaming data APIs, and advisory licenses with unit pricing and COGS.
3. **`orders`**: Transaction orders, statuses (`Completed`, `Pending`, `Cancelled`), payment channels, and timestamps.
4. **`order_items`**: Line-item details connecting orders and products with purchase quantities and discount percentages.

---

## 2. Query Catalogue & Analytical Breakdown

### Query 1: Filtered Transaction History (`SELECT`, `WHERE`, `ORDER BY`)
- **Objective:** Extract all fulfilled high-value client transactions (`Corporate` and `HNI`) ordered by recency.
- **Key Concepts:** `JOIN`, multi-condition `WHERE (status = 'Completed' AND segment IN (...))`, `ORDER BY order_date DESC`.
- **Business Use Case:** Real-time customer relationship management (CRM) audit.

### Query 2: Segment Commercial Performance (`GROUP BY` & Aggregations)
- **Objective:** Compute total order count, aggregate net revenue, and average line-item size per customer segment.
- **Key Concepts:** `COUNT(DISTINCT ...)`, `SUM(quantity * unit_price * (1 - discount))`, `ROUND(..., 2)`.
- **Expected Output:**
  - `Corporate`: Highest total revenue (~₹3.47 Lakhs) across high-ticket software orders.
  - `HNI`: High average order value.
  - `Retail`: Highest transaction volume with smaller ticket sizes.

### Query 3: High-Performing Categories (`HAVING` Thresholding)
- **Objective:** Filter categories that exceed ₹50,000 in completed sales.
- **Key Concepts:** Difference between `WHERE` (pre-aggregation row filter) and `HAVING` (post-aggregation group filter).

### Query 4: Multi-Table Product Profitability Analysis
- **Objective:** Quantify unit economics, gross revenue, Cost of Goods Sold (COGS), net profit, and gross profit margin percentage per product.
- **Formula:**
  $$\text{Net Profit} = \sum (\text{Qty} \times \text{Price} \times (1 - \text{Discount})) - \sum (\text{Qty} \times \text{Cost})$$
  $$\text{Margin \%} = \frac{\text{Net Profit}}{\text{Net Revenue}} \times 100$$
- **Finding:** *Retail Screener Pass* and *Tax Engine* achieve high margins (>47%), whereas *Bluestock Pro Terminal* drives the largest absolute gross profit (₹84,000).

### Query 5: Subquery-Driven High-Value Customer Identification
- **Objective:** Identify clients whose lifetime spend exceeds the company-wide average customer spend.
- **Key Concepts:** Scalar subquery inside a `HAVING` clause computing dynamically calculated benchmarks.
- **Result:** Highlights key accounts: Aarav Mehta (₹1.60L), Sneha Patel (₹1.21L), and Vikram Malhotra (₹1.09L).

### Query 6: Window Functions — Segment Spending Ranks (`ROW_NUMBER`, `DENSE_RANK`)
- **Objective:** Assign intra-segment ranks to customers based on total expenditures.
- **Syntax:**
  ```sql
  DENSE_RANK() OVER (PARTITION BY segment ORDER BY total_spend DESC) AS segment_rank
  ```
- **Business Value:** Enables localized VIP tiering without collapsing underlying row detail.

### Query 7: Window Functions — Cumulative Running Revenue
- **Objective:** Track financial pacing and day-by-day revenue accumulation across the fiscal quarter.
- **Syntax:**
  ```sql
  SUM(daily_revenue) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
  ```
- **Insight:** Visualizes accelerating quarterly capital inflows up to ₹5.19 Lakhs.

### Query 8: Time-Series Delta & Month-over-Month Growth (`LAG`)
- **Objective:** Calculate sequential monthly revenue growth rates.
- **Syntax:**
  ```sql
  LAG(net_revenue, 1) OVER (ORDER BY sales_month)
  ```
- **Formula:** $\frac{\text{Rev}_m - \text{Rev}_{m-1}}{\text{Rev}_{m-1}} \times 100$
- **Result:** Captures seasonality: June enterprise peak (₹2.88L), July consolidation (₹99k), and August rebound (+33.25% to ₹1.32L).

---

## 3. How to Execute
Execute directly in any standard SQL shell or via SQLite CLI:
```bash
sqlite3 :memory: < week_01_core_analytics/sql/practice_queries.sql
```
All queries execute cleanly and deterministically against the in-memory schema.
