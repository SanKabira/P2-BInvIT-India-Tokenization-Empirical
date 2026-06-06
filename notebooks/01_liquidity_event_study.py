"""
GATE 2 — P2 Notebook 01: Liquidity event study around SEBI InvIT 3rd Amendment (3 Sep 2025).

Inputs:  data/raw/Finance_Connector/{ENTITY}_event_2025.csv  (real OHLCV, Finance connector)
Outputs: data/processed/liquidity_daily_panel.csv
         data/processed/liquidity_event_summary.csv
         data/processed/paired_tests.csv
         data/processed/chi_square_access.csv
         figures/*.png (300 DPI)

Statistical design:
  - Paired t-test (and Wilcoxon) on per-entity pre vs post mean liquidity proxies.
  - Daily-level Welch t-test pre vs post pooled within entity (robustness).
  - Chi-square: access/liquidity tier (High vs Low rupee-volume) x period (pre/post)
    using zero-return-day incidence as the access/illiquidity event.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, os.path.dirname(__file__))
from lib_liquidity import (load_ohlcv, compute_proxies, split_event, summarize,
                           roll_spread, ENTITY_META, EVENT_DATE)

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(BASE, "data", "raw", "Finance_Connector")
PROC = os.path.join(BASE, "data", "processed")
FIG = os.path.join(BASE, "figures")
os.makedirs(PROC, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

ENTITIES = ["INDIGRID", "PGINVIT", "IRBINVIT", "EMBASSY", "MINDSPACE", "BIRET"]

plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300, "font.size": 10,
                     "axes.titlesize": 11, "axes.labelsize": 10})

# ---------------------------------------------------------------- load + proxies
panels = {}
summaries = []
for e in ENTITIES:
    df = load_ohlcv(os.path.join(RAW, f"{e}_event_2025.csv"))
    df = compute_proxies(df)
    df["entity"] = e
    df["type"] = ENTITY_META[e]["type"]
    df["exchange"] = ENTITY_META[e]["exchange"]
    df["period"] = np.where(df["date"] >= EVENT_DATE, "post", "pre")
    panels[e] = df
    summaries.append(summarize(df, e))

panel = pd.concat(panels.values(), ignore_index=True)
panel.to_csv(os.path.join(PROC, "liquidity_daily_panel.csv"), index=False)

summ = pd.DataFrame(summaries)
summ.to_csv(os.path.join(PROC, "liquidity_event_summary.csv"), index=False)
print("=== Event summary (per entity) ===")
print(summ[["entity", "n_pre", "n_post", "amihud_pre_mean", "amihud_post_mean",
            "hl_spread_pre_mean", "hl_spread_post_mean",
            "zero_ret_pre_pct", "zero_ret_post_pct"]].to_string(index=False))

# ---------------------------------------------------------------- paired tests (cross-entity)
# Paired across the 6 entities: pre-mean vs post-mean of each proxy.
paired_rows = []
for col in ["amihud", "hl_spread", "rupee_vol", "abs_ret"]:
    pre = summ[f"{col}_pre_mean"].values
    post = summ[f"{col}_post_mean"].values
    t, p_t = stats.ttest_rel(post, pre)
    w, p_w = stats.wilcoxon(post, pre)
    paired_rows.append({
        "proxy": col, "n_pairs": len(pre),
        "pre_mean": np.mean(pre), "post_mean": np.mean(post),
        "mean_change": np.mean(post - pre),
        "t_stat": t, "p_value_ttest": p_t,
        "wilcoxon_stat": w, "p_value_wilcoxon": p_w,
    })
paired = pd.DataFrame(paired_rows)
paired.to_csv(os.path.join(PROC, "paired_tests.csv"), index=False)
print("\n=== Paired tests (post vs pre, n=6 entities) ===")
print(paired.to_string(index=False))

# ---------------------------------------------------------------- daily-level Welch (pooled robustness)
welch_rows = []
for col in ["amihud", "hl_spread"]:
    pre_v = panel.loc[panel.period == "pre", col].dropna()
    post_v = panel.loc[panel.period == "post", col].dropna()
    t, p = stats.ttest_ind(post_v, pre_v, equal_var=False)
    welch_rows.append({"proxy": col, "n_pre": len(pre_v), "n_post": len(post_v),
                       "pre_mean": pre_v.mean(), "post_mean": post_v.mean(),
                       "welch_t": t, "p_value": p})
welch = pd.DataFrame(welch_rows)
welch.to_csv(os.path.join(PROC, "welch_daily_tests.csv"), index=False)
print("\n=== Welch daily-level tests (pooled) ===")
print(welch.to_string(index=False))

# ---------------------------------------------------------------- chi-square: access tier x period
# Tier each entity by median rupee-volume (High vs Low liquidity). Event = zero-return day.
median_rv = panel.groupby("entity")["rupee_vol"].median()
overall_med = median_rv.median()
panel["liq_tier"] = panel["entity"].map(lambda e: "High" if median_rv[e] >= overall_med else "Low")

ct = pd.crosstab([panel["liq_tier"]], [panel["period"], panel["zero_ret"]])
# 2x2: rows = liq tier, cols = whether a zero-return (stale/illiquid) day occurred
tbl = pd.crosstab(panel["liq_tier"], panel["zero_ret"])
chi2, p_chi, dof, exp = stats.chi2_contingency(tbl)
chi_df = pd.DataFrame({
    "test": ["chi_square_liqtier_x_zeroret"],
    "chi2": [chi2], "dof": [dof], "p_value": [p_chi],
    "low_tier_zero_days": [int(tbl.loc["Low", 1]) if 1 in tbl.columns else 0],
    "high_tier_zero_days": [int(tbl.loc["High", 1]) if 1 in tbl.columns else 0],
})
chi_df.to_csv(os.path.join(PROC, "chi_square_access.csv"), index=False)
print("\n=== Chi-square: liquidity tier x zero-return-day incidence ===")
print(tbl)
print(chi_df.to_string(index=False))

# Save tier assignment
median_rv.rename("median_rupee_vol").reset_index().assign(
    liq_tier=lambda d: d["entity"].map(lambda e: "High" if median_rv[e] >= overall_med else "Low")
).to_csv(os.path.join(PROC, "entity_liquidity_tiers.csv"), index=False)

print("\nProcessed files written to", PROC)
