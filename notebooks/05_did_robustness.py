"""
P2 — Notebook 05: Scopus-uplift robustness for the SEBI InvIT 3rd Amendment liquidity event-study.

Addresses GAP_AUDIT_P2 P0/P1 items:
  (1) Power: continuous Jan-2024..Dec-2025 daily panel (~496 days/entity) from the
      Perplexity Finance connector (data/raw/Finance_Connector/*_continuous_2024_2025.csv).
  (2) Identification: difference-in-differences with entity + time fixed effects,
      treatment = InvIT x Post; REITs as control group; cluster-robust SEs.
  (3) Inference: entity-block bootstrap CIs for headline effects.
  (4) Placebo event dates + event-window sensitivity grid.
  (5) Liquidity proxy matrix (Amihud, log-Amihud, Corwin-Schultz HL, zero-return ratio,
      turnover ratio, rupee volume).
  (6) GARCH model selection (GARCH(1,1)-t vs EGARCH vs GJR) by AIC/BIC + diagnostics.

INTEGRITY: every observation is real connector OHLCV committed to the repo. No fabrication.
Forecasts/simulations are NONE here — this notebook only analyses observed prices/volumes.

The two-way fixed-effects DiD is estimated by the within (alternating-projections demeaning)
transform rather than dummy expansion: with ~490 date dummies a formula-based OLS is
prohibitively slow, and the within estimator is numerically identical for the single
treatment coefficient. The primary spec is cross-checked against statsmodels dummy-OLS.

Run:  python3 notebooks/05_did_robustness.py
Outputs: data/processed/*.csv  +  figures/*.png  (300 DPI)
"""
import os, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import t as tdist
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
from arch import arch_model

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(BASE, "data", "raw", "Finance_Connector")
PROC = os.path.join(BASE, "data", "processed")
FIG = os.path.join(BASE, "figures")
os.makedirs(PROC, exist_ok=True); os.makedirs(FIG, exist_ok=True)

EVENT_DATE = pd.Timestamp("2025-09-03")  # SEBI InvIT (3rd Amendment) Regulations 2025 notified
ENTITY_META = {
    "INDIGRID": "InvIT", "PGINVIT": "InvIT", "IRBINVIT": "InvIT",
    "EMBASSY": "REIT", "MINDSPACE": "REIT", "BIRET": "REIT",
}
ENTITIES = list(ENTITY_META)
RNG = np.random.default_rng(42)

plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})

# ---------------------------------------------------------------- build continuous panel
def corwin_schultz(df):
    """Corwin & Schultz (2012) high-low bid-ask spread estimator (2-day)."""
    hi = df["high"].values; lo = df["low"].values
    n = len(df); out = np.full(n, np.nan)
    with np.errstate(all="ignore"):
        for t in range(1, n):
            h2 = max(hi[t], hi[t-1]); l2 = min(lo[t], lo[t-1])
            if lo[t] <= 0 or lo[t-1] <= 0 or l2 <= 0:
                continue
            beta = (np.log(hi[t]/lo[t]))**2 + (np.log(hi[t-1]/lo[t-1]))**2
            gamma = (np.log(h2/l2))**2
            denom = 3 - 2*np.sqrt(2)
            alpha = (np.sqrt(2*beta) - np.sqrt(beta))/denom - np.sqrt(gamma/denom)
            s = 2*(np.exp(alpha) - 1)/(1 + np.exp(alpha))
            out[t] = s if s > 0 else 0.0  # CS sets negative spreads to 0
    return out

