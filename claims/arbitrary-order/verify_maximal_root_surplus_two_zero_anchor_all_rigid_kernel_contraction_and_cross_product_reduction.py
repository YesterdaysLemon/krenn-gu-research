"""Focused exact checks for GLS58.

The written proof carries the characteristic-zero complete-witness theorem.
This verifier uses exact integer/rational tensors to check the one- and
two-kernel matching reconstructions coefficientwise, the boundary covector
alternative, the binary six-vertex endpoint, and the injective cross-product
boundary.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import combinations, product

import sympy as sp

Vector = tuple[Fraction, Fraction, Fraction]
Matrix = tuple[tuple[Fraction, Fraction, Fraction], ...]
Matching = tuple[tuple[int, int], ...]

ZERO_VECTOR: Vector = (Fraction(0), Fraction(0), Fraction(0))
ZERO_MATRIX: Matrix = (ZERO_VECTOR, ZERO_VECTOR, ZERO_VECTOR)


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[Matching] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[row][column] for row in range(3))
        for column in range(3)
    )


def matrix_add(*matrices: Matrix) -> Matrix:
    return tuple(
        tuple(sum(matrix[row][column] for matrix in matrices) for column in range(3))
        for row in range(3)
    )


def matrix_scale(value: Fraction, matrix: Matrix) -> Matrix:
    return tuple(
        tuple(value * entry for entry in row)
        for row in matrix
    )


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(x * y for y in right) for x in left)


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def left_contract(vector: Vector, matrix: Matrix) -> Vector:
    return tuple(
        sum(vector[row] * matrix[row][column] for row in range(3))
        for column in range(3)
    )  # type: ignore[return-value]


def bilinear(left: Vector, matrix: Matrix, right: Vector) -> Fraction:
    return sum(x * y for x, y in zip(left, matvec(matrix, right), strict=True))


def basis(colour: int) -> Vector:
    return tuple(Fraction(int(index == colour)) for index in range(3))  # type: ignore[return-value]


def edge_matrix(
    edges: dict[tuple[int, int], Matrix], left: int, right: int
) -> Matrix:
    if left < right:
        return edges.get((left, right), ZERO_MATRIX)
    return transpose(edges.get((right, left), ZERO_MATRIX))


def matching_coefficient(
    vertices: tuple[int, ...],
    local_vectors: dict[int, Vector],
    edges: dict[tuple[int, int], Matrix],
) -> Fraction:
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        value = Fraction(1)
        for left, right in matching:
            value *= bilinear(
                local_vectors[left],
                edge_matrix(edges, left, right),
                local_vectors[right],
            )
        total += value
    return total


def sparse_matching_tensor(
    vertices: tuple[int, ...], edges: dict[tuple[int, int], Matrix]
) -> Counter[tuple[int, ...]]:
    coefficients: Counter[tuple[int, ...]] = Counter()
    position = {vertex: index for index, vertex in enumerate(vertices)}
    for matching in perfect_matchings(vertices):
        edge_entries: list[tuple[tuple[int, int, Fraction], ...]] = []
        for left, right in matching:
            matrix = edge_matrix(edges, left, right)
            entries = tuple(
                (row, column, matrix[row][column])
                for row in range(3)
                for column in range(3)
                if matrix[row][column]
            )
            if not entries:
                break
            edge_entries.append(entries)
        else:
            for choices in product(*edge_entries):
                word = [-1] * len(vertices)
                value = Fraction(1)
                for (left, right), (left_colour, right_colour, entry) in zip(
                    matching, choices, strict=True
                ):
                    word[position[left]] = left_colour
                    word[position[right]] = right_colour
                    value *= entry
                coefficients[tuple(word)] += value
    return +coefficients


def deterministic_matrix(seed: int) -> Matrix:
    values = tuple(Fraction(((seed + 3 * index) % 11) - 5) for index in range(9))
    return tuple(tuple(values[3 * row + column] for column in range(3)) for row in range(3))


def dense_graph_edges() -> tuple[dict[tuple[int, int], Matrix], Vector, Vector]:
    # Vertices: A=(0,1), deficient labels n=2,t=3, and R=(4,5,6,7).
    vertices = tuple(range(8))
    k = (Fraction(1), Fraction(1), Fraction(0))
    ell = (Fraction(1), Fraction(0), Fraction(1))
    edges: dict[tuple[int, int], Matrix] = {}
    seed = 1
    for left, right in combinations(vertices, 2):
        if (left, right) == (0, 1):
            edges[(left, right)] = ZERO_MATRIX
        else:
            edges[(left, right)] = deterministic_matrix(seed)
        seed += 1

    # Make k and ell full joint-kernel vectors at n and t respectively.
    k_rows: Matrix = (
        (Fraction(1), Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
        ZERO_VECTOR,
    )
    ell_rows: Matrix = (
        (Fraction(1), Fraction(0), Fraction(-1)),
        (Fraction(0), Fraction(1), Fraction(0)),
        ZERO_VECTOR,
    )
    edges[(0, 2)] = k_rows
    edges[(1, 2)] = ZERO_MATRIX
    edges[(0, 3)] = ell_rows
    edges[(1, 3)] = ZERO_MATRIX
    assert matvec(edges[(0, 2)], k) == ZERO_VECTOR
    assert matvec(edges[(1, 2)], k) == ZERO_VECTOR
    assert matvec(edges[(0, 3)], ell) == ZERO_VECTOR
    assert matvec(edges[(1, 3)], ell) == ZERO_VECTOR
    return edges, k, ell


def audit_boundary_covector_alternative() -> dict[str, int]:
    prime = 5
    vectors = tuple(product(range(prime), repeat=3))
    cases = 0
    pure_obstructions = 0
    witnesses = 0
    for colour in range(3):
        for covector in vectors:
            cases += 1
            admissible = [
                vector
                for vector in vectors
                if sum(covector[index] * vector[index] for index in range(3)) % prime == 0
                and vector[colour] % prime
            ]
            is_nonzero_pure = (
                covector[colour] % prime != 0
                and all(
                    covector[index] % prime == 0
                    for index in range(3)
                    if index != colour
                )
            )
            assert bool(admissible) != is_nonzero_pure
            pure_obstructions += int(is_nonzero_pure)
            witnesses += len(admissible)

    assert cases == 3 * 5**3
    assert pure_obstructions == 3 * 4
    assert witnesses == 7500
    return {
        "F5_covector_colour_cases": cases,
        "F5_nonzero_pure_obstructions": pure_obstructions,
        "F5_kernel_coordinate_witnesses": witnesses,
    }


def audit_one_kernel_ten_deck_identity() -> dict[str, int]:
    edges, k, _ = dense_graph_edges()
    vertices = tuple(range(8))
    n = 2
    open_vertices = (0, 1, 3, 4, 5, 6, 7)
    auxiliary_remainder = (3, 4, 5, 6, 7)
    checked = 0

    for word in product(range(3), repeat=len(open_vertices)):
        local = {vertex: basis(colour) for vertex, colour in zip(open_vertices, word, strict=True)}
        local[n] = k
        direct = matching_coefficient(vertices, local, edges)

        reconstructed = Fraction(0)
        for left, right in combinations(auxiliary_remainder, 2):
            companion = (
                bilinear(local[0], edge_matrix(edges, 0, left), local[left])
                * bilinear(local[1], edge_matrix(edges, 1, right), local[right])
                + bilinear(local[0], edge_matrix(edges, 0, right), local[right])
                * bilinear(local[1], edge_matrix(edges, 1, left), local[left])
            )
            deck_vertices = tuple(
                vertex
                for vertex in auxiliary_remainder
                if vertex not in (left, right)
            )
            deck_local = {vertex: local[vertex] for vertex in deck_vertices}
            deck_local[n] = k
            # H_(Bhat-D)(k,-) lives on n plus the three remaining labels.
            deck = matching_coefficient((n,) + deck_vertices, deck_local, edges)
            reconstructed += companion * deck

        assert direct == reconstructed
        checked += 1

    assert checked == 3**7
    return {
        "one_kernel_coefficients_checked": checked,
        "one_kernel_pair_decks": 10,
    }


def build_descended_edges(
    edges: dict[tuple[int, int], Matrix], k: Vector, ell: Vector
) -> dict[tuple[int, int], Matrix]:
    descended: dict[tuple[int, int], Matrix] = {}
    retained = (0, 1, 4, 5, 6, 7)
    for left, right in combinations(retained, 2):
        if (left, right) == (0, 1):
            descended[(left, right)] = ZERO_MATRIX
        elif left < 2:
            descended[(left, right)] = edge_matrix(edges, left, right)
        else:
            h = bilinear(k, edge_matrix(edges, 2, 3), ell)
            a_left = left_contract(k, edge_matrix(edges, 2, left))
            a_right = left_contract(k, edge_matrix(edges, 2, right))
            b_left = left_contract(ell, edge_matrix(edges, 3, left))
            b_right = left_contract(ell, edge_matrix(edges, 3, right))
            descended[(left, right)] = matrix_add(
                matrix_scale(h, edge_matrix(edges, left, right)),
                outer(a_left, b_right),
                outer(b_left, a_right),
            )
    return descended


def audit_two_kernel_six_vertex_descent() -> dict[str, int]:
    edges, k, ell = dense_graph_edges()
    vertices = tuple(range(8))
    retained = (0, 1, 4, 5, 6, 7)
    descended = build_descended_edges(edges, k, ell)
    checked = 0

    for word in product(range(3), repeat=6):
        local = {vertex: basis(colour) for vertex, colour in zip(retained, word, strict=True)}
        original_local = dict(local)
        original_local[2] = k
        original_local[3] = ell
        direct = matching_coefficient(vertices, original_local, edges)
        reconstructed = matching_coefficient(retained, local, descended)
        assert direct == reconstructed
        checked += 1

    assert checked == 3**6
    return {
        "two_kernel_coefficients_checked": checked,
        "original_eight_vertex_matchings": len(perfect_matchings(vertices)),
        "descended_six_vertex_matchings": len(perfect_matchings(retained)),
    }


def diagonal_cell(colour: int, value: int = 1) -> Matrix:
    return tuple(
        tuple(
            Fraction(value if row == colour and column == colour else 0)
            for column in range(3)
        )
        for row in range(3)
    )


def integer_matrix(rows: tuple[tuple[int, int, int], ...]) -> Matrix:
    return tuple(tuple(Fraction(entry) for entry in row) for row in rows)


def audit_h_zero_all_rigid_binary_boundary() -> dict[str, int]:
    # Full eight-vertex lift: 0,1 are probes; 2,3 are deficient;
    # 4,5,6,7 are the retained ports 0,1,2,3.
    vertices = tuple(range(8))
    retained = (0, 1, 4, 5, 6, 7)
    boundary_kernel = (Fraction(1), Fraction(1), Fraction(0))
    deficient_probe_rows: Matrix = (
        (Fraction(1), Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
        ZERO_VECTOR,
    )
    raw_edges: dict[tuple[int, int], Matrix] = {
        (0, 1): ZERO_MATRIX,
        (0, 2): deficient_probe_rows,
        (1, 2): ZERO_MATRIX,
        (0, 3): deficient_probe_rows,
        (1, 3): ZERO_MATRIX,
        (2, 3): ZERO_MATRIX,
        (0, 4): diagonal_cell(0),
        (1, 5): diagonal_cell(0),
        (1, 6): diagonal_cell(1),
        (0, 7): diagonal_cell(1),
        (2, 4): outer(basis(0), basis(1)),
        (2, 6): outer(basis(0), basis(0)),
        (3, 5): outer(basis(0), basis(1)),
        (3, 7): outer(basis(0), basis(0)),
    }

    assert matvec(edge_matrix(raw_edges, 0, 2), boundary_kernel) == ZERO_VECTOR
    assert matvec(edge_matrix(raw_edges, 1, 2), boundary_kernel) == ZERO_VECTOR
    assert matvec(edge_matrix(raw_edges, 0, 3), boundary_kernel) == ZERO_VECTOR
    assert matvec(edge_matrix(raw_edges, 1, 3), boundary_kernel) == ZERO_VECTOR
    assert bilinear(
        boundary_kernel,
        edge_matrix(raw_edges, 2, 3),
        boundary_kernel,
    ) == 0

    expected_a = {4: basis(1), 5: ZERO_VECTOR, 6: basis(0), 7: ZERO_VECTOR}
    expected_b = {4: ZERO_VECTOR, 5: basis(1), 6: ZERO_VECTOR, 7: basis(0)}
    for port in (4, 5, 6, 7):
        assert left_contract(
            boundary_kernel, edge_matrix(raw_edges, 2, port)
        ) == expected_a[port]
        assert left_contract(
            boundary_kernel, edge_matrix(raw_edges, 3, port)
        ) == expected_b[port]

    descended = build_descended_edges(raw_edges, boundary_kernel, boundary_kernel)
    expected_descended: dict[tuple[int, int], Matrix] = {
        (0, 4): diagonal_cell(0),
        (1, 5): diagonal_cell(0),
        (1, 6): diagonal_cell(1),
        (0, 7): diagonal_cell(1),
        (4, 5): diagonal_cell(1),
        (6, 7): diagonal_cell(0),
        (4, 7): outer(basis(1), basis(0)),
        (5, 6): outer(basis(1), basis(0)),
    }
    assert all(
        edge_matrix(descended, left, right)
        == edge_matrix(expected_descended, left, right)
        for left, right in combinations(retained, 2)
    )

    checked = 0
    for word in product(range(3), repeat=6):
        local = {
            vertex: basis(colour)
            for vertex, colour in zip(retained, word, strict=True)
        }
        full_local = dict(local)
        full_local[2] = boundary_kernel
        full_local[3] = boundary_kernel
        assert matching_coefficient(vertices, full_local, raw_edges) == matching_coefficient(
            retained, local, descended
        )
        checked += 1

    coefficients = sparse_matching_tensor(retained, descended)
    assert coefficients == Counter({(0,) * 6: 1, (1,) * 6: 1})

    expected_ranks = {2: 2, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1}
    rigid_colours = {2: 2, 3: 2, 4: 0, 5: 0, 6: 1, 7: 1}
    for label in range(2, 8):
        rows = tuple(
            edge_matrix(raw_edges, probe, label)[root_colour]
            for probe in (0, 1)
            for root_colour in range(3)
        )
        row_matrix = sp.Matrix(rows)
        assert row_matrix.rank() == expected_ranks[label]
        assert sp.Matrix(rows + (basis(rigid_colours[label]),)).rank() == row_matrix.rank()

    assert checked == 3**6
    return {
        "h_zero_binary_full_lift_edges": len(raw_edges),
        "h_zero_binary_contracted_coefficients": checked,
        "h_zero_binary_effective_edges": len(expected_descended),
        "h_zero_binary_nonzero_words": len(coefficients),
        "h_zero_binary_rigid_retained_ports": 4,
        "h_zero_binary_rigid_deficient_labels": 2,
    }


def sympy_matrix(rows: tuple[tuple[int, int, int], ...]) -> sp.Matrix:
    return sp.Matrix(rows)


def audit_injective_cross_product_boundary() -> dict[str, int]:
    z_0 = sp.Matrix(sp.symbols("z00 z01 z02"))
    z_1 = sp.Matrix(sp.symbols("z10 z11 z12"))
    permutation = sympy_matrix(((0, 0, 1), (1, 0, 0), (0, 1, 0)))
    additions = (
        sympy_matrix(((1, 0, 0), (0, 0, 0), (0, 0, 0))),
        sympy_matrix(((0, 0, 0), (0, 1, 0), (0, 0, 0))),
        sp.zeros(3),
        sympy_matrix(((0, 0, 0), (0, 0, 0), (0, 0, 1))),
        sp.zeros(3),
        sp.zeros(3),
    )
    y_cells = ((2, 2), (0, 1), (0, 0), (0, 2), (1, 1), (0, 1))
    vanished_coordinates = (2, None, 0, None, 1, None)
    crosses: list[sp.Matrix] = []

    for addition, (row, column), vanished in zip(
        additions, y_cells, vanished_coordinates, strict=True
    ):
        x_matrix = permutation + addition
        y_matrix = sp.zeros(3)
        y_matrix[row, column] = 1
        assert x_matrix.det() == 1
        a = x_matrix.T * z_0
        b = y_matrix.T * z_1
        cross = a.cross(b)
        assert sp.expand(a.dot(cross)) == 0
        assert sp.expand(b.dot(cross)) == 0
        assert any(sp.expand(entry) != 0 for entry in cross)
        if vanished is not None:
            assert sp.expand(cross[vanished]) == 0
        crosses.append(cross)

    products = [
        sp.prod(crosses[label][colour] for label in range(6))
        for colour in range(3)
    ]
    assert all(sp.expand(value) == 0 for value in products)
    cross_identity = sum(z_0[colour] * z_1[colour] * products[colour] for colour in range(3))
    assert sp.expand(cross_identity) == 0
    return {
        "injective_joint_maps": 6,
        "nonzero_cross_polynomials": 6,
        "termwise_zero_colour_products": 3,
    }


def audit_injective_physical_control() -> dict[str, int]:
    # Exact same-graph control for the termwise cross-product boundary.  It
    # has the three required pure coefficients but many mixed coefficients,
    # so it is not a witness.
    vertices = tuple(range(8))
    labels = (2, 3, 4, 5, 6, 7)  # q0,q1,u0,u1,u2,u3
    permutation = integer_matrix(((0, 0, 1), (1, 0, 0), (0, 1, 0)))
    additions = (
        diagonal_cell(0),
        diagonal_cell(1),
        ZERO_MATRIX,
        diagonal_cell(2),
        ZERO_MATRIX,
        ZERO_MATRIX,
    )
    y_cells = ((2, 2), (0, 1), (0, 0), (0, 2), (1, 1), (0, 1))
    edges: dict[tuple[int, int], Matrix] = {(0, 1): ZERO_MATRIX}
    for label, addition, (row, column) in zip(
        labels, additions, y_cells, strict=True
    ):
        edges[(0, label)] = matrix_add(permutation, addition)
        y_edge = [list(row_values) for row_values in ZERO_MATRIX]
        y_edge[row][column] = Fraction(1)
        edges[(1, label)] = tuple(tuple(values) for values in y_edge)

    edges[(3, 7)] = matrix_add(diagonal_cell(0), diagonal_cell(2))
    edges[(5, 6)] = diagonal_cell(0)
    edges[(2, 7)] = diagonal_cell(1)
    edges[(4, 5)] = diagonal_cell(1)
    edges[(4, 6)] = diagonal_cell(2)

    coefficients = sparse_matching_tensor(vertices, edges)

    pure = tuple(coefficients[(colour,) * 8] for colour in range(3))
    mixed = {word: value for word, value in coefficients.items() if len(set(word)) > 1}
    assert pure == (1, 1, 1)
    assert len(coefficients) == 64
    assert len(mixed) == 61
    assert max(coefficients.values()) == 2
    assert sum(coefficients.values()) == 66
    return {
        "injective_control_supported_words": len(coefficients),
        "injective_control_mixed_words": len(mixed),
        "injective_control_coloured_matching_terms": int(sum(coefficients.values())),
    }


def main() -> None:
    summary: dict[str, int] = {}
    summary.update(audit_boundary_covector_alternative())
    summary.update(audit_one_kernel_ten_deck_identity())
    summary.update(audit_two_kernel_six_vertex_descent())
    summary.update(audit_h_zero_all_rigid_binary_boundary())
    summary.update(audit_injective_cross_product_boundary())
    summary.update(audit_injective_physical_control())
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("GLS58 focused exact verifier: PASS")


if __name__ == "__main__":
    main()
