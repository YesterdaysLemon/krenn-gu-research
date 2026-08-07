#!/usr/bin/env python3
"""Verify the H31 obstruction on the first-plane fiber at infinity."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md"
CHART = ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md"
PREVIOUS = ROOT / "P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md"
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
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common)
        + (variables[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        tuple(beta[mode][coordinate] for coordinate in common)
        + (variables[4 + mode],)
        for mode in range(4)
    )
    coefficients = {}
    for bits in BITS4:
        coefficients[bits] = permanent(
            tuple(
                beta_p[mode] if bits[mode] else alpha_p[mode]
                for mode in range(4)
            )
        )
    mixed = sp.Matrix([
        [
            sp.diff(coefficients[bits], variable)
            for variable in variables
        ]
        for bits in BITS4
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ])
    alpha_diagonal = sp.Matrix([[
        sp.diff(coefficients[(0, 0, 0, 0)], variable)
        for variable in variables
    ]])
    beta_diagonal = sp.Matrix([[
        sp.diff(coefficients[(1, 1, 1, 1)], variable)
        for variable in variables
    ]])
    return mixed, alpha_diagonal, beta_diagonal


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
                int(index == coordinate) for index in range(4)
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


def marked_extension(
    distinguished: int,
    extension: sp.Matrix,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    mode: int,
) -> sp.Matrix:
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[row][coordinate] for coordinate in common)
        + (extension[row],)
        for row in range(4)
    )
    beta_p = tuple(
        tuple(beta[row][coordinate] for coordinate in common)
        + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(mode, alpha_p, beta_p)


def diagonal_pairs(
    data: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> tuple[tuple[sp.Expr, sp.Expr], ...]:
    mixed, alpha_diagonal, beta_diagonal = data
    return tuple(
        (
            sp.factor((alpha_diagonal * vector)[0]),
            sp.factor((beta_diagonal * vector)[0]),
        )
        for vector in mixed.nullspace()
    )


def main() -> None:
    H, N = sp.symbols("H N", nonzero=True)
    E, A, D = sp.symbols("E A D")
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    variables = x + y

    first_plane = (
        (0, 0, 1, H),
        (-D / H, A, A * N * E, D * N),
    )
    first_pluecker = tuple(
        sp.factor(
            first_plane[0][left] * first_plane[1][right]
            - first_plane[0][right] * first_plane[1][left]
        )
        for left, right in itertools.combinations(range(4), 2)
    )
    expected_pluecker = (
        0, D / H, D, -A, -A * H, N * (D - A * E * H)
    )
    assert all(
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(
            first_pluecker, expected_pluecker, strict=True
        )
    )

    raw_rows = (
        first_plane,
        ((E, 1, 0, 0), (0, 0, 1, H)),
        ((0, 1, 0, H * N * E), (-1 / N, 0, 1, 0)),
        ((1, 0, N, 0), (0, 0, -1 / H, 1)),
    )
    raw_coefficients = {
        bits: permanent(
            tuple(raw_rows[mode][bits[mode]] for mode in range(4))
        )
        for bits in BITS4
    }
    expected_raw = {
        (0, 0, 0, 0): 2 * E * H * N,
        (0, 1, 0, 0): 2 * H,
        (1, 0, 0, 0): 2 * A * E**2 * H * N**2,
        (1, 1, 0, 0): 2 * A * E * H * N,
    }
    assert all(
        sp.factor(value - expected_raw.get(bits, 0)) == 0
        for bits, value in raw_coefficients.items()
    )

    alpha = (
        (0, 0, 1, H),
        (0, 0, 1, H),
        (0, 1, 0, H * N * E),
        (1, 0, N, 0),
    )
    beta = (
        (-D / H, A, 0, N * (D - A * E * H)),
        (E, 1, -E * N, -E * H * N),
        (-1 / N, 0, 1, 0),
        (0, 0, -1 / H, 1),
    )
    pure_coefficients = {
        bits: permanent(
            tuple(
                beta[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for bits in BITS4
    }
    assert pure_coefficients[(0, 0, 0, 0)] == 2 * H
    assert all(
        value == 0
        for bits, value in pure_coefficients.items()
        if bits != (0, 0, 0, 0)
    )

    data = {
        distinguished: extension_data(
            distinguished, alpha, beta, variables
        )
        for distinguished in range(4)
    }
    generic_pairs = {
        distinguished: diagonal_pairs(value)
        for distinguished, value in data.items()
    }
    assert generic_pairs == {
        0: ((-2 * H * N, 0),),
        1: ((2 * H, 0),),
        2: ((-2 * H**2, 0),),
        3: ((0, 2 * A / (H * N)), (2 * H, 2 * A * E)),
    }

    t, u, v = sp.symbols("t u v")
    certificates: dict[str, sp.Expr] = {}

    generic_q3_basis = data[3][0].nullspace()
    extension = t * generic_q3_basis[0] + u * generic_q3_basis[1]
    marked = marked_extension(3, extension, alpha, beta, 3)
    determinant = sp.factor(marked[[0, 1, 3, 7], :].det())
    expected = 8 * A * H**2 * u**2 * (t + E * H * N * u) / N**3
    assert sp.factor(determinant - expected) == 0
    certificates["generic_q3"] = determinant

    alpha_E0 = tuple(
        tuple(sp.sympify(entry).subs(E, 0) for entry in row)
        for row in alpha
    )
    beta_E0 = tuple(
        tuple(sp.sympify(entry).subs(E, 0) for entry in row)
        for row in beta
    )
    data_E0 = {
        distinguished: extension_data(
            distinguished, alpha_E0, beta_E0, variables
        )
        for distinguished in range(4)
    }
    pairs_E0 = {
        distinguished: diagonal_pairs(value)
        for distinguished, value in data_E0.items()
    }
    assert pairs_E0[0] == ((0, 2 * A), (-2 * H * N, 0))
    assert all(pair[1] == 0 for pair in pairs_E0[1])
    assert pairs_E0[2] == (
        (0, -2 * A / N),
        (0, -2 * D / H),
        (-2 * H**2, -2 * D),
    )
    assert pairs_E0[3] == ((0, 2 * A / (H * N)), (2 * H, 0))

    e0_specs = {
        0: (
            (t, u),
            3,
            [0, 1, 3, 7],
            -8 * A * H**3 * t * u**2,
        ),
        2: (
            (t, u, v),
            3,
            [0, 1, 3, 7],
            8 * H**4 * v**2
            * (A * H * t + D * H * N * v + D * N * u) / N**3,
        ),
        3: (
            (t, u),
            3,
            [0, 1, 3, 7],
            8 * A * H**2 * t * u**2 / N**3,
        ),
    }
    for distinguished, (
        coefficients, mode, rows, expected
    ) in e0_specs.items():
        basis = data_E0[distinguished][0].nullspace()
        extension = sum(
            (
                coefficient * vector
                for coefficient, vector in zip(
                    coefficients, basis, strict=True
                )
            ),
            sp.zeros(8, 1),
        )
        marked = marked_extension(
            distinguished, extension, alpha_E0, beta_E0, mode
        )
        determinant = sp.factor(marked[rows, :].det())
        assert sp.factor(determinant - expected) == 0
        certificates[f"E0_q{distinguished}"] = determinant

    alpha_D0 = tuple(
        tuple(sp.sympify(entry).subs(D, 0) for entry in row)
        for row in alpha
    )
    beta_D0 = tuple(
        tuple(sp.sympify(entry).subs(D, 0) for entry in row)
        for row in beta
    )
    data_D0 = extension_data(2, alpha_D0, beta_D0, variables)
    assert diagonal_pairs(data_D0) == (
        (0, 2 * A * E),
        (-2 * H**2, 2 * A * E * H),
    )
    basis_D0 = data_D0[0].nullspace()
    extension = t * basis_D0[0] + u * basis_D0[1]
    marked = marked_extension(2, extension, alpha_D0, beta_D0, 3)
    determinant = sp.factor(marked[[0, 1, 3, 7], :].det())
    expected = -8 * A * E * H**5 * u**2 * (t + H * u) / N**2
    assert sp.factor(determinant - expected) == 0
    certificates["D0_q2"] = determinant

    alpha_A0 = tuple(
        tuple(sp.sympify(entry).subs({A: 0, E: 0}) for entry in row)
        for row in alpha
    )
    beta_A0 = tuple(
        tuple(sp.sympify(entry).subs({A: 0, E: 0}) for entry in row)
        for row in beta
    )
    data_A0 = extension_data(2, alpha_A0, beta_A0, variables)
    pairs_A0 = diagonal_pairs(data_A0)
    assert pairs_A0 == (
        (0, 0),
        (0, -2 * D / H),
        (-2 * H**2, -2 * D),
    )
    basis_A0 = data_A0[0].nullspace()
    extension = t * basis_A0[1] + u * basis_A0[2]
    marked = marked_extension(2, extension, alpha_A0, beta_A0, 2)
    determinant = sp.factor(marked[[0, 2, 6, 7], :].det())
    expected = -8 * D**2 * H**2 * N**2 * u**2 * (t + H * u)
    assert sp.factor(determinant - expected) == 0
    certificates["A0_E0_q2"] = determinant

    for (
        specialized_alpha,
        specialized_beta,
        mode_by_distinguished,
    ) in (
        (alpha, beta, {3: 3}),
        (alpha_E0, beta_E0, {0: 3, 2: 3, 3: 3}),
        (alpha_D0, beta_D0, {2: 3, 3: 3}),
        (alpha_A0, beta_A0, {2: 2}),
    ):
        for distinguished, mode in mode_by_distinguished.items():
            pure_marked = one_marked_map(
                mode, specialized_alpha, specialized_beta
            )
            assert any(
                pure_marked[row, distinguished] != 0
                for row in range(8)
            )

    output = {
        "verified": True,
        "field": "C",
        "schubert_divisor": "Delta_0(01)=0",
        "base_open_conditions": ["H", "N"],
        "fiber_direction_condition": "(A,D)!=(0,0)",
        "pure_coefficient": "2*H",
        "marked_certificates": {
            key: str(value)
            for key, value in certificates.items()
        },
        "all_four_distinguished_orientations_excluded": True,
        "remaining_known_component_geometry": (
            "Delta_1(12)*Delta_2(12)*Delta_3(03)=0"
        ),
        "dependencies": {
            CHART.name: sha256(CHART),
            PREVIOUS.name: sha256(PREVIOUS),
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
        ROOT / "tmp" / "p5_h31_component_fiber_infinity_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
