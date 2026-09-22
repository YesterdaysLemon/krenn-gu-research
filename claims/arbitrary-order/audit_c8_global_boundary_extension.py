"""Exact k=3 color-regular extension of the C8+split local delta tensor."""

from __future__ import annotations

from itertools import product


COLORS = range(3)
MA, MB, MC = 0, 1, 2
MATCHINGS = {
    MA: ((0, 1), (2, 3)),
    MB: ((0, 2), (1, 3)),
    MC: ((0, 3), (1, 2)),
}


def add(entries, u, v, cu, cv, weight, name):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    key = (u, v, cu, cv)
    assert key not in entries, (key, entries.get(key), name)
    entries[key] = (weight, name)


def make_table():
    entries = {}
    crossing = []
    for base in (0, 4, 8):
        for color, matching in MATCHINGS.items():
            for x, y in matching:
                add(entries, base + x, base + y, color, color, 1,
                    f"P{color}:{base+x}-{base+y}")

    # Each map is a bijection from the first color's 12 physical vertices to
    # the second color's 12 physical vertices.  The component cycles make a
    # genuine global color-regular support with no within-component crossing.
    ac = {
        0: (4, 1), 2: (7, 1),       # E0 -> P0, product x0=+1
        1: (5, 1), 3: (6, -1),      # E1 -> P1, product x1=-1
        4: (8, 1), 5: (9, 1), 6: (10, 1), 7: (11, 1),
        8: (0, 1), 9: (1, 1), 10: (2, 1), 11: (3, 1),
    }
    bc = {
        0: (8, 1), 2: (11, -1),     # E0 -> Q0, product -1
        1: (9, 1), 3: (10, -1),     # E1 -> Q1, product -1
        8: (4, 1), 9: (5, 1), 10: (6, 1), 11: (7, 1),
        4: (0, 1), 5: (1, 1), 6: (2, 1), 7: (3, 1),
    }
    ab = {
        0: (4, 1), 1: (5, 1), 2: (6, 1), 3: (7, 1),
        4: (8, 1), 5: (9, 1), 6: (10, 1), 7: (11, 1),
        8: (0, 1), 9: (1, 1), 10: (2, 1), 11: (3, 1),
    }
    for label, ca, cb, mapping in (("ac", MA, MC, ac), ("bc", MB, MC, bc),
                                    ("ab", MA, MB, ab)):
        assert set(mapping) == set(range(12))
        assert len({v for v, _ in mapping.values()}) == 12
        for u, (v, weight) in mapping.items():
            assert u // 4 != v // 4
            add(entries, u, v, ca, cb, weight, f"{label}:{u}-{v}")
            crossing.append((u, v, ca, cb))

    degree = {(u, c): 0 for u in range(12) for c in COLORS}
    for u, v, cu, cv in crossing:
        degree[(u, cu)] += 1
        degree[(v, cv)] += 1
    assert set(degree.values()) == {2}
    return entries, degree


def terms_for(word, entries):
    adjacency = {u: [] for u in range(12)}
    for (u, v, cu, cv), (weight, name) in entries.items():
        if word[u] == cu and word[v] == cv:
            adjacency[u].append((v, weight, name))
            adjacency[v].append((u, weight, name))

    def rec(unmatched):
        if not unmatched:
            return [(1, ())]
        u = min(unmatched, key=lambda z: sum(v in unmatched for v, _, _ in adjacency[z]))
        out = []
        for v, weight, name in adjacency[u]:
            if v in unmatched:
                for tail_weight, tail in rec(unmatched - {u, v}):
                    out.append((weight * tail_weight, (name,) + tail))
        return out

    return rec(frozenset(range(12)))


def main():
    entries, degree = make_table()
    histogram = {d: list(degree.values()).count(d) for d in set(degree.values())}
    result = {}
    nonzero_terms = 0
    for local in product(COLORS, repeat=4):
        word = local + (MC,) * 8
        terms = terms_for(word, entries)
        coefficient = sum(weight for weight, _ in terms)
        expected = 1 if local == (MC,) * 4 else 0
        assert coefficient == expected, (local, coefficient, terms)
        result[local] = (coefficient, terms)
        nonzero_terms += len(terms)

    # The singleton aaaa|cccc|cccc row is the C8 cancellation 1+x0*x1.
    a_terms = result[(MA,) * 4][1]
    assert sorted(weight for weight, _ in a_terms) == [-1, 1]
    # The opposite bbbb row factors as (1-1)(1-1), with four terms.
    b_terms = result[(MB,) * 4][1]
    assert sorted(weight for weight, _ in b_terms) == [-1, -1, 1, 1]

    print("crossing_entries", 36)
    print("state_crossing_degree_histogram", histogram)
    print("local_words_checked", len(result))
    print("supported_terms_across_local_words", nonzero_terms)
    print("aaaa_term_weights", sorted(weight for weight, _ in a_terms))
    print("bbbb_term_weights", sorted(weight for weight, _ in b_terms))
    print("GLOBAL_COLORREGULAR_LOCAL_DELTA_PASS")


if __name__ == "__main__":
    main()
