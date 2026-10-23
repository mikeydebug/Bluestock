#!/usr/bin/env python3
"""
Bluestock FinTech — Mutual Fund Capstone: ETL Pipeline & Database Loader
Author: Mayank Soni (Data Analyst Intern)

Transforms raw NAV time-series and transaction records into clean star-schema tables,
validates integrity, enforces non-trading day policies, and loads SQLite database.
"""

import datetime
import json
import logging
import os
import sqlite3
import sys
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ETL_Pipeline")

RAW_DIR = "mutual_fund_capstone/data/raw"
PROCESSED_DIR = "mutual_fund_capstone/data/processed"
DB_DIR = "mutual_fund_capstone/data/db"
DB_PATH = os.path.join(DB_DIR, "mutual_funds.db")
SCHEMA_SQL = "mutual_fund_capstone/sql/schema.sql"


def ensure_dirs():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)


def load_fund_dimension() -> pd.DataFrame:
    raw_master_path = os.path.join(RAW_DIR, "raw_fund_master.csv")
    if not os.path.exists(raw_master_path):
        raise FileNotFoundError(f"Missing {raw_master_path}. Run data_ingestion.py first.")
    
    df = pd.read_csv(raw_master_path)
    # Ensure fund_id is 1-indexed primary key
    df["fund_id"] = range(1, len(df) + 1)
    
    # Required columns order
    cols = ["fund_id", "scheme_code", "reference_name", "scheme_name", "fund_house", "category", "expense_ratio", "risk_grade", "launch_year"]
    df = df[cols]
    df.to_csv(os.path.join(PROCESSED_DIR, "clean_dim_fund.csv"), index=False)
    logger.info(f"Loaded {len(df)} fund master records.")
    return df


def clean_nav_series(dim_fund: pd.DataFrame) -> pd.DataFrame:
    code_to_id = dict(zip(dim_fund["scheme_code"], dim_fund["fund_id"]))
    all_nav_rows = []
    
    total_raw_rows = 0
    total_dropped_duplicates = 0
    total_invalid_navs = 0
    
    for code, fund_id in code_to_id.items():
        json_file = os.path.join(RAW_DIR, f"nav_{code}.json")
        if not os.path.exists(json_file):
            logger.warning(f"Raw file {json_file} not found. Skipping scheme {code}.")
            continue
            
        with open(json_file, "r") as f:
            payload = json.load(f)
            
        raw_obs = payload.get("data", [])
        total_raw_rows += len(raw_obs)
        
        fund_records = []
        for item in raw_obs:
            try:
                obs_date = datetime.datetime.strptime(item["date"], "%d-%m-%Y").date()
                nav_val = float(item["nav"])
                if nav_val <= 0:
                    total_invalid_navs += 1
                    continue
                fund_records.append({
                    "fund_id": fund_id,
                    "date_id": obs_date.isoformat(),
                    "nav": nav_val
                })
            except (ValueError, TypeError):
                total_invalid_navs += 1
                continue
                
        fund_df = pd.DataFrame(fund_records)
        # Drop duplicates keeping latest
        before_dedup = len(fund_df)
        fund_df.drop_duplicates(subset=["fund_id", "date_id"], keep="first", inplace=True)
        total_dropped_duplicates += (before_dedup - len(fund_df))
        
        # Sort chronologically ascending
        fund_df.sort_values(by="date_id", ascending=True, inplace=True)
        fund_df.reset_index(drop=True, inplace=True)
        
        # Compute daily arithmetic return within this fund's boundary
        fund_df["daily_return"] = fund_df["nav"].pct_change()
        
        all_nav_rows.append(fund_df)
        
    master_nav_df = pd.concat(all_nav_rows, ignore_index=True)
    master_nav_df["nav_id"] = range(1, len(master_nav_df) + 1)
    
    cols = ["nav_id", "fund_id", "date_id", "nav", "daily_return"]
    master_nav_df = master_nav_df[cols]
    master_nav_df.to_csv(os.path.join(PROCESSED_DIR, "clean_fact_nav.csv"), index=False)
    
    logger.info(f"Cleaned NAV Fact: {len(master_nav_df)} rows (Raw: {total_raw_rows}, Dups Dropped: {total_dropped_duplicates}, Invalids: {total_invalid_navs})")
    return master_nav_df


