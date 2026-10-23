# Mutual Fund Analytics Capstone — Quantitative Methodology & Assumptions

**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Topic:** Quantitative Modeling & Risk Analytics Methodology  

---

## 1. Core Financial Methodology & Formulas

### 1.1 Return Generation
Daily arithmetic returns are calculated per individual fund scheme:
$$R_{i, t} = \frac{NAV_{i, t} - NAV_{i, t-1}}{NAV_{i, t-1}}$$
Returns are only calculated between sequential active trading observations.

### 1.2 Compound Annual Growth Rate (CAGR)
$$\text{CAGR} = \left(\frac{NAV_{\text{end}}}{NAV_{\text{start}}}\right)^{\frac{1}{Y}} - 1$$
where $Y = \frac{\text{Calendar Days Between End and Start}}{365.25}$.
- 1-Year CAGR: $Y \approx 1.0$ (minimum 250 observations required)
- 3-Year CAGR: $Y \approx 3.0$ (minimum 750 observations required)
- 5-Year CAGR: $Y \approx 5.0$ (minimum 1,250 observations required)

### 1.3 Annualised Volatility
$$\sigma_{\text{ann}} = \sigma_{\text{daily}} \times \sqrt{252}$$
where $\sigma_{\text{daily}} = \sqrt{\frac{1}{N-1} \sum_{t=1}^N (R_t - \bar{R})^2}$.

### 1.4 Sharpe Ratio
$$\text{Sharpe Ratio} = \frac{R_{\text{ann}} - R_f}{\sigma_{\text{ann}}}$$
- **Risk-Free Rate Assumption:** $R_f = 6.5\%$ annualised ($0.065$).
- **Annualised Portfolio Return:** $R_{\text{ann}} = \bar{R}_{\text{daily}} \times 252$.

### 1.5 Sortino Ratio
Measures return relative to downside semideviation:
$$\text{Sortino Ratio} = \frac{R_{\text{ann}} - R_f}{\sigma_{\text{downside, ann}}}$$
where $\sigma_{\text{downside, ann}} = \sqrt{\frac{1}{N} \sum_{t=1}^N \min(0, R_t - \frac{R_f}{252})^2} \times \sqrt{252}$.

### 1.6 Systematic Risk (Beta) and Jensen's Alpha via OLS
Using `scipy.stats.linregress` on aligned fund and NIFTY 100 daily returns:
$$R_{\text{fund}, t} = \alpha_{\text{daily}} + \beta \times R_{\text{market}, t} + \epsilon_t$$
- **Beta ($\beta$):** Regression slope measuring sensitivity to market movements.
- **Annualised Arithmetic Alpha ($\alpha$):**
  $$\alpha_{\text{ann}} = \alpha_{\text{daily}} \times 252 \times 100 \quad (\text{percentage})$$

### 1.7 Maximum Drawdown (MDD)
$$\text{Drawdown}_t = \frac{NAV_t}{\max_{\tau \le t} NAV_\tau} - 1$$
$$\text{Max Drawdown} = \min_{t} (\text{Drawdown}_t)$$
The peak date is the timestamp of the running maximum prior to the drawdown trough.

### 1.8 Composite Multi-Factor Fund Scorecard (0–100)
The rubric's composite weighted ranking:
$$\text{Raw Score} = 0.30 \times P_{\text{3Y Return}} + 0.25 \times P_{\text{Sharpe}} + 0.20 \times P_{\text{Alpha}} + 0.15 \times P_{\text{TER}}^{-1} + 0.10 \times P_{\text{MaxDD}}^{-1}$$
where $P_X$ is the percentile rank ($0 \le P \le 100$).
- Higher 3Y Return, Sharpe, and Alpha yield higher percentile ranks.
- Lower TER and shallower Maximum Drawdown yield higher percentile ranks.
- Scaled linearly to a clean 0–100 range.

### 1.9 Historical 95% Value at Risk (VaR) and CVaR
- **Daily 95% VaR (Signed Return Quantile):** 5th percentile of daily return distribution.
- **Daily 95% Loss VaR (%):** Negative of the 5th percentile return.
- **Conditional VaR (CVaR / Expected Shortfall):** Mean of daily returns falling at or below the 5th percentile.

### 1.10 Herfindahl-Hirschman Index (HHI) for Sector Concentration
$$\text{HHI} = \sum_{k=1}^K (\text{Sector Weight}_k)^2$$
Where weights are expressed on a 0–100 percentage scale.
- $\text{HHI} < 1500$: Highly Diversified
- $1500 \le \text{HHI} \le 2500$: Moderately Concentrated
- $\text{HHI} > 2500$: Highly Concentrated