def load_continuous(e):
    fp = os.path.join(RAW, f"{e}_continuous_2024_2025.csv")
    df = pd.read_csv(fp, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    df = df.dropna(subset=["close", "volume"])
    df = df[df["volume"] > 0].copy()
    df["ret"] = df["close"].pct_change()
    df["abs_ret"] = df["ret"].abs()
    df["rupee_vol"] = df["close"] * df["volume"]
    # Amihud (2002), scaled per billion-rupee turnover for readability
    df["amihud"] = df["abs_ret"] / df["rupee_vol"] * 1e9
    df["log_amihud"] = np.log1p(df["amihud"])
    # Corwin-Schultz (2012) two-day high-low spread estimator
    df["cs_spread"] = corwin_schultz(df)
    # simple high-low relative spread
    df["hl_spread"] = (df["high"] - df["low"]) / ((df["high"] + df["low"]) / 2.0)
    df["zero_ret"] = (df["abs_ret"] < 1e-9).astype(int)
    df["turnover"] = df["volume"]  # share turnover proxy
    df["log_rupee_vol"] = np.log(df["rupee_vol"])
    df["entity"] = e
    df["type"] = ENTITY_META[e]
    df["invit"] = int(ENTITY_META[e] == "InvIT")
    df["post"] = (df["date"] >= EVENT_DATE).astype(int)
    return df

panels = {e: load_continuous(e) for e in ENTITIES}
panel = pd.concat(panels.values(), ignore_index=True)
panel = panel.dropna(subset=["ret"]).reset_index(drop=True)
panel["date_str"] = panel["date"].dt.strftime("%Y%m%d")
panel.to_csv(os.path.join(PROC, "liquidity_daily_panel_continuous.csv"), index=False)
print(f"Continuous panel: {len(panel)} entity-days, "
      f"{panel['date'].min().date()}..{panel['date'].max().date()}")
print(panel.groupby(["type","post"]).size().rename("n_days"))

PROXIES = ["amihud", "log_amihud", "cs_spread", "hl_spread", "zero_ret",
           "turnover", "rupee_vol"]

# ---------------------------------------------------------------- (5) proxy matrix: pre/post by group
rows = []
for col in PROXIES:
    for grp, gdf in panel.groupby("type"):
        pre = gdf.loc[gdf.post == 0, col].dropna()
        post = gdf.loc[gdf.post == 1, col].dropna()
        t, p = stats.ttest_ind(post, pre, equal_var=False)
        rows.append({"proxy": col, "group": grp,
                     "pre_mean": pre.mean(), "post_mean": post.mean(),
                     "pct_change": (post.mean()-pre.mean())/abs(pre.mean())*100 if pre.mean() else np.nan,
                     "welch_t": t, "p_value": p, "n_pre": len(pre), "n_post": len(post)})
proxy_matrix = pd.DataFrame(rows)
proxy_matrix.to_csv(os.path.join(PROC, "liquidity_proxy_matrix.csv"), index=False)
print("\n=== Liquidity proxy matrix (pre/post by group) ===")
print(proxy_matrix.to_string(index=False))

# ---------------------------------------------------------------- (2) Difference-in-differences (two-way FE within)
def twoway_demean(d, cols, ent_col="entity", time_col="date_str", n_iter=200, tol=1e-12):
    """Iterative (alternating-projections) two-way within transform for entity & time FE."""
    X = d[cols].to_numpy(dtype=float).copy()
    ent = d[ent_col].to_numpy(); tim = d[time_col].to_numpy()
    _, ent_idx = np.unique(ent, return_inverse=True)
    _, tim_idx = np.unique(tim, return_inverse=True)
    n_ent = ent_idx.max() + 1; n_tim = tim_idx.max() + 1
    ent_cnt = np.bincount(ent_idx, minlength=n_ent).astype(float)
    tim_cnt = np.bincount(tim_idx, minlength=n_tim).astype(float)
    prev = None
    for _ in range(n_iter):
        for j in range(X.shape[1]):
            em = np.bincount(ent_idx, weights=X[:, j], minlength=n_ent) / ent_cnt
            X[:, j] -= em[ent_idx]
            tm = np.bincount(tim_idx, weights=X[:, j], minlength=n_tim) / tim_cnt
            X[:, j] -= tm[tim_idx]
        if prev is not None and np.max(np.abs(X - prev)) < tol:
            break
        prev = X.copy()
    return X

def did_within(d, outcome):
    """Two-way FE DiD via within transform; cluster-robust SE by entity."""
    d = d.copy()
    d["treat"] = (d["invit"] * d["post"]).astype(float)
    W = twoway_demean(d, [outcome, "treat"])
    y = W[:, 0]; x = W[:, 1]
    xtx = float(x @ x)
    n = len(d)
    if xtx <= 1e-18:
        return dict(did_coef=np.nan, cluster_se=np.nan, p_value=np.nan,
                    ci_low=np.nan, ci_high=np.nan, n_obs=n)
    beta = float((x @ y) / xtx)
    resid = y - beta * x
    ent = d["entity"].to_numpy(); ents = np.unique(ent)
    G = len(ents)
    k = 1 + d["entity"].nunique() + d["date_str"].nunique()  # absorbed dof
    meat = 0.0
    for e in ents:
        m = ent == e
        sc = float((x[m] * resid[m]).sum())
        meat += sc * sc
    bread = 1.0 / xtx
    dof_adj = (G / (G - 1)) * ((n - 1) / max(n - k, 1))
    var = bread * meat * bread * dof_adj
    se = float(np.sqrt(var)) if var > 0 else np.nan
    dfree = G - 1
    tstat = beta / se if (se and se > 0) else np.nan
    p = float(2 * tdist.sf(abs(tstat), dfree)) if np.isfinite(tstat) else np.nan
    crit = float(tdist.ppf(0.975, dfree))
    return dict(did_coef=beta, cluster_se=se, p_value=p,
                ci_low=beta - crit * se, ci_high=beta + crit * se, n_obs=n)

did_rows = []
for outcome in ["log_amihud", "amihud", "cs_spread", "hl_spread"]:
    d = panel.dropna(subset=[outcome]).copy()
    did_rows.append({"outcome": outcome, **did_within(d, outcome)})
did = pd.DataFrame(did_rows)
did.to_csv(os.path.join(PROC, "did_results.csv"), index=False)
print("\n=== Difference-in-differences (treatment = InvIT x Post; entity+date FE; cluster SE) ===")
print(did.to_string(index=False))

# Cross-check primary spec against statsmodels dummy OLS (exact) for validation.
_chk = panel.dropna(subset=["log_amihud"]).copy()
_chk["treat"] = _chk["invit"] * _chk["post"]
_m = smf.ols("log_amihud ~ treat + C(entity) + C(date_str)", data=_chk).fit(
    cov_type="cluster", cov_kwds={"groups": _chk["entity"]})
print(f"[validation] statsmodels dummy-OLS treat coef={_m.params['treat']:.6f} "
      f"se={_m.bse['treat']:.6f} p={_m.pvalues['treat']:.4f}  | "
      f"within coef={did.loc[did.outcome=='log_amihud','did_coef'].iloc[0]:.6f} "
      f"se={did.loc[did.outcome=='log_amihud','cluster_se'].iloc[0]:.6f}")

# ---------------------------------------------------------------- (3) entity-block bootstrap CIs
def block_bootstrap_did(outcome, n_boot=2000):
    d0 = panel.dropna(subset=[outcome]).copy()
    ents = d0["entity"].unique()
    parts_by_ent = {e: d0[d0.entity == e] for e in ents}
    coefs = []
    for _ in range(n_boot):
        samp_ents = RNG.choice(ents, size=len(ents), replace=True)
        parts = []
        for i, e in enumerate(samp_ents):
            t = parts_by_ent[e].copy()
            t["entity"] = f"{e}_{i}"  # unique label so entity FE works with repeats
            parts.append(t)
        bs = pd.concat(parts, ignore_index=True)
        try:
            coefs.append(did_within(bs, outcome)["did_coef"])
        except Exception:
            continue
    return np.array([c for c in coefs if np.isfinite(c)])

boot_rows = []
for outcome in ["log_amihud", "amihud"]:
    coefs = block_bootstrap_did(outcome, n_boot=2000)
    boot_rows.append({"outcome": outcome, "boot_mean": coefs.mean(),
                      "boot_se": coefs.std(ddof=1),
                      "ci_low_2.5": np.percentile(coefs, 2.5),
                      "ci_high_97.5": np.percentile(coefs, 97.5),
                      "p_two_sided": 2*min((coefs > 0).mean(), (coefs < 0).mean()),
                      "n_boot": len(coefs)})
bootstrap = pd.DataFrame(boot_rows)
bootstrap.to_csv(os.path.join(PROC, "bootstrap_cis.csv"), index=False)
print("\n=== Entity-block bootstrap CIs for DiD coefficient (2000 reps) ===")
print(bootstrap.to_string(index=False))

# ---------------------------------------------------------------- (4) placebo event dates
placebo_dates = pd.to_datetime(["2024-06-03", "2024-09-03", "2024-12-03", "2025-03-03"])
plac_rows = []
pre_only = panel[panel["date"] < EVENT_DATE].copy()  # restrict to pre-reform window
for pdate in placebo_dates:
    d = pre_only.dropna(subset=["log_amihud"]).copy()
    d["post"] = (d["date"] >= pdate).astype(int)
    if d["post"].nunique() < 2:
        continue
    try:
        r = did_within(d, "log_amihud")
        plac_rows.append({"placebo_date": str(pdate.date()), "did_coef": r["did_coef"],
                          "p_value": r["p_value"], "n_obs": r["n_obs"]})
    except Exception:
        plac_rows.append({"placebo_date": str(pdate.date()), "did_coef": np.nan,
                          "p_value": np.nan, "n_obs": 0})
real_coef = did.loc[did.outcome == "log_amihud", "did_coef"].iloc[0]
real_p = did.loc[did.outcome == "log_amihud", "p_value"].iloc[0]
plac_rows.append({"placebo_date": "REAL 2025-09-03", "did_coef": real_coef,
                  "p_value": real_p, "n_obs": int(did.loc[did.outcome=="log_amihud","n_obs"].iloc[0])})
placebo = pd.DataFrame(plac_rows)
placebo.to_csv(os.path.join(PROC, "placebo_tests.csv"), index=False)
print("\n=== Placebo event-date tests (log_amihud DiD) ===")
print(placebo.to_string(index=False))

# ---------------------------------------------------------------- (4) event-window sensitivity
windows = [20, 40, 60, 90, 120]
win_rows = []
for w in windows:
    lo = EVENT_DATE - pd.Timedelta(days=int(w*1.6))  # ~w trading days as calendar days
    hi = EVENT_DATE + pd.Timedelta(days=int(w*1.6))
    d = panel[(panel.date >= lo) & (panel.date <= hi)].dropna(subset=["log_amihud"]).copy()
    if d["post"].nunique() < 2 or d["invit"].nunique() < 2:
        continue
    try:
        r = did_within(d, "log_amihud")
        win_rows.append({"window_trading_days_approx": w, "did_coef": r["did_coef"],
                         "p_value": r["p_value"], "n_obs": r["n_obs"]})
    except Exception:
        continue
ews = pd.DataFrame(win_rows)
ews.to_csv(os.path.join(PROC, "event_window_sensitivity.csv"), index=False)
print("\n=== Event-window sensitivity (log_amihud DiD) ===")
print(ews.to_string(index=False))

# ---------------------------------------------------------------- (6) GARCH model selection
gm_rows = []
for e in ENTITIES:
    r = (panel.loc[panel.entity == e, "ret"].dropna().values) * 100
    if len(r) < 60:
        continue
    specs = {
        "GARCH(1,1)-t": dict(vol="GARCH", p=1, q=1, dist="t"),
        "EGARCH(1,1)-t": dict(vol="EGARCH", p=1, q=1, dist="t"),
        "GJR-GARCH(1,1)-t": dict(vol="GARCH", p=1, o=1, q=1, dist="t"),
    }
    for name, kw in specs.items():
        try:
            res = arch_model(r, mean="Constant", **kw).fit(disp="off")
            std_resid = res.std_resid[~np.isnan(res.std_resid)]
            lb = sm.stats.acorr_ljungbox(std_resid, lags=[10], return_df=True)
            arch_lm = res.arch_lm_test(lags=10)
            persistence = res.params.get("alpha[1]", 0) + res.params.get("beta[1]", 0)
            gm_rows.append({"entity": e, "spec": name, "aic": res.aic, "bic": res.bic,
                            "loglik": res.loglikelihood, "persistence": persistence,
                            "ljungbox_p_lag10": float(lb["lb_pvalue"].iloc[0]),
                            "arch_lm_p": float(arch_lm.pval)})
        except Exception:
            continue
garch_sel = pd.DataFrame(gm_rows)
garch_sel.to_csv(os.path.join(PROC, "garch_model_selection.csv"), index=False)
if not garch_sel.empty:
    winners = garch_sel.loc[garch_sel.groupby("entity")["aic"].idxmin()]
    print("\n=== GARCH model selection — AIC winner per entity ===")
    print(winners[["entity","spec","aic","bic","persistence","ljungbox_p_lag10","arch_lm_p"]].to_string(index=False))

# ============================================================ FIGURES (300 DPI)
# Fig 7 — DiD coefficient plot with cluster CI + bootstrap CI (log_amihud)
fig, ax = plt.subplots(figsize=(7, 4))
row = did[did.outcome == "log_amihud"].iloc[0]
brow = bootstrap[bootstrap.outcome == "log_amihud"].iloc[0]
ax.errorbar([0], [row.did_coef], yerr=[[row.did_coef-row.ci_low],[row.ci_high-row.did_coef]],
            fmt="o", color="#1f4e79", capsize=6, label="Cluster-robust 95% CI", ms=8)
ax.errorbar([0.25], [brow.boot_mean],
            yerr=[[brow.boot_mean-brow["ci_low_2.5"]],[brow["ci_high_97.5"]-brow.boot_mean]],
            fmt="s", color="#c0392b", capsize=6, label="Block-bootstrap 95% CI", ms=8)
ax.axhline(0, color="black", lw=0.8, ls="--")
ax.set_xlim(-0.4, 0.7); ax.set_xticks([])
ax.set_ylabel("DiD coefficient (InvIT x Post) on log-Amihud")
ax.set_title("Reform effect on InvIT illiquidity vs REIT controls\n(negative = liquidity improved)")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig7_did_coefficient.png"), bbox_inches="tight")
plt.close(fig)

# Fig 8 — event-window sensitivity
if not ews.empty:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ews["window_trading_days_approx"], ews["did_coef"], "o-", color="#1f4e79")
    ax.axhline(0, color="black", lw=0.8, ls="--")
    ax.set_xlabel("Approx. half-window (trading days)")
    ax.set_ylabel("DiD coefficient (log-Amihud)")
    ax.set_title("Event-window sensitivity of the reform effect")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig8_event_window_sensitivity.png"), bbox_inches="tight")
    plt.close(fig)

