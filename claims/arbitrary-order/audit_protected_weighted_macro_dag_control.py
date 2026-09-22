#!/usr/bin/env python3
"""Standalone audit of the literal 72-entry weighted macro/DAG control.

This standard-library checker reads only the literal JSON fixture.  It does
not import search, derivation, or primary verification code.  Its coefficient
engine first generates every unlabelled perfect matching of twelve vertices,
then filters and weights that fixed list for each requested color word.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, _HERE = bootstrap(__file__)
FIXTURE = REPO_ROOT / "tests/fixtures/protected_twelve_vertex_weighted_macro_dag_control.json"
VERTICES = tuple(range(12))
COLORS = (0, 1, 2)
DELETED = {12, 15, 48, 61, 71, 74}


def all_perfect_matchings(vertices):
    """Generate each unlabelled perfect matching exactly once."""
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in all_perfect_matchings(remainder):
            yield ((first, second),) + tail


def local_partner(vertex, color):
    base = 4 * (vertex // 4)
    return base + ((vertex % 4) ^ (color + 1))


def protected_literals():
    """Return the exact protected unit-K4 scalar dictionary."""
    result = {}
    for base in (0, 4, 8):
        for u, v in combinations(range(base, base + 4), 2):
            color = ((u - base) ^ (v - base)) - 1
            assert color in COLORS
            result[(u, v, color, color)] = Fraction(1)
    assert len(result) == 18
    return result


def parse_fixture():
    raw_bytes = FIXTURE.read_bytes()
    raw = json.loads(raw_bytes.decode("utf-8"))
    assert raw["schema"] == "k3-weighted-macro-dag-countercontrol-v1"
    entries = raw["crossing_entries"]
    assert len(entries) == 72
    assert raw["deleted_source_indices"] == sorted(DELETED)

    indices = [entry["source_index"] for entry in entries]
    assert len(set(indices)) == 72
    assert set(indices) == set(range(78)) - DELETED

    crossing = {}
    provenance = {}
    for entry in entries:
        assert set(entry) == {"source_index", "u", "v", "a", "b", "weight"}
        index = entry["source_index"]
        u, v = entry["u"], entry["v"]
        a, b = entry["a"], entry["b"]
        weight = Fraction(entry["weight"])
        assert 0 <= u < v < 12
        assert u // 4 != v // 4  # physical hollowness across K4 components
        assert a in COLORS and b in COLORS and a != b  # color-hollow block
        assert weight != 0
        key = (u, v, a, b)
        assert key not in crossing
        crossing[key] = weight
        provenance[key] = index
    assert len(crossing) == 72
    return raw_bytes, raw, crossing, provenance


def term_for_matching(matching, word, scalar_weights, provenance):
    value = Fraction(1)
    crossing_indices = []
    for u, v in matching:
        key = (u, v, word[u], word[v])
        weight = scalar_weights.get(key)
        if weight is None:
            return None
        value *= weight
        if key in provenance:
            crossing_indices.append(provenance[key])
    return value, tuple(crossing_indices)


def evaluate_word(matchings, word, scalar_weights, provenance):
    terms = []
    for matching in matchings:
        term = term_for_matching(matching, word, scalar_weights, provenance)
        if term is not None:
            value, crossing_indices = term
            terms.append((matching, value, crossing_indices))
    return sum((value for _, value, _ in terms), Fraction(0)), terms


def arcs_for_color(crossing, color):
    arcs = set()
    for u, v, a, b in crossing:
        if b == color and a != color:
            arcs.add((u, local_partner(v, color)))
        if a == color and b != color:
            arcs.add((v, local_partner(u, color)))
    return arcs


def dfs_topological_order(arcs):
    """Reject a directed cycle using three-state DFS; return a topo order."""
    outgoing = {vertex: [] for vertex in VERTICES}
    for source, target in sorted(arcs):
        outgoing[source].append(target)
    state = [0] * 12  # 0 unseen, 1 active, 2 finished
    finish = []

    def visit(vertex):
        assert state[vertex] != 1, f"directed cycle reaches {vertex}"
        if state[vertex] == 2:
            return
        state[vertex] = 1
        for target in outgoing[vertex]:
            visit(target)
        state[vertex] = 2
        finish.append(vertex)

    for vertex in VERTICES:
        if state[vertex] == 0:
            visit(vertex)
    order = tuple(reversed(finish))
    position = {vertex: i for i, vertex in enumerate(order)}
    assert all(position[source] < position[target] for source, target in arcs)
    return order


def complete_minority_pairs(word, background):
    pairs = []
    for vertex in VERTICES:
        mate = local_partner(vertex, background)
        if vertex < mate and word[vertex] != background and word[mate] != background:
            pairs.append((vertex, mate))
    return pairs


def main():
    raw_bytes, raw, crossing, provenance = parse_fixture()
    protected = protected_literals()
    assert set(protected).isdisjoint(crossing)
    scalar_weights = dict(protected)
    scalar_weights.update(crossing)
    assert len(scalar_weights) == 90

    matchings = tuple(all_perfect_matchings(VERTICES))
    assert len(matchings) == 10395
    assert len(set(matchings)) == 10395
    assert all(
        sorted(vertex for edge in matching for vertex in edge) == list(VERTICES)
        for matching in matchings
    )

    arc_counts = {}
    orders = {}
    for color, expected_count in enumerate((33, 38, 37)):
        arcs = arcs_for_color(crossing, color)
        assert len(arcs) == expected_count
        arc_counts[color] = len(arcs)
        orders[color] = dfs_topological_order(arcs)

    macro_term_counts = {}
    for component_colors in product(COLORS, repeat=3):
        word = tuple(component_colors[vertex // 4] for vertex in VERTICES)
        coefficient, terms = evaluate_word(
            matchings, word, scalar_weights, provenance
        )
        target = Fraction(1) if len(set(component_colors)) == 1 else Fraction(0)
        assert coefficient == target, (component_colors, coefficient)
        macro_term_counts["".join(map(str, component_colors))] = len(terms)

    assert Counter(macro_term_counts.values()) == Counter(
        {1: 3, 2: 14, 3: 6, 5: 1, 9: 1, 10: 1, 11: 1}
    )

    witness = tuple(int(digit) for digit in "121011111221")
    minority_pairs = complete_minority_pairs(witness, background=1)
    assert minority_pairs == [(1, 3)]
    coefficient, terms = evaluate_word(matchings, witness, scalar_weights, provenance)
    assert coefficient == Fraction(-1)
    assert len(terms) == 1
    matching, value, crossing_indices = terms[0]
    assert value == Fraction(-1)
    assert crossing_indices == (16, 46)
    assert matching == ((0, 2), (1, 11), (3, 8), (4, 6), (5, 7), (9, 10))

    receipt = {
        "status": "WEIGHTED_MACRO_DAG_INDEPENDENT_AUDIT_PASS",
        "fixture_sha256": sha256(raw_bytes).hexdigest(),
        "perfect_matchings": len(matchings),
        "protected_literals": len(protected),
        "crossing_literals": len(crossing),
        "arc_counts": arc_counts,
        "dfs_orders": orders,
        "macro_term_counts": macro_term_counts,
        "witness": {
            "word": "1210|1111|1221",
            "background": 1,
            "q": len(minority_pairs),
            "minority_pairs": minority_pairs,
            "terms": len(terms),
            "coefficient": str(coefficient),
            "crossing_indices": crossing_indices,
            "matching": matching,
        },
        "scope": raw["scope"],
    }
    receipt_text = json.dumps(receipt, indent=2) + "\n"
    print(receipt_text, end="")


if __name__ == "__main__":
    main()
