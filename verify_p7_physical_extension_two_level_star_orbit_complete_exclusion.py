"""Symbolic replay for complete exclusion of two-level physical P7 stars."""

from itertools import combinations

import sympy as sp

VERTICES = tuple(range(7))
EDGES = tuple(combinations(VERTICES, 2))


def standard_vectors(size):
    vectors = []
    for i in range(size - 1):
        vector = [sp.Integer(0)] * size
        vector[i] = 1
        vector[-1] = -1
        vectors.append(vector)
    return vectors


def local_pencil(m, p, q):
    n = 7 - m
    values = [p] * m + [q] * n
    alpha = sum(values)
    redge = sp.zeros(7, 21)
    pmat = sp.zeros(21, 7)
    delta = []
    for row, (i, j) in enumerate(EDGES):
        redge[i, row] = redge[j, row] = 1
        pmat[row, i] = values[j]
        pmat[row, j] = values[i]
        delta.append(alpha - 2 * (values[i] + values[j]))
    return sp.diag(*delta) + pmat * redge


def edge_vector(m, rule):
    result = sp.zeros(21, 1)
    for row, (i, j) in enumerate(EDGES):
        result[row] = rule(i, j, i < m, j < m)
    return result


def embedded_harmonic(vertices):
    internal_edges = tuple(combinations(vertices, 2))
    incidence = sp.zeros(len(vertices), len(internal_edges))
    vertex_index = {v: i for i, v in enumerate(vertices)}
    for col, (i, j) in enumerate(internal_edges):
        incidence[vertex_index[i], col] = 1
        incidence[vertex_index[j], col] = 1
    result = []
    for vector in incidence.nullspace():
        weights = dict(zip(internal_edges, vector))
        result.append(
            sp.Matrix([weights.get(edge, sp.Integer(0)) for edge in EDGES])
        )
    return result


def decomposition(m, p, q):
    n = 7 - m
    a_vertices = tuple(range(m))
    b_vertices = tuple(range(m, 7))
    a_standard = standard_vectors(m)
    b_standard = standard_vectors(n)
    columns = []
    blocks = []

    delta_aa = (m - 4) * p + n * q
    delta_ab = (m - 2) * p + (n - 2) * q
    delta_bb = m * p + (n - 4) * q

    for sa in a_standard:
        for sb in b_standard:
            columns.append(
                edge_vector(
                    m,
                    lambda i, j, ia, ja, sa=sa, sb=sb: (
                        sa[i] * sb[j - m] if ia and not ja else 0
                    ),
                )
            )
            blocks.append(sp.Matrix([[delta_ab]]))

    for vector in embedded_harmonic(a_vertices):
        columns.append(vector)
        blocks.append(sp.Matrix([[delta_aa]]))
    for vector in embedded_harmonic(b_vertices):
        columns.append(vector)
        blocks.append(sp.Matrix([[delta_bb]]))

    if m == 2:
        for sa in a_standard:
            columns.append(
                edge_vector(
                    m,
                    lambda i, _j, ia, ja, sa=sa: sa[i] if ia and not ja else 0,
                )
            )
            blocks.append(sp.Matrix([[delta_ab + n * q]]))
    else:
        ka = sp.Matrix(
            [
                [2 * (m - 3) * p + n * q, p * n],
                [(m - 2) * q, (m - 2) * p + 2 * (n - 1) * q],
            ]
        )
        for sa in a_standard:
            columns.extend(
                [
                    edge_vector(
                        m,
                        lambda i, j, ia, ja, sa=sa: (
                            sa[i] + sa[j] if ia and ja else 0
                        ),
                    ),
                    edge_vector(
                        m,
                        lambda i, _j, ia, ja, sa=sa: (
                            sa[i] if ia and not ja else 0
                        ),
                    ),
                ]
            )
            blocks.append(ka)

    kb = sp.Matrix(
        [
            [2 * (m - 1) * p + (n - 2) * q, p * (n - 2)],
            [m * q, m * p + 2 * (n - 3) * q],
        ]
    )
    for sb in b_standard:
        columns.extend(
            [
                edge_vector(
                    m,
                    lambda _i, j, ia, ja, sb=sb: (
                        sb[j - m] if ia and not ja else 0
                    ),
                ),
                edge_vector(
                    m,
                    lambda i, j, ia, ja, sb=sb: (
                        sb[i - m] + sb[j - m] if not ia and not ja else 0
                    ),
                ),
            ]
        )
        blocks.append(kb)

    type_columns = [
        edge_vector(m, lambda _i, _j, ia, ja: int(ia and ja)),
        edge_vector(m, lambda _i, _j, ia, ja: int(ia and not ja)),
        edge_vector(m, lambda _i, _j, ia, ja: int(not ia and not ja)),
    ]
    cmn = sp.Matrix(
        [
            [3 * (m - 2) * p + n * q, 2 * p * n, 0],
            [
                (m - 1) * q,
                2 * ((m - 1) * p + (n - 1) * q),
                (n - 1) * p,
            ],
            [0, 2 * q * m, m * p + 3 * (n - 2) * q],
        ]
    )
    columns.extend(type_columns)
    blocks.append(cmn)
    return sp.Matrix.hstack(*columns), sp.diag(*blocks), blocks


