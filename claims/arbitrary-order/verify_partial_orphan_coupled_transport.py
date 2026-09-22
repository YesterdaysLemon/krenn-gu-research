#!/usr/bin/env python3
"""Finite sector replay for same-component partial-orphan transport."""

from functools import lru_cache
from itertools import permutations


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((u, v),) + tail)
    return tuple(answer)


ALL_MATCHINGS = perfect_matchings(tuple(range(12)))


def protected_entries():
    entries = {}
    for base in (0, 4, 8):
        for colour, pairs in MATCHINGS.items():
            for u, v in pairs:
                entries[(base + u, base + v, colour, colour)] = "protected"
    return entries


def add(entries, u, v, cu, cv, name):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    entries[(u, v, cu, cv)] = name


def supported_terms(word, entries):
    answer = []
    for matching in ALL_MATCHINGS:
        names = []
        for u, v in matching:
            name = entries.get((u, v, word[u], word[v]))
            if name is None:
                break
            names.append(name)
        else:
            answer.append(tuple(names))
    return answer


def is_M0_resource(u, v):
    return u // 4 == v // 4 and frozenset((u % 4, v % 4)) in {
        frozenset(edge) for edge in MATCHINGS[0]
    }


def main():
    # a=0, b=1, c=2.  R=A01.  Its orphan targets are the M_b(B) edge B02;
    # the complementary M_b(B) edge is B13.
    r, s = 0, 1
    y, z = 4, 6
    l0, l1 = 5, 7
    word = (0, 0, 0, 0, 2, 1, 2, 1, 0, 0, 0, 0)

    placements = 0
    repaired = 0
    for q0, q1 in permutations((0, 1, 2, 3, 8, 9, 10, 11), 2):
        entries = protected_entries()
        add(entries, r, y, 0, 2, "orphan-0")
        add(entries, s, z, 0, 2, "orphan-1")
        add(entries, l0, q0, 1, 0, "exit-0")
        add(entries, l1, q1, 1, 0, "exit-1")
        terms = supported_terms(word, entries)

        # The direct orphan term with protected L always exists.
        assert len(terms) >= 1
        expect_extra = is_M0_resource(q0, q1) and frozenset((q0, q1)) != frozenset((r, s))
        assert len(terms) == 1 + int(expect_extra), (q0, q1, terms)
        placements += 1
        repaired += int(expect_extra)

    assert placements == 56
    assert repaired == 6
    print("target_placements=56 direct_sector_always=PASS")
    print("extra_sector_iff_distinct_Ma_resource=6 PASS")
    print("PARTIAL_ORPHAN_COUPLED_TRANSPORT_REPLAY_PASS")


if __name__ == "__main__":
    main()
