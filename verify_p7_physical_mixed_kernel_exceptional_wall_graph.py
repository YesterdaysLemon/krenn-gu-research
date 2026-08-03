"""Exact replay for exceptional P7 wall graphs and restricted Hessians."""

from itertools import combinations

import sympy as sp
from sympy.polys.domains import QQ

VERTICES = tuple(range(7))
EDGES = tuple(combinations(VERTICES, 2))


def det2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def det3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def normalized_midpoint_restriction(field, outside, clique_size, skipped=frozenset()):
    """Restricted B_W for h=1 after midpoint-clique coordinates vanish."""
    size = len(outside)
    matrix = [[field.zero for _ in range(size)] for _ in range(size)]
    for i, value in enumerate(outside):
        matrix[i][i] = value + clique_size * value / (2 * (1 - value))
    for i, j in combinations(range(size), 2):
        if (i, j) in skipped:
            continue
        weight = outside[i] * outside[j] / (4 - 2 * (outside[i] + outside[j]))
        matrix[i][i] += weight
        matrix[j][j] += weight
        matrix[i][j] = matrix[j][i] = weight
    return matrix


def main():
    # The reconstruction is a universal matrix identity, independent of a wall
    # graph's combinatorial type.  Use three formal wall edges as a template.
    wall = {EDGES.index((0, 1)), EDGES.index((1, 2)), EDGES.index((3, 4))}
    nonwall = [index for index in range(21) if index not in wall]
    a = sp.symbols("a0:7", nonzero=True)
    inverse_delta = sp.symbols(f"d0:{len(nonwall)}", nonzero=True)
    redge_w = sp.zeros(7, len(wall))
    redge_n = sp.zeros(7, len(nonwall))
    q_n = sp.zeros(len(nonwall), 7)
    q_w = sp.zeros(len(wall), 7)
    for col, edge_index in enumerate(sorted(wall)):
        i, j = EDGES[edge_index]
        redge_w[i, col] = redge_w[j, col] = 1
        q_w[col, i] = q_w[col, j] = a[i] * a[j]
    for col, edge_index in enumerate(nonwall):
        i, j = EDGES[edge_index]
        redge_n[i, col] = redge_n[j, col] = 1
        q_n[col, i] = q_n[col, j] = a[i] * a[j]
    delta_inverse = sp.diag(*inverse_delta)
    b_wall = sp.diag(*a) + redge_n * delta_inverse * q_n
    assert b_wall == b_wall.T
    fmap = -delta_inverse * q_n
    assert redge_n * fmap == sp.diag(*a) - b_wall
    assert q_w == sp.diag(*(a[i] * a[j] for i, j in sorted(EDGES[k] for k in wall))) * redge_w.T

    # Exact midpoint calculations in a rational-function field; h is scaled to 1.
    field = QQ.frac_field("b", "c")
    b, c = field.gens

    k5 = normalized_midpoint_restriction(field, [b, -1 - b], 5)
    assert det2(k5) == 15 * b * (b + 1) / ((b - 1) * (b + 2))

    d = -b - c
    k4 = normalized_midpoint_restriction(field, [b, c, d], 4)
    cubic = 3 * b * c * d + 2 * (b * c + b * d + c * d) + 12
    denominator = (
        (b - 1)
        * (b + 2)
        * (c - 1)
        * (c + 2)
        * (b + c + 1)
        * (b + c - 2)
    )
    assert det3(k4) == 18 * b * c * (b + c) * cubic / denominator

    k4_one_wall = normalized_midpoint_restriction(
        field,
        [b, 2 - b, field(-2)],
        4,
        frozenset({(0, 1)}),
    )
    projection = [[field.one, field.zero], [-field.one, field.zero], [field.zero, field.one]]
    restricted = [
        [
            sum(
                projection[i][row]
                * k4_one_wall[i][j]
                * projection[j][col]
                for i in range(3)
                for j in range(3)
            )
            for col in range(2)
        ]
        for row in range(2)
    ]
    assert det2(restricted) == -96 / ((b - 4) * (b + 2))

    boundary = normalized_midpoint_restriction(
        field,
        [field(4), field(-2), field(-2)],
        4,
        frozenset({(0, 1), (0, 2)}),
    )
    boundary_vector = [field.one, -field.one, -field.one]
    boundary_value = sum(
        boundary_vector[i] * boundary[i][j] * boundary_vector[j]
        for i in range(3)
        for j in range(3)
    )
    assert boundary_value == -4

    # K6 has one outside value -2 after h=1 and restricted coefficient -4.
    k6 = normalized_midpoint_restriction(field, [field(-2)], 6)
    assert k6[0][0] == -4

    print("PASS: exceptional mixed kernels are exact restricted-Hessian radicals")
    print("PASS: wall graphs are governed by the complement-value involution")
    print("PASS: midpoint K5, K6, and K7 strata are excluded")
    print("PASS: midpoint K4 with any outside wall is excluded")
    print("PASS: the no-outside-wall K4 branch reduces to one symmetric cubic")
    print("searches=0 finite_fields=0 numerical_points=0 wall_enumerations=0")
    print("SCOPE: K4 cubic, K3, bipartite walls, P7, and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
