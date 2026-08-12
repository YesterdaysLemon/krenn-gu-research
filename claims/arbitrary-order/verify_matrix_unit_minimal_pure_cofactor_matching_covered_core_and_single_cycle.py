"""Primary exact checks for the minimal pure-cofactor allowed core."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import reduce
from itertools import combinations
from math import gcd
from operator import mul

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Weights = dict[Edge, Fraction]


def edge(left: int, right: int) -> Edge:
    """Return a canonically ordered edge."""
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    """Enumerate perfect matchings by first-vertex deletion."""
    if not vertices:
        return ((),)
    first = vertices[0]
    records = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            records.append((edge(first, partner),) + matching)
    return tuple(records)


def matching_weight(matching: Matching, weights: Weights) -> Fraction:
    """Return the exact product of one matching's edge weights."""
    return reduce(mul, (weights.get(item, Fraction(0)) for item in matching), Fraction(1))


def supported_matchings(vertices: tuple[int, ...], weights: Weights) -> tuple[Matching, ...]:
    """Return all support perfect matchings on the selected vertices."""
    return tuple(
        matching
        for matching in perfect_matchings(vertices)
        if all(weights.get(item, Fraction(0)) for item in matching)
    )


def hafnian(vertices: tuple[int, ...], weights: Weights) -> Fraction:
    """Evaluate the scalar hafnian exactly."""
    return sum(
        (matching_weight(matching, weights) for matching in perfect_matchings(vertices)),
        Fraction(0),
    )


def minimal_cancellation(vertices: tuple[int, ...], weights: Weights) -> tuple[int, ...]:
    """Select the first least-cardinality supported hafnian zero."""
    for size in range(2, len(vertices) + 1, 2):
        for subset in combinations(vertices, size):
            if supported_matchings(subset, weights) and hafnian(subset, weights) == 0:
                return subset
    raise AssertionError("no supported cancellation")


def cofactor_flow(vertices: tuple[int, ...], weights: Weights) -> dict[Edge, Fraction]:
    """Return all nonzero C_ij=z_ij haf(R-{i,j})."""
    result = {}
    for left, right in combinations(vertices, 2):
        item = edge(left, right)
        complement = tuple(vertex for vertex in vertices if vertex not in item)
        value = weights.get(item, Fraction(0)) * hafnian(complement, weights)
        if value:
            result[item] = value
    return result


def allowed_edges(vertices: tuple[int, ...], weights: Weights) -> set[Edge]:
    """Return the union of all support perfect matchings."""
    return {item for matching in supported_matchings(vertices, weights) for item in matching}


def components(vertices: tuple[int, ...], graph_edges: set[Edge]) -> tuple[tuple[int, ...], ...]:
    """Return connected components of a spanning simple graph."""
    neighbours: dict[int, set[int]] = defaultdict(set)
    for left, right in graph_edges:
        neighbours[left].add(right)
        neighbours[right].add(left)
    unseen = set(vertices)
    records = []
    while unseen:
        start = min(unseen)
        stack = [start]
        seen = {start}
        while stack:
            current = stack.pop()
            for neighbour in neighbours[current]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        unseen -= seen
        records.append(tuple(sorted(seen)))
    return tuple(records)


def degrees(vertices: tuple[int, ...], graph_edges: set[Edge]) -> dict[int, int]:
    """Return graph degrees."""
    return {
        vertex: sum(vertex in item for item in graph_edges)
        for vertex in vertices
    }


def symmetric_cycle_containing(first: Matching, second: Matching, target: Edge) -> set[Edge]:
    """Return the symmetric-difference cycle containing a target edge."""
    difference = set(first) ^ set(second)
    assert target in difference
    adjacency: dict[int, list[Edge]] = defaultdict(list)
    for item in difference:
        for vertex in item:
            adjacency[vertex].append(item)
    assert all(len(records) == 2 for records in adjacency.values())

    selected = set()
    stack = [target]
    while stack:
        item = stack.pop()
        if item in selected:
            continue
        selected.add(item)
        for vertex in item:
            stack.extend(record for record in adjacency[vertex] if record not in selected)
    assert len(selected) % 2 == 0
    return selected


def assert_every_edge_alternates(
    vertices: tuple[int, ...], weights: Weights, reference: Matching
) -> int:
    """Check the theorem's fixed-reference alternating-cycle generation."""
    matchings = supported_matchings(vertices, weights)
    active = allowed_edges(vertices, weights)
    checked = 0
    for item in active:
        witness = next(
            matching
            for matching in matchings
            if item in (set(reference) ^ set(matching))
        )
        cycle = symmetric_cycle_containing(reference, witness, item)
        assert cycle <= active
        checked += 1
    return checked


