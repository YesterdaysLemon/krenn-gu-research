"""Exact symbolic replay for the P7 Boolean-down/master-Hessian reduction."""

from itertools import combinations

import sympy as sp

N = 7
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))
TRIPLES = tuple(combinations(VERTICES, 3))
EDGE_INDEX = {edge: k for k, edge in enumerate(EDGES)}


def incidence_matrices():
    """Return vertex-edge, down, and complemented-up incidence matrices."""
    redge = sp.zeros(N, len(EDGES))
    for k, edge in enumerate(EDGES):
        for i in edge:
            redge[i, k] = 1

    down3 = sp.zeros(len(EDGES), len(TRIPLES))
    up2 = sp.zeros(len(EDGES), len(TRIPLES))
    for row, edge in enumerate(EDGES):
        edge_set = set(edge)
        for col, triple in enumerate(TRIPLES):
            triple_set = set(triple)
            down3[row, col] = int(edge_set <= triple_set)
            up2[row, col] = 2 * int(edge_set.isdisjoint(triple_set))
    return redge, down3, up2


def pencils(a, redge):
    """Build the local and complemented multiplication pencils."""
    alpha = sum(a)
    delta = [alpha - 2 * (a[i] + a[j]) for i, j in EDGES]

    pmat = sp.zeros(len(EDGES), N)
    for row, (i, j) in enumerate(EDGES):
        pmat[row, i] = a[j]
        pmat[row, j] = a[i]
    local = sp.diag(*delta) + pmat * redge

    mixed = sp.zeros(len(EDGES), len(EDGES))
    for row, g in enumerate(EDGES):
        gset = set(g)
        for col, e in enumerate(EDGES):
            eset = set(e)
            if eset.isdisjoint(gset):
                mixed[row, col] = 2 * sum(
                    a[v] for v in VERTICES if v not in eset | gset
                )
    return delta, pmat, local, mixed


def assert_zero_matrix(matrix):
    assert all(sp.cancel(entry) == 0 for entry in matrix)


def main():
    redge, down3, up2 = incidence_matrices()
    ones = sp.ones(len(EDGES), len(EDGES))
    identity = sp.eye(len(EDGES))
    jmat = 2 * identity + sp.Rational(2, 3) * ones - redge.T * redge

    assert down3.rank() == up2.rank() == len(EDGES)
    assert jmat * down3 == up2
    assert jmat.det() == 2**16 * 3**6
    lam = sp.symbols("lambda")
    assert sp.factor(jmat.charpoly(lam).as_expr()) == (
        (lam - 4) * (lam + 3) ** 6 * (lam - 2) ** 14
    )

    # Prove the pencil identity universally, with seven independent symbols.
    a = sp.symbols("a0:7")
    delta, pmat, local, mixed = pencils(a, redge)
    assert_zero_matrix(mixed - jmat * local)

    # The all-one control recovers the three edge-module eigenspaces.
    _, _, local_one, mixed_one = pencils([sp.Integer(1)] * N, redge)
    assert sp.factor(local_one.charpoly(lam).as_expr()) == (
        (lam - 15) * (lam - 8) ** 6 * (lam - 3) ** 14
    )
    assert sp.factor(mixed_one.charpoly(lam).as_expr()) == (
        (lam - 60) * (lam + 24) ** 6 * (lam - 6) ** 14
    )

    # Generic Schur complement, symmetry, reconstruction, and master energy.
    delta_inverse = sp.diag(*(1 / value for value in delta))
    tmat = sp.eye(N) + redge * delta_inverse * pmat
    amat = sp.diag(*a)
    hmat = tmat * amat
    assert_zero_matrix(hmat - hmat.T)

    fmap = -delta_inverse * pmat
    assert_zero_matrix(redge * fmap - (sp.eye(N) - tmat))
    assert_zero_matrix(local * fmap + pmat * tmat)

    x = sp.symbols("x0:7")
    energy = sp.Rational(1, 2) * sum(a[i] * x[i] ** 2 for i in VERTICES)
    for k, (i, j) in enumerate(EDGES):
        energy += (
            sp.Rational(1, 2)
            * a[i]
            * a[j]
            / delta[k]
            * (x[i] + x[j]) ** 2
        )
    energy_hessian = sp.hessian(energy, x)
    assert_zero_matrix(energy_hessian - hmat)

    # Check the determinant lemma over an exact point away from every divisor.
    sample_a = tuple(sp.Integer(2) ** i for i in VERTICES)
    sample_delta, _, sample_local, sample_mixed = pencils(sample_a, redge)
    assert all(value != 0 for value in sample_delta)
    _, sample_p, _, _ = pencils(sample_a, redge)
    sample_t = sp.eye(N) + redge * sp.diag(
        *(1 / value for value in sample_delta)
    ) * sample_p
    assert sample_local.det() == sp.prod(sample_delta) * sample_t.det()
    assert sample_mixed.det() == (2**16 * 3**6) * sample_local.det()

    # Independently recover the two contractions from the 21 local residuals.
    f = sp.symbols("f0:21")
    fvec = sp.Matrix(f)
    rvec = redge * fvec
    total_r = sum(rvec)
    residual = local * fvec
    fa = sp.zeros(N, 1)
    for k, (i, j) in enumerate(EDGES):
        fa[i] += a[j] * f[k]
        fa[j] += a[i] * f[k]
    for i in VERTICES:
        incident_residual = sum(
            residual[EDGE_INDEX[tuple(sorted((i, j)))]]
            for j in VERTICES
            if j != i
        )
        contracted = a[i] * total_r + 2 * (sum(a) - 2 * a[i]) * rvec[i]
        contracted -= 2 * fa[i]
        assert sp.expand(incident_residual - contracted) == 0

    print("PASS: Boolean down and complemented up have the same 14-dimensional kernel")
    print("PASS: U2 = J D3 and det(J) = 2^16 3^6")
    print("PASS: M_A = J L_A as a universal seven-parameter pencil")
    print("PASS: the generic 21-dimensional kernel descends to the symmetric 7x7 Hessian")
    print("PASS: exact determinant and reconstruction controls hold")
    print("UNKNOWN: whether a full-edge physical P7 extension survives all remaining equations")


if __name__ == "__main__":
    main()
