"""Matching-type audit of the GLD31 generic bidirected-spur exclusion."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import (
    H,
    KEYS,
    MULTIPLIERS,
    P,
    S_MINUS,
    S_PLUS,
    U,
    V,
    W,
    Z,
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
    return {
        (0, 1): U,
        (1, 0): V,
        (0, 2): W,
        (2, 0): Z,
    }.get((root, port), sp.Integer(0))


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


def main():
    combined, rhs = {}, 0
    for row_key, multiplier in zip(KEYS, MULTIPLIERS, strict=True):
        audit_row, audit_rhs = equation(*row_key)
        primary_row, primary_rhs = primary_equation(*row_key)
        assert all(
            sp.expand(audit_row.get(index, 0) - primary_row.get(index, 0)) == 0
            for index in set(audit_row) | set(primary_row)
        )
        assert sp.expand(audit_rhs - primary_rhs) == 0
        for index, coefficient in audit_row.items():
            combined[index] = sp.factor(combined.get(index, 0) + multiplier * coefficient)
        rhs = sp.factor(rhs + multiplier * audit_rhs)
    combined = {index: value for index, value in combined.items() if value != 0}
    detector = 2 * U * V * W * Z * (U * V + 1) * S_MINUS * S_PLUS * H * P
    assert not combined
    assert sp.factor(rhs - detector) == 0
    print(
        "PASS: recursive-permanent audit independently derives all 16 GLD31 rows "
        "and the generic bidirected-spur detector"
    )


if __name__ == "__main__":
    main()
