#!/usr/bin/env python3
"""Verify exact B_all properness fixtures for the fixed-pencil equality sources.

The script checks the rank/codimension bookkeeping for the generic and
rank-degenerate q=20 strata and constructs exact full balanced sensors inside
their four-K5 incidence fibres.  The component ledger and its geometric
exhaustion are owned by the accompanying theorem; this script supplies the
nonvanishing witnesses only and makes no global Krenn--Gu claim.
"""

from __future__ import annotations

import json
import random
from itertools import combinations, permutations, product

import sympy as sp


CHARTS = tuple(range(4))
VERTICES = tuple(range(4))
PAIRS = tuple(combinations(VERTICES, 2))
EXPECTED_MINORS = {
    "A_generic": "901659762416043994210084799/108900000",
    "A_one_collinear_cross_incompatible": "-1448448441823432644071/675",
    "A_one_collinear_cross_compatible": "-2274084059487166952/5",
    "A_both_collinear_cross_compatible": "2164688055123072",
    "B_generic": "-345919614259292012/3375",
    "B_one_collinear": "-11187289987739049817/144000",
    "B_both_collinear_cross_incompatible": "-1772405772269592",
    "B_both_collinear_cross_compatible": "-245747897116304/375",
    "C_two_one_three_synchronized_plus_line": "13392112152672",
    "D_injective_three_synchronized_plus_line": "1987165331179776",
}


def evaluation(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[row] * right[column] for row in range(3) for column in range(3)]
    )


def tuple_rank(vectors: tuple[sp.Matrix, ...]) -> int:
    return sp.Matrix.hstack(*vectors).rank()


def edge_ranks(roots: tuple[tuple[sp.Matrix, ...], ...]) -> tuple[int, ...]:
    return tuple(
        tuple_rank(
            tuple(evaluation(roots[chart][left], roots[chart][right]) for chart in CHARTS)
        )
        for left, right in PAIRS
    )


def p1_vector(value: int) -> sp.Matrix:
    return sp.Matrix((1, value, 0))


def generic_p2_vectors() -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix(value)
        for value in ((1, 2, 1), (2, 1, 1), (3, 4, 1), (5, 1, 1))
    )


def other_generic_p2_vectors() -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix(value)
        for value in ((2, 1, 1), (1, 3, 1), (4, 2, 1), (3, 5, 1))
    )


def roots_from_columns(
    first: tuple[sp.Matrix, ...],
    second: tuple[sp.Matrix, ...],
    third: tuple[sp.Matrix, ...],
    fourth: tuple[sp.Matrix, ...],
) -> tuple[tuple[sp.Matrix, ...], ...]:
    return tuple(
        (first[chart], second[chart], third[chart], fourth[chart])
        for chart in CHARTS
    )


def q20_fixtures() -> dict[str, tuple[tuple[sp.Matrix, ...], ...]]:
    e2 = sp.Matrix((0, 0, 1))
    synchronized_e2 = (e2,) * 4
    p1_xy = tuple(p1_vector(value) for value in (1, 2, 3, 4))
    line_xyz = tuple(
        sp.Matrix((1, value, -1 - value)) for value in (1, 2, 3, 4)
    )
    line_xyz_other = tuple(
        sp.Matrix((1, value, -1 - value)) for value in (1, 3, 4, 7)
    )
    line_xyz_mobius = tuple(
        sp.Matrix((1 + value, value, -1 - 2 * value))
        for value in (1, 2, 3, 4)
    )
    generic_b = generic_p2_vectors()
    generic_c = other_generic_p2_vectors()
    synchronized_xy = (sp.Matrix((1, 1, 0)),) * 4
    synchronized_xyz = (sp.Matrix((1, 2, 1)),) * 4
    synchronized_yz = (sp.Matrix((0, 1, 1)),) * 4
    synchronized_xz = (sp.Matrix((1, 0, 1)),) * 4

    return {
        "A_generic": roots_from_columns(
            synchronized_e2, p1_xy, generic_b, generic_c
        ),
        "A_one_collinear_cross_incompatible": roots_from_columns(
            synchronized_e2,
            p1_xy,
            line_xyz_other,
            generic_c,
        ),
        "A_one_collinear_cross_compatible": roots_from_columns(
            synchronized_e2, p1_xy, line_xyz_mobius, generic_c
        ),
        "A_both_collinear_cross_compatible": roots_from_columns(
            synchronized_e2, p1_xy, line_xyz_mobius, line_xyz
        ),
        "B_generic": roots_from_columns(
            synchronized_e2, synchronized_xy, generic_b, generic_c
        ),
        "B_one_collinear": roots_from_columns(
            synchronized_e2, synchronized_xy, line_xyz_mobius, generic_c
        ),
        "B_both_collinear_cross_incompatible": roots_from_columns(
            synchronized_e2,
            synchronized_xy,
            line_xyz,
            line_xyz_other,
        ),
        "B_both_collinear_cross_compatible": roots_from_columns(
            synchronized_e2, synchronized_xy, line_xyz, line_xyz_mobius
        ),
        "C_two_one_three_synchronized_plus_line": roots_from_columns(
            synchronized_e2, synchronized_xy, synchronized_xyz, line_xyz
        ),
        "D_injective_three_synchronized_plus_line": roots_from_columns(
            synchronized_yz, synchronized_xy, synchronized_xz, line_xyz
        ),
    }


