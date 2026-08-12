"""Independent no-import audit of the pure-cofactor port/fan reduction."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, permutations
from math import prod

Edge = tuple[int, int]
WeightedMatching = tuple[frozenset[Edge], Fraction]


def canon(left: int, right: int) -> Edge:
    """Return an unordered edge in canonical tuple form."""

    return (left, right) if left < right else (right, left)


def matching_census(
    vertex_count: int, weights: dict[Edge, Fraction]
) -> dict[int, list[WeightedMatching]]:
    """Enumerate disjoint edge masks and group them by their covered vertices."""

    records: dict[int, list[WeightedMatching]] = defaultdict(list)
    records[0].append((frozenset(), Fraction(1)))
    weighted_edges = tuple(weights.items())
    for size in range(1, vertex_count // 2 + 1):
        for selected in combinations(weighted_edges, size):
            vertex_mask = 0
            value = Fraction(1)
            edge_set: set[Edge] = set()
            valid = True
            for item, weight in selected:
                item_mask = (1 << item[0]) | (1 << item[1])
                if vertex_mask & item_mask:
                    valid = False
                    break
                vertex_mask |= item_mask
                value *= weight
                edge_set.add(item)
            if valid:
                records[vertex_mask].append((frozenset(edge_set), value))
    return records


def theta_route_data(d: int) -> tuple[int, dict[Edge, Fraction], tuple[Fraction, ...]]:
    """Build Theta_d in a representation independent of the primary checker."""

    weights: dict[Edge, Fraction] = {}
    route_values = tuple(
        Fraction(1 if index < d - 1 else -(d - 1)) for index in range(d)
    )
    for index, route_value in enumerate(route_values):
        a_vertex = 2 + 2 * index
        b_vertex = 3 + 2 * index
        weights[canon(0, a_vertex)] = Fraction(1)
        weights[canon(a_vertex, b_vertex)] = Fraction(1)
        weights[canon(b_vertex, 1)] = route_value
    return 2 * d + 2, weights, route_values


def route_state(mask: int, d: int) -> tuple[bool, bool, tuple[tuple[bool, bool], ...]]:
    """Decode endpoint and internal-pair membership for a theta subset."""

    endpoint_u = bool(mask & 1)
    endpoint_w = bool(mask & 2)
    internal = tuple(
        (bool(mask & (1 << (2 + 2 * index))), bool(mask & (1 << (3 + 2 * index))))
        for index in range(d)
    )
    return endpoint_u, endpoint_w, internal


def audit_sparse_route_family(d: int) -> dict[str, object]:
    """Audit all principal subsets and sparse root ports by edge-mask census."""

    vertex_count, weights, route_values = theta_route_data(d)
    census = matching_census(vertex_count, weights)
    full_mask = (1 << vertex_count) - 1
    full_records = census[full_mask]
    assert len(full_records) == d
    assert sum((value for _, value in full_records), Fraction(0)) == 0

    supported_zero_masks = []
    nonunique_masks = 0
    for mask, records in census.items():
        if mask == 0 or mask.bit_count() % 2:
            continue
        value = sum((weight for _, weight in records), Fraction(0))
        if records and value == 0:
            supported_zero_masks.append(mask)
        if len(records) <= 1:
            if records:
                assert value != 0
            continue

        nonunique_masks += 1
        endpoint_u, endpoint_w, internal = route_state(mask, d)
        assert endpoint_u and endpoint_w
        assert all(left == right for left, right in internal)
        complete_routes = tuple(
            index for index, state in enumerate(internal) if state == (True, True)
        )
        assert len(records) == len(complete_routes)
        assert value == sum((route_values[index] for index in complete_routes), Fraction(0))

    assert supported_zero_masks == [full_mask]

    ports: dict[Edge, list[Fraction]] = defaultdict(list)
    for edge_set, value in full_records:
        root_edge = next(item for item in edge_set if 0 in item)
        ports[root_edge].append(value)
    assert len(ports) == d
    assert all(len(values) == 1 for values in ports.values())
    assert sorted(value for values in ports.values() for value in values) == sorted(route_values)

    reference_value = route_values[0]
    characters = [value / reference_value for value in route_values[1:]]
    assert Fraction(1) + sum(characters, Fraction(0)) == 0
    return {
        "arity": d,
        "principal_subsets": len(census),
        "nonunique_subsets": nonunique_masks,
        "least_zero_is_full": True,
        "root_ports": len(ports),
    }


def abstract_theta(path_lengths: tuple[int, int, int]) -> tuple[int, dict[Edge, Fraction], tuple[Edge, ...]]:
    """Build three internally disjoint paths between vertices zero and one."""

    next_vertex = 2
    weights: dict[Edge, Fraction] = {}
    first_edges: list[Edge] = []
    for length in path_lengths:
        path = [0]
        for _ in range(length - 1):
            path.append(next_vertex)
            next_vertex += 1
        path.append(1)
        route_edges = [canon(path[index], path[index + 1]) for index in range(length)]
        first_edges.append(route_edges[0])
        for item in route_edges:
            weights[item] = Fraction(1)
    return next_vertex, weights, tuple(first_edges)


def audit_theta_endpoint_states() -> dict[str, object]:
    """Audit the odd/odd/odd and odd/even/even matching counts."""

    closed_count, closed_weights, closed_roots = abstract_theta((5, 3, 1))
    closed_census = matching_census(closed_count, closed_weights)
    closed_records = closed_census[(1 << closed_count) - 1]
    assert len(closed_records) == 3
    closed_allowed = set().union(*(edge_set for edge_set, _ in closed_records))
    assert closed_allowed == set(closed_weights)
    assert all(any(item in edge_set for edge_set, _ in closed_records) for item in closed_roots)

    open_count, open_weights, open_roots = abstract_theta((3, 4, 2))
    open_census = matching_census(open_count, open_weights)
    open_records = open_census[(1 << open_count) - 1]
    assert len(open_records) == 2
    open_allowed = set().union(*(edge_set for edge_set, _ in open_records))
    assert open_roots[0] not in open_allowed
    assert open_roots[1] in open_allowed and open_roots[2] in open_allowed

    return {
        "closed_lengths": (5, 3, 1),
        "closed_matchings": len(closed_records),
        "closed_matching_covered": True,
        "open_lengths": (3, 4, 2),
        "open_matchings": len(open_records),
        "odd_path_root_open": True,
    }


def audit_k4_open_completion() -> dict[str, object]:
    """Audit the K4 one-open-port carrier without cycle-construction code."""

    full_weights = {
        canon(0, 1): Fraction(1),
        canon(2, 3): Fraction(1),
        canon(0, 2): Fraction(1),
        canon(1, 3): Fraction(1),
        canon(0, 3): Fraction(1),
        canon(1, 2): Fraction(-2),
    }
    full_records = matching_census(4, full_weights)[15]
    assert sorted(value for _, value in full_records) == [Fraction(-2), Fraction(1), Fraction(1)]
    assert sum((value for _, value in full_records), Fraction(0)) == 0

    theta_edges = {
        canon(0, 2),
        canon(0, 1),
        canon(1, 2),
        canon(0, 3),
        canon(2, 3),
    }
    theta_weights = {item: full_weights[item] for item in theta_edges}
    theta_records = matching_census(4, theta_weights)[15]
    theta_allowed = set().union(*(edge_set for edge_set, _ in theta_records))
    assert len(theta_records) == 2
    assert canon(0, 2) not in theta_allowed
    assert canon(1, 3) not in theta_edges
    assert any(canon(0, 2) in edge_set and canon(1, 3) in edge_set for edge_set, _ in full_records)
    return {
        "full_matchings": len(full_records),
        "theta_matchings": len(theta_records),
        "open_edge": canon(0, 2),
        "exterior_completion": canon(1, 3),
    }


def audit_k33_aggregate() -> dict[str, object]:
    """Audit aggregate ports using a bipartite permutation expansion."""

    left = (0, 1, 2)
    right = (3, 4, 5)

    def weight(row: int, column: int) -> Fraction:
        return Fraction(-2 if (row, column) == (0, 3) else 1)

    matching_values: list[tuple[tuple[int, ...], Fraction]] = []
    for assignment in permutations(right):
        value = prod(weight(row, column) for row, column in zip(left, assignment, strict=True))
        matching_values.append((assignment, value))
    assert len(matching_values) == 6
    assert sum((value for _, value in matching_values), Fraction(0)) == 0

    ports = {
        column: sum(
            (value for assignment, value in matching_values if assignment[0] == column),
            Fraction(0),
        )
        for column in right
    }
    port_counts = {
        column: sum(assignment[0] == column for assignment, _ in matching_values)
        for column in right
    }
    assert ports == {3: Fraction(-4), 4: Fraction(2), 5: Fraction(2)}
    assert set(port_counts.values()) == {2}

    minor_values = []
    for selected_left in combinations(left, 2):
        for selected_right in combinations(right, 2):
            value = sum(
                (
                    prod(
                        weight(row, column)
                        for row, column in zip(selected_left, assignment, strict=True)
                    )
                    for assignment in permutations(selected_right)
                ),
                Fraction(0),
            )
            minor_values.append(value)
    assert set(minor_values) == {Fraction(-1), Fraction(2)}
    assert all(weight(row, column) for row in left for column in right)
    return {
        "full_permanent": Fraction(0),
        "port_counts": port_counts,
        "port_values": ports,
        "proper_two_by_two_values": sorted(set(minor_values)),
    }


def main() -> None:
    sparse = [audit_sparse_route_family(d) for d in (3, 4, 5, 6)]
    theta = audit_theta_endpoint_states()
    open_completion = audit_k4_open_completion()
    aggregate = audit_k33_aggregate()
    print("independent sparse route audit:", sparse)
    print("independent theta state audit:", theta)
    print("independent open completion audit:", open_completion)
    print("independent aggregate audit:", aggregate)
    print("minimal pure-cofactor port/fan no-import audit: PASS")


if __name__ == "__main__":
    main()
