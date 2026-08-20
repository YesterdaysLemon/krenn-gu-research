"""Primary exact replay for the GLD28 uv=1 directed-spur divisor."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import sympy as sp


R = tuple(range(4))
Q0, Q1 = 4, 5
PORTS = tuple(range(6, 10))
VERTICES = R + (Q0, Q1) + PORTS
EDGES = tuple(combinations(R, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, V, W = sp.symbols("u v w")
Q = U**2 + 1


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


DIVISOR_KEYS = tuple(
    key(*words)
    for words in (
        ("0000", "0011"), ("0011", "0011"), ("0100", "0100"),
        ("0101", "0000"), ("0010", "0010"), ("0001", "0001"),
        ("0002", "0002"), ("0200", "0200"), ("0020", "0020"),
        ("0100", "1000"), ("1100", "1100"), ("0000", "1100"),
        ("0110", "0000"), ("0110", "0110"), ("0000", "0110"),
        ("0011", "0000"),
    )
)
DIVISOR_MULTIPLIERS = (
    4 * U**2 * (U + W + 1) * (U * W + 4 * U + W**2 + 2 * W),
    2 * U * (U + W + 1) * (U * W + 2 * U + W)
    * (U * W + 4 * U + W**2 + 2 * W),
    -4 * U * (U + W + 1) * (U * W + 2 * U + W)
    * (U * W + 2 * U + W**2 + 3 * W),
    -2 * U * (U + 1) * (U + W) * (W + 2) * (U + W + 1)
    * (U * W + 2 * U + W),
    -2 * U * (U + W + 1) * (U * W + 2 * U + W)
    * (U * W + 4 * U + W**2 + 3 * W),
    -2 * U * (U + W + 1) * (U * W + 2 * U + W)
    * (U * W + 4 * U + W**2 + 2 * W),
    2 * U * (U + W) * (W + 2) * (U + W + 1) * (U * W + 2 * U + W),
    4 * U * (U + W) * (W + 2) * (U + W + 1) * (U * W + 2 * U + W),
    2 * U * (2 * U + W) * (U + W + 1) * (U * W + 2 * U + W),
    -4 * U**2 * (U + W) * (W + 2) * (U + W + 1) * (U * W + 2 * U + W),
    4 * U * (U + W) * (W + 2) * (U + W + 1) * (U * W + 2 * U + W),
    4 * U * (U + W) * (W + 2) * (U + W + 1) * (U * W + 2 * U + W),
    -4 * U**2 * (U + W + 1) ** 2 * (U * W + 2 * U + W),
    4 * U * W * (U + W + 1) * (U * W + 2 * U + W),
    4 * U * W * (U * W + 2 * U + W),
    (U + W + 1) * (U * W + 2 * U + W)
    * (U**2 * W**2 + 4 * U**2 * W + 4 * U**2 + U * W**3
       + 3 * U * W**2 + 4 * U * W + W**3 + 2 * W**2),
)

COMMON_CURVE_KEYS = tuple(
    key(*words)
    for words in (
        ("0100", "1110"), ("1010", "1010"), ("1100", "1100"),
        ("0020", "0020"), ("0200", "0200"), ("0100", "0100"),
        ("0100", "1000"), ("0110", "0110"), ("0002", "0002"),
        ("0000", "1100"), ("0110", "0000"), ("0101", "0000"),
        ("1100", "0000"), ("0010", "0010"), ("0000", "0110"),
        ("0011", "0000"),
    )
)
U_PLUS_W_MULTIPLIERS = (
    -4 * U * (U + 1), -4 * U * (U + 1), 4 * U * (U - 1),
    -2 * U**2 - U - 1, 4 * (U**2 - 2 * U - 1),
    -2 * (2 * U**2 - 7 * U - 3), 8 * U**2, -2 * (5 * U + 3),
    -2 * (U + 1), 4 * U * (U - 1), 2 * (U - 1) * (2 * U + 1),
    2 * (U + 1) ** 2, 4 * U, (U + 3) * (2 * U + 1),
    -2 * (5 * U + 3), 2 * (U + 1),
)
W_MINUS_TWO_MULTIPLIERS = (
    -2 * U**2 * (U - 1) * (U + 1), -2 * U**2 * (U - 1) * (U + 1),
    4 * U * (U - 1), -(U - 1) * (U**2 + 4 * U - 1),
    -2 * U * (U - 1) ** 2, 2 * (U - 1) * (U + 1) * (2 * U - 1),
    2 * U**2 * (U - 1) ** 2 * (U + 2),
    -2 * (U - 1) * (2 * U**2 + 3 * U - 1),
    -U * (U - 1) ** 2 * (U + 1), 4 * U * (U - 1),
    -U * (U - 1) * (U**3 - U**2 - 5 * U + 1),
    U * (U - 1) ** 2 * (U + 1) ** 2, 2 * U**2 * (U - 1),
    (U - 1) * (U**3 + 3 * U**2 + 3 * U - 1),
    -2 * (2 * U**2 + 3 * U - 1), U * (U - 1) ** 2 * (U + 1),
)

U_PLUS_W_PLUS_ONE_KEYS = tuple(
    key(*words)
    for words in (
        ("0120", "0120"), ("0020", "0020"), ("0001", "0001"),
        ("0002", "0002"), ("0100", "0100"), ("0200", "0200"),
        ("0100", "1000"), ("1100", "1100"), ("0000", "1100"),
        ("0101", "0000"), ("0011", "0011"), ("0010", "0010"),
        ("0011", "0000"), ("0000", "0011"),
    )
)
U_PLUS_W_PLUS_ONE_MULTIPLIERS = (
    4 * U * (U + 1) * Q, -4 * U**2 * Q, 2 * U * (3 * U - 1) * Q,
    -2 * U * (U - 1) * Q, -8 * U * Q, -4 * U * (U - 1) * Q,
    4 * U**2 * (U - 1) * Q, -4 * U * (U - 1) * Q,
    -4 * U * (U - 1) * Q, 2 * U * (U - 1) * (U + 1) * Q,
    -2 * U * (3 * U - 1) * Q, 2 * U * (3 * U - 1) * Q,
    Q * (3 * U**3 + U**2 + U - 1), 4 * U**2 * (3 * U - 1),
)

LAST_CURVE_KEYS = tuple(
    key(*words)
    for words in (
        ("1000", "1000"), ("1100", "1100"), ("0020", "0020"),
        ("0200", "0200"), ("0100", "0100"), ("0100", "1000"),
        ("1100", "0000"), ("0010", "0010"), ("0110", "0110"),
        ("0002", "0002"), ("0000", "1100"), ("0110", "0000"),
        ("0101", "0000"), ("0000", "0110"), ("0011", "0000"),
    )
)
LAST_CURVE_MULTIPLIERS = (
    U * (U + 1) * (U + 3) * Q, -(U + 1) ** 3 * Q, -U * (U + 1) * Q,
    -(U - 1) * (U + 1) * (U + 2) * Q,
    (U + 1) * Q * (U**2 + 2 * U - 1), -U * (U - 1) * (U + 1) * Q,
    -U * (U + 3) * Q, -(U + 1) * Q, 2 * (U + 1) * Q,
    -(U - 1) * Q, -(U + 1) ** 3 * Q, (U + 1) * Q**2,
    (U - 1) * (U + 1) * Q, 2 * (U + 1) ** 2, (U - 1) * Q,
)


def point_table(words, multipliers):
    return tuple(key(*pair) for pair in words), tuple(map(sp.sympify, multipliers))


POINT_A_KEYS, POINT_A_MULTIPLIERS = point_table(
    (
        ("0100", "1110"), ("1010", "1010"), ("1100", "1100"),
        ("1000", "1000"), ("0100", "0100"), ("0200", "0200"),
        ("0000", "1100"), ("0110", "0110"), ("0100", "1000"),
        ("0002", "0002"), ("0110", "0000"), ("0000", "0110"),
        ("0011", "0000"), ("0020", "0020"), ("0010", "0010"),
    ),
    (4, 4, -4, -4, 10, -4, -4, -6, -4, -2, -6, -6, 2, 1, 1),
)
POINT_B_KEYS, POINT_B_MULTIPLIERS = point_table(
    (
        ("1110", "0010"), ("1100", "0000"), ("0101", "0000"),
        ("0110", "0000"), ("0000", "1100"), ("0002", "0002"),
        ("0200", "0200"), ("0020", "0020"), ("0100", "0100"),
        ("0100", "1000"), ("1100", "1100"), ("0011", "0000"),
    ),
    (1, -1, 2, -2, -2, -1, -2, 1, 2, 2, -2, 1),
)
POINT_C_KEYS, POINT_C_MULTIPLIERS = point_table(
    (
        ("0100", "1110"), ("1010", "1010"), ("1100", "1100"),
        ("1000", "1000"), ("0200", "0200"), ("0000", "1100"),
        ("0010", "0010"), ("0110", "0110"), ("0100", "1000"),
        ("0020", "0020"), ("0002", "0002"), ("0110", "0000"),
        ("0000", "0110"), ("0100", "0100"), ("0011", "0000"),
    ),
    (-2, -2, -4, 2, -4, -4, -2, 6, -4, 4, -2, 6, -3, -2, 2),
)
POINT_D_KEYS, POINT_D_MULTIPLIERS = point_table(
    (
        ("0100", "1110"), ("1010", "1010"), ("0020", "0020"),
        ("0200", "0200"), ("0100", "1000"), ("0110", "0110"),
        ("0100", "0100"), ("0002", "0002"), ("1100", "0000"),
        ("0010", "0010"), ("0000", "0110"), ("0101", "0000"),
        ("0011", "0000"),
    ),
    (-2, -2, -1, -2, 2, -4, 4, -1, 1, 3, -4, 2, 1),
)

QUADRATIC_KEYS = tuple(
    key(*words)
    for words in (
        ("0120", "0120"), ("0020", "0020"), ("0002", "0002"),
        ("0100", "0100"), ("0101", "0000"), ("0200", "0200"),
        ("0100", "1000"), ("1100", "1100"), ("0000", "1100"),
        ("0011", "0000"), ("1000", "1000"), ("1100", "0000"),
    )
)
QUADRATIC_MULTIPLIERS = (
    -2 * U, U - 1, -1, 2 * U + 2, U + 1, -3 * U - 1,
    1 - U, -2, -2, 1, U + 3, U - 2,
)


def p_index(q, r, c):
    return (0 if q == 0 else 12) + 3 * r + c


def w_index(a, b, c, d):
    if a > b:
        a, b, c, d = b, a, d, c
    return 24 + 9 * EDGE_INDEX[(a, b)] + 3 * c + d


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = matchings(VERTICES)
assert len(MATCHINGS) == 945


def cross(root, port, root_word, port_word):
    colour = port_word[port]
    if root_word[root] != colour:
        return 0
    if colour != 0:
        return sp.Integer(root == port)
    if root == port:
        return sp.Integer(1)
    return {(0, 1): U, (1, 0): V, (0, 2): W}.get((root, port), sp.Integer(0))


def equation(port_word, root_word):
    x, y = (1, 1, 0), (1, -1, 0)
    row, constant = {}, 0
    for matching in MATCHINGS:
        variable, coefficient = None, sp.Integer(1)
        for raw_left, raw_right in matching:
            left, right = sorted((raw_left, raw_right))
            edge_variable = None
            if left in R and right in R:
                edge_variable = w_index(left, right, root_word[left], root_word[right])
            elif left in R and right in (Q0, Q1):
                edge_variable = p_index(right - Q0, left, root_word[left])
            elif left in R and right in PORTS:
                coefficient *= cross(left, right - PORTS[0], root_word, port_word)
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


def mod_q(value):
    return sp.rem(sp.Poly(sp.expand(value), U), sp.Poly(Q, U)).as_expr()


def assert_certificate(keys, multipliers, substitutions, detector):
    row, rhs = combine(keys, multipliers, substitutions)
    assert not row
    assert sp.factor(rhs - detector) == 0


def main():
    assert_certificate(
        DIVISOR_KEYS, DIVISOR_MULTIPLIERS, {V: 1 / U},
        -4 * U * (U + W) * (W + 2) * (U + W + 1) * (U * W + 2 * U + W),
    )
    assert_certificate(COMMON_CURVE_KEYS, U_PLUS_W_MULTIPLIERS, {V: 1 / U, W: -U}, 4 * (U + 1))
    assert_certificate(
        COMMON_CURVE_KEYS, W_MINUS_TWO_MULTIPLIERS, {V: 1 / U, W: -2},
        2 * U * (U - 1) ** 2 * (U + 1),
    )
    assert_certificate(
        U_PLUS_W_PLUS_ONE_KEYS, U_PLUS_W_PLUS_ONE_MULTIPLIERS,
        {V: 1 / U, W: -U - 1}, 4 * U * (U - 1) * Q,
    )
    assert_certificate(
        LAST_CURVE_KEYS, LAST_CURVE_MULTIPLIERS,
        {V: 1 / U, W: -2 * U / (U + 1)}, 2 * (U - 1) * Q,
    )
    assert_certificate(POINT_A_KEYS, POINT_A_MULTIPLIERS, {U: -1, V: -1, W: 1}, 4)
    assert_certificate(POINT_B_KEYS, POINT_B_MULTIPLIERS, {U: 1, V: 1, W: -2}, 2)
    assert_certificate(POINT_C_KEYS, POINT_C_MULTIPLIERS, {U: -1, V: -1, W: -2}, 4)
    assert_certificate(POINT_D_KEYS, POINT_D_MULTIPLIERS, {U: 1, V: 1, W: -1}, 2)
    row, rhs = combine(QUADRATIC_KEYS, QUADRATIC_MULTIPLIERS, {V: -U, W: -U - 1})
    assert all(mod_q(value) == 0 for value in row.values())
    assert mod_q(rhs - 2) == 0
    print("PASS: exact certificates close the full GLD28 uv=1 directed-spur divisor")


if __name__ == "__main__":
    main()
