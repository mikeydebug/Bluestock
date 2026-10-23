# Bluestock FinTech — Capstone Project Demo Video Script

**Title:** Mutual Fund Quantitative Analytics & Power BI Intelligence Suite  
**Presenter:** Mayank Soni (Data Analyst Intern, Bluestock FinTech)  
**Total Target Duration:** 5 Minutes (00:00 - 05:00)  
**Deliverables Covered:** AMFI Ingestion, SQLite Star Schema, Quant Engine, Power BI Dashboard, Risk Recommender CLI  

---

## Video Recording Setup Guide
1. **Resolution:** 1080p (1920x1080) at 30 or 60 fps.
2. **Tools Recommended:** OBS Studio or Loom for dual-screen recording (webcam in bottom-right corner, screen sharing active).
3. **Screen Layouts:**
   - Visual Scene 1: Presentation Title Slide & Architecture Diagram
   - Visual Scene 2: Terminal / VS Code running automated pipeline and pytest suite
   - Visual Scene 3: Power BI Dashboard (PDF/PNG Walkthrough across all 4 pages)
   - Visual Scene 4: Interactive Risk Recommender CLI Demo
   - Visual Scene 5: Executive Conclusions & Final Report Preview

---

## Timed Narration Script

### [00:00 - 00:45] Scene 1: Introduction & Project Scope
- **Visual:** Display Slide 1 & Slide 2 of `Bluestock_MF_Presentation.pptx`.
- **Narration:**
  > "Hello everyone, my name is Mayank Soni, and today I am excited to present my Data Analytics Internship Capstone Project at Bluestock FinTech: The Mutual Fund Quantitative Analytics and Business Intelligence Suite.
  >
  > In the Indian mutual fund landscape, retail investors often chase past returns without understanding underlying risk, volatility, or fee drag. Our mission for Bluestock was to engineer an end-to-end institutional-grade analytics pipeline that digests authentic AMFI NAV data across six flagship mutual funds, unifies 5,000 investor transactions into a star schema SQLite database, calculates risk-adjusted quantitative metrics, and delivers dynamic intelligence through an interactive 4-page Power BI Dashboard."

---

### [00:45 - 01:45] Scene 2: ETL Pipeline, Database Architecture & Automated Testing
- **Visual:** Open VS Code terminal. Run `python3 mutual_fund_capstone/scripts/run_pipeline.py` followed by `pytest -v tests/`. Show the terminal output and SQLite schema diagram.
- **Narration:**
  > "Let's begin under the hood with our engineering foundation. Here in our terminal, I'm executing our master pipeline script, `run_pipeline.py`.
  >
  > In just over six seconds, the pipeline ingests 20,389 authentic daily NAV records directly from the official AMFI API across our multi-asset cohort: Nippon India Large Cap, SBI Small Cap, Quant Mid Cap, Axis ELSS, HDFC Money Market, and Aditya Birla Debt.
  >
  > We enforce strict non-trading day data hygiene—refusing to forward-fill weekend prices—and load a star-schema relational model in SQLite with foreign key constraints and B-tree indexes. 
  >
  > To ensure production reliability, we built an automated QA test suite using `pytest`. As you can see, all 20 tests pass with a 100% success rate, validating our date parsers, NAV positivity rules, CAGR formulations, CAPM regression models, and SQL integrity."

---

### [01:45 - 03:30] Scene 3: Power BI Dashboard & Visual Intelligence
- **Visual:** Switch full screen to `final_submission/dashboard_exports/Dashboard.pdf` or open the 4 high-res page PNGs in sequence.

#### Page 1: Industry & Fund House Overview (01:45 - 02:10)
- **Narration:**
  > "Now turning to our interactive Power BI Business Intelligence Suite. 
  >
  > Page 1 provides an executive macroeconomic view of our fund universe. We track ₹74.87 Lakh Crores in total AUM, monitor net monthly inflows, and display our 6 funds categorized by risk grade and expense ratio. Notice how equity funds command higher TERs of 0.70% to 0.76%, while money market debt operates at an ultra-low 0.20%."

#### Page 2: Fund Performance & Quantitative Risk Matrix (02:10 - 02:40)
- **Narration:**
  > "Page 2 is our quantitative engine room. Here, investors can analyze multi-period CAGR alongside modern portfolio theory metrics. 
  >
  > SBI Small Cap leads aggressive wealth generation with a 23.47% 3-year CAGR and an annual Alpha of +12.39% over the NIFTY 100. However, on a risk-adjusted basis, HDFC Money Market shines with an incredible Sharpe ratio of 1.97 and a Sortino ratio of 2.14, accompanied by a near-zero maximum drawdown of just -0.01%."

#### Page 3: Investor Demographics & Behavioral Analytics (02:40 - 03:05)
- **Narration:**
  > "Page 3 analyzes 5,000 investor transactions. We uncover that 64.7% of all active capital originates from millennial and Gen-Z cohorts aged 25 to 40, predominantly through monthly SIPs. 
  >
  > Furthermore, our geographic breakdown proves that Beyond-30 or B30 cities now contribute 42% of total transaction volume, highlighting the democratization of retail investing across Tier 2 and Tier 3 India."

#### Page 4: SIP Market Trends & Scenario Calculator (03:05 - 03:30)
- **Narration:**
  > "Page 4 highlights SIP continuity and long-term compounding. Investors can model 5-year and 10-year monthly SIP horizons with expected returns of 12% to 18%. 
  >
  > Our cohort analysis demonstrates that investors who maintain unbroken SIP schedules for over 36 months experience a 94% retention rate and weather market drawdowns far better than lump-sum market timers."

---

### [03:30 - 04:15] Scene 4: Interactive Risk Recommender CLI Demo
- **Visual:** Switch back to terminal. Run `python3 mutual_fund_capstone/scripts/recommender.py` and interactively select Conservative, Moderate, and Aggressive profiles.
- **Narration:**
  > "To bridge analytics with client action, we developed a production-ready Python CLI Recommender tool. 
  >
  > When a client with a Conservative risk profile inputs an investment, the algorithm allocates capital to low-volatility debt and money market funds with a 95% Value at Risk under 0.05%. 
  >
  > Conversely, for an Aggressive profile with a 5-year horizon, the recommender dynamically constructs an equity growth portfolio anchored by Nippon Large Cap and SBI Small Cap, optimizing for multi-factor scorecard rating and alpha generation."

---

### [04:15 - 05:00] Scene 5: Conclusion, Strategic Roadmap & Q&A
- **Visual:** Switch to Slide 12 of `Bluestock_MF_Presentation.pptx` (Strategic Recommendations) and flash `Final_Report.pdf`.
- **Narration:**
  > "In conclusion, this project delivers a complete enterprise-ready mutual fund analytics ecosystem for Bluestock FinTech:
  > - An automated data ingestion and ETL pipeline.
  > - An optimized star-schema SQLite data warehouse.
  > - A mathematically verified quantitative analytics engine.
  > - A 4-page executive Power BI Dashboard suite.
  > - And a comprehensive 20-page research report and 12-slide presentation deck.
  >
  > All source code, datasets, and documentation are committed and packaged for immediate deployment. Thank you for your time and mentorship throughout this internship, and I look forward to your questions!"

---

## Demo Video Checklist
- [x] Clear audio with no background noise.
- [x] Full-screen transitions smooth between slides, terminal, and dashboard.
- [x] Video length between 4:45 and 5:15 minutes.
- [x] Upload video to Google Drive under `06_Demo_Video/` and set share permissions to 'Anyone with the link can view'.
