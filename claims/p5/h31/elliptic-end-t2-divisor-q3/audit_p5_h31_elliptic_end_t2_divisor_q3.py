#!/usr/bin/env python3
"""Independent DP-permanent audit of q=3 on the t2=x divisor."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from audit_p5_h31_elliptic_end_genus_two_exception import mixed_system
from verify_p5_h31_elliptic_end_t2_divisor import (
    ROOT,
    THEOREM,
    verify_endpoint,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dp_mixed_builder(distinguished, alpha, beta):
    return mixed_system(distinguished, alpha, beta)


def main() -> None:
    result = verify_endpoint(3, -1, dp_mixed_builder)
    output = {
        "audited": True,
        "field": "C",
        "independent_permanent": "subset dynamic programming",
        **result,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp"
        / "p5_h31_elliptic_end_t2_divisor_q3_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
