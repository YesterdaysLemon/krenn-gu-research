"""Primary exact replay for the GLD31 generic bidirected-spur exclusion."""

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
U, V, W, Z = sp.symbols("u v w z")
S_MINUS = U * V + W * Z - 1
S_PLUS = U * V + W * Z + 1
H = U * V + V * W + W + 1
P = (
    -U**2 * V**2 * Z - U**2 * V**2 + U**2 * V * Z**2
    + 2 * U**2 * V * Z + U**2 * V - U * V**2 * W + U * V**2
    + 4 * U * V * W * Z - U * W * Z**2 + U * W + U * Z**2
    + 2 * U * Z + U + V**2 * W**2 * Z + V**2 * W
    - V * W**2 * Z**2 + 2 * V * W**2 * Z + 2 * V * W + V
    - W**2 * Z**2 + W**2 * Z + W * Z**2 + W + Z + 1
)


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


KEYS = tuple(
    key(*words)
    for words in (
        ("0011", "0011"), ("0010", "0010"), ("0001", "0001"),
        ("0011", "0000"), ("0000", "0011"), ("0002", "0002"),
        ("1000", "1000"), ("0100", "1000"), ("0100", "0100"),
        ("1000", "0100"), ("0100", "0010"), ("1100", "0000"),
        ("0110", "0000"), ("0101", "0000"), ("1010", "0000"),
        ("0111", "0010"),
    )
)

