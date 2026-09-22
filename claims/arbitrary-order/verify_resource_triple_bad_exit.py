"""Standalone literal replay of the k=3 bad-exit cycle control."""

from collections import defaultdict
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "resource_triple_bad_exit_control.json").read_text())
V = tuple(range(12))
LOCAL = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
PROTECTED = {
    c: tuple((u + 4 * k, v + 4 * k) for k in range(3) for u, v in LOCAL[c])
    for c in range(3)
}


def sedge(x, y):
    return tuple(sorted((tuple(x), tuple(y))))


def physical_matchings(rem=V):
    if not rem:
        yield ()
        return
    u = rem[0]
    for i in range(1, len(rem)):
        v = rem[i]
        for tail in physical_matchings(rem[1:i] + rem[i + 1:]):
            yield ((u, v),) + tail


def functional_cycles(mapping):
    cycles = []
    finished = set()
    for start in V:
        path, position = [], {}
        u = start
        while u not in position and u not in finished:
            position[u] = len(path)
            path.append(u)
            finished.add(u)
            u = mapping[u][0]
        if u in position:
            cycles.append(tuple(path[position[u]:]))
    return tuple(cycles)


def matching_word_counts(entries):
    by_pair = defaultdict(list)
    for (u, a), (v, b) in entries:
        by_pair[tuple(sorted((u, v)))].append((u, a, v, b))
    counts = defaultdict(int)
    for pm in physical_matchings():
        options = [by_pair[tuple(sorted(edge))] for edge in pm]
        if any(not choices for choices in options):
            continue
        for chosen in product(*options):
            word = [-1] * len(V)
            for u, a, v, b in chosen:
                assert word[u] in (-1, a) and word[v] in (-1, b)
                word[u], word[v] = a, b
            counts[tuple(word)] += 1
    return counts


def main():
    blocks = DATA["blocks"]
    all_resources, all_crossings = [], []
    block_states = []
    for block in blocks:
        resources = [(c, tuple(edge)) for c, edge in block["resources"]]
        assert {c for c, _ in resources} == {0, 1, 2}
        states = {(v, c) for c, edge in resources for v in edge}
        assert len(states) == 6
        block_states.append(states)
        all_resources.extend(resources)
        local_crossings = []
        for u, a, v, b in block["crossings"]:
            assert a != b and u != v and u // 4 != v // 4
            assert (u, a) in states and (v, b) in states
            local_crossings.append(sedge((u, a), (v, b)))
        assert len(set(local_crossings)) == 3
        all_crossings.extend(local_crossings)

    all_states = {(v, c) for v in V for c in range(3)}
    assert set().union(*block_states) == all_states
    assert sum(map(len, block_states)) == len(all_states)
    assert sorted(all_resources) == sorted(
        (c, edge) for c, pm in PROTECTED.items() for edge in pm
    )
    degree = {state: 0 for state in all_states}
    for x, y in all_crossings:
        degree[x] += 1
        degree[y] += 1
    assert set(degree.values()) == {1}

    entries = set(all_crossings)
    entries.update(
        sedge((u, c), (v, c))
        for c, pm in PROTECTED.items()
        for u, v in pm
    )

    cycle_receipt = {}
    for a in range(3):
        mate = {u: v for edge in PROTECTED[a] for u, v in (edge, edge[::-1])}
        mapping = {}
        for u in V:
            source = (mate[u], a)
            incident = [y if x == source else x for x, y in all_crossings
                        if x == source or y == source]
            assert len(incident) == 1
            target = incident[0]
            assert target[1] != a
            mapping[u] = target
        cycles = functional_cycles(mapping)
        for cycle in cycles:
            chosen = set(cycle)
            assert any(mate[u] in chosen for u in cycle)
            word = [a] * len(V)
            for u in cycle:
                v, b = mapping[u]
                word[v] = b
            # Every cycle-selected word is killed by a nonadjacent double exit.
            assert matching_word_counts(entries).get(tuple(word), 0) == 0
        cycle_receipt[a] = cycles

    counts = matching_word_counts(entries)
    unique_mixed = sorted(
        word for word, count in counts.items()
        if count == 1 and len(set(word)) > 1
    )
    assert unique_mixed  # This is a route obstruction, not a UPM support.
    print("K3_DEGREE1_BAD_EXIT_CONTROL_PASS")
    print("cycles", cycle_receipt)
    print("supported_terms", sum(counts.values()), "supported_words", len(counts))
    print("unique_mixed", len(unique_mixed), "first", "".join(map(str, unique_mixed[0])))


if __name__ == "__main__":
    main()
