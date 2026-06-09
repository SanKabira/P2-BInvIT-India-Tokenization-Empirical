# Data Sources & Provenance Register — P2

This document tracks **every** data source used in this paper. No number enters the analysis without an entry here. Per the project integrity mandate: every figure traces to a real, downloadable source committed here; where redistribution is restricted, the retrieval URL and access date are logged.

## Status Legend
- 🔴 Not collected
- 🟡 Identified / restricted redistribution (retrieval URL + access date logged)
- 🟢 Collected and committed / documented

**Treatment event for the empirical design:** SEBI (Infrastructure Investment Trusts) (Third Amendment) Regulations, 2025 — notified/gazetted **2 September 2025** — which reduced the minimum investment in a privately placed InvIT from **₹1 crore to ₹25 lakh** (Regulation 14(2)(c)) and omitted the ₹25 crore proviso. Pre/post event window: **2025-06-03 → 2025-12-03**.

---

## Module 1 — Market Data (Liquidity & Cost) — PRIMARY SOURCE: Perplexity Finance connector

Daily OHLCV + volume pulled via the Perplexity Finance connector (point-in-time provider data). NSE/BSE direct redistribution is restricted (NSE data policy), so the Finance connector is the primary retrieval path; raw CSVs are committed.

| # | Entity (type) | Ticker | Files | Status | Date |
|---|---|---|---|---|---|
| 1 | IndiGrid (InvIT) | INDIGRID-IV.NS | Finance_Connector/INDIGRID_fy2425_daily.csv, INDIGRID_event_2025.csv | 🟢 | 2026-06-06 |
| 2 | PowerGrid InvIT (InvIT) | PGINVIT.NS | Finance_Connector/PGINVIT_fy2425_daily.csv, PGINVIT_event_2025.csv | 🟢 | 2026-06-06 |
| 3 | IRB InvIT (InvIT) | IRBINVIT.NS | Finance_Connector/IRBINVIT_fy2425_daily.csv, IRBINVIT_event_2025.csv | 🟢 | 2026-06-06 |
| 4 | Embassy REIT (REIT, robustness) | EMBASSY.NS | Finance_Connector/EMBASSY_fy2425_daily.csv, EMBASSY_event_2025.csv | 🟢 | 2026-06-06 |
| 5 | Mindspace REIT (REIT, robustness) | MINDSPACE.BO | Finance_Connector/MINDSPACE_fy2425_daily.csv, MINDSPACE_event_2025.csv | 🟢 | 2026-06-06 |
| 6 | Brookfield India REIT (REIT, robustness) | BIRET.BO | Finance_Connector/BIRET_fy2425_daily.csv, BIRET_event_2025.csv | 🟢 | 2026-06-06 |

**Coverage gap (documented, not fabricated):** National Highways InvIT (NHIT) and Cube Highways InvIT (CUBEINVIT) are **not in the Finance connector provider coverage** as of 2026-06-06 (ticker lookup returned NOT_FOUND). The analysis proceeds with the 6 entities above (3 InvITs + 3 REIT robustness controls) and notes this gap. No proxy or imputed series substitutes for the missing entities.

**2026-06-09 continuous-panel re-pull (rigour uplift):** to address the statistical-power shortfall flagged in `GAP_AUDIT_P2.md` (P0-1), a **gap-free continuous daily price/volume series spanning January 2024 – December 2025** was pulled from the same Perplexity Finance connector for all six entities (~20 months pre-reform, ~3 months post). This yields the estimation panel `data/processed/liquidity_daily_panel_continuous.csv` (**2,954 entity-days**) on which the difference-in-differences, bootstrap, placebo, event-window-sensitivity, six-proxy, and GARCH-model-selection analyses now run. Tickers: INDIGRID-IV.NS, PGINVIT.NS, IRBINVIT.NS (InvITs); EMBASSY.NS, MINDSPACE-RR.NS, BIRET.BO (REIT controls). Retrieval method: Perplexity Finance connector continuous-CSV pull, access date **2026-06-09**. No observation was fabricated, imputed, or simulated; the new numbers trace to the committed continuous CSVs.

Liquidity proxies derived from this data (committed in data/processed/): Amihud (2002) illiquidity, Roll (1984) spread, high-low relative spread, daily rupee turnover, zero-return-day incidence. NSE data policy (redistribution restricted) 🟡: https://www.nseindia.com/static/market-data/nse-data-policy (accessed 2026-06-06).

