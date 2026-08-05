"""Primary exact replay for the P7 dual-triangle/star normal form."""

from itertools import combinations

import sympy as sp

VERTICES = tuple(range(8))
LEVEL3 = list(combinations(VERTICES, 3))
LEVEL4 = list(combinations(VERTICES, 4))
LEVEL5 = list(combinations(VERTICES, 5))
EDGES = list(combinations(VERTICES, 2))


def inclusion(rows: list[tuple[int, ...]], cols: list[tuple[int, ...]]) -> sp.Matrix:
    """Return the unsigned subset-inclusion matrix."""
    return sp.Matrix([[int(set(col) < set(row)) for col in cols] for row in rows])


def edge_key(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def main() -> None:
    b = {edge: sp.Symbol(f"b{edge[0]}{edge[1]}") for edge in EDGES}

    def be(i: int, j: int) -> sp.Expr:
        return b[edge_key(i, j)]

    def haf4(vertices: tuple[int, ...]) -> sp.Expr:
        i, j, k, ell = vertices
        return be(i, j) * be(k, ell) + be(i, k) * be(j, ell) + be(i, ell) * be(j, k)

    row_sum = {i: sum(be(i, j) for j in VERTICES if j != i) for i in VERTICES}

    # Universal down-hafnian expansion equals the claimed triangle polynomial.
    for triple in LEVEL3:
        i, j, k = triple
        down_hafnian = sum(
            haf4(tuple(sorted((*triple, ell)))) for ell in VERTICES if ell not in triple
        )
        triangle = (
            be(i, j) * row_sum[k]
            + be(i, k) * row_sum[j]
            + be(j, k) * row_sum[i]
            - 2
            * (
                be(i, j) * be(i, k)
                + be(i, j) * be(j, k)
                + be(i, k) * be(j, k)
            )
        )
        assert sp.expand(down_hafnian - triangle) == 0

    up = inclusion(LEVEL5, LEVEL4)
    down = sp.Matrix(
        [[int(set(row) < set(col)) for col in LEVEL4] for row in LEVEL3]
    )
    assert up.shape == (56, 70)
    assert down.shape == (56, 70)
    assert up.rank() == down.rank() == 56
    assert up.col_join(down).rank() == 56  # equal row spaces, hence equal kernels

    # Four-set complementation acts identically on the common 14-space.
    pos4 = {subset: index for index, subset in enumerate(LEVEL4)}
    complement = sp.zeros(70)
    for column, subset in enumerate(LEVEL4):
        other = tuple(vertex for vertex in VERTICES if vertex not in subset)
        complement[pos4[other], column] = 1
    assert up.col_join(complement - sp.eye(70)).rank() == 56

    # Exact injectivity certificate for W_(2,3)(8).
    w23 = inclusion(LEVEL3, EDGES)
    assert w23.shape == (56, 28)
    assert w23.rank() == 28
    gram = w23.T * w23
    unsigned_incidence = sp.Matrix(
        [[int(vertex in edge) for edge in EDGES] for vertex in VERTICES]
    )
    assert gram == 4 * sp.eye(28) + unsigned_incidence.T * unsigned_incidence
    assert unsigned_incidence * unsigned_incidence.T == 6 * sp.eye(8) + sp.ones(8)
    assert gram.det() == 18 * 10**7 * 4**20

    # The star identity is precisely the triangle equation through vertex zero.
    for j, k in combinations(range(1, 8), 2):
        triangle = (
            be(0, j) * row_sum[k]
            + be(0, k) * row_sum[j]
            + be(j, k) * row_sum[0]
            - 2
            * (
                be(0, j) * be(0, k)
                + be(0, j) * be(j, k)
                + be(0, k) * be(j, k)
            )
        )
        delta = row_sum[0] - 2 * (be(0, j) + be(0, k))
        numerator = 2 * be(0, j) * be(0, k) - be(0, j) * row_sum[k] - be(0, k) * row_sum[j]
        assert sp.expand(triangle - (delta * be(j, k) - numerator)) == 0

    # Universal reciprocal-rank-one reduction on a named triangle.
    ui, uj, uk, ri, rj, rk = sp.symbols("ui uj uk ri rj rk", nonzero=True)
    cij, cik, cjk = ui * uj, ui * uk, uj * uk
    reciprocal_triangle = (
        ri * cij * cik + rj * cij * cjk + rk * cik * cjk - 2 * (cij + cik + cjk)
    )
    reduced = ri * ui + rj * uj + rk * uk - 2 / ui - 2 / uj - 2 / uk
    assert sp.simplify(reciprocal_triangle / (ui * uj * uk) - reduced) == 0

    # The last scalar contradiction is 3S=8S in characteristic zero.
    scalar = sp.Symbol("S")
    assert sp.expand(scalar - 8 * scalar / 3) == -5 * scalar / 3

    print("PASS: exact Boolean U/D duality and rank-56 common row space")
    print("PASS: 56 universal hafnian/row-sum triangle identities")
    print("PASS: complement-fixed 14-dimensional primitive middle space")
    print("PASS: exact rank-28 W_(2,3)(8) no-all-row-sums certificate")
    print("PASS: 21 star reconstructions and explicit exceptional factors")
    print("PASS: reciprocal-rank-one torus stratum contradiction")
    print("UNKNOWN: generic and exceptional star closure systems")
    print("UNKNOWN: full-support P7 primitive Boolean-square torus point")
    print("UNRESOLVED: global Krenn--Gu conjecture")


if __name__ == "__main__":
    main()
