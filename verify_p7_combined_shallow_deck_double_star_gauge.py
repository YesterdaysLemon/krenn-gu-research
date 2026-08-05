"""Primary exact checks for the P7 combined-deck double-star theorem.

The script audits fixed symbolic identities and tangent ranks.  It performs
no graph, support, word, or parameter-family search.
"""

from __future__ import annotations

from itertools import combinations

from sympy import Matrix, factor, simplify, symbols


def hafnian(matrix: list[list[object]], vertices: tuple[int, ...]) -> object:
    """Recursive hafnian used only on one symbolic representative per order."""
    if not vertices:
        return 1
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        partner = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        total += matrix[first][partner] * hafnian(matrix, remainder)
    return simplify(total)


def verify_double_star_hafnians() -> None:
    """Check the order-four formula and representative higher annihilation."""
    center, x0, x1, y0, y1 = symbols("c x0 x1 y0 y1")
    size = 8
    matrix: list[list[object]] = [[0 for _ in range(size)] for _ in range(size)]

    def put(i: int, j: int, value: object) -> None:
        matrix[i][j] = value
        matrix[j][i] = value

    put(0, 1, center)
    leaf_x = [x0, x1, 2, 3, 5, 7]
    leaf_y = [y0, y1, 11, 13, 17, 19]
    for offset, leaf in enumerate(range(2, size)):
        put(0, leaf, leaf_x[offset])
        put(1, leaf, leaf_y[offset])

    four = hafnian(matrix, (0, 1, 2, 3))
    assert simplify(four - (x0 * y1 + x1 * y0)) == 0
    assert hafnian(matrix, (0, 1, 2, 3, 4, 5)) == 0
    assert hafnian(matrix, tuple(range(8))) == 0

    scale = symbols("t", nonzero=True)
    scaled = (scale * x0) * (y1 / scale) + (scale * x1) * (y0 / scale)
    assert simplify(scaled - four) == 0


def off_diagonal_gram_jacobian(m: int) -> Matrix:
    """Jacobian of x_i*y_j+x_j*y_i at x_i=1, y_i=i+1."""
    rows: list[list[int]] = []
    for i, j in combinations(range(m), 2):
        row = [0] * (2 * m)
        row[2 * i] = j + 1
        row[2 * i + 1] = 1
        row[2 * j] = i + 1
        row[2 * j + 1] = 1
        rows.append(row)
    return Matrix(rows)


def triangle_edge_matrix(m: int) -> Matrix:
    """Map leaf-edge variations to all triangle sums."""
    edges = list(combinations(range(m), 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    rows: list[list[int]] = []
    for triple in combinations(range(m), 3):
        row = [0] * len(edges)
        for edge in combinations(triple, 2):
            row[edge_index[edge]] = 1
        rows.append(row)
    return Matrix(rows)


def verify_tangent_ranks() -> None:
    """Check restricted rank 13 and the rank-34 ambient certificate."""
    m = 7
    gram = off_diagonal_gram_jacobian(m)
    assert gram.rank() == 2 * m - 1 == 13

    triangle = triangle_edge_matrix(m)
    assert triangle.rank() == len(list(combinations(range(m), 2))) == 21

    leaf_edges = list(combinations(range(m), 2))
    edge_index = {edge: index for index, edge in enumerate(leaf_edges)}
    width = len(leaf_edges) + 2 * m + 1
    rows: list[list[int]] = []

    # Four-deck rows on {p,i,j,k}: all three varied leaf edges occur.
    for triple in combinations(range(m), 3):
        row = [0] * width
        for edge in combinations(triple, 2):
            row[edge_index[edge]] = 1
        rows.append(row)

    # Four-deck rows on {p,q,i,j}: c*z_ij plus the Gram differential.
    gram_offset = len(leaf_edges)
    for (i, j), gram_row in zip(combinations(range(m), 2), gram.tolist(), strict=True):
        row = [0] * width
        row[edge_index[(i, j)]] = 1
        row[gram_offset : gram_offset + 2 * m] = gram_row
        rows.append(row)

    ambient_certificate = Matrix(rows)
    assert ambient_certificate.rank() == 34

    center_direction = Matrix([0] * (width - 1) + [1])
    shore_direction = [0] * len(leaf_edges)
    for i in range(m):
        shore_direction.extend((1, -(i + 1)))
    shore_direction.append(0)
    assert ambient_certificate * center_direction == Matrix.zeros(len(rows), 1)
    assert ambient_certificate * Matrix(shore_direction) == Matrix.zeros(len(rows), 1)


def verify_support_incidence_torus() -> None:
    """Check the two-dimensional vertex-scaling kernel for pqij labels."""
    m = 7
    rows: list[list[int]] = []
    for i, j in combinations(range(m), 2):
        row = [1, 1] + [0] * m
        row[2 + i] = 1
        row[2 + j] = 1
        rows.append(row)
    incidence = Matrix(rows)
    assert incidence.rank() == m
    assert len(incidence.nullspace()) == 2


def verify_zero_deck_ratio_identity() -> None:
    """Audit the symbolic substitution behind the edge-torus exclusion."""
    a12 = symbols("a12", nonzero=True)
    u_i, u_j, u_k = symbols("u_i u_j u_k", nonzero=True)
    r_i, r_j, r_k = symbols("r_i r_j r_k")

    def inferred_edge(u_left: object, r_left: object, u_right: object, r_right: object) -> object:
        return -(u_left * r_right * u_right + u_right * r_left * u_left) / a12

    a_jk = inferred_edge(u_j, r_j, u_k, r_k)
    a_ik = inferred_edge(u_i, r_i, u_k, r_k)
    a_ij = inferred_edge(u_i, r_i, u_j, r_j)
    substituted = u_i * a_jk + u_j * a_ik + u_k * a_ij
    expected = -2 * u_i * u_j * u_k * (r_i + r_j + r_k) / a12
    assert simplify(substituted - expected) == 0

    # Four triple sums on four ratios have determinant -3.
    triple_sums = Matrix(
        [
            [1, 1, 1, 0],
            [1, 1, 0, 1],
            [1, 0, 1, 1],
            [0, 1, 1, 1],
        ]
    )
    assert factor(triple_sums.det()) == -3


def main() -> None:
    verify_double_star_hafnians()
    print("PASS: symbolic double-star H4 formula and H6/H8 annihilation")
    verify_tangent_ranks()
    print("PASS: hyperbolic Gram rank 13 and ambient nine-vertex rank 34")
    verify_support_incidence_torus()
    print("PASS: double-star deck-support incidence torus has dimension two")
    verify_zero_deck_ratio_identity()
    print("PASS: zero four-deck cannot meet the full edge torus in characteristic zero")
    print("SCOPE: fixed symbolic audits; searches=0; support_enumerations=0")
    print("BOUNDARY: GHZ exclusion of the two-cover stratum and global Krenn-Gu remain UNKNOWN")


if __name__ == "__main__":
    main()
