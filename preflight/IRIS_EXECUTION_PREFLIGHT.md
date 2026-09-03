# Iris Execution Preflight

- Fully supported cases in static manifest: **22**
- Numeric supported cases executed: **18**
- Input contracts executed through Iris `fetch_concept_actuals`: **21**
- Passed input contracts: **21**
- Iris registry version: **2026-06-23**
- Benchmark freeze date: **2026-07-29**

The preflight isolates the exact Iris provider binding required by each
benchmark fact, feeds it the fact's frozen raw observations, and compares the
Iris-produced value and unit with the benchmark gold. Cross-series cases execute
each input contract separately before the benchmark-level arithmetic.

Clarification cases have no numeric input contract; their inclusion is checked
through ontology status and task applicability in the coverage manifest.