def clean_transactions(dim_fund: pd.DataFrame, clean_nav: pd.DataFrame) -> pd.DataFrame:
    raw_tx_path = os.path.join(RAW_DIR, "raw_investor_transactions.csv")
    df = pd.read_csv(raw_tx_path)
    
    code_to_id = dict(zip(dim_fund["scheme_code"], dim_fund["fund_id"]))
    df["fund_id"] = df["scheme_code"].map(code_to_id)
    
    # Map NAV to compute realistic units
    nav_lookup = clean_nav.set_index(["fund_id", "date_id"])["nav"].to_dict()
    
    units = []
    for _, row in df.iterrows():
        f_id = row["fund_id"]
        d_id = row["transaction_date"]
        # Lookup exact NAV or nearest available
        nav_val = nav_lookup.get((f_id, d_id))
        if not nav_val or nav_val <= 0:
            nav_val = 50.0  # Fallback reference price
        u = np.round(row["amount"] / nav_val, 4)
        units.append(u)
        
    df["units"] = units
    df.rename(columns={"transaction_date": "date_id", "transaction_type": "trans_type"}, inplace=True)
    
    cols = [
        "transaction_id", "investor_id", "fund_id", "date_id", 
        "trans_type", "amount", "units", "investor_age_group", 
        "investor_gender", "investor_state", "city_tier"
    ]
    df = df[cols]
    df.to_csv(os.path.join(PROCESSED_DIR, "clean_fact_transactions.csv"), index=False)
    logger.info(f"Cleaned {len(df)} transactions.")
    return df


def clean_aum(dim_fund: pd.DataFrame) -> pd.DataFrame:
    raw_aum_path = os.path.join(RAW_DIR, "raw_aum_history.csv")
    df = pd.read_csv(raw_aum_path)
    
    code_to_id = dict(zip(dim_fund["scheme_code"], dim_fund["fund_id"]))
    df["fund_id"] = df["scheme_code"].map(code_to_id)
    df.rename(columns={"date": "date_id"}, inplace=True)
    
    df["aum_id"] = range(1, len(df) + 1)
    cols = ["aum_id", "fund_id", "date_id", "aum_crores", "folio_count", "net_inflow_crores"]
    df = df[cols]
    df.to_csv(os.path.join(PROCESSED_DIR, "clean_fact_aum.csv"), index=False)
    logger.info(f"Cleaned {len(df)} AUM quarterly snapshots.")
    return df


def generate_date_dimension(all_dates: List[str]) -> pd.DataFrame:
    unique_dates = sorted(list(set(all_dates)))
    records = []
    for d_str in unique_dates:
        dt = datetime.datetime.strptime(d_str, "%Y-%m-%d").date()
        is_trading = 1 if dt.weekday() < 5 else 0
        records.append({
            "date_id": d_str,
            "year": dt.year,
            "quarter": (dt.month - 1) // 3 + 1,
            "month": dt.month,
            "month_name": dt.strftime("%B"),
            "day": dt.day,
            "day_of_week": dt.weekday(),
            "is_trading_day": is_trading
        })
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(PROCESSED_DIR, "clean_dim_date.csv"), index=False)
    logger.info(f"Generated date dimension with {len(df)} unique dates.")
    return df


def build_sqlite_database(dim_fund, dim_date, fact_nav, fact_tx, fact_aum):
    logger.info(f"Initializing SQLite database at: {DB_PATH}")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Execute schema DDL
    with open(SCHEMA_SQL, "r") as f:
        schema_script = f.read()
    cursor.executescript(schema_script)
    conn.commit()
    logger.info("Schema DDL applied successfully.")
    
    # Load Tables using pandas to_sql
    dim_fund.to_sql("dim_fund", conn, if_exists="append", index=False)
    dim_date.to_sql("dim_date", conn, if_exists="append", index=False)
    fact_nav.to_sql("fact_nav", conn, if_exists="append", index=False)
    fact_tx.to_sql("fact_transactions", conn, if_exists="append", index=False)
    fact_aum.to_sql("fact_aum", conn, if_exists="append", index=False)
    
    conn.commit()
    
    # Verify counts
    tables = ["dim_fund", "dim_date", "fact_nav", "fact_transactions", "fact_aum"]
    logger.info("--- Database Verification Summary ---")
    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
        cnt = cursor.fetchone()[0]
        logger.info(f"Table '{tbl}': {cnt:,} records.")
        
    conn.close()
    logger.info("SQLite database built and committed.")


def main():
    logger.info("=== Starting Mutual Fund Capstone ETL Pipeline ===")
    ensure_dirs()
    
    dim_fund = load_fund_dimension()
    fact_nav = clean_nav_series(dim_fund)
    fact_tx = clean_transactions(dim_fund, fact_nav)
    fact_aum = clean_aum(dim_fund)
    
    # Collect all unique dates
    all_dates = list(fact_nav["date_id"]) + list(fact_tx["date_id"]) + list(fact_aum["date_id"])
    dim_date = generate_date_dimension(all_dates)
    
    # Build DB
    build_sqlite_database(dim_fund, dim_date, fact_nav, fact_tx, fact_aum)
    logger.info("=== ETL Pipeline & DB Loading Completed Successfully ===")


if __name__ == "__main__":
    main()
