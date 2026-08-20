"""Primary 945-match replay for the GLD47 reverse-orbit closure."""

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
U, W = sp.symbols("u w")

CASES = {
    "minus_one": {
        "keys": (
            ("1000", "0010"), ("0010", "0010"), ("0020", "0020"),
            ("0200", "0200"), ("0002", "0002"), ("0011", "0000"),
            ("0110", "0110"), ("0100", "0100"), ("0011", "0011"),
            ("0010", "1011"), ("0011", "1001"), ("0010", "1000"),
            ("0010", "1110"), ("0000", "1100"), ("0101", "0000"),
            ("0001", "0001"), ("0000", "1001"),
        ),
        "weights": (
            1,
            2,
            sp.Rational(-3, 2),
            1 / (W - 1),
            1 / (W - 1),
            1 / W,
            -(W + 1) / (2 * W),
            -(W + 1) / (2 * W * (W - 1)),
            -(W - 1) / (2 * W),
            -(W - 1) ** 2 / (2 * W**2),
            -(W - 1) / W**2,
            (W - 1) / W**2,
            -(W - 1) * (W + 1) / (2 * W**2),
            (W - 1) / (2 * W**2),
            -1 / (W - 1),
            -(3 * W - 1) / (2 * W * (W - 1)),
            -(W - 1) / (2 * W**2),
        ),
        "denominator": 2 * W**2 * (W - 1),
    },
    "product": {
        "keys": (
            ("1000", "0010"), ("0010", "0010"), ("0010", "1000"),
            ("0020", "0020"), ("0001", "0001"), ("0012", "0012"),
            ("0011", "1001"), ("0011", "0011"), ("0000", "0011"),
            ("0000", "1001"), ("0011", "0000"), ("0100", "0100"),
            ("0110", "0000"), ("0210", "0210"), ("0111", "0010"),
        ),
        "weights": (
            -1 / U,
            2,
            -U * (U + 1),
            -(U - 2) / (U - 1),
            sp.Rational(-1, 2),
            -1,
            U * (U + 1),
            1,
            1 / (U + 1),
            -U * (U + 1) / (U - 1),
            -(U - 1) / 2,
            sp.Rational(1, 2),
            -(U + 1) / 2,
            -1,
            1,
        ),
        "denominator": 2 * U * (U - 1) * (U + 1),
    },
}


def word(value):
    return tuple(map(int, value))


def p_index(which, root, colour):
    return (0 if which == 0 else 12) + 3 * root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first, answer = vertices[0], []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = matchings(VERTICES)
assert len(MATCHINGS) == 945


def amplitudes(case):
    if case == "minus_one":
        return {
            (0, 0, 2): sp.Integer(-1),
            (0, 2, 0): W,
            (1, 2, 0): sp.Rational(1, 2),
            (1, 0, 2): W / (W - 1),
        }
    return {
        (0, 0, 2): U,
        (0, 2, 0): -1 / U,
        (1, 2, 0): U / (U - 1),
        (1, 0, 2): 1 / (U + 1),
    }


def cross(root, port, root_word, port_word, case):
    colour = port_word[port]
    if root_word[root] != colour:
        return 0
    if root == port:
        return sp.Integer(1)
    return amplitudes(case).get((colour, root, port), sp.Integer(0))


def equation(port_word, root_word, case):
    x, y = (1, 1, 0), (1, -1, 0)
    row, constant = {}, 0
    for matching in MATCHINGS:
        variable, coefficient = None, sp.Integer(1)
        for raw_left, raw_right in matching:
            left, right = sorted((raw_left, raw_right))
            edge_variable = None
            if left in ROOTS and right in ROOTS:
                edge_variable = w_index(left, right, root_word[left], root_word[right])
            elif left in ROOTS and right in (Q0, Q1):
                edge_variable = p_index(right - Q0, left, root_word[left])
            elif left in ROOTS and right in PORTS:
                coefficient *= cross(left, right - PORTS[0], root_word, port_word, case)
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


def main():
    for case, data in CASES.items():
        combined, rhs = {}, 0
        for (port_word, root_word), weight in zip(data["keys"], data["weights"], strict=True):
            row, value = equation(word(port_word), word(root_word), case)
            rhs += weight * value
            for index, coefficient in row.items():
                combined[index] = sp.factor(combined.get(index, 0) + weight * coefficient)
        assert not {index: value for index, value in combined.items() if value != 0}, case
        assert sp.factor(rhs) == 1, case
        denominator = sp.factor(sp.lcm([sp.denom(sp.cancel(value)) for value in data["weights"]]))
        assert denominator == sp.factor(data["denominator"]), case
    print(
        "PASS: 945-match expansion closes both GLD47 reverse-orbit "
        "exceptional divisor types"
    )


if __name__ == "__main__":
    main()
