# CHANGELOG — P2: Scopus/Q1 Rigour Uplift (Reviewer-Style Response)

**Manuscript:** *Did Lowering the Entry Ticket Move the Needle? Liquidity Around SEBI's 2025 InvIT Reform, and What It Implies for Tokenization*
**Target journal:** Journal of Risk and Financial Management (JRFM, MDPI; Scopus, Finance).
**Uplift date:** 2026-06-09. **Author:** Sandeep S (GitHub: SanKabira).

This change-log responds point-by-point to the internal `GAP_AUDIT_P2.md` (senior finance-journal referee + quantitative research engineer stance). Each item gives the original shortfall, the action taken, and where the evidence now lives. **Integrity statement:** every new number traces to the continuous daily OHLCV series pulled from the Perplexity Finance connector on 2026-06-09 and committed to the repository; retrieval is logged in `DATA_SOURCES.md`. No observation was fabricated or simulated. The survey arm remains unfielded and is flagged as such throughout.

---

## Responses to P0 (blocker) items

### P0-1 — Statistical power / sample size
**Original concern:** The event file held ~126 trading days/entity (~3 months each side); cross-entity paired tests had only n = 6 pairs — underpowered, and referees would reject inference from six pairs.
**Action taken:** Re-pulled a **gap-free continuous daily price/volume series spanning January 2024 – December 2025** from the same Finance connector (~20 months pre-reform, ~3 months post). The estimation panel is now **2,954 entity-days** across the six trusts (`data/processed/liquidity_daily_panel_continuous.csv`). All inference now runs on this panel rather than on six aggregated pairs.
**Where to verify:** `notebooks/05_did_robustness.py`; panel CSV; Table 2 header reports n = 2,954 entity-days.

### P0-2 — No identification strategy
**Original concern:** Pre/post means and a pooled Welch test do not isolate the reform from market-wide trends; the REIT "control" was asserted, not modelled.
**Action taken:** Implemented a **two-way fixed-effects difference-in-differences** estimator with entity and date fixed effects, treatment = InvIT × Post, with the three listed REITs (Embassy, Mindspace, Brookfield India) as an unaffected control group (the September 2025 amendment applies to InvITs, not REITs). The within (two-way demeaning) estimator is validated against a dummy-OLS specification to machine precision to avoid the ~490-column dummy matrix.
**Result:** On log-Amihud the InvIT × Post interaction is **−0.20306** (correctly signed: InvIT illiquidity fell relative to controls), but not statistically significant once common time trends are removed and SEs are clustered across only three treated trusts. The high–low spread interaction **is** significant (−0.0023393, p = 0.034).
**Where to verify:** `data/processed/did_results.csv`; manuscript §5.2; Table 2; Figure 7.

### P0-3 — Inference fragility
**Original concern:** Welch t on pooled daily observations treats serially-correlated daily liquidity as i.i.d., understating SEs and overstating significance.
**Action taken:** (i) **Entity-clustered standard errors** in the DiD (clustered across the small number of trusts, the conservative choice). (ii) An **entity-block bootstrap** (2,000 replications resampling whole trusts) for the headline log-Amihud and raw-Amihud effects. The bootstrap log-Amihud mean is −0.20259 with a 95% CI of [−0.636, +0.105] — tighter than the cluster-robust interval but still straddling zero, confirming the effect is negative on average but imprecise.
**Where to verify:** `data/processed/bootstrap_cis.csv`; manuscript §5.3; Figure 7 (both CI types plotted).

---

## Responses to P1 (important) items

### P1-4 — Single event date, no placebo
**Original concern:** One notification date (3 September 2025) with no test that the effect is specific to it.
**Action taken:** Added **four placebo (pseudo-event) dates** at pre-reform points (3 Jun 2024, 3 Sep 2024, 3 Dec 2024, 3 Mar 2025) and an **event-window sensitivity grid** (±20/±40/±60/±90/±120 trading days). The placebo DiD coefficients are all small (−0.064, −0.054, −0.068, −0.056) and none approaches the true −0.203 (≈3× larger), consistent with parallel pre-trends. The event-window estimate stabilises as the window widens (+0.085 at ±20d, then −0.074, −0.152, −0.155, −0.163), showing the negative effect is not an artefact of one hand-picked window.
**Where to verify:** `data/processed/placebo_tests.csv`, `event_window_sensitivity.csv`; manuscript §5.3; Table 3; Figures 8–9.

### P1-5 — Narrow liquidity proxy set
**Original concern:** Amihud + high-low + Roll only; Roll often undefined; turnover used loosely.
**Action taken:** Expanded to a **six-proxy matrix**: Amihud illiquidity, log-Amihud, Corwin–Schultz high–low spread, intraday high–low relative spread, Lesmond zero-return ratio, turnover ratio, and rupee volume. The InvIT pre/post panel (Table 1) shows every cost-based proxy moving toward greater liquidity (Amihud −93.0%, t = −2.64, p = 0.008; log-Amihud −80.4%; Corwin–Schultz −22.5%; high–low spread −19.9%), while volume-based proxies roughly double (turnover +135.2%, rupee volume +150.9%). Results are no longer proxy-dependent; Roll is dropped where the covariance is positive (undefined).
**Where to verify:** `data/processed/liquidity_proxy_matrix.csv`; manuscript §5.1; Table 1; Figures 1–6.

