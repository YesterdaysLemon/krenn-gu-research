#!/usr/bin/env python3
"""Portable finite replay of the protected-pair cubic matching bridge.

This primary checker uses an abstract complete protected-edge pairing and
does not import project scientific code.  It checks both the literal two-K4
PSFD table and a three-K4 pairing whose component graph is a triangle.  The
first fixture has six parallel labelled component edges, so it is a local
correspondence check rather than a valid simple-layer WP1 instance.
"""

from collections import defaultdict
from itertools import product


COLORS = range(3)
PORTS = range(4)

# Protected K4 matchings, as unordered local-port pairs.
M = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}

# (left color, right color): two crossing entries in weight order +1,-1.
TABLE = {
    (0, 1): ((2, 3), (3, 1)),
    (0, 2): ((0, 3), (1, 0)),
    (1, 0): ((1, 1), (3, 0)),
    (1, 2): ((0, 2), (2, 1)),
    (2, 0): ((1, 3), (2, 2)),
    (2, 1): ((0, 0), (3, 2)),
}


def perfect_matchings(vertices):
    """Yield perfect matchings of a tuple as tuples of unordered pairs."""
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def scalar_entries(protected, gadgets, crossing_weights):
    """Build literal scalar entries, allowing several color entries per pair."""
    edges = defaultdict(list)

    def add(u, v, cu, cv, weight, tag):
        if u > v:
            u, v, cu, cv = v, u, cv, cu
        edges[(u, v)].append((cu, cv, weight, tag))

    for name, (c, u, v) in protected.items():
        add(u, v, c, c, 1, ("protected", name))
    for i, (name, edge_a, edge_b, ordered_a, ordered_b) in enumerate(gadgets):
        a = protected[edge_a][0]
        b = protected[edge_b][0]
        w0, w1 = crossing_weights[i]
        add(ordered_a[0], ordered_b[0], a, b, w0, ("crossing", i, name, 0))
        add(ordered_a[1], ordered_b[1], a, b, w1, ("crossing", i, name, 1))
    return edges


def direct_source(protected, gadgets, crossing_weights):
    edges = scalar_entries(protected, gadgets, crossing_weights)
    totals = defaultdict(int)
    terms = defaultdict(list)
    physical_vertices = sorted(
        {endpoint for _, u, v in protected.values() for endpoint in (u, v)}
    )
    pms = list(perfect_matchings(tuple(physical_vertices)))
    for pm in pms:
        if not all(tuple(sorted(e)) in edges for e in pm):
            continue
        choices = [edges[tuple(sorted(e))] for e in pm]
        for selected in product(*choices):
            word = [None] * len(physical_vertices)
            weight = 1
            tags = []
            valid = True
            for (u0, v0), (cu, cv, w, tag) in zip(pm, selected):
                u, v = sorted((u0, v0))
                if word[u] not in (None, cu) or word[v] not in (None, cv):
                    valid = False
                    break
                word[u], word[v] = cu, cv
                weight *= w
                tags.append(tag)
            if valid:
                word = tuple(word)
                totals[word] += weight
                terms[word].append((weight, tuple(tags)))
    return totals, terms, len(pms)


def abstract_pairing_fixture():
    """Translate the literal table into the abstract protected-edge pairing."""
    protected = {}
    edge_id = {}
    for shore in range(2):
        off = 4 * shore
        for c in COLORS:
            for pair_index, (x, y) in enumerate(M[c]):
                name = ("m", shore, c, pair_index)
                protected[name] = (c, off + x, off + y)
                edge_id[(shore, c, frozenset((x, y)))] = name

    gadgets = []
    for (a, b), entries in TABLE.items():
        (lx, ry), (lz, rw) = entries
        left = edge_id[(0, a, frozenset((lx, lz)))]
        right = edge_id[(1, b, frozenset((ry, rw)))]
        # The ordered endpoints also record the chosen crossing bijection.
        gadgets.append(((a, b), left, right, (lx, lz), (4 + ry, 4 + rw)))
    assert len({g[1] for g in gadgets} | {g[2] for g in gadgets}) == 12
    return protected, gadgets


