#!/usr/bin/env python3
"""Verify the exact affine-chart closure of the P4 component."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md"
COMPONENT = ROOT / "P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
PERMUTATIONS = tuple(itertools.permutations(range(4)))
WORDS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def main() -> None:
    plane_symbols = sp.symbols("a b c d e f g h i j k l m n o p")
    (
        a, b, c, d, e, f, g, h,
        i, j, k, ell, m, n, o, p,
    ) = plane_symbols
    rows = (
        sp.Matrix(((1, 0, a, b), (0, 1, c, d))),
        sp.Matrix(((e, 1, 0, f), (g, 0, 1, h))),
        sp.Matrix(((i, 1, 0, j), (k, 0, 1, ell))),
        sp.Matrix(((1, m, n, 0), (0, o, p, 1))),
    )
    component_equations = (
        f, g, i, ell, m, o,
        h * p + 1,
        n * k + 1,
        j - h * n * e,
        h * c - d - j,
        b - h * (a - n),
    )

    E, I, L, Q, C = sp.symbols("E I L Q C")
    family_coordinates = (
        -Q * (C + E * I * L) / E,
        -C * Q - E * I * (L * Q + 1),
        C / E + I * L,
        C,
        L, 0, 0, E,
        0, E * I * L, -1 / I, 0,
        0, I, 0, -1 / E,
    )
    family_substitution = dict(
        zip(plane_symbols, family_coordinates, strict=True)
    )
    assert all(
        sp.factor(equation.subs(family_substitution)) == 0
        for equation in component_equations
    )

    free_symbols = (a, d, e, h, n)
    D = d + h * n * e
    closure_coordinates = (
        a, h * (a - n), D / h, d,
        e, 0, 0, h,
        0, h * n * e, -1 / n, 0,
        0, n, 0, -1 / h,
    )
    closure_substitution = dict(
        zip(plane_symbols, closure_coordinates, strict=True)
    )
    assert all(
        sp.factor(equation.subs(closure_substitution)) == 0
        for equation in component_equations
    )
    assert len(free_symbols) == 5

    inverse_parameters = {
        E: h,
        I: n,
        L: e,
        C: d,
        Q: -a * h / D,
    }
    recovered_coordinates = tuple(
        sp.factor(sp.sympify(coordinate).subs(inverse_parameters))
        for coordinate in family_coordinates
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(
            recovered_coordinates, closure_coordinates, strict=True
        )
    )

    coefficients = {
        word: permanent(
            [rows[mode][word[mode], :] for mode in range(4)]
        ).subs(closure_substitution)
        for word in WORDS
    }
    coefficients = {
        word: sp.factor(value)
        for word, value in coefficients.items()
    }
    expected_nonzero = {
        (0, 0, 0, 0): 2 * a * e * h * n,
        (0, 1, 0, 0): 2 * a * h,
        (1, 0, 0, 0): 2 * e * n * D,
        (1, 1, 0, 0): 2 * D,
    }
    assert all(
        sp.factor(coefficients[word] - expected_nonzero.get(word, 0)) == 0
        for word in WORDS
    )

    output = {
        "verified": True,
        "field": "C",
        "grassmann_chart_dimension": 16,
        "component_equations": len(component_equations),
        "component_chart_dimension": len(free_symbols),
        "free_coordinates": [str(symbol) for symbol in free_symbols],
        "family_open_condition": "D=d+h*n*e != 0",
        "nonzero_boundary_condition": "D=0 and a!=0",
        "nonzero_tensor_coefficients": {
            "".join(map(str, word)): str(value)
            for word, value in expected_nonzero.items()
        },
        "tensor_factorization": (
            "2*(a*h*x0+D*y0)*(e*n*x1+y1)*x2*x3"
        ),
        "remaining_schubert_boundary": [
            "Delta_0(01)",
            "Delta_1(12)",
            "Delta_2(12)",
            "Delta_3(03)",
        ],
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
        },
        "all_components_classified": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_pure_rank_two_component_chart_closure_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
