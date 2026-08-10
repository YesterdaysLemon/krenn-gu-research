"""Independent no-import audit for block-square-zero Wick completion."""

from fractions import Fraction
from itertools import combinations


def poly_add(left, right):
    out = dict(left)
    for exponent, coefficient in right.items():
        out[exponent] = out.get(exponent, 0) + coefficient
        if out[exponent] == 0:
            del out[exponent]
    return out


def poly_mul(left, right):
    out = {}
    for exponent_left, coefficient_left in left.items():
        for exponent_right, coefficient_right in right.items():
            exponent = tuple(a + b for a, b in zip(exponent_left, exponent_right))
            out[exponent] = out.get(exponent, 0) + coefficient_left * coefficient_right
    return {key: value for key, value in out.items() if value}


def poly_scale(poly, scalar):
    return {exponent: coefficient * scalar for exponent, coefficient in poly.items()}


def derivative(poly, variable):
    out = {}
    for exponent, coefficient in poly.items():
        if exponent[variable] == 0:
            continue
        new_exponent = list(exponent)
        new_exponent[variable] -= 1
        key = tuple(new_exponent)
        out[key] = out.get(key, 0) + coefficient * exponent[variable]
    return out


def vertex_mul(left, right):
    out = {}
    for monomial_left, coefficient_left in left.items():
        vertices_left = {vertex for vertex, _ in monomial_left}
        for monomial_right, coefficient_right in right.items():
            if vertices_left & {vertex for vertex, _ in monomial_right}:
                continue
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] = out.get(monomial, 0) + coefficient_left * coefficient_right
    return {key: value for key, value in out.items() if value}


def vertex_add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, 0) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def vertex_scale(poly, scalar):
    return {monomial: coefficient * scalar for monomial, coefficient in poly.items()}


def factorial(number):
    result = 1
    for factor in range(2, number + 1):
        result *= factor
    return result


def nilpotent_exp(quadratic, vertex_count):
    result = {(): Fraction(1)}
    power = {(): Fraction(1)}
    for degree in range(1, vertex_count // 2 + 1):
        power = vertex_mul(power, quadratic)
        result = vertex_add(result, vertex_scale(power, Fraction(1, factorial(degree))))
    return result


def nilpotent_log(moment, vertex_count):
    positive = dict(moment)
    positive[()] = positive.get((), 0) - 1
    positive.pop((), None)
    result = {}
    power = {(): Fraction(1)}
    for degree in range(1, vertex_count + 1):
        power = vertex_mul(power, positive)
        result = vertex_add(
            result,
            vertex_scale(power, Fraction((-1) ** (degree - 1), degree)),
        )
    return result


def hafnian_polynomial(edge_polys, vertices):
    vertices = tuple(vertices)
    if not vertices:
        return {(0, 0, 0): 1}
    first = vertices[0]
    total = {}
    for position in range(1, len(vertices)):
        second = vertices[position]
        edge = tuple(sorted((first, second)))
        rest = vertices[1:position] + vertices[position + 1 :]
        total = poly_add(
            total, poly_mul(edge_polys[edge], hafnian_polynomial(edge_polys, rest))
        )
    return total


def audit_logarithm():
    vertex_count = 6
    quadratic = {}
    for i, j in combinations(range(vertex_count), 2):
        # Two colours, deliberately nonsymmetric colour blocks.
        for a in range(2):
            for b in range(2):
                quadratic[((i, a), (j, b))] = Fraction(
                    1 + 11 * i + 7 * j + 3 * a - 2 * b
                )
    moment = nilpotent_exp(quadratic, vertex_count)
    assert nilpotent_log(moment, vertex_count) == quadratic
    assert nilpotent_exp(nilpotent_log(moment, vertex_count), vertex_count) == moment


def audit_hessian():
    vertex_count = 6
    edge_polys = {}
    for edge_number, edge in enumerate(combinations(range(vertex_count), 2)):
        # Dense ternary quadrics with exact integer coefficients.
        terms = {}
        exponents = ((2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1))
        for term_number, exponent in enumerate(exponents):
            terms[exponent] = 1 + 5 * edge_number - 3 * term_number
        edge_polys[edge] = terms

    vertices = tuple(range(vertex_count))
    full = hafnian_polynomial(edge_polys, vertices)
    for a, b in combinations(range(3), 2):
        direct = derivative(derivative(full, a), b)
        rhs = {}
        edges = list(edge_polys)
        for edge in edges:
            rest = tuple(vertex for vertex in vertices if vertex not in edge)
            term = poly_mul(
                derivative(derivative(edge_polys[edge], a), b),
                hafnian_polynomial(edge_polys, rest),
            )
            rhs = poly_add(rhs, term)
        for edge, other in combinations(edges, 2):
            if set(edge) & set(other):
                continue
            rest = tuple(
                vertex
                for vertex in vertices
                if vertex not in edge and vertex not in other
            )
            cofactor = hafnian_polynomial(edge_polys, rest)
            first = poly_mul(
                derivative(edge_polys[edge], a), derivative(edge_polys[other], b)
            )
            second = poly_mul(
                derivative(edge_polys[edge], b), derivative(edge_polys[other], a)
            )
            rhs = poly_add(rhs, poly_mul(poly_add(first, second), cofactor))
        assert direct == rhs


if __name__ == "__main__":
    audit_logarithm()
    audit_hessian()
    print("block-square-zero Wick completion independent audit: PASS")
