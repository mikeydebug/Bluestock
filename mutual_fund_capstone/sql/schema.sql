-- ============================================================================
-- BLUESTOCK FINTECH — MUTUAL FUND ANALYTICS CAPSTONE
-- Relational Star Schema DDL Specification for SQLite 3 / PostgreSQL
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. FUND DIMENSION TABLE
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_fund;

CREATE TABLE dim_fund (
    fund_id INTEGER PRIMARY KEY,
    scheme_code INTEGER UNIQUE NOT NULL,
    reference_name TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT NOT NULL,
    expense_ratio REAL NOT NULL,
    risk_grade TEXT NOT NULL,
    launch_year INTEGER NOT NULL
);

-- 2. CALENDAR DATE DIMENSION TABLE
CREATE TABLE dim_date (
    date_id TEXT PRIMARY KEY, -- 'YYYY-MM-DD'
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    day INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    is_trading_day INTEGER NOT NULL DEFAULT 1
);

-- 3. HISTORICAL DAILY NAV FACT TABLE
CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER NOT NULL,
    date_id TEXT NOT NULL,
    nav REAL NOT NULL CHECK(nav > 0),
    daily_return REAL,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id) ON DELETE CASCADE,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id) ON DELETE CASCADE,
    UNIQUE(fund_id, date_id)
);

-- Indexes for time-series slicing and joins
CREATE INDEX idx_nav_fund_date ON fact_nav(fund_id, date_id);
CREATE INDEX idx_nav_date ON fact_nav(date_id);

-- 4. INVESTOR TRANSACTIONS FACT TABLE
CREATE TABLE fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    investor_id INTEGER NOT NULL,
    fund_id INTEGER NOT NULL,
    date_id TEXT NOT NULL,
    trans_type TEXT NOT NULL CHECK(trans_type IN ('SIP', 'Lumpsum', 'Redemption')),
    amount REAL NOT NULL CHECK(amount > 0),
    units REAL NOT NULL,
    investor_age_group TEXT NOT NULL,
    investor_gender TEXT NOT NULL,
    investor_state TEXT NOT NULL,
    city_tier TEXT NOT NULL CHECK(city_tier IN ('T30', 'B30')),
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id) ON DELETE CASCADE,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id) ON DELETE CASCADE
);

CREATE INDEX idx_trans_fund ON fact_transactions(fund_id);
CREATE INDEX idx_trans_date ON fact_transactions(date_id);
CREATE INDEX idx_trans_investor ON fact_transactions(investor_id);

-- 5. QUARTERLY AUM AND FOLIO FACT TABLE
CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER NOT NULL,
    date_id TEXT NOT NULL,
    aum_crores REAL NOT NULL CHECK(aum_crores >= 0),
    folio_count INTEGER NOT NULL,
    net_inflow_crores REAL NOT NULL,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id) ON DELETE CASCADE,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id) ON DELETE CASCADE,
    UNIQUE(fund_id, date_id)
);

CREATE INDEX idx_aum_fund ON fact_aum(fund_id);

-- 6. QUANTITATIVE PERFORMANCE AND RISK FACT TABLE
CREATE TABLE fact_performance (
    perf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER NOT NULL,
    as_of_date TEXT NOT NULL,
    cagr_1y REAL,
    cagr_3y REAL,
    cagr_5y REAL,
    volatility_ann REAL NOT NULL,
    sharpe_ratio REAL NOT NULL,
    sortino_ratio REAL NOT NULL,
    beta REAL NOT NULL,
    alpha REAL NOT NULL,
    max_drawdown REAL NOT NULL,
    max_dd_peak_date TEXT,
    max_dd_trough_date TEXT,
    fund_score REAL NOT NULL,
    tracking_error REAL,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id) ON DELETE CASCADE,
    FOREIGN KEY (as_of_date) REFERENCES dim_date(date_id) ON DELETE CASCADE,
    UNIQUE(fund_id, as_of_date)
);

CREATE INDEX idx_perf_fund ON fact_performance(fund_id);
