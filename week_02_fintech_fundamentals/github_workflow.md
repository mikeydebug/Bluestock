# Week 2 — Professional Git & GitHub Collaboration Workflow

**File:** `week_02_fintech_fundamentals/github_workflow.md`  
**Author:** Mayank Soni (Data Analyst Intern)  
**Organization:** Bluestock Fintech  
**Topic:** Software Engineering Fundamentals — Version Control & CI/CD Discipline  

---

## 1. Version Control Philosophy in FinTech Analytics

In quantitative finance and data engineering, version control serves as a statutory audit trail. Every algorithmic modification, data cleaning rule change, and metric calculation adjustment must be traceably recorded, reviewable through pull requests, and reproducible.

---

## 2. Standard Branching Strategy (GitFlow / Feature Branching)

```
main (Production / Stable Releases)
  │
  ├── release/v1.0.0 (Submission Freeze)
  │     │
  │     └── hotfix/patch-nav-parsing
  │
  └── develop (Integration Branch)
        │
        ├── feature/nav-api-ingestion
        ├── feature/sqlite-star-schema
        ├── feature/fund-scorecard-quant
        └── feature/powerbi-dax-models
```

- **`main`**: Protected branch containing validated, release-ready deliverables. Direct pushes are disabled; changes require approved Pull Requests with passing CI tests.
- **`develop`**: Central integration branch where feature branches are merged.
- **`feature/*`**: Ephemeral branches for developing specific tasks (e.g., `feature/fund-scorecard`).

---

## 3. Step-by-Step Command Walkthrough

### 3.1 Initializing the Local Repository & Verification
```bash
# Navigate to the workspace root
cd /Users/mayanksoni/Desktop/Bluestock_FinTech

# Initialize local git repository (if not already done)
git init

# Check working tree status
git status
```

### 3.2 Branch Management
```bash
# Create and switch to a new feature branch
git checkout -b feature/mutual-fund-capstone

# List all local branches
git branch -v
```

### 3.3 Atomic Commits with Conventional Commit Messages
Commits should be atomic (focusing on a single logical change) and follow standard conventions:
- `feat:` Introduces a new feature or analytical engine
- `fix:` Patches an anomaly, bug, or calculation defect
- `docs:` Documentation, READMEs, or analysis reports
- `test:` Adds or updates automated test suites
- `refactor:` Code improvements without altering output metrics

```bash
# Stage specific files (respecting .gitignore to avoid committing *.db or caches)
git add week_01_core_analytics/
git add week_02_fintech_fundamentals/

# Commit with a clear, descriptive message
git commit -m "feat(week-1-2): implement foundational analytics, SQL suite, and FinTech domain modules"
```

### 3.4 Linking to a Remote Repository (GitHub)
*Note on Remote Operations:* A remote repository is only linked and pushed when valid remote credentials and repository targets are established.
```bash
# Add authenticated remote origin (Example syntax)
# git remote add origin https://github.com/mayanksoni/Bluestock_FinTech_Internship.git

# Set upstream tracking and push
# git push -u origin main
```

### 3.5 Pull Request (PR) Lifecycle & Code Review
1. **Push Feature Branch:** `git push origin feature/mutual-fund-capstone`
2. **Open Pull Request:** Open PR targeting `develop` on GitHub with:
   - Summary of changes implemented
   - Evidence of passing tests (`pytest` run log)
   - Data diff / schema impact assessment
3. **Peer Review:** Code review conducted by senior mentors.
4. **Squash & Merge:** Merge feature branch into integration branch upon approval.

### 3.6 Semantic Version Tagging
Release milestones are tagged with immutable semantic versions:
```bash
git tag -a v1.0.0 -m "Release v1.0.0: Complete Bluestock FinTech Internship Deliverables"
# git push origin v1.0.0
```

---

## 4. Repository Hygiene & Secret Prevention
- Sensitive `.env` files and API keys are strictly barred via `.gitignore`.
- Binary databases (`*.db`, `*.sqlite`) are excluded to avoid Git bloat; reproducible database build scripts (`run_pipeline.py`) are committed instead.
- Jupyter Notebook checkpoints (`.ipynb_checkpoints`) and Python compilation artifacts (`__pycache__`) are excluded.
