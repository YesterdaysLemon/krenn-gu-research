"""Primary exact replay for the GLD27 uv=-1 directed-spur divisor."""

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
Q = U**2 + 2 * U - 1

DIVISOR_KEYS = (
    ((0, 1, 0, 2), (0, 1, 0, 2)),
    ((1, 0, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((1, 0, 0, 0), (0, 1, 0, 0)),
    ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((1, 0, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
    ((1, 0, 0, 1), (0, 0, 0, 0)),
)
DIVISOR_MULTIPLIERS = (
    -2 * U * W * (U - 1) * Q,
    -2 * U**2 * W * (U - 1) * (U + 1),
    2 * U**2 * W * (U - 1) * (U + 1),
    -2 * U**3 * W * (U - 1) * (U + 1),
    2 * W * (U - 1) ** 2,
    2 * U**2 * W * (U - 1),
    U**2 * (W + 2) * Q,
    2 * U**2 * (U**2 + U * W + 2 * U - W - 1),
    U * (2 * U + W) * Q,
    -U**2 * W * (U - 1) * (U + 1) ** 2,
    -2 * U**2 * Q,
    U * W * (U - 1) ** 2 * (U + 1),
)

LINE_KEYS = (
    ((0, 1, 0, 2), (0, 1, 0, 2)), ((0, 1, 1, 0), (0, 1, 1, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)), ((0, 1, 0, 0), (0, 0, 1, 0)),
    ((1, 0, 0, 0), (1, 0, 0, 0)), ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((1, 1, 0, 0), (0, 0, 0, 0)), ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)), ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 0), (0, 1, 1, 0)), ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 1, 1, 1), (0, 0, 1, 0)), ((1, 0, 0, 1), (0, 0, 0, 0)),
)
LINE_MULTIPLIERS = (
    -2 * W * (W + 1) * (W + 2), -2 * W * (W + 2),
    2 * W * (W + 2) ** 2, -2 * (W + 2),
    -2 * W * (W + 1) * (W + 2), -2 * W * (W + 1) * (W + 2),
    W * (W + 1) * (W + 2), -2 * W * (W + 2),
    -2 * (W**3 + 4 * W**2 + 4 * W + 2), 2 * W, -2 * W,
    W**2 * (W + 3), 2 * (W + 1) * (W + 2), 2 * W,
)

POINT_MINUS_ONE_KEYS = (
    ((0, 1, 0, 2), (0, 1, 0, 2)), ((1, 0, 1, 0), (1, 0, 1, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)), ((0, 1, 0, 0), (0, 0, 1, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)), ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 0), (1, 1, 1, 0)), ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)), ((0, 1, 1, 1), (0, 0, 1, 0)),
    ((1, 0, 0, 1), (0, 0, 0, 0)), ((0, 1, 0, 1), (0, 0, 0, 0)),
)
POINT_MINUS_ONE_MULTIPLIERS = (
    -1, -1, -1, 1, 1, sp.Rational(1, 2), -1, 1,
    sp.Rational(-1, 2), -1, 1, 1,
)

POINT_MINUS_TWO_KEYS = (
    ((0, 1, 0, 2), (0, 1, 0, 2)), ((0, 1, 1, 0), (0, 1, 1, 0)),
    ((0, 1, 0, 0), (0, 0, 1, 0)), ((1, 0, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)), ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 0), (0, 0, 0, 0)), ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((1, 0, 1, 0), (0, 0, 0, 0)), ((1, 0, 0, 0), (1, 1, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)), ((0, 1, 1, 1), (0, 0, 1, 0)),
)
POINT_MINUS_TWO_MULTIPLIERS = (
    -1, 1, sp.Rational(-1, 2), -1, -1, sp.Rational(1, 2),
    sp.Rational(1, 2), sp.Rational(-1, 2), sp.Rational(-1, 2), 1,
    sp.Rational(1, 2), sp.Rational(-1, 2),
)

QUADRATIC_KEYS = (
    ((0, 1, 0, 2), (0, 1, 0, 2)), ((1, 1, 0, 0), (1, 1, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)), ((1, 0, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)), ((0, 0, 0, 0), (1, 1, 0, 0)),
    ((0, 1, 1, 0), (0, 0, 0, 0)), ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((1, 0, 1, 0), (0, 0, 0, 0)), ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)), ((1, 0, 0, 1), (0, 0, 0, 0)),
)
QUADRATIC_MULTIPLIERS = (
    -4 * W, -4 * W, -4 * U * W, 4 * W * (U + 2), 4 * W, -4 * W,
    -(U + 1) * (W + 2), -2 * (U + 1),
    -U * W - 2 * U - 3 * W - 2, -2 * U * W, 2 * (U + 1), 2 * W,
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
    for key, multiplier in zip(keys, multipliers, strict=True):
        row, value = equation(*key)
        multiplier = sp.sympify(multiplier).subs(substitutions)
        for index, coefficient in row.items():
            combined[index] = sp.factor(
                combined.get(index, 0) + multiplier * coefficient.subs(substitutions)
            )
        rhs = sp.factor(rhs + multiplier * value.subs(substitutions))
    return {index: value for index, value in combined.items() if value != 0}, rhs


def mod_q(value):
    return sp.rem(sp.Poly(sp.expand(value), U), sp.Poly(Q, U)).as_expr()


def main():
    row, rhs = combine(DIVISOR_KEYS, DIVISOR_MULTIPLIERS, {V: -1 / U})
    assert not row and sp.expand(rhs - 2 * U * W * (U - 1) * Q) == 0
    row, rhs = combine(LINE_KEYS, LINE_MULTIPLIERS, {U: 1, V: -1})
    assert not row and sp.expand(rhs - 2 * W * (W + 1) * (W + 2)) == 0
    row, rhs = combine(POINT_MINUS_ONE_KEYS, POINT_MINUS_ONE_MULTIPLIERS, {U: 1, V: -1, W: -1})
    assert not row and rhs == 1
    row, rhs = combine(POINT_MINUS_TWO_KEYS, POINT_MINUS_TWO_MULTIPLIERS, {U: 1, V: -1, W: -2})
    assert not row and rhs == 1
    row, rhs = combine(QUADRATIC_KEYS, QUADRATIC_MULTIPLIERS, {V: -U - 2})
    assert all(mod_q(value) == 0 for value in row.values())
    assert mod_q(rhs - 4 * W) == 0
    print("PASS: exact certificates close the full GLD27 uv=-1 directed-spur divisor")


if __name__ == "__main__":
    main()
