from __future__ import annotations

import argparse
import json
from pathlib import Path

from fred_sembench.fred import fetch_observations
from fred_sembench.manifest import build_release_manifest
from fred_sembench.provenance import build_source_provenance
from scripts.release_checks import compute_paper_results, validate_release


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "release_manifest.json"
PROVENANCE_PATH = ROOT / "data" / "source_provenance.csv"


# Print one JSON payload to standard output.
def _print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


# Validate the complete public artifact and print its inventory.
def _validate() -> int:
    _print_json({"status": "PASS", **validate_release(ROOT)})
    return 0


# Recompute the paper result tables from deterministic score records.
def _reproduce() -> int:
    _print_json(compute_paper_results(ROOT))
    return 0


# Validate metadata-only snapshot hashes without claiming raw-body verification.
def _verify_hashes() -> int:
    rows = [
        json.loads(line)
        for line in (ROOT / "data" / "snapshot_manifest.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    valid = len(rows) == 50 and all(
        len(row["response_sha256"]) == 64 for row in rows
    )
    _print_json({"status": "PASS" if valid else "FAIL", "entries": len(rows)})
    return 0 if valid else 1


# Write or check the deterministic release manifest.
def _manifest(write: bool) -> int:
    expected = build_release_manifest(ROOT)
    if write:
        MANIFEST_PATH.write_text(expected, encoding="utf-8")
        print(f"Wrote {MANIFEST_PATH.name}")
        return 0
    actual = MANIFEST_PATH.read_text(encoding="utf-8")
    if actual != expected:
        print("release_manifest.json is stale")
        return 1
    print("release_manifest.json is current")
    return 0


# Write or check the per-series source provenance table.
def _provenance(write: bool) -> int:
    expected = build_source_provenance(ROOT)
    if write:
        PROVENANCE_PATH.write_text(expected, encoding="utf-8")
        print(f"Wrote {PROVENANCE_PATH.relative_to(ROOT)}")
        return 0
    actual = PROVENANCE_PATH.read_text(encoding="utf-8")
    if actual != expected:
        print("data/source_provenance.csv is stale")
        return 1
    print("data/source_provenance.csv is current")
    return 0


# Download current observations for one series with the user's FRED API key.
def _fetch(series_id: str) -> int:
    _print_json(fetch_observations(series_id))
    return 0


# Build the command-line parser for public release operations.
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fred-sembench")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "score", "verify-hashes", "reproduce-paper"):
        commands.add_parser(name)
    manifest = commands.add_parser("manifest")
    manifest.add_argument("--write", action="store_true")
    provenance = commands.add_parser("provenance")
    provenance.add_argument("--write", action="store_true")
    fetch = commands.add_parser("fetch-fred")
    fetch.add_argument("series_id")
    return parser


# Dispatch a public release command.
def main() -> int:
    args = _build_parser().parse_args()
    if args.command == "validate":
        return _validate()
    if args.command in {"score", "reproduce-paper"}:
        return _reproduce()
    if args.command == "verify-hashes":
        return _verify_hashes()
    if args.command == "manifest":
        return _manifest(args.write)
    if args.command == "provenance":
        return _provenance(args.write)
    return _fetch(args.series_id)
