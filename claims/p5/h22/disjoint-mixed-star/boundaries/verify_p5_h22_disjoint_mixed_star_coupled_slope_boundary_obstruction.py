#!/usr/bin/env python3
"""Verify the coupled slope-parameter H22 boundary on component eight."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from verify_p4_disjoint_mixed_star_pure_component import family
from verify_p5_h22_disjoint_mixed_star_component_generic_obstruction import (
    build_model,
    markers,
    matrix_declaration,
    run_singular,
    singular,
    weighted_row,
)
from verify_p5_h22_mixed_orientation_component_generic_obstruction import (
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md"
)
PARAMETER_THEOREM = (
    ROOT
    / "P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md"
)
a, b, f, phi, r = sp.symbols("a b f phi r")
P = a**2 * f + a * b * f + a + b
Q = -a**2 * f + a * b * f + a - b
COUPLED = sp.cancel(-Q / P)
CERTIFICATES = {
    "01": (1, (0, 4, 5, 7)),
    "23": (0, (0, 1, 3, 7)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def marked_map(model, direction: str, mode: int) -> sp.Matrix:
    shifts = model["shifts"]
    extensions = model["extensions"]
    planes = family(a, b, f, phi)
    alpha = tuple(tuple(plane.row(0)) for plane in planes)
    canonical_beta = tuple(tuple(plane.row(1)) for plane in planes)
    beta = tuple(
        tuple(
            sp.expand(
                canonical_beta[index][coordinate]
                + shifts[index] * alpha[index][coordinate]
            )
            for coordinate in range(4)
        )
        for index in range(4)
    )
    alpha_d = tuple(
        weighted_row(
            alpha[index],
            extensions[index],
            direction,
            r,
        )
        for index in range(4)
    )
    beta_d = tuple(
        weighted_row(
            beta[index],
            extensions[4 + index],
            direction,
            r,
        )
        for index in range(4)
    )
    return one_marked_map(mode, alpha_d, beta_d)


def verify_direction(direction: str) -> dict[str, object]:
    model = build_model(direction)
    mode, rows = CERTIFICATES[direction]
    substitutions = {r: COUPLED}
    marked = marked_map(model, direction, mode)
    minor = marked.extract(rows, range(4)).subs(substitutions)
    extensions = model["extensions"]
    shifts = model["shifts"]
    w = sp.Symbol("w")
    variables = extensions + (w, phi) + shifts
    lines = [
        "ring R=(0,a,b,f),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(1),dp(4));",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
    ]
    for index, expression in enumerate(model["mixed"]):
        lines.append(
            f"poly g{index}="
            + singular(sp.cancel(expression.subs(substitutions)))
            + ";"
        )
    lines.extend(
        (
            matrix_declaration("H", minor),
            "poly h=det(H);",
            "poly da="
            + singular(
                sp.cancel(
                    model["diagonal_a"].subs(substitutions)
                )
            )
            + "-1;",
            "poly db=w*("
            + singular(
                sp.cancel(
                    model["diagonal_b"].subs(substitutions)
                )
            )
            + ")-1;",
            "ideal I=C,"
            + ",".join(f"g{index}" for index in range(14))
            + ",da,db,h;",
            "I=slimgb(I);",
            (
                f'"CODEX_RESULT:{direction}:"+'
                'string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        f"coupled slope direction {direction}",
        timeout=600,
    )
    expected = f"CODEX_RESULT:{direction}:1:1"
    assert markers(output) == [expected], output
    return {
        "direction": direction,
        "marked_mode": mode,
        "minor_rows": list(rows),
        "coupled_slope": str(COUPLED),
        "normalized_first_diagonal": True,
        "inverted_second_diagonal": True,
        "fitting_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "principal coupled slope-parameter divisor" in theorem_text
    coefficient = (
        a**2 * f * (r - 1)
        + a * b * f * (r + 1)
        + a * (r + 1)
        + b * (r - 1)
    )
    assert sp.expand(coefficient - (r * P + Q)) == 0
    assert sp.cancel(coefficient.subs(r, COUPLED)) == 0
    assert sp.expand(P + Q - 2 * a * (b * f + 1)) == 0
    assert sp.expand(P - Q - 2 * (a**2 * f + b)) == 0
    certificates = [
        verify_direction(direction) for direction in ("01", "23")
    ]
    result = {
        "statement": (
            "The weighted H22 incidence is empty on the principal "
            "coupled slope-parameter divisor of component eight."
        ),
        "scope": "generic coupled divisor over characteristic zero",
        "slope_numerator": str(-Q),
        "slope_denominator": str(P),
        "denominator_zero_boundary": [
            "bf=-1,a=b",
            "bf=-1,a=-b",
        ],
        "certificates": certificates,
        "proof_boundary": {
            "unextracted_certificate_denominators": "open",
            "deeper_parameter_projective_boundaries": "open",
            "component_exhaustiveness": "open",
            "global_prize_conjecture": "unresolved",
        },
        "sha256": {
            "theorem": sha256(THEOREM),
            "parameter_theorem": sha256(PARAMETER_THEOREM),
        },
        "verified": True,
    }
    output = (
        ROOT
        / "tmp"
        / "p5_h22_disjoint_mixed_star_coupled_slope_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
