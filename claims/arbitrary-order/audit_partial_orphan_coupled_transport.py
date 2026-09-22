#!/usr/bin/env python3
"""Independent physical-sector audit of same-component orphan transport."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}


@dataclass(frozen=True)
class Edge:
    u: int
    cu: int
    v: int
    cv: int
    symbol: str
    kind: str


def canonical(u: int, cu: int, v: int, cv: int, symbol: str, kind: str) -> Edge:
    if (v, cv) < (u, cu):
        u, cu, v, cv = v, cv, u, cu
    return Edge(u, cu, v, cv, symbol, kind)


def protected_edges(component_count: int) -> list[Edge]:
    edges = []
    for component in range(component_count):
        base = 4 * component
        for color, pairs in MATCHINGS.items():
            for left, right in pairs:
                edges.append(
                    canonical(
                        base + left,
                        color,
                        base + right,
                        color,
                        f"P{component}:{color}:{left}{right}",
                        "protected",
                    )
                )
    return edges


def matchings(word: tuple[int, ...], edges: list[Edge]) -> tuple[tuple[str, ...], ...]:
    incident: dict[int, list[Edge]] = {vertex: [] for vertex in range(len(word))}
    seen = set()
    for edge in edges:
        key = (edge.u, edge.cu, edge.v, edge.cv)
        assert key not in seen
        seen.add(key)
        if word[edge.u] == edge.cu and word[edge.v] == edge.cv:
            incident[edge.u].append(edge)
            incident[edge.v].append(edge)

    terms: list[tuple[str, ...]] = []

    def visit(remaining: frozenset[int], symbols: tuple[str, ...]) -> None:
        if not remaining:
            terms.append(tuple(sorted(symbols)))
            return
        u = min(
            remaining,
            key=lambda vertex: sum(
                (edge.v if edge.u == vertex else edge.u) in remaining
                for edge in incident[vertex]
            ),
        )
        for edge in incident[u]:
            v = edge.v if edge.u == u else edge.u
            if v in remaining:
                visit(remaining - {u, v}, symbols + (edge.symbol,))

    visit(frozenset(range(len(word))), ())
    return tuple(sorted(terms))


def resource_color(port_u: int, port_v: int) -> int:
    pair = frozenset((port_u, port_v))
    matches = [
        color
        for color, resources in MATCHINGS.items()
        if pair in {frozenset(resource) for resource in resources}
    ]
    assert len(matches) == 1
    return matches[0]


def is_resource(u: int, v: int, color: int) -> bool:
    return (
        u // 4 == v // 4
        and frozenset((u % 4, v % 4))
        in {frozenset(resource) for resource in MATCHINGS[color]}
    )


def crossing_symbols(term: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(symbol for symbol in term if not symbol.startswith("P"))


def audit_q1_type_step(component_count: int) -> dict[str, object]:
    # Normalize a=0,b=1,c=2 and R=A01.  Test the forbidden possibility that
    # the same-component orphan targets form M_a(B)=B01.
    r, s = 0, 1
    y, z = 4, 5
    assert resource_color(y % 4, z % 4) == 0
    word = [0] * (4 * component_count)
    word[y] = 2
    word[z] = 2
    q_a = sum(
        word[4 * component + u] != 0 and word[4 * component + v] != 0
        for component in range(component_count)
        for u, v in MATCHINGS[0]
    )
    assert q_a == 1
    edges = protected_edges(component_count)
    edges.extend(
        (
            canonical(r, 0, y, 2, "h0", "crossing"),
            canonical(s, 0, z, 2, "h1", "crossing"),
        )
    )
    terms = matchings(tuple(word), edges)
    assert len(terms) == 1
    assert crossing_symbols(terms[0]) == ("h0", "h1")
    return {
        "component_count": component_count,
        "q_a": q_a,
        "matching_count": len(terms),
        "crossing_monomial": list(crossing_symbols(terms[0])),
    }


def audit_coupled_word(component_count: int) -> dict[str, object]:
    # R=A01; y,z=B02 form M_b; L=B13 is its M_b complement.
    r, s = 0, 1
    y, z = 4, 6
    l0, l1 = 5, 7
    assert resource_color(y % 4, z % 4) == 1
    assert frozenset((l0 % 4, l1 % 4)) == frozenset((1, 3))
    word = [0] * (4 * component_count)
    word[y] = word[z] = 2
    word[l0] = word[l1] = 1

    target_domain = tuple(
        vertex for vertex in range(4 * component_count) if vertex // 4 != 1
    )
    placement_count = 0
    extra_count = 0
    collision_with_r_count = 0
    for q0, q1 in permutations(target_domain, 2):
        edges = protected_edges(component_count)
        edges.extend(
            (
                canonical(r, 0, y, 2, "h0", "crossing"),
                canonical(s, 0, z, 2, "h1", "crossing"),
                canonical(l0, 1, q0, 0, "g0", "crossing"),
                canonical(l1, 1, q1, 0, "g1", "crossing"),
            )
        )
        terms = matchings(tuple(word), edges)
        monomials = {crossing_symbols(term) for term in terms}
        expect_extra = is_resource(q0, q1, 0) and frozenset((q0, q1)) != {
            r,
            s,
        }
        expected = {("h0", "h1")}
        if expect_extra:
            expected.add(("g0", "g1", "h0", "h1"))
            extra_count += 1
        assert monomials == expected, (component_count, q0, q1, monomials)
        if r in (q0, q1) or s in (q0, q1):
            collision_with_r_count += 1
            assert ("g0", "g1", "h0", "h1") not in monomials
        placement_count += 1

    expected_placements = len(target_domain) * (len(target_domain) - 1)
    expected_extra = 2 * (2 * (component_count - 1) - 1)
    assert placement_count == expected_placements
    assert extra_count == expected_extra
    return {
        "component_count": component_count,
        "ordered_exit_placements": placement_count,
        "placements_with_extra_sector": extra_count,
        "placements_colliding_with_R": collision_with_r_count,
        "direct_crossing_monomial": ["h0", "h1"],
        "extra_crossing_monomial": ["g0", "g1", "h0", "h1"],
    }


def verify() -> dict[str, object]:
    q1_receipts = [audit_q1_type_step(k) for k in (2, 3, 4)]
    coupled_receipts = [audit_coupled_word(k) for k in (2, 3, 4)]
    return {
        "status": "INDEPENDENT_PARTIAL_ORPHAN_COUPLED_TRANSPORT_PASS",
        "q1_type_step": q1_receipts,
        "coupled_word": coupled_receipts,
        "coefficient_form": "h if no distinct Ma target resource; h*(1+g) otherwise",
        "scope": (
            "finite normalized sector replay for k=2,3,4; the written uniqueness "
            "argument proves arbitrary k and nonzero weights"
        ),
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