## Module 2 — Company Financials (free public pages)

| # | Variable | Source | Status | Note |
|---|---|---|---|---|
| 7 | InvIT/REIT fundamentals (cross-check) | Screener.in free public company pages | 🟡 | Screener bulk export is premium-only (https://support.screener.in/article/28-export-screen-results, accessed 2026-06-06). Free public pages readable; Finance connector is the primary structured source. |

## Module 3 — SEBI Regulatory Coding

| # | Variable | Source | File | Status | Date |
|---|---|---|---|---|---|
| 8 | InvIT Master Circular (11 Jul 2025), 237 pp | SEBI | data/raw/SEBI/SEBI_Master_Circular_InvIT_2025-07-11.pdf | 🟢 | 2026-06-06 |
| 9 | InvIT 3rd Amendment 2025 (gazette 2 Sep 2025), 10 pp | SEBI | data/raw/SEBI/SEBI_InvIT_3rd_Amendment_2025-09-03.pdf | 🟢 | 2026-06-06 |
| 10 | Coded provisions matrix (14 provisions, P01–P14) | Derived from above | data/raw/SEBI/provisions_coded.csv | 🟢 | 2026-06-06 |

URLs (🟢 public/free):
- Master Circular landing: https://www.sebi.gov.in/legal/master-circulars/jul-2025/master-circular-for-infrastructure-investment-trusts-invits-_95233.html
- 3rd Amendment landing: https://www.sebi.gov.in/legal/regulations/sep-2025/securities-and-exchange-board-of-india-infrastructure-investment-trusts-third-amendment-regulations-2025_96437.html
- 3rd Amendment gazette PDF: https://www.sebi.gov.in/sebi_data/attachdocs/sep-2025/1757046936652.pdf

## Module 4 — Survey (instrument only; NO responses collected or fabricated)

| # | Variable | Source | File | Status | Date |
|---|---|---|---|---|---|
| 11 | Sample frame & design | Sandeep_S_PhD_Vault/09_Survey_Zoho (private) | data/raw/survey/SAMPLE_FRAME.md | 🟢 (documented) | 2026-06-06 |
| 12 | Survey responses | Zoho field collection | data/raw/survey/survey_responses.csv | 🔴 **PENDING — not collected** | — |

The instrument (8 constructs, 5-pt Likert, target N≥250) resides in a **private** repository and is summarized in SAMPLE_FRAME.md without redistribution. **No survey responses have been collected, simulated, or fabricated.** Any survey-dependent model (adoption logistic regression) is marked PENDING in notebooks/04_survey_adoption_PENDING.py and aborts if no real data file is present.

---

## Processed outputs (all derived from the raw sources above)

### Original (event-file) outputs
- data/processed/liquidity_daily_panel.csv — daily proxies, all 6 entities, pre/post flagged
- data/processed/liquidity_event_summary.csv — per-entity pre/post means/medians
- data/processed/paired_tests.csv — cross-entity paired t / Wilcoxon (post vs pre)
- data/processed/welch_daily_tests.csv — pooled daily-level Welch tests
- data/processed/chi_square_access.csv + entity_liquidity_tiers.csv — access tier x stale-day
- data/processed/garch_params.csv — GARCH params + pre/post conditional volatility
- data/processed/ml_classification_results.csv — LogReg/RF/XGBoost tier classification
- data/processed/shap_feature_importance.csv — SHAP attribution (XGBoost)

### Rigour-uplift outputs (2026-06-09, continuous panel; produced by notebooks/05_did_robustness.py)
- data/processed/liquidity_daily_panel_continuous.csv — continuous Jan-2024–Dec-2025 panel (2,954 entity-days)
- data/processed/liquidity_proxy_matrix.csv — six-proxy pre/post matrix with t-tests
- data/processed/did_results.csv — two-way FE DiD (InvIT×Post), entity-clustered SEs, four outcomes
- data/processed/bootstrap_cis.csv — entity-block bootstrap CIs (2,000 reps)
- data/processed/placebo_tests.csv — four pre-reform pseudo-event DiD coefficients
- data/processed/event_window_sensitivity.csv — DiD over ±20/40/60/90/120-day windows
- data/processed/garch_model_selection.csv — GARCH/EGARCH/GJR AIC per trust + selected model

---
*Maintainer: Sandeep S (@SanKabira). Last updated: 2026-06-09 (Scopus/Q1 rigour uplift).*
