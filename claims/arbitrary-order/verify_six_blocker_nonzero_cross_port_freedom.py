#!/usr/bin/env python3
"""Verify local port freedom under nonzero exchanged-root coupling."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_NONZERO_CROSS_PORT_FREEDOM.md"


def profile(rows: sp.Matrix) -> int:
    rank = rows.rank()
    mask = 0
    for colour in range(3):
        coordinate = sp.eye(3).row(colour)
        if rows.col_join(coordinate).rank() == rank:
            mask |= 1 << colour
    return mask


def blocker_root_rows() -> tuple[sp.Matrix, ...]:
    e0, e1, e2 = (sp.eye(3).row(index) for index in range(3))
    exceptional = (
        sp.Matrix.vstack(e1, e2, e1 + e2, e1 + 2 * e2, e1 - e2, e0),
        sp.Matrix.vstack(e0, e2, e0 + e2, e0 + 2 * e2, e0 - e2, e1),
        sp.Matrix.vstack(e0, e1, e0 + e1, e0 + 2 * e1, e0 - e1, e2),
    )
    full = sp.Matrix.vstack(
        e0,
        e1,
        e2,
        e0 + e1 + e2,
        e0 + 2 * e1 + 3 * e2,
        3 * e0 + 2 * e1 + e2,
    )
    return (*exceptional, full, full.copy(), full.copy())


def port_rows() -> tuple[tuple[sp.Matrix, ...], tuple[sp.Matrix, ...]]:
    port_b = tuple(
        sp.Matrix([row])
        for row in (
            (1, 1, 0),
            (0, 1, 1),
            (1, 0, 1),
            (2, 1, 1),
            (1, 3, 1),
            (1, 1, 4),
        )
    )
    port_a = tuple(
        sp.Matrix([row])
        for row in (
            (0, 1, 2),
            (2, 0, 1),
            (1, 2, 0),
            (1, 1, 2),
            (2, 1, 1),
            (1, 2, 1),
        )
    )
    return port_b, port_a


def permanent(matrix: tuple[tuple[sp.Rational, ...], ...]) -> sp.Rational:
    states: dict[int, sp.Rational] = {0: sp.S.One}
    for column in range(6):
        next_states: dict[int, sp.Rational] = {}
        for mask, value in states.items():
            for row in range(6):
                if mask & (1 << row):
                    continue
                new_mask = mask | (1 << row)
                next_states[new_mask] = next_states.get(new_mask, sp.S.Zero) + (
                    value * matrix[row][column]
                )
        states = next_states
    return sp.cancel(states.get(63, sp.S.Zero))


def contraction_tensor(modes: tuple[sp.Matrix, ...]) -> tuple[sp.Rational, ...]:
    coefficients = []
    for word in itertools.product(range(3), repeat=6):
        scalar_matrix = tuple(
            tuple(modes[mode][row, word[mode]] for mode in range(6)) for row in range(6)
        )
        coefficients.append(permanent(scalar_matrix))
    return tuple(coefficients)


def symbolic_normal_forms() -> None:
    # Once independent x,z are chosen as e0,e1, every common-root covector
    # annihilating both belongs to the one-dimensional space <e2^*>.
    beta = sp.symbols("beta", nonzero=True)
    gamma = sp.symbols("gamma")
    h = sp.symbols("h", nonzero=True)
    x = sp.Matrix([1, 0, 0])
    z = sp.Matrix([0, 1, 0])
    common = sp.Matrix([[0, 0, h]])
    cross = sp.Matrix([[beta, 0, gamma]])
    assert (cross * x)[0] == beta
    assert (cross * z)[0] == 0
    assert common * x == sp.zeros(1, 1)
    assert common * z == sp.zeros(1, 1)
    assert common.rank() == 1
    total = sp.Matrix.vstack(common, cross)
    assert total.rank() == 2
    assert total.nullspace() == [z]

    # Universal section of W -> (W(x,-), W(z,-)).
    r = sp.Matrix([sp.symbols("r0:3")])
    s = sp.Matrix([sp.symbols("s0:3")])
    alpha = sp.Matrix([1, 0, 0])
    zeta = sp.Matrix([0, 1, 0])
    block = alpha * r + zeta * s
    assert x.T * block == r
    assert z.T * block == s


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero local structural theorem",
        "dim H_b <= 1",
        "12*14-12*18=-48 != 0",
        "This model is deliberately only local",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    for dependency in (
        "SIX_BLOCKER_MAXIMAL_OVERLAP_PORT_SWAP_COLLAPSE.md",
        "SIX_BLOCKER_ADMISSIBLE_QUOTIENT_CATALOGUE.md",
        "ONE_NONBLOCKER_SURPLUS_PERMANENT_EXTRACTION.md",
    ):
        assert (ROOT / dependency).exists()

    symbolic_normal_forms()

    x = sp.Matrix([1, 1, 1])
    z_a = sp.Matrix([1, 2, 3])
    z_b = sp.Matrix([1, 3, 2])
    h_a = sp.Matrix([1, -2, 1])
    h_b = sp.Matrix([-1, -1, 2])
    alpha_a = sp.Matrix([2, -1, 0])
    zeta_a = sp.Matrix([-1, 1, 0])
    alpha_b = sp.Matrix([sp.Rational(3, 2), sp.Rational(-1, 2), 0])
    zeta_b = sp.Matrix([sp.Rational(-1, 2), sp.Rational(1, 2), 0])

    for vector in (x, z_a, z_b):
        assert all(entry != 0 for entry in vector)
    assert (h_a.T * x)[0] == (h_a.T * z_a)[0] == 0
    assert (h_b.T * x)[0] == (h_b.T * z_b)[0] == 0
    for root, port, alpha, zeta in (
        (x, z_a, alpha_a, zeta_a),
        (x, z_b, alpha_b, zeta_b),
    ):
        assert (alpha.T * root)[0] == 1
        assert (alpha.T * port)[0] == 0
        assert (zeta.T * root)[0] == 0
        assert (zeta.T * port)[0] == 1

    cross_block = alpha_a * alpha_b.T
    assert cross_block != sp.zeros(3)
    assert (x.T * cross_block * x)[0] == 1
    assert (x.T * cross_block * z_b)[0] == 0
    assert (z_a.T * cross_block * x)[0] == 0

    section = sp.Matrix([1, 0, 0])
    common_to_a = section * h_a.T
    common_to_b = section * h_b.T
    common_pair = sp.diag(1, -1, 0)
    for block in (common_to_a, common_to_b, common_pair):
        assert block != sp.zeros(3)
        assert (x.T * block * x)[0] == 0

    nonblocker_b = sp.Matrix.vstack(*(h_b.T for _ in range(4)), alpha_b.T)
    nonblocker_a = sp.Matrix.vstack(*(h_a.T for _ in range(4)), alpha_a.T)
    assert nonblocker_b.rank() == nonblocker_a.rank() == 2
    assert len(nonblocker_b.nullspace()) == len(nonblocker_a.nullspace()) == 1
    assert nonblocker_b * z_b == sp.zeros(5, 1)
    assert nonblocker_a * z_a == sp.zeros(5, 1)
    assert profile(nonblocker_b) == profile(nonblocker_a) == 0

    roots = blocker_root_rows()
    port_b, port_a = port_rows()
    left_modes = []
    right_modes = []
    for mode, root_rows in enumerate(roots):
        left = sp.Matrix.vstack(root_rows[:5, :], port_b[mode])
        right = sp.Matrix.vstack(root_rows[:4, :], root_rows[5, :], port_a[mode])
        assert left.rank() == right.rank() == 3
        left_modes.append(left)
        right_modes.append(right)

        # The common root rows use a section with x^T section=1.
        for common_index in range(4):
            covector = root_rows.row(common_index)
            block = section * covector
            assert block != sp.zeros(3)
            assert x.T * block == covector

        # One edge block simultaneously realizes the exchanged root and port
        # rows, as in the universal section lemma.
        row_a = root_rows.row(4)
        row_b = root_rows.row(5)
        block_a = alpha_a * row_a + zeta_a * port_a[mode]
        block_b = alpha_b * row_b + zeta_b * port_b[mode]
        assert block_a != sp.zeros(3)
        assert block_b != sp.zeros(3)
        assert x.T * block_a == row_a
        assert z_a.T * block_a == port_a[mode]
        assert x.T * block_b == row_b
        assert z_b.T * block_b == port_b[mode]

    left_profiles = tuple(profile(matrix[:5, :]) for matrix in roots)
    right_profiles = tuple(profile(matrix[[0, 1, 2, 3, 5], :]) for matrix in roots)
    left_root_ranks = tuple(matrix[:5, :].rank() for matrix in roots)
    right_root_ranks = tuple(matrix[[0, 1, 2, 3, 5], :].rank() for matrix in roots)
    assert left_profiles == (6, 5, 3, 7, 7, 7)
    assert right_profiles == (7, 7, 7, 7, 7, 7)
    assert left_root_ranks == (2, 2, 2, 3, 3, 3)
    assert right_root_ranks == (3, 3, 3, 3, 3, 3)

    # No single six-output linear map sends all left local maps to their
    # corresponding right local maps.
    transform_entries = sp.symbols("q0:36")
    transform = sp.Matrix(6, 6, transform_entries)
    transform_equations = []
    for left, right in zip(left_modes, right_modes):
        transform_equations.extend(transform * left - right)
    coefficient_matrix, target = sp.linear_eq_to_matrix(
        transform_equations, transform_entries
    )
    assert coefficient_matrix.rank() == 36
    assert coefficient_matrix.row_join(target).rank() == 37
    assert sp.linsolve((coefficient_matrix, target), transform_entries) == sp.EmptySet

    left_tensor = contraction_tensor(tuple(left_modes))
    right_tensor = contraction_tensor(tuple(right_modes))
    assert len(left_tensor) == len(right_tensor) == 3**6
    assert (left_tensor[1], right_tensor[1]) == (12, 18)
    assert (left_tensor[3], right_tensor[3]) == (12, 14)
    proportionality_minor = left_tensor[1] * right_tensor[3] - (
        left_tensor[3] * right_tensor[1]
    )
    assert proportionality_minor == -48
    assert sum(value != 0 for value in left_tensor) == 476
    assert sum(value != 0 for value in right_tensor) == 476

    ghz_left = tuple(z_b[colour] * x[colour] ** 5 for colour in range(3))
    ghz_right = tuple(z_a[colour] * x[colour] ** 5 for colour in range(3))
    assert ghz_left == (1, 3, 2)
    assert ghz_right == (1, 2, 3)
    assert ghz_left[0] * ghz_right[1] - ghz_left[1] * ghz_right[0] == -1

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "exchanged_cross_coupling": 1,
                "common_incident_span_bound": 1,
                "left_profiles": left_profiles,
                "right_profiles": right_profiles,
                "left_root_map_ranks": left_root_ranks,
                "right_root_map_ranks": right_root_ranks,
                "common_output_map_system_ranks": [36, 37],
                "target_words_checked_per_tensor": 3**6,
                "left_nonzero_coefficients": 476,
                "right_nonzero_coefficients": 476,
                "proportionality_minor": int(proportionality_minor),
                "local_p6_proportionality_forced": False,
                "local_incident_blocks_realized": True,
                "global_matching_identity_realized": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
