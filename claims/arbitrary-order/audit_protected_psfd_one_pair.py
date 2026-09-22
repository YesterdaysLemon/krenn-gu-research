"""Independent literal replay of the finite PSFD base's q=0/q=1 boundary.

This file does not import the formula/search implementation.  It builds the
248-vertex scalar graph directly from the published PSFD table and counts
perfect matchings by recursive forced-endpoint elimination.
"""
import json

MATCH = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
LABELS = ((0,1),(0,2),(1,0),(1,2),(2,0),(2,1))
SHIFTS = (0,1,3,8,12,18)
PORTS = {
    (0,1):((2,3),(3,1)), (0,2):((0,3),(1,0)),
    (1,0):((1,1),(3,0)), (1,2):((0,2),(2,1)),
    (2,0):((1,3),(2,2)), (2,1):((0,0),(3,2)),
}


def vertex(side, index, port):
    return 4 * (31 * side + index) + port


def check_word():
    word = [0] * 248
    minorities = {
        (0,0,0):1, (0,0,2):1, (0,1,2):2,
        (0,13,3):1, (0,16,2):2, (0,28,3):1,
        (1,0,1):1, (1,1,0):2, (1,1,1):1,
        (1,13,3):1, (1,16,1):1, (1,28,3):1,
    }
    for key, color in minorities.items():
        word[vertex(*key)] = color

    adjacency = [0] * 248
    literal_entries = 0

    def add(u, v, a, b):
        nonlocal literal_entries
        literal_entries += 1
        if word[u] == a and word[v] == b:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u

    for side in range(2):
        for index in range(31):
            for color, matching in enumerate(MATCH):
                for p, q in matching:
                    add(vertex(side,index,p), vertex(side,index,q), color, color)

    for label, shift in zip(LABELS, SHIFTS, strict=True):
        a, b = label
        for left in range(31):
            right = (left + shift) % 31
            for p, q in PORTS[label]:
                add(vertex(0,left,p), vertex(1,right,q), a, b)

    memo = {}
    witness = []

    def count(mask, chosen):
        if not mask:
            if not witness:
                witness.extend(chosen)
            return 1
        if mask in memo:
            return memo[mask]
        remaining = mask
        best = None
        best_neighbors = 0
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            v = bit.bit_length() - 1
            neighbors = adjacency[v] & mask
            degree = neighbors.bit_count()
            if degree == 0:
                memo[mask] = 0
                return 0
            if best is None or degree < best_neighbors.bit_count():
                best, best_neighbors = v, neighbors
                if degree == 1:
                    break
        total = 0
        neighbors = best_neighbors
        while neighbors:
            bit = neighbors & -neighbors
            neighbors -= bit
            mate = bit.bit_length() - 1
            total += count(mask ^ (1 << best) ^ bit, chosen + [(best, mate)])
            if total >= 2:
                total = 2
                break
        memo[mask] = total
        return total

    multiplicity = count((1 << 248) - 1, [])
    q0 = sum(
        word[vertex(side,index,p)] != 0
        and word[vertex(side,index,q)] != 0
        for side in range(2)
        for index in range(31)
        for p, q in MATCH[0]
    )
    assert q0 == 1
    assert multiplicity == 1
    assert len(witness) == 124
    print(json.dumps({
        "status": "PASS",
        "vertices": 248,
        "literal_scalar_entries": literal_entries,
        "minorities": len(minorities),
        "q_0": q0,
        "perfect_matching_count_capped_2": multiplicity,
        "witness_edges": len(witness),
    }, sort_keys=True))


def check_cycles():
    """Exhaust simple directed cycles on independent physical vertex sets."""
    checked = 0
    for c in range(3):
        adjacency = [set() for _ in range(248)]
        for (a, b), shift in zip(LABELS, SHIFTS, strict=True):
            for left in range(31):
                right = (left + shift) % 31
                for p, q in PORTS[a, b]:
                    u, v = vertex(0, left, p), vertex(1, right, q)
                    if b == c:
                        adjacency[u].add(v ^ (c + 1))
                    if a == c:
                        adjacency[v].add(u ^ (c + 1))

        def find_cycle(start, current, path, excluded):
            nonlocal checked
            checked += 1
            for target in sorted(adjacency[current]):
                if target == start and len(path) >= 2:
                    return path
                # Rotation canonicalization retains every possible cycle at
                # its smallest vertex; partner exclusion enforces q=0.
                if target < start or target in excluded:
                    continue
                answer = find_cycle(
                    start, target, path + (target,),
                    excluded | {target, target ^ (c + 1)},
                )
                if answer is not None:
                    return answer
            return None

        for start in range(248):
            answer = find_cycle(start, start, (start,), {start, start ^ (c + 1)})
            assert answer is None, (c, answer)
    return checked


def main():
    check_word()
    print('PSFD_BASE_INDEPENDENT_CYCLE_ABSENCE_PASS', check_cycles())
    print('Finite base only: no claim for arbitrary PSFD lifts or P1.')


if __name__ == '__main__':
    main()
