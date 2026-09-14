"""Exact two-edge surplus-shore physical certificates (no auxiliary cofactors)."""
from __future__ import annotations

import itertools

from krenn_gu.eight_vertex_physical_hafnian_identity import (
    ENTRY_ID_OF, ENTRY_KEYS, add, hafnian_polynomial, multiply, perfect_matchings, scale,
)


def entry(u, v, a, b):
    return ENTRY_ID_OF[(u, v, a, b) if u < v else (v, u, b, a)]


def make_pattern(adjacent=False, same_alternates=False):
    """The four isomorphism types of this two-edge, two-moving-leaf family."""
    shore = (3, 4, 5, 6, 7)
    centres = (3, 3 if adjacent else 6)
    moving = (5, 7)
    alternates = (1 if same_alternates else 2, 1)
    edges = {tuple(sorted(pair)) for pair in zip(centres, moving, strict=True)}
    options = {v: (0, alternates[moving.index(v)]) if v in moving else (0,) for v in shore}
    zeros = sorted(entry(u, v, a, b) for u, v in itertools.combinations(shore, 2)
                   if (u, v) not in edges
                   for a in options[u] for b in options[v])
    ordinary = [entry(c, v, 0, 0) for c, v in zip(centres, moving, strict=True)]
    changed = [entry(c, v, 0, a) for c, v, a in zip(centres, moving, alternates, strict=True)]
    sources = []
    for first, second in ((1, 1), (1, 0), (0, 1), (0, 0)):
        word = [0] * 8
        word[5], word[7] = first * alternates[0], second * alternates[1]
        sources.append({"word": "".join(map(str, word)),
                        "multiplier": sorted((ordinary[0] if first else changed[0],
                                              ordinary[1] if second else changed[1])),
                        "coefficient": -1 if first == second else 1})
    return {"schema": "eight-vertex-two-edge-surplus-shore-v1", "n": 8,
            "shore": list(shore), "covering_edges": [list(e) for e in sorted(edges)],
            "base_colour": 0, "moving_vertices": list(moving),
            "alternate_colours": list(alternates), "zero_entry_ids": zeros,
            "nonzero_entry_ids": sorted(changed), "target_monomial": sorted(changed),
            "sources": sources}


def replay(payload):
    if not isinstance(payload, dict) or payload.get("schema") not in (
            "eight-vertex-two-edge-surplus-shore-v1", "eight-vertex-physical-degree6-identity-v1"):
        raise ValueError("unsupported physical certificate")
    if type(payload.get("n")) is not int or payload["n"] != 8:
        raise ValueError("order must be integer eight")
    for key in ("zero_entry_ids", "nonzero_entry_ids", "target_monomial"):
        values = payload.get(key)
        if not isinstance(values, list) or not all(type(v) is int and 1 <= v <= 252 for v in values):
            raise ValueError(f"invalid {key}")
        if key != "target_monomial" and len(values) != len(set(values)):
            raise ValueError(f"duplicate {key}")
    zeros, nonzeros = set(payload["zero_entry_ids"]), set(payload["nonzero_entry_ids"])
    if zeros & nonzeros or not set(payload["target_monomial"]) <= nonzeros:
        raise ValueError("target monomial is not guaranteed nonzero")
    if len(payload["target_monomial"]) > 6 or not isinstance(payload.get("sources"), list):
        raise ValueError("invalid degree-six certificate")
    residual = {tuple(sorted(payload["target_monomial"])): -1}
    counts = []
    for source in payload["sources"]:
        word = source["word"]
        if not isinstance(word, str) or len(word) != 8 or set(word) - set("012"):
            raise ValueError("invalid source word")
        coefficient = source["coefficient"]
        multiplier = source["multiplier"]
        if type(coefficient) is not int or not isinstance(multiplier, list) or len(multiplier) > 2 or not all(
                type(v) is int and 1 <= v <= 252 for v in multiplier):
            raise ValueError("invalid physical multiplier")
        polynomial = hafnian_polynomial(tuple(range(8)), tuple(map(int, word)), zeros)
        counts.append(len(polynomial))
        if len(set(word)) == 1:
            polynomial = add(polynomial, {(): -1})
        monomial = {} if zeros.intersection(multiplier) else {tuple(sorted(multiplier)): 1}
        residual = add(residual, scale(coefficient, multiply(monomial, polynomial)))
    if residual:
        raise ValueError(f"physical polynomial residual has {len(residual)} terms")
    return {"status": "PASS", "scope": "guarded_eight_vertex_physical_exclusion",
            "matching_count": len(perfect_matchings(tuple(range(8)))),
            "source_term_counts": counts, "physical_degree_bound": 6,
            "zero_entry_ids": sorted(zeros), "nonzero_entry_ids": sorted(nonzeros),
            "physical_cut": sorted((*zeros, *(-v for v in nonzeros)), key=abs),
            "uses_rho": False, "cofactor_divisions": 0}


def four_patterns():
    return [make_pattern(adjacent, same) for adjacent in (False, True) for same in (False, True)]


def describe_entry(identifier):
    u, v, a, b = ENTRY_KEYS[identifier - 1]
    return f"W{u}{v}[{a},{b}]"
