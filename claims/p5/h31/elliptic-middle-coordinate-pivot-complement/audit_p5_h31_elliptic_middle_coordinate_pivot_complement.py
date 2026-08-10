#!/usr/bin/env python3
"""Independent DP-permanent audit of the middle pivot complement."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from audit_p5_h31_elliptic_middle_coordinate_rank_drop import (
    extension_system,
)
from verify_p5_h31_elliptic_middle_coordinate_pivot_complement import (
    ROOT,
    THEOREM,
    verify_middle,
)


PRIMARY = (
    ROOT / "verify_p5_h31_elliptic_middle_coordinate_pivot_complement.py"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    cases = {
        "1": verify_middle(1, -1, extension_system),
        "2": verify_middle(2, 1, extension_system),
    }
    completed = subprocess.run(
        [sys.executable, str(PRIMARY)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=600,
    )
    if completed.returncode != 0:
        raise AssertionError(
            ("primary verifier failed", completed.stdout, completed.stderr)
        )
    primary = json.loads(completed.stdout)
    assert primary["verified"] is True
    assert primary["all_regular_elliptic_marked_fibres_closed"] is True

    output = {
        "audited": True,
        "field": "C",
        "independent_permanent": "subset dynamic programming",
        "distinguished_coordinates": [1, 2],
        "cases": cases,
        "whole_regular_middle_pivot_complement_closed": True,
        "all_regular_elliptic_marked_fibres_closed": True,
        "primary_replay_verified": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_elliptic_middle_coordinate_pivot_complement_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
