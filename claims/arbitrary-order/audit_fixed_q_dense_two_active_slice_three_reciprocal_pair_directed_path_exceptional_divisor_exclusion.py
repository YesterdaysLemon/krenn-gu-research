"""Standalone recursive-permanent audit of the GLD51 directed-path closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, W = sp.symbols("u w")
ROW_KEYS = (
    ("1001", "0000"), ("0012", "0012"), ("0010", "0010"),
    ("0002", "0002"), ("0101", "0000"), ("0011", "0000"),
    ("1000", "0100"), ("0100", "0010"), ("0020", "0020"),
    ("0100", "0100"), ("0010", "0001"), ("0001", "0001"),
    ("0110", "0011"), ("0110", "0000"),
)


def word(value):
    return tuple(map(int, value))


def p_index(which, root, colour):
    return (0 if which == 0 else 12) + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour, root, port):
    if root == port:
        return sp.Integer(1)
    return {
        (0, 0, 1): U,
        (1, 1, 0): U / (U - 1),
        (0, 1, 2): -1 / (U + 1),
        (1, 2, 1): 1 / (U + 2),
        (0, 2, 3): W,
        (1, 3, 2): W / (W - 1),
    }.get((colour, root, port), sp.Integer(0))


def permanent(rows, ports, root_word, port_word):
    if not rows:
        return sp.Integer(1)
    first, total = rows[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        entry = cross_value(port_word[port], first, port)
        if entry:
            total += entry * permanent(
                rows[1:], ports[:index] + ports[index + 1 :], root_word, port_word
            )
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
            add_entry(
                row,
                w_index(left_root, right_root, root_word[left_root], root_word[right_root]),
                corrected * minor,
            )
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


def main():
    matrix, rhs = [], []
    for port_word, root_word in ROW_KEYS:
        row, value = equation(word(port_word), word(root_word))
        matrix.append([sp.factor(row.get(index, 0)) for index in range(81)])
        rhs.append(sp.factor(value))
    nullspace = DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix()
    assert nullspace.rows == 1
    vector = [sp.factor(nullspace[0, index]) for index in range(nullspace.cols)]
    detector = sp.factor(sum(value * target for value, target in zip(vector, rhs, strict=True)))
    assert detector != 0
    weights = [sp.factor(value / detector) for value in vector]
    assert sp.factor(sum(value * target for value, target in zip(weights, rhs, strict=True))) == 1
    denominator = sp.factor(sp.lcm([sp.denom(sp.cancel(value)) for value in weights]))
    assert denominator == U * W * (U - 1)
    print(
        "PASS: standalone recursive-permanent audit derives the GLD51 "
        "three-pair directed-path contradiction"
    )


if __name__ == "__main__":
    main()
