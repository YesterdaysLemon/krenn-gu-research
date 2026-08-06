#!/usr/bin/env python3
"""Verify the zero-slope H22 boundary of component eight."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from verify_p5_h22_disjoint_mixed_star_component_generic_obstruction import (
    D01_BASE_ROWS,
    D01_EXTRA_ROWS,
    D01_PIVOT_COLUMNS,
    FITTING_0137,
    FITTING_0157,
    build_model,
    determinant_declarations,
    markers,
    matrix_declaration,
    run_singular,
    singular,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md"
)
COMPONENT = ROOT / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md"
GENERIC = (
    ROOT
    / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_d01_minor_content_ledger() -> dict[str, object]:
    """Factor the contents of the D01 maximal minors and rank pivot."""
    model = build_model("01")
    pivot = model["mixed_matrix"].extract(
        D01_BASE_ROWS,
        D01_PIVOT_COLUMNS,
    )
    lines = [
        "ring R=(0,a,b,f,r),(phi,t0,t1,t2,t3),dp;",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
        matrix_declaration("PIV", pivot),
        "poly q7=det(PIV);",
        *determinant_declarations(
            model["mixed_matrix"],
            D01_BASE_ROWS,
            D01_EXTRA_ROWS,
        ),
        "ideal KC=std(C);",
    ]
    for index in range(8):
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
            "poly X=afr+af-r+1;",
        )
    )
    for index in range(8):
        lines.extend(
            (
                f'execute("poly N{index}="+n{index}+";");',
                f'execute("poly E{index}="+e{index}+";");',
            )
        )
    expected_numerators = (
        "2048*f*r*a^2*(af-1)^2*(af+1)^2*K^2*(r+1)^2"
        "*(r-1)^3*(bf+1)^6",
        "2048*f*r*X*a^2*(af-1)^2*(af+1)^2*K^2*(r+1)^2"
        "*(r-1)^3*(bf+1)^6",
        "2048*f*r*a^2*(af-1)^2*(af+1)^2*K^2*(r+1)^2"
        "*(r-1)^3*(bf+1)^6",
        "2048*f*K*r*X*a^2*(af-1)^2*(af+1)^2*(r+1)^2"
        "*(r-1)^3*(bf+1)^6",
        "2048*f*K*r*X*a^2*(af-1)^2*(af+1)^2*(r+1)^2"
        "*(r-1)^3*(bf+1)^6",
        "2048*f*(af-1)*(af+1)*K*r*a^2*(r-1)^2*(r+1)^2"
        "*(bf+1)^5",
        "2048*f*K*r*X*a^2*(af-1)^2*(af+1)^2*(r+1)^2"
        "*(r-1)^3*(bf+1)^6",
        "128*(af-1)*(af+1)*K*(r+1)*(r-1)^3*(bf+1)^4",
    )
    expected_denominator_powers = (6, 5, 6, 5, 5, 6, 5, 4)
    for index, (numerator, power) in enumerate(
        zip(
            expected_numerators,
            expected_denominator_powers,
            strict=True,
        )
    ):
        lines.append(
            f"int u{index}=((N{index}-({numerator})==0)"
            f"&&(E{index}-b^3*P^{power}==0));"
        )
    lines.extend(
        (
            '"CODEX_RESULT:CONTENT:"+'
            + "+".join(
                f"string(u{index})" for index in range(8)
            )
            + ";",
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        "D01 selected-minor and pivot parameter contents",
        timeout=300,
    )
    assert markers(output) == [
        "CODEX_RESULT:CONTENT:11111111"
    ], output
    return {
        "direction": "01",
        "maximal_minor_base_rows": list(D01_BASE_ROWS),
        "maximal_minor_extra_rows": list(D01_EXTRA_ROWS),
        "pivot_columns": list(D01_PIVOT_COLUMNS),
        "common_maximal_minor_factors": [
            "a",
            "f",
            "r",
            "af-1",
            "af+1",
            "-a^2 f^2+b^2 f^2+bf+1",
            "r+1",
            "r-1",
            "bf+1",
        ],
        "common_with_rank_pivot": [
            "af-1",
            "af+1",
            "-a^2 f^2+b^2 f^2+bf+1",
            "r+1",
            "r-1",
            "bf+1",
        ],
        "maximal_minor_only_factors": ["a", "f", "r"],
        "some_maximal_minors_only_factor": "afr+af-r+1",
        "denominator_factors": ["b", "a^2 f+b"],
        "exact_content_identities": True,
    }


def verify_d01_zero_slope() -> dict[str, object]:
    model = build_model("01")
    r = model["parameters"][-1]
    extensions = model["extensions"]
    shifts = model["shifts"]
    variables = extensions + (sp.Symbol("phi"),) + shifts
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
            + singular(expression.subs(r, 0))
            + ";"
        )
    lines.extend(
        (
            "poly d="
            + singular(model["diagonal_a"].subs(r, 0))
            + "-1;",
            "ideal I=C,"
            + ",".join(f"g{index}" for index in range(14))
            + ",d;",
            "I=slimgb(I);",
            (
                '"CODEX_RESULT:D01:"'
                '+string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        "D01 zero-slope binary obstruction",
        timeout=300,
    )
    assert markers(output) == ["CODEX_RESULT:D01:1:1"], output
    return {
        "direction": "01",
        "slope": 0,
        "obstruction": "binary incidence",
        "forced_zero_diagonal": "first",
        "incidence_ideal_unit": True,
    }


def verify_d23_zero_slope() -> dict[str, object]:
    model = build_model("23")
    r = model["parameters"][-1]
    extensions = model["extensions"]
    shifts = model["shifts"]
    w = sp.Symbol("w")
    variables = extensions + (w, sp.Symbol("phi")) + shifts
    lines = [
        "ring R=(0,a,b,f),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(5));",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
    ]
    for index, expression in enumerate(model["mixed"]):
        lines.append(
            f"poly g{index}="
            + singular(expression.subs(r, 0))
            + ";"
        )
    for index, rows in enumerate(
        (FITTING_0137, FITTING_0157)
    ):
        minor = model["marked"].extract(
            rows, range(4)
        ).subs(r, 0)
        lines.extend(
            (
                matrix_declaration(f"H{index}", minor),
                f"poly h{index}=det(H{index});",
            )
        )
    lines.extend(
        (
            "poly da="
            + singular(model["diagonal_a"].subs(r, 0))
            + "-1;",
            "poly db=w*("
            + singular(model["diagonal_b"].subs(r, 0))
            + ")-1;",
            "ideal I=C,"
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
                '"CODEX_RESULT:D23:"'
                '+string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        "D23 zero-slope full Fitting obstruction",
        timeout=300,
    )
    assert markers(output) == ["CODEX_RESULT:D23:1:1"], output
    return {
        "direction": "23",
        "slope": 0,
        "obstruction": "unsplit two-minor Fitting incidence",
        "minor_rows": [
            list(FITTING_0137),
            list(FITTING_0157),
        ],
        "normalized_first_diagonal": True,
        "inverted_second_diagonal": True,
        "incidence_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "exact characteristic-zero slope-endpoint theorem" in (
        theorem_text
    )
    assert "No graph satisfying the prize equation" in theorem_text

    result = {
        "statement": (
            "The zero-slope weighted H22 incidence is empty over the "
            "generic point of component eight."
        ),
        "scope": (
            "generic component parameters at the compactified slope "
            "endpoint r=0 over characteristic zero"
        ),
        "d01_minor_content_ledger": (
            verify_d01_minor_content_ledger()
        ),
        "certificates": [
            verify_d01_zero_slope(),
            verify_d23_zero_slope(),
        ],
        "proof_boundary": {
            "special_component_parameter_divisors": "open",
            "other_projective_boundaries": "open",
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
        ROOT
        / "tmp"
        / "p5_h22_disjoint_mixed_star_zero_slope_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
