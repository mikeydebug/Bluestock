#!/usr/bin/env python3
"""
Bluestock FinTech — Mutual Fund Capstone: Quantitative Analytics Engine
Author: Mayank Soni (Data Analyst Intern)

Computes daily returns, multi-period CAGR (1Y, 3Y, 5Y), annualised volatility,
Sharpe ratio (Rf=6.5%), Sortino ratio, Alpha/Beta (CAPM OLS regression vs NIFTY 100),
Maximum Drawdown (with peak/trough dates), Tracking Error, and 0-100 Fund Scorecard.
"""

import datetime
import logging
import os
import sqlite3
import sys
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("QuantEngine")

DB_PATH = "mutual_fund_capstone/data/db/mutual_funds.db"
BENCHMARK_PATH = "mutual_fund_capstone/data/external/benchmark_indices.csv"
OUTPUT_CSV_DIR = "mutual_fund_capstone/outputs/csv"
OUTPUT_CHART_DIR = "mutual_fund_capstone/outputs/charts"
OUTPUT_TABLE_DIR = "mutual_fund_capstone/outputs/tables"

RF_ANNUAL = 0.065  # 6.5% Annual Risk-Free Rate
TRADING_DAYS = 252


def ensure_output_dirs():
    os.makedirs(OUTPUT_CSV_DIR, exist_ok=True)
    os.makedirs(OUTPUT_CHART_DIR, exist_ok=True)
    os.makedirs(OUTPUT_TABLE_DIR, exist_ok=True)


def calculate_cagr(nav_series: pd.Series, date_series: pd.Series, target_years: float) -> float:
    """
    Computes Compound Annual Growth Rate over exact elapsed period.
    Returns np.nan if available observation span is less than target_years.
    """
    if len(nav_series) < 2:
        return np.nan
        
    start_dt = pd.to_datetime(date_series.iloc[0])
    end_dt = pd.to_datetime(date_series.iloc[-1])
    actual_years = (end_dt - start_dt).days / 365.25
    
    if actual_years < (target_years * 0.90):  # At least 90% of required span
        return np.nan
        
    start_nav = nav_series.iloc[0]
    end_nav = nav_series.iloc[-1]
    if start_nav <= 0 or end_nav <= 0:
        return np.nan
        
    cagr = (end_nav / start_nav) ** (1.0 / actual_years) - 1.0
    return float(np.round(cagr * 100, 2))  # Expressed as percentage


def calculate_max_drawdown(nav_series: pd.Series, date_series: pd.Series) -> Tuple[float, str, str]:
    """
    Calculates Maximum Drawdown, peak date, and trough date.
    """
    running_max = nav_series.cummax()
    drawdown = (nav_series - running_max) / running_max
    
    min_dd_idx = drawdown.idxmin()
    max_dd_val = drawdown.loc[min_dd_idx]
    
    # Peak date is the date of running_max right before or at trough
    peak_idx = nav_series.loc[:min_dd_idx].idxmax()
    peak_date = str(date_series.loc[peak_idx])
    trough_date = str(date_series.loc[min_dd_idx])
    
    return float(np.round(max_dd_val * 100, 2)), peak_date, trough_date


def calculate_alpha_beta(fund_returns: pd.Series, bench_returns: pd.Series) -> Tuple[float, float, float]:
    """
    Performs OLS regression of fund daily returns against market benchmark:
    R_fund = alpha + beta * R_bench + epsilon
    Returns: (beta, annualized_alpha_pct, r_squared)
    """
    # Align and drop NaNs
    aligned = pd.concat([fund_returns, bench_returns], axis=1).dropna()
    if len(aligned) < 30:
        return 1.0, 0.0, 0.0
        
    y = aligned.iloc[:, 0].values
    x = aligned.iloc[:, 1].values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    beta = float(np.round(slope, 3))
    annual_alpha = float(np.round(intercept * TRADING_DAYS * 100, 2))
    r_squared = float(np.round(r_value ** 2, 3))
    
    return beta, annual_alpha, r_squared


