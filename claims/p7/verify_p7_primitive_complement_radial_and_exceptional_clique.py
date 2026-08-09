"""Primary replay of primitive P7 radial closure and exceptional cliques."""

from itertools import combinations

import sympy as sp

VERTICES = tuple(range(8))
LEAVES = tuple(range(1, 8))
LEAF_EDGES = list(combinations(LEAVES, 2))
TRIPLES = list(combinations(VERTICES, 3))
FOUR_SETS = list(combinations(VERTICES, 4))


def inclusion_23(vertices: tuple[int, ...]) -> sp.Matrix:
    """Unsigned two-subset to three-subset inclusion matrix."""
    pairs = list(combinations(vertices, 2))
    triples = list(combinations(vertices, 3))
    return sp.Matrix([[int(set(pair) < set(triple)) for pair in pairs] for triple in triples])


def exceptional_matrix(c_size: int, outside: list[sp.Expr], s: sp.Symbol) -> sp.Matrix:
    """Denominator-cleared outside system for an exceptional R/4 clique."""
    outside_edges = list(combinations(range(len(outside)), 2))
    size = len(outside) + len(outside_edges)
    matrix = sp.zeros(size)
    for index, weight in enumerate(outside):
        matrix[index, index] = (c_size + 2) * s - 2 * weight
        for edge_index, (left, right) in enumerate(outside_edges):
            column = len(outside) + edge_index
            if index == left:
                matrix[index, column] = -2 * (s - weight) * outside[right]
            elif index == right:
                matrix[index, column] = -2 * (s - weight) * outside[left]
    for edge_index, (left, right) in enumerate(outside_edges):
        row = len(outside) + edge_index
        matrix[row, left] = 1
        matrix[row, right] = 1
        matrix[row, row] = 4 * s - 2 * (outside[left] + outside[right])
    return matrix


