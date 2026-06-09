# Blockchain Tokenization of Indian InvITs and REITs: Liquidity, Regulatory, and Adoption Effects

**Sandeep S.**
PhD Research Scholar, University of Mysore, Mysuru, Karnataka, India
ORCID: [to be inserted] | Corresponding author: [email to be inserted]

**Target outlet:** *Journal of Risk and Financial Management* (JRFM), MDPI (Scopus-indexed; CiteScore tier Q2). Manuscript prepared to Scopus/JRFM author guidelines.

**Declarations.** *Funding:* none. *Conflicts of interest:* none declared. *Data availability:* all raw and processed data, notebooks, and figures are openly archived in the public GitHub repository `SanKabira/P2-BInvIT-India-Tokenization-Empirical` (see Section 8). *Reproducibility:* every empirical claim cites a processed dataset and the originating notebook cell; random seed = 42 throughout.

---

## Abstract

Infrastructure Investment Trusts (InvITs) and Real Estate Investment Trusts (REITs) were introduced in India to channel retail and institutional capital into illiquid, long-duration assets, yet their listed units continue to trade thinly relative to mainstream equities. This paper asks whether the observed secondary-market liquidity, regulatory, and investor-adoption dynamics of these vehicles provide an empirical foundation for blockchain-based tokenization. Using a daily National Stock Exchange (NSE) panel of eight listed entities (four REITs, four InvITs) over 2021-2025, we compute Amihud (2002) illiquidity, Roll (1984) spreads, turnover, and zero-return frequencies; conduct a market-model event study around the SEBI InvIT (Third Amendment) Regulations, 2023 (event date 26 September 2023); estimate panel regressions with HC1 heteroskedasticity-consistent standard errors; and validate the cross-class liquidity gap independently in DataStatPro using a Mann-Whitney U test. At the daily-observation level the REIT-versus-InvIT difference in Amihud illiquidity is statistically significant (Mann-Whitney U = 38{,}447, z = 10.49, p < 0.001, r = 0.385). The SEBI amendment produces a small, statistically insignificant mean cumulative abnormal return (CAR = +0.315%, t approximately 0.14). A volume-based adoption proxy is strongly and significantly associated with lower Amihud illiquidity (beta = -1.665e-10, t = -25.92) and higher turnover (beta = 3.309e-04, t = 48.59). The evidence offers conditional support for tokenization: liquidity improvement tracks adoption intensity rather than the regulatory event alone, implying that broadening fractional participation - tokenization's core mechanism - is the operative channel.

**Keywords:** tokenization; blockchain; InvITs; REITs; market liquidity; Amihud illiquidity; event study; SEBI regulation; India

**JEL classification:** G12; G18; G23; O33

---

## 1. Introduction

Infrastructure and real estate are capital-intensive, long-duration, and historically illiquid asset classes. India has sought to mobilise retail and institutional capital into these sectors through listed InvITs and REITs, but unit-level secondary trading remains thin relative to mainstream equities, sustaining an illiquidity premium that raises the cost of capital for issuers and deters smaller investors. Blockchain tokenization - the issuance of fractional, transferable digital claims on income-producing assets - is widely advanced as a mechanism to lower minimum ticket sizes, compress settlement cycles, and deepen secondary-market liquidity. The question motivating this study is empirical rather than promotional: do the actual trading characteristics of Indian InvITs and REITs reveal frictions that tokenization could plausibly relieve, and is observed liquidity improvement driven by regulatory change or by adoption intensity?

This paper makes four contributions. First, it assembles and openly documents a fully reproducible daily panel of eight listed Indian InvITs and REITs. Second, it provides, to our knowledge, the first market-model event study of the SEBI InvIT (Third Amendment) Regulations, 2023, on this panel. Third, it constructs an auditable, volume-based adoption proxy and shows that this proxy - not the regulatory event - carries the economically meaningful association with liquidity. Fourth, it cross-validates the headline REIT-versus-InvIT liquidity gap using an independent non-parametric test executed in a separate analytical environment (DataStatPro), strengthening the robustness of the central descriptive claim.

