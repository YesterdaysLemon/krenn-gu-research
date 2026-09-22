"""Literal full-array replay of the two hidden-overlap witness words.

This imports no scientific implementation.  It constructs complete equality
gadget arrays with arbitrary exterior split/transit allocations and exact
rational nonzero lane weights.  The all-order proof is in the owning note;
this finite replay checks exterior isolation, matching multiplicity and q.
"""

from fractions import Fraction
from itertools import permutations, product


PAIRS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def literal_edges(k, colors):
    edges = set()
    for component in range(k):
        base = (
            ((component - 1) % k, 1, (component - 1) % k, 2),
            ((component - 1) % k, 2, (component + 1) % k, 0),
            ((component + 1) % k, 0, (component + 1) % k, 1),
        )
        for color, row in enumerate(base):
            source = (component, colors[color])
            for pos in (0, 2):
                target = (row[pos], colors[row[pos + 1]])
                edges.add(tuple(sorted((source, target))))
    assert len(edges) == 3 * k
    for component in range(k):
        for color in range(3):
            literal = (component, color)
            neighbors = [edge[1] if edge[0] == literal else edge[0]
                         for edge in edges if literal in edge]
            assert len(neighbors) == 2
            assert {x[1] for x in neighbors} == set(range(3)) - {color}
    return sorted(edges)


def build(k, colors, resources, orientation_bits):
    a, b, c = colors
    root, foreign = 0, k - 1
    f_edges = literal_edges(k, colors)
    choices = {}
    for index, (left, right) in enumerate(f_edges):
        # Exterior choices deliberately allow coincident and split resources.
        choices[(left, right)] = (index + left[0] + left[1]) % 2
        choices[(right, left)] = (index // 2 + right[0]) % 2
    root_literal = (root, a)
    b_literal, c_literal = (foreign, b), (foreign, c)
    for target in (b_literal, c_literal):
        choices[(root_literal, target)] = resources[0]
    choices[(b_literal, root_literal)] = resources[1]
    choices[(c_literal, root_literal)] = resources[2]

    scalar = []
    lane_maps = {}
    for component in range(k):
        for color in range(3):
            for u, v in PAIRS[color]:
                scalar.append((4 * component + u, 4 * component + v,
                               color, color, Fraction(1)))
    for index, (left, right) in enumerate(f_edges):
        lc, la = left
        rc, ra = right
        lp = PAIRS[la][choices[(left, right)]]
        rp = PAIRS[ra][choices[(right, left)]]
        flip = index % 2
        edge = {left, right}
        if edge == {root_literal, b_literal}:
            flip = orientation_bits[0]
        elif edge == {root_literal, c_literal}:
            flip = orientation_bits[1]
        if flip:
            rp = tuple(reversed(rp))
        weight = Fraction(index + 2, index + 1)
        for lane, (u, v) in enumerate(zip(lp, rp)):
            factor = weight if lane == 0 else -1 / weight
            pu, pv = 4 * lc + u, 4 * rc + v
            scalar.append((pu, pv, la, ra, factor))
            if left == root_literal:
                lane_maps[(ra, v)] = (u, factor)
            elif right == root_literal:
                lane_maps[(la, u)] = (v, factor)
    assert len(scalar) == 12 * k
    assert len({(u, v, a, b) for u, v, a, b, _ in scalar}) == len(scalar)
    return scalar, lane_maps


def matching_terms(word, edges):
    adjacency = [[] for _ in word]
    for u, v, a, b, weight in edges:
        if word[u] == a and word[v] == b:
            adjacency[u].append((v, weight))
            adjacency[v].append((u, weight))

    def visit(mask):
        if not mask:
            return [Fraction(1)]
        first = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << first)
        terms = []
        for other, weight in adjacency[first]:
            if rest & (1 << other):
                terms.extend(weight * term
                             for term in visit(rest ^ (1 << other)))
        return terms

    return visit((1 << len(word)) - 1)


def paired_depth(word, color):
    return sum(word[4 * component + u] != color
               and word[4 * component + v] != color
               for component in range(len(word) // 4)
               for u, v in PAIRS[color])


def main():
    counts = {"misaligned_q1": 0, "aligned_q2": 0}
    for k, colors, resources, bits in product(
            (2, 3, 4, 7), permutations(range(3)),
            product(range(2), repeat=3), product(range(2), repeat=2)):
        a, b, c = colors
        foreign = k - 1
        edges, maps = build(k, colors, resources, bits)
        pair_b = set(PAIRS[b][resources[1]])
        pair_c = set(PAIRS[c][resources[2]])
        shared, = pair_b & pair_c
        unshared_b, = pair_b - pair_c
        unshared_c, = pair_c - pair_b
        word = [a] * (4 * k)
        if maps[(b, unshared_b)][0] != maps[(c, unshared_c)][0]:
            word[4 * foreign + unshared_b] = b
            word[4 * foreign + unshared_c] = c
            expected = maps[(b, unshared_b)][1] * maps[(c, unshared_c)][1]
            assert paired_depth(word, a) == 1
            counts["misaligned_q1"] += 1
        else:
            word[4 * foreign:4 * foreign + 4] = [c] * 4
            word[4 * foreign + shared] = b
            expected = maps[(b, shared)][1] * maps[(c, unshared_c)][1]
            assert tuple(paired_depth(word, x) for x in colors) == (
                2, 2 * k - 1, 2 * k - 2)
            assert min(paired_depth(word, x) for x in range(3)) == 2
            counts["aligned_q2"] += 1
        assert len(set(word)) > 1
        assert matching_terms(word, edges) == [expected]
        assert expected != 0
    assert counts == {"misaligned_q1": 384, "aligned_q2": 384}
    print("HIDDEN_FULL_ARRAY_WORD_REPLAY_PASS", counts)


if __name__ == "__main__":
    main()
