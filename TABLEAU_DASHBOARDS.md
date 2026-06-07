# Tableau Public Dashboards — P2: BInvIT India Tokenization

Interactive, publicly accessible dashboards backing the empirical results in this repository.
All figures are computed from real NSE daily OHLCV (2021-01-01 to 2025-12-31, 8 entities, 8,965 daily rows) using HC1 heteroskedasticity-consistent standard errors. GARCH(1,1) persistence was estimated with a NumPy variance-targeted grid-MLE fallback (the `arch` package was unavailable in the execution kernel).

Author profile: https://public.tableau.com/app/profile/sandeep.s1797

## Dashboards

### 1. Liquidity — Amihud Illiquidity by Entity (SEBI Amendment)
https://public.tableau.com/app/profile/sandeep.s1797/viz/P2BInvITIndiaTokenization-LiquiditySEBIAmendment/AmihudIlliquiditybyEntity
Source table: `data/processed/liquidity_by_entity.csv`

### 2. CAR Event Study — [-10, +10] by Entity (SEBI InvIT 3rd Amendment)
https://public.tableau.com/app/profile/sandeep.s1797/viz/P2BInvITIndiaTokenization-CAREventStudySEBI3rdAmendment/CAR-1010byEntity-SEBIInvIT3rdAmendment
Source table: `data/processed/event_study_car.csv`
Event date: 2023-09-26. Mean CAR[-10,+10] across 8 entities = +0.315% (cross-sectional t ~ 0.14; not statistically distinguishable from zero).

### 3. Panel Coefficients (HC1 Robust SEs) — Adoption Proxy & SEBI Post-Event
https://public.tableau.com/app/profile/sandeep.s1797/viz/P2BInvITIndiaTokenization-PanelCoefficientsHC1Robust/PanelCoefficientsHC1RobustSEs-AdoptionProxySEBIPost-Event
Source table: `data/processed/panel_coefficients.csv`

## HC1 Panel Regression — Coefficient Table

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

## Adoption Proxy (volume-based, secondary data)
Built from the CSV `VOLUME` column (no fabrication):
- `turnover_growth` = pct change of 21-day rolling mean VOLUME
- `volume_share` = entity daily VOLUME / total panel VOLUME that day
- `activity_trend` = 63-day rolling mean of log(VOLUME + 1)
- `adoption_proxy_zscore` = row-wise average of the three z-scored components

Notes: `statsmodels` was unavailable in the kernel, so OLS with HC1 robust SEs was implemented manually in NumPy. Random seed = 42.
