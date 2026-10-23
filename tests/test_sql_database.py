"""
Bluestock FinTech — Test Suite: SQLite Star Schema & Analytical Queries
Author: Mayank Soni (Data Analyst Intern)

Tests database connection, table schemas, foreign key referential integrity,
index creation, and analytical query execution on mutual_funds.db.
"""

import os
import sqlite3
import pandas as pd
import pytest

DB_PATH = "mutual_fund_capstone/data/db/mutual_funds.db"


@pytest.fixture(scope="module")
def db_conn():
    """Provides a SQLite connection to the capstone database."""
    if not os.path.exists(DB_PATH):
        pytest.skip(f"Database file {DB_PATH} not found. Run run_pipeline.py first.")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    yield conn
    conn.close()


def test_required_tables_exist(db_conn):
    """Verify that all 6 star-schema production tables are present in sqlite_master."""
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    
    expected_tables = {
        "dim_fund",
        "dim_date",
        "fact_nav",
        "fact_transactions",
        "fact_aum",
        "fact_performance"
    }
    assert expected_tables.issubset(tables)


def test_table_row_counts(db_conn):
    """Verify that all tables are populated with expected minimum volume."""
    counts = {}
    for tbl in ["dim_fund", "dim_date", "fact_nav", "fact_transactions", "fact_aum", "fact_performance"]:
        cursor = db_conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
        counts[tbl] = cursor.fetchone()[0]
        
    assert counts["dim_fund"] == 6
    assert counts["dim_date"] >= 1000
    assert counts["fact_nav"] >= 20000
    assert counts["fact_transactions"] >= 5000
    assert counts["fact_aum"] >= 50
    assert counts["fact_performance"] == 6


def test_foreign_key_referential_integrity(db_conn):
    """Verify that child tables have zero orphaned fund_id references."""
    for child in ["fact_nav", "fact_transactions", "fact_aum", "fact_performance"]:
        query = f"""
            SELECT COUNT(*) 
            FROM {child} c
            LEFT JOIN dim_fund p ON c.fund_id = p.fund_id
            WHERE p.fund_id IS NULL;
        """
        cursor = db_conn.cursor()
        cursor.execute(query)
        orphans = cursor.fetchone()[0]
        assert orphans == 0, f"Found {orphans} orphaned records in {child}!"


def test_performance_indexes_exist(db_conn):
    """Verify that critical B-tree indexes exist for query optimization."""
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
    indexes = {row[0] for row in cursor.fetchall()}
    
    expected_indexes = {
        "idx_nav_fund_date",
        "idx_nav_date",
        "idx_trans_fund",
        "idx_trans_date",
        "idx_trans_investor",
        "idx_aum_fund",
        "idx_perf_fund"
    }
    assert expected_indexes.issubset(indexes)


def test_analytical_queries_execution(db_conn):
    """Execute core analytical queries and verify non-empty, valid return values."""
    # Query 1: Latest NAV per Fund
    q1 = """
        SELECT f.scheme_name, f.category, n.nav, n.date_id
        FROM fact_nav n
        JOIN dim_fund f ON n.fund_id = f.fund_id
        WHERE n.date_id = (SELECT MAX(date_id) FROM fact_nav WHERE fund_id = f.fund_id)
        ORDER BY f.fund_id;
    """
    df1 = pd.read_sql(q1, db_conn)
    assert len(df1) == 6
    assert (df1["nav"] > 0).all()
    
    # Query 2: Transaction Volume by Type
    q2 = """
        SELECT trans_type, COUNT(*) as count, SUM(amount) as total_vol
        FROM fact_transactions
        GROUP BY trans_type;
    """
    df2 = pd.read_sql(q2, db_conn)
    assert len(df2) >= 3  # SIP, Lumpsum, Redemption
    assert (df2["total_vol"] > 0).all()
    
    # Query 3: Multi-Factor Performance Ranking
    q3 = """
        SELECT f.reference_name, p.sharpe_ratio, p.cagr_3y, p.alpha, p.beta
        FROM fact_performance p
        JOIN dim_fund f ON p.fund_id = f.fund_id
        ORDER BY p.sharpe_ratio DESC;
    """
    df3 = pd.read_sql(q3, db_conn)
    assert len(df3) == 6
    assert df3.iloc[0]["sharpe_ratio"] >= df3.iloc[-1]["sharpe_ratio"]
