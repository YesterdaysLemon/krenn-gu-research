"""Primary exact checks for the pure-cofactor port/fan reduction."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations
from math import comb
from operator import mul
from functools import reduce

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Weights = dict[Edge, Fraction]


def edge(left: int, right: int) -> Edge:
    """Return a canonically ordered edge."""

    return (left, right) if left < right else (right, left)


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    """Enumerate perfect matchings by first-vertex deletion."""

    if not vertices:
        return ((),)
    first = vertices[0]
    records: list[Matching] = []
    for index, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            records.append((edge(first, partner),) + matching)
    return tuple(records)


def matching_weight(matching: Matching, weights: Weights) -> Fraction:
    """Return the exact product of the matching weights."""

    return reduce(
        mul,
        (weights.get(item, Fraction(0)) for item in matching),
        Fraction(1),
    )


def supported_matchings(vertices: tuple[int, ...], weights: Weights) -> tuple[Matching, ...]:
    """Return support perfect matchings on a principal vertex set."""

    return tuple(
        matching
        for matching in perfect_matchings(vertices)
        if all(weights.get(item, Fraction(0)) for item in matching)
    )


def hafnian(vertices: tuple[int, ...], weights: Weights) -> Fraction:
    """Evaluate a small exact weighted hafnian."""

    return sum(
        (matching_weight(matching, weights) for matching in supported_matchings(vertices, weights)),
        Fraction(0),
    )


def least_cancellation(vertices: tuple[int, ...], weights: Weights) -> tuple[int, ...]:
    """Find the first least-cardinality supported principal hafnian zero."""

    for size in range(2, len(vertices) + 1, 2):
        for subset in combinations(vertices, size):
            if supported_matchings(subset, weights) and hafnian(subset, weights) == 0:
                return subset
    raise AssertionError("no supported cancellation")


def cofactor(vertices: tuple[int, ...], item: Edge, weights: Weights) -> Fraction:
    """Evaluate z_e times the complementary principal hafnian."""

    complement = tuple(vertex for vertex in vertices if vertex not in item)
    return weights.get(item, Fraction(0)) * hafnian(complement, weights)


def allowed_edges(vertices: tuple[int, ...], weights: Weights) -> set[Edge]:
    """Return the union of the support perfect matchings."""

    return {
        item
        for matching in supported_matchings(vertices, weights)
        for item in matching
    }


def port_partition(
    vertices: tuple[int, ...], weights: Weights, root: int
) -> dict[Edge, tuple[Matching, ...]]:
    """Partition all perfect matchings by their root edge."""

    records = supported_matchings(vertices, weights)
    ports: dict[Edge, list[Matching]] = {}
    for matching in records:
        root_edge = next(item for item in matching if root in item)
        ports.setdefault(root_edge, []).append(matching)
    return {item: tuple(entries) for item, entries in ports.items()}


def symmetric_component(first: Matching, second: Matching, root: int) -> set[Edge]:
    """Return the symmetric-difference cycle through the root vertex."""

    difference = set(first) ^ set(second)
    adjacency: dict[int, set[int]] = {}
    for left, right in difference:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    assert root in adjacency
    component_vertices = {root}
    frontier = [root]
    while frontier:
        current = frontier.pop()
        for neighbour in adjacency[current]:
            if neighbour not in component_vertices:
                component_vertices.add(neighbour)
                frontier.append(neighbour)
    component = {
        item
        for item in difference
        if item[0] in component_vertices and item[1] in component_vertices
    }
    degrees = {
        vertex: sum(vertex in item for item in component)
        for vertex in component_vertices
    }
    assert set(degrees.values()) == {2}
    assert len(component) % 2 == 0
    return component


def ordered_cycle(cycle: set[Edge], root: int, first_edge: Edge) -> tuple[int, ...]:
    """Order a simple cycle from a specified root edge."""

    assert root in first_edge
    neighbour = first_edge[0] if first_edge[1] == root else first_edge[1]
    vertices = [root, neighbour]
    previous = root
    current = neighbour
    while current != root:
        candidates = []
        for item in cycle:
            if current not in item:
                continue
            other = item[0] if item[1] == current else item[1]
            if other != previous:
                candidates.append(other)
        assert len(candidates) == 1
        previous, current = current, candidates[0]
        vertices.append(current)
    return tuple(vertices)


def path_edges(vertices: tuple[int, ...]) -> set[Edge]:
    """Return consecutive edges of an ordered path."""

    return {edge(vertices[index], vertices[index + 1]) for index in range(len(vertices) - 1)}


def theta_from_cycles(
    cycle_e: set[Edge],
    cycle_f: set[Edge],
    reference: Matching,
    root: int,
    p_edge: Edge,
    e_edge: Edge,
    f_edge: Edge,
) -> tuple[tuple[int, int, int], set[Edge], set[int]]:
    """Construct the first-return theta and report its three path lengths."""

    ordered_e = ordered_cycle(cycle_e, root, e_edge)
    base_vertices = {vertex for item in cycle_f for vertex in item}
    return_index = next(
        index
        for index, vertex in enumerate(ordered_e[1:-1], start=1)
        if vertex in base_vertices
    )
    target = ordered_e[return_index]
    b_vertices = ordered_e[: return_index + 1]

    ordered_p = ordered_cycle(cycle_f, root, p_edge)
    p_index = ordered_p.index(target)
    p_vertices = ordered_p[: p_index + 1]

    ordered_f = ordered_cycle(cycle_f, root, f_edge)
    f_index = ordered_f.index(target)
    f_vertices = ordered_f[: f_index + 1]

    theta_edges = path_edges(b_vertices) | path_edges(p_vertices) | path_edges(f_vertices)
    theta_vertices = {vertex for item in theta_edges for vertex in item}
    lengths = (len(b_vertices) - 1, len(p_vertices) - 1, len(f_vertices) - 1)

    for item in reference:
        left_in = item[0] in theta_vertices
        right_in = item[1] in theta_vertices
        assert left_in == right_in
        if left_in:
            assert item in theta_edges
    return lengths, theta_edges, theta_vertices


def theta_family(d: int) -> tuple[tuple[int, ...], Weights, tuple[Matching, ...]]:
    """Build the exact sparse d-route theta sharpness family."""

    root = 0
    other_root = 1
    weights: Weights = {}
    expected: list[Matching] = []
    for index in range(d):
        a_vertex = 2 + 2 * index
        b_vertex = 3 + 2 * index
        route_weight = Fraction(1 if index < d - 1 else -(d - 1))
        weights[edge(root, a_vertex)] = Fraction(1)
        weights[edge(a_vertex, b_vertex)] = Fraction(1)
        weights[edge(b_vertex, other_root)] = route_weight
    for selected in range(d):
        matching = [edge(root, 2 + 2 * selected), edge(3 + 2 * selected, other_root)]
        matching.extend(
            edge(2 + 2 * index, 3 + 2 * index)
            for index in range(d)
            if index != selected
        )
        expected.append(tuple(sorted(matching)))
    vertices = tuple(range(2 * d + 2))
    return vertices, weights, tuple(expected)


def assert_sparse_theta_family(d: int) -> dict[str, object]:
    """Check minimality, ports, fans, and theta data for Theta_d."""

    vertices, weights, expected = theta_family(d)
    records = tuple(tuple(sorted(record)) for record in supported_matchings(vertices, weights))
    assert set(records) == set(expected)
    assert hafnian(vertices, weights) == 0
    assert least_cancellation(vertices, weights) == vertices
    assert allowed_edges(vertices, weights) == set(weights)

    ports = port_partition(vertices, weights, 0)
    assert len(ports) == d
    assert {len(entries) for entries in ports.values()} == {1}
    port_values = {
        item: sum((matching_weight(record, weights) for record in entries), Fraction(0))
        for item, entries in ports.items()
    }
    assert all(value == cofactor(vertices, item, weights) for item, value in port_values.items())
    assert sum(port_values.values(), Fraction(0)) == 0

    reference = expected[0]
    p_edge = edge(0, 2)
    cycles: dict[Edge, set[Edge]] = {}
    ratios: list[Fraction] = []
    for index in range(1, d):
        exit_edge = edge(0, 2 + 2 * index)
        cycle = symmetric_component(reference, expected[index], 0)
        assert p_edge in cycle and exit_edge in cycle
        assert set(reference) ^ cycle == set(expected[index])
        cycles[exit_edge] = cycle
        ratios.append(
            matching_weight(expected[index], weights)
            / matching_weight(reference, weights)
        )
    assert Fraction(1) + sum(ratios, Fraction(0)) == 0

    fan_edges = set().union(*cycles.values())
    fan_vertices = {vertex for item in fan_edges for vertex in item}
    assert fan_vertices == set(vertices)
    assert len(supported_matchings(tuple(sorted(fan_vertices)), weights)) == d

    if d >= 3:
        e_edge = edge(0, 4)
        f_edge = edge(0, 6)
        lengths, theta_edges, theta_vertices = theta_from_cycles(
            cycles[e_edge],
            cycles[f_edge],
            reference,
            0,
            p_edge,
            e_edge,
            f_edge,
        )
        assert lengths == (3, 3, 3)
        theta_weights = {item: weights[item] for item in theta_edges}
        theta_records = supported_matchings(tuple(sorted(theta_vertices)), theta_weights)
        assert len(theta_records) == 3
        assert allowed_edges(tuple(sorted(theta_vertices)), theta_weights) == theta_edges

    return {
        "arity": d,
        "vertices": len(vertices),
        "perfect_matchings": len(records),
        "theta_pairs": comb(d - 1, 2),
        "port_mode": "sparse",
    }


def assert_open_port_k4() -> dict[str, object]:
    """Check the odd/even/even cubic theta and exterior completion."""

    vertices = (0, 1, 2, 3)
    weights: Weights = {
        edge(0, 1): Fraction(1),
        edge(2, 3): Fraction(1),
        edge(0, 2): Fraction(1),
        edge(1, 3): Fraction(1),
        edge(0, 3): Fraction(1),
        edge(1, 2): Fraction(-2),
    }
    reference = tuple(sorted((edge(0, 1), edge(2, 3))))
    e_matching = tuple(sorted((edge(0, 2), edge(1, 3))))
    f_matching = tuple(sorted((edge(0, 3), edge(1, 2))))
    assert hafnian(vertices, weights) == 0
    assert least_cancellation(vertices, weights) == vertices
    assert set(supported_matchings(vertices, weights)) == {
        reference,
        e_matching,
        f_matching,
    }

    cycle_e = symmetric_component(reference, e_matching, 0)
    cycle_f = symmetric_component(reference, f_matching, 0)
    lengths, theta_edges, theta_vertices = theta_from_cycles(
        cycle_e,
        cycle_f,
        reference,
        0,
        edge(0, 1),
        edge(0, 2),
        edge(0, 3),
    )
    assert sorted(lengths) == [1, 2, 2]
    theta_weights = {item: weights[item] for item in theta_edges}
    theta_records = supported_matchings(tuple(sorted(theta_vertices)), theta_weights)
    assert len(theta_records) == 2
    assert edge(0, 2) not in allowed_edges(tuple(sorted(theta_vertices)), theta_weights)
    assert edge(1, 3) not in theta_edges
    assert edge(1, 3) in cycle_e
    assert len(supported_matchings(vertices, weights)) == 3
    return {
        "active_graph": "K4",
        "theta_lengths": sorted(lengths),
        "theta_matchings": len(theta_records),
        "full_fan_matchings": 3,
        "open_port": edge(0, 2),
    }


def assert_aggregate_k33() -> dict[str, object]:
    """Check the exact nonzero aggregate-port sharpness model."""

    vertices = tuple(range(6))
    weights: Weights = {
        edge(left, right): Fraction(-2 if (left, right) == (0, 3) else 1)
        for left in range(3)
        for right in range(3, 6)
    }
    records = supported_matchings(vertices, weights)
    assert len(records) == 6
    assert hafnian(vertices, weights) == 0
    assert least_cancellation(vertices, weights) == vertices
    assert allowed_edges(vertices, weights) == set(weights)

    ports = port_partition(vertices, weights, 0)
    assert {len(entries) for entries in ports.values()} == {2}
    values = {
        item: sum((matching_weight(record, weights) for record in entries), Fraction(0))
        for item, entries in ports.items()
    }
    assert values == {
        edge(0, 3): Fraction(-4),
        edge(0, 4): Fraction(2),
        edge(0, 5): Fraction(2),
    }
    assert all(value == cofactor(vertices, item, weights) for item, value in values.items())
    assert sum(values.values(), Fraction(0)) == 0
    return {
        "active_graph": "K3,3",
        "perfect_matchings": len(records),
        "root_degree": len(ports),
        "port_sizes": sorted(len(entries) for entries in ports.values()),
        "port_values": values,
    }


def main() -> None:
    sparse = [assert_sparse_theta_family(d) for d in (3, 4, 5)]
    open_port = assert_open_port_k4()
    aggregate = assert_aggregate_k33()
    print("sparse fan checks:", sparse)
    print("one-open-port theta check:", open_port)
    print("aggregate port check:", aggregate)
    print("minimal pure-cofactor port/fan primary checks: PASS")


if __name__ == "__main__":
    main()
