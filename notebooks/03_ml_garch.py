"""
GATE 2 — P2 Notebook 03: GARCH volatility + ML classification.

PART A (RUNNABLE on real data): GARCH(1,1) on daily returns of each entity to
characterise conditional volatility, and a pre/post comparison of fitted
conditional volatility (a liquidity-risk channel of the SEBI amendment).

PART B (RUNNABLE on real market data): ML classification of liquidity tier
(High vs Low) from daily microstructure features (Amihud, hl_spread, turnover,
zero_ret, abs_ret) using LogisticRegression / RandomForest / XGBoost, with SHAP
feature attribution. This demonstrates the modelling pipeline on REAL data while
the survey-based adoption model remains PENDING field collection.

PART C (PENDING): survey-based adoption logistic regression — pipeline scaffolded,
NOT executed, because no real survey responses have been collected (no fabrication).
"""
import os, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from arch import arch_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.pipeline import Pipeline
import xgboost as xgb
import shap

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROC = os.path.join(BASE, "data", "processed")
FIG = os.path.join(BASE, "figures")
EVENT = pd.Timestamp("2025-09-03")
plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})

panel = pd.read_csv(os.path.join(PROC, "liquidity_daily_panel.csv"), parse_dates=["date"])
ENTITIES = ["INDIGRID", "PGINVIT", "IRBINVIT", "EMBASSY", "MINDSPACE", "BIRET"]

# ============================================================ PART A: GARCH(1,1)
garch_rows = []
fig, axes = plt.subplots(2, 3, figsize=(13, 7), sharex=True)
for ax, e in zip(axes.flat, ENTITIES):
    d = panel[panel.entity == e].sort_values("date").copy()
    d_ret = d.dropna(subset=["ret"]).copy()   # rows that actually have a return
    r = (d_ret["ret"].values) * 100            # percent returns
    if len(r) < 30:
        continue
    am = arch_model(r, mean="Constant", vol="GARCH", p=1, q=1, dist="t")
    res = am.fit(disp="off")
    cond_vol = np.asarray(res.conditional_volatility)
    dates = pd.to_datetime(d_ret["date"].values)  # aligned 1:1 with returns
    cv = pd.Series(cond_vol, index=dates)
    pre_cv = cv[cv.index < EVENT].mean()
    post_cv = cv[cv.index >= EVENT].mean()
    garch_rows.append({
        "entity": e, "type": d["type"].iloc[0],
        "omega": res.params.get("omega", np.nan),
        "alpha1": res.params.get("alpha[1]", np.nan),
        "beta1": res.params.get("beta[1]", np.nan),
        "persistence": res.params.get("alpha[1]", 0) + res.params.get("beta[1]", 0),
        "cond_vol_pre_mean": pre_cv, "cond_vol_post_mean": post_cv,
        "loglik": res.loglikelihood, "aic": res.aic,
    })
    ax.plot(cv.index, cv.values, color="#1f4e79", lw=1.3)
    ax.axvline(EVENT, color="black", ls="--", lw=1)
    ax.set_title(f"{e}")
    ax.tick_params(axis="x", labelsize=8, rotation=30)
fig.suptitle("GARCH(1,1) Conditional Volatility (daily, %) Around SEBI 3rd Amendment",
             fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(FIG, "fig5_garch_condvol.png"), bbox_inches="tight")
plt.close(fig)

garch = pd.DataFrame(garch_rows)
garch.to_csv(os.path.join(PROC, "garch_params.csv"), index=False)
print("=== GARCH(1,1) parameters & pre/post conditional volatility ===")
print(garch.to_string(index=False))

# ============================================================ PART B: ML classification
# Target: liquidity tier (High=1, Low=0) from daily microstructure features.
tiers = pd.read_csv(os.path.join(PROC, "entity_liquidity_tiers.csv"))
tier_map = dict(zip(tiers["entity"], tiers["liq_tier"]))
feat_cols = ["amihud", "hl_spread", "log_rupee_vol", "zero_ret", "abs_ret"]
ml = panel.dropna(subset=feat_cols).copy()
ml["y"] = (ml["entity"].map(tier_map) == "High").astype(int)
X = ml[feat_cols].values
y = ml["y"].values
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)

results = []
# LogReg
logr = Pipeline([("sc", StandardScaler()), ("lr", LogisticRegression(max_iter=1000))])
logr.fit(Xtr, ytr)
results.append(("LogisticRegression", accuracy_score(yte, logr.predict(Xte)),
                roc_auc_score(yte, logr.predict_proba(Xte)[:, 1])))
# RF
rf = RandomForestClassifier(n_estimators=300, random_state=42)
rf.fit(Xtr, ytr)
results.append(("RandomForest", accuracy_score(yte, rf.predict(Xte)),
                roc_auc_score(yte, rf.predict_proba(Xte)[:, 1])))
# XGB
xgbc = xgb.XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.1,
                         eval_metric="logloss", random_state=42)
xgbc.fit(Xtr, ytr)
results.append(("XGBoost", accuracy_score(yte, xgbc.predict(Xte)),
                roc_auc_score(yte, xgbc.predict_proba(Xte)[:, 1])))

ml_res = pd.DataFrame(results, columns=["model", "accuracy", "roc_auc"])
ml_res.to_csv(os.path.join(PROC, "ml_classification_results.csv"), index=False)
print("\n=== ML classification (liquidity tier from microstructure features) ===")
print(ml_res.to_string(index=False))

# SHAP on XGBoost
explainer = shap.TreeExplainer(xgbc)
shap_vals = explainer.shap_values(Xte)
mean_abs = np.abs(shap_vals).mean(axis=0)
shap_df = pd.DataFrame({"feature": feat_cols, "mean_abs_shap": mean_abs}).sort_values(
    "mean_abs_shap", ascending=False)
shap_df.to_csv(os.path.join(PROC, "shap_feature_importance.csv"), index=False)
print("\n=== SHAP mean|value| feature importance (XGBoost) ===")
print(shap_df.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(shap_df["feature"][::-1], shap_df["mean_abs_shap"][::-1], color="#1f4e79")
ax.set_xlabel("Mean |SHAP value|")
ax.set_title("SHAP Feature Importance — Liquidity-Tier Classifier (XGBoost)",
             fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig6_shap_importance.png"), bbox_inches="tight")
plt.close(fig)

# ============================================================ PART C: PENDING survey model
print("\n=== PART C: Survey-based adoption logistic regression ===")
print("STATUS: PENDING — no real survey responses collected. Pipeline scaffolded in")
print("notebooks/04_survey_adoption_PENDING.py; will execute only on real data.")
print("\nAll processed outputs written to", PROC)
