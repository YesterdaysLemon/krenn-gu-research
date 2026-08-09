"""Independent no-import audit of the six-vertex cubic condensation no-go."""

from fractions import Fraction
from itertools import permutations

VERTICES = tuple(range(6))
EDGES = tuple((left, right) for left in VERTICES for right in VERTICES if left < right)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ZERO = (0,) * len(EDGES)
TEMPLATES = {
    "T3": ((0, 1), (0, 1), (0, 1)),
    "DA": ((0, 1), (0, 1), (0, 2)),
    "DD": ((0, 1), (0, 1), (2, 3)),
    "K3": ((0, 1), (1, 2), (0, 2)),
    "K13": ((0, 1), (0, 2), (0, 3)),
    "P4": ((0, 1), (1, 2), (2, 3)),
    "P3K2": ((0, 1), (1, 2), (3, 4)),
    "3K2": ((0, 1), (2, 3), (4, 5)),
}


def add(left, right):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        if not result[monomial]:
            del result[monomial]
    return result


def multiply(left, right):
    result = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(
                a + b for a, b in zip(monomial_left, monomial_right, strict=True)
            )
            result[monomial] = (
                result.get(monomial, Fraction(0))
                + coefficient_left * coefficient_right
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def edge_monomial(edge):
    exponents = list(ZERO)
    exponents[EDGE_INDEX[tuple(sorted(edge))]] = 1
    return {tuple(exponents): Fraction(1)}


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for partner in vertices[1:]:
        remaining = tuple(vertex for vertex in vertices if vertex not in (first, partner))
        for tail in perfect_matchings(remaining):
            yield (tuple(sorted((first, partner))),) + tail


def product(polynomials):
    result = {ZERO: Fraction(1)}
    for polynomial in polynomials:
        result = multiply(result, polynomial)
    return result


def orbit(template):
    images = set()
    for permutation in permutations(VERTICES):
        images.add(
            tuple(
                sorted(
                    tuple(sorted((permutation[left], permutation[right])))
                    for left, right in template
                )
            )
        )
    return images


def main() -> None:
    hafnian = {}
    for matching in perfect_matchings(VERTICES):
        hafnian = add(hafnian, product(edge_monomial(edge) for edge in matching))
    assert len(hafnian) == 15
    target = multiply(hafnian, hafnian)

    cofactors = {}
    for deleted in EDGES:
        remaining = tuple(vertex for vertex in VERTICES if vertex not in deleted)
        value = {}
        for matching in perfect_matchings(remaining):
            value = add(value, product(edge_monomial(edge) for edge in matching))
        cofactors[deleted] = value
        assert len(value) == 3

    orbit_sums = {}
    for name, template in TEMPLATES.items():
        value = {}
        for cofactor_edges in orbit(template):
            value = add(value, product(cofactors[edge] for edge in cofactor_edges))
        orbit_sums[name] = value

    private = {
        "T3": (3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0),
        "DA": (3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0),
        "DD": (3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1),
        "K3": (3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0),
        "K13": (3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0),
        "P4": (3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0),
        "P3K2": (2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1),
        "3K2": (2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2),
    }
    for row, monomial in private.items():
        assert target.get(monomial, 0) == int(row == "3K2")
        for column, polynomial in orbit_sums.items():
            expected = (2 if row == "P3K2" else 1) if row == column else 0
            assert polynomial.get(monomial, 0) == expected

    two_triangles = (1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1)
    assert target.get(two_triangles, 0) == 0
    assert orbit_sums["3K2"].get(two_triangles, 0) == 6
    assert all(
        orbit_sums[name].get(two_triangles, 0) == 0
        for name in TEMPLATES
        if name != "3K2"
    )

    print("AUDIT PASS: independent rational hafnian/cofactor construction")
    print("AUDIT PASS: eight orbit-private coefficient functionals")
    print("AUDIT PASS: independent two-triangle coefficient equals six")
    print("AUDIT SCOPE: higher polar relation and tensor marked-star bridge open")
    print("project_imports=0 support_searches=0 word_searches=0")


if __name__ == "__main__":
    main()
