"""Exact checks for the three-edge-cut form of the GHZ closure face criterion.

For a cubic graph G on 2m vertices with a proper three-edge-colouring this
script enumerates every three-edge cut, the set F of perfect matchings that
cross each such cut exactly once, and the exact rank r of the cut rows
(vertex stars included).  It checks on each instance

* every perfect matching crosses each three-edge cut once or three times,
  and each colour class crosses it once;
* r <= 3m - 2, and dim aff(F) = 3m - r;
* r = 3m - 2  <=>  F is the set of colour classes;
* when F is the set of colour classes, the explicit cut-counting potential
  nu(e) = m * k(e) - K satisfies condition (3) of the closure theorem with
  gap at least 2m, where k(e) counts nontrivial three-edge cuts through e
  and K is their number;
* when F is larger, whether a second proper three-edge-colouring exists
  (an exact non-face certificate that does not use Edmonds' theorem).

Instances: the canonical truncation family n = 4..16 of the closure theorem
(positive), K_{3,3} and the cube (negative controls), and the two WP1 cubic
fixtures of the protected pair-gadget bridge (mechanism probe).

Exact integer/rational arithmetic only.  The script replays the displayed
finite instances; the written note is the argument.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_sibling(filename):
    spec = importlib.util.spec_from_file_location(Path(filename).stem, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(rows):
    rows = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    if not rows:
        return 0
    for column in range(len(rows[0])):
        pivot = next(
            (i for i in range(pivot_row, len(rows)) if rows[i][column] != 0), None
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        lead = rows[pivot_row]
        for i in range(len(rows)):
            if i != pivot_row and rows[i][column] != 0:
                factor = rows[i][column] / lead[column]
                rows[i] = [a - factor * b for a, b in zip(rows[i], lead)]
        pivot_row += 1
    return pivot_row


def perfect_matchings(vertices, adjacency):
    def visit(free):
        if not free:
            yield frozenset()
            return
        u = min(free, key=lambda x: (len(adjacency[x] & free), repr(x)))
        for v in sorted(adjacency[u] & free, key=repr):
            for tail in visit(free - {u, v}):
                yield tail | {frozenset((u, v))}

    yield from visit(frozenset(vertices))


def nontrivial_three_edge_cuts(vertices, adjacency, edges):
    """All edge triples equal to delta(U) with 1 < |U| < |V| - 1."""
    cuts = []
    for triple in itertools.combinations(edges, 3):
        removed = set(triple)
        component = {}
        count = 0
        for start in vertices:
            if start in component:
                continue
            component[start] = count
            stack = [start]
            while stack:
                u = stack.pop()
                for w in adjacency[u]:
                    if frozenset((u, w)) in removed or w in component:
                        continue
                    component[w] = count
                    stack.append(w)
            count += 1
        if count < 2:
            continue
        for mask in range(1, 2 ** count - 1):
            shore = {v for v in vertices if (mask >> component[v]) & 1}
            if not 1 < len(shore) < len(vertices) - 1:
                continue
            if {e for e in edges if len(e & shore) == 1} == removed:
                if len(shore) % 2 != 1:
                    raise AssertionError("three-edge cut with an even shore")
                cuts.append(frozenset(removed))
                break
    return cuts


def analyse(name, colour, expect_face):
    edges = sorted(colour, key=lambda e: sorted(map(repr, e)))
    vertices = sorted(set().union(*edges), key=repr)
    adjacency = {v: set() for v in vertices}
    for edge in edges:
        u, v = tuple(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    if len(vertices) % 2:
        raise AssertionError(f"{name}: odd order")
    m = len(vertices) // 2
    for v in vertices:
        if sorted(colour[e] for e in edges if v in e) != [0, 1, 2]:
            raise AssertionError(f"{name}: not cubic and properly coloured at {v!r}")
    if len(edges) != 3 * m:
        raise AssertionError(f"{name}: edge count")
    classes = [frozenset(e for e in edges if colour[e] == c) for c in range(3)]
    matchings = list(perfect_matchings(vertices, adjacency))
    if len(set(matchings)) != len(matchings):
        raise AssertionError(f"{name}: duplicate matchings")
    if any(cls not in matchings for cls in classes):
        raise AssertionError(f"{name}: colour class is not a perfect matching")

    cuts = nontrivial_three_edge_cuts(vertices, adjacency, edges)
    for matching in matchings:
        for cut in cuts:
            if len(matching & cut) not in (1, 3):
                raise AssertionError(f"{name}: matching crosses a cut evenly")
    for cls in classes:
        if any(len(cls & cut) != 1 for cut in cuts):
            raise AssertionError(f"{name}: colour class crosses a cut three times")
    face = [N for N in matchings if all(len(N & cut) == 1 for cut in cuts)]

    def vector(edge_set):
        return [1 if e in edge_set else 0 for e in edges]

    stars = [frozenset(e for e in edges if v in e) for v in vertices]
    r = rank([vector(row) for row in stars + cuts])
    base = vector(classes[0])
    dim_face = rank([[a - b for a, b in zip(vector(N), base)] for N in face])
    dim_polytope = rank([[a - b for a, b in zip(vector(N), base)] for N in matchings])
    if r > 3 * m - 2:
        raise AssertionError(f"{name}: cut rank exceeds 3m-2")
    if dim_face != 3 * m - r:
        raise AssertionError(f"{name}: dim aff(F) != 3m - r")
    is_face = set(face) == set(classes)
    if is_face != (r == 3 * m - 2) or is_face != (dim_face == 2):
        raise AssertionError(f"{name}: equivalence of the face conditions fails")
    if is_face != expect_face:
        raise AssertionError(f"{name}: expected face={expect_face}, found {is_face}")

    row = {
        "instance": name,
        "vertices": len(vertices),
        "edges": len(edges),
        "perfect_matchings": len(matchings),
        "nontrivial_three_edge_cuts": len(cuts),
        "cut_rank_r": r,
        "three_m_minus_two": 3 * m - 2,
        "matchings_crossing_every_cut_once": len(face),
        "dim_aff_F": dim_face,
        "dim_polytope": dim_polytope,
        "colour_classes_form_face": is_face,
    }
    if is_face:
        through = {e: sum(1 for cut in cuts if e in cut) for e in edges}
        nu = {e: m * through[e] - len(cuts) for e in edges}
        if any(sum(nu[e] for e in cls) != 0 for cls in classes):
            raise AssertionError(f"{name}: cut potential nonzero on a colour class")
        extra = [sum(nu[e] for e in N) for N in matchings if N not in classes]
        if extra and min(extra) < 2 * m:
            raise AssertionError(f"{name}: cut potential gap below 2m")
        row["cut_potential_min_extra"] = min(extra) if extra else None
    else:
        others = [N for N in matchings if N not in classes]
        second = any(
            not (A & B) and frozenset(edges) - A - B in matchings
            for A, B in itertools.combinations(others, 2)
        )
        row["second_three_edge_colouring"] = second
    return row, matchings, classes, face


def k33():
    return {frozenset((i, 3 + j)): (i + j) % 3 for i in range(3) for j in range(3)}


def cube():
    return {
        frozenset((v, v ^ (1 << bit))): bit
        for v in range(8)
        for bit in range(3)
        if not v & (1 << bit)
    }


def wp1_probe(bridge, name, protected, gadgets):
    vertices, adjacency, edge_data, _ = bridge.build_h(protected, gadgets)
    colour = {edge: data[1] for edge, data in edge_data.items()}
    row, matchings, classes, face = analyse(name, colour, expect_face=False)
    components = sorted({u // 4 for _, a, b in protected.values() for u in (a, b)})

    def in_target_class(N):
        word = bridge.h_pm_to_word(N, edge_data)
        q = bridge.q_vector(word, protected)
        constant = all(
            len({word[u] for u in range(4 * k, 4 * k + 4)}) == 1 for k in components
        )
        return constant or min(q) <= 1

    extra_all = [N for N in matchings if N not in classes]
    extra_face = [N for N in face if N not in classes]
    row["extra_matchings"] = len(extra_all)
    row["extra_matchings_in_wp1_target_class"] = sum(map(in_target_class, extra_all))
    row["extra_matchings_crossing_every_cut_once"] = len(extra_face)
    row["of_those_in_wp1_target_class"] = sum(map(in_target_class, extra_face))
    return row


def main() -> None:
    closure = load_sibling(
        "verify_ghz_closure_matching_polytope_face_asymptotic_realizability.py"
    )
    bridge = load_sibling("verify_protected_pair_gadget_cubic_bridge.py")
    rows = []
    orders = []
    for n, colour, _, _ in closure.canonical_family(16):
        row, _, _, _ = analyse(f"canonical truncation family n={n}", colour, True)
        orders.append(n)
        rows.append(row)
    if orders != list(range(4, 17, 2)):
        raise AssertionError("family does not cover n = 4..16")
    prism = rows[1]
    if (prism["perfect_matchings"], prism["nontrivial_three_edge_cuts"]) != (4, 1):
        raise AssertionError("six-vertex member is not the prism")
    for name, colour in (("K_{3,3} control", k33()), ("cube control", cube())):
        row, _, _, _ = analyse(name, colour, False)
        if row["nontrivial_three_edge_cuts"] != 0 or not row["second_three_edge_colouring"]:
            raise AssertionError(f"{name}: unexpected control data")
        rows.append(row)
    expected = {
        "WP1 two-K4 literal table": (20, 30, 30, 10, 27, 24),
        "WP1 three-K4 triangle": (30, 45, 160, 15, 157, 56),
    }
    fixtures = (
        ("WP1 two-K4 literal table", bridge.abstract_pairing_fixture()),
        ("WP1 three-K4 triangle", bridge.nonbipartite_triangle_fixture()),
    )
    for name, (protected, gadgets) in fixtures:
        row = wp1_probe(bridge, name, protected, gadgets)
        found = (
            row["vertices"], row["edges"], row["perfect_matchings"],
            row["dim_aff_F"], row["extra_matchings"],
            row["extra_matchings_in_wp1_target_class"],
        )
        if found != expected[name]:
            raise AssertionError(f"{name}: expected {expected[name]}, found {found}")
        if row["nontrivial_three_edge_cuts"] != 0:
            raise AssertionError(f"{name}: unexpected nontrivial three-edge cut")
        if row["matchings_crossing_every_cut_once"] != row["perfect_matchings"]:
            raise AssertionError(f"{name}: cut filter is not vacuous")
        if row["dim_aff_F"] != row["dim_polytope"]:
            raise AssertionError(f"{name}: F is not full-dimensional in the polytope")
        rows.append(row)
    for row in rows:
        print(json.dumps(row))
    print(
        "VERIFIED: three-edge-cut face criterion on the canonical family n = 4..16, "
        "two negative controls, and the two WP1 cubic fixtures"
    )


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"FAILED: {error}")
        sys.exit(1)
