"""
Liquidity proxy computation for Indian InvITs/REITs around the
SEBI InvIT (Third Amendment) Regulations 2025 event (notified 3 Sep 2025).

All inputs are real daily OHLCV pulled via the Perplexity Finance connector
and committed under data/raw/Finance_Connector/. NO fabricated data.

Liquidity proxies (all standard, citable):
  - Amihud (2002) illiquidity:  ILLIQ_t = |r_t| / (Close_t * Volume_t)   (rupee volume)
  - Roll (1984) effective spread: 2 * sqrt(-cov(dP_t, dP_{t-1})) when cov<0 else NaN
  - High-low spread (Corwin-Schultz style simple proxy): (High-Low)/((High+Low)/2)
  - Turnover proxy: Volume_t (and rupee turnover = Close*Volume); zero-return-day flag.

Event study: treatment date = 2025-09-03. Pre window = before, Post window = on/after.
"""
import numpy as np
import pandas as pd

EVENT_DATE = pd.Timestamp("2025-09-03")  # SEBI InvIT 3rd Amendment notified

# Entity classification for cross-section (chi-square tier test)
ENTITY_META = {
    "INDIGRID":  {"type": "InvIT", "exchange": "NSE"},
    "PGINVIT":   {"type": "InvIT", "exchange": "NSE"},
    "IRBINVIT":  {"type": "InvIT", "exchange": "NSE"},
    "EMBASSY":   {"type": "REIT",  "exchange": "NSE"},
    "MINDSPACE": {"type": "REIT",  "exchange": "BSE"},
    "BIRET":     {"type": "REIT",  "exchange": "BSE"},
}


def load_ohlcv(path):
    df = pd.read_csv(path, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    df = df.dropna(subset=["close", "volume"])
    df = df[df["volume"] > 0].copy()  # drop non-trading rows for spread/illiq
    return df


def compute_proxies(df):
    """Return df with daily liquidity proxies added."""
    df = df.copy()
    df["ret"] = df["close"].pct_change()
    df["abs_ret"] = df["ret"].abs()
    df["rupee_vol"] = df["close"] * df["volume"]
    # Amihud illiquidity (scaled by 1e6 for readability: *1e6 / rupee_vol)
    df["amihud"] = df["abs_ret"] / df["rupee_vol"] * 1e9  # per billion-rupee turnover
    # High-low relative spread
    df["hl_spread"] = (df["high"] - df["low"]) / ((df["high"] + df["low"]) / 2.0)
    # Zero-return day flag (proxy for stale/illiquid pricing)
    df["zero_ret"] = (df["ret"].abs() < 1e-9).astype(int)
    df["log_rupee_vol"] = np.log(df["rupee_vol"])
    return df


def roll_spread(prices):
    """Roll (1984) implied effective spread from serial covariance of price changes."""
    dp = pd.Series(prices).diff().dropna()
    if len(dp) < 3:
        return np.nan
    cov = np.cov(dp.values[1:], dp.values[:-1])[0, 1]
    if cov < 0:
        return 2.0 * np.sqrt(-cov)
    return np.nan  # positive covariance -> Roll undefined


def split_event(df):
    pre = df[df["date"] < EVENT_DATE].copy()
    post = df[df["date"] >= EVENT_DATE].copy()
    return pre, post


def summarize(df, label):
    pre, post = split_event(df)
    out = {"entity": label, "n_pre": len(pre), "n_post": len(post)}
    for col in ["amihud", "hl_spread", "rupee_vol", "volume", "abs_ret"]:
        out[f"{col}_pre_mean"] = pre[col].mean()
        out[f"{col}_post_mean"] = post[col].mean()
        out[f"{col}_pre_median"] = pre[col].median()
        out[f"{col}_post_median"] = post[col].median()
    out["zero_ret_pre_pct"] = pre["zero_ret"].mean() * 100
    out["zero_ret_post_pct"] = post["zero_ret"].mean() * 100
    out["roll_pre"] = roll_spread(pre["close"].values)
    out["roll_post"] = roll_spread(post["close"].values)
    return out
