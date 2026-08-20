"""Primary 945-match replay for the GLD54 reverse-disjoint closure."""

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
U, V, W = sp.symbols("u v w")
CASES = {
    "u_minus": {
        "keys": (
            ("1000", "0100"), ("0100", "0100"), ("0010", "0001"),
            ("0002", "0002"), ("0001", "0001"), ("0011", "0011"),
            ("0010", "0010"), ("0011", "0000"), ("0000", "0011"),
            ("0200", "0200"), ("0110", "0101"), ("0101", "0101"),
            ("0100", "1101"), ("0000", "1001"),
        ),
        "weights": (
            1, (3 * V + 1) / (2 * V), (W**2 + 3 * W - 1) / (2 * V * W * (2 * W - 1)),
            (W - 2) * (V * W**2 + 2 * V * W - V - W**2) / (V * (V - 1) * (W - 1) * (2 * W - 1)),
            -(V * W**2 + 2 * V * W - 4 * V - W**2) / (2 * V * (V - 1) * (W - 1)),
            (W - 1) * (W + 1) / (2 * V * (2 * W - 1)), -(W + 1) / (2 * V),
            1 / (2 * V), (W - 1) * (W + 1) / (2 * V * (2 * W - 1)),
            sp.Rational(-3, 2), -(V + 1) / (2 * V * W), (V + 1) / (2 * V * (W - 1)),
            -(V - 1) * (V + 1) * (W - 2) / (2 * V**2 * (W - 1) * (W + 1)),
            (V - 1) * (W - 2) / (2 * V**2 * (W - 1) * (W + 1)),
        ),
        "denominator": 2 * V**2 * W * (V - 1) * (W - 1) * (W + 1) * (2 * W - 1),
    },
    "w_minus": {
        "keys": (
            ("1000", "0100"), ("0010", "0001"), ("0001", "0001"),
            ("0002", "0002"), ("0100", "0100"), ("0011", "0000"),
            ("0200", "0200"), ("0110", "0000"), ("0101", "0000"),
            ("0110", "0101"), ("0010", "0111"), ("0000", "0110"),
        ),
        "weights": (
            -1 / U, 1 / (2 * U * V), 1 / (U * V + 1),
            -(3 * U * V - 1) / (4 * U * V * (U * V + 1)), (5 * U * V - 1) / (4 * U * V),
            -(3 * U * V + 1) / (4 * U * V * (U * V + 1)), -(U - 2) / (U - 1),
            (U + 1) / (2 * U * V), (U + 1) / (2 * U * V), (U * V - 1) / (2 * U * V),
            -(U * V - 1) / (2 * U * V * (U + 1)), (U * V - 1) / (4 * U * V * (U + 1)),
        ),
        "denominator": 4 * U * V * (U - 1) * (U + 1) * (U * V + 1),
    },
    "w_half": {
        "keys": (
            ("1000", "0100"), ("0010", "0001"), ("0002", "0002"),
            ("0001", "0001"), ("0100", "0100"), ("0012", "0012"),
            ("0010", "0010"), ("0011", "0000"), ("0200", "0200"),
            ("0110", "0000"), ("0101", "0000"), ("0110", "0101"),
            ("0101", "0101"), ("0000", "0101"),
        ),
        "weights": (
            -1 / U, -1 / (U * V), -(5 * U * V - 1) / (2 * U * V * (U * V + 1)),
            (2 * U * V - 1) / (U * V * (U * V + 1)), (3 * U * V - 1) / (2 * U * V),
            -sp.Rational(3, 4) / (U * V), sp.Rational(3, 4) / (U * V), -1 / (2 * U * V),
            -(U - 2) / (U - 1), (U + 1) / (2 * U * V), (U + 1) / (2 * U * V),
            -(U * V - 1) / (U * V), -(U * V - 1) / (U * V), -(U * V - 1) / (U * V * (U + 1)),
        ),
        "denominator": 4 * U * V * (U - 1) * (U + 1) * (U * V + 1),
    },
    "product": {
        "keys": (
            ("1000", "0100"), ("0010", "0001"), ("0001", "0001"),
            ("0100", "0100"), ("0010", "0010"), ("0101", "0000"),
            ("0102", "0102"), ("0200", "0200"), ("0110", "0101"),
            ("0101", "0101"), ("0110", "0000"),
        ),
        "weights": (
            -1 / U, (W + 2) / (2 * W), -(2 * W + 1) / (2 * (W - 1)), 2,
            -(W + 1) / 2, -(U + 1) / 2, -(W - 2) / (W - 1), -(U - 2) / (U - 1),
            -1 / W, 1, -(U + 1) / 2,
        ),
        "denominator": 2 * U * W * (U - 1) * (W - 1),
    },
    "both_minus": {
        "keys": (
            ("1000", "0100"), ("0100", "0100"), ("0010", "0001"),
            ("0001", "0001"), ("0002", "0002"), ("0011", "0000"),
            ("0200", "0200"), ("0110", "0101"), ("0101", "0101"),
        ),
        "weights": (
            1, (3 * V - 1) / (4 * V), -1 / (2 * V), -1 / (2 * V), 1 / (4 * V),
            (5 * V + 1) / (4 * V * (V - 1)), sp.Rational(-3, 2),
            (V + 1) / (2 * V), (V + 1) / (2 * V),
        ),
        "denominator": 4 * V * (V - 1),
    },
    "minus_half": {
        "keys": (
            ("1000", "0100"), ("0100", "0100"), ("0010", "0001"),
            ("0002", "0002"), ("0001", "0001"), ("0012", "0012"),
            ("0010", "0010"), ("0011", "0000"), ("0200", "0200"),
            ("0110", "0101"), ("0101", "0101"), ("0100", "1101"),
            ("0000", "1001"),
        ),
        "weights": (
            1, (3 * V + 1) / (2 * V), 1 / V, (5 * V + 1) / (2 * V * (V - 1)),
            -(2 * V + 1) / (V * (V - 1)), sp.Rational(3, 4) / V,
            -sp.Rational(3, 4) / V, 1 / (2 * V), sp.Rational(-3, 2),
            -(V + 1) / V, -(V + 1) / V, -(V - 1) * (V + 1) / V**2,
            (V - 1) / V**2,
        ),
        "denominator": 4 * V**2 * (V - 1),
    },
}


