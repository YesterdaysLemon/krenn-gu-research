"""Exact primary checks for the beta-three route-port pairing mechanism.

This standalone verifier builds the two bipartite beta-three route kernels as
actual subdivided simple graphs.  Route lengths are arbitrary positive integers
subject to the required parity: the Q/Q kernel has four odd routes, while the
Q/C2 kernel has route multiplicities 2, 2, 1 with four odd routes and one even
route.  Perfect matchings and weighted hafnians are enumerated exactly.

The checks are deliberately mechanism-scoped.  They verify several exact
subdivision and nonzero rational-weight fixtures, not every possible graph or
weight assignment.  In particular, they do not prove the global Krenn--Gu
conjecture.  The global status remains UNRESOLVED.

No theorem, audit, or repository implementation is imported.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from math import prod
from typing import TypeAlias

Edge: TypeAlias = tuple[int, int]
Matching: TypeAlias = tuple[Edge, ...]


def edge(left: int, right: int) -> Edge:
    """Return one undirected edge in canonical order."""

    assert left != right
    return (left, right) if left < right else (right, left)


@dataclass(frozen=True)
class Route:
    """One internally vertex-disjoint path between two branch vertices."""

    name: str
    path: tuple[int, ...]

    @property
    def length(self) -> int:
        return len(self.path) - 1

    @property
    def edges(self) -> tuple[Edge, ...]:
        return tuple(edge(left, right) for left, right in zip(self.path, self.path[1:]))

    @property
    def left_edge(self) -> Edge:
        return self.edges[0]

    @property
    def right_edge(self) -> Edge:
        return self.edges[-1]

    @property
    def endpoints(self) -> tuple[int, int]:
        return (self.path[0], self.path[-1])


@dataclass(frozen=True)
class RouteGraph:
    """A weighted graph whose non-branch vertices lie on disjoint routes."""

    vertices: tuple[int, ...]
    routes: tuple[Route, ...]
    weights: dict[Edge, Fraction]

    @property
    def support(self) -> frozenset[Edge]:
        return frozenset(self.weights)


@cache
def enumerate_perfect_matchings(
    vertices: tuple[int, ...], support: frozenset[Edge]
) -> tuple[Matching, ...]:
    """Enumerate perfect matchings of the induced support on ``vertices``."""

    if not vertices:
        return ((),)

    first = vertices[0]
    matchings: list[Matching] = []
    for position, partner in enumerate(vertices[1:], start=1):
        chosen = edge(first, partner)
        if chosen not in support:
            continue
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in enumerate_perfect_matchings(remainder, support):
            matchings.append((chosen, *tail))
    return tuple(matchings)


def matching_weight(matching: Matching, weights: dict[Edge, Fraction]) -> Fraction:
    """Return the exact product of all edge weights in a matching."""

    return prod((weights[item] for item in matching), start=Fraction(1))


def weighted_hafnian(
    vertices: tuple[int, ...], support: frozenset[Edge], weights: dict[Edge, Fraction]
) -> Fraction:
    """Return the exact weighted perfect-matching sum on ``vertices``."""

    return sum(
        (matching_weight(matching, weights) for matching in enumerate_perfect_matchings(vertices, support)),
        start=Fraction(0),
    )


def build_route_graph(
    branch_count: int,
    specifications: tuple[tuple[str, int, int, int], ...],
    selected_route_weights: dict[str, Fraction],
    right_weighted_routes: frozenset[str] = frozenset(),
) -> RouteGraph:
    """Build internally disjoint paths and weight each selected left port."""

    assert branch_count > 0
    vertices = list(range(branch_count))
    routes: list[Route] = []
    weights: dict[Edge, Fraction] = {}
    next_vertex = branch_count

    for name, left, right, length in specifications:
        assert 0 <= left < branch_count
        assert 0 <= right < branch_count
        assert left != right
        assert length > 0
        internal = tuple(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        vertices.extend(internal)
        route = Route(name=name, path=(left, *internal, right))
        for item in route.edges:
            assert item not in weights, "direct parallel routes would not form a simple graph"
            weights[item] = Fraction(1)
        routes.append(route)

    route_by_name = {route.name: route for route in routes}
    assert len(route_by_name) == len(routes)
    assert set(selected_route_weights) <= set(route_by_name)
    assert right_weighted_routes <= set(selected_route_weights)
    for name, value in selected_route_weights.items():
        assert value != 0
        selected_edge = (
            route_by_name[name].right_edge
            if name in right_weighted_routes
            else route_by_name[name].left_edge
        )
        weights[selected_edge] = value

    graph = RouteGraph(vertices=tuple(sorted(vertices)), routes=tuple(routes), weights=weights)
    assert all(value != 0 for value in graph.weights.values())
    return graph


def assert_bipartite(graph: RouteGraph) -> dict[int, int]:
    """Check the support graph is bipartite and return a two-coloring."""

    neighbors = {vertex: set() for vertex in graph.vertices}
    for left, right in graph.support:
        neighbors[left].add(right)
        neighbors[right].add(left)

    colors: dict[int, int] = {}
    for start in graph.vertices:
        if start in colors:
            continue
        colors[start] = 0
        pending = [start]
        while pending:
            current = pending.pop()
            for neighbor in neighbors[current]:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[current]
                    pending.append(neighbor)
                else:
                    assert colors[neighbor] != colors[current]
    return colors


def route_state(route: Route, matching: Matching) -> tuple[int, int]:
    """Record whether the matching uses the left and right route ports."""

    return (int(route.left_edge in matching), int(route.right_edge in matching))


def expected_route_edges(route: Route, state: tuple[int, int]) -> frozenset[Edge]:
    """Return the unique alternating route matching for an allowed state."""

    if route.length % 2 == 1:
        allowed = {(0, 0), (1, 1)}
        start = 0 if state == (1, 1) else 1
    else:
        allowed = {(1, 0), (0, 1)}
        start = 0 if state == (1, 0) else 1
    assert state in allowed
    return frozenset(route.edges[start::2])


def assert_route_restrictions(graph: RouteGraph, matchings: tuple[Matching, ...]) -> None:
    """Check every matching restricts to the parity-forced route alternation."""

    for matching in matchings:
        covered = sorted(vertex for item in matching for vertex in item)
        assert covered == list(graph.vertices)
        for route in graph.routes:
            actual = frozenset(item for item in route.edges if item in matching)
            assert actual == expected_route_edges(route, route_state(route, matching))


def port_indices(
    route: Route, endpoint: int, matchings: tuple[Matching, ...]
) -> frozenset[int]:
    """Return indices of global matchings using this route endpoint edge."""

    assert endpoint in route.endpoints
    endpoint_edge = route.left_edge if endpoint == route.endpoints[0] else route.right_edge
    return frozenset(index for index, matching in enumerate(matchings) if endpoint_edge in matching)


def port_contribution(
    indices: frozenset[int], matchings: tuple[Matching, ...], weights: dict[Edge, Fraction]
) -> Fraction:
    """Sum complete matching products using a chosen endpoint port."""

    return sum(
        (matching_weight(matchings[index], weights) for index in indices), start=Fraction(0)
    )


def incident_edge_contribution(graph: RouteGraph, endpoint_edge: Edge) -> Fraction:
    """Compute weight(edge) times the exact complementary hafnian."""

    remaining = tuple(vertex for vertex in graph.vertices if vertex not in endpoint_edge)
    return graph.weights[endpoint_edge] * weighted_hafnian(remaining, graph.support, graph.weights)


def assert_full_port_contribution(
    graph: RouteGraph,
    route: Route,
    endpoint: int,
    matchings: tuple[Matching, ...],
) -> Fraction:
    """Cross-check a nonzero port sum, including its incident edge factor."""

    indices = port_indices(route, endpoint, matchings)
    contribution = port_contribution(indices, matchings, graph.weights)
    endpoint_edge = route.left_edge if endpoint == route.endpoints[0] else route.right_edge
    assert contribution == incident_edge_contribution(graph, endpoint_edge)
    assert contribution != 0
    return contribution


def assert_least_supported_zero(graph: RouteGraph) -> int:
    """Check every proper supported induced even subset has nonzero hafnian."""

    assert weighted_hafnian(graph.vertices, graph.support, graph.weights) == 0
    full_mask = (1 << len(graph.vertices)) - 1
    checked = 0
    for vertex_mask in range(1, full_mask):
        if vertex_mask.bit_count() % 2:
            continue
        vertices = tuple(
            vertex
            for position, vertex in enumerate(graph.vertices)
            if vertex_mask & (1 << position)
        )
        if not enumerate_perfect_matchings(vertices, graph.support):
            continue
        assert weighted_hafnian(vertices, graph.support, graph.weights) != 0
        checked += 1
    return checked


def check_qq_fixture(
    lengths: tuple[int, int, int, int],
    values: tuple[Fraction, ...],
    right_weighted_routes: frozenset[str] = frozenset(),
) -> RouteGraph:
    """Check four odd Q/Q routes give four equal singleton port pairs."""

    assert len(values) == 4
    assert all(length > 0 and length % 2 == 1 for length in lengths)
    assert sum(values, start=Fraction(0)) == 0
    names = tuple(f"q{index}" for index in range(4))
    specifications = tuple(
        (name, 0, 1, length) for name, length in zip(names, lengths, strict=True)
    )
    graph = build_route_graph(
        branch_count=2,
        specifications=specifications,
        selected_route_weights=dict(zip(names, values, strict=True)),
        right_weighted_routes=right_weighted_routes,
    )
    colors = assert_bipartite(graph)
    assert colors[0] != colors[1]

    matchings = enumerate_perfect_matchings(graph.vertices, graph.support)
    assert len(matchings) == 4
    assert_route_restrictions(graph, matchings)

    singleton_pairs: list[frozenset[int]] = []
    for route, expected_value in zip(graph.routes, values, strict=True):
        assert route.length % 2 == 1
        left_port = port_indices(route, route.endpoints[0], matchings)
        right_port = port_indices(route, route.endpoints[1], matchings)
        assert left_port == right_port
        assert len(left_port) == 1
        singleton_pairs.append(left_port)
        left_sum = assert_full_port_contribution(graph, route, route.endpoints[0], matchings)
        right_sum = assert_full_port_contribution(graph, route, route.endpoints[1], matchings)
        assert left_sum == right_sum == expected_value

    assert set().union(*singleton_pairs) == set(range(4))
    assert sum(map(len, singleton_pairs)) == 4
    assert weighted_hafnian(graph.vertices, graph.support, graph.weights) == 0
    return graph


def check_qc2_fixture(
    vx_lengths: tuple[int, int],
    vy_lengths: tuple[int, int],
    xy_length: int,
    values: tuple[Fraction, Fraction, Fraction, Fraction],
) -> RouteGraph:
    """Check the 2,2,1 Q/C2 route kernel and complementary even ports."""

    assert all(length > 0 and length % 2 == 1 for length in (*vx_lengths, *vy_lengths))
    assert xy_length > 0 and xy_length % 2 == 0
    assert sum(values, start=Fraction(0)) == 0
    names = ("vx0", "vx1", "vy0", "vy1")
    specifications = (
        ("vx0", 0, 1, vx_lengths[0]),
        ("vx1", 0, 1, vx_lengths[1]),
        ("vy0", 0, 2, vy_lengths[0]),
        ("vy1", 0, 2, vy_lengths[1]),
        ("xy", 1, 2, xy_length),
    )
    graph = build_route_graph(
        branch_count=3,
        specifications=specifications,
        selected_route_weights=dict(zip(names, values, strict=True)),
    )
    colors = assert_bipartite(graph)
    assert colors[0] != colors[1]
    assert colors[0] != colors[2]
    assert colors[1] == colors[2]

    matchings = enumerate_perfect_matchings(graph.vertices, graph.support)
    assert len(matchings) == 4
    assert_route_restrictions(graph, matchings)
    route_by_name = {route.name: route for route in graph.routes}

    odd_singletons: list[frozenset[int]] = []
    for name, expected_value in zip(names, values, strict=True):
        route = route_by_name[name]
        assert route.length % 2 == 1
        left_port = port_indices(route, route.endpoints[0], matchings)
        right_port = port_indices(route, route.endpoints[1], matchings)
        assert left_port == right_port
        assert len(left_port) == 1
        odd_singletons.append(left_port)
        left_sum = assert_full_port_contribution(graph, route, route.endpoints[0], matchings)
        right_sum = assert_full_port_contribution(graph, route, route.endpoints[1], matchings)
        assert left_sum == right_sum == expected_value

    assert set().union(*odd_singletons) == set(range(4))
    assert sum(map(len, odd_singletons)) == 4

    even_route = route_by_name["xy"]
    assert even_route.length % 2 == 0
    x_port = port_indices(even_route, 1, matchings)
    y_port = port_indices(even_route, 2, matchings)
    assert len(x_port) == len(y_port) == 2
    assert x_port.isdisjoint(y_port)
    assert x_port | y_port == frozenset(range(4))

    x_sum = assert_full_port_contribution(graph, even_route, 1, matchings)
    y_sum = assert_full_port_contribution(graph, even_route, 2, matchings)
    full_hafnian = weighted_hafnian(graph.vertices, graph.support, graph.weights)
    assert full_hafnian == 0
    assert x_sum + y_sum == full_hafnian
    assert x_sum == -y_sum
    return graph


def main() -> None:
    """Run several exact subdivision and rational-weight fixtures."""

    qq_fixtures = (
        ((1, 3, 5, 7), (Fraction(1), Fraction(2), Fraction(3), Fraction(-6))),
        (
            (3, 3, 5, 9),
            (Fraction(1, 2), Fraction(2, 3), Fraction(5, 6), Fraction(-2)),
        ),
        (
            (3, 5, 7, 11),
            (Fraction(7, 5), Fraction(-2, 5), Fraction(3), Fraction(-4)),
        ),
    )
    for lengths, values in qq_fixtures:
        check_qq_fixture(lengths, values)

    qc2_fixtures = (
        (
            (1, 3),
            (1, 5),
            2,
            (Fraction(2), Fraction(-5), Fraction(1), Fraction(2)),
        ),
        (
            (3, 5),
            (5, 7),
            4,
            (Fraction(4, 3), Fraction(-13, 3), Fraction(1, 2), Fraction(5, 2)),
        ),
        (
            (1, 7),
            (3, 9),
            6,
            (Fraction(7, 5), Fraction(-17, 5), Fraction(3, 7), Fraction(11, 7)),
        ),
    )
    for vx_lengths, vy_lengths, xy_length, values in qc2_fixtures:
        check_qc2_fixture(vx_lengths, vy_lengths, xy_length, values)

    displayed_qq_control = check_qq_fixture(
        (3, 3, 3, 3),
        (Fraction(1), Fraction(1), Fraction(1), Fraction(-3)),
        right_weighted_routes=frozenset({"q3"}),
    )
    displayed_qc2_control = check_qc2_fixture(
        (1, 3),
        (1, 3),
        2,
        (Fraction(-3), Fraction(1), Fraction(1), Fraction(1)),
    )
    assert assert_least_supported_zero(displayed_qq_control) == 141
    assert assert_least_supported_zero(displayed_qc2_control) == 51

    print("A5 beta-three route-port pairing verifier: PASS")
    print(f"  Q/Q fixtures: {len(qq_fixtures)}; four odd singleton port pairs each")
    print(f"  Q/C2 fixtures: {len(qc2_fixtures)}; multiplicities 2,2,1")
    print("  exact full port contributions include their incident edge factors")
    print("  zero full hafnians force complementary even-port sums to be exact negatives")
    print("  displayed least-zero controls: Q/Q 141 and Q/C2 51 proper supported subsets")
    print("  scope: length-parametric mechanisms exercised on listed exact fixtures")
    print("  global Krenn--Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
