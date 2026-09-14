"""Replay all four finite specializations of the shared-hafnian transfer."""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

bootstrap(__file__)
from krenn_gu.two_slice_transfer import validate_four_patterns  # noqa: E402


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "patterns": validate_four_patterns()}, indent=2))
