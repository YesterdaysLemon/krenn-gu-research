"""Independent bounded audit of beta-three route-port pairing.

This standard-library audit derives the route statements directly from
perfect matchings of physical subdivisions.  It imports no repository code
and deliberately supplies only bounded mechanism checks:

* Q/Q and Q/C^2 subdivisions over several small route lengths;
* equal endpoint-port sets on odd routes;
* complementary two-element endpoint-port sets on the even Q/C^2 route;
* exact edge-weighted cofactor/port identities on least-zero fixtures; and
* a sharp warning that the corresponding bare deletion hafnians need not be
  equal when the two endpoint-edge weights differ.

The fixtures are scalar pure-core controls.  They contain no mixed target
data and support no mixed-target or global Krenn--Gu inference.  The global
conjecture remains UNRESOLVED.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

Edge = tuple[int, int]


def edge(left: int, right: int) -> Edge:
    """Return one undirected edge in canonical order."""

    assert left != right
    return (left, right) if left < right else (right, left)


@dataclass(frozen=True)
class Route:
    """One oriented branch-to-branch path in a physical subdivision."""

    name: str
    start: int
    finish: int
    path: tuple[int, ...]
    edges: tuple[Edge, ...]

    @property
    def length(self) -> int:
        return len(self.edges)


@dataclass(frozen=True)
class RouteGraph:
    """A simple graph together with its distinguished suppressed routes."""

    order: int
    branch_count: int
    edges: tuple[Edge, ...]
    routes: tuple[Route, ...]


class MatchingOracle:
    """Exact perfect matchings of induced vertex sets as edge bitmasks."""

    def __init__(self, graph: RouteGraph) -> None:
        self.graph = graph
        self.edge_index = {item: index for index, item in enumerate(graph.edges)}
        assert len(self.edge_index) == len(graph.edges)
        adjacency: list[list[tuple[int, int]]] = [[] for _ in range(graph.order)]
        for index, (left, right) in enumerate(graph.edges):
            adjacency[left].append((right, index))
            adjacency[right].append((left, index))
        self.adjacency = tuple(tuple(row) for row in adjacency)
        self.cache: dict[int, tuple[int, ...]] = {0: (0,)}

    def matchings(self, vertex_mask: int) -> tuple[int, ...]:
        """Return every perfect matching of the induced mask."""

        if vertex_mask in self.cache:
            return self.cache[vertex_mask]
        if vertex_mask.bit_count() % 2:
            return ()
        first_bit = vertex_mask & -vertex_mask
        first = first_bit.bit_length() - 1
        remainder = vertex_mask ^ first_bit
        output: list[int] = []
        for neighbour, edge_index in self.adjacency[first]:
            neighbour_bit = 1 << neighbour
            if not remainder & neighbour_bit:
                continue
            for tail in self.matchings(remainder ^ neighbour_bit):
                output.append(tail | (1 << edge_index))
        result = tuple(output)
        self.cache[vertex_mask] = result
        return result

    def full_matchings(self) -> tuple[int, ...]:
        return self.matchings((1 << self.graph.order) - 1)

    def edge_bit(self, item: Edge) -> int:
        return 1 << self.edge_index[item]


def build_route_graph(
    branch_count: int,
    specifications: tuple[tuple[str, int, int, int], ...],
) -> RouteGraph:
    """Subdivide labelled kernel routes with fresh internal vertices."""

    next_vertex = branch_count
    routes: list[Route] = []
    all_edges: list[Edge] = []
    for name, start, finish, length in specifications:
        assert 0 <= start < branch_count
        assert 0 <= finish < branch_count
        assert start != finish and length >= 1
        internal = tuple(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        path = (start, *internal, finish)
        route_edges = tuple(
            edge(path[index], path[index + 1]) for index in range(length)
        )
        routes.append(Route(name, start, finish, path, route_edges))
        all_edges.extend(route_edges)
    assert len(set(all_edges)) == len(all_edges), "physical graph must be simple"
    return RouteGraph(
        order=next_vertex,
        branch_count=branch_count,
        edges=tuple(sorted(all_edges)),
        routes=tuple(routes),
    )


def vertex_degrees(graph: RouteGraph) -> tuple[int, ...]:
    degrees = [0] * graph.order
    for left, right in graph.edges:
        degrees[left] += 1
        degrees[right] += 1
    return tuple(degrees)


def endpoint_port(
    oracle: MatchingOracle,
    matchings: tuple[int, ...],
    item: Edge,
) -> frozenset[int]:
    """Indices of full matchings in the incident-edge port."""

    item_bit = oracle.edge_bit(item)
    return frozenset(
        index for index, matching in enumerate(matchings) if matching & item_bit
    )


def assert_route_pairing(graph: RouteGraph, topology: str) -> None:
    """Check route parity and endpoint-port pairing on one subdivision."""

    oracle = MatchingOracle(graph)
    matchings = oracle.full_matchings()
    assert len(matchings) == 4
    assert graph.edges
    assert len(graph.edges) - graph.order + 1 == 3
    assert set().union(
        *(
            {
                graph.edges[index]
                for index in range(len(graph.edges))
                if mask & (1 << index)
            }
            for mask in matchings
        )
    ) == set(graph.edges)

    degrees = vertex_degrees(graph)
    assert all(degree == 2 for degree in degrees[graph.branch_count :])
    if topology == "Q/Q":
        assert degrees[:2] == (4, 4)
    else:
        assert topology == "Q/C^2"
        assert degrees[:3] == (4, 3, 3)

    even_routes = 0
    for route in graph.routes:
        first_port = endpoint_port(oracle, matchings, route.edges[0])
        last_port = endpoint_port(oracle, matchings, route.edges[-1])
        if route.length % 2:
            # An odd route has endpoint states 00 and 11.
            assert first_port == last_port
            assert len(first_port) == 1
        else:
            # The unique Q/C^2 even route has states 10 and 01.
            even_routes += 1
            assert len(first_port) == len(last_port) == 2
            assert first_port.isdisjoint(last_port)
            assert first_port | last_port == frozenset(range(4))
    assert even_routes == (topology == "Q/C^2")

    branch_profiles = []
    for branch in range(graph.branch_count):
        ports = [
            endpoint_port(oracle, matchings, item)
            for item in graph.edges
            if branch in item
        ]
        branch_profiles.append(tuple(sorted(len(port) for port in ports)))
    if topology == "Q/Q":
        assert branch_profiles == [(1, 1, 1, 1), (1, 1, 1, 1)]
    else:
        assert branch_profiles == [(1, 1, 1, 1), (1, 1, 2), (1, 1, 2)]


def audit_small_subdivisions() -> tuple[int, int, dict[int, int], dict[int, int]]:
    """Enumerate labelled Q/Q and Q/C^2 subdivisions over bounded lengths."""

    odd_lengths = (1, 3, 5, 7)
    even_lengths = (2, 4, 6)
    qq_count = 0
    qq_orders: Counter[int] = Counter()
    for lengths in product(odd_lengths, repeat=4):
        # A simple physical graph has at most one unsubdivided route on a
        # fixed branch pair.  Longer parallel routes have fresh interiors.
        if lengths.count(1) > 1:
            continue
        graph = build_route_graph(
            2,
            tuple((f"r{index}", 0, 1, length) for index, length in enumerate(lengths)),
        )
        assert_route_pairing(graph, "Q/Q")
        qq_count += 1
        qq_orders[graph.order] += 1

    qcc_count = 0
    qcc_orders: Counter[int] = Counter()
    for vx_lengths in product(odd_lengths, repeat=2):
        if vx_lengths == (1, 1):
            continue
        for vy_lengths in product(odd_lengths, repeat=2):
            if vy_lengths == (1, 1):
                continue
            for xy_length in even_lengths:
                specifications = (
                    ("vx0", 0, 1, vx_lengths[0]),
                    ("vx1", 0, 1, vx_lengths[1]),
                    ("vy0", 0, 2, vy_lengths[0]),
                    ("vy1", 0, 2, vy_lengths[1]),
                    ("xy", 1, 2, xy_length),
                )
                graph = build_route_graph(3, specifications)
                assert_route_pairing(graph, "Q/C^2")
                qcc_count += 1
                qcc_orders[graph.order] += 1

    assert qq_count == 189
    assert qcc_count == 675
    return (
        qq_count,
        qcc_count,
        dict(sorted(qq_orders.items())),
        dict(sorted(qcc_orders.items())),
    )


def matching_weight(
    graph: RouteGraph,
    weights: dict[Edge, Fraction],
    matching: int,
) -> Fraction:
    value = Fraction(1)
    for index, item in enumerate(graph.edges):
        if matching & (1 << index):
            value *= weights[item]
    return value


def hafnian(
    graph: RouteGraph,
    oracle: MatchingOracle,
    weights: dict[Edge, Fraction],
    vertex_mask: int,
) -> Fraction:
    return sum(
        (
            matching_weight(graph, weights, matching)
            for matching in oracle.matchings(vertex_mask)
        ),
        Fraction(0),
    )


def weighted_port_sum(
    graph: RouteGraph,
    oracle: MatchingOracle,
    weights: dict[Edge, Fraction],
    matchings: tuple[int, ...],
    item: Edge,
) -> Fraction:
    item_bit = oracle.edge_bit(item)
    return sum(
        (
            matching_weight(graph, weights, matching)
            for matching in matchings
            if matching & item_bit
        ),
        Fraction(0),
    )


def bare_deletion_hafnian(
    graph: RouteGraph,
    oracle: MatchingOracle,
    weights: dict[Edge, Fraction],
    item: Edge,
) -> Fraction:
    full_mask = (1 << graph.order) - 1
    left, right = item
    return hafnian(
        graph,
        oracle,
        weights,
        full_mask ^ (1 << left) ^ (1 << right),
    )


def assert_least_supported_zero(
    graph: RouteGraph,
    oracle: MatchingOracle,
    weights: dict[Edge, Fraction],
) -> int:
    """Check a full zero and every proper supported induced even subset."""

    full_mask = (1 << graph.order) - 1
    assert oracle.full_matchings()
    assert hafnian(graph, oracle, weights, full_mask) == 0
    checked = 0
    for vertex_mask in range(1, full_mask):
        if vertex_mask.bit_count() % 2 or not oracle.matchings(vertex_mask):
            continue
        assert hafnian(graph, oracle, weights, vertex_mask) != 0
        checked += 1
    return checked


def assert_weighted_route_ports(
    graph: RouteGraph,
    weights: dict[Edge, Fraction],
) -> tuple[MatchingOracle, tuple[int, ...]]:
    """Check edge-weighted cofactors and route endpoint sums exactly."""

    oracle = MatchingOracle(graph)
    matchings = oracle.full_matchings()
    assert len(matchings) == 4
    assert (
        sum(
            (matching_weight(graph, weights, matching) for matching in matchings),
            Fraction(0),
        )
        == 0
    )

    for route in graph.routes:
        first, last = route.edges[0], route.edges[-1]
        first_set = endpoint_port(oracle, matchings, first)
        last_set = endpoint_port(oracle, matchings, last)
        first_sum = weighted_port_sum(graph, oracle, weights, matchings, first)
        last_sum = weighted_port_sum(graph, oracle, weights, matchings, last)

        # The cofactor port includes its incident edge weight.  This is the
        # exact Laplace term, not the bare deletion hafnian.
        assert first_sum == weights[first] * bare_deletion_hafnian(
            graph, oracle, weights, first
        )
        assert last_sum == weights[last] * bare_deletion_hafnian(
            graph, oracle, weights, last
        )
        assert first_sum and last_sum

        if route.length % 2:
            assert first_set == last_set
            assert first_sum == last_sum
        else:
            assert len(first_set) == len(last_set) == 2
            assert first_set.isdisjoint(last_set)
            assert first_set | last_set == frozenset(range(4))
            assert first_sum == -last_sum
    return oracle, matchings


def audit_weighted_fixtures() -> dict[str, object]:
    """Replay exact least-zero Q/Q and Q/C^2 port-pairing fixtures."""

    qq = build_route_graph(
        2,
        tuple((f"r{index}", 0, 1, 3) for index in range(4)),
    )
    qq_weights = {item: Fraction(1) for item in qq.edges}
    sharp_route = qq.routes[-1]
    qq_weights[sharp_route.edges[-1]] = Fraction(-3)
    qq_oracle, qq_matchings = assert_weighted_route_ports(qq, qq_weights)
    qq_full_weights = sorted(
        matching_weight(qq, qq_weights, matching) for matching in qq_matchings
    )
    assert qq_full_weights == [Fraction(-3), Fraction(1), Fraction(1), Fraction(1)]
    qq_proper = assert_least_supported_zero(qq, qq_oracle, qq_weights)
    assert qq_proper == 141

    # Sharp boundary: the odd-route endpoint ports are the same full matching
    # and their weighted sums agree, but unequal endpoint weights make the
    # bare deletion hafnians unequal.
    sharp_first, sharp_last = sharp_route.edges[0], sharp_route.edges[-1]
    sharp_port = weighted_port_sum(qq, qq_oracle, qq_weights, qq_matchings, sharp_first)
    assert (
        sharp_port
        == weighted_port_sum(qq, qq_oracle, qq_weights, qq_matchings, sharp_last)
        == Fraction(-3)
    )
    sharp_bare = (
        bare_deletion_hafnian(qq, qq_oracle, qq_weights, sharp_first),
        bare_deletion_hafnian(qq, qq_oracle, qq_weights, sharp_last),
    )
    assert (qq_weights[sharp_first], qq_weights[sharp_last]) == (
        Fraction(1),
        Fraction(-3),
    )
    assert sharp_bare == (Fraction(-3), Fraction(1))
    assert sharp_bare[0] != sharp_bare[1]

    qcc = build_route_graph(
        3,
        (
            ("vx0", 0, 1, 1),
            ("vx1", 0, 1, 3),
            ("vy0", 0, 2, 1),
            ("vy1", 0, 2, 3),
            ("xy", 1, 2, 2),
        ),
    )
    qcc_weights = {item: Fraction(1) for item in qcc.edges}
    qcc_weights[qcc.routes[0].edges[0]] = Fraction(-3)
    qcc_oracle, qcc_matchings = assert_weighted_route_ports(qcc, qcc_weights)
    qcc_full_weights = sorted(
        matching_weight(qcc, qcc_weights, matching) for matching in qcc_matchings
    )
    assert qcc_full_weights == [Fraction(-3), Fraction(1), Fraction(1), Fraction(1)]
    qcc_proper = assert_least_supported_zero(qcc, qcc_oracle, qcc_weights)
    assert qcc_proper == 51

    even_route = qcc.routes[-1]
    even_sums = tuple(
        weighted_port_sum(qcc, qcc_oracle, qcc_weights, qcc_matchings, item)
        for item in (even_route.edges[0], even_route.edges[-1])
    )
    assert set(even_sums) == {Fraction(-2), Fraction(2)}
    assert even_sums[0] == -even_sums[1]

    return {
        "Q/Q": {
            "order": qq.order,
            "matching_weights": tuple(qq_full_weights),
            "proper_supported_minors": qq_proper,
            "unequal_bare_deletion_hafnians": sharp_bare,
            "common_weighted_port_sum": sharp_port,
        },
        "Q/C^2": {
            "order": qcc.order,
            "matching_weights": tuple(qcc_full_weights),
            "proper_supported_minors": qcc_proper,
            "even_endpoint_port_sums": even_sums,
        },
    }


def main() -> None:
    qq_count, qcc_count, qq_orders, qcc_orders = audit_small_subdivisions()
    fixtures = audit_weighted_fixtures()
    print("PASS: independent beta-three route-port pairing audit")
    print(
        "bounded subdivisions "
        f"(Q/Q, Q/C^2): ({qq_count}, {qcc_count}); "
        "odd lengths <=7, even lengths <=6"
    )
    print(f"Q/Q order distribution: {qq_orders}")
    print(f"Q/C^2 order distribution: {qcc_orders}")
    print(f"exact least-zero fixtures: {fixtures}")
    print("odd-route endpoint ports: equal sets and equal nonzero weighted sums")
    print("even-route endpoint ports: complementary doubletons and exact negatives")
    print(
        "SCOPE: bounded scalar pure-core mechanism audit only; no mixed-target "
        "inference"
    )
    print("GLOBAL KRENN-GU STATUS: UNRESOLVED")


if __name__ == "__main__":
    main()
