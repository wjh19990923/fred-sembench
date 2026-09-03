# Automated QA Report

- Concepts: **50**
- Facts: **100**
- Questions: **200**
- Snapshots with verified SHA-256: **50**
- Questions per concept: **4**
- Task distribution: **{"ambiguous_unsupported": 20, "concept_series_disambiguation": 40, "cross_series_reasoning": 20, "direct_retrieval": 40, "point_in_time_vintage": 40, "transform_unit": 40}**
- Exact normalized duplicate questions: **0**
- Near-duplicate review candidates at token Jaccard ≥ 0.80: **15**
- Numeric facts recomputed successfully: **100**

## Remaining gates

1. Independent domain review of all question wording and economic usefulness.
2. Independent verification of official units and source attribution.
3. ALFRED historical-vintage expansion; current PIT cases use the 2026-07-29 frozen current-vintage snapshot.
4. Copyright and redistribution review before public dataset release.
5. Grouped train/dev/test split after question-family adjudication.

## Near-duplicate candidates

- `fred_sem_0008` ↔ `fred_sem_0048`: 0.80
- `fred_sem_0011` ↔ `fred_sem_0131`: 0.81
- `fred_sem_0020` ↔ `fred_sem_0060`: 0.84
- `fred_sem_0025` ↔ `fred_sem_0105`: 0.83
- `fred_sem_0027` ↔ `fred_sem_0067`: 0.83
- `fred_sem_0027` ↔ `fred_sem_0104`: 0.83
- `fred_sem_0032` ↔ `fred_sem_0072`: 0.83
- `fred_sem_0036` ↔ `fred_sem_0076`: 0.81
- `fred_sem_0039` ↔ `fred_sem_0116`: 0.91
- `fred_sem_0039` ↔ `fred_sem_0159`: 0.91
- `fred_sem_0067` ↔ `fred_sem_0104`: 0.80
- `fred_sem_0071` ↔ `fred_sem_0108`: 0.85
- `fred_sem_0116` ↔ `fred_sem_0159`: 0.91
- `fred_sem_0139` ↔ `fred_sem_0179`: 0.80
- `fred_sem_0147` ↔ `fred_sem_0187`: 0.82
