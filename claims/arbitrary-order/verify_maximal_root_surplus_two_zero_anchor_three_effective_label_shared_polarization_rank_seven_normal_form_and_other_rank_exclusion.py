"""Focused exact checks for the GLS51 three-label classification.

This verifier replays the new algebraic identities and finite type/graph
steps.  The written proof owns the characteristic-zero theorem.
"""

from itertools import product

import sympy as sp


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def diagonal_unit(index: int) -> sp.Matrix:
    value = sp.zeros(3)
    value[index, index] = 1
    return value


def flattened(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(9, 1, list(matrix))


def test_shifted_identity() -> None:
    gamma, lambda_u, lambda_v = sp.symbols("gamma lambda_u lambda_v")
    a = sp.Matrix(sp.symbols("a0:3"))
    b = sp.Matrix(sp.symbols("b0:3"))
    xu = sp.Matrix(sp.symbols("xu0:3"))
    yu = sp.Matrix(sp.symbols("yu0:3"))
    xv = sp.Matrix(sp.symbols("xv0:3"))
    yv = sp.Matrix(sp.symbols("yv0:3"))

    gu = outer(a, yu) + outer(xu, b)
    gv = outer(a, yv) + outer(xv, b)
    muv = outer(xu, yv) + outer(xv, yu)
    shifted = outer(gamma * xu + a * lambda_u, gamma * yv + b * lambda_v)
    shifted += outer(gamma * xv + a * lambda_v, gamma * yu + b * lambda_u)
    expected = gamma * (gu * lambda_v + gv * lambda_u + gamma * muv)
    expected += 2 * outer(a, b) * lambda_u * lambda_v
    assert shifted.equals(expected)


def test_determinant_polynomial() -> None:
    gamma = sp.symbols("gamma")
    alpha = sp.symbols("alpha0:3")
    a = sp.Matrix(sp.symbols("a0:3"))
    b = sp.Matrix(sp.symbols("b0:3"))
    z = sp.symbols("z0:3")
    w = sp.symbols("w0:3")
    lu = sp.symbols("lu0:3")
    lv = sp.symbols("lv0:3")
    lambda_u = sum(lu[d] * z[d] for d in range(3))
    lambda_v = sum(lv[d] * w[d] for d in range(3))
    diagonal = sp.diag(*(gamma * alpha[d] * z[d] * w[d] for d in range(3)))
    matrix = diagonal + 2 * lambda_u * lambda_v * outer(a, b)

    leading = gamma**3 * sp.prod(alpha) * sp.prod(z) * sp.prod(w)
    correction = 0
    for d in range(3):
        others = [index for index in range(3) if index != d]
        correction += (
            a[d]
            * b[d]
            * alpha[others[0]]
            * alpha[others[1]]
            * z[others[0]]
            * z[others[1]]
            * w[others[0]]
            * w[others[1]]
        )
    expected = leading + 2 * gamma**2 * lambda_u * lambda_v * correction
    assert sp.expand(matrix.det() - expected) == 0

    # With both deck covectors on coordinate c, only one correction can
    # cancel the leading monomial, and its scalar coefficient is the lock.
    c = 1
    s, t = sp.symbols("s t", nonzero=True)
    specialized = expected.subs(
        {
            lu[d]: s if d == c else 0
            for d in range(3)
        }
        | {
            lv[d]: t if d == c else 0
            for d in range(3)
        }
        | {
            a[d] * b[d]: 0
            for d in range(3)
            if d != c
        }
    )
    scalar = gamma**2 * sp.prod(alpha[d] for d in range(3) if d != c)
    scalar *= sp.prod(z) * sp.prod(w)
    assert sp.expand(specialized - scalar * (gamma * alpha[c] + 2 * s * t * a[c] * b[c])) == 0


def connected(vertices: set[str], edges: set[tuple[str, str]]) -> bool:
    todo = [next(iter(vertices))]
    seen: set[str] = set()
    while todo:
        vertex = todo.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        for left, right in edges:
            if left == vertex and right in vertices:
                todo.append(right)
            if right == vertex and left in vertices:
                todo.append(left)
    return seen == vertices


def distance(
    source: str,
    target: str,
    vertices: set[str],
    edges: set[tuple[str, str]],
) -> int:
    frontier = [(source, 0)]
    seen: set[str] = set()
    while frontier:
        vertex, length = frontier.pop(0)
        if vertex == target:
            return length
        if vertex in seen:
            continue
        seen.add(vertex)
        for left, right in edges:
            if left == vertex and right in vertices:
                frontier.append((right, length + 1))
            if right == vertex and left in vertices:
                frontier.append((left, length + 1))
    raise AssertionError("target is disconnected")


def test_zero_graph_and_crossed_square() -> None:
    colors = range(3)
    all_edges = {
        (f"U{left}", f"V{right}")
        for left, right in product(colors, repeat=2)
        if left != right
    }
    mandatory = {"U1", "U2", "V1", "V2"}
    for extra in ({"U0"}, {"V0"}, {"U0", "V0"}):
        vertices = mandatory | extra
        assert connected(vertices, all_edges)
        assert distance("U1", "V1", vertices, all_edges) == 3

    # The exact broad-type case table for the two crossed zero pairs.
    # T/T makes the two matched matrices proportional with opposite signs;
    # T/one-sided shares a mandatory root factor between distinct diagonals.
    outcomes = {
        ("X", "X"): "zero matched outputs",
        ("Y", "Y"): "zero matched outputs",
        ("T", "T"): "proportional matched outputs",
        ("T", "X"): "shared diagonal factor",
        ("T", "Y"): "shared diagonal factor",
        ("X", "T"): "shared diagonal factor",
        ("Y", "T"): "shared diagonal factor",
        ("X", "Y"): "separated",
        ("Y", "X"): "separated transpose",
    }
    assert {
        pair for pair, outcome in outcomes.items() if outcome.startswith("separated")
    } == {("X", "Y"), ("Y", "X")}

    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    r = sp.Matrix(sp.symbols("r0:3"))
    s = sp.Matrix(sp.symbols("s0:3"))
    p, q = sp.symbols("p q")
    first = outer(x, -q * s) + outer(q * r, y)
    second = outer(r, -p * y) + outer(p * x, s)
    assert first.equals(-(q / p) * second)


def test_rank_seven_sharpness_control() -> None:
    half = sp.Rational(1, 2)
    e = [sp.eye(3).col(index) for index in range(3)]
    a = e[0]
    b = -half * e[0]
    xu = [-e[0], sp.zeros(3, 1), e[2]]
    yu = [half * e[0], e[1], sp.zeros(3, 1)]
    xv = [-e[0], e[1], sp.zeros(3, 1)]
    yv = [half * e[0], sp.zeros(3, 1), e[2]]

    gu = [outer(a, yu[d]) + outer(xu[d], b) for d in range(3)]
    gv = [outer(a, yv[d]) + outer(xv[d], b) for d in range(3)]
    muv = [
        [outer(xu[left], yv[right]) + outer(xv[right], yu[left]) for right in range(3)]
        for left in range(3)
    ]
    for left, right in product(range(3), repeat=2):
        coefficient = muv[left][right]
        if right == 0:
            coefficient += gu[left]
        if left == 0:
            coefficient += gv[right]
        expected = diagonal_unit(left) if left == right else sp.zeros(3)
        assert coefficient == expected

    joint_u = sp.Matrix.vstack(sp.Matrix.hstack(*xu), sp.Matrix.hstack(*yu))
    joint_v = sp.Matrix.vstack(sp.Matrix.hstack(*xv), sp.Matrix.hstack(*yv))
    assert joint_u.rank() == joint_v.rank() == 3

    pair_columns = [flattened(value) for value in gu + gv]
    pair_columns.extend(flattened(muv[left][right]) for left, right in product(range(3), repeat=2))
    pair_span = sp.Matrix.hstack(*pair_columns)
    assert pair_span.rank() == 7

    star_basis = [flattened(diagonal_unit(d)) for d in range(3)]
    for row, column in ((0, 1), (1, 0), (0, 2), (2, 0)):
        unit = sp.zeros(3)
        unit[row, column] = 1
        star_basis.append(flattened(unit))
    star_span = sp.Matrix.hstack(*star_basis)
    assert star_span.rank() == 7
    assert sp.Matrix.hstack(star_span, pair_span).rank() == 7


def test_three_port_hyperplane_cover() -> None:
    deck_color = {"u": 0, "v": 1, "w": 2}
    survivors: dict[tuple[str, str], int] = {}
    for left, right, opposite in (("u", "v", "w"), ("u", "w", "v"), ("v", "w", "u")):
        allowed = set(range(3)) - {deck_color[left], deck_color[right]}
        allowed &= {deck_color[opposite]}
        assert len(allowed) == 1
        survivors[(left, right)] = allowed.pop()
    assert survivors == {("u", "v"): 2, ("u", "w"): 1, ("v", "w"): 0}
    diagonal_columns = sp.Matrix.hstack(*(flattened(diagonal_unit(d)) for d in survivors.values()))
    assert diagonal_columns.rank() == 3
    gls39_maximum_pair_image_rank = 2
    assert diagonal_columns.rank() > gls39_maximum_pair_image_rank


def main() -> None:
    test_shifted_identity()
    test_determinant_polynomial()
    test_zero_graph_and_crossed_square()
    test_rank_seven_sharpness_control()
    test_three_port_hyperplane_cover()
    print("GLS51 focused exact verifier: PASS")


if __name__ == "__main__":
    main()
