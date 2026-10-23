# Week 1 — Power BI Business Performance Dashboard Specification

**File:** `week_01_core_analytics/power_bi/README.md`  
**Dataset Reference:** `week_01_core_analytics/eda/cleaned_dataset.csv`  
**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Topic:** Core Data Analytics Foundation — BI Data Modeling & Performance Reporting  

---

## 1. Executive Business Purpose

The **Week 1 Business Performance Dashboard** is designed to provide executive leadership with real-time visibility into commercial sales velocity, geographic market penetration, customer segment dynamics, and product profitability across Bluestock Fintech's analytics and software solutions.

---

## 2. Relational Star Schema Data Model

The data model conforms to standard Kimball dimensional modeling principles, separating dimension lookup tables from high-volume transaction fact tables.

```
       ┌──────────────────┐               ┌──────────────────┐
       │   Dim_Product    │               │     Dim_Date     │
       ├──────────────────┤               ├──────────────────┤
       │ PK  Product_ID   │               │ PK  Date_ID      │
       │     Product_Name │               │     Year         │
       │     Category     │               │     Quarter      │
       │     Cost_Price   │               │     Month_Name   │
       └────────┬─────────┘               └────────┬─────────┘
                │ 1                                │ 1
                │                                  │
                │ *                              * │
       ┌────────┴──────────────────────────────────┴─────────┐
       │                     Fact_Sales                      │
       ├─────────────────────────────────────────────────────┤
       │ PK  Order_ID                                        │
       │ FK  Date_ID                                         │
       │ FK  Product_ID                                      │
       │ FK  Customer_Segment_ID                             │
       │ FK  Region_ID                                       │
       │     Units                                           │
       │     Unit_Price                                      │
       │     Gross_Revenue                                   │
       │     Discount_Amount                                 │
       │     Net_Revenue                                     │
       │     Cost_of_Goods                                   │
       │     Net_Profit                                      │
       └────────┬──────────────────────────────────┬─────────┘
                │ *                              * │
                │ 1                              │ 1
       ┌────────┴─────────┐               ┌────────┴─────────┐
       │   Dim_Segment    │               │    Dim_Region    │
       ├──────────────────┤               ├──────────────────┤
       │ PK  Segment_ID   │               │ PK  Region_ID    │
       │     Segment_Name │               │     Region_Name  │
       │     Tier         │               │     Zone_Manager │
       └──────────────────┘               └──────────────────┘
```

---

## 3. Core Business DAX Measures Catalog

To ensure dynamic, context-aware reporting, all aggregations are defined as explicit DAX measures:

### 3.1 Total Commercial Revenue
```dax
Total Net Revenue = 
SUM(Fact_Sales[net_revenue])
```

### 3.2 Total Net Profit
```dax
Total Net Profit = 
SUM(Fact_Sales[net_profit])
```

### 3.3 Operating Profit Margin (%)
```dax
Operating Profit Margin % = 
DIVIDE([Total Net Profit], [Total Net Revenue], 0)
```

### 3.4 Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE([Total Net Revenue], DISTINCTCOUNT(Fact_Sales[order_id]), 0)
```

### 3.5 Discount Penetration Rate
```dax
Discount Penetration % = 
DIVIDE(SUM(Fact_Sales[discount_amount]), SUM(Fact_Sales[gross_revenue]), 0)
```

---

## 4. Visual Layout & Interactive Elements

| Visual Section | Visual Type | Primary Fields | Interactive Slicers / Filters |
|---|---|---|---|
| **Top KPI Ribbon** | 4 Multi-Row KPI Cards | Net Revenue, Net Profit, Margin %, AOV | Date Range, Segment |
| **Geographic Velocity** | Filled Map / Clustered Bar | X: `Region`, Y: `Total Net Revenue` | Region Slicer (North, South, East, West) |
| **Segment Mix** | Donut Chart | Legend: `Customer_Segment`, Values: `Net_Revenue` | Customer Type (Corporate, Retail, HNI) |
| **Product Unit Economics**| Scatter Plot | X: `Unit Price`, Y: `Profit Margin %`, Size: `Units` | Product Category |
| **Monthly Trend** | Area Chart with Line | X: `Month_Name`, Y: `Net Revenue` vs `Prior Period` | Year / Quarter |

---

## 5. Step-by-Step Implementation Guide in Power BI Desktop

1. **Data Ingestion:**
   - Launch Power BI Desktop $\to$ Click **Get Data** $\to$ Select **Text/CSV**.
   - Browse to `week_01_core_analytics/eda/cleaned_dataset.csv` and click **Load**.
2. **Data Modeling:**
   - Navigate to the **Model View**.
   - Create explicit 1-to-many single-direction relationships between dimensions and `Fact_Sales`.
3. **Measure Creation:**
   - Create a dedicated measure table: Home $\to$ Enter Data $\to$ Table Name: `_Measures`.
   - Add the DAX measures detailed in Section 3 above.
4. **Visual Formatting:**
   - Apply Bluestock FinTech corporate navy theme (`#1F4E78`, `#2F5597`, `#FFFFFF`).
   - Format currency values as Indian Rupee (`₹#,##0`).
