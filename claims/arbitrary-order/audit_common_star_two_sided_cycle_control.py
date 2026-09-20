"""Independent audit of the two-sided binary cycle control.

This script does not import the primary checker.  It reduces the triangular
parameter tower one polynomial at a time rather than using a Groebner basis,
and it reconstructs literal protected-K4 graphs on 36 physical vertices.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations
import json
from pathlib import Path

import sympy as sp


S, R, T = sp.symbols("s r t")
FS = 3 * S**2 + 3 * S + 1
PR = (
    (3 * S + 1) * R**4
    + 12 * (S + 1) * R**3
    - 6 * (3 * S + 1) * R**2
    + 12 * (S + 1) * R
    + 3 * S
    + 1
)
ET = (
    -2 * R * (R + 1) * (3 * S + 1) * T**2
    + (3 * R**2 * S + 3 * R**2 - 6 * R * S - 10 * R + 3 * S + 3) * T
    + 6 * (R + 1) * (2 * S + 1)
)

CYCLE = (0, 1, 2)
INCOMING = (3, 4)
OUTGOING = (5, 6)
CLOSING = (7, 8)
SIZE = 9


def permanent(matrix, rows, columns):
    rows = tuple(rows)
    columns = tuple(columns)
    if not rows:
        return sp.Integer(1)
    return sum(
        sp.prod(matrix[row, column] for row, column in zip(rows, order))
        for order in permutations(columns)
    )


def source(matrix_a, matrix_b, rows, columns):
    rows = tuple(rows)
    columns = tuple(columns)
    return sp.together(
        sum(
            permanent(matrix_a, selected_rows, selected_columns)
            * permanent(matrix_b, selected_rows, selected_columns)
            for degree in range(min(len(rows), len(columns)) + 1)
            for selected_rows in combinations(rows, degree)
            for selected_columns in combinations(columns, degree)
        )
    )


def reduce_sr(expression):
    """Reduce in Q(s)[r]/(PR), then Q[s]/(FS), without Groebner."""

    numerator = sp.cancel(expression).as_numer_denom()[0]
    r_domain = sp.QQ.frac_field(S)
    r_remainder = sp.Poly(numerator, R, domain=r_domain).rem(
        sp.Poly(PR, R, domain=r_domain)
    )
    reduced = []
    for (r_degree,), coefficient in r_remainder.terms():
        coefficient_numerator = sp.cancel(coefficient).as_numer_denom()[0]
        s_remainder = sp.Poly(coefficient_numerator, S, domain=sp.QQ).rem(
            sp.Poly(FS, S, domain=sp.QQ)
        )
        if s_remainder.as_expr():
            reduced.append(s_remainder.as_expr() * R**r_degree)
    return sp.expand(sum(reduced, sp.Integer(0)))


def triangular_remainder(expression):
    """Reduce t, then r, then s through the explicit triangular tower."""

    numerator = sp.cancel(expression).as_numer_denom()[0]
    t_domain = sp.QQ.frac_field(S, R)
    t_remainder = sp.Poly(numerator, T, domain=t_domain).rem(
        sp.Poly(ET, T, domain=t_domain)
    )
    reduced = []
    for (t_degree,), coefficient in t_remainder.terms():
        residual = sp.expand(reduce_sr(coefficient))
        if residual:
            reduced.append(residual * T**t_degree)
    return sp.expand(sum(reduced, sp.Integer(0)))


def equal_in_tower(left, right=0):
    return triangular_remainder(left - right) == 0


def build_matrices():
    q = -1 - S
    w = S / 2
    delta = -1 - 3 * w
    matrix_a = sp.zeros(SIZE)
    matrix_b = sp.zeros(SIZE)

    def add_arc(row, column, product, center=sp.Integer(1)):
        assert not matrix_a[row, column]
        matrix_a[row, column] = center
        matrix_b[row, column] = product / center

    for row in CYCLE:
        add_arc(row, (row + 1) % 3, q)
    for row in INCOMING:
        for column in CYCLE:
            add_arc(row, column, w)
    for row in CYCLE:
        for column in OUTGOING:
            add_arc(row, column, w)
    factor_block = ((R * T, T), (T, R * T))
    for row_position, row in enumerate(INCOMING):
        for column_position, column in enumerate(OUTGOING):
            add_arc(
                row,
                column,
                delta / 2,
                factor_block[row_position][column_position],
            )
    for row in OUTGOING:
        for column in CLOSING:
            add_arc(row, column, sp.Rational(-1, 2))
    for row in CLOSING:
        for column in INCOMING:
            add_arc(row, column, sp.Rational(-1, 2))
    return matrix_a, matrix_b


def parameter_report():
    norm = sp.factor(sp.resultant(FS, PR, S) / 3)
    expected = R**8 + 36 * R**6 + 134 * R**4 + 36 * R**2 + 1
    assert sp.expand(norm - expected) == 0
    forbidden = R * (R + 1) * (R**2 - 1) * (R**2 + 1)
    assert sp.gcd(sp.Poly(norm, R), sp.Poly(forbidden, R)) == 1

    # These lower-field factors control every leading coefficient, constant
    # coefficient, product, and denominator in the construction.
    for factor in (S, 1 + S, 2 + 3 * S, 3 * S + 1, 2 * S + 1):
        assert sp.gcd(sp.Poly(FS, S), sp.Poly(factor, S)) == 1

    return {
        "norm": str(norm),
        "forbidden_coprime": True,
        "tower_degrees": [2, 4, 2],
    }


def support_report(matrix_a, matrix_b):
    arcs = []
    for row in range(SIZE):
        for column in range(SIZE):
            assert bool(matrix_a[row, column]) == bool(matrix_b[row, column])
            if matrix_a[row, column]:
                assert row != column
                assert not matrix_a[column, row]
                arcs.append((row, column))
    assert len(arcs) == 27
    return tuple(arcs)


def component_cut_source(matrix_a, matrix_b, selected):
    selected = tuple(selected)
    complement = tuple(vertex for vertex in range(SIZE) if vertex not in selected)
    return source(matrix_a, matrix_b, selected, complement)


def physical_graph(matrix_a, matrix_b, selected):
    selected = set(selected)
    adjacency = [dict() for _ in range(4 * SIZE)]
    internal_matchings = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
    }

    def add_edge(left, right, weight):
        assert left != right and weight
        assert right not in adjacency[left]
        adjacency[left][right] = weight
        adjacency[right][left] = weight

    for component in range(SIZE):
        color = 0 if component in selected else 1
        for left, right in internal_matchings[color]:
            add_edge(4 * component + left, 4 * component + right, sp.Integer(1))

    for row in range(SIZE):
        if row not in selected:
            continue
        for column in range(SIZE):
            if column in selected or not matrix_a[row, column]:
                continue
            add_edge(4 * row, 4 * column, matrix_a[row, column])
            add_edge(4 * row + 1, 4 * column + 2, matrix_b[row, column])
    return adjacency


def physical_source(adjacency):
    """Literal weighted perfect-matching recurrence on the 36 vertices."""

    full_mask = (1 << len(adjacency)) - 1

    @lru_cache(maxsize=None)
    def recurse(mask):
        if not mask:
            return sp.Integer(1), 1
        active = [vertex for vertex in range(len(adjacency)) if mask & (1 << vertex)]
        first = min(
            active,
            key=lambda vertex: sum(
                bool(mask & (1 << neighbor)) for neighbor in adjacency[vertex]
            ),
        )
        without_first = mask & ~(1 << first)
        total = sp.Integer(0)
        supported = 0
        for second, weight in adjacency[first].items():
            if not (without_first & (1 << second)):
                continue
            subvalue, subcount = recurse(without_first & ~(1 << second))
            total += weight * subvalue
            supported += subcount
        return sp.together(total), supported

    return recurse(full_mask)


def check_localized_faces(matrix_a, matrix_b):
    q = -1 - S
    checked = 0
    for degree in range(4):
        for selected in combinations(CYCLE, degree):
            expected = (-q) ** degree if degree < 3 else 0
            assert equal_in_tower(source(matrix_a, matrix_b, INCOMING, selected), expected)
            assert equal_in_tower(source(matrix_a, matrix_b, selected, OUTGOING), expected)
            checked += 2
    return checked


def check_binary_cuts(matrix_a, matrix_b):
    counts = Counter()
    physical_supported = {}
    checked = 0
    for degree in (1, 2, 7, 8):
        for selected in combinations(range(SIZE), degree):
            component_value = component_cut_source(matrix_a, matrix_b, selected)
            physical_value, supported = physical_source(
                physical_graph(matrix_a, matrix_b, selected)
            )
            assert sp.cancel(component_value - physical_value) == 0
            assert equal_in_tower(component_value)
            counts[degree] += 1
            physical_supported["".join(map(str, selected))] = supported
            checked += 1
    assert checked == 90
    return {
        "cuts_checked": checked,
        "cuts_by_size": dict(sorted(counts.items())),
        "physical_component_mismatches": 0,
        "supported_matching_count_range": [
            min(physical_supported.values()),
            max(physical_supported.values()),
        ],
    }


def check_failure(matrix_a, matrix_b):
    selected = (0, 1, 3)
    expected = (R**2 + 1) / (12 * R)
    component_value = component_cut_source(matrix_a, matrix_b, selected)
    physical_value, supported = physical_source(physical_graph(matrix_a, matrix_b, selected))
    assert sp.cancel(component_value - physical_value) == 0
    assert equal_in_tower(component_value, expected)
    norm = R**8 + 36 * R**6 + 134 * R**4 + 36 * R**2 + 1
    assert sp.gcd(sp.Poly(norm, R), sp.Poly(R * (R**2 + 1), R)) == 1
    return {
        "selected_zero_components": list(selected),
        "word": "001011111",
        "value": "(r^2+1)/(12*r)",
        "supported_physical_matchings": supported,
        "nonzero": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    matrix_a, matrix_b = build_matrices()
    arcs = support_report(matrix_a, matrix_b)
    report = {
        "parameters": parameter_report(),
        "actual_factors": {
            "components": SIZE,
            "physical_vertices": 4 * SIZE,
            "arcs": len(arcs),
            "same_support": True,
            "loops": 0,
            "opposite_pairs": 0,
        },
        "localized_face_equations_checked": check_localized_faces(matrix_a, matrix_b),
        "binary_s1_same_s2": check_binary_cuts(matrix_a, matrix_b),
        "remaining_failure": check_failure(matrix_a, matrix_b),
        "third_color_distinct_s2": "NOT_SUPPLIED",
        "scope": "TWO_SIDED_FACE_PLUS_BINARY_S1_SAME_S2_CONTROL_ONLY",
        "global_status": "UNRESOLVED",
    }
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
        print(json.dumps({"status": "PASS", "output": str(args.output)}))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
