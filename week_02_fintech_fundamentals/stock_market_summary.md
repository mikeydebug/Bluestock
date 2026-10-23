# Week 2 — Indian Capital Markets & Corporate Valuation Fundamentals

**Author:** Mayank Soni (B.Tech Computer Science)  
**Role:** Data Analyst Intern  
**Organization:** Bluestock Fintech  
**Topic:** FinTech Domain & Financial Economics  

---

## 1. Indian Capital Market Architecture

The Indian securities ecosystem is governed under the statutory oversight of the **Securities and Exchange Board of India (SEBI)** established under the SEBI Act, 1992.

```
                      ┌─────────────────────────────────┐
                      │    SEBI (Regulator & Auditor)   │
                      └────────────────┬────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────┐                             ┌───────────────────────┐
│ National Stock Exch.  │                             │ Bombay Stock Exchange │
│        (NSE)          │                             │        (BSE)          │
│ Benchmark: NIFTY 50   │                             │  Benchmark: SENSEX    │
└───────────┬───────────┘                             └───────────┬───────────┘
            │                                                     │
            └──────────────────────────┬──────────────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │   Depositories (NSDL & CDSL)    │
                      │  Clearing Corp (NSCCL & ICCL)   │
                      └────────────────┬────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │ Registered Brokerages & FinTechs│
                      │  (Zerodha, Groww, AngelOne)     │
                      └─────────────────────────────────┘
```

