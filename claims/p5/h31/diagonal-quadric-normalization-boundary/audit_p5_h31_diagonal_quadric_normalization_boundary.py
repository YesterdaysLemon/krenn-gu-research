#!/usr/bin/env python3
"""Independent DP-permanent audit of the normalization boundary."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from audit_p5_h31_elliptic_middle_coordinate_rank_drop import (
    extension_system,
)
from verify_p5_h31_diagonal_quadric_normalization_boundary import (
    ROOT,
    THEOREM,
    verify_boundary,
)


PRIMARY = (
    ROOT / "verify_p5_h31_diagonal_quadric_normalization_boundary.py"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    result = verify_boundary(extension_system)
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
    assert primary["whole_normalized_affine_slice_marked_fibre_closed"] is True

    output = {
        "audited": True,
        "field": "C",
        "independent_permanent": "subset dynamic programming",
        **result,
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
        / "p5_h31_diagonal_quadric_normalization_boundary_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
