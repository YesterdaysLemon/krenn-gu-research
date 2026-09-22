"""Independent N=1 reconstruction of the state-C4 to cubic-H bridge."""

from collections import defaultdict
from itertools import product


COLORS = (0, 1, 2)
MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
LABELS = tuple((a, b) for a in COLORS for b in COLORS if a != b)


def all_matchings(vertices, edges):
    vertices = frozenset(vertices)
    incident = defaultdict(list)
    for edge in edges:
        u, v = edge
        incident[u].append(v)
        incident[v].append(u)

    def visit(free):
        if not free:
            yield ()
            return
        u = min(free, key=lambda x: (len([v for v in incident[x] if v in free]), repr(x)))
        for v in incident[u]:
            if v not in free:
                continue
            edge = tuple(sorted((u, v), key=repr))
            for tail in visit(free - {u, v}):
                yield (edge,) + tail

    yield from visit(vertices)


def allocation_gadgets():
    gadgets = []
    seen_states = set()
    for a, b in LABELS:
        left_others = sorted(c for c in COLORS if c != a)
        right_others = sorted(c for c in COLORS if c != b)
        left_pair = MATCHINGS[a][left_others.index(b)]
        right_local = MATCHINGS[b][right_others.index(a)]
        right_pair = tuple(4 + x for x in right_local)
        l1, l2 = left_pair
        r1, r2 = right_pair
        states = ((l1, a), (l2, a), (r1, b), (r2, b))
        assert not (seen_states & set(states))
        seen_states.update(states)
        # Protected edges l1-l2 and r1-r2; straight crossings l1-r1,l2-r2.
        P = ((l1, a), (r2, b))
        Q = ((l2, a), (r1, b))
        gadgets.append({"label": (a, b), "states": states, "P": P, "Q": Q})
    assert seen_states == {(v, c) for v in range(8) for c in COLORS}
    return gadgets


def build_H(gadgets):
    vertices = set(range(8))
    edges = set()
    edge_color = {}
    for index, gadget in enumerate(gadgets):
        p = ("P", index)
        q = ("Q", index)
        vertices.update((p, q))
        third = next(c for c in COLORS if c not in gadget["label"])
        internal = tuple(sorted((p, q), key=repr))
        edges.add(internal)
        edge_color[internal] = third
        for aux, states in ((p, gadget["P"]), (q, gadget["Q"])):
            for physical, color in states:
                edge = tuple(sorted((physical, aux), key=repr))
                edges.add(edge)
                edge_color[edge] = color
    degree = defaultdict(int)
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    assert set(vertices) == set(degree)
    assert set(degree.values()) == {3}
    for v in vertices:
        assert {edge_color[e] for e in edges if v in e} == set(COLORS)
    # Simple is automatic from the edge set; check triangle-free literally.
    neighbors = {v: set() for v in vertices}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    assert all(not (neighbors[u] & neighbors[v]) for u, v in edges)
    return vertices, edges, edge_color


def word_from_H_matching(matching, edge_color):
    word = [None] * 8
    for edge in matching:
        for endpoint in edge:
            if isinstance(endpoint, int):
                assert word[endpoint] is None
                word[endpoint] = edge_color[edge]
    assert all(c is not None for c in word)
    return tuple(word)


def scalar_support(gadgets):
    weights = {}
    for gadget in gadgets:
        (l1, a), (l2, _), (r1, b), (r2, _) = gadget["states"]
        weights[(min(l1, l2), max(l1, l2), a, a)] = 1
        weights[(min(r1, r2), max(r1, r2), b, b)] = 1
        weights[(l1, r1, a, b)] = 1
        weights[(l2, r2, a, b)] = -1
    assert len(weights) == 24
    return weights


def physical_coefficient(word, weights):
    geometric = {(u, v) for u, v, _, _ in weights}
    terms = []
    for matching in all_matchings(range(8), geometric):
        value = 1
        for u, v in matching:
            factor = weights.get((u, v, word[u], word[v]))
            if factor is None:
                break
            value *= factor
        else:
            terms.append(value)
    return sum(terms), tuple(terms)


def main():
    gadgets = allocation_gadgets()
    vertices, edges, edge_color = build_H(gadgets)
    h_matchings = tuple(all_matchings(vertices, edges))
    words = tuple(word_from_H_matching(m, edge_color) for m in h_matchings)
    assert len(set(words)) == len(words)
    pure = {(c,) * 8 for c in COLORS}
    assert pure <= set(words)
    assert len(words) >= 4

    weights = scalar_support(gadgets)
    nonzero = {}
    for word in product(COLORS, repeat=8):
        coefficient, terms = physical_coefficient(word, weights)
        if coefficient:
            nonzero[word] = (coefficient, terms)
            assert len(terms) == 1
    assert set(nonzero) == set(words)
    assert all(nonzero[word] == (1, (1,)) for word in pure)
    assert set(words) - pure

    print(f"state_gadgets={len(gadgets)} H_vertices={len(vertices)} H_edges={len(edges)}")
    print(f"H_perfect_matchings={len(h_matchings)} nonzero_words={len(nonzero)}")
    print(f"mixed_unique_words={len(set(words)-pure)}")
    print("proper_3_edge_coloring=PASS simple=PASS triangle_free=PASS")
    print("pm_word_bijection_and_coefficients=PASS")
    print("N1_CUBIC_BRIDGE_RECONSTRUCTION_PASS")


if __name__ == "__main__":
    main()
