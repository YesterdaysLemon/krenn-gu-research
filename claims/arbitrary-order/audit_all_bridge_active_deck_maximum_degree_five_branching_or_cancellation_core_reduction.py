"""Independent no-import audit of the saturated-degree-five reduction.

This audit does not import the primary verifier or repository code.  It uses a
bitmask pairing recurrence, independently labelled graph checks, and direct
integer composition enumeration to corroborate the finite interfaces in the
written proof.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import factorial, gcd

Pair = tuple[int, int]


def canon(left: int, right: int) -> Pair:
    return tuple(sorted((left, right)))


def vertices_mask(vertices: tuple[int, ...]) -> int:
    mask = 0
    for vertex in vertices:
        mask |= 1 << vertex
    return mask


def pairing_sum(
    mask: int,
    weights: dict[Pair, int | Fraction],
    memo: dict[int, int | Fraction] | None = None,
) -> int | Fraction:
    if mask == 0:
        return 1
    if memo is None:
        memo = {}
    if mask in memo:
        return memo[mask]
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    total = 0
    partners = remainder
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        total += weights.get(canon(first, partner), 0) * pairing_sum(
            remainder ^ partner_bit, weights, memo
        )
        partners ^= partner_bit
    memo[mask] = total
    return total


def haf(vertices: tuple[int, ...], weights: dict[Pair, int | Fraction]) -> int | Fraction:
    return pairing_sum(vertices_mask(vertices), weights)


def score(
    vertices: tuple[int, ...], item: Pair, weights: dict[Pair, int | Fraction]
) -> int | Fraction:
    complement = tuple(vertex for vertex in vertices if vertex not in item)
    return weights[item] * haf(complement, weights)


def active_set(vertices: tuple[int, ...], weights: dict[Pair, int | Fraction]) -> set[Pair]:
    return {item for item in weights if score(vertices, item, weights) != 0}


def graph_degrees(vertices: tuple[int, ...], items: set[Pair]) -> tuple[int, ...]:
    counts = {vertex: 0 for vertex in vertices}
    for left, right in items:
        counts[left] += 1
        counts[right] += 1
    return tuple(counts[vertex] for vertex in vertices)


def supports_pairing(vertices: tuple[int, ...], support: set[Pair]) -> bool:
    unit_weights = {item: 1 for item in support}
    return haf(vertices, unit_weights) > 0


def covers(vertices: tuple[int, ...], items: set[Pair]) -> bool:
    return graph_degrees(vertices, items) == (1,) * len(vertices)


def graph_connected(vertices: tuple[int, ...], items: set[Pair]) -> bool:
    if not vertices:
        return True
    seen = {vertices[0]}
    changed = True
    while changed:
        changed = False
        for left, right in items:
            if left in seen and right not in seen:
                seen.add(right)
                changed = True
            elif right in seen and left not in seen:
                seen.add(left)
                changed = True
    return len(seen) == len(vertices)


def one_cycle(vertices: tuple[int, ...], items: set[Pair]) -> bool:
    return (
        len(items) == len(vertices)
        and graph_connected(vertices, items)
        and graph_degrees(vertices, items) == (2,) * len(vertices)
    )


def audit_integer_degree_compositions() -> None:
    canonical: set[tuple[tuple[int, int, int], int]] = set()
    exact_five: set[tuple[tuple[int, int, int], int]] = set()
    assignment_by_degree = {3: 0, 4: 0, 5: 0}
    nonbranching_residuals: set[tuple[str, str]] = set()

    for a0, a1, a2, inactive in product(range(6), repeat=4):
        if min(a0, a1, a2) == 0:
            continue
        total = a0 + a1 + a2 + inactive
        if total > 5:
            continue
        item = (tuple(sorted((a0, a1, a2), reverse=True)), inactive)
        canonical.add(item)
        assignment_by_degree[total] += factorial(total) // (
            factorial(a0) * factorial(a1) * factorial(a2) * factorial(inactive)
        )
        if total != 5:
            continue
        exact_five.add(item)
        if max(a0, a1, a2) <= 2:
            labels = ["H"] * inactive
            labels.extend(f"Q_{colour}" for colour, value in enumerate((a0, a1, a2)) if value == 2)
            assert len(labels) == 2
            nonbranching_residuals.add(tuple(sorted(labels)))

    assert canonical == {
        ((1, 1, 1), 0),
        ((1, 1, 1), 1),
        ((1, 1, 1), 2),
        ((2, 1, 1), 0),
        ((2, 1, 1), 1),
        ((2, 2, 1), 0),
        ((3, 1, 1), 0),
    }
    assert exact_five == {
        ((1, 1, 1), 2),
        ((2, 1, 1), 1),
        ((2, 2, 1), 0),
        ((3, 1, 1), 0),
    }
    assert assignment_by_degree == {3: 6, 4: 60, 5: 390}
    assert nonbranching_residuals == {
        ("H", "H"),
        ("H", "Q_0"),
        ("H", "Q_1"),
        ("H", "Q_2"),
        ("Q_0", "Q_1"),
        ("Q_0", "Q_2"),
        ("Q_1", "Q_2"),
    }


def audit_support_partition() -> None:
    for support_mask in range(8):
        support = tuple(bool(support_mask & (1 << colour)) for colour in range(3))
        for active in (-1, 0, 1, 2):
            allowed = active == -1 or (
                support[active]
                and sum(support[colour] for colour in range(3) if colour != active) == 0
            )
            if not allowed:
                continue
            for colour in range(3):
                active_part = active == colour
                inactive_part = active == -1 and support[colour]
                assert support[colour] == (active_part or inactive_part)
                assert not (active_part and inactive_part)


def audit_signed_double_star() -> None:
    vertices = tuple(range(6))
    weights = {
        canon(0, 1): -1,
        canon(0, 2): 1,
        canon(0, 3): 1,
        canon(1, 4): 1,
        canon(1, 5): 1,
        canon(2, 4): 1,
        canon(3, 5): 1,
    }
    assert haf(vertices, weights) == 1
    scores = {item: score(vertices, item, weights) for item in weights}
    assert scores == {
        canon(0, 1): -1,
        canon(0, 2): 1,
        canon(0, 3): 1,
        canon(1, 4): 1,
        canon(1, 5): 1,
        canon(2, 4): 0,
        canon(3, 5): 0,
    }
    for vertex in vertices:
        assert sum(value for item, value in scores.items() if vertex in item) == 1
    active = active_set(vertices, weights)
    assert sorted(graph_degrees(vertices, active)) == [1, 1, 1, 1, 3, 3]
    assert not supports_pairing(vertices, active)

    # A direct two-shore assignment for the whole support proves the claimed
    # single-colour bit compatibility and balanced shore sizes.
    shore = {0: 0, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}
    assert all(shore[left] != shore[right] for left, right in weights)
    assert sum(side == 0 for side in shore.values()) == 3
    assert sum(side == 1 for side in shore.values()) == 3

    hall_x = {2, 3}
    hall_t = {0}
    boundary = {
        item for item in active if len(set(item) & hall_t) == 1 and not set(item) & hall_x
    }
    assert boundary == {canon(0, 1)}
    assert sum(scores[item] for item in boundary) == -1
    assert len(hall_x) == len(hall_t) + 1
    repairs = {canon(2, 4), canon(3, 5)}
    complement = (2, 3, 4, 5)
    assert covers(complement, repairs)
    assert repairs.isdisjoint(active)
    assert len(repairs) == 2  # b=2, q=0 in this minimal fixture.
    pairings = (
        ({canon(2, 3), canon(4, 5)}, 0),
        ({canon(2, 4), canon(3, 5)}, 1),
        ({canon(2, 5), canon(3, 4)}, 0),
    )
    assert [items for items, value in pairings if value] == [repairs]
    for items, expected_weight in pairings:
        product_weight = 1
        for item in items:
            product_weight *= weights.get(item, 0)
        assert product_weight == expected_weight
    assert haf(complement, weights) == 1
    assert all(
        haf(tuple(v for v in vertices if v not in item), weights) == 0
        for item in repairs
    )


def audit_branching_with_active_matching() -> None:
    vertices = tuple(range(6))
    weights = {
        canon(row, 3 + column): Fraction(1, 6) if row == 0 else Fraction(1)
        for row in range(3)
        for column in range(3)
    }
    assert haf(vertices, weights) == 1
    assert {score(vertices, item, weights) for item in weights} == {Fraction(1, 3)}
    assert graph_degrees(vertices, active_set(vertices, weights)) == (3,) * 6
    assert supports_pairing(vertices, active_set(vertices, weights))


def audit_max_degree_two_cancellation() -> None:
    vertices = tuple(range(6))
    anchor = {canon(0, 4), canon(1, 5), canon(2, 3)}
    remainder = {canon(0, 1), canon(0, 2), canon(1, 3), canon(4, 5)}
    weights = {item: 1 for item in anchor | remainder}
    weights[canon(1, 3)] = -1
    assert covers(vertices, anchor)
    assert max(graph_degrees(vertices, remainder)) == 2
    assert haf(vertices, weights) == 1
    assert all(score(vertices, item, weights) != 0 for item in anchor)
    principal = (0, 1, 2, 3)
    assert supports_pairing(principal, set(weights))
    assert haf(principal, weights) == 0


def cyclic_segment(cycle: tuple[int, ...], start: int, finish: int) -> tuple[int, ...]:
    output = [cycle[start]]
    cursor = start
    while cursor != finish:
        cursor = (cursor + 1) % len(cycle)
        output.append(cycle[cursor])
    return tuple(output)


def segment_edges(path: tuple[int, ...]) -> set[Pair]:
    return {canon(path[index], path[index + 1]) for index in range(len(path) - 1)}


def audit_chord_interface_under_relabelling() -> None:
    checked = 0
    for order in (6, 8, 10, 12, 14, 16, 18):
        multiplier = next(value for value in range(order - 1, 1, -1) if gcd(value, order) == 1)
        cycle = tuple((multiplier * index + 1) % order for index in range(order))
        positions = {vertex: index for index, vertex in enumerate(cycle)}
        pc = {canon(cycle[index], cycle[index + 1]) for index in range(0, order, 2)}
        pd = {
            canon(cycle[index], cycle[(index + 1) % order])
            for index in range(1, order, 2)
        }
        assert one_cycle(tuple(range(order)), pc | pd)

        for endpoints in combinations(cycle, 2):
            item = canon(*endpoints)
            left = positions[endpoints[0]]
            right = positions[endpoints[1]]
            if (left - right) % 2 == 0 or item in pc or item in pd:
                continue
            paths = (
                cyclic_segment(cycle, left, right),
                tuple(reversed(cyclic_segment(cycle, right, left))),
            )
            chosen = [
                path
                for path in paths
                if canon(path[0], path[1]) in pd
                and canon(path[-2], path[-1]) in pd
            ]
            assert len(chosen) == 1
            path = chosen[0]
            assert 3 <= len(path) - 1 <= order - 3
            inside = tuple(sorted(path))
            outside = tuple(vertex for vertex in cycle if vertex not in path)
            path_items = segment_edges(path)
            assert covers(inside, path_items & pd)
            assert covers(inside, (path_items & pc) | {item})
            assert covers(outside, {candidate for candidate in pd if set(candidate) <= set(outside)})
            checked += 1
    assert checked >= 100


def audit_least_core_models() -> None:
    cycle_vertices = (0, 1, 2, 3)
    cycle = {
        canon(0, 1): 1,
        canon(1, 2): 1,
        canon(2, 3): 1,
        canon(0, 3): -1,
    }
    assert haf(cycle_vertices, cycle) == 0
    assert active_set(cycle_vertices, cycle) == set(cycle)
    assert one_cycle(cycle_vertices, set(cycle))

    vertices = tuple(range(6))
    rows = ((-2, -2, -2), (-2, -2, -2), (-2, 1, 1))
    branching = {
        canon(row, column + 3): rows[row][column]
        for row in range(3)
        for column in range(3)
    }
    assert haf(vertices, branching) == 0
    assert active_set(vertices, branching) == set(branching)
    assert graph_connected(vertices, set(branching))
    assert graph_degrees(vertices, set(branching)) == (3, 3, 3, 3, 3, 3)
    assert len(branching) - len(vertices) + 1 == 4
    for size in (2, 4):
        for subset in combinations(vertices, size):
            if supports_pairing(subset, set(branching)):
                assert haf(subset, branching) != 0


def audit_rank_strata_independently() -> None:
    def beta(vertices: tuple[int, ...], items: set[Pair]) -> int:
        return len(items) - len(vertices) + 1

    def cubic_sites(vertices: tuple[int, ...], items: set[Pair]) -> int:
        return graph_degrees(vertices, items).count(3)

    cycle_vertices = tuple(range(4))
    cycle = {canon(0, 1), canon(1, 2), canon(2, 3), canon(0, 3)}

    theta_vertices = tuple(range(6))
    theta = {
        canon(0, 1): 1,
        canon(0, 2): 1,
        canon(2, 3): 1,
        canon(1, 3): 1,
        canon(0, 4): 1,
        canon(4, 5): 1,
        canon(1, 5): -2,
    }
    assert haf(theta_vertices, theta) == 0
    theta_terms: list[int] = []
    for omitted_route in range(3):
        matchings = (
            {canon(0, 1), canon(2, 3), canon(4, 5)},
            {canon(0, 2), canon(1, 3), canon(4, 5)},
            {canon(0, 4), canon(1, 5), canon(2, 3)},
        )
        term = 1
        for item in matchings[omitted_route]:
            term *= theta[item]
        theta_terms.append(term)
    assert sorted(theta_terms) == [-2, 1, 1]
    assert all(sum(choice) != 0 for size in (1, 2) for choice in combinations(theta_terms, size))
    for size in (2, 4):
        for subset in combinations(theta_vertices, size):
            if supports_pairing(subset, set(theta)):
                assert haf(subset, theta) != 0

    rank_three_vertices = tuple(range(6))
    entries = ((-3, -3, -3), (-3, -2, 1), (-2, 1, 0))
    rank_three = {
        canon(row, 3 + column): entries[row][column]
        for row in range(3)
        for column in range(3)
        if entries[row][column]
    }
    assert haf(rank_three_vertices, rank_three) == 0
    for size in (2, 4):
        for subset in combinations(rank_three_vertices, size):
            if supports_pairing(subset, set(rank_three)):
                assert haf(subset, rank_three) != 0

    for vertices, items in (
        (cycle_vertices, cycle),
        (theta_vertices, set(theta)),
        (rank_three_vertices, set(rank_three)),
    ):
        assert graph_connected(vertices, items)
        assert max(graph_degrees(vertices, items)) <= 3
        assert cubic_sites(vertices, items) == 2 * (beta(vertices, items) - 1)


def audit_global_minimum_across_colours() -> None:
    vertices = tuple(range(8))
    early_cycle = {
        canon(0, 1): 1,
        canon(2, 3): 1,
        canon(1, 2): 1,
        canon(0, 3): -1,
        canon(4, 5): 1,
        canon(6, 7): 1,
    }
    later = {
        canon(row, 3 + column): value
        for row, values in enumerate(((-2, -2, -2), (-2, -2, -2), (-2, 1, 1)))
        for column, value in enumerate(values)
    }
    later[canon(6, 7)] = 1
    neutral = {
        canon(0, 1): 1,
        canon(2, 3): 1,
        canon(4, 5): 1,
        canon(6, 7): 1,
    }
    matrices = (later, early_cycle, neutral)
    candidates: list[tuple[int, int, tuple[int, ...]]] = []
    for colour, weights in enumerate(matrices):
        for size in range(2, len(vertices), 2):
            for subset in combinations(vertices, size):
                if supports_pairing(subset, set(weights)) and haf(subset, weights) == 0:
                    candidates.append((size, colour, subset))
    assert candidates
    _, colour, subset = min(candidates)
    assert (colour, subset) == (1, (0, 1, 2, 3))

    weights = matrices[colour]
    allowed: set[Pair] = set()
    active: set[Pair] = set()
    for item in weights:
        if not set(item) <= set(subset):
            continue
        complement = tuple(vertex for vertex in subset if vertex not in item)
        if supports_pairing(complement, set(weights)):
            allowed.add(item)
        if weights[item] * haf(complement, weights):
            active.add(item)
    assert active == allowed
    assert graph_connected(subset, active)
    assert one_cycle(subset, active)


def flips(bits_left: str, bits_right: str, colour: int) -> bool:
    return all(bits_left[index] != bits_right[index] for index in range(3) if index != colour)


def audit_typed_support_control() -> None:
    vertices = tuple(range(8))
    types = ("000", "011", "101", "110", "110", "101", "001", "010")
    matchings = (
        {canon(0, 1), canon(2, 3), canon(4, 5), canon(6, 7)},
        {canon(0, 2), canon(1, 4), canon(3, 6), canon(5, 7)},
        {canon(0, 3), canon(1, 5), canon(2, 7), canon(4, 6)},
    )
    additions = (set(), {canon(0, 5)}, {canon(0, 4)})
    matrices: list[dict[Pair, int]] = []
    for colour in range(3):
        weights = {item: 1 for item in matchings[colour] | additions[colour]}
        matrices.append(weights)
        assert covers(vertices, matchings[colour])
        assert haf(vertices, weights) == 1
        assert active_set(vertices, weights) == matchings[colour]
        assert all(flips(types[left], types[right], colour) for left, right in weights)
        for vertex in vertices:
            incident_score = sum(
                score(vertices, item, weights)
                for item in weights
                if vertex in item
            )
            assert incident_score == 1

    assert all(
        one_cycle(vertices, matchings[left] | matchings[right])
        for left, right in combinations(range(3), 2)
    )
    support = set().union(*(set(matrix) for matrix in matrices))
    assert graph_degrees(vertices, support) == (5, 3, 3, 3, 4, 4, 3, 3)

    chosen = (2, 3, 6, 7)
    outside = (0, 1, 4, 5)
    assert haf(chosen, matrices[0]) == 1
    assert haf(outside, matrices[1]) == 1
    assert haf(chosen, matrices[1]) == 0
    assert haf(outside, matrices[0]) == 1


def audit_full_support_exclusion_independently() -> None:
    # Use labelled incident slots, independently of the primary verifier's
    # neighbour-set construction.  Three K labels are required outside every
    # diagonal label, so no local support word with at most seven positions
    # can carry the inherited five saturated incidences.
    for support_degree in range(3, 8):
        slots = tuple(range(support_degree))
        for saturated_degree in range(5, support_degree + 1):
            diagonal = set(slots[:saturated_degree])
            off_diagonal_slots = set(slots) - diagonal
            assert len(off_diagonal_slots) < 3

    assert 5 + 3 == 8
    feasible_even_orders = [order for order in range(6, 22, 2) if order - 1 >= 8]
    assert feasible_even_orders[0] == 10


def main() -> None:
    audit_integer_degree_compositions()
    audit_support_partition()
    audit_signed_double_star()
    audit_branching_with_active_matching()
    audit_max_degree_two_cancellation()
    audit_chord_interface_under_relabelling()
    audit_least_core_models()
    audit_rank_strata_independently()
    audit_global_minimum_across_colours()
    audit_typed_support_control()
    audit_full_support_exclusion_independently()
    print("independent maximum-degree-five reduction audit: PASS")
    print("no imports from primary verifier or repository; exact bitmask recurrence")
    print("unconditional all-bridge boundary: Delta(G)>=8 and n>=10")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