def nonbipartite_triangle_fixture():
    """A complete pairing on three K4s whose component graph is a triangle."""
    protected = {}
    for component in range(3):
        off = 4 * component
        for c in COLORS:
            for pair_index, (x, y) in enumerate(M[c]):
                protected[(component, c, pair_index)] = (c, off + x, off + y)

    pairs = []
    # Three gadgets on each side of the component triangle.  Each component
    # uses both protected edges of every color exactly once overall.
    for c in COLORS:
        pairs.append(((0, c, 0), (1, (c + 1) % 3, 0)))
        pairs.append(((1, c, 1), (2, (c + 1) % 3, 0)))
        pairs.append(((2, c, 1), (0, (c + 1) % 3, 1)))

    gadgets = []
    for i, (edge_a, edge_b) in enumerate(pairs):
        _, au, av = protected[edge_a]
        _, bu, bv = protected[edge_b]
        gadgets.append((("triangle", i), edge_a, edge_b, (au, av), (bu, bv)))
    used = [edge for g in gadgets for edge in g[1:3]]
    assert len(used) == 18 and set(used) == set(protected)
    return protected, gadgets


def build_h(protected, gadgets):
    """Build H from an abstract complete pairing of protected colored edges."""
    # Physical vertices are 0..7. Aux vertices are strings to keep the proof
    # roles visible in receipts.
    adjacency = defaultdict(set)
    edge_data = {}
    state_spoke = {}

    def add_edge(u, v, kind, color, gadget):
        key = frozenset((u, v))
        assert len(key) == 2 and key not in edge_data
        adjacency[u].add(v)
        adjacency[v].add(u)
        edge_data[key] = (kind, color, gadget)

    used = []
    for gadget_index, (name, edge_a, edge_b, ordered_a, ordered_b) in enumerate(gadgets):
        a, au, av = protected[edge_a]
        b, bu, bv = protected[edge_b]
        assert a != b
        assert {au, av} == set(ordered_a)
        assert {bu, bv} == set(ordered_b)
        assert au // 4 != bu // 4  # fixture's hollow/different-component condition
        used.extend((edge_a, edge_b))
        g = (gadget_index, name)
        # With ordered endpoints (au,av), (bu,bv), crossings are au-bu and
        # av-bv.  The state-C4 bipartition is P={au,bv}, Q={av,bu}.
        p = ("P", gadget_index, name)
        q = ("Q", gadget_index, name)
        states_p = ((ordered_a[0], a), (ordered_b[1], b))
        states_q = ((ordered_a[1], a), (ordered_b[0], b))
        for u, c in states_p:
            add_edge(u, p, "spoke", c, g)
            assert (u, c) not in state_spoke
            state_spoke[(u, c)] = frozenset((u, p))
        for u, c in states_q:
            add_edge(u, q, "spoke", c, g)
            assert (u, c) not in state_spoke
            state_spoke[(u, c)] = frozenset((u, q))
        third = ({0, 1, 2} - {a, b}).pop()
        add_edge(p, q, "central", third, g)

    assert len(used) == len(protected) and set(used) == set(protected)
    assert len(used) == len(set(used))
    vertices = tuple(adjacency)
    physical_vertices = {
        endpoint
        for _, first, second in protected.values()
        for endpoint in (first, second)
    }
    assert len(vertices) == len(physical_vertices) + 2 * len(gadgets)
    assert len(edge_data) == 5 * len(gadgets)
    assert len(state_spoke) == 2 * len(protected)
    assert all(len(adjacency[v]) == 3 for v in vertices)
    # Proper edge coloring: each vertex sees colors {0,1,2}.
    assert all(
        {edge_data[frozenset((v, w))][1] for w in adjacency[v]} == {0, 1, 2}
        for v in vertices
    )
    # Simple and triangle-free.
    assert all(
        not (adjacency[u] & adjacency[v])
        for u in vertices
        for v in adjacency[u]
    )
    return vertices, adjacency, edge_data, state_spoke


def graph_perfect_matchings(vertices, adjacency):
    remaining = set(vertices)

    def rec(rem, chosen):
        if not rem:
            yield tuple(chosen)
            return
        u = min(rem, key=lambda x: (len(adjacency[x] & rem), repr(x)))
        for v in sorted(adjacency[u] & rem, key=repr):
            yield from rec(rem - {u, v}, chosen + [frozenset((u, v))])

    yield from rec(remaining, [])


