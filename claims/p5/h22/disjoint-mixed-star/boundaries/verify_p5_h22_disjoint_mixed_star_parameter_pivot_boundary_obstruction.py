#!/usr/bin/env python3
"""Verify the parameter-pivot H22 boundaries of component eight."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sys
HERE = Path(__file__).resolve().parent


def _repo_root() -> Path:
    for candidate in (HERE, *HERE.parents):
        if (candidate / ".git").exists():
            return candidate
    return HERE


REPO_ROOT = _repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

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
    HERE / "P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md"
)
COMPONENT = REPO_ROOT / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md"
DIRECTIONS = ("01", "23")

a, b, f, phi, r = sp.symbols("a b f phi r")
BRANCHES = (
    (
        "a_eq_b__bf_eq_minus1",
        {a: b, f: -1 / b},
        ("b", "phi", "r"),
        None,
    ),
    (
        "a_eq_minus_b__bf_eq_minus1",
        {a: -b, f: -1 / b},
        ("b", "phi", "r"),
        None,
    ),
    (
        "a_eq_b__bphi_eq_plus1",
        {a: b, phi: 1 / b},
        ("b", "f", "r"),
        None,
    ),
    (
        "a_eq_b__bphi_eq_minus1",
        {a: b, phi: -1 / b},
        ("b", "f", "r"),
        None,
    ),
    (
        "a_eq_minus_b__bphi_eq_plus1",
        {a: -b, phi: 1 / b},
        ("b", "f", "r"),
        None,
    ),
    (
        "a_eq_minus_b__bphi_eq_minus1",
        {a: -b, phi: -1 / b},
        ("b", "f", "r"),
        None,
    ),
    (
        "b_eq_zero__af_eq_plus1",
        {b: 0, a: 1 / f},
        ("f", "phi", "r"),
        None,
    ),
    (
        "b_eq_zero__af_eq_minus1",
        {b: 0, a: -1 / f},
        ("f", "phi", "r"),
        None,
    ),
    (
        "f_eq_zero__bphi_eq_plus1",
        {f: 0, b: 1 / phi},
        ("a", "phi", "r"),
        None,
    ),
    (
        "f_eq_zero__bphi_eq_minus1",
        {f: 0, b: -1 / phi},
        ("a", "phi", "r"),
        None,
    ),
    (
        "a_eq_zero__quadratic",
        {a: 0},
        ("b", "f", "r"),
        "phi",
    ),
    (
        "phi_eq_zero__quadratic",
        {phi: 0},
        ("b", "f", "r"),
        "a",
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_branch(
    branch: str,
    substitutions: dict[sp.Symbol, sp.Expr],
    parameters: tuple[str, ...],
    algebraic_variable: str | None,
    direction: str,
) -> dict[str, object]:
    model = build_model(direction)
    component_relation = sp.cancel(
        model["component"].subs(substitutions)
    )
    if algebraic_variable is None:
        assert component_relation == 0
    else:
        assert component_relation != 0
    extensions = model["extensions"]
    shifts = model["shifts"]
    w = sp.Symbol("w")
    algebraic = (
        (sp.Symbol(algebraic_variable),)
        if algebraic_variable is not None
        else ()
    )
    variables = extensions + (w,) + algebraic + shifts
    blocks = (
        "(dp(9),dp(1),dp(4))"
        if algebraic_variable is not None
        else "(dp(9),dp(4))"
    )
    lines = [
        "ring R=(0,"
        + ",".join(parameters)
        + "),("
        + ",".join(map(str, variables))
        + f"),{blocks};",
        "option(redSB);",
    ]
    if algebraic_variable is not None:
        lines.append("poly C=" + singular(component_relation) + ";")
    for index, expression in enumerate(model["mixed"]):
        lines.append(
            f"poly g{index}="
            + singular(sp.cancel(expression.subs(substitutions)))
            + ";"
        )
    fitting_rows = (
        (FITTING_0157, (0, 4, 5, 7))
        if branch.startswith("f_eq_zero") and direction == "01"
        else (FITTING_0137, FITTING_0157)
    )
    for index, rows in enumerate(fitting_rows):
        minor = model["marked"].extract(rows, range(4)).subs(
            substitutions
        )
        lines.extend(
            (
                matrix_declaration(f"H{index}", minor),
                f"poly h{index}=det(H{index});",
            )
        )
    lines.extend(
        (
            "poly da="
            + singular(
                sp.cancel(model["diagonal_a"].subs(substitutions))
            )
            + "-1;",
            "poly db=w*("
            + singular(
                sp.cancel(model["diagonal_b"].subs(substitutions))
            )
            + ")-1;",
            "ideal I="
            + ("C," if algebraic_variable is not None else "")
            + ",".join(f"g{index}" for index in range(14))
            + ",da,db,h0,h1;",
            "I=slimgb(I);",
            (
                f'"CODEX_RESULT:{branch}:{direction}:"+'
                'string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        f"parameter boundary {branch} direction {direction}",
        timeout=300,
    )
    expected = f"CODEX_RESULT:{branch}:{direction}:1:1"
    assert markers(output) == [expected], output
    return {
        "branch": branch,
        "direction": direction,
        "coefficient_field_parameters": list(parameters),
        "component_relation_mode": (
            "identically_zero"
            if algebraic_variable is None
            else f"quadratic_in_{algebraic_variable}"
        ),
        "minor_rows": [list(rows) for rows in fitting_rows],
        "normalized_first_diagonal": True,
        "inverted_second_diagonal": True,
        "fitting_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "twelve codimension-one rank-two boundary branches" in theorem_text
    assert "No graph satisfying the prize equation" in theorem_text
    fraction_field = sp.QQ.frac_field(b, f)
    assert sp.Poly(
        sp.expand(
            build_model("01")["component"].subs(a, 0)
        ),
        phi,
        domain=fraction_field,
    ).is_irreducible
    assert sp.Poly(
        sp.expand(
            build_model("01")["component"].subs(phi, 0)
        ),
        a,
        domain=fraction_field,
    ).is_irreducible
    certificates = [
        verify_branch(
            branch,
            substitutions,
            parameters,
            algebraic_variable,
            direction,
        )
        for branch, substitutions, parameters, algebraic_variable in BRANCHES
        for direction in DIRECTIONS
    ]
    result = {
        "statement": (
            "The generic weighted H22 incidence is empty on the twelve "
            "rank-two parameter-pivot branches of component eight."
        ),
        "scope": "generic points of twelve boundary branches over characteristic zero",
        "branches": [
            branch for branch, _subs, _params, _algebraic in BRANCHES
        ],
        "directions": list(DIRECTIONS),
        "unit_ideal_certificates": certificates,
        "rank_one_boundary": [
            "bf=-1,bphi=1",
            "bf=-1,bphi=-1",
        ],
        "proof_boundary": {
            "special_divisors_inside_branches": "open",
            "other_parameter_projective_boundaries": "open",
            "component_exhaustiveness": "open",
            "global_prize_conjecture": "unresolved",
        },
        "sha256": {
            "theorem": sha256(THEOREM),
            "component": sha256(COMPONENT),
        },
        "verified": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_parameter_pivot_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
