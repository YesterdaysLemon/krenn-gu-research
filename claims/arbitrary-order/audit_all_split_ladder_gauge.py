"""Exact k=2 replay of the odd-twist all-split ladder gauge."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import isqrt


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
RESOURCES = {
    "A": ((0, 1), (4, 5), (2, 3), (6, 7)),
    "B": ((4, 6), (0, 2), (5, 7), (1, 3)),
    "C": ((0, 3), (4, 7), (1, 2), (5, 6)),
}
COLORS = {"A": 0, "B": 1, "C": 2}
RESOURCE_CYCLE = tuple(
    label for i in range(4) for label in (f"A{i}", f"B{i}", f"C{i}")
)
F_EDGES = tuple(
    edge
    for i in range(4)
    for edge in ((f"A{i}", f"B{i}"), (f"B{i}", f"C{i}"),
                 (f"C{i}", f"A{(i + 1) % 4}"))
)


def resource(label):
    return RESOURCES[label[0]][int(label[1:])]


def label_for(kind, u):
    for i, edge in enumerate(RESOURCES[kind]):
        if u in edge:
            return f"{kind}{i}"
    raise AssertionError


def resource_mate(kind, u):
    edge = resource(label_for(kind, u))
    return edge[1] if u == edge[0] else edge[0]


def edge_index(left, right):
    wanted = frozenset((left, right))
    for i, edge in enumerate(F_EDGES):
        if frozenset(edge) == wanted:
            return i
    raise AssertionError((left, right))


def build_maps(bitmask):
    maps = {}
    for i, (left, right) in enumerate(F_EDGES):
        right_order = resource(right)[::-1] if (bitmask >> i) & 1 else resource(right)
        lane_map = {}
        for u, v in zip(resource(left), right_order):
            lane_map[u] = v
            lane_map[v] = u
        maps[frozenset((left, right))] = lane_map
    return maps


def tau(kind_from, kind_to, u, maps):
    left = label_for(kind_from, u)
    for candidate in F_EDGES:
        if left in candidate:
            other = candidate[1] if candidate[0] == left else candidate[0]
            if other.startswith(kind_to):
                return maps[frozenset(candidate)][u]
    raise AssertionError((kind_from, kind_to, u))


def transition(kind_from, kind_to, maps):
    return {
        u: tau(kind_from, kind_to, resource_mate(kind_from, u), maps)
        for u in range(8)
    }


def is_hamilton(permutation):
    seen = set()
    u = 0
    while u not in seen:
        seen.add(u)
        u = permutation[u]
    return u == 0 and len(seen) == 8


def find_hamilton_bitmask():
    for bitmask in range(1 << len(F_EDGES)):
        maps = build_maps(bitmask)
        if all(
            is_hamilton(transition(x, y, maps))
            for x, y in (("A", "B"), ("B", "C"), ("C", "A"))
        ):
            assert bitmask.bit_count() % 2 == 1
            return bitmask, maps
    raise AssertionError("no Hamilton endpoint pattern")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


ALL_MATCHINGS = tuple(perfect_matchings(range(8)))


def add(entries, u, v, cu, cv, weight):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    key = (u, v, cu, cv)
    assert key not in entries
    entries[key] = weight


def build_weighted_table(bitmask):
    entries = {}
    for base in (0, 4):
        for color, pairs in MATCHINGS.items():
            for x, y in pairs:
                add(entries, base + x, base + y, color, color, Fraction(1))

    for i, (left, right) in enumerate(F_EDGES):
        right_order = resource(right)[::-1] if (bitmask >> i) & 1 else resource(right)
        alpha = Fraction(4) if i == 0 else Fraction(1)
        for lane, (u, v) in enumerate(zip(resource(left), right_order)):
            weight = alpha if lane == 0 else -1 / alpha
            add(entries, u, v, COLORS[left[0]], COLORS[right[0]], weight)
    return entries


def coefficient(word, entries):
    total = Fraction(0)
    for matching in ALL_MATCHINGS:
        weight = Fraction(1)
        for u, v in matching:
            key = (u, v, word[u], word[v])
            if key not in entries:
                break
            weight *= entries[key]
        else:
            total += weight
    return total


def rational_sqrt(value):
    assert value > 0
    n, d = isqrt(value.numerator), isqrt(value.denominator)
    assert n * n == value.numerator and d * d == value.denominator
    return Fraction(n, d)


def main():
    bitmask, maps = find_hamilton_bitmask()
    assert bitmask.bit_count() % 2 == 1

    eps = []
    alpha = []
    for i in range(len(RESOURCE_CYCLE)):
        left = RESOURCE_CYCLE[i]
        right = RESOURCE_CYCLE[(i + 1) % len(RESOURCE_CYCLE)]
        index = edge_index(left, right)
        eps.append((bitmask >> index) & 1)
        alpha.append(Fraction(4) if index == 0 else Fraction(1))
    assert sum(eps) % 2 == 1

    # The closure map has form C/t.  Evaluating it at t=1 gives C.
    probe = Fraction(1)
    for a, e in zip(alpha, eps):
        r = 1 if e == 0 else -1
        probe = (a ** (-r)) * (probe ** (-r))
    closure_constant = probe
    t = [rational_sqrt(closure_constant)]
    for a, e in zip(alpha, eps):
        r = 1 if e == 0 else -1
        t.append((a ** (-r)) * (t[-1] ** (-r)))
    assert t[-1] == t[0]
    t = t[:-1]

    state_gauge = {}
    for label, value in zip(RESOURCE_CYCLE, t):
        u, v = resource(label)
        state_gauge[(u, COLORS[label[0]])] = value
        state_gauge[(v, COLORS[label[0]])] = 1 / value
    assert len(state_gauge) == 24

    before = build_weighted_table(bitmask)
    after = {}
    for (u, v, cu, cv), weight in before.items():
        after[(u, v, cu, cv)] = weight * state_gauge[(u, cu)] * state_gauge[(v, cv)]

    # Every protected rung is +1; each resource edge has lanes +1,-1.
    for base in (0, 4):
        for color, pairs in MATCHINGS.items():
            for x, y in pairs:
                assert after[(base + x, base + y, color, color)] == 1
    for i, (left, right) in enumerate(F_EDGES):
        right_order = resource(right)[::-1] if (bitmask >> i) & 1 else resource(right)
        values = []
        for u, v in zip(resource(left), right_order):
            if u > v:
                key = (v, u, COLORS[right[0]], COLORS[left[0]])
            else:
                key = (u, v, COLORS[left[0]], COLORS[right[0]])
            values.append(after[key])
        assert values == [1, -1], (i, values)

    # Check exact coefficient covariance for every physical word.
    for word in product(range(3), repeat=8):
        factor = Fraction(1)
        for u, color in enumerate(word):
            factor *= state_gauge[(u, color)]
        assert coefficient(word, after) == factor * coefficient(word, before)

    for color in range(3):
        pure = (color,) * 8
        assert coefficient(pure, before) == coefficient(pure, after) == 1

    print("hamilton_endpoint_bitmask", bitmask)
    print("total_endpoint_flip_parity", sum(eps) % 2)
    print("closure_constant", closure_constant)
    print("physical_words_checked", 3 ** 8)
    print("EXACT_K2_LADDER_GAUGE_PASS")


if __name__ == "__main__":
    main()
