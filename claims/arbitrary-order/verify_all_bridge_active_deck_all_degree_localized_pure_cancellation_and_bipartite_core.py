"""Exact focused checks for the all-degree all-bridge core reduction.

The accompanying written argument is arbitrary-order.  This standalone
stdlib verifier checks its finite combinatorial mechanisms and sharp controls:

* selected-triple component/chord geometry through bounded even order;
* the Hall-deficient two-repair control with exact hafnians and scores;
* bipartite shore excess, the beta-one/beta-two classifications, and the
  perfect-matching-polytope dimension on all small labelled core graphs;
* the matching-count/port-aggregate implication; and
* the exact sparse Theta_d and aggregate K_(3,3) weighted controls.

It imports no repository module, does not enumerate arbitrary order, and does
not search for Krenn--Gu witnesses.  The global conjecture is UNRESOLVED.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, permutations

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def edge(left: int, right: int) -> Edge:
    """Return an undirected edge in canonical order."""

    assert left != right
    return (left, right) if left < right else (right, left)


def all_edges(vertices: tuple[int, ...]) -> set[Edge]:
    return {edge(left, right) for left, right in combinations(vertices, 2)}


def degrees(vertices: tuple[int, ...], items: set[Edge]) -> dict[int, int]:
    output = {vertex: 0 for vertex in vertices}
    for left, right in items:
        output[left] += 1
        output[right] += 1
    return output


def is_matching_on(vertices: set[int], items: set[Edge]) -> bool:
    return all(
        sum(vertex in item for item in items) == 1
        for vertex in vertices
    ) and all(set(item) <= vertices for item in items)


def adjacency(vertices: tuple[int, ...], items: set[Edge]) -> dict[int, set[int]]:
    output = {vertex: set() for vertex in vertices}
    for left, right in items:
        output[left].add(right)
        output[right].add(left)
    return output


def connected_components(
    vertices: tuple[int, ...], items: set[Edge]
) -> tuple[frozenset[int], ...]:
    neighbours = adjacency(vertices, items)
    unseen = set(vertices)
    output: list[frozenset[int]] = []
    while unseen:
        start = min(unseen)
        component = {start}
        queue = deque([start])
        unseen.remove(start)
        while queue:
            current = queue.popleft()
            for neighbour in neighbours[current]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        output.append(frozenset(component))
    return tuple(output)


def is_connected(vertices: tuple[int, ...], items: set[Edge]) -> bool:
    return len(connected_components(vertices, items)) == 1


def bipartition(
    vertices: tuple[int, ...], items: set[Edge]
) -> tuple[frozenset[int], frozenset[int]]:
    neighbours = adjacency(vertices, items)
    side: dict[int, int] = {}
    for start in vertices:
        if start in side:
            continue
        side[start] = 0
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in neighbours[current]:
                wanted = 1 - side[current]
                if neighbour in side:
                    assert side[neighbour] == wanted
                else:
                    side[neighbour] = wanted
                    queue.append(neighbour)
    return (
        frozenset(vertex for vertex, value in side.items() if value == 0),
        frozenset(vertex for vertex, value in side.items() if value == 1),
    )


@cache
def complete_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    """Enumerate all perfect matchings on a complete labelled vertex set."""

    if not vertices:
        return ((),)
    first = vertices[0]
    output: list[Matching] = []
    for position, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in complete_matchings(remainder):
            output.append((edge(first, partner), *tail))
    return tuple(output)


class ExactHafnian:
    """Exact support matching and hafnian recursion on vertices 0,...,n-1."""

    def __init__(self, order: int, weights: dict[Edge, int | Fraction]) -> None:
        self.order = order
        self.weights = {
            item: Fraction(value) for item, value in weights.items() if value
        }
        self._hafnian_cache: dict[int, Fraction] = {0: Fraction(1)}
        self._matching_cache: dict[int, tuple[Matching, ...]] = {0: ((),)}

    def mask(self, vertices: tuple[int, ...] | set[int]) -> int:
        output = 0
        for vertex in vertices:
            assert 0 <= vertex < self.order
            output |= 1 << vertex
        return output

    def hafnian_mask(self, mask: int) -> Fraction:
        if mask in self._hafnian_cache:
            return self._hafnian_cache[mask]
        if mask.bit_count() % 2:
            return Fraction(0)
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        total = Fraction(0)
        scan = remainder
        while scan:
            partner_bit = scan & -scan
            partner = partner_bit.bit_length() - 1
            value = self.weights.get(edge(first, partner), Fraction(0))
            if value:
                total += value * self.hafnian_mask(remainder ^ partner_bit)
            scan ^= partner_bit
        self._hafnian_cache[mask] = total
        return total

    def hafnian(self, vertices: tuple[int, ...] | set[int]) -> Fraction:
        return self.hafnian_mask(self.mask(vertices))

    def matchings_mask(self, mask: int) -> tuple[Matching, ...]:
        if mask in self._matching_cache:
            return self._matching_cache[mask]
        if mask.bit_count() % 2:
            return ()
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        output: list[Matching] = []
        scan = remainder
        while scan:
            partner_bit = scan & -scan
            partner = partner_bit.bit_length() - 1
            item = edge(first, partner)
            if item in self.weights:
                for tail in self.matchings_mask(remainder ^ partner_bit):
                    output.append((item, *tail))
            scan ^= partner_bit
        result = tuple(output)
        self._matching_cache[mask] = result
        return result

    def matchings(self, vertices: tuple[int, ...] | set[int]) -> tuple[Matching, ...]:
        return self.matchings_mask(self.mask(vertices))

    def matching_weight(self, matching: Matching) -> Fraction:
        output = Fraction(1)
        for item in matching:
            output *= self.weights[item]
        return output


def rational_rank(matrix: list[list[int | Fraction]]) -> int:
    """Compute exact row rank by Fraction Gaussian elimination."""

    if not matrix:
        return 0
    rows = [[Fraction(value) for value in row] for row in matrix]
    column_count = len(rows[0])
    assert all(len(row) == column_count for row in rows)
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def matching_incidence_rank(matchings: tuple[Matching, ...], items: set[Edge]) -> int:
    """Affine rank of the perfect-matching incidence points."""

    assert matchings
    edge_order = tuple(sorted(items))
    reference = set(matchings[0])
    differences = [
        [int(item in matching) - int(item in reference) for item in edge_order]
        for matching in map(set, matchings[1:])
    ]
    return rational_rank(differences)


def incidence_rank(vertices: tuple[int, ...], items: set[Edge]) -> int:
    edge_order = tuple(sorted(items))
    return rational_rank(
        [[int(vertex in item) for item in edge_order] for vertex in vertices]
    )


def cycle_paths(
    vertices: tuple[int, ...], cycle: set[Edge], start: int, finish: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the two simple start--finish paths in one cycle."""

    neighbours = adjacency(vertices, cycle)
    assert all(len(neighbours[vertex]) == 2 for vertex in vertices)
    output: list[tuple[int, ...]] = []
    for first in sorted(neighbours[start]):
        path = [start, first]
        previous, current = start, first
        while current != finish:
            choices = neighbours[current] - {previous}
            assert len(choices) == 1
            following = next(iter(choices))
            assert following not in path or following == finish
            path.append(following)
            previous, current = current, following
        output.append(tuple(path))
    assert len(output) == 2
    assert len(output[0]) + len(output[1]) - 2 == len(vertices)
    return output[0], output[1]


