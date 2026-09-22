"""Exact k=3 C9-square search modulo color-preserving K4 translations.

Color-1 literals are split, as forced by the nontriangle macro row.  Color-0
and color-2 literals may be split or coincident.  The color-preserving Klein
four group on each K4 flips an even subset of the three protected-pair
indices.  We gauge-fix the first color-0 and color-1 incidence at every
component, leaving 8^3 allocation representatives.  All endpoint bijections
are then enumerated.  Hidden Q1 alignment is imposed at every coincident
color-0/2 literal, and literal scalar matching terms are grouped by word.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product


K = 3
COLORS = range(3)
M_LOCAL = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}


def node(component, color):
    return 3 * component + color


def node_data(t):
    return divmod(t, 3)


def build_f_edges():
    neighbors = {t: set() for t in range(3 * K)}
    for A in range(K):
        listed = {
            0: ((A - 1) % K, 1, (A - 1) % K, 2),
            1: ((A - 1) % K, 2, (A + 1) % K, 0),
            2: ((A + 1) % K, 0, (A + 1) % K, 1),
        }
        for a, flat in listed.items():
            t = node(A, a)
            for i in (0, 2):
                u = node(flat[i], flat[i + 1])
                neighbors[t].add(u)
                neighbors[u].add(t)
    assert {len(v) for v in neighbors.values()} == {2}
    edges = sorted({tuple(sorted((t, u))) for t, ns in neighbors.items() for u in ns})
    assert len(edges) == 9
    return edges, neighbors


F_EDGES, F_NEIGHBORS = build_f_edges()
INCIDENT = {t: tuple(i for i, e in enumerate(F_EDGES) if t in e) for t in range(9)}


def physical_pair(t, choice):
    A, a = node_data(t)
    return tuple(4 * A + p for p in M_LOCAL[a][choice])


def verify_gauge_action():
    flips = set()
    for delta in range(4):
        vector = []
        for c in COLORS:
            images = {tuple(sorted((x ^ delta, y ^ delta))) for x, y in M_LOCAL[c]}
            assert images == {tuple(sorted(edge)) for edge in M_LOCAL[c]}
            first_image = tuple(sorted((M_LOCAL[c][0][0] ^ delta, M_LOCAL[c][0][1] ^ delta)))
            vector.append(0 if first_image == tuple(sorted(M_LOCAL[c][0])) else 1)
        flips.add(tuple(vector))
    assert flips == {(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)}


def pair_choices(bits):
    """Three free bits per component after the Klein-four gauge fixing."""
    choice = {}
    for A in range(K):
        t0, t1, t2 = (node(A, a) for a in COLORS)
        e00, e01 = INCIDENT[t0]
        e10, e11 = INCIDENT[t1]
        e20, e21 = INCIDENT[t2]
        # Gauge: first incidences at colors 0 and 1 use pair index zero.
        choice[(t0, e00)] = 0
        choice[(t0, e01)] = (bits >> (3 * A)) & 1
        choice[(t1, e10)] = 0
        choice[(t1, e11)] = 1  # color 1 is split.
        choice[(t2, e20)] = (bits >> (3 * A + 1)) & 1
        choice[(t2, e21)] = (bits >> (3 * A + 2)) & 1
    return choice


def edge_maps(choice, map_bits):
    """Return directed endpoint maps for each incidence of every F edge."""
    maps = {}
    for i, (t, u) in enumerate(F_EDGES):
        rt = physical_pair(t, choice[(t, i)])
        ru = physical_pair(u, choice[(u, i)])
        if (map_bits >> i) & 1:
            image = (ru[1], ru[0])
        else:
            image = ru
        fwd = dict(zip(rt, image))
        maps[(t, i)] = fwd
        maps[(u, i)] = {v: k for k, v in fwd.items()}
    return maps


def hidden_alignment_holds(choice, maps):
    for t in range(9):
        _, a = node_data(t)
        e0, e1 = INCIDENT[t]
        if a == 1 or choice[(t, e0)] != choice[(t, e1)]:
            continue
        u = next(x for x in F_EDGES[e0] if x != t)
        v = next(x for x in F_EDGES[e1] if x != t)
        Bu, _ = node_data(u)
        Bv, _ = node_data(v)
        assert Bu == Bv
        su = set(physical_pair(u, choice[(u, e0)]))
        sv = set(physical_pair(v, choice[(v, e1)]))
        shared = su & sv
        assert len(shared) == 1
        pu = next(iter(su - shared))
        pv = next(iter(sv - shared))
        inv_u = {target: root for root, target in maps[(t, e0)].items()}
        inv_v = {target: root for root, target in maps[(t, e1)].items()}
        if inv_u[pu] != inv_v[pv]:
            return False
    return True


def is_transit(choice, t):
    e0, e1 = INCIDENT[t]
    return choice[(t, e0)] == choice[(t, e1)]


def scalar_edges(choice, maps):
    edges = []
    for A in range(K):
        for c in COLORS:
            for x, y in M_LOCAL[c]:
                edges.append((4 * A + x, 4 * A + y, c, c, 1, f"P{A}{c}:{x}{y}"))
    for i, (t, u) in enumerate(F_EDGES):
        rt = physical_pair(t, choice[(t, i)])
        fwd = maps[(t, i)]
        _, ct = node_data(t)
        _, cu = node_data(u)
        for lane, p in enumerate(rt):
            q = fwd[p]
            weight = 1 if lane == 0 else -1
            if p < q:
                edges.append((p, q, ct, cu, weight, f"X{i}:{t}-{u}:{p}-{q}"))
            else:
                edges.append((q, p, cu, ct, weight, f"X{i}:{t}-{u}:{p}-{q}"))
    keys = [(x, y, cx, cy) for x, y, cx, cy, _, _ in edges]
    assert len(keys) == len(set(keys)) == 36
    return edges


def q_vector(word):
    values = []
    for c in COLORS:
        q = 0
        for A in range(K):
            for x, y in M_LOCAL[c]:
                if word[4 * A + x] != c and word[4 * A + y] != c:
                    q += 1
        values.append(q)
    return tuple(values)


def classify_terms(edges):
    full = (1 << 12) - 1
    adjacency = defaultdict(list)
    for index, (x, y, _, _, _, _) in enumerate(edges):
        adjacency[x].append(index)
        adjacency[y].append(index)
    word = [-1] * 12
    counts = defaultdict(int)
    coefficients = defaultdict(int)
    witnesses = {}

    def visit(mask, coefficient, names):
        if mask == full:
            w = tuple(word)
            counts[w] += 1
            coefficients[w] += coefficient
            witnesses.setdefault(w, tuple(names))
            return
        u = next(v for v in range(12) if not ((mask >> v) & 1))
        for edge_index in adjacency[u]:
            x, y, cx, cy, weight, name = edges[edge_index]
            v = y if x == u else x
            if (mask >> v) & 1:
                continue
            cu, cv = (cx, cy) if x == u else (cy, cx)
            assert word[u] == word[v] == -1
            word[u], word[v] = cu, cv
            visit(mask | (1 << u) | (1 << v), coefficient * weight, names + [name])
            word[u] = word[v] = -1

    visit(0, 1, [])
    unique_low = []
    for w, count in counts.items():
        if count != 1 or len(set(w)) == 1:
            continue
        q = q_vector(w)
        if min(q) <= 1:
            unique_low.append((w, q, witnesses[w]))
    macro_counts = {}
    for colors in product(COLORS, repeat=K):
        w = tuple(c for c in colors for _ in range(4))
        macro_counts[colors] = counts[w]
    assert all(macro_counts[c] == 1 for c in ((0, 0, 0), (1, 1, 1), (2, 2, 2)))
    assert all(count >= 2 for colors, count in macro_counts.items() if len(set(colors)) > 1)
    assert all(coefficients[tuple(c for c in colors for _ in range(4))] ==
               (1 if len(set(colors)) == 1 else 0)
               for colors in product(COLORS, repeat=K))
    return counts, unique_low, macro_counts


def main():
    verify_gauge_action()
    independent_transversals = []
    for colors in product(COLORS, repeat=K):
        selected = {node(A, colors[A]) for A in range(K)}
        if not any(t in selected and u in selected for t, u in F_EDGES):
            independent_transversals.append(colors)
    assert independent_transversals == [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
    aligned = 0
    checked = 0
    adjacent_hidden_pair_allocations = 0
    passing = []
    q_hist = defaultdict(int)
    sample_failures = []
    for pair_bits in range(1 << 9):
        choice = pair_choices(pair_bits)
        if any(is_transit(choice, t) and is_transit(choice, u) for t, u in F_EDGES):
            adjacent_hidden_pair_allocations += 1
            continue
        for map_bits in range(1 << 9):
            maps = edge_maps(choice, map_bits)
            if not hidden_alignment_holds(choice, maps):
                continue
            aligned += 1
            edges = scalar_edges(choice, maps)
            counts, unique_low, _macro = classify_terms(edges)
            checked += 1
            if not unique_low:
                passing.append((pair_bits, map_bits, sum(counts.values()), len(counts)))
                print("P1_SUPPORT_CANDIDATE", passing[-1], flush=True)
            else:
                first = unique_low[0]
                q_hist[first[1]] += 1
                if len(sample_failures) < 8:
                    sample_failures.append((pair_bits, map_bits, first))
    print("F_edges", F_EDGES)
    print("gauge_fixed_raw_configurations", (1 << 18))
    print("adjacent_hidden_pair_allocations_excluded_analytically",
          adjacent_hidden_pair_allocations)
    print("raw_isolated_hidden_configurations",
          ((1 << 9) - adjacent_hidden_pair_allocations) * (1 << 9))
    print("q1_aligned_configurations", aligned)
    print("independent_transversals", independent_transversals)
    print("checked_scalar_supports", checked)
    print("first_failure_q_histogram", dict(sorted(q_hist.items())))
    print("sample_failures", sample_failures)
    print("passing_configurations", len(passing))
    if passing:
        print("passing_rows", passing[:20])
        print("C9_P1_SUPPORT_FOUND")
    else:
        print("C9_FAMILY_EXCLUDED")


if __name__ == "__main__":
    main()
