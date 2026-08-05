"""Primary checks for the seven-leaf projected-Veronese ramification theorem."""

from itertools import combinations, combinations_with_replacement

import sympy as sp

VERTICES = tuple(range(7))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FOUR_SETS = tuple(combinations(VERTICES, 4))
FIVE_SETS = tuple(combinations(VERTICES, 5))
SYMMETRIC_PAIRS = tuple(combinations_with_replacement(range(len(EDGES)), 2))


def disjoint(edge_left: tuple[int, int], edge_right: tuple[int, int]) -> bool:
    return not set(edge_left).intersection(edge_right)


def multiplication_projection() -> sp.Matrix:
    """Sym^2(A_2) -> A_4 in the unordered tensor-monomial basis."""
    rows = []
    for four_set in FOUR_SETS:
        support = set(four_set)
        row = []
        for left_index, right_index in SYMMETRIC_PAIRS:
            left = EDGES[left_index]
            right = EDGES[right_index]
            row.append(
                int(
                    left_index != right_index
                    and disjoint(left, right)
                    and set(left).union(right) == support
                )
            )
        rows.append(row)
    return sp.Matrix(rows)


def hafnian_jacobian(values: tuple[sp.Expr, ...]) -> sp.Matrix:
    rows = []
    for four_set in FOUR_SETS:
        support = set(four_set)
        row = []
        for edge in EDGES:
            if not set(edge).issubset(support):
                row.append(sp.Integer(0))
                continue
            complement = tuple(sorted(support.difference(edge)))
            row.append(values[EDGE_INDEX[complement]])
        rows.append(row)
    return sp.Matrix(rows)


def symmetric_tangent_coordinates(
    values: tuple[sp.Expr, ...], directions: tuple[sp.Expr, ...]
) -> sp.Matrix:
    coordinates = []
    for left, right in SYMMETRIC_PAIRS:
        if left == right:
            coordinates.append(values[left] * directions[left])
        else:
            coordinates.append(
                values[left] * directions[right]
                + values[right] * directions[left]
            )
    return sp.Matrix(coordinates)


def tangent_embedding(values: tuple[sp.Expr, ...]) -> sp.Matrix:
    columns = []
    for direction_index in range(len(EDGES)):
        direction = tuple(
            sp.Integer(index == direction_index) for index in range(len(EDGES))
        )
        columns.append(symmetric_tangent_coordinates(values, direction))
    return sp.Matrix.hstack(*columns)


def lefschetz_four_to_five() -> sp.Matrix:
    return sp.Matrix(
        [
            [int(set(four_set).issubset(five_set)) for four_set in FOUR_SETS]
            for five_set in FIVE_SETS
        ]
    )


def main() -> None:
    projection = multiplication_projection()
    assert projection.shape == (35, 231)
    assert projection.rank() == 35
    assert len(SYMMETRIC_PAIRS) - projection.rank() == 196
    print("PASS: Boolean multiplication is a 35 x 231 surjection with 196-kernel")

    f = sp.symbols("f0:21")
    k = sp.symbols("k0:21")
    jacobian = hafnian_jacobian(f)
    tangent = symmetric_tangent_coordinates(f, k)
    assert projection * tangent == jacobian * sp.Matrix(k)
    print("PASS: projected Veronese tangent equals the four-hafnian Jacobian")

    all_one = tuple(sp.Integer(1) for _ in EDGES)
    assert hafnian_jacobian(all_one).rank() == 21
    assert tangent_embedding(all_one).rank() == 21
    print("PASS: all-one graph is unramified and the Veronese tangent is injective")

    lefschetz = lefschetz_four_to_five()
    assert lefschetz.shape == (21, 35)
    assert lefschetz.rank() == 21
    assert len(FOUR_SETS) - lefschetz.rank() == 14
    print("PASS: primitive four-form target is the 14-dimensional Lefschetz kernel")

    print("searches=0 finite_fields=0 graph_enumerations=0 numerics=0")
    print("SCOPE: physical primitive ramification torus remains UNKNOWN")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
