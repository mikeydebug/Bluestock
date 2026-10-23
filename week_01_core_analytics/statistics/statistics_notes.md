# Week 1 — Comprehensive Statistics & Quantitative Foundations

**Author:** Mayank Soni (B.Tech Computer Science)  
**Role:** Data Analyst Intern  
**Organization:** Bluestock Fintech  
**Topic:** Core Data Analytics Foundation — Statistical Methods in Financial Analytics  

---

## 1. Measures of Central Tendency

Measures of central tendency identify the single summary value that attempts to describe a set of data by identifying the central position within that dataset.

### 1.1 Arithmetic Mean vs. Geometric Mean
- **Arithmetic Mean ($\mu$ or $\bar{X}$):**
  $$\bar{X} = \frac{1}{N} \sum_{i=1}^N X_i$$
  *Financial Application:* Suitable for calculating average daily returns over a short horizon.
  *Limitation:* Highly sensitive to extreme outliers. If a dataset has daily returns $[-50\%, +100\%]$, the arithmetic mean is $+25\%$, but the investor actually has zero net capital gain ($1 \times 0.5 \times 2 = 1.0$).
- **Geometric Mean ($G$):**
  $$G = \left( \prod_{i=1}^N (1 + R_i) \right)^{1/N} - 1$$
  *Financial Application:* Compulsory for multi-period compounding returns (CAGR), because it accounts for sequence and portfolio compounding effects.

### 1.2 Median
- **Definition:** The middle value when data is sorted in ascending order.
  $$\text{Median} = \begin{cases} X_{(N+1)/2} & \text{if } N \text{ is odd} \\ \frac{X_{(N/2)} + X_{(N/2 + 1)}}{2} & \text{if } N \text{ is even} \end{cases}$$
- *Financial Application:* Essential for skewed distributions, such as retail investor account balances or executive compensation, where a few ultra-wealthy outliers distort the arithmetic mean.

### 1.3 Mode
- **Definition:** The observation that appears with the highest frequency.
- *Financial Application:* Identifying the most common SIP installment date (e.g., 5th or 10th of every month) or most common ticket size (e.g., ₹1,000 or ₹5,000).

---

## 2. Measures of Dispersion & Risk

In finance and investment analytics, dispersion is the mathematical equivalent of **financial risk** or uncertainty.

### 2.1 Variance ($\sigma^2$) and Standard Deviation ($\sigma$)
- **Sample Variance ($s^2$):**
  $$s^2 = \frac{1}{N-1} \sum_{i=1}^N (X_i - \bar{X})^2$$
  *Why $N-1$ (Bessel's Correction):* Corrects for the downward bias in estimating population variance from a sample.
- **Sample Standard Deviation ($s$):**
  $$s = \sqrt{s^2}$$
- **Annualised Volatility ($\sigma_{\text{ann}}$):**
  $$\sigma_{\text{ann}} = \sigma_{\text{daily}} \times \sqrt{252}$$
  *Why $\sqrt{252}$:* Under the assumption of independent and identically distributed (i.i.d.) returns, variance scales linearly with time ($252 \times \sigma^2$), meaning standard deviation scales with the square root of trading days ($\sqrt{252}$).

### 2.2 Semideviation & Downside Risk
Standard deviation treats positive upside gains (a +10% rally) and negative downside plunges (a -10% crash) as equally bad. Downside semideviation isolates only returns falling below a minimum acceptable return (MAR):
$$\sigma_{\text{downside}} = \sqrt{\frac{1}{N} \sum_{t=1}^N \min(0, R_t - \text{MAR})^2}$$
This serves as the core denominator of the **Sortino Ratio**.

---

## 3. Association & Covariance

### 3.1 Pearson Correlation Coefficient ($r$)
Measures the strength and direction of the linear relationship between two continuous variables:
$$r_{X, Y} = \frac{\sum_{i=1}^N (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^N (X_i - \bar{X})^2} \sqrt{\sum_{i=1}^N (Y_i - \bar{Y})^2}} \in [-1, +1]$$

| $r$ Value Range | Interpretation | Financial Portfolio Implication |
|---|---|---|
| $+0.80 \text{ to } +1.00$ | Very strong positive | Both assets move in lockstep; low diversification benefit |
| $+0.30 \text{ to } +0.70$ | Moderate positive | Typical of equity funds in the same market sector |
| $-0.30 \text{ to }+0.30$ | Negligible / Uncorrelated | Ideal for multi-asset diversification (e.g., Gold vs Equities) |
| $-0.70 \text{ to } -1.00$ | Strong negative | Perfect hedging pair; cushions overall portfolio drawdown |

---

## 4. Basic Probability & Risk Modeling

### 4.1 Fundamental Rules
- **Addition Rule for Mutually Exclusive Events:** $P(A \cup B) = P(A) + P(B)$
- **Multiplication Rule for Independent Events:** $P(A \cap B) = P(A) \times P(B)$

### 4.2 Conditional Probability & Bayes' Theorem
The probability of event $A$ occurring given that event $B$ has already occurred:
$$P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{P(B \mid A) P(A)}{P(B)}$$
*FinTech Application:* Credit scoring and fraud detection. Given that a transaction occurs from a foreign IP at 3:00 AM ($B$), what is the probability that it is fraudulent ($A$)?

---

## 5. Introductory Linear Regression & Capital Asset Pricing (CAPM)

### 5.1 Simple Ordinary Least Squares (OLS) Regression
Models the dependency of a response variable $Y$ on an explanatory variable $X$:
$$Y_i = \alpha + \beta X_i + \epsilon_i$$
The objective is to minimize the Sum of Squared Residuals (SSR):
$$\min_{\alpha, \beta} \sum_{i=1}^N (Y_i - (\alpha + \beta X_i))^2$$

- **Slope ($\beta$):**
  $$\beta = \frac{\text{Cov}(X, Y)}{\text{Var}(X)} = \frac{\sum (X_i - \bar{X})(Y_i - \bar{Y})}{\sum (X_i - \bar{X})^2}$$
- **Intercept ($\alpha$):**
  $$\alpha = \bar{Y} - \beta \bar{X}$$

### 5.2 Financial Interpretation in Mutual Funds
When regressing a mutual fund's daily returns ($Y = R_{\text{fund}}$) against the market benchmark ($X = R_{\text{market}}$):
1. **Beta ($\beta$):** Measures systematic market risk.
   - $\beta = 1.0$: Fund volatility matches the broader market index.
   - $\beta > 1.0$: High-beta aggressive fund (e.g., Small-Cap fund with $\beta = 1.25$ gains 1.25% when market rises 1%, but falls 1.25% when market drops 1%).
   - $\beta < 1.0$: Defensive fund (e.g., FMCG / Large-Cap fund with $\beta = 0.75$).
2. **Alpha ($\alpha$):** Measures manager skill or excess value generated above what market exposure explains.
   $$\text{Annualized Alpha} = \alpha_{\text{daily}} \times 252 \times 100\%$$
   A positive alpha ($>0\%$) indicates that the fund manager outperformed the benchmark on a risk-adjusted basis.
