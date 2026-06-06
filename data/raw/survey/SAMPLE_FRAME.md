# Survey Sample Frame & Data-Collection Status

**Study:** Blockchain Tokenization of Indian InvITs — Investor Awareness, Adoption Intention, and Perceived Liquidity/Access Effects
**Instrument source:** `Sandeep_S_PhD_Vault/09_Survey_Zoho/Survey_Instrument.md` (read-only reference, private repo — NOT redistributed)
**Status as of this commit:** Instrument finalized; **field collection PENDING. No responses have been collected or fabricated.**

---

## 1. Target Population

Institutional and sophisticated retail participants in the Indian listed-trust ecosystem (InvITs and, for robustness, REITs), plus intermediaries and advisors who shape allocation decisions. This population is the relevant decision-making universe for adoption of a tokenized-unit structure, because the SEBI InvIT framework historically restricted access to large-ticket investors before the September 2025 amendment lowered the minimum.

## 2. Sampling Approach

Non-probability **purposive + snowball** sampling. The trust ecosystem is small and concentrated; a census-style random frame is not feasible. Prospects are drawn from publicly identifiable roles (investor-relations leads, fund/trust executives, listed advisory-firm professionals, and industry-association contacts).

## 3. Sample Frame Composition (prospect register)

Source file: `Sandeep_S_PhD_Vault/09_Survey_Zoho/Survey_Target_List.csv`.
The register header targets **125 prospects**; **28 named prospects are currently enumerated** (the remainder are to be populated during outreach). Segments:

| Segment | Example organizations (from register) | Rationale |
| --- | --- | --- |
| REIT investor-relations leads | Embassy, Brookfield, Mindspace, Nexus | Closest analogues to InvIT unit-holders; liquidity experience |
| InvIT executives | IndiGrid, IRB InvIT, PowerGrid InvIT | Direct issuer-side adoption decision-makers |
| Real-estate advisory | CBRE, JLL, Knight Frank | Allocation advisors; tokenization-readiness views |
| Industry associations | Bharat InvITs Association | Sector-level policy and adoption signal |
| Global REIT bodies | Nareit, EPRA | Comparative international benchmark on tokenization |

## 4. Target Sample Size & Power

- Target **N ≥ 250** completed responses (per instrument design).
- Rationale: supports the planned **logistic regression** (adoption intention) and **chi-square** (access by liquidity/free-float tier) with adequate cell counts and ≥10 events-per-predictor for the 6-construct model.

## 5. Constructs & Measurement (8 latent constructs, 5-point Likert)

From `Construct_Measurement_Matrix.csv` / `Survey_Instrument.md`:

| Code | Construct |
| --- | --- |
| AWARE | Awareness of tokenization / blockchain in trusts |
| DIVERS | Diversification motive |
| RISKP | Risk perception |
| REGTRUST | Trust in regulator / regulatory clarity |
| BLR | Blockchain reliability / technology trust |
| ADOPT | Adoption intention (primary DV) |

## 6. Hypotheses (H1–H7)

Mapped in `Hypothesis_Data_Mapping.md`. Adoption intention (ADOPT) is modeled as a function of AWARE, DIVERS, RISKP (−), REGTRUST, and BLR, with liquidity/access tier as a moderating/grouping variable for the chi-square test.

## 7. Data-Collection Pipeline (not yet executed)

1. Zoho Survey instrument deployment (setup documented in `Zoho_Setup_Guide.md`).
2. Outreach via `Outreach_Template.md` to the prospect register.
3. Response export → `data/raw/survey/survey_responses.csv` (**file does not yet exist — to be created only from real collected responses**).
4. Cleaning/coding → `data/processed/survey_clean.csv`.

## 8. Data-Availability / Integrity Statement

- **No survey responses have been collected, simulated, or fabricated for this study to date.**
- Any analysis depending on survey data (logistic regression of ADOPT; survey-based chi-square) is marked **PENDING — awaiting field collection** in the notebooks and manuscript.
- The instrument, construct matrix, and target register reside in a **private** repository and are summarized here without redistribution, per the project data-integrity mandate.