def expected_compensation() -> dict[str, dict[str, object]]:
    # c_rank is codimension inside the relevant generic q=20 root stratum.
    # A has Delta=0.  B has Delta=3.
    cases = {
        "A_generic": (0, 0),
        "A_one_collinear_cross_incompatible": (0, 2),
        "A_one_collinear_cross_compatible": (0, 3),
        "A_both_collinear_cross_compatible": (0, 6),
        "B_generic": (3, 0),
        "B_one_collinear": (3, 2),
        "B_both_collinear_cross_incompatible": (3, 4),
        "B_both_collinear_cross_compatible": (3, 5),
        "C_two_one_three_synchronized_plus_line": (9, 2),
        "D_injective_three_synchronized_plus_line": (9, 2),
    }
    result: dict[str, dict[str, object]] = {}
    for name, roots in q20_fixtures().items():
        ranks = edge_ranks(roots)
        delta, c_rank = cases[name]
        compensated = delta + c_rank + sum(ranks)
        result[name] = {
            "ranks_01_02_03_12_13_23": ranks,
            "Delta": delta,
            "c_rank": c_rank,
            "compensated_q": compensated,
        }
        assert compensated >= 20
    assert result["A_generic"]["compensated_q"] == 20
    assert result["B_generic"]["compensated_q"] == 20
    assert result["B_one_collinear"]["compensated_q"] == 20
    assert result["B_both_collinear_cross_incompatible"]["compensated_q"] == 20
    assert result["B_both_collinear_cross_compatible"]["compensated_q"] == 20
    assert result["C_two_one_three_synchronized_plus_line"]["compensated_q"] == 20
    assert result["D_injective_three_synchronized_plus_line"]["compensated_q"] == 20
    return result


def p1_segre_determinant() -> sp.Expr:
    a = sp.symbols("a0:4")
    b = sp.symbols("b0:4")
    columns = [sp.Matrix((1, b[t], a[t], a[t] * b[t])) for t in CHARTS]
    determinant = sp.factor(sp.Matrix.hstack(*columns).det())
    assert determinant != 0
    # It is alternating separately in each labelled quadruple and is the
    # single full-support dependence equation on the P1 x P1 chart.
    assert sp.Poly(determinant, *a, *b).total_degree() == 4
    return determinant


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second), *matching)


def parity_subsets() -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for size in (0, 2, 4)
        for subset in combinations(VERTICES, size)
    )


def sensor_matrix(
    root_blocks: dict[tuple[int, int], sp.Matrix],
    cross_covectors: dict[tuple[int, int], sp.Matrix],
) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for selected_nonroots in parity_subsets():
        entries = []
        for colours in product(range(3), repeat=4):
            value = sp.Integer(0)
            for selected_roots in combinations(VERTICES, len(selected_nonroots)):
                remaining = tuple(root for root in VERTICES if root not in selected_roots)
                for target_order in permutations(selected_nonroots):
                    cross_value = sp.prod(
                        cross_covectors[(root, nonroot)][colours[root]]
                        for root, nonroot in zip(selected_roots, target_order, strict=True)
                    )
                    for matching in perfect_matchings(remaining):
                        root_value = sp.prod(
                            root_blocks[tuple(sorted((first, second)))][
                                colours[first], colours[second]
                            ]
                            for first, second in matching
                        )
                        value += cross_value * root_value
            entries.append(sp.expand(value))
        columns.append(sp.Matrix(entries))
    return sp.Matrix.hstack(*columns)


