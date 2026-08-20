"""Primary exact replay for the GLD26 generic directed-spur exclusion."""

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
U, V, W = sp.symbols("u v w")
F = U * V - U - V - 1
H = U * V + V * W + W + 1
J = (
    U**2 * V**2
    - 2 * U**2 * V
    - 2 * U * V**2
    - U * V * W
    - 2 * U * V
    - U * W
    - 2 * U
    - V**2 * W
    - 3 * V * W
    - 2 * V
    - 2 * W
    - 3
)

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
    -U * V * W * (U * V - 1) * (U * V + 1) * H * J,
    -U * V * W * (U * V - 1) * (U * V + 1) * (U + V + 2) * H**2,
    U * V * W * (U * V - 1) * (U * V + 1) * H * J,
    U * V * W * (U * V - 1) * (U + V + 2) * H**3,
    -U * V * W * (U * V - 1) * (U * V + 1) ** 2 * J,
    -U * V * W * (U * V - 1) * (U * V + 1) * F * H**2,
    U * V * W * (U + 1) * (U * V - 1) * (U * V + 1) ** 2 * H**2,
    -U * W * (U + 1) * (U * V - 1) * (U * V + 1) ** 2 * H**2,
    U * V * W * (V + 1) * (U * V - 1) * (U * V + 1) ** 2 * H**2,
    -V * W * (V + 1) * (U * V - 1) * (U * V + 1) ** 2 * H**2,
    U * (U * V - 1) * (U * V + 1) ** 3 * F * H,
    -U * V * W * (U * V - 1) * (U * V + 1) ** 2 * H**2,
    U * V * W * (U * V + 1) ** 2 * (U * V - W - 1) * F * H,
    U * V * W * (U * V - 1) * (U * V + 1) * F * H**2,
    U * V * W * (U * V + 1) ** 2 * (U * V + V * W - 1) * F * H,
    U * V * W * (U * V - 1) * (U * V + 1) * F * H**2,
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
    if (root, port) == (0, 2):
        return W
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


def main():
    combined = {}
    combined_rhs = 0
    for key, multiplier in zip(KEYS, MULTIPLIERS, strict=True):
        row, rhs = equation(*key)
        for index, coefficient in row.items():
            combined[index] = sp.factor(
                combined.get(index, 0) + multiplier * coefficient
            )
        combined_rhs = sp.factor(combined_rhs + multiplier * rhs)
    combined = {index: value for index, value in combined.items() if value != 0}
    detector = U * V * W * (U * V - 1) * (U * V + 1) ** 2 * F * H**2
    assert not combined
    assert sp.expand(combined_rhs - detector) == 0
    print(
        "PASS: direct 945-match expansion gives the exact GLD26 "
        "three-parameter generic directed-spur detector"
    )


if __name__ == "__main__":
    main()
