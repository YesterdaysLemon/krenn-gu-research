"""Primary exact replay for the GLD25 two-amplitude switch exclusion."""

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
U, V = sp.symbols("u v")
F = U * V - U - V - 1
Q = U**2 + 2 * U - 1


GENERIC_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)), ((1, 0, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)), ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 0, 2, 0), (0, 0, 2, 0)), ((0, 0, 0, 2), (0, 0, 0, 2)),
    ((0, 1, 1, 0), (0, 0, 0, 0)), ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 0), (0, 1, 1, 0)), ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 0, 1, 0), (0, 0, 1, 0)), ((0, 0, 0, 0), (0, 1, 1, 0)),
    ((0, 1, 0, 1), (0, 1, 0, 1)), ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 0, 0, 0), (0, 1, 0, 1)), ((0, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)), ((0, 0, 0, 0), (0, 0, 1, 1)),
)

G = U**2 * V**2 - 3 * U**2 * V - 3 * U * V**2 - 4 * U * V - U - V - 1
GENERIC_MULTIPLIERS = (
    -2 * U * V * (U + 1) * (U * V + 1),
    2 * U * V * (U + 1) ** 2 * (U * V + 1),
    -2 * U * (U + 1) ** 2 * (U * V + 1),
    2 * U * V * (U + 1) * (V + 1) * (U * V + 1),
    -2 * U * V * (U + 1) * F,
    -2 * U * V * (U + 1) * F,
    (U + 1) ** 2 * (U * V + 1) * F,
    (U + 1) ** 2 * (U * V + 1) * F,
    -(U + 1) * (U * V - 1) * (U * V + 1) * F,
    2 * (U + 1) * (U * V - 1) * (U * V + 1) * F,
    (U + 1) * G,
    -(U * V - 1) * (U * V + 1) * F,
    -(U + 1) * (U * V - 1) * (U * V + 1) * F,
    (U + 1) * G,
    -(U * V - 1) * (U * V + 1) * F,
    2 * (U + 1) * (U**2 * V**2 + U + V + 1),
    2 * (U + 1) * (U * V + 1) * (U + V + 1),
    2 * (U + 1) * (U * V + 1) * (U + V + 1),
)

U_MINUS_ONE_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)), ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 0, 2, 0), (0, 0, 2, 0)), ((0, 0, 0, 2), (0, 0, 0, 2)),
    ((0, 1, 0, 0), (0, 1, 0, 0)), ((0, 1, 2, 0), (0, 1, 2, 0)),
    ((0, 1, 0, 2), (0, 1, 0, 2)), ((0, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)), ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)), ((0, 0, 0, 0), (0, 0, 1, 1)),
)
U_MINUS_ONE_MULTIPLIERS = (
    V - 1, -(V - 1) * (V + 1), V - 1, V - 1,
    2 * (V - 1) * (V + 1), -(V - 1) * (V + 1),
    -(V - 1) * (V + 1), -V - 1, V - 1, 1 - V, 1 - V, V - 1,
)

UV_MINUS_ONE_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)), ((1, 0, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)), ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)), ((0, 1, 2, 0), (0, 1, 2, 0)),
    ((0, 1, 0, 2), (0, 1, 0, 2)), ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)), ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)), ((0, 1, 1, 1), (0, 1, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
)
UV_MINUS_ONE_MULTIPLIERS = (
    2 * U, -2 * U * (U + 1), -2 * U**2 * (U + 1), -2 * (U - 1),
    4 * Q, -2 * Q, -2 * Q, -(U**2 - 1), -(U**2 - 1),
    -(U + 1) * Q, -(U + 1) * Q, 2 * Q, 2 * (U**2 + U - 1),
)

F_ZERO_KEYS = (
    ((1, 1, 0, 0), (1, 1, 0, 0)), ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((0, 2, 0, 0), (0, 2, 0, 0)), ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 0, 2, 0), (0, 0, 2, 0)), ((0, 0, 0, 2), (0, 0, 0, 2)),
    ((0, 0, 0, 0), (1, 1, 0, 0)), ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)), ((0, 1, 1, 0), (0, 1, 1, 0)),
    ((0, 0, 1, 0), (0, 0, 1, 0)), ((0, 0, 0, 0), (0, 1, 1, 0)),
    ((0, 1, 0, 1), (0, 1, 0, 1)), ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 0, 0, 0), (0, 1, 0, 1)), ((0, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)), ((0, 0, 0, 0), (0, 0, 1, 1)),
)
F_ZERO_MULTIPLIERS = (
    2 * U * (U + 1) ** 2 * Q,
    -2 * U * (U + 1) * Q * (U - 1),
    2 * U * (U + 1) ** 2 * Q,
    -2 * (U + 1) * Q * (2 * U**2 + U + 1),
    2 * U * (U + 1) ** 2 * (U - 1),
    2 * U * (U + 1) ** 2 * (U - 1),
    2 * U * (U + 1) ** 2 * Q,
    -(U + 1) ** 2 * Q * (U - 1),
    -(U + 1) ** 2 * Q * (U - 1),
    (U + 1) * (U**2 + 1) * Q,
    -(U + 1) * (3 * U**2 + 4 * U - 1) * (U - 1),
    (U**2 + 1) * Q,
    (U + 1) * (U**2 + 1) * Q,
    -(U + 1) * (3 * U**2 + 4 * U - 1) * (U - 1),
    (U**2 + 1) * Q,
    2 * (U + 1) * (U - 1) ** 2,
    2 * (U + 1) * Q * (U - 1),
    2 * (U + 1) * Q * (U - 1),
)

