"""Independent no-import audit of the GLD26 generic directed-spur exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
P0_BASE, P1_BASE, W_BASE, ALPHA_BASE = 0, 12, 24, 78

Monomial = tuple[int, int, int]
Poly = dict[Monomial, Fraction]


def clean(value: Poly) -> Poly:
    return {term: coefficient for term, coefficient in value.items() if coefficient}


def monomial(
    u_exponent: int,
    v_exponent: int,
    w_exponent: int,
    coefficient: int | Fraction = 1,
) -> Poly:
    scalar = Fraction(coefficient)
    return {(u_exponent, v_exponent, w_exponent): scalar} if scalar else {}


ZERO: Poly = {}
ONE = monomial(0, 0, 0)
U = monomial(1, 0, 0)
V = monomial(0, 1, 0)
W = monomial(0, 0, 1)


def add(left: Poly, right: Poly) -> Poly:
    answer = dict(left)
    for term, coefficient in right.items():
        answer[term] = answer.get(term, Fraction(0)) + coefficient
    return clean(answer)


def sum_poly(*values: Poly) -> Poly:
    answer: Poly = {}
    for value in values:
        answer = add(answer, value)
    return answer


def scale(value: Poly, scalar: int | Fraction) -> Poly:
    factor = Fraction(scalar)
    return clean({term: factor * coefficient for term, coefficient in value.items()})


def multiply(left: Poly, right: Poly) -> Poly:
    answer: Poly = {}
    for (lu, lv, lw), left_coefficient in left.items():
        for (ru, rv, rw), right_coefficient in right.items():
            term = (lu + ru, lv + rv, lw + rw)
            answer[term] = answer.get(term, Fraction(0)) + (
                left_coefficient * right_coefficient
            )
    return clean(answer)


def product(*values: Poly) -> Poly:
    answer = ONE
    for value in values:
        answer = multiply(answer, value)
    return answer


def power(value: Poly, exponent: int) -> Poly:
    answer = ONE
    for _ in range(exponent):
        answer = multiply(answer, value)
    return answer


UV = multiply(U, V)
UV_MINUS_ONE = add(UV, scale(ONE, -1))
UV_PLUS_ONE = add(UV, ONE)
U_PLUS_ONE = add(U, ONE)
V_PLUS_ONE = add(V, ONE)
F = sum_poly(UV, scale(U, -1), scale(V, -1), scale(ONE, -1))
H = sum_poly(UV, multiply(V, W), W, ONE)
J = sum_poly(
    monomial(2, 2, 0),
    monomial(2, 1, 0, -2),
    monomial(1, 2, 0, -2),
    monomial(1, 1, 1, -1),
    monomial(1, 1, 0, -2),
    monomial(1, 0, 1, -1),
    monomial(1, 0, 0, -2),
    monomial(0, 2, 1, -1),
    monomial(0, 1, 1, -3),
    monomial(0, 1, 0, -2),
    monomial(0, 0, 1, -2),
    monomial(0, 0, 0, -3),
)


def p_index(which: int, root: int, colour: int) -> int:
    return (P0_BASE if which == 0 else P1_BASE) + 3 * root + colour


def w_index(left: int, right: int, lc: int, rc: int) -> int:
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return W_BASE + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour: int, root: int, port: int) -> Poly:
    if colour != 0:
        return ONE if root == port else ZERO
    if root == port:
        return ONE
    if (root, port) == (0, 1):
        return U
    if (root, port) == (1, 0):
        return V
    if (root, port) == (0, 2):
        return W
    return ZERO


def permanent(
    rows: tuple[int, ...],
    ports: tuple[int, ...],
    root_word: tuple[int, ...],
    port_word: tuple[int, ...],
) -> Poly:
    if not rows:
        return ONE
    first = rows[0]
    total: Poly = {}
    for index, port in enumerate(ports):
        if root_word[first] != port_word[port]:
            continue
        edge = cross_value(port_word[port], first, port)
        if not edge:
            continue
        tail = permanent(
            rows[1:],
            ports[:index] + ports[index + 1 :],
            root_word,
            port_word,
        )
        total = add(total, multiply(edge, tail))
    return total


def add_entry(row: dict[int, Poly], index: int, value: Poly) -> None:
    updated = add(row.get(index, ZERO), value)
    if updated:
        row[index] = updated
    else:
        row.pop(index, None)


def closed_form_equation(
    port_word: tuple[int, ...], root_word: tuple[int, ...]
) -> tuple[dict[int, Poly], Poly]:
    """Derive one complete row from the three possible matching types."""

    x = (1, 1, 0)
    y = (1, -1, 0)
    row: dict[int, Poly] = {}
    rhs = scale(permanent(ROOTS, ROOTS, root_word, port_word), -1)

    for omitted_port in ROOTS:
        retained_ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            retained_roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(retained_roots, retained_ports, root_word, port_word)
            colour = port_word[omitted_port]
            add_entry(
                row,
                p_index(0, missing_root, root_word[missing_root]),
                scale(minor, y[colour]),
            )
            add_entry(
                row,
                p_index(1, missing_root, root_word[missing_root]),
                scale(minor, x[colour]),
            )

    for omitted_ports in EDGES:
        left_port, right_port = omitted_ports
        left_colour = port_word[left_port]
        right_colour = port_word[right_port]
        corrected = x[left_colour] * y[right_colour] + y[left_colour] * x[right_colour]
        if not corrected:
            continue
        retained_ports = tuple(port for port in ROOTS if port not in omitted_ports)
        for internal_roots in EDGES:
            retained_roots = tuple(root for root in ROOTS if root not in internal_roots)
            minor = permanent(retained_roots, retained_ports, root_word, port_word)
            left_root, right_root = internal_roots
            add_entry(
                row,
                w_index(
                    left_root,
                    right_root,
                    root_word[left_root],
                    root_word[right_root],
                ),
                scale(minor, corrected),
            )

    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, ALPHA_BASE + port_word[0], scale(ONE, -1))
    return row, rhs


KEYS = (
    ((0, 0, 1, 1), (0, 0, 1, 1)),
    ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 0, 0), (0, 0, 1, 1)),
    ((0, 0, 0, 2), (0, 0, 0, 2)),
    ((1, 0, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((1, 0, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 0, 0), (0, 0, 1, 0)),
    ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((1, 0, 1, 0), (0, 0, 0, 0)),
    ((1, 0, 0, 1), (0, 0, 0, 0)),
)

MULTIPLIERS = (
    scale(product(U, V, W, UV_MINUS_ONE, UV_PLUS_ONE, H, J), -1),
    scale(
        product(U, V, W, UV_MINUS_ONE, UV_PLUS_ONE, sum_poly(U, V, scale(ONE, 2)), power(H, 2)),
        -1,
    ),
    product(U, V, W, UV_MINUS_ONE, UV_PLUS_ONE, H, J),
    product(U, V, W, UV_MINUS_ONE, sum_poly(U, V, scale(ONE, 2)), power(H, 3)),
    scale(product(U, V, W, UV_MINUS_ONE, power(UV_PLUS_ONE, 2), J), -1),
    scale(product(U, V, W, UV_MINUS_ONE, UV_PLUS_ONE, F, power(H, 2)), -1),
    product(U, V, W, U_PLUS_ONE, UV_MINUS_ONE, power(UV_PLUS_ONE, 2), power(H, 2)),
    scale(product(U, W, U_PLUS_ONE, UV_MINUS_ONE, power(UV_PLUS_ONE, 2), power(H, 2)), -1),
    product(U, V, W, V_PLUS_ONE, UV_MINUS_ONE, power(UV_PLUS_ONE, 2), power(H, 2)),
    scale(product(V, W, V_PLUS_ONE, UV_MINUS_ONE, power(UV_PLUS_ONE, 2), power(H, 2)), -1),
    product(U, UV_MINUS_ONE, power(UV_PLUS_ONE, 3), F, H),
    scale(product(U, V, W, UV_MINUS_ONE, power(UV_PLUS_ONE, 2), power(H, 2)), -1),
    product(U, V, W, power(UV_PLUS_ONE, 2), sum_poly(UV, scale(W, -1), scale(ONE, -1)), F, H),
    product(U, V, W, UV_MINUS_ONE, UV_PLUS_ONE, F, power(H, 2)),
    product(U, V, W, power(UV_PLUS_ONE, 2), sum_poly(UV, multiply(V, W), scale(ONE, -1)), F, H),
    product(U, V, W, UV_MINUS_ONE, UV_PLUS_ONE, F, power(H, 2)),
)


def main() -> None:
    combined: dict[int, Poly] = {}
    combined_rhs: Poly = {}
    for key, multiplier in zip(KEYS, MULTIPLIERS, strict=True):
        row, rhs = closed_form_equation(*key)
        for variable, coefficient in row.items():
            add_entry(combined, variable, multiply(multiplier, coefficient))
        combined_rhs = add(combined_rhs, multiply(multiplier, rhs))
    detector = product(
        U,
        V,
        W,
        UV_MINUS_ONE,
        power(UV_PLUS_ONE, 2),
        F,
        power(H, 2),
    )
    assert not combined
    assert combined_rhs == detector
    print(
        "PASS: independent sparse Q[u,v,w] matching-type audit replays "
        "the exact GLD26 generic directed-spur detector"
    )


if __name__ == "__main__":
    main()
