# Annotation Guidelines

Every case is currently `machine_generated_pending_domain_review`. A reviewer
must not approve a case solely because its arithmetic passes.

## Review order

1. Read the question without looking at the gold answer.
2. Identify the intended economic concept, series, transform, unit, period, and
   as-of boundary.
3. Open the cited local snapshot and independently reproduce the answer.
4. Check the official FRED series page for unit, frequency, source, and notes.
5. Decide whether the alternative series is a plausible error, rather than an
   arbitrary distractor.
6. Mark the case `accept`, `revise`, or `reject` in `questions_review.csv`.

## Acceptance criteria

- The question has one numeric answer or one clearly defined clarification.
- The period and as-of semantics cannot be silently reinterpreted.
- The gold selects the correct concept and series.
- The transform is deterministic and the requested unit is explicit.
- The answer is reproducible from the frozen snapshot at the stated precision.
- The official source is distinguished from FRED as the available provider.
- The wording is natural and economically useful.
- The case is not merely a date-swapped duplicate.

## Task-specific checks

- `direct_retrieval`: no unrequested transform is applied.
- `concept_series_disambiguation`: the confounder is genuinely plausible.
- `transform_unit`: the direction and rounding of the calculation are correct.
- `point_in_time_vintage`: do not describe current-vintage snapshots as
  historical ALFRED vintages.
- `cross_series_reasoning`: both input transforms and subtraction order are
  explicit; reject economically meaningless comparisons.
- `ambiguous_unsupported`: the gold must not contain a numeric answer.

## Dataset status

Only cases accepted by two independent reviewers and reconciled through
adjudication should be promoted into a release candidate. Automated
recomputation verifies arithmetic and provenance integrity, not domain validity.
