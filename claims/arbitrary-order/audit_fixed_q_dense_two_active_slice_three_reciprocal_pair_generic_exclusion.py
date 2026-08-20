"""Standalone recursive-permanent audit of the thirteen GLD50 orbit cores."""

from __future__ import annotations

from itertools import combinations, permutations

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, V, W = sp.symbols("u v w")


def rows(value):
    return tuple(tuple(part for part in item.split(":")) for item in value.split(","))


ORBIT_DATA = {
    ((0, 1), (0, 2), (0, 3)): (4, rows(
        "1001:0000,1000:0100,0100:0100,0011:0011,0010:0010,0001:0001,"
        "0011:0000,0000:0011,0200:0200,0020:0020,0002:0002,1000:0010,"
        "1000:0001,0110:0000,0101:0000"
    ), U * V * W * (U - 1) * (V - 1) * (W - 1) * (W + 1) * (V + W + 1)),
    ((0, 1), (0, 2), (1, 0)): (24, rows(
        "1000:0100,0020:0020,0002:0002,0011:0011,0010:0010,0001:0001,"
        "0000:0011,0100:0100,0011:0000,0200:0200,0110:0000,0101:0000,"
        "0110:0110,0000:0110,0101:0101,0000:0101"
    ), 2 * U * W * (U - 1) * (U + 1) * (U + V) * (V + 2) * (U * W + 1)
       * (U + V + 1) * (U * W + V * W + V + 1)),
    ((0, 1), (0, 2), (1, 2)): (24, rows(
        "1001:0000,1000:0010,0100:0010,0010:0010,0020:0020,0002:0002,"
        "0110:0110,0000:0110,0120:0120,0101:0000,0011:0000,0011:0011,"
        "0001:0001,0000:0011"
    ), V * W * (U - V) * (U + V + 1) * (U * W + V - W - 1)
       * (U * W + V + W + 1)),
    ((0, 1), (0, 2), (1, 3)): (24, rows(
        "1000:0010,0100:0001,0001:0001,0002:0002,0010:0010,0020:0020,"
        "0101:0101,0100:0100,0011:0000,0011:0011,0000:0011,0101:0000,"
        "0000:0101,0102:0102,0110:0000"
    ), U * V * W * (U + 1) * (V - 1) * (U * W + V * W + V + W + 1)),
    ((0, 1), (0, 2), (3, 0)): (12, rows(
        "1000:0100,0001:1000,0001:0001,0010:0010,0001:0010,0002:0002,"
        "0011:0011,0000:0011,0011:1010,0000:1010,0100:0100,0001:0100,"
        "0011:0000,0101:0000,1000:0010,0110:0000,0101:0101,0000:0101"
    ), U * V * W**3 * (U + 1) * (U + 2) * (U - V) * (V + 1) * (V + 2)
       * (W + 1)),
    ((0, 1), (0, 2), (3, 1)): (24, rows(
        "1000:0010,0001:0100,0001:0001,0002:0002,0011:0110,0000:0110,"
        "0011:0011,0000:0011,0010:0010,0020:0020,0100:0100,0011:0000,"
        "0101:0101,0101:0000,0000:0101,0200:0200"
    ), 2 * U * V * W**2 * (U + 1) * (V - 1) * (V + 1) * (W - 1)
       * (U + V + 1) * (U + V * W + V + W + 1)),
    ((0, 1), (1, 0), (2, 0)): (24, rows(
        "1000:0100,0002:0002,0010:1000,0010:0010,0020:0020,0011:1001,"
        "0000:1001,0011:0011,0000:0011,0001:0001,0100:0100,0010:0100,"
        "0011:0000,0100:1000,0110:0000,0101:0000,0110:0110,0000:0110"
    ), 2 * U * V * W**2 * (U + 1) * (U * V + 1) * (V + W + 1)
       * (U * V - V - 1)
       * (U**2 * V * W**2 - U**2 * V * W - U**2 * W**2 + U**2 * W
          - 4 * U * V * W**2 + U * V * W + 2 * U * V + U * W
          - 2 * V * W**2 + 2 * V * W - 2 * V + 4 * W**2 - 2 * W)),
    ((0, 1), (1, 0), (2, 3)): (12, rows(
        "1000:0100,0010:0001,0002:0002,0001:0001,0100:0100,0011:0011,"
        "0010:0010,0011:0000,0000:0011,0200:0200,0110:0000,0101:0000,"
        "0110:0101,0101:0101,0000:0101"
    ), 2 * U * V * W * (U - 1) * (U + 1) * (W - 1) * (W + 1) * (2 * W - 1)
       * (U * V + 1)),
    ((0, 1), (1, 2), (2, 0)): (8, rows(
        "1000:0100,0002:0002,0010:0010,0020:0020,0011:0011,0001:0001,"
        "0000:0011,0100:0010,0011:0000,0010:0100,0100:0100,0100:1000,"
        "0010:1000,0110:0000,0101:0000,0011:1001,0000:1001"
    ), 2 * U**2 * V * W**2 * (U * V * W - 1) * (U * V * W + 1)
       * (U * V + V + 1) * (V * W + W + 1) * (U * W - U - 2 * W + 1)
       * (U * V**2 * W - U * V * W + 2 * V**2 * W - 4 * V * W + V + 2 * W + 1)),
    ((0, 1), (1, 2), (2, 3)): (24, rows(
        "1001:0000,0012:0012,0002:0002,0010:0010,0011:0000,0101:0000,"
        "1000:0100,0100:0010,0001:0001,0011:0011,0000:0011,0100:0100,"
        "0010:0001,0110:0011,0110:0000"
    ), U * V**2 * W * (U - 1) * (U * V + V + 1)),
    ((0, 1), (1, 2), (3, 1)): (12, rows(
        "1000:0100,0001:0100,0001:0001,0002:0002,0011:0011,0010:0010,"
        "0000:0011,0011:0110,0000:0110,0001:0010,0100:0010,0100:0100,"
        "0011:0000,0101:0011,0101:0000,0101:0101,0000:0101"
    ), 2 * U * V**3 * W**2 * (U + 1) * (W - 1) * (U - W - 1) * (U + W + 1)
       * (U * V + V + 1)),
    ((0, 1), (1, 2), (3, 2)): (24, rows(
        "1000:0100,0001:0001,0100:0010,0010:0010,0020:0020,0100:0100,"
        "0002:0002,0011:0011,0011:0000,0000:0011,0001:0010,0101:0011,"
        "0101:0000,0101:0110,0000:0110,0101:0101,0000:0101"
    ), U * V**2 * W * (U - 1) * (U + 1) * (W - 1) * (W + 1)
       * (U * V + V + 1) * (2 * U * V * W - 2 * U * W + 2 * V * W - W - 1)),
    ((0, 1), (2, 1), (3, 1)): (4, rows(
        "1000:0100,0001:0100,0002:0002,0001:0001,0010:0100,0010:0010,"
        "0011:0000,0011:0011,0000:0011,0011:0101,0000:0101,0011:0110,"
        "0000:0110,0100:0100,0200:0200,0101:0000,0101:0101"
    ), 2 * U * V * W * (W - 1) * (U - V + 1) * (U + V + 1) * (U + W + 1)
       * (2 * V * W - V - W) * (U - V - W - 1)),
}


