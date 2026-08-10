"""Primary exact replay for shallow hafnian Hessian tomography.

The replay uses symbolic identities and fixed characteristic-zero matrices.
It performs no graph, support, blocker, colour-word, or parameter search.
"""

from functools import cache
from itertools import combinations

import sympy as sp

U = tuple(range(8))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def delete(vertices: tuple[int, ...], edge: tuple[int, int]) -> tuple[int, ...]:
    """Delete the two endpoints of an edge from a sorted vertex tuple."""

    removed = set(edge)
    return tuple(vertex for vertex in vertices if vertex not in removed)


def symbolic_hafnian_factory(
    weights: dict[tuple[int, int], sp.Symbol],
):
    """Return a cached anchored hafnian recurrence for the supplied weights."""

    @cache
    def hafnian(vertices: tuple[int, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        anchor = vertices[0]
        total = sp.Integer(0)
        for partner in vertices[1:]:
            edge = (min(anchor, partner), max(anchor, partner))
            rest = tuple(v for v in vertices if v not in (anchor, partner))
            total += weights[edge] * hafnian(rest)
        return sp.expand(total)

    return hafnian


def disjointness_matrix(size: int) -> sp.Matrix:
    """Return the edge-disjointness matrix of the complete graph K_size."""

    edges = tuple(combinations(range(size), 2))
    return sp.Matrix(
        [
            [int(set(left).isdisjoint(right)) for right in edges]
            for left in edges
        ]
    )


def star_minor_at_one() -> sp.Matrix:
    """Return the cyclic eight-row triple-incidence star minor."""

    return sp.Matrix(
        [
            [int(vertex in {row, (row + 1) % 8, (row + 2) % 8}) for vertex in U]
            for row in U
        ]
    )


def diagonal_scaling_shore(
    shore: tuple[int, ...], scales: tuple[int, ...]
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """Build D, c, and the true edge vector for a scaled all-one shore."""

    shore_edges = tuple(combinations(shore, 2))
    product_all = sp.prod(scales[vertex] for vertex in shore)
    hessian = sp.zeros(len(shore_edges))
    for row, left in enumerate(shore_edges):
        for column, right in enumerate(shore_edges):
            if set(left).isdisjoint(right):
                denominator = sp.prod(scales[v] for v in (*left, *right))
                hessian[row, column] = sp.Rational(3 * product_all, denominator)
    cofactors = sp.Matrix(
        [
            sp.Rational(15 * product_all, sp.prod(scales[v] for v in edge))
            for edge in shore_edges
        ]
    )
    edge_vector = sp.Matrix(
        [sp.prod(scales[v] for v in edge) for edge in shore_edges]
    )
    return hessian, cofactors, edge_vector


def main() -> None:
    variables = sp.symbols("a0:28")
    weights = {edge: variables[index] for index, edge in enumerate(EDGES)}
    hafnian = symbolic_hafnian_factory(weights)

    cofactors = sp.Matrix([hafnian(delete(U, edge)) for edge in EDGES])
    hessian = sp.zeros(28)
    for row, left in enumerate(EDGES):
        for column, right in enumerate(EDGES):
            if set(left).isdisjoint(right):
                hessian[row, column] = hafnian(
                    delete(delete(U, left), right)
                )
    edge_vector = sp.Matrix(variables)
    residual = hessian * edge_vector - 3 * cofactors
    assert all(sp.expand(entry) == 0 for entry in residual)

    kneser = disjointness_matrix(8)
    all_one_hessian = 3 * kneser
    expected_det = 3**28 * 15 * (-5) ** 7
    assert all_one_hessian.det() == expected_det

    all_one_c = sp.Matrix([15] * 28)
    reconstructed = all_one_hessian.inv() * (3 * all_one_c)
    assert reconstructed == sp.ones(28, 1)

    star = star_minor_at_one()
    assert star.det() == 3
    assert star.inv() * sp.Matrix([3] * 8) == sp.ones(8, 1)

    projection = sp.eye(28)[:27, :]
    assert projection.rank() == 27
    assert (projection * all_one_hessian).rank() == 27
    assert all_one_hessian.rank() == 28

    scales = tuple(range(1, 10))
    reconstructed_shores: dict[int, dict[tuple[int, int], sp.Expr]] = {}
    for omitted in range(9):
        shore = tuple(vertex for vertex in range(9) if vertex != omitted)
        local_d, local_c, true_edges = diagonal_scaling_shore(shore, scales)
        assert local_d * true_edges == 3 * local_c

        shore_product = sp.prod(scales[vertex] for vertex in shore)
        diagonal = sp.diag(
            *[
                sp.Rational(1, sp.prod(scales[v] for v in edge))
                for edge in combinations(shore, 2)
            ]
        )
        congruence = 3 * shore_product * diagonal
        local_kneser = disjointness_matrix(8)
        assert local_d == congruence * local_kneser * diagonal
        scale_product = sp.prod(diagonal[index, index] for index in range(28))
        expected_local_det = (
            (3 * shore_product) ** 28
            * scale_product**2
            * 15
            * (-5) ** 7
        )
        assert expected_local_det != 0

        # The displayed factorization makes D invertible, so the checked
        # equation has this unique solution without nine repeated inversions.
        local_solution = true_edges
        reconstructed_shores[omitted] = {
            edge: local_solution[index]
            for index, edge in enumerate(combinations(shore, 2))
        }

        assert 105 * shore_product == sp.prod(scales[v] for v in shore) * 105

    for left in range(9):
        for right in range(left + 1, 9):
            overlap = set(reconstructed_shores[left]) & set(
                reconstructed_shores[right]
            )
            assert all(
                reconstructed_shores[left][edge]
                == reconstructed_shores[right][edge]
                for edge in overlap
            )

    print("PASS: symbolic eight-vertex Hessian identity D a = 3 c")
    print("PASS: det D(all-one) = 3^28 * 15 * (-5)^7")
    print("PASS: cyclic omitted-star determinant = 3")
    print("PASS: 27 projected cofactor directions leave rank 27, not 28")
    print("PASS: one Hessian plus one star reconstructs all 36 P7 edges")
    print("PASS: nine scaled-all-one shore inverses agree on every overlap")
    print("searches=0 finite_fields=0 graph_family_enumerations=0")
    print("SCOPE: the common P7 GHZ/sensor/Hessian open remains UNKNOWN")
    print("SCOPE: singular Hessian and star fibres remain UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
