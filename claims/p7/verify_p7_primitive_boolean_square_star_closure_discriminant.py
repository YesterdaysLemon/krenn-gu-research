"""Primary exact replay of the P7 star-closure discriminant theorem."""

from itertools import combinations

import sympy as sp

LEAVES = tuple(range(1, 8))
LEAF_EDGES = list(combinations(LEAVES, 2))


def inclusion_23(vertices: tuple[int, ...]) -> sp.Matrix:
    """Unsigned two-subset/three-subset inclusion matrix."""
    edges = list(combinations(vertices, 2))
    triples = list(combinations(vertices, 3))
    return sp.Matrix([[int(set(edge) < set(triple)) for edge in edges] for triple in triples])


def main() -> None:
    # Universal derivation of the normalized anchor equation and leaf equation.
    aj, ak, al, yj, yk, yl, xjk, xjl, xkl, big_r = sp.symbols(
        "aj ak al yj yk yl xjk xjl xkl R", nonzero=True
    )
    bjk = aj * ak * xjk
    bjl = aj * al * xjl
    bkl = ak * al * xkl
    rj, rk, rl = aj * (1 + yj), ak * (1 + yk), al * (1 + yl)
    anchor_triangle = sp.expand(
        aj * rk + ak * rj + bjk * big_r
        - 2 * (aj * ak + aj * bjk + ak * bjk)
    )
    anchor_reduced = aj * ak * (yj + yk + (big_r - 2 * (aj + ak)) * xjk)
    assert sp.expand(anchor_triangle - anchor_reduced) == 0

    leaf_triangle = sp.expand(
        bjk * rl + bjl * rk + bkl * rj
        - 2 * (bjk * bjl + bjk * bkl + bjl * bkl)
    )
    leaf_reduced = aj * ak * al * (
        xjk * (1 + yl)
        + xjl * (1 + yk)
        + xkl * (1 + yj)
        - 2 * (aj * xjk * xjl + ak * xjk * xkl + al * xjl * xkl)
    )
    assert sp.expand(leaf_triangle - leaf_reduced) == 0

    # Build the fixed all-one star pencil and its exact Schur complement.
    edge_position = {edge: index for index, edge in enumerate(LEAF_EDGES)}
    unsigned = sp.zeros(7, 21)
    weighted = sp.zeros(7, 21)
    for edge, column in edge_position.items():
        for vertex in edge:
            row = vertex - 1
            unsigned[row, column] = 1
            weighted[row, column] = 1
    assert unsigned == weighted
    assert unsigned * unsigned.T == 5 * sp.eye(7) + sp.ones(7)
    schur = 3 * sp.eye(21) + unsigned.T * weighted
    expected = 15 * 8**6 * 3**14
    assert schur.det() == expected == 5 * 8**6 * 3**15

    # Directly rebuild T and check the Schur determinant at the same point.
    block = sp.eye(7).row_join(-weighted).col_join(unsigned.T.row_join(3 * sp.eye(21)))
    assert block.shape == (28, 28)
    assert block.det() == expected

    # W_(2,3)(s) is injective for every possible s>=5 here.
    for size in range(5, 9):
        vertices = tuple(range(size))
        w23 = inclusion_23(vertices)
        edge_incidence = sp.Matrix(
            [[int(vertex in edge) for edge in combinations(vertices, 2)] for vertex in vertices]
        )
        gram = w23.T * w23
        assert gram == (size - 4) * sp.eye(sp.binomial(size, 2)) + edge_incidence.T * edge_incidence
        assert edge_incidence * edge_incidence.T == (size - 2) * sp.eye(size) + sp.ones(size)
        assert w23.rank() == sp.binomial(size, 2)

    # Universal difference identity for the four-value Cayley classification.
    y1, y2, y3, y4 = sp.symbols("y1 y2 y3 y4", nonzero=True)

    def cayley(x: sp.Expr, y: sp.Expr, z: sp.Expr) -> sp.Expr:
        return x * y + x * z + y * z - x - y - z

    assert sp.factor(cayley(y1, y2, y3) - cayley(y1, y2, y4)) == (y3 - y4) * (y1 + y2 - 1)
    cayley_ideal = sp.groebner(
        [
            cayley(y1, y2, y3),
            cayley(y1, y2, y4),
            cayley(y1, y3, y4),
            cayley(y2, y3, y4),
        ],
        y1,
        y2,
        y3,
        y4,
        order="lex",
    )
    for value in (y1, y2, y3, y4):
        consequence = value * (value - 1) * (value**2 - value + 1)
        assert cayley_ideal.reduce(sp.expand(consequence))[1] == 0
    for left, right in combinations((y1, y2, y3, y4), 2):
        consequence = (left - right) * (left + right - 1)
        assert cayley_ideal.reduce(sp.expand(consequence))[1] == 0

    # The two classified branches and the final four-zero-row contradiction.
    p, q, n = sp.symbols("p q n", nonzero=True)
    assert sp.rem(p**2 - p + 1, p**2 - p + 1, p) == 0
    q_sub = 1 - p
    assert sp.rem(sp.expand(p * q_sub - 1), p**2 - p + 1, p) == 0
    same_reciprocal = sp.expand(2 * p**2 - 2 * p)
    cross_reciprocal = sp.expand(2 * p * q_sub - p - q_sub)
    assert sp.rem(same_reciprocal + 2, p**2 - p + 1, p) == 0
    assert sp.rem(cross_reciprocal - 1, p**2 - p + 1, p) == 0

    row_a = sp.Rational(3, 2) + n * q + (4 - n) * p
    row_b = sp.Rational(3, 2) + n * p + (4 - n) * q
    assert sp.expand(row_a - row_b - (2 * n - 4) * (q - p)) == 0
    assert sp.expand(row_a.subs({n: 2, q: 1 - p})) == sp.Rational(7, 2)

    # Boundary equivalence is exactly Delta*x=-(y_j+y_k), with x nonzero.
    delta = sp.Symbol("Delta")
    assert sp.expand((yj + yk + delta * xjk).subs(delta, 0)) == yj + yk
    assert sp.solve(sp.Eq(yj + yk + delta * xjk, 0), delta) == [-(yj + yk) / xjk]

    print("PASS: universal anchor and 35-leaf normalized triangle formulas")
    print("PASS: exact 28 x 28 all-one star-pencil determinant 5*8^6*3^15")
    print("PASS: exact W_(2,3)(s) injectivity for 5<=s<=8")
    print("PASS: four-zero-row Cayley classification and 7/2 contradiction")
    print("PASS: exceptional divisor iff y-pair sum vanishes on the torus")
    print("UNKNOWN: P=0 full-support kernel satisfying all 35 leaf quadrics")
    print("UNKNOWN: primitive Boolean-square edge-torus point")
    print("UNRESOLVED: global Krenn--Gu conjecture")


if __name__ == "__main__":
    main()
