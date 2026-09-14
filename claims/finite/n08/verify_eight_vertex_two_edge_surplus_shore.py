"""Replay the four degree-six two-edge surplus-shore physical patterns."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)
from krenn_gu.two_edge_surplus_shore import four_patterns, replay  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern", type=Path)
    args = parser.parse_args()
    patterns = [json.loads(args.pattern.read_text())] if args.pattern else four_patterns()
    results = [replay(pattern) for pattern in patterns]
    print(json.dumps({"status": "PASS", "patterns": results}, indent=2))


if __name__ == "__main__":
    main()
