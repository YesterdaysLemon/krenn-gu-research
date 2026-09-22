"""Independent no-import audit of the k=3 closure-free cycle obstruction."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path


FIXTURE = Path(__file__).with_name("resource_triple_bad_exit_control.json")


def edge_key(left, right):
    return tuple(sorted((tuple(left), tuple(right))))


def canonical_cycle(cycle):
    cycle = tuple(cycle)
    return min(cycle[i:] + cycle[:i] for i in range(len(cycle)))


def all_functional_cycles(successor):
    """Enumerate every directed simple cycle, independent of traversal order."""
    found = set()
    for start in sorted(successor):
        path = []
        at = {}
        u = start
        while u not in at:
            at[u] = len(path)
            path.append(u)
            u = successor[u]
        cyc = tuple(path[at[u] :])
        found.add(canonical_cycle(cyc))
    return tuple(sorted(found))


def matching_count(word, incident):
    """Count colored scalar-edge perfect-matching terms for one physical word."""
    remaining = frozenset(range(len(word)))

    def rec(vertices):
        if not vertices:
            return 1
        u = min(vertices)
        total = 0
        for v, cu, cv in incident[u]:
            if v in vertices and word[u] == cu and word[v] == cv:
                total += rec(vertices - {u, v})
        return total

    return rec(remaining)


def enumerate_terms(n, incident):
    words = Counter()

    def rec(vertices, colors):
        if not vertices:
            words[tuple(colors)] += 1
            return
        u = min(vertices)
        for v, cu, cv in incident[u]:
            if v not in vertices:
                continue
            next_colors = list(colors)
            next_colors[u] = cu
            next_colors[v] = cv
            rec(vertices - {u, v}, next_colors)

    rec(frozenset(range(n)), [-1] * n)
    return words


def main():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    blocks = data["blocks"]
    n = 12

    resources = []
    crossings = []
    state_block = {}
    resource_block = {}
    crossing_block = {}
    for block_id, block in enumerate(blocks):
        assert sorted(color for color, _ in block["resources"]) == [0, 1, 2]
        local_states = []
        for color, endpoints in block["resources"]:
            endpoints = tuple(endpoints)
            assert len(endpoints) == 2 and endpoints[0] != endpoints[1]
            resource = (color, endpoints)
            resources.append(resource)
            resource_block[(color, frozenset(endpoints))] = block_id
            for vertex in endpoints:
                state = (vertex, color)
                assert state not in state_block
                state_block[state] = block_id
                local_states.append(state)
        seen_pairs = set()
        local_degree = Counter()
        for u, cu, v, cv in block["crossings"]:
            assert cu != cv
            assert u // 4 != v // 4
            assert u != v
            assert state_block[(u, cu)] == block_id == state_block[(v, cv)]
            key = edge_key((u, cu), (v, cv))
            assert key not in crossing_block
            crossing_block[key] = block_id
            crossings.append(((u, cu), (v, cv)))
            seen_pairs.add(frozenset((cu, cv)))
            local_degree[(u, cu)] += 1
            local_degree[(v, cv)] += 1
        assert seen_pairs == {frozenset((0, 1)), frozenset((0, 2)), frozenset((1, 2))}
        assert set(local_degree) == set(local_states)
        assert set(local_degree.values()) == {1}

    # The resource ledger is exactly the three protected K4 one-factorizations.
    expected = set()
    local_matchings = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    for offset in (0, 4, 8):
        for color, pairs in local_matchings.items():
            for u, v in pairs:
                expected.add((color, frozenset((offset + u, offset + v))))
    actual = {(color, frozenset(endpoints)) for color, endpoints in resources}
    assert actual == expected
    assert len(resources) == 18
    assert len(crossings) == 18
    assert set(state_block) == {(v, c) for v in range(n) for c in range(3)}

    mate = {c: {} for c in range(3)}
    for color, (u, v) in resources:
        mate[color][u] = v
        mate[color][v] = u

    scalar_edges = set()
    incident = defaultdict(list)
    for color, (u, v) in resources:
        scalar_edges.add(edge_key((u, color), (v, color)))
        incident[u].append((v, color, color))
        incident[v].append((u, color, color))
    for (u, cu), (v, cv) in crossings:
        scalar_edges.add(edge_key((u, cu), (v, cv)))
        incident[u].append((v, cu, cv))
        incident[v].append((u, cv, cu))

    cycle_receipt = {}
    expected_ledgers = {
        0: canonical_cycle((5, 11, 2, 10)),
        1: canonical_cycle((8, 6, 9, 4, 2)),
        2: canonical_cycle((9, 3, 5, 10, 4)),
    }
    for base in range(3):
        successor = {}
        target_state = {}
        for (u, cu), (v, cv) in crossings:
            if cu == base:
                source = mate[base][u]
                assert source not in successor
                successor[source] = v
                target_state[source] = (v, cv)
            if cv == base:
                source = mate[base][v]
                assert source not in successor
                successor[source] = u
                target_state[source] = (u, cu)
        assert set(successor) == set(range(n))
        cycles = all_functional_cycles(successor)
        assert cycles == (expected_ledgers[base],)

        for cycle in cycles:
            chosen = set(cycle)
            word = [base] * n
            for source in cycle:
                target, foreign = target_state[source]
                assert successor[source] == target
                word[target] = foreign

            double_hits = []
            for color, endpoints in resources:
                if color != base or not set(endpoints) <= chosen:
                    continue
                u, v = endpoints
                exits = (target_state[u], target_state[v])
                adjacent = edge_key(*exits) in scalar_edges
                double_hits.append((tuple(sorted(endpoints)), exits, adjacent))
            assert double_hits
            assert all(not adjacent for _, _, adjacent in double_hits)
            assert matching_count(tuple(word), incident) == 0
            assert len(set(word)) > 1
            cycle_receipt[base] = {
                "cycle": cycle,
                "word": tuple(word),
                "double_hits": tuple(double_hits),
            }

    terms = enumerate_terms(n, incident)
    total_terms = sum(terms.values())
    unique_mixed = sum(
        multiplicity == 1 and len(set(word)) > 1
        for word, multiplicity in terms.items()
    )
    assert total_terms == 364
    assert len(terms) == 342
    assert unique_mixed == 317
    assert terms[(0,) * 8 + (1,) * 4] == 1

    # Independently replay the degree-one block factorization on every macro
    # word of the fixture.  With unit edge weights, each saturated C6 block
    # doubles the term count and every unsaturated block is forced.
    macro_receipt = {}
    for phi in product(range(3), repeat=3):
        word = tuple(color for color in phi for _ in range(4))
        saturated = []
        for block_id, block in enumerate(blocks):
            selected = [
                word[endpoints[0]] == color
                for color, endpoints in block["resources"]
            ]
            if all(selected):
                saturated.append(block_id)
        direct = matching_count(word, incident)
        predicted = 2 ** len(saturated)
        assert direct == predicted
        macro_receipt[phi] = (tuple(saturated), direct)
    binary_mixed = tuple([0] * 8 + [1] * 4)
    assert macro_receipt[(0, 0, 1)] == ((), 1)
    assert matching_count(binary_mixed, incident) == 1

    print("INDEPENDENT_CLOSURE_NECESSITY_AUDIT_PASS")
    print("resources", len(resources), "crossings", len(crossings), "states", len(state_block))
    print("cycles", {a: receipt["cycle"] for a, receipt in cycle_receipt.items()})
    print("cycle_words", {a: receipt["word"] for a, receipt in cycle_receipt.items()})
    print("double_hits", {a: receipt["double_hits"] for a, receipt in cycle_receipt.items()})
    print("terms", total_terms, "words", len(terms), "unique_mixed", unique_mixed)
    print("macro_words", len(macro_receipt), "binary_witness", binary_mixed)


if __name__ == "__main__":
    main()
