#!/usr/bin/env python3
"""Verify a coefficient-quadratic H22 boundary of component eight."""

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
    FITTING_0137,
    FITTING_0157,
    build_model,
    markers,
    matrix_declaration,
    run_singular,
    singular,
)


THEOREM = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_COEFFICIENT_QUADRATIC_BOUNDARY_OBSTRUCTION.md"
)
COMPONENT = REPO_ROOT / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md"
GENERIC = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
DIRECTIONS = ("01", "23")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_direction(direction: str) -> dict[str, object]:
    model = build_model(direction)
    extensions = model["extensions"]
    shifts = model["shifts"]
    w = sp.Symbol("w")
    variables = (
        extensions
        + (w, sp.Symbol("b"), sp.Symbol("phi"))
        + shifts
    )
    lines = [
        "ring R=(0,a,f,r),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(2),dp(4));",
        "option(redSB);",
        "poly A=a^2*f^2+2*b*f+1;",
        "poly C=" + singular(model["component"]) + ";",
    ]
    for index, expression in enumerate(model["mixed"]):
        lines.append(f"poly g{index}={singular(expression)};")
    fitting_rows = (FITTING_0137, FITTING_0157)
    for index, rows in enumerate(fitting_rows):
        minor = model["marked"].extract(rows, range(4))
        lines.extend(
            (
                matrix_declaration(f"H{index}", minor),
                f"poly h{index}=det(H{index});",
            )
        )
    lines.extend(
        (
            "poly da=" + singular(model["diagonal_a"]) + "-1;",
            "poly db=w*("
            + singular(model["diagonal_b"])
            + ")-1;",
            "ideal I=A,C,"
            + ",".join(
                [
                    *(f"g{index}" for index in range(14)),
                    "da",
                    "db",
                    "h0",
                    "h1",
                ]
            )
            + ";",
            "I=slimgb(I);",
            (
                f'"CODEX_RESULT:{direction}:"'
                '+string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        f"coefficient-quadratic full incidence {direction}",
        timeout=600,
    )
    assert markers(output) == [
        f"CODEX_RESULT:{direction}:1:1"
    ], output
    return {
        "direction": direction,
        "coefficient_field_parameters": ["a", "f", "r"],
        "algebraic_variables": ["b", "phi"],
        "normalization_equations": [
            "a^2 f^2+2bf+1",
            "Phi",
        ],
        "minor_rows": [list(rows) for rows in fitting_rows],
        "normalized_first_diagonal": True,
        "inverted_second_diagonal": True,
        "unsplit_full_fitting_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "exact characteristic-zero theorem" in theorem_text
    assert "new irreducible quadratic branch" in theorem_text
    assert "No graph satisfying the prize equation" in theorem_text

    model = build_model("01")
    a, b, f, phi, _r = model["parameters"]
    normalized_b = -(a**2 * f**2 + 1) / (2 * f)
    quadratic = (
        (a**2 * f**2 + 1) * phi**2
        + f**2 * (a**2 * f**2 - 3)
    )
    assert sp.factor(
        model["component"].subs(b, normalized_b)
        + (a * f - 1)
        * (a * f + 1)
        * quadratic
        / (4 * f**2)
    ) == 0
    fraction_field = sp.QQ.frac_field(a, f)
    assert sp.Poly(
        quadratic,
        phi,
        domain=fraction_field,
    ).is_irreducible
    discriminant = sp.factor(
        sp.discriminant(quadratic, phi)
    )
    assert discriminant == (
        -4
        * f**2
        * (a**2 * f**2 - 3)
        * (a**2 * f**2 + 1)
    )

    certificates = [
        verify_direction(direction) for direction in DIRECTIONS
    ]
    result = {
        "statement": (
            "The generic weighted H22 incidence is empty on the new "
            "coefficient-quadratic branch of component eight."
        ),
        "scope": (
            "generic point of one irreducible quadratic component "
            "boundary over characteristic zero"
        ),
        "normalization": {
            "coefficient_divisor": "a^2 f^2+2bf+1=0",
            "b": "-(a^2 f^2+1)/(2f)",
            "new_quadratic_branch": str(quadratic),
            "quadratic_irreducible_over_C(a,f)": True,
            "quadratic_discriminant": str(discriminant),
        },
        "directions": list(DIRECTIONS),
        "unit_ideal_certificates": certificates,
        "proof_boundary": {
            "special_divisors_inside_branch": "open",
            "other_certificate_factors": "not yet classified",
            "component_exhaustiveness": "open",
            "global_prize_conjecture": "unresolved",
        },
        "sha256": {
            "theorem": sha256(THEOREM),
            "component": sha256(COMPONENT),
            "generic_h22": sha256(GENERIC),
        },
        "verified": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_coefficient_quadratic_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
