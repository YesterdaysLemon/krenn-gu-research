"""Standalone recursive-permanent audit of the GLD42 reciprocal spike chart."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, V = sp.symbols("u v")

DIVISOR_KEYS = (("1202", "0212"), ("2212", "2212"), ("0222", "0222"))
GENERIC_KEYS = (
    ("0000", "0011"),
    ("0001", "0001"),
    ("0002", "0002"),
    ("0010", "0010"),
    ("0011", "0000"),
    ("0011", "0011"),
    ("0020", "0020"),
    ("0101", "0000"),
    ("0110", "0000"),
    ("0200", "0200"),
    ("1000", "0010"),
    ("1001", "0000"),
    ("1100", "0000"),
)
POINT_KEYS = (
    ("0002", "0002"),
    ("0010", "0010"),
    ("0011", "0000"),
    ("0012", "0012"),
    ("0020", "0020"),
    ("0101", "0000"),
    ("0110", "0000"),
    ("0200", "0200"),
    ("1000", "0010"),
    ("1001", "0000"),
    ("1100", "0000"),
)


def word(value):
    return tuple(map(int, value))


def p_index(which, root, colour):
    return (0 if which == 0 else 12) + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour, root, port, u_value, v_value):
    if root == port:
        return sp.Integer(1)
    if colour == 0 and (root, port) == (0, 2):
        return u_value
    if colour == 1 and (root, port) == (2, 0):
        return v_value
    return sp.Integer(0)


def permanent(rows, ports, root_word, port_word, u_value, v_value):
    if not rows:
        return sp.Integer(1)
    first, total = rows[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        entry = cross_value(port_word[port], first, port, u_value, v_value)
        if entry:
            total += entry * permanent(
                rows[1:],
                ports[:index] + ports[index + 1 :],
                root_word,
                port_word,
                u_value,
                v_value,
            )
    return sp.expand(total)


def add_entry(row, index, value):
    value = sp.expand(row.get(index, 0) + value)
    if value:
        row[index] = value
    else:
        row.pop(index, None)


def equation(port_word, root_word, u_value, v_value):
    x, y = (1, 1, 0), (1, -1, 0)
    row = {}
    rhs = -permanent(ROOTS, ROOTS, root_word, port_word, u_value, v_value)
    for omitted_port in ROOTS:
        retained_ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            retained_roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(
                retained_roots,
                retained_ports,
                root_word,
                port_word,
                u_value,
                v_value,
            )
            colour = port_word[omitted_port]
            add_entry(row, p_index(0, missing_root, root_word[missing_root]), y[colour] * minor)
            add_entry(row, p_index(1, missing_root, root_word[missing_root]), x[colour] * minor)
    for left_port, right_port in EDGES:
        lc, rc = port_word[left_port], port_word[right_port]
        corrected = x[lc] * y[rc] + y[lc] * x[rc]
        retained_ports = tuple(port for port in ROOTS if port not in (left_port, right_port))
        for left_root, right_root in EDGES:
            retained_roots = tuple(root for root in ROOTS if root not in (left_root, right_root))
            minor = permanent(
                retained_roots,
                retained_ports,
                root_word,
                port_word,
                u_value,
                v_value,
            )
            add_entry(
                row,
                w_index(left_root, right_root, root_word[left_root], root_word[right_root]),
                corrected * minor,
            )
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


def derive(keys, u_value, v_value):
    rows, rhs = [], []
    for port_word, root_word in keys:
        row, value = equation(word(port_word), word(root_word), u_value, v_value)
        rows.append([sp.factor(row.get(index, 0)) for index in range(81)])
        rhs.append(sp.factor(value))
    nullspace = sp.Matrix(rows).T.nullspace()
    assert len(nullspace) == 1
    vector = [sp.factor(value / nullspace[0][-1]) for value in nullspace[0]]
    detector = sp.factor(sum(value * target for value, target in zip(vector, rhs, strict=True)))
    return vector, detector


def main():
    divisor_vector, divisor = derive(DIVISOR_KEYS, U, V)
    assert divisor_vector == [-1 / V, U / V, 1]
    assert sp.factor(V * divisor) == U * V - U - V

    generic_vector, generic_detector = derive(GENERIC_KEYS, U, U / (U - 1))
    assert generic_detector == 1
    denominator_lcm = sp.factor(sp.lcm([sp.denom(sp.cancel(value)) for value in generic_vector]))
    assert denominator_lcm == U * (U - 1) * (U + 1)

    point_vector, point_detector = derive(
        POINT_KEYS,
        sp.Rational(-1),
        sp.Rational(1, 2),
    )
    assert point_detector == 1
    assert [sp.factor(2 * value) for value in point_vector] == [
        2,
        6,
        2,
        -4,
        -3,
        2,
        2,
        -2,
        2,
        2,
        2,
    ]

    masks = tuple(product((False, True), repeat=2))
    assert len(masks) == 4
    assert sum(all(mask) for mask in masks) == 1
    assert sum(not all(mask) for mask in masks) == 3
    print(
        "PASS: standalone recursive-permanent audit derives the GLD42 divisor, "
        "generic curve core, exceptional point, and four-mask cover"
    )


if __name__ == "__main__":
    main()
