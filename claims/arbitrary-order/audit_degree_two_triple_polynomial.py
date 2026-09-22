#!/usr/bin/env python3
"""Independent recursive matching audit for the degree-two triple block."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import argparse


Resource = tuple[str, str]
Edge = tuple[str, str, str]

RESOURCES: dict[str, Resource] = {
    "A": ("A0", "A1"),
    "B": ("B0", "B1"),
    "C": ("C0", "C1"),
}
PROTECTED: tuple[Edge, ...] = tuple(
    (ends[0], ends[1], f"p{name}") for name, ends in RESOURCES.items()
)
AB: tuple[Edge, ...] = (("A0", "B0", "ab0"), ("A1", "B1", "ab1"))
AC: tuple[Edge, ...] = (("A0", "C0", "ac0"), ("A1", "C1", "ac1"))
BC_PRISM: tuple[Edge, ...] = (("B0", "C0", "bc0"), ("B1", "C1", "bc1"))
BC_K33: tuple[Edge, ...] = (("B0", "C1", "bc0"), ("B1", "C0", "bc1"))


def canonical(edge: Edge) -> Edge:
    u, v, name = edge
    return (u, v, name) if u < v else (v, u, name)


def matchings(vertices: frozenset[str], edges: tuple[Edge, ...]) -> tuple[tuple[str, ...], ...]:
    """Enumerate recursively, independently of the author's combination scan."""
    incident: dict[str, list[Edge]] = {vertex: [] for vertex in vertices}
    for raw in edges:
        edge = canonical(raw)
        u, v, _ = edge
        if u in vertices and v in vertices:
            incident[u].append(edge)
            incident[v].append(edge)

    out: list[tuple[str, ...]] = []

    def visit(remaining: frozenset[str], chosen: tuple[str, ...]) -> None:
        if not remaining:
            out.append(tuple(sorted(chosen)))
            return
        u = min(remaining)
        for left, right, name in incident[u]:
            v = right if left == u else left
            if v in remaining:
                visit(remaining - {u, v}, chosen + (name,))

    visit(vertices, ())
    return tuple(sorted(out))


def product(term: tuple[str, ...], weights: dict[str, Fraction]) -> Fraction:
    result = Fraction(1)
    for edge in term:
        result *= weights[edge]
    return result


def coefficient(terms: tuple[tuple[str, ...], ...], weights: dict[str, Fraction]) -> Fraction:
    return sum((product(term, weights) for term in terms), start=Fraction(0))


def verify() -> dict[str, object]:
    vertices = frozenset(vertex for ends in RESOURCES.values() for vertex in ends)
    assert len(vertices) == 6  # Full selection requires pairwise physical disjointness.

    prism_edges = PROTECTED + AB + AC + BC_PRISM
    k33_edges = PROTECTED + AB + AC + BC_K33
    prism_terms = matchings(vertices, prism_edges)
    k33_terms = matchings(vertices, k33_edges)

    pair_terms = {}
    for pair, crossing in (("AB", AB), ("AC", AC), ("BC", BC_PRISM)):
        selected = frozenset(RESOURCES[pair[0]] + RESOURCES[pair[1]])
        terms = matchings(selected, PROTECTED + crossing)
        assert len(terms) == 2
        pair_terms[pair] = terms

    protected_names = {"pA", "pB", "pC"}
    prism_cross_only = tuple(
        term for term in prism_terms if protected_names.isdisjoint(term)
    )
    k33_cross_only = tuple(term for term in k33_terms if protected_names.isdisjoint(term))
    assert len(prism_terms) == 4
    assert not prism_cross_only
    assert len(k33_terms) == 6
    assert len(k33_cross_only) == 2

    common_expected = {
        ("pA", "pB", "pC"),
        ("ab0", "ab1", "pC"),
        ("ac0", "ac1", "pB"),
        ("bc0", "bc1", "pA"),
    }
    assert set(prism_terms) == common_expected
    assert common_expected < set(k33_terms)

    # Each crossing edge occurs exactly once across the two K3,3-only terms.
    assert sorted(edge for term in k33_cross_only for edge in term) == sorted(
        ("ab0", "ab1", "ac0", "ac1", "bc0", "bc1")
    )

    # Exact rational formula checks with non-unit, signed weights.
    weights = {
        "pA": Fraction(2),
        "pB": Fraction(-3),
        "pC": Fraction(5),
        "ab0": Fraction(7),
        "ab1": Fraction(11),
        "ac0": Fraction(-13),
        "ac1": Fraction(17),
        "bc0": Fraction(19),
        "bc1": Fraction(-23),
    }
    p_product = weights["pA"] * weights["pB"] * weights["pC"]
    sigmas = {
        "AB": weights["ab0"] * weights["ab1"] / (weights["pA"] * weights["pB"]),
        "AC": weights["ac0"] * weights["ac1"] / (weights["pA"] * weights["pC"]),
        "BC": weights["bc0"] * weights["bc1"] / (weights["pB"] * weights["pC"]),
    }
    prism_formula = p_product * (1 + sum(sigmas.values(), start=Fraction(0)))
    assert coefficient(prism_terms, weights) == prism_formula

    taus = tuple(product(term, weights) / p_product for term in k33_cross_only)
    k33_formula = p_product * (
        1 + sum(sigmas.values(), start=Fraction(0)) + sum(taus, start=Fraction(0))
    )
    assert coefficient(k33_terms, weights) == k33_formula
    assert taus[0] * taus[1] == sigmas["AB"] * sigmas["AC"] * sigmas["BC"]

    # Face-zero specialization: each crossing-pair product is -p_i p_j.
    face_zero_weights = {
        "pA": Fraction(1),
        "pB": Fraction(1),
        "pC": Fraction(1),
        "ab0": Fraction(1),
        "ab1": Fraction(-1),
        "ac0": Fraction(1),
        "ac1": Fraction(-1),
        "bc0": Fraction(1),
        "bc1": Fraction(-1),
    }
    for terms in pair_terms.values():
        assert coefficient(terms, face_zero_weights) == 0
    assert coefficient(prism_terms, face_zero_weights) == -2

    # If differently coloured resources overlap physically, no word can select
    # both endpoint states at the shared physical vertex; the six-state local
    # polynomial consequently requires the explicit disjointness hypothesis.
    overlapping_coloured_resources = {
        "A": ((0, 0), (1, 0)),
        "B": ((1, 1), (2, 1)),
    }
    assignments: dict[int, int] = {}
    conflict = False
    for states in overlapping_coloured_resources.values():
        for physical, color in states:
            if physical in assignments and assignments[physical] != color:
                conflict = True
            assignments[physical] = color
    assert conflict

    return {
        "status": "INDEPENDENT_DEGREE2_TRIPLE_LOCAL_PASS",
        "pair_face_matching_counts": {key: len(value) for key, value in pair_terms.items()},
        "prism_matching_count": len(prism_terms),
        "prism_crossing_only_count": len(prism_cross_only),
        "k33_matching_count": len(k33_terms),
        "k33_crossing_only_count": len(k33_cross_only),
        "tau_product_identity": True,
        "face_zero_prism_coefficient": -2,
        "overlap_conflict_demonstrated": conflict,
        "scope": "local six-endpoint factorization only; global zero-block isolation remains open",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(verify(), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    print(rendered)


if __name__ == "__main__":
    main()
