#!/usr/bin/env python3
"""Verify the H31 obstruction for all orientations of the family chart."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md"
COMPONENT = ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
ORIENTATION_THREE = ROOT / "P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def extension_data(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    variables: tuple[sp.Symbol, ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, tuple[str, ...]]:
    x = variables[:4]
    y = variables[4:]
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common)
        + (x[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        tuple(beta[mode][coordinate] for coordinate in common)
        + (y[mode],)
        for mode in range(4)
    )
    coefficients = {}
    for bits in BITS4:
        word = "".join(map(str, bits))
        coefficients[word] = permanent(
            tuple(
                beta_p[mode] if bits[mode] else alpha_p[mode]
                for mode in range(4)
            )
        )
    mixed_words = tuple(
        word
        for word in coefficients
        if word not in ("0000", "1111")
    )
    mixed = sp.Matrix(
        [
            [
                sp.diff(coefficients[word], variable)
                for variable in variables
            ]
            for word in mixed_words
        ]
    )
    alpha_diagonal = sp.Matrix([[
        sp.diff(coefficients["0000"], variable)
        for variable in variables
    ]])
    beta_diagonal = sp.Matrix([[
        sp.diff(coefficients["1111"], variable)
        for variable in variables
    ]])
    return mixed, alpha_diagonal, beta_diagonal, mixed_words


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    rows = []
    for bits in BITS3:
        selected: list[tuple[sp.Expr, ...] | None] = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other] if bits[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate)
                for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def assert_kernel(
    matrix: sp.Matrix,
    vectors: tuple[sp.Matrix, ...],
) -> None:
    for vector in vectors:
        assert (matrix * vector).applyfunc(sp.simplify) == sp.zeros(
            matrix.rows, 1
        )


def main() -> None:
    E, I = sp.symbols("E I", nonzero=True)
    L, Q, C = sp.symbols("L Q C")
    D = C + E * I * L
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    variables = x + y

    beta = (
        (0, 1, D / E, C),
        (0, 0, 1, E),
        (0, 1, 0, E * I * L),
        (1, 0, I, 0),
    )
    alpha = (
        (1, Q, 0, -E * I * (1 + L * Q)),
        (L, 1, -I * L, -E * I * L),
        (-1 / I, 0, 1, 0),
        (0, 0, -1 / E, 1),
    )
    data = {
        distinguished: extension_data(
            distinguished, alpha, beta, variables
        )
        for distinguished in (0, 1, 2)
    }

    generic_kernels = {
        0: sp.Matrix((1, L, -1 / I, 0, 0, 0, 0, 1)),
        1: sp.Matrix((Q, 1, 0, 0, 1, 0, 1, 0)),
        2: sp.Matrix((
            0, -L, 1 / I, -1 / (E * I),
            D / (E * I), 1 / I, 0, 1,
        )),
    }
    generic_beta_values = {0: 2 * D, 1: 2 * D, 2: 2 * D / I}
    for distinguished, kernel in generic_kernels.items():
        mixed, alpha_diagonal, beta_diagonal, _words = data[distinguished]
        assert_kernel(mixed, (kernel,))
        assert sp.factor((alpha_diagonal * kernel)[0]) == 0
        assert sp.factor(
            (beta_diagonal * kernel)[0] - generic_beta_values[distinguished]
        ) == 0

    generic_minor_specs = {
        0: (
            (
                ("0001", "0010", "0011", "0110", "1000", "1010", "1011"),
                (0, 1, 2, 3, 4, 5, 6),
                4 * E**3 * I**9 * L**4 * (2 * L * Q + 1)
                * (Q * D + E * I),
            ),
            (
                ("0010", "0011", "0100", "0101", "0110", "1000", "1010"),
                (0, 1, 2, 3, 4, 5, 6),
                -4 * E**3 * I**6 * L**3 * Q**3,
            ),
        ),
        1: (
            (
                ("0001", "0010", "0011", "0100", "0101", "0110", "1000"),
                (0, 1, 2, 3, 4, 5, 7),
                4 * E**4 * I**6 * L**6 * (L * Q + 1) ** 2,
            ),
            (
                ("0001", "0010", "0011", "0100", "0110", "1000", "1010"),
                (0, 1, 2, 3, 4, 5, 7),
                -4 * E**3 * I**7 * L**9 * (L * Q + 2),
            ),
        ),
        2: (
            (
                ("0001", "0010", "0011", "0110", "0111", "1000", "1010"),
                (0, 1, 2, 3, 4, 5, 6),
                -4 * E**4 * I**2 * L**2 * (2 * L * Q + 1),
            ),
            (
                ("0010", "0011", "0100", "0101", "0111", "1000", "1010"),
                (0, 1, 2, 3, 4, 5, 6),
                4 * E**4 * L**2 * Q**2,
            ),
        ),
    }
    generic_minors = {}
    for distinguished, specifications in generic_minor_specs.items():
        mixed, _alpha_diagonal, _beta_diagonal, words = data[distinguished]
        values = []
        for row_words, columns, expected in specifications:
            rows = [words.index(word) for word in row_words]
            value = sp.factor(mixed[rows, list(columns)].det())
            assert sp.factor(value - expected) == 0
            values.append(value)
        generic_minors[distinguished] = values

    exceptional = {
        distinguished: (
            mixed.subs(L, 0),
            alpha_diagonal.subs(L, 0),
            beta_diagonal.subs(L, 0),
            words,
        )
        for distinguished, (
            mixed, alpha_diagonal, beta_diagonal, words
        ) in data.items()
    }
    exceptional_kernels = {
        0: (
            sp.Matrix((-Q, -1, 0, 0, 1, 0, 1, 0)),
            sp.Matrix((1, 0, -1 / I, 0, 0, 0, 0, 1)),
        ),
        1: tuple(
            sp.eye(8)[:, index]
            for index in (0, 1, 4, 5, 6)
        ),
        2: (
            sp.Matrix((I, 0, 0, -1 / E, C / E, 1, 0, 0)),
            sp.Matrix((-Q, -1, 0, 0, 1, 0, 1, 0)),
            sp.Matrix((-1, 0, 1 / I, 0, 0, 0, 0, 1)),
        ),
    }
    exceptional_minor_specs = {
        0: (
            ("0001", "0010", "0110", "0111", "1000", "1100"),
            (0, 1, 2, 3, 4, 5),
            2 * E**3 * I**5,
        ),
        1: (
            ("0100", "0101", "1101"),
            (2, 3, 7),
            8 * C * E**2,
        ),
        2: (
            ("0001", "0010", "0110", "0111", "1000"),
            (0, 1, 2, 3, 4),
            E**3,
        ),
    }
    exceptional_diagonals = {}
    for distinguished, kernels in exceptional_kernels.items():
        mixed, alpha_diagonal, beta_diagonal, words = exceptional[
            distinguished
        ]
        assert_kernel(mixed, kernels)
        row_words, columns, expected = exceptional_minor_specs[distinguished]
        rows = [words.index(word) for word in row_words]
        minor = sp.factor(mixed[rows, list(columns)].det())
        assert sp.factor(minor - expected) == 0
        exceptional_diagonals[distinguished] = tuple(
            (
                sp.factor((alpha_diagonal * kernel)[0]),
                sp.factor((beta_diagonal * kernel)[0]),
            )
            for kernel in kernels
        )

    assert exceptional_diagonals == {
        0: ((-2 * Q, 2 * E * I), (0, 2 * C)),
        1: ((0, 0), (0, 0), (0, 0), (0, 0), (0, 2 * C)),
        2: ((-2, 2 * C), (2 * Q / I, 2 * E), (2 / I, 0)),
    }

    t, u, v = sp.symbols("t u v")
    marked_results = {}
    pure_alpha = tuple(
        tuple(sp.sympify(entry).subs(L, 0) for entry in row)
        for row in alpha
    )
    pure_beta = tuple(
        tuple(sp.sympify(entry).subs(L, 0) for entry in row)
        for row in beta
    )
    pure_marked = one_marked_map(1, pure_alpha, pure_beta)

    for distinguished, coefficients in {
        0: (t, u),
        2: (t, u, v),
    }.items():
        extension = sum(
            (
                coefficient * kernel
                for coefficient, kernel in zip(
                    coefficients,
                    exceptional_kernels[distinguished],
                    strict=True,
                )
            ),
            sp.zeros(8, 1),
        )
        common = tuple(
            coordinate
            for coordinate in range(4)
            if coordinate != distinguished
        )
        alpha_p = tuple(
            tuple(pure_alpha[mode][coordinate] for coordinate in common)
            + (extension[mode],)
            for mode in range(4)
        )
        beta_p = tuple(
            tuple(pure_beta[mode][coordinate] for coordinate in common)
            + (extension[4 + mode],)
            for mode in range(4)
        )
        marked_p = one_marked_map(1, alpha_p, beta_p)
        if distinguished == 0:
            minors = (
                sp.factor(marked_p[[0, 2, 6, 7], :].det()),
            )
            expected = (
                -8 * I * Q * t**2 * (E * I * t + C * u) / E,
            )
            pure_entries = (sp.factor(pure_marked[0, 0]),)
            assert pure_entries == (Q,)
        else:
            minors = (
                sp.factor(marked_p[[0, 2, 4, 7], :].det()),
                sp.factor(marked_p[[0, 2, 6, 7], :].det()),
            )
            expected = (
                8 * t * (C * t + E * u) * (I * t - Q * u - v)
                / (E * I),
                8 * u * (C * t + E * u) * (I * t - Q * u - v)
                / (E * I),
            )
            pure_entries = (sp.factor(pure_marked[2, 2]),)
            assert pure_entries == (1,)
        assert all(
            sp.factor(actual - wanted) == 0
            for actual, wanted in zip(minors, expected, strict=True)
        )
        marked_results[distinguished] = {
            "neighbor_minors": [str(value) for value in minors],
            "pure_distinguished_entries": [
                str(value) for value in pure_entries
            ],
        }

    output = {
        "verified": True,
        "field": "C",
        "new_distinguished_orientations": [0, 1, 2],
        "prior_distinguished_orientation": 3,
        "generic_mixed_ranks": {"0": 7, "1": 7, "2": 7},
        "generic_first_diagonals": {"0": 0, "1": 0, "2": 0},
        "exceptional_mixed_ranks": {"0": 6, "1": 3, "2": 5},
        "exceptional_kernel_dimensions": {"0": 2, "1": 5, "2": 3},
        "orientation_1_binary_Delta2_possible": False,
        "orientations_with_marked_injectivity": [0, 2],
        "marked_results": marked_results,
        "family_chart_symmetry_orbit_H31_lift_possible": False,
        "component_boundaries_excluded": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            ORIENTATION_THREE.name: sha256(ORIENTATION_THREE),
        },
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p5_h31_rank_two_component_orbit_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
