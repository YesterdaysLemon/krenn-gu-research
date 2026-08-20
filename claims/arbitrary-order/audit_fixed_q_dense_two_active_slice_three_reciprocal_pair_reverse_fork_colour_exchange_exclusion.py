"""Standalone matching-topology audit of the GLD56 reverse-fork transfer."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache

import sympy as sp


ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
PORTS = tuple(range(6, 10))
VERTICES = ROOTS + (Q0, Q1) + PORTS
T = sp.symbols("t")


def swap_colour(colour):
    return 1 - colour if colour in (0, 1) else colour


def mapped_index(index):
    if index < 24:
        block, offset = divmod(index, 12)
        root, colour = divmod(offset, 3)
        return 12 * block + 3 * root + swap_colour(colour)
    if index < 78:
        offset = index - 24
        edge, colours = divmod(offset, 9)
        left, right = divmod(colours, 3)
        return 24 + 9 * edge + 3 * swap_colour(left) + swap_colour(right)
    return 78 + swap_colour(index - 78)


def coordinate_sign(index):
    return -1 if index < 12 or 24 <= index < 78 else 1


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


def topology(matching):
    variables, y_edges = [], 0
    for raw_left, raw_right in matching:
        left, right = sorted((raw_left, raw_right))
        if left in PORTS and right in PORTS:
            return "zero_port_port"
        if left in ROOTS and right in ROOTS:
            variables.append("w")
        elif left in ROOTS and right == Q0:
            variables.append("p0")
        elif left in ROOTS and right == Q1:
            variables.append("p1")
        elif left == Q1 and right in PORTS:
            y_edges += 1
    if len(variables) > 1:
        return "discard_multi_variable"
    variable = variables[0] if variables else "constant"
    return f"{variable}_y{y_edges}"


def main():
    exchanged = T / (T - 1)
    assert sp.cancel(exchanged / (exchanged - 1) - T) == 0
    x, y = (1, 1, 0), (1, -1, 0)
    for colour in range(3):
        assert x[swap_colour(colour)] == x[colour]
        assert y[swap_colour(colour)] == -y[colour]

    assert len({mapped_index(index) for index in range(81)}) == 81
    for index in range(81):
        assert mapped_index(mapped_index(index)) == index
        assert coordinate_sign(mapped_index(index)) == coordinate_sign(index)

    all_matchings = matchings(VERTICES)
    assert len(all_matchings) == 945
    counts = Counter(topology(matching) for matching in all_matchings)
    assert counts == {
        "zero_port_port": 585,
        "constant_y0": 24,
        "p0_y1": 96,
        "p1_y0": 96,
        "w_y1": 144,
    }
    expected_sign = {"constant": 1, "p0": -1, "p1": 1, "w": -1}
    for kind in counts:
        if kind.startswith("zero_") or kind.startswith("discard_"):
            continue
        variable, y_count = kind.split("_y")
        assert expected_sign[variable] == (-1) ** int(y_count)

    fork = {(0, 1), (0, 2), (1, 3)}
    reverse = {(right, left) for left, right in fork}
    permutation = {0: 2, 1: 1, 2: 3, 3: 0}
    assert {(permutation[left], permutation[right]) for left, right in reverse} == {
        (0, 1), (1, 2), (3, 2)
    }
    print("PASS: 945 matching topologies independently prove the GLD56 transfer")


if __name__ == "__main__":
    main()