### 1.1 Exchanges & Benchmark Indices
- **National Stock Exchange (NSE):** Established in 1992 as the first demutualized electronic exchange in India. Operates the **NIFTY 50**, a free-float market-capitalization-weighted index comprising 50 of the largest and most liquid Indian blue-chip stocks spanning 13 sectors.
- **Bombay Stock Exchange (BSE):** Established in 1875 (Asia's oldest exchange). Operates the **S&P BSE SENSEX**, a free-float market-capitalization-weighted index of 30 well-established, financially sound companies.
- **Trading Mechanisms:** T+1 rolling settlement cycle (with select T+0 instantaneous settlement pilots introduced by SEBI in 2024).

### 1.2 Primary vs. Secondary Markets: IPO & SME IPO
- **Initial Public Offering (IPO):** The primary market mechanism whereby an unlisted private corporation issues fresh equity shares or an Offer for Sale (OFS) to the public to raise long-term capital and list on the main board (NSE/BSE). Requires minimum net tangible assets of ₹3 Cr and average operating profit of ₹15 Cr across 3 prior years.
- **SME IPO:** Tailored listing platforms (NSE Emerge, BSE SME) designed for Small and Medium Enterprises with lower post-issue paid-up capital limits (up to ₹25 Cr) and streamlined regulatory compliance, enabling emerging ventures to access public liquidity.

---

## 2. Market Capitalisation Classifications

Market capitalization is the total aggregate equity value of a publicly traded company:
$$\text{Market Capitalisation} = \text{Total Outstanding Shares} \times \text{Current Market Price (CMP)}$$

SEBI categorizes listed equity stocks into standardized tiers (revised semi-annually by AMFI):
1. **Large Cap:** Top 1st to 100th company in terms of full market capitalization (e.g., Reliance Industries, TCS, HDFC Bank). Characterized by lower volatility, institutional stability, and steady dividend yields.
2. **Mid Cap:** 101st to 250th company by market capitalization. Balances higher growth trajectory with moderate operational volatility.
3. **Small Cap:** 251st company onwards by market capitalization. High growth potential accompanied by liquidity constraints, wider bid-ask spreads, and elevated downside risk.

---

## 3. Financial Ratios & Valuation Metrics

### 3.1 Earnings Per Share (EPS)
$$\text{Diluted EPS} = \frac{\text{Net Profit After Tax (PAT)} - \text{Preferred Dividends}}{\text{Weighted Average Number of Diluted Shares Outstanding}}$$
EPS reflects the portion of a company's profit allocated to each share of common stock.

### 3.2 Price-to-Earnings Ratio (P/E)
$$\text{P/E Ratio} = \frac{\text{Current Market Price per Share}}{\text{Annual Earnings Per Share (EPS)}}$$
- **Trailing Twelve Months (TTM) P/E:** Based on realized past earnings.
- **Forward P/E:** Based on projected consensus earnings estimates.
- *Analytical Use:* Indicates how many rupees investors are willing to pay today for every ₹1 of company earnings. High P/E may imply expected rapid future earnings growth or market overvaluation.

### 3.3 Price-to-Book Ratio (P/B)
$$\text{P/B Ratio} = \frac{\text{Current Market Price per Share}}{\text{Book Value per Share (BVPS)}}$$
where $\text{BVPS} = \frac{\text{Total Equity Shareholders' Funds} - \text{Intangible Assets}}{\text{Total Outstanding Shares}}$.
- *Analytical Use:* Standard metric for capital-intensive sectors and banking institutions (e.g., HDFC Bank, SBI) where physical and financial book assets generate earnings.

### 3.4 Dividend Yield & Corporate Actions
- **Dividend Yield:** $\frac{\text{Annual Dividend per Share}}{\text{Current Market Price}} \times 100\%$.
- **Stock Split:** Dividing existing shares into multiple shares (e.g., a 1:2 split halves face value and share price while doubling total share count). Increases retail liquidity without changing market capitalization.
- **Bonus Shares:** Free additional shares granted to existing shareholders funded out of free reserves/surplus, demonstrating balance sheet strength.
- **Trading Volume:** The aggregate number of shares transacted over a given timeframe; confirms breakout strength and price momentum.

---

## 4. The Three Primary Financial Statements

Financial analysts synthesize three mandatory audited statements to evaluate corporate financial health:

### 4.1 Balance Sheet (Statement of Financial Position)
- **Accounting Equation:** $\text{Assets} = \text{Liabilities} + \text{Shareholders' Equity}$
- **Current vs. Non-Current:** Distinguishes short-term working capital (cash, receivables, inventory $< 12$ months) from long-term capital assets (plant, property, equipment, patents).

### 4.2 Profit & Loss Statement (Statement of Comprehensive Income)
$$\text{Net Revenue} - \text{COGS} = \text{Gross Profit}$$
$$\text{Gross Profit} - \text{Operating Expenses} = \text{EBITDA}$$
$$\text{EBITDA} - \text{Depreciation \& Amortization} = \text{EBIT (Operating Profit)}$$
$$\text{EBIT} - \text{Finance Costs} + \text{Other Income} = \text{EBT (Profit Before Tax)}$$
$$\text{EBT} - \text{Tax Expense} = \text{PAT (Profit After Tax)}$$

### 4.3 Cash Flow Statement (AS-3 / Ind AS 7)
Reconciles accrual accounting net income with actual liquid cash generation across three activity categories:
1. **Cash Flow from Operating Activities (CFO):** Core cash generated from primary customer operations. If $\text{CFO} < \text{PAT}$ consistently, it flags aggressive accrual accounting or inventory build-up.
2. **Cash Flow from Investing Activities (CFI):** Capital expenditure (CapEx) in property, infrastructure, or acquisitions.
3. **Cash Flow from Financing Activities (CFF):** Issuance/repayment of debt, equity buybacks, and dividend payments.

---

## 5. Distinction Between Historical and Current Information
- **Audited Financial Statements (Historical):** Represent statutory, historical accounting truths for specific completed financial years (e.g., FY2023-24 ended March 31, 2024). They are immutable and verified by independent statutory auditors.
- **Real-Time Market Prices (Current):** Continuously fluctuate during live exchange trading hours based on instantaneous order matching, macroeconomic rate expectations, and market sentiment.
- *Analytical Caveat:* Ratios combining market price with historical earnings (such as TTM P/E) bridge real-time valuation with historical fundamental performance.
