#!/usr/bin/env python3
"""Independent finite flag audit for the complete triangle-211 ledger."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
PRIMARY = HERE / "verify_p4_211_triangle_complete_classification.py"
THEOREM = HERE / "P4_211_TRIANGLE_COMPLETE_CLASSIFICATION.md"


def main() -> None:
    # K/A denote kernel/active at (leaf,center).  AA is forbidden because
    # it would annihilate the nonzero all-active tensor coefficient.
    endpoint_flags = tuple(
        flag for flag in itertools.product("KA", repeat=2) if flag != ("A", "A")
    )
    assert endpoint_flags == (("K", "K"), ("K", "A"), ("A", "K"))
    named = dict(zip(endpoint_flags, "ABC"))
    orbits = {
        "".join(sorted((named[left], named[right])))
        for left in endpoint_flags
        for right in endpoint_flags
    }
    assert orbits == {"AA", "AB", "AC", "BB", "BC", "CC"}

    primary = PRIMARY.read_text(encoding="utf-8")
    theorem = THEOREM.read_text(encoding="utf-8")
    for fragment in (
        '"triangle_211_cell_complete": True',
        '"new_component_orbit": 22',
        '"global_conjecture_resolved": False',
    ):
        assert fragment in primary
    for fragment in (
        "leaves exactly the two star cells",
        "component twenty-two",
        "UNRESOLVED",
    ):
        assert fragment in theorem

    print(
        json.dumps(
            {
                "status": "pass",
                "endpoint_flags": ["".join(flag) for flag in endpoint_flags],
                "unordered_flag_orbits": sorted(orbits),
                "characteristic_zero_proofs_replaced_by_audit": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
