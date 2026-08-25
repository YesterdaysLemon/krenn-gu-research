"""Verify the GLD71 punctured-syndrome and Eisenstein-norm parent theorem."""

from __future__ import annotations

import importlib.util
import json
from itertools import permutations, product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
PARENT = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / (
        "verify_four_root_complete_q_layer_secant_boundary_trap_and_"
        "torus_star_compression.py"
    )
)

# A pinned sparse basis of the fixed star's 37-dimensional annihilator.  Each
# entry is ((root, leaf_1, leaf_2, leaf_3), coefficient).  The verifier checks
# the basis against the independently reconstructed GLD70 columns before use.
SPARSE_RELATIONS = (
    (((1, 1, 1, 1), 1),),
    (((0, 0, 0, 0), 1),),
    (((2, 2, 0, 0), 1), ((2, 2, 1, 1), -1)),
    (((2, 0, 2, 0), 1), ((2, 1, 2, 1), -1)),
    (((2, 0, 0, 2), 1), ((2, 1, 1, 2), -1)),
    (
        ((0, 1, 2, 1), 1),
        ((0, 2, 1, 1), -1),
        ((1, 1, 2, 0), -1),
        ((1, 2, 1, 0), 1),
    ),
    (
        ((0, 1, 1, 2), 1),
        ((0, 1, 2, 1), -1),
        ((1, 0, 1, 2), -1),
        ((1, 0, 2, 1), 1),
    ),
    (
        ((0, 1, 1, 2), 1),
        ((0, 2, 1, 1), -1),
        ((1, 1, 0, 2), -1),
        ((1, 2, 0, 1), 1),
    ),
    (
        ((0, 1, 0, 2), 1),
        ((0, 1, 2, 0), -1),
        ((1, 0, 0, 2), -1),
        ((1, 0, 2, 0), 1),
    ),
    (
        ((0, 1, 0, 1), 1),
        ((0, 1, 1, 0), -1),
        ((1, 0, 0, 1), -1),
        ((1, 0, 1, 0), 1),
    ),
    (
        ((0, 0, 2, 1), 1),
        ((0, 2, 0, 1), -1),
        ((1, 0, 2, 0), -1),
        ((1, 2, 0, 0), 1),
    ),
    (
        ((0, 0, 1, 2), 1),
        ((0, 2, 1, 0), -1),
        ((1, 0, 0, 2), -1),
        ((1, 2, 0, 0), 1),
    ),
    (
        ((0, 0, 1, 1), 1),
        ((0, 1, 0, 1), -1),
        ((1, 0, 1, 0), -1),
        ((1, 1, 0, 0), 1),
    ),
    (
        ((1, 1, 0, 1), 1),
        ((1, 1, 1, 0), -1),
        ((1, 2, 0, 1), -1),
        ((1, 2, 1, 0), 1),
        ((2, 1, 0, 1), -1),
        ((2, 1, 1, 0), 1),
    ),
    (
        ((1, 0, 1, 1), 1),
        ((1, 0, 1, 2), -1),
        ((1, 1, 0, 1), -1),
        ((1, 1, 0, 2), 1),
        ((2, 0, 1, 1), -1),
        ((2, 1, 0, 1), 1),
    ),
    (
        ((0, 0, 1, 0), 1),
        ((0, 0, 1, 2), -1),
        ((0, 1, 0, 0), -1),
        ((0, 1, 0, 2), 1),
        ((2, 0, 1, 0), -1),
        ((2, 1, 0, 0), 1),
    ),
    (
        ((0, 0, 0, 1), 1),
        ((0, 0, 1, 0), -1),
        ((0, 2, 0, 1), -1),
        ((0, 2, 1, 0), 1),
        ((2, 0, 0, 1), -1),
        ((2, 0, 1, 0), 1),
    ),
    (
        ((0, 0, 1, 1), 1),
        ((0, 1, 0, 0), -1),
        ((1, 0, 0, 0), -1),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
    ),
    (
        ((0, 0, 1, 0), 1),
        ((0, 1, 0, 1), -1),
        ((1, 0, 0, 0), 1),
        ((1, 0, 1, 0), -2),
        ((1, 0, 1, 1), 1),
        ((1, 1, 1, 0), 1),
    ),
    (
        ((0, 0, 1, 0), 1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 1, 0), -2),
        ((0, 1, 1, 1), 1),
        ((1, 0, 0, 1), -1),
        ((1, 1, 1, 0), 1),
    ),
    (
        ((0, 0, 0, 1), 1),
        ((0, 1, 1, 0), -1),
        ((1, 0, 0, 0), 1),
        ((1, 0, 0, 1), -2),
        ((1, 0, 1, 1), 1),
        ((1, 1, 0, 1), 1),
    ),
    (
        ((0, 0, 2, 0), 2),
        ((0, 2, 0, 0), -2),
        ((1, 0, 1, 1), 1),
        ((1, 0, 1, 2), -2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 0, 2), 2),
        ((1, 1, 2, 1), -1),
        ((1, 2, 1, 1), 1),
    ),
    (
        ((0, 0, 1, 0), 1),
        ((0, 0, 1, 2), -2),
        ((0, 0, 2, 0), 1),
        ((0, 1, 0, 0), -1),
        ((0, 1, 0, 2), 2),
        ((0, 2, 0, 0), -1),
        ((1, 1, 2, 1), -2),
        ((1, 2, 1, 1), 2),
    ),
    (
        ((0, 0, 0, 2), 2),
        ((0, 0, 2, 0), -2),
        ((1, 1, 0, 1), 1),
        ((1, 1, 1, 0), -1),
        ((1, 1, 1, 2), -1),
        ((1, 1, 2, 1), 1),
        ((1, 2, 0, 1), -2),
        ((1, 2, 1, 0), 2),
    ),
    (
        ((0, 0, 0, 1), 1),
        ((0, 0, 0, 2), 1),
        ((0, 0, 1, 0), -1),
        ((0, 0, 2, 0), -1),
        ((0, 2, 0, 1), -2),
        ((0, 2, 1, 0), 2),
        ((1, 1, 1, 2), -2),
        ((1, 1, 2, 1), 2),
    ),
    (
        ((1, 1, 0, 0), 1),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
        ((1, 2, 0, 0), -1),
        ((1, 2, 0, 1), 1),
        ((1, 2, 1, 0), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 1), 1),
        ((2, 1, 1, 0), 1),
        ((2, 2, 0, 0), 1),
        ((2, 2, 0, 1), -1),
        ((2, 2, 1, 0), -1),
    ),
    (
        ((1, 0, 1, 0), 1),
        ((1, 0, 1, 1), -1),
        ((1, 0, 2, 0), -1),
        ((1, 0, 2, 1), 1),
        ((1, 1, 1, 0), -1),
        ((1, 1, 2, 0), 1),
        ((2, 0, 1, 0), -1),
        ((2, 0, 1, 1), 1),
        ((2, 0, 2, 0), 1),
        ((2, 0, 2, 1), -1),
        ((2, 1, 1, 0), 1),
        ((2, 1, 2, 0), -1),
    ),
    (
        ((1, 0, 0, 1), 1),
        ((1, 0, 0, 2), -1),
        ((1, 0, 1, 1), -1),
        ((1, 0, 1, 2), 1),
        ((1, 1, 0, 1), -1),
        ((1, 1, 0, 2), 1),
        ((2, 0, 0, 1), -1),
        ((2, 0, 0, 2), 1),
        ((2, 0, 1, 1), 1),
        ((2, 0, 1, 2), -1),
        ((2, 1, 0, 1), 1),
        ((2, 1, 0, 2), -1),
    ),
    (
        ((0, 0, 1, 0), 1),
        ((0, 0, 1, 2), -1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 2), -1),
        ((0, 1, 1, 0), -1),
        ((0, 1, 1, 2), 1),
        ((2, 0, 1, 0), -1),
        ((2, 0, 1, 2), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 2), 1),
        ((2, 1, 1, 0), 1),
        ((2, 1, 1, 2), -1),
    ),
    (
        ((0, 0, 0, 1), 1),
        ((0, 0, 2, 1), -1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 1), -1),
        ((0, 1, 2, 0), -1),
        ((0, 1, 2, 1), 1),
        ((2, 0, 0, 1), -1),
        ((2, 0, 2, 1), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 1), 1),
        ((2, 1, 2, 0), 1),
        ((2, 1, 2, 1), -1),
    ),
    (
        ((0, 0, 0, 1), 1),
        ((0, 0, 1, 0), 1),
        ((0, 0, 1, 1), -1),
        ((0, 2, 0, 1), -1),
        ((0, 2, 1, 0), -1),
        ((0, 2, 1, 1), 1),
        ((2, 0, 0, 1), -1),
        ((2, 0, 1, 0), -1),
        ((2, 0, 1, 1), 1),
        ((2, 2, 0, 1), 1),
        ((2, 2, 1, 0), 1),
        ((2, 2, 1, 1), -1),
    ),
    (
        ((1, 0, 0, 0), 8),
        ((1, 0, 0, 1), -4),
        ((1, 0, 1, 0), -4),
        ((1, 0, 1, 1), 2),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
        ((1, 1, 1, 2), 3),
        ((1, 1, 2, 1), 3),
        ((1, 2, 0, 0), -12),
        ((1, 2, 0, 1), 6),
        ((1, 2, 1, 0), 6),
        ((2, 1, 1, 1), 6),
    ),
    (
        ((0, 0, 0, 1), 1),
        ((0, 0, 0, 2), -3),
        ((0, 0, 1, 0), -2),
        ((0, 0, 1, 1), 4),
        ((0, 0, 2, 1), -6),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 1), -2),
        ((0, 1, 1, 0), 4),
        ((0, 1, 1, 1), -8),
        ((0, 1, 2, 0), -6),
        ((0, 1, 2, 1), 12),
        ((0, 2, 0, 0), -3),
        ((2, 0, 0, 0), -6),
    ),
    (
        ((1, 0, 0, 0), 4),
        ((1, 0, 0, 1), -8),
        ((1, 0, 1, 0), -2),
        ((1, 0, 1, 1), 1),
        ((1, 0, 1, 2), 6),
        ((1, 1, 0, 0), -2),
        ((1, 1, 0, 1), 13),
        ((1, 1, 0, 2), -6),
        ((1, 1, 1, 0), -2),
        ((1, 1, 1, 2), -6),
        ((1, 1, 2, 1), 3),
        ((1, 2, 1, 1), 3),
        ((2, 0, 0, 1), 12),
        ((2, 1, 0, 1), -12),
    ),
    (
        ((1, 0, 0, 0), 4),
        ((1, 0, 0, 1), -2),
        ((1, 0, 1, 0), -2),
        ((1, 0, 1, 1), -8),
        ((1, 0, 2, 1), 12),
        ((1, 1, 0, 0), 4),
        ((1, 1, 0, 1), -5),
        ((1, 1, 1, 0), 1),
        ((1, 1, 1, 2), 3),
        ((1, 1, 2, 1), -3),
        ((1, 2, 0, 0), -12),
        ((1, 2, 0, 1), 6),
        ((1, 2, 1, 0), 6),
        ((2, 0, 1, 1), 12),
        ((2, 0, 2, 1), -24),
        ((2, 1, 2, 1), 12),
    ),
    (
        ((1, 0, 0, 0), 4),
        ((1, 0, 0, 1), -2),
        ((1, 0, 1, 0), -2),
        ((1, 0, 1, 1), -8),
        ((1, 0, 1, 2), 12),
        ((1, 1, 0, 0), 4),
        ((1, 1, 0, 1), 1),
        ((1, 1, 1, 0), -5),
        ((1, 1, 1, 2), -3),
        ((1, 1, 2, 1), 3),
        ((1, 2, 0, 0), -12),
        ((1, 2, 0, 1), 6),
        ((1, 2, 1, 0), 6),
        ((2, 0, 1, 1), 12),
        ((2, 0, 1, 2), -24),
        ((2, 1, 1, 2), 12),
    ),
    (
        ((1, 0, 0, 0), 4),
        ((1, 0, 0, 1), -2),
        ((1, 0, 1, 0), 4),
        ((1, 0, 1, 1), -5),
        ((1, 0, 2, 0), -12),
        ((1, 0, 2, 1), 6),
        ((1, 1, 0, 0), -2),
        ((1, 1, 0, 1), -8),
        ((1, 1, 1, 0), 1),
        ((1, 1, 1, 2), 3),
        ((1, 1, 2, 0), 6),
        ((1, 2, 0, 1), 12),
        ((1, 2, 1, 1), -3),
        ((2, 1, 0, 1), 12),
        ((2, 2, 0, 1), -24),
        ((2, 2, 1, 1), 12),
    ),
)

