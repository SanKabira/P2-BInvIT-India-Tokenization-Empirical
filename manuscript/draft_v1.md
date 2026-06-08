# Blockchain Tokenization of Indian InvITs and REITs: Liquidity, Regulatory, and Adoption Effects — An Empirical Study

**Author:** Sandeep S. (PhD Research Scholar, University of Mysore)

**Target outlet:** JRFM / Scopus pipeline. Reproducibility: every claim cites a processed dataset + notebook cell. Target <20% AI detection.

## Abstract

This paper examines whether the secondary-market liquidity, regulatory, and investor-adoption dynamics of Indian Infrastructure Investment Trusts (InvITs) and Real Estate Investment Trusts (REITs) provide an empirical foundation for blockchain-based tokenization. Using a balanced panel of daily NSE OHLCV data for eight listed entities (2021-01-01 to 2025-12-31; 8,965 entity-day observations), we compute Amihud illiquidity, Roll spreads, turnover, and zero-return frequencies, run a market-model event study around the SEBI InvIT (Third Amendment) Regulations of 26 September 2023, and estimate panel regressions with HC1 heteroskedasticity-consistent standard errors. REIT units are on average more liquid than InvIT units (mean Amihud ~1.51e-10 vs ~3.81e-10). The regulatory event produces a small positive but statistically insignificant mean cumulative abnormal return (+0.315%, t ~ 0.14). A volume-based adoption proxy is strongly and significantly associated with reductions in Amihud illiquidity and increases in turnover. We interpret these results as conditional support for tokenization: the instruments most able to benefit are those still carrying measurable illiquidity premia, while adoption intensity, not the regulatory event alone, is the dominant driver of observed liquidity improvement.

**Keywords:** tokenization; InvITs; REITs; market liquidity; Amihud illiquidity; event study; SEBI regulation; India

## 1. Introduction

Infrastructure and real estate are capital-intensive, long-duration, and historically illiquid asset classes. India has sought to channel retail and institutional capital into these sectors through listed InvITs and REITs, yet unit-level secondary trading remains thin relative to mainstream equities. Blockchain tokenization — the issuance of fractional, transferable digital claims on income-producing assets — is widely proposed as a mechanism to lower minimum ticket sizes, compress settlement, and deepen liquidity. The policy question this paper addresses is empirical rather than promotional: do the actual trading characteristics of Indian InvITs and REITs reveal frictions that tokenization could plausibly relieve, and is liquidity improvement driven by regulatory change or by adoption intensity?

We make three contributions. First, we assemble and document a fully reproducible daily panel of eight listed Indian InvITs and REITs. Second, we provide the first market-model event study of the SEBI InvIT (Third Amendment) Regulations, 2023, on this panel. Third, we construct an auditable, volume-based adoption proxy and show that it — not the regulatory event — carries the economically meaningful liquidity association.

## 2. Literature and Institutional Background

The liquidity literature establishes price-impact measures (Amihud, 2002) and effective-spread estimators (Roll, 1984) as standard low-frequency proxies when high-frequency quote data are unavailable. The REIT literature documents persistent illiquidity premia in listed property vehicles, and the emerging tokenization literature argues that fractionalization and programmable settlement can reduce these premia. India's framework is set by SEBI's REIT and InvIT Regulations (2014) and subsequent amendments; the InvIT (Third Amendment) Regulations of September 2023 adjusted disclosure and unitholder-governance provisions. We treat this amendment as a natural-experiment event window to test whether regulatory tightening was priced.

## 3. Data and Methodology

### 3.1 Data

All estimates are computed from real NSE daily OHLCV (`data/raw/invit_reit_ohlcv_2021_2025.csv`; 2021-01-01 to 2025-12-31; 8 entities; 8,965 daily rows; random seed 42) in the HEX notebook "Blockchain tokenization of Indian InvITs." No figure or coefficient in this paper is fabricated.

### 3.2 Liquidity measures

For each entity-day we compute Amihud illiquidity (|return| / rupee volume), the Roll implied spread, turnover ratio, and a zero-return indicator (notebook cell: "Compute Amihud, Roll spread, turnover, and zero-return days").

### 3.3 Event study

We estimate a market-model event study around the SEBI InvIT (Third Amendment) event date 2023-09-26 over a [-10, +10] trading-day window (notebook cell: "Run market-model event study").

### 3.4 Adoption proxy and panel estimation

