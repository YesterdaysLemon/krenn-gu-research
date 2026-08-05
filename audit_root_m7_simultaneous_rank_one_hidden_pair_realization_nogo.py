"""Independent no-import audit of the simultaneous rank-one countermodel."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, Fraction]


def monomial(coefficient: int, *variables: str) -> Polynomial:
    if coefficient == 0:
        return {}
    return {tuple(sorted(variables)): Fraction(coefficient)}


def add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for key, value in polynomial.items():
            result[key] = result.get(key, Fraction(0)) + value
            if result[key] == 0:
                del result[key]
    return result


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_key, left_value in left.items():
        for right_key, right_value in right.items():
            key = tuple(sorted(left_key + right_key))
            result[key] = result.get(key, Fraction(0)) + left_value * right_value
    return result


def scale(coefficient: int, polynomial: Polynomial) -> Polynomial:
    return {key: coefficient * value for key, value in polynomial.items()}


def main() -> None:
    edge = {
        (1, 2): monomial(1, "a", "x1", "x2"),
        (3, 4): monomial(1, "b", "x3", "x4"),
        (0, 3): monomial(1, "c", "y0", "y3"),
        (2, 4): monomial(1, "d", "y2", "y4"),
    }

    def get_edge(i: int, j: int) -> Polynomial:
        return edge.get(tuple(sorted((i, j))), {})

    def hafnian4(vertices: tuple[int, int, int, int]) -> Polynomial:
        i, j, k, ell = vertices
        return add(
            multiply(get_edge(i, j), get_edge(k, ell)),
            multiply(get_edge(i, k), get_edge(j, ell)),
            multiply(get_edge(i, ell), get_edge(j, k)),
        )

    roots = tuple(range(5))
    h = [hafnian4(tuple(i for i in roots if i != k)) for k in roots]
    assert h[0] == monomial(1, "a", "b", "x1", "x2", "x3", "x4")
    assert h[1] == monomial(1, "c", "d", "y0", "y2", "y3", "y4")
    assert h[2] == h[3] == {}
    assert h[4] == monomial(1, "a", "c", "x1", "x2", "y0", "y3")

    # A0=A1=B0=1, B1=2: determinant=1 and permanent sigma=3.
    endpoint = {
        (0, 0): monomial(1, "x0"),
        (0, 1): monomial(1, "x0"),
        (1, 0): monomial(1, "y1"),
        (1, 1): monomial(2, "y1"),
    }

    def endpoint_edge(i: int, t: int) -> Polynomial:
        return endpoint.get((i, t), {})

    def two_endpoint_form(vertices: tuple[int, ...]) -> Polynomial:
        total: Polynomial = {}
        for i, j in combinations(vertices, 2):
            remainder = [vertex for vertex in vertices if vertex not in (i, j)]
            endpoint_permanent = add(
                multiply(endpoint_edge(i, 0), endpoint_edge(j, 1)),
                multiply(endpoint_edge(i, 1), endpoint_edge(j, 0)),
            )
            total = add(total, multiply(endpoint_permanent, get_edge(*remainder)))
        return total

    residual_edge = 5
    q = [
        add(
            scale(residual_edge, h[k]),
            two_endpoint_form(tuple(i for i in roots if i != k)),
        )
        for k in roots
    ]
    assert q[0] == scale(residual_edge, h[0])
    assert q[1] == scale(residual_edge, h[1])
    assert q[4] == scale(residual_edge, h[4])
    assert q[2] == monomial(3, "b", "x0", "x3", "x4", "y1")
    assert q[3] == monomial(3, "d", "x0", "y1", "y2", "y4")
    assert not h[2] and not h[3]

    g0 = add(
        endpoint_edge(0, 0) and multiply(endpoint_edge(0, 0), h[0]),
        multiply(endpoint_edge(1, 0), h[1]),
    )
    g1 = add(multiply(endpoint_edge(0, 1), h[0]), multiply(endpoint_edge(1, 1), h[1]))
    assert g0 == add(
        monomial(1, "a", "b", "x0", "x1", "x2", "x3", "x4"),
        monomial(1, "c", "d", "y0", "y1", "y2", "y3", "y4"),
    )
    assert g1 == add(
        monomial(1, "a", "b", "x0", "x1", "x2", "x3", "x4"),
        monomial(2, "c", "d", "y0", "y1", "y2", "y3", "y4"),
    )
    assert 1 * 2 - 1 * 1 == 1
    assert 1 * 2 + 1 * 1 == 3
    assert scale(1, g0) == g0

    print("independent no-import simultaneous rank-one hidden-pair audit: PASS")


if __name__ == "__main__":
    main()
