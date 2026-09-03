from __future__ import annotations

import json
from pathlib import Path

from release_checks import compute_paper_results


# Print the headline paper results from the released deterministic scores.
def main() -> int:
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(compute_paper_results(root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
