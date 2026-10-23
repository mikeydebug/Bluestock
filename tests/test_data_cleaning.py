"""
Bluestock FinTech — Test Suite: Data Cleaning & Ingestion Validation
Author: Mayank Soni (Data Analyst Intern)

Tests date parsing, NAV positivity enforcement, duplicate elimination,
non-trading day policy compliance, and data schema integrity.
"""

import datetime
import os
import numpy as np
import pandas as pd
import pytest


def test_date_parsing_valid():
    """Verify that standard Indian mutual fund date strings (DD-MM-YYYY) parse to ISO (YYYY-MM-DD)."""
    raw_dates = ["01-01-2024", "15-08-2023", "29-02-2024"]  # Note 2024 is leap year
    expected = ["2024-01-01", "2023-08-15", "2024-02-29"]
    
    parsed = [datetime.datetime.strptime(d, "%d-%m-%Y").date().isoformat() for d in raw_dates]
    assert parsed == expected


def test_date_parsing_invalid():
    """Verify that invalid date formats raise ValueError."""
    invalid_dates = ["32-01-2024", "2024-02-30", "not-a-date", ""]
    for d in invalid_dates:
        with pytest.raises(ValueError):
            datetime.datetime.strptime(d, "%d-%m-%Y")


def test_nav_positivity_enforcement():
    """Verify that non-positive NAV values (<= 0) are strictly rejected."""
    raw_navs = [15.25, 0.0, -10.5, 102.45, "invalid", None]
    valid_navs = []
    
    for val in raw_navs:
        try:
            num = float(val)
            if num > 0:
                valid_navs.append(num)
        except (ValueError, TypeError):
            continue
            
    assert valid_navs == [15.25, 102.45]
    assert all(n > 0 for n in valid_navs)


def test_duplicate_detection_and_deduplication():
    """Verify that duplicate observations on (fund_id, date_id) are removed keeping the first."""
    records = [
        {"fund_id": 1, "date_id": "2024-01-02", "nav": 100.50},
        {"fund_id": 1, "date_id": "2024-01-02", "nav": 100.55},  # Duplicate
        {"fund_id": 1, "date_id": "2024-01-03", "nav": 101.20},
        {"fund_id": 2, "date_id": "2024-01-02", "nav": 55.10},
    ]
    df = pd.DataFrame(records)
    assert len(df) == 4
    
    deduped = df.drop_duplicates(subset=["fund_id", "date_id"], keep="first")
    assert len(deduped) == 3
    assert deduped.iloc[0]["nav"] == 100.50  # First kept


def test_non_trading_day_policy_no_forward_fill():
    """
    Verify that weekend/holiday gaps are NOT forward-filled.
    Trading calendars must respect actual exchange closure dates.
    """
    dates = pd.date_range("2024-01-01", "2024-01-07")  # Mon to Sun
    # Simulating authentic exchange data: Fri Jan 5 has NAV, Sat/Sun Jan 6/7 do not
    nav_series = pd.Series([100.0, 101.0, 101.5, 102.0, 103.0, np.nan, np.nan], index=dates)
    
    # Under our strict ETL policy, no ffill() is performed on raw observations
    clean_series = nav_series.dropna()
    assert len(clean_series) == 5
    assert "2024-01-06" not in clean_series.index.strftime("%Y-%m-%d")
    assert "2024-01-07" not in clean_series.index.strftime("%Y-%m-%d")


def test_daily_return_calculation():
    """Verify daily return calculation formula: R_t = (NAV_t - NAV_{t-1}) / NAV_{t-1}."""
    navs = pd.Series([100.0, 105.0, 102.9, 102.9])
    expected_returns = [np.nan, 0.05, -0.02, 0.0]
    
    calc_returns = navs.pct_change()
    np.testing.assert_allclose(calc_returns.values[1:], expected_returns[1:], rtol=1e-4)
    assert pd.isna(calc_returns.iloc[0])


def test_dim_fund_file_structure():
    """Verify that clean_dim_fund.csv contains all required master attributes and valid ranges."""
    file_path = "mutual_fund_capstone/data/processed/clean_dim_fund.csv"
    if not os.path.exists(file_path):
        pytest.skip("clean_dim_fund.csv not yet built on disk.")
        
    df = pd.read_csv(file_path)
    required_cols = {"fund_id", "scheme_code", "reference_name", "scheme_name", "fund_house", "category", "expense_ratio", "risk_grade"}
    assert required_cols.issubset(set(df.columns))
    assert len(df) == 6
    assert (df["expense_ratio"] > 0).all()
    assert (df["expense_ratio"] < 3.0).all()  # SEBI expense ratio cap