def assert_single_cycle_core() -> dict[str, object]:
    """Check a least six-cycle cancellation with an inactive support chord."""
    vertices = tuple(range(6))
    weights: Weights = {
        (0, 1): Fraction(1),
        (1, 2): Fraction(1),
        (2, 3): Fraction(1),
        (3, 4): Fraction(1),
        (4, 5): Fraction(1),
        (0, 5): Fraction(-1),
        (0, 2): Fraction(7),
    }
    assert hafnian(vertices, weights) == 0
    assert minimal_cancellation(vertices, weights) == vertices

    matchings = supported_matchings(vertices, weights)
    assert len(matchings) == 2
    assert sorted(matching_weight(record, weights) for record in matchings) == [-1, 1]

    active = set(cofactor_flow(vertices, weights))
    allowed = allowed_edges(vertices, weights)
    cycle = set(weights) - {(0, 2)}
    assert active == allowed == cycle
    assert components(vertices, active) == (vertices,)
    assert set(degrees(vertices, active).values()) == {2}
    assert assert_every_edge_alternates(vertices, weights, matchings[0]) == 6

    flow = cofactor_flow(vertices, weights)
    assert tuple(flow[item] for item in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5))) == (
        1,
        -1,
        1,
        -1,
        1,
        -1,
    )
    assert all(
        sum(value for item, value in flow.items() if vertex in item) == 0
        for vertex in vertices
    )

    # Every cycle-edge cofactor is one supported monomial; the inactive chord
    # has no supported complement at all.
    for item in cycle:
        complement = tuple(vertex for vertex in vertices if vertex not in item)
        assert len(supported_matchings(complement, weights)) == 1
    chord_complement = tuple(vertex for vertex in vertices if vertex not in (0, 2))
    assert not supported_matchings(chord_complement, weights)

    exponent = tuple(
        int(item in matchings[0]) - int(item in matchings[1])
        for item in sorted(cycle)
    )
    assert gcd(*[abs(value) for value in exponent if value]) == 1

    return {
        "vertices": len(vertices),
        "support_edges": len(weights),
        "allowed_edges": len(allowed),
        "perfect_matchings": len(matchings),
        "inactive_chord": (0, 2),
        "primitive_relation": True,
        "monomial_first_cofactors": len(cycle),
    }


def assert_branching_core() -> dict[str, object]:
    """Check the connected matching-covered branching alternative."""
    vertices = tuple(range(4))
    weights: Weights = {
        (0, 1): Fraction(1),
        (2, 3): Fraction(1),
        (0, 2): Fraction(1),
        (1, 3): Fraction(1),
        (0, 3): Fraction(1),
        (1, 2): Fraction(-2),
    }
    assert hafnian(vertices, weights) == 0
    assert minimal_cancellation(vertices, weights) == vertices
    matchings = supported_matchings(vertices, weights)
    assert len(matchings) == 3

    active = set(cofactor_flow(vertices, weights))
    assert active == allowed_edges(vertices, weights) == set(weights)
    assert components(vertices, active) == (vertices,)
    degree_map = degrees(vertices, active)
    assert set(degree_map.values()) == {3}
    beta = len(active) - len(vertices) + 1
    excess = sum(value - 2 for value in degree_map.values())
    assert (beta, excess) == (3, 4)
    assert assert_every_edge_alternates(vertices, weights, matchings[0]) == 6

    return {
        "active_graph": "K4",
        "perfect_matchings": len(matchings),
        "cyclomatic_rank": beta,
        "branching_excess": excess,
        "branch_vertices": sum(value >= 3 for value in degree_map.values()),
    }


def assert_component_minimality() -> dict[str, object]:
    """Check exact factorization before selection of the least residual."""
    vertices = tuple(range(6))
    weights: Weights = {
        (0, 1): Fraction(2),
        (0, 2): Fraction(3),
        (1, 3): Fraction(-2),
        (2, 3): Fraction(3),
        (4, 5): Fraction(5),
    }
    assert hafnian(vertices, weights) == 0
    allowed = allowed_edges(vertices, weights)
    pieces = components(vertices, allowed)
    assert pieces == ((0, 1, 2, 3), (4, 5))
    factors = tuple(hafnian(piece, weights) for piece in pieces)
    assert factors == (0, 5)
    assert hafnian(vertices, weights) == factors[0] * factors[1]
    selected = minimal_cancellation(vertices, weights)
    assert selected == pieces[0]
    assert components(selected, allowed_edges(selected, weights)) == (selected,)
    return {
        "nonminimal_components": len(pieces),
        "factor_hafnians": factors,
        "least_residual": selected,
        "least_core_connected": True,
    }


def main() -> None:
    """Run the primary exact checks."""
    cycle = assert_single_cycle_core()
    branch = assert_branching_core()
    minimality = assert_component_minimality()
    print("minimal pure-cofactor matching-covered core primary checks: PASS")
    print(f"  primitive single-cycle core: {cycle}")
    print(f"  connected branching core: {branch}")
    print(f"  component factorization/minimality: {minimality}")


if __name__ == "__main__":
    main()
