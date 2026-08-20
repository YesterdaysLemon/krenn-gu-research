"""Independent no-import audit of the GLD25 two-amplitude switch exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
P0_BASE, P1_BASE, W_BASE, ALPHA_BASE = 0, 12, 24, 78

Monomial = tuple[int, int]
Poly = dict[Monomial, Fraction]
Uni = dict[int, Fraction]


def clean(value: Poly) -> Poly:
    return {term: coefficient for term, coefficient in value.items() if coefficient}


def constant(value: int | Fraction) -> Poly:
    coefficient = Fraction(value)
    return {(0, 0): coefficient} if coefficient else {}


ONE = constant(1)
U: Poly = {(1, 0): Fraction(1)}
V: Poly = {(0, 1): Fraction(1)}


def add(left: Poly, right: Poly) -> Poly:
    answer = dict(left)
    for term, coefficient in right.items():
        answer[term] = answer.get(term, Fraction(0)) + coefficient
    return clean(answer)


def scale(value: Poly, scalar: int | Fraction) -> Poly:
    factor = Fraction(scalar)
    return clean({term: factor * coefficient for term, coefficient in value.items()})


def multiply(left: Poly, right: Poly) -> Poly:
    answer: Poly = {}
    for (left_u, left_v), left_coefficient in left.items():
        for (right_u, right_v), right_coefficient in right.items():
            term = (left_u + right_u, left_v + right_v)
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


def difference(left: Poly, right: Poly) -> Poly:
    return add(left, scale(right, -1))


U_PLUS_ONE = add(U, ONE)
U_MINUS_ONE = add(U, constant(-1))
V_PLUS_ONE = add(V, ONE)
V_MINUS_ONE = add(V, constant(-1))
UV = multiply(U, V)
UV_PLUS_ONE = add(UV, ONE)
UV_MINUS_ONE = add(UV, constant(-1))
F = add(add(UV, scale(U, -1)), add(scale(V, -1), constant(-1)))
Q = add(add(power(U, 2), scale(U, 2)), constant(-1))
G = add(
    add(
        add(power(UV, 2), scale(multiply(power(U, 2), V), -3)),
        scale(multiply(U, power(V, 2)), -3),
    ),
    add(scale(UV, -4), add(scale(U, -1), add(scale(V, -1), constant(-1)))),
)


def p_index(which: int, root: int, colour: int) -> int:
    return (P0_BASE if which == 0 else P1_BASE) + 3 * root + colour


def w_index(left: int, right: int, lc: int, rc: int) -> int:
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return W_BASE + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour: int, root: int, port: int) -> Poly:
    if colour != 0:
        return ONE if root == port else {}
    if root == port:
        return ONE
    if (root, port) == (0, 1):
        return U
    if (root, port) == (1, 0):
        return V
    return {}


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
    updated = add(row.get(index, {}), value)
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
        add_entry(row, ALPHA_BASE + port_word[0], constant(-1))
    return row, rhs


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
    scale(product(U, V, U_PLUS_ONE, UV_PLUS_ONE), -2),
    scale(product(U, V, power(U_PLUS_ONE, 2), UV_PLUS_ONE), 2),
    scale(product(U, power(U_PLUS_ONE, 2), UV_PLUS_ONE), -2),
    scale(product(U, V, U_PLUS_ONE, V_PLUS_ONE, UV_PLUS_ONE), 2),
    scale(product(U, V, U_PLUS_ONE, F), -2),
    scale(product(U, V, U_PLUS_ONE, F), -2),
    product(power(U_PLUS_ONE, 2), UV_PLUS_ONE, F),
    product(power(U_PLUS_ONE, 2), UV_PLUS_ONE, F),
    scale(product(U_PLUS_ONE, UV_MINUS_ONE, UV_PLUS_ONE, F), -1),
    scale(product(U_PLUS_ONE, UV_MINUS_ONE, UV_PLUS_ONE, F), 2),
    product(U_PLUS_ONE, G),
    scale(product(UV_MINUS_ONE, UV_PLUS_ONE, F), -1),
    scale(product(U_PLUS_ONE, UV_MINUS_ONE, UV_PLUS_ONE, F), -1),
    product(U_PLUS_ONE, G),
    scale(product(UV_MINUS_ONE, UV_PLUS_ONE, F), -1),
    scale(product(U_PLUS_ONE, add(add(power(UV, 2), U), add(V, ONE))), 2),
    scale(product(U_PLUS_ONE, UV_PLUS_ONE, add(add(U, V), ONE)), 2),
    scale(product(U_PLUS_ONE, UV_PLUS_ONE, add(add(U, V), ONE)), 2),
)

U_MINUS_ONE_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 0, 2, 0), (0, 0, 2, 0)),
    ((0, 0, 0, 2), (0, 0, 0, 2)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 2, 0), (0, 1, 2, 0)),
    ((0, 1, 0, 2), (0, 1, 0, 2)),
    ((0, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
    ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 0, 0, 0), (0, 0, 1, 1)),
)
U_MINUS_ONE_MULTIPLIERS = (
    V_MINUS_ONE,
    scale(product(V_MINUS_ONE, V_PLUS_ONE), -1),
    V_MINUS_ONE,
    V_MINUS_ONE,
    scale(product(V_MINUS_ONE, V_PLUS_ONE), 2),
    scale(product(V_MINUS_ONE, V_PLUS_ONE), -1),
    scale(product(V_MINUS_ONE, V_PLUS_ONE), -1),
    scale(V_PLUS_ONE, -1),
    V_MINUS_ONE,
    scale(V_MINUS_ONE, -1),
    scale(V_MINUS_ONE, -1),
    V_MINUS_ONE,
)

UV_MINUS_ONE_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((1, 0, 0, 0), (1, 0, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 2, 0), (0, 1, 2, 0)),
    ((0, 1, 0, 2), (0, 1, 0, 2)),
    ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 1), (0, 1, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
)
UV_MINUS_ONE_MULTIPLIERS = (
    scale(U, 2),
    scale(product(U, U_PLUS_ONE), -2),
    scale(product(power(U, 2), U_PLUS_ONE), -2),
    scale(U_MINUS_ONE, -2),
    scale(Q, 4),
    scale(Q, -2),
    scale(Q, -2),
    scale(difference(power(U, 2), ONE), -1),
    scale(difference(power(U, 2), ONE), -1),
    scale(product(U_PLUS_ONE, Q), -1),
    scale(product(U_PLUS_ONE, Q), -1),
    scale(Q, 2),
    scale(add(add(power(U, 2), U), constant(-1)), 2),
)

F_ZERO_KEYS = (
    ((1, 1, 0, 0), (1, 1, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 0, 2, 0), (0, 0, 2, 0)),
    ((0, 0, 0, 2), (0, 0, 0, 2)),
    ((0, 0, 0, 0), (1, 1, 0, 0)),
    ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 0), (0, 1, 1, 0)),
    ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 0), (0, 1, 1, 0)),
    ((0, 1, 0, 1), (0, 1, 0, 1)),
    ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 0, 0, 0), (0, 1, 0, 1)),
    ((0, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
    ((0, 0, 0, 0), (0, 0, 1, 1)),
)
F_ZERO_MULTIPLIERS = (
    scale(product(U, power(U_PLUS_ONE, 2), Q), 2),
    scale(product(U, U_PLUS_ONE, Q, U_MINUS_ONE), -2),
    scale(product(U, power(U_PLUS_ONE, 2), Q), 2),
    scale(product(U_PLUS_ONE, Q, add(scale(power(U, 2), 2), add(U, ONE))), -2),
    scale(product(U, power(U_PLUS_ONE, 2), U_MINUS_ONE), 2),
    scale(product(U, power(U_PLUS_ONE, 2), U_MINUS_ONE), 2),
    scale(product(U, power(U_PLUS_ONE, 2), Q), 2),
    scale(product(power(U_PLUS_ONE, 2), Q, U_MINUS_ONE), -1),
    scale(product(power(U_PLUS_ONE, 2), Q, U_MINUS_ONE), -1),
    product(U_PLUS_ONE, add(power(U, 2), ONE), Q),
    scale(
        product(U_PLUS_ONE, add(scale(power(U, 2), 3), add(scale(U, 4), constant(-1))), U_MINUS_ONE),
        -1,
    ),
    product(add(power(U, 2), ONE), Q),
    product(U_PLUS_ONE, add(power(U, 2), ONE), Q),
    scale(
        product(U_PLUS_ONE, add(scale(power(U, 2), 3), add(scale(U, 4), constant(-1))), U_MINUS_ONE),
        -1,
    ),
    product(add(power(U, 2), ONE), Q),
    scale(product(U_PLUS_ONE, power(U_MINUS_ONE, 2)), 2),
    scale(product(U_PLUS_ONE, Q, U_MINUS_ONE), 2),
    scale(product(U_PLUS_ONE, Q, U_MINUS_ONE), 2),
)

POINT_KEYS = (
    ((1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 2, 0), (0, 1, 2, 0)),
    ((0, 1, 0, 2), (0, 1, 0, 2)),
    ((0, 1, 1, 1), (0, 1, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
)
POINT_MULTIPLIERS = tuple(
    constant(value)
    for value in (Fraction(1, 2), -1, 2, -1, -1, 1, Fraction(1, 2))
)

QUADRATIC_KEYS = (
    ((1, 1, 0, 0), (1, 1, 0, 0)),
    ((0, 1, 0, 0), (1, 0, 0, 0)),
    ((0, 2, 0, 0), (0, 2, 0, 0)),
    ((0, 1, 0, 0), (0, 1, 0, 0)),
    ((0, 1, 2, 0), (0, 1, 2, 0)),
    ((0, 1, 0, 2), (0, 1, 0, 2)),
    ((0, 0, 0, 0), (1, 1, 0, 0)),
    ((0, 0, 1, 0), (0, 0, 1, 0)),
    ((0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 1), (0, 1, 0, 0)),
    ((0, 0, 1, 1), (0, 0, 1, 1)),
)
QUADRATIC_MULTIPLIERS = (
    constant(-1),
    scale(U, -1),
    constant(-1),
    constant(3),
    constant(-1),
    constant(-1),
    constant(-1),
    constant(Fraction(-1, 2)),
    constant(Fraction(-1, 2)),
    scale(U_PLUS_ONE, Fraction(-1, 2)),
    scale(U_PLUS_ONE, Fraction(-1, 2)),
    ONE,
    ONE,
)


def combine(keys: tuple, multipliers: tuple[Poly, ...]) -> tuple[dict[int, Poly], Poly]:
    combined: dict[int, Poly] = {}
    combined_rhs: Poly = {}
    for key, multiplier in zip(keys, multipliers, strict=True):
        row, rhs = closed_form_equation(*key)
        for variable, coefficient in row.items():
            add_entry(combined, variable, multiply(multiplier, coefficient))
        combined_rhs = add(combined_rhs, multiply(multiplier, rhs))
    return combined, combined_rhs


def univariate_clean(value: Uni) -> Uni:
    return {exponent: coefficient for exponent, coefficient in value.items() if coefficient}


def univariate_add(left: Uni, right: Uni) -> Uni:
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, Fraction(0)) + coefficient
    return univariate_clean(answer)


def univariate_multiply(left: Uni, right: Uni) -> Uni:
    answer: Uni = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            answer[exponent] = answer.get(exponent, Fraction(0)) + (
                left_coefficient * right_coefficient
            )
    return univariate_clean(answer)


def univariate_power(value: Uni, exponent: int) -> Uni:
    answer: Uni = {0: Fraction(1)}
    for _ in range(exponent):
        answer = univariate_multiply(answer, value)
    return answer


def substitute_u(value: Poly, at: int | Fraction) -> Uni:
    answer: Uni = {}
    point = Fraction(at)
    for (u_exponent, v_exponent), coefficient in value.items():
        answer[v_exponent] = answer.get(v_exponent, Fraction(0)) + (
            coefficient * point**u_exponent
        )
    return univariate_clean(answer)


def substitute_uv_minus_one(value: Poly) -> Uni:
    answer: Uni = {}
    for (u_exponent, v_exponent), coefficient in value.items():
        exponent = u_exponent - v_exponent
        answer[exponent] = answer.get(exponent, Fraction(0)) + (
            coefficient * (-1) ** v_exponent
        )
    return univariate_clean(answer)


def substitute_f_zero_numerator(value: Poly) -> Uni:
    if not value:
        return {}
    denominator_degree = max(v_exponent for _, v_exponent in value)
    answer: Uni = {}
    for (u_exponent, v_exponent), coefficient in value.items():
        term = {u_exponent: coefficient}
        term = univariate_multiply(
            term,
            univariate_power({0: Fraction(1), 1: Fraction(1)}, v_exponent),
        )
        term = univariate_multiply(
            term,
            univariate_power(
                {0: Fraction(-1), 1: Fraction(1)},
                denominator_degree - v_exponent,
            ),
        )
        answer = univariate_add(answer, term)
    return answer


def evaluate_point(value: Poly, u_value: int, v_value: int) -> Fraction:
    return sum(
        coefficient * Fraction(u_value) ** u_exponent * Fraction(v_value) ** v_exponent
        for (u_exponent, v_exponent), coefficient in value.items()
    )


def substitute_quadratic(value: Poly) -> Uni:
    answer: Uni = {}
    minus_u_minus_two = {0: Fraction(-2), 1: Fraction(-1)}
    for (u_exponent, v_exponent), coefficient in value.items():
        term = univariate_multiply(
            {u_exponent: coefficient},
            univariate_power(minus_u_minus_two, v_exponent),
        )
        answer = univariate_add(answer, term)
    return answer


def reduce_q(value: Uni) -> Uni:
    answer = dict(value)
    while answer and max(answer) >= 2:
        exponent = max(answer)
        coefficient = answer.pop(exponent)
        answer[exponent - 1] = answer.get(exponent - 1, Fraction(0)) - 2 * coefficient
        answer[exponent - 2] = answer.get(exponent - 2, Fraction(0)) + coefficient
        answer = univariate_clean(answer)
    return answer


def assert_rows(rows: dict[int, Poly], check) -> None:
    assert all(not check(value) for value in rows.values())


def main() -> None:
    rows, rhs = combine(GENERIC_KEYS, GENERIC_MULTIPLIERS)
    assert not rows
    generic_target = scale(product(U, V, U_PLUS_ONE, UV_PLUS_ONE, F), 2)
    assert rhs == generic_target

    rows, rhs = combine(U_MINUS_ONE_KEYS, U_MINUS_ONE_MULTIPLIERS)
    assert_rows(rows, lambda value: substitute_u(value, -1))
    u_minus_one_target = scale(product(V, V_MINUS_ONE), 2)
    assert not substitute_u(difference(rhs, u_minus_one_target), -1)

    rows, rhs = combine(UV_MINUS_ONE_KEYS, UV_MINUS_ONE_MULTIPLIERS)
    assert_rows(rows, substitute_uv_minus_one)
    assert not substitute_uv_minus_one(difference(rhs, scale(Q, 2)))

    rows, rhs = combine(F_ZERO_KEYS, F_ZERO_MULTIPLIERS)
    assert_rows(rows, substitute_f_zero_numerator)
    f_zero_target = scale(product(U, power(U_PLUS_ONE, 2), Q), -2)
    assert not substitute_f_zero_numerator(difference(rhs, f_zero_target))

    rows, rhs = combine(POINT_KEYS, POINT_MULTIPLIERS)
    assert all(evaluate_point(value, -1, 1) == 0 for value in rows.values())
    assert evaluate_point(rhs, -1, 1) == 1

    rows, rhs = combine(QUADRATIC_KEYS, QUADRATIC_MULTIPLIERS)
    assert all(not reduce_q(substitute_quadratic(value)) for value in rows.values())
    assert not reduce_q(substitute_quadratic(difference(rhs, ONE)))

    print(
        "PASS: independent sparse-polynomial matching-type audit replays "
        "the generic detector and every exceptional stratum"
    )


if __name__ == "__main__":
    main()
