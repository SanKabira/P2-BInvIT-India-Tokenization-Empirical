"""
GATE 2 — P2 Notebook 02: Publication figures (300 DPI) from processed liquidity panel.
Reads data/processed/*.csv, writes figures/*.png.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROC = os.path.join(BASE, "data", "processed")
FIG = os.path.join(BASE, "figures")
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300, "font.size": 10,
                     "axes.titlesize": 12, "axes.labelsize": 10, "legend.fontsize": 8,
                     "axes.spines.top": False, "axes.spines.right": False})

panel = pd.read_csv(os.path.join(PROC, "liquidity_daily_panel.csv"), parse_dates=["date"])
summ = pd.read_csv(os.path.join(PROC, "liquidity_event_summary.csv"))
EVENT = pd.Timestamp("2025-09-03")
ENTITIES = ["INDIGRID", "PGINVIT", "IRBINVIT", "EMBASSY", "MINDSPACE", "BIRET"]
COLORS = {"InvIT": "#1f4e79", "REIT": "#c55a11"}

# ---- Fig 1: Amihud illiquidity time series, faceted, with event line
fig, axes = plt.subplots(2, 3, figsize=(13, 7), sharex=True)
for ax, e in zip(axes.flat, ENTITIES):
    d = panel[panel.entity == e].sort_values("date")
    typ = d["type"].iloc[0]
    roll = d["amihud"].rolling(5, min_periods=1).mean()
    ax.plot(d["date"], d["amihud"], color=COLORS[typ], alpha=0.35, lw=0.8)
    ax.plot(d["date"], roll, color=COLORS[typ], lw=1.8, label="5-day MA")
    ax.axvline(EVENT, color="black", ls="--", lw=1)
    ax.set_title(f"{e} ({typ})")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.tick_params(axis="x", labelsize=8)
fig.suptitle("Amihud (2002) Illiquidity Around SEBI InvIT 3rd Amendment (3 Sep 2025)",
             fontweight="bold")
fig.text(0.06, 0.5, "Amihud illiquidity (|r| / ₹-volume ×1e9)", va="center",
         rotation="vertical")
fig.tight_layout(rect=[0.07, 0, 1, 0.96])
fig.savefig(os.path.join(FIG, "fig1_amihud_timeseries.png"), bbox_inches="tight")
plt.close(fig)

# ---- Fig 2: Pre vs Post mean Amihud (grouped bar)
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(summ))
w = 0.38
ax.bar(x - w/2, summ["amihud_pre_mean"], w, label="Pre-event", color="#9dc3e6")
ax.bar(x + w/2, summ["amihud_post_mean"], w, label="Post-event", color="#1f4e79")
ax.set_xticks(x); ax.set_xticklabels(summ["entity"], rotation=20)
ax.set_ylabel("Mean Amihud illiquidity")
ax.set_title("Mean Amihud Illiquidity: Pre vs Post SEBI 3rd Amendment", fontweight="bold")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig2_amihud_prepost_bar.png"), bbox_inches="tight")
plt.close(fig)

# ---- Fig 3: Rupee turnover pre vs post (log scale)
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w/2, summ["rupee_vol_pre_mean"], w, label="Pre-event", color="#ffd28a")
ax.bar(x + w/2, summ["rupee_vol_post_mean"], w, label="Post-event", color="#c55a11")
ax.set_yscale("log")
ax.set_xticks(x); ax.set_xticklabels(summ["entity"], rotation=20)
ax.set_ylabel("Mean daily ₹ turnover (log scale)")
ax.set_title("Daily Rupee Turnover: Pre vs Post SEBI 3rd Amendment", fontweight="bold")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig3_turnover_prepost.png"), bbox_inches="tight")
plt.close(fig)

# ---- Fig 4: High-low spread distribution pre vs post (box by period)
fig, ax = plt.subplots(figsize=(9, 5))
data_pre = [panel[(panel.entity == e) & (panel.period == "pre")]["hl_spread"].dropna()*100 for e in ENTITIES]
data_post = [panel[(panel.entity == e) & (panel.period == "post")]["hl_spread"].dropna()*100 for e in ENTITIES]
positions_pre = np.arange(len(ENTITIES))*2 - 0.35
positions_post = np.arange(len(ENTITIES))*2 + 0.35
bp1 = ax.boxplot(data_pre, positions=positions_pre, widths=0.6, patch_artist=True,
                 boxprops=dict(facecolor="#9dc3e6"), showfliers=False)
bp2 = ax.boxplot(data_post, positions=positions_post, widths=0.6, patch_artist=True,
                 boxprops=dict(facecolor="#1f4e79"), showfliers=False)
ax.set_xticks(np.arange(len(ENTITIES))*2)
ax.set_xticklabels(ENTITIES, rotation=20)
ax.set_ylabel("High-low relative spread (%)")
ax.set_title("Intraday High-Low Spread: Pre vs Post SEBI 3rd Amendment", fontweight="bold")
ax.legend([bp1["boxes"][0], bp2["boxes"][0]], ["Pre-event", "Post-event"])
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig4_hlspread_box.png"), bbox_inches="tight")
plt.close(fig)

print("Figures written:")
for f in sorted(os.listdir(FIG)):
    if f.endswith(".png"):
        print(" ", f, os.path.getsize(os.path.join(FIG, f)), "bytes")