def word(value): return tuple(map(int, value))
def p_index(which, root, colour): return (0 if which == 0 else 12) + 3 * root + colour
def w_index(left, right, lc, rc):
    if left > right: left, right, lc, rc = right, left, rc, lc
    return 24 + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices: return ((),)
    first, answer = vertices[0], []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest): answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = matchings(VERTICES)
assert len(MATCHINGS) == 945


def amplitudes(case):
    if case in ("u_minus", "both_minus", "minus_half"):
        first = (-1, sp.Rational(1, 2))
    else:
        first = (U, U / (U - 1))
    if case == "product":
        second = (-1 / U, 1 / (U + 1))
    else:
        second = (V, V / (V - 1))
    if case in ("w_minus", "both_minus"):
        third = (-1, sp.Rational(1, 2))
    elif case in ("w_half", "minus_half"):
        third = (sp.Rational(1, 2), -1)
    else:
        third = (W, W / (W - 1))
    return {
        (0, 0, 1): first[0], (1, 1, 0): first[1],
        (0, 1, 0): second[0], (1, 0, 1): second[1],
        (0, 2, 3): third[0], (1, 3, 2): third[1],
    }


def cross(root, port, root_word, port_word, case):
    colour = port_word[port]
    if root_word[root] != colour: return 0
    if root == port: return sp.Integer(1)
    return amplitudes(case).get((colour, root, port), sp.Integer(0))


def equation(port_word, root_word, case):
    x, y = (1, 1, 0), (1, -1, 0)
    row, constant = {}, 0
    for matching in MATCHINGS:
        variable, coefficient = None, sp.Integer(1)
        for raw_left, raw_right in matching:
            left, right = sorted((raw_left, raw_right)); edge_variable = None
            if left in ROOTS and right in ROOTS: edge_variable = w_index(left, right, root_word[left], root_word[right])
            elif left in ROOTS and right in (Q0, Q1): edge_variable = p_index(right - Q0, left, root_word[left])
            elif left in ROOTS and right in PORTS: coefficient *= cross(left, right - PORTS[0], root_word, port_word, case)
            elif left == Q0 and right == Q1: pass
            elif left in (Q0, Q1) and right in PORTS: coefficient *= (x if left == Q0 else y)[port_word[right - PORTS[0]]]
            elif left in PORTS and right in PORTS: coefficient = 0
            else: raise AssertionError((left, right))
            if coefficient == 0: break
            if edge_variable is not None:
                if variable is not None: coefficient = 0; break
                variable = edge_variable
        if coefficient == 0: continue
        if variable is None: constant += coefficient
        else: row[variable] = sp.expand(row.get(variable, 0) + coefficient)
    if len(set(port_word)) == 1 and root_word == port_word: row[78 + port_word[0]] = -1
    return row, sp.expand(-constant)


def main():
    for case, data in CASES.items():
        combined, rhs = {}, 0
        for (port_word, root_word), weight in zip(data["keys"], data["weights"], strict=True):
            row, value = equation(word(port_word), word(root_word), case); rhs += weight * value
            for index, coefficient in row.items(): combined[index] = sp.factor(combined.get(index, 0) + weight * coefficient)
        assert not {i: v for i, v in combined.items() if v != 0}, case
        assert sp.factor(rhs) == 1, case
        denominator = sp.factor(sp.lcm([sp.denom(sp.cancel(v)) for v in data["weights"]]))
        assert denominator == sp.factor(data["denominator"]), (case, denominator)
    print("PASS: 945-match expansion closes the full GLD54 reverse-disjoint exceptional union")


if __name__ == "__main__": main()
