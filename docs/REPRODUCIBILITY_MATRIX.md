# Reproducibility matrix

| Paper claim | Public evidence | Verification command |
| --- | --- | --- |
| 50 concepts, 100 facts, 200 questions | `data/` | `fred-sembench validate` |
| 50 snapshot identities and hashes | `data/snapshot_manifest.jsonl` | `fred-sembench verify-hashes` |
| 48 cases in each condition | `results/*/` | `fred-sembench validate` |
| Supported scores: 4/22, 13/22, 17/22 | scores plus `preflight/iris_supported_questions.jsonl` | `fred-sembench reproduce-paper` |
| Diagnostic scores: 4/48, 28/48, 25/48 | `results/*/deterministic_scores.jsonl` | `fred-sembench reproduce-paper` |
| Iris exact-contract coverage | `preflight/` | inspect `IRIS_PREFLIGHT_REPORT.md` |
| Model, dates, run counts, and tool policy | `results/*/run_manifest.json` | inspect the three manifests |
| Prompt and scoring disclosure | `prompts/`, `reference_scoring/` | compare hashes in the run manifests |
| Credential-free observable traces | `results/*/tool_traces.jsonl` | `fred-sembench validate` |
| Release file integrity | `release_manifest.json` | `fred-sembench manifest` |

The release verifies the recorded experiment. It does not claim that current
live FRED responses reproduce the historical byte-frozen source bodies.
