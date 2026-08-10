#!/usr/bin/env python3
"""Independent DP-permanent audit of q=3 on the t3=1 divisor."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from audit_p5_h31_elliptic_end_t3_divisor import dp_system_builder
from verify_p5_h31_elliptic_end_t3_divisor import (
    ROOT,
    THEOREM,
    verify_endpoint,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    result = verify_endpoint(3, -1, dp_system_builder)
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
        / "p5_h31_elliptic_end_t3_divisor_q3_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
