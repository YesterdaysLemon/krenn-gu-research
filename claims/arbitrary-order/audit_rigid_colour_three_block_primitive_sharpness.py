"""Independent no-import audit of the three-block cycle countermechanism.

This uses shore counts, explicit cycle-neighbour logic, and the staircase
word formula rather than the primary check's matching recursion.  It is not
the arbitrary-order proof.
"""


def cycle_edge(n, u, v):
    return (u - v) % n in (1, n - 1)


def forced_path_matching(n, removed):
    remaining = set(range(n)) - set(removed)
    chosen = set()
    while remaining:
        neighbours = {
            u: {v for v in remaining if v != u and cycle_edge(n, u, v)}
            for u in remaining
        }
        endpoint = next((u for u, adjacent in neighbours.items() if len(adjacent) == 1), None)
        assert endpoint is not None
        partner = next(iter(neighbours[endpoint]))
        chosen.add(tuple(sorted((endpoint, partner))))
        remaining.remove(endpoint)
        remaining.remove(partner)
    return chosen


def audit_order(n):
    even = set(range(0, n, 2))
    odd = set(range(1, n, 2))
    first = set(sorted(even)[:2])
    second = set(sorted(even)[2:4])
    mediator = set(range(n)) - first - second

    assert len(first) == len(second) == 2
    assert not any(cycle_edge(n, u, v) for u in first for v in first if u < v)
    assert not any(cycle_edge(n, u, v) for u in second for v in second if u < v)
    assert not any(cycle_edge(n, u, v) for u in first | second for v in first | second if u < v)

    for vertices, expected_gap in (
        (mediator, 4),
        (first | mediator, 2),
        (second | mediator, 2),
    ):
        left = len(vertices & even)
        right = len(vertices & odd)
        assert right - left == expected_gap

    # An even cycle has exactly the two alternating selections.
    matching_a = {(u, u + 1) for u in range(0, n, 2)}
    matching_b = {(u, (u + 1) % n) for u in range(1, n, 2)}
    assert len(matching_a) == len(matching_b) == n // 2
    assert matching_a.isdisjoint(matching_b)

    # In the complement of the cycle, the middle four-hafnian term is the
    # sole surviving pairing on 0,1,2,3.
    assert not cycle_edge(n, 0, 2)
    assert not cycle_edge(n, 1, 3)
    assert cycle_edge(n, 0, 1)
    assert cycle_edge(n, 1, 2)
    assert cycle_edge(n, 2, 3)
    four_terms = (
        (not cycle_edge(n, 0, 1)) and (not cycle_edge(n, 2, 3)),
        (not cycle_edge(n, 0, 2)) and (not cycle_edge(n, 1, 3)),
        (not cycle_edge(n, 0, 3)) and (not cycle_edge(n, 1, 2)),
    )
    assert four_terms == (False, True, False)

    remaining_a = {(u, u + 1) for u in range(4, n, 2)}
    assert len(remaining_a) == (n - 4) // 2

    # Saturating the odd shore cannot change a full matching: any odd--odd
    # edge creates a shore imbalance.  Deleting x_0=0 and x_1=2 instead
    # forces exactly one chord y_0--y_j.  The residual paths give distinct
    # staircase patterns on x_2,...,x_(m-1).
    m = n // 2
    patterns = set()
    x_vertices = tuple(2 * i for i in range(2, m))
    for j in range(1, m):
        y_0 = 1
        y_j = 2 * j + 1
        residual = forced_path_matching(n, {0, 2, y_0, y_j})
        predicted = {
            (2 * i + 1, 2 * (i + 1)) for i in range(1, j)
        } | {
            (2 * i, 2 * i + 1) for i in range(j + 1, m)
        }
        assert residual == predicted

        covered = {y_0, y_j}
        for u, v in residual:
            assert cycle_edge(n, u, v)
            assert u not in covered and v not in covered
            covered.update((u, v))
        assert covered == set(range(n)) - {0, 2}

        labels_at_x = {}
        for u, v in residual:
            colour = min(u, v) % 2
            for endpoint in (u, v):
                if endpoint in x_vertices:
                    labels_at_x[endpoint] = colour
        pattern = tuple(labels_at_x[x] for x in x_vertices)
        assert pattern == (1,) * (j - 1) + (0,) * (m - 1 - j)
        patterns.add(pattern)

    # Shore balance forces exactly one odd--odd chord, and y_0 loses both
    # cycle neighbours when x_0,x_1 are deleted.  Hence the cases above are
    # exhaustive, one for each possible partner y_j.
    required_odd_chords = (len(odd) - (len(even) - 2)) // 2
    assert required_odd_chords == 1
    assert all(not cycle_edge(n, 1, x) for x in x_vertices)
    assert len(patterns) == m - 1


def main():
    for n in (8, 10, 12, 14, 16, 18):
        audit_order(n)
    print("independent rigid-colour primitive shore audit: PASS")
    print("scope: bounded parity and chord audit only")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
