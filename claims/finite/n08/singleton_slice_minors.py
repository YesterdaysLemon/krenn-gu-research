"""Exact rank-one slice-minor certificates around a singleton edge.

Let ``{x,y}`` be a monochromatic singleton block supported only at
``(c,c)``.  Fix a nonmonochromatic colouring of all other vertices and let
``R(i,j)`` be the sum of matching monomials for colour ``i`` at ``x`` and
colour ``j`` at ``y``, restricted to perfect matchings that avoid
``{x,y}``.

The target slice is identically zero.  Matchings that use ``{x,y}`` give a
scalar multiple of its singleton block, so

    R = -H * W_xy

for one scalar minor amplitude ``H``.  Hence ``rank(R) <= 1`` and every
``2 x 2`` minor of ``R`` vanishes.  If a support leaves exactly one
monomial in such a minor, its explicitly nonzero product cannot vanish.

This module detects that characteristic-zero, value-free obstruction.  It
does not infer a global theorem from finite support scans.
"""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import itertools
from collections import Counter

from krenn_gu.search_witness import EquationSystem

Edge = tuple[int, int]
Monomial = tuple[int, ...]


def singleton_edges(
    system: EquationSystem,
    selected_entries: set[int],
) -> dict[Edge, int]:
    """Return blocks supported at exactly one diagonal coordinate."""
    result: dict[Edge, int] = {}
    for edge in system.edges:
        offset = system.edge_index[edge] * system.d * system.d
        support = {
            entry - offset
            for entry in selected_entries
            if offset <= entry < offset + system.d * system.d
        }
        for colour in range(system.d):
            if support == {colour * system.d + colour}:
                result[edge] = colour
                break
    return result


def equation_index_map(
    system: EquationSystem,
) -> dict[tuple[int, ...], int]:
    return {
        tuple(map(int, colouring)): index
        for index, colouring in enumerate(system.colourings)
    }


def product_monomial(
    system: EquationSystem,
    first_matching: int,
    first_equation: int,
    second_matching: int,
    second_equation: int,
) -> Monomial:
    return tuple(
        sorted(
            [
                *map(
                    int,
                    system.variable_ids[
                        first_matching, first_equation, :
                    ],
                ),
                *map(
                    int,
                    system.variable_ids[
                        second_matching, second_equation, :
                    ],
                ),
            ]
        )
    )


def active_outward_matchings(
    system: EquationSystem,
    selected_entries: set[int],
    avoided_edge: Edge,
    equation_index: int,
) -> list[int]:
    return [
        matching_index
        for matching_index, matching in enumerate(system.matchings)
        if avoided_edge not in matching
        and all(
            int(factor) in selected_entries
            for factor in system.variable_ids[
                matching_index, equation_index, :
            ]
        )
    ]


def restricted_minor(
    system: EquationSystem,
    selected_entries: set[int],
    active: dict[tuple[int, int], list[int]],
    equations: dict[tuple[int, int], int],
    rows: tuple[int, int],
    columns: tuple[int, int],
) -> Counter[Monomial]:
    """Expand one outward-slice minor on the selected support."""
    first_row, second_row = rows
    first_column, second_column = columns
    result: Counter[Monomial] = Counter()
    for sign, first_corner, second_corner in (
        (
            1,
            (first_row, first_column),
            (second_row, second_column),
        ),
        (
            -1,
            (first_row, second_column),
            (second_row, first_column),
        ),
    ):
        for first_matching in active[first_corner]:
            for second_matching in active[second_corner]:
                monomial = product_monomial(
                    system,
                    first_matching,
                    equations[first_corner],
                    second_matching,
                    equations[second_corner],
                )
                if not all(
                    factor in selected_entries for factor in monomial
                ):
                    raise AssertionError(
                        "active product contains a zero factor"
                    )
                result[monomial] += sign
    return Counter(
        {
            monomial: coefficient
            for monomial, coefficient in result.items()
            if coefficient
        }
    )


def support_singleton_slice_minor_certificate(
    system: EquationSystem,
    selected_entries: set[int],
) -> dict[str, object] | None:
    """Return the first singleton-slice minor with one active monomial."""
    indices = equation_index_map(system)
    for edge, singleton_colour in singleton_edges(
        system,
        selected_entries,
    ).items():
        left, right = edge
        rest_vertices = [
            vertex
            for vertex in range(system.n)
            if vertex not in edge
        ]
        outward = [
            matching_index
            for matching_index, matching in enumerate(system.matchings)
            if edge not in matching
        ]
        for rest_colours in itertools.product(
            range(system.d),
            repeat=len(rest_vertices),
        ):
            if len(set(rest_colours)) < 2:
                continue
            base = [0] * system.n
            for vertex, colour in zip(
                rest_vertices,
                rest_colours,
                strict=True,
            ):
                base[vertex] = colour
            equations: dict[tuple[int, int], int] = {}
            active: dict[tuple[int, int], list[int]] = {}
            for left_colour in range(system.d):
                for right_colour in range(system.d):
                    colouring = list(base)
                    colouring[left] = left_colour
                    colouring[right] = right_colour
                    equation = indices[tuple(colouring)]
                    equations[left_colour, right_colour] = equation
                    active[left_colour, right_colour] = [
                        matching_index
                        for matching_index in outward
                        if all(
                            int(factor) in selected_entries
                            for factor in system.variable_ids[
                                matching_index, equation, :
                            ]
                        )
                    ]
            for rows in itertools.combinations(range(system.d), 2):
                for columns in itertools.combinations(
                    range(system.d),
                    2,
                ):
                    polynomial = restricted_minor(
                        system,
                        selected_entries,
                        active,
                        equations,
                        rows,
                        columns,
                    )
                    if len(polynomial) != 1:
                        continue
                    monomial, coefficient = next(
                        iter(polynomial.items())
                    )
                    return {
                        "certificate_kind": (
                            "singleton_slice_minor"
                        ),
                        "singleton_edge": list(edge),
                        "singleton_colour": singleton_colour,
                        "rest_vertices": rest_vertices,
                        "rest_colouring": list(rest_colours),
                        "rows": list(rows),
                        "columns": list(columns),
                        "equation_indices": {
                            f"{row},{column}": equations[row, column]
                            for row in rows
                            for column in columns
                        },
                        "active_matching_indices": {
                            f"{row},{column}": active[row, column]
                            for row in rows
                            for column in columns
                        },
                        "surviving_monomial": list(monomial),
                        "surviving_coefficient": coefficient,
                    }
    return None
