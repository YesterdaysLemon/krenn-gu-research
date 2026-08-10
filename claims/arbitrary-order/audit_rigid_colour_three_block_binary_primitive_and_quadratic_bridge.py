"""Independent no-import audit for the rigid-colour three-block theorem.

This uses mask dynamic programming and two canonical incidence forms rather
than importing the primary verifier.  The arbitrary-order proof remains the
written proof.
"""

from itertools import combinations, product
from math import comb


def edge(u, v):
    return (u, v) if u < v else (v, u)


def generic_matchings(vertices):
    if not vertices:
        return [frozenset()]
    u = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        v = vertices[index]
        for tail in generic_matchings(vertices[1:index] + vertices[index + 1 :]):
            answer.append(tail | {edge(u, v)})
    return answer


def audit_convolution():
    for n in (4, 6, 8):
        vertices = tuple(range(n))
        full = generic_matchings(vertices)
        for k in range(n // 2 + 1):
            counts = {matching: 0 for matching in full}
            for subset in combinations(vertices, 2 * k):
                subset = set(subset)
                left = generic_matchings(tuple(sorted(subset)))
                right = generic_matchings(tuple(v for v in vertices if v not in subset))
                for first in left:
                    for second in right:
                        counts[first | second] += 1
            assert set(counts.values()) == {comb(n // 2, k)}


def add(table, u, v, left, right, weight=1):
    key = edge(u, v)
    assert key not in table
    table[key] = (left, right, weight) if u < v else (right, left, weight)


def value(table, word):
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
            key = edge(u, v)
            if key not in table:
                continue
            left, right, weight = table[key]
            if u > v:
                left, right = right, left
            if (word[u], word[v]) == (left, right):
                total += weight * rec(rest ^ bit)
        memo[mask] = total
        return total

    return rec((1 << len(word)) - 1)


def canonical_all_d():
    table = {}
    for u, v in ((0, 2), (1, 4), (3, 5)):
        add(table, u, v, 0, 0)
    for u, v in ((1, 3), (0, 5), (2, 4)):
        add(table, u, v, 1, 1)
    add(table, 0, 3, 0, 1)
    add(table, 1, 2, 1, 0, -1)
    add(table, 1, 5, 0, 1)
    add(table, 0, 4, 1, 0, -1)
    add(table, 3, 4, 0, 1)
    add(table, 2, 5, 1, 0, -1)
    return table


def canonical_one_s():
    table = {}
    for u, v in ((0, 2), (1, 4), (3, 5)):
        add(table, u, v, 0, 0)
    for u, v in ((0, 3), (1, 5), (2, 4)):
        add(table, u, v, 1, 1)
    add(table, 3, 4, 0, 1)
    add(table, 2, 5, 1, 0, -1)
    return table


def audit_six_forms():
    for table, expected_forbidden in ((canonical_all_d(), 6), (canonical_one_s(), 2)):
        nonzero = {
            word: value(table, word)
            for word in product(range(2), repeat=6)
            if value(table, word)
        }
        assert nonzero[(0,) * 6] == 1
        assert nonzero[(1,) * 6] == 1
        forbidden = {word: scalar for word, scalar in nonzero.items() if len(set(word)) > 1}
        assert len(forbidden) == expected_forbidden
        assert all(scalar != 0 for scalar in forbidden.values())


def audit_order_four():
    table = {}
    factors = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    for colour, matching in enumerate(factors):
        for u, v in matching:
            add(table, u, v, colour, colour)
    nonzero = {
        word: value(table, word)
        for word in product(range(3), repeat=4)
        if value(table, word)
    }
    assert nonzero == {(0,) * 4: 1, (1,) * 4: 1, (2,) * 4: 1}


def cycle_matchings(m, shifts):
    support = {
        edge(i, m + (i + shift) % m)
        for shift in shifts
        for i in range(m)
    }

    def rec(vertices):
        if not vertices:
            return [frozenset()]
        u = vertices[0]
        answer = []
        for index in range(1, len(vertices)):
            v = vertices[index]
            if edge(u, v) not in support:
                continue
            for tail in rec(vertices[1:index] + vertices[index + 1 :]):
                answer.append(tail | {edge(u, v)})
        return answer

    return rec(tuple(range(2 * m)))


def audit_shift_cycles():
    for m in (3, 5, 7):
        for shifts in ((0, 1), (0, 2), (1, 2)):
            assert len(cycle_matchings(m, shifts)) == 2
        assert len(cycle_matchings(m, (0, 1, 2))) > 3


def main():
    audit_convolution()
    audit_six_forms()
    audit_order_four()
    audit_shift_cycles()
    print("independent rigid-colour three-block audit: PASS")
    print("scope: bounded incidence/convolution audit only")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