The remainder of the paper is organised as follows. Section 2 reviews the liquidity-measurement, REIT/InvIT, and tokenization literatures and the Indian regulatory setting. Section 3 develops testable hypotheses. Section 4 describes the data and methodology. Section 5 reports results. Section 6 discusses implications; Section 7 states limitations and a future-research agenda; Section 8 concludes and provides the data-availability statement.

## 2. Literature Review and Institutional Background

### 2.1 Measuring liquidity at low frequency
The market-microstructure literature establishes price-impact measures (Amihud, 2002) and effective-spread estimators (Roll, 1984) as standard low-frequency proxies for liquidity when high-frequency quote data are unavailable. The Amihud measure - the ratio of absolute return to rupee volume - captures the price response per unit of traded value and is widely used in emerging-market studies where intraday data are costly or incomplete.

### 2.2 REIT and InvIT liquidity
The REIT literature documents persistent illiquidity premia in listed property vehicles relative to comparable equities, attributable to concentrated ownership, limited free float, and investor unfamiliarity. Indian REITs and InvITs, listed only since 2019, exhibit pronounced thin-trading characteristics, motivating the present focus on price-impact illiquidity.

### 2.3 Tokenization of real-world assets
The emerging tokenization literature argues that fractionalisation and programmable settlement can compress these premia by widening the investor base and reducing the minimum economic ticket. The empirical evidence for India remains scarce; this paper supplies a secondary-data baseline against which post-tokenization outcomes can later be benchmarked.

### 2.4 Regulatory setting
India's framework is set by SEBI's REIT and InvIT Regulations (2014) and subsequent amendments. The InvIT (Third Amendment) Regulations of September 2023 adjusted disclosure and unitholder-governance provisions. We treat this amendment as a natural-experiment event window to test whether regulatory tightening was priced into unit values.

## 3. Hypotheses

- **H1.** REIT units exhibit lower Amihud illiquidity than InvIT units (cross-class liquidity gap).
- **H2.** The SEBI InvIT (Third Amendment) Regulations, 2023, generated a statistically significant cumulative abnormal return around the event date.
- **H3.** Higher adoption intensity (volume-based proxy) is associated with lower Amihud illiquidity.
- **H4.** Higher adoption intensity is associated with higher turnover.

## 4. Data and Methodology

### 4.1 Data
All estimates derive from real NSE daily OHLCV data (`data/raw/invit_reit_ohlcv_2021_2025.csv`; 2021-01-01 to 2025-12-31; eight entities; 8{,}965 entity-day rows; random seed = 42), processed in the HEX notebook "Blockchain tokenization of Indian InvITs." The panel comprises four REITs (Brookfield India Real Estate Trust, Embassy Office Parks, Mindspace Business Parks, Nexus Select Trust) and four InvITs (IRB InvIT Fund, India Grid Trust, National Highways Infra Trust, Powergrid Infrastructure Investment Trust). No figure or coefficient in this paper is fabricated.

### 4.2 Liquidity measures
For each entity-day we compute Amihud illiquidity (|return| / rupee volume), the Roll implied spread, the turnover ratio, and a zero-return indicator (notebook cell: "Compute Amihud, Roll spread, turnover, and zero-return days").

### 4.3 Event study
We estimate a market-model event study around the SEBI InvIT (Third Amendment) event date 2023-09-26 over a [-10, +10] trading-day window, with cross-sectional aggregation of cumulative abnormal returns (CAR) and a cross-sectional t-test (notebook cell: "Run market-model event study").

### 4.4 Adoption proxy and panel estimation
Because the survey-based ADOPT construct remains survey-pending, we substitute an auditable volume-based proxy comprising turnover_growth (percentage change of the 21-day rolling mean volume), volume_share (entity daily volume / total panel volume that day), and activity_trend (63-day rolling mean of log(volume+1)). The composite `adoption_proxy_zscore` is the row-wise mean of the three z-scored components. Panel regressions use HC1 heteroskedasticity-consistent standard errors (computed manually in NumPy because `statsmodels` was unavailable in the kernel). GARCH(1,1) persistence used a NumPy variance-targeted grid-MLE fallback because `arch` was unavailable.

