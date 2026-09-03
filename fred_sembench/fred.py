from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "providers.json"


# Load the public provider contract from the repository configuration.
def _load_provider_config() -> dict[str, str]:
    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return payload["fred"]


# Fetch current FRED observations using a user-supplied API credential.
def fetch_observations(series_id: str) -> dict[str, object]:
    config = _load_provider_config()
    api_key = os.environ.get(config["api_key_environment_variable"])
    if not api_key:
        raise RuntimeError(
            f"Set {config['api_key_environment_variable']} before fetching FRED data."
        )
    query = urlencode({
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
    })
    with urlopen(f"{config['observations_endpoint']}?{query}", timeout=30) as response:
        return json.load(response)
