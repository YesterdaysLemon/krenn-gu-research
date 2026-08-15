"""Primary exact checks for the co-two sensor corank-two strengthening."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
from math import comb

import sympy as sp

Vector = tuple[Fraction, ...]


def edges(vertex_count: int) -> list[tuple[int, int]]:
    """Return the square-free degree-two coordinate edges."""
    return list(combinations(range(vertex_count), 2))


def projective(vector: Vector) -> Vector:
    """Normalize a nonzero rational vector by its first nonzero entry."""
    pivot = next(entry for entry in vector if entry)
    return tuple(entry / pivot for entry in vector)


def square_free_product(left: Vector, right: Vector) -> Vector:
    """Multiply two degree-one forms in the square-free algebra."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in edges(len(left))
    )


def quadratic_vertices(quadratic: Vector) -> frozenset[int]:
    """Return the coordinate vertices incident to nonzero quadratic terms."""
    vertex_count = int((1 + (1 + 8 * len(quadratic)) ** 0.5) / 2)
    assert comb(vertex_count, 2) == len(quadratic)
    result: set[int] = set()
    for coefficient, edge in zip(quadratic, edges(vertex_count), strict=True):
        if coefficient:
            result.update(edge)
    return frozenset(result)


def graph_kind(edge_set: frozenset[tuple[int, int]]) -> str:
    """Classify one of the support graphs arising from two small supports."""
    vertices = sorted({vertex for edge in edge_set for vertex in edge})
    degrees = sorted(
        sum(vertex in edge for edge in edge_set) for vertex in vertices
    )
    signatures = {
        (1, 1): "edge",
        (1, 1, 2): "path",
        (2, 2, 2): "triangle",
        (2, 2, 2, 2): "K22",
    }
    return signatures[tuple(degrees)]


def symbolic_support_graphs() -> Counter[str]:
    """Enumerate the cancellation-sensitive support-set cases symbolically."""
    supports = [
        frozenset(support)
        for size in (1, 2)
        for support in combinations(range(4), size)
    ]
    kinds: Counter[str] = Counter()
    for left_index, left_support in enumerate(supports):
        for right_support in supports[left_index:]:
            union = left_support | right_support
            intersection = left_support & right_support

            if left_support == right_support and len(left_support) == 1:
                continue

            if left_support == right_support and len(left_support) == 2:
                # The only coefficient can cancel.  Conditional on a nonzero
                # product, its graph is the single edge on the common support.
                graph = frozenset({tuple(sorted(left_support))})
            else:
                graph = frozenset(
                    (first, second)
                    for first, second in edges(4)
                    if (first in left_support and second in right_support)
                    or (second in left_support and first in right_support)
                )

            incident = {vertex for edge in graph for vertex in edge}
            assert incident == union
            kind = graph_kind(graph)
            kinds[kind] += 1

            if len(union) == 4:
                assert not intersection
                assert kind == "K22"
                shores = {
                    frozenset(left_support),
                    frozenset(right_support),
                }
                candidate_shores = {
                    frozenset(side)
                    for side in combinations(union, 2)
                    if all((first in side) != (second in side) for first, second in graph)
                }
                assert candidate_shores == shores

    assert set(kinds) == {"edge", "path", "triangle", "K22"}
    return kinds


def rational_support_two_forms(vertex_count: int) -> list[Vector]:
    """Return a finite projective grid of support-at-most-two forms."""
    forms: list[Vector] = []
    for first in range(vertex_count):
        singleton = [Fraction(0) for _ in range(vertex_count)]
        singleton[first] = Fraction(1)
        forms.append(tuple(singleton))
    for first, second in combinations(range(vertex_count), 2):
        for ratio in (-3, -2, -1, 1, 2, 3):
            pair = [Fraction(0) for _ in range(vertex_count)]
            pair[first] = Fraction(1)
            pair[second] = Fraction(ratio)
            forms.append(tuple(pair))
    return forms


def rational_factor_line_regression() -> dict[str, object]:
    """Group exact rational products and rank all observed factor lines."""
    vertex_count = 4
    forms = rational_support_two_forms(vertex_count)
    factor_lines: dict[Vector, set[Vector]] = defaultdict(set)
    for left, right in combinations_with_replacement(forms, 2):
        product = square_free_product(left, right)
        if not any(product):
            continue
        quadratic = projective(product)
        factor_lines[quadratic].update((projective(left), projective(right)))

    histogram: Counter[tuple[int, int]] = Counter()
    maximum_by_vertices: dict[int, int] = defaultdict(int)
    for quadratic, factors in factor_lines.items():
        rank = sp.Matrix([list(factor) for factor in factors]).rank()
        vertex_count_q = len(quadratic_vertices(quadratic))
        histogram[(vertex_count_q, rank)] += 1
        maximum_by_vertices[vertex_count_q] = max(
            maximum_by_vertices[vertex_count_q], rank
        )
        if vertex_count_q <= 2:
            assert rank <= 2
        if vertex_count_q == 4:
            assert rank <= 2
        if rank >= 3:
            assert vertex_count_q == 3

    assert maximum_by_vertices[4] == 2
    return {
        "projective_forms": len(forms),
        "projective_products": len(factor_lines),
        "(vertices,factor_span)_histogram": dict(sorted(histogram.items())),
        "max_factor_span_by_vertices": dict(sorted(maximum_by_vertices.items())),
    }


def symbolic_weighted_k22() -> dict[str, sp.Expr]:
    """Check the rank-one edge ratios fixing each K2,2 factor line."""
    a_0, a_1, b_2, b_3 = sp.symbols("a_0 a_1 b_2 b_3", nonzero=True)
    matrix = sp.Matrix(
        [
            [a_0 * b_2, a_0 * b_3],
            [a_1 * b_2, a_1 * b_3],
        ]
    )
    determinant = sp.factor(matrix.det())
    assert determinant == 0
    row_ratio = sp.cancel(matrix[0, 0] / matrix[1, 0])
    column_ratio = sp.cancel(matrix[0, 0] / matrix[0, 1])
    assert row_ratio == a_0 / a_1
    assert column_ratio == b_2 / b_3
    return {
        "edge_matrix_determinant": determinant,
        "first_shore_ratio": row_ratio,
        "second_shore_ratio": column_ratio,
    }


def conditional_dimension_bounds() -> dict[int, tuple[int, int]]:
    """Tabulate (pair lower bound, complementary sensor upper bound)."""
    return {r: (5, comb(r, 2) - 2) for r in range(3, 13)}


def main() -> None:
    graphs = symbolic_support_graphs()
    k22 = symbolic_weighted_k22()
    factors = rational_factor_line_regression()
    bounds = conditional_dimension_bounds()
    assert bounds[6] == (5, 13)
    print("arbitrary permanent co-two corank-two primary checks: PASS")
    print(f"  symbolic support-graph cases: {dict(sorted(graphs.items()))}")
    print(f"  symbolic weighted K2,2 ratios: {k22}")
    print(f"  exact rational factor-line regression: {factors}")
    print(f"  conditional (pair lower, sensor upper) bounds: {bounds}")


if __name__ == "__main__":
    main()
