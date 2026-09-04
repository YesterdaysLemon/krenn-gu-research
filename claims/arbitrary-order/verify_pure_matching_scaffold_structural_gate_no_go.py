"""Primary finite scaffold replay; stdlib rational arithmetic only.

Scope: finite jet, hollow-row surjectivity and mixed-word controls.
This does not computationally certify the generic-geometry arguments.
"""

from fractions import Fraction as Q
from itertools import combinations
import json


def det(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    out = Q(1)
    for col in range(len(a)):
        pivot = next((r for r in range(col, len(a)) if a[r][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            out = -out
        p = a[col][col]
        out *= p
        for r in range(col + 1, len(a)):
            factor = a[r][col] / p
            for j in range(col, len(a)):
                a[r][j] -= factor * a[col][j]
    return out


# Polynomials as exponent-tuples -> exact rational coefficients.
zero_exp = (0,) * 10


def coordinate(root, coordinate):
    exp = list(zero_exp)
    if coordinate:
        exp[2 * root + coordinate - 1] = 1
    return tuple(exp)


blocks = {}
rows = []
for i in range(5):
    for step in [1, 2]:
        j = (i + step) % 5
        directed = (
            {(1, 2): Q(1), (0, 2): Q(-1)}
            if step == 1
            else {(2, 1): Q(1), (0, 1): Q(-1)}
        )
        e = tuple(sorted((i, j)))
        assert e not in blocks
        physical = directed if i < j else {(b, a): v for (a, b), v in directed.items()}
        assert all(a != b for a, b in physical)
        blocks[e] = physical
        poly = {}
        for (a, b), coefficient in physical.items():
            exponents = tuple(
                x + y for x, y in zip(coordinate(e[0], a), coordinate(e[1], b))
            )
            poly[exponents] = poly.get(exponents, Q(0)) + coefficient
        assert sum(poly.values()) == 0
        derivative = [
            sum(coefficient * exp[k] for exp, coefficient in poly.items())
            for k in range(10)
        ]
        expected = [Q(0)] * 10
        expected[2 * i + step - 1] = Q(1)
        assert derivative == expected
        rows.append(derivative)
assert len(blocks) == 10
assert det(rows) == 1

# A hollow matrix has six independent coefficient variables. Directly form
# the contraction map and select three columns giving a nonzero minor.
offdiag = [(a, b) for a in range(3) for b in range(3) if a != b]
selected = [offdiag.index(e) for e in [(1, 0), (0, 1), (0, 2)]]
minor_values = []
for x in [(Q(1), Q(1), Q(1)), (Q(2), Q(3), Q(5))]:
    contraction = [
        [x[a] if b == output else Q(0) for a, b in offdiag] for output in range(3)
    ]
    minor = [[row[column] for column in selected] for row in contraction]
    value = det(minor)
    assert value == x[1] * x[0] ** 2 and value != 0
    minor_values.append(str(value))

# Two exact disjoint K4 scaffolds, with no inter-block filling. Enumerate
# every perfect matching on eight labelled vertices rather than invoking
# any factorization formula.
support = {}
coloured_matchings = [[(0, 1), (2, 3)], [(0, 2), (1, 3)], [(0, 3), (1, 2)]]
for offset in [0, 4]:
    for colour, matching in enumerate(coloured_matchings):
        for a, b in matching:
            support[(a + offset, b + offset)] = colour


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for b in vertices[1:]:
        for remainder in matchings(tuple(v for v in vertices[1:] if v != b)):
            yield ((a, b),) + remainder


all_matchings = list(matchings(tuple(range(8))))
assert len(all_matchings) == 105


def amplitude(word):
    contributing = []
    for matching in all_matchings:
        coefficient = Q(1)
        for a, b in matching:
            if support.get((a, b)) != word[a] or word[a] != word[b]:
                coefficient = Q(0)
                break
        if coefficient:
            contributing.append(matching)
    return Q(len(contributing)), contributing


mixed = (0, 0, 0, 0, 1, 1, 1, 1)
value, contributing = amplitude(mixed)
assert value == 1 and contributing == [((0, 1), (2, 3), (4, 6), (5, 7))]
pure = [str(amplitude((c,) * 8)[0]) for c in range(3)]
assert pure == ["1", "1", "1"]
print(
    json.dumps(
        {
            "scope": "finite exact controls only; not genericity certification or a GHZ witness",
            "arithmetic": "stdlib Fraction",
            "root_count": 5,
            "hollow_blocks": 10,
            "all_root_forms_at_ones": "0",
            "root_Jacobian": "10-by-10 identity in source-step row order",
            "root_Jacobian_determinant": str(det(rows)),
            "hollow_contraction_pivot_columns": [[1, 0], [0, 1], [0, 2]],
            "hollow_contraction_minor_formula": "x[1]*x[0]^2",
            "hollow_contraction_exact_minor_values": minor_values,
            "eight_vertex_matchings_enumerated": len(all_matchings),
            "pure_amplitudes": pure,
            "mixed_word": mixed,
            "mixed_amplitude": str(value),
            "unique_contributing_matching": contributing[0],
            "all_checks": "PASS",
        },
        indent=2,
    )
)
