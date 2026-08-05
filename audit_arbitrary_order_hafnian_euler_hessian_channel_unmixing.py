"""Independent no-import audit of hafnian Euler--Hessian unmixing."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations

Edge = tuple[int, int]
Monomial = frozenset[int]
Polynomial = dict[Monomial, Fraction]


def edges(q: int) -> tuple[Edge, ...]:
    return tuple(combinations(range(q), 2))


def matching_monomials(
    active: tuple[int, ...], edge_index: dict[Edge, int]
) -> tuple[Monomial, ...]:
    @cache
    def visit(vertices: tuple[int, ...]) -> tuple[Monomial, ...]:
        if not vertices:
            return (frozenset(),)
        first = vertices[0]
        answer: list[Monomial] = []
        for offset, partner in enumerate(vertices[1:], start=1):
            edge = tuple(sorted((first, partner)))
            remainder = vertices[1:offset] + vertices[offset + 1 :]
            for monomial in visit(remainder):
                answer.append(monomial | {edge_index[edge]})
        return tuple(answer)

    return visit(tuple(sorted(active)))


def evaluate_polynomial(
    polynomial: Polynomial,
    weight_vector: list[Fraction],
    derivatives: tuple[int, ...] = (),
) -> Fraction:
    if len(set(derivatives)) != len(derivatives):
        return Fraction(0)
    derivative_set = set(derivatives)
    total = Fraction(0)
    for monomial, coefficient in polynomial.items():
        if not derivative_set.issubset(monomial):
            continue
        value = coefficient
        for edge in monomial - derivative_set:
            value *= weight_vector[edge]
        total += value
    return total


def response_polynomials(
    q: int,
    direct: list[Fraction],
    channels: list[list[Fraction]],
) -> list[Polynomial]:
    edge_order = edges(q)
    edge_index = {edge: index for index, edge in enumerate(edge_order)}
    vertices = tuple(range(q))
    h_terms = matching_monomials(vertices, edge_index)
    c_terms = [
        matching_monomials(
            tuple(vertex for vertex in vertices if vertex not in edge), edge_index
        )
        for edge in edge_order
    ]
    response: list[Polynomial] = []
    for coordinate, direct_value in enumerate(direct):
        polynomial: Polynomial = {}
        for monomial in h_terms:
            polynomial[monomial] = polynomial.get(monomial, Fraction(0)) + direct_value
        for edge, terms in enumerate(c_terms):
            for monomial in terms:
                polynomial[monomial] = polynomial.get(
                    monomial, Fraction(0)
                ) + channels[edge][coordinate]
        response.append(
            {monomial: value for monomial, value in polynomial.items() if value}
        )
    return response


def hafnian_value(
    active: tuple[int, ...],
    weight: dict[Edge, Fraction],
) -> Fraction:
    @cache
    def visit(vertices: tuple[int, ...]) -> Fraction:
        if not vertices:
            return Fraction(1)
        first = vertices[0]
        total = Fraction(0)
        for offset, partner in enumerate(vertices[1:], start=1):
            remainder = vertices[1:offset] + vertices[offset + 1 :]
            total += weight[tuple(sorted((first, partner)))] * visit(remainder)
        return total

    return visit(tuple(sorted(active)))


def hafnian_jet(
    q: int, weight: dict[Edge, Fraction]
) -> tuple[Fraction, list[Fraction], list[list[Fraction]], list[list[list[Fraction]]]]:
    edge_order = edges(q)
    vertices = tuple(range(q))
    h_value = hafnian_value(vertices, weight)
    c_vector = [
        hafnian_value(tuple(v for v in vertices if v not in edge), weight)
        for edge in edge_order
    ]
    size = len(edge_order)
    d_matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    j_tensor = [
        [[Fraction(0) for _ in range(size)] for _ in range(size)]
        for _ in range(size)
    ]
    for row, edge in enumerate(edge_order):
        for column, other in enumerate(edge_order):
            if not set(edge).isdisjoint(other):
                continue
            deleted = set(edge + other)
            d_matrix[row][column] = hafnian_value(
                tuple(v for v in vertices if v not in deleted), weight
            )
            for third, last in enumerate(edge_order):
                if deleted.isdisjoint(last):
                    all_deleted = deleted | set(last)
                    j_tensor[third][row][column] = hafnian_value(
                        tuple(v for v in vertices if v not in all_deleted), weight
                    )
    return h_value, c_vector, d_matrix, j_tensor


def matmul(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [
            sum(
                (left[row][middle] * right[middle][column] for middle in range(len(right))),
                Fraction(0),
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [
        sum((entry * value for entry, value in zip(row, vector, strict=True)), Fraction(0))
        for row in matrix
    ]


def inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    size = len(matrix)
    work = [
        [Fraction(value) for value in row_values]
        + [Fraction(int(row_index == column)) for column in range(size)]
        for row_index, row_values in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        pivot_value = work[column][column]
        work[column] = [value / pivot_value for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    value - factor * pivot_entry
                    for value, pivot_entry in zip(
                        work[row], work[column], strict=True
                    )
                ]
    return [row[size:] for row in work]


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    value - factor * pivot_entry
                    for value, pivot_entry in zip(work[row], work[rank], strict=True)
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def kernel_vector(matrix: list[list[Fraction]]) -> list[Fraction]:
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    value - factor * pivot_entry
                    for value, pivot_entry in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free_columns = [column for column in range(columns) if column not in pivot_columns]
    assert len(free_columns) == 1
    free = free_columns[0]
    vector = [Fraction(0) for _ in range(columns)]
    vector[free] = Fraction(1)
    for row, pivot in enumerate(pivot_columns):
        vector[pivot] = -work[row][free]
    assert matvec(matrix, vector) == [Fraction(0)] * rows
    return vector


def contract_third(
    third: list[list[list[Fraction]]], vector: list[Fraction]
) -> list[list[Fraction]]:
    size = len(third)
    return [
        [
            sum(
                (third[index][row][column] * vector[index] for index in range(size)),
                Fraction(0),
            )
            for column in range(size)
        ]
        for row in range(size)
    ]


def subtract_matrices(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [a - b for a, b in zip(left_row, right_row, strict=True)]
        for left_row, right_row in zip(left, right, strict=True)
    ]


def response_jet_from_polynomials(
    polynomials: list[Polynomial], weight_vector: list[Fraction]
) -> tuple[list[Fraction], list[list[Fraction]], list[list[list[Fraction]]]]:
    size = len(weight_vector)
    values = [evaluate_polynomial(polynomial, weight_vector) for polynomial in polynomials]
    gradients = [
        [
            evaluate_polynomial(polynomial, weight_vector, (edge,))
            for polynomial in polynomials
        ]
        for edge in range(size)
    ]
    hessians = [
        [
            [
                evaluate_polynomial(polynomial, weight_vector, (row, column))
                for column in range(size)
            ]
            for row in range(size)
        ]
        for polynomial in polynomials
    ]
    return values, gradients, hessians


def audit_open_six_vertex_response() -> None:
    q = 6
    m = q // 2
    edge_order = edges(q)
    size = len(edge_order)
    direct = [Fraction(2), Fraction(-3)]
    channels = [
        [Fraction(index + 1), Fraction((-1) ** index * (index + 2))]
        for index in range(size)
    ]
    polynomials = response_polynomials(q, direct, channels)
    weight = {
        edge: Fraction(2 + (edge[0] + 1) * (edge[1] + 1)) for edge in edge_order
    }
    weight_vector = [weight[edge] for edge in edge_order]
    h_value, c_vector, d_matrix, third = hafnian_jet(q, weight)
    values, gradients, response_hessians = response_jet_from_polynomials(
        polynomials, weight_vector
    )
    d_inverse = inverse(d_matrix)

    for coordinate in range(len(direct)):
        channel = [row[coordinate] for row in channels]
        expected_gradient = [
            c_vector[row] * direct[coordinate] + value
            for row, value in enumerate(matvec(d_matrix, channel))
        ]
        gradient = [row[coordinate] for row in gradients]
        assert gradient == expected_gradient
        expected_hessian = [
            [
                d_matrix[row][column] * direct[coordinate] + correction
                for column, correction in enumerate(correction_row)
            ]
            for row, correction_row in enumerate(contract_third(third, channel))
        ]
        assert response_hessians[coordinate] == expected_hessian

        t_tilde = matvec(d_inverse, gradient)
        s_matrix = subtract_matrices(
            response_hessians[coordinate], contract_third(third, t_tilde)
        )
        normalized = matmul(d_inverse, s_matrix)
        recovered_u = (m - 1) * sum(
            (normalized[index][index] for index in range(size)), Fraction(0)
        ) / size
        assert recovered_u == direct[coordinate]
        assert normalized == [
            [
                recovered_u / (m - 1) if row == column else Fraction(0)
                for column in range(size)
            ]
            for row in range(size)
        ]
        recovered_channel = [
            t_tilde[index] - weight_vector[index] * recovered_u / (m - 1)
            for index in range(size)
        ]
        assert recovered_channel == channel

        first_recovered_u = (m - 1) * (
            sum(
                (
                    c_vector[index] * t_tilde[index]
                    for index in range(size)
                ),
                Fraction(0),
            )
            - values[coordinate]
        ) / h_value
        assert first_recovered_u == direct[coordinate]


def audit_zero_hafnian_gauge() -> None:
    q = 4
    m = q // 2
    edge_order = edges(q)
    direct = [Fraction(3), Fraction(-4)]
    channels = [
        [Fraction(index + 2), Fraction(2 * index - 3)]
        for index in range(len(edge_order))
    ]
    polynomials = response_polynomials(q, direct, channels)
    assigned = [1, 1, 1, -2, 1, 1]
    weight_vector = [Fraction(value) for value in assigned]
    weight = dict(zip(edge_order, weight_vector, strict=True))
    h_value, c_vector, d_matrix, third = hafnian_jet(q, weight)
    values, gradients, response_hessians = response_jet_from_polynomials(
        polynomials, weight_vector
    )
    d_inverse = inverse(d_matrix)
    assert h_value == 0
    assert all(weight_vector)

    for coordinate in range(len(direct)):
        gradient = [row[coordinate] for row in gradients]
        t_tilde = matvec(d_inverse, gradient)
        assert values[coordinate] == sum(
            (c_vector[index] * t_tilde[index] for index in range(len(edge_order))),
            Fraction(0),
        )

    gauge = [Fraction(5), Fraction(-7)]
    shifted_direct = [
        direct[coordinate] - (m - 1) * gauge[coordinate]
        for coordinate in range(len(direct))
    ]
    shifted_channels = [
        [
            channels[edge][coordinate] + weight_vector[edge] * gauge[coordinate]
            for coordinate in range(len(direct))
        ]
        for edge in range(len(edge_order))
    ]
    for coordinate in range(len(direct)):
        shifted_value = h_value * shifted_direct[coordinate] + sum(
            (
                c_vector[edge] * shifted_channels[edge][coordinate]
                for edge in range(len(edge_order))
            ),
            Fraction(0),
        )
        shifted_gradient = [
            c_vector[row] * shifted_direct[coordinate] + value
            for row, value in enumerate(
                matvec(
                    d_matrix,
                    [row[coordinate] for row in shifted_channels],
                )
            )
        ]
        assert shifted_value == values[coordinate]
        assert shifted_gradient == [row[coordinate] for row in gradients]

        t_tilde = matvec(d_inverse, [row[coordinate] for row in gradients])
        s_matrix = subtract_matrices(
            response_hessians[coordinate], contract_third(third, t_tilde)
        )
        normalized = matmul(d_inverse, s_matrix)
        recovered_u = (m - 1) * sum(
            (normalized[index][index] for index in range(len(edge_order))),
            Fraction(0),
        ) / len(edge_order)
        assert recovered_u == direct[coordinate]


def audit_full_torus_singular_kernel() -> None:
    q = 6
    edge_order = edges(q)
    left = {0, 1, 2}
    weight: dict[Edge, Fraction] = {}
    for edge in edge_order:
        if edge[0] in left and edge[1] in left:
            weight[edge] = Fraction(1)
        elif edge[0] not in left and edge[1] not in left:
            weight[edge] = Fraction(2)
        else:
            weight[edge] = Fraction(1)
    h_value, c_vector, d_matrix, _ = hafnian_jet(q, weight)
    assert h_value == 24
    assert all(weight.values())
    assert matrix_rank(d_matrix) == len(edge_order) - 1
    kernel = kernel_vector(d_matrix)

    direct = [Fraction(2), Fraction(-3)]
    channels = [
        [Fraction(index + 1), Fraction((-1) ** index * (index + 2))]
        for index in range(len(edge_order))
    ]
    gradients = [
        [
            c_vector[row] * direct[coordinate]
            + matvec(
                d_matrix, [channel[coordinate] for channel in channels]
            )[row]
            for coordinate in range(len(direct))
        ]
        for row in range(len(edge_order))
    ]
    for coordinate in range(len(direct)):
        gradient = [row[coordinate] for row in gradients]
        assert sum(
            (kernel[index] * gradient[index] for index in range(len(edge_order))),
            Fraction(0),
        ) == 0

    bad_gradient = [row[0] + kernel[index] for index, row in enumerate(gradients)]
    assert sum(
        (kernel[index] * bad_gradient[index] for index in range(len(edge_order))),
        Fraction(0),
    ) != 0


def audit_support_arithmetic() -> None:
    assert [(roots, 3 * (roots + 2) + 3) for roots in (3, 4, 5)] == [
        (3, 18),
        (4, 21),
        (5, 24),
    ]


def main() -> None:
    audit_open_six_vertex_response()
    audit_zero_hafnian_gauge()
    audit_full_torus_singular_kernel()
    audit_support_arithmetic()
    print("independent hafnian Euler-Hessian channel audit: PASS")
    print("matching-monomial q=6 response and both inversions: exact")
    print("full-torus q=4 h=0 gauge and second-jet recovery: exact")
    print("full-torus q=6 corank-one kernel discriminant: exact")
    print("conditional support staircase 18/21/24: exact")
    print("legal response-edge jet exposure: UNKNOWN")
    print("global Krenn-Gu: UNRESOLVED")


if __name__ == "__main__":
    main()
