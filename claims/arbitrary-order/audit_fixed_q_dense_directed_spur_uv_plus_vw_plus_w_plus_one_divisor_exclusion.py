"""Matching-type audit of the GLD30 uv+vw+w+1 directed-spur divisor."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

from verify_fixed_q_dense_directed_spur_uv_plus_vw_plus_w_plus_one_divisor_exclusion import (
    F,
    GENERIC_KEYS,
    GENERIC_MULTIPLIERS,
    H,
    QA,
    QB,
    SUM_ZERO_KEYS,
    SUM_ZERO_MULTIPLIERS,
    U,
    U_ONE_KEYS,
    U_ONE_MULTIPLIERS,
    V,
    W,
    W_MINUS_TWO_KEYS,
    W_MINUS_TWO_MULTIPLIERS,
    equation as primary_equation,
)


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def p_index(which, root, colour):
    return (0 if which == 0 else 12) + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour, root, port):
    if colour != 0:
        return sp.Integer(root == port)
    if root == port:
        return sp.Integer(1)
    return {(0, 1): U, (1, 0): V, (0, 2): W}.get((root, port), sp.Integer(0))


def permanent(rows, ports, root_word, port_word):
    if not rows:
        return sp.Integer(1)
    first, total = rows[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        edge = cross_value(port_word[port], first, port)
        if edge:
            total += edge * permanent(
                rows[1:], ports[:index] + ports[index + 1 :], root_word, port_word
            )
    return sp.expand(total)


def add_entry(row, index, value):
    updated = sp.expand(row.get(index, 0) + value)
    if updated:
        row[index] = updated
    else:
        row.pop(index, None)


def equation(port_word, root_word):
    x, y = (1, 1, 0), (1, -1, 0)
    row = {}
    rhs = -permanent(ROOTS, ROOTS, root_word, port_word)
    for omitted_port in ROOTS:
        retained_ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            retained_roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(retained_roots, retained_ports, root_word, port_word)
            colour = port_word[omitted_port]
            add_entry(row, p_index(0, missing_root, root_word[missing_root]), y[colour] * minor)
            add_entry(row, p_index(1, missing_root, root_word[missing_root]), x[colour] * minor)
    for left_port, right_port in EDGES:
        lc, rc = port_word[left_port], port_word[right_port]
        corrected = x[lc] * y[rc] + y[lc] * x[rc]
        if not corrected:
            continue
        retained_ports = tuple(port for port in ROOTS if port not in (left_port, right_port))
        for left_root, right_root in EDGES:
            retained_roots = tuple(root for root in ROOTS if root not in (left_root, right_root))
            minor = permanent(retained_roots, retained_ports, root_word, port_word)
            add_entry(
                row,
                w_index(left_root, right_root, root_word[left_root], root_word[right_root]),
                corrected * minor,
            )
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


def combine(keys, multipliers, substitutions):
    combined, rhs = {}, 0
    for row_key, multiplier in zip(keys, multipliers, strict=True):
        row, value = equation(*row_key)
        multiplier = sp.sympify(multiplier).subs(substitutions)
        for index, coefficient in row.items():
            combined[index] = sp.factor(
                combined.get(index, 0) + multiplier * coefficient.subs(substitutions)
            )
        rhs = sp.factor(rhs + multiplier * value.subs(substitutions))
    return {index: value for index, value in combined.items() if value != 0}, rhs


def assert_certificate(keys, multipliers, substitutions, detector):
    row, rhs = combine(keys, multipliers, substitutions)
    assert not row
    assert sp.factor(rhs - detector) == 0


def main():
    tables = (
        (GENERIC_KEYS, GENERIC_MULTIPLIERS),
        (U_ONE_KEYS, U_ONE_MULTIPLIERS),
        (SUM_ZERO_KEYS, SUM_ZERO_MULTIPLIERS),
        (W_MINUS_TWO_KEYS, W_MINUS_TWO_MULTIPLIERS),
    )
    distinct_keys = tuple(dict.fromkeys(row_key for keys, _ in tables for row_key in keys))
    for row_key in distinct_keys:
        audit_row, audit_rhs = equation(*row_key)
        primary_row, primary_rhs = primary_equation(*row_key)
        assert all(
            sp.expand(audit_row.get(index, 0) - primary_row.get(index, 0)) == 0
            for index in set(audit_row) | set(primary_row)
        )
        assert sp.expand(audit_rhs - primary_rhs) == 0

    h_sub = {W: -(U * V + 1) / (V + 1)}
    assert sp.factor(H.subs(h_sub)) == 0
    assert_certificate(
        GENERIC_KEYS,
        GENERIC_MULTIPLIERS,
        h_sub,
        -U * V * (U - 1) * (U + V) * (U * V + 1) * (U * V - 2 * V - 1),
    )
    assert_certificate(
        U_ONE_KEYS, U_ONE_MULTIPLIERS, {U: 1, W: -1},
        -2 * V * (V - 1) * (V + 1),
    )
    assert_certificate(
        SUM_ZERO_KEYS, SUM_ZERO_MULTIPLIERS, {V: -U, W: -U - 1},
        -U * (U - 1) * (U + 1) * QA**2,
    )
    assert_certificate(
        W_MINUS_TWO_KEYS, W_MINUS_TWO_MULTIPLIERS,
        {V: 1 / (U - 2), W: -2},
        2 * U * (U - 1) * QB,
    )
    assert sp.factor(H.subs(V, -1) - (1 - U)) == 0
    assert sp.factor((U * V - 1).subs(V, -U) + QA) == 0
    assert sp.factor(F.subs(V, 1 / (U - 2)) + QB / (U - 2)) == 0
    print(
        f"PASS: recursive-permanent audit independently derives {len(distinct_keys)} rows "
        "and closes the full GLD30 divisor"
    )


if __name__ == "__main__":
    main()
