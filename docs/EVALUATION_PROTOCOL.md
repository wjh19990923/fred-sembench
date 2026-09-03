# Evaluation protocol

FRED-SemBench freezes 50 independently selected concepts and 200 questions.
The paper comparison uses the 48 questions associated with the 12 concepts
that overlap Iris at the concept level. Exact-contract preflight retains 22 of
those cases as the primary supported slice.

Every condition uses `gpt-5.6-sol` with medium reasoning and one run per
question. Each question starts in a fresh thread. The LLM-only condition has no
external tools, FRED+Web has live Web search and read-only FRED access, and Iris
has only its read-only semantic interface.

Deterministic scoring requires the expected value at the declared precision,
compatible units, and any required clarification. Equivalent conversions and
paraphrases have not received complete independent adjudication, so scores are
conservative. See each `results/*/run_manifest.json` for execution metadata.