POINT_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)), ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)), ((0, 1, 2, 0), (0, 1, 2, 0)),
    ((0, 1, 0, 2), (0, 1, 0, 2)), ((0, 1, 1, 1), (0, 1, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
)
POINT_MULTIPLIERS = (sp.Rational(1, 2), -1, 2, -1, -1, 1, sp.Rational(1, 2))

QUADRATIC_KEYS = (
    ((1, 1, 0, 0), (1, 1, 0, 0)), ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((0, 2, 0, 0), (0, 2, 0, 0)), ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 2, 0), (0, 1, 2, 0)), ((0, 1, 0, 2), (0, 1, 0, 2)),
    ((0, 0, 0, 0), (1, 1, 0, 0)), ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)), ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)), ((0, 1, 1, 1), (0, 1, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
)
QUADRATIC_MULTIPLIERS = (
    -1, -U, -1, 3, -1, -1, -1, sp.Rational(-1, 2), sp.Rational(-1, 2),
    -(U + 1) / 2, -(U + 1) / 2, 1, 1,
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
    if (root, port) == (0, 1):
        return U
    if (root, port) == (1, 0):
        return V
    return sp.Integer(0)


def equation(port_word, root_word):
    x, y = (1, 1, 0), (1, -1, 0)
    row = {}
    constant = 0
    for matching in MATCHINGS:
        variable = None
        coefficient = sp.Integer(1)
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
                port = right - PORTS[0]
                coefficient *= (x if left == Q0 else y)[port_word[port]]
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


def combine(keys, multipliers, substitutions=None):
    combined, rhs = {}, 0
    for key, multiplier in zip(keys, multipliers, strict=True):
        row, value = equation(*key)
        multiplier = sp.sympify(multiplier)
        if substitutions:
            row = {index: entry.subs(substitutions) for index, entry in row.items()}
            value = value.subs(substitutions)
            multiplier = multiplier.subs(substitutions)
        for index, entry in row.items():
            combined[index] = sp.factor(combined.get(index, 0) + multiplier * entry)
        rhs = sp.factor(rhs + multiplier * value)
    return {index: value for index, value in combined.items() if value != 0}, sp.factor(rhs)


def mod_q(value):
    numerator = sp.together(value).as_numer_denom()[0]
    return sp.rem(sp.Poly(numerator, U), sp.Poly(Q, U)).as_expr()


def main():
    row, rhs = combine(GENERIC_KEYS, GENERIC_MULTIPLIERS)
    assert not row and sp.factor(rhs) == 2 * U * V * (U + 1) * (U * V + 1) * F

    row, rhs = combine(U_MINUS_ONE_KEYS, U_MINUS_ONE_MULTIPLIERS, {U: -1})
    assert not row and rhs == 2 * V * (V - 1)

    row, rhs = combine(UV_MINUS_ONE_KEYS, UV_MINUS_ONE_MULTIPLIERS, {V: -1 / U})
    assert not row and sp.expand(rhs - 2 * Q) == 0

    row, rhs = combine(F_ZERO_KEYS, F_ZERO_MULTIPLIERS, {V: (U + 1) / (U - 1)})
    assert not row and sp.expand(rhs + 2 * U * (U + 1) ** 2 * Q) == 0

    row, rhs = combine(POINT_KEYS, POINT_MULTIPLIERS, {U: -1, V: 1})
    assert not row and rhs == 1

    row, rhs = combine(QUADRATIC_KEYS, QUADRATIC_MULTIPLIERS, {V: -U - 2})
    assert all(mod_q(value) == 0 for value in row.values())
    assert mod_q(rhs - 1) == 0
    print(
        "PASS: direct 945-match certificates exclude the generic chart, "
        "three divisors, one point, and the quadratic intersection"
    )


if __name__ == "__main__":
    main()
