#!/usr/bin/env python3
"""Exact color-regular control for a partial pair plus orphan endpoints.

This is a genuine three-component hollow array.  It proves only that the
full 81-word tensor on one component against one uniform background does
not force the complement of a cancelling pair to be another resource.
"""

from functools import lru_cache
from itertools import product


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}


def add(entries, u, v, cu, cv, weight, name):
    assert u // 4 != v // 4 or cu == cv
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    key = (u, v, cu, cv)
    assert key not in entries, (key, entries[key], name)
    entries[key] = (weight, name)


def build_entries():
    entries = {}
    for base in (0, 4, 8):
        for colour, pairs in MATCHINGS.items():
            for u, v in pairs:
                add(entries, base + u, base + v, colour, colour, 1,
                    f"P{colour}:{base+u}-{base+v}")

    # The displayed values are target vertices.  Every table is a global
    # permutation and every crossing joins different protected components.
    f02 = (4, 7, 5, 8, 9, 10, 11, 0, 1, 2, 3, 6)
    w02 = (1, -1, 1, 1) + (1,) * 8
    f12 = (5, 4, 6, 8, 9, 10, 11, 0, 1, 2, 3, 7)
    w12 = (1, 1, -1, 1) + (1,) * 8
    f01 = (4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3)
    w01 = (1,) * 12

    for label, ca, cb, mapping, weights in (
        ("02", 0, 2, f02, w02),
        ("12", 1, 2, f12, w12),
        ("01", 0, 1, f01, w01),
    ):
        assert set(mapping) == set(range(12))
        for u, (v, weight) in enumerate(zip(mapping, weights)):
            assert u // 4 != v // 4
            add(entries, u, v, ca, cb, weight, f"X{label}:{u}-{v}")
    return entries, f02, f12


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            answer.append(((u, v),) + tail)
    return tuple(answer)


ALL_MATCHINGS = matchings(tuple(range(12)))


def coefficient(word, entries):
    terms = []
    for matching in ALL_MATCHINGS:
        weight = 1
        names = []
        for u, v in matching:
            item = entries.get((u, v, word[u], word[v]))
            if item is None:
                break
            factor, name = item
            weight *= factor
            names.append(name)
        else:
            terms.append((weight, tuple(names)))
    return sum(weight for weight, _ in terms), terms


def main():
    entries, f02, f12 = build_entries()
    crossings = [key for key in entries if key[0] // 4 != key[1] // 4]
    assert len(crossings) == 36

    degree = {(u, c): [] for u in range(12) for c in range(3)}
    for u, v, cu, cv in crossings:
        degree[(u, cu)].append(cv)
        degree[(v, cv)].append(cu)
    for (u, colour), neighbours in degree.items():
        assert sorted(neighbours) == [c for c in range(3) if c != colour]

    # A's 0--2 layer has one cancelling M_0 -> M_2 pair and two orphan
    # targets in distinct exterior components.  The 1--2 layer is analogous.
    assert frozenset(f02[:2]) == frozenset((4, 7))
    assert f02[2] // 4 != f02[3] // 4
    assert frozenset((f12[0], f12[2])) == frozenset((5, 6))
    assert f12[1] // 4 != f12[3] // 4

    term_rows = {}
    for local in product(range(3), repeat=4):
        word = local + (2,) * 8
        value, terms = coefficient(word, entries)
        target = int(local == (2, 2, 2, 2))
        assert value == target, (local, value, terms)
        if terms:
            term_rows[local] = tuple(weight for weight, _ in terms)
    assert term_rows == {
        (0, 0, 0, 0): (1, -1),
        (1, 1, 1, 1): (1, -1),
        (2, 2, 2, 2): (1,),
    }

    # Keep the global evidence boundary explicit.
    failure = (0, 0, 0, 0) + (1,) * 4 + (2,) * 4
    value, terms = coefficient(failure, entries)
    assert value != 0

    print("crossing_entries=36 color_regular=PASS")
    print("A_02=one_pair_plus_two_orphans A_12=one_pair_plus_two_orphans")
    print("local_rows=A|2222|2222 all81_exact_delta=PASS")
    print("supported_local_rows=0000:(1,-1) 1111:(1,-1) 2222:(1)")
    print(f"explicit_global_failure=0000|1111|2222 coefficient={value} terms={len(terms)}")
    print("PARTIAL_PAIR_ORPHAN_LOCAL_CONTROL_PASS")


if __name__ == "__main__":
    main()
