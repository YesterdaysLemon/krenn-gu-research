#!/usr/bin/env python3
"""Verify the H31 obstruction on the nonzero component chart boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md"
CHART = (
    REPO_ROOT
    / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md"
)
ORBIT = REPO_ROOT / "claims/p5/h31/rank-two-component-orbit/P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md"
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
        word = "".join(map(str, bits))
        coefficients[word] = permanent(
            tuple(
                beta_p[mode] if bits[mode] else alpha_p[mode]
                for mode in range(4)
            )
        )
    words = tuple(
        word for word in coefficients if word not in ("0000", "1111")
    )
    mixed = sp.Matrix([
        [
            sp.diff(coefficients[word], variable)
            for variable in variables
        ]
        for word in words
    ])
    alpha_diagonal = sp.Matrix([[
        sp.diff(coefficients["0000"], variable)
        for variable in variables
    ]])
    beta_diagonal = sp.Matrix([[
        sp.diff(coefficients["1111"], variable)
        for variable in variables
    ]])
    return mixed, alpha_diagonal, beta_diagonal, words


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


def assert_kernel(matrix: sp.Matrix, vectors: tuple[sp.Matrix, ...]) -> None:
    for vector in vectors:
        assert (matrix * vector).applyfunc(sp.simplify) == sp.zeros(
            matrix.rows, 1
        )


def diagonal_pairs(
    alpha_diagonal: sp.Matrix,
    beta_diagonal: sp.Matrix,
    vectors: tuple[sp.Matrix, ...],
) -> tuple[tuple[sp.Expr, sp.Expr], ...]:
    return tuple(
        (
            sp.factor((alpha_diagonal * vector)[0]),
            sp.factor((beta_diagonal * vector)[0]),
        )
        for vector in vectors
    )


def rank_minor(
    matrix: sp.Matrix,
    words: tuple[str, ...],
    row_words: tuple[str, ...],
    columns: tuple[int, ...],
) -> sp.Expr:
    rows = [words.index(word) for word in row_words]
    return sp.factor(matrix[rows, list(columns)].det())


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


def main() -> None:
    A, H, N = sp.symbols("A H N", nonzero=True)
    R = sp.symbols("R")
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    variables = x + y
    alpha = (
        (1, 0, A, H * (A - N)),
        (0, 0, 1, H),
        (0, 1, 0, H * N * R),
        (1, 0, N, 0),
    )
    beta = (
        (0, 1, 0, -H * N * R),
        (R, 1, -R * N, -R * H * N),
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
    assert pure_coefficients[(0, 0, 0, 0)] == 2 * A * H
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

    generic_kernels = {
        0: (sp.Matrix((-N, 0, 0, -N, 0, -N * R, 1, 0)),),
        1: (sp.Matrix((0, 0, 1, 0, 1, 1, 0, 0)),),
        2: (
            sp.Matrix((N, 0, 0, N, 0, -N * R, 1, 0)),
            sp.Matrix((-H * (A - N), -H, 0, 0, 0, 0, 0, 1)),
        ),
        3: (
            sp.Matrix((0, 0, -1, 0, 1, 1, 0, 0)),
            sp.Matrix((H * (A - N), H, 0, 0, 0, 0, 0, 1)),
        ),
    }
    expected_generic_diagonals = {
        0: ((-2 * A * H * N, 0),),
        1: ((2 * A * H, 0),),
        2: ((2 * H * N, 2 * R), (-2 * H**2 * (A - N), 2 * H * R)),
        3: ((0, 2 / (H * N)), (2 * A * H, 2 * R)),
    }
    for distinguished, vectors in generic_kernels.items():
        mixed, alpha_diagonal, beta_diagonal, _words = data[distinguished]
        assert_kernel(mixed, vectors)
        assert diagonal_pairs(
            alpha_diagonal, beta_diagonal, vectors
        ) == expected_generic_diagonals[distinguished]

    generic_rank_minors = {
        0: (
            (
                ("0001", "0100", "0101", "0110", "1000", "1011", "1100"),
                (0, 1, 2, 3, 4, 5, 7),
                -4 * H**5 * N**5 * R**2 * (A - N) ** 3,
            ),
        ),
        1: (
            (
                ("0001", "0010", "0011", "0100", "0101", "0111", "1000"),
                (0, 1, 2, 3, 4, 6, 7),
                4 * H**4 * N**3 * R**6 * (A - N) ** 2 * (2 * A + N),
            ),
            (
                ("0001", "0010", "0011", "0100", "0101", "0110", "1000"),
                (0, 1, 2, 3, 4, 6, 7),
                4 * H**5 * N**3 * R**6 * (A - N) ** 2
                * (A + N) * (2 * A - N),
            ),
        ),
        2: (
            (
                ("0001", "0101", "0111", "1000", "1010", "1100"),
                (0, 1, 2, 3, 4, 5),
                -2 * H**3 * R / N,
            ),
        ),
        3: (
            (
                ("0001", "0100", "0101", "0111", "1000", "1010"),
                (0, 1, 2, 3, 4, 6),
                -2 * R / H**3,
            ),
        ),
    }
    for distinguished, specifications in generic_rank_minors.items():
        mixed, _ad, _bd, words = data[distinguished]
        for row_words, columns, expected in specifications:
            assert sp.factor(
                rank_minor(mixed, words, row_words, columns) - expected
            ) == 0

    collision_data = {
        distinguished: (
            mixed.subs(A, N),
            alpha_diagonal.subs(A, N),
            beta_diagonal.subs(A, N),
            words,
        )
        for distinguished, (
            mixed, alpha_diagonal, beta_diagonal, words
        ) in data.items()
    }
    collision_kernels = {
        0: (
            sp.Matrix((-N, 0, 0, -N, 0, -N * R, 1, 0)),
            sp.Matrix((0, -H, 0, 0, 0, 0, 0, 1)),
        ),
        1: (
            sp.Matrix((0, 0, 1, 0, 1, 1, 0, 0)),
            sp.Matrix((0, H, 0, 0, 0, 0, 0, 1)),
        ),
    }
    collision_expected = {
        0: ((-2 * H * N**2, 0), (0, -2 * H * N * R)),
        1: (
            (2 * H * N, 0),
            (2 * H**2 * N**2 * R, -2 * H * N * R**2),
        ),
    }
    collision_minor_specs = {
        0: (
            ("0001", "0101", "0111", "1000", "1010", "1100"),
            (0, 1, 2, 3, 4, 5),
            -2 * H**3 * N**5 * R,
        ),
        1: (
            ("0001", "0010", "0100", "0101", "1000", "1010"),
            (0, 1, 2, 3, 4, 6),
            4 * H**4 * N**6 * R**6,
        ),
    }
    for distinguished, vectors in collision_kernels.items():
        mixed, alpha_diagonal, beta_diagonal, words = collision_data[
            distinguished
        ]
        assert_kernel(mixed, vectors)
        assert diagonal_pairs(
            alpha_diagonal, beta_diagonal, vectors
        ) == collision_expected[distinguished]
        row_words, columns, expected = collision_minor_specs[distinguished]
        assert sp.factor(
            rank_minor(mixed, words, row_words, columns) - expected
        ) == 0

    zero_data = {
        distinguished: (
            mixed.subs(R, 0),
            alpha_diagonal.subs(R, 0),
            beta_diagonal.subs(R, 0),
            words,
        )
        for distinguished, (
            mixed, alpha_diagonal, beta_diagonal, words
        ) in data.items()
    }
    zero_kernels = {
        0: (
            sp.Matrix((0, 0, -1, 0, 1, 1, 0, 0)),
            sp.Matrix((-N, 0, 0, -N, 0, 0, 1, 0)),
        ),
        2: (
            sp.Matrix((0, 0, -1, 0, 1, 1, 0, 0)),
            sp.Matrix((N, 0, 0, N, 0, 0, 1, 0)),
            sp.Matrix((-H * (A - N), -H, 0, 0, 0, 0, 0, 1)),
        ),
        3: (
            sp.Matrix((0, 0, -1, 0, 1, 1, 0, 0)),
            sp.Matrix((H * (A - N), H, 0, 0, 0, 0, 0, 1)),
        ),
    }
    zero_expected = {
        0: ((0, 2), (-2 * A * H * N, 0)),
        2: ((0, -2 / N), (2 * H * N, 0), (-2 * H**2 * (A - N), 0)),
        3: ((0, 2 / (H * N)), (2 * A * H, 0)),
    }
    for distinguished, vectors in zero_kernels.items():
        mixed, alpha_diagonal, beta_diagonal, _words = zero_data[
            distinguished
        ]
        assert_kernel(mixed, vectors)
        assert diagonal_pairs(
            alpha_diagonal, beta_diagonal, vectors
        ) == zero_expected[distinguished]
    zero_one_mixed, zero_one_alpha, zero_one_beta, _zero_one_words = (
        zero_data[1]
    )
    zero_one_kernel = zero_one_mixed.nullspace()
    assert all(
        sp.factor((zero_one_beta * vector)[0]) == 0
        for vector in zero_one_kernel
    )

    t, u, v = sp.symbols("t u v")
    pure_marked = {
        mode: one_marked_map(mode, alpha, beta)
        for mode in (0, 2)
    }
    marked_certificates = {}

    extension = t * generic_kernels[2][0] + u * generic_kernels[2][1]
    marked = marked_extension(2, extension, alpha, beta, 2)
    determinant = sp.factor(marked[[0, 2, 3, 7], :].det())
    F = N * t - H * (A - N) * u
    G = t + H * u
    assert sp.factor(determinant - 8 * H * N * R * G * F**2) == 0
    assert pure_marked[2][3, 2] == 1
    marked_certificates["generic_q2"] = determinant

    extension = t * generic_kernels[3][0] + u * generic_kernels[3][1]
    marked = marked_extension(3, extension, alpha, beta, 2)
    determinant = sp.factor(marked[[0, 3, 4, 7], :].det())
    K = t + H * N * R * u
    assert sp.factor(determinant - 8 * A * u**2 * K) == 0
    assert pure_marked[2][3, 3] == -1 / H
    marked_certificates["generic_q3"] = determinant

    alpha_collision = tuple(
        tuple(sp.sympify(entry).subs(A, N) for entry in row)
        for row in alpha
    )
    beta_collision = tuple(
        tuple(sp.sympify(entry).subs(A, N) for entry in row)
        for row in beta
    )
    collision_marked = one_marked_map(
        0, alpha_collision, beta_collision
    )
    for distinguished, expected, rows in (
        (0, 8 * H**2 * N**3 * R**2 * t * u**2, [0, 1, 5, 7]),
        (
            1,
            -8 * H**2 * N * R**3 * u**2 * (t + H * N * R * u),
            [0, 3, 5, 7],
        ),
    ):
        extension = (
            t * collision_kernels[distinguished][0]
            + u * collision_kernels[distinguished][1]
        )
        marked = marked_extension(
            distinguished,
            extension,
            alpha_collision,
            beta_collision,
            0,
        )
        determinant = sp.factor(marked[rows, :].det())
        assert sp.factor(determinant - expected) == 0
        assert any(
            collision_marked[row, distinguished] != 0
            for row in range(8)
        )
        marked_certificates[f"collision_q{distinguished}"] = determinant

    alpha_zero = tuple(
        tuple(sp.sympify(entry).subs(R, 0) for entry in row)
        for row in alpha
    )
    beta_zero = tuple(
        tuple(sp.sympify(entry).subs(R, 0) for entry in row)
        for row in beta
    )
    zero_marked = one_marked_map(2, alpha_zero, beta_zero)
    zero_marked_specs = {
        0: (
            t * zero_kernels[0][0] + u * zero_kernels[0][1],
            [0, 3, 6, 7],
            8 * A * H * N**3 * t**2 * u,
        ),
        2: (
            t * zero_kernels[2][0]
            + u * zero_kernels[2][1]
            + v * zero_kernels[2][2],
            [0, 3, 6, 7],
            8 * H * t**2 * (N * u - H * (A - N) * v),
        ),
        3: (
            t * zero_kernels[3][0] + u * zero_kernels[3][1],
            [0, 3, 4, 7],
            8 * A * t * u**2,
        ),
    }
    for distinguished, (
        extension, rows, expected
    ) in zero_marked_specs.items():
        marked = marked_extension(
            distinguished, extension, alpha_zero, beta_zero, 2
        )
        determinant = sp.factor(marked[rows, :].det())
        assert sp.factor(determinant - expected) == 0
        assert any(
            zero_marked[row, distinguished] != 0
            for row in range(8)
        )
        marked_certificates[f"R0_q{distinguished}"] = determinant

    output = {
        "verified": True,
        "field": "C",
        "boundary_parameters": ["A", "H", "N", "R"],
        "nonvanishing_parameters": ["A", "H", "N"],
        "generic_mixed_ranks": [7, 7, 6, 6],
        "collision_A_eq_N_mixed_ranks_q01": [6, 6],
        "R_zero_mixed_ranks_A_neq_N": [6, 2, 5, 6],
        "R_zero_mixed_ranks_A_eq_N_q01": [5, 1],
        "marked_certificates": {
            key: str(value)
            for key, value in marked_certificates.items()
        },
        "all_four_distinguished_orientations_excluded": True,
        "remaining_known_component_geometry": "preferred_Pluecker_Schubert_boundary",
        "dependencies": {
            CHART.name: sha256(CHART),
            ORBIT.name: sha256(ORBIT),
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
        REPO_ROOT / "tmp" / "p5_h31_component_chart_boundary_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
