"""Exact sparse verification of hidden-overlay surjectivity."""

from __future__ import annotations

from functools import cache

import sympy as sp

a, b, c, d, e, f = sp.symbols("a b c d e f")
CORE = ("s0", "s1", "s2", "s3")
TERMINALS = ("1", "2", "3", "4")


def edge_key(u: str, v: str) -> tuple[str, str]:
    return tuple(sorted((u, v)))


WEIGHTS = {
    edge_key("s0", "s3"): -1,
    edge_key("s1", "s2"): 1,
    edge_key("s0", "1"): 1,
    edge_key("s0", "2"): -1,
    edge_key("s0", "4"): -1,
    edge_key("s3", "3"): -1,
    edge_key("s3", "1"): a,
    edge_key("s3", "2"): b,
    edge_key("s3", "4"): c,
    edge_key("1", "2"): d,
    edge_key("1", "4"): e,
    edge_key("2", "4"): f,
}


@cache
def hafnian(vertices: tuple[str, ...]) -> sp.Expr:
    if not vertices:
        return sp.Integer(1)
    first = vertices[0]
    total = 0
    for index, partner in enumerate(vertices[1:], start=1):
        weight = WEIGHTS.get(edge_key(first, partner), 0)
        if weight:
            rest = vertices[1:index] + vertices[index + 1 :]
            total += weight * hafnian(rest)
    return sp.expand(total)


def h(extra: tuple[str, ...], added_core: tuple[str, ...] = ()) -> sp.Expr:
    vertices = tuple(sorted(CORE + added_core + extra))
    return hafnian(vertices)


def monomial_map(expr: sp.Expr) -> dict[tuple[int, ...], sp.Expr]:
    return dict(sp.Poly(sp.expand(expr), a, b, c, d, e, f).terms())


def main() -> None:
    visible = [
        h(TERMINALS) * h(()),
        h(("1", "2")) * h(("3", "4")),
        h(("1", "3")) * h(("2", "4")),
        h(("1", "4")) * h(("2", "3")),
    ]
    expected = [-d - e + f, -a + b - d, b + c + f, -a + c - e]
    assert all(
        sp.expand(got - want) == 0 for got, want in zip(visible, expected, strict=True)
    )

    maps = [monomial_map(expr) for expr in visible]
    hidden = {}
    for i in range(4):
        for j in range(i + 1, 4):
            common = set(maps[i]) & set(maps[j])
            assert len(common) == 1
            exponent = common.pop()
            assert maps[i][exponent] == maps[j][exponent]
            monomial = sp.prod(
                var**power
                for var, power in zip((a, b, c, d, e, f), exponent, strict=True)
            )
            hidden[(i, j)] = maps[i][exponent] * monomial

    hidden_vector = sp.Matrix(
        [hidden[pair] for pair in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))]
    )
    assert hidden_vector == sp.Matrix([-d, f, -e, b, -a, c])
    jacobian = hidden_vector.jacobian((a, b, c, d, e, f))
    assert abs(jacobian.det()) == 1

    incidence = sp.Matrix(
        [
            [1, 1, 1, 0, 0, 0],
            [1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1],
        ]
    )
    assert incidence * hidden_vector == sp.Matrix(expected)
    assert incidence.rank() == 4

    # Add two isolated unit edges to enlarge the four-core to eight vertices.
    added = ("t0", "t1", "t2", "t3")
    WEIGHTS[edge_key("t0", "t1")] = 1
    WEIGHTS[edge_key("t2", "t3")] = 1
    hafnian.cache_clear()
    extended = [
        h(TERMINALS, added) * h((), added),
        h(("1", "2"), added) * h(("3", "4"), added),
        h(("1", "3"), added) * h(("2", "4"), added),
        h(("1", "4"), added) * h(("2", "3"), added),
    ]
    assert all(
        sp.expand(got - want) == 0 for got, want in zip(extended, expected, strict=True)
    )

    print("root m=7 hidden-overlay surjectivity: exact sparse verification PASS")
    print("six-variable Jacobian determinant:", jacobian.det())


if __name__ == "__main__":
    main()
