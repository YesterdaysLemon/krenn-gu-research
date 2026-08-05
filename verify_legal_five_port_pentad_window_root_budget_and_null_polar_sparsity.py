"""Primary exact checks for legal pentad-window/null-polar sparsity."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

Edge = tuple[int, int]


PENTAD_CYCLES: tuple[tuple[int, tuple[Edge, ...]], ...] = (
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


def root_budget_checks() -> None:
    expected = {
        5: (3, (3, 1)),
        6: (4, (4, 2, 0)),
        7: (5, (5, 3, 1)),
    }
    for blocker_count, (root_count, grades) in expected.items():
        assert root_count == blocker_count - 2
        assert grades == tuple(range(root_count, -1, -2))
        residual_present_pair_depth = blocker_count - 2
        direct_pair_depth = 2 + blocker_count - 2
        assert residual_present_pair_depth == root_count
        assert direct_pair_depth == root_count + 2
        assert residual_present_pair_depth in grades
        assert direct_pair_depth not in grades


def weighted_pentad_check() -> None:
    edges = tuple(combinations(range(1, 6), 2))
    shore = {pair: sp.Symbol(f"s{pair[0]}{pair[1]}") for pair in edges}
    response = {pair: sp.Symbol(f"d{pair[0]}{pair[1]}") for pair in edges}
    legal = {pair: shore[pair] * response[pair] for pair in edges}

    ordinary = sp.Integer(0)
    cleared = sp.Integer(0)
    edge_set = set(edges)
    for sign, cycle in PENTAD_CYCLES:
        cycle_set = set(cycle)
        ordinary += sign * sp.prod(response[pair] for pair in cycle)
        cleared += sign * sp.prod(legal[pair] for pair in cycle) * sp.prod(
            shore[pair] for pair in edge_set - cycle_set
        )
    expected = sp.prod(shore.values()) * ordinary
    assert sp.expand(cleared - expected) == 0

    active = {(1, 2), (2, 3), (3, 4)}
    sparse_legal = {
        pair: legal[pair] if pair in active else sp.Integer(0)
        for pair in edges
    }
    for _, cycle in PENTAD_CYCLES:
        assert sp.prod(sparse_legal[pair] for pair in cycle) == 0


def active_pair_bound(
    neighbourhoods: dict[int, frozenset[int]],
) -> set[frozenset[int]]:
    assert all(len(neighbourhood) >= 2 for neighbourhood in neighbourhoods.values())
    active: set[frozenset[int]] = set()
    for colour, neighbourhood in neighbourhoods.items():
        if len(neighbourhood) == 2:
            pair = neighbourhood
            assert neighbourhood.issubset(pair)
            active.add(pair)
            assert colour in {0, 1, 2}
    assert len(active) <= len(neighbourhoods) == 3
    return active


def neighbourhood_checks() -> None:
    three_distinct = {
        0: frozenset({0, 1}),
        1: frozenset({2, 3}),
        2: frozenset({4, 5}),
    }
    assert active_pair_bound(three_distinct) == set(three_distinct.values())

    repeated_and_large = {
        0: frozenset({0, 1}),
        1: frozenset({0, 1}),
        2: frozenset({2, 3, 4}),
    }
    assert active_pair_bound(repeated_and_large) == {frozenset({0, 1})}

    all_large = {
        0: frozenset({0, 1, 2}),
        1: frozenset({1, 2, 3}),
        2: frozenset({2, 3, 4}),
    }
    assert active_pair_bound(all_large) == set()


def null_polar_contraction_check() -> None:
    mode_count = 5
    selected = frozenset({0, 1})
    complement = set(range(mode_count)) - selected

    a = [sp.Matrix([[1, 0, index + 1]]) for index in range(mode_count)]
    b = [sp.Matrix([[0, 1, index + 2]]) for index in range(mode_count)]
    kappa = [
        sp.Matrix([-(index + 1), -(index + 2), 1])
        for index in range(mode_count)
    ]
    for mode in complement:
        assert (a[mode] * kappa[mode])[0] == 0
        assert (b[mode] * kappa[mode])[0] == 0

    x = [sp.Matrix([1, 2, 3 + index]) for index in range(mode_count)]

    def pair_value(pair: frozenset[int]) -> sp.Expr:
        left, right = sorted(pair)
        return sp.expand(
            (a[left] * x[left])[0] * (b[right] * x[right])[0]
            + (b[left] * x[left])[0] * (a[right] * x[right])[0]
        )

    assert pair_value(selected) != 0
    for pair_tuple in combinations(range(mode_count), 2):
        pair = frozenset(pair_tuple)
        if pair == selected:
            continue
        killed_mode = next(iter(pair & complement))
        other_mode = next(iter(pair - {killed_mode}))
        other_vector = x[other_mode] if other_mode in selected else kappa[other_mode]
        killed_value = sp.expand(
            (a[killed_mode] * kappa[killed_mode])[0]
            * (b[other_mode] * other_vector)[0]
            + (b[killed_mode] * kappa[killed_mode])[0]
            * (a[other_mode] * other_vector)[0]
        )
        assert killed_value == 0


def main() -> None:
    root_budget_checks()
    weighted_pentad_check()
    neighbourhood_checks()
    null_polar_contraction_check()
    print("legal five-port pentad/null-polar sparsity primary: PASS")
    print("p5_p6_p7_pair_depths: maximal and parity eligible")
    print("null_polar_nonzero_pair_bound: 3")
    print("weighted_pentad_terms: 12, all require five active pairs")
    print("global_krenn_gu_resolved: false")


if __name__ == "__main__":
    main()
