"""Symbolic replay for the P7 Boolean-square stationarity master system."""

from itertools import combinations

import sympy as sp

VERTICES = tuple(range(7))
EDGES = tuple(combinations(VERTICES, 2))
FOURSETS = tuple(combinations(VERTICES, 4))
FIVESETS = tuple(combinations(VERTICES, 5))


def add_poly(left, right):
    result = dict(left)
    for subset, coefficient in right.items():
        result[subset] = sp.expand(result.get(subset, 0) + coefficient)
    return {subset: coefficient for subset, coefficient in result.items() if coefficient != 0}


def scale_poly(value, poly):
    return {subset: sp.expand(value * coefficient) for subset, coefficient in poly.items()}


def multiply_poly(left, right):
    result = {}
    for first, x in left.items():
        for second, y in right.items():
            if first & second:
                continue
            subset = first | second
            result[subset] = result.get(subset, 0) + x * y
    return {subset: sp.expand(value) for subset, value in result.items()}


def incidence_rank():
    matrix = sp.zeros(len(FIVESETS), len(FOURSETS))
    for row, five in enumerate(FIVESETS):
        five_set = frozenset(five)
        for col, four in enumerate(FOURSETS):
            matrix[row, col] = int(frozenset(four) < five_set)
    return matrix.rank(), len(FOURSETS) - matrix.rank()


def main():
    a = sp.symbols("a0:7")
    f = sp.symbols("f0:21")
    t = sp.symbols("t")
    ell = {frozenset({i}): sp.Integer(1) for i in VERTICES}
    avec = {frozenset({i}): a[i] for i in VERTICES}
    fpoly = {frozenset(edge): f[k] for k, edge in enumerate(EDGES)}

    ell_a = multiply_poly(ell, avec)
    f_squared = multiply_poly(fpoly, fpoly)
    psi_poly = scale_poly(sp.Rational(1, 2), f_squared)
    phi_poly = multiply_poly(fpoly, ell_a)

    psi = {}
    phi = {}
    for four in FOURSETS:
        four_set = frozenset(four)
        matchings = []
        first = four[0]
        for partner in four[1:]:
            edge = frozenset({first, partner})
            other = four_set - edge
            matchings.append((edge, other))
        psi[four_set] = sum(
            fpoly[edge] * fpoly[other] for edge, other in matchings
        )
        phi[four_set] = sum(
            fpoly[edge] * ell_a[other] + fpoly[other] * ell_a[edge]
            for edge, other in matchings
        )
        assert sp.expand(psi_poly[four_set] - psi[four_set]) == 0
        assert sp.expand(phi_poly[four_set] - phi[four_set]) == 0

    primitive = multiply_poly(ell, psi_poly)
    for five in FIVESETS:
        five_set = frozenset(five)
        expected = sum(psi[five_set - {i}] for i in five)
        assert sp.expand(primitive[five_set] - expected) == 0
    assert incidence_rank() == (21, 14)

    mixed = multiply_poly(multiply_poly(multiply_poly(ell, ell), avec), fpoly)
    lambda_poly = scale_poly(-1, phi_poly)
    assert add_poly(multiply_poly(ell, lambda_poly), mixed) == {}

    annihilator = multiply_poly(
        fpoly,
        add_poly(scale_poly(2, ell_a), scale_poly(t, fpoly)),
    )
    radial = add_poly(scale_poly(2, phi_poly), scale_poly(2 * t, psi_poly))
    assert add_poly(annihilator, scale_poly(-1, radial)) == {}

    # On the generic reconstruction, Phi=-Lambda with the announced signs.
    w = sp.symbols("w0:21")
    x = sp.symbols("x0:7")
    reconstruction = {
        f[k]: -w[k] * (x[i] + x[j]) for k, (i, j) in enumerate(EDGES)
    }
    for four in FOURSETS:
        four_set = frozenset(four)
        lambda_expected = -sp.expand(phi[four_set].subs(reconstruction))
        assert sp.expand(lambda_poly[four_set].subs(reconstruction) - lambda_expected) == 0

    # The two fixed Lefschetz maps used to exclude Psi=0.
    u23 = sp.zeros(35, 21)
    triples = tuple(combinations(VERTICES, 3))
    for row, triple in enumerate(triples):
        triple_set = set(triple)
        for col, edge in enumerate(EDGES):
            u23[row, col] = int(set(edge) < triple_set)
    u34 = sp.zeros(35, 35)
    for row, four in enumerate(FOURSETS):
        four_set = set(four)
        for col, triple in enumerate(triples):
            u34[row, col] = int(set(triple) < four_set)
    assert u23.rank() == 21
    assert u34.det() != 0

    print("PASS: quartet covariants are exactly F^2/2 and -F ell A")
    print("PASS: primitivity places Psi in the fixed 14-dimensional P4")
    print("PASS: the mixed kernel automatically places Lambda in the same P4")
    print("PASS: the full annihilator is exactly t Psi = Lambda")
    print("PASS: square-zero cannot survive the physical full-support maps")
    print("searches=0 finite_fields=0 numerical_points=0 tuple_enumerations=0")
    print("SCOPE: stationary good locus, P7, and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
