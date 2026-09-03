from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CONDITIONS = {
    "llm_only": "results/llm_only",
    "fred_web": "results/fred_web",
    "iris": "results/iris",
}
FORBIDDEN_TEXT = (
    "C:\\Users\\",
    "/Users/",
    '"thread_id"',
    "sourceAuth",
    "auth.json",
    "runtime-home",
)


# Load newline-delimited JSON records from a release artifact.
def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


# Count strict correct scores for one condition and one optional case subset.
def _strict_fraction(
    scores: list[dict[str, Any]],
    case_ids: set[str] | None = None,
) -> str:
    selected = scores
    if case_ids is not None:
        selected = [row for row in scores if row["case_id"] in case_ids]
    correct = sum(bool(row["is_correct"]) for row in selected)
    return f"{correct}/{len(selected)}"


# Recompute the headline paper results from the published score records.
def compute_paper_results(root: Path) -> dict[str, dict[str, str]]:
    supported_rows = load_jsonl(
        root / "preflight" / "iris_supported_questions.jsonl"
    )
    supported_ids = {row["case_id"] for row in supported_rows}
    scores = {
        name: load_jsonl(root / relative / "deterministic_scores.jsonl")
        for name, relative in CONDITIONS.items()
    }
    return {
        "overall": {
            name: _strict_fraction(rows) for name, rows in scores.items()
        },
        "supported": {
            name: _strict_fraction(rows, supported_ids)
            for name, rows in scores.items()
        },
    }


# Find release files containing local paths or authentication-related fields.
def _find_forbidden_text(root: Path) -> list[str]:
    failures: list[str] = []
    skipped_parts = {".git", "__pycache__"}
    for path in root.rglob("*"):
        if not path.is_file() or skipped_parts.intersection(path.parts):
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in FORBIDDEN_TEXT:
            if pattern in body and path.name not in {".gitignore", "release_checks.py"}:
                failures.append(f"{path.relative_to(root)}: {pattern}")
    return failures


# Validate artifact counts, privacy boundaries, and reported paper scores.
def validate_release(root: Path) -> dict[str, int]:
    concepts = json.loads(
        (root / "data" / "concepts.json").read_text(encoding="utf-8")
    )["concepts"]
    facts = load_jsonl(root / "data" / "facts.jsonl")
    questions = load_jsonl(root / "data" / "questions.jsonl")
    snapshots = load_jsonl(root / "data" / "snapshot_manifest.jsonl")
    supported = load_jsonl(root / "preflight" / "iris_supported_questions.jsonl")
    assert len(concepts) == 50
    assert len(facts) == 100
    assert len(questions) == 200
    assert len(snapshots) == 50
    assert len(supported) == 22
    assert not (root / "snapshots").exists()
    for relative in CONDITIONS.values():
        assert len(load_jsonl(root / relative / "responses.jsonl")) == 48
        assert len(load_jsonl(root / relative / "tool_traces.jsonl")) == 48
        assert len(load_jsonl(root / relative / "deterministic_scores.jsonl")) == 48
    expected = {
        "overall": {"llm_only": "4/48", "fred_web": "28/48", "iris": "25/48"},
        "supported": {"llm_only": "4/22", "fred_web": "13/22", "iris": "17/22"},
    }
    assert compute_paper_results(root) == expected
    failures = _find_forbidden_text(root)
    assert not failures, "Forbidden release content:\n" + "\n".join(failures)
    return {
        "concepts": len(concepts),
        "facts": len(facts),
        "questions": len(questions),
        "snapshots": len(snapshots),
        "experiment_cases": 48,
    }


# Run validation as a standalone release preflight command.
def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = validate_release(root)
    print(json.dumps({"status": "PASS", **report}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
