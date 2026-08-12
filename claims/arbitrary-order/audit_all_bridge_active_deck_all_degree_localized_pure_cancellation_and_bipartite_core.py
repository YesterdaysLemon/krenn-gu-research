"""Independent bounded audit for the all-degree all-bridge reduction.

This file deliberately imports no repository module and does not inspect or
import the primary verifier.  It reconstructs the finite controls with sparse
edge dictionaries, bitmask perfect-matching recursion, exact ``Fraction``
arithmetic, and exact Gaussian rank on integer incidence vectors.

The checks below are bounded QA for the displayed finite interfaces.  They do
not enumerate arbitrary-order graphs and are not the proof of the written
arbitrary-order theorem.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction
from functools import cache
from itertools import pairwise

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def edge(u: int, v: int) -> Edge:
    """Return an undirected edge in canonical order."""
    assert u != v
    return (u, v) if u < v else (v, u)


def vertices_mask(vertices: set[int] | tuple[int, ...] | list[int]) -> int:
    mask = 0
    for vertex in vertices:
        mask |= 1 << vertex
    return mask


def matching_oracle(
    order: int, weights: dict[Edge, Fraction]
):
    """Return an exact cached ``(number, hafnian)`` oracle for every mask."""
    adjacency: list[list[tuple[int, Fraction]]] = [[] for _ in range(order)]
    for (u, v), weight in weights.items():
        if weight:
            adjacency[u].append((v, weight))
            adjacency[v].append((u, weight))

    @cache
    def evaluate(mask: int) -> tuple[int, Fraction]:
        if mask == 0:
            return 1, Fraction(1)
        if mask.bit_count() % 2:
            return 0, Fraction(0)

        first_bit = mask & -mask
        u = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        number = 0
        value = Fraction(0)
        for v, weight in adjacency[u]:
            v_bit = 1 << v
            if remainder & v_bit:
                sub_number, sub_value = evaluate(remainder ^ v_bit)
                number += sub_number
                value += weight * sub_value
        return number, value

    return evaluate


def enumerate_matchings(order: int, edges: set[Edge], mask: int | None = None):
    """Enumerate support perfect matchings by an independent bitmask recursion."""
    if mask is None:
        mask = (1 << order) - 1
    adjacency = [0] * order
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u

    @cache
    def visit(current: int) -> tuple[Matching, ...]:
        if current == 0:
            return ((),)
        if current.bit_count() % 2:
            return ()
        first_bit = current & -current
        u = first_bit.bit_length() - 1
        candidates = adjacency[u] & (current ^ first_bit)
        answer: list[Matching] = []
        while candidates:
            v_bit = candidates & -candidates
            candidates ^= v_bit
            v = v_bit.bit_length() - 1
            for tail in visit(current ^ first_bit ^ v_bit):
                answer.append((edge(u, v), *tail))
        return tuple(answer)

    return visit(mask)


def integer_gaussian_rank(rows: list[list[int]]) -> int:
    """Compute the rank of an integer matrix by exact Gaussian elimination."""
    if not rows:
        return 0
    width = len(rows[0])
    matrix = [[Fraction(value) for value in row] for row in rows]
    assert all(len(row) == width for row in matrix)
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                value - multiple * basis
                for value, basis in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def adjacency(order: int, edges: set[Edge]) -> list[set[int]]:
    graph = [set() for _ in range(order)]
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph


def connected(order: int, edges: set[Edge]) -> bool:
    graph = adjacency(order, edges)
    reached = {0}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in graph[u] - reached:
            reached.add(v)
            queue.append(v)
    return len(reached) == order


def bipartition(order: int, edges: set[Edge]) -> tuple[set[int], set[int]] | None:
    graph = adjacency(order, edges)
    colour: dict[int, int] = {}
    for root in range(order):
        if root in colour:
            continue
        colour[root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    queue.append(v)
                elif colour[v] == colour[u]:
                    return None
    left = {vertex for vertex, side in colour.items() if side == 0}
    return left, set(range(order)) - left


def cycle_graph(length: int) -> tuple[int, set[Edge]]:
    return length, {edge(vertex, (vertex + 1) % length) for vertex in range(length)}


def theta_graph(path_lengths: tuple[int, ...]) -> tuple[int, set[Edge], list[list[int]]]:
    """Build internally disjoint paths between hubs 0 and 1."""
    next_vertex = 2
    edges: set[Edge] = set()
    paths: list[list[int]] = []
    for length in path_lengths:
        assert length >= 1
        internal = list(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        path = [0, *internal, 1]
        paths.append(path)
        edges.update(edge(u, v) for u, v in pairwise(path))
    return next_vertex, edges, paths


def k33_graph() -> tuple[int, set[Edge]]:
    return 6, {edge(left, 3 + right) for left in range(3) for right in range(3)}


def is_perfect_matching(vertices: set[int], matching: set[Edge]) -> bool:
    seen: set[int] = set()
    for u, v in matching:
        if u not in vertices or v not in vertices or u in seen or v in seen:
            return False
        seen.update((u, v))
    return seen == vertices


def audit_hall_counting_identity() -> None:
    """Brute-force the shore count b=q+2 on small complete supports."""
    cases = 0
    matchings_checked = 0
    for shore_size in range(3, 7):
        order = 2 * shore_size
        support = {
            edge(u, shore_size + w)
            for u in range(shore_size)
            for w in range(shore_size)
        }
        for x_size in range(2, shore_size):
            x_shore = set(range(x_size))
            t_shore = set(range(shore_size, shore_size + x_size - 1))
            y = x_size
            t = shore_size
            remaining = ((1 << order) - 1) ^ (1 << y) ^ (1 << t)
            for matching in enumerate_matchings(order, support, remaining):
                a_count = 0
                b_count = 0
                q_count = 0
                for u, v in matching:
                    if u >= shore_size:
                        u, v = v, u
                    if u in x_shore and v in t_shore - {t}:
                        a_count += 1
                    elif u in x_shore and v not in t_shore:
                        b_count += 1
                    elif u not in x_shore | {y} and v in t_shore - {t}:
                        q_count += 1
                assert a_count + b_count == x_size
                assert a_count + q_count == x_size - 2
                assert b_count == q_count + 2
                assert b_count >= 2
                matchings_checked += 1
            cases += 1
    assert cases == 10
    assert matchings_checked == 566


def double_star_weights(
    a: Fraction, b: Fraction, f: Fraction, g: Fraction
) -> dict[Edge, Fraction]:
    """Return the six-vertex signed double-star scalar control."""
    assert a and b and f and g
    return {
        edge(0, 3): a,
        edge(1, 3): b,
        edge(2, 3): -1 / (f * g),
        edge(2, 4): 1 / (a * g),
        edge(2, 5): 1 / (b * f),
        edge(0, 4): f,
        edge(1, 5): g,
    }


def audit_hall_double_star_and_common_zeros() -> None:
    active = {
        edge(0, 3),
        edge(1, 3),
        edge(2, 3),
        edge(2, 4),
        edge(2, 5),
    }
    repairs = {edge(0, 4), edge(1, 5)}
    assert not enumerate_matchings(6, active)
    assert {v for e in repairs for v in e} == {0, 1, 4, 5}

    controls = (
        double_star_weights(Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
        double_star_weights(Fraction(2), Fraction(3), Fraction(2), Fraction(5)),
        double_star_weights(Fraction(-1), Fraction(4), Fraction(3), Fraction(-2)),
    )
    for weights in controls:
        evaluate = matching_oracle(6, weights)
        full_mask = (1 << 6) - 1
        assert evaluate(full_mask) == (3, Fraction(1))
        scores: dict[Edge, Fraction] = {}
        for candidate, value in weights.items():
            deleted = full_mask ^ (1 << candidate[0]) ^ (1 << candidate[1])
            scores[candidate] = value * evaluate(deleted)[1]
        assert {candidate for candidate, score in scores.items() if score} == active
        assert scores[edge(2, 3)] == -1
        assert all(scores[candidate] == 1 for candidate in active - {edge(2, 3)})
        for vertex in range(6):
            assert sum(
                score for candidate, score in scores.items() if vertex in candidate
            ) == 1
        assert all(scores[candidate] == 0 for candidate in repairs)

    # These are three separately parametrized scalar matrices, not a claimed
    # simultaneous graph witness.  They show exact common repair-cofactor zeros
    # and the sharp b=2 interface without borrowing a primary-verifier fixture.
    full_mask = (1 << 6) - 1
    for repair in repairs:
        deleted = full_mask ^ (1 << repair[0]) ^ (1 << repair[1])
        assert [matching_oracle(6, weights)(deleted)[1] for weights in controls] == [
            Fraction(0),
            Fraction(0),
            Fraction(0),
        ]


def audit_disconnected_selected_pair_cut() -> None:
    p_colour = {edge(0, 1), edge(2, 3), edge(4, 5), edge(6, 7)}
    p_other = {edge(1, 2), edge(0, 3), edge(5, 6), edge(4, 7)}
    union = p_colour | p_other
    graph = adjacency(8, union)
    component = {0}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in graph[u] - component:
            component.add(v)
            queue.append(v)
    complement = set(range(8)) - component
    assert component == {0, 1, 2, 3}
    assert complement == {4, 5, 6, 7}
    assert is_perfect_matching(component, p_colour & {e for e in union if set(e) <= component})
    assert is_perfect_matching(
        complement, p_other & {e for e in union if set(e) <= complement}
    )

    zero_factor = {
        edge(0, 1): Fraction(1),
        edge(2, 3): Fraction(1),
        edge(0, 2): Fraction(1),
        edge(1, 3): Fraction(-1),
    }
    nonzero_factor = {
        edge(5, 6): Fraction(2),
        edge(4, 7): Fraction(3),
    }
    assert matching_oracle(8, zero_factor)(vertices_mask(component)) == (
        2,
        Fraction(0),
    )
    assert matching_oracle(8, nonzero_factor)(vertices_mask(complement)) == (
        1,
        Fraction(6),
    )


def audit_hamiltonian_chord_cut() -> None:
    p_colour = {edge(0, 1), edge(2, 3), edge(4, 5), edge(6, 7)}
    p_other = {edge(1, 2), edge(3, 4), edge(5, 6), edge(0, 7)}
    cycle = p_colour | p_other
    assert connected(8, cycle)
    assert all(len(neighbours) == 2 for neighbours in adjacency(8, cycle))

    chord = edge(0, 3)
    assert chord not in cycle
    arcs = ([0, 1, 2, 3], [0, 7, 6, 5, 4, 3])
    assert all((len(path) - 1) % 2 == 1 for path in arcs)

    def begins_and_ends_in_other(path: list[int]) -> bool:
        return (
            edge(path[0], path[1]) in p_other
            and edge(path[-2], path[-1]) in p_other
        )

    selected_arcs = [path for path in arcs if begins_and_ends_in_other(path)]
    assert selected_arcs == [[0, 7, 6, 5, 4, 3]]
    arc = selected_arcs[0]
    shore = set(arc)
    complement = set(range(8)) - shore
    other_on_shore = {candidate for candidate in p_other if set(candidate) <= shore}
    other_on_complement = {
        candidate for candidate in p_other if set(candidate) <= complement
    }
    chord_matching = {chord} | {
        candidate
        for candidate in p_colour
        if set(candidate) < shore and not set(candidate) & set(chord)
    }
    assert is_perfect_matching(shore, other_on_shore)
    assert is_perfect_matching(complement, other_on_complement)
    assert is_perfect_matching(shore, chord_matching)

    second_matching = {edge(0, 5), edge(3, 6), edge(4, 7)}
    chord_factor = {candidate: Fraction(1) for candidate in chord_matching}
    chord_factor.update({candidate: Fraction(1) for candidate in second_matching})
    chord_factor[edge(0, 5)] = Fraction(-1)
    complement_factor = {edge(1, 2): Fraction(5)}
    assert matching_oracle(8, chord_factor)(vertices_mask(shore)) == (
        2,
        Fraction(0),
    )
    assert matching_oracle(8, complement_factor)(vertices_mask(complement)) == (
        1,
        Fraction(5),
    )


def audit_saturated_bit_flip_bipartiteness() -> None:
    """Enumerate the universal fixed-bit bipartitions of pure supports."""
    normal_types = tuple(range(8))
    for pure_colour in range(3):
        other_bits = [bit for bit in range(3) if bit != pure_colour]
        support = {
            edge(left, right)
            for left in normal_types
            for right in normal_types
            if left < right
            and all(((left >> bit) & 1) != ((right >> bit) & 1) for bit in other_bits)
        }
        assert support
        for fixed_bit in other_bits:
            assert all(
                ((left >> fixed_bit) & 1) != ((right >> fixed_bit) & 1)
                for left, right in support
            )
        assert bipartition(8, support) is not None

    # The one-open profile has one odd and two even routes.  It contains odd
    # cycles, is nonbipartite, and its odd route is absent from both internal
    # perfect matchings.  It therefore cannot occur inside an all-bridge pure
    # support, although it remains a valid generic pure-residual profile.
    order, one_open, paths = theta_graph((1, 2, 2))
    matchings = enumerate_matchings(order, one_open)
    open_edge = edge(paths[0][0], paths[0][1])
    assert order == 4
    assert bipartition(order, one_open) is None
    assert len(matchings) == 2
    assert all(open_edge not in matching for matching in matchings)

    closed_order, closed_theta, _ = theta_graph((3, 3, 3))
    closed_matchings = enumerate_matchings(closed_order, closed_theta)
    assert bipartition(closed_order, closed_theta) is not None
    assert len(closed_matchings) == 3
    assert set().union(*(set(matching) for matching in closed_matchings)) == closed_theta


def weighted_theta(route_count: int) -> tuple[int, dict[Edge, Fraction]]:
    order, support, paths = theta_graph((3,) * route_count)
    weights = {candidate: Fraction(1) for candidate in support}
    weights[edge(paths[-1][0], paths[-1][1])] = Fraction(-(route_count - 1))
    return order, weights


def weighted_k33() -> tuple[int, dict[Edge, Fraction]]:
    matrix = (
        (Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(-2)),
    )
    weights = {
        edge(left, 3 + right): matrix[left][right]
        for left in range(3)
        for right in range(3)
    }
    return 6, weights


def assert_least_supported_zero(order: int, weights: dict[Edge, Fraction]) -> None:
    evaluate = matching_oracle(order, weights)
    full_mask = (1 << order) - 1
    full_number, full_value = evaluate(full_mask)
    assert full_number >= 2
    assert full_value == 0
    for mask in range(1, full_mask):
        if mask.bit_count() % 2:
            continue
        number, value = evaluate(mask)
        assert not number or value != 0


def audit_core_polytope(
    name: str, order: int, edges: set[Edge]
) -> tuple[int, int, dict[int, list[Matching]]]:
    del name  # The caller keeps names solely to make failures easy to localize.
    assert connected(order, edges)
    shores = bipartition(order, edges)
    assert shores is not None
    left, right = shores
    assert len(left) == len(right)
    graph = adjacency(order, edges)
    assert min(map(len, graph)) >= 2

    matchings = enumerate_matchings(order, edges)
    assert matchings
    allowed = set().union(*(set(matching) for matching in matchings))
    assert allowed == edges

    ordered_edges = sorted(edges)
    vectors = [
        [int(candidate in matching) for candidate in ordered_edges]
        for matching in matchings
    ]
    affine_rows = [
        [value - base for value, base in zip(vector, vectors[0], strict=True)]
        for vector in vectors[1:]
    ]
    incidence_rows = [
        [int(vertex in candidate) for candidate in ordered_edges]
        for vertex in range(order)
    ]
    beta = len(edges) - order + 1
    assert integer_gaussian_rank(incidence_rows) == order - 1
    assert integer_gaussian_rank(affine_rows) == beta
    assert len(matchings) >= beta + 1

    left_excess = sum(len(graph[vertex]) - 2 for vertex in left)
    right_excess = sum(len(graph[vertex]) - 2 for vertex in right)
    assert left_excess == right_excess == beta - 1

    ports: dict[int, list[Matching]] = {}
    for vertex in range(order):
        incident = [candidate for candidate in ordered_edges if vertex in candidate]
        local_ports = {
            candidate: [matching for matching in matchings if candidate in matching]
            for candidate in incident
        }
        assert all(local_ports.values())
        assert sum(map(len, local_ports.values())) == len(matchings)
        degree = len(incident)
        if degree <= beta:
            assert any(len(port) >= 2 for port in local_ports.values())
        ports[vertex] = [matching for port in local_ports.values() for matching in port]
    return beta, len(matchings), ports


def audit_matching_polytope_and_excess() -> None:
    for length in (4, 6, 8, 10, 12):
        order, support = cycle_graph(length)
        beta, number, _ = audit_core_polytope(f"cycle-{length}", order, support)
        assert (beta, number) == (1, 2)
        assert all(len(neighbours) == 2 for neighbours in adjacency(order, support))

    for route_count in range(3, 9):
        order, weights = weighted_theta(route_count)
        support = set(weights)
        beta, number, _ = audit_core_polytope(
            f"theta-{route_count}", order, support
        )
        assert beta == route_count - 1
        assert number == route_count == beta + 1
        hub_ports = [
            [matching for matching in enumerate_matchings(order, support) if e in matching]
            for e in support
            if 0 in e
        ]
        assert len(hub_ports) == route_count
        assert all(len(port) == 1 for port in hub_ports)
        assert_least_supported_zero(order, weights)

    order, weights = weighted_k33()
    support = set(weights)
    beta, number, _ = audit_core_polytope("K3,3", order, support)
    assert beta == 4
    assert number == 6 >= beta + 1
    matchings = enumerate_matchings(order, support)
    for vertex in range(order):
        for candidate in support:
            if vertex not in candidate:
                continue
            port = [matching for matching in matchings if candidate in matching]
            assert len(port) == 2
            port_sum = sum(
                (
                    product(weights[item] for item in matching)
                    for matching in port
                ),
                Fraction(0),
            )
            assert port_sum != 0
    assert_least_supported_zero(order, weights)

    # At beta=2, the equal shore excess is one.  Thus each shore has exactly
    # one cubic site and no quartic site; the tested matching-covered carrier
    # is necessarily the closed three-route theta rather than one-open.
    order, support, paths = theta_graph((3, 3, 3))
    beta, number, _ = audit_core_polytope("beta-two-theta", order, support)
    shores = bipartition(order, support)
    assert shores is not None
    graph = adjacency(order, support)
    assert beta == 2 and number == 3
    assert all(
        [len(graph[vertex]) for vertex in shore].count(3) == 1
        for shore in shores
    )
    assert all(len(path) - 1 == 3 for path in paths)


def product(values) -> Fraction:
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def audit_degree_six_interfaces() -> None:
    shapes: set[tuple[int, int, int, int]] = set()
    for a0 in range(1, 7):
        for a1 in range(1, 7):
            for a2 in range(1, 7):
                inactive = 6 - a0 - a1 - a2
                if inactive < 0:
                    continue
                active = sorted((a0, a1, a2), reverse=True)
                shapes.add((*active, inactive))
                # A pure colour-e support is disjoint from the two other
                # active decks.  At saturated degree at most six this leaves
                # at most four incident support edges.
                assert 6 - a1 - a2 <= 4
    assert shapes == {
        (1, 1, 1, 3),
        (2, 1, 1, 2),
        (2, 2, 1, 1),
        (3, 1, 1, 1),
        (2, 2, 2, 0),
        (3, 2, 1, 0),
        (4, 1, 1, 0),
    }

    # With maximum core degree four, each bipartition shore distributes
    # beta-1 units of excess among cubic (+1) and quartic (+2) sites.
    shore_patterns: dict[int, set[tuple[int, int]]] = {}
    for beta in range(1, 7):
        patterns = {
            (cubic, quartic)
            for quartic in range(beta)
            for cubic in range(beta + 1)
            if cubic + 2 * quartic == beta - 1
        }
        shore_patterns[beta] = patterns
    assert shore_patterns[1] == {(0, 0)}
    assert shore_patterns[2] == {(1, 0)}
    assert shore_patterns[3] == {(0, 1), (2, 0)}


def main() -> None:
    audit_hall_counting_identity()
    print("Hall-deficient shore count and b=q+2 repair bound: PASS")
    audit_hall_double_star_and_common_zeros()
    print("signed double-star and three scalar common-cofactor-zero controls: PASS")
    audit_disconnected_selected_pair_cut()
    print("selected-PM disconnected component/complement interface: PASS")
    audit_hamiltonian_chord_cut()
    print("selected-PM Hamiltonian chord-arc/complement interface: PASS")
    audit_saturated_bit_flip_bipartiteness()
    print("universal pure-support bipartition and one-open theta exclusion: PASS")
    audit_matching_polytope_and_excess()
    print("matching-polytope rank, shore excess, beta strata, and ports: PASS")
    audit_degree_six_interfaces()
    print("bounded degree-six local and bipartite-excess interfaces: PASS")
    print(
        "scope: bounded exact QA only; the written proof carries the "
        "arbitrary-order quantifiers"
    )
    print("independence: no repository imports and no primary-verifier imports")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