# Fig 9 — placebo vs real
if not placebo.empty:
    fig, ax = plt.subplots(figsize=(7, 4))
    pl = placebo.copy(); pl["lab"] = pl["placebo_date"].astype(str)
    colors = ["#7f8c8d" if "REAL" not in s else "#c0392b" for s in pl["lab"]]
    ax.bar(range(len(pl)), pl["did_coef"], color=colors)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(range(len(pl))); ax.set_xticklabels(pl["lab"], rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("DiD coefficient (log-Amihud)")
    ax.set_title("Placebo pseudo-events (grey) vs real reform (red)")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig9_placebo_tests.png"), bbox_inches="tight")
    plt.close(fig)

# Fig 10 — proxy robustness panel (InvIT pct change by proxy)
fig, ax = plt.subplots(figsize=(8, 4.5))
inv = proxy_matrix[proxy_matrix.group == "InvIT"].set_index("proxy")
order = ["amihud","log_amihud","cs_spread","hl_spread","zero_ret","turnover","rupee_vol"]
vals = [inv.loc[p,"pct_change"] if p in inv.index else np.nan for p in order]
ax.barh(order[::-1], vals[::-1], color="#1f4e79")
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Post vs pre % change (InvIT group)")
ax.set_title("Robustness across liquidity proxies (InvIT group)")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig10_proxy_robustness.png"), bbox_inches="tight")
plt.close(fig)

print("\nAll robustness outputs written to", PROC)
print("Figures:", [f for f in os.listdir(FIG) if f.startswith(("fig7","fig8","fig9","fig10"))])
