# FRED-SemBench

FRED-SemBench is a 200-question benchmark candidate for evaluating semantic
reliability in LLM access to macroeconomic data. It accompanies the FinNLP 2026
paper **“FRED-SemBench: Evaluating Semantic Reliability in LLM Access to
Macroeconomic Data.”**

The release separates retrieval from semantic correctness: an answer must use
the intended concept, series, transformation, unit, observation period, and
data-vintage interpretation.

> **Candidate status:** the benchmark contains 50 independently selected
> concepts and 200 machine-generated questions. Automated checks are complete,
> while full independent domain adjudication remains future work. The paper's
> primary comparison uses a pre-registered 22-question Iris-supported slice;
> the accompanying diagnostic evaluation contains 48 questions.

## Released artifacts

| Path | Contents |
| --- | --- |
| `data/` | Questions, concepts, derived facts, allocation, data dictionary, and snapshot hashes |
| `prompts/` | Instructions used for LLM-only, FRED+Web, Iris, and judge configurations |
| `results/` | Recorded responses, deterministic scores, run manifests, and credential-free tool traces |
| `preflight/` | Iris coverage decisions created before the Iris evaluation |
| `reference_scoring/` | Scoring programs retained from the paper experiments |
| `scripts/` | Release validation and paper-result reproduction |
| `docs/` | Annotation guidance and benchmark QA report |

Raw FRED CSV snapshots are intentionally not redistributed. The release
includes series identifiers, source URLs, retrieval dates, derived evidence,
and SHA-256 hashes for auditability. See [DATA_LICENSE.md](DATA_LICENSE.md).

## Quick verification

Python 3.10 or newer is sufficient; validation has no third-party dependencies.

```bash
python scripts/release_checks.py
python scripts/reproduce_paper.py
python -m unittest discover -s tests -v
```

Expected headline results:

| Scope | LLM-only | FRED+Web | Iris |
| --- | ---: | ---: | ---: |
| Iris-supported slice | 4/22 | 13/22 | 17/22 |
| 48-question diagnostic slice | 4/48 | 28/48 | 25/48 |

## Data files

- `questions.jsonl`: 200 benchmark questions with explicit semantic gold
  contracts and source attribution.
- `concepts.json`: 50 independently selected macroeconomic concepts.
- `facts.jsonl`: 100 verified, derived fact records used to construct numeric
  answers.
- `snapshot_manifest.jsonl`: retrieval metadata and SHA-256 hashes for 50
  source snapshots; the raw snapshot bodies are not included.
- `questions_review.csv`: flat review view of all questions.

The canonical structured dataset is also published on the Hugging Face Hub.
The Hugging Face link will be added after repository initialization.

## Iris boundary

Iris is a commercial Kairos-AI system. This repository includes the benchmark,
interface-level prompts, recorded responses, deterministic scores, coverage
decisions, and credential-free execution traces used in the paper. It does not
include the proprietary Iris production implementation, credentials, or an
entitlement to the commercial service. The recorded artifacts allow the paper
results to be audited without production access.

## Trace privacy

The public traces contain observable tool identities, allowlisted arguments,
status fields, byte counts, and content hashes. They do not include API keys,
authentication files, cookies, local runtime homes, hidden chain-of-thought, or
the original tool result bodies. Per-run Codex thread identifiers were removed
from response records before publication.

## FRED notice

This product uses the FRED® API but is not endorsed or certified by the Federal
Reserve Bank of St. Louis. FRED series can carry source-specific copyright and
redistribution conditions. Users are responsible for following the FRED terms
and the terms of each original data provider:

- <https://fred.stlouisfed.org/legal/>
- <https://fred.stlouisfed.org/docs/api/terms_of_use.html>

## Citation

Citation metadata is available in [`CITATION.cff`](CITATION.cff). A version DOI
will be added after the paper release is archived.

## Licenses

- Source code: Apache License 2.0; see [`LICENSE`](LICENSE).
- Kairos-AI-authored benchmark structure and annotations: see
  [`DATA_LICENSE.md`](DATA_LICENSE.md).
- Third-party source data and names remain subject to their original terms.

## Contact

Corresponding author: Peter Zhang, Kairos-AI — founders@kairos-ai.io
