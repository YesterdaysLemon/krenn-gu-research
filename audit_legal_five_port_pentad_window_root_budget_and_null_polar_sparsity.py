"""Independent no-import audit of legal pentad-window polar sparsity."""

from __future__ import annotations

from itertools import combinations

Edge = tuple[int, int]
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, int]


CYCLES: tuple[tuple[int, tuple[Edge, ...]], ...] = (
    (1, ((1, 2), (1, 3), (2, 4), (3, 5), (4, 5))),
    (-1, ((1, 2), (1, 3), (2, 5), (3, 4), (4, 5))),
    (-1, ((1, 2), (1, 4), (2, 3), (3, 5), (4, 5))),
    (1, ((1, 2), (1, 4), (2, 5), (3, 4), (3, 5))),
    (1, ((1, 2), (1, 5), (2, 3), (3, 4), (4, 5))),
    (-1, ((1, 2), (1, 5), (2, 4), (3, 4), (3, 5))),
    (1, ((1, 3), (1, 4), (2, 3), (2, 5), (4, 5))),
    (-1, ((1, 3), (1, 4), (2, 4), (2, 5), (3, 5))),
    (-1, ((1, 3), (1, 5), (2, 3), (2, 4), (4, 5))),
    (1, ((1, 3), (1, 5), (2, 4), (2, 5), (3, 4))),
    (-1, ((1, 4), (1, 5), (2, 3), (2, 5), (3, 4))),
    (1, ((1, 4), (1, 5), (2, 3), (2, 4), (3, 5))),
)


def clean(polynomial: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(
                first + second
                for first, second in zip(monomial_left, monomial_right, strict=True)
            )
            result[monomial] = result.get(monomial, 0) + coefficient_left * coefficient_right
    return clean(result)


def monomial(indices: tuple[int, ...], count: int) -> Polynomial:
    exponent = [0] * count
    for index in indices:
        exponent[index] += 1
    return {tuple(exponent): 1}


def scale(polynomial: Polynomial, coefficient: int) -> Polynomial:
    return clean({monomial_key: coefficient * value for monomial_key, value in polynomial.items()})


def sparse_weighted_identity() -> None:
    edges = tuple(combinations(range(1, 6), 2))
    edge_index = {pair: index for index, pair in enumerate(edges)}
    variable_count = 20
    ordinary: Polynomial = {}
    cleared: Polynomial = {}

    for sign, cycle in CYCLES:
        cycle_indices = tuple(edge_index[pair] + 10 for pair in cycle)
        ordinary = add(ordinary, scale(monomial(cycle_indices, variable_count), sign))

        cycle_set = set(cycle)
        legal_indices: list[int] = []
        for pair in cycle:
            index = edge_index[pair]
            legal_indices.extend((index, index + 10))
        for pair in edges:
            if pair not in cycle_set:
                legal_indices.append(edge_index[pair])
        cleared = add(
            cleared,
            scale(monomial(tuple(legal_indices), variable_count), sign),
        )

    shore_product = monomial(tuple(range(10)), variable_count)
    assert cleared == multiply(shore_product, ordinary)
    assert len(cleared) == 12

    active = {(1, 2), (2, 3), (3, 4)}
    for _, cycle in CYCLES:
        assert not set(cycle).issubset(active)


def budget_and_neighbourhood_logic() -> None:
    ledger = []
    for blocker_count in (5, 6, 7):
        roots = blocker_count - 2
        grades = tuple(range(roots, -1, -2))
        ledger.append((blocker_count, roots, grades, roots, roots + 2))
    assert ledger == [
        (5, 3, (3, 1), 3, 5),
        (6, 4, (4, 2, 0), 4, 6),
        (7, 5, (5, 3, 1), 5, 7),
    ]

    neighbourhoods = (
        frozenset({0, 4}),
        frozenset({1, 5}),
        frozenset({2, 6}),
    )
    possible_nonzero_pairs = {
        neighbourhood
        for neighbourhood in neighbourhoods
        if len(neighbourhood) == 2
    }
    assert len(possible_nonzero_pairs) == 3

    for pair in possible_nonzero_pairs:
        witnessing_colours = [
            colour
            for colour, neighbourhood in enumerate(neighbourhoods)
            if neighbourhood.issubset(pair)
        ]
        assert len(witnessing_colours) == 1
        colour = witnessing_colours[0]
        assert neighbourhoods[colour] == pair


def dot(row: tuple[int, int, int], vector: tuple[int, int, int]) -> int:
    return sum(first * second for first, second in zip(row, vector, strict=True))


def integer_null_contraction() -> None:
    modes = tuple(range(5))
    selected = frozenset({0, 1})
    a = tuple((1, 0, mode + 1) for mode in modes)
    b = tuple((0, 1, mode + 2) for mode in modes)
    kappa = tuple((-(mode + 1), -(mode + 2), 1) for mode in modes)
    endpoint = tuple((1, 2, mode + 3) for mode in modes)

    for mode in modes:
        assert dot(a[mode], kappa[mode]) == 0
        assert dot(b[mode], kappa[mode]) == 0

    def evaluate_pair(pair: frozenset[int], vectors: tuple[tuple[int, int, int], ...]) -> int:
        left, right = sorted(pair)
        return dot(a[left], vectors[left]) * dot(b[right], vectors[right]) + dot(
            b[left], vectors[left]
        ) * dot(a[right], vectors[right])

    assert evaluate_pair(selected, endpoint) != 0
    mixed_vectors = list(kappa)
    for mode in selected:
        mixed_vectors[mode] = endpoint[mode]
    vectors = tuple(mixed_vectors)
    for pair_tuple in combinations(modes, 2):
        pair = frozenset(pair_tuple)
        if pair != selected:
            assert evaluate_pair(pair, vectors) == 0


def main() -> None:
    sparse_weighted_identity()
    budget_and_neighbourhood_logic()
    integer_null_contraction()
    print("legal five-port pentad/null-polar sparsity independent audit: PASS")
    print("weighted_sparse_terms: 12")
    print("maximum_colour_certified_pairs: 3")
    print("p5_p6_p7_direct_pair_budget_gap: 2")
    print("global_krenn_gu_resolved: false")


if __name__ == "__main__":
    main()
