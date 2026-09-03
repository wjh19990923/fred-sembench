# FRED-SemBench v1.0.0-paper

This is the immutable artifact release accompanying the accepted FinNLP 2026
short paper, *FRED-SemBench: Evaluating Semantic Reliability in LLM Access to
Macroeconomic Data*.

## Scope

- 200 benchmark questions covering 50 independently selected FRED concepts.
- A 48-question diagnostic evaluation and the paper's pre-registered
  22-question Iris-supported comparison.
- Recorded results that reproduce the reported headline scores:
  - LLM-only: 4/48 overall and 4/22 on the supported slice.
  - FRED+Web: 28/48 overall and 13/22 on the supported slice.
  - Iris: 25/48 overall and 17/22 on the supported slice.

## Included artifacts

- Benchmark questions, concepts, derived facts, allocation, and data dictionary.
- Prompts, recorded responses, deterministic scores, run manifests, and
  credential-free tool traces.
- Per-series source provenance, retrieval metadata, and snapshot hashes.
- Installable `fred-sembench` validation and reproduction commands.
- Evaluation protocol, Iris interface boundary, limitations, and
  reproducibility matrix.

The structured dataset is also available through the Hugging Face Dataset
Viewer at <https://huggingface.co/datasets/wangjinh/FRED-SemBench>. Paper
metadata and citation guidance are in [`PAPER.md`](PAPER.md) and
[`CITATION.cff`](CITATION.cff).

## Verification

```bash
python -m pip install .
fred-sembench validate
fred-sembench verify-hashes
fred-sembench reproduce-paper
fred-sembench manifest
```

`release_manifest.json` records the SHA-256 digest, size, and purpose of every
released file.

## Publication boundary

Raw FRED CSV snapshots are not redistributed. The original provider terms apply
to each source series. The release does not include the proprietary Iris
production implementation, credentials, authentication material, original tool
result bodies, hidden chain-of-thought, or commercial-service access. See
[`DATA_LICENSE.md`](DATA_LICENSE.md) and [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md).

Zenodo and DOI registration are intentionally deferred and are not part of this
release.
