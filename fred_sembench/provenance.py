from __future__ import annotations

import csv
import io
import json
from pathlib import Path


FIELDS = (
    "series_id",
    "original_source",
    "series_url",
    "retrieved_on",
    "publication_form",
    "rights_status",
)


# Load newline-delimited records from one release data file.
def _load_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


# Build a per-series source and publication-boundary table.
def build_source_provenance(root: Path) -> str:
    facts = _load_jsonl(root / "data" / "facts.jsonl")
    series: dict[str, dict[str, str]] = {}
    for fact in facts:
        snapshot = fact["snapshot"]
        source = fact["source"]
        series_id = snapshot["series_id"]
        series[series_id] = {
            "series_id": series_id,
            "original_source": source["official_source"],
            "series_url": source["series_url"],
            "retrieved_on": snapshot["retrieved_on"],
            "publication_form": "metadata_and_derived_evidence_only",
            "rights_status": "original_provider_terms_apply",
        }
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(series[key] for key in sorted(series))
    return output.getvalue()
