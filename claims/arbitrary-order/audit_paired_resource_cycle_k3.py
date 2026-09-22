"""Independent nonbipartite k=3 replay of the paired-block cycle proof."""

from collections import defaultdict


M = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def resource(component, color, index):
    return (component, color, index,
            tuple(4 * component + p for p in M[color][index]))


def paired_resources(k=3):
    """Three color-pair layers on the directed component k-cycle."""
    pairs = []
    for i in range(k):
        j = (i + 1) % k
        pairs.append((resource(i, 0, 0), resource(j, 1, 0)))
        pairs.append((resource(i, 1, 1), resource(j, 2, 0)))
        pairs.append((resource(i, 2, 1), resource(j, 0, 1)))
    flat = [r[:3] for pair in pairs for r in pair]
    assert len(flat) == len(set(flat)) == 6 * k
    assert all(x[0] != y[0] and x[1] != y[1] for x, y in pairs)
    return pairs


DIAG = {(0, 0), (1, 1)}
ANTI = {(0, 1), (1, 0)}
FULL = {(i, j) for i in range(2) for j in range(2)}
THREE = [FULL - {missing} for missing in sorted(FULL)]


def build(patterns):
    pairs = paired_resources()
    protected = []
    for component in range(3):
        for color in range(3):
            for u, v in M[color]:
                protected.append((4 * component + u, 4 * component + v,
                                  color, color))
    crossings = []
    for gid, ((left, right), support) in enumerate(zip(pairs, patterns)):
        for i, j in support:
            crossings.append((left[3][i], right[3][j], left[1], right[1], gid))
    return pairs, protected, crossings


def directed_cycle(base, pairs, crossings):
    mate = {}
    owner = {}
    for rid, r in enumerate(x for pair in pairs for x in pair):
        u, v = r[3]
        mate[(u, r[1])] = v
        mate[(v, r[1])] = u
        owner[r[:3]] = rid

    incident = defaultdict(list)
    for u, v, a, b, _ in crossings:
        incident[(u, a)].append((v, b))
        incident[(v, b)].append((u, a))

    # Select the lexicographically first outgoing arc at each vertex.  A
    # functional digraph has a directed cycle, found by the standard walk.
    successor = {}
    for u in range(12):
        options = sorted(incident[(mate[(u, base)], base)])
        assert options
        successor[u] = options[0]

    seen_at = {}
    walk = []
    u = 0
    while u not in seen_at:
        seen_at[u] = len(walk)
        walk.append(u)
        u = successor[u][0]
    cycle = walk[seen_at[u]:]
    assert cycle and successor[cycle[-1]][0] == cycle[0]
    return cycle, successor


def count_matchings(word, protected, crossings):
    adjacency = [[] for _ in word]
    for u, v, a, b in protected:
        if word[u] == a and word[v] == b:
            adjacency[u].append(v)
            adjacency[v].append(u)
    for u, v, a, b, _ in crossings:
        if word[u] == a and word[v] == b:
            adjacency[u].append(v)
            adjacency[v].append(u)

    def rec(mask):
        if not mask:
            return 1
        u = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << u)
        return sum(rec(rest ^ (1 << v)) for v in adjacency[u]
                   if rest & (1 << v))

    return rec((1 << len(word)) - 1)


def run(patterns):
    pairs, protected, crossings = build(patterns)
    for base in range(3):
        cycle, successor = directed_cycle(base, pairs, crossings)
        word = [base] * 12
        for u in cycle:
            v, foreign = successor[u]
            word[v] = foreign
        assert len(set(word)) > 1
        assert count_matchings(word, protected, crossings) == 1


def main():
    suites = []
    suites.append([FULL] * 9)
    suites.append([THREE[i % 4] for i in range(9)])
    suites.append([THREE[(i + 2) % 4] for i in range(9)])
    suites.append([DIAG, FULL, THREE[0], ANTI, THREE[1], FULL,
                   THREE[2], DIAG, THREE[3]])
    suites.append([ANTI, THREE[3], FULL, THREE[2], DIAG, THREE[1],
                   FULL, THREE[0], ANTI])
    for patterns in suites:
        run(patterns)
    print("PAIRED_BLOCK_K3_NONBIPARTITE_AUDIT_PASS",
          {"suites": len(suites), "base_color_cases": 3 * len(suites),
           "simultaneously_dense_suites": 3})


if __name__ == "__main__":
    main()
