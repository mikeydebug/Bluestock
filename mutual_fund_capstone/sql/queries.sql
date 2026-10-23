-- ============================================================================
-- BLUESTOCK FINTECH — MUTUAL FUND ANALYTICS PRODUCTION SQL QUERIES
-- Author: Mayank Soni (Data Analyst Intern)
-- Topic: Analytical SQL for Database Verification, Reporting, and BI Feeds
-- ============================================================================

-- QUERY 1: Scheme Profile & Latest AUM Summary
SELECT 
    f.fund_id,
    f.scheme_code,
    f.scheme_name,
    f.fund_house,
    f.category,
    f.expense_ratio,
    f.risk_grade,
    a.aum_crores AS latest_aum_crores,
    a.folio_count AS latest_folios,
    a.date_id AS aum_as_of_date
FROM dim_fund f
LEFT JOIN fact_aum a ON f.fund_id = a.fund_id
WHERE a.date_id = (SELECT MAX(date_id) FROM fact_aum WHERE fund_id = f.fund_id)
ORDER BY a.aum_crores DESC;

-- QUERY 2: Quantitative Fund Scorecard & Risk-Adjusted Ranking
SELECT 
    f.scheme_code,
    f.scheme_name,
    f.category,
    f.risk_grade,
    p.cagr_3y,
    p.volatility_ann,
    p.sharpe_ratio,
    p.sortino_ratio,
    p.alpha,
    p.beta,
    p.max_drawdown,
    p.fund_score,
    DENSE_RANK() OVER (ORDER BY p.fund_score DESC) AS overall_rank
FROM fact_performance p
JOIN dim_fund f ON p.fund_id = f.fund_id
ORDER BY p.fund_score DESC;

-- QUERY 3: Monthly Inflow Velocity & SIP Contribution
SELECT 
    SUBSTR(t.date_id, 1, 7) AS transaction_month,
    COUNT(t.transaction_id) AS total_transactions,
    ROUND(SUM(CASE WHEN t.trans_type = 'SIP' THEN t.amount ELSE 0 END), 2) AS sip_inflow_inr,
    ROUND(SUM(CASE WHEN t.trans_type = 'Lumpsum' THEN t.amount ELSE 0 END), 2) AS lumpsum_inflow_inr,
    ROUND(SUM(CASE WHEN t.trans_type = 'Redemption' THEN t.amount ELSE 0 END), 2) AS redemption_outflow_inr,
    ROUND(
        (SUM(CASE WHEN t.trans_type = 'SIP' THEN t.amount ELSE 0 END) +
         SUM(CASE WHEN t.trans_type = 'Lumpsum' THEN t.amount ELSE 0 END) -
         SUM(CASE WHEN t.trans_type = 'Redemption' THEN t.amount ELSE 0 END)), 2
    ) AS net_capital_inflow_inr
FROM fact_transactions t
GROUP BY SUBSTR(t.date_id, 1, 7)
ORDER BY transaction_month DESC;

-- QUERY 4: Demographic & Geographic Concentration (T30 vs B30)
SELECT 
    t.city_tier,
    t.investor_state,
    COUNT(DISTINCT t.investor_id) AS active_investors,
    COUNT(t.transaction_id) AS transaction_volume,
    ROUND(SUM(t.amount), 2) AS total_invested_inr,
    ROUND(AVG(t.amount), 2) AS avg_ticket_size_inr,
    ROUND(
        SUM(t.amount) * 100.0 / (SELECT SUM(amount) FROM fact_transactions), 2
    ) AS pct_of_total_inflow
FROM fact_transactions t
GROUP BY t.city_tier, t.investor_state
ORDER BY total_invested_inr DESC;

-- QUERY 5: Age Group Investment Preferences & Ticket Sizes
SELECT 
    t.investor_age_group,
    f.category,
    COUNT(t.transaction_id) AS order_count,
    ROUND(SUM(t.amount), 2) AS aggregate_investment,
    ROUND(AVG(t.amount), 2) AS avg_ticket_size
FROM fact_transactions t
JOIN dim_fund f ON t.fund_id = f.fund_id
GROUP BY t.investor_age_group, f.category
ORDER BY t.investor_age_group, aggregate_investment DESC;

-- QUERY 6: Running Drawdown & Worst Capital Impairment Check
SELECT 
    f.scheme_name,
    MIN(n.daily_return) AS worst_single_day_return,
    MAX(n.daily_return) AS best_single_day_return,
    ROUND(AVG(n.daily_return) * 100, 4) AS avg_daily_return_pct,
    COUNT(n.nav_id) AS total_trading_days
FROM fact_nav n
JOIN dim_fund f ON n.fund_id = f.fund_id
GROUP BY f.fund_id, f.scheme_name;