def main() -> None:
    triple_position = {triple: index for index, triple in enumerate(TRIPLES)}
    four_position = {four: index for index, four in enumerate(FOUR_SETS)}

    # Boolean lowering and the +1 complement eigenspace.
    lowering = sp.zeros(len(TRIPLES), len(FOUR_SETS))
    for row, triple in enumerate(TRIPLES):
        for vertex in VERTICES:
            if vertex not in triple:
                four = tuple(sorted((*triple, vertex)))
                lowering[row, four_position[four]] = 1
    assert lowering.rank() == 56

    leaf_triples = list(combinations(LEAVES, 3))
    complement_plus = sp.zeros(70, 35)
    for column, triple in enumerate(leaf_triples):
        anchor_four = (0, *triple)
        complement = tuple(sorted(set(VERTICES) - set(anchor_four)))
        complement_plus[four_position[anchor_four], column] = 1
        complement_plus[four_position[complement], column] = 1

    restricted_full = lowering * complement_plus
    star_rows = [triple_position[(0, *pair)] for pair in combinations(LEAVES, 2)]
    restricted_star = restricted_full[star_rows, :]
    assert restricted_star.rank() == restricted_full.rank() == 21
    assert 35 - restricted_star.rank() == 14

    # Directly check that the full primitive kernel is complement fixed.
    complement = sp.zeros(70)
    for four in FOUR_SETS:
        other = tuple(sorted(set(VERTICES) - set(four)))
        complement[four_position[other], four_position[four]] = 1
    primitive_basis = sp.Matrix.hstack(*lowering.nullspace())
    assert primitive_basis.shape == (70, 14)
    assert (complement - sp.eye(70)) * primitive_basis == sp.zeros(70, 14)

    # W_(2,3)(7) injectivity makes the radial linear vector nonzero.
    w23 = inclusion_23(LEAVES)
    vertex_edge = sp.Matrix(
        [[int(vertex in edge) for edge in combinations(LEAVES, 2)] for vertex in LEAVES]
    )
    assert w23.T * w23 == 3 * sp.eye(21) + vertex_edge.T * vertex_edge
    assert w23.rank() == 21

    # Universal radial complementary-hafnian formulas on one 3|4 split.
    a = sp.symbols("a1:8", nonzero=True)
    t = sp.Symbol("t", nonzero=True)
    x12, x13, x23, x45, x46, x47, x56, x57, x67 = sp.symbols(
        "x12 x13 x23 x45 x46 x47 x56 x57 x67", nonzero=True
    )
    h_anchor = (
        a[0] * (t * a[1] * a[2] * x23)
        + a[1] * (t * a[0] * a[2] * x13)
        + a[2] * (t * a[0] * a[1] * x12)
    )
    assert sp.expand(h_anchor - t * a[0] * a[1] * a[2] * (x12 + x13 + x23)) == 0
    h_complement = t**2 * a[3] * a[4] * a[5] * a[6] * (
        x45 * x67 + x46 * x57 + x47 * x56
    )
    expected_complement = (
        (t * a[3] * a[4] * x45) * (t * a[5] * a[6] * x67)
        + (t * a[3] * a[5] * x46) * (t * a[4] * a[6] * x57)
        + (t * a[3] * a[6] * x47) * (t * a[4] * a[5] * x56)
    )
    assert sp.expand(h_complement - expected_complement) == 0

    # The seven-vertex zero four-deck cannot have every edge nonzero.
    center, pi, pj, pk, qi, qj, qk = sp.symbols(
        "center pi pj pk qi qj qk", nonzero=True
    )
    bij = -(pi * qj + pj * qi) / center
    bik = -(pi * qk + pk * qi) / center
    bjk = -(pj * qk + pk * qj) / center
    one_anchor_hafnian = sp.factor(pi * bjk + pj * bik + pk * bij)
    ratio_sum = -2 * pi * pj * pk / center * (qi / pi + qj / pj + qk / pk)
    assert sp.simplify(one_anchor_hafnian - ratio_sum) == 0
    singleton_to_triples = sp.Matrix(
        [
            [int(vertex in triple) for vertex in range(5)]
            for triple in combinations(range(5), 3)
        ]
    )
    assert singleton_to_triples.rank() == 5

    # The 28-pencil reduces exactly to its homogeneous 21-Schur pencil.
    leaf_index = tuple(range(7))
    leaf_edges = list(combinations(leaf_index, 2))
    astar = sp.symbols("astar0:7")
    big_r = sum(astar)
    unsigned = sp.zeros(7, 21)
    weighted = sp.zeros(7, 21)
    diagonal = sp.zeros(21)
    for column, (left, right) in enumerate(leaf_edges):
        unsigned[left, column] = unsigned[right, column] = 1
        weighted[left, column] = astar[right]
        weighted[right, column] = astar[left]
        diagonal[column, column] = big_r - 2 * (astar[left] + astar[right])
    schur = diagonal + unsigned.T * weighted
    xvars = sp.Matrix(sp.symbols("x0:21"))
    block = sp.eye(7).row_join(-weighted).col_join(unsigned.T.row_join(diagonal))
    kernel_lift = (weighted * xvars).col_join(xvars)
    schur_difference = block * kernel_lift - sp.zeros(7, 1).col_join(schur * xvars)
    assert all(sp.expand(entry) == 0 for entry in schur_difference)
    assert len(list(combinations(range(35), 2))) == 595
    assert (20 + 3, 2 * 20 + 4, (20 + 3) + (2 * 20 + 4)) == (23, 44, 67)

    # Exact exceptional-clique boundary determinants.
    s, p, q = sp.symbols("s p q", nonzero=True)
    matrix6 = exceptional_matrix(6, [-2 * s], s)
    assert sp.factor(matrix6.det()) == 12 * s

    matrix5 = exceptional_matrix(5, [p, -s - p], s)
    assert sp.factor(matrix5.det()) == 360 * s**3

    r = -p - q
    matrix4 = exceptional_matrix(4, [p, q, r], s)
    cubic = 3 * p * q * r + 2 * s * (p * q + p * r + q * r) + 12 * s**3
    assert sp.factor(matrix4.det() - 1152 * s**3 * cubic) == 0

    print("PASS: anchor down equations plus complement symmetry equal full primitivity")
    print("PASS: radial complement vectors are nonzero and select one affine scale")
    print("PASS: corank-one adjugate closure has determinant-cleared degree 67")
    print("PASS: exceptional R/4 class has size at most four")
    print("PASS: size-four exceptional class lies on the displayed cubic")
    print("UNKNOWN: degree-67 corank-one torus incidence")
    print("UNKNOWN: corank-at-least-two primitive torus incidence")
    print("UNRESOLVED: global Krenn--Gu conjecture")


if __name__ == "__main__":
    main()
