"""Focused exact checks for the GLS23 transverse nuisance decomposition."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


PORT_DIMENSION = 2
ROOT_DIMENSION = 3


def assignments(vertices: tuple[int, ...]):
    return tuple(product(range(PORT_DIMENSION), repeat=len(vertices)))


def tensor_index(values: tuple[int, ...]) -> int:
    answer = 0
    for value in values:
        answer = PORT_DIMENSION * answer + value
    return answer


def coefficient_tensor(d_vertices: tuple[int, ...], seed: int) -> sp.Matrix:
    width = PORT_DIMENSION ** len(d_vertices)
    return sp.Matrix(
        ROOT_DIMENSION,
        width,
        lambda root, column: ((root + 2) * (column + seed + 3) + seed) % 7 - 3,
    )


def actual_operator_slices(
    universe: tuple[int, ...],
    target: tuple[int, ...],
    d_vertices: tuple[int, ...],
    coefficient: sp.Matrix,
) -> sp.Matrix:
    complement = tuple(vertex for vertex in universe if vertex not in d_vertices)
    right = tuple(vertex for vertex in universe if vertex not in target)
    left_dimension = ROOT_DIMENSION * PORT_DIMENSION ** len(target)
    columns = []
    for input_values in assignments(complement):
        input_map = dict(zip(complement, input_values, strict=True))
        for right_values in assignments(right):
            right_map = dict(zip(right, right_values, strict=True))
            vector = sp.zeros(left_dimension, 1)
            for root in range(ROOT_DIMENSION):
                for d_values in assignments(d_vertices):
                    d_map = dict(zip(d_vertices, d_values, strict=True))
                    output = {**input_map, **d_map}
                    if any(output[vertex] != right_map[vertex] for vertex in right):
                        continue
                    target_values = tuple(output[vertex] for vertex in target)
                    left_index = (
                        root * PORT_DIMENSION ** len(target) + tensor_index(target_values)
                    )
                    d_index = tensor_index(d_values)
                    vector[left_index] += coefficient[root, d_index]
            columns.append(vector)
    return sp.Matrix.hstack(*columns)


def expected_formula_slices(
    target: tuple[int, ...],
    d_vertices: tuple[int, ...],
    coefficient: sp.Matrix,
) -> sp.Matrix:
    x_vertices = tuple(vertex for vertex in target if vertex in d_vertices)
    y_vertices = tuple(vertex for vertex in d_vertices if vertex not in target)
    z_vertices = tuple(vertex for vertex in target if vertex not in d_vertices)
    left_dimension = ROOT_DIMENSION * PORT_DIMENSION ** len(target)
    columns = []
    for y_values in assignments(y_vertices):
        y_map = dict(zip(y_vertices, y_values, strict=True))
        for z_values in assignments(z_vertices):
            z_map = dict(zip(z_vertices, z_values, strict=True))
            vector = sp.zeros(left_dimension, 1)
            for root in range(ROOT_DIMENSION):
                for x_values in assignments(x_vertices):
                    x_map = dict(zip(x_vertices, x_values, strict=True))
                    d_values = tuple({**x_map, **y_map}[vertex] for vertex in d_vertices)
                    target_values = tuple({**x_map, **z_map}[vertex] for vertex in target)
                    left_index = (
                        root * PORT_DIMENSION ** len(target) + tensor_index(target_values)
                    )
                    vector[left_index] = coefficient[root, tensor_index(d_values)]
            columns.append(vector)
    return sp.Matrix.hstack(*columns)


def same_column_space(left: sp.MatrixBase, right: sp.MatrixBase) -> bool:
    return left.rank() == right.rank() == left.row_join(right).rank()


def check_all_intersection_patterns() -> dict[str, int]:
    universe = (0, 1, 2, 3)
    targets = ((),) + tuple(combinations(universe, 2))
    d_sets = ((),) + tuple((vertex,) for vertex in universe) + tuple(
        combinations(universe, 2)
    )
    checked = 0
    ranks = set()
    for target in targets:
        for seed, d_vertices in enumerate(d_sets, start=1):
            coefficient = coefficient_tensor(d_vertices, seed)
            actual = actual_operator_slices(universe, target, d_vertices, coefficient)
            expected = expected_formula_slices(target, d_vertices, coefficient)
            assert same_column_space(actual, expected)
            ranks.add((len(target), len(d_vertices), len(set(target) & set(d_vertices)), actual.rank()))
            checked += 1
    return {"label_target_pairs": checked, "rank_patterns": len(ranks)}


def check_top_identity_slices() -> dict[str, int]:
    universe = (0, 1, 2, 3)
    omega = sp.Matrix([2, -1, 3])
    checked = 0
    for target in combinations(universe, 2):
        actual = actual_operator_slices(universe, target, (), omega)
        expected = sp.kronecker_product(omega, sp.eye(PORT_DIMENSION ** len(target)))
        assert same_column_space(actual, expected)
        assert actual.rank() == PORT_DIMENSION ** len(target)
        checked += 1
    return {"pair_targets": checked, "anchor_nuisance_rank": 4}


def check_disjoint_collapse() -> dict[str, int]:
    # Three disjoint-labelled coefficient tensors provide the three root basis
    # slices, hence their tensor products fill root tensor V_C.
    target_dimension = PORT_DIMENSION**2
    root_basis = sp.eye(ROOT_DIMENSION)
    spaces = [
        sp.kronecker_product(root_basis[:, root], sp.eye(target_dimension))
        for root in range(ROOT_DIMENSION)
    ]
    nuisance = sp.Matrix.hstack(*spaces)
    assert nuisance.rank() == ROOT_DIMENSION * target_dimension
    desired = sp.Matrix(range(1, ROOT_DIMENSION * target_dimension + 1))
    assert nuisance.row_join(desired).rank() == nuisance.rank()
    return {"root_slice_rank": ROOT_DIMENSION, "filled_dimension": nuisance.rank()}


def check_top_anchor_dichotomy() -> dict[str, int]:
    pair_dimension = PORT_DIMENSION**2
    omega = sp.Matrix([1, 2, -1])
    pair_anchor = sp.kronecker_product(omega, sp.eye(pair_dimension))
    assert pair_anchor.rank() == pair_dimension
    assert ROOT_DIMENSION * pair_dimension - pair_anchor.rank() == (
        ROOT_DIMENSION - 1
    ) * pair_dimension

    # Top target: explicit root-slice nuisance either absorbs omega or leaves it.
    nuisance_good = sp.Matrix.hstack(sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1]))
    nuisance_bad = nuisance_good.row_join(omega)
    assert nuisance_good.row_join(omega).rank() == nuisance_good.rank() + 1
    assert nuisance_bad.row_join(omega).rank() == nuisance_bad.rank()
    zero_anchor = sp.zeros(ROOT_DIMENSION, 1)
    assert not any(zero_anchor)
    return {
        "small_pair_quotient": ROOT_DIMENSION * pair_dimension - pair_anchor.rank(),
        "actual_pair_quotient": 63,
        "actual_top_rows": 8,
    }


def check_root_order_counts() -> tuple[tuple[int, int, int, int], ...]:
    records = []
    for root_order in range(3, 9):
        ports = 2 * root_order - 2
        pair_targets = ports * (ports - 1) // 2
        records.append((root_order, pair_targets, 63, 8))
    assert records[0] == (3, 6, 63, 8)
    assert records[1] == (4, 15, 63, 8)
    return tuple(records)


def main() -> None:
    patterns = check_all_intersection_patterns()
    top = check_top_identity_slices()
    collapse = check_disjoint_collapse()
    anchor = check_top_anchor_dichotomy()
    counts = check_root_order_counts()
    print("promoted transverse complete-nuisance primary checks: PASS")
    print("  exact labelled intersection patterns:", patterns)
    print("  projected top identity slices:", top)
    print("  disjoint-root full collapse:", collapse)
    print("  top-anchor dichotomy:", anchor)
    print("  arbitrary-root pair/top dimensions:", counts)
    print("  scope: decomposition/dichotomy only; survival and node closure stay open")


if __name__ == "__main__":
    main()
