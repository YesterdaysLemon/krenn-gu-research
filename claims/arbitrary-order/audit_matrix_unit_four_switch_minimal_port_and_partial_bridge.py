"""Independent no-import audit of the finite matrix-unit ledgers.

This audit uses mask recursion rather than the primary script's matching list.
It does not prove the arbitrary-order theorem.
"""

from itertools import product


def table_eight():
    table = {}

    def add(edge_list, labels, weights=None):
        if weights is None:
            weights = [1] * len(edge_list)
        for edge, weight in zip(edge_list, weights):
            table[edge] = labels + (weight,)

    add([(0, 1), (2, 3), (4, 5), (6, 7), (1, 2), (1, 3)], (0, 0))
    add([(0, 2), (0, 3)], (1, 0), [1, -1])
    add([(0, 4), (1, 5), (2, 6), (3, 7)], (1, 1))
    add([(0, 5), (1, 6), (2, 7), (3, 4)], (2, 2))
    add([(1, 4), (2, 5)], (2, 0))
    add([(2, 4)], (0, 1))
    add([(3, 5)], (0, 2))
    for u in range(8):
        for v in range(u + 1, 8):
            table.setdefault((u, v), (1, 2, 1))
    return table


def table_six():
    table = {}

    def add(edge_list, labels, weights=None):
        if weights is None:
            weights = [1] * len(edge_list)
        for edge, weight in zip(edge_list, weights):
            table[edge] = labels + (weight,)

    add([(0, 5), (1, 2), (3, 4)], (0, 0))
    add([(0, 1), (0, 3)], (1, 0))
    add([(2, 5), (4, 5)], (0, 2), [1, -1])
    add([(1, 3), (0, 4), (1, 5), (2, 3)], (1, 1))
    add([(2, 4), (0, 2), (1, 4), (3, 5)], (2, 2))
    return table


def oriented(table, u, v):
    if u < v:
        return table[(u, v)]
    right, left, weight = table[(v, u)]
    return left, right, weight


def value(table, word):
    memo = {0: 1}

    def rec(mask):
        if mask in memo:
            return memo[mask]
        low = mask & -mask
        u = low.bit_length() - 1
        rest = mask ^ low
        total = 0
        candidates = rest
        while candidates:
            bit = candidates & -candidates
            v = bit.bit_length() - 1
            candidates ^= bit
            a, b, weight = oriented(table, u, v)
            if word[u] == a and word[v] == b:
                total += weight * rec(rest ^ bit)
        memo[mask] = total
        return total

    return rec((1 << len(word)) - 1)


def active_count(table, word):
    memo = {0: 1}

    def rec(mask):
        if mask in memo:
            return memo[mask]
        low = mask & -mask
        u = low.bit_length() - 1
        rest = mask ^ low
        total = 0
        bits = rest
        while bits:
            bit = bits & -bits
            bits ^= bit
            v = bit.bit_length() - 1
            left, right, _ = oriented(table, u, v)
            if word[u] == left and word[v] == right:
                total += rec(rest ^ bit)
        memo[mask] = total
        return total

    return rec((1 << len(word)) - 1)


def audit_eight():
    table = table_eight()
    assert len(table) == 28
    for c in range(3):
        assert value(table, (c,) * 8) == 1
        for d in range(3):
            for v in range(8):
                word = [c] * 8
                word[v] = d
                assert value(table, tuple(word)) == (c == d)
            if c != d:
                for p in range(8):
                    for q in range(p + 1, 8):
                        word = [d] * 8
                        word[p] = word[q] = c
                        assert value(table, tuple(word)) == 0
    assert value(table, (1, 0, 0, 0, 0, 0, 0, 0)) == 0
    assert sum(
        value(table, word) != 0 and len(set(word)) > 1
        for word in product(range(3), repeat=8)
    ) == 79


def audit_six():
    table = table_six()
    assert len(table) == 15
    sets = [{0, 5}, {1, 3}, {2, 4}]
    found = [set(), set(), set()]
    for (u, v), (left, right, _) in table.items():
        if left != right:
            found[right].add(u)
            found[left].add(v)
    assert found == sets
    off_target_active_counts = []
    for c, boundary in enumerate(sets):
        assert value(table, (c,) * 6) == 1
        p, q = sorted(boundary)
        for x, y in product(range(3), repeat=2):
            word = [c] * 6
            word[p], word[q] = x, y
            assert value(table, tuple(word)) == ((x, y) == (c, c))
            if (x, y) != (c, c):
                count = active_count(table, tuple(word))
                if count:
                    off_target_active_counts.append(count)
    assert off_target_active_counts == [2]
    assert sum(
        value(table, word) != 0 and len(set(word)) > 1
        for word in product(range(3), repeat=6)
    ) == 10


def main():
    audit_eight()
    audit_six()
    print("independent matrix-unit mask audit: PASS")
    print("scope: finite endpoint and coefficient audit only")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
