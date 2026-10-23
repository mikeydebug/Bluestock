# Week 2 — Full-Stack FinTech Software Architecture

**Topic:** Software Architecture Fundamentals  
**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  

---

## 1. System Architecture Flow Diagram

```mermaid
flowchart TD
    subgraph Client_Layer ["1. CLIENT & PRESENTATION LAYER"]
        UA["User Action / Investor Journey\n(Browse Funds, Place SIP, View Portfolio)"]
        FE["Client Frontend Application\n(React.js / Next.js / Mobile App)"]
    end

    subgraph API_Backend_Layer ["2. APPLICATION & API BACKEND"]
        GW["API Gateway & Reverse Proxy\n(Rate Limiting, Auth, TLS Termination)"]
        BE["Backend Microservices / API\n(Python FastAPI / Django REST Framework)"]
        AUTH["Auth & Identity Provider\n(JWT, OAuth2, SEBI KYC Validation)"]
    end

    subgraph Data_Persistence ["3. TRANSACTIONAL & RELATIONAL DATABASE"]
        DB[("Core Transactional RDBMS\n(PostgreSQL / SQLite Star Schema)\n- dim_fund, dim_date\n- fact_nav, fact_transactions")]
        CACHE[("In-Memory Caching\n(Redis: Live NAVs, Session State)")]
    end

    subgraph ETL_Data_Pipeline ["4. ETL & ANALYTICAL DATA PIPELINE"]
        SCHED["Orchestration Engine\n(Cron / Apache Airflow)"]
        INGEST["Data Ingestion Workers\n(AMFI mfapi.in, NSE Market Feeds)"]
        TRANS["Data Cleaning & Transformation\n(Pandas, NumPy, Anomaly Filters)"]
        QUANT["Quant Risk Engine\n(CAGR, Sharpe, Sortino, VaR/CVaR)"]
    end

    subgraph Business_Intelligence ["5. ANALYTICS & BI DASHBOARD LAYER"]
        PBI["Interactive BI Dashboards\n(Power BI / Dash Plotly)\n- 4 Executive Analytical Views\n- Dynamic DAX Slicers & Heatmaps"]
        EXEC["Executive Stakeholders & Retail Investors"]
    end

    %% Interactions
    UA -->|"1. Triggers Request / Click"| FE
    FE -->|"2. HTTPS / WSS API Call"| GW
    GW -->|"3. Routed & Authenticated"| BE
    BE <-->|"4. User Session / KYC"| AUTH
    BE <-->|"5. Read / Write Orders"| DB
    BE <-->|"Fast Read Cached Quotes"| CACHE

    %% Pipeline Flow
    SCHED -->|"Triggers Scheduled Jobs"| INGEST
    INGEST -->|"External Market Feeds"| TRANS
    TRANS -->|"Loads Clean Facts"| DB
    DB -->|"Extracts Historical Series"| QUANT
    QUANT -->|"Computes Risk & Scorecards"| DB

    %% BI Reporting
    DB -->|"DirectQuery / Star Schema Import"| PBI
    PBI -->|"Interactive Risk-Return Insights"| EXEC
```

---

## 2. Component Explanations

1. **User Action:** Retail investors, wealth managers, or institutional clients initiate actions such as searching schemes, triggering SIP mandates, or viewing portfolio risk profiles.
2. **Frontend Layer:** Responsive single-page application built with modern web technologies delivering sub-100ms UI responsiveness, real-time charting, and interactive order tickets.
3. **Backend / API Gateway:** Handles authorization, request throttling, and routing to transactional microservices. Validates client payloads and guarantees idempotent financial order execution.
4. **Relational Database Layer:** High-integrity relational database enforcing ACID properties, foreign key constraints, and indexing. Implements a star schema optimized for fast analytical aggregations.
5. **ETL & Data Pipeline:** Automated pipeline orchestrating ingestion from external exchanges and AMFI endpoints, executing data cleaning, and calculating quantitative risk scores.
6. **Analytics Dashboard Layer:** High-impact business intelligence dashboards providing executive visibility into AUM trends, Sharpe-ranked fund scorecards, investor cohorts, and downside risk metrics.