def primitive_orbit_coefficients(u, v, w):
    return (
        6 * w * (4 * v + w),
        6 * (u * w + 2 * v**2 + 2 * v * w),
        6 * (2 * u * v + u * w + 2 * v**2),
    )


def main():
    p, q, t = sp.symbols("p q t")

    c25, k25, blocks25 = decomposition(2, p, q)
    l25 = local_pencil(2, p, q)
    assert c25.shape == (21, 21) and c25.det() != 0
    assert l25 * c25 == c25 * k25
    det25 = sp.prod(block.det() for block in blocks25)
    expected25 = (
        5
        * 2**14
        * 3**6
        * q**8
        * (2 * p + q) ** 5
        * (p**2 + 2 * p * q + 3 * q**2) ** 4
    )
    assert sp.factor(det25 - expected25) == 0
    assert sp.factor((p**2 + 2 * p * q + 3 * q**2).subs(p, -q / 2)) != 0

    c34, k34, blocks34 = decomposition(3, p, q)
    l34 = local_pencil(3, p, q)
    assert c34.shape == (21, 21) and c34.det() != 0
    assert l34 * c34 == c34 * k34
    cubic = p**3 + 2 * p**2 * q + 3 * p * q**2 + 4 * q**3
    expected34 = (
        2**14
        * 3**6
        * p**2
        * q**4
        * (p + 2 * q) ** 6
        * (3 * p**2 + 2 * p * q + q**2) ** 3
        * cubic
    )
    det34 = sp.prod(block.det() for block in blocks34)
    assert sp.factor(det34 - expected34) == 0

    cubic_t = t**3 + 2 * t**2 + 3 * t + 4
    quadratic_t = 3 * t**2 + 2 * t + 1
    assert sp.resultant(cubic_t, quadratic_t, t) == 256
    assert cubic_t.subs(t, 0) != 0
    assert cubic_t.subs(t, 4) != 0
    assert cubic_t.subs(t, -2) != 0

    u = 8 * t**2
    v = -t * (3 * t + 4)
    w = -2 * (t**2 + 2 * t + 8) / t
    trivial34 = blocks34[-1].subs({p: t, q: 1})
    kernel_residual = trivial34 * sp.Matrix([u, v, w])
    assert all(sp.rem(sp.cancel(value).as_numer_denom()[0], cubic_t, t) == 0 for value in kernel_residual)

    primitive = primitive_orbit_coefficients(u, v, w)
    first_numerator, first_denominator = sp.factor(primitive[0]).as_numer_denom()
    expected_numerator = 24 * (t**2 + 2 * t + 8) * (
        6 * t**3 + 9 * t**2 + 2 * t + 8
    )
    assert sp.expand(first_numerator - expected_numerator) == 0
    assert first_denominator == t**2
    assert sp.resultant(cubic_t, t**2 + 2 * t + 8, t) == 256
    assert sp.resultant(cubic_t, 6 * t**3 + 9 * t**2 + 2 * t + 8, t) == 1280

    print("PASS: exact S_m x S_n edge-module bases diagonalize both two-level pencils")
    print("PASS: the 2+5 determinant walls omit the AA orbit")
    print("PASS: the 3+4 determinant has one full-edge block-constant cubic wall")
    print("PASS: a primitive five-set coefficient is nonzero at every cubic root")
    print("THEOREM: every nonzero P7 star with at most two values is excluded")
    print("searches=0 finite_fields=0 numerical_roots=0 graph_enumerations=0")
    print("SCOPE: three-level stars, general P7, and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
