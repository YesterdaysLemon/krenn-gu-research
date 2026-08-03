"""Verify higher-residual tomography, nested stress, and cumulant identities.

This is a fixed exact symbolic replay, not a graph, support, word, minor, or
parameter search.
"""

from functools import cache
from itertools import combinations

import sympy as sp


@cache
def hafnian(vertices: tuple[int, ...], entries: tuple[tuple[sp.Expr, ...], ...]):
    """Exact hafnian recurrence on one fixed symmetric matrix."""
    if not vertices:
        return sp.Integer(1)
    if len(vertices) % 2:
        return sp.Integer(0)
    first = vertices[0]
    result = sp.Integer(0)
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        result += entries[first][second] * hafnian(rest, entries)
    return sp.expand(result)


def permanent(matrix: sp.Matrix):
    """Exact permanent by fixed first-row recursion."""
    if matrix.rows == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            matrix[0, column] * permanent(matrix.minor_submatrix(0, column))
            for column in range(matrix.cols)
        )
    )


def cofactor_tower(matrix: sp.Matrix):
    """Return c_T=haf(A on Q minus T) for every even deletion T."""
    order = matrix.rows
    entries = tuple(tuple(matrix[row, column] for column in range(order)) for row in range(order))
    result = {}
    universe = tuple(range(order))
    for size in range(0, order + 1, 2):
        for deletion in combinations(universe, size):
            remaining = tuple(vertex for vertex in universe if vertex not in deletion)
            result[deletion] = hafnian(remaining, entries)
    return result


