"""Primary exact replay for the GLD42 reciprocal two-slice spike chart."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import sympy as sp


ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
PORTS = tuple(range(6, 10))
VERTICES = ROOTS + (Q0, Q1) + PORTS
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


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first, answer = vertices[0], []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = matchings(VERTICES)
assert len(MATCHINGS) == 945


def cross(root, port, root_word, port_word, u_value, v_value):
    colour = port_word[port]
    if root_word[root] != colour:
        return 0
    if root == port:
        return sp.Integer(1)
    if colour == 0 and (root, port) == (0, 2):
        return u_value
    if colour == 1 and (root, port) == (2, 0):
        return v_value
    return sp.Integer(0)


def equation(port_word, root_word, u_value, v_value):
    x, y = (1, 1, 0), (1, -1, 0)
    row, constant = {}, 0
    for matching in MATCHINGS:
        variable, coefficient = None, sp.Integer(1)
        for raw_left, raw_right in matching:
            left, right = sorted((raw_left, raw_right))
            edge_variable = None
            if left in ROOTS and right in ROOTS:
                edge_variable = w_index(left, right, root_word[left], root_word[right])
            elif left in ROOTS and right in (Q0, Q1):
                edge_variable = p_index(right - Q0, left, root_word[left])
            elif left in ROOTS and right in PORTS:
                coefficient *= cross(
                    left,
                    right - PORTS[0],
                    root_word,
                    port_word,
                    u_value,
                    v_value,
                )
            elif left == Q0 and right == Q1:
                pass
            elif left in (Q0, Q1) and right in PORTS:
                coefficient *= (x if left == Q0 else y)[port_word[right - PORTS[0]]]
            elif left in PORTS and right in PORTS:
                coefficient = 0
            else:
                raise AssertionError((left, right))
            if coefficient == 0:
                break
            if edge_variable is not None:
                if variable is not None:
                    coefficient = 0
                    break
                variable = edge_variable
        if coefficient == 0:
            continue
        if variable is None:
            constant += coefficient
        else:
            row[variable] = sp.expand(row.get(variable, 0) + coefficient)
    if len(set(port_word)) == 1 and root_word == port_word:
        row[78 + port_word[0]] = -1
    return row, sp.expand(-constant)


def combine(keys, weights, u_value, v_value):
    combined, rhs = {}, 0
    for (port_word, root_word), weight in zip(keys, weights, strict=True):
        row, value = equation(word(port_word), word(root_word), u_value, v_value)
        rhs += weight * value
        for index, coefficient in row.items():
            combined[index] = sp.factor(combined.get(index, 0) + weight * coefficient)
    combined = {index: value for index, value in combined.items() if value != 0}
    return combined, sp.factor(rhs)


def main():
    divisor_row, divisor_rhs = combine(DIVISOR_KEYS, (1, -U, -V), U, V)
    assert divisor_row == {}
    assert divisor_rhs == -(U * V - U - V)

    generic_v = U / (U - 1)
    generic_weights = (
        -2 / (U + 1),
        2,
        -1,
        3,
        -2 * U - 1,
        -2,
        -(U - 2) / (U - 1),
        1,
        1,
        -1,
        -1 / U,
        1,
        1,
    )
    generic_row, generic_rhs = combine(GENERIC_KEYS, generic_weights, U, generic_v)
    assert generic_row == {}
    assert generic_rhs == 1
    cleared = sp.factor(U * (U - 1) * (U + 1))
    cleared_row, cleared_rhs = combine(
        GENERIC_KEYS,
        tuple(sp.factor(cleared * weight) for weight in generic_weights),
        U,
        generic_v,
    )
    assert cleared_row == {}
    assert cleared_rhs == cleared

    point_weights = (2, 6, 2, -4, -3, 2, 2, -2, 2, 2, 2)
    point_row, point_rhs = combine(
        POINT_KEYS,
        point_weights,
        sp.Rational(-1),
        sp.Rational(1, 2),
    )
    assert point_row == {}
    assert point_rhs == 2
    print(
        "PASS: 945-match GLD42 replay gives the reciprocal-spike divisor, "
        "generic curve contradiction, and exceptional-point core"
    )


if __name__ == "__main__":
    main()
