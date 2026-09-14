"""Exact physical controls for the common-star component-target obstruction.

This finite replay is not the arbitrary-order proof or its independent audit.
Edges are (component_u, component_v, color_u, color_v, center_weight, leaf_weight).
All arithmetic here is rational; the owning theorem allows complex factors.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json


def validate_graph(graph, *, triangle_free=False):
    n = graph["n"]
    if type(n) is not int or n < 2:
        raise ValueError("invalid component count")
    seen = set()
    for u, v, a, b, center, leaf in graph["edges"]:
        if not (0 <= u < v < n) or a not in range(3) or b not in range(3) or a == b:
            raise ValueError("invalid labelled component edge")
        if (u, v) in seen:
            raise ValueError("duplicate component edge")
        seen.add((u, v))
        if any(not isinstance(w, (int, Fraction)) or not w for w in (center, leaf)):
            raise ValueError("the finite control needs nonzero rational factors")
    if triangle_free:
        for i, j, k in combinations(range(n), 3):
            if {(i, j), (i, k), (j, k)} <= seen:
                raise ValueError("component graph is not triangle-free")
    return True


def check_colors(graph, colors):
    validate_graph(graph)
    if len(colors) != graph["n"] or any(c not in range(3) for c in colors):
        raise ValueError("one ternary color per component is required")


def physical_amplitude(graph, colors):
    """Build all 4k physical vertices, then expand their scalar hafnian."""
    check_colors(graph, colors)
    n = 4 * graph["n"]
    neighbors = [[] for _ in range(n)]

    def edge(u, v, value):
        value = Fraction(value)
        neighbors[u].append((v, value))
        neighbors[v].append((u, value))

    for component, c in enumerate(colors):
        for x in range(4):
            y = x ^ (c + 1)
            if x < y:
                edge(4 * component + x, 4 * component + y, 1)
    for u, v, a, b, center, leaf in graph["edges"]:
        if colors[u] == a and colors[v] == b:
            edge(4 * u, 4 * v, center)
            edge(4 * u + a + 1, 4 * v + b + 1, leaf)

    @lru_cache(None)
    def haf(mask):
        if not mask:
            return Fraction(1)
        first = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << first)
        return sum((weight * haf(rest ^ (1 << second))
                    for second, weight in neighbors[first]
                    if rest & (1 << second)), Fraction(0))

    return haf((1 << n) - 1)


def reduced_amplitudes(graph, colors):
    """Enumerate component matchings to evaluate double-haf and monomer-dimer views.

    This compares the reduced identity; it is not an independent audit.
    It does not call the physical-vertex recursion.
    """
    check_colors(graph, colors)
    compatible = [(u, v, Fraction(center), Fraction(leaf))
                  for u, v, a, b, center, leaf in graph["edges"]
                  if colors[u] == a and colors[v] == b]
    layer_a, layer_b = defaultdict(Fraction), defaultdict(Fraction)
    matching_sum = Fraction(0)

    def enumerate_matchings(index, used, product_a, product_b):
        nonlocal matching_sum
        if index == len(compatible):
            layer_a[used] += product_a
            layer_b[used] += product_b
            matching_sum += product_a * product_b
            return
        enumerate_matchings(index + 1, used, product_a, product_b)
        u, v, a, b = compatible[index]
        bits = (1 << u) | (1 << v)
        if not used & bits:
            enumerate_matchings(index + 1, used | bits, product_a * a, product_b * b)

    enumerate_matchings(0, 0, Fraction(1), Fraction(1))
    double_haf = sum((value * layer_b[mask] for mask, value in layer_a.items()), Fraction(0))
    return double_haf, matching_sum


def edge_rows(graph, edge_index):
    """Evaluate the actual three component words for the indicated labelled edge."""
    u, v, a, b, center, leaf = graph["edges"][edge_index]
    background = next(c for c in range(3) if c not in (a, b))
    words = []
    for changed in ((u,), (v,), (u, v)):
        word = [background] * graph["n"]
        for w in changed:
            word[w] = a if w == u else b
        words.append(tuple(word))
    values = tuple(physical_amplitude(graph, word) for word in words)
    return {"words": tuple(words), "values": values,
            "q": Fraction(center) * Fraction(leaf),
            "residual": values[2] - values[0] * values[1]}


def forest_control():
    return {"n": 4, "edges": [
        (0, 1, 0, 1, 2, Fraction(1, 2)),
        (0, 2, 0, 2, 3, Fraction(-1, 3)),
        (1, 3, 1, 2, -2, Fraction(1, 2)),
    ]}


def cycle_control():
    return {"n": 4, "edges": [
        (0, 1, 0, 1, 1, 1), (1, 2, 1, 0, 1, 1),
        (2, 3, 0, 1, 1, 1), (0, 3, 0, 1, 1, 1),
    ]}


def triangle_control():
    return {"n": 3, "edges": [
        (0, 1, 0, 1, 1, 1), (0, 2, 0, 2, 1, -1),
        (1, 2, 1, 2, 1, -1),
    ]}


def verify_controls():
    forest = forest_control()
    validate_graph(forest, triangle_free=True)
    rows = edge_rows(forest, 0)
    assert rows["values"] == (0, 0, 1) and rows["residual"] == rows["q"] == 1
    for word in rows["words"]:
        physical = physical_amplitude(forest, word)
        assert reduced_amplitudes(forest, word) == (physical, physical)
    assert all(physical_amplitude(forest, (c,) * 4) == 1 for c in range(3))
    cycle_word = (0, 1, 0, 1)
    assert physical_amplitude(cycle_control(), cycle_word) == 9
    assert reduced_amplitudes(cycle_control(), cycle_word) == (9, 7)
    triangle = edge_rows(triangle_control(), 0)
    assert triangle["values"] == (0, 0, 0) and triangle["residual"] != triangle["q"]
    port_forest = {"n": 4, "edges": [
        (u, v, a, b, 1, -1) for u, v, a, b, _, _ in forest["edges"]]}
    port_triangle = {"n": 3, "edges": [
        (u, v, a, b, 1, -1) for u, v, a, b, _, _ in triangle_control()["edges"]]}
    assert edge_rows(port_forest, 0)["values"] == (0, 0, -1)
    assert edge_rows(port_triangle, 0)["values"] == (0, 0, -2)
    return {"status": "PASS", "forest_rows": [0, 0, 1],
            "cycle_physical_double_haf_matching": [9, 9, 7],
            "triangle_boundary_rows": [0, 0, 0],
            "unique_port_double_failures": [-1, -2],
            "scope": "finite exact physical controls; arbitrary-order proof is in the owner"}


if __name__ == "__main__":
    print(json.dumps(verify_controls(), indent=2))
