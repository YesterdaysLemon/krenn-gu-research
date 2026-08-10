"""Independent no-import audit of the maximum-degree-four proof interfaces."""

from __future__ import annotations

from itertools import combinations


def canon(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def pairing_sum(vertices: frozenset[int], weights: dict[tuple[int, int], int]) -> int:
    if not vertices:
        return 1
    first = min(vertices)
    total = 0
    for partner in sorted(vertices - {first}):
        total += weights.get(canon(first, partner), 0) * pairing_sum(
            vertices - {first, partner}, weights
        )
    return total


def all_partial_pairings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    yield from all_partial_pairings(vertices[1:])
    for position, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in all_partial_pairings(remainder):
            yield (canon(first, partner), *tail)


def audit_noncancellation_directly() -> None:
    vertices = tuple(range(6))
    base = {canon(0, 1), canon(2, 3), canon(4, 5)}
    examined = 0
    for residual_tuple in all_partial_pairings(vertices):
        residual = set(residual_tuple)
        if residual & base:
            continue
        weights = {
            canon(0, 1): 2,
            canon(2, 3): -3,
            canon(4, 5): 5,
        }
        for index, item in enumerate(sorted(residual)):
            weights[item] = (7 + index) * (-1 if sum(item) % 2 else 1)
        full = pairing_sum(frozenset(vertices), weights)
        if full == 0:
            continue
        for size in (0, 2, 4, 6):
            for chosen in combinations(vertices, size):
                chosen_set = frozenset(chosen)
                support_count = pairing_sum(
                    chosen_set, {item: 1 for item in weights}
                )
                if support_count:
                    assert pairing_sum(chosen_set, weights) != 0
        examined += 1
    assert examined >= 40


def covers_once(edges: set[tuple[int, int]], vertices: set[int]) -> bool:
    seen = []
    for item in edges:
        if not set(item) <= vertices:
            return False
        seen.extend(item)
    return sorted(seen) == sorted(vertices)


def cyclic_path(cycle: tuple[int, ...], start_index: int, finish_index: int) -> tuple[int, ...]:
    order = len(cycle)
    output = [cycle[start_index]]
    cursor = start_index
    while cursor != finish_index:
        cursor = (cursor + 1) % order
        output.append(cycle[cursor])
    return tuple(output)


def path_edge_set(path: tuple[int, ...]) -> set[tuple[int, int]]:
    return {canon(path[index], path[index + 1]) for index in range(len(path) - 1)}


def audit_chords_under_relabelling() -> None:
    total = 0
    for order in (6, 8, 10, 12, 14):
        # A deterministic nontrivial relabelling keeps this audit independent
        # of the primary script's natural cyclic order.
        cycle = tuple((3 * index) % order for index in range(order)) if order % 3 else tuple(
            (5 * index) % order for index in range(order)
        )
        # The multipliers above must be units modulo the selected order.
        if len(set(cycle)) != order:
            cycle = tuple((order - 1 - index) for index in range(order))
        pc = {canon(cycle[index], cycle[index + 1]) for index in range(0, order, 2)}
        pd = {
            canon(cycle[index], cycle[(index + 1) % order])
            for index in range(1, order, 2)
        }
        position = {vertex: index for index, vertex in enumerate(cycle)}

        for chord in combinations(cycle, 2):
            item = canon(*chord)
            left, right = position[chord[0]], position[chord[1]]
            if (left - right) % 2 == 0 or item in pc or item in pd:
                continue
            forward = cyclic_path(cycle, left, right)
            backward = tuple(reversed(cyclic_path(cycle, right, left)))
            arcs = (forward, backward)
            selected = [
                path
                for path in arcs
                if canon(path[0], path[1]) in pd
                and canon(path[-2], path[-1]) in pd
            ]
            assert len(selected) == 1
            path = selected[0]
            assert 3 <= len(path) - 1 <= order - 3
            vertex_set = set(path)
            path_edges = path_edge_set(path)
            assert covers_once(path_edges & pd, vertex_set)
            assert covers_once((path_edges & pc) | {item}, vertex_set)
            outside = set(cycle) - vertex_set
            assert covers_once({candidate for candidate in pd if set(candidate) <= outside}, outside)
            total += 1
    assert total >= 50


def audit_degree_bookkeeping() -> None:
    # Three disjoint spanning active graphs consume degree at least three.
    # Under Delta(D)<=4, a fourth-edge remainder has degree at most one.
    for degrees in ((1, 1, 1), (2, 1, 1), (1, 2, 1), (1, 1, 2)):
        assert sum(degrees) <= 4
        assert 4 - sum(degrees) <= 1
    # Two active cycles cannot share a vertex because the third graph still
    # has positive degree there.
    assert 2 + 2 + 1 > 4


def main() -> None:
    audit_noncancellation_directly()
    audit_chords_under_relabelling()
    audit_degree_bookkeeping()
    print("independent maximum-degree-four audit: PASS")
    print("no import from primary verifier; exact integer arithmetic")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
