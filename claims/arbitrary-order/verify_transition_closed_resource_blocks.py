#!/usr/bin/env python3
"""Portable positive replay for transition-closed resource blocks.

The script builds literal protected/scalar supports.  It checks the local
K3,3 triple block and its triangular-prism mutation, then constructs all-
triple and hybrid pair/triple partitions on three protected K4 components.
For each global support it constructs a directed-cycle word and counts its
physical perfect matchings directly.  A two-vertex example checks physically
overlapping resources.  This is finite corroboration, not the all-order proof.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path


COLORS = (0, 1, 2)
LOCAL_MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


State = tuple[int, int]


@dataclass(frozen=True, order=True)
class Resource:
    name: str
    color: int
    endpoints: tuple[int, int]


@dataclass(frozen=True, order=True)
class Scalar:
    left: State
    right: State
    kind: str
    block: str


@dataclass
class Support:
    vertex_count: int
    resources: tuple[Resource, ...]
    blocks: dict[str, tuple[Resource, ...]]
    scalars: tuple[Scalar, ...]


def scalar_key(left: State, right: State) -> frozenset[State]:
    assert left != right
    return frozenset((left, right))


def protected_scalar(resource: Resource, block: str) -> Scalar:
    u, v = resource.endpoints
    return Scalar((u, resource.color), (v, resource.color), "protected", block)


def crossing(
    left_resource: Resource,
    left_index: int,
    right_resource: Resource,
    right_index: int,
    block: str,
) -> Scalar:
    left = (left_resource.endpoints[left_index], left_resource.color)
    right = (right_resource.endpoints[right_index], right_resource.color)
    assert left[0] != right[0], "physical scalar self-loop"
    return Scalar(left, right, "crossing", block)


def triple_scalars(
    resources: tuple[Resource, Resource, Resource],
    block: str,
    bc_anti: bool = True,
) -> list[Scalar]:
    a, b, c = resources
    result = [protected_scalar(resource, block) for resource in resources]
    for i in range(2):
        result.append(crossing(a, i, b, i, block))
        result.append(crossing(a, i, c, i, block))
        result.append(crossing(b, i, c, 1 - i if bc_anti else i, block))
    return result


def pair_scalars(
    resources: tuple[Resource, Resource], block: str
) -> list[Scalar]:
    a, b = resources
    return [
        protected_scalar(a, block),
        protected_scalar(b, block),
        crossing(a, 0, b, 0, block),
        crossing(a, 1, b, 1, block),
    ]


def scalar_index(support: Support) -> dict[frozenset[State], Scalar]:
    index: dict[frozenset[State], Scalar] = {}
    for scalar in support.scalars:
        key = scalar_key(scalar.left, scalar.right)
        assert key not in index
        index[key] = scalar
    return index


def verify_partition(support: Support) -> dict[str, object]:
    expected_states = {
        (vertex, color)
        for vertex in range(support.vertex_count)
        for color in COLORS
    }
    resource_states: dict[State, Resource] = {}
    for resource in support.resources:
        assert resource.color in COLORS
        u, v = resource.endpoints
        assert u != v
        for state in ((u, resource.color), (v, resource.color)):
            assert state not in resource_states
            resource_states[state] = resource
    assert set(resource_states) == expected_states

    block_for_resource: dict[str, str] = {}
    for block, resources in support.blocks.items():
        assert 2 <= len(resources) <= 3
        assert len({resource.color for resource in resources}) == len(resources)
        for resource in resources:
            assert resource.name not in block_for_resource
            block_for_resource[resource.name] = block
    assert set(block_for_resource) == {resource.name for resource in support.resources}

    crossing_degree = Counter({state: 0 for state in expected_states})
    protected_count = 0
    crossing_count = 0
    for scalar in support.scalars:
        assert scalar.block in support.blocks
        assert scalar.left[0] != scalar.right[0]
        left_resource = resource_states[scalar.left]
        right_resource = resource_states[scalar.right]
        assert left_resource in support.blocks[scalar.block]
        assert right_resource in support.blocks[scalar.block]
        if scalar.kind == "protected":
            protected_count += 1
            assert left_resource == right_resource
        else:
            crossing_count += 1
            assert left_resource != right_resource
            assert left_resource.color != right_resource.color
            crossing_degree[scalar.left] += 1
            crossing_degree[scalar.right] += 1
    scalar_index(support)
    assert protected_count == len(support.resources)
    assert min(crossing_degree.values()) >= 1
    return {
        "vertices": support.vertex_count,
        "resources": len(support.resources),
        "blocks": len(support.blocks),
        "block_size_histogram": dict(Counter(map(len, support.blocks.values()))),
        "protected_scalars": protected_count,
        "crossing_scalars": crossing_count,
        "crossing_degree_histogram": dict(Counter(crossing_degree.values())),
    }


def transition_closure_failures(support: Support) -> list[dict[str, object]]:
    index = scalar_index(support)
    neighbors: dict[State, set[State]] = defaultdict(set)
    for scalar in support.scalars:
        if scalar.kind == "crossing":
            neighbors[scalar.left].add(scalar.right)
            neighbors[scalar.right].add(scalar.left)

    failures: list[dict[str, object]] = []
    for block, resources in support.blocks.items():
        for resource in resources:
            u, v = resource.endpoints
            from_u = neighbors[(v, resource.color)]
            from_v = neighbors[(u, resource.color)]
            assert from_u and from_v
            for target_u, target_v in product(from_u, from_v):
                if target_u[0] == target_v[0]:
                    continue
                if scalar_key(target_u, target_v) not in index:
                    failures.append(
                        {
                            "block": block,
                            "resource": resource.name,
                            "targets": (target_u, target_v),
                        }
                    )
    return failures


def local_graph_type(bc_anti: bool) -> dict[str, object]:
    resources = (
        Resource("a", 0, (0, 1)),
        Resource("b", 1, (2, 3)),
        Resource("c", 2, (4, 5)),
    )
    support = Support(
        6,
        resources,
        {"T": resources},
        tuple(triple_scalars(resources, "T", bc_anti=bc_anti)),
    )
    assert len({state for resource in resources for state in (
        (resource.endpoints[0], resource.color),
        (resource.endpoints[1], resource.color),
    )}) == 6
    scalar_index(support)
    adjacency = {state: set() for resource in resources for state in (
        (resource.endpoints[0], resource.color),
        (resource.endpoints[1], resource.color),
    )}
    for scalar in support.scalars:
        adjacency[scalar.left].add(scalar.right)
        adjacency[scalar.right].add(scalar.left)
    assert set(map(len, adjacency.values())) == {3}

    triangles = 0
    states = sorted(adjacency)
    for x, y, z in combinations(states, 3):
        if y in adjacency[x] and z in adjacency[x] and z in adjacency[y]:
            triangles += 1
    failures = transition_closure_failures(support)
    if bc_anti:
        # The displayed bipartition makes all nine possible cross edges.
        shores = (
            {(0, 0), (3, 1), (5, 2)},
            {(1, 0), (2, 1), (4, 2)},
        )
        assert all(
            right in adjacency[left]
            for left in shores[0]
            for right in shores[1]
        )
        assert triangles == 0 and not failures
        graph = "K3,3"
    else:
        assert triangles == 2 and failures
        graph = "triangular_prism"
    return {
        "graph": graph,
        "vertices": 6,
        "edges": len(support.scalars),
        "triangles": triangles,
        "transition_closure_failures": len(failures),
    }


def k4_resources() -> tuple[Resource, ...]:
    resources: list[Resource] = []
    for component in range(3):
        for color, matching in enumerate(LOCAL_MATCHINGS):
            for edge_index, (u, v) in enumerate(matching):
                resources.append(
                    Resource(
                        f"c{color}.k{component}.e{edge_index}",
                        color,
                        (4 * component + u, 4 * component + v),
                    )
                )
    return tuple(resources)


def resource_map(resources: tuple[Resource, ...]) -> dict[tuple[int, int, int], Resource]:
    result = {}
    for resource in resources:
        color, component, edge_index = (
            int(piece[1:]) for piece in resource.name.split(".")
        )
        result[(color, component, edge_index)] = resource
    return result


def build_three_k4_support(hybrid: bool) -> Support:
    resources = k4_resources()
    lookup = resource_map(resources)
    blocks: dict[str, tuple[Resource, ...]] = {}
    scalars: list[Scalar] = []

    if not hybrid:
        for component in range(3):
            for edge_index in range(2):
                block = f"T{component}.{edge_index}"
                triple = (
                    lookup[(0, component, edge_index)],
                    lookup[(1, (component + 1) % 3, edge_index)],
                    lookup[(2, (component + 2) % 3, edge_index)],
                )
                blocks[block] = triple
                scalars.extend(triple_scalars(triple, block))
    else:
        # Two triples consume all resources in components (color,component)
        # (0,0), (1,1), and (2,2).  The remaining resources form two paired
        # blocks of each color type.
        for edge_index in range(2):
            block = f"T0.{edge_index}"
            triple = (
                lookup[(0, 0, edge_index)],
                lookup[(1, 1, edge_index)],
                lookup[(2, 2, edge_index)],
            )
            blocks[block] = triple
            scalars.extend(triple_scalars(triple, block))
        pair_specs = (
            (0, 1, 1, 0),
            (0, 2, 2, 0),
            (1, 2, 2, 1),
        )
        for color_a, color_b, component_a, component_b in pair_specs:
            for edge_index in range(2):
                block = f"P{color_a}{color_b}.{edge_index}"
                pair = (
                    lookup[(color_a, component_a, edge_index)],
                    lookup[(color_b, component_b, edge_index)],
                )
                blocks[block] = pair
                scalars.extend(pair_scalars(pair, block))

    return Support(12, resources, blocks, tuple(scalars))


def mate_maps(support: Support) -> tuple[dict[int, int], ...]:
    result = []
    for color in COLORS:
        mate = {}
        for resource in support.resources:
            if resource.color != color:
                continue
            u, v = resource.endpoints
            mate[u] = v
            mate[v] = u
        assert set(mate) == set(range(support.vertex_count))
        result.append(mate)
    return tuple(result)


def transition_arcs(
    support: Support, base: int
) -> dict[int, tuple[tuple[int, int], ...]]:
    mates = mate_maps(support)[base]
    crossings = [scalar for scalar in support.scalars if scalar.kind == "crossing"]
    arcs: dict[int, list[tuple[int, int]]] = {u: [] for u in range(support.vertex_count)}
    for u in range(support.vertex_count):
        source = (mates[u], base)
        for scalar in crossings:
            if scalar.left == source:
                arcs[u].append(scalar.right)
            elif scalar.right == source:
                arcs[u].append(scalar.left)
        assert arcs[u]
    return {u: tuple(values) for u, values in arcs.items()}


def cycle_candidates(
    arcs: dict[int, tuple[tuple[int, int], ...]]
):
    for start in arcs:
        stack = [(start, (start,), ())]
        while stack:
            current, vertices, chosen = stack.pop()
            for target, label in arcs[current]:
                arc = (current, target, label)
                if target == start:
                    yield vertices, chosen + (arc,)
                elif target not in vertices:
                    stack.append((target, vertices + (target,), chosen + (arc,)))


def compatible_physical_edges(
    support: Support, word: tuple[int, ...]
) -> dict[int, set[int]]:
    adjacency = {vertex: set() for vertex in range(support.vertex_count)}
    for scalar in support.scalars:
        u, color_u = scalar.left
        v, color_v = scalar.right
        if word[u] == color_u and word[v] == color_v:
            adjacency[u].add(v)
            adjacency[v].add(u)
    return adjacency


def count_physical_matchings(
    support: Support, word: tuple[int, ...]
) -> tuple[int, tuple[tuple[int, int], ...] | None]:
    adjacency = compatible_physical_edges(support, word)
    full_mask = (1 << support.vertex_count) - 1

    @lru_cache(maxsize=None)
    def count(mask: int) -> int:
        if mask == 0:
            return 1
        low = mask & -mask
        u = low.bit_length() - 1
        return sum(
            count(mask ^ (1 << u) ^ (1 << v))
            for v in adjacency[u]
            if mask & (1 << v)
        )

    total = count(full_mask)
    if total != 1:
        return total, None
    matching = []
    mask = full_mask
    while mask:
        low = mask & -mask
        u = low.bit_length() - 1
        choices = [
            v
            for v in adjacency[u]
            if mask & (1 << v)
            and count(mask ^ (1 << u) ^ (1 << v)) > 0
        ]
        assert len(choices) == 1
        v = choices[0]
        matching.append(tuple(sorted((u, v))))
        mask ^= (1 << u) | (1 << v)
    return total, tuple(sorted(matching))


def block_case_histogram(
    support: Support, base: int, cycle_vertices: tuple[int, ...]
) -> dict[int, int]:
    cycle_set = set(cycle_vertices)
    histogram = Counter()
    for resources in support.blocks.values():
        base_resources = [resource for resource in resources if resource.color == base]
        if not base_resources:
            continue
        assert len(base_resources) == 1
        histogram[sum(vertex in cycle_set for vertex in base_resources[0].endpoints)] += 1
    return dict(sorted(histogram.items()))


def find_positive_witness(
    support: Support, require_two_exit: bool
) -> dict[str, object]:
    for base in COLORS:
        arcs = transition_arcs(support, base)
        for cycle_vertices, chosen in cycle_candidates(arcs):
            word = [base] * support.vertex_count
            for _, target, label in chosen:
                word[target] = label
            literal_word = tuple(word)
            if len(set(literal_word)) == 1:
                continue
            cases = block_case_histogram(support, base, cycle_vertices)
            if require_two_exit and cases.get(2, 0) == 0:
                continue
            count, matching = count_physical_matchings(support, literal_word)
            assert count == 1 and matching is not None
            return {
                "base": base,
                "cycle_vertices": list(cycle_vertices),
                "cycle_arcs": [list(arc) for arc in chosen],
                "word_by_k4": [
                    "".join(map(str, literal_word[start : start + 4]))
                    for start in range(0, support.vertex_count, 4)
                ],
                "block_r_histogram": cases,
                "physical_matching_count": count,
                "physical_matching": [list(edge) for edge in matching],
            }
    raise AssertionError("the finite transition-closed support had no requested witness")


def verify_global_support(hybrid: bool) -> dict[str, object]:
    support = build_three_k4_support(hybrid)
    ledger = verify_partition(support)
    failures = transition_closure_failures(support)
    assert not failures
    ordinary = find_positive_witness(support, require_two_exit=False)
    two_exit = find_positive_witness(support, require_two_exit=True)
    return {
        "kind": "hybrid_pair_triple" if hybrid else "all_triple",
        "ledger": ledger,
        "transition_closure_failures": 0,
        "mixed_unique_witness": ordinary,
        "two_exit_mixed_unique_witness": two_exit,
    }


def verify_overlap_control() -> dict[str, object]:
    resources = tuple(Resource(f"c{color}", color, (0, 1)) for color in COLORS)
    block = "overlap"
    scalars = [protected_scalar(resource, block) for resource in resources]
    for left, right in combinations(resources, 2):
        scalars.append(crossing(left, 0, right, 1, block))
        scalars.append(crossing(left, 1, right, 0, block))
    support = Support(2, resources, {block: resources}, tuple(scalars))
    ledger = verify_partition(support)
    assert not transition_closure_failures(support)
    mixed_counts = {}
    for word in product(COLORS, repeat=2):
        if word[0] == word[1]:
            continue
        count, _ = count_physical_matchings(support, word)
        assert count == 1
        mixed_counts["".join(map(str, word))] = count
    return {
        "ledger": ledger,
        "transition_closure_failures": 0,
        "mixed_word_matching_counts": mixed_counts,
    }


def verify() -> dict[str, object]:
    local_positive = local_graph_type(bc_anti=True)
    local_mutation = local_graph_type(bc_anti=False)
    assert local_positive["transition_closure_failures"] == 0
    assert local_mutation["transition_closure_failures"] > 0
    return {
        "status": "TRANSITION_CLOSED_POSITIVE_REPLAY_PASS",
        "local_positive": local_positive,
        "local_all_diagonal_mutation": local_mutation,
        "all_triple_three_k4": verify_global_support(hybrid=False),
        "hybrid_three_k4": verify_global_support(hybrid=True),
        "physical_overlap_control": verify_overlap_control(),
        "scope": (
            "finite literal corroboration of the conditional block theorem; "
            "not a source-driven normal-form reduction"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional JSON receipt path")
    args = parser.parse_args()
    rendered = json.dumps(verify(), indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    print(rendered)


if __name__ == "__main__":
    main()
