"""Primary exact replay for the GLD24 balanced one-switch exclusion."""

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
T = sp.Symbol("t")

P0_BASE, P1_BASE, W_BASE, ALPHA_BASE = 0, 12, 24, 78
NVARIABLES = 81


GENERIC_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((1, 0, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 0, 2, 0), (0, 0, 2, 0)),
    ((0, 0, 0, 2), (0, 0, 0, 2)),
    ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 0), (0, 1, 1, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 0), (0, 1, 1, 0)),
    ((0, 1, 0, 1), (0, 1, 0, 1)),
    ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 0, 0, 0), (0, 1, 0, 1)),
    ((0, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
    ((0, 0, 0, 0), (0, 0, 1, 1)),
)

GENERIC_MULTIPLIERS = (
    -2 * T * (T + 1),
    4 * T * (T + 1),
    -4 * (T + 1),
    2 * T * (T + 1) ** 2,
    4 * T,
    4 * T,
    -4 * (T + 1),
    -4 * (T + 1),
    2 * (T**2 - 1),
    -4 * (T**2 - 1),
    -2 * (T**2 + 4 * T + 1),
    T**2 - 1,
    2 * (T**2 - 1),
    -2 * (T**2 + 4 * T + 1),
    T**2 - 1,
    2 * (T**2 + T + 2),
    2 * (T + 1) * (T + 2),
    2 * (T + 1) * (T + 2),
)

EXCEPTIONAL_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((1, 0, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 2, 0), (0, 1, 2, 0)),
    ((0, 1, 0, 2), (0, 1, 0, 2)),
    ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 1), (0, 1, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
)

EXCEPTIONAL_MULTIPLIERS = (
    sp.Rational(1, 2),
    -1,
    -1,
    2,
    -1,
    -1,
    -1,
    -1,
    1,
    sp.Rational(1, 2),
)


def p_index(which: int, root: int, colour: int) -> int:
    return (P0_BASE if which == 0 else P1_BASE) + 3 * root + colour


def w_index(left: int, right: int, lc: int, rc: int) -> int:
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return W_BASE + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


@lru_cache(maxsize=None)
def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((first, second),) + tail)
    return tuple(output)


MATCHINGS = perfect_matchings(VERTICES)
assert len(MATCHINGS) == 945


def cross_value(
    root: int,
    port: int,
    root_word: tuple[int, ...],
    port_word: tuple[int, ...],
) -> sp.Expr:
    colour = port_word[port]
    if root_word[root] != colour:
        return sp.Integer(0)
    if colour != 0:
        return sp.Integer(root == port)
    if root == port or (root, port) == (0, 1):
        return sp.Integer(1)
    if (root, port) == (1, 0):
        return T
    return sp.Integer(0)


def matching_term(
    matching: tuple[tuple[int, int], ...],
    root_word: tuple[int, ...],
    port_word: tuple[int, ...],
) -> tuple[int | None, sp.Expr]:
    variable = None
    coefficient = sp.Integer(1)
    x = (1, 1, 0)
    y = (1, -1, 0)

    for raw_left, raw_right in matching:
        left, right = sorted((raw_left, raw_right))
        edge_variable = None
        if left in ROOTS and right in ROOTS:
            edge_variable = w_index(left, right, root_word[left], root_word[right])
        elif left in ROOTS and right in (Q0, Q1):
            edge_variable = p_index(right - Q0, left, root_word[left])
        elif left in ROOTS and right in PORTS:
            port = right - PORTS[0]
            coefficient *= cross_value(left, port, root_word, port_word)
        elif left == Q0 and right == Q1:
            pass
        elif left in (Q0, Q1) and right in PORTS:
            port = right - PORTS[0]
            shore = x if left == Q0 else y
            coefficient *= shore[port_word[port]]
        elif left in PORTS and right in PORTS:
            return None, sp.Integer(0)
        else:
            raise AssertionError((left, right))

        if coefficient == 0:
            return None, sp.Integer(0)
        if edge_variable is not None:
            if variable is not None:
                return None, sp.Integer(0)
            variable = edge_variable
    return variable, sp.expand(coefficient)


def equation(
    port_word: tuple[int, ...], root_word: tuple[int, ...]
) -> tuple[dict[int, sp.Expr], sp.Expr]:
    row: dict[int, sp.Expr] = {}
    constant = sp.Integer(0)
    for matching in MATCHINGS:
        variable, coefficient = matching_term(matching, root_word, port_word)
        if coefficient == 0:
            continue
        if variable is None:
            constant += coefficient
        else:
            row[variable] = sp.expand(row.get(variable, 0) + coefficient)
    if len(set(port_word)) == 1 and root_word == port_word:
        row[ALPHA_BASE + port_word[0]] = sp.Integer(-1)
    return row, sp.expand(-constant)


def combine(
    keys: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
    multipliers: tuple[sp.Expr, ...],
    specialization: dict[sp.Symbol, sp.Expr] | None = None,
) -> tuple[dict[int, sp.Expr], sp.Expr]:
    combined: dict[int, sp.Expr] = {}
    combined_rhs = sp.Integer(0)
    for key, multiplier in zip(keys, multipliers, strict=True):
        row, rhs = equation(*key)
        if specialization:
            multiplier = sp.sympify(multiplier).subs(specialization)
            row = {
                variable: coefficient.subs(specialization)
                for variable, coefficient in row.items()
            }
            rhs = rhs.subs(specialization)
        for variable, coefficient in row.items():
            combined[variable] = sp.expand(
                combined.get(variable, 0) + multiplier * coefficient
            )
        combined_rhs = sp.expand(combined_rhs + multiplier * rhs)
    return {
        variable: sp.factor(coefficient)
        for variable, coefficient in combined.items()
        if coefficient != 0
    }, sp.factor(combined_rhs)


def main() -> None:
    assert all(
        0 <= variable < NVARIABLES
        for key in GENERIC_KEYS + EXCEPTIONAL_KEYS
        for variable in equation(*key)[0]
    )
    generic_row, generic_rhs = combine(GENERIC_KEYS, GENERIC_MULTIPLIERS)
    assert not generic_row
    assert generic_rhs == -4 * T * (T + 1)

    exceptional_row, exceptional_rhs = combine(
        EXCEPTIONAL_KEYS,
        EXCEPTIONAL_MULTIPLIERS,
        {T: sp.Integer(-1)},
    )
    assert not exceptional_row
    assert exceptional_rhs == 1
    print(
        "PASS: 945-match expansion gives an 18-row -4t(t+1) detector "
        "and a 10-row t=-1 contradiction"
    )


if __name__ == "__main__":
    main()
