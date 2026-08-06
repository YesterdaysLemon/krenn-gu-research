#!/usr/bin/env python3
"""Verify three linear-slope H22 boundaries of component eight."""

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
from verify_p5_h22_disjoint_mixed_star_coupled_slope_boundary_obstruction import (
    marked_map,
)


THEOREM = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_LINEAR_SLOPE_BOUNDARY_OBSTRUCTION.md"
)
COMPONENT = REPO_ROOT / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md"
GENERIC = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
a, b, f, phi, r = sp.symbols("a b f phi r")
SLOPE_GRAPHS = {
    "source_plus": (a + b) * r + (a - b),
    "source_minus": (a + b) * r - (a - b),
    "basis_ratio": (a * f - 1) * r + (a * f + 1),
}
CERTIFICATES = {
    ("source_plus", "01"): (0, (FITTING_0137, FITTING_0157)),
    ("source_plus", "23"): (0, (FITTING_0137, FITTING_0157)),
    ("source_minus", "01"): (0, (FITTING_0137, FITTING_0157)),
    ("source_minus", "23"): (0, (FITTING_0137, FITTING_0157)),
    ("basis_ratio", "01"): (1, ((0, 4, 5, 7),)),
    ("basis_ratio", "23"): (0, (FITTING_0137, FITTING_0157)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_case(graph: str, direction: str) -> dict[str, object]:
    model = build_model(direction)
    mode, fitting_rows = CERTIFICATES[(graph, direction)]
    marked = (
        model["marked"]
        if mode == 0
        else marked_map(model, direction, mode)
    )
    extensions = model["extensions"]
    shifts = model["shifts"]
    w = sp.Symbol("w")
    variables = (
        extensions
        + (w, sp.Symbol("r"), sp.Symbol("phi"))
        + shifts
    )
    lines = [
        "ring R=(0,a,b,f),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(2),dp(4));",
        "option(redSB);",
        "poly S=" + singular(SLOPE_GRAPHS[graph]) + ";",
        "poly C=" + singular(model["component"]) + ";",
    ]
    for index, expression in enumerate(model["mixed"]):
        lines.append(f"poly g{index}={singular(expression)};")
    for index, rows in enumerate(fitting_rows):
        minor = marked.extract(rows, range(4))
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
            "ideal I=S,C,"
            + ",".join(
                [
                    *(f"g{index}" for index in range(14)),
                    "da",
                    "db",
                    *(
                        f"h{index}"
                        for index in range(len(fitting_rows))
                    ),
                ]
            )
            + ";",
            "I=slimgb(I);",
            (
                f'"CODEX_RESULT:{graph}:{direction}:"'
                '+string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        f"linear slope {graph} direction {direction}",
        timeout=600,
    )
    assert markers(output) == [
        f"CODEX_RESULT:{graph}:{direction}:1:1"
    ], output
    return {
        "graph": graph,
        "slope_equation": str(SLOPE_GRAPHS[graph]),
        "direction": direction,
        "marked_mode": mode,
        "minor_rows": [list(rows) for rows in fitting_rows],
        "normalized_first_diagonal": True,
        "inverted_second_diagonal": True,
        "unsplit_full_fitting_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "three rational slope graphs" in theorem_text
    assert "cross-mode repair" in theorem_text
    assert "No graph satisfying the prize equation" in theorem_text

    component = build_model("01")["component"]
    assert component.subs({a: 0, b: 0}) == -1
    assert sp.expand(
        SLOPE_GRAPHS["source_plus"].subs(b, -a)
    ) == 2 * a
    assert sp.expand(
        SLOPE_GRAPHS["source_minus"].subs(b, -a)
    ) == -2 * a
    assert sp.expand(
        SLOPE_GRAPHS["basis_ratio"].subs(f, 1 / a)
    ) == 2

    certificates = [
        verify_case(graph, direction)
        for graph in SLOPE_GRAPHS
        for direction in ("01", "23")
    ]
    result = {
        "statement": (
            "The generic weighted H22 incidence is empty on three "
            "rational slope graphs of component eight."
        ),
        "scope": (
            "generic points of three linear slope divisors over "
            "characteristic zero"
        ),
        "slope_graphs": {
            graph: str(equation)
            for graph, equation in SLOPE_GRAPHS.items()
        },
        "unit_ideal_certificates": certificates,
        "proof_boundary": {
            "special_divisors_inside_graphs": "open",
            "remaining_quadratic_slope_candidate": "open",
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
        / "p5_h22_disjoint_mixed_star_linear_slope_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
