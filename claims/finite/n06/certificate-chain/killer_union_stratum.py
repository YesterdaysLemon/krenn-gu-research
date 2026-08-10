"""Normalized polynomial strata for non-cubic killer-edge unions."""

from __future__ import annotations

from collections import Counter

import numpy as np

from generate_prism_singular import amplitude_polynomial
from killer_pattern_certificates import pattern_arcs
from prism_orbit_screen import Polynomial
from search_killer_patterns import active_mask_for_pattern
from search_witness import EquationSystem

Edge = tuple[int, int]
Pattern = list[list[int]]


def mutual_gauge_rank(
    system: EquationSystem,
    pattern: Pattern,
) -> tuple[int, int]:
    """Return (mutual singleton edges, vertex-colour gauge incidence rank).

    A nonzero singleton on edge ``{u,v}`` scales by the product of the two
    local vertex-colour gauge variables at its active row and column.  The
    corresponding unsigned graph-incidence matrix has rank ``|V|-b`` in
    each collection of nontrivial components, where ``b`` is the number of
    bipartite components.  Full row rank is exactly the condition needed to
    normalize all mutual singleton weights independently.
    """
    active = active_mask_for_pattern(system, pattern)
    coordinate_edges: list[
        tuple[tuple[int, int], tuple[int, int]]
    ] = []
    for edge, edge_arcs in pattern_arcs(pattern).items():
        if len(edge_arcs) != 2:
            continue
        edge_index = system.edge_index[edge]
        active_entries = [
            index
            for index in range(edge_index * 9, edge_index * 9 + 9)
            if active[index]
        ]
        if len(active_entries) != 1:
            raise ValueError(
                f"mutual edge {edge} has {len(active_entries)} active entries"
            )
        entry_position = active_entries[0] - edge_index * 9
        row, column = divmod(entry_position, 3)
        coordinate_edges.append(
            ((edge[0], row), (edge[1], column))
        )

    adjacency: dict[tuple[int, int], set[tuple[int, int]]] = {}
    for first, second in coordinate_edges:
        adjacency.setdefault(first, set()).add(second)
        adjacency.setdefault(second, set()).add(first)
    seen: set[tuple[int, int]] = set()
    rank = 0
    for root in adjacency:
        if root in seen:
            continue
        colours = {root: 0}
        stack = [root]
        vertices = 0
        degree_sum = 0
        bipartite = True
        while stack:
            vertex = stack.pop()
            if vertex in seen:
                continue
            seen.add(vertex)
            vertices += 1
            neighbours = adjacency[vertex]
            degree_sum += len(neighbours)
            for neighbour in neighbours:
                expected = 1 - colours[vertex]
                if neighbour in colours:
                    if colours[neighbour] != expected:
                        bipartite = False
                else:
                    colours[neighbour] = expected
                    stack.append(neighbour)
        rank += vertices - (1 if bipartite else 0)
        if degree_sum % 2:
            raise AssertionError("coordinate graph degree sum is odd")
    return len(coordinate_edges), rank


def normalized_union_stratum(
    system: EquationSystem, pattern: Pattern
) -> tuple[np.ndarray, np.ndarray]:
    """Normalize every mutual singleton killer block to one."""
    active = active_mask_for_pattern(system, pattern)
    fixed = np.zeros(system.variable_count, dtype=np.complex128)
    arcs = pattern_arcs(pattern)
    for edge, edge_arcs in arcs.items():
        if len(edge_arcs) != 2:
            continue
        edge_index = system.edge_index[edge]
        start = edge_index * 9
        active_entries = [
            index
            for index in range(start, start + 9)
            if active[index]
        ]
        if len(active_entries) != 1:
            raise ValueError(
                f"mutual edge {edge} has {len(active_entries)} active entries"
            )
        flat_index = active_entries[0]
        fixed[flat_index] = 1
        active[flat_index] = False
    return fixed, active


def union_orbit_equations(
    system: EquationSystem,
    pattern: Pattern,
    normalize_mutual: bool = True,
) -> tuple[list[str], list[Polynomial], dict[str, int]]:
    names, equations, variable_names, _ = (
        union_orbit_equations_with_colourings(
            system,
            pattern,
            normalize_mutual=normalize_mutual,
        )
    )
    return names, equations, variable_names


def union_orbit_equations_with_colourings(
    system: EquationSystem,
    pattern: Pattern,
    normalize_mutual: bool = True,
) -> tuple[
    list[str],
    list[Polynomial],
    dict[str, int],
    list[tuple[int, ...]],
]:
    if normalize_mutual:
        fixed, active = normalized_union_stratum(system, pattern)
    else:
        fixed = np.zeros(
            system.variable_count,
            dtype=np.complex128,
        )
        active = active_mask_for_pattern(system, pattern)
    indices = [int(index) for index in np.flatnonzero(active)]
    names = [f"x{index}" for index in range(len(indices))]
    variable_names = {
        flat_index: name
        for flat_index, name in zip(indices, names)
    }
    equations: list[Polynomial] = []
    equation_colourings: list[tuple[int, ...]] = []
    for raw_colouring in system.colourings:
        colouring = tuple(int(value) for value in raw_colouring)
        if len(set(colouring)) == 1:
            continue
        polynomial = amplitude_polynomial(
            system, fixed, variable_names, colouring
        )
        if polynomial:
            equations.append(polynomial)
            equation_colourings.append(colouring)
    return names, equations, variable_names, equation_colourings