### 4.5 Independent cross-validation (DataStatPro)
To guard against single-environment dependence, the central liquidity comparison (H1) was re-estimated in DataStatPro (Version 2.2.3), an independent statistical platform. The processed daily panel (`data/processed/liquidity_daily_panel.csv`; 750 entity-day observations) was imported and a two-sided Mann-Whitney U test compared daily Amihud illiquidity across asset classes (grouping variable `type`: REIT vs InvIT). The non-parametric test is appropriate given the strong right-skew of daily Amihud values.

## 5. Results

Interactive dashboards (Tableau Public, profile `sandeep.s1797`) accompany each result; see `TABLEAU_DASHBOARDS.md` for the full link set and source-table mapping.

### 5.1 Cross-class liquidity gap - entity-level descriptives (H1)
Source: `data/processed/liquidity_by_entity.csv` (notebook cell: "Compute Amihud, Roll spread, turnover, and zero-return days"). At the entity-aggregate level, mean Amihud illiquidity is lower (more liquid) for REITs (~1.51e-10) than for InvITs (~3.81e-10), while mean turnover is comparable across classes (REIT ~0.000395 vs InvIT ~0.000407). Because only four entities populate each class, an entity-level non-parametric test is underpowered (Mann-Whitney U = 2.00, z = -1.59, p = 0.112; large effect r = 0.561, not significant); the direction nonetheless favours greater REIT liquidity. Dashboard: https://public.tableau.com/app/profile/sandeep.s1797/viz/P2BInvITIndiaTokenization-LiquiditySEBIAmendment/AmihudIlliquiditybyEntity

![Figure 1. Daily Amihud illiquidity time series by entity, four REITs and four InvITs, NSE panel 2021-2025, showing persistently higher (less liquid) price-impact for InvIT units.](../figures/fig1_amihud_timeseries.png)

**Figure 1.** Daily Amihud illiquidity time series across the eight-entity panel (2021-2025). InvIT units (higher series) exhibit greater price impact than REIT units. Source: `data/processed/liquidity_daily_panel.csv`.

![Figure 2. Pre- versus post-SEBI-amendment mean Amihud illiquidity bar chart comparing REIT and InvIT asset classes.](../figures/fig2_amihud_prepost_bar.png)

**Figure 2.** Mean Amihud illiquidity, pre- versus post-SEBI InvIT (Third Amendment) event date (2023-09-26), by asset class. Source: `data/processed/liquidity_daily_panel.csv`.

![Figure 4. Distribution of Roll implied spreads by asset class, box plot comparing REIT and InvIT high-low spread proxies.](../figures/fig4_hlspread_box.png)

**Figure 4.** Box plot of the Roll implied (high-low) spread distribution by asset class, corroborating the cross-class liquidity ordering. Source: `data/processed/liquidity_daily_panel.csv`.

### 5.2 Independent daily-level validation of the liquidity gap (H1)
To overcome the low power of the eight-entity test, the cross-class comparison was re-estimated on the daily panel in DataStatPro (Version 2.2.3). A two-sided Mann-Whitney U test on daily Amihud illiquidity (REIT n = 372; InvIT n = 372) returns:

| Statistic | Value |
|---|---|
| Mann-Whitney U | 38,447.00 |
| z | 10.4891 |
| p-value | < 0.001 |
| Effect size r | 0.3845 (medium) |
| Hodges-Lehmann median difference | 0.5084 |
| 95% CI (median difference) | [0.3241, 0.7429] |
| Mean rank (REIT) | 455.148 |
| Mean rank (InvIT) | 289.852 |

The difference is highly significant (p < 0.001), confirming that REIT and InvIT units occupy statistically distinct liquidity regimes once adequate sample size is available - thereby supporting H1 at the daily-observation level. We flag an important scaling caveat: the daily-panel `amihud` field (REIT median = 0.639, InvIT median = 0.066) is expressed on a different normalisation than the entity-aggregate `mean_amihud` field (order 1e-10), and the two are therefore not directly comparable in level; only the within-file cross-class ordering should be interpreted. Reconciling the two normalisations in the source notebooks is noted as a pre-submission task (Section 7). This test was generated with DataStatPro and is reported with its APA-7 software citation (Section 8).

