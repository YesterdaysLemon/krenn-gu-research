"""Primary verifier for the GHZ closure / matching-polytope face theorem.

Builds the canonical truncation family G_n (n = 4, 6, ..., 16) starting from
K_4, checks exactly in integers that the three colour classes have potential
zero while every other perfect matching has potential at least one, and for
n <= 10 expands the matrix-unit family T_{W(eps)} symbolically over all
perfect matchings of K_n to confirm T_{W(eps)} = Delta_n + eps R(eps).

Exact combinatorial and symbolic checks only; no floating point.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy

Edge = frozenset


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def perfect_matchings(vertices, adjacency):
    """All perfect matchings of the graph on `vertices` (recursive)."""
    vertices = sorted(vertices)
    if not vertices:
        yield frozenset()
        return
    first = vertices[0]
    rest = vertices[1:]
    for partner in rest:
        if partner in adjacency[first]:
            remaining = [u for u in rest if u != partner]
            for matching in perfect_matchings(remaining, adjacency):
                yield matching | {Edge({first, partner})}


def adjacency_of(edges):
    adjacency: dict[int, set[int]] = {}
    for edge in edges:
        u, v = tuple(edge)
        adjacency.setdefault(u, set()).add(v)
        adjacency.setdefault(v, set()).add(u)
    return adjacency


def k4_start():
    colour = {
        Edge({0, 1}): 0, Edge({2, 3}): 0,
        Edge({0, 2}): 1, Edge({1, 3}): 1,
        Edge({0, 3}): 2, Edge({1, 2}): 2,
    }
    potential = {edge: 0 for edge in colour}
    return colour, potential


def truncate(colour, potential, vertex, new_labels):
    """Replace `vertex` by a triangle on `new_labels` = (t_0, t_1, t_2)."""
    incident = [edge for edge in colour if vertex in edge]
    if len(incident) != 3:
        raise AssertionError("truncation requires a cubic vertex")
    partner_of_colour = {}
    for edge in incident:
        (partner,) = tuple(edge - {vertex})
        partner_of_colour[colour[edge]] = partner
    if sorted(partner_of_colour) != [0, 1, 2]:
        raise AssertionError("incident colours must be 0,1,2")

    # Potential bound: 3A + sum_c nu(v u_c) + min_N nu(N) >= 1.
    vertices = sorted(set().union(*colour))
    closed_nbhd = {vertex, *partner_of_colour.values()}
    reduced_edges = [edge for edge in colour if not (edge & closed_nbhd)]
    reduced_vertices = [u for u in vertices if u not in closed_nbhd]
    reduced_adj = adjacency_of(reduced_edges)
    for u in reduced_vertices:
        reduced_adj.setdefault(u, set())
    inner = [
        sum(potential[e] for e in matching)
        for matching in perfect_matchings(reduced_vertices, reduced_adj)
    ]
    attach_sum = sum(potential[edge] for edge in incident)
    if inner:
        needed = 1 - attach_sum - min(inner)
        shift = max(1, -(-needed // 3))  # ceiling division
    else:
        shift = 1

    new_colour = {}
    new_potential = {}
    for edge in colour:
        if vertex not in edge:
            new_colour[edge] = colour[edge]
            new_potential[edge] = potential[edge]
    for c, partner in partner_of_colour.items():
        edge = Edge({partner, new_labels[c]})
        new_colour[edge] = c
        new_potential[edge] = potential[Edge({vertex, partner})] + shift
    for a, b in ((0, 1), (0, 2), (1, 2)):
        edge = Edge({new_labels[a], new_labels[b]})
        new_colour[edge] = 3 - a - b
        new_potential[edge] = -shift
    return new_colour, new_potential, shift


def canonical_family(max_n):
    """Yield (n, colour, potential, shift) for n = 4, 6, ..., max_n."""
    colour, potential = k4_start()
    n = 4
    yield n, colour, potential, 0
    while n + 2 <= max_n:
        vertex = n - 1  # largest label
        colour, potential, shift = truncate(
            colour, potential, vertex, (n - 1, n, n + 1)
        )
        n += 2
        yield n, colour, potential, shift


def check_family(n, colour, potential):
    vertices = sorted(set().union(*colour))
    if vertices != list(range(n)):
        raise AssertionError(f"n={n}: unexpected vertex labels")
    adjacency = adjacency_of(colour)
    # cubic and properly coloured
    for v in vertices:
        incident = [edge for edge in colour if v in edge]
        if len(incident) != 3:
            raise AssertionError(f"n={n}: vertex {v} is not cubic")
        if sorted(colour[e] for e in incident) != [0, 1, 2]:
            raise AssertionError(f"n={n}: colouring not proper at {v}")
    classes = [
        frozenset(edge for edge in colour if colour[edge] == c)
        for c in range(3)
    ]
    matchings = list(perfect_matchings(vertices, adjacency))
    matching_set = set(matchings)
    for c, cls in enumerate(classes):
        if cls not in matching_set:
            raise AssertionError(f"n={n}: colour class {c} is not a PM")
        if sum(potential[e] for e in cls) != 0:
            raise AssertionError(f"n={n}: colour class {c} has nonzero nu")
    extras = [m for m in matchings if m not in classes]
    extra_potentials = [sum(potential[e] for e in m) for m in extras]
    if any(value < 1 for value in extra_potentials):
        raise AssertionError(f"n={n}: an extra matching has nu <= 0")
    # induced words: constant words only from the colour classes
    for m in matchings:
        word = {}
        for edge in m:
            for v in edge:
                word[v] = colour[edge]
        constant = len(set(word.values())) == 1
        if constant != (m in classes):
            raise AssertionError(f"n={n}: constant-word bookkeeping failed")
    return {
        "n": n,
        "edges": len(colour),
        "perfect_matchings": len(matchings),
        "extra_matchings": len(extras),
        "min_extra_potential": min(extra_potentials) if extras else None,
        "max_abs_potential": max(abs(value) for value in potential.values()),
    }


def symbolic_tensor_check(n, colour, potential):
    """Expand T_{W(eps)} over all perfect matchings of K_n symbolically."""
    eps = sympy.Symbol("eps")
    complete_adj = {v: set(range(n)) - {v} for v in range(n)}
    coefficients: dict[tuple[int, ...], sympy.Expr] = {}
    for matching in perfect_matchings(range(n), complete_adj):
        if not all(edge in colour for edge in matching):
            continue  # zero block
        word = [None] * n
        term = sympy.Integer(1)
        for edge in matching:
            c = colour[edge]
            for v in edge:
                word[v] = c
            term *= eps ** potential[edge]
        key = tuple(word)
        coefficients[key] = sympy.expand(coefficients.get(key, 0) + term)
    for c in range(3):
        if coefficients.get((c,) * n) != 1:
            raise AssertionError(f"n={n}: constant word {c} coefficient != 1")
    mixed_orders = []
    for word, value in coefficients.items():
        if len(set(word)) == 1:
            continue
        poly = sympy.Poly(sympy.expand(value), eps)
        if poly.is_zero:
            raise AssertionError("empty mixed coefficient recorded")
        lowest = min(monom[0] for monom in poly.monoms())
        if lowest < 1:
            raise AssertionError(f"n={n}: mixed word {word} has eps^0 term")
        mixed_orders.append(lowest)
    return {
        "nonconstant_words_touched": len(mixed_orders),
        "lowest_mixed_order": min(mixed_orders) if mixed_orders else None,
    }


def main() -> None:
    max_n = 16
    rows = []
    for n, colour, potential, shift in canonical_family(max_n):
        row = check_family(n, colour, potential)
        row["shift_A"] = shift
        if n <= 10:
            row.update(symbolic_tensor_check(n, colour, potential))
        rows.append(row)
        print(json.dumps(row))
    if [row["n"] for row in rows] != list(range(4, max_n + 1, 2)):
        raise AssertionError("family does not cover every even order")
    prism = rows[1]
    if (prism["perfect_matchings"], prism["extra_matchings"]) != (4, 1):
        raise AssertionError("six-vertex member is not the prism")
    if prism.get("lowest_mixed_order") != 3:
        raise AssertionError("prism extra matching should have eps^3")
    out_dir = Path("tmp")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "ghz_closure_face_family_verified.json"
    payload = {
        "verifier": Path(__file__).name,
        "verifier_sha256": sha256_file(Path(__file__)),
        "rows": rows,
        "verified": True,
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print("VERIFIED: canonical truncation family realises Delta_n asymptotically for n = 4..16")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"FAILED: {error}")
        sys.exit(1)
