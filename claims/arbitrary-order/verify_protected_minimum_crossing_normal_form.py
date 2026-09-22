#!/usr/bin/env python3
"""Exhaust the local two-cross boundary behind the 6k equality case.

Three protected K4 components are used only so the two supported crossings
may land in the same or in different exterior components.  Fix the singleton
macro word A=0, B=C=1.  For every two-element support among the 32 possible
0|1 crossings incident with A, compare literal perfect-matching existence
with the claimed protected-pair-bijection criterion.
"""

from itertools import combinations


MATCHINGS = {
    0: (((0, 1), (2, 3))),
    1: (((0, 2), (1, 3))),
    2: (((0, 3), (1, 2))),
}


def protected_edges(component: int, color: int):
    off = 4 * component
    return {
        tuple(sorted((off + u, off + v)))
        for u, v in MATCHINGS[color]
    }


def has_crossing_pm(cross_support):
    """Literal matching recursion; protected factors have weight one."""
    edges = set(cross_support)
    edges |= protected_edges(0, 0)
    edges |= protected_edges(1, 1)
    edges |= protected_edges(2, 1)
    by_vertex = {v: [] for v in range(12)}
    for e in edges:
        u, v = e
        by_vertex[u].append(e)
        by_vertex[v].append(e)

    found = []

    def rec(unmatched, chosen):
        if not unmatched:
            if any(e in cross_support for e in chosen):
                found.append(tuple(chosen))
            return
        u = min(unmatched)
        for e in by_vertex[u]:
            v = e[1] if e[0] == u else e[0]
            if v in unmatched:
                rec(unmatched - {u, v}, chosen + [e])

    rec(set(range(12)), [])
    return found


def is_pair_bijection(two_edges):
    roots = []
    exterior = []
    for u, v in two_edges:
        assert u < 4 <= v
        roots.append(u)
        exterior.append(v)
    if len(set(roots)) < 2 or len(set(exterior)) < 2:
        return False
    root_set = set(roots)
    ext_components = {v // 4 for v in exterior}
    if len(ext_components) != 1:
        return False
    ext_component = next(iter(ext_components))
    ext_local = {v - 4 * ext_component for v in exterior}
    return (
        root_set in [set(pair) for pair in MATCHINGS[0]]
        and ext_local in [set(pair) for pair in MATCHINGS[1]]
    )


def main():
    possible = [tuple(sorted((u, v))) for u in range(4) for v in range(4, 12)]
    valid = 0
    for support_tuple in combinations(possible, 2):
        support = set(support_tuple)
        matchings = has_crossing_pm(support)
        criterion = is_pair_bijection(support_tuple)
        assert bool(matchings) == criterion, (support_tuple, matchings, criterion)
        if criterion:
            valid += 1
            # With only these two crossing entries there is exactly one
            # crossing PM.  Therefore its scalar contribution is w1*w2.
            assert len(matchings) == 1
            assert support.issubset(set(matchings[0]))

    assert len(list(combinations(possible, 2))) == 496
    assert valid == 16  # 2 root pairs * 2 exteriors * 2 target pairs * 2 bijections
    print("two_edge_supports=496")
    print("pair_bijection_supports=16")
    print("shared_endpoint_and_split_exterior_boundaries=PASS")
    print("MINIMUM_DENSITY_TWO_EDGE_EQUALITY_PASS")


if __name__ == "__main__":
    main()
