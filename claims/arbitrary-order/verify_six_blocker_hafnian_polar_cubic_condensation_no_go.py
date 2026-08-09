"""Verify the six-vertex hafnian cubic polar-condensation no-go."""

from itertools import combinations, permutations

import sympy as sp

VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
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


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for partner in vertices[1:]:
        rest = tuple(vertex for vertex in vertices if vertex not in (first, partner))
        edge = tuple(sorted((first, partner)))
        for tail in perfect_matchings(rest):
            yield (edge,) + tail


def orbit(template: tuple[tuple[int, int], ...]):
    images = set()
    for permutation in permutations(VERTICES):
        image = tuple(
            sorted(tuple(sorted((permutation[left], permutation[right]))) for left, right in template)
        )
        images.add(image)
    return images


def main() -> None:
    variables = sp.symbols("x01 x02 x03 x04 x05 x12 x13 x14 x15 x23 x24 x25 x34 x35 x45")
    edge_variable = dict(zip(EDGES, variables, strict=True))
    hafnian = sp.expand(
        sum(
            sp.prod(edge_variable[edge] for edge in matching)
            for matching in perfect_matchings(VERTICES)
        )
    )
    assert len(sp.Poly(hafnian, *variables).terms()) == 15
    cofactors = {
        edge: sp.diff(hafnian, edge_variable[edge])
        for edge in EDGES
    }
    assert all(len(sp.Poly(value, *variables).terms()) == 3 for value in cofactors.values())

    orbit_sums = {}
    expected_sizes = {
        "T3": 15,
        "DA": 120,
        "DD": 90,
        "K3": 20,
        "K13": 60,
        "P4": 180,
        "P3K2": 180,
        "3K2": 15,
    }
    for name, template in TEMPLATES.items():
        monomials = orbit(template)
        assert len(monomials) == expected_sizes[name]
        orbit_sums[name] = sp.Poly(
            sp.expand(
                sum(sp.prod(cofactors[edge] for edge in monomial) for monomial in monomials)
            ),
            *variables,
        )

    target = sp.Poly(sp.expand(hafnian**2), *variables)
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
    expected_diagonal = {name: 1 for name in TEMPLATES}
    expected_diagonal["P3K2"] = 2
    for row_name, monomial in private.items():
        assert target.coeff_monomial(monomial) == int(row_name == "3K2")
        for column_name, polynomial in orbit_sums.items():
            expected = expected_diagonal[row_name] if row_name == column_name else 0
            assert polynomial.coeff_monomial(monomial) == expected

    two_triangles = (1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1)
    assert target.coeff_monomial(two_triangles) == 0
    assert orbit_sums["3K2"].coeff_monomial(two_triangles) == 6
    assert all(
        orbit_sums[name].coeff_monomial(two_triangles) == 0
        for name in TEMPLATES
        if name != "3K2"
    )

    print("PASS: eight invariant cubic cofactor orbit types")
    print("PASS: diagonal private-coefficient separation")
    print("PASS: matching coefficient forced to one")
    print("PASS: two-triangle coefficient gives 6=0 contradiction")
    print("SCOPE: higher-weight and tensor-valued cross-depth relations remain UNKNOWN")
    print("graph_support_searches=0 blocker_word_searches=0")


if __name__ == "__main__":
    main()
