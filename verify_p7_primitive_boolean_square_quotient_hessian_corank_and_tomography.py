"""Verify primitive P7 quotient-Hessian corank and tomography exactly."""

from itertools import combinations, product

import sympy as sp

VERTICES = tuple(range(8))
EDGES = tuple(combinations(VERTICES, 2))
FOUR_SETS = tuple(combinations(VERTICES, 4))
FOUR_INDEX = {subset: index for index, subset in enumerate(FOUR_SETS)}


def standard_tableaux() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """The fourteen standard tableaux of shape (4,4)."""
    tableaux = []
    for top in combinations(VERTICES, 4):
        bottom = tuple(vertex for vertex in VERTICES if vertex not in top)
        if all(left < right for left, right in zip(top, bottom, strict=True)):
            tableaux.append((top, bottom))
    return tableaux


def polytabloid(top: tuple[int, ...], bottom: tuple[int, ...]) -> sp.Matrix:
    """Coefficient column of the product of the four column differences."""
    values = [0] * len(FOUR_SETS)
    for choices in product((0, 1), repeat=4):
        subset = tuple(
            sorted(
                bottom[index] if choice else top[index]
                for index, choice in enumerate(choices)
            )
        )
        values[FOUR_INDEX[subset]] += (-1) ** sum(choices)
    return sp.Matrix(values)


def catalecticant(four_vector: sp.Matrix) -> sp.Matrix:
    """Edge Hessian C_H(e,f)=H_(e union f) on disjoint pairs."""
    matrix = sp.zeros(len(EDGES))
    for row, edge in enumerate(EDGES):
        for column, other in enumerate(EDGES):
            if set(edge).isdisjoint(other):
                subset = tuple(sorted((*edge, *other)))
                matrix[row, column] = four_vector[FOUR_INDEX[subset]]
    return matrix


def incidence() -> sp.Matrix:
    matrix = sp.zeros(len(EDGES), len(VERTICES))
    for row, edge in enumerate(EDGES):
        for vertex in edge:
            matrix[row, vertex] = 1
    return matrix


def is_primitive(four_vector: sp.Matrix) -> bool:
    for triple in combinations(VERTICES, 3):
        total = sum(
            four_vector[FOUR_INDEX[tuple(sorted((*triple, vertex)))]]
            for vertex in VERTICES
            if vertex not in triple
        )
        if total != 0:
            return False
    return True


def is_complement_fixed(four_vector: sp.Matrix) -> bool:
    for subset in FOUR_SETS:
        complement = tuple(vertex for vertex in VERTICES if vertex not in subset)
        if four_vector[FOUR_INDEX[subset]] != four_vector[FOUR_INDEX[complement]]:
            return False
    return True


def main() -> None:
    tableaux = standard_tableaux()
    assert len(tableaux) == 14
    primitive_basis = [polytabloid(top, bottom) for top, bottom in tableaux]
    assert sp.Matrix.hstack(*primitive_basis).rank() == 14

    vertex_edge = incidence()
    assert vertex_edge.T * vertex_edge == 6 * sp.eye(8) + sp.ones(8)
    assert vertex_edge.rank() == 8

    # Checking the complete primitive basis proves the universal linear claim.
    for vector in primitive_basis:
        assert is_primitive(vector)
        assert is_complement_fixed(vector)
        assert catalecticant(vector) * vertex_edge == sp.zeros(28, 8)

    control = sum(primitive_basis, sp.zeros(70, 1))
    control_hessian = catalecticant(control)
    named_edges = (
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 5),
        (4, 6),
    )
    edge_index = {edge: index for index, edge in enumerate(EDGES)}
    indices = [edge_index[edge] for edge in named_edges]
    named_minor = control_hessian.extract(indices, indices)
    determinant = named_minor.det(method="domain-ge")
    assert determinant == 1_551_182_856_192
    assert sp.factorint(determinant) == {2: 18, 3: 6, 8117: 1}
    assert control_hessian.rank() == 20
    kernel_basis = sp.Matrix.hstack(*control_hessian.nullspace())
    assert kernel_basis.rank() == 8
    assert sp.Matrix.hstack(kernel_basis, vertex_edge).rank() == 8

    # Fixed exact linear-algebra replay of quotient reconstruction and gauge.
    quotient_basis = sp.Matrix.hstack(*vertex_edge.T.nullspace())
    assert quotient_basis.shape == (28, 20)
    quotient_hessian = quotient_basis.T * control_hessian * quotient_basis
    assert quotient_hessian.det() != 0

    coordinates = sp.Matrix([index - 9 for index in range(20)])
    gauge = sp.Matrix([2, -1, 3, 0, 4, -2, 1, 5])
    primitive_edge = quotient_basis * coordinates
    full_edge = primitive_edge + vertex_edge * gauge
    cofactor = control_hessian * full_edge / 3
    assert vertex_edge.T * cofactor == sp.zeros(8, 1)
    assert control_hessian * primitive_edge == control_hessian * full_edge

    compressed_cofactor = quotient_basis.T * cofactor
    recovered = 3 * quotient_hessian.inv() * compressed_cofactor
    assert recovered == coordinates
    top_scalar = (full_edge.T * cofactor)[0] / 4
    assert 4 * top_scalar == (primitive_edge.T * cofactor)[0]
    assert 4 * top_scalar == 3 * (
        compressed_cofactor.T * quotient_hessian.inv() * compressed_cofactor
    )[0]

    print("PASS: all 14 primitive polytabloids force the 8 incidence kernels")
    print("PASS: R^T R = 6I+J and primitive edge quotient has dimension 20")
    print("PASS: six-hafnian cofactor has eight zero vertex row sums")
    print("PASS: named rank-20 minor = 2^18*3^6*8117")
    print("PASS: quotient reconstruction, additive gauge, and scalar stress")
    print("searches=0 finite_fields=0 graph_enumerations=0")
    print("SCOPE: rank-20 control is not asserted to be a physical square")
    print("SCOPE: primitive-square quotient-open incidence remains UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