ATLAS_RELATION_INDICES = tuple(range(33)) + (34, 35, 36)
ROOT_TWO_RELATIONS = (
    (((2, 0, 1, 2), 1), ((2, 1, 0, 2), -1)),
    (((2, 0, 0, 2), 1), ((2, 1, 1, 2), -1)),
    (((2, 0, 2, 1), 1), ((2, 1, 2, 0), -1)),
    (((2, 0, 2, 0), 1), ((2, 1, 2, 1), -1)),
    (((2, 2, 0, 1), 1), ((2, 2, 1, 0), -1)),
    (((2, 2, 0, 0), 1), ((2, 2, 1, 1), -1)),
)


def load_parent():
    spec = importlib.util.spec_from_file_location("gld70_parent", PARENT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def full_relations(parent) -> list[list[int]]:
    relations = []
    for support in SPARSE_RELATIONS:
        relation = [0] * 81
        for indices, coefficient in support:
            relation[parent.LOCAL_INDEX[indices]] = coefficient
        relations.append(relation)
    return relations


def check_punctured_code(parent, relations):
    q_columns, residual_columns, pair_columns = parent.full_q_layer_columns(
        *parent.canonical_torus_star(1)
    )
    all_columns = q_columns + residual_columns + pair_columns
    basis = [all_columns[index] for index in parent.STAR_PIVOT_COLUMNS]
    punctured_rows = [
        row
        for row, indices in enumerate(parent.LOCAL_INDICES)
        if sum(indices[leaf] == 2 for leaf in (1, 2, 3)) <= 1
    ]
    erased_rows = [row for row in range(81) if row not in punctured_rows]
    assert (len(punctured_rows), len(erased_rows)) == (60, 21)
    assert all(not column[row] for column in pair_columns for row in punctured_rows)
    assert (
        parent.matrix_rank(
            [[column[row] for column in pair_columns] for row in erased_rows]
        )
        == 21
    )
    assert parent.column_rank(pair_columns) == 21
    quotient_columns = q_columns + residual_columns
    assert (
        parent.matrix_rank(
            [[column[row] for column in quotient_columns] for row in punctured_rows]
        )
        == 23
    )
    assert parent.column_rank(all_columns) == 44

    relation_matrix = sp.Matrix(relations)
    assert relation_matrix.rank() == 37
    assert all(
        sum(relation[row] * column[row] for row in range(81)) == 0
        for relation in relations
        for column in basis
    )
    assert all(not relation[row] for relation in relations for row in erased_rows)
    assert (
        sp.Matrix(
            [[relation[row] for row in punctured_rows] for relation in relations]
        ).rank()
        == 37
    )

    for leaf_permutation in permutations((1, 2, 3)):
        transformed = []
        for column in basis:
            new_column = [parent.Q(0)] * 81
            for row, indices in enumerate(parent.LOCAL_INDICES):
                new_indices = (
                    indices[0],
                    indices[leaf_permutation[0]],
                    indices[leaf_permutation[1]],
                    indices[leaf_permutation[2]],
                )
                new_column[parent.LOCAL_INDEX[new_indices]] = column[row]
            transformed.append(new_column)
        assert parent.column_rank(basis + transformed) == 44
    return all_columns, basis, punctured_rows


def incidence_equations(parent, relation_supports):
    variables = sp.symbols("a0:3 b0:3 c0:3 d0:3")
    a, b, c, d = (
        variables[0:3],
        variables[3:6],
        variables[6:9],
        variables[9:12],
    )
    equations = []
    for support in relation_supports:
        equations.append(
            sp.expand(
                sum(
                    coefficient
                    * a[indices[0]]
                    * b[indices[1]]
                    * c[indices[2]]
                    * d[indices[3]]
                    for indices, coefficient in support
                )
            )
        )
    return variables, (a, b, c, d), equations


def check_one_word_atlas(parent) -> int:
    selected = tuple(SPARSE_RELATIONS[index] for index in ATLAS_RELATION_INDICES)
    variables, (a, b, c, d), equations = incidence_equations(parent, selected)
    charts = 0
    for b_pivot, c_pivot, d_pivot, a_pivot in product(
        range(2), range(2), range(3), range(3)
    ):
        pivots = (a[a_pivot], b[b_pivot], c[c_pivot], d[d_pivot])
        substitutions = {pivot: 1 for pivot in pivots}
        remaining = tuple(variable for variable in variables if variable not in pivots)
        chart_equations = [
            sp.expand(equation.subs(substitutions)) for equation in equations
        ]
        chart_equations = [equation for equation in chart_equations if equation]
        groebner = sp.groebner(chart_equations, *remaining, order="grevlex")
        assert len(groebner.polys) == 1
        assert groebner.polys[0].total_degree() == 0
        assert groebner.polys[0].LC() != 0
        charts += 1
    assert charts == 36
    return charts


def check_root_slice_gates(parent, basis):
    punctured_by_root = []
    for root in range(3):
        rows = [
            parent.LOCAL_INDEX[indices]
            for indices in parent.LOCAL_INDICES
            if indices[0] == root and sum(indices[leaf] == 2 for leaf in (1, 2, 3)) <= 1
        ]
        projection_rank = sp.Matrix(
            [[int(column[row]) for column in basis] for row in rows]
        ).rank()
        punctured_by_root.append(len(rows) - projection_rank)
    assert punctured_by_root == [4, 4, 6]

    root_two = []
    for support in ROOT_TWO_RELATIONS:
        relation = [0] * 81
        for indices, coefficient in support:
            relation[parent.LOCAL_INDEX[indices]] = coefficient
        assert all(
            sum(relation[row] * column[row] for row in range(81)) == 0
            for column in basis
        )
        root_two.append(relation)

    x = sp.symbols("x0:3")
    p = sp.symbols("p0:3")
    y = sp.symbols("y0:3")
    q = sp.symbols("q0:3")
    z = sp.symbols("z0:3")
    r = sp.symbols("r0:3")
    leaves = (
        sp.Matrix([[1, 1, 1], x, p]),
        sp.Matrix([[1, 1, 1], y, q]),
        sp.Matrix([[1, 1, 1], z, r]),
    )
    actual = sp.Matrix(
        [
            [
                sp.expand(
                    sum(
                        relation[parent.LOCAL_INDEX[(2, i, j, k)]]
                        * leaves[0][i, component]
                        * leaves[1][j, component]
                        * leaves[2][k, component]
                        for i, j, k in product(range(3), repeat=3)
                    )
                )
                for component in range(3)
            ]
            for relation in root_two
        ]
    )
    expected = sp.Matrix(
        [
            [r[k] * (y[k] - x[k]) for k in range(3)],
            [r[k] * (1 - x[k] * y[k]) for k in range(3)],
            [q[k] * (z[k] - x[k]) for k in range(3)],
            [q[k] * (1 - x[k] * z[k]) for k in range(3)],
            [p[k] * (z[k] - y[k]) for k in range(3)],
            [p[k] * (1 - y[k] * z[k]) for k in range(3)],
        ]
    )
    assert all(sp.expand(entry) == 0 for entry in actual - expected)
    return tuple(punctured_by_root)


def check_eisenstein_gate(parent):
    q_columns, residual_columns, _pair_columns = parent.full_q_layer_columns(
        *parent.canonical_torus_star(1)
    )
    gamma = sp.symbols("gamma")
    x = sp.symbols("u0:8")
    y = sp.symbols("v0:8")
    tensor = {}
    for indices in product(range(2), repeat=4):
        row = parent.LOCAL_INDEX[indices]
        value = gamma * int(q_columns[0][row])
        for residual in range(2):
            parameters = x if residual == 0 else y
            for mode in range(4):
                for index in range(2):
                    column = residual_columns[residual * 12 + mode * 3 + index]
                    value += parameters[2 * mode + index] * int(column[row])
        tensor[indices] = sp.expand(value)

    alpha = [x[2 * mode] - y[2 * mode] for mode in range(4)]
    beta = [x[2 * mode + 1] - y[2 * mode + 1] for mode in range(4)]
    norms = [sp.expand(a * a - a * b + b * b) for a, b in zip(alpha, beta)]
    expected = (
        16 * (norms[0] - norms[1]) * (norms[2] - norms[3]),
        16 * (norms[0] - norms[2]) * (norms[1] - norms[3]),
        16 * (norms[0] - norms[3]) * (norms[1] - norms[2]),
    )
    determinants = []
    for left_modes in ((0, 1), (0, 2), (0, 3)):
        right_modes = tuple(mode for mode in range(4) if mode not in left_modes)
        matrix = sp.Matrix(
            4,
            4,
            lambda row, column, left_modes=left_modes, right_modes=right_modes: tensor[
                tuple(
                    ((row >> (1 - left_modes.index(mode))) & 1)
                    if mode in left_modes
                    else ((column >> (1 - right_modes.index(mode))) & 1)
                    for mode in range(4)
                )
            ],
        )
        determinants.append(sp.factor(matrix.det(method="domain-ge")))
    assert all(
        sp.expand(actual - target) == 0
        for actual, target in zip(determinants, expected, strict=True)
    )
    return tuple(len(sp.Poly(value).terms()) for value in determinants)


def coefficient_matrix(parent, relations, leaves):
    return sp.Matrix(
        [
            [
                sum(
                    relation[parent.LOCAL_INDEX[(root, i, j, k)]]
                    * leaves[0][i, component]
                    * leaves[1][j, component]
                    * leaves[2][k, component]
                    for i, j, k in product(range(3), repeat=3)
                )
                for root in range(3)
                for component in range(3)
            ]
            for relation in relations
        ]
    )


def check_secant_two_boundary(parent, relations, all_columns):
    leaf = sp.Matrix([[1, 1, 1], [-1, 0, 0], [0, -1, 0]])
    centre = sp.Matrix([[0, 1, -1], [0, 0, 0], [0, 0, 1]])
    leaves = (leaf, leaf, leaf)
    matrix = coefficient_matrix(parent, relations, leaves)
    kernel = matrix.nullspace()
    assert leaf.det() == 1
    assert matrix.rank() == 8
    assert kernel == [sp.Matrix([0, 1, -1, 0, 0, 0, 0, 0, 1])]
    assert centre.det() == 0 and centre.rank() == 2
    pair_columns = [1, 4, 7, 2, 5, 8]
    assert matrix[:, pair_columns].rank() == 5

    tensor = [
        sum(
            centre[root, component]
            * leaf[i, component]
            * leaf[j, component]
            * leaf[k, component]
            for component in range(3)
        )
        for root, i, j, k in parent.LOCAL_INDICES
    ]
    raw_coefficients = [parent.Q(0)] * 79
    raw_coefficients[0] = parent.Q(-1, 6)
    for residual_index in range(0, 24, 3):
        raw_coefficients[1 + residual_index] = parent.Q(-1, 12)
    for pair_index, coefficient in (
        (0, parent.Q(-5, 12)),
        (2, parent.Q(1, 4)),
        (9, parent.Q(-5, 12)),
        (18, parent.Q(-5, 12)),
    ):
        raw_coefficients[25 + pair_index] = coefficient
    replay = [
        sum(
            coefficient * column[row]
            for coefficient, column in zip(raw_coefficients, all_columns, strict=True)
        )
        for row in range(81)
    ]
    assert replay == tensor
    rational_tensor = [parent.Q(entry) for entry in tensor]
    assert parent.epsilon(rational_tensor) == 0
    assert tuple(
        parent.balanced_flattening_rank(rational_tensor, modes)
        for modes in ((0, 1), (0, 2), (0, 3))
    ) == (2, 2, 2)
    return matrix.rank(), centre.rank(), matrix[:, pair_columns].rank()


def main() -> None:
    parent = load_parent()
    relations = full_relations(parent)
    all_columns, basis, punctured_rows = check_punctured_code(parent, relations)
    atlas_charts = check_one_word_atlas(parent)
    slice_gates = check_root_slice_gates(parent, basis)
    norm_terms = check_eisenstein_gate(parent)
    boundary = check_secant_two_boundary(parent, relations, all_columns)
    result = {
        "status": "exact_parent_theorem_not_global_resolution",
        "global_conjecture": "UNRESOLVED",
        "star_dimension": 44,
        "pair_erasure_dimension": 21,
        "punctured_ambient_dimension": len(punctured_rows),
        "punctured_nuisance_dimension": 23,
        "syndrome_dimension": len(relations),
        "one_word_non_erasure_atlas_charts": atlas_charts,
        "root_slice_gate_dimensions": slice_gates,
        "binary_eisenstein_gate_term_counts": norm_terms,
        "nonhidden_secant_two_control_ranks": boundary,
        "determinant_safe_three_word_statement_proved": False,
    }
    print("four-root torus-star punctured syndrome and Eisenstein gate: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