def random_kernel_block(
    roots: tuple[tuple[sp.Matrix, ...], ...],
    left: int,
    right: int,
    rng: random.Random,
) -> sp.Matrix:
    equations = sp.Matrix.vstack(
        *[
            evaluation(roots[chart][left], roots[chart][right]).T
            for chart in CHARTS
        ]
    )
    kernel = equations.nullspace()
    assert kernel
    for _ in range(20):
        coefficients = [rng.randint(-3, 3) for _ in kernel]
        vector = sum(
            (coefficient * basis for coefficient, basis in zip(coefficients, kernel, strict=True)),
            sp.zeros(9, 1),
        )
        if vector != sp.zeros(9, 1):
            block = sp.Matrix(3, 3, list(vector))
            assert all(
                (roots[chart][left].T * block * roots[chart][right])[0] == 0
                for chart in CHARTS
            )
            return block
    raise AssertionError("failed to sample a nonzero root-block kernel element")


def random_annihilator(root: sp.Matrix, rng: random.Random) -> sp.Matrix:
    """Sample a nonzero covector in the exact annihilator of one root."""
    kernel = root.T.nullspace()
    assert len(kernel) == 2
    for _ in range(20):
        coefficients = [rng.randint(-3, 3) for _ in kernel]
        vector = sum(
            (
                coefficient * basis
                for coefficient, basis in zip(coefficients, kernel, strict=True)
            ),
            sp.zeros(3, 1),
        )
        if vector != sp.zeros(3, 1):
            assert (root.T * vector)[0] == 0
            return vector
    raise AssertionError("failed to sample a nonzero annihilator covector")


def find_full_sensor(
    roots: tuple[tuple[sp.Matrix, ...], ...], seed: int
) -> dict[str, object]:
    rng = random.Random(seed)
    for attempt in range(1, 81):
        root_blocks = {
            pair: random_kernel_block(roots, pair[0], pair[1], rng) for pair in PAIRS
        }
        cross_covectors = {
            (root, nonroot): random_annihilator(roots[nonroot][root], rng)
            for root in VERTICES
            for nonroot in VERTICES
        }
        if any(vector == sp.zeros(3, 1) for vector in cross_covectors.values()):
            continue
        assert all(
            (roots[chart][root].T * cross_covectors[(root, chart)])[0] == 0
            for root in VERTICES
            for chart in CHARTS
        )
        sensor = sensor_matrix(root_blocks, cross_covectors)
        rank = sensor.rank()
        if rank == 8:
            selected_rows = list(sp.Matrix(sensor.T).rref()[1])
            assert len(selected_rows) == 8
            minor = sensor.extract(selected_rows, range(8)).det()
            assert minor != 0
            return {
                "attempt": attempt,
                "rank": rank,
                "selected_rows": selected_rows,
                "minor": str(minor),
            }
    raise AssertionError("no exact full sensor found in 80 deterministic attempts")


def main() -> None:
    compensation = expected_compensation()
    determinant = p1_segre_determinant()
    full_sensors = {
        name: find_full_sensor(roots, seed=20260830 + index)
        for index, (name, roots) in enumerate(q20_fixtures().items())
    }
    assert {
        name: fixture["minor"] for name, fixture in full_sensors.items()
    } == EXPECTED_MINORS
    result = {
        "status": "exact_fixed_pencil_b_all_properness_fixtures",
        "global_conjecture": "UNRESOLVED",
        "compensation": compensation,
        "p1_segre_dependence_polynomial": str(determinant),
        "full_sensor_search": full_sensors,
        "scope_limit": (
            "q=20 equality sources and displayed degenerations only; the "
            "component exhaustion and multi-pencil closure are separate"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
