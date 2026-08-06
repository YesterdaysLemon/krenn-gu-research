#!/usr/bin/env python3
"""Verify the equal/opposite-weight H22 obstruction on component eight."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=[".."])

import sympy as sp

from verify_p5_h22_disjoint_mixed_star_component_generic_obstruction import (
    build_model,
    markers,
    run_singular,
    singular,
)


THEOREM = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md"
)
GENERIC_THEOREM = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
SLOPES = (sp.Integer(1), sp.Integer(-1))
DIRECTIONS = ("01", "23")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_incidence(direction: str, slope: sp.Integer) -> dict[str, object]:
    model = build_model(direction)
    r = model["parameters"][-1]
    extensions = model["extensions"]
    shifts = model["shifts"]
    variables = extensions + (sp.Symbol("phi"),) + shifts
    diagonal_name = "diagonal_a" if slope == 1 else "diagonal_b"
    lines = [
        "ring R=(0,a,b,f),("
        + ",".join(map(str, variables))
        + "),(dp(8),dp(5));",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
    ]
    for index, expression in enumerate(model["mixed"]):
        lines.append(
            f"poly g{index}="
            + singular(expression.subs(r, slope))
            + ";"
        )
    lines.extend(
        (
            "poly d="
            + singular(model[diagonal_name].subs(r, slope))
            + "-1;",
            "ideal I=C,"
            + ",".join(f"g{index}" for index in range(14))
            + ",d;",
            "I=slimgb(I);",
            (
                f'"CODEX_RESULT:{direction}:{int(slope)}:"+'
                'string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        f"slope {int(slope)} direct incidence {direction}",
        timeout=300,
    )
    expected = f"CODEX_RESULT:{direction}:{int(slope)}:1:1"
    assert markers(output) == [expected], output
    return {
        "direction": direction,
        "slope": int(slope),
        "mixed_equations": 14,
        "normalized_diagonal": "first" if slope == 1 else "second",
        "forced_zero_on_mixed_kernel": (
            "first" if slope == 1 else "second"
        ),
        "incidence_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "exact characteristic-zero slope-boundary theorem" in theorem_text
    assert "global Krenn--Gu conjecture" in theorem_text
    certificates = [
        verify_incidence(direction, slope)
        for slope in SLOPES
        for direction in DIRECTIONS
    ]
    result = {
        "statement": (
            "The equal- and opposite-weight binary H22 incidences on "
            "the generic disjoint mixed-star component are empty."
        ),
        "scope": "generic component parameters over characteristic zero",
        "slopes": [int(slope) for slope in SLOPES],
        "directions": list(DIRECTIONS),
        "certificates": certificates,
        "proof_boundary": {
            "other_exceptional_slopes": "open",
            "component_parameter_divisors": "open",
            "projective_marking_boundaries": "open",
            "component_exhaustiveness": "open",
            "global_prize_conjecture": "unresolved",
        },
        "sha256": {
            "theorem": sha256(THEOREM),
            "generic_theorem": sha256(GENERIC_THEOREM),
        },
        "verified": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_equal_opposite_weight_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
