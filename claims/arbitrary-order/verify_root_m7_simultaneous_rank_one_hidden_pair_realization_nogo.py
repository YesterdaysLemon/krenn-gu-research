"""Symbolic verifier for the simultaneous rank-one hidden-pair countermodel."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def main() -> None:
    xs = sp.symbols("x0:5", nonzero=True)
    ys = sp.symbols("y0:5", nonzero=True)
    a, b, c, d = sp.symbols("a b c d", nonzero=True)
    a0, a1, b0, b1 = sp.symbols("A0 A1 B0 B1")
    residual_edge = sp.symbols("r")

    edge: dict[tuple[int, int], sp.Expr] = {
        (1, 2): a * xs[1] * xs[2],
        (3, 4): b * xs[3] * xs[4],
        (0, 3): c * ys[0] * ys[3],
        (2, 4): d * ys[2] * ys[4],
    }

    def e(i: int, j: int) -> sp.Expr:
        return edge.get(tuple(sorted((i, j))), sp.S.Zero)

    def hafnian4(vertices: tuple[int, int, int, int]) -> sp.Expr:
        i, j, k, ell = vertices
        return sp.expand(
            e(i, j) * e(k, ell) + e(i, k) * e(j, ell) + e(i, ell) * e(j, k)
        )

    roots = tuple(range(5))
    h = [hafnian4(tuple(i for i in roots if i != k)) for k in roots]
    expected_h = [
        a * b * xs[1] * xs[2] * xs[3] * xs[4],
        c * d * ys[0] * ys[2] * ys[3] * ys[4],
        0,
        0,
        a * c * ys[0] * ys[3] * xs[1] * xs[2],
    ]
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(h, expected_h, strict=True)
    )

    endpoint = {
        (0, 0): a0 * xs[0],
        (0, 1): a1 * xs[0],
        (1, 0): b0 * ys[1],
        (1, 1): b1 * ys[1],
    }

    def endpoint_edge(i: int, t: int) -> sp.Expr:
        return endpoint.get((i, t), sp.S.Zero)

    def hafnian_with_two_endpoints(vertices: tuple[int, ...]) -> sp.Expr:
        total = sp.S.Zero
        for i, j in combinations(vertices, 2):
            remainder = [vertex for vertex in vertices if vertex not in (i, j)]
            endpoint_permanent = endpoint_edge(i, 0) * endpoint_edge(
                j, 1
            ) + endpoint_edge(i, 1) * endpoint_edge(j, 0)
            total += endpoint_permanent * e(remainder[0], remainder[1])
        return sp.expand(total)

    sigma = a0 * b1 + a1 * b0
    q = [
        sp.expand(
            residual_edge * h[k]
            + hafnian_with_two_endpoints(tuple(i for i in roots if i != k))
        )
        for k in roots
    ]
    expected_q = [
        residual_edge * h[0],
        residual_edge * h[1],
        sigma * b * xs[0] * ys[1] * xs[3] * xs[4],
        sigma * d * xs[0] * ys[1] * ys[2] * ys[4],
        residual_edge * h[4],
    ]
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(q, expected_q, strict=True)
    )

    x_all = sp.prod(xs)
    y_all = sp.prod(ys)
    g = [sp.expand(sum(endpoint_edge(k, t) * h[k] for k in roots)) for t in range(2)]
    assert sp.expand(g[0] - (a0 * a * b * x_all + b0 * c * d * y_all)) == 0
    assert sp.expand(g[1] - (a1 * a * b * x_all + b1 * c * d * y_all)) == 0
    coefficient_matrix = sp.Matrix([[a0 * a * b, b0 * c * d], [a1 * a * b, b1 * c * d]])
    assert sp.factor(coefficient_matrix.det()) == a * b * c * d * (a0 * b1 - a1 * b0)

    # The nonzero/nonzero pairs are proportional; the other two have a zero
    # h member.  Hence every scalar-form pair has rank at most one.
    assert all(sp.expand(q[k] - residual_edge * h[k]) == 0 for k in (0, 1, 4))
    assert h[2] == h[3] == 0

    # A concrete legal root tangent chart.
    rho = sp.Matrix([1, 1, 1])
    x_covector = sp.Matrix([[1, 0, -1]])
    y_covector = sp.Matrix([[0, 1, -1]])
    assert (x_covector * rho)[0] == 0
    assert (y_covector * rho)[0] == 0

    print("root m=7 simultaneous rank-one hidden-pair realization: PASS")
    print("bounded symbolic hafnian identities only; no support search was performed")


if __name__ == "__main__":
    main()
