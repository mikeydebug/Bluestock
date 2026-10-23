# Week 2 — Resilient REST API Data Ingestion Engine

**File:** `week_02_fintech_fundamentals/api_extraction/api_extraction.py`  
**Output:** `week_02_fintech_fundamentals/api_extraction/extracted_fund_data.csv`  
**Author:** Mayank Soni (Data Analyst Intern)  
**Topic:** FinTech Software Fundamentals — Network Protocols, JSON Parsing & ETL  

---

## 1. Architectural Design & Network Resilience

In modern FinTech platforms, automated market data ingestion must be resilient to network jitter, rate limiting, and intermittent upstream provider downtime. This script implements an enterprise-grade extraction utility adhering to production best practices:

1. **Configurable Network Timeouts:** Prevents socket hanging using an explicit `timeout=15` parameter on all requests.
2. **Exponential Backoff & Retries:** Handles transient HTTP status codes (`429 Too Many Requests`, `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`) using exponential delay doubling: $t_{\text{wait}} = 2^{\text{attempt}}$ seconds.
3. **Payload Contract Validation:** Inspects JSON dictionary structure, verifies metadata keys (`fund_house`, `scheme_code`, `scheme_name`), and guarantees the presence of sequential observation records before proceeding.
4. **Data Normalization:** Converts non-standard `DD-MM-YYYY` string representations into ISO 8601 `YYYY-MM-DD` timestamps, filters invalid/negative NAV values, sorts observations chronologically, and derives daily arithmetic percentage returns:
   $$R_t = \frac{NAV_t - NAV_{t-1}}{NAV_{t-1}}$$
5. **Security & Governance:** Strict adherence to zero-credential leakage; connects to open public AMFI endpoints without embedding API tokens or secret keys.

---

## 2. API Contract & Output Fields

- **Upstream Endpoint:** `https://api.mfapi.in/mf/<scheme_code>`
- **HTTP Method:** `GET`
- **Output CSV Schema:**
  - `scheme_code` (Integer): AMFI 6-digit identifier
  - `scheme_name` (Text): Full fund title
  - `fund_house` (Text): Asset Management Company
  - `category` (Text): SEBI asset classification
  - `date` (ISO Date): Trading date `YYYY-MM-DD`
  - `nav` (Float): Net Asset Value in INR
  - `daily_return` (Float): Decimal arithmetic return

---

## 3. How to Run & Verify

Run from the repository root:
```bash
python3 week_02_fintech_fundamentals/api_extraction/api_extraction.py --scheme 118632 --limit 100
```
Inspect the exported CSV:
```bash
head -n 10 week_02_fintech_fundamentals/api_extraction/extracted_fund_data.csv
```
