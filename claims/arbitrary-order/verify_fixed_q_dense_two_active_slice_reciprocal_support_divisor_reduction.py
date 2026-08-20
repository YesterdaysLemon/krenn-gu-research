"""Primary exact replay for the GLD43 reciprocal-support divisor reduction."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, permutations

import sympy as sp


ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
PORTS = tuple(range(6, 10))
VERTICES = ROOTS + (Q0, Q1) + PORTS
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
AMPLITUDES = {
    (colour, i, j): sp.symbols(f"a{colour}{i}{j}")
    for colour in (0, 1)
    for i in ROOTS
    for j in ROOTS
    if i != j
}


def key(port_word, root_word):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


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


def cross(root, port, root_word, port_word):
    colour = port_word[port]
    if root_word[root] != colour:
        return 0
    if root == port:
        return sp.Integer(1)
    if colour in (0, 1):
        return AMPLITUDES[(colour, root, port)]
    return sp.Integer(0)


def equation(port_word, root_word):
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


def permute_word(word, permutation):
    answer = [None] * 4
    for old_index, new_index in enumerate(permutation):
        answer[new_index] = word[old_index]
    return tuple(answer)


def representatives():
    answer = {}
    for permutation in permutations(ROOTS):
        answer.setdefault((permutation[0], permutation[2]), permutation)
    assert set(answer) == {(i, j) for i in ROOTS for j in ROOTS if i != j}
    return answer


def cleaned(row):
    return {index: sp.factor(value) for index, value in row.items() if value != 0}


def main():
    base_keys = (
        key("1202", "0212"),
        key("2212", "2212"),
        key("0222", "0222"),
    )
    checked = set()
    for edge, permutation in representatives().items():
        x = AMPLITUDES[(0, *edge)]
        y = AMPLITUDES[(1, edge[1], edge[0])]
        row_keys = tuple(
            tuple(permute_word(word, permutation) for word in row_key)
            for row_key in base_keys
        )
        equations = tuple(equation(*row_key) for row_key in row_keys)
        rows = tuple(cleaned(row) for row, _ in equations)
        rhs = tuple(value for _, value in equations)
        combined = {
            index: sp.factor(
                rows[0].get(index, 0)
                - x * rows[1].get(index, 0)
                - y * rows[2].get(index, 0)
            )
            for index in set().union(*(set(row) for row in rows))
        }
        assert not {index: value for index, value in combined.items() if value != 0}
        detector = sp.factor(rhs[0] - x * rhs[1] - y * rhs[2])
        assert detector == -(x * y - x - y)
        checked.add(edge)
    assert len(checked) == 12
    print(
        "PASS: 945-match expansion gives all 12 GLD43 reciprocal-support "
        "divisors over the simultaneous 24-amplitude ring"
    )


if __name__ == "__main__":
    main()
