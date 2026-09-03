# FRED-SemBench V1 Candidate Data Dictionary

## `concepts.json`

- `concept_id`: frozen benchmark identifier from `FRED-C001` to `FRED-C050`.
- `name`: human-readable indicator concept.
- `series_id`: canonical FRED series used by the benchmark.
- `frequency`: reported observation frequency.
- `official_source`: agency responsible for the underlying statistic.
- `unit` / `display_unit`: normalized and human-readable units.
- `precision`: decimal quantization used for gold answers.
- `change_kind`: deterministic rule used to construct the change fact.
- `alternative_series_id`: plausible confounder used in disambiguation cases.

## `facts.jsonl`

Each concept has a `level` fact and a `change` fact.

- `fact_id`: stable fact identifier.
- `benchmark_concept_id`: foreign key to `concepts.json`.
- `series_ids`: required provider series.
- `observation_period` / `observation_dates`: human and ISO representations.
- `as_of`: benchmark snapshot cutoff.
- `vintage_mode`: currently `frozen_current_vintage`.
- `raw_observations`: values used by the deterministic derivation.
- `derivation`: transform name and formula description.
- `answer`: numeric gold, unit, and precision.
- `source`: official source, provider, and series URL.
- `snapshot`: request URL, local file, snapshot ID, and SHA-256.
- `verification`: automatic recomputation status.

## `questions.jsonl`

- `case_id`: stable ID from `fred_sem_0001` to `fred_sem_0200`.
- `primary_concept_id`: concept used for allocation and stratification.
- `task_type`: one of the six frozen task types.
- `fact_ids`: evidence records; empty for clarification cases.
- `gold.answer_mode`: `numeric` or `clarification`.
- `gold`: concept, series, transform, period, answer, provenance, and required response elements.
- `confounders`: alternative series and the expected common error.
- `annotation`: review status and review notes.

## Review files

- `allocation.csv`: one row per concept and one binary column per task type.
- `questions_review.csv`: flattened review view; reviewers complete
  `reviewer_decision` and `reviewer_notes`.
- `QA_REPORT.md`: automated results and unresolved release gates.

## Snapshot semantics

The CSV files reproduce the provider responses downloaded on 2026-07-29. They
are frozen current-vintage evidence, not historical ALFRED vintages. A future
historical-vintage extension must use a distinct benchmark version.
