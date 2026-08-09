"""Primary exact checks for response-deck and root-parity legality theorems."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp


def canonical_edge(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def hafnian(
    vertices: tuple[int, ...],
    weights: dict[tuple[int, int], sp.Expr],
) -> sp.Expr:
    """Return the exact matching polynomial by the first-vertex recurrence."""

    @cache
    def rec(remaining: tuple[int, ...]) -> sp.Expr:
        if not remaining:
            return sp.Integer(1)
        if len(remaining) % 2:
            return sp.Integer(0)
        first = remaining[0]
        total = sp.Integer(0)
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += weights.get(canonical_edge(first, partner), sp.Integer(0)) * rec(
                rest
            )
        return sp.expand(total)

    return rec(vertices)


def permanent(matrix: sp.Matrix) -> sp.Expr:
    """Exact permanent by a row/subset recurrence."""

    rows, cols = matrix.shape
    assert rows == cols

    @cache
    def rec(row: int, available: tuple[int, ...]) -> sp.Expr:
        if row == rows:
            return sp.Integer(1)
        total = sp.Integer(0)
        for position, col in enumerate(available):
            rest = available[:position] + available[position + 1 :]
            total += matrix[row, col] * rec(row + 1, rest)
        return sp.expand(total)

    return rec(0, tuple(range(cols)))


def response_deck_checks() -> None:
    q = tuple(range(6))
    edges = tuple(combinations(q, 2))
    a = {edge: sp.Symbol(f"a{edge[0]}{edge[1]}") for edge in edges}
    u = sp.symbols("u0:2")
    t = {
        edge: sp.symbols(f"t{edge[0]}{edge[1]}_0:2")
        for edge in edges
    }

    def residual_hafnian(vertices: tuple[int, ...]) -> sp.Expr:
        return hafnian(vertices, a)

    def deck(vertices: tuple[int, ...], coordinate: int) -> sp.Expr:
        value = residual_hafnian(vertices) * u[coordinate]
        for edge in combinations(vertices, 2):
            remainder = tuple(vertex for vertex in vertices if vertex not in edge)
            value += residual_hafnian(remainder) * t[edge][coordinate]
        return sp.expand(value)

    top = [deck(q, coordinate) for coordinate in range(2)]
    for edge in edges:
        remaining = tuple(vertex for vertex in q if vertex not in edge)
        for coordinate in range(2):
            assert sp.expand(sp.diff(top[coordinate], a[edge]) - deck(remaining, coordinate)) == 0

    for first, second in combinations(edges, 2):
        for coordinate in range(2):
            derivative = sp.diff(top[coordinate], a[first], a[second])
            if set(first).isdisjoint(second):
                deleted = set(first) | set(second)
                remaining = tuple(vertex for vertex in q if vertex not in deleted)
                assert sp.expand(derivative - deck(remaining, coordinate)) == 0
            else:
                assert sp.expand(derivative) == 0

    matchings = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    for coordinate in range(2):
        values = [sp.diff(top[coordinate], a[x], a[y]) for x, y in matchings]
        assert all(sp.expand(value - values[0]) == 0 for value in values[1:])
        assert sp.expand(values[0] - deck((4, 5), coordinate)) == 0

    alpha = sp.Symbol("alpha")
    pure = sp.symbols("pure0:2")
    channel = sp.symbols("channel0:2")
    two_residual_top = tuple(alpha * pure[i] + channel[i] for i in range(2))
    recovered_pure = tuple(sp.diff(value, alpha) for value in two_residual_top)
    recovered_channel = tuple(
        sp.expand(two_residual_top[i] - alpha * recovered_pure[i])
        for i in range(2)
    )
    assert recovered_pure == pure
    assert recovered_channel == channel
    print("six-residual response derivatives = named principal deletion decks: PASS")


def augmented_hafnian_checks() -> None:
    roots = tuple(range(4))
    deleted_two = (4, 5)
    root_edges = tuple(combinations(roots, 2))
    ell = {edge: sp.Symbol(f"l{edge[0]}{edge[1]}") for edge in root_edges}
    cross_two = {
        canonical_edge(root, deleted): sp.Symbol(f"h{root}_{deleted}")
        for root in roots
        for deleted in deleted_two
    }
    weights_two = {**ell, **cross_two}
    block_hafnian = hafnian(roots + deleted_two, weights_two)
    explicit = sp.Integer(0)
    for root_pair in root_edges:
        remaining = tuple(root for root in roots if root not in root_pair)
        p, q = deleted_two
        explicit += ell[root_pair] * (
            cross_two[canonical_edge(remaining[0], p)]
            * cross_two[canonical_edge(remaining[1], q)]
            + cross_two[canonical_edge(remaining[0], q)]
            * cross_two[canonical_edge(remaining[1], p)]
        )
    assert sp.expand(block_hafnian - explicit) == 0
    assert sp.expand(block_hafnian.subs({value: 0 for value in ell.values()})) == 0

    deleted_four = tuple(range(4, 8))
    cross_four = {
        canonical_edge(root, deleted): sp.Symbol(f"k{root}_{deleted}")
        for root in roots
        for deleted in deleted_four
    }
    weights_four = {**ell, **cross_four}
    block_four = hafnian(roots + deleted_four, weights_four)
    incidence = sp.Matrix(
        [[cross_four[canonical_edge(root, deleted)] for deleted in deleted_four] for root in roots]
    )
    assert sp.expand(block_four - permanent(incidence)) == 0

    odd_vertices = tuple(range(5))
    odd_weights = {
        edge: sp.Symbol(f"o{edge[0]}{edge[1]}")
        for edge in combinations(odd_vertices, 2)
    }
    assert hafnian(odd_vertices, odd_weights) == 0
    print("augmented-hafnian root weights and odd-root parity: PASS")


def p6_fan_certificate() -> None:
    matrix_a = sp.Matrix([[1, 0, 1, 1], [0, 1, 0, 1]])
    matrix_b = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    columns: list[sp.Matrix] = []
    for i, j in combinations(range(4), 2):
        columns.append(
            sp.kronecker_product(matrix_a[:, i], matrix_b[:, j])
            + sp.kronecker_product(matrix_a[:, j], matrix_b[:, i])
        )
    fan = sp.Matrix.hstack(*columns)
    assert fan.shape == (6, 6)
    assert fan.det() == -2
    assert fan.rank() == 6

    edge_order = tuple(combinations(range(4), 2))
    complement = sp.zeros(6, 6)
    for row, pair in enumerate(edge_order):
        opposite = tuple(vertex for vertex in range(4) if vertex not in pair)
        complement[row, edge_order.index(opposite)] = 1
    assert complement * complement == sp.eye(6)
    assert complement.det() == -1
    print("clean 2x3 four-residual fan determinant -2: PASS")


def pair_vacuum_fibre_check() -> None:
    x, y, z, tau = sp.symbols("x y z tau")
    weights = {
        (0, 2): x,
        (1, 3): y,
        (2, 3): tau,
        (4, 5): z,
    }
    full = hafnian(tuple(range(6)), weights)
    deleted = hafnian((2, 3, 4, 5), weights)
    assert sp.expand(full - x * y * z) == 0
    assert sp.expand(deleted - tau * z) == 0
    assert sp.diff(full, tau) == 0
    assert sp.diff(deleted, tau) == z
    print("nonzero complete-tensor pair-vacuum affine fibre: PASS")


def main() -> None:
    response_deck_checks()
    augmented_hafnian_checks()
    p6_fan_certificate()
    pair_vacuum_fibre_check()
    print("response-jet principal-deletion/root-parity primary verification: PASS")


if __name__ == "__main__":
    main()
