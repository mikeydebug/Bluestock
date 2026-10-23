#!/usr/bin/env python3
"""
Bluestock FinTech — Mutual Fund Capstone: Educational Fund Recommender Engine
Author: Mayank Soni (Data Analyst Intern)

Provides educational, risk-aligned mutual fund ranking based on investor risk tolerance,
investment horizon, and risk-adjusted performance (Sharpe ratio and composite Fund Scorecard).

DISCLAIMER: This software is designed strictly for academic, educational, and analytical
demonstration purposes. It does NOT constitute personalized financial, investment, or legal advice.
Past performance is no guarantee of future returns.
"""

import argparse
import os
import sqlite3
import sys
from typing import Dict, List

import pandas as pd

DB_PATH = "mutual_fund_capstone/data/db/mutual_funds.db"


def recommend_funds(risk_tolerance: str, horizon_years: int = 3, top_n: int = 3) -> pd.DataFrame:
    """
    Filters and ranks funds matching investor risk tolerance and horizon.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run run_pipeline.py first.")
        
    conn = sqlite3.connect(DB_PATH)
    
    query = """
    SELECT 
        f.scheme_code,
        f.reference_name,
        f.scheme_name,
        f.fund_house,
        f.category,
        f.risk_grade,
        f.expense_ratio,
        p.cagr_3y,
        p.volatility_ann,
        p.sharpe_ratio,
        p.alpha,
        p.max_drawdown,
        p.fund_score
    FROM dim_fund f
    JOIN fact_performance p ON f.fund_id = p.fund_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Risk tolerance mapping
    risk_tolerance = risk_tolerance.strip().title()
    if risk_tolerance in ["Low", "Conservative"]:
        allowed_grades = ["Low", "Moderate"]
    elif risk_tolerance in ["Moderate", "Balanced"]:
        allowed_grades = ["Low", "Moderate", "High"]
    elif risk_tolerance in ["High", "Aggressive", "Very High"]:
        allowed_grades = ["Moderate", "High", "Very High"]
    else:
        allowed_grades = list(df["risk_grade"].unique())
        
    filtered = df[df["risk_grade"].isin(allowed_grades)].copy()
    
    # Horizon adjustments: If short horizon (<2 years), prioritize low volatility / money market
    if horizon_years < 2:
        filtered.sort_values(by=["volatility_ann", "sharpe_ratio"], ascending=[True, False], inplace=True)
    else:
        # Long horizon: Rank by composite fund score and Sharpe ratio
        filtered.sort_values(by=["fund_score", "sharpe_ratio"], ascending=[False, False], inplace=True)
        
    return filtered.head(top_n)


def main():
    parser = argparse.ArgumentParser(description="Bluestock FinTech Mutual Fund Recommendation Engine")
    parser.add_argument("--risk", type=str, default="Moderate", choices=["Low", "Moderate", "High", "Conservative", "Aggressive"], help="Investor risk profile")
    parser.add_argument("--horizon", type=int, default=3, help="Investment horizon in years")
    parser.add_argument("--top", type=int, default=3, help="Number of funds to recommend")
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("BLUESTOCK FINTECH — EDUCATIONAL MUTUAL FUND RECOMMENDER ENGINE")
    print("="*80)
    print(f"Investor Risk Profile: {args.risk.upper()} | Investment Horizon: {args.horizon} Year(s)")
    print("DISCLAIMER: For educational analytics only; not personalized financial advice.")
    print("-" * 80)
    
    try:
        recommendations = recommend_funds(args.risk, args.horizon, args.top)
        display_cols = [
            "reference_name", "scheme_name", "category", "risk_grade", 
            "cagr_3y", "sharpe_ratio", "volatility_ann", "fund_score"
        ]
        print(recommendations[display_cols].to_string(index=False))
        print("="*80 + "\n")
    except Exception as e:
        print(f"Error running recommendation engine: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
