"""Primary exact replay for the P7 quotient-singular radial incidence."""

from __future__ import annotations

import itertools

import sympy as sp

VERTICES = tuple(range(8))
LEAVES = tuple(range(1, 8))
EDGES = tuple(itertools.combinations(VERTICES, 2))
LEAF_EDGES = tuple(itertools.combinations(LEAVES, 2))
TRIPLES = tuple(itertools.combinations(LEAVES, 3))
FOUR_SETS = tuple(itertools.combinations(LEAVES, 4))
FIVE_SETS = tuple(itertools.combinations(LEAVES, 5))
SIX_SETS = tuple(itertools.combinations(LEAVES, 6))
GLOBAL_FOUR_SETS = tuple(itertools.combinations(VERTICES, 4))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
LEAF_EDGE_INDEX = {edge: index for index, edge in enumerate(LEAF_EDGES)}
FOUR_INDEX = {subset: index for index, subset in enumerate(FOUR_SETS)}
FIVE_INDEX = {subset: index for index, subset in enumerate(FIVE_SETS)}


def boolean_add(
    left: dict[frozenset[int], sp.Expr],
    right: dict[frozenset[int], sp.Expr],
) -> dict[frozenset[int], sp.Expr]:
    """Add sparse Boolean-algebra elements."""
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = sp.expand(out.get(monomial, 0) + coefficient)
        if out[monomial] == 0:
            del out[monomial]
    return out


def boolean_scale(
    scalar: sp.Expr,
    value: dict[frozenset[int], sp.Expr],
) -> dict[frozenset[int], sp.Expr]:
    """Scale a sparse Boolean-algebra element."""
    return {
        monomial: sp.expand(scalar * coefficient)
        for monomial, coefficient in value.items()
        if sp.expand(scalar * coefficient) != 0
    }


