"""Primary symbolic checks for the block-square-zero Wick theorem."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


def add_poly(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = sp.expand(out.get(monomial, 0) + coefficient)
        if out[monomial] == 0:
            del out[monomial]
    return out


def mul_poly(left, right):
    """Multiply in the vertex-exclusive algebra.

    A monomial is a sorted tuple of (vertex, colour) pairs.
    """
    out = {}
    for monomial_left, coefficient_left in left.items():
        vertices_left = {vertex for vertex, _ in monomial_left}
        for monomial_right, coefficient_right in right.items():
            if vertices_left & {vertex for vertex, _ in monomial_right}:
                continue
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] = sp.expand(
                out.get(monomial, 0) + coefficient_left * coefficient_right
            )
    return {monomial: value for monomial, value in out.items() if value != 0}


def scale_poly(poly, scalar):
    return {
        monomial: sp.expand(scalar * coefficient)
        for monomial, coefficient in poly.items()
        if coefficient != 0
    }


def exp_nilpotent(quadratic, vertex_count):
    result = {(): sp.Integer(1)}
    power = {(): sp.Integer(1)}
    for degree in range(1, vertex_count // 2 + 1):
        power = mul_poly(power, quadratic)
        result = add_poly(
            result, scale_poly(power, sp.Rational(1, sp.factorial(degree)))
        )
    return result


def log_nilpotent(moment, vertex_count):
    positive = dict(moment)
    positive[()] = sp.expand(positive.get((), 0) - 1)
    if positive.get(()) == 0:
        positive.pop((), None)
    result = {}
    power = {(): sp.Integer(1)}
    for degree in range(1, vertex_count + 1):
        power = mul_poly(power, positive)
        result = add_poly(
            result,
            scale_poly(power, sp.Rational((-1) ** (degree - 1), degree)),
        )
    return result


def check_wick_exponential():
    vertex_count = 4
    colour_count = 2
    weights = {}
    quadratic = {}
    for i, j in combinations(range(vertex_count), 2):
        for a, b in product(range(colour_count), repeat=2):
            weight = sp.Symbol(f"w{i}{j}_{a}{b}")
            weights[i, j, a, b] = weight
            quadratic[((i, a), (j, b))] = weight

    moment = exp_nilpotent(quadratic, vertex_count)
    assert log_nilpotent(moment, vertex_count) == quadratic

    for colours in product(range(colour_count), repeat=vertex_count):
        monomial = tuple(enumerate(colours))
        expected = (
            weights[0, 1, colours[0], colours[1]]
            * weights[2, 3, colours[2], colours[3]]
            + weights[0, 2, colours[0], colours[2]]
            * weights[1, 3, colours[1], colours[3]]
            + weights[0, 3, colours[0], colours[3]]
            * weights[1, 2, colours[1], colours[2]]
        )
        assert sp.expand(moment[monomial] - expected) == 0


def hafnian(matrix, vertices=None):
    if vertices is None:
        vertices = tuple(range(matrix.rows))
    vertices = tuple(vertices)
    if not vertices:
        return sp.Integer(1)
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        total += matrix[first, second] * hafnian(matrix, rest)
    return sp.expand(total)


def check_mixed_hessian_formula():
    t = sp.symbols("t0:3")
    vertex_count = 4
    edges = list(combinations(range(vertex_count), 2))
    quadrics = {}
    for edge_number, edge in enumerate(edges):
        coefficients = sp.symbols(f"a{edge_number}_0:6")
        quadrics[edge] = (
            coefficients[0] * t[0] ** 2
            + coefficients[1] * t[1] ** 2
            + coefficients[2] * t[2] ** 2
            + coefficients[3] * t[0] * t[1]
            + coefficients[4] * t[0] * t[2]
            + coefficients[5] * t[1] * t[2]
        )
    matrix = sp.zeros(vertex_count)
    for (i, j), quadric in quadrics.items():
        matrix[i, j] = matrix[j, i] = quadric

    full = hafnian(matrix)
    for a, b in combinations(range(3), 2):
        rhs = 0
        for edge in edges:
            rest = tuple(vertex for vertex in range(vertex_count) if vertex not in edge)
            rhs += sp.diff(quadrics[edge], t[a], t[b]) * hafnian(matrix, rest)
        for edge, other in combinations(edges, 2):
            if set(edge) & set(other):
                continue
            rhs += sp.diff(quadrics[edge], t[a]) * sp.diff(
                quadrics[other], t[b]
            ) + sp.diff(quadrics[edge], t[b]) * sp.diff(quadrics[other], t[a])
        assert sp.expand(sp.diff(full, t[a], t[b]) - rhs) == 0


def check_fermat_test():
    t = sp.symbols("t0:3")
    n = 8
    fermat = sum(variable**n for variable in t)
    for a, b in combinations(range(3), 2):
        assert sp.diff(fermat, t[a], t[b]) == 0
    for colour in range(3):
        point = {variable: int(index == colour) for index, variable in enumerate(t)}
        assert fermat.subs(point) == 1

    # A generic mixed monomial is detected by a mixed second derivative.
    for exponents in product(range(n + 1), repeat=3):
        if sum(exponents) != n or sum(exponent > 0 for exponent in exponents) < 2:
            continue
        monomial = sp.prod(t[index] ** exponents[index] for index in range(3))
        detected = any(
            sp.diff(monomial, t[a], t[b]) != 0 for a, b in combinations(range(3), 2)
        )
        assert detected


if __name__ == "__main__":
    check_wick_exponential()
    check_mixed_hessian_formula()
    check_fermat_test()
    print("block-square-zero Wick completion primary verifier: PASS")
