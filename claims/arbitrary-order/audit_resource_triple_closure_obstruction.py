"""Replay the exact resource-triple obstruction to naive cycle balance."""

V = tuple(range(4))
PROTECTED = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 2), (1, 3)),
}
CROSSINGS = (
    (1, 0, 2, 1),
    (0, 0, 3, 2),
    (0, 1, 1, 2),
    (3, 0, 1, 1),
    (2, 0, 0, 2),
    (3, 1, 2, 2),
)
BLOCKS = (
    ((0, (0, 1)), (1, (0, 2)), (2, (1, 3))),
    ((0, (2, 3)), (1, (1, 3)), (2, (0, 2))),
)


def physical_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in physical_matchings(rest):
            yield ((u, v),) + tail


def compatible_edges(word):
    edges = set()
    for color, pm in PROTECTED.items():
        for u, v in pm:
            if word[u] == word[v] == color:
                edges.add(tuple(sorted((u, v))))
    for u, a, v, b in CROSSINGS:
        if word[u] == a and word[v] == b:
            edges.add(tuple(sorted((u, v))))
    return edges


def main():
    states = {(v, c) for v in V for c in range(3)}
    block_states = []
    for block in BLOCKS:
        local = {(v, color) for color, edge in block for v in edge}
        assert len(local) == 6
        block_states.append(local)
    assert block_states[0].isdisjoint(block_states[1])
    assert block_states[0] | block_states[1] == states

    degree = {state: 0 for state in states}
    for u, a, v, b in CROSSINGS:
        assert u != v
        degree[(u, a)] += 1
        degree[(v, b)] += 1
        assert any((u, a) in local and (v, b) in local
                   for local in block_states)
    assert set(degree.values()) == {1}

    mate0 = {}
    for u, v in PROTECTED[0]:
        mate0[u] = v
        mate0[v] = u
    arcs = {}
    for u in V:
        source = (mate0[u], 0)
        choices = [(v, b) for x, a, v, b in CROSSINGS
                   if (x, a) == source]
        choices += [(x, a) for x, a, v, b in CROSSINGS
                    if (v, b) == source]
        assert len(choices) == 1
        arcs[u] = choices[0]
    assert {u: v for u, (v, _) in arcs.items()} == {0: 2, 2: 1, 1: 3, 3: 0}

    cycle = (0, 2, 1, 3)
    word = [0] * 4
    for u in cycle:
        v, label = arcs[u]
        word[v] = label
    assert tuple(word) == (2, 1, 1, 2)

    edges = compatible_edges(word)
    count = sum(all(tuple(sorted(edge)) in edges for edge in pm)
                for pm in physical_matchings(V))
    assert count == 0
    print("TRIPLE_BLOCK_BALANCE_OBSTRUCTION_PASS "
          f"word={''.join(map(str, word))} matching_count={count}")


if __name__ == "__main__":
    main()