### P1-6 — GARCH(1,1) specification unjustified
**Original concern:** No model selection, no diagnostics, no persistence/half-life discussion.
**Action taken:** Ran a **per-trust GARCH-family model-selection exercise** (GARCH, EGARCH, GJR-GARCH, all with Student-t innovations) ranked by AIC. The AIC-minimising winners are **EGARCH for PowerGrid InvIT (959.58) and Brookfield India (1284.19), plain GARCH for IndiGrid (916.29), IRB InvIT (1012.62), and Embassy (1523.93), and GJR for Mindspace (1331.96)** — direct evidence that leverage/asymmetry matters for some series and that a blanket GARCH(1,1) would have been misspecified for them. The §5.4 narrative now matches the selected winners exactly.
**Where to verify:** `data/processed/garch_model_selection.csv`, `garch_params.csv`; manuscript §5.4; Table 4; Figure 5.

### P1-7 — InvIT-vs-REIT causal framing / ML overclaim risk
**Original concern:** The ML tier classifier (ROC-AUC ~0.9) sat near the causal claims, risking conflation of a descriptive classifier with the causal event effect.
**Action taken:** The ML section is now **explicitly framed as descriptive/robustness** (microstructure separability of liquid vs illiquid names) and physically separated from the DiD causal claim into §5.5. The text states plainly that the classifier "validates the pipeline" rather than the event effect, and reports ROC-AUC of 0.906 (LogReg), 0.900 (RF), 0.901 (XGB) with SHAP attributing the signal to log rupee volume and high–low spread. The chi-square access test (χ² = 2.24, p = 0.13) is reported without overclaiming.
**Where to verify:** `data/processed/ml_classification_results.csv`, `shap_feature_importance.csv`, `chi_square_access.csv`; manuscript §5.5; Table 5; SHAP figure.

### P1-8 — Literature positioning thin / dated
**Original concern:** 16 references, several non-indexed (arXiv, "Anonymous"), little 2024–2026 RWA-tokenization and InvIT microstructure.
**Action taken:** Expanded to **26 verified, citable references** (APA/MDPI style), prioritising 2023–2026 Scopus-indexed work. Added the method anchors (Amihud 2002; Corwin–Schultz 2012; Ardia, Guidotti & Kroencke 2024; Roll 1984; Bollerslev 1986; Nelson 1991; Glosten–Jagannathan–Runkle 1993; Lundberg & Lee 2017; Chen & Guestrin 2016) and current liquidity/tokenization sources (Będowska-Sójka et al. 2022; Hafner, Linton & Wang 2024; Lee et al. 2024; Muzaffar & Malik 2024; Essa & Giouvris 2023; Swinkels 2023; Zhang, Li & Roca 2023). **The non-citable arXiv/"Anonymous" items were dropped**; the Popov et al. (2022) entry was corrected. DOIs verified.
**Where to verify:** `references/references.bib` (28 entries; 26 cited in-text); manuscript References section.

---

## Responses to P2 (polish) items

### P2-9 — Contribution framing
**Original concern:** "First empirical baseline" asserted without an explicit gap statement.
**Action taken:** Rewrote the contribution paragraph as an **identification-aware empirical baseline** against which any future tokenized structure can be benchmarked, with the gap statement made explicit relative to prior regulatory-liquidity event studies. The abstract and introduction now frame the reform as "a precondition for, rather than a treatment of, tokenization itself."

### P2-10 — Survey arm
**Original concern:** Correctly pending — must stay clearly flagged after the uplift.
**Action taken:** All "survey pending / no tokenized InvIT exists in India" caveats are **preserved verbatim** in the Limitations and Data Availability sections. No survey responses were invented.

---

## New analytical artifacts added in this uplift

1. `notebooks/05_did_robustness.py` — continuous-panel build, two-way FE DiD, cluster-robust + entity-block-bootstrap CIs, placebo dates, event-window grid, six-proxy matrix, GARCH model selection. Runs end-to-end on committed real data.
2. New processed tables: `did_results.csv`, `bootstrap_cis.csv`, `placebo_tests.csv`, `event_window_sensitivity.csv`, `liquidity_proxy_matrix.csv`, `garch_model_selection.csv`, `garch_params.csv`, `ml_classification_results.csv`, `shap_feature_importance.csv`, `chi_square_access.csv`, `liquidity_daily_panel_continuous.csv`.
3. New 300-DPI figures (1–10): Amihud panel by trust, mean Amihud pre/post, rupee turnover, high–low spread distribution, selected-model conditional volatility paths, six-proxy robustness panel, DiD coefficient with both CI types, event-window sensitivity curve, placebo-versus-real comparison, SHAP feature importance.
4. `manuscript/P2_manuscript_JRFM.docx` — MDPI/JRFM-styled manuscript (Article type, Palatino Linotype) mirroring the uplifted Markdown.

## Items deliberately kept intact (per audit Section B)

- The baseline empirical result — **Amihud illiquidity falls post-reform, concentrated in the InvITs** — is preserved; the uplift strengthens rather than replaces it.
- The reproducible notebook pipeline and `DATA_SOURCES.md` provenance.
- The honest treatment of the survey arm as pending.
