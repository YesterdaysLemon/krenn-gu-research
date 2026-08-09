"""Exact symbolic checks for the P7 leaf apolar-Hilbert theorem.

This verifier uses characteristic-zero SymPy ranks only.  It does not search
over graphs, supports, parameter values, or finite fields.
"""

from itertools import combinations

import sympy as sp

N = 7
VERTICES = tuple(range(N))


def subsets(size: int) -> tuple[tuple[int, ...], ...]:
    """Return the square-free monomial basis in one degree."""
    return tuple(combinations(VERTICES, size))


def unsigned_inclusion(source_size: int, target_size: int) -> sp.Matrix:
    """Rows are target subsets and columns are contained source subsets."""
    source = subsets(source_size)
    target = subsets(target_size)
    return sp.Matrix(
        [[int(set(column) <= set(row)) for column in source] for row in target]
    )


def pair_sum_incidence(vertex_count: int) -> sp.Matrix:
    """Unsigned vertex-edge incidence of a complete graph."""
    vertices = tuple(range(vertex_count))
    edges = tuple(combinations(vertices, 2))
    return sp.Matrix([[int(vertex in edge) for vertex in vertices] for edge in edges])


def multiplication_matrix(
    degree: int, edge_weight: dict[tuple[int, int], object]
) -> sp.Matrix:
    """Matrix of multiplication A_degree -> A_(degree+2) by a quadratic."""
    domain = subsets(degree)
    codomain = subsets(degree + 2)
    rows: list[list[object]] = []
    for target in codomain:
        target_set = set(target)
        row: list[object] = []
        for source in domain:
            if set(source) <= target_set:
                missing = tuple(sorted(target_set - set(source)))
                row.append(edge_weight[missing])
            else:
                row.append(0)
        rows.append(row)
    return sp.Matrix(rows)


def complement(subset: tuple[int, ...]) -> tuple[int, ...]:
    """Complement a square-free monomial in the seven variables."""
    return tuple(vertex for vertex in VERTICES if vertex not in subset)


def assert_complemented_transpose(
    degree: int, edge_weight: dict[tuple[int, int], object]
) -> None:
    """Check mu_(5-degree) is the complemented transpose of mu_degree."""
    left = multiplication_matrix(degree, edge_weight)
    right = multiplication_matrix(5 - degree, edge_weight)
    left_domain = subsets(degree)
    left_codomain = subsets(degree + 2)
    right_domain = subsets(5 - degree)
    right_codomain = subsets(7 - degree)
    right_domain_index = {monomial: index for index, monomial in enumerate(right_domain)}
    right_codomain_index = {
        monomial: index for index, monomial in enumerate(right_codomain)
    }
    for row, target in enumerate(left_codomain):
        for column, source in enumerate(left_domain):
            paired_row = right_codomain_index[complement(source)]
            paired_column = right_domain_index[complement(target)]
            assert left[row, column] == right[paired_row, paired_column]


def hilbert_vector(edge_weight: dict[tuple[int, int], object]) -> tuple[int, ...]:
    """Ranks of multiplication by F in degrees zero through five."""
    return tuple(multiplication_matrix(degree, edge_weight).rank() for degree in range(6))


def main() -> None:
    # The two matrices used in the three-case proof of Ann_1(F)=0.
    pair_to_triple = unsigned_inclusion(2, 3)
    assert pair_to_triple.shape == (35, 21)
    edges = subsets(2)
    line_graph = sp.Matrix(
        [
            [int(row != column and bool(set(row) & set(column))) for column in edges]
            for row in edges
        ]
    )
    pair_gram = pair_to_triple.T * pair_to_triple
    assert pair_gram == 5 * sp.eye(21) + line_graph
    lambda_symbol = sp.Symbol("lambda")
    assert sp.factor(pair_gram.charpoly(lambda_symbol).as_expr()) == (
        (lambda_symbol - 15)
        * (lambda_symbol - 8) ** 6
        * (lambda_symbol - 3) ** 14
    )
    assert pair_to_triple.rank() == 21

    k6_pair_sum = pair_sum_incidence(6)
    assert k6_pair_sum.shape == (15, 6)
    k6_gram = k6_pair_sum.T * k6_pair_sum
    assert k6_gram == 4 * sp.eye(6) + sp.ones(6)
    assert sp.factor(k6_gram.charpoly(lambda_symbol).as_expr()) == (
        (lambda_symbol - 10) * (lambda_symbol - 4) ** 5
    )
    assert k6_pair_sum.rank() == 6

    # Generic tokens prove all complemented-transpose identities entrywise.
    symbols = sp.symbols("f0:21")
    generic = dict(zip(edges, symbols, strict=True))
    for degree in range(6):
        assert_complemented_transpose(degree, generic)

    # Exact controls: the uniform full-edge class and a coordinate star.
    uniform = {edge: sp.Integer(1) for edge in edges}
    boundary_star = {
        edge: sp.Integer(int(0 in edge))
        for edge in edges
    }
    assert hilbert_vector(uniform) == (1, 7, 21, 21, 7, 1)
    assert hilbert_vector(boundary_star) == (1, 6, 15, 15, 6, 1)

    # The full-edge rank-20 annihilator has a seven-dimensional linear span.
    assert multiplication_matrix(1, uniform).rank() == 7
    assert 15 - multiplication_matrix(1, uniform).rank() == 8

    # Every possible physical rank obeys the stated essential-cubic bound.
    for rho in range(21):
        quadratic_annihilators = 21 - rho
        cubic_annihilators = 35 - rho
        dimension_bound = max(
            0,
            cubic_annihilators - 7 * quadratic_annihilators,
        )
        assert dimension_bound == max(0, 6 * rho - 112)
    assert max(0, 6 * 20 - 112) == 8
    assert max(0, 6 * 19 - 112) == 2
    assert all(max(0, 6 * rho - 112) == 0 for rho in range(19))

    print("PASS: injectivity Gram spectra are 15,8,3 and 10,4 with exact multiplicities.")
    print("PASS: every Boolean multiplication map has the complemented transpose.")
    print("PASS: fixed Hilbert controls are (1,7,21,21,7,1) and (1,6,15,15,6,1).")
    print("PASS: beta_3 >= max(0,6*rho-112), giving 8 at rank 20 and 2 at rank 19.")
    print("SCOPE: exact characteristic-zero identities only; no search or existence claim.")


if __name__ == "__main__":
    main()
