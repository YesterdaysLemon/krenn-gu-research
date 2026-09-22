"""Independent exact replay of the color-regular C8-to-split coefficient."""

from __future__ import annotations

from itertools import permutations


A, B, C = 0, 1, 2
MATCHINGS = {
    A: ((0, 1), (2, 3)),
    B: ((0, 2), (1, 3)),
    C: ((0, 3), (1, 2)),
}
COMPONENTS = (tuple(range(4)), tuple(range(4, 8)), tuple(range(8, 12)))
EXTERIOR = tuple(range(4, 12))
AC_WEIGHTS = (2, 3, 5, 7)
BC_WEIGHTS = (11, 13, 17, 19)


def global_protected_edges(color):
    return {
        frozenset((base + u, base + v))
        for base in (0, 4, 8)
        for u, v in MATCHINGS[color]
    }


def add_entry(entries, u, v, cu, cv, weight, name):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    key = (u, v, cu, cv)
    assert key not in entries
    entries[key] = (weight, name)


def table_for(ac_map, bc_map):
    entries = {}
    for base in (0, 4, 8):
        for color, matching in MATCHINGS.items():
            for u, v in matching:
                add_entry(
                    entries,
                    base + u,
                    base + v,
                    color,
                    color,
                    1,
                    f"P{color}:{base+u}-{base+v}",
                )
    for u, v in enumerate(ac_map):
        add_entry(entries, u, v, A, C, AC_WEIGHTS[u], f"ac:{u}-{v}")
    for u, v in enumerate(bc_map):
        add_entry(entries, u, v, B, C, BC_WEIGHTS[u], f"bc:{u}-{v}")
    return entries


def exact_terms(word, entries):
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
            if v not in unmatched:
                continue
            for tail_weight, tail_names in rec(unmatched - {u, v}):
                out.append((weight * tail_weight, (name,) + tail_names))
        return out

    return rec(frozenset(range(12)))


def ac_map_for(source_matching, target_edges):
    """Map the two source edges to target_edges, preserving tuple order."""
    out = [None] * 4
    for source, target in zip(source_matching, target_edges):
        out[source[0]], out[source[1]] = target
    assert all(v is not None for v in out)
    return tuple(out)


def main():
    mc_edges = global_protected_edges(C)
    target_patterns = {
        "same_component": ((4, 7), (5, 6)),
        "spanning_components": ((4, 7), (8, 11)),
    }
    checked = 0

    for pattern_name, targets in target_patterns.items():
        assert all(frozenset(edge) in mc_edges for edge in targets)
        ac_map = ac_map_for(MATCHINGS[B], targets)

        # The pullback matching is M_b.  M_a union M_b is a 4-cycle on the
        # source ports and expands to one alternating C8 through the targets.
        assert set(map(frozenset, MATCHINGS[A])) != set(map(frozenset, MATCHINGS[B]))

        for bc_map in permutations(EXTERIOR, 4):
            entries = table_for(ac_map, bc_map)
            for r_index, R in enumerate(MATCHINGS[B]):
                Rprime = MATCHINGS[B][1 - r_index]
                word = [C] * 12
                for u in R:
                    word[u] = A
                for u in Rprime:
                    word[u] = B

                terms = exact_terms(tuple(word), entries)
                x = AC_WEIGHTS[R[0]] * AC_WEIGHTS[R[1]]
                P = frozenset(ac_map[u] for u in R)
                image_rprime = frozenset(bc_map[u] for u in Rprime)
                optional = image_rprime in mc_edges and image_rprime != P
                y = BC_WEIGHTS[Rprime[0]] * BC_WEIGHTS[Rprime[1]]
                expected_weights = sorted((x, x * y) if optional else (x,))
                actual_weights = sorted(weight for weight, _ in terms)
                assert actual_weights == expected_weights, (
                    pattern_name,
                    bc_map,
                    R,
                    P,
                    image_rprime,
                    actual_weights,
                    expected_weights,
                    terms,
                )
                checked += 1

    # Independently verify the N=M_c empty-q1 obstruction used to select
    # N=M_b from the three K4 matchings.
    empty_q1_checks = 0
    for targets in target_patterns.values():
        ac_map = ac_map_for(MATCHINGS[C], targets)
        for R in MATCHINGS[C]:
            word = [C] * 12
            for u in R:
                word[u] = A
            # bc entries are irrelevant because no b state is selected.
            terms = exact_terms(tuple(word), table_for(ac_map, (4, 5, 8, 9)))
            expected = AC_WEIGHTS[R[0]] * AC_WEIGHTS[R[1]]
            assert [weight for weight, _ in terms] == [expected]
            empty_q1_checks += 1

    print("target_patterns", len(target_patterns))
    print("bc_injections_per_pattern", 8 * 7 * 6 * 5)
    print("two_term_formula_cases", checked)
    print("empty_q1_N_equals_Mc_checks", empty_q1_checks)
    print("C8_TO_SPLIT_INDEPENDENT_PASS")


if __name__ == "__main__":
    main()
