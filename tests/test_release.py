from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fred_sembench.cli import resolve_artifact_root
from fred_sembench.manifest import build_release_manifest
from scripts.release_checks import compute_paper_results, validate_release


ROOT = Path(__file__).resolve().parents[1]


class ReleaseChecksTest(unittest.TestCase):
    # Verify that the public package contains the complete benchmark metadata.
    def test_release_inventory(self) -> None:
        report = validate_release(ROOT)

        self.assertEqual(report["concepts"], 50)
        self.assertEqual(report["facts"], 100)
        self.assertEqual(report["questions"], 200)
        self.assertEqual(report["snapshots"], 50)
        self.assertEqual(report["experiment_cases"], 48)

    # Verify that the public scores reproduce every headline result in the paper.
    def test_paper_results(self) -> None:
        results = compute_paper_results(ROOT)

        self.assertEqual(results["overall"], {
            "llm_only": "4/48",
            "fred_web": "28/48",
            "iris": "25/48",
        })
        self.assertEqual(results["supported"], {
            "llm_only": "4/22",
            "fred_web": "13/22",
            "iris": "17/22",
        })

    # Verify that the committed manifest matches every tracked release file.
    def test_release_manifest(self) -> None:
        expected = build_release_manifest(ROOT)
        actual = (ROOT / "release_manifest.json").read_text(encoding="utf-8")

        self.assertEqual(actual, expected)

    # Verify that local wheel-build outputs never enter the release manifest.
    def test_release_manifest_excludes_build_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "included.txt").write_text("release", encoding="utf-8")
            (root / "build").mkdir()
            (root / "build" / "wheel.txt").write_text("build", encoding="utf-8")
            (root / "fred_sembench.egg-info").mkdir()
            (root / "fred_sembench.egg-info" / "PKG-INFO").write_text(
                "metadata", encoding="utf-8"
            )

            manifest = build_release_manifest(root)

        self.assertIn("included.txt", manifest)
        self.assertNotIn("wheel.txt", manifest)
        self.assertNotIn("PKG-INFO", manifest)

    # Verify that the public module exposes the documented validation command.
    def test_cli_validate(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "fred_sembench", "validate"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"status": "PASS"', result.stdout)

    # Verify that an installed CLI uses the checked-out artifact in its cwd.
    def test_cli_resolves_checkout_root(self) -> None:
        installed_module = Path("C:/venv/site-packages/fred_sembench/cli.py")

        self.assertEqual(resolve_artifact_root(ROOT, installed_module), ROOT)

    # Verify that publication documentation covers evidence and limitations.
    def test_release_documentation(self) -> None:
        required = (
            "docs/EVALUATION_PROTOCOL.md",
            "docs/IRIS_INTERFACE.md",
            "docs/LIMITATIONS.md",
            "docs/REPRODUCIBILITY_MATRIX.md",
        )

        self.assertTrue(all((ROOT / path).is_file() for path in required))

    # Verify that every source series has an explicit publication boundary.
    def test_source_provenance(self) -> None:
        path = ROOT / "data" / "source_provenance.csv"
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))

        self.assertEqual(len(rows), 50)
        self.assertTrue(all(row["original_source"] for row in rows))
        self.assertTrue(all(
            row["publication_form"] == "metadata_and_derived_evidence_only"
            for row in rows
        ))
        self.assertTrue(all(
            row["rights_status"] == "original_provider_terms_apply"
            for row in rows
        ))

    # Verify that the paper, code, and dataset discovery paths are reciprocal.
    def test_cross_links(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        paper = (ROOT / "PAPER.md").read_text(encoding="utf-8")
        github_url = "https://github.com/wjh19990923/fred-sembench"
        dataset_url = "https://huggingface.co/datasets/wangjinh/FRED-SemBench"

        self.assertIn("PAPER.md", readme)
        self.assertIn(dataset_url, readme)
        self.assertIn(github_url, paper)
        self.assertIn(dataset_url, paper)


if __name__ == "__main__":
    unittest.main()
