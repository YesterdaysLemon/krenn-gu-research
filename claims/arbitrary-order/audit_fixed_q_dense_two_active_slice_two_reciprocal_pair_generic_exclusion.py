"""Standalone recursive-permanent audit of the five GLD44 orbit cores."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, W = sp.symbols("u w")

ORBIT_DATA = {
    "reverse": ((2, 0), (
        ("1000", "0010"), ("0002", "0002"), ("0010", "0010"),
        ("0010", "1000"), ("0020", "0020"), ("0011", "0011"),
        ("0001", "0001"), ("0000", "0011"), ("0011", "1001"),
        ("0000", "1001"), ("0011", "0000"), ("0200", "0200"),
        ("0110", "0000"), ("0110", "0110"), ("0100", "0100"),
        ("0000", "0110"), ("0101", "0000"),
    ), 2 * U * W**2 * (U - 1) * (U + 1) * (W + 1) * (U * W + 1)),
    "same_tail": ((0, 1), (
        ("1010", "0000"), ("1000", "0100"), ("0100", "0100"),
        ("0011", "0011"), ("0010", "0010"), ("0001", "0001"),
        ("0011", "0000"), ("0000", "0011"), ("0200", "0200"),
        ("0020", "0020"), ("0002", "0002"), ("0110", "0000"),
        ("0101", "0000"), ("1001", "0000"),
    ), W * (U + 1) ** 2 * (W - 1)),
    "same_head": ((1, 2), (
        ("1001", "0000"), ("1000", "0010"), ("0100", "0010"),
        ("0010", "0010"), ("0020", "0020"), ("0002", "0002"),
        ("0110", "0110"), ("0000", "0110"), ("0120", "0120"),
        ("0101", "0000"), ("0011", "0000"), ("0011", "0011"),
        ("0001", "0001"), ("0000", "0011"),
    ), U * W * (U + 1) * (U - W - 1) * (U + W + 1)),
    "chain": ((2, 1), (
        ("1001", "0000"), ("1000", "0010"), ("0010", "0010"),
        ("0020", "0020"), ("0011", "0011"), ("0000", "0011"),
        ("0001", "0001"), ("0100", "0100"), ("0011", "0000"),
        ("0002", "0002"), ("0110", "0110"), ("0110", "0000"),
        ("0000", "0110"), ("0200", "0200"), ("0011", "0101"),
        ("0010", "0100"), ("0000", "0101"),
    ), 2 * U * W**2 * (U - 1) * (U + 1) * (W - 1) * (U * W + W + 1)),
    "disjoint": ((1, 3), (
        ("1100", "0000"), ("1000", "0010"), ("0100", "0001"),
        ("0002", "0002"), ("0010", "0010"), ("0020", "0020"),
        ("0001", "0001"), ("0110", "0000"), ("0011", "0000"),
        ("0011", "0011"), ("0000", "0011"), ("1001", "0000"),
    ), U * W * (U - 1) * (U + 1) * (W - 1) * (W + 1)),
}


def word(value):
    return tuple(map(int, value))


def p_index(which, root, colour):
    return (0 if which == 0 else 12) + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour, root, port, second_edge):
    pairs = ((0, 2), second_edge)
    values = (U, W)
    reciprocal = (U / (U - 1), W / (W - 1))
    if root == port:
        return sp.Integer(1)
    if colour == 0:
        for edge, value in zip(pairs, values, strict=True):
            if (root, port) == edge:
                return value
    if colour == 1:
        for edge, value in zip(pairs, reciprocal, strict=True):
            if (port, root) == edge:
                return value
    return sp.Integer(0)


def permanent(rows, ports, root_word, port_word, second_edge):
    if not rows:
        return sp.Integer(1)
    first, total = rows[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        entry = cross_value(port_word[port], first, port, second_edge)
        if entry:
            total += entry * permanent(
                rows[1:], ports[:index] + ports[index + 1 :],
                root_word, port_word, second_edge
            )
    return sp.expand(total)


def add_entry(row, index, value):
    value = sp.expand(row.get(index, 0) + value)
    if value:
        row[index] = value
    else:
        row.pop(index, None)


def equation(port_word, root_word, second_edge):
    x, y = (1, 1, 0), (1, -1, 0)
    row = {}
    rhs = -permanent(ROOTS, ROOTS, root_word, port_word, second_edge)
    for omitted_port in ROOTS:
        retained_ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            retained_roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(retained_roots, retained_ports, root_word, port_word, second_edge)
            colour = port_word[omitted_port]
            add_entry(row, p_index(0, missing_root, root_word[missing_root]), y[colour] * minor)
            add_entry(row, p_index(1, missing_root, root_word[missing_root]), x[colour] * minor)
    for left_port, right_port in EDGES:
        lc, rc = port_word[left_port], port_word[right_port]
        corrected = x[lc] * y[rc] + y[lc] * x[rc]
        retained_ports = tuple(port for port in ROOTS if port not in (left_port, right_port))
        for left_root, right_root in EDGES:
            retained_roots = tuple(root for root in ROOTS if root not in (left_root, right_root))
            minor = permanent(retained_roots, retained_ports, root_word, port_word, second_edge)
            add_entry(row, w_index(left_root, right_root, root_word[left_root], root_word[right_root]), corrected * minor)
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


def derive(keys, second_edge):
    rows, rhs = [], []
    for port_word, root_word in keys:
        row, value = equation(word(port_word), word(root_word), second_edge)
        rows.append([sp.factor(row.get(index, 0)) for index in range(81)])
        rhs.append(sp.factor(value))
    nullspace = DomainMatrix.from_Matrix(sp.Matrix(rows).T).nullspace().to_Matrix()
    assert nullspace.rows == 1
    vector = [sp.factor(nullspace[0, index]) for index in range(nullspace.cols)]
    detector = sp.factor(sum(value * target for value, target in zip(vector, rhs, strict=True)))
    assert detector != 0
    weights = [sp.factor(value / detector) for value in vector]
    assert sp.factor(sum(value * target for value, target in zip(weights, rhs, strict=True))) == 1
    denominator = sp.factor(sp.lcm([sp.denom(sp.cancel(value)) for value in weights]))
    return denominator


def classify(first, second):
    a, b = first
    c, d = second
    if a == d and b == c:
        return "reverse"
    if a == c:
        return "same_tail"
    if b == d:
        return "same_head"
    if b == c or d == a:
        return "chain"
    return "disjoint"


def main():
    for name, (edge, keys, expected_denominator) in ORBIT_DATA.items():
        assert derive(keys, edge) == sp.factor(expected_denominator), name

    directed_edges = tuple((i, j) for i in ROOTS for j in ROOTS if i != j)
    counts = {name: 0 for name in ORBIT_DATA}
    for first, second in combinations(directed_edges, 2):
        counts[classify(first, second)] += 1
    assert counts == {
        "reverse": 6,
        "same_tail": 12,
        "same_head": 12,
        "chain": 24,
        "disjoint": 12,
    }
    assert sum(counts.values()) == 66
    print(
        "PASS: standalone recursive-permanent audit derives the five GLD44 "
        "cores and exhausts all 66 two-pair support masks"
    )


if __name__ == "__main__":
    main()
