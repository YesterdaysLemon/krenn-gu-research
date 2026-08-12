"""Exact focused checks for the beta-three extremal-sparse core interface.

The accompanying A4 proof is arbitrary-order.  This standalone stdlib
verifier checks the finite combinatorial interfaces used by that proof:

* the shore-excess/port pigeonhole and density arithmetic;
* every labelled connected bipartite matching-covered graph through 4+4;
* the sparse-site opposite-shore dichotomy, including the two-connected
  route case and the beta-three Q/Q versus Q/CC suppressed kernels;
* exact opposite-site port multiplicities; and
* sharp weighted least-residual controls (Theta_4, K_(3,3)-e, and an
  order-eight Q/CC sparse-site graph), including every proper supported
  induced even minor.

The census is bounded and is not an arbitrary-order proof or a search for a
Krenn--Gu witness.  The global conjecture remains UNRESOLVED.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from itertools import permutations, product

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def edge(left: int, right: int) -> Edge:
    """Return one undirected edge in canonical order."""

    assert left != right
    return (left, right) if left < right else (right, left)


def adjacency(vertices: tuple[int, ...], items: set[Edge]) -> dict[int, set[int]]:
    neighbours = {vertex: set() for vertex in vertices}
    for left, right in items:
        assert left in neighbours and right in neighbours
        neighbours[left].add(right)
        neighbours[right].add(left)
    return neighbours


def degrees(vertices: tuple[int, ...], items: set[Edge]) -> dict[int, int]:
    neighbours = adjacency(vertices, items)
    return {vertex: len(neighbours[vertex]) for vertex in vertices}


def is_connected(vertices: tuple[int, ...], items: set[Edge]) -> bool:
    if not vertices:
        return True
    neighbours = adjacency(vertices, items)
    seen = {vertices[0]}
    queue = deque([vertices[0]])
    while queue:
        current = queue.popleft()
        for neighbour in neighbours[current]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return len(seen) == len(vertices)


def articulation_vertices(vertices: tuple[int, ...], items: set[Edge]) -> set[int]:
    """Return the cut vertices by direct exact deletion tests."""

    output: set[int] = set()
    for deleted in vertices:
        remainder = tuple(vertex for vertex in vertices if vertex != deleted)
        induced = {item for item in items if deleted not in item}
        if remainder and not is_connected(remainder, induced):
            output.add(deleted)
    return output


def bipartite_matchings(
    left: tuple[int, ...], right: tuple[int, ...], items: set[Edge]
) -> tuple[Matching, ...]:
    """Enumerate perfect matchings of one fixed equal-shore support."""

    assert len(left) == len(right)
    output: list[Matching] = []
    for image in permutations(right):
        matching = tuple(edge(left[index], image[index]) for index in range(len(left)))
        if set(matching) <= items:
            output.append(matching)
    return tuple(output)


def matching_ports(
    vertex: int, matchings: tuple[Matching, ...], items: set[Edge]
) -> dict[Edge, tuple[Matching, ...]]:
    incident = sorted(item for item in items if vertex in item)
    return {
        item: tuple(matching for matching in matchings if item in matching)
        for item in incident
    }


def positive_excess_profile(
    shore: tuple[int, ...], degree: dict[int, int]
) -> tuple[int, ...]:
    """Positive terms in sum_(shore)(degree-2), in decreasing order."""

    return tuple(sorted((degree[v] - 2 for v in shore if degree[v] > 2), reverse=True))


def suppress_degree_two_routes(
    vertices: tuple[int, ...], items: set[Edge], branches: set[int]
) -> tuple[tuple[int, int, int], ...]:
    """Suppress maximal degree-two paths to (endpoint, endpoint, length)."""

    assert branches
    neighbours = adjacency(vertices, items)
    degree = {vertex: len(neighbours[vertex]) for vertex in vertices}
    assert all(degree[vertex] == 2 for vertex in vertices if vertex not in branches)
    traversed: set[Edge] = set()
    routes: list[tuple[int, int, int]] = []
    for start in sorted(branches):
        for first in sorted(neighbours[start]):
            first_edge = edge(start, first)
            if first_edge in traversed:
                continue
            traversed.add(first_edge)
            previous, current = start, first
            length = 1
            while current not in branches:
                choices = neighbours[current] - {previous}
                assert len(choices) == 1
                following = next(iter(choices))
                next_edge = edge(current, following)
                assert next_edge not in traversed
                traversed.add(next_edge)
                previous, current = current, following
                length += 1
            # A route returning to the same branch makes that branch a cut
            # vertex (or isolates a cycle); matching-covered cores forbid it.
            assert current != start
            routes.append((min(start, current), max(start, current), length))
    assert traversed == items
    return tuple(sorted(routes))


def integer_partitions(total: int, maximum: int | None = None) -> tuple[tuple[int, ...], ...]:
    """All decreasing positive integer partitions of total."""

    if total == 0:
        return ((),)
    ceiling = total if maximum is None else min(total, maximum)
    output: list[tuple[int, ...]] = []
    for first in range(ceiling, 0, -1):
        for tail in integer_partitions(total - first, first):
            output.append((first, *tail))
    return tuple(output)


def verify_integer_and_density_truth_table() -> tuple[int, int]:
    """Check the exact arithmetic behind the general sparse-site split.

    The equations are polynomial/integer identities; the loop is an explicit
    finite truth table, not a formal proof for unbounded beta.
    """

    partition_rows = 0
    density_rows = 0
    for beta in range(2, 33):
        matching_count = beta + 1
        sparse_degree = beta + 1

        # A sparse site contributes all beta-1 units of its own shore excess.
        assert sparse_degree - 2 == beta - 1
        assert (beta - 1) - (sparse_degree - 2) == 0

        # Active exclusivity makes the two other-colour incident active edges
        # physically new.  The A2 killer inequality then adds three support
        # neighbours: deg_D >= beta+3 and deg_G >= beta+6.
        degree_d_lower = sparse_degree + 2
        degree_g_lower = degree_d_lower + 3
        assert degree_d_lower == beta + 3
        assert degree_g_lower == beta + 6
        density_rows += 1

        for parts in integer_partitions(beta - 1):
            assert parts and sum(parts) == beta - 1
            partition_rows += 1
            if len(parts) == 1:
                assert parts == (beta - 1,)
                assert parts[0] + 2 == sparse_degree == matching_count
            else:
                # Every positive part leaves at least one unit for another
                # site, hence degree <= beta < N and an aggregate port.
                assert max(parts) <= beta - 2
                assert all(part + 2 <= beta < matching_count for part in parts)

    # The beta-three row is exactly Q=(2) versus CC=(1,1).
    assert integer_partitions(2) == ((2,), (1, 1))
    return partition_rows, density_rows


def verify_qq_routes(
    vertices: tuple[int, ...],
    items: set[Edge],
    matchings: tuple[Matching, ...],
    branch_vertices: tuple[int, int],
    beta: int,
) -> None:
    """Check the opposite-singleton case: a closed all-odd theta."""

    routes = suppress_degree_two_routes(vertices, items, set(branch_vertices))
    assert len(routes) == beta + 1
    assert all((left, right) == tuple(sorted(branch_vertices)) for left, right, _ in routes)
    assert all(length % 2 == 1 for _, _, length in routes)
    assert len(matchings) == beta + 1
    for vertex in branch_vertices:
        ports = matching_ports(vertex, matchings, items)
        assert len(ports) == beta + 1
        assert all(len(port) == 1 for port in ports.values())


def verify_beta_three_qcc_routes(
    vertices: tuple[int, ...],
    items: set[Edge],
    matchings: tuple[Matching, ...],
    quartic: int,
    cubics: tuple[int, int],
) -> None:
    """Check the unique beta-three Q/CC suppressed multigraph and ports."""

    routes = suppress_degree_two_routes(vertices, items, {quartic, *cubics})
    endpoint_multiplicity = Counter((left, right) for left, right, _ in routes)
    first, second = sorted(cubics)
    assert endpoint_multiplicity == Counter(
        {
            tuple(sorted((quartic, first))): 2,
            tuple(sorted((quartic, second))): 2,
            (first, second): 1,
        }
    )
    for left, right, length in routes:
        if quartic in (left, right):
            assert length % 2 == 1
        else:
            assert (left, right) == (first, second)
            assert length % 2 == 0

    assert len(matchings) == 4
    quartic_ports = matching_ports(quartic, matchings, items)
    assert sorted(len(port) for port in quartic_ports.values()) == [1, 1, 1, 1]
    for cubic in cubics:
        cubic_ports = matching_ports(cubic, matchings, items)
        assert sorted(len(port) for port in cubic_ports.values()) == [1, 1, 2]


def cc_route_state_profile(
    h: int, p: int, q: int
) -> tuple[bool, int, bool, dict[int, tuple[int, ...]]]:
    """Enumerate endpoint states for one C^2/C^2 suppressed kernel.

    Branches 0,1 are on one shore and 2,3 on the other.  There are h even
    routes on each same-shore pair, p odd routes on pairs 0--2 and 1--3,
    and q odd routes on pairs 0--3 and 1--2.  Odd-route endpoint states are
    00/11; even-route endpoint states are 10/01.
    """

    assert min(h, p, q) >= 0 and h + p + q == 3
    routes: list[tuple[int, int, bool]] = []
    for _ in range(h):
        routes.extend(((0, 1, False), (2, 3, False)))
    for _ in range(p):
        routes.extend(((0, 2, True), (1, 3, True)))
    for _ in range(q):
        routes.extend(((0, 3, True), (1, 2, True)))
    assert len(routes) == 6

    kernel_edges = {edge(left, right) for left, right, _ in routes}
    connected = is_connected((0, 1, 2, 3), kernel_edges)
    options = [((0, 0), (1, 1)) if odd else ((1, 0), (0, 1)) for _, _, odd in routes]
    assignments: list[tuple[int, ...]] = []
    for choices in product((0, 1), repeat=len(routes)):
        covered = [0, 0, 0, 0]
        for route_index, choice in enumerate(choices):
            left, right, _ = routes[route_index]
            left_state, right_state = options[route_index][choice]
            covered[left] += left_state
            covered[right] += right_state
        if covered == [1, 1, 1, 1]:
            assignments.append(choices)

    seen_states = [
        {choices[route_index] for choices in assignments}
        for route_index in range(len(routes))
    ]
    # Both alternating states are necessary for every nontrivial suppressed
    # route to have all of its physical edges allowed.  In the h=2 case, in
    # particular, each cross route is forced to state 00 and its endpoint
    # edges are absent from every matching.
    allowed = bool(assignments) and all(states == {0, 1} for states in seen_states)

    port_sizes: dict[int, list[int]] = {branch: [] for branch in range(4)}
    for route_index, (left, right, _) in enumerate(routes):
        for endpoint_position, branch in enumerate((left, right)):
            count = sum(
                options[route_index][choices[route_index]][endpoint_position]
                for choices in assignments
            )
            port_sizes[branch].append(count)
    return (
        connected,
        len(assignments),
        allowed,
        {branch: tuple(sorted(values)) for branch, values in port_sizes.items()},
    )


def verify_cc_kernel_truth_table() -> dict[tuple[int, int, int], tuple[bool, int, bool]]:
    """Exhaust all ten integer h+p+q=3 C^2/C^2 cases."""

    summary: dict[tuple[int, int, int], tuple[bool, int, bool]] = {}
    for h in range(4):
        for p in range(4 - h):
            q = 3 - h - p
            connected, matching_count, allowed, ports = cc_route_state_profile(h, p, q)
            summary[(h, p, q)] = (connected, matching_count, allowed)

            if h == 0 and min(p, q) == 0:
                assert not connected
                assert matching_count == 9 and allowed
            elif h == 0:
                assert {p, q} == {1, 2}
                assert connected and matching_count == 5 and allowed
                assert all(values == (1, 2, 2) for values in ports.values())
            elif h == 1:
                assert p + q == 2
                assert connected and matching_count == 4 and allowed
                assert all(values == (1, 1, 2) for values in ports.values())
            elif h == 2:
                assert {p, q} == {0, 1}
                assert connected and matching_count == 4 and not allowed
                # The two cross routes never cover either branch endpoint.
                assert all(values == (0, 2, 2) for values in ports.values())
            else:
                assert (h, p, q) == (3, 0, 0)
                assert not connected and matching_count == 0 and not allowed
    assert len(summary) == 10
    return summary


def verify_beta_three_cc_routes(
    vertices: tuple[int, ...],
    items: set[Edge],
    matchings: tuple[Matching, ...],
    left_branches: tuple[int, int],
    right_branches: tuple[int, int],
) -> tuple[int, int, int]:
    """Identify one physical C^2/C^2 core in the abstract truth table."""

    branch_set = {*left_branches, *right_branches}
    routes = suppress_degree_two_routes(vertices, items, branch_set)
    left_set, right_set = set(left_branches), set(right_branches)
    h_left = sum({left, right} <= left_set for left, right, _ in routes)
    h_right = sum({left, right} <= right_set for left, right, _ in routes)
    assert h_left == h_right
    h = h_left

    left_first, left_second = sorted(left_branches)
    right_first, right_second = sorted(right_branches)
    multiplicity = Counter((left, right) for left, right, _ in routes)
    p = multiplicity[edge(left_first, right_first)]
    q = multiplicity[edge(left_first, right_second)]
    assert multiplicity[edge(left_second, right_second)] == p
    assert multiplicity[edge(left_second, right_first)] == q
    assert h + p + q == 3

    for left, right, length in routes:
        same_shore = ({left, right} <= left_set) or ({left, right} <= right_set)
        assert (length % 2 == 0) == same_shore

    connected, matching_count, allowed, abstract_ports = cc_route_state_profile(h, p, q)
    assert connected and allowed
    assert matching_count == len(matchings) in {4, 5}
    for index, branch in enumerate(
        (left_first, left_second, right_first, right_second)
    ):
        physical_ports = tuple(
            sorted(len(port) for port in matching_ports(branch, matchings, items).values())
        )
        assert physical_ports == abstract_ports[index]
        assert any(size >= 2 for size in physical_ports)
    return h, min(p, q), max(p, q)


def verify_small_graph_census() -> dict[int, tuple[int, int, int, int, int, int, int]]:
    """Exhaust all labelled bipartite supports through equal shores 4+4."""

    summary: dict[int, tuple[int, int, int, int, int]] = {}
    total_sparse_sites = 0
    beta_three_qq_sites = 0
    beta_three_qcc_sites = 0
    beta_three_cc_n4_graphs = 0
    beta_three_cc_n5_graphs = 0

    for shore_size in (2, 3, 4):
        left = tuple(range(shore_size))
        right = tuple(range(shore_size, 2 * shore_size))
        vertices = left + right
        possible = tuple(edge(u, w) for u in left for w in right)
        covered_count = 0
        core_count = 0
        sparse_sites = 0
        qq_sites = 0
        qcc_sites = 0
        cc_n4_graphs = 0
        cc_n5_graphs = 0

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
            covered_count += 1

            degree = degrees(vertices, items)
            if min(degree.values()) < 2:
                continue
            core_count += 1
            assert not articulation_vertices(vertices, items)

            beta = len(items) - len(vertices) + 1
            matching_count = len(matchings)
            assert matching_count >= beta + 1
            assert sum(degree[v] - 2 for v in left) == beta - 1
            assert sum(degree[v] - 2 for v in right) == beta - 1
            assert all(degree[v] <= beta + 1 for v in vertices)

            if beta == 3:
                left_profile = positive_excess_profile(left, degree)
                right_profile = positive_excess_profile(right, degree)
                assert left_profile in {(2,), (1, 1)}
                assert right_profile in {(2,), (1, 1)}
                if left_profile == right_profile == (1, 1):
                    left_branches = tuple(v for v in left if degree[v] == 3)
                    right_branches = tuple(v for v in right if degree[v] == 3)
                    signature = verify_beta_three_cc_routes(
                        vertices,
                        items,
                        matchings,
                        (left_branches[0], left_branches[1]),
                        (right_branches[0], right_branches[1]),
                    )
                    if len(matchings) == 5:
                        assert signature == (0, 1, 2)
                        cc_n5_graphs += 1
                        beta_three_cc_n5_graphs += 1
                    else:
                        assert signature in {(1, 0, 2), (1, 1, 1)}
                        cc_n4_graphs += 1
                        beta_three_cc_n4_graphs += 1

            for vertex in vertices:
                if degree[vertex] < 3:
                    continue
                ports = matching_ports(vertex, matchings, items)
                assert all(ports.values())
                is_sparse = all(len(port) == 1 for port in ports.values())
                assert is_sparse == (matching_count == degree[vertex])
                if not is_sparse:
                    continue

                sparse_sites += 1
                total_sparse_sites += 1
                assert degree[vertex] == matching_count == beta + 1
                own = left if vertex in left else right
                opposite = right if vertex in left else left
                assert positive_excess_profile(own, degree) == (beta - 1,)
                assert [v for v in own if degree[v] > 2] == [vertex]

                opposite_profile = positive_excess_profile(opposite, degree)
                assert opposite_profile
                assert sum(opposite_profile) == beta - 1
                opposite_branches = tuple(v for v in opposite if degree[v] > 2)
                if len(opposite_profile) == 1:
                    assert opposite_profile == (beta - 1,)
                    other = opposite_branches[0]
                    assert degree[other] == matching_count == beta + 1
                    verify_qq_routes(
                        vertices, items, matchings, (vertex, other), beta
                    )
                    if beta == 3:
                        qq_sites += 1
                        beta_three_qq_sites += 1
                else:
                    assert all(value <= beta - 2 for value in opposite_profile)
                    for other in opposite_branches:
                        assert degree[other] <= beta < matching_count
                        other_ports = matching_ports(other, matchings, items)
                        assert any(len(port) >= 2 for port in other_ports.values())
                    if beta == 3:
                        assert opposite_profile == (1, 1)
                        assert len(opposite_branches) == 2
                        verify_beta_three_qcc_routes(
                            vertices,
                            items,
                            matchings,
                            vertex,
                            (opposite_branches[0], opposite_branches[1]),
                        )
                        qcc_sites += 1
                        beta_three_qcc_sites += 1

        assert covered_count > 0 and core_count > 0
        summary[shore_size] = (
            covered_count,
            core_count,
            sparse_sites,
            qq_sites,
            qcc_sites,
            cc_n4_graphs,
            cc_n5_graphs,
        )

    assert total_sparse_sites > 0
    assert beta_three_qq_sites > 0
    assert beta_three_qcc_sites > 0
    assert beta_three_cc_n4_graphs > 0
    assert beta_three_cc_n5_graphs > 0
    return summary


class ExactHafnian:
    """Exact Fraction hafnian and supported-matching recursion on bitmasks."""

    def __init__(self, order: int, weights: dict[Edge, int | Fraction]) -> None:
        self.order = order
        self.weights = {
            item: Fraction(value) for item, value in weights.items() if value
        }
        self._hafnians: dict[int, Fraction] = {0: Fraction(1)}
        self._matchings: dict[int, tuple[Matching, ...]] = {0: ((),)}

    def hafnian(self, mask: int) -> Fraction:
        if mask in self._hafnians:
            return self._hafnians[mask]
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
                total += value * self.hafnian(remainder ^ partner_bit)
            scan ^= partner_bit
        self._hafnians[mask] = total
        return total

    def matchings(self, mask: int) -> tuple[Matching, ...]:
        if mask in self._matchings:
            return self._matchings[mask]
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
                for tail in self.matchings(remainder ^ partner_bit):
                    output.append((item, *tail))
            scan ^= partner_bit
        result = tuple(output)
        self._matchings[mask] = result
        return result

    def matching_weight(self, matching: Matching) -> Fraction:
        product = Fraction(1)
        for item in matching:
            product *= self.weights[item]
        return product


def assert_least_supported_zero(system: ExactHafnian) -> int:
    """Check full cancellation and every proper supported induced even set."""

    full = (1 << system.order) - 1
    assert system.matchings(full)
    assert system.hafnian(full) == 0
    checked = 0
    for mask in range(1, full):
        if mask.bit_count() % 2 or not system.matchings(mask):
            continue
        assert system.hafnian(mask) != 0
        checked += 1
    return checked


def assert_control_core(
    system: ExactHafnian,
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[tuple[Matching, ...], int]:
    vertices = left + right
    items = set(system.weights)
    matchings = bipartite_matchings(left, right, items)
    assert is_connected(vertices, items)
    assert min(degrees(vertices, items).values()) >= 2
    assert set().union(*(set(matching) for matching in matchings)) == items
    beta = len(items) - len(vertices) + 1
    assert beta == 3 and len(matchings) == 4
    assert {
        frozenset(matching)
        for matching in system.matchings((1 << system.order) - 1)
    } == {frozenset(matching) for matching in matchings}
    return matchings, assert_least_supported_zero(system)


def verify_theta_four_control() -> tuple[int, int, int, int, int]:
    """A weighted closed all-odd four-route theta with a least zero."""

    start, finish = 0, 1
    weights: dict[Edge, Fraction] = {}
    for index in range(4):
        first = 2 + 2 * index
        second = first + 1
        weights[edge(start, first)] = Fraction(1)
        weights[edge(first, second)] = Fraction(1)
        weights[edge(second, finish)] = Fraction(1 if index < 3 else -3)
    system = ExactHafnian(10, weights)
    left = (0, 3, 5, 7, 9)
    right = (1, 2, 4, 6, 8)
    matchings, proper = assert_control_core(system, left, right)
    vertices = tuple(range(10))
    verify_qq_routes(vertices, set(weights), matchings, (start, finish), beta=3)
    return system.order, len(weights), 3, len(matchings), proper


def verify_k33_minus_edge_control() -> tuple[int, int, int, int, int]:
    """An exact beta-three N=4 non-theta CC/CC least residual."""

    left = (0, 1, 2)
    right = (3, 4, 5)
    weights = {
        edge(u, w): Fraction(1)
        for u in left
        for w in right
        if (u, w) != (2, 5)
    }
    weights[edge(0, 3)] = Fraction(-3)
    system = ExactHafnian(6, weights)
    matchings, proper = assert_control_core(system, left, right)
    degree = degrees(left + right, set(weights))
    assert positive_excess_profile(left, degree) == (1, 1)
    assert positive_excess_profile(right, degree) == (1, 1)
    assert proper == 17
    return system.order, len(weights), 3, len(matchings), proper


def verify_order_eight_cc_n5_control() -> tuple[int, int, int, int, int]:
    """An exact C^2/C^2 cross-multiplicity [[1,2],[2,1]] control."""

    # Branches 0,1 lie on the left and 2,3 on the right.  Four routes are
    # direct; 0--4--5--3 doubles 0--3 and 1--6--7--2 doubles 1--2.
    left = (0, 1, 5, 7)
    right = (2, 3, 4, 6)
    items = {
        edge(0, 2),
        edge(0, 3),
        edge(1, 2),
        edge(1, 3),
        edge(0, 4),
        edge(4, 5),
        edge(5, 3),
        edge(1, 6),
        edge(6, 7),
        edge(7, 2),
    }
    weights = {item: Fraction(1) for item in items}
    weights[edge(0, 2)] = Fraction(-4)
    system = ExactHafnian(8, weights)
    vertices = tuple(range(8))
    matchings = bipartite_matchings(left, right, items)
    assert is_connected(vertices, items)
    assert min(degrees(vertices, items).values()) == 2
    assert set().union(*(set(matching) for matching in matchings)) == items
    assert (len(items) - len(vertices) + 1, len(matchings)) == (3, 5)
    signature = verify_beta_three_cc_routes(
        vertices, items, matchings, (0, 1), (2, 3)
    )
    assert signature == (0, 1, 2)
    assert {
        frozenset(matching)
        for matching in system.matchings((1 << system.order) - 1)
    } == {frozenset(matching) for matching in matchings}
    proper = assert_least_supported_zero(system)
    return system.order, len(weights), 3, len(matchings), proper


def verify_order_eight_qcc_control() -> tuple[int, int, int, int, int]:
    """An exact sparse-quartic/non-theta Q/CC least residual."""

    left = (0, 1, 2, 3)
    right = (4, 5, 6, 7)
    row_columns = {
        0: (0, 1, 2, 3),
        1: (1, 3),
        2: (0, 2),
        3: (0, 1),
    }
    weights = {
        edge(row, 4 + column): Fraction(1)
        for row, columns in row_columns.items()
        for column in columns
    }
    weights[edge(0, 4)] = Fraction(-3)
    system = ExactHafnian(8, weights)
    matchings, proper = assert_control_core(system, left, right)
    degree = degrees(left + right, set(weights))
    assert positive_excess_profile(left, degree) == (2,)
    assert positive_excess_profile(right, degree) == (1, 1)
    assert degree[0] == 4
    assert sorted(
        len(port)
        for port in matching_ports(0, matchings, set(weights)).values()
    ) == [1, 1, 1, 1]
    cubics = tuple(vertex for vertex in right if degree[vertex] == 3)
    verify_beta_three_qcc_routes(
        left + right, set(weights), matchings, quartic=0, cubics=(cubics[0], cubics[1])
    )
    assert proper == 51
    return system.order, len(weights), 3, len(matchings), proper


def main() -> None:
    arithmetic = verify_integer_and_density_truth_table()
    cc_truth_table = verify_cc_kernel_truth_table()
    census = verify_small_graph_census()
    theta = verify_theta_four_control()
    k33_minus_edge = verify_k33_minus_edge_control()
    cc_n5 = verify_order_eight_cc_n5_control()
    order_eight = verify_order_eight_qcc_control()

    print("PASS: extremal-sparse opposite-shore primary controls")
    print(f"integer/density rows (partitions, beta rows): {arithmetic}")
    print(f"C^2/C^2 kernel states ((h,p,q): connected,N,allowed): {cc_truth_table}")
    print(
        "small cores (m: covered, min-degree-two, sparse sites, "
        "beta3 Q/Q sites, beta3 Q/CC sites, beta3 C^2/C^2 N4 graphs, "
        f"beta3 C^2/C^2 N5 graphs): {census}"
    )
    print(f"Theta_4 control (|V|, |E|, beta, N, proper minors): {theta}")
    print(f"K_(3,3)-e control (|V|, |E|, beta, N, proper minors): {k33_minus_edge}")
    print(f"order-eight C^2/C^2 N=5 control (|V|, |E|, beta, N, proper minors): {cc_n5}")
    print(f"order-eight Q/CC control (|V|, |E|, beta, N, proper minors): {order_eight}")
    print(
        "SCOPE: exact arithmetic and exhaustive labelled graph checks only "
        "through equal shores 4+4, plus fixed exact weighted controls. The "
        "arbitrary-order theorem is supplied by the written proof, not this "
        "bounded census."
    )
    print("GLOBAL KRENN-GU STATUS: UNRESOLVED")


if __name__ == "__main__":
    main()
