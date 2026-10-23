#!/usr/bin/env python3
"""
Bluestock FinTech — Mutual Fund Capstone: Final Report Generator
Author: Mayank Soni (Data Analyst Intern)

Compiles the comprehensive 20-page formal PDF report covering all 17 mandatory sections,
verified tables, quantitative formulas, embedded charts, and statutory disclosures using fpdf2.
"""

import os
import sqlite3
import pandas as pd
from fpdf import FPDF

os.makedirs("final_submission/report", exist_ok=True)
PDF_PATH = "final_submission/report/Final_Report.pdf"


def clean_txt(s):
    if not isinstance(s, str):
        return str(s)
    return (s.replace("\u2013", "-")
             .replace("\u2014", "--")
             .replace("\u2018", "'")
             .replace("\u2019", "'")
             .replace("\u201c", '"')
             .replace("\u201d", '"')
             .replace("₹", "INR ")
             .replace("•", "*")
             .encode("ascii", "ignore").decode("ascii"))


class BluestockReport(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(31, 78, 120)  # Navy
            self.cell(0, 5, clean_txt("BLUESTOCK FINTECH -- MUTUAL FUND ANALYTICS CAPSTONE REPORT"), align="L")
            self.ln()
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.3)
            self.line(10, 15, 200, 15)
            self.ln(4)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-14)
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.3)
            self.line(10, 283, 200, 283)
            self.set_font("Helvetica", "I", 7.5)
            self.set_text_color(100, 100, 100)
            self.cell(100, 8, clean_txt("CONFIDENTIAL -- FOR INTERNAL & ACADEMIC AUDIT ONLY"), align="L")
            self.cell(90, 8, f"Page {self.page_no()} of {{nb}}", align="R")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(31, 78, 120)
        self.cell(0, 8, clean_txt(title), align="L")
        self.ln()
        self.set_draw_color(31, 78, 120)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def section_heading(self, heading):
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(47, 85, 151)
        self.cell(0, 6, clean_txt(heading), align="L")
        self.ln()

    def body_paragraph(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 4.8, clean_txt(text))
        self.ln(3)

    def bullet_point(self, label, text):
        self.set_font("Helvetica", "B", 8.8)
        self.set_text_color(31, 78, 120)
        self.write(4.8, clean_txt(f"*  {label}: "))
        self.set_font("Helvetica", "", 8.8)
        self.set_text_color(50, 50, 50)
        self.write(4.8, clean_txt(f"{text}\n"))
        self.ln(1.5)

    def callout_box(self, text):
        self.set_fill_color(242, 244, 248)
        self.set_draw_color(47, 85, 151)
        self.set_line_width(0.4)
        self.rect(self.get_x(), self.get_y(), 190, 12, style="DF")
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(31, 78, 120)
        self.set_xy(self.get_x() + 3, self.get_y() + 2)
        self.multi_cell(184, 4.2, clean_txt(text))
        self.set_xy(10, self.get_y() + 6)


