#!/usr/bin/env python3
"""Verify the af/aphi H22 boundary of component eight."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import (  # noqa: E402
    bootstrap,
    expose_claim_package,
)

REPO_ROOT, HERE = bootstrap(__file__, also=[".."])
# The disjoint-mixed-star P4 component package moved in Stage 3;
# expose it through the shared helper (Stage 4 consolidation of the
# Stage 3 per-importer shims) so the bare-name import below
# resolves.
expose_claim_package(REPO_ROOT, "claims/p4/components/disjoint-mixed-star")

import sympy as sp

from verify_p4_disjoint_mixed_star_pure_component import (  # noqa: E402
    family)
from verify_p5_h22_disjoint_mixed_star_component_generic_obstruction import (
    D23_BASE_ROWS,
    D23_EXTRA_ROWS,
    FITTING_0137,
    FITTING_0157,
    build_model,
    determinant_declarations,
    markers,
    matrix_declaration,
    run_singular,
    singular,
)


THEOREM = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_AF_APHI_BOUNDARY_OBSTRUCTION.md"
)
COMPONENT = (
    REPO_ROOT / "claims" / "p4" / "components" / "disjoint-mixed-star"
    / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md")
GENERIC = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
DIRECTIONS = ("01", "23")

a, b, f, phi, r = sp.symbols("a b f phi r")
BRANCHES = (
    ("af_plus1__aphi_plus1", 1, 1),
    ("af_plus1__aphi_minus1", 1, -1),
    ("af_minus1__aphi_plus1", -1, 1),
    ("af_minus1__aphi_minus1", -1, -1),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def substitutions(f_sign: int, phi_sign: int) -> dict[sp.Symbol, sp.Expr]:
    return {
        f: sp.Rational(f_sign, 1) / a,
        phi: sp.Rational(phi_sign, 1) / a,
    }


def verify_d23_minor_content_ledger() -> dict[str, object]:
    """Factor the parameter contents of the seven selected D23 minors."""
    model = build_model("23")
    lines = [
        "ring R=(0,a,b,f,r),(phi,t0,t1,t2,t3),dp;",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
        *determinant_declarations(
            model["mixed_matrix"],
            D23_BASE_ROWS,
            D23_EXTRA_ROWS,
        ),
        "ideal KC=std(C);",
    ]
    for index in range(7):
        lines.extend(
            (
                f"poly p{index}=reduce(q{index},KC);",
                f"list F{index}=factorize(p{index});",
                f"number c{index}=leadcoef(F{index}[1][1]);",
                f"string n{index}=string(numerator(c{index}));",
                f"string e{index}=string(denominator(c{index}));",
            )
        )
    lines.extend(
        (
            "ring S=0,(a,b,f,r),dp;",
            "poly P=a2f+b;",
            "poly K=-a2f2+b2f2+bf+1;",
            "poly L=a2bf2+2a2f+b;",
        )
    )
    for index in range(7):
        lines.extend(
            (
                f'execute("poly N{index}="+n{index}+";");',
                f'execute("poly E{index}="+e{index}+";");',
            )
        )
    expected_numerators = (
        "-2048*a*(af-1)*(af+1)*K*r*(r+1)^2*(bf+1)^3*(r-1)^4",
        "-2048*a*(af-1)*(af+1)*K*r*(r+1)^2*(bf+1)^4*(r-1)^4",
        "-2048*a*(af-1)*(af+1)*K*r*(r+1)^2*(bf+1)^3*(r-1)^4",
        "2048*a*(af-1)*(af+1)*L*K*r*(r+1)^2*(r-1)^3*(bf+1)^4",
        "-2048*a*(af-1)*(af+1)*L*K*r*(r+1)^2*(r-1)^3*(bf+1)^4",
        "-2048*a*(af-1)*(af+1)*L*K*r*(r+1)^2*(r-1)^3*(bf+1)^4",
        "-2048*a*(af-1)*(af+1)*L*K*r*(r+1)^2*(r-1)^3*(bf+1)^4",
    )
    expected_denominator_powers = (2, 2, 2, 2, 4, 4, 4)
    for index, (numerator, power) in enumerate(
        zip(
            expected_numerators,
            expected_denominator_powers,
            strict=True,
        )
    ):
        lines.append(
            f"int u{index}=((N{index}-({numerator})==0)"
            f"&&(E{index}-P^{power}==0));"
        )
    lines.extend(
        (
            '"CODEX_RESULT:CONTENT:"+'
            + "+".join(
                f"string(u{index})" for index in range(7)
            )
            + ";",
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        "D23 selected-minor parameter contents",
        timeout=300,
    )
    assert markers(output) == ["CODEX_RESULT:CONTENT:1111111"], output
    return {
        "direction": "23",
        "base_rows": list(D23_BASE_ROWS),
        "extra_rows": list(D23_EXTRA_ROWS),
        "common_numerator_factors": [
            "a",
            "af-1",
            "af+1",
            "-a^2 f^2+b^2 f^2+bf+1",
            "r",
            "r+1",
            "r-1",
            "bf+1",
        ],
        "additional_last_four_factor": "a^2 b f^2+2a^2 f+b",
        "denominator_factor": "a^2 f+b",
        "exact_content_identities": True,
    }


def verify_branch(
    branch: str,
    f_sign: int,
    phi_sign: int,
    direction: str,
) -> dict[str, object]:
    model = build_model(direction)
    branch_substitutions = substitutions(f_sign, phi_sign)
    assert sp.cancel(
        model["component"].subs(branch_substitutions)
    ) == 0
    assert all(
        plane.subs(branch_substitutions).rank() == 2
        for plane in family(a, b, f, phi)
    )

    extensions = model["extensions"]
    shifts = model["shifts"]
    w = sp.Symbol("w")
    variables = extensions + (w,) + shifts
    lines = [
        "ring R=(0,a,b,r),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(4));",
        "option(redSB);",
    ]
    for index, expression in enumerate(model["mixed"]):
        lines.append(
            f"poly g{index}="
            + singular(
                sp.cancel(expression.subs(branch_substitutions))
            )
            + ";"
        )
    fitting_names: list[str] = []
    if direction == "01":
        for index, rows in enumerate(
            (FITTING_0137, FITTING_0157)
        ):
            minor = model["marked"].extract(
                rows, range(4)
            ).subs(branch_substitutions)
            lines.extend(
                (
                    matrix_declaration(f"H{index}", minor),
                    f"poly h{index}=det(H{index});",
                )
            )
            fitting_names.append(f"h{index}")
    lines.extend(
        (
            "poly da="
            + singular(
                sp.cancel(
                    model["diagonal_a"].subs(branch_substitutions)
                )
            )
            + "-1;",
            "poly db=w*("
            + singular(
                sp.cancel(
                    model["diagonal_b"].subs(branch_substitutions)
                )
            )
            + ")-1;",
            "ideal I="
            + ",".join(
                [
                    *(f"g{index}" for index in range(14)),
                    "da",
                    "db",
                    *fitting_names,
                ]
            )
            + ";",
            "I=slimgb(I);",
            (
                f'"CODEX_RESULT:{branch}:{direction}:"'
                '+string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        f"af/aphi boundary {branch} direction {direction}",
        timeout=300,
    )
    assert markers(output) == [
        f"CODEX_RESULT:{branch}:{direction}:1:1"
    ], output
    return {
        "branch": branch,
        "direction": direction,
        "coefficient_field_parameters": ["a", "b", "r"],
        "component_relation_mode": "identically_zero",
        "local_plane_ranks": [2, 2, 2, 2],
        "normalized_first_diagonal": True,
        "inverted_second_diagonal": True,
        "obstruction": (
            "binary incidence unit ideal"
            if direction == "23"
            else "two-minor Fitting unit ideal"
        ),
        "minor_rows": (
            []
            if direction == "23"
            else [list(FITTING_0137), list(FITTING_0157)]
        ),
        "unit_ideal": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "four rational rank-two branches" in theorem_text
    assert "No graph satisfying the prize equation" in theorem_text

    component = build_model("01")["component"]
    assert sp.factor(a**2 * component.subs(f, 1 / a)) == (
        b * (a + b) * (a * phi - 1) * (a * phi + 1)
    )
    assert sp.factor(a**2 * component.subs(f, -1 / a)) == (
        -b * (a - b) * (a * phi - 1) * (a * phi + 1)
    )
    coefficient_factor = -a**2 * f**2 + b**2 * f**2 + b * f + 1
    assert sp.expand(
        component
        + coefficient_factor
        - b * phi**2 * (a**2 * f + b)
    ) == 0
    assert sp.factor(
        a**4 * component.subs(f, -b / a**2)
    ) == (-(a - b) ** 2 * (a + b) ** 2)

    content_ledger = verify_d23_minor_content_ledger()
    certificates = [
        verify_branch(branch, f_sign, phi_sign, direction)
        for branch, f_sign, phi_sign in BRANCHES
        for direction in DIRECTIONS
    ]
    result = {
        "statement": (
            "The generic weighted H22 incidence is empty on the four "
            "rank-two branches af=+/-1, aphi=+/-1 of component eight."
        ),
        "scope": (
            "generic points of four rational boundary branches over "
            "characteristic zero"
        ),
        "branches": [branch for branch, _f, _phi in BRANCHES],
        "directions": list(DIRECTIONS),
        "d23_minor_content_ledger": content_ledger,
        "unit_ideal_certificates": certificates,
        "proof_boundary": {
            "special_divisors_inside_branches": "open",
            "other_parameter_projective_boundaries": "open",
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
        / "p5_h22_disjoint_mixed_star_af_aphi_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
