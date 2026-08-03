"""Primary symbolic verifier for the hafnian-to-spinor route exclusion."""

from __future__ import annotations

import sympy as sp


def hafnian(matrix, vertices=None):
    if vertices is None:
        vertices = tuple(range(matrix.rows))
    vertices = tuple(vertices)
    if not vertices:
        return sp.Integer(1)
    if len(vertices) % 2:
        return sp.Integer(0)
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        total += matrix[first, second] * hafnian(matrix, rest)
    return sp.expand(total)


def check_four_point_defect():
    h12, h13, h14, h23, h24, h34 = sp.symbols("h12 h13 h14 h23 h24 h34")
    h1234 = h12 * h34 + h13 * h24 + h14 * h23
    defect = h1234 - h12 * h34 + h13 * h24 - h14 * h23
    assert sp.expand(defect - 2 * h13 * h24) == 0


def check_six_point_sign_contradiction():
    t11, t12, t13, t21, t22, t23 = sp.symbols("t11 t12 t13 t21 t22 t23")
    # If the first two sign equations hold, the left side below vanishes.
    first_two_elimination = (t11 * t22) * (t12 * t23) - (-t12 * t21) * (-t13 * t22)
    assert sp.factor(first_two_elimination) == t12 * t22 * (t11 * t23 - t13 * t21)
    # The third sign equation makes the same difference twice a nonzero product.
    implied_plus = t11 * t23 - t13 * t21
    required_minus = t11 * t23 + t13 * t21
    assert sp.expand(required_minus - implied_plus - 2 * t13 * t21) == 0


def check_delta_matroid_counterexample():
    matrix = sp.zeros(6)
    weights = {
        (0, 1): 1,
        (0, 2): 1,
        (0, 3): 1,
        (0, 5): 1,
        (1, 4): 1,
        (2, 4): 1,
        (3, 4): -1,
        (4, 5): 2,
    }
    for (i, j), value in weights.items():
        matrix[i, j] = matrix[j, i] = value

    x = frozenset((0, 3, 4, 5))
    y = frozenset((0, 1, 2, 4))
    assert hafnian(matrix, tuple(sorted(x))) == 1
    assert hafnian(matrix, tuple(sorted(y))) == 2
    symmetric_difference = x ^ y
    assert symmetric_difference == frozenset((1, 2, 3, 5))
    for other in symmetric_difference:
        exchanged = x ^ frozenset((5, other))
        assert hafnian(matrix, tuple(sorted(exchanged))) == 0


if __name__ == "__main__":
    check_four_point_defect()
    check_six_point_sign_contradiction()
    check_delta_matroid_counterexample()
    print("bosonic hafnian spinor no-transfer primary verifier: PASS")
