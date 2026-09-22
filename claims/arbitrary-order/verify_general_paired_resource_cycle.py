"""Exact four-vertex replay of the abstract three-matching cycle theorem."""

from itertools import product


PMS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def resource_pairings(resources):
    """All perfect pairings of six resources, never pairing equal colors."""
    def rec(left, pairs):
        if not left:
            yield tuple(pairs)
            return
        i = left[0]
        for pos in range(1, len(left)):
            j = left[pos]
            if resources[i][0] == resources[j][0]:
                continue
            rest = left[1:pos] + left[pos + 1:]
            yield from rec(rest, pairs + [(i, j)])
    yield from rec(tuple(range(6)), [])


def block_supports(e, f):
    allowed = [(i, j) for i in range(2) for j in range(2)
               if e[i] != f[j]]
    for bits in range(1, 1 << len(allowed)):
        support = {allowed[t] for t in range(len(allowed)) if bits >> t & 1}
        if ({(0, 0), (1, 1)} <= support or
                {(0, 1), (1, 0)} <= support):
            yield support


def find_cycle(arcs):
    n = len(arcs)
    for start in range(n):
        stack = [(start, [start], {start})]
        while stack:
            u, path, seen = stack.pop()
            for v, _ in arcs[u]:
                if v == start:
                    return tuple(path)
                if v not in seen:
                    stack.append((v, path + [v], seen | {v}))
    raise AssertionError("minimum outdegree one but no directed cycle")


def count_physical_matchings(word, protected, crossings):
    edges = set()
    for color, pm in enumerate(protected):
        for u, v in pm:
            if word[u] == word[v] == color:
                edges.add(tuple(sorted((u, v))))
    for u, a, v, b in crossings:
        if word[u] == a and word[v] == b:
            edges.add(tuple(sorted((u, v))))
    return sum(all(tuple(sorted(edge)) in edges for edge in pm) for pm in PMS)


def replay(protected, pairing, supports):
    resources = [(color, edge)
                 for color, pm in enumerate(protected) for edge in pm]
    paired = {}
    crossings = []
    for (ri, rj), support in zip(pairing, supports):
        a, e = resources[ri]
        b, f = resources[rj]
        paired[ri] = (rj, support, False)
        paired[rj] = (ri, support, True)
        for i, j in support:
            crossings.append((e[i], a, f[j], b))

    loop_cycles = 0
    for base in range(3):
        state_resource = {}
        mate = {}
        for rid, (color, edge) in enumerate(resources):
            u, v = edge
            state_resource[(u, color)] = rid
            state_resource[(v, color)] = rid
            mate[(u, color)] = v
            mate[(v, color)] = u

        arcs = [[] for _ in range(4)]
        for u in range(4):
            um = mate[(u, base)]
            rid = state_resource[(u, base)]
            other, support, reversed_shores = paired[rid]
            foreign_color, foreign_edge = resources[other]
            base_edge = resources[rid][1]
            i = base_edge.index(um)
            if not reversed_shores:
                js = [j for ii, j in support if ii == i]
            else:
                js = [ii for ii, j in support if j == i]
            for j in js:
                arcs[u].append((foreign_edge[j], foreign_color))
            assert arcs[u]

        cycle = find_cycle(arcs)
        loop_cycles += len(cycle) == 1
        word = [base] * 4
        for pos, u in enumerate(cycle):
            v = cycle[(pos + 1) % len(cycle)]
            labels = {color for target, color in arcs[u] if target == v}
            assert len(labels) == 1
            word[v] = labels.pop()
        assert len(set(word)) > 1
        assert count_physical_matchings(word, protected, crossings) == 1
    return loop_cycles


def main():
    cases = 0
    loop_words = 0
    overlap_pairs = 0
    for protected in product(PMS, repeat=3):
        resources = [(color, edge)
                     for color, pm in enumerate(protected) for edge in pm]
        for pairing in resource_pairings(resources):
            choices = []
            for ri, rj in pairing:
                choices.append(tuple(block_supports(resources[ri][1],
                                                     resources[rj][1])))
                if resources[ri][1] == resources[rj][1]:
                    overlap_pairs += 1
            for supports in product(*choices):
                loop_words += replay(protected, pairing, supports)
                cases += 1
    print(f"GENERAL_THREE_MATCHING_CYCLE_PASS cases={cases} "
          f"loop_words={loop_words} "
          f"overlap_pair_observations={overlap_pairs}")


if __name__ == "__main__":
    main()