def h_pm_to_word(pm, edge_data):
    physical_vertices = {
        v for edge in edge_data for v in edge if isinstance(v, int)
    }
    assert physical_vertices == set(range(len(physical_vertices)))
    word = [None] * len(physical_vertices)
    for edge in pm:
        kind, color, _ = edge_data[edge]
        if kind != "spoke":
            continue
        physical = next(v for v in edge if isinstance(v, int))
        assert word[physical] is None
        word[physical] = color
    assert all(c is not None for c in word)
    return tuple(word)


def q_vector(word, protected):
    return tuple(
        sum(
            1
            for edge_color, u, v in protected.values()
            if edge_color == c and word[u] != c and word[v] != c
        )
        for c in COLORS
    )


def audit_fixture(name, protected, gadgets, crossing_weights, expect_product_minus_one):
    totals, terms, complete_pm_count = direct_source(
        protected, gadgets, crossing_weights
    )
    vertices, adjacency, edge_data, _ = build_h(protected, gadgets)
    hpms = list(graph_perfect_matchings(vertices, adjacency))
    h_by_word = defaultdict(list)
    for pm in hpms:
        h_by_word[h_pm_to_word(pm, edge_data)].append(pm)

    # This is the weight-independent injection: an H matching selects no full
    # state C4, and its physical word has one and only one original term.
    assert all(len(pms) == 1 for pms in h_by_word.values())
    assert all(len(terms[word]) == 1 for word in h_by_word)
    assert all(totals[word] != 0 for word in h_by_word)

    nonzero = {word: coeff for word, coeff in totals.items() if coeff}
    if expect_product_minus_one:
        assert set(h_by_word) == set(nonzero)

    physical_count = 2 * len(protected) // 3
    pure = {(c,) * physical_count for c in COLORS}
    assert pure <= set(h_by_word)
    for c in COLORS:
        color_pm = {
            edge for edge, (_, color, _) in edge_data.items() if color == c
        }
        assert len(color_pm) * 2 == len(vertices)
        assert h_pm_to_word(tuple(color_pm), edge_data) == (c,) * physical_count
        assert any(set(pm) == color_pm for pm in hpms)

    mixed_words = set(h_by_word) - pure
    min_q_histogram = defaultdict(int)
    for word in mixed_words:
        min_q_histogram[min(q_vector(word, protected))] += 1

    return {
        "name": name,
        "physical_unlabelled_matchings": complete_pm_count,
        "supported_original_terms": sum(len(v) for v in terms.values()),
        "supported_original_words": len(terms),
        "cancelled_words": sum(1 for word in terms if totals[word] == 0),
        "H_vertices": len(vertices),
        "H_edges": sum(map(len, adjacency.values())) // 2,
        "H_perfect_matchings": len(hpms),
        "nonzero_source_words": len(nonzero),
        "mixed_H_words": len(mixed_words),
        "mixed_H_min_q_histogram": dict(sorted(min_q_histogram.items())),
    }


def main():
    protected, gadgets = abstract_pairing_fixture()
    receipt = audit_fixture(
        "literal_psfd_two_component",
        protected,
        gadgets,
        [(1, -1)] * len(gadgets),
        True,
    )
    for key, value in receipt.items():
        print(f"{key}={value}")

    protected2, gadgets2 = nonbipartite_triangle_fixture()
    receipt2 = audit_fixture(
        "nonbipartite_component_triangle",
        protected2,
        gadgets2,
        [(1, -1)] * len(gadgets2),
        True,
    )
    for key, value in receipt2.items():
        print(f"{key}={value}")

    # Weight sharpness: the H injection needs only nonzero crossing entries;
    # the converse from every nonzero word to H uses product -1.
    receipt3 = audit_fixture(
        "nonbipartite_arbitrary_nonzero_weights",
        protected2,
        gadgets2,
        [(i + 2, i + 3) for i in range(len(gadgets2))],
        False,
    )
    for key, value in receipt3.items():
        print(f"{key}={value}")
    print("PROTECTED_PAIR_CUBIC_BRIDGE_PASS")


if __name__ == "__main__":
    main()
