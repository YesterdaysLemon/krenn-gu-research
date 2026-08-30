#!/usr/bin/env python3
"""Independent exact q=20 fixtures, ruling circuits, and one B_all audit.

The construction is written from the definitions with SymPy and imports no
Kestrel or repository research module.  It replays the ten displayed q=20
fixture/deformation types, builds exact balanced sensor matrices, and checks
the diagonal-complete m=4 all-balanced rank-drop mechanism.  The complementary
ruling fixture is a mechanism audit (active-active and active-structural), not
a q<=22 survivor or a Krenn--Gu counterexample.

The B_all calculation is intentionally scoped: it checks the exact m=4
diagonal-complete family on all 70 ordered balanced 4|4 cuts and the symbolic
quadratic divisibility behind the rank bound.  It does not classify arbitrary
members of B_all or impose the full witness equations.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path

import sympy as sp


CHARTS = tuple(range(4))
VERTICES = tuple(range(4))
PAIRS = tuple(combinations(VERTICES, 2))
INPUT_PATH = Path(__file__).with_name(
    "balanced_m3_full_sensor_q22_near_frontier_input_v1.json"
)
INPUT_SHA256 = (
    "d5b821a47f8164f56e1254e9400ff1875bab650ce5e64be3a0e191129bed541a"
)
RECORDS_SHA256 = (
    "650e8ed6e2165a3066fc9ba1cda30709b9f6e24fe599a6860afb2b1deb471550"
)


def evaluation(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[row] * right[column] for row in range(3) for column in range(3)]
    )


def tuple_rank(vectors: tuple[sp.Matrix, ...]) -> int:
    return sp.Matrix.hstack(*vectors).rank()


def edge_ranks(
    roots: tuple[tuple[sp.Matrix, ...], ...]
) -> tuple[int, ...]:
    return tuple(
        tuple_rank(
            tuple(
                evaluation(roots[chart][left], roots[chart][right])
                for chart in CHARTS
            )
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
            synchronized_e2, p1_xy, line_xyz_other, generic_c
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
            synchronized_e2, synchronized_xy, line_xyz, line_xyz_other
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


EXPECTED_COMPENSATION = {
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


def parity_subsets(vertex_count: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for size in range(vertex_count + 1)
        if size % 2 == vertex_count % 2
        for subset in combinations(range(vertex_count), size)
    )


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((first, second), *matching)


def companion_scalar(m: int, subset_size: int) -> int:
    return (
        comb(m, subset_size)
        * factorial(subset_size)
        * odd_double_factorial(m - subset_size - 1)
    )


def odd_double_factorial(value: int) -> int:
    if value == -1:
        return 1
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def companion_polynomials(
    m: int,
    z_vectors: tuple[tuple[int | sp.Expr, int | sp.Expr, int | sp.Expr], ...],
) -> tuple[tuple[int, ...], list[sp.Expr]]:
    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)
    subsets = parity_subsets(m)
    columns = []
    for subset in subsets:
        polynomial = sp.Integer(companion_scalar(m, len(subset)))
        polynomial *= (x**2 + y**2 + z**2) ** ((m - len(subset)) // 2)
        for target in subset:
            polynomial *= sum(
                z_vectors[target][colour] * variables[colour]
                for colour in range(3)
            )
        columns.append(sp.expand(polynomial))
    return subsets, columns


def polynomial_rank(polynomials: list[sp.Expr], degree: int) -> int:
    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)
    monomials = [
        variables[0] ** first
        * variables[1] ** second
        * variables[2] ** (degree - first - second)
        for first in range(degree + 1)
        for second in range(degree - first + 1)
    ]
    matrix = sp.Matrix(
        [
            [
                sp.Poly(polynomial, *variables).coeff_monomial(monomial)
                for polynomial in polynomials
            ]
            for monomial in monomials
        ]
    )
    return matrix.rank()


def sensor_matrix(
    root_blocks: dict[tuple[int, int], sp.Matrix],
    cross_covectors: dict[tuple[int, int], sp.Matrix],
) -> sp.Matrix:
    columns = []
    for selected_nonroots in parity_subsets(4):
        entries = []
        for colours in product(range(3), repeat=4):
            value = sp.Integer(0)
            for selected_roots in combinations(VERTICES, len(selected_nonroots)):
                remaining = tuple(
                    root for root in VERTICES if root not in selected_roots
                )
                for target_order in permutations(selected_nonroots):
                    cross_value = sp.prod(
                        cross_covectors[(root, nonroot)][colours[root]]
                        for root, nonroot in zip(
                            selected_roots, target_order, strict=True
                        )
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
            (
                coefficient * basis
                for coefficient, basis in zip(coefficients, kernel, strict=True)
            ),
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


def exact_full_sensor(
    roots: tuple[tuple[sp.Matrix, ...], ...], seed: int
) -> dict[str, object]:
    rng = random.Random(seed)
    for attempt in range(1, 81):
        root_blocks = {
            pair: random_kernel_block(roots, pair[0], pair[1], rng)
            for pair in PAIRS
        }
        cross_covectors = {
            (root, nonroot): random_annihilator(roots[nonroot][root], rng)
            for root in VERTICES
            for nonroot in VERTICES
        }
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
                "minor_sha256": hashlib.sha256(str(minor).encode()).hexdigest(),
            }
    raise AssertionError("no exact full sensor found in 80 deterministic attempts")


def audit_q20_fixtures() -> dict[str, object]:
    results = {}
    for index, (name, roots) in enumerate(q20_fixtures().items()):
        ranks = edge_ranks(roots)
        delta, c_rank = EXPECTED_COMPENSATION[name]
        compensated = delta + c_rank + sum(ranks)
        assert compensated >= 20
        results[name] = {
            "ranks_01_02_03_12_13_23": ranks,
            "Delta": delta,
            "c_rank": c_rank,
            "compensated_q": compensated,
            "full_sensor": exact_full_sensor(roots, 2_026_083_000 + index),
        }
    assert results["A_generic"]["compensated_q"] == 20
    assert results["B_generic"]["compensated_q"] == 20
    assert results["B_one_collinear"]["compensated_q"] == 20
    assert results["B_both_collinear_cross_incompatible"]["compensated_q"] == 20
    assert results["B_both_collinear_cross_compatible"]["compensated_q"] == 20
    assert results["C_two_one_three_synchronized_plus_line"]["compensated_q"] == 20
    assert results["D_injective_three_synchronized_plus_line"]["compensated_q"] == 20
    return results


def audit_complementary_ruling_fixture() -> dict[str, object]:
    # Both partitions are 2+1+1 with disjoint repeated pairs (0,1) and
    # (2,3).  Dense normal vectors lie on x+y+z=0; the structural right
    # vectors lie in the coordinate plane z=0 (mask 3), of rank two.
    left_partition = (0, 0, 1, 2)
    right_partition = (0, 1, 2, 2)
    dense = [
        sp.Matrix((1, 0, -1)),
        sp.Matrix((0, 1, -1)),
        sp.Matrix((1, 1, -2)),
    ]
    left_active = (dense[0], dense[0], dense[1], dense[2])
    right_active = (dense[0], dense[1], dense[2], dense[2])
    structural = [
        sp.Matrix((1, 0, 0)),
        sp.Matrix((0, 1, 0)),
        sp.Matrix((1, 1, 0)),
    ]
    right_structural = (
        structural[0], structural[1], structural[2], structural[2]
    )
    generic_left = tuple(
        sp.Matrix(value)
        for value in ((1, 2, 3), (1, 2, 3), (2, 5, 7), (3, 7, 11))
    )
    generic_right = tuple(
        sp.Matrix(value)
        for value in ((2, 3, 5), (3, 5, 7), (5, 7, 11), (7, 11, 13))
    )
    normal = sp.Matrix((1, 1, 1))
    assert all((normal.T * vector)[0] == 0 for vector in dense)
    assert left_partition.count(0) == right_partition.count(2) == 2
    assert set((0, 1)) | set((2, 3)) == set(VERTICES)
    generic_rank = tuple_rank(
        tuple(evaluation(left, right) for left, right in zip(generic_left, generic_right, strict=True))
    )
    active_active_rank = tuple_rank(
        tuple(evaluation(left, right) for left, right in zip(left_active, right_active, strict=True))
    )
    active_structural_rank = tuple_rank(
        tuple(evaluation(left, right) for left, right in zip(left_active, right_structural, strict=True))
    )
    assert generic_rank == 4
    assert active_active_rank == 3
    assert active_structural_rank == 3
    assert sp.Matrix.hstack(*right_structural).rank() == 2
    return {
        "left_partition": left_partition,
        "right_partition": right_partition,
        "repeated_pairs": ((0, 1), (2, 3)),
        "generic_rank": generic_rank,
        "active_active_rank": active_active_rank,
        "active_structural_rank": active_structural_rank,
        "structural_right_rank": 2,
        "normal": (1, 1, 1),
    }


def input_ruling_support_audit() -> dict[str, object]:
    raw = INPUT_PATH.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == INPUT_SHA256
    data = json.loads(raw.decode("utf-8"))
    records_sha = hashlib.sha256(
        json.dumps(data["records"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert records_sha == RECORDS_SHA256
    active_structural_cells = 0
    complementary_cells = 0
    repeated_pairs = Counter()
    for record in data["records"]:
        partitions = tuple(tuple(values) for values in record["partitions"])
        for left, right in PAIRS:
            left_pair = repeated_pair(partitions[left])
            right_pair = repeated_pair(partitions[right])
            if left_pair is None or right_pair is None:
                continue
            active_structural_cells += 1
            repeated_pairs[(left_pair, right_pair)] += 1
            if not set(left_pair) & set(right_pair) and set(left_pair) | set(right_pair) == set(VERTICES):
                complementary_cells += 1
    assert active_structural_cells == 30
    assert complementary_cells == 0
    return {
        "records": len(data["records"]),
        "both_2_plus_1_plus_1_pair_cells": active_structural_cells,
        "complementary_repeated_pair_cells": complementary_cells,
        "repeated_pair_histogram": {
            str(key): value for key, value in sorted(repeated_pairs.items(), key=str)
        },
    }


def repeated_pair(partition: tuple[int, ...]) -> tuple[int, int] | None:
    if len(set(partition)) != 3:
        return None
    pairs = [
        pair
        for pair in combinations(range(4), 2)
        if partition[pair[0]] == partition[pair[1]]
    ]
    assert len(pairs) == 1
    return pairs[0]


def diagonal_word_coefficient(counts: tuple[int, int, int]) -> int:
    if any(count % 2 for count in counts):
        return 0
    result = 1
    for count in counts:
        result *= odd_double_factorial(count - 1)
    return result


def audit_b_all_diagonal_m4() -> dict[str, object]:
    symbols = sp.symbols("z0:4_0:3")
    symbolic_z = tuple(
        tuple(symbols[3 * index + colour] for colour in range(3))
        for index in range(4)
    )
    subsets, symbolic_columns = companion_polynomials(4, symbolic_z)
    x, y, z = sp.symbols("x y z")
    quadratic = x**2 + y**2 + z**2
    all_cross = tuple(range(4))
    divisible = 0
    for subset, polynomial in zip(subsets, symbolic_columns, strict=True):
        if subset == all_cross:
            continue
        _, remainder = sp.div(polynomial, quadratic, x, y, z)
        assert sp.expand(remainder) == 0
        divisible += 1
    numeric_z = tuple((1, index + 1, (index + 1) ** 2) for index in range(4))
    _, numeric_columns = companion_polynomials(4, numeric_z)
    numeric_rank = polynomial_rank(numeric_columns, 4)
    assert numeric_rank == 7
    _, ternary_columns = companion_polynomials(
        3, tuple((1, index + 1, (index + 1) ** 2) for index in range(3))
    )
    assert polynomial_rank(ternary_columns, 3) == 4
    cuts_checked = 0
    for root_set in combinations(range(8), 4):
        # For the diagonal-complete graph, relabelling a cut gives the same
        # exact four-root companion formula.  Recompute its numeric rank for
        # every ordered R|N cut rather than relying on one representative.
        nonroots = tuple(vertex for vertex in range(8) if vertex not in root_set)
        assert len(root_set) == len(nonroots) == 4
        _, cut_columns = companion_polynomials(
            4,
            tuple((1, vertex + 1, (vertex + 1) ** 2) for vertex in nonroots),
        )
        assert polynomial_rank(cut_columns, 4) == 7
        cuts_checked += 1
    assert cuts_checked == comb(8, 4) == 70
    pure = diagonal_word_coefficient((8, 0, 0))
    mixed = diagonal_word_coefficient((2, 6, 0))
    odd = diagonal_word_coefficient((1, 7, 0))
    assert (pure, mixed, odd) == (105, 15, 0)
    assert sp.Rational(mixed, pure) == sp.Rational(1, 7)
    return {
        "m": 4,
        "columns": len(symbolic_columns),
        "quadratic_divisible_non_all_cross": divisible,
        "numeric_sensor_rank": numeric_rank,
        "column_rank_defect": len(symbolic_columns) - numeric_rank,
        "ordered_balanced_cuts_checked": cuts_checked,
        "pure_coefficient": pure,
        "mixed_coefficient": mixed,
        "mixed_to_pure_ratio": "1/7",
        "m3_threshold_rank": 4,
        "scope": "diagonal-complete m=4 B_all mechanism only",
    }


def main() -> None:
    fixtures = audit_q20_fixtures()
    ruling = audit_complementary_ruling_fixture()
    input_audit = input_ruling_support_audit()
    b_all = audit_b_all_diagonal_m4()
    print("balanced m=3 q20 exact fixture/B_all audit: PASS")
    print(
        json.dumps(
            {
                "status": "independent_exact_fixture_and_b_all_audit",
                "global_conjecture": "UNRESOLVED",
                "q20_fixtures": fixtures,
                "complementary_ruling_fixture": ruling,
                "q22_input_ruling_support": input_audit,
                "b_all_diagonal_m4": b_all,
                "scope_limit": (
                    "exact displayed fixtures and diagonal-complete m=4 B_all "
                    "mechanism; no arbitrary B_all classification, full target "
                    "closure, or global theorem"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
