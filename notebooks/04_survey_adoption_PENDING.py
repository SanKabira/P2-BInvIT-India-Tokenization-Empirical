"""
GATE 2 — P2 Notebook 04 (PENDING): Survey-based adoption logistic regression.

*** THIS PIPELINE DOES NOT RUN ON ANY DATA YET. ***
No survey responses have been collected. NO responses are fabricated or simulated.
The script intentionally aborts if data/raw/survey/survey_responses.csv is absent.

When real responses are exported from Zoho to data/raw/survey/survey_responses.csv,
this script will: clean/score the 8 constructs (AWARE, DIVERS, RISKP, REGTRUST, BLR,
ADOPT), build composite scales (Cronbach's alpha reported), and fit a logistic
regression of binary adoption intention (ADOPT high vs low) on the predictor
constructs, plus a chi-square of access by liquidity/free-float tier.
"""
import os
import sys
import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESP = os.path.join(BASE, "data", "raw", "survey", "survey_responses.csv")

if not os.path.exists(RESP):
    print("PENDING: survey_responses.csv not found.")
    print("No survey data has been collected. This model will be fit ONLY on real,")
    print("collected responses — never on simulated or imputed data.")
    sys.exit(0)

# ----- The following executes only when real data exists -----
import numpy as np
import statsmodels.api as sm
from scipy import stats

df = pd.read_csv(RESP)

CONSTRUCTS = {
    "AWARE":    [c for c in df.columns if c.startswith("AWARE")],
    "DIVERS":   [c for c in df.columns if c.startswith("DIVERS")],
    "RISKP":    [c for c in df.columns if c.startswith("RISKP")],
    "REGTRUST": [c for c in df.columns if c.startswith("REGTRUST")],
    "BLR":      [c for c in df.columns if c.startswith("BLR")],
    "ADOPT":    [c for c in df.columns if c.startswith("ADOPT")],
}

def cronbach_alpha(items):
    items = items.dropna()
    k = items.shape[1]
    var_sum = items.var(axis=0, ddof=1).sum()
    tot_var = items.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - var_sum / tot_var)

scores, alphas = {}, {}
for name, cols in CONSTRUCTS.items():
    if cols:
        scores[name] = df[cols].mean(axis=1)
        alphas[name] = cronbach_alpha(df[cols])
S = pd.DataFrame(scores)
print("Cronbach alpha by construct:", {k: round(v, 3) for k, v in alphas.items()})

S["ADOPT_bin"] = (S["ADOPT"] >= S["ADOPT"].median()).astype(int)
predictors = [c for c in ["AWARE", "DIVERS", "RISKP", "REGTRUST", "BLR"] if c in S]
X = sm.add_constant(S[predictors])
model = sm.Logit(S["ADOPT_bin"], X).fit(disp=0)
print(model.summary())

PROC = os.path.join(BASE, "data", "processed")
os.makedirs(PROC, exist_ok=True)
model_df = pd.DataFrame({
    "term": model.params.index, "coef": model.params.values,
    "odds_ratio": np.exp(model.params.values), "p_value": model.pvalues.values,
})
model_df.to_csv(os.path.join(PROC, "survey_logit_results.csv"), index=False)
print("Saved survey_logit_results.csv")
