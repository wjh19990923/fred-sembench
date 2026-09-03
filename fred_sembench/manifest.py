from __future__ import annotations

import hashlib
import json
from pathlib import Path


EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache"}
EXCLUDED_FILES = {"release_manifest.json"}
PURPOSES = {
    "data": "benchmark data and source provenance",
    "docs": "evaluation and reproducibility documentation",
    "fred_sembench": "public command-line implementation",
    "paper": "camera-ready paper",
    "preflight": "pre-registered Iris coverage decisions",
    "prompts": "experiment instructions",
    "reference_scoring": "frozen experiment scoring programs",
    "results": "recorded responses, scores, traces, and run metadata",
    "scripts": "standalone validation and reproduction entry points",
    "tests": "release verification tests",
}


# Compute the SHA-256 digest for one release file.
def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


# Describe the role of a file using its top-level release directory.
def _purpose(relative_path: Path) -> str:
    if len(relative_path.parts) > 1:
        return PURPOSES.get(relative_path.parts[0], "release metadata")
    return "release metadata and entry-point documentation"


# Enumerate release files while excluding runtime and self-referential output.
def _release_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and not EXCLUDED_PARTS.intersection(path.parts)
        and path.name not in EXCLUDED_FILES
        and path.suffix != ".pyc"
    )


# Build the deterministic machine-readable release manifest.
def build_release_manifest(root: Path) -> str:
    files = []
    for path in _release_files(root):
        relative = path.relative_to(root)
        files.append({
            "path": relative.as_posix(),
            "sha256": _sha256(path),
            "size_bytes": path.stat().st_size,
            "purpose": _purpose(relative),
        })
    payload = {
        "schema_version": "1.0.0",
        "release": "v1.0.0-paper",
        "file_count": len(files),
        "files": files,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
