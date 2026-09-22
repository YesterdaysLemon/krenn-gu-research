#!/usr/bin/env python3
"""Independent literal audit of the twelve-vertex macro-cycle control.

The audit reads only the durable 22-entry Boolean fixture, adds the implicit
protected unit entries, and uses a standalone lowest-free-vertex perfect-
matching recursion.  It imports none of the one-/two-pair formula verifiers
or the exploratory generator.  This independence concerns the finite replay;
the fixture is not a P1 control or a weighted source.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402


REPO_ROOT, _HERE = bootstrap(__file__)
DEFAULT_FIXTURE = (
    REPO_ROOT / "tests/fixtures/protected_twelve_vertex_macro_cycle_control.json"
)
VERTEX_COUNT = 12
COMPONENT_COUNT = 3


def protected_color(u: int, v: int) -> int:
    """Return the unique protected color of one internal K4 edge."""

    if u // 4 != v // 4 or u == v:
        raise ValueError("protected edge must join distinct vertices of one K4")
    return ((u % 4) ^ (v % 4)) - 1


def protected_partner(vertex: int, color: int) -> int:
    """Return the partner of ``vertex`` in its component's ``M_color``."""

    return 4 * (vertex // 4) + ((vertex % 4) ^ (color + 1))


def protected_pairs(color: int, vertex_count: int = VERTEX_COUNT):
    """Yield all ``M_color`` edges on ``vertex_count / 4`` components."""

    for u in range(vertex_count):
        v = protected_partner(u, color)
        if u < v:
            yield u, v


def load_fixture(path: Path = DEFAULT_FIXTURE):
    """Load and validate the stripped literal support fixture."""

    raw_bytes = path.read_bytes()
    raw = json.loads(raw_bytes.decode("utf-8"))
    assert set(raw) == {"schema", "scope", "support"}
    assert raw["schema"] == "protected-twelve-vertex-macro-cycle-control-v1"
    assert raw["scope"]["components"] == COMPONENT_COUNT
    assert raw["scope"]["physical_vertices"] == VERTEX_COUNT
    support = [tuple(entry) for entry in raw["support"]]
    assert len(support) == 22 and len(set(support)) == 22
    for u, v, color_u, color_v in support:
        assert 0 <= u < v < VERTEX_COUNT
        assert u // 4 != v // 4
        assert 0 <= color_u < 3 and 0 <= color_v < 3
        assert color_u != color_v
    return raw_bytes, support


def scalar_edges(crossing_support):
    """Construct the 18 implicit protected entries plus literal crossings."""

    edges = []
    for component in range(COMPONENT_COUNT):
        block = range(4 * component, 4 * component + 4)
        for u, v in itertools.combinations(block, 2):
            color = protected_color(u, v)
            edges.append((u, v, color, color, "protected"))
    edges.extend((*entry, "literal-crossing") for entry in crossing_support)
    return edges


def enumerate_terms(edges, vertex_count: int = VERTEX_COUNT):
    """Enumerate scalar perfect-matching terms by lowest free vertex."""

    incident = defaultdict(list)
    for edge_id, (u, v, color_u, color_v, _kind) in enumerate(edges):
        incident[u].append((edge_id, v, color_u, color_v))
        incident[v].append((edge_id, u, color_v, color_u))

    full_mask = (1 << vertex_count) - 1
    word = [-1] * vertex_count
    chosen = []
    terms = []

    def visit(mask: int) -> None:
        if mask == full_mask:
            assert all(color >= 0 for color in word)
            terms.append((tuple(word), tuple(chosen)))
            return
        free = (~mask) & full_mask
        first_bit = free & -free
        u = first_bit.bit_length() - 1
        for edge_id, v, color_u, color_v in incident[u]:
            if mask & (1 << v):
                continue
            word[u], word[v] = color_u, color_v
            chosen.append(edge_id)
            visit(mask | (1 << u) | (1 << v))
            chosen.pop()
            word[u] = word[v] = -1

    visit(0)
    return terms


def collision_count(word: tuple[int, ...], majority: int) -> int:
    """Count ``M_majority`` pairs with two non-majority endpoints."""

    return sum(
        word[u] != majority and word[v] != majority
        for u, v in protected_pairs(majority, len(word))
    )


def directed_arcs(crossing_support, majority: int):
    """Build the complete union of actual PSMR arcs for one majority."""

    arcs = set()
    for u, v, color_u, color_v in crossing_support:
        if color_u != majority and color_v == majority:
            arcs.add((u, protected_partner(v, majority)))
        if color_v != majority and color_u == majority:
            arcs.add((v, protected_partner(u, majority)))
    return arcs


def topological_order(vertex_count: int, arcs):
    """Return one topological order, or ``None`` when a directed cycle exists."""

    outgoing = defaultdict(set)
    indegree = [0] * vertex_count
    for u, v in arcs:
        if v not in outgoing[u]:
            outgoing[u].add(v)
            indegree[v] += 1
    ready = [u for u in range(vertex_count) if indegree[u] == 0]
    order = []
    while ready:
        u = ready.pop()
        order.append(u)
        for v in sorted(outgoing[u]):
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
    return tuple(order) if len(order) == vertex_count else None


def format_term(edge_ids, edges):
    """Drop provenance from a selected scalar matching term."""

    return tuple(edges[edge_id][:4] for edge_id in edge_ids)


def audit(path: Path = DEFAULT_FIXTURE) -> dict[str, object]:
    """Run the complete finite literal audit and return a compact receipt."""

    fixture_bytes, crossing_support = load_fixture(path)
    edges = scalar_edges(crossing_support)
    terms = enumerate_terms(edges)
    by_word = defaultdict(list)
    for word, edge_ids in terms:
        by_word[word].append(edge_ids)
    counts = Counter({word: len(choices) for word, choices in by_word.items()})

    assert len(edges) == 40
    assert len(terms) == 605
    assert len(by_word) == 401
    pure_counts = {color: counts[(color,) * VERTEX_COUNT] for color in range(3)}
    assert pure_counts == {0: 1, 1: 1, 2: 1}

    mixed_macro = {}
    macro_choices = {}
    for labels in itertools.product(range(3), repeat=COMPONENT_COUNT):
        word = tuple(labels[vertex // 4] for vertex in range(VERTEX_COUNT))
        if len(set(labels)) == 1:
            continue
        mixed_macro[labels] = counts[word]
        macro_choices[labels] = [
            choice
            for choice in by_word[word]
            if any(edges[edge_id][4] == "literal-crossing" for edge_id in choice)
        ]
    assert len(mixed_macro) == 24
    assert min(mixed_macro.values()) == 2
    macro_histogram = Counter(mixed_macro.values())
    assert macro_histogram == Counter({2: 16, 3: 5, 4: 2, 8: 1})

    localized = []
    for word, edge_ids in terms:
        for majority in range(3):
            if any(color != majority for color in word) and collision_count(word, majority) == 0:
                localized.append((word, majority, edge_ids))
    assert localized == []

    dag_receipt = []
    for majority in range(3):
        arcs = directed_arcs(crossing_support, majority)
        order = topological_order(VERTEX_COUNT, arcs)
        assert order is not None
        dag_receipt.append(
            {
                "majority": majority,
                "arc_count": len(arcs),
                "topological_order": order,
            }
        )
    assert [item["arc_count"] for item in dag_receipt] == [12, 13, 13]

    mixed_words = [word for word in by_word if len(set(word)) > 1]
    unique_mixed = [word for word in mixed_words if counts[word] == 1]
    assert len(unique_mixed) == 260
    q1_supported = [
        (word, majority)
        for word in mixed_words
        for majority in range(3)
        if collision_count(word, majority) == 1
    ]
    q1_unique = [
        (word, majority)
        for word, majority in q1_supported
        if counts[word] == 1
    ]
    assert len(q1_supported) == 62
    assert len(q1_unique) == 56

    mixed_qmin_histogram = Counter(
        min(collision_count(word, majority) for majority in range(3))
        for word in mixed_words
    )
    unique_qmin_histogram = Counter(
        min(collision_count(word, majority) for majority in range(3))
        for word in unique_mixed
    )
    assert mixed_qmin_histogram == Counter({1: 62, 2: 253, 3: 77, 4: 6})
    assert unique_qmin_histogram == Counter({1: 56, 2: 160, 3: 44})

    crossing_ids = [
        edge_id for edge_id, edge in enumerate(edges) if edge[4] == "literal-crossing"
    ]
    deletable = []
    for edge_id in crossing_ids:
        if all(
            any(edge_id not in choice for choice in choices)
            for choices in macro_choices.values()
        ):
            deletable.append(edges[edge_id][:4])
    assert deletable == []

    q1_witness = tuple(map(int, "002000001100"))
    assert tuple(collision_count(q1_witness, c) for c in range(3)) == (1, 4, 5)
    assert counts[q1_witness] == 1
    witness_choices = by_word[q1_witness]
    assert len(witness_choices) == 1
    witness_term = format_term(witness_choices[0], edges)
    expected_witness_term = (
        (0, 1, 0, 0),
        (2, 9, 2, 1),
        (3, 8, 0, 1),
        (4, 5, 0, 0),
        (6, 7, 0, 0),
        (10, 11, 0, 0),
    )
    assert set(witness_term) == set(expected_witness_term)

    canonical_support = json.dumps(crossing_support, separators=(",", ":"))
    return {
        "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "canonical_support_sha256": hashlib.sha256(
            canonical_support.encode("ascii")
        ).hexdigest(),
        "literal_crossing_entries": len(crossing_support),
        "scalar_entries_total": len(edges),
        "supported_terms": len(terms),
        "supported_words": len(by_word),
        "pure_counts": pure_counts,
        "mixed_macro_count_histogram": dict(sorted(macro_histogram.items())),
        "localized_q0_supported_terms": len(localized),
        "D_c": dag_receipt,
        "mixed_qmin_histogram": dict(sorted(mixed_qmin_histogram.items())),
        "unique_mixed_qmin_histogram": dict(sorted(unique_qmin_histogram.items())),
        "q1_supported_word_majorities": len(q1_supported),
        "q1_unique_word_majorities": len(q1_unique),
        "unique_q1_witness": {
            "word": q1_witness,
            "q_vector": (1, 4, 5),
            "term": witness_term,
        },
        "macro_inclusion_deletable_entries": len(deletable),
        "status": "PROTECTED_TWELVE_VERTEX_MACRO_CYCLE_CONTROL_AUDIT_PASS",
    }


def main() -> None:
    print(json.dumps(audit(), indent=2))


if __name__ == "__main__":
    main()