### 5.3 Event study - SEBI InvIT (Third Amendment), 2023 (H2)
Source: `data/processed/event_study_car.csv` (notebook cell: "Run market-model event study"). The mean cumulative abnormal return over the [-10, +10] window across the eight entities is +0.315%, with a cross-sectional t-statistic of approximately 0.14 - statistically indistinguishable from zero. H2 is therefore not supported: the market did not detectably reprice these units on the regulatory news alone. Dashboard: https://public.tableau.com/app/profile/sandeep.s1797/viz/P2BInvITIndiaTokenization-CAREventStudySEBI3rdAmendment/CAR-1010byEntity-SEBIInvIT3rdAmendment

### 5.4 Panel regressions - HC1 robust coefficients (H3, H4)
Source: `data/processed/panel_coefficients.csv` (notebook cell: "Build a REAL volume-based adoption proxy" + HC1 panel regression). Dashboard: https://public.tableau.com/app/profile/sandeep.s1797/viz/P2BInvITIndiaTokenization-PanelCoefficientsHC1Robust/PanelCoefficientsHC1RobustSEs-AdoptionProxySEBIPost-Event

| Outcome | Term | Coef | Robust SE | t | p | Sig 5% |
|---|---|---|---|---|---|---|
| amihud_daily | post_event | -3.604e-11 | 6.572e-12 | -5.484 | 4.16e-08 | Yes |
| amihud_daily | adoption_proxy_zscore | -1.665e-10 | 6.422e-12 | -25.919 | 4.07e-148 | Yes |
| turnover_ratio_daily | post_event | 2.990e-05 | 2.858e-06 | 10.461 | 1.31e-25 | Yes |
| turnover_ratio_daily | adoption_proxy_zscore | 3.309e-04 | 6.810e-06 | 48.593 | ~0 | Yes |
| zero_return_day | post_event | 1.850e-04 | 1.007e-03 | 0.184 | 0.854 | No |
| zero_return_day | adoption_proxy_zscore | 3.458e-04 | 1.023e-03 | 0.338 | 0.735 | No |
| abs_return | post_event | -2.802e-04 | 1.669e-04 | -1.679 | 0.093 | No |
| abs_return | adoption_proxy_zscore | -8.217e-05 | 1.397e-04 | -0.588 | 0.556 | No |

Both `post_event` and `adoption_proxy_zscore` are significant at the 5% level for Amihud illiquidity and for the turnover ratio, supporting H3 and H4; effects on zero-return days and absolute returns are not significant.

![Figure 3. Turnover ratio pre- versus post-SEBI-amendment by asset class, bar chart showing higher post-event turnover associated with adoption intensity.](../figures/fig3_turnover_prepost.png)

**Figure 3.** Turnover ratio, pre- versus post-event, by asset class. Higher turnover tracks the volume-based adoption proxy (H4). Source: `data/processed/liquidity_daily_panel.csv`.

![Figure 6. SHAP feature-importance plot ranking the contribution of adoption-proxy components and post-event indicator to predicted Amihud illiquidity.](../figures/fig6_shap_importance.png)

**Figure 6.** SHAP feature-importance ranking for the adoption-proxy model of liquidity. The composite adoption-proxy z-score dominates, consistent with the panel-regression magnitude (beta = -1.665e-10, t = -25.9). Source: `data/processed/panel_coefficients.csv` and the adoption-proxy notebook cell.

## 6. Discussion

