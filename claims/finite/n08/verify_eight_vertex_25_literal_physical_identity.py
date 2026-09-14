"""Replay the exact 25-literal eight-vertex physical-hafnian identity."""

from __future__ import annotations

import argparse
import json
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from krenn_gu.eight_vertex_physical_hafnian_identity import (  # noqa: E402
    analyze_pattern_orbit,
    replay_eight_vertex_physical_hafnian_identity,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pattern",
        type=_BootstrapPath,
        default=REPO_ROOT
        / "tests"
        / "fixtures"
        / "eight_vertex_physical_hafnian_identity_25_literal.json",
    )
    parser.add_argument(
        "--support",
        type=_BootstrapPath,
        help="optionally analyze the allowed orbit against a tracked support fixture",
    )
    args = parser.parse_args()
    payload = json.loads(args.pattern.read_text(encoding="utf-8"))
    result = replay_eight_vertex_physical_hafnian_identity(payload)
    if args.support is not None:
        support = json.loads(args.support.read_text(encoding="utf-8"))
        result["support_orbit_analysis"] = analyze_pattern_orbit(
            payload,
            support.get("nonzero_entry_ids"),
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
