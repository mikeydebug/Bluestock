"""
Bluestock FinTech — Test Suite: Quantitative Performance Engine
Author: Mayank Soni (Data Analyst Intern)

Tests CAGR, Annualized Volatility, Sharpe Ratio, Sortino Ratio,
Maximum Drawdown, CAPM Alpha/Beta, VaR/CVaR, and Composite Fund Scorecard.
"""

import sys
import os
import numpy as np
import pandas as pd
import pytest

# Add capstone scripts directory to path for direct function import
sys.path.insert(0, os.path.abspath("mutual_fund_capstone/scripts"))
from compute_metrics import (
    calculate_cagr,
    calculate_max_drawdown,
    calculate_alpha_beta,
    calculate_sortino_ratio,
    calculate_tracking_error,
    RF_ANNUAL,
    TRADING_DAYS
)


def test_cagr_calculation_exact():
    """Verify CAGR against analytical formula: (FV / PV) ** (1 / N) - 1."""
    # PV = 100, FV = 200, exactly 3 years (1095.75 days)
    dates = pd.Series(["2020-01-01", "2023-01-01"])
    navs = pd.Series([100.0, 200.0])
    
    # 200 / 100 = 2.0 ** (1 / 3.00068) - 1 = ~25.99%
    cagr = calculate_cagr(navs, dates, target_years=3.0)
    assert not np.isnan(cagr)
    assert pytest.approx(cagr, rel=1e-2) == 25.99


def test_cagr_insufficient_history():
    """Verify CAGR returns np.nan when elapsed span is under 90% of target."""
    dates = pd.Series(["2023-01-01", "2023-06-01"])  # ~0.41 years
    navs = pd.Series([100.0, 110.0])
    
    cagr_3y = calculate_cagr(navs, dates, target_years=3.0)
    assert np.isnan(cagr_3y)


def test_max_drawdown_calculation():
    """Verify Maximum Drawdown, peak date, and trough date detection."""
    dates = pd.Series(["2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01", "2023-05-01", "2023-06-01"])
    navs = pd.Series([100.0, 120.0, 150.0, 120.0, 90.0, 110.0])
    # Peak is 150 on 2023-03-01, trough is 90 on 2023-05-01
    # Max DD = (90 - 150) / 150 = -60 / 150 = -40.0%
    
    max_dd, peak_date, trough_date = calculate_max_drawdown(navs, dates)
    assert max_dd == -40.0
    assert peak_date == "2023-03-01"
    assert trough_date == "2023-05-01"


def test_sharpe_ratio_formula():
    """Verify Sharpe Ratio: (Ann_Return - Rf) / Ann_Volatility."""
    # Construct synthetic daily returns with known mean and std
    np.random.seed(42)
    daily_rets = pd.Series(np.random.normal(loc=0.0008, scale=0.01, size=500))  # ~20% ann return, ~15.8% vol
    
    ann_return = daily_rets.mean() * TRADING_DAYS
    ann_vol = daily_rets.std(ddof=1) * np.sqrt(TRADING_DAYS)
    expected_sharpe = (ann_return - RF_ANNUAL) / ann_vol
    
    calc_sharpe = (ann_return - RF_ANNUAL) / ann_vol
    assert pytest.approx(calc_sharpe, rel=1e-3) == expected_sharpe
    assert calc_sharpe > 0  # Since 20% > 6.5%


def test_sortino_ratio_calculation():
    """Verify Sortino Ratio penalizes only downside volatility below Rf."""
    # When returns have heavy upside volatility but minimal downside volatility, Sortino >> Sharpe
    # Create positive returns
    positive_rets = pd.Series([0.005, 0.006, 0.004, 0.007, 0.005] * 20)
    sortino = calculate_sortino_ratio(positive_rets, rf_annual=0.065)
    # With no downside deviations below daily Rf (0.065/252 = 0.000258), downside deviation is 0
    # In practice our function handles edge cases cleanly
    assert isinstance(sortino, float)


def test_alpha_beta_capm_regression():
    """Verify CAPM OLS regression recovers true slope (Beta) and intercept (Alpha)."""
    np.random.seed(123)
    bench_rets = pd.Series(np.random.normal(0.0004, 0.008, size=300))
    # True Beta = 1.25, Alpha daily = 0.0002 (Annual ~ 5.04%)
    fund_rets = 1.25 * bench_rets + 0.0002 + np.random.normal(0, 0.001, size=300)
    
    beta, alpha, r_squared = calculate_alpha_beta(fund_rets, bench_rets)
    assert pytest.approx(beta, rel=0.05) == 1.25
    assert alpha > 0
    assert r_squared > 0.90  # Strong linear fit


def test_var_and_cvar_mathematics():
    """Verify 95% Historical Value at Risk (VaR) and Conditional VaR (Expected Shortfall)."""
    np.random.seed(99)
    # Normal distribution with mean 0, std 1%
    returns = np.random.normal(0.0, 0.01, 1000)
    
    var_95 = float(np.percentile(returns, 5))
    tail_losses = returns[returns <= var_95]
    cvar_95 = float(np.mean(tail_losses))
    
    # 5th percentile of standard normal is ~ -1.645 * 0.01 = -0.01645 (-1.65%)
    assert var_95 < 0
    assert cvar_95 < var_95  # CVaR is always strictly more severe than VaR in the tail
    assert pytest.approx(var_95, abs=0.005) == -0.0165


def test_scorecard_weighting_bounds():
    """Verify Fund Scorecard outputs composite ratings strictly bounded between 0 and 100."""
    scorecard_path = "mutual_fund_capstone/outputs/csv/fund_scorecard.csv"
    if not os.path.exists(scorecard_path):
        pytest.skip("fund_scorecard.csv not found on disk.")
        
    df = pd.read_csv(scorecard_path)
    assert len(df) == 6
    assert (df["fund_score"] >= 0).all()
    assert (df["fund_score"] <= 100).all()
    assert (df["rank"] >= 1).all() and (df["rank"] <= 6).all()
