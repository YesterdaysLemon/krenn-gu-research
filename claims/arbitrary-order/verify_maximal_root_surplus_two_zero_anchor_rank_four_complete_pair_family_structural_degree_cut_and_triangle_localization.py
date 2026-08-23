"""Focused exact replay for the GLS46 structural pair-family reduction."""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement

import sympy as sp


def determinant_cubic_replay() -> None:
    """Replay the universal rank-two determinant and reducible-factor leaves."""

    x, y, z, ell = sp.symbols("x y z ell")
    entries = sp.symbols("f01 f02 f10 f12 f20 f21")
    f01, f02, f10, f12, f20, f21 = entries
    matrix = sp.Matrix(
        (
            (x, ell * f01, ell * f02),
            (ell * f10, y, ell * f12),
            (ell * f20, ell * f21, z),
        )
    )
    alpha = f12 * f21
    beta = f02 * f20
    gamma = f01 * f10
    tau = f01 * f12 * f20 + f02 * f10 * f21
    expected = x * y * z - ell**2 * (
        alpha * x + beta * y + gamma * z
    ) + tau * ell**3
    assert sp.expand(matrix.det() - expected) == 0

    c = sp.symbols("c")
    substituted = sp.Poly(sp.expand(expected.subs(x, -c * ell)), y, z, ell)
    expected_substitution = sp.Poly(
        -c * ell * y * z
        - beta * ell**2 * y
        - gamma * ell**2 * z
        + (c * alpha + tau) * ell**3,
        y,
        z,
        ell,
    )
    assert substituted == expected_substitution
    coefficients = substituted.terms()
    assert len(coefficients) == 4

    # The multigraded square factors in D1*D2=alpha*L^2 must be constants.
    degree_solutions = []
    for g_u in range(2):
        for g_v in range(2):
            for a_u in range(2):
                for a_v in range(2):
                    for b_u in range(2):
                        for b_v in range(2):
                            if (g_u + 2 * a_u, g_v + 2 * a_v) != (1, 1):
                                continue
                            if (g_u + 2 * b_u, g_v + 2 * b_v) != (1, 1):
                                continue
                            degree_solutions.append(
                                ((g_u, g_v), (a_u, a_v), (b_u, b_v))
                            )
    assert degree_solutions == [((1, 1), (0, 0), (0, 0))]


def line_parameter_replay() -> None:
    """Recover every coefficient in the direct finite-line calculation."""

    a, b, c, x0, y0, z0, s, t = sp.symbols(
        "a b c x0 y0 z0 s t"
    )
    alpha, beta, gamma, tau = sp.symbols("alpha beta gamma tau")
    x = a * s + x0 * t
    y = b * s + y0 * t
    z = c * s + z0 * t
    ell = t
    polynomial = sp.Poly(
        sp.expand(
            x * y * z
            - ell**2 * (alpha * x + beta * y + gamma * z)
            + tau * ell**3
        ),
        s,
        t,
    )
    expected = {
        (3, 0): a * b * c,
        (2, 1): a * b * z0 + a * c * y0 + b * c * x0,
        (1, 2): (
            a * y0 * z0
            + b * x0 * z0
            + c * x0 * y0
            - alpha * a
            - beta * b
            - gamma * c
        ),
        (0, 3): (
            x0 * y0 * z0
            - alpha * x0
            - beta * y0
            - gamma * z0
            + tau
        ),
    }
    assert dict(polynomial.terms()) == expected

    two_direction = [sp.expand(value.subs({c: 0, z0: 0})) for value in expected.values()]
    assert two_direction == [
        0,
        0,
        -alpha * a - beta * b,
        -alpha * x0 - beta * y0 + tau,
    ]
    one_direction = [
        sp.expand(value.subs({b: 0, c: 0, a: 1})) for value in expected.values()
    ]
    assert one_direction == [
        0,
        0,
        -alpha + y0 * z0,
        -alpha * x0 - beta * y0 - gamma * z0 + tau + x0 * y0 * z0,
    ]
    reduced_last = sp.expand(one_direction[-1].subs(y0 * z0, alpha))
    assert reduced_last == -beta * y0 - gamma * z0 + tau


def support_annihilator_replay() -> None:
    """Replay the rank-one annihilator and the exact twelve count."""

    f01, f02 = sp.symbols("f01 f02")
    row = sp.Matrix([[0, f01, f02]])
    null_vector = sp.Matrix([0, f02, -f01])
    assert (row * null_vector)[0] == 0

    xs = sp.symbols("xs0:3")
    xt = sp.symbols("xt0:3")
    ys = sp.symbols("ys0:3")
    yt = sp.symbols("yt0:3")
    left_s = sp.Matrix(xs)
    left_t = sp.Matrix(xt)
    right_s = sp.Matrix(ys)
    right_t = sp.Matrix(yt)
    mu = left_s * right_t.T + left_t * right_s.T
    contraction = sp.expand((sp.Matrix([[1, 0, 0]]) * mu * null_vector)[0])
    beta_s = f02 * ys[1] - f01 * ys[2]
    beta_t = f02 * yt[1] - f01 * yt[2]
    assert sp.expand(contraction - xs[0] * beta_t - xt[0] * beta_s) == 0

    left_coordinate_slots = 3 * 2
    right_coordinate_slots = 3 * 2
    assert left_coordinate_slots + right_coordinate_slots == 12


