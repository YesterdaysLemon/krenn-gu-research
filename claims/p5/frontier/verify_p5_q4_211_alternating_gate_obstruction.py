#!/usr/bin/env python3
"""Verify the q4_211 alternating-gate obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md"
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS
        )
    )


def slice_matrix(mode, row_pairs):
    matrix = []
    other_modes = [index for index in range(4) if index != mode]
    for word in itertools.product((0, 1), repeat=3):
        row = []
        for coordinate in range(4):
            rows = []
            other_index = 0
            for index in range(4):
                if index == mode:
                    rows.append(
                        sp.Matrix(
                            [
                                int(entry == coordinate)
                                for entry in range(4)
                            ]
                        )
                    )
                else:
                    rows.append(
                        row_pairs[index][word[other_index]]
                    )
                    other_index += 1
            row.append(permanent(rows))
        matrix.append(row)
    assert len(other_modes) == 3
    return sp.Matrix(matrix)


def derivative(polynomial, variables, direction):
    return sp.expand(
        sum(
            coefficient * sp.diff(polynomial, variable)
            for coefficient, variable in zip(
                direction,
                variables,
                strict=True,
            )
        )
    )


def main() -> None:
    p, q, r, t = sp.symbols("p q r t")
    x2, x3, y2, y3 = sp.symbols("x2 x3 y2 y3")
    z2, z3, d2, d3 = sp.symbols("z2 z3 d2 d3")
    lam = p * t + q * r
    delta = p * t - q * r
    e2 = sp.Matrix([0, 0, 1, 0])
    e3 = sp.Matrix([0, 0, 0, 1])

    transverse = (
        (e2, e3),
        (sp.Matrix([p, q, x2, x3]), e2),
        (e3, sp.Matrix([r, -t, y2, y3])),
        (
            sp.Matrix(
                [delta * r, delta * t, lam * y2, lam * y3]
            ),
            sp.Matrix(
                [delta * p, -delta * q, -lam * x2, -lam * x3]
            ),
        ),
    )
    transverse_matrices = [
        slice_matrix(mode, transverse) for mode in (1, 2, 3)
    ]
    transverse_rows = (
        (0, 1, 3, 7),
        (0, 4, 6, 7),
        (0, 1, 5, 7),
    )
    transverse_minors = [
        sp.factor(matrix[list(rows), :].det())
        for matrix, rows in zip(
            transverse_matrices,
            transverse_rows,
            strict=True,
        )
    ]
    assert all(matrix.rank() == 4 for matrix in transverse_matrices)
    assert sp.expand(
        transverse_minors[0] + delta**4 * lam**3
    ) == 0
    assert sp.expand(
        transverse_minors[1] + delta**4 * lam**3
    ) == 0
    assert sp.expand(
        transverse_minors[2] + delta**2 * lam
    ) == 0

    tangent = (
        (e2, e3),
        (sp.Matrix([p, q, 0, 0]), e2),
        (e3, sp.Matrix([p, -q, 0, 0])),
        (
            sp.Matrix([p, q, z2, z3]),
            sp.Matrix([p, -q, d2, d3]),
        ),
    )
    tangent_matrices = [
        slice_matrix(mode, tangent) for mode in (1, 2, 3)
    ]
    tangent_minors = [
        sp.factor(tangent_matrices[0][[0, 1, 3, 7], :].det()),
        sp.factor(tangent_matrices[1][[0, 4, 6, 7], :].det()),
    ]
    assert [matrix.rank() for matrix in tangent_matrices] == [4, 4, 2]
    assert all(
        sp.expand(value + 8 * p**3 * q**3) == 0
        for value in tangent_minors
    )
    assert tangent_matrices[2][:, 2:] == sp.zeros(8, 2)
    assert tangent_matrices[2][:, :2].rank() == 2

    # Restriction from H coordinates (e1,e2,w+,w-) to
    # K coordinates (e0,e1,e2).
    tangent_mode_three_on_k = sp.Matrix(
        [
            [(z2 + z3) / 2, p, q],
            [(d2 + d3) / 2, p, -q],
        ]
    )
    last_two_determinant = sp.factor(
        tangent_mode_three_on_k[:, 1:].det()
    )
    assert last_two_determinant == -2 * p * q
    distinguished_on_k = sp.Matrix([[1, 0, 0], [sp.Symbol("a"), 1, 1]])
    distinguished_normal = distinguished_on_k.nullspace()[0]
    assert distinguished_normal == sp.Matrix([0, -1, 1])

    x0, x1, x2_source, x3_source, x4 = sp.symbols(
        "x0 x1 x2_source x3_source x4"
    )
    b, c = sp.symbols("b c", nonzero=True)
    variables = (x0, x1, x2_source, x3_source, x4)
    source_permanent = sp.prod(variables)
    n = (0, 0, 0, c, b)
    double_n = derivative(
        derivative(source_permanent, variables, n),
        variables,
        n,
    )
    triple_n = derivative(double_n, variables, n)
    assert sp.expand(double_n - 2 * b * c * x0 * x1 * x2_source) == 0
    assert triple_n == 0

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b*c != 0",
        "transverse_slice_ranks": [
            matrix.rank() for matrix in transverse_matrices
        ],
        "transverse_witness_minors": [
            str(value) for value in transverse_minors
        ],
        "tangent_slice_ranks": [
            matrix.rank() for matrix in tangent_matrices
        ],
        "tangent_gate_witness_minors": [
            str(value) for value in tangent_minors
        ],
        "tangent_third_slice_kernel": "span(e2*,e3*)",
        "double_normal_contraction": str(sp.factor(double_n)),
        "triple_normal_contraction": str(triple_n),
        "tangent_K_projection_determinant": str(last_two_determinant),
        "two_cross_marked_boundary_excluded": True,
        "one_cross_normal_incidence_retained": True,
        "adjacent_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_alternating_gate_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
