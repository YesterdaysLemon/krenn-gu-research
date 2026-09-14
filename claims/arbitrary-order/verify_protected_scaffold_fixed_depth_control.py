"""Exact finite controls for the protected-scaffold fixed-depth no-go theorem.

Checks the explicit n=248 base array, its literal source amplitudes on
selected words, and small word-ball permutation constructions. The written
proof, not this finite replay, owns all minority words and arbitrary depth.

Uses only the standard library. Prints JSON and writes no files.
"""

import itertools
import json
from collections import Counter, deque
from functools import lru_cache


LABELS = tuple(itertools.permutations(range(3), 2))
SHIFTS = (0, 1, 3, 8, 12, 18)
POSITIONS = (
    ((2, 3), (3, 1)),
    ((0, 3), (1, 0)),
    ((1, 1), (3, 0)),
    ((0, 2), (2, 1)),
    ((1, 3), (2, 2)),
    ((0, 0), (3, 2)),
)
PAIR_WEIGHTS = (1, -1)
FAILURE_L = "0100100100100100101001002000000"
FAILURE_R = "0000120100100100100201001000000"
MATCHINGS = (
    (frozenset((0, 1)), frozenset((2, 3))),
    (frozenset((0, 2)), frozenset((1, 3))),
    (frozenset((0, 3)), frozenset((1, 2))),
)


def component_edges():
    return [
        (i, 31 + (i + shift) % 31, label)
        for label, shift in enumerate(SHIFTS)
        for i in range(31)
    ]


def girth(edges):
    adjacency = [[] for _ in range(62)]
    for u, v, _ in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    shortest = 63
    for start in range(62):
        distances = {start: 0}
        parents = {start: None}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if v not in distances:
                    distances[v] = distances[u] + 1
                    parents[v] = u
                    queue.append(v)
                elif parents[u] != v:
                    shortest = min(shortest, distances[u] + distances[v] + 1)
    return shortest


def literal_entries(edges):
    """Build every nonzero physical edge entry, including its color labels."""
    entries = {}
    for block in range(62):
        for c, matching in enumerate(MATCHINGS):
            for pair in matching:
                u, v = sorted(pair)
                entries[(4 * block + u, 4 * block + v, c, c)] = 1
    for left, right, label in edges:
        c, d = LABELS[label]
        for (u, v), value in zip(POSITIONS[label], PAIR_WEIGHTS):
            key = (4 * left + u, 4 * right + v, c, d)
            assert key not in entries
            entries[key] = value
    return entries


def full_source(word, entries):
    """Exact matching sum, factoring connected scalar support components."""
    adjacency = [dict() for _ in word]
    for (u, v, a, b), value in entries.items():
        if (word[u], word[v]) == (a, b):
            adjacency[u][v] = value
            adjacency[v][u] = value

    @lru_cache(maxsize=None)
    def matchings(vertices):
        if not vertices:
            return 1
        u, *rest = vertices
        return sum(
            adjacency[u][v] * matchings(tuple(rest[:j] + rest[j + 1 :]))
            for j, v in enumerate(rest)
            if v in adjacency[u]
        )

    remaining = set(range(len(word)))
    total = 1
    while remaining:
        component = {min(remaining)}
        queue = list(component)
        for u in queue:
            for v in adjacency[u]:
                if v not in component:
                    component.add(v)
                    queue.append(v)
        remaining -= component
        total *= matchings(tuple(sorted(component)))
    return total


def word_ball_control(radius):
    words = [()]
    level = [()]
    for _ in range(radius):
        level = [w + (a,) for w in level for a in range(6) if not w or w[-1] != a]
        words.extend(level)
    indices = {w: i for i, w in enumerate(words)}
    permutations = []
    for a in range(6):
        permutation = []
        for w in words:
            if w and w[0] == a:
                image = w[1:]
            elif len(w) < radius:
                image = (a,) + w
            else:
                image = w
            permutation.append(indices[image])
        assert sorted(permutation) == list(range(len(words)))
        assert all(permutation[permutation[i]] == i for i in range(len(words)))
        permutations.append(permutation)
    for w in words[1:]:
        current = indices[()]
        for a in reversed(w):
            current = permutations[a][current]
        assert words[current] == w
    return {
        "radius": radius,
        "word_ball_size": len(words),
        "nonidentity_reduced_products_checked": len(words) - 1,
    }


def verify():
    edges = component_edges()
    assert len(edges) == 186
    assert len({(u, v) for u, v, _ in edges}) == 186
    assert all(u < 31 <= v for u, v, _ in edges)
    incident_labels = [[] for _ in range(62)]
    for u, v, label in edges:
        incident_labels[u].append(label)
        incident_labels[v].append(label)
    assert all(sorted(labels) == list(range(6)) for labels in incident_labels)
    differences = Counter((a - b) % 31 for a in SHIFTS for b in SHIFTS if a != b)
    assert differences == {i: 1 for i in range(1, 31)}
    assert girth(edges) == 6

    for label, (c, d) in enumerate(LABELS):
        assert frozenset(u for u, _ in POSITIONS[label]) in MATCHINGS[c]
        assert frozenset(v for _, v in POSITIONS[label]) in MATCHINGS[d]
        assert PAIR_WEIGHTS[0] * PAIR_WEIGHTS[1] == -1
    for color in range(3):
        row_pairs = [
            frozenset(u for u, _ in POSITIONS[label])
            for label, (c, _) in enumerate(LABELS)
            if c == color
        ]
        column_pairs = [
            frozenset(v for _, v in POSITIONS[label])
            for label, (_, d) in enumerate(LABELS)
            if d == color
        ]
        assert set(row_pairs) == set(MATCHINGS[color])
        assert set(column_pairs) == set(MATCHINGS[color])

    entries = literal_entries(edges)
    assert len(entries) == 744
    assert all(a == b for u, v, a, b in entries if u // 4 == v // 4)
    assert all(a != b for u, v, a, b in entries if u // 4 != v // 4)
    pure_values = [full_source([c] * 248, entries) for c in range(3)]
    assert pure_values == [1, 1, 1]

    single_minor_component_checks = 0
    for c, d in LABELS:
        for block in range(62):
            word = [c] * 248
            word[4 * block : 4 * block + 4] = [d] * 4
            assert full_source(word, entries) == 0
            single_minor_component_checks += 1

    assert len(FAILURE_L) == len(FAILURE_R) == 31
    colors = list(map(int, FAILURE_L + FAILURE_R))
    assert len(set(colors)) > 1
    available = [
        (u, v, label)
        for u, v, label in edges
        if (colors[u], colors[v]) == LABELS[label]
    ]
    assert available == []
    word = [c for c in colors for _ in range(4)]
    failure_value = full_source(word, entries)
    assert failure_value == 1

    return {
        "status": "verified_exact_finite_controls",
        "scope": "n248 base control and finite word balls; arbitrary-depth statement uses written proof",
        "component_vertices": 62,
        "physical_vertices": 248,
        "component_edges": len(edges),
        "component_graph_girth": 6,
        "nonzero_physical_entries": len(entries),
        "pure_amplitudes": pure_values,
        "single_minor_component_words_checked": single_minor_component_checks,
        "exhaustive_minorities_up_to_four_word_check": False,
        "failure_component_colors_L": FAILURE_L,
        "failure_component_colors_R": FAILURE_R,
        "failure_available_gadgets": len(available),
        "failure_full_source": failure_value,
        "failure_target": 0,
        "word_ball_controls": [word_ball_control(r) for r in (1, 2, 3)],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
