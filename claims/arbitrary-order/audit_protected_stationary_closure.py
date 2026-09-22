#!/usr/bin/env python3
"""Audit stationary one-pair closure repairs in two sharp finite controls.

The audit classifies literal ``q_c=1`` matching terms in the accepted v3
Laurent control and the twelve-vertex Boolean macro-cycle control.  It reuses
the standalone literal enumerator from ``audit_protected_macro_cycle_control``;
it is therefore a companion audit, not an independent implementation of that
enumerator.  It imports no common-minor formula verifier.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, _HERE = bootstrap(__file__)

from audit_protected_macro_cycle_control import (  # noqa: E402
    DEFAULT_FIXTURE as TWELVE_VERTEX_FIXTURE,
    collision_count,
    directed_arcs,
    enumerate_terms,
    load_fixture,
    protected_color,
    protected_partner,
    topological_order,
)


V3_FIXTURE = REPO_ROOT / "tests/fixtures/eight_vertex_scaffold_subsystem_controls.json"


def scalar_edges(component_count: int, crossing_support):
    """Construct implicit protected entries and supplied crossing entries."""

    edges = []
    for component in range(component_count):
        block = range(4 * component, 4 * component + 4)
        for u, v in itertools.combinations(block, 2):
            color = protected_color(u, v)
            edges.append((u, v, color, color, "protected"))
    edges.extend((*entry, "literal-crossing") for entry in crossing_support)
    return edges


def load_v3_fixture(path: Path = V3_FIXTURE):
    """Return the v3 literal support and its exact Laurent edge weights."""

    data = json.loads(path.read_text(encoding="utf-8"))
    family = next(
        item
        for item in data["families"]
        if item["name"] == "independent_minorities_and_component_constants_v3"
    )
    support = []
    weights = {}
    width = len(data["parameter_order"])
    for index, ((color_u, color_v), positions) in enumerate(
        zip(data["parameter_order"], family["supports"], strict=True)
    ):
        assert len(positions) == 2
        for which, (left, right) in enumerate(positions):
            entry = (left, right + 4, color_u, color_v)
            support.append(entry)
            exponent = [0] * width
            exponent[index] = 1 if which == 0 else -1
            weights[entry] = (1 if which == 0 else -1, tuple(exponent))
    assert len(support) == 12 and len(set(support)) == 12
    return support, weights


def q1_signature(word, chosen, edges, majority: int):
    """Classify one literal ``q=1`` term by closure and directed path lengths."""

    vertex_count = len(word)
    pairs = [
        (u, protected_partner(u, majority))
        for u in range(vertex_count)
        if u < protected_partner(u, majority)
    ]
    complete = [
        (u, v) for u, v in pairs if word[u] != majority and word[v] != majority
    ]
    if len(complete) != 1:
        raise ValueError("q1 signature requires exactly one complete minority pair")
    x, y = complete[0]
    singles = []
    clean = []
    for u, v in pairs:
        flags = word[u] != majority, word[v] != majority
        if sum(flags) == 1:
            singles.append(u if flags[0] else v)
        elif not any(flags):
            clean.append((u, v))

    boundary_vertices = set(singles) | {x, y}
    selected = [edges[edge_id] for edge_id in chosen]
    selected_pairs = {tuple(sorted((u, v))) for u, v, *_ in selected}
    direct = [
        (u, v)
        for u, v, *_ in selected
        if u in boundary_vertices and v in boundary_vertices
    ]
    opened = [edge for edge in clean if tuple(sorted(edge)) not in selected_pairs]
    assert len(direct) + len(opened) == 1

    if direct:
        boundary = tuple(sorted(direct[0]))
        closure = "direct"
    else:
        z, zbar = opened[0]
        mates = {}
        for u, v, *_ in selected:
            if u in (z, zbar):
                mates[u] = v
            if v in (z, zbar):
                mates[v] = u
        boundary = tuple(sorted((mates[z], mates[zbar])))
        assert all(vertex in boundary_vertices for vertex in boundary)
        closure = "resource"

    arcs = {}
    for u, v, *_ in selected:
        if u in boundary_vertices:
            sink = protected_partner(v, majority)
            if sink in singles:
                arcs[u] = sink
        if v in boundary_vertices:
            sink = protected_partner(u, majority)
            if sink in singles:
                arcs[v] = sink
    for vertex in boundary:
        arcs.pop(vertex, None)

    lengths = []
    for source in (x, y):
        if source in boundary:
            lengths.append(0)
            continue
        current = source
        length = 0
        seen = set()
        while current in arcs:
            assert current not in seen
            seen.add(current)
            current = arcs[current]
            length += 1
        assert current in boundary
        lengths.append(length)
    assert sum(lengths) == len(singles)
    boundary_types = tuple(
        sorted("special" if vertex in (x, y) else "sink" for vertex in boundary)
    )
    return closure, boundary_types, tuple(sorted(lengths)), len(singles)


def term_laurent(chosen, edges, weights):
    """Evaluate one v3 term as ``(integer coefficient, exponent vector)``."""

    coefficient = 1
    exponent = [0] * 6
    for edge_id in chosen:
        u, v, color_u, color_v, kind = edges[edge_id]
        if kind == "protected":
            continue
        factor_coefficient, factor_exponent = weights[(u, v, color_u, color_v)]
        coefficient *= factor_coefficient
        exponent = [
            left + right
            for left, right in zip(exponent, factor_exponent, strict=True)
        ]
    return coefficient, tuple(exponent)


def analyze_control(
    name: str,
    component_count: int,
    crossing_support,
    stationary_word: tuple[int, ...],
    stationary_majority: int,
    *,
    weights=None,
):
    """Return the exact q1/path/minimality receipt for one finite control."""

    vertex_count = 4 * component_count
    edges = scalar_edges(component_count, crossing_support)
    terms = enumerate_terms(edges, vertex_count)
    by_word = defaultdict(list)
    for word, chosen in terms:
        by_word[word].append(chosen)

    mixed_macros = []
    for labels in itertools.product(range(3), repeat=component_count):
        if len(set(labels)) == 1:
            continue
        word = tuple(labels[vertex // 4] for vertex in range(vertex_count))
        choices = [
            chosen
            for chosen in by_word[word]
            if any(edges[edge_id][4] == "literal-crossing" for edge_id in chosen)
        ]
        assert choices
        mixed_macros.append((labels, choices))

    crossing_ids = [
        edge_id for edge_id, edge in enumerate(edges) if edge[4] == "literal-crossing"
    ]
    deletable = [
        edges[edge_id][:4]
        for edge_id in crossing_ids
        if all(
            any(edge_id not in choice for choice in choices)
            for _labels, choices in mixed_macros
        )
    ]
    assert deletable == []

    q1_instances = []
    q1_unique = []
    for word, choices in by_word.items():
        if len(set(word)) == 1:
            continue
        for majority in range(3):
            if collision_count(word, majority) != 1:
                continue
            signatures = [
                q1_signature(word, chosen, edges, majority) for chosen in choices
            ]
            q1_instances.append((word, majority, signatures))
            if len(choices) == 1:
                q1_unique.append((word, majority, signatures[0]))

    stationary_signatures = next(
        signatures
        for word, majority, signatures in q1_instances
        if word == stationary_word and majority == stationary_majority
    )
    assert stationary_signatures == [
        ("direct", ("sink", "special"), (0, 2), 2),
        ("resource", ("sink", "special"), (0, 2), 2),
    ]
    stationary_choices = by_word[stationary_word]
    stationary_terms = [
        tuple(edges[edge_id][:4] for edge_id in chosen)
        for chosen in stationary_choices
    ]

    dag_receipt = []
    for majority in range(3):
        arcs = directed_arcs(crossing_support, majority)
        order = topological_order(vertex_count, arcs)
        dag_receipt.append(
            {
                "majority": majority,
                "arc_count": len(arcs),
                "is_DAG": order is not None,
            }
        )

    receipt = {
        "name": name,
        "literal_crossing_entries": len(crossing_support),
        "supported_terms": len(terms),
        "supported_words": len(by_word),
        "D_c": dag_receipt,
        "macro_inclusion_deletable_entries": len(deletable),
        "q1_supported_word_majorities": len(q1_instances),
        "q1_unique_word_majorities": len(q1_unique),
        "q1_unique_signature_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(item[2] for item in q1_unique).items(), key=lambda item: str(item[0])
            )
        },
        "stationary_word": stationary_word,
        "stationary_majority": stationary_majority,
        "stationary_signatures": stationary_signatures,
        "stationary_terms": stationary_terms,
    }

    if weights is not None:
        laurent_terms = [
            term_laurent(chosen, edges, weights) for chosen in stationary_choices
        ]
        assert len(laurent_terms) == 2
        assert laurent_terms[0][1] == laurent_terms[1][1]
        assert laurent_terms[0][0] == -laurent_terms[1][0]
        receipt["stationary_laurent_terms"] = laurent_terms
        receipt["stationary_laurent_sum"] = 0
    return receipt


def audit() -> dict[str, object]:
    """Audit both sharp controls and assert their reviewed finite receipts."""

    v3_support, v3_weights = load_v3_fixture()
    v3 = analyze_control(
        "eight_vertex_v3",
        2,
        v3_support,
        tuple(map(int, "00122212")),
        2,
        weights=v3_weights,
    )
    assert (v3["supported_terms"], v3["supported_words"]) == (60, 45)
    assert (v3["q1_supported_word_majorities"], v3["q1_unique_word_majorities"]) == (
        30,
        24,
    )

    _fixture_bytes, twelve_support = load_fixture(TWELVE_VERTEX_FIXTURE)
    twelve = analyze_control(
        "twelve_vertex_macro_cycle",
        3,
        twelve_support,
        tuple(map(int, "000000202202")),
        0,
    )
    assert (twelve["supported_terms"], twelve["supported_words"]) == (605, 401)
    assert (
        twelve["q1_supported_word_majorities"],
        twelve["q1_unique_word_majorities"],
    ) == (62, 56)
    assert [entry["arc_count"] for entry in twelve["D_c"]] == [12, 13, 13]
    assert all(entry["is_DAG"] for entry in twelve["D_c"])

    return {
        "controls": [v3, twelve],
        "scope": (
            "finite exact stationary-closure controls; no P1, SFULL, or "
            "Krenn-Gu resolution"
        ),
        "status": "PROTECTED_STATIONARY_CLOSURE_AUDIT_PASS",
    }


def main() -> None:
    print(json.dumps(audit(), indent=2))


if __name__ == "__main__":
    main()
