"""Independent matching-type audit of the GLD27 uv=-1 divisor exclusion."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
U, V, W = sp.symbols("u v w")
Q = U**2 + 2 * U - 1


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


DIVISOR_KEYS = tuple(
    key(*words)
    for words in (
        ("0102", "0102"), ("1000", "1000"), ("0100", "0100"),
        ("0100", "1000"), ("1000", "0100"), ("1100", "0000"),
        ("0110", "0000"), ("0001", "0001"), ("1010", "0000"),
        ("0101", "0000"), ("0011", "0011"), ("1001", "0000"),
    )
)
DIVISOR_MULTIPLIERS = (
    -2 * U * W * (U - 1) * Q, -2 * U**2 * W * (U - 1) * (U + 1),
    2 * U**2 * W * (U - 1) * (U + 1), -2 * U**3 * W * (U - 1) * (U + 1),
    2 * W * (U - 1) ** 2, 2 * U**2 * W * (U - 1), U**2 * (W + 2) * Q,
    2 * U**2 * (U**2 + U * W + 2 * U - W - 1), U * (2 * U + W) * Q,
    -U**2 * W * (U - 1) * (U + 1) ** 2, -2 * U**2 * Q,
    U * W * (U - 1) ** 2 * (U + 1),
)

LINE_KEYS = tuple(
    key(*words)
    for words in (
        ("0102", "0102"), ("0110", "0110"), ("0100", "0100"),
        ("0100", "0010"), ("1000", "1000"), ("0100", "1000"),
        ("1100", "0000"), ("0110", "0000"), ("0101", "0000"),
        ("0010", "0010"), ("0000", "0110"), ("0001", "0001"),
        ("0111", "0010"), ("1001", "0000"),
    )
)
LINE_MULTIPLIERS = (
    -2 * W * (W + 1) * (W + 2), -2 * W * (W + 2), 2 * W * (W + 2) ** 2,
    -2 * (W + 2), -2 * W * (W + 1) * (W + 2),
    -2 * W * (W + 1) * (W + 2), W * (W + 1) * (W + 2),
    -2 * W * (W + 2), -2 * (W**3 + 4 * W**2 + 4 * W + 2), 2 * W,
    -2 * W, W**2 * (W + 3), 2 * (W + 1) * (W + 2), 2 * W,
)

POINT_MINUS_ONE_KEYS = tuple(
    key(*words)
    for words in (
        ("0102", "0102"), ("1010", "1010"), ("0100", "1000"),
        ("0100", "0010"), ("0100", "0100"), ("1100", "0000"),
        ("0100", "1110"), ("0010", "0010"), ("0001", "0001"),
        ("0111", "0010"), ("1001", "0000"), ("0101", "0000"),
    )
)
POINT_MINUS_ONE_MULTIPLIERS = (
    -1, -1, -1, 1, 1, sp.Rational(1, 2), -1, 1,
    sp.Rational(-1, 2), -1, 1, 1,
)

POINT_MINUS_TWO_KEYS = tuple(
    key(*words)
    for words in (
        ("0102", "0102"), ("0110", "0110"), ("0100", "0010"),
        ("1000", "1000"), ("0100", "1000"), ("1100", "0000"),
        ("0110", "0000"), ("0101", "0000"), ("1010", "0000"),
        ("1000", "1110"), ("0001", "0001"), ("0111", "0010"),
    )
)
POINT_MINUS_TWO_MULTIPLIERS = (
    -1, 1, sp.Rational(-1, 2), -1, -1, sp.Rational(1, 2),
    sp.Rational(1, 2), sp.Rational(-1, 2), sp.Rational(-1, 2), 1,
    sp.Rational(1, 2), sp.Rational(-1, 2),
)

QUADRATIC_KEYS = tuple(
    key(*words)
    for words in (
        ("0102", "0102"), ("1100", "1100"), ("0100", "1000"),
        ("1000", "0100"), ("0100", "0100"), ("0000", "1100"),
        ("0110", "0000"), ("0001", "0001"), ("1010", "0000"),
        ("0101", "0000"), ("0011", "0011"), ("1001", "0000"),
    )
)
QUADRATIC_MULTIPLIERS = (
    -4 * W, -4 * W, -4 * U * W, 4 * W * (U + 2), 4 * W, -4 * W,
    -(U + 1) * (W + 2), -2 * (U + 1), -U * W - 2 * U - 3 * W - 2,
    -2 * U * W, 2 * (U + 1), 2 * W,
)


def p_index(which, root, colour):
    return (0 if which == 0 else 12) + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour, root, port):
    if colour != 0:
        return sp.Integer(root == port)
    if root == port:
        return sp.Integer(1)
    return {(0, 1): U, (1, 0): V, (0, 2): W}.get((root, port), sp.Integer(0))


def permanent(rows, ports, root_word, port_word):
    if not rows:
        return sp.Integer(1)
    first, total = rows[0], 0
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        edge = cross_value(port_word[port], first, port)
        if edge:
            total += edge * permanent(
                rows[1:], ports[:index] + ports[index + 1 :], root_word, port_word
            )
    return sp.expand(total)


def add_entry(row, index, value):
    updated = sp.expand(row.get(index, 0) + value)
    if updated:
        row[index] = updated
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
        if not corrected:
            continue
        retained_ports = tuple(p for p in ROOTS if p not in (left_port, right_port))
        for left_root, right_root in EDGES:
            retained_roots = tuple(r for r in ROOTS if r not in (left_root, right_root))
            minor = permanent(retained_roots, retained_ports, root_word, port_word)
            add_entry(
                row,
                w_index(left_root, right_root, root_word[left_root], root_word[right_root]),
                corrected * minor,
            )
    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, 78 + port_word[0], -1)
    return row, sp.expand(rhs)


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
    print("PASS: independent matching-type audit closes the GLD27 uv=-1 divisor")


if __name__ == "__main__":
    main()
