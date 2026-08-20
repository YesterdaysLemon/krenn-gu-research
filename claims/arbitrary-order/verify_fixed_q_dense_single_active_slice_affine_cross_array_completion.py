"""Primary exact replay for the GLD41 single-active-slice affine completion."""

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
AMPLITUDES = {(i, j): sp.symbols(f"a{i}{j}") for i in ROOTS for j in ROOTS if i != j}


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
    if colour != 0:
        return sp.Integer(root == port)
    if root == port:
        return sp.Integer(1)
    return AMPLITUDES[(root, port)]


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
        edge = (permutation[0], permutation[2])
        answer.setdefault(edge, permutation)
    assert set(answer) == set(AMPLITUDES)
    return answer


def cleaned(row):
    return {index: sp.factor(value) for index, value in row.items() if value != 0}


def main():
    base_first = key("1202", "0212")
    base_second = key("2212", "2212")
    checked = set()
    for edge, permutation in representatives().items():
        amplitude = AMPLITUDES[edge]
        first_key = tuple(permute_word(word, permutation) for word in base_first)
        second_key = tuple(permute_word(word, permutation) for word in base_second)
        first_row, first_rhs = equation(*first_key)
        second_row, second_rhs = equation(*second_key)
        first_row, second_row = cleaned(first_row), cleaned(second_row)
        assert len(second_row) == 2
        assert set(second_row.values()) == {-1, 1}
        assert first_row == {index: amplitude * value for index, value in second_row.items()}
        assert first_rhs == 0
        assert second_rhs == -1
        combined = {
            index: sp.factor(first_row.get(index, 0) - amplitude * second_row.get(index, 0))
            for index in range(81)
        }
        assert not {index: value for index, value in combined.items() if value != 0}
        assert sp.factor(first_rhs - amplitude * second_rhs - amplitude) == 0
        checked.add(edge)
    assert checked == set(AMPLITUDES)
    print(
        "PASS: 945-match expansion gives 12 exact entry detectors for the "
        "full GLD41 single-active-slice affine cross array"
    )


if __name__ == "__main__":
    main()
