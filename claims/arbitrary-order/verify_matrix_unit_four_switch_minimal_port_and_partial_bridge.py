"""Exact focused checks for the matrix-unit four-switch theorem.

The arbitrary-order proof is the written matching argument.  This script only
audits endpoint orientation, small coefficient ledgers, and the two displayed
countermechanisms.
"""

from __future__ import annotations

from itertools import product

EdgeData = tuple[int, int, int]


def matchings(vertices: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not vertices:
        return [()]
    u = vertices[0]
    out: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            out.append(((u, v),) + tail)
    return out


def edge_key(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def oriented(data: dict[tuple[int, int], EdgeData], u: int, v: int) -> EdgeData:
    a, b, weight = data[edge_key(u, v)]
    return (a, b, weight) if u < v else (b, a, weight)


def coefficient(
    data: dict[tuple[int, int], EdgeData], word: tuple[int, ...]
) -> tuple[int, list[tuple[tuple[int, int], ...]]]:
    total = 0
    active: list[tuple[tuple[int, int], ...]] = []
    for matching in matchings(tuple(range(len(word)))):
        weight = 1
        for u, v in matching:
            a, b, edge_weight = oriented(data, u, v)
            if word[u] != a or word[v] != b:
                weight = 0
                break
            weight *= edge_weight
        if weight:
            total += weight
            active.append(matching)
    return total, active


def complete_table(n: int, entries: dict[tuple[int, int], EdgeData]) -> None:
    assert len(entries) == n * (n - 1) // 2
    assert all(weight != 0 for _, _, weight in entries.values())


def gadget_eight() -> dict[tuple[int, int], EdgeData]:
    data: dict[tuple[int, int], EdgeData] = {}

    def put(edges: list[tuple[int, int]], labels: tuple[int, int], weight: int = 1) -> None:
        for u, v in edges:
            assert u < v and (u, v) not in data
            data[(u, v)] = (labels[0], labels[1], weight)

    put([(0, 1), (2, 3), (4, 5), (6, 7), (1, 2), (1, 3)], (0, 0))
    put([(0, 2)], (1, 0))
    put([(0, 3)], (1, 0), -1)
    put([(0, 4), (1, 5), (2, 6), (3, 7)], (1, 1))
    put([(0, 5), (1, 6), (2, 7), (3, 4)], (2, 2))
    put([(1, 4), (2, 5)], (2, 0))
    put([(2, 4)], (0, 1))
    put([(3, 5)], (0, 2))
    for u in range(8):
        for v in range(u + 1, 8):
            data.setdefault((u, v), (1, 2, 1))
    complete_table(8, data)
    return data


def gadget_six() -> dict[tuple[int, int], EdgeData]:
    data: dict[tuple[int, int], EdgeData] = {}

    def put(edges: list[tuple[int, int]], labels: tuple[int, int], weights: list[int] | None = None) -> None:
        if weights is None:
            weights = [1] * len(edges)
        for (u, v), weight in zip(edges, weights, strict=True):
            assert u < v and (u, v) not in data
            data[(u, v)] = (labels[0], labels[1], weight)

    put([(0, 5), (1, 2), (3, 4)], (0, 0))
    put([(0, 1), (0, 3)], (1, 0))
    put([(2, 5), (4, 5)], (0, 2), [1, -1])
    put([(1, 3), (0, 4), (1, 5), (2, 3)], (1, 1))
    put([(2, 4), (0, 2), (1, 4), (3, 5)], (2, 2))
    complete_table(6, data)
    return data


def check_eight() -> None:
    data = gadget_eight()
    for colour in range(3):
        value, active = coefficient(data, (colour,) * 8)
        assert value == 1 and len(active) == 1

    for base in range(3):
        for exceptional in range(3):
            for vertex in range(8):
                word = [base] * 8
                word[vertex] = exceptional
                value, _ = coefficient(data, tuple(word))
                assert value == (1 if base == exceptional else 0)

    for first in range(3):
        for second in range(3):
            if first == second:
                continue
            for p in range(8):
                for q in range(p + 1, 8):
                    word = [second] * 8
                    word[p] = word[q] = first
                    value, _ = coefficient(data, tuple(word))
                    assert value == 0

    value, active = coefficient(data, (1, 0, 0, 0, 0, 0, 0, 0))
    assert value == 0
    assert set(active) == {
        ((0, 2), (1, 3), (4, 5), (6, 7)),
        ((0, 3), (1, 2), (4, 5), (6, 7)),
    }

    nonzero_mixed = 0
    for word in product(range(3), repeat=8):
        value, _ = coefficient(data, word)
        if value and len(set(word)) > 1:
            nonzero_mixed += 1
    assert nonzero_mixed == 79


def nonrigidity_sets(data: dict[tuple[int, int], EdgeData], n: int) -> list[set[int]]:
    result = [set() for _ in range(3)]
    for (u, v), (a, b, _) in data.items():
        if a != b:
            result[b].add(u)
            result[a].add(v)
    return result


def check_six() -> None:
    data = gadget_six()
    assert nonrigidity_sets(data, 6) == [{0, 5}, {1, 3}, {2, 4}]
    for colour in range(3):
        value, _ = coefficient(data, (colour,) * 6)
        assert value == 1

    sets = [{0, 5}, {1, 3}, {2, 4}]
    off_target_active_counts = []
    for colour, boundary in enumerate(sets):
        p, q = sorted(boundary)
        for a, b in product(range(3), repeat=2):
            word = [colour] * 6
            word[p], word[q] = a, b
            value, active = coefficient(data, tuple(word))
            assert value == (1 if (a, b) == (colour, colour) else 0)
            if (a, b) != (colour, colour) and active:
                off_target_active_counts.append(len(active))
    assert off_target_active_counts == [2]

    nonzero_mixed = 0
    for word in product(range(3), repeat=6):
        value, _ = coefficient(data, word)
        if value and len(set(word)) > 1:
            nonzero_mixed += 1
    assert nonzero_mixed == 10


def check_four_switch_ledger() -> None:
    # The mate involution has four distinct endpoints off the matching, and
    # minimum k=4 or k=3 leaves exactly the stated delta-pair types.
    matching = {(0, 1), (2, 3), (4, 5), (6, 7)}
    mate = {u: v for u, v in matching for u, v in ((u, v), (v, u))}
    for u in range(8):
        for v in range(u + 1, 8):
            if edge_key(u, v) in matching:
                continue
            up, vp = mate[u], mate[v]
            assert len({u, v, up, vp}) == 4
            assert edge_key(mate[up], mate[vp]) == edge_key(u, v)

    pairs = {(x, y) for x in range(3) for y in range(3)}
    assert {tuple(sorted(pair)) for pair in pairs if sum(pair) in {0, 4}} == {
        (0, 0),
        (2, 2),
    }
    assert {tuple(sorted(pair)) for pair in pairs if sum(pair) in {0, 3, 4}} == {
        (0, 0),
        (1, 2),
        (2, 2),
    }


def main() -> None:
    check_four_switch_ledger()
    check_eight()
    check_six()
    print("matrix-unit four-switch/minimal-port focused checks: PASS")
    print("scope: exact finite convention checks; arbitrary-order proof is written")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
