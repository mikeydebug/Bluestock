# Week 2 — Software Architecture Documentation

**File:** `week_02_fintech_fundamentals/software_architecture/README.md`  
**Diagram:** `week_02_fintech_fundamentals/software_architecture/architecture_diagram.md`  
**Author:** Mayank Soni (Data Analyst Intern)  
**Topic:** FinTech Domain & Software Architecture Fundamentals  

---

## 1. End-to-End Architectural Deep Dive

Financial technology systems demand stringent standards of reliability, sub-millisecond data freshness, strict regulatory auditability, and data security. The multi-tiered architecture implemented in the Bluestock FinTech platform separates concerns across five specialized layers:

### Layer 1: Client & Presentation Layer
- **Components:** Web application (React.js / Next.js) and native mobile apps (iOS / Android).
- **Core Functionality:** User authentication, portfolio overview, interactive scheme screeners, order entry modals, and personalized risk profiling questionnaires.
- **Security:** Secure storage of access tokens, SSL pinning, and zero client-side caching of sensitive financial credentials.

### Layer 2: API Gateway & Backend Microservices
- **Components:** API Gateway (Kong / NGINX) and application backends (Python FastAPI / Django REST).
- **Core Functionality:**
  - Dynamic rate-limiting and DDoS mitigation.
  - JWT token validation and role-based access control (RBAC).
  - Transaction orchestration: placing mutual fund purchase orders via BSE StAR MF / NSE NMF II exchange routing pipes.
  - Sub-10ms response times for cached financial instrument queries.

### Layer 3: Persistent Relational & Cache Data Stores
- **Components:** PostgreSQL / SQLite (Transactional DB) and Redis (In-Memory Key-Value Store).
- **Core Functionality:**
  - Relational schema enforcing ACID guarantees for user folios, order ledgers, and transaction facts.
  - High-speed caching for hot data: live intraday NAVs, top trending schemes, and active user session states.

### Layer 4: ETL Data Pipeline & Quantitative Engine
- **Components:** Automated ingestion workers, data transformation modules (Pandas, NumPy), and mathematical compute engines.
- **Core Functionality:**
  - Ingests daily AMFI NAV closing prices after 9:00 PM IST exchange cutoff.
  - Computes risk and performance metrics: CAGR, Sharpe, Sortino, Jensen's Alpha, Beta, and Value at Risk (VaR).
  - Populates analytical fact tables (`fact_performance`, `fact_aum`).

### Layer 5: Business Intelligence & Executive Dashboard Layer
- **Components:** Power BI / Plotly Dash executive dashboards.
- **Core Functionality:**
  - Four executive pages: Industry Overview, Fund Performance, Investor Analytics, and SIP Market Trends.
  - Self-service filtering for wealth managers, compliance auditors, and executive leadership.
