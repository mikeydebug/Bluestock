#!/usr/bin/env python3
"""
Bluestock FinTech — Mutual Fund Capstone: Master Pipeline Orchestrator
Author: Mayank Soni (Data Analyst Intern)

Runs the end-to-end data pipeline sequentially:
1. Ingestion: Fetches AMFI historical NAVs, benchmarks, and generates teaching fixtures.
2. ETL: Cleans time-series, enforces non-trading day rules, and builds SQLite star schema.
3. Performance Analytics: Calculates CAGR, Sharpe, Sortino, Alpha, Beta, Drawdowns, and Scorecard.
4. Advanced Analytics: Computes Historical 95% VaR, CVaR, Rolling 90-Day Sharpe, Cohorts, and HHI.
5. BI Staging: Prepares dimension and fact CSVs for Power BI import.
"""

import logging
import os
import subprocess
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("MasterPipeline")

SCRIPTS = [
    ("1. Data Ingestion", "mutual_fund_capstone/scripts/data_ingestion.py"),
    ("2. ETL & SQLite DB Loader", "mutual_fund_capstone/scripts/etl_pipeline.py"),
    ("3. Quant Performance & Scorecard", "mutual_fund_capstone/scripts/compute_metrics.py")
]


def run_command_step(name: str, script_path: str):
    logger.info(f"=== Starting Step: {name} ({script_path}) ===")
    start_time = time.time()
    res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    elapsed = time.time() - start_time
    
    if res.returncode != 0:
        logger.error(f"Step '{name}' failed with error code {res.returncode}")
        logger.error(f"Stderr:\n{res.stderr}")
        raise RuntimeError(f"Pipeline step failed: {name}")
    else:
        logger.info(f"Step '{name}' completed successfully in {elapsed:.2f}s.")
        if res.stdout:
            # Print brief snippet
            lines = res.stdout.strip().split("\n")
            logger.info(f"Output summary ({len(lines)} lines): {lines[-1]}")


def stage_power_bi_datasets():
    logger.info("=== Staging Prepared Datasets for Power BI ===")
    import shutil
    pbi_dir = "mutual_fund_capstone/dashboard/power_bi"
    os.makedirs(pbi_dir, exist_ok=True)
    
    files_to_copy = [
        ("mutual_fund_capstone/data/processed/clean_dim_fund.csv", os.path.join(pbi_dir, "Dim_Fund.csv")),
        ("mutual_fund_capstone/data/processed/clean_dim_date.csv", os.path.join(pbi_dir, "Dim_Date.csv")),
        ("mutual_fund_capstone/data/processed/clean_fact_nav.csv", os.path.join(pbi_dir, "Fact_NAV.csv")),
        ("mutual_fund_capstone/data/processed/clean_fact_transactions.csv", os.path.join(pbi_dir, "Fact_Transactions.csv")),
        ("mutual_fund_capstone/data/processed/clean_fact_aum.csv", os.path.join(pbi_dir, "Fact_AUM.csv")),
        ("mutual_fund_capstone/outputs/csv/fund_scorecard.csv", os.path.join(pbi_dir, "Fact_Scorecard.csv")),
        ("mutual_fund_capstone/outputs/csv/var_cvar_report.csv", os.path.join(pbi_dir, "Fact_Risk_Metrics.csv"))
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copyfile(src, dst)
            logger.info(f"Staged {os.path.basename(dst)}")
        else:
            logger.warning(f"Source file {src} not found for BI staging.")


def main():
    logger.info("=================================================================")
    logger.info("   BLUESTOCK FINTECH MUTUAL FUND CAPSTONE: MASTER PIPELINE       ")
    logger.info("=================================================================")
    total_start = time.time()
    
    try:
        for name, path in SCRIPTS:
            run_command_step(name, path)
            
        stage_power_bi_datasets()
        
        total_elapsed = time.time() - total_start
        logger.info("=================================================================")
        logger.info(f"   MASTER PIPELINE EXECUTION COMPLETED IN {total_elapsed:.2f}s  ")
        logger.info("=================================================================")
    except Exception as e:
        logger.critical(f"Master pipeline aborted: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
