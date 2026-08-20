"""Primary exact replay for the GLD29 uv-u-v-1 directed-spur divisor."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import sympy as sp


R = tuple(range(4))
Q0, Q1_VERTEX = 4, 5
PORTS = tuple(range(6, 10))
VERTICES = R + (Q0, Q1_VERTEX) + PORTS
EDGES = tuple(combinations(R, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, V, W = sp.symbols("u v w")
QA = U**2 + 1
Q1 = U**2 + 2 * U - 1
QB = U**2 - 2 * U - 1
Q2 = U**2 + 2 * U * W + 2 * U - 1


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


GENERIC_KEYS = tuple(
    key(*words)
    for words in (
        ("0000", "0011"), ("0011", "0011"), ("0100", "0100"),
        ("0101", "0000"), ("0101", "0101"), ("0010", "0010"),
        ("0001", "0001"), ("0002", "0002"), ("0200", "0200"),
        ("0020", "0020"), ("0100", "1000"), ("1100", "1100"),
        ("0000", "1100"), ("0110", "0000"), ("0110", "0110"),
        ("0000", "0110"), ("0000", "0101"), ("0011", "0000"),
    )
)
GENERIC_MULTIPLIERS = (
    -(U - 1) * (U + 1) * (U + W + 1) * Q1**2
    * (U * W + 4 * U + W**2 + 2 * W),
    -(U - 1) * (U + 1) * (U + W + 1) * Q1 * Q2
    * (U * W + 4 * U + W**2 + 2 * W),
    (U + 1) * (U + W + 1) * Q1 * Q2
    * (3 * U**3 * W + 8 * U**3 + 3 * U**2 * W**2 + 10 * U**2 * W
       + 4 * U**2 + 2 * U * W**2 + 7 * U * W + 4 * U + W**2 + 2 * W),
    (U - 1) * (U + 1) ** 2 * (U + W) * (W + 2) * (U + W + 1) * Q1 * Q2,
    -(U + 1) * (U + W) * QA * (W + 2) * (U + W + 1) * Q1 * Q2,
    (U - 1) * (U + 1) * (U + W + 1) * Q2
    * (U**3 * W + 6 * U**3 + U**2 * W**2 + 6 * U**2 * W + 8 * U**2
       + 2 * U * W**2 + 5 * U * W - 2 * U - W**2 - 2 * W),
    2 * U * (U - 1) * (U + 1) * (U + W + 1) * Q2
    * (U**2 * W + 3 * U**2 + U * W**2 + 3 * U * W + 4 * U + W**2 + 2 * W - 1),
    -2 * U * (U - 1) * (U + 1) ** 2 * (U + W) * (W + 2) * (U + W + 1) * Q2,
    -2 * U * (U + 1) ** 2 * (U + W) * (W + 2) * (U + W + 1) * Q1 * Q2,
    -2 * U * (U - 1) * (U + 1) ** 2 * (2 * U + W) * (U + W + 1) * Q2,
    2 * U * (U - 1) * (U + 1) * (U + W) * (W + 2) * (U + W + 1) * Q1 * Q2,
    -2 * U * (U + 1) ** 2 * (U + W) * (W + 2) * (U + W + 1) * Q1 * Q2,
    -2 * U * (U + 1) ** 2 * (U + W) * (W + 2) * (U + W + 1) * Q1 * Q2,
    2 * U * (U - 1) * (U + 1) * (U + W + 1) ** 2 * Q1 * Q2,
    -2 * U * (U + 1) * (U + W + 1) * Q1
    * (U**2 + U * W + W + 1) * Q2,
    -2 * U * (U + 1) * Q1 * (U**2 + U * W + W + 1) * Q2,
    -(U + W) * QA * (W + 2) * (U + W + 1) * Q1 * Q2,
    (U - 1) * (U + 1) * (U + W + 1) * Q2
    * (U**3 * W - U**2 * W**2 - 6 * U**2 * W - 4 * U**2
       - 2 * U * W**3 - 4 * U * W**2 + U * W + 4 * U + W**2 + 2 * W),
)

COMMON_CURVE_KEYS = tuple(
    key(*words)
    for words in (
        ("1010", "0000"), ("0110", "0000"), ("0010", "0010"),
        ("0020", "0020"), ("0110", "0110"), ("0200", "0200"),
        ("0100", "1000"), ("1100", "1100"), ("0002", "0002"),
        ("0100", "0100"), ("0000", "1100"), ("0101", "0000"),
        ("0000", "0110"), ("0001", "0001"), ("0101", "0101"),
        ("0000", "0101"), ("0011", "0000"),
    )
)
U_PLUS_W_MULTIPLIERS = (
    2 * U * (U - 1) * (U + 1) ** 2 * Q1,
    -(U - 1) * (U + 1) * Q1 * (3 * U**3 + U**2 + U - 1),
    -(U - 1) * (U + 1) * QA * (U**2 + 4 * U - 1),
    U * (U - 1) * (U + 1) ** 3 * QA,
    (U + 1) * QA * Q1 * (U**2 + 4 * U - 1),
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    2 * U * (U - 1) ** 2 * (U + 1) * QA * Q1,
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    -2 * U * (U - 1) ** 2 * (U + 1) ** 2 * QA,
    U * (U + 1) ** 2 * (3 * U - 5) * QA * Q1,
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    (U - 1) ** 2 * (U + 1) ** 2 * QA * Q1,
    (U + 1) * QA * Q1 * (U**2 + 4 * U - 1),
    (U - 1) ** 2 * (U + 1) * QA**2,
    -(U - 1) * (U + 1) * QA**2 * Q1,
    -(U - 1) * QA**2 * Q1,
    2 * U * (U - 1) ** 2 * (U + 1) ** 2 * QA,
)
W_MINUS_TWO_MULTIPLIERS = (
    2 * U * (U - 1) ** 2 * (U + 1) ** 2 * Q1,
    -(U - 1) ** 2 * (U + 1) * Q1 * (3 * U**3 + U**2 + U - 1),
    -(U - 1) ** 2 * (U + 1) * QA * (3 * U**2 - 1),
    2 * (U - 1) ** 2 * (U + 1) ** 2 * (2 * U - 1) * QA,
    (U - 1) * (U + 1) * QA * (3 * U**2 - 1) * Q1,
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    2 * U * (U - 1) ** 2 * (U + 1) * QA * Q1,
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    -2 * U * (U - 1) ** 2 * (U + 1) ** 2 * QA,
    2 * (U - 1) * (U + 1) ** 2 * QA * Q1,
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    (U - 1) ** 2 * (U + 1) ** 2 * QA * Q1,
    (U + 1) * QA * (3 * U**2 - 1) * Q1,
    (U - 1) ** 2 * (U + 1) * QA**2,
    -(U - 1) * (U + 1) * QA**2 * Q1,
    -(U - 1) * QA**2 * Q1,
    2 * U * (U - 1) ** 2 * (U + 1) ** 2 * QA,
)

U_PLUS_W_PLUS_ONE_KEYS = tuple(
    key(*words)
    for words in (
        ("0120", "0120"), ("0020", "0020"), ("0001", "0001"),
        ("0002", "0002"), ("0101", "0101"), ("0100", "0100"),
        ("0200", "0200"), ("0100", "1000"), ("1100", "1100"),
        ("0000", "1100"), ("0101", "0000"), ("0011", "0011"),
        ("0010", "0010"), ("0000", "0101"), ("0011", "0000"),
        ("0000", "0011"),
    )
)
U_PLUS_W_PLUS_ONE_MULTIPLIERS = (
    4 * U**2 * (U + 1) * QA * Q1,
    -2 * U * (U - 1) * (U + 1) * QA * Q1,
    4 * U * (U - 1) * (U + 1) * QA * (U**2 + U - 1),
    -2 * U * (U - 1) ** 2 * (U + 1) ** 2 * QA,
    -(U - 1) * (U + 1) * QA**2 * Q1,
    (U + 1) * QA * Q1 * (3 * U**3 - 5 * U**2 - U - 1),
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    2 * U * (U - 1) ** 2 * (U + 1) * QA * Q1,
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    -2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1,
    (U - 1) ** 2 * (U + 1) ** 2 * QA * Q1,
    -(U - 1) * (U + 1) * (3 * U - 1) * QA * Q1,
    (U - 1) * (U + 1) * (3 * U - 1) * QA * Q1,
    -(U - 1) * QA**2 * Q1,
    (U - 1) * (U + 1) * QA * (5 * U**3 - U**2 + U - 1),
    (U - 1) * (U + 1) * (3 * U - 1) * Q1**2,
)

Q2_KEYS = tuple(
    key(*words)
    for words in (
        ("1000", "1000"), ("0020", "0020"), ("0200", "0200"),
        ("0100", "1000"), ("1100", "0000"), ("0010", "0010"),
        ("0110", "0110"), ("1100", "1100"), ("0100", "0100"),
        ("0002", "0002"), ("0000", "1100"), ("0110", "0000"),
        ("0101", "0000"), ("0000", "0110"), ("0001", "0001"),
        ("0101", "0101"), ("0000", "0101"), ("0011", "0000"),
    )
)
Q2_MULTIPLIERS = (
    (U - 1) * (U + 1) ** 2 * QA * Q1 * (U**4 - 12 * U**3 + 4 * U**2 - 1),
    4 * U**2 * (U - 1) * (U + 1) ** 2 * QA * (3 * U**2 - 2 * U + 1),
    -2 * U**2 * (U + 1) * QA * Q1 * (U**4 - 4 * U**3 + 12 * U**2 - 1),
    (U - 1) ** 2 * (U + 1) * QA * Q1 * (U**4 + 6 * U**3 - 2 * U**2 + 2 * U + 1),
    -(U - 1) * (U + 1) * QA * Q1 * (U**4 - 12 * U**3 + 4 * U**2 - 1),
    -4 * U**2 * (U - 1) ** 2 * (U + 1) * QA * QB,
    4 * U**2 * (U - 1) * (U + 1) * QA * QB * Q1,
    -2 * U * (U - 1) ** 2 * (U + 1) ** 2 * QA * QB * Q1,
    (U - 1) * (U + 1) * QA * QB * Q1 * (3 * U**3 - 5 * U**2 - U - 1),
    -2 * U * (U - 1) ** 3 * (U + 1) ** 2 * QA * QB,
    -2 * U * (U - 1) ** 2 * (U + 1) ** 2 * QA * QB * Q1,
    -4 * U**2 * (U - 1) * (U + 1) * QA**2 * Q1,
    (U - 1) ** 3 * (U + 1) ** 2 * QA * QB * Q1,
    8 * U**3 * (U - 1) * (U + 1) * QB * Q1,
    (U - 1) ** 3 * (U + 1) * QA**2 * QB,
    -(U - 1) ** 2 * (U + 1) * QA**2 * QB * Q1,
    -(U - 1) ** 2 * QA**2 * QB * Q1,
    2 * U * (U - 1) ** 3 * (U + 1) ** 2 * QA * QB,
)

CYLINDER_KEYS = tuple(
    key(*words)
    for words in (
        ("0102", "0102"), ("0100", "0100"), ("0002", "0002"),
        ("0200", "0200"), ("0020", "0020"), ("0100", "1000"),
        ("1100", "1100"), ("0000", "1100"), ("0110", "0000"),
        ("0101", "0000"), ("0120", "0120"), ("1000", "1000"),
        ("1100", "0000"), ("0011", "0011"),
    )
)
L = 3 * U * W + U + 7 * W + 3
CYLINDER_MULTIPLIERS = (
    -2 * W * (W + 2) * L,
    2 * W * (6 * U * W**2 + 17 * U * W + 6 * U + 14 * W**2 + 41 * W + 18),
    (W + 2) * (3 * U * W**2 - 3 * U * W - 2 * U + 7 * W**2 - 7 * W - 4),
    -2 * (U * W**3 + 5 * U * W**2 + 5 * U * W + 2 * U + 2 * W**3 + 12 * W**2 + 15 * W + 6),
    -2 * (W + 1) * (2 * U * W + 2 * U + 5 * W + 4),
    -2 * (2 * U * W**3 + 4 * U * W**2 - U * W - 2 * U + 5 * W**3 + 9 * W**2 - W - 2),
    -2 * W * (W + 2) * L,
    -2 * W * (W + 2) * L,
    -2 * W * (U * W + 2 * U + 3 * W + 4),
    -2 * W * (W + 2) * (2 * U * W + U + 5 * W + 2),
    -2 * W * (3 * U * W + 2 * U + 7 * W + 6),
    -2 * (2 * U * W**3 + 2 * U * W**2 - 3 * U * W - 2 * U + 5 * W**3 + 5 * W**2 - 9 * W - 6),
    3 * U * W**3 + 3 * U * W**2 - 6 * U * W - 4 * U + 7 * W**3 + 7 * W**2 - 12 * W - 8,
    2 * (W + 2) * (2 * U * W + U + 5 * W + 2),
)

Q1_W_MINUS_U_KEYS = tuple(
    key(*words)
    for words in (
        ("1010", "0000"), ("0110", "0000"), ("0102", "0102"),
        ("0100", "0100"), ("0002", "0002"), ("0200", "0200"),
        ("0100", "1000"), ("1100", "1100"), ("0000", "1100"),
        ("0101", "0000"), ("0011", "0011"), ("1000", "1000"),
        ("1100", "0000"),
    )
)
Q1_W_MINUS_U_MULTIPLIERS = (
    U + 3, U + 5, -4, 8, 2 * U + 8, 2 * U - 2, -2 * U - 2,
    -4, -4, -2 * U - 2, -2 * U - 6, -2 * U - 2, 2,
)

Q1_W_MINUS_TWO_KEYS = tuple(
    key(*words)
    for words in (
        ("1010", "0000"), ("0102", "0102"), ("0100", "0100"),
        ("0002", "0002"), ("0200", "0200"), ("0100", "1000"),
        ("1100", "1100"), ("0000", "1100"), ("0101", "0000"),
        ("0011", "0011"), ("1000", "1000"), ("1100", "0000"),
    )
)
Q1_W_MINUS_TWO_BASE_MULTIPLIERS = (
    -U - 3, -2 * (U + 3), 4 * (U + 3), 2 * U + 5, -2,
    -2 * (U + 2), -2 * (U + 3), -2 * (U + 3), -2 * (U + 2),
    -U - 2, -2 * (U + 2), U + 3,
)
Q1_W_MINUS_TWO_MULTIPLIERS = tuple((1 - U) * value for value in Q1_W_MINUS_TWO_BASE_MULTIPLIERS)


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
            elif left in R and right in (Q0, Q1_VERTEX):
                edge_variable = p_index(right - Q0, left, root_word[left])
            elif left in R and right in PORTS:
                coefficient *= cross(left, right - PORTS[0], root_word, port_word)
            elif left == Q0 and right == Q1_VERTEX:
                pass
            elif left in (Q0, Q1_VERTEX) and right in PORTS:
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


def mod_q1(value):
    return sp.rem(sp.Poly(sp.expand(value), U), sp.Poly(Q1, U)).as_expr()


def assert_certificate(keys, multipliers, substitutions, detector):
    row, rhs = combine(keys, multipliers, substitutions)
    assert not row
    assert sp.factor(rhs - detector) == 0


def assert_q1_certificate(keys, multipliers, substitutions, detector):
    row, rhs = combine(keys, multipliers, substitutions)
    assert all(mod_q1(value) == 0 for value in row.values())
    assert mod_q1(rhs - detector) == 0


def main():
    f_sub = {V: (U + 1) / (U - 1)}
    generic_detector = 2 * U * (U + 1) ** 2 * (U + W) * (W + 2) * (U + W + 1) * Q1 * Q2
    assert_certificate(GENERIC_KEYS, GENERIC_MULTIPLIERS, f_sub, generic_detector)
    curve_detector = 2 * U * (U - 1) * (U + 1) ** 2 * QA * Q1
    assert_certificate(COMMON_CURVE_KEYS, U_PLUS_W_MULTIPLIERS, {**f_sub, W: -U}, curve_detector)
    assert_certificate(COMMON_CURVE_KEYS, W_MINUS_TWO_MULTIPLIERS, {**f_sub, W: -2}, curve_detector)
    assert_certificate(
        U_PLUS_W_PLUS_ONE_KEYS, U_PLUS_W_PLUS_ONE_MULTIPLIERS,
        {**f_sub, W: -U - 1}, curve_detector,
    )
    assert_certificate(
        Q2_KEYS, Q2_MULTIPLIERS, {**f_sub, W: -Q1 / (2 * U)},
        2 * U * (U - 1) ** 2 * (U + 1) ** 2 * QA * QB * Q1,
    )
    assert_q1_certificate(CYLINDER_KEYS, CYLINDER_MULTIPLIERS, {V: -U - 2}, 2 * W * (W + 2) * L)
    assert_q1_certificate(
        Q1_W_MINUS_U_KEYS, Q1_W_MINUS_U_MULTIPLIERS,
        {V: -U - 2, W: -U}, 4,
    )
    assert_q1_certificate(
        Q1_W_MINUS_TWO_KEYS, Q1_W_MINUS_TWO_MULTIPLIERS,
        {V: -U - 2, W: -2}, 4,
    )
    print("PASS: exact certificates close the full GLD29 uv-u-v-1 directed-spur divisor")


if __name__ == "__main__":
    main()