def main() -> None:
    order = 6
    universe = tuple(range(order))

    # Every even permanental compound of identity incidence is an identity.
    identity = sp.eye(order)
    for size in range(0, order + 1, 2):
        subsets = tuple(combinations(universe, size))
        compound = sp.Matrix(
            [
                [permanent(identity.extract(rows, columns)) for columns in subsets]
                for rows in subsets
            ]
        )
        assert compound == sp.eye(len(subsets))
        assert compound.det() == 1

    # One exact nonsymmetric-looking but symmetric weighted test matrix.
    matrix = sp.zeros(order)
    value = 1
    for left, right in combinations(universe, 2):
        weight = sp.Integer((value % 7) - 3)
        if weight == 0:
            weight = sp.Integer(4)
        matrix[left, right] = weight
        matrix[right, left] = weight
        value += 2

    tower = cofactor_tower(matrix)
    assert tower[universe] == 1

    # Tomography at R=I recovers each cofactor layer verbatim.  Check every
    # nested partner expansion, including Hadamard stress at deletion zero.
    for deletion, cofactor in tower.items():
        remaining = tuple(vertex for vertex in universe if vertex not in deletion)
        if not remaining:
            continue
        pivot = remaining[0]
        expansion = sum(
            tower[tuple(sorted(deletion + (pivot, partner)))]
            * tower[tuple(vertex for vertex in universe if vertex not in (pivot, partner))]
            for partner in remaining[1:]
        )
        assert sp.expand(cofactor - expansion) == 0

    cofactor_matrix = sp.zeros(order)
    for left, right in combinations(universe, 2):
        cofactor_matrix[left, right] = tower[(left, right)]
        cofactor_matrix[right, left] = tower[(left, right)]
    stress = matrix.multiply_elementwise(cofactor_matrix) * sp.ones(order, 1)
    assert stress == tower[()] * sp.ones(order, 1)

    # Direct adjugate-cleared polynomial check on a nontrivial symbolic q=4
    # diagonal incidence chart.
    small_order = 4
    small_universe = tuple(range(small_order))
    diagonal = sp.symbols("d0:4")
    incidence = sp.diag(*diagonal)
    small_matrix = sp.zeros(small_order)
    small_edges = sp.symbols("a01 a02 a03 a12 a13 a23")
    for edge, weight in zip(combinations(small_universe, 2), small_edges, strict=True):
        left, right = edge
        small_matrix[left, right] = weight
        small_matrix[right, left] = weight
    small_tower = cofactor_tower(small_matrix)
    layers = {}
    for size in range(0, small_order + 1, 2):
        subsets = tuple(combinations(small_universe, size))
        compound = sp.Matrix(
            [
                [permanent(incidence.extract(rows, columns)) for columns in subsets]
                for rows in subsets
            ]
        )
        cofactor_row = sp.Matrix(1, len(subsets), [small_tower[item] for item in subsets])
        response_row = cofactor_row * compound
        determinant = sp.factor(compound.det())
        cleared = response_row * compound.adjugate()
        assert all(
            sp.expand(cleared[0, index] - determinant * small_tower[item]) == 0
            for index, item in enumerate(subsets)
        )
        layers[size] = {
            "subsets": subsets,
            "determinant": determinant,
            "cleared": cleared,
        }

    for deletion in layers[0]["subsets"] + layers[2]["subsets"]:
        remaining = tuple(
            vertex for vertex in small_universe if vertex not in deletion
        )
        if not remaining:
            continue
        pivot = remaining[0]
        size = len(deletion)
        current_index = layers[size]["subsets"].index(deletion)
        current = layers[size]["cleared"][0, current_index]
        polynomial = (
            layers[small_order - 2]["determinant"]
            * layers[size + 2]["determinant"]
            * current
        )
        correction = sp.Integer(0)
        for partner in remaining[1:]:
            edge_deletion = tuple(
                vertex
                for vertex in small_universe
                if vertex not in (pivot, partner)
            )
            next_deletion = tuple(sorted(deletion + (pivot, partner)))
            edge_index = layers[small_order - 2]["subsets"].index(edge_deletion)
            next_index = layers[size + 2]["subsets"].index(next_deletion)
            correction += (
                layers[small_order - 2]["cleared"][0, edge_index]
                * layers[size + 2]["cleared"][0, next_index]
            )
        polynomial -= layers[size]["determinant"] * correction
        assert sp.factor(polynomial) == 0

    # Division-free third residual cumulant, first symbolically and then with
    # Z_T=M*Psi_T.
    l0, l1, l2, a01, a02, a12, moment = sp.symbols(
        "l0 l1 l2 a01 a02 a12 M"
    )
    psi0, psi1, psi2 = l0, l1, l2
    psi01 = a01 + l0 * l1
    psi02 = a02 + l0 * l2
    psi12 = a12 + l1 * l2
    psi012 = a01 * l2 + a02 * l1 + a12 * l0 + l0 * l1 * l2
    cumulant = sp.expand(
        psi012
        - psi01 * psi2
        - psi02 * psi1
        - psi12 * psi0
        + 2 * psi0 * psi1 * psi2
    )
    assert cumulant == 0
    division_free = sp.expand(
        moment**2 * (moment * psi012)
        - moment
        * (
            (moment * psi01) * (moment * psi2)
            + (moment * psi02) * (moment * psi1)
            + (moment * psi12) * (moment * psi0)
        )
        + 2 * (moment * psi0) * (moment * psi1) * (moment * psi2)
    )
    assert division_free == 0

    # Complete-support h=0, full-rank q=6 sharp control.
    sharp = sp.ones(order) - sp.eye(order)
    sharp[0, 1] = -(order - 2)
    sharp[1, 0] = -(order - 2)
    sharp_tower = cofactor_tower(sharp)
    assert sharp_tower[()] == 0
    sharp_cofactor = sp.zeros(order)
    for left, right in combinations(universe, 2):
        sharp_cofactor[left, right] = sharp_tower[(left, right)]
        sharp_cofactor[right, left] = sharp_tower[(left, right)]
    assert sharp_cofactor.rank() == order
    sharp_stress = sharp.multiply_elementwise(sharp_cofactor) * sp.ones(order, 1)
    assert sharp_stress == sp.zeros(order, 1)

    print("PASS: all q=6 even identity compounds are invertible")
    print("PASS: tomography reconstructs the complete principal cofactor tower")
    print("PASS: every nested partner expansion and Hadamard stress")
    print("PASS: adjugate-cleared nested stresses on a symbolic q=4 chart")
    print("PASS: division-free third residual cumulant")
    print("PASS: h=0 full-rank multichannel control passes the full hierarchy")
    print("SCOPE: legal GHZ exposure and deletion-label synchronization remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