def boolean_mul(
    left: dict[frozenset[int], sp.Expr],
    right: dict[frozenset[int], sp.Expr],
) -> dict[frozenset[int], sp.Expr]:
    """Multiply modulo z_i^2=0."""
    out: dict[frozenset[int], sp.Expr] = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            if left_monomial & right_monomial:
                continue
            monomial = left_monomial | right_monomial
            out[monomial] = sp.expand(
                out.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {
        monomial: sp.expand(coefficient)
        for monomial, coefficient in out.items()
        if sp.expand(coefficient) != 0
    }


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    """Test a symbolic matrix after exact expansion."""
    return all(sp.expand(entry) == 0 for entry in matrix)


def leaf_lefschetz(source_degree: int) -> sp.Matrix:
    """One-step multiplication by ell_L."""
    source = tuple(itertools.combinations(LEAVES, source_degree))
    target = tuple(itertools.combinations(LEAVES, source_degree + 1))
    return sp.Matrix(
        [
            [int(set(column).issubset(row)) for column in source]
            for row in target
        ]
    )


def leaf_complement_4_to_3() -> sp.Matrix:
    """Matrix J:A_4(L)->A_3(L)."""
    return sp.Matrix(
        [
            [int(tuple(vertex for vertex in LEAVES if vertex not in triple) == four)
             for four in FOUR_SETS]
            for triple in TRIPLES
        ]
    )


def leaf_total_zero_basis() -> sp.Matrix:
    """Integral 21 x 20 basis with the final edge balancing the total."""
    basis = sp.zeros(21, 20)
    for column in range(20):
        basis[column, column] = 1
        basis[20, column] = -1
    return basis


def leaf_down_matrix() -> sp.Matrix:
    """Unsigned vertex-edge incidence on the seven leaves."""
    return sp.Matrix(
        [[int(vertex in edge) for edge in LEAF_EDGES] for vertex in LEAVES]
    )


def global_iota_basis(leaf_basis: sp.Matrix) -> sp.Matrix:
    """Embed total-zero leaf quadrics into the global zero-row quotient."""
    down = leaf_down_matrix() * leaf_basis
    out = sp.zeros(28, 20)
    for leaf_row, edge in enumerate(LEAF_EDGES):
        out[EDGE_INDEX[edge], :] = leaf_basis[leaf_row, :]
    for vertex_index, vertex in enumerate(LEAVES):
        out[EDGE_INDEX[(0, vertex)], :] = -down[vertex_index, :]
    return out


def standard_tableaux() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Return the fourteen standard tableaux of shape (4,4)."""
    tableaux = []
    for top in itertools.combinations(VERTICES, 4):
        bottom = tuple(vertex for vertex in VERTICES if vertex not in top)
        if all(left < right for left, right in zip(top, bottom, strict=True)):
            tableaux.append((top, bottom))
    return tableaux


def polytabloid(
    top: tuple[int, ...], bottom: tuple[int, ...]
) -> dict[tuple[int, ...], int]:
    """Expand one fixed (4,4) column polytabloid."""
    out = {subset: 0 for subset in GLOBAL_FOUR_SETS}
    for choices in itertools.product((0, 1), repeat=4):
        subset = tuple(
            sorted(
                bottom[index] if choice else top[index]
                for index, choice in enumerate(choices)
            )
        )
        out[subset] += (-1) ** sum(choices)
    return out


def catalecticant(global_h: dict[tuple[int, ...], sp.Expr]) -> sp.Matrix:
    """Build the 28 x 28 complement-fixed edge catalecticant."""
    return sp.Matrix(
        [
            [
                global_h[tuple(sorted((*edge, *other)))]
                if set(edge).isdisjoint(other)
                else 0
                for other in EDGES
            ]
            for edge in EDGES
        ]
    )


def global_h_from_leaf(n_vector: sp.Matrix) -> dict[tuple[int, ...], sp.Expr]:
    """Build H_N=z_0 JN+N from leaf four-set coefficients."""
    out: dict[tuple[int, ...], sp.Expr] = {}
    for subset in GLOBAL_FOUR_SETS:
        if 0 not in subset:
            out[subset] = n_vector[FOUR_INDEX[subset]]
        else:
            triple = tuple(vertex for vertex in subset if vertex != 0)
            complement = tuple(vertex for vertex in LEAVES if vertex not in triple)
            out[subset] = n_vector[FOUR_INDEX[complement]]
    return out


def phi_matrix(n_vector: sp.Matrix, leaf_basis: sp.Matrix) -> sp.Matrix:
    """Matrix of Phi_N on a supplied leaf quadratic basis."""
    n_form = {
        frozenset(subset): n_vector[index]
        for index, subset in enumerate(FOUR_SETS)
    }
    jn_form = {
        frozenset(triple): n_vector[
            FOUR_INDEX[tuple(vertex for vertex in LEAVES if vertex not in triple)]
        ]
        for triple in TRIPLES
    }
    down = leaf_down_matrix() * leaf_basis
    columns = []
    for column in range(leaf_basis.cols):
        g_form = {
            frozenset(edge): leaf_basis[row, column]
            for row, edge in enumerate(LEAF_EDGES)
            if leaf_basis[row, column] != 0
        }
        d_form = {
            frozenset({vertex}): down[row, column]
            for row, vertex in enumerate(LEAVES)
            if down[row, column] != 0
        }
        phi = boolean_add(
            boolean_mul(g_form, jn_form),
            boolean_scale(-1, boolean_mul(d_form, n_form)),
        )
        columns.append(
            sp.Matrix([phi.get(frozenset(subset), 0) for subset in FIVE_SETS])
        )
    return sp.Matrix.hstack(*columns)


def main() -> None:
    """Run the exact symbolic replay."""
    lefschetz_4_5 = leaf_lefschetz(4)
    lefschetz_3_4 = leaf_lefschetz(3)
    complement_4_3 = leaf_complement_4_to_3()
    assert lefschetz_4_5.rank() == 21
    primitive_basis = sp.Matrix.hstack(*lefschetz_4_5.nullspace())
    assert primitive_basis.shape == (35, 14)
    assert matrix_is_zero(lefschetz_4_5 * primitive_basis)
    assert matrix_is_zero(
        (sp.eye(35) + lefschetz_3_4 * complement_4_3) * primitive_basis
    )

    h_coordinates = sp.symbols("h_0:14")
    n_vector = primitive_basis * sp.Matrix(h_coordinates)
    global_h = global_h_from_leaf(n_vector)
    h_form = {frozenset(subset): coefficient for subset, coefficient in global_h.items()}
    ell_global = {frozenset({vertex}): sp.Integer(1) for vertex in VERTICES}
    assert boolean_mul(ell_global, h_form) == {}
    for subset in GLOBAL_FOUR_SETS:
        complement = tuple(vertex for vertex in VERTICES if vertex not in subset)
        assert sp.expand(global_h[subset] - global_h[complement]) == 0

    leaf_basis = leaf_total_zero_basis()
    iota_basis = global_iota_basis(leaf_basis)
    incidence = sp.Matrix(
        [[int(vertex in edge) for vertex in VERTICES] for edge in EDGES]
    )
    assert leaf_basis.rank() == 20
    assert iota_basis.rank() == 20
    assert incidence.T * iota_basis == sp.zeros(8, 20)

    gamma = sp.symbols("g_0:20")
    g_vector = leaf_basis * sp.Matrix(gamma)
    down_vector = leaf_down_matrix() * g_vector
    g_form = {
        frozenset(edge): g_vector[row]
        for row, edge in enumerate(LEAF_EDGES)
    }
    d_form = {
        frozenset({vertex}): down_vector[row]
        for row, vertex in enumerate(LEAVES)
    }
    w_form = boolean_add(
        g_form,
        {
            frozenset({0, vertex}): -down_vector[row]
            for row, vertex in enumerate(LEAVES)
        },
    )
    n_form = {
        frozenset(subset): n_vector[index]
        for index, subset in enumerate(FOUR_SETS)
    }
    jn_form = {
        frozenset(triple): n_vector[
            FOUR_INDEX[tuple(vertex for vertex in LEAVES if vertex not in triple)]
        ]
        for triple in TRIPLES
    }
    phi = boolean_add(
        boolean_mul(g_form, jn_form),
        boolean_scale(-1, boolean_mul(d_form, n_form)),
    )
    ell_leaf = {frozenset({vertex}): sp.Integer(1) for vertex in LEAVES}
    assert boolean_mul(g_form, n_form) == boolean_scale(
        -1, boolean_mul(ell_leaf, phi)
    )
    factored = boolean_add(
        {frozenset({0}) | monomial: coefficient for monomial, coefficient in phi.items()},
        boolean_scale(-1, boolean_mul(ell_leaf, phi)),
    )
    assert boolean_mul(w_form, h_form) == factored

    phi_on_basis = phi_matrix(n_vector, leaf_basis)
    complemented_phi = sp.zeros(21, 20)
    for edge_row, edge in enumerate(LEAF_EDGES):
        complement = tuple(vertex for vertex in LEAVES if vertex not in edge)
        complemented_phi[edge_row, :] = phi_on_basis[FIVE_INDEX[complement], :]
    assert matrix_is_zero(sp.ones(1, 21) * complemented_phi)
    square_phi = complemented_phi[:20, :]
    assert square_phi.shape == (20, 20)

    global_d = catalecticant(global_h)
    assert matrix_is_zero(global_d * incidence)
    assert matrix_is_zero(
        global_d * iota_basis - iota_basis * square_phi
    )

    # Basis-level perfect-pairing normalization for D w = complement(wH).
    for edge in EDGES:
        for other in EDGES:
            if set(edge).isdisjoint(other):
                union = tuple(sorted((*edge, *other)))
                complement = tuple(vertex for vertex in VERTICES if vertex not in union)
                assert sp.expand(global_h[union] - global_h[complement]) == 0
            else:
                assert global_d[EDGE_INDEX[edge], EDGE_INDEX[other]] == 0

    # Physical radial coefficient dictionary.
    a = {vertex: sp.Symbol(f"a_{vertex}") for vertex in LEAVES}
    x = {edge: sp.Symbol(f"x_{edge[0]}{edge[1]}") for edge in LEAF_EDGES}
    linear_a = {frozenset({vertex}): a[vertex] for vertex in LEAVES}
    physical_f = {
        frozenset(edge): a[edge[0]] * a[edge[1]] * x[edge]
        for edge in LEAF_EDGES
    }
    physical_m = boolean_mul(linear_a, physical_f)
    physical_n = boolean_scale(sp.Rational(1, 2), boolean_mul(physical_f, physical_f))
    for triple in TRIPLES:
        expected = sp.prod(a[vertex] for vertex in triple) * sum(
            x[edge] for edge in itertools.combinations(triple, 2)
        )
        assert sp.expand(physical_m[frozenset(triple)] - expected) == 0
    for four in FOUR_SETS:
        p, q, r, s = four
        expected = sp.prod(a[vertex] for vertex in four) * (
            x[(p, q)] * x[(r, s)]
            + x[(p, r)] * x[(q, s)]
            + x[(p, s)] * x[(q, r)]
        )
        assert sp.expand(physical_n[frozenset(four)] - expected) == 0
    t = sp.Symbol("t")
    q_form = boolean_add(
        {frozenset({0}) | monomial: coefficient for monomial, coefficient in linear_a.items()},
        boolean_scale(t, physical_f),
    )
    q_square_half = boolean_scale(sp.Rational(1, 2), boolean_mul(q_form, q_form))
    radial_expansion = boolean_add(
        {
            frozenset({0}) | monomial: t * coefficient
            for monomial, coefficient in physical_m.items()
        },
        boolean_scale(t**2, physical_n),
    )
    assert set(q_square_half) == set(radial_expansion)
    assert all(
        sp.expand(q_square_half[monomial] - radial_expansion[monomial]) == 0
        for monomial in q_square_half
    )

    # Fixed ambient primitive rank-20 control inherited from the sibling note.
    tableaux = standard_tableaux()
    assert len(tableaux) == 14
    control = {subset: 0 for subset in GLOBAL_FOUR_SETS}
    for top, bottom in tableaux:
        vector = polytabloid(top, bottom)
        for subset in GLOBAL_FOUR_SETS:
            control[subset] += vector[subset]
    control_n = sp.Matrix([control[subset] for subset in FOUR_SETS])
    assert lefschetz_4_5 * control_n == sp.zeros(21, 1)
    control_phi = phi_matrix(control_n, leaf_basis)
    control_complemented = sp.zeros(21, 20)
    for edge_row, edge in enumerate(LEAF_EDGES):
        complement = tuple(vertex for vertex in LEAVES if vertex not in edge)
        control_complemented[edge_row, :] = control_phi[FIVE_INDEX[complement], :]
    assert sp.ones(1, 21) * control_complemented == sp.zeros(1, 20)
    control_square = control_complemented[:20, :]
    assert control_square.rank() == 20
    control_determinant = control_square.det(method="domain-ge")
    assert control_determinant == 1_519_811_734_108_372_992
    assert sp.factorint(control_determinant) == {2: 24, 3: 13, 7: 1, 8117: 1}
    assert catalecticant(control).rank() == 20

    print("PASS: quotient kernel equals the degree-two Boolean annihilator")
    print("PASS: leaf primitive space has dimension 14 and N+ell*JN=0")
    print("PASS: iota identifies the 20-dimensional leaf hyperplane with P")
    print("PASS: iota(G)H_N=(z_0-ell_L)Phi_N(G)")
    print("PASS: D|P is conjugate to the square 20 x 20 complemented Phi map")
    print("PASS: radial u/v coefficient dictionary and Q^2/2 expansion")
    print("PASS: fixed Phi determinant = 2^24*3^13*7*8117")
    print("searches=0 finite_fields=0 graph_enumerations=0 groebner=0")
    print("SCOPE: the rank-20 control is not asserted physical")
    print("SCOPE: physical quotient-singular radial incidence remains UNKNOWN")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