def word(value):
    return tuple(map(int, value))


def p_index(which, root, colour):
    return (0 if which == 0 else 12) + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour, root, port, support):
    if root == port:
        return sp.Integer(1)
    variables = (U, V, W)
    if colour == 0:
        for edge, value in zip(support, variables, strict=True):
            if (root, port) == edge:
                return value
    if colour == 1:
        for edge, value in zip(support, variables, strict=True):
            if (port, root) == edge:
                return value / (value - 1)
    return sp.Integer(0)


def permanent(rows_, ports, root_word, port_word, support):
    if not rows_:
        return sp.Integer(1)
    first, total = rows_[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        entry = cross_value(port_word[port], first, port, support)
        if entry:
            total += entry * permanent(
                rows_[1:], ports[:index] + ports[index + 1 :],
                root_word, port_word, support
            )
    return sp.expand(total)


def add_entry(row, index, value):
    value = sp.expand(row.get(index, 0) + value)
    if value:
        row[index] = value
    else:
        row.pop(index, None)


def equation(port_word, root_word, support):
    x, y = (1, 1, 0), (1, -1, 0)
    row = {}
    rhs = -permanent(ROOTS, ROOTS, root_word, port_word, support)
    for omitted_port in ROOTS:
        retained_ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            retained_roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(retained_roots, retained_ports, root_word, port_word, support)
            colour = port_word[omitted_port]
            add_entry(row, p_index(0, missing_root, root_word[missing_root]), y[colour] * minor)
            add_entry(row, p_index(1, missing_root, root_word[missing_root]), x[colour] * minor)
    for left_port, right_port in EDGES:
        lc, rc = port_word[left_port], port_word[right_port]
        corrected = x[lc] * y[rc] + y[lc] * x[rc]
        retained_ports = tuple(port for port in ROOTS if port not in (left_port, right_port))
        for left_root, right_root in EDGES:
            retained_roots = tuple(root for root in ROOTS if root not in (left_root, right_root))
            minor = permanent(retained_roots, retained_ports, root_word, port_word, support)
            add_entry(
                row,
                w_index(left_root, right_root, root_word[left_root], root_word[right_root]),
                corrected * minor,
            )
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


def canonical(support):
    answer = []
    for permutation in reversed(tuple(permutations(ROOTS))):
        answer.append(tuple(sorted((permutation[i], permutation[j]) for i, j in support)))
    return min(answer)


def main():
    directed_edges = tuple(reversed(tuple((i, j) for i in ROOTS for j in ROOTS if i != j)))
    census = {}
    for support in reversed(tuple(combinations(directed_edges, 3))):
        representative = canonical(support)
        census[representative] = census.get(representative, 0) + 1
    assert census == {support: data[0] for support, data in ORBIT_DATA.items()}
    assert len(census) == 13 and sum(census.values()) == 220

    for support, (_, keys, expected_denominator) in reversed(tuple(ORBIT_DATA.items())):
        matrix, rhs = [], []
        for port_word, root_word in reversed(keys):
            row, value = equation(word(port_word), word(root_word), support)
            matrix.append([sp.factor(row.get(index, 0)) for index in reversed(range(81))])
            rhs.append(sp.factor(value))
        nullspace = DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix()
        assert nullspace.rows == 1, support
        vector = [sp.factor(nullspace[0, index]) for index in range(nullspace.cols)]
        detector = sp.factor(sum(value * target for value, target in zip(vector, rhs, strict=True)))
        assert detector != 0, support
        weights = [sp.factor(value / detector) for value in vector]
        assert sp.factor(sum(value * target for value, target in zip(weights, rhs, strict=True))) == 1
        denominator = sp.factor(
            sp.lcm([sp.denom(sp.cancel(value)) for value in weights])
        )
        assert denominator == sp.factor(expected_denominator), support
    print(
        "PASS: standalone recursive-permanent audit derives all thirteen "
        "GLD50 cores and independently exhausts 220 support masks"
    )


if __name__ == "__main__":
    main()