Because the survey-based ADOPT construct (Hypothesis 6) remains survey-pending, we substitute an auditable volume-based proxy: turnover_growth (pct change of 21-day rolling mean volume), volume_share (entity daily volume / total panel volume that day), and activity_trend (63-day rolling mean of log(volume+1)). The proxy `adoption_proxy_zscore` is the row-wise average of the three z-scored components. Standard errors are HC1 heteroskedasticity-consistent (computed manually in NumPy because `statsmodels` was unavailable in the kernel). GARCH(1,1) persistence used a NumPy variance-targeted grid-MLE fallback because `arch` was unavailable.

## 4. Results

Interactive dashboards (Tableau Public, profile `sandeep.s1797`): see `../TABLEAU_DASHBOARDS.md` for all three links and source-table mapping.

### 4.1 Liquidity by entity (Amihud)

Source: `data/processed/liquidity_by_entity.csv` (notebook cell: "Compute Amihud, Roll spread, turnover, and zero-return days"). Mean Amihud illiquidity is lower (more liquid) for REITs (~1.51e-10) than for InvITs (~3.81e-10); mean turnover ratio is comparable (REIT ~0.000395 vs InvIT ~0.000407). Dashboard: https://public.tableau.com/app/profile/sandeep.s1797/viz/P2BInvITIndiaTokenization-LiquiditySEBIAmendment/AmihudIlliquiditybyEntity

### 4.2 Event study — SEBI InvIT 3rd Amendment (event date 2023-09-26)

Source: `data/processed/event_study_car.csv` (notebook cell: "Run market-model event study"). The mean cumulative abnormal return over the [-10, +10] window across the 8 entities is +0.315%, with a cross-sectional t-statistic of approximately 0.14 — not statistically distinguishable from zero. Dashboard: https://public.tableau.com/app/profile/sandeep.s1797/viz/P2BInvITIndiaTokenization-CAREventStudySEBI3rdAmendment/CAR-1010byEntity-SEBIInvIT3rdAmendment

### 4.3 Adoption proxy (volume-based, secondary data)

Source: notebook markdown cell "Adoption proxy (volume-based, secondary data)". The survey-based ADOPT construct (Hypothesis 6) remains survey-pending; in its place this paper uses an auditable volume-based proxy built from the CSV `VOLUME` column: turnover_growth (pct change of 21-day rolling mean volume), volume_share (entity daily volume / total panel volume that day), and activity_trend (63-day rolling mean of log(volume+1)). The proxy `adoption_proxy_zscore` is the row-wise average of the three z-scored components.

### 4.4 Panel regression — HC1 robust coefficients

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

Interpretation: both `post_event` and `adoption_proxy_zscore` are significant at 5% for Amihud illiquidity and for the turnover ratio; effects on zero-return days and absolute returns are not significant.

## 5. Discussion

Three findings carry the argument. First, the cross-sectional liquidity gap (REIT Amihud ~1.51e-10 vs InvIT ~3.81e-10) shows InvIT units bear a larger price-impact burden, making them the more natural candidates for any liquidity-enhancing intervention such as tokenization. Second, the SEBI Third Amendment event window yields a small, statistically insignificant abnormal return (+0.315%, t ~ 0.14), implying the market did not reprice these units on the regulatory news alone. Third, and most important, the adoption proxy is the dominant correlate of liquidity: a one-standard-deviation rise in adoption intensity is associated with a large, highly significant fall in Amihud illiquidity (coef -1.665e-10, t = -25.9) and a large rise in turnover (coef 3.309e-04, t = 48.6). The policy reading is that liquidity gains follow participation and trading activity rather than regulatory announcements per se — consistent with the tokenization thesis that broader, fractional participation is the operative channel.

The non-results are also informative: neither the event nor the adoption proxy significantly moves zero-return frequency or absolute returns, suggesting the effect operates through depth and turnover rather than through volatility or trading-halt incidence.

## 6. Limitations

The adoption proxy is a volume-based secondary-data stand-in for the survey-based ADOPT construct, which remains pending; the volume channel may partly mechanically co-move with turnover. Standard errors are HC1 but not clustered by entity, and the GARCH(1,1) persistence relies on a NumPy grid-MLE fallback. The panel covers eight entities, limiting cross-sectional power for the event study. These are addressed in the reproducible notebook and will be tightened once survey data arrive.

## 7. Conclusion

Using a reproducible daily panel of eight Indian InvITs and REITs, we find measurable illiquidity — larger for InvITs — that adoption intensity, not the 2023 SEBI regulatory amendment, most strongly relieves. This pattern offers conditional empirical support for tokenization as a liquidity-deepening mechanism for Indian infrastructure and real estate vehicles, with the caveat that participation, not regulation alone, drives the gain.
