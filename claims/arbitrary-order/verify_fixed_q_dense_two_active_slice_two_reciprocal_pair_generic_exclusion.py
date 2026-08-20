"""Primary 945-match replay for the five GLD44 two-pair orbit certificates."""

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

ORBIT_DATA = {
    "reverse": {
        "edge": (2, 0),
        "keys": (
            ("1000", "0010"), ("0002", "0002"), ("0010", "0010"),
            ("0010", "1000"), ("0020", "0020"), ("0011", "0011"),
            ("0001", "0001"), ("0000", "0011"), ("0011", "1001"),
            ("0000", "1001"), ("0011", "0000"), ("0200", "0200"),
            ("0110", "0000"), ("0110", "0110"), ("0100", "0100"),
            ("0000", "0110"), ("0101", "0000"),
        ),
        "weights": (
            -1 / U,
            -1 / (U * W + 1),
            2,
            (W - 1) / W**2,
            -(U - 2) / (U - 1),
            -(U * W + 1) / (2 * U * W),
            (3 * U * W + 1) / (2 * U * W * (U * W + 1)),
            -(U * W + 1) / (2 * U * W * (U + 1)),
            -(W - 1) / W**2,
            -(W - 1) / (W * (W + 1)),
            (U - 1) / (2 * U * W),
            -1 / (U * W + 1),
            (U + 1) / (2 * U * W),
            -(U * W - 1) / (2 * U * W),
            (U * W - 1) / (2 * U * W * (U * W + 1)),
            -(U * W - 1) / (2 * U * W * (U + 1)),
            1 / (U * W + 1),
        ),
        "denominator": 2 * U * W**2 * (U - 1) * (U + 1) * (W + 1) * (U * W + 1),
    },
    "same_tail": {
        "edge": (0, 1),
        "keys": (
            ("1010", "0000"), ("1000", "0100"), ("0100", "0100"),
            ("0011", "0011"), ("0010", "0010"), ("0001", "0001"),
            ("0011", "0000"), ("0000", "0011"), ("0200", "0200"),
            ("0020", "0020"), ("0002", "0002"), ("0110", "0000"),
            ("0101", "0000"), ("1001", "0000"),
        ),
        "weights": (
            1 / (U + 1),
            -1 / W,
            1,
            -(U + 2) / (U + 1),
            (U + 2) / (U + 1),
            (U + 2) / (U + 1),
            -U - 1,
            -(U + 2) / (U + 1) ** 2,
            -(W - 2) / (W - 1),
            -1 / (U + 1),
            -1,
            1,
            1,
            1,
        ),
        "denominator": W * (U + 1) ** 2 * (W - 1),
    },
    "same_head": {
        "edge": (1, 2),
        "keys": (
            ("1001", "0000"), ("1000", "0010"), ("0100", "0010"),
            ("0010", "0010"), ("0020", "0020"), ("0002", "0002"),
            ("0110", "0110"), ("0000", "0110"), ("0120", "0120"),
            ("0101", "0000"), ("0011", "0000"), ("0011", "0011"),
            ("0001", "0001"), ("0000", "0011"),
        ),
        "weights": (
            1,
            -(U - 1) / (U * (U - W - 1)),
            (U - 1) * (W - 1) / (U * W * (U - W - 1)),
            (2 * U**2 * W - 2 * U * W**2 - U + 2 * W**2 - 3 * W + 1)
            / (U * W * (U - W - 1)),
            -(U**2 * W - U * W**2 + U * W - U + 2 * W**2 - 4 * W + 1)
            / (U * W * (U - W - 1)),
            -1,
            -(W - 1) * (U + W - 1) / (U * W * (U - W - 1)),
            -(W - 1) * (U + W - 1) / (U * W * (U + 1) * (U - W - 1)),
            (2 * W - 1) * (U + W - 1) / (U * W * (U - W - 1)),
            1,
            -U - W,
            -1,
            1,
            -1 / (U + W + 1),
        ),
        "denominator": U * W * (U + 1) * (U - W - 1) * (U + W + 1),
    },
    "chain": {
        "edge": (2, 1),
        "keys": (
            ("1001", "0000"), ("1000", "0010"), ("0010", "0010"),
            ("0020", "0020"), ("0011", "0011"), ("0000", "0011"),
            ("0001", "0001"), ("0100", "0100"), ("0011", "0000"),
            ("0002", "0002"), ("0110", "0110"), ("0110", "0000"),
            ("0000", "0110"), ("0200", "0200"), ("0011", "0101"),
            ("0010", "0100"), ("0000", "0101"),
        ),
        "weights": (
            1,
            -1 / U,
            (3 * U * W - 3 * U - 4 * W) / (2 * U * (W - 1)),
            -(U**2 * W - U**2 - 3 * U * W + U + W + 1)
            / (U * (U - 1) * (W - 1)),
            -(U * W + 2) / (2 * U * W),
            -(U * W + 2) / (2 * U * W * (U + 1)),
            (U * W + 1) / (U * W),
            -(W + 1) / (U * W),
            -(2 * U**2 * W + U + 2) / (2 * U * W),
            -1,
            (W + 1) / (U * W),
            (U + 1) / (U * W),
            (W + 1) / (U * W * (U + 1)),
            1 / U,
            -(W - 1) / (2 * W**2),
            (W - 1) / (2 * W**2),
            -(W - 1) / (2 * W * (U * W + W + 1)),
        ),
        "denominator": 2 * U * W**2 * (U - 1) * (U + 1) * (W - 1) * (U * W + W + 1),
    },
    "disjoint": {
        "edge": (1, 3),
        "keys": (
            ("1100", "0000"), ("1000", "0010"), ("0100", "0001"),
            ("0002", "0002"), ("0010", "0010"), ("0020", "0020"),
            ("0001", "0001"), ("0110", "0000"), ("0011", "0000"),
            ("0011", "0011"), ("0000", "0011"), ("1001", "0000"),
        ),
        "weights": (
            1,
            -1 / U,
            -1 / W,
            -(W - 2) / (W - 1),
            2,
            -(U - 2) / (U - 1),
            2,
            1,
            -U * W - U - W,
            -1,
            -1 / ((U + 1) * (W + 1)),
            1,
        ),
        "denominator": U * W * (U - 1) * (U + 1) * (W - 1) * (W + 1),
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


def cross(root, port, root_word, port_word, second_edge):
    colour = port_word[port]
    if root_word[root] != colour:
        return 0
    if root == port:
        return sp.Integer(1)
    pairs = ((0, 2), second_edge)
    values = (U, W)
    reciprocal = (U / (U - 1), W / (W - 1))
    if colour == 0:
        for edge, value in zip(pairs, values, strict=True):
            if (root, port) == edge:
                return value
    if colour == 1:
        for edge, value in zip(pairs, reciprocal, strict=True):
            if (port, root) == edge:
                return value
    return sp.Integer(0)


def equation(port_word, root_word, second_edge):
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
                coefficient *= cross(
                    left, right - PORTS[0], root_word, port_word, second_edge
                )
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


def denominator_lcm(weights):
    return sp.factor(sp.lcm([sp.denom(sp.cancel(value)) for value in weights]))


def main():
    for name, data in ORBIT_DATA.items():
        combined, rhs = {}, 0
        for (port_word, root_word), weight in zip(
            data["keys"], data["weights"], strict=True
        ):
            row, value = equation(word(port_word), word(root_word), data["edge"])
            rhs += weight * value
            for index, coefficient in row.items():
                combined[index] = sp.factor(
                    combined.get(index, 0) + weight * coefficient
                )
        assert not {index: value for index, value in combined.items() if value != 0}, name
        assert sp.factor(rhs) == 1, name
        assert denominator_lcm(data["weights"]) == sp.factor(data["denominator"]), name
    print(
        "PASS: 945-match expansion verifies the five GLD44 generic "
        "two-reciprocal-pair orbit certificates"
    )


if __name__ == "__main__":
    main()