def path_edges(path: tuple[int, ...]) -> tuple[Edge, ...]:
    return tuple(edge(left, right) for left, right in pairwise(path))


def verify_component_localization(
    vertices: tuple[int, ...], first: set[Edge], second: set[Edge]
) -> int:
    union = first | second
    components = connected_components(vertices, union)
    assert len(components) >= 2
    checked = 0
    for component in components:
        shore = set(component)
        complement = set(vertices) - shore
        assert shore and complement
        assert len(shore) % 2 == len(complement) % 2 == 0
        assert is_matching_on(shore, {item for item in first if set(item) <= shore})
        assert is_matching_on(
            complement, {item for item in second if set(item) <= complement}
        )
        checked += 1
    return checked


def cycle_bit_side(
    vertices: tuple[int, ...], first: set[Edge], second: set[Edge]
) -> dict[int, int]:
    union = first | second
    assert is_connected(vertices, union)
    left, right = bipartition(vertices, union)
    assert len(left) == len(right)
    return {vertex: int(vertex in right) for vertex in vertices}


def verify_chord_localization(
    vertices: tuple[int, ...],
    chord: Edge,
    colour_matching: set[Edge],
    other_matching: set[Edge],
) -> None:
    """Check the odd other--other arc and its two supported cut factors."""

    cycle = colour_matching | other_matching
    assert chord not in cycle
    assert is_connected(vertices, cycle)
    paths = cycle_paths(vertices, cycle, *chord)
    assert all((len(path) - 1) % 2 == 1 for path in paths)
    other_paths = [
        path
        for path in paths
        if path_edges(path)[0] in other_matching
        and path_edges(path)[-1] in other_matching
    ]
    assert len(other_paths) == 1
    selected = other_paths[0]
    length = len(selected) - 1
    assert 1 < length < len(vertices) - 1
    shore = set(selected)
    complement = set(vertices) - shore
    assert len(shore) % 2 == len(complement) % 2 == 0
    other_on_shore = {item for item in other_matching if set(item) <= shore}
    other_off_shore = {
        item for item in other_matching if set(item) <= complement
    }
    colour_on_shore = {
        item for item in colour_matching if set(item) <= shore
    } | {chord}
    assert is_matching_on(shore, other_on_shore)
    assert is_matching_on(complement, other_off_shore)
    assert is_matching_on(shore, colour_on_shore)


