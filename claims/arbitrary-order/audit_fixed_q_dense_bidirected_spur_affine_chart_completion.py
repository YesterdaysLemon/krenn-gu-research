"""Standalone recursive-permanent audit of the GLD40 affine chart completion."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, V, W, Z = sp.symbols("u v w z")


def key(port_word, root_word):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


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
    return {(0, 1): U, (1, 0): V, (0, 2): W, (2, 0): Z}.get((root, port), sp.Integer(0))


def permanent(rows, ports, root_word, port_word):
    if not rows:
        return sp.Integer(1)
    first, total = rows[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        edge = cross_value(port_word[port], first, port)
        if edge:
            total += edge * permanent(rows[1:], ports[:index] + ports[index + 1 :], root_word, port_word)
    return sp.expand(total)


def add_entry(row, index, value):
    value = sp.expand(row.get(index, 0) + value)
    if value:
        row[index] = value
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
        retained_ports = tuple(port for port in ROOTS if port not in (left_port, right_port))
        for left_root, right_root in EDGES:
            retained_roots = tuple(root for root in ROOTS if root not in (left_root, right_root))
            minor = permanent(retained_roots, retained_ports, root_word, port_word)
            add_entry(row, w_index(left_root, right_root, root_word[left_root], root_word[right_root]), corrected * minor)
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


def derive(row_keys, substitutions, expected_multiplier):
    rows, rhs = [], []
    for row_key in row_keys:
        row, value = equation(*row_key)
        rows.append([
            sp.factor(sp.sympify(row.get(index, 0)).subs(substitutions))
            for index in range(81)
        ])
        rhs.append(sp.factor(value.subs(substitutions)))
    nullspace = DomainMatrix.from_Matrix(sp.Matrix(rows).T).nullspace().to_Matrix()
    assert nullspace.rows == 1
    vector = [sp.factor(nullspace[0, index]) for index in range(nullspace.cols)]
    common = sp.factor(sp.gcd_list(vector))
    vector = [sp.factor(value / common) for value in vector]
    if vector[0].could_extract_minus_sign():
        vector = [-value for value in vector]
    assert vector == [1, -expected_multiplier]
    detector = sp.factor(sum(value * target for value, target in zip(vector, rhs, strict=True)))
    assert detector == expected_multiplier


def support_branch(mask):
    u_nonzero, v_nonzero, w_nonzero, z_nonzero = mask
    if u_nonzero:
        return "u"
    if w_nonzero:
        return "w"
    if v_nonzero:
        return "v_on_u=w=0"
    if z_nonzero:
        return "z_on_u=w=v=0"
    return "private_identity"


def main():
    derive((key("1022", "0122"), key("2122", "2122")), {}, U)
    derive((key("1202", "0212"), key("2212", "2212")), {}, W)
    boundary = {U: 0, W: 0}
    derive((key("0100", "1000"), key("1222", "1222")), boundary, V)
    derive((key("0010", "1000"), key("1222", "1222")), boundary, Z)

    branches = {support_branch(mask) for mask in product((False, True), repeat=4)}
    assert branches == {"u", "w", "v_on_u=w=0", "z_on_u=w=v=0", "private_identity"}
    assert support_branch((False, False, False, False)) == "private_identity"
    print(
        "PASS: standalone recursive-permanent audit derives all four GLD40 "
        "detectors and exhausts the 16 support masks"
    )


if __name__ == "__main__":
    main()
