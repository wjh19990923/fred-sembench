from __future__ import annotations

import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
