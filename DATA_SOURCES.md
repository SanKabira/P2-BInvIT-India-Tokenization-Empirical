# Data Sources & Provenance Register — P2

This document tracks **every** data source used in this paper. No number enters the analysis without an entry here. Update the Status and Date when data is collected (GATE 1).

## Status Legend
- 🔴 Not collected
- 🟡 Identified, pending download (await user approval per task rules)
- 🟢 Collected and committed / documented

---

## Module 1 — NSE Market Data (Liquidity & Cost)

| # | Variable | Source | Target file | Status | URL logged | Date |
|---|---|---|---|---|---|---|
| 1 | IndiGrid daily close / volume FY24-25 | NSE India | data/raw/NSE/indigrid_daily_fy2425.csv | 🔴 | — | — |
| 2 | Bid-ask spread (intraday/EOD) | NSE India | data/raw/NSE/indigrid_spread.csv | 🔴 | — | — |
| 3 | Other listed InvITs daily price/volume | NSE India | data/raw/NSE/invits_daily_fy2425.csv | 🔴 | — | — |
| 4 | Turnover / traded value | NSE India | data/raw/NSE/invits_turnover.csv | 🔴 | — | — |

## Module 2 — Screener.in Financials (Core Watchlist)

| # | Variable | Source | Target file | Status | URL logged | Date |
|---|---|---|---|---|---|---|
| 5 | InvIT #1 financials | Screener.in | data/raw/Screener/ | 🔴 | — | — |
| 6 | InvIT #2 financials | Screener.in | data/raw/Screener/ | 🔴 | — | — |
| 7 | InvIT #3 financials | Screener.in | data/raw/Screener/ | 🔴 | — | — |
| 8 | InvIT #4 financials | Screener.in | data/raw/Screener/ | 🔴 | — | — |
| 9 | InvIT #5 financials | Screener.in | data/raw/Screener/ | 🔴 | — | — |

*(Exact 5 tickers to be confirmed from the user's Core Watchlist at GATE 1.)*

## Module 3 — SEBI Regulatory Coding

| # | Variable | Source | Target file | Status | URL logged | Date |
|---|---|---|---|---|---|---|
| 10 | InvIT Master Circular provisions (July 2025) | SEBI | data/raw/SEBI/master_circular_2025.pdf | 🔴 | — | — |
| 11 | 3rd Amendment 2025 provisions | SEBI | data/raw/SEBI/invit_3rd_amendment_2025.pdf | 🔴 | — | — |
| 12 | Coded provision matrix | Derived | data/processed/sebi_coded_provisions.csv | 🔴 | — | — |

## Module 4 — Survey (only if used; no invented responses)

| # | Variable | Source | Target file | Status | URL logged | Date |
|---|---|---|---|---|---|---|
| 13 | Sample frame (Zoho Survey_Target_List) | Existing asset | data/raw/survey/sample_frame.csv | 🔴 | — | — |
| 14 | Survey instrument | Existing asset | data/raw/survey/instrument.md | 🔴 | — | — |

---
*Maintainer: Sandeep S (@SanKabira). Last updated: 2026-06-06.*