R0 = (
    -U**2 * V**2 * Z - U**2 * V**2 + U**2 * V * Z**2
    + 3 * U**2 * V * Z + 2 * U**2 * V + 2 * U * V**2
    + 4 * U * V * W * Z + U * V * W + U * V * Z + 2 * U * V
    + U * W * Z + U * W + U * Z**2 + 3 * U * Z + 2 * U
    + V**2 * W**2 * Z + V**2 * W - V * W**2 * Z**2
    + 3 * V * W**2 * Z + V * W * Z + 3 * V * W + 2 * V
    - W**2 * Z**2 + 2 * W**2 * Z + 2 * W * Z**2 + 2 * W * Z
    + 2 * W + 2 * Z + 3
)
R1 = (
    -U**2 * V * Z - U**2 * V - U * V**2 * W * Z - U * V**2
    + U * V * W * Z**2 - 3 * U * V * W * Z - U * V * W
    - U * V * Z - 2 * U * V - U * W * Z - U * W - U * Z - U
    - V**2 * W**2 * Z - V**2 * W + V * W**2 * Z**2
    - 3 * V * W**2 * Z - 2 * V * W * Z - 3 * V * W - V
    + W**2 * Z**2 - 2 * W**2 * Z - W * Z**2 - W * Z - 2 * W - Z - 2
)
R3 = (
    -U**3 * V**3 * Z - U**3 * V**3 + U**3 * V**2 * Z**2
    + 2 * U**3 * V**2 * Z + U**3 * V**2 - U**2 * V**3 * W
    + U**2 * V**3 + 4 * U**2 * V**2 * W * Z + U**2 * V**2 * Z
    + U**2 * V**2 + U**2 * V * W * Z**2 + 2 * U**2 * V * W * Z
    + U**2 * V * W + 2 * U**2 * V * Z**2 + 2 * U**2 * V * Z
    + U * V**3 * W**2 * Z + U * V**3 * W - U * V**2 * W**2 * Z**2
    + 4 * U * V**2 * W**2 * Z + 4 * U * V**2 * W * Z
    + 3 * U * V**2 * W + 2 * U * V**2 * Z - U * V * W**2 * Z**2
    + 3 * U * V * W**2 * Z + 3 * U * V * W * Z**2
    + 2 * U * V * W * Z + U * V * W + 2 * U * V * Z**2
    + 5 * U * V * Z + U * V + U * W * Z**2 - U * W + U * Z**2 - U
    - V**2 * W**2 * Z - V**2 * W + V * W**2 * Z**2
    - 2 * V * W**2 * Z + 2 * V * W * Z - 2 * V * W + 2 * V * Z - V
    + W**2 * Z**2 - W**2 * Z - W * Z**2 + 2 * W * Z - W
    + 2 * Z**2 + 3 * Z - 1
)
R6 = (
    U**2 * V * Z + U**2 * V + 2 * U * V * W * Z + U * V * W
    + 2 * U * V * Z + U * V + U * W * Z + U * W + U * Z + U
    + V * W**2 * Z + 2 * V * W * Z + V * W + W**2 * Z + W * Z + W + 1
)
R8 = (
    -U * V**2 + U * V * Z - U * V - V**2 * W + V * W * Z
    - 2 * V * W - V + W * Z - W - Z - 1
)
R10 = (
    -U * V * Z - U * V + U * Z**2 + 2 * U * Z + U
    - V * W * Z + V + W * Z**2 + W * Z + Z + 1
)
R11 = (
    -2 * U**2 * V**2 * Z - U**2 * V**2 + 3 * U**2 * V * Z**2
    + U**2 * V * Z - 2 * U * V**2 * W * Z - U * V**2 * W
    + 4 * U * V * W * Z**2 - U * V * W + 2 * U * V * Z**2
    + U * V * Z + U * W * Z**2 - U * W * Z - U * Z**2 - U * Z
    + V * W**2 * Z**2 - V * W**2 * Z + 2 * V * W * Z**2
    + V * W * Z + V * W + W**2 * Z**2 - W**2 * Z - W * Z**2
    - 2 * W * Z + W + Z + 1
)
R12 = (
    U**2 * V**2 - 3 * U**2 * V * Z - U**2 * V - U * V**2
    - 4 * U * V * W * Z - U * V * W - 3 * U * V * Z - 2 * U * V
    - U * W * Z + U * W + U * Z + U - 3 * V * W**2 * Z
    - 3 * V * W * Z + V * W + V + W**2 * Z**2 - W**2 * Z
    - W * Z**2 - 2 * W * Z + W + Z + 1
)
R13 = (
    -U**3 * V**3 * Z - U**3 * V**3 + U**3 * V**2 * Z**2
    + 2 * U**3 * V**2 * Z + U**3 * V**2 - U**2 * V**3 * W
    + U**2 * V**3 + 4 * U**2 * V**2 * W * Z + U**2 * V**2 * Z
    + U**2 * V**2 + U**2 * V * W * Z**2 + 2 * U**2 * V * W * Z
    + U**2 * V * W + U * V**3 * W**2 * Z + U * V**3 * W
    - U * V**2 * W**2 * Z**2 + 4 * U * V**2 * W**2 * Z
    + 2 * U * V**2 * W * Z + 3 * U * V**2 * W
    - U * V * W**2 * Z**2 + 3 * U * V * W**2 * Z
    + U * V * W * Z**2 - 2 * U * V * W * Z + U * V * W
    + U * V * Z + U * V - U * W * Z**2 - 2 * U * W * Z - U * W
    - U * Z**2 - 2 * U * Z - U - 3 * V**2 * W**2 * Z
    - 2 * V**2 * W * Z - V**2 * W + V * W**2 * Z**2
    - 6 * V * W**2 * Z - 2 * V * W * Z**2 - 6 * V * W * Z
    - 2 * V * W - V + W**2 * Z**2 - 3 * W**2 * Z - 3 * W * Z**2
    - 4 * W * Z - W - Z - 1
)
R14 = (
    -U**2 * V**2 * Z - U**2 * V**2 + U**2 * V * Z + U**2 * V
    - 4 * U * V**2 * W * Z - U * V**2 * W - 2 * U * V**2 * Z
    + U * V**2 + 2 * U * V * W * Z**2 + U * V * W - U * V * Z
    + 2 * U * V + U * W * Z**2 + U * W * Z - U * Z - U
    - 3 * V**2 * W**2 * Z - 2 * V**2 * W * Z + V**2 * W
    + 2 * V * W**2 * Z**2 - V * W**2 * Z - V * W * Z
    + V * W - V + W**2 * Z**2 - 1
)
R15 = (
    U**4 * V**4 * Z + U**4 * V**4 - U**4 * V**3 * Z**2
    - 2 * U**4 * V**3 * Z - U**4 * V**3 + U**3 * V**4 * W
    - U**3 * V**4 - U**3 * V**3 * W * Z**2 - 5 * U**3 * V**3 * W * Z
    + U**3 * V**2 * W * Z**3 + U**3 * V**2 * W * Z**2
    - U**3 * V**2 * W * Z - U**3 * V**2 * W - U**3 * V**2 * Z**2
    - 2 * U**3 * V**2 * Z - U**3 * V**2 - U**2 * V**4 * W**2 * Z
    - U**2 * V**4 * W + U**2 * V**3 * W**2 * Z**2
    - 5 * U**2 * V**3 * W**2 * Z - 2 * U**2 * V**3 * W * Z**2
    - 3 * U**2 * V**3 * W * Z - 2 * U**2 * V**3 * W - U**2 * V**3
    + 5 * U**2 * V**2 * W**2 * Z**2 - 3 * U**2 * V**2 * W**2 * Z
    + 2 * U**2 * V**2 * W * Z**3 + 2 * U**2 * V**2 * W * Z**2
    - U**2 * V**2 * W * Z - U**2 * V**2 * W - 2 * U**2 * V**2 * Z
    - 2 * U**2 * V**2 + U**2 * V * W**2 * Z**3
    + 2 * U**2 * V * W**2 * Z**2 + U**2 * V * W**2 * Z
    + 2 * U**2 * V * W * Z**3 + 4 * U**2 * V * W * Z**2
    + 2 * U**2 * V * W * Z + U**2 * V * Z**2 + 2 * U**2 * V * Z
    + U**2 * V + U * V**3 * W**3 * Z**2 + U * V**3 * W**2 * Z
    + 4 * U * V**3 * W * Z - U * V**2 * W**3 * Z**3
    + 4 * U * V**2 * W**3 * Z**2 + 10 * U * V**2 * W**2 * Z**2
    + 3 * U * V**2 * W**2 * Z + 2 * U * V**2 * W * Z**2
    + 6 * U * V**2 * W * Z - U * V**2 * W + U * V**2
    - U * V * W**3 * Z**3 + 3 * U * V * W**3 * Z**2
    + 3 * U * V * W**2 * Z**3 + 10 * U * V * W**2 * Z**2
    + 3 * U * V * W**2 * Z + 2 * U * V * W * Z**3
    + 7 * U * V * W * Z**2 + 9 * U * V * W * Z
    + U * W**2 * Z**3 + 2 * U * W**2 * Z**2 + U * W**2 * Z
    + U * W * Z**3 + 3 * U * W * Z**2 + 3 * U * W * Z + U * W
    + U * Z**2 + 2 * U * Z + U + 2 * V**3 * W**3 * Z**2
    + 2 * V**3 * W**2 * Z - 2 * V**2 * W**3 * Z**3
    + 7 * V**2 * W**3 * Z**2 + 2 * V**2 * W**2 * Z**2
    + 8 * V**2 * W**2 * Z + 4 * V**2 * W * Z + V**2 * W
    - 3 * V * W**3 * Z**3 + 8 * V * W**3 * Z**2
    + 4 * V * W**2 * Z**3 + 5 * V * W**2 * Z**2
    + 10 * V * W**2 * Z + 4 * V * W * Z**2 + 9 * V * W * Z
    + 2 * V * W + V - W**3 * Z**3 + 3 * W**3 * Z**2
    + 3 * W**2 * Z**3 + 3 * W**2 * Z**2 + 4 * W**2 * Z
    + 4 * W * Z**2 + 5 * W * Z + W + Z + 1
)

