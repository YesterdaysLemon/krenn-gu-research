"""Primary exact replay for the GLD30 uv+vw+w+1 directed-spur divisor."""

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
H = U * V + V * W + W + 1
F = U * V - U - V - 1
QA = U**2 + 1
QB = U**2 - 2 * U - 1


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


GENERIC_KEYS = tuple(
    key(*words)
    for words in (
        ("0010", "0010"), ("0011", "0000"), ("0002", "0002"),
        ("1000", "1000"), ("0100", "1000"), ("0100", "0100"),
        ("1000", "0100"), ("0100", "0010"), ("1100", "0000"),
        ("0110", "0000"), ("0101", "0000"), ("1001", "0000"),
        ("0110", "0110"), ("0000", "0110"), ("1100", "1100"),
        ("0000", "1100"),
    )
)
GENERIC_MULTIPLIERS = (
    -U * (U + V) * (V + 1) ** 2 * (U * V + 1),
    -U * V * (U - 1) * (U + V) * (U * V - 2 * V - 1),
    U * V * (U - 1) * (U + V) * (U * V - 2 * V - 1),
    -U * (U + 1) * (U + V)
    * (U**2 * V**2 - U * V**3 - 5 * U * V**2 - 2 * U * V + V**2 - V - 1),
    -U * V * (U - 1) * (U + V) * (V + 1) * (U * V + 2 * U - 1),
    U * V * (U + V) * (V + 1) ** 2 * (U * V + 2 * U - 1),
    -(U + V)
    * (U**3 * V**2 + U**2 * V**4 + U**2 * V**3 - 3 * U**2 * V**2
       - 2 * U**2 * V + U * V**3 - U * V - U + 2 * V**2 + V),
    -U * (U + V) * (V + 1) ** 2 * (U * V + 2 * U - 1),
    U * (U + V)
    * (U**2 * V**2 - U * V**3 - 5 * U * V**2 - 2 * U * V + V**2 - V - 1),
    U * (U + V) ** 2 * (V + 1) * (U * V + 1),
    -U * V * (U - 1) * (U + V) * (U * V - 2 * V - 1),
    -U * V * (U - 1) * (U + V) * (U * V - 2 * V - 1),
    -U * (U + V) * (V + 1) * (U * V + 1) * (U * V - 2 * V - 1),
    -U * (V + 1) ** 2 * (U * V + 1) * (U * V - 2 * V - 1),
    U * (U + V)
    * (U**3 * V**2 + U**2 * V**4 + 2 * U**2 * V**3 - 2 * U**2 * V**2
       - 2 * U**2 * V - U * V**4 - 5 * U * V**3 - 7 * U * V**2
       - 3 * U * V - U + V**3 + 2 * V**2 - V - 1),
    U * (U + V)
    * (U**3 * V**2 + U**2 * V**4 + 2 * U**2 * V**3 - 2 * U**2 * V**2
       - 2 * U**2 * V - U * V**4 - 5 * U * V**3 - 7 * U * V**2
       - 3 * U * V - U + V**3 + 2 * V**2 - V - 1),
)

U_ONE_KEYS = tuple(
    key(*words)
    for words in (
        ("0010", "0010"), ("0011", "0000"), ("0002", "0002"),
        ("0100", "1000"), ("0100", "0100"), ("1000", "0100"),
        ("0100", "0010"), ("1100", "0000"), ("0110", "0000"),
        ("0101", "0000"), ("1010", "0000"), ("1001", "0000"),
        ("1010", "1010"), ("0100", "1110"),
    )
)
U_ONE_MULTIPLIERS = (
    -V * (V - 1) * (V + 3),
    -2 * V * (V - 1),
    2 * V * (V - 1),
    -2 * (V - 1) * (V + 1),
    V * (V - 1) * (V + 1) ** 2,
    -V * (V - 1) * (V + 1) ** 2,
    -(V - 1) * (V + 1) ** 2,
    -V * (V - 1) * (V + 1),
    V * (V**2 + 5 * V + 2),
    -2 * V * (V - 1),
    -V * (2 * V**2 + 3 * V + 3),
    -2 * V * (V - 1),
    2 * V * (V - 1) * (V + 1),
    2 * V * (V - 1) * (V + 1),
)

