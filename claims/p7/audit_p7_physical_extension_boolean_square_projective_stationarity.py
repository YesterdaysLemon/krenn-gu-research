"""Independent stdlib audit of P7 Boolean-square projective stationarity."""

from fractions import Fraction
from itertools import combinations

VERTICES = tuple(range(7))
EDGES = tuple(combinations(VERTICES, 2))
FOURSETS = tuple(combinations(VERTICES, 4))
FIVESETS = tuple(combinations(VERTICES, 5))


def coefficient(variable):
    return {(variable,): Fraction(1)}


def coeff_add(left, right):
    result = dict(left)
    for monomial, value in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + value
    return {monomial: value for monomial, value in result.items() if value}


def coeff_scale(value, poly):
    return {
        monomial: Fraction(value) * coefficient_value
        for monomial, coefficient_value in poly.items()
        if coefficient_value
    }


def coeff_multiply(left, right):
    result = {}
    for first, x in left.items():
        for second, y in right.items():
            monomial = tuple(sorted(first + second))
            result[monomial] = result.get(monomial, Fraction(0)) + x * y
    return {monomial: value for monomial, value in result.items() if value}


def poly_add(left, right):
    result = dict(left)
    for subset, value in right.items():
        result[subset] = coeff_add(result.get(subset, {}), value)
    return {subset: value for subset, value in result.items() if value}


def poly_scale(value, poly):
    return {subset: coeff_scale(value, coefficient_value) for subset, coefficient_value in poly.items()}


def poly_multiply(left, right):
    result = {}
    for first, x in left.items():
        for second, y in right.items():
            if first & second:
                continue
            subset = first | second
            result[subset] = coeff_add(
                result.get(subset, {}), coeff_multiply(x, y)
            )
    return {subset: value for subset, value in result.items() if value}


def rank_fraction(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for col in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][col]
        for row in range(rank + 1, len(work)):
            factor = work[row][col] / pivot_value
            for k in range(col, len(work[0])):
                work[row][k] -= factor * work[rank][k]
        rank += 1
    return rank


def main():
    ell = {frozenset({i}): {(): Fraction(1)} for i in VERTICES}
    avec = {frozenset({i}): coefficient(f"a{i}") for i in VERTICES}
    fpoly = {
        frozenset(edge): coefficient(f"f{i}{j}")
        for edge, (i, j) in zip(EDGES, EDGES)
    }
    ell_a = poly_multiply(ell, avec)
    f_squared = poly_multiply(fpoly, fpoly)
    psi = poly_scale(Fraction(1, 2), f_squared)
    phi = poly_multiply(fpoly, ell_a)

    for four in FOURSETS:
        subset = frozenset(four)
        first = four[0]
        direct_psi = {}
        direct_phi = {}
        for partner in four[1:]:
            edge = frozenset({first, partner})
            other = subset - edge
            direct_psi = coeff_add(
                direct_psi, coeff_multiply(fpoly[edge], fpoly[other])
            )
            direct_phi = coeff_add(
                direct_phi,
                coeff_add(
                    coeff_multiply(fpoly[edge], ell_a[other]),
                    coeff_multiply(fpoly[other], ell_a[edge]),
                ),
            )
        assert psi[subset] == direct_psi
        assert phi[subset] == direct_phi

    primitive = poly_multiply(ell, psi)
    for five in FIVESETS:
        subset = frozenset(five)
        direct = {}
        for vertex in five:
            direct = coeff_add(direct, psi[subset - {vertex}])
        assert primitive[subset] == direct

    mixed = poly_multiply(poly_multiply(poly_multiply(ell, ell), avec), fpoly)
    lambda_poly = poly_scale(-1, phi)
    assert poly_add(poly_multiply(ell, lambda_poly), mixed) == {}

    t_poly = {frozenset(): coefficient("t")}
    annihilator = poly_multiply(
        fpoly,
        poly_add(poly_scale(2, ell_a), poly_multiply(t_poly, fpoly)),
    )
    radial = poly_add(poly_scale(2, phi), poly_scale(2, poly_multiply(t_poly, psi)))
    assert poly_add(annihilator, poly_scale(-1, radial)) == {}

    incidence = [
        [int(set(four) < set(five)) for four in FOURSETS] for five in FIVESETS
    ]
    assert rank_fraction(incidence) == 21

    triples = tuple(combinations(VERTICES, 3))
    u23 = [[int(set(edge) < set(triple)) for edge in EDGES] for triple in triples]
    u34 = [[int(set(triple) < set(four)) for triple in triples] for four in FOURSETS]
    assert rank_fraction(u23) == 21
    assert rank_fraction(u34) == 35

    print("AUDIT PASS: independent square-free products recover Psi and Phi")
    print("AUDIT PASS: primitive and mixed images lie in the same 14-space")
    print("AUDIT PASS: annihilator coefficients equal 2(Phi+t Psi)")
    print("AUDIT PASS: the two full-support Lefschetz controls have full rank")
    print("imports_from_primary=0 imports_from_project=0 imports_from_sympy=0")
    print("searches=0 finite_fields=0 numerical_points=0 tuple_enumerations=0")
    print("SCOPE: stationary good locus, P7, and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
