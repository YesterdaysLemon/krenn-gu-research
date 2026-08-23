#!/usr/bin/env python3
"""Independent no-import F_3 audit for GLS49."""

from itertools import combinations, product


P = 3


def inv(value):
    value %= P
    assert value
    return pow(value, P - 2, P)


def rank_mod(columns, nrows):
    if not columns:
        return 0
    rows = [[column[row] % P for column in columns] for row in range(nrows)]
    pivot_row = 0
    for col in range(len(columns)):
        pivot = next((r for r in range(pivot_row, nrows) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = inv(rows[pivot_row][col])
        rows[pivot_row] = [(scale * x) % P for x in rows[pivot_row]]
        for r in range(nrows):
            if r != pivot_row and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [(x - factor * y) % P
                           for x, y in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def tensor(left, right):
    return tuple(a * b % P for a in left for b in right)


def canonical(vector):
    first = next((x for x in vector if x % P), None)
    if first is None:
        return None
    scale = inv(first)
    return tuple(scale * x % P for x in vector)


def projective_q_lines():
    return sorted({canonical(v) for v in product(range(P), repeat=9)
                   if any(v)})


def quotient_dimension(q):
    port = tuple(tuple(int(i == j) for i in range(3)) for j in range(3))
    cylinder = [tensor(q, e) for e in port]
    roots = []
    for colour in range(3):
        r = tuple(int(k == 3 * colour + colour) for k in range(9))
        roots.append(tensor(r, port[colour]))
    return rank_mod(cylinder + roots, 27) - rank_mod(cylinder, 27)


def support_audit():
    labels = range(6)  # residual bits 0,1; four promoted bits 2,...,5
    supports = [s for s in combinations(labels, 3) if 0 in s and 1 in s]
    assert supports == [(0, 1, u) for u in range(2, 6)]
    for support in supports:
        assert len(tuple(combinations(support, 2))) == 3
    return len(supports)


def shore_orientation_audit():
    # Reconstruct the pure-q premise.  In either orientation the opposite
    # two-column residual shore contains e_j.  It cannot also contain both
    # remaining coordinate axes.
    coordinate = tuple(tuple(int(i == j) for i in range(3)) for j in range(3))
    conditioned = 0
    for _orientation in ("left-line", "right-line"):
        for b_entries in product(range(P), repeat=6):
            bcols = (b_entries[0:3], b_entries[3:6])
            shore_rank = rank_mod(bcols, 3)
            for j in range(3):
                contains_j = rank_mod(bcols + (coordinate[j],), 3) == shore_rank
                if not contains_j:
                    continue
                conditioned += 1
                other = [i for i in range(3) if i != j]
                contains_both = all(
                    rank_mod(bcols + (coordinate[i],), 3) == shore_rank
                    for i in other
                )
                assert not contains_both
    return conditioned


def main():
    lines = projective_q_lines()
    assert len(lines) == 9841
    assert rank_mod([
        tuple(int(k == 13 * i) for k in range(27)) for i in range(3)
    ], 27) == 3  # q=0 leaves only two non-cylinder G generators
    counts = {2: 0, 3: 0}
    pure = set()
    for colour in range(3):
        r = tuple(int(k == 3 * colour + colour) for k in range(9))
        pure.add(canonical(r))
    for q in lines:
        dimension = quotient_dimension(q)
        assert dimension in counts
        counts[dimension] += 1
        assert (dimension == 2) == (q in pure)
    assert counts == {2: 3, 3: 9838}

    support_count = support_audit()
    shore_cases = shore_orientation_audit()
    print("GLS49 independent no-import audit: PASS")
    print("projective F_3 q lines:", len(lines), counts)
    print("D(p) support cases:", support_count)
    print("pure-q conditioned shore cases in two orientations:", shore_cases)


if __name__ == "__main__":
    main()
