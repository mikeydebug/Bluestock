#!/usr/bin/env python3
"""
Bluestock FinTech — Week 2 REST API Ingestion & Extraction Engine
Author: Mayank Soni (Data Analyst Intern)

Fetches financial market time-series from public REST endpoints, validates payload structure,
handles network timeouts and retries, parses JSON, and exports structured CSV data.
"""

import argparse
import datetime
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional

import pandas as pd
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("API_Extractor")

DEFAULT_SCHEME_CODE = 118632  # Nippon India Large Cap Fund Direct Growth
BASE_URL = "https://api.mfapi.in/mf/"
DEFAULT_OUTPUT_CSV = "week_02_fintech_fundamentals/api_extraction/extracted_fund_data.csv"


def fetch_api_payload(scheme_code: int, timeout: int = 15, max_retries: int = 3) -> Dict[str, Any]:
    """
    Fetches raw JSON payload from the AMFI API with resilient error and retry handling.
    """
    url = f"{BASE_URL}{scheme_code}"
    logger.info(f"Initiating HTTP GET request to: {url}")
    
    headers = {
        "User-Agent": "BluestockFinTech-Analytics/1.0 (Educational Academic Research)",
        "Accept": "application/json"
    }
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            logger.info(f"HTTP status code: {response.status_code} (Attempt {attempt}/{max_retries})")
            
            if response.status_code == 200:
                payload = response.json()
                return payload
            elif response.status_code == 404:
                logger.error(f"Scheme code {scheme_code} not found on server (HTTP 404).")
                raise ValueError(f"Invalid scheme code: {scheme_code}")
            elif response.status_code in [429, 500, 502, 503, 504]:
                logger.warning(f"Server busy or rate-limited ({response.status_code}). Backing off...")
                time.sleep(2 ** attempt)
            else:
                response.raise_for_status()
                
        except (requests.ConnectionError, requests.Timeout) as e:
            logger.warning(f"Network error on attempt {attempt}: {str(e)}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                logger.error("Maximum retries exhausted. Network request failed.")
                raise
                
    raise RuntimeError("Failed to retrieve data after multiple retry attempts.")


def validate_payload_schema(payload: Dict[str, Any]) -> bool:
    """
    Validates that the returned JSON payload adheres to expected API contract.
    """
    if not isinstance(payload, dict):
        logger.error("Payload is not a valid JSON dictionary.")
        return False
        
    meta = payload.get("meta")
    data = payload.get("data")
    
    if not isinstance(meta, dict) or not isinstance(data, list):
        logger.error("Missing or malformed 'meta' or 'data' elements in response.")
        return False
        
    required_meta_keys = ["fund_house", "scheme_code", "scheme_name", "scheme_category"]
    missing_meta = [k for k in required_meta_keys if k not in meta]
    if missing_meta:
        logger.error(f"Payload metadata missing expected keys: {missing_meta}")
        return False
        
    if len(data) == 0:
        logger.warning("Data series is empty (0 observations).")
        return False
        
    sample_obs = data[0]
    if "date" not in sample_obs or "nav" not in sample_obs:
        logger.error("Data records lack required 'date' or 'nav' fields.")
        return False
        
    logger.info(f"Schema validation PASSED. Total observations: {len(data)}")
    logger.info(f"Fund House: {meta.get('fund_house')} | Scheme: {meta.get('scheme_name')}")
    return True


def transform_and_export_csv(payload: Dict[str, Any], output_path: str, limit: Optional[int] = None) -> pd.DataFrame:
    """
    Transforms raw JSON observations into a cleaned, structured DataFrame and exports to CSV.
    """
    meta = payload["meta"]
    raw_data = payload["data"]
    
    if limit is not None and limit > 0:
        raw_data = raw_data[:limit]
        
    records = []
    for item in raw_data:
        try:
            # Parse DD-MM-YYYY to standard ISO YYYY-MM-DD
            obs_date = datetime.datetime.strptime(item["date"], "%d-%m-%Y").date()
            nav_val = float(item["nav"])
            if nav_val <= 0:
                continue
            records.append({
                "scheme_code": meta.get("scheme_code"),
                "scheme_name": meta.get("scheme_name"),
                "fund_house": meta.get("fund_house"),
                "category": meta.get("scheme_category"),
                "date": obs_date.isoformat(),
                "nav": nav_val
            })
        except (ValueError, TypeError) as parse_err:
            logger.warning(f"Skipping unparseable record {item}: {parse_err}")
            continue
            
    df = pd.DataFrame(records)
    # Sort chronologically ascending
    df.sort_values(by="date", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Compute daily percentage return
    df["daily_return"] = df["nav"].pct_change()
    
    # Create directory if missing
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Successfully saved {len(df)} validated observations to {output_path}")
    return df


def main():
    parser = argparse.ArgumentParser(description="Bluestock FinTech API Data Extractor")
    parser.add_argument("--scheme", type=int, default=DEFAULT_SCHEME_CODE, help="AMFI 6-digit scheme code")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_CSV, help="Target output CSV path")
    parser.add_argument("--limit", type=int, default=300, help="Limit number of recent observations")
    args = parser.parse_args()
    
    logger.info("=== Starting REST API Extraction Pipeline ===")
    try:
        payload = fetch_api_payload(scheme_code=args.scheme)
        if not validate_payload_schema(payload):
            logger.error("Validation failed. Aborting pipeline.")
            sys.exit(1)
            
        df = transform_and_export_csv(payload, args.output, limit=args.limit)
        print("\n--- First 5 Exported Observations ---")
        print(df.head().to_string())
        print("\n--- Summary Statistics ---")
        print(df[["nav", "daily_return"]].describe().to_string())
        logger.info("=== Extraction Pipeline Completed Successfully ===")
    except Exception as e:
        logger.error(f"Extraction pipeline crashed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