def verify_selected_triple_geometry() -> dict[int, tuple[int, int, int, int]]:
    """Exhaust selected triples up to relabelling of the first matching."""

    summary: dict[int, tuple[int, int, int, int]] = {}
    for order in (4, 6, 8):
        vertices = tuple(range(order))
        matchings = complete_matchings(vertices)
        first = frozenset(edge(2 * index, 2 * index + 1) for index in range(order // 2))
        triples = 0
        disconnected_triples = 0
        hamiltonian_triples = 0
        localized_checks = 0
        complete = all_edges(vertices)
        for second_tuple in matchings:
            second = frozenset(second_tuple)
            if first & second:
                continue
            for third_tuple in matchings:
                third = frozenset(third_tuple)
                if (first | second) & third:
                    continue
                selected = (set(first), set(second), set(third))
                triples += 1
                pair_components: dict[tuple[int, int], int] = {}
                for colour, other in combinations(range(3), 2):
                    union = selected[colour] | selected[other]
                    assert all(
                        value == 2 for value in degrees(vertices, union).values()
                    )
                    pair_components[(colour, other)] = len(
                        connected_components(vertices, union)
                    )
                if any(value > 1 for value in pair_components.values()):
                    disconnected_triples += 1
                    for (colour, other), count in pair_components.items():
                        if count > 1:
                            localized_checks += verify_component_localization(
                                vertices, selected[colour], selected[other]
                            )
                    continue

                hamiltonian_triples += 1
                # Pair P_i union P_j bipartitions the third normal bit.
                bit_side: dict[int, dict[int, int]] = {}
                for bit in range(3):
                    colours = [colour for colour in range(3) if colour != bit]
                    bit_side[bit] = cycle_bit_side(
                        vertices, selected[colours[0]], selected[colours[1]]
                    )
                residual = complete - set().union(*selected)
                for chord in residual:
                    for colour in range(3):
                        # A saturated colour-c edge flips both non-c bits.
                        if not all(
                            bit_side[bit][chord[0]] != bit_side[bit][chord[1]]
                            for bit in range(3)
                            if bit != colour
                        ):
                            continue
                        for other in range(3):
                            if other == colour:
                                continue
                            verify_chord_localization(
                                vertices,
                                chord,
                                selected[colour],
                                selected[other],
                            )
                            localized_checks += 1
        assert triples > 0
        if order == 4:
            # K4's one-factorization has no residual edge.  This is the exact
            # control showing why nonempty R_P (from Delta(D)>=5) is needed.
            assert hamiltonian_triples > 0
            assert localized_checks == 0
        elif localized_checks == 0:
            # A bounded selected triple need not admit a residual physical
            # pair that flips both required normal bits.  The chord theorem is
            # conditional on such a saturated residual edge; topology alone
            # does not assert its existence.
            assert hamiltonian_triples > 0 or disconnected_triples > 0
        summary[order] = (
            triples,
            disconnected_triples,
            hamiltonian_triples,
            localized_checks,
        )
    return summary


def verify_hall_deficient_control() -> None:
    """Replay the exact six-vertex Hall shore and its two inactive repairs."""

    vertices = tuple(range(6))
    weights = {
        edge(0, 1): Fraction(-1),
        edge(0, 2): Fraction(1),
        edge(0, 3): Fraction(1),
        edge(1, 4): Fraction(1),
        edge(1, 5): Fraction(1),
        edge(2, 4): Fraction(1),
        edge(3, 5): Fraction(1),
    }
    system = ExactHafnian(6, weights)
    full_mask = (1 << 6) - 1
    full_matchings = system.matchings_mask(full_mask)
    assert sorted(system.matching_weight(item) for item in full_matchings) == [
        -1,
        1,
        1,
    ]
    assert system.hafnian_mask(full_mask) == 1

    scores: dict[Edge, Fraction] = {}
    for item, value in system.weights.items():
        complement_mask = full_mask ^ system.mask(set(item))
        scores[item] = value * system.hafnian_mask(complement_mask)
    expected = {
        edge(0, 1): Fraction(-1),
        edge(0, 2): Fraction(1),
        edge(0, 3): Fraction(1),
        edge(1, 4): Fraction(1),
        edge(1, 5): Fraction(1),
        edge(2, 4): Fraction(0),
        edge(3, 5): Fraction(0),
    }
    assert scores == expected
    for vertex in vertices:
        assert sum(value for item, value in scores.items() if vertex in item) == 1

    active = {item for item, value in scores.items() if value}
    assert not any(set(matching) <= active for matching in complete_matchings(vertices))
    left, right = bipartition(vertices, set(weights))
    assert {left, right} == {frozenset({0, 4, 5}), frozenset({1, 2, 3})}

    hall_shore = {1, 2, 3}
    hall_x = {2, 3}
    hall_t = {
        vertex
        for vertex in (0, 4, 5)
        if any(edge(vertex, item) in active for item in hall_x)
    }
    assert hall_t == {0}
    assert len(hall_x) == len(hall_t) + 1
    for proper_size in range(1, len(hall_x)):
        for subset_tuple in combinations(sorted(hall_x), proper_size):
            subset = set(subset_tuple)
            neighbours = {
                vertex
                for vertex in (0, 4, 5)
                if any(edge(vertex, item) in active for item in subset)
            }
            assert len(neighbours) >= len(subset)

    boundary = {
        item
        for item in active
        if len(set(item) & hall_t) == 1 and len(set(item) & (hall_shore - hall_x)) == 1
    }
    assert boundary == {edge(0, 1)}
    assert sum(scores[item] for item in boundary) == -1

    boundary_edge = next(iter(boundary))
    complement = set(vertices) - set(boundary_edge)
    complement_matchings = system.matchings(complement)
    assert complement_matchings == ((edge(2, 4), edge(3, 5)),)
    repairs = set(complement_matchings[0])
    assert repairs.isdisjoint(active)
    assert len(repairs) == 2
    outside_t = {4, 5}
    b = sum(
        len(set(item) & hall_x) == 1 and len(set(item) & outside_t) == 1
        for item in repairs
    )
    q = sum(
        len(set(item) & (hall_shore - hall_x - {1})) == 1
        and len(set(item) & (hall_t - {0})) == 1
        for item in repairs
    )
    assert (b, q) == (2, 0)
    assert b == q + 2
    for repair in repairs:
        assert system.hafnian(set(vertices) - set(repair)) == 0


def bipartite_matchings(
    left: tuple[int, ...], right: tuple[int, ...], items: set[Edge]
) -> tuple[Matching, ...]:
    output: list[Matching] = []
    for image in permutations(right):
        matching = tuple(edge(vertex, partner) for vertex, partner in zip(left, image))
        if set(matching) <= items:
            output.append(matching)
    return tuple(output)


def matching_ports(
    vertex: int, matchings: tuple[Matching, ...], items: set[Edge]
) -> dict[Edge, tuple[Matching, ...]]:
    output: dict[Edge, list[Matching]] = {
        item: [] for item in items if vertex in item
    }
    for matching in matchings:
        incident = [item for item in matching if vertex in item]
        assert len(incident) == 1
        output[incident[0]].append(matching)
    return {item: tuple(port) for item, port in output.items()}


def theta_route_lengths(
    vertices: tuple[int, ...], items: set[Edge], endpoints: tuple[int, int]
) -> tuple[int, int, int]:
    """Trace the three routes in a graph with exactly two cubic vertices."""

    start, finish = endpoints
    neighbours = adjacency(vertices, items)
    routes: list[tuple[int, ...]] = []
    used_internal: set[int] = set()
    for first in sorted(neighbours[start]):
        path = [start, first]
        previous, current = start, first
        while current != finish:
            assert len(neighbours[current]) == 2
            following = next(iter(neighbours[current] - {previous}))
            assert following not in path
            path.append(following)
            previous, current = current, following
        internal = set(path[1:-1])
        assert not (internal & used_internal)
        used_internal |= internal
        routes.append(tuple(path))
    assert len(routes) == 3
    assert used_internal == set(vertices) - {start, finish}
    assert set().union(*(set(path_edges(path)) for path in routes)) == items
    return tuple(sorted(len(path) - 1 for path in routes))  # type: ignore[return-value]


def verify_fractional_decomposition(
    vertices: tuple[int, ...], items: set[Edge], matchings: tuple[Matching, ...]
) -> None:
    """Run the Hall/subtraction decomposition on a positive exact point."""

    assert matchings
    denominator = sum(range(1, len(matchings) + 1))
    coefficients = [Fraction(index, denominator) for index in range(1, len(matchings) + 1)]
    point = {item: Fraction(0) for item in items}
    for coefficient, matching in zip(coefficients, matchings):
        for item in matching:
            point[item] += coefficient
    for vertex in vertices:
        assert sum(value for item, value in point.items() if vertex in item) == 1
    assert all(value > 0 for value in point.values())

    residual = dict(point)
    decomposition: list[tuple[Fraction, Matching]] = []
    while any(residual.values()):
        support = {item for item, value in residual.items() if value > 0}
        supported = next(
            (matching for matching in matchings if set(matching) <= support), None
        )
        assert supported is not None  # Hall's condition supplies this matching.
        epsilon = min(residual[item] for item in supported)
        assert epsilon > 0
        decomposition.append((epsilon, supported))
        for item in supported:
            residual[item] -= epsilon
        for vertex in vertices:
            row_sum = sum(value for item, value in residual.items() if vertex in item)
            assert row_sum == 1 - sum(value for value, _ in decomposition)
    assert sum(value for value, _ in decomposition) == 1
    reconstructed = {item: Fraction(0) for item in items}
    for coefficient, matching in decomposition:
        for item in matching:
            reconstructed[item] += coefficient
    assert reconstructed == point


def verify_small_matching_covered_graphs() -> dict[int, tuple[int, int, int]]:
    """Exhaust all labelled equal-shore bipartite graphs through 4+4."""

    summary: dict[int, tuple[int, int, int]] = {}
    beta_one_seen = 0
    beta_two_seen = 0
    forced_aggregate_sites = 0
    for shore_size in (2, 3, 4):
        left = tuple(range(shore_size))
        right = tuple(range(shore_size, 2 * shore_size))
        vertices = left + right
        possible = tuple(edge(l_vertex, r_vertex) for l_vertex in left for r_vertex in right)
        matching_covered_count = 0
        least_core_count = 0
        local_aggregate_sites = 0
        for mask in range(1, 1 << len(possible)):
            items = {
                item for index, item in enumerate(possible) if mask & (1 << index)
            }
            if not is_connected(vertices, items):
                continue
            matchings = bipartite_matchings(left, right, items)
            if not matchings:
                continue
            allowed = set().union(*(set(matching) for matching in matchings))
            if allowed != items:
                continue
            matching_covered_count += 1
            beta = len(items) - len(vertices) + 1
            assert beta >= 0
            assert incidence_rank(vertices, items) == len(vertices) - 1
            assert matching_incidence_rank(matchings, items) == beta
            assert len(matchings) >= beta + 1

            degree = degrees(vertices, items)
            if min(degree.values()) < 2:
                continue
            least_core_count += 1
            left_excess = sum(degree[vertex] - 2 for vertex in left)
            right_excess = sum(degree[vertex] - 2 for vertex in right)
            assert left_excess == right_excess == beta - 1
            assert all(value <= beta + 1 for value in degree.values())

            if beta == 1:
                beta_one_seen += 1
                assert set(degree.values()) == {2}
                assert len(items) == len(vertices)
                assert len(matchings) == 2
            if beta == 2:
                beta_two_seen += 1
                cubic_left = [vertex for vertex in left if degree[vertex] == 3]
                cubic_right = [vertex for vertex in right if degree[vertex] == 3]
                assert len(cubic_left) == len(cubic_right) == 1
                assert all(value in {2, 3} for value in degree.values())
                routes = theta_route_lengths(
                    vertices, items, (cubic_left[0], cubic_right[0])
                )
                assert all(length % 2 == 1 for length in routes)
                assert len(matchings) == 3

            for vertex, value in degree.items():
                ports = matching_ports(vertex, matchings, items)
                assert len(ports) == value
                assert all(ports.values())
                singleton_ports = all(len(port) == 1 for port in ports.values())
                assert singleton_ports == (len(matchings) == value)
                if value <= beta:
                    assert len(matchings) >= beta + 1 > value
                    assert any(len(port) >= 2 for port in ports.values())
                    local_aggregate_sites += 1
                    if value == 3 and beta >= 3:
                        forced_aggregate_sites += 1
                if singleton_ports:
                    assert value == len(matchings) == beta + 1
        assert matching_covered_count > 0
        summary[shore_size] = (
            matching_covered_count,
            least_core_count,
            local_aggregate_sites,
        )
    assert beta_one_seen > 0
    assert beta_two_seen > 0
    assert forced_aggregate_sites > 0
    return summary


def assert_least_supported_zero(system: ExactHafnian) -> None:
    full_mask = (1 << system.order) - 1
    assert system.matchings_mask(full_mask)
    assert system.hafnian_mask(full_mask) == 0
    for mask in range(1, full_mask):
        if mask.bit_count() % 2:
            continue
        if system.matchings_mask(mask):
            assert system.hafnian_mask(mask) != 0


def verify_theta_controls() -> dict[int, tuple[int, int, int, int]]:
    """Check d=3 by the theta tracer and d=4,...,8 directly."""

    summary: dict[int, tuple[int, int, int, int]] = {}
    for d in range(3, 9):
        start, finish = 0, 1
        weights: dict[Edge, Fraction] = {}
        routes: list[tuple[int, int, int, int]] = []
        for index in range(d):
            first = 2 + 2 * index
            second = first + 1
            routes.append((start, first, second, finish))
            weights[edge(start, first)] = Fraction(1)
            weights[edge(first, second)] = Fraction(1)
            weights[edge(second, finish)] = (
                Fraction(1) if index < d - 1 else Fraction(-(d - 1))
            )
        order = 2 + 2 * d
        vertices = tuple(range(order))
        items = set(weights)
        system = ExactHafnian(order, weights)
        matchings = system.matchings(vertices)
        beta = len(items) - order + 1
        assert (beta, len(matchings)) == (d - 1, d)
        assert matching_incidence_rank(matchings, items) == beta
        assert len(matchings) == beta + 1
        degree = degrees(vertices, items)
        assert degree[start] == degree[finish] == d == beta + 1
        assert all(degree[vertex] == 2 for vertex in vertices[2:])
        assert all(len(route) - 1 == 3 for route in routes)
        assert set().union(*(set(path_edges(route)) for route in routes)) == items
        ports = matching_ports(start, matchings, items)
        assert len(ports) == d
        assert all(len(port) == 1 for port in ports.values())
        assert_least_supported_zero(system)
        left, right = bipartition(vertices, items)
        assert len(left) == len(right) == d + 1
        verify_fractional_decomposition(vertices, items, matchings)
        summary[d] = (order, len(items), beta, len(matchings))
    return summary


def verify_k33_aggregate_control() -> tuple[int, int, int, int]:
    left = (0, 1, 2)
    right = (3, 4, 5)
    vertices = left + right
    weights = {
        edge(l_vertex, r_vertex): Fraction(1)
        for l_vertex in left
        for r_vertex in right
    }
    weights[edge(0, 3)] = Fraction(-2)
    items = set(weights)
    system = ExactHafnian(6, weights)
    matchings = system.matchings(vertices)
    beta = len(items) - len(vertices) + 1
    assert (beta, len(matchings)) == (4, 6)
    assert matching_incidence_rank(matchings, items) == beta
    assert len(matchings) >= beta + 1
    assert_least_supported_zero(system)
    ports = matching_ports(0, matchings, items)
    assert {item: len(port) for item, port in ports.items()} == {
        edge(0, 3): 2,
        edge(0, 4): 2,
        edge(0, 5): 2,
    }
    port_sums = {
        item: sum(system.matching_weight(matching) for matching in port)
        for item, port in ports.items()
    }
    assert port_sums == {
        edge(0, 3): Fraction(-4),
        edge(0, 4): Fraction(2),
        edge(0, 5): Fraction(2),
    }
    assert sum(port_sums.values()) == 0
    verify_fractional_decomposition(vertices, items, matchings)
    return len(vertices), len(items), beta, len(matchings)


def main() -> None:
    triple_summary = verify_selected_triple_geometry()
    verify_hall_deficient_control()
    graph_summary = verify_small_matching_covered_graphs()
    theta_summary = verify_theta_controls()
    k33_summary = verify_k33_aggregate_control()

    print("PASS: all-degree all-bridge localization/core controls")
    print(f"selected triples (n: total, disconnected, Hamiltonian, cuts): {triple_summary}")
    print(f"small bipartite cores (m: covered, min-degree-two, aggregate sites): {graph_summary}")
    print(f"Theta_d extremal sparse controls (d: |V|, |E|, beta, N): {theta_summary}")
    print(f"K_(3,3) aggregate control (|V|, |E|, beta, N): {k33_summary}")
    print(
        "SCOPE: exact bounded mechanism/control audit; the arbitrary-order "
        "claims are supplied by the accompanying written proofs, not by a "
        "finite graph census."
    )
    print("GLOBAL KRENN-GU STATUS: UNRESOLVED")


if __name__ == "__main__":
    main()