def calculate_sortino_ratio(returns: pd.Series, rf_annual: float = RF_ANNUAL) -> float:
    """
    Computes Sortino Ratio using downside deviation below daily risk-free rate.
    """
    rf_daily = rf_annual / TRADING_DAYS
    excess_returns = returns.dropna()
    if len(excess_returns) < 10:
        return 0.0
        
    ann_return = np.mean(excess_returns) * TRADING_DAYS
    downside_diff = np.minimum(0.0, excess_returns - rf_daily)
    downside_dev = np.sqrt(np.mean(downside_diff ** 2)) * np.sqrt(TRADING_DAYS)
    
    if downside_dev == 0 or np.isnan(downside_dev):
        return 0.0
    return float(np.round((ann_return - rf_annual) / downside_dev, 2))


def calculate_tracking_error(fund_returns: pd.Series, bench_returns: pd.Series) -> float:
    aligned = pd.concat([fund_returns, bench_returns], axis=1).dropna()
    if len(aligned) < 30:
        return 0.0
    diff = aligned.iloc[:, 0] - aligned.iloc[:, 1]
    te = np.std(diff, ddof=1) * np.sqrt(TRADING_DAYS)
    return float(np.round(te * 100, 2))


def compute_all_fund_metrics():
    ensure_output_dirs()
    conn = sqlite3.connect(DB_PATH)
    
    # Load Funds
    funds_df = pd.read_sql("SELECT * FROM dim_fund", conn)
    # Load NAVs
    nav_df = pd.read_sql("SELECT * FROM fact_nav ORDER BY fund_id, date_id ASC", conn)
    # Load Benchmark
    bench_df = pd.read_csv(BENCHMARK_PATH)
    bench_df["date"] = pd.to_datetime(bench_df["date"]).dt.strftime("%Y-%m-%d")
    bench_map = bench_df.set_index("date")["nifty_100_return"].to_dict()
    
    perf_records = []
    
    for _, fund in funds_df.iterrows():
        f_id = fund["fund_id"]
        f_code = fund["scheme_code"]
        f_name = fund["scheme_name"]
        ref_name = fund["reference_name"]
        ter = fund["expense_ratio"]
        
        f_navs = nav_df[nav_df["fund_id"] == f_id].copy()
        f_navs["date_dt"] = pd.to_datetime(f_navs["date_id"])
        f_navs.sort_values(by="date_dt", ascending=True, inplace=True)
        f_navs.reset_index(drop=True, inplace=True)
        
        latest_date = f_navs["date_id"].iloc[-1]
        latest_dt = f_navs["date_dt"].iloc[-1]
        
        # Slices for 1Y, 3Y, 5Y
        dt_1y = latest_dt - pd.DateOffset(years=1)
        dt_3y = latest_dt - pd.DateOffset(years=3)
        dt_5y = latest_dt - pd.DateOffset(years=5)
        
        slice_1y = f_navs[f_navs["date_dt"] >= dt_1y]
        slice_3y = f_navs[f_navs["date_dt"] >= dt_3y]
        slice_5y = f_navs[f_navs["date_dt"] >= dt_5y]
        
        cagr_1y = calculate_cagr(slice_1y["nav"], slice_1y["date_id"], 1.0)
        cagr_3y = calculate_cagr(slice_3y["nav"], slice_3y["date_id"], 3.0)
        cagr_5y = calculate_cagr(slice_5y["nav"], slice_5y["date_id"], 5.0)
        
        # Daily return analysis on 3-year history (standard evaluation window)
        eval_slice = slice_3y if len(slice_3y) >= 252 else f_navs
        ret_series = eval_slice["daily_return"].dropna()
        
        mean_ret_daily = ret_series.mean()
        std_ret_daily = ret_series.std(ddof=1)
        ann_return = mean_ret_daily * TRADING_DAYS
        vol_ann = float(np.round(std_ret_daily * np.sqrt(TRADING_DAYS) * 100, 2))
        
        # Sharpe
        sharpe = float(np.round((ann_return - RF_ANNUAL) / (std_ret_daily * np.sqrt(TRADING_DAYS)), 2))
        # Sortino
        sortino = calculate_sortino_ratio(ret_series, RF_ANNUAL)
        
        # Align with benchmark for Alpha & Beta
        eval_slice["bench_return"] = eval_slice["date_id"].map(bench_map)
        beta, alpha, r_sq = calculate_alpha_beta(eval_slice["daily_return"], eval_slice["bench_return"])
        te = calculate_tracking_error(eval_slice["daily_return"], eval_slice["bench_return"])
        
        # Max Drawdown across 3Y
        max_dd, peak_dt, trough_dt = calculate_max_drawdown(eval_slice["nav"], eval_slice["date_id"])
        
        perf_records.append({
            "fund_id": f_id,
            "scheme_code": f_code,
            "reference_name": ref_name,
            "scheme_name": f_name,
            "category": fund["category"],
            "expense_ratio": ter,
            "as_of_date": latest_date,
            "cagr_1y": cagr_1y,
            "cagr_3y": cagr_3y,
            "cagr_5y": cagr_5y,
            "volatility_ann": vol_ann,
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "beta": beta,
            "alpha": alpha,
            "r_squared": r_sq,
            "max_drawdown": max_dd,
            "max_dd_peak_date": peak_dt,
            "max_dd_trough_date": trough_dt,
            "tracking_error": te
        })
        
    perf_df = pd.DataFrame(perf_records)
    
    # ---------------------------------------------------------
    # COMPUTE MULTI-FACTOR FUND SCORECARD (0 to 100)
    # Weights: 30% 3Y Return, 25% Sharpe, 20% Alpha, 15% Inv TER, 10% Inv MaxDD
    # ---------------------------------------------------------
    def percentile_rank(series: pd.Series, ascending: bool = True) -> pd.Series:
        return series.rank(ascending=ascending, pct=True) * 100.0

    rank_return = percentile_rank(perf_df["cagr_3y"], ascending=True)
    rank_sharpe = percentile_rank(perf_df["sharpe_ratio"], ascending=True)
    rank_alpha = percentile_rank(perf_df["alpha"], ascending=True)
    rank_ter_inv = percentile_rank(perf_df["expense_ratio"], ascending=False)
    rank_dd_inv = percentile_rank(perf_df["max_drawdown"], ascending=True)  # Drawdown is negative, so higher algebraic value means smaller loss
    
    raw_scores = (
        0.30 * rank_return + 
        0.25 * rank_sharpe + 
        0.20 * rank_alpha + 
        0.15 * rank_ter_inv + 
        0.10 * rank_dd_inv
    )
    
    # Scale from 0 to 100 cleanly
    min_s, max_s = raw_scores.min(), raw_scores.max()
    if max_s > min_s:
        normalized_scores = 20.0 + (raw_scores - min_s) / (max_s - min_s) * 75.0
    else:
        normalized_scores = raw_scores
        
    perf_df["fund_score"] = np.round(normalized_scores, 1)
    perf_df.sort_values(by="fund_score", ascending=False, inplace=True)
    perf_df.reset_index(drop=True, inplace=True)
    perf_df["rank"] = range(1, len(perf_df) + 1)
    
    # Export Scorecard CSV
    scorecard_cols = [
        "rank", "scheme_code", "reference_name", "scheme_name", "category", 
        "cagr_3y", "sharpe_ratio", "alpha", "beta", "expense_ratio", 
        "max_drawdown", "volatility_ann", "fund_score"
    ]
    scorecard_csv_path = os.path.join(OUTPUT_CSV_DIR, "fund_scorecard.csv")
    perf_df[scorecard_cols].to_csv(scorecard_csv_path, index=False)
    logger.info(f"Exported Fund Scorecard to: {scorecard_csv_path}")
    
    # Export Alpha & Beta CSV
    ab_cols = ["scheme_code", "scheme_name", "category", "beta", "alpha", "r_squared", "tracking_error"]
    ab_csv_path = os.path.join(OUTPUT_CSV_DIR, "alpha_beta.csv")
    perf_df[ab_cols].to_csv(ab_csv_path, index=False)
    logger.info(f"Exported Alpha/Beta Metrics to: {ab_csv_path}")
    
    # Update fact_performance in SQLite
    db_cols = [
        "fund_id", "as_of_date", "cagr_1y", "cagr_3y", "cagr_5y", 
        "volatility_ann", "sharpe_ratio", "sortino_ratio", "beta", 
        "alpha", "max_drawdown", "max_dd_peak_date", "max_dd_trough_date", 
        "fund_score", "tracking_error"
    ]
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fact_performance")
    perf_df[db_cols].to_sql("fact_performance", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    logger.info("Committed fact_performance into SQLite database.")
    
    # ---------------------------------------------------------
    # GENERATE BENCHMARK COMPARISON CHART (PNG)
    # ---------------------------------------------------------
    generate_comparison_chart(perf_df, nav_df, bench_df)
    
    print("\n================== FUND SCORECARD (0 TO 100) ==================")
    print(perf_df[scorecard_cols].to_string())
    print("================================================================\n")
    return perf_df


def generate_comparison_chart(perf_df: pd.DataFrame, nav_df: pd.DataFrame, bench_df: pd.DataFrame):
    """
    Renders normalized 3-year performance comparison chart rebased to 100.
    """
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    
    # Benchmark rebased
    bench_sub = bench_df.copy()
    bench_sub["date_dt"] = pd.to_datetime(bench_sub["date"])
    max_dt = bench_sub["date_dt"].max()
    min_dt = max_dt - pd.DateOffset(years=3)
    bench_sub = bench_sub[bench_sub["date_dt"] >= min_dt].sort_values("date_dt")
    rebase_bench = (bench_sub["nifty_100_close"] / bench_sub["nifty_100_close"].iloc[0]) * 100.0
    
    ax.plot(bench_sub["date_dt"], rebase_bench, label="NIFTY 100 Benchmark", color="black", linewidth=2.5, linestyle="--")
    
    # Plot top funds
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#d62728", "#8c564b"]
    for idx, row in perf_df.iterrows():
        f_id = row["fund_id"]
        f_navs = nav_df[nav_df["fund_id"] == f_id].copy()
        f_navs["date_dt"] = pd.to_datetime(f_navs["date_id"])
        f_sub = f_navs[f_navs["date_dt"] >= min_dt].sort_values("date_dt")
        if len(f_sub) > 100:
            rebased = (f_sub["nav"] / f_sub["nav"].iloc[0]) * 100.0
            label = f"{row['reference_name']} ({row['category']}) [Score: {row['fund_score']}]"
            ax.plot(f_sub["date_dt"], rebased, label=label, color=colors[idx % len(colors)], linewidth=1.8)
            
    ax.set_title("3-Year Cumulative Growth Comparison: Top Funds vs. NIFTY 100 (Rebased to 100)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Observation Date", fontsize=11, labelpad=8)
    ax.set_ylabel("Portfolio Value (Base = 100)", fontsize=11, labelpad=8)
    ax.legend(loc="upper left", frameon=True, fontsize=9)
    ax.grid(True, linestyle=":", alpha=0.6)
    
    chart_path = os.path.join(OUTPUT_CHART_DIR, "benchmark_comparison.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300)
    plt.close()
    logger.info(f"Saved benchmark comparison chart to: {chart_path}")


def main():
    logger.info("=== Starting Performance Analytics Engine ===")
    compute_all_fund_metrics()
    logger.info("=== Performance Analytics Engine Completed Successfully ===")


if __name__ == "__main__":
    main()