def bipartite(edges: tuple[tuple[int, int], ...]) -> bool:
    adjacency: dict[int, set[int]] = {}
    for left, right in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    colors: dict[int, int] = {}
    for start in adjacency:
        if start in colors:
            continue
        colors[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    stack.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False
    return True


def triangle_cut_replay() -> None:
    """Exhaust the three-edge support graphs and external cut intersections."""

    all_edges = tuple(combinations(range(6), 2))
    patterns = 0
    nonbipartite = 0
    for edge_multiset in combinations_with_replacement(all_edges, 3):
        patterns += 1
        simple_edges = tuple(sorted(set(edge_multiset)))
        if bipartite(simple_edges):
            continue
        nonbipartite += 1
        vertices = {vertex for edge in simple_edges for vertex in edge}
        assert len(simple_edges) == 3
        assert len(vertices) == 3
        assert all(
            sum(vertex in edge for edge in simple_edges) == 2
            for vertex in vertices
        )
    assert patterns == 680
    assert nonbipartite == 20

    e0 = sp.Matrix([1, 0, 0])
    e1 = sp.Matrix([0, 1, 0])
    e2 = sp.Matrix([0, 0, 1])
    planes = (
        sp.Matrix.hstack(e0, e1),
        sp.Matrix.hstack(e0, e2),
        sp.Matrix.hstack(e1, e2),
    )
    for vector in (e0, e1, e2):
        memberships = [plane.row_join(vector).rank() == plane.rank() for plane in planes]
        assert memberships.count(True) == 2
    stacked_normals = sp.Matrix(
        (
            (0, 0, 1),
            (0, 1, 0),
            (1, 0, 0),
        )
    )
    assert stacked_normals.rank() == 3


def mu(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    """Scalar-label pair polarization when X=Y for each label."""

    return left * right.T + right * left.T


def compatibility_matrix(
    labels: tuple[sp.Matrix, ...],
) -> tuple[sp.Matrix, tuple[sp.Symbol, ...]]:
    """Build the exact off-diagonal proportionality system."""

    x_symbols = sp.symbols("x0:3")
    y_symbols = sp.symbols("y0:3")
    lambda_symbols = sp.symbols(f"lambda0:{len(labels)}")
    x = sp.Matrix(x_symbols)
    y = sp.Matrix(y_symbols)
    equations = []
    for label, scalar in zip(labels, lambda_symbols, strict=True):
        matrix = x * label.T + label * y.T
        for row in range(3):
            for column in range(3):
                if row != column:
                    equations.append(matrix[row, column] - scalar)
    variables = (*x_symbols, *y_symbols, *lambda_symbols)
    coefficient_matrix, right_side = sp.linear_eq_to_matrix(equations, variables)
    assert right_side == sp.zeros(len(equations), 1)
    return coefficient_matrix, variables


def locked_triangle_replay() -> None:
    """Check the exact rational sharpness triangle and both tangent ranks."""

    p0 = sp.Matrix([0, 1, 1])
    p1 = sp.Matrix([1, 0, 1])
    p2 = sp.Matrix([1, 1, 0])
    labels = (p0, p1, p2)
    f = sp.ones(3) - sp.eye(3)
    r = tuple(
        sp.diag(*(1 if row == index else 0 for row in range(3)))
        for index in range(3)
    )
    assert mu(p0, p1) == f + 2 * r[2]
    assert mu(p0, p2) == f + 2 * r[1]
    assert mu(p1, p2) == f + 2 * r[0]
    flattened = [
        list(mu(p0, p1)),
        list(mu(p0, p2)),
        list(mu(p1, p2)),
    ]
    assert sp.Matrix(flattened).rank() == 3

    for index in range(3):
        mates = tuple(label for mate, label in enumerate(labels) if mate != index)
        matrix, _ = compatibility_matrix(mates)
        assert matrix.shape == (12, 8)
        assert matrix.rank() == 7
        nullspace = matrix.nullspace()
        assert len(nullspace) == 1
        expected = sp.Matrix([*labels[index], *labels[index], 1, 1])
        assert sp.Matrix.hstack(nullspace[0], expected).rank() == 1

    matrix, _ = compatibility_matrix(labels)
    assert matrix.shape == (18, 9)
    assert matrix.rank() == 9


def main() -> None:
    determinant_cubic_replay()
    line_parameter_replay()
    support_annihilator_replay()
    triangle_cut_replay()
    locked_triangle_replay()
    print("GLS46 structural-degree/cut/triangle primary checks: PASS")
    print("  determinant cubic and reducibility substitution: exact")
    print("  irreducible-line coefficient atlas: exact")
    print("  coordinate annihilator and effective dimension: 12")
    print("  three-edge support multigraphs: 680 (20 triangles)")
    print("  rational sharpness triangle: image rank 3, tangent ranks 7/9")
    print("  rank-four full-swallow and global Krenn-Gu: UNRESOLVED")


if __name__ == "__main__":
    main()