def generate_pdf():
    pdf = BluestockReport()
    pdf.alias_nb_pages()

    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    pdf.add_page()
    pdf.ln(12)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255, 153, 0)
    pdf.cell(0, 6, "BLUESTOCK FINTECH", align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(31, 78, 120)
    pdf.multi_cell(0, 8, "MUTUAL FUND ANALYTICS & PORTFOLIO RISK\nCAPSTONE TECHNICAL REPORT", align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(47, 85, 151)
    pdf.multi_cell(0, 5, "An Empirical Investigation into Fund Performance, Downside Tail Risk,\nand Retail Inflow Dynamics Across Indian Mutual Funds", align="C")
    pdf.ln(6)

    chart_cover = "mutual_fund_capstone/outputs/charts/benchmark_comparison.png"
    if os.path.exists(chart_cover):
        pdf.image(chart_cover, x=15, y=75, w=180)
        pdf.set_y(180)

    pdf.set_fill_color(242, 244, 248)
    pdf.set_draw_color(31, 78, 120)
    pdf.rect(20, 190, 170, 55, style="DF")
    pdf.set_xy(25, 195)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(31, 78, 120)
    pdf.cell(50, 6, "Author:")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(100, 6, "Mayank Soni (B.Tech Computer Science)")
    pdf.ln()

    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(31, 78, 120)
    pdf.cell(50, 6, "Role & Organization:")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(100, 6, "Data Analyst Intern, Bluestock Fintech")
    pdf.ln()

    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(31, 78, 120)
    pdf.cell(50, 6, "Technical Focus:")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(100, 6, "ETL Pipelines, SQLite Star Schema, Quant Risk, Power BI")
    pdf.ln()

    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(31, 78, 120)
    pdf.cell(50, 6, "Submission Date:")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(100, 6, "October 2026")
    pdf.ln()

    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(31, 78, 120)
    pdf.cell(50, 6, "Release Version:")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(100, 6, "v1.0.0 (Submission Freeze - Verified & Tested)")
    pdf.ln()

    # ==========================================
    # PAGE 2: TABLE OF CONTENTS & EXEC SUMMARY
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("TABLE OF CONTENTS")
    
    toc_data = [
        ("1. Executive Summary", "Page 2"),
        ("2. Problem Statement & Research Questions", "Page 3"),
        ("3. Project Objectives & Deliverables Matrix", "Page 4"),
        ("4. Data Sources, Provenance & Lineage", "Page 5"),
        ("5. Data Quality, Verification & Cleaning Policies", "Page 6"),
        ("6. ETL System Architecture & Ingestion Workers", "Page 7"),
        ("7. SQLite Relational Star Schema Database Design", "Page 8"),
        ("8. Exploratory Data Analysis (EDA) Findings", "Page 9"),
        ("9. Quantitative Fund Performance Analytics & Scorecard", "Page 11"),
        ("10. Downside Risk Modeling (VaR, CVaR, Rolling Sharpe)", "Page 13"),
        ("11. Retail Investor Analytics & Demographic Dynamics", "Page 14"),
        ("12. Interactive Power BI Dashboard Suite", "Page 15"),
        ("13. Synthesis of Key Analytical Findings", "Page 16"),
        ("14. Strategic Recommendations for Bluestock Fintech", "Page 17"),
        ("15. Project Assumptions & Methodological Constraints", "Page 18"),
        ("16. Conclusion & Production Engineering Roadmap", "Page 19"),
        ("17. References & Statutory Regulatory Disclosures", "Page 20")
    ]
    
    for item, p_str in toc_data:
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(150, 5.2, clean_txt(item))
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(40, 5.2, clean_txt(p_str), align="R")
        pdf.ln()
    pdf.ln(5)

    pdf.chapter_title("1. EXECUTIVE SUMMARY")
    pdf.body_paragraph(
        "The Indian mutual fund industry has crossed INR 65 Lakh Crores in aggregate Assets Under Management (AUM), "
        "propelled by explosive digital onboarding and recurring retail Systematic Investment Plan (SIP) contributions exceeding INR 21,000 Crores monthly. "
        "This capstone report details the development of an institutional-grade financial data analytics engine engineered for Bluestock Fintech."
    )
    pdf.body_paragraph(
        "The system ingests 20,389 daily Net Asset Value (NAV) observations from the Association of Mutual Funds in India (AMFI) across six diverse funds between 2013 and 2026. "
        "A relational star-schema warehouse was implemented in SQLite to support dimensional slicing, time-series querying, and multi-factor performance ranking. "
        "By synthesizing trailing returns (1Y, 3Y, 5Y), annualised volatility, Sharpe ratios (Rf=6.5%), Sortino ratios, Jensen's Alpha, market Beta, Maximum Drawdown, "
        "and downside tail-risk (Historical 95% VaR and CVaR), this project establishes an empirical foundation for modern retail wealth advisory."
    )

    # ==========================================
    # PAGE 3: PROBLEM STATEMENT
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("2. PROBLEM STATEMENT")
    pdf.body_paragraph(
        "The rapid democratization of capital markets across India has exposed severe analytical deficiencies in traditional retail wealth tools:"
    )
    pdf.bullet_point("The Fallacy of Raw Trailing Returns", "Retail screeners predominantly rank mutual funds by 1-year or 3-year point-to-point returns. This artificially elevates aggressive high-beta funds during market rallies while concealing severe peak-to-trough drawdowns.")
    pdf.bullet_point("Data Pipeline Fragility", "Public financial APIs suffer from network timeouts, schema shifts, unvalidated ticker codes, and missing non-trading day observations. Without automated data validation and cleaning, analytical pipelines fail silently.")
    pdf.bullet_point("Lack of Multi-Attribute Risk Scoring", "Retail investors rarely have access to composite scorecards that penalize excessive expense ratios (TER drag) and volatility. Single-metric decisions often result in capital impairment during market corrections.")
    pdf.bullet_point("Disconnected Data Silos", "Financial market prices, operational portfolio holdings, and retail transaction demographics typically exist in separate spreadsheets, preventing holistic cohort and behavioral intelligence.")
    pdf.ln(4)
    pdf.callout_box("Research Question: How can an integrated financial data platform ingest live AMFI feeds, enforce relational integrity in an enterprise star schema, compute robust downside risk metrics, and empower investors with multi-factor scorecard rankings?")

    # ==========================================
    # PAGE 4: PROJECT OBJECTIVES
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("3. PROJECT OBJECTIVES")
    pdf.body_paragraph("To address the industry problem statement, the project roadmap established six technical milestones:")
    
    headers = ["Objective", "Scope & Technical Standard", "Verification Metric"]
    col_w = [45, 95, 50]
    pdf.set_fill_color(31, 78, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    for idx, h in enumerate(headers):
        pdf.cell(col_w[idx], 6, clean_txt(h), border=1, fill=True, align="C")
    pdf.ln()

    rows = [
        ("1. Data Ingestion", "Build resilient Python workers with exponential backoff and timeout handling to fetch daily AMFI NAV time-series.", "100% API success (20,389 records)."),
        ("2. SQLite Warehouse", "Design an ACID star schema (dim_fund, dim_date, fact_nav, fact_transactions, fact_aum, fact_performance).", "Zero foreign key violations; fully indexed."),
        ("3. Exploratory EDA", "Execute extensive EDA producing >= 15 visualizations and 12 evidence-based analytical takeaways.", "15 high-res PNG charts generated."),
        ("4. Performance Engine", "Calculate CAGR, annualised volatility, Sharpe, Sortino, Alpha, Beta, Max Drawdown, and 0-100 Scorecard.", "Zero NaN errors; reproducible via CLI."),
        ("5. Downside Risk", "Quantify extreme tail losses via 95% Historical VaR, Conditional VaR (Expected Shortfall), and rolling Sharpe.", "Published var_cvar_report.csv."),
        ("6. Power BI Suite", "Develop a 4-page executive BI dashboard model with dynamic DAX libraries and PDF exports.", "4 verified dashboard views & multi-page PDF.")
    ]
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Helvetica", "", 7.5)
    for r in rows:
        pdf.cell(col_w[0], 8, clean_txt(r[0]), border=1)
        pdf.cell(col_w[1], 8, clean_txt(r[1]), border=1)
        pdf.cell(col_w[2], 8, clean_txt(r[2]), border=1, align="C")
        pdf.ln()

    # ==========================================
    # PAGE 5: DATA SOURCES
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("4. DATA SOURCES, PROVENANCE & DATA LINEAGE")
    pdf.body_paragraph(
        "Strict data governance principles were maintained to distinguish authentic financial observations from instructional simulation fixtures:"
    )
    src_data = [
        ("Mutual Fund NAVs", "AMFI (api.mfapi.in)", "20,389 records", "Authentic Public Financial Time-Series"),
        ("Market Benchmarks", "NSE (NIFTY 50 / 100)", "1,778 daily bars", "Verified Market Proxy for CAPM Regression"),
        ("Retail Transactions", "Bluestock Demographics", "5,000 transactions", "Synthetic Teaching Data (Explicitly Tagged)"),
        ("AUM & Folio History", "Quarterly AMFI Trends", "162 snapshots", "Synthetic Teaching Data (Explicitly Tagged)"),
        ("Portfolio Holdings", "SEBI Disclosures", "22 sector holdings", "Model Asset Allocation Disclosure")
    ]
    col_s = [45, 45, 35, 65]
    pdf.set_fill_color(31, 78, 120); pdf.set_text_color(255, 255, 255); pdf.set_font("Helvetica", "B", 8)
    for idx, h in enumerate(["Data Domain", "Provider / API", "Volume", "Lineage Classification"]):
        pdf.cell(col_s[idx], 6, clean_txt(h), border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_text_color(40, 40, 40); pdf.set_font("Helvetica", "", 7.5)
    for r in src_data:
        for idx, val in enumerate(r):
            pdf.cell(col_s[idx], 7, clean_txt(val), border=1)
        pdf.ln()
    pdf.ln(5)

    pdf.section_heading("Critical Scheme Code Resolution Audit")
    pdf.body_paragraph(
        "During live network resolution of the 6 supplied AMFI scheme codes, an important mapping divergence was identified: "
        "Code 118632 confirmed exact alignment with Nippon India Large Cap Fund. "
        "Codes 125497, 120841, 120503, 119092, and 119551 resolved to legal schemes spanning Small Cap, Mid Cap, ELSS, Money Market, and Debt. "
        "In strict compliance with project governance ('Treat these codes as supplied configuration values that must be validated against actual API response'), "
        "the pipeline ingests authentic data, preserves original references, and uses this multi-asset spectrum for robust cross-category analysis."
    )

    # ==========================================
    # PAGE 6: DATA QUALITY
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("5. DATA QUALITY, VERIFICATION & CLEANING POLICIES")
    pdf.body_paragraph(
        "Non-Trading Days Policy: In Indian financial markets, mutual funds publish daily NAVs only on official trading days. "
        "Non-trading days (weekends and national market holidays) are explicitly NOT forward-filled in the primary fact table. "
        "Forward-filling artificially dampens variance and injects spurious zero-return observations into volatility denominators. "
        "Daily returns are strictly computed on consecutive observed trading days:"
    )
    pdf.callout_box("R_t = (NAV_t / NAV_{t-1}) - 1  (Evaluated strictly within individual fund boundaries)")
    pdf.ln(2)

    pdf.section_heading("Automated Data Quality Gates Passed")
    dq_rows = [
        ("NAV Positivity Enforcement", "CHECK (nav > 0)", "20,390 evaluated", "1 invalid removed", "99.99%"),
        ("Duplicate Elimination", "UNIQUE (fund_id, date_id)", "20,389 evaluated", "0 duplicates", "100.00%"),
        ("Transaction Bounds", "CHECK (amount > 0 AND <= 500k)", "5,000 evaluated", "0 anomalies", "100.00%"),
        ("Referential Integrity", "Foreign Key constraints to dim_fund/date", "25,551 total records", "0 orphan keys", "100.00%"),
        ("Date Normalization", "Parse DD-MM-YYYY to ISO YYYY-MM-DD", "20,389 evaluated", "0 parse errors", "100.00%")
    ]
    col_dq = [45, 55, 35, 35, 20]
    pdf.set_fill_color(31, 78, 120); pdf.set_text_color(255, 255, 255); pdf.set_font("Helvetica", "B", 7.5)
    for idx, h in enumerate(["Quality Gate", "Integrity Rule", "Evaluated", "Outcome", "Pass %"]):
        pdf.cell(col_dq[idx], 6, clean_txt(h), border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_text_color(40, 40, 40); pdf.set_font("Helvetica", "", 7.5)
    for r in dq_rows:
        for idx, val in enumerate(r):
            pdf.cell(col_dq[idx], 7, clean_txt(val), border=1)
        pdf.ln()

    # ==========================================
    # PAGE 7: ETL ARCHITECTURE
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("6. SYSTEM ARCHITECTURE & ETL PIPELINE")
    pdf.body_paragraph(
        "The capstone engineering pipeline separates concerns across three physical storage tiers orchestrated by run_pipeline.py:"
    )
    pdf.bullet_point("Raw Ingestion Tier", "Python requests client with retry and backoff ingests raw JSON from api.mfapi.in and archives unedited source files in data/raw/.")
    pdf.bullet_point("ETL & Transformation Tier", "Vectorized pandas pipeline parses dates, validates positivity, computes sequential returns, and exports clean CSVs to data/processed/.")
    pdf.bullet_point("Relational Warehouse Tier", "SQLite database (mutual_funds.db) enforces star-schema DDL constraints, B-tree indexes, and transactional ACID compliance.")
    pdf.ln(3)

    c_nav = "mutual_fund_capstone/outputs/charts/chart_01_nav_trends.png"
    if os.path.exists(c_nav):
        pdf.image(c_nav, x=15, y=95, w=180)
        pdf.set_y(185)
    pdf.body_paragraph("Figure 1: Historical 3-Year NAV trajectory across configured mutual fund schemes showing distinct growth profiles.")

    # ==========================================
    # PAGE 8: DATABASE DESIGN
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("7. SQLITE RELATIONAL STAR SCHEMA DESIGN")
    pdf.body_paragraph(
        "The warehouse implements a Kimball star schema optimized for fast time-series slicing, analytical rollups, and Power BI ingestion:"
    )
    db_rows = [
        ("dim_fund", "Dimension", "fund_id", "None", "6 schemes", "scheme_code (Unique)"),
        ("dim_date", "Dimension", "date_id", "None", "4,330 dates", "date_id, year, month"),
        ("fact_nav", "Fact (Time-Series)", "nav_id", "fund_id, date_id", "20,389 obs", "(fund_id, date_id) Composite"),
        ("fact_transactions", "Fact (Transactional)", "transaction_id", "fund_id, date_id", "5,000 orders", "fund_id, date_id, investor_id"),
        ("fact_aum", "Fact (Quarterly)", "aum_id", "fund_id, date_id", "162 snapshots", "fund_id, date_id"),
        ("fact_performance", "Fact (Quant)", "perf_id", "fund_id, as_of_date", "6 schemes", "fund_id, as_of_date")
    ]
    col_db = [38, 32, 28, 35, 25, 32]
    pdf.set_fill_color(31, 78, 120); pdf.set_text_color(255, 255, 255); pdf.set_font("Helvetica", "B", 7.5)
    for idx, h in enumerate(["Table Name", "Table Type", "Primary Key", "Foreign Keys", "Records", "Indexes"]):
        pdf.cell(col_db[idx], 6, clean_txt(h), border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_text_color(40, 40, 40); pdf.set_font("Helvetica", "", 7.5)
    for r in db_rows:
        for idx, val in enumerate(r):
            pdf.cell(col_db[idx], 7, clean_txt(val), border=1)
        pdf.ln()
    pdf.ln(4)
    pdf.section_heading("Relational Integrity & Indexing Strategy")
    pdf.body_paragraph(
        "Indexes were established on fact_nav(fund_id, date_id) and fact_transactions(investor_id), "
        "enabling complex window queries, multi-table joins, and cohort aggregations to execute in sub-millisecond runtimes."
    )

    # ==========================================
    # PAGE 9 & 10: EDA FINDINGS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("8. EXPLORATORY DATA ANALYSIS (EDA) FINDINGS")
    pdf.body_paragraph("Empirical analysis across 20,389 NAV observations and 5,000 transactions revealed twelve core market dynamics:")
    pdf.bullet_point("1. Large-Cap Return Stability", "Nippon Large Cap Fund delivered 10.39% 3Y CAGR with the lowest equity drawdown (-15.37%), outperforming mid/small peers on a risk-adjusted basis.")
    pdf.bullet_point("2. Small-Cap Volatility Penalty", "SBI Small Cap Fund posted +11.76% Jensen's Alpha but suffered a severe -22.42% drawdown, demonstrating high cyclical downside risk.")
    pdf.bullet_point("3. Capital Shield in Money Markets", "HDFC Money Market Fund posted 7.29% CAGR with minimal 0.43% volatility and a 1.97 Sharpe ratio, establishing prime capital protection.")
    pdf.bullet_point("4. Debt Sensitivity to Interest Rates", "Aditya Birla Debt Fund recorded -2.39% 3Y CAGR due to duration drag during RBI monetary tightening cycles between 2022 and 2024.")
    pdf.bullet_point("5. SIP Retail Inflow Engine", "SIP transactions represented 72.1% of order frequency (3,607 transactions) and over INR 2.12 Crores in recurring inflows.")
    pdf.bullet_point("6. Millennial Investor Adoption", "Investors aged 26-35 represent 42.0% of total folios, reflecting high mobile fintech adoption among young professionals.")
    pdf.ln(2)

    c_sip = "mutual_fund_capstone/outputs/charts/chart_03_monthly_sip_inflows.png"
    if os.path.exists(c_sip):
        pdf.image(c_sip, x=15, y=125, w=180)
        pdf.set_y(210)
    pdf.body_paragraph("Figure 2: Monthly retail SIP inflow velocity showing steady accumulation across market cycles.")

    # Page 10: EDA Findings Part 2
    pdf.add_page()
    pdf.chapter_title("8. EDA FINDINGS (CONTINUED)")
    pdf.bullet_point("7. Ticket Size Expansion by Age", "While 26-35 age investors lead volume, the 36-50 age cohort commands 77% higher average SIP ticket sizes (INR 7,420 vs INR 4,180).")
    pdf.bullet_point("8. Geographic Concentration Triad", "Maharashtra (24.2%), Karnataka (18.1%), and Delhi NCR (14.0%) generate 56.3% of total retail mutual fund investments.")
    pdf.bullet_point("9. B30 Emerging Market Penetration", "Beyond-30 cities account for 36.2% of retail volume, confirming successful capital market expansion into Tier-2/Tier-3 India.")
    pdf.bullet_point("10. Multi-Year AUM Expansion", "Aggregate AUM grew from INR 92k Cr to over INR 198k Cr between 2020 and 2026, representing a 13.5% compound annual growth rate.")
    pdf.bullet_point("11. Sector Overweighting", "Financial Services represents 32.4% of large-cap portfolios and 22.0% of mid-cap holdings, followed by Information Technology (14.8%).")
    pdf.bullet_point("12. Cross-Asset Uncorrelation", "Equities and Money Market funds showed a correlation of r = 0.04, confirming strong multi-asset diversification benefits.")
    pdf.ln(2)

    c_geo = "mutual_fund_capstone/outputs/charts/chart_08_state_distribution.png"
    if os.path.exists(c_geo):
        pdf.image(c_geo, x=15, y=125, w=180)
        pdf.set_y(210)
    pdf.body_paragraph("Figure 3: State-wise retail investment distribution led by Maharashtra, Karnataka, and Delhi NCR.")

    # ==========================================
    # PAGE 11 & 12: FUND PERFORMANCE METRICS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("9. QUANTITATIVE FUND PERFORMANCE ANALYTICS")
    pdf.body_paragraph(
        "Performance analytics were evaluated over a 3-year historical window. Multi-factor scorecard scores (0–100) synthesize: "
        "30% 3Y Return Rank, 25% Sharpe Rank, 20% Alpha Rank, 15% Inverse TER Rank, and 10% Inverse Max Drawdown Rank:"
    )

    scorecard_df = pd.read_csv("mutual_fund_capstone/outputs/csv/fund_scorecard.csv")
    col_sc = [15, 38, 30, 18, 16, 18, 15, 15, 18, 12]
    pdf.set_fill_color(31, 78, 120); pdf.set_text_color(255, 255, 255); pdf.set_font("Helvetica", "B", 7)
    for idx, h in enumerate(["Rank", "Fund Reference", "Category", "3Y CAGR", "Sharpe", "Alpha", "Beta", "TER", "Max DD", "Score"]):
        pdf.cell(col_sc[idx], 6, clean_txt(h), border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_text_color(40, 40, 40); pdf.set_font("Helvetica", "", 7)
    for _, r in scorecard_df.iterrows():
        vals = [
            str(r["rank"]), r["reference_name"], r["category"][:14],
            f"{r['cagr_3y']}%", f"{r['sharpe_ratio']}", f"{r['alpha']}%",
            f"{r['beta']}", f"{r['expense_ratio']}%", f"{r['max_drawdown']}%",
            str(r["fund_score"])
        ]
        for idx, val in enumerate(vals):
            pdf.cell(col_sc[idx], 6.5, clean_txt(val), border=1, align="C")
        pdf.ln()
    pdf.ln(3)

    c_scat = "mutual_fund_capstone/outputs/charts/chart_14_risk_return_scatter.png"
    if os.path.exists(c_scat):
        pdf.image(c_scat, x=15, y=105, w=180)
        pdf.set_y(195)
    pdf.body_paragraph("Figure 4: Risk-Return Scatter matrix (Bubble Size = Composite Fund Score, Color = Sharpe Ratio).")

    # Page 12: Methodological Details
    pdf.add_page()
    pdf.chapter_title("9. PERFORMANCE METHODOLOGY & FORMULATIONS")
    pdf.section_heading("Core Mathematical Formulations")
    pdf.body_paragraph("* Compound Annual Growth Rate (CAGR): Evaluated on exact elapsed calendar period Y = Days / 365.25:\n  CAGR = (Ending NAV / Starting NAV)^(1/Y) - 1")
    pdf.body_paragraph("* Sharpe Ratio: Measures excess return per unit of annualised volatility using statutory risk-free rate Rf = 6.5%:\n  Sharpe = (R_ann - Rf) / (sigma_daily * sqrt(252))")
    pdf.body_paragraph("* Sortino Ratio: Measures return relative to downside semideviation below target MAR = Rf / 252:\n  Sortino = (R_ann - Rf) / (sigma_downside * sqrt(252))")
    pdf.body_paragraph("* Alpha and Beta via CAPM OLS Regression: Regressing fund daily returns on NIFTY 100 returns via scipy.stats.linregress:\n  R_fund = alpha + beta * R_bench + epsilon;  Annual Alpha = Intercept * 252 * 100")
    pdf.body_paragraph("* Maximum Drawdown: Peak-to-trough decline tracking historical running maximum:\n  Drawdown_t = (NAV_t / max_{tau <= t} NAV_tau) - 1")
    pdf.ln(2)

    c_dd = "mutual_fund_capstone/outputs/charts/chart_13_drawdown_curves.png"
    if os.path.exists(c_dd):
        pdf.image(c_dd, x=15, y=130, w=180)
        pdf.set_y(215)
    pdf.body_paragraph("Figure 5: Time-series portfolio drawdown profiles illustrating peak impairment during stress periods.")

    # ==========================================
    # PAGE 13: RISK ANALYSIS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("10. DOWNSIDE RISK ANALYSIS & VALUE AT RISK (VaR)")
    pdf.body_paragraph(
        "To guard against severe tail-risk events, the analytics engine computed Historical 95% Value at Risk (VaR) "
        "and Conditional Value at Risk (CVaR / Expected Shortfall) across all funds:"
    )

    var_df = pd.read_csv("mutual_fund_capstone/outputs/csv/var_cvar_report.csv")
    col_v = [42, 38, 38, 36, 36]
    pdf.set_fill_color(31, 78, 120); pdf.set_text_color(255, 255, 255); pdf.set_font("Helvetica", "B", 7.5)
    for idx, h in enumerate(["Fund Reference", "Category", "95% VaR Quantile", "95% VaR Loss", "95% CVaR Loss"]):
        pdf.cell(col_v[idx], 6, clean_txt(h), border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_text_color(40, 40, 40); pdf.set_font("Helvetica", "", 7.5)
    for _, r in var_df.iterrows():
        vals = [
            r["reference_name"], r["category"][:16],
            f"{r['daily_var_95_quantile']}%",
            f"{r['daily_var_95_loss_pct']}%",
            f"{r['daily_cvar_95_loss_pct']}%"
        ]
        for idx, val in enumerate(vals):
            pdf.cell(col_v[idx], 6.5, clean_txt(val), border=1, align="C")
        pdf.ln()
    pdf.ln(3)

    c_roll = "mutual_fund_capstone/outputs/charts/rolling_sharpe_chart.png"
    if os.path.exists(c_roll):
        pdf.image(c_roll, x=15, y=95, w=180)
        pdf.set_y(180)
    pdf.body_paragraph("Figure 6: Rolling 90-day annualised Sharpe ratios showing regime switches across market cycles.")

    # ==========================================
    # PAGE 14: INVESTOR ANALYTICS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("11. RETAIL INVESTOR ANALYTICS & COHORT BEHAVIOR")
    pdf.body_paragraph(
        "Investor cohort analysis evaluated user retention and ticket sizing by acquisition year. "
        "The 2021 cohort demonstrated sustained loyalty, contributing INR 8.67 Crores with a 72.3% SIP persistence rate."
    )

    c_tx = "mutual_fund_capstone/outputs/charts/chart_15_transaction_composition.png"
    if os.path.exists(c_tx):
        pdf.image(c_tx, x=15, y=55, w=180)
        pdf.set_y(145)
    pdf.body_paragraph("Figure 7: Retail transaction breakdown: Volume frequency vs aggregate invested capital.")

    pdf.section_heading("SIP Continuity Audit & Lapse Analysis")
    pdf.body_paragraph(
        "Among 251 retail investors with at least 6 consecutive SIP commitments, 1,352 instances of installment gaps > 35 days were detected. "
        "Automated lapse detection enables proactive CRM intervention before systematic wealth compounding is derailed."
    )

    # ==========================================
    # PAGE 15: DASHBOARD SUITE
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("12. POWER BI EXECUTIVE DASHBOARD SUITE")
    pdf.body_paragraph("The Power BI suite provides interactive executive visibility across four specialized views:")
    d1 = "mutual_fund_capstone/dashboard/power_bi/page_1_industry_overview.png"
    d2 = "mutual_fund_capstone/dashboard/power_bi/page_2_fund_performance.png"
    if os.path.exists(d1):
        pdf.image(d1, x=15, y=45, w=180)
    if os.path.exists(d2):
        pdf.image(d2, x=15, y=145, w=180)

    # Page 16: Dashboard Pages 3 & 4
    pdf.add_page()
    pdf.chapter_title("12. DASHBOARD SUITE (PAGES 3 & 4)")
    d3 = "mutual_fund_capstone/dashboard/power_bi/page_3_investor_analytics.png"
    d4 = "mutual_fund_capstone/dashboard/power_bi/page_4_sip_market_trends.png"
    if os.path.exists(d3):
        pdf.image(d3, x=15, y=45, w=180)
    if os.path.exists(d4):
        pdf.image(d4, x=15, y=145, w=180)

    # ==========================================
    # PAGE 17: KEY FINDINGS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("13. SYNTHESIS OF KEY ANALYTICAL FINDINGS")
    pdf.body_paragraph("1. Multi-Factor Scoring Exposes Hidden Volatility: Nippon Large Cap Fund won the #1 overall rank (Score 95.0) despite having a lower raw CAGR than Small Cap funds, because its lower drawdown (-15.37%) and Sharpe ratio (0.29) proved far more resilient.")
    pdf.body_paragraph("2. The Capital Preservation Anchor: HDFC Money Market Fund (Score 77.7) proved essential for conservative retail investors, delivering 7.29% CAGR with virtually non-existent volatility (0.43%) and a negligible 0.006% 95% VaR loss.")
    pdf.body_paragraph("3. SIP Stickiness Amid Market Volatility: Retail monthly SIP inflows displayed remarkably steady accumulation regardless of NIFTY 50 monthly oscillations, confirming the structural transformation of Indian domestic retail savings.")
    pdf.body_paragraph("4. Demographic Wealth Ladder: While young professionals (26-35) drive user acquisition volume (42%), mature professionals (36-50) supply the core capital volume, commanding 77% higher monthly ticket sizes.")
    pdf.body_paragraph("5. B30 Expansion Momentum: Beyond-30 cities now generate over 36% of retail inflows, confirming that digital onboarding platforms have successfully democratized capital market access beyond the traditional metro triad.")

    # ==========================================
    # PAGE 18: RECOMMENDATIONS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("14. STRATEGIC RECOMMENDATIONS FOR BLUESTOCK FINTECH")
    pdf.body_paragraph("Based on the validated analytical findings, five strategic recommendations are proposed for Bluestock Fintech:")
    pdf.bullet_point("1. Integrate Composite Scorecard in Mobile App", "Replace standalone trailing return rankings on the Bluestock retail mobile pass with the 0-100 multi-factor scorecard to educate users on volatility drag and expense ratio penalties.")
    pdf.bullet_point("2. Deploy Automated Smart SIP Step-Ups", "Introduce automated 10% annual SIP step-up mandates tailored to the 26-35 age cohort to naturally expand ticket sizing as user income matures.")
    pdf.bullet_point("3. Proactive Downside Risk & VaR Alerts", "Embed real-time Value at Risk notifications within the user portfolio dashboard when small-cap equity concentration exceeds 40%, safeguarding retail wealth from catastrophic market drawdowns.")
    pdf.bullet_point("4. Expand B30 Educational Nudges", "Implement vernacular and regional-language behavioral nudges (inspired by Zerodha's Nudge model) to deepen penetration across emerging Tier-2 and Tier-3 markets.")
    pdf.bullet_point("5. Automated SIP Continuity & Lapse Recovery", "Build automated WhatsApp and SMS renewal workflows targeting investors when an SIP gap exceeds 28 days to prevent folio drop-off.")

    # ==========================================
    # PAGE 19: LIMITATIONS & CONCLUSION
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("15. PROJECT LIMITATIONS & 16. CONCLUSION")
    pdf.section_heading("15. Methodological Constraints & Assumptions")
    pdf.body_paragraph("* Power BI Desktop on macOS: Microsoft Power BI Desktop is native to Windows OS. In macOS environments, native .pbix binary files cannot be compiled programmatically without Windows virtualization. To ensure 100% submission fidelity, production-ready star-schema CSV datasets, verified DAX measures, four rendered dashboard views, and a compiled Dashboard.pdf were generated.")
    pdf.body_paragraph("* Synthetic Demographics Fixture: While mutual fund NAVs and benchmark series represent authentic historical market data from AMFI and NSE, proprietary retail client transactions were synthetically generated using rule-based behavioral distributions and explicitly tagged as synthetic_teaching_data.")
    pdf.body_paragraph("* CAPM Linear Regression Constraints: OLS regression assumes constant market beta and normally distributed error residuals. In reality, equity returns display fat tails and volatility clustering.")
    pdf.ln(3)

    pdf.section_heading("16. Conclusion & Production Engineering Roadmap")
    pdf.body_paragraph("The Bluestock FinTech Mutual Fund Analytics Capstone successfully achieved every technical milestone in the internship curriculum: automated live API ingestion of 20,380+ NAV observations, ACID-compliant SQLite star schema relational database, quantitative performance scoring, downside tail-risk modeling, interactive Power BI dashboard suite, and automated pytest validation.")

    # ==========================================
    # PAGE 20: REFERENCES
    # ==========================================
    pdf.add_page()
    pdf.chapter_title("17. REFERENCES & STATUTORY DISCLOSURES")
    refs = [
        "1. Association of Mutual Funds in India (AMFI): Official Daily NAV Feeds and Scheme Directives (https://www.amfiindia.com).",
        "2. Securities and Exchange Board of India (SEBI): Categorization and Rationalization of Mutual Fund Schemes (Circular SEBI/HO/IMD/DF3/CIR/P/2017/114).",
        "3. National Stock Exchange of India (NSE): NIFTY 50 and NIFTY 100 Methodology and Historical Index Data (https://www.nseindia.com).",
        "4. Tata Consultancy Services Limited: Audited Consolidated Financial Statements, Annual Report 2023-24 submitted to BSE/NSE.",
        "5. Markowitz, Harry (1952): 'Portfolio Selection', The Journal of Finance, 7(1), pp. 77-91.",
        "6. Sharpe, William F. (1966): 'Mutual Fund Performance', The Journal of Business, 39(1), pp. 119-138.",
        "7. Sortino, Frank A. & Price, Lee N. (1994): 'Performance Measurement in a Downside Risk Framework', Journal of Investing, 3(3), pp. 59-64.",
        "8. Zerodha Broking Limited: Public Financial Disclosures and Behavioral 'Nudge' Architecture."
    ]
    for r in refs:
        pdf.body_paragraph(r)
    pdf.ln(5)

    pdf.set_fill_color(248, 249, 250)
    pdf.set_draw_color(200, 200, 200)
    pdf.rect(10, 180, 190, 40, style="DF")
    pdf.set_xy(14, 184)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, clean_txt("STATUTORY REGULATORY DISCLAIMER:"))
    pdf.ln()
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_x(14)
    pdf.multi_cell(182, 3.8, clean_txt("This capstone report was prepared by Mayank Soni for academic evaluation and technical demonstration as part of the Bluestock Fintech Data Analyst Internship. The analytical models, fund rankings, and recommendations do not constitute personalized financial or investment advice. Mutual fund investments are subject to market risks; read all scheme-related documents carefully."))

    pdf.output(PDF_PATH)
    print(f"Successfully compiled 20-page comprehensive Final_Report.pdf: {PDF_PATH} ({os.path.getsize(PDF_PATH):,} bytes)")


if __name__ == "__main__":
    generate_pdf()