SUM_ZERO_KEYS = tuple(
    key(*words)
    for words in (
        ("0010", "0010"), ("0011", "0000"), ("0002", "0002"),
        ("1000", "1000"), ("0100", "1000"), ("0100", "0100"),
        ("1000", "0100"), ("0100", "0010"), ("1100", "0000"),
        ("0110", "0000"), ("0101", "0000"), ("1010", "0000"),
        ("1001", "0000"), ("1010", "1010"), ("0100", "1110"),
    )
)
SUM_ZERO_MULTIPLIERS = (
    2 * U * QA,
    U * QA**2,
    -U * QA**2,
    -U**2 * (U - 1) ** 2 * (U + 1) * QA,
    (U - 1) * (U + 1) ** 2 * QA,
    -U * (U - 1) ** 2 * (U + 1) * QA,
    (U - 1) ** 2 * (U + 1) * QA,
    -(U - 1) ** 2 * (U + 1) * QA,
    -U * (U - 1) * (U + 1) * QA,
    -U * (U - 1) * (U**3 + U**2 + 3 * U + 1),
    U * QA**2,
    -U * (U - 1) * (U**4 + U**3 + U**2 + U - 2),
    U * QA**2,
    U * (U - 1) * (U + 1) * QA**2,
    U * (U - 1) * (U + 1) * QA**2,
)

W_MINUS_TWO_KEYS = tuple(
    key(*words)
    for words in (
        ("0010", "0010"), ("0011", "0000"), ("0002", "0002"),
        ("1000", "1000"), ("0100", "1000"), ("0100", "0100"),
        ("1000", "0100"), ("0100", "0010"), ("1100", "0000"),
        ("0110", "0000"), ("0101", "0000"), ("1010", "0000"),
        ("1001", "0000"), ("0110", "0110"), ("0000", "0110"),
    )
)
W_MINUS_TWO_MULTIPLIERS = (
    U * (U - 2) * (U**2 - 3),
    U * (U - 2) * QB,
    -U * (U - 2) * QB,
    -2 * U * (U - 2) * (U - 1) * (U + 1),
    2 * U * (U - 2) ** 2 * (U - 1) * (U + 1),
    -2 * U * (U - 2) * (U - 1) * (U + 1),
    2 * (U - 1) ** 2,
    2 * U * (U - 2) ** 2 * (U - 1) * (U + 1),
    2 * U * (U - 2) * (U - 1),
    -U * (U - 2) * (U - 1) * (U**3 - U**2 - U - 3),
    U * (U - 2) * QB,
    U * (U - 2) * (U - 1) * QB,
    U * (U - 2) * QB,
    2 * U * (U - 1) * QB,
    2 * U * QB,
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


def assert_certificate(keys, multipliers, substitutions, detector):
    row, rhs = combine(keys, multipliers, substitutions)
    assert not row
    assert sp.factor(rhs - detector) == 0


def main():
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

    # Algebraic overlap checks used by the written exhaustive case split.
    assert sp.factor(H.subs(V, -1) - (1 - U)) == 0
    assert sp.factor(H.subs({U: 1, W: -1})) == 0
    assert sp.factor(H.subs({V: -U, W: -U - 1})) == 0
    assert sp.factor(H.subs({V: 1 / (U - 2), W: -2})) == 0
    assert sp.factor((U * V - 1).subs({U: 1, V: 1})) == 0
    assert sp.factor((U * V + 1).subs({U: 1, V: -1})) == 0
    assert sp.factor((U * V - 1).subs(V, -U) + QA) == 0
    assert sp.factor(F.subs(V, 1 / (U - 2)) + QB / (U - 2)) == 0
    print(
        "PASS: exact certificates close the full GLD30 uv+vw+w+1 divisor "
        "and complete the nonzero directed-spur chart"
    )


if __name__ == "__main__":
    main()
