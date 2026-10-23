# Power BI Data Model — Enterprise DAX Measures Catalog

**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**File:** `mutual_fund_capstone/dashboard/power_bi/DAX_MEASURES.md`  
**Target Platform:** Microsoft Power BI Desktop / Power BI Service  

---

## 1. Dimensional Table Definitions & Model Setup

Create a dedicated measure staging table in Power BI:  
**Home $\to$ Enter Data $\to$ Table Name: `_Measures`**

---

## 2. Core Financial & AUM Measures

### 2.1 Latest Industry AUM (₹ Crores)
```dax
Total AUM Cr = 
VAR LatestDate = MAX(Dim_Date[date_id])
RETURN
CALCULATE(
    SUM(Fact_AUM[aum_crores]),
    Fact_AUM[date_id] = LatestDate
)
```

### 2.2 Quarterly AUM YoY Growth (%)
```dax
AUM YoY Growth % = 
VAR CurrentAUM = [Total AUM Cr]
VAR PriorYearAUM = 
    CALCULATE(
        [Total AUM Cr],
        SAMEPERIODLASTYEAR(Dim_Date[date_id])
    )
RETURN
DIVIDE(CurrentAUM - PriorYearAUM, PriorYearAUM, 0)
```

### 2.3 Total Active Folios (Lakhs)
```dax
Total Active Folios Lakhs = 
VAR LatestDate = MAX(Dim_Date[date_id])
RETURN
DIVIDE(
    CALCULATE(SUM(Fact_AUM[folio_count]), Fact_AUM[date_id] = LatestDate),
    100000,
    0
)
```

---

## 3. Retail Transaction & Inflow Measures

### 3.1 Total Monthly SIP Inflows (₹ Lakhs)
```dax
SIP Inflow Lakhs = 
DIVIDE(
    CALCULATE(
        SUM(Fact_Transactions[amount]),
        Fact_Transactions[trans_type] = "SIP"
    ),
    100000,
    0
)
```

### 3.2 Total Net Capital Inflow (₹ Lakhs)
```dax
Net Inflow Lakhs = 
VAR Inflows = 
    CALCULATE(
        SUM(Fact_Transactions[amount]), 
        Fact_Transactions[trans_type] IN {"SIP", "Lumpsum"}
    )
VAR Outflows = 
    CALCULATE(
        SUM(Fact_Transactions[amount]), 
        Fact_Transactions[trans_type] = "Redemption"
    )
RETURN
DIVIDE(Inflows - Outflows, 100000, 0)
```

### 3.3 Average SIP Ticket Size (₹)
```dax
Average SIP Ticket Size = 
CALCULATE(
    AVERAGE(Fact_Transactions[amount]),
    Fact_Transactions[trans_type] = "SIP"
)
```

### 3.4 B30 Market Penetration Rate (%)
```dax
B30 Inflow Share % = 
VAR B30Amount = 
    CALCULATE(
        SUM(Fact_Transactions[amount]), 
        Fact_Transactions[city_tier] = "B30"
    )
VAR TotalAmount = SUM(Fact_Transactions[amount])
RETURN
DIVIDE(B30Amount, TotalAmount, 0)
```

---

## 4. Quantitative Performance & Risk DAX Measures

### 4.1 Weighted Composite Fund Score
```dax
Weighted Fund Score = 
AVERAGE(Fact_Scorecard[fund_score])
```

### 4.2 Portfolio Weighted Sharpe Ratio
```dax
Weighted Sharpe Ratio = 
DIVIDE(
    SUMX(Fact_Scorecard, Fact_Scorecard[sharpe_ratio] * RELATED(Fact_AUM[aum_crores])),
    SUM(Fact_AUM[aum_crores]),
    0
)
```

### 4.3 3-Year Annualised Return (%)
```dax
Avg 3Y CAGR % = 
AVERAGE(Fact_Scorecard[cagr_3y])
```

### 4.4 Max Capital Impairment (Worst Drawdown %)
```dax
Worst Drawdown % = 
MIN(Fact_Scorecard[max_drawdown])
```
