# GAP AUDIT — P2 (SEBI 2025 InvIT Reform Liquidity Event-Study)

**Target journal:** Journal of Risk and Financial Management (JRFM, MDPI; Scopus Q2/Q1, Finance).
**Reviewer stance:** senior finance-journal referee + quantitative research engineer.
**Audit date:** 2026-06-09. **Verdict on current draft:** *major revision* — the empirical core is honest and reproducible, but identification, statistical power, and robustness fall short of Scopus/Q1 acceptance.

This audit is grounded in the committed code (`notebooks/01_liquidity_event_study.py`, `notebooks/03_ml_garch.py`, `notebooks/lib_liquidity.py`) and data (`data/raw/Finance_Connector/`), not just the manuscript.

---

## A. Prioritized fix-list (P0 = blocker, P1 = important, P2 = polish)

| # | Pri | Shortfall (current) | Fix delivered in this uplift |
|---|-----|---------------------|------------------------------|
| 1 | **P0** | **Statistical power / sample.** Event file = 126 trading days/entity (~3 mo each side); cross-entity paired tests have only n=6 pairs. Underpowered; reviewers will reject inference from 6 pairs. | Re-pull **continuous Jan 2024–Dec 2025 daily series (~496 days/entity)** from the same Finance connector → ~20 mo pre / ~3 mo post. Panel ≈ 2,900 entity-days. |
| 2 | **P0** | **No identification strategy.** Pre/post means and a pooled Welch test do not isolate the reform from market-wide trends. REIT "control" is asserted, not modelled. | Proper **difference-in-differences** with entity + time fixed effects, treatment = InvIT × Post, clustered SEs; REITs as the control group. |
| 3 | **P0** | **Inference fragility.** Welch t on pooled daily obs treats serially-correlated daily liquidity as iid → understated SEs and overstated significance. | **Block bootstrap CIs** (entity-block resampling) for all headline effects; **Newey–West / cluster-robust** SEs in DiD. |
| 4 | **P1** | **Single event date, no placebo.** One notification date (3 Sep 2025); no test that the effect is specific to it. | **Placebo event dates** (pseudo-events pre-reform) + **event-window sensitivity** (±20/±40/±60 trading days) grid. |
| 5 | **P1** | **Narrow liquidity proxy set.** Amihud + high-low + Roll; Roll often undefined (positive cov). Turnover used loosely. | Add **Amihud (log), Corwin–Schultz high-low spread, zero-return ratio (Lesmond), turnover ratio, rupee-volume**; report a proxy matrix so results are not proxy-dependent. |
| 6 | **P1** | **GARCH(1,1) spec unjustified.** No model selection, no diagnostics, no persistence/half-life discussion. | Justify via **AIC/BIC vs GARCH(1,1)-t, EGARCH, GJR**; report persistence (α+β), Ljung–Box on standardised residuals, ARCH-LM. |
| 7 | **P1** | **InvIT-vs-REIT causal framing weak.** ML tier classifier (ROC-AUC ~0.9) is described near the causal claims; risks conflating a *descriptive* classifier with the *causal* event effect. | Re-frame ML explicitly as **descriptive/robustness** (microstructure separability), physically separated from the DiD causal claim. Keep, don't overclaim. |
| 8 | **P1** | **Literature positioning thin / dated.** 16 refs, several non-indexed (arXiv, "Anonymous"), little 2024–2026 RWA-tokenization & InvIT microstructure. | Expand to **~30 refs**, prioritise 2023–2026 Scopus-indexed; drop/replace non-citable items; fix DOIs to MDPI style. |
| 9 | **P2** | **Contribution framing.** "First empirical baseline" is asserted; needs explicit gap statement vs prior event-studies of regulatory liquidity shocks. | Rewrite contribution para with 3 numbered, defensible contributions. |
| 10 | **P2** | **Survey arm.** Correctly pending — must stay clearly flagged after uplift. | Preserve all "survey pending / no tokenized InvIT exists" caveats verbatim in Data Availability + Limitations. |

---

## B. What is already acceptable (keep intact)

- Real, connector-sourced OHLCV committed to the repo; no fabrication. **Baseline empirical result (Amihud illiquidity falls post-reform, concentrated in InvITs) is preserved** — the uplift strengthens, not replaces, it.
- Reproducible notebook pipeline; clear DATA_SOURCES provenance.
- Honest treatment of the survey arm as pending.

## C. New analytical artifacts this uplift adds (P2)

1. `notebooks/05_did_robustness.py` — continuous panel build, DiD with FE, cluster-robust + block-bootstrap CIs, placebo dates, event-window grid, proxy matrix, GARCH model selection. Runs end-to-end on committed real data.
2. New processed tables: `did_results.csv`, `bootstrap_cis.csv`, `placebo_tests.csv`, `event_window_sensitivity.csv`, `liquidity_proxy_matrix.csv`, `garch_model_selection.csv`.
3. New 300-DPI figures: DiD coefficient plot, event-window sensitivity curve, placebo distribution, proxy-robustness panel.
4. `CHANGELOG_P2.md` — reviewer-style point-by-point response.

*Integrity:* every new number traces to the committed continuous CSVs (`*_continuous_2024_2025.csv`) pulled from the Perplexity Finance connector on 2026-06-09; retrieval logged in `DATA_SOURCES.md`. No fabricated or simulated observations.
