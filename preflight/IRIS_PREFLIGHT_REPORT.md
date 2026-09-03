# Iris Evaluation Subset Preflight Report

## Result

- Benchmark universe: **200**
- Fully supported main-experiment cases: **22**
- Partial/candidate exploratory cases: **3**
- Excluded from Iris accuracy: **175**
- Executable coverage excluding candidate: **11.0%**

The earlier 48-case estimate was a concept/task upper bound. This preflight also
requires exact provider series, deterministic transform, output unit, and every
cross-series input to match the current Iris execution contract.

## Fully supported cases by task

| Task | Count |
|---|---:|
| `ambiguous_unsupported` | 4 |
| `concept_series_disambiguation` | 3 |
| `cross_series_reasoning` | 3 |
| `direct_retrieval` | 3 |
| `point_in_time_vintage` | 3 |
| `transform_unit` | 6 |

## Fully supported cases by benchmark concept

| Benchmark concept | Count |
|---|---:|
| `FRED-C001` | 2 |
| `FRED-C002` | 1 |
| `FRED-C004` | 2 |
| `FRED-C005` | 2 |
| `FRED-C008` | 2 |
| `FRED-C010` | 2 |
| `FRED-C016` | 1 |
| `FRED-C022` | 3 |
| `FRED-C031` | 3 |
| `FRED-C034` | 1 |
| `FRED-C040` | 2 |
| `FRED-C041` | 1 |

## Partial candidate cases

`fred_sem_0081`, `fred_sem_0082`, `fred_sem_0084`

These cases map to `FED_RATE_PATH`, which remains `candidate`. They are excluded
from the main accuracy denominator.

## Primary exclusion reasons

| Reason | Count |
|---|---:|
| `no_concept_mapping` | 144 |
| `transform_mismatch` | 15 |
| `series_mismatch` | 11 |
| `task_not_applicable` | 4 |
| `no_supported_iris_concept` | 1 |

## Important findings

1. Several Iris concepts expose transformed values such as MoM, YoY, or monthly
   change, while the benchmark case requests the raw level.
2. `US_REAL_GDP_QOQ` uses `A191RL1Q225SBEA`, whereas the benchmark Real GDP
   concept uses `GDPC1`.
3. `US_HOUSING_STARTS` scales `HOUST` from thousands to millions, so raw-level
   benchmark units do not match its execution contract.
4. A cross-series case is included only when every referenced fact has an exact
   supported Iris contract.
5. Coverage is not accuracy. Model experiments still need to measure whether
   Iris answers these cases correctly.

## Experimental use

- Main Raw FRED vs Iris experiment:
  `iris_supported_questions.jsonl`
- Exploratory candidate analysis:
  `iris_partial_questions.jsonl`
- Do not treat excluded cases as Iris failures.
