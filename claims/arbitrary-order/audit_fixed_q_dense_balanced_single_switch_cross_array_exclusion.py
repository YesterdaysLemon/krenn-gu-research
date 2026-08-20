"""Independent no-import audit of the GLD24 balanced one-switch exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
P0_BASE, P1_BASE, W_BASE, ALPHA_BASE = 0, 12, 24, 78

Poly = tuple[Fraction, ...]
ZERO: Poly = ()
ONE: Poly = (Fraction(1),)
T: Poly = (Fraction(0), Fraction(1))


def poly(*coefficients: int | Fraction) -> Poly:
    values = [Fraction(value) for value in coefficients]
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def add_poly(left: Poly, right: Poly) -> Poly:
    size = max(len(left), len(right))
    return poly(
        *(
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(size)
        )
    )


def scale_poly(value: Poly, scalar: int | Fraction) -> Poly:
    return poly(*(coefficient * Fraction(scalar) for coefficient in value))


def multiply_poly(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return ZERO
    answer = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            answer[left_index + right_index] += left_value * right_value
    return poly(*answer)


def evaluate(value: Poly, at: int | Fraction) -> Fraction:
    answer = Fraction(0)
    for coefficient in reversed(value):
        answer = answer * Fraction(at) + coefficient
    return answer


def p_index(which: int, root: int, colour: int) -> int:
    return (P0_BASE if which == 0 else P1_BASE) + 3 * root + colour


def w_index(left: int, right: int, lc: int, rc: int) -> int:
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return W_BASE + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def cross_value(colour: int, root: int, port: int) -> Poly:
    if colour != 0:
        return ONE if root == port else ZERO
    if root == port or (root, port) == (0, 1):
        return ONE
    if (root, port) == (1, 0):
        return T
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
    total = ZERO
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
        total = add_poly(total, multiply_poly(edge, tail))
    return total


def add_entry(row: dict[int, Poly], index: int, value: Poly) -> None:
    if not value:
        return
    updated = add_poly(row.get(index, ZERO), value)
    if updated:
        row[index] = updated
    else:
        row.pop(index, None)


def closed_form_equation(
    port_word: tuple[int, ...], root_word: tuple[int, ...]
) -> tuple[dict[int, Poly], Poly]:
    """Derive one row from the three possible nonzero matching types."""

    x = (1, 1, 0)
    y = (1, -1, 0)
    row: dict[int, Poly] = {}
    rhs = scale_poly(permanent(ROOTS, ROOTS, root_word, port_word), -1)

    for omitted_port in ROOTS:
        retained_ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            retained_roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(
                retained_roots,
                retained_ports,
                root_word,
                port_word,
            )
            colour = port_word[omitted_port]
            add_entry(
                row,
                p_index(0, missing_root, root_word[missing_root]),
                scale_poly(minor, y[colour]),
            )
            add_entry(
                row,
                p_index(1, missing_root, root_word[missing_root]),
                scale_poly(minor, x[colour]),
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
            minor = permanent(
                retained_roots,
                retained_ports,
                root_word,
                port_word,
            )
            left_root, right_root = internal_roots
            add_entry(
                row,
                w_index(
                    left_root,
                    right_root,
                    root_word[left_root],
                    root_word[right_root],
                ),
                scale_poly(minor, corrected),
            )

    if len(set(port_word)) == 1 and root_word == port_word:
        add_entry(row, ALPHA_BASE + port_word[0], poly(-1))
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
    poly(0, -2, -2),
    poly(0, 4, 4),
    poly(-4, -4),
    poly(0, 2, 4, 2),
    poly(0, 4),
    poly(0, 4),
    poly(-4, -4),
    poly(-4, -4),
    poly(-2, 0, 2),
    poly(4, 0, -4),
    poly(-2, -8, -2),
    poly(-1, 0, 1),
    poly(-2, 0, 2),
    poly(-2, -8, -2),
    poly(-1, 0, 1),
    poly(4, 2, 2),
    poly(4, 6, 2),
    poly(4, 6, 2),
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
    Fraction(1, 2),
    Fraction(-1),
    Fraction(-1),
    Fraction(2),
    Fraction(-1),
    Fraction(-1),
    Fraction(-1),
    Fraction(-1),
    Fraction(1),
    Fraction(1, 2),
)


def generic_audit() -> None:
    combined: dict[int, Poly] = {}
    combined_rhs = ZERO
    for key, multiplier in zip(GENERIC_KEYS, GENERIC_MULTIPLIERS, strict=True):
        row, rhs = closed_form_equation(*key)
        for variable, coefficient in row.items():
            add_entry(
                combined,
                variable,
                multiply_poly(multiplier, coefficient),
            )
        combined_rhs = add_poly(combined_rhs, multiply_poly(multiplier, rhs))
    assert not combined
    assert combined_rhs == poly(0, -4, -4)


def exceptional_audit() -> None:
    combined: dict[int, Fraction] = {}
    combined_rhs = Fraction(0)
    for key, multiplier in zip(EXCEPTIONAL_KEYS, EXCEPTIONAL_MULTIPLIERS, strict=True):
        row, rhs = closed_form_equation(*key)
        for variable, coefficient in row.items():
            updated = combined.get(variable, Fraction(0)) + (
                multiplier * evaluate(coefficient, -1)
            )
            if updated:
                combined[variable] = updated
            else:
                combined.pop(variable, None)
        combined_rhs += multiplier * evaluate(rhs, -1)
    assert not combined
    assert combined_rhs == 1


def main() -> None:
    generic_audit()
    exceptional_audit()
    print(
        "PASS: independent polynomial matching-type audit replays "
        "-4t(t+1) and the exact t=-1 exception"
    )


if __name__ == "__main__":
    main()