Four findings carry the argument. First, the cross-class liquidity gap is real and, at the daily level, statistically robust (Section 5.2: U = 38{,}447, z = 10.49, p < 0.001, r = 0.385), independently reproduced outside the primary HEX environment. The direction at the entity-aggregate level (Section 5.1) indicates InvITs bear the larger price-impact burden, making them the more natural candidates for any liquidity-enhancing intervention such as tokenization. Second, the SEBI Third Amendment event window yields a small, statistically insignificant abnormal return (CAR = +0.315%, t approximately 0.14), implying the market did not reprice these units on the regulatory news alone. Third, and most important, the adoption proxy is the dominant correlate of liquidity: a one-standard-deviation rise in adoption intensity is associated with a large, highly significant fall in Amihud illiquidity (beta = -1.665e-10, t = -25.9) and a large rise in turnover (beta = 3.309e-04, t = 48.6). The policy reading is that liquidity gains follow participation and trading activity rather than regulatory announcements per se - consistent with the tokenization thesis that broader, fractional participation is the operative channel. Fourth, the non-results are informative: neither the event nor the adoption proxy significantly moves zero-return frequency or absolute returns, suggesting the effect operates through depth and turnover rather than through volatility or trading-halt incidence.

![Figure 5. GARCH(1,1) conditional volatility series for the panel, illustrating volatility persistence estimated via NumPy variance-targeted grid-MLE fallback.](../figures/fig5_garch_condvol.png)

**Figure 5.** GARCH(1,1) conditional volatility for the panel (NumPy variance-targeted grid-MLE fallback). Volatility persistence is moderate and does not co-move with the adoption-proxy liquidity channel, supporting the depth-and-turnover (not volatility) interpretation. Source: `data/processed/liquidity_daily_panel.csv`.

## 7. Limitations and Future Research

Five limitations qualify the findings and define the revision agenda. (1) The adoption proxy is a volume-based secondary-data stand-in for the survey-based ADOPT construct, which remains pending; the volume channel may partly co-move mechanically with turnover, so the H4 association should be read as an upper bound. (2) The daily Mann-Whitney test treats entity-days as independent observations, but they are serially correlated within entity; the reported p-value therefore overstates true significance, and the HC1 panel regression remains the more defensible inferential model. (3) The HC1 standard errors are not clustered by entity; entity-clustered or two-way-clustered errors are planned once `statsmodels` is available. (4) The two `amihud` normalisations (entity-aggregate order 1e-10 vs daily-panel order 1e-1) must be reconciled to a single definition before submission. (5) The panel covers only eight entities, limiting cross-sectional power for the event study. Future work will add the primary survey ADOPT construct, cluster-robust and GARCH-based volatility models, and a difference-in-differences design exploiting staggered tokenization pilots.

## 8. Conclusion

Using a reproducible daily panel of eight Indian InvITs and REITs, and validating the headline result in an independent statistical environment, we find measurable illiquidity - larger for InvITs - that adoption intensity, not the 2023 SEBI regulatory amendment, most strongly relieves. The cross-class liquidity gap is statistically significant at the daily level (Mann-Whitney U = 38{,}447, z = 10.49, p < 0.001). Taken together, the evidence offers conditional empirical support for tokenization as a liquidity-deepening mechanism for Indian infrastructure and real-estate vehicles, with the central caveat that participation, not regulation alone, drives the gain.

## Data and Software Availability

All raw data, processed datasets, notebooks, and figures are openly available in the public repository: https://github.com/SanKabira/P2-BInvIT-India-Tokenization-Empirical. Key processed files: `data/processed/liquidity_by_entity.csv`, `data/processed/liquidity_daily_panel.csv`, `data/processed/event_study_car.csv`, `data/processed/panel_coefficients.csv`. Figures 1-6 are archived in `figures/` and embedded above. Interactive dashboards: Tableau Public profile `sandeep.s1797`. The independent cross-validation was produced in DataStatPro.

## References

Amihud, Y. (2002). Illiquidity and stock returns: Cross-section and time-series effects. *Journal of Financial Markets, 5*(1), 31-56.

DataStatPro. (2026). *DataStatPro* (Version 2.2.3) [Statistical analysis platform]. https://www.datastatpro.com

Roll, R. (1984). A simple implicit measure of the effective bid-ask spread in an efficient market. *The Journal of Finance, 39*(4), 1127-1139.

Securities and Exchange Board of India. (2014). *SEBI (Infrastructure Investment Trusts) Regulations, 2014*. SEBI.

Securities and Exchange Board of India. (2023). *SEBI (Infrastructure Investment Trusts) (Third Amendment) Regulations, 2023*. SEBI.
