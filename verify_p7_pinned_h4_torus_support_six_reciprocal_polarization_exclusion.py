"""Primary exact replay for the P7 support-six torus exclusion."""

from itertools import combinations

import sympy as sp


def haf4(vertices: tuple[int, int, int, int], edge: dict[tuple[int, int], sp.Expr]) -> sp.Expr:
    """Four-vertex hafnian in the fixed vertex ordering."""
    a, b, c, d = vertices

    def e(i: int, j: int) -> sp.Expr:
        return edge[tuple(sorted((i, j)))]

    return sp.expand(e(a, b) * e(c, d) + e(a, c) * e(b, d) + e(a, d) * e(b, c))


def inclusion(rows: list[tuple[int, ...]], columns: list[tuple[int, ...]]) -> sp.Matrix:
    """Unsigned subset-inclusion matrix."""
    return sp.Matrix([[int(set(column) <= set(row)) for column in columns] for row in rows])


def main() -> None:
    support = tuple(range(6))
    c1, c2 = 6, 7
    u = sp.symbols("u0:6")
    v = sp.symbols("v0:6")
    d = {(i, j): sp.Symbol(f"d{i}{j}") for i, j in combinations(support, 2)}

    raw_edge: dict[tuple[int, int], sp.Expr] = {(c1, c2): sp.Integer(1)}
    for i in support:
        raw_edge[tuple(sorted((i, c1)))] = u[i]
        raw_edge[tuple(sorted((i, c2)))] = v[i]
    raw_edge.update(d)

    triple = (0, 1, 2)
    three_support_row = sum(
        haf4(tuple(sorted((set(triple) - {removed}) | {c1, c2})), raw_edge)
        for removed in triple
    )
    expected_three = sum(
        d[tuple(sorted((i, j)))] + u[i] * v[j] + v[i] * u[j]
        for i, j in combinations(triple, 2)
    )
    assert sp.expand(three_support_row - expected_three) == 0

    recovered_edge = dict(raw_edge)
    for i, j in combinations(support, 2):
        recovered_edge[(i, j)] = -(u[i] * v[j] + v[i] * u[j])

    quad = (0, 1, 2, 3)
    four_support_row = sum(
        haf4(tuple(sorted((set(quad) - {removed}) | {c1})), recovered_edge)
        for removed in quad
    )
    mixed_cubic_sum = sum(
        v[i] * u[j] * u[k] + u[i] * v[j] * u[k] + u[i] * u[j] * v[k]
        for i, j, k in combinations(quad, 3)
    )
    assert sp.expand(four_support_row + 2 * mixed_cubic_sum) == 0

    reciprocal_sum = sum(
        (v[i] + v[j]) / (u[i] * u[j]) for i, j in combinations(quad, 2)
    )
    assert sp.factor(mixed_cubic_sum / sp.prod(u[i] for i in quad) - reciprocal_sum) == 0

    edges = list(combinations(support, 2))
    triples = list(combinations(support, 3))
    quads = list(combinations(support, 4))
    w23 = inclusion(triples, edges)
    w24 = inclusion(quads, edges)
    assert w23.shape == (20, 15)
    assert w23.rank() == 15
    assert w24.shape == (15, 15)
    assert w24.det() == 1458

    final_three = sp.Matrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    assert final_three.det() == -2

    print("PASS: exact P7 support-six reciprocal-polarization exclusion replay")
    print("W_(2,3)(6) rank: 15")
    print("det W_(2,4)(6): 1458")
    print("final three-pair determinant: -2")
    print("scope: universal characteristic-zero identities; no support or parameter search")


if __name__ == "__main__":
    main()
