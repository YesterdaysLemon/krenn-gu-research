#!/usr/bin/env python3
"""Independent exact replay of the literal weighted macro/DAG control.

The checker reads only the literal 72-entry repository fixture and
uses Fraction arithmetic.  It does not import the search or derivation code.
"""

from __future__ import annotations

from collections import defaultdict, deque
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, _HERE = bootstrap(__file__)
FIXTURE = REPO_ROOT / "tests/fixtures/protected_twelve_vertex_weighted_macro_dag_control.json"
N = 12


def protected_colour(u: int, v: int) -> int:
    assert u // 4 == v // 4 and u != v
    return (u % 4 ^ v % 4) - 1


def partner(v: int, c: int) -> int:
    return 4 * (v // 4) + ((v % 4) ^ (c + 1))


def protected_pairs(c: int):
    for v in range(N):
        w = partner(v, c)
        if v < w:
            yield v, w


def q_c(word, c: int) -> int:
    return sum(word[u] != c and word[v] != c for u, v in protected_pairs(c))


def build_weighted_edges(crossing_entries):
    edges = []
    for base in (0, 4, 8):
        for u, v in itertools.combinations(range(base, base + 4), 2):
            c = protected_colour(u, v)
            edges.append((u, v, c, c, Fraction(1), "protected"))
    for entry in crossing_entries:
        i = entry["source_index"]
        u, v, a, b = (entry[k] for k in ("u", "v", "a", "b"))
        weight = Fraction(entry["weight"])
        assert weight
        edges.append((u, v, a, b, weight, f"x{i}"))
    return edges


def coefficient(word, edges, with_terms=False):
    incident = defaultdict(list)
    for edge in edges:
        u, v, a, b, weight, name = edge
        if word[u] == a and word[v] == b:
            incident[u].append((v, weight, name))
            incident[v].append((u, weight, name))
    full = (1 << N) - 1
    total = Fraction(0)
    terms = []

    def visit(mask, value, names):
        nonlocal total
        if mask == full:
            total += value
            if with_terms:
                terms.append((tuple(names), value))
            return
        free = (~mask) & full
        u = (free & -free).bit_length() - 1
        for v, weight, name in incident[u]:
            if mask & (1 << v):
                continue
            names.append(name)
            visit(mask | (1 << u) | (1 << v), value * weight, names)
            names.pop()

    visit(0, Fraction(1), [])
    return total, terms


def arcs_for_majority(edges, c):
    arcs = set()
    for u, v, a, b, _, provenance in edges:
        if provenance == "protected":
            continue
        if b == c and a != c:
            arcs.add((u, partner(v, c)))
        if a == c and b != c:
            arcs.add((v, partner(u, c)))
    return arcs


def kahn_order(arcs):
    outgoing = defaultdict(list)
    indegree = [0] * N
    for u, v in sorted(arcs):
        outgoing[u].append(v)
        indegree[v] += 1
    ready = deque(i for i, d in enumerate(indegree) if d == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in outgoing[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
    assert len(order) == N, (arcs, order)
    return order


def main():
    fixture_bytes = FIXTURE.read_bytes()
    raw = json.loads(fixture_bytes.decode("utf-8"))
    assert raw["schema"] == "k3-weighted-macro-dag-countercontrol-v1"
    crossing_entries = raw["crossing_entries"]
    assert len(crossing_entries) == 72
    source_indices = [x["source_index"] for x in crossing_entries]
    assert len(set(source_indices)) == 72
    physical_entries = [(x["u"], x["v"], x["a"], x["b"]) for x in crossing_entries]
    assert len(set(physical_entries)) == 72
    for u, v, a, b in physical_entries:
        assert 0 <= u < v < N and u // 4 != v // 4
        assert 0 <= a < 3 and 0 <= b < 3 and a != b
    weights = [Fraction(x["weight"]) for x in crossing_entries]
    assert all(weights)

    edges = build_weighted_edges(crossing_entries)

    dag_data = {}
    for c in range(3):
        arcs = arcs_for_majority(edges, c)
        dag_data[c] = {"arcs": len(arcs), "order": kahn_order(arcs)}

    macro = {}
    for labels in itertools.product(range(3), repeat=3):
        word = tuple(labels[v // 4] for v in range(N))
        value, terms = coefficient(word, edges, with_terms=True)
        target = Fraction(1) if len(set(labels)) == 1 else Fraction(0)
        assert value == target, (labels, value, terms)
        macro["".join(map(str, labels))] = {
            "coefficient": str(value),
            "terms": len(terms),
        }

    # A target-zero non-macro source row that explicitly fails.  In the full
    # 78-entry domain this is the sealed splice row; deletion preserves its
    # sole matching and its coefficient here is exactly -1.
    failing_word = tuple(map(int, "121011111221"))
    assert q_c(failing_word, 1) == 1
    assert [(u, v) for u, v in protected_pairs(1)
            if failing_word[u] != 1 and failing_word[v] != 1] == [(1, 3)]
    failure, failure_terms = coefficient(failing_word, edges, with_terms=True)
    assert failure == -1
    assert len(failure_terms) == 1
    crossing_names = tuple(x for x in failure_terms[0][0] if x != "protected")
    assert crossing_names == ("x16", "x46")

    result = {
        "status": "EXACT_WEIGHTED_MACRO_DAG_COUNTERCONTROL",
        "scope": "component-constant coefficient equations only; not a full-source witness",
        "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "source_78_sha256_from_fixture": raw["source_78_sha256"],
        "retained_crossing_entries": len(crossing_entries),
        "deleted_source_indices_from_fixture": raw["deleted_source_indices"],
        "nonunit_weights": {
            str(x["source_index"]): x["weight"]
            for x in crossing_entries if Fraction(x["weight"]) != 1
        },
        "whole_D": dag_data,
        "macro": macro,
        "explicit_full_source_failure": {
            "word": "1210|1111|1221",
            "majority": 1,
            "q_majority": 1,
            "complete_minority_pair": [1, 3],
            "coefficient": str(failure),
            "crossing_factors": crossing_names,
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
