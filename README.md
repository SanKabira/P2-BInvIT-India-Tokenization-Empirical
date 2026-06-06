# P2: Blockchain Tokenization of Indian InvITs — Liquidity, Cost, and Access Effects

> **An Empirical Study of Blockchain-Based Tokenization Effects on Liquidity, Transaction Cost, and Retail Access in India's Listed Infrastructure Investment Trusts (InvITs)**

[![Target](https://img.shields.io/badge/Target-Scopus%20Q1%2FQ2-blue)](https://www.scopus.com)
[![Status](https://img.shields.io/badge/Status-Data%20Collection%20Phase-orange)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-green)]()
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey)]()
[![Reproducible](https://img.shields.io/badge/Reproducible-Yes-success)]()

---

## Research Objective

This paper empirically tests whether blockchain-based tokenization of Indian InvITs improves three outcomes for investors:

1. **Liquidity** — narrower bid-ask spreads, higher turnover, reduced price impact
2. **Transaction cost** — lower frictional and intermediation costs
3. **Access** — broader retail participation through fractionalization and lower minimum lot sizes

The study uses **real, downloadable market and regulatory data** — NSE trading data for listed InvITs (FY2024-25), Screener.in financials, and coded SEBI regulatory provisions — analyzed through reproducible statistical and machine-learning notebooks.

### Industry alignment (2025-26)
- SEBI InvIT Master Circular (July 2025) and the 3rd Amendment (2025)
- SM-REIT framework
- National Infrastructure Pipeline 2030

---

## NO FABRICATED DATA — Core Principle

Every number in this paper traces to a real, downloadable source that is committed to this repository (or, where licensing prohibits redistribution, fully documented with a retrieval URL and access date in `DATA_SOURCES.md`). No synthetic, simulated, or invented observations are used as empirical results. Any simulated/illustrative figures are clearly labelled as such and confined to the supplementary section.

---

## Repository Structure

```
P2-BInvIT-India-Tokenization-Empirical/
│
├── data/
│   ├── raw/                 # Original downloaded datasets (DO NOT MODIFY)
│   │   ├── NSE/             # IndiGrid & listed-InvIT daily price/volume/bid-ask FY24-25
│   │   ├── Screener/        # Core Watchlist InvIT financial exports
│   │   └── SEBI/            # Master Circular 2025 + amendment source PDFs
│   └── processed/           # Cleaned, analysis-ready datasets
│
├── notebooks/               # Reproducible Jupyter/Colab analysis
│   ├── 01_liquidity_ttest.ipynb        # Paired t-test pre/post tokenization
│   ├── 02_access_chisquare.ipynb       # Chi-square: access by investor tier
│   ├── 03_adoption_logit.ipynb         # Logistic regression: adoption
│   ├── 04_ml_comparison_shap.ipynb     # LogReg vs RF vs XGBoost + SHAP
│   └── 05_garch_spread_volatility.ipynb # GARCH on bid-ask spread
│
├── figures/                 # 300 DPI figures generated FROM notebooks
│
├── manuscript/              # Paper draft, supplementary, journal-formatted versions
│
├── references/              # references.bib (Zotero/BibTeX export)
│
├── DATA_SOURCES.md          # Provenance register — every source URL + status
├── DATA_AVAILABILITY.md     # Data-availability statement (journal-ready)
└── requirements.txt         # Pinned Python dependencies
```

---

## Reproducibility Chain

This repository is designed so that any reviewer can reproduce every result from scratch:

```
[1] Raw sources (data/raw/) ──committed with URLs in DATA_SOURCES.md
        │
        ▼
[2] Cleaning notebooks ──> data/processed/ (deterministic, seed-fixed)
        │
        ▼
[3] Analysis notebooks ──> statistics, ML models, p-values, effect sizes
        │
        ▼
[4] Figure cells ──> figures/*.png at 300 DPI
        │
        ▼
[5] manuscript/ ──> every claim cites a processed file + notebook cell
```

**To reproduce:**
```bash
git clone https://github.com/SanKabira/P2-BInvIT-India-Tokenization-Empirical.git
cd P2-BInvIT-India-Tokenization-Empirical
pip install -r requirements.txt
jupyter lab   # run notebooks 01 → 05 in order
```
All random operations fix `random_state=42`. Software versions are pinned in `requirements.txt`.

---

## Data Provenance & Ethics
- Market data sourced from NSE/Screener.in for academic research use; redistribution limited per source terms (see `DATA_SOURCES.md`).
- Survey data (if used) follows the documented sample frame; no responses are invented.
- Regulatory text quoted from official SEBI publications under fair-use for research.

---

## Author
**Sandeep S** — PhD Research Scholar (REITs & InvITs)
GitHub: [@SanKabira](https://github.com/SanKabira)

## License
Code: MIT. Text & figures: CC BY 4.0. Third-party data retains its original license.
