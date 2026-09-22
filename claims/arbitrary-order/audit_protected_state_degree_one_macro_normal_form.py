"""Exact two-K4 long-cycle switch control for the macro-normal-form lemma."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product


COLORS = (0, 1, 2)
MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
LABELS = tuple((a, b) for a in COLORS for b in COLORS if a != b)


def protected_edges():
    result = []
    for base in (0, 4):
        for color in COLORS:
            for u, v in MATCHINGS[color]:
                result.append(((base + u, color), (base + v, color), "P"))
    return result


def initial_crossings():
    result = []
    by_label = {}
    for a, b in LABELS:
        ai = sorted(c for c in COLORS if c != a).index(b)
        bi = sorted(c for c in COLORS if c != b).index(a)
        au, av = MATCHINGS[a][ai]
        bu, bv = (4 + x for x in MATCHINGS[b][bi])
        edges = [((au, a), (bu, b), "X"), ((av, a), (bv, b), "X")]
        by_label[(a, b)] = len(result)
        result.extend(edges)
    return result, by_label


def switch_to_long_cycle(crossings, by_label):
    switched = list(crossings)
    i = by_label[(0, 1)]
    j = by_label[(0, 2)]
    s1, t1, _ = switched[i]
    s2, t2, _ = switched[j]
    assert s1[1] == s2[1] == 0 and t1[1] == 1 and t2[1] == 2
    switched[i] = (s1, t2, "X")
    switched[j] = (s2, t1, "X")
    return switched


def state_component_sizes(edges):
    neighbors = defaultdict(set)
    for s, t, _ in edges:
        neighbors[s].add(t)
        neighbors[t].add(s)
    all_states = {(v, c) for v in range(8) for c in COLORS}
    assert set(neighbors) == all_states
    assert {len(neighbors[s]) for s in all_states} == {2}
    unseen = set(all_states)
    sizes = []
    while unseen:
        stack = [unseen.pop()]
        seen = set(stack)
        while stack:
            s = stack.pop()
            for t in neighbors[s]:
                if t not in seen:
                    seen.add(t)
                    unseen.remove(t)
                    stack.append(t)
        sizes.append(len(seen))
    return sorted(sizes)


def enumerate_physical_terms(edges):
    by_vertex = defaultdict(list)
    for index, (s, t, kind) in enumerate(edges):
        by_vertex[s[0]].append(index)
        by_vertex[t[0]].append(index)

    def visit(free, chosen):
        if not free:
            yield tuple(chosen)
            return
        u = min(free)
        for index in by_vertex[u]:
            s, t, _ = edges[index]
            v = t[0] if s[0] == u else s[0]
            if v not in free or v == u:
                continue
            yield from visit(free - {u, v}, chosen + [index])

    return tuple(visit(set(range(8)), []))


def word_of(term, edges):
    word = [None] * 8
    for index in term:
        s, t, _ = edges[index]
        for v, c in (s, t):
            assert word[v] is None
            word[v] = c
    return tuple(word)


def main():
    crossings, by_label = initial_crossings()
    crossings = switch_to_long_cycle(crossings, by_label)
    edges = protected_edges() + crossings

    crossing_states = [state for s, t, _ in crossings for state in (s, t)]
    assert len(crossing_states) == len(set(crossing_states)) == 24
    assert all(s[0] // 4 != t[0] // 4 and s[1] != t[1] for s, t, _ in crossings)
    sizes = state_component_sizes(edges)
    assert sizes == [4, 4, 4, 4, 8]

    terms = enumerate_physical_terms(edges)
    counts = Counter(word_of(term, edges) for term in terms)
    macros = {}
    for left, right in product(COLORS, repeat=2):
        word = (left,) * 4 + (right,) * 4
        macros[(left, right)] = counts[word]
        assert counts[word] >= 1
    assert macros[(0, 1)] == 1
    assert macros[(0, 2)] == 1

    print("state_component_sizes", sizes)
    print("singleton_macro_term_counts", macros)
    print("uncovered_singletons", [(0, 1), (0, 2)])
    print("LONG_CYCLE_MACRO_GAP_PASS")


if __name__ == "__main__":
    main()