MULTIPLIERS = (
    -2 * U * V * W * Z * S_MINUS * S_PLUS * H * R0,
    -2 * U * V * W * Z * S_MINUS * S_PLUS * H * R1,
    2 * U * V * W * Z * (U * V + 1) * S_MINUS * H * R0,
    -U * V * W * S_MINUS * S_PLUS * H * R3,
    -2 * U * V * W * Z * (U * V + 1) * S_MINUS * S_PLUS * R0,
    -2 * U * V * W * Z * (U * V + 1) * S_MINUS * H * P,
    -2 * U * V * W * Z * (U * V + 1) * S_MINUS * S_PLUS * H * R6,
    2 * U * W * Z * (U * V + 1) * S_MINUS * S_PLUS * H * R6,
    2 * U * V * W * Z * (U * V + 1) * S_MINUS * S_PLUS * H * R8,
    -2 * V * W * Z * (U * V + 1) * (W * Z + 1) * S_MINUS * S_PLUS * H * R8,
    2 * U * Z * (U * V + 1) ** 2 * S_MINUS * S_PLUS * H * R10,
    -2 * U * V * W * Z * (U * V + 1) * S_PLUS * H * R11,
    -2 * U * V * W * Z * (U * V + 1) * S_PLUS * H * R12,
    U * (U * V + 1) * S_MINUS * S_PLUS * H * R13,
    2 * U * V * W * Z * (U * V + 1) * S_PLUS * H * R14,
    U * S_MINUS * S_PLUS * H * R15,
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
    return {
        (0, 1): U,
        (1, 0): V,
        (0, 2): W,
        (2, 0): Z,
    }.get((root, port), sp.Integer(0))


def equation(port_word, root_word):
    x, y = (1, 1, 0), (1, -1, 0)
    row, constant = {}, 0
    for matching in MATCHINGS:
        variable, coefficient = None, sp.Integer(1)
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
    combined, rhs = {}, 0
    for row_key, multiplier in zip(KEYS, MULTIPLIERS, strict=True):
        row, value = equation(*row_key)
        for index, coefficient in row.items():
            combined[index] = sp.factor(combined.get(index, 0) + multiplier * coefficient)
        rhs = sp.factor(rhs + multiplier * value)
    combined = {index: value for index, value in combined.items() if value != 0}
    detector = 2 * U * V * W * Z * (U * V + 1) * S_MINUS * S_PLUS * H * P
    assert not combined
    assert sp.factor(rhs - detector) == 0
    print(
        "PASS: direct 945-match expansion gives the exact GLD31 "
        "four-parameter generic bidirected-spur detector"
    )


if __name__ == "__main__":
    main()
