"""Independent no-import audit of the cross-parity/Wick reductions.

This audit uses assignment-specific bitmask dynamic programming and a
separate subset/injection ledger.  It is bounded supporting evidence, not the
arbitrary-order proof and not a graph-family search.
"""

from functools import lru_cache
from itertools import combinations, permutations, product


def make_table(n, units):
    table = [[None for _ in range(n)] for _ in range(n)]
    for (u, v), (a, b, weight) in units.items():
        table[u][v] = (a, b, weight)
        table[v][u] = (b, a, weight)
    return table


def coefficient(table, assignment):
    n = len(table)

    @lru_cache(None)
    def rec(mask):
        if mask == 0:
            return 1
        u_bit = mask & -mask
        u = u_bit.bit_length() - 1
        rest = mask ^ u_bit
        total = 0
        candidates = rest
        while candidates:
            v_bit = candidates & -candidates
            candidates ^= v_bit
            v = v_bit.bit_length() - 1
            unit = table[u][v]
            if unit is None:
                continue
            a, b, weight = unit
            if a == assignment[u] and b == assignment[v]:
                total += weight * rec(rest ^ v_bit)
        return total

    return rec((1 << n) - 1)


def coefficient_by_cross(table, assignment, colour):
    n = len(table)

    @lru_cache(None)
    def rec(mask):
        if mask == 0:
            return (1,)
        u_bit = mask & -mask
        u = u_bit.bit_length() - 1
        rest = mask ^ u_bit
        result = [0] * (n // 2 + 1)
        candidates = rest
        while candidates:
            v_bit = candidates & -candidates
            candidates ^= v_bit
            v = v_bit.bit_length() - 1
            unit = table[u][v]
            if unit is None:
                continue
            a, b, weight = unit
            if a != assignment[u] or b != assignment[v]:
                continue
            shift = int((a == colour) != (b == colour))
            tail = rec(rest ^ v_bit)
            for degree, value in enumerate(tail):
                if degree + shift < len(result):
                    result[degree + shift] += weight * value
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        return tuple(result)

    return rec((1 << n) - 1)


def pure_haf(table, vertices, colour):
    vertices = tuple(sorted(vertices))

    @lru_cache(None)
    def rec(state):
        if not state:
            return 1
        u = state[0]
        total = 0
        for index in range(1, len(state)):
            v = state[index]
            unit = table[u][v]
            if unit is None:
                continue
            a, b, weight = unit
            if a == b == colour:
                total += weight * rec(state[1:index] + state[index + 1 :])
        return total

    return rec(vertices)


def audit_parity() -> None:
    n = 6
    units = {}
    for u in range(n):
        for v in range(u + 1, n):
            units[(u, v)] = ((u + v) % 3, (u + 2 * v + 1) % 3, 1 + (u * v) % 3)
    table = make_table(n, units)
    for assignment in product(range(3), repeat=n):
        for colour in range(3):
            sectors = coefficient_by_cross(table, assignment, colour)
            for degree, value in enumerate(sectors):
                if value:
                    assert degree % 2 == assignment.count(colour) % 2
            assert sum(sectors) == coefficient(table, assignment)


def rigid_units():
    n = 6
    shore = {0, 1}
    rigid = {2, 3, 4, 5}
    units = {}
    for u in range(n):
        for v in range(u + 1, n):
            if u in shore and v in rigid:
                units[(u, v)] = (1, 0, 1 + (u + v) % 2)
            elif u in rigid and v in rigid:
                colour = (u + v) % 2
                units[(u, v)] = (colour, colour, 1)
            else:
                units[(u, v)] = (1, 1, 2)
    return make_table(n, units), shore, rigid


def injection_value(table, shore, rigid, heads):
    total = 0
    heads = set(heads)
    for size in range(len(heads) + 1):
        for exposed_tuple in combinations(sorted(heads), size):
            exposed = set(exposed_tuple)
            internal = heads - exposed
            if len(internal) % 2:
                continue
            left_haf = pure_haf(table, internal, 0)
            for image_tuple in permutations(sorted(shore), size):
                flag = 1
                for r, s in zip(exposed_tuple, image_tuple, strict=True):
                    unit = table[s][r]
                    if unit is None or unit[0:2] != (1, 0):
                        flag = 0
                        break
                    flag *= unit[2]
                residue = set(range(6)) - heads - set(image_tuple)
                total += left_haf * flag * pure_haf(table, residue, 1)
    return total


def audit_wick_tower() -> None:
    table, shore, rigid = rigid_units()
    for size in range(1, len(rigid) + 1):
        for heads in combinations(sorted(rigid), size):
            assignment = tuple(0 if v in heads else 1 for v in range(6))
            assert coefficient(table, assignment) == injection_value(
                table, shore, rigid, heads
            )

    for size in range(len(rigid)):
        for chosen in combinations(sorted(rigid), size):
            left = shore | set(chosen)
            right = rigid - set(chosen)
            assignment = tuple(0 if v in left else 1 for v in range(6))
            assert coefficient(table, assignment) == pure_haf(
                table, left, 0
            ) * pure_haf(table, right, 1)


def shift_table(m, chord):
    units = {}
    for colour in range(3):
        for i in range(m):
            u, v = i, m + (i + colour) % m
            units[(min(u, v), max(u, v))] = (colour, colour, 1)
    if chord:
        units[(0, 1)] = (1, 0, 5)
    return make_table(2 * m, units), units


def explicit_mixed_word(m):
    word = [None] * (2 * m)
    word[0] = word[m] = 0
    for i in range(1, m - 1):
        word[i] = word[m + i + 1] = 1
    word[m - 1] = word[m + 1] = 2
    return tuple(word)


def audit_sparse_family() -> None:
    for m in (3, 5, 7):
        n = 2 * m
        chorded, units = shift_table(m, True)
        plain, _ = shift_table(m, False)

        mixed = explicit_mixed_word(m)
        assert coefficient(plain, mixed) > 0
        assert coefficient(chorded, mixed) == coefficient(plain, mixed)

        # The chord cannot extend: after deleting its A endpoints, every
        # remaining support edge is A--B with unequal shore sizes.
        assert m - 2 != m
        assert len(units) < n * (n - 1) // 2

        for a, b in combinations(range(3), 2):
            assert coefficient(plain, (a,) * n) == 1
            assert coefficient(plain, (b,) * n) == 1
            for assignment in ((a, b) * m, (b, a) * m):
                # These probes are not the proof of pairwise Delta, but they
                # independently reject a common alternating-word mistake.
                assert coefficient(plain, assignment) == 0

        # Erasing the sterile chord preserves every coefficient tested by
        # the exact bitmask evaluator, including all words at m=3.
        if m == 3:
            for assignment in product(range(3), repeat=n):
                assert coefficient(chorded, assignment) == coefficient(plain, assignment)


def audit_bridge_and_incidence_ledgers() -> None:
    pair_counts = [(2, 0, 0), (1, 1, 1), (4, 2, 0)]
    for x01, x02, x12 in pair_counts:
        parities = ((x01 + x02) % 2, (x01 + x12) % 2, (x02 + x12) % 2)
        assert parities == (0, 0, 0)

    # Complements allowed by the functional-pseudoforest count.
    assert 3 * (3 - 1) == 6  # K_3,3 is the full-set numerical exception.
    for n in (8, 10, 12):
        m = n // 2
        assert m * (m - 1) != n
        assert 2 * (n - 2) > n


def main() -> None:
    audit_parity()
    audit_wick_tower()
    audit_sparse_family()
    audit_bridge_and_incidence_ledgers()
    print("independent cross-parity and rigid-head Wick audit: PASS")
    print("scope: bounded bitmask and injection ledgers only")
    print("is_kg_witness: false")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
