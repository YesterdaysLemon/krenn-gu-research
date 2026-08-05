"""Independent no-import audit of the hafnian Hessian open-jet theorem."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations
from math import comb

Edge = tuple[int, int]


def edges(q: int) -> tuple[Edge, ...]:
    return tuple(combinations(range(q), 2))


def odd_double_factorial(n: int) -> int:
    if n == -1:
        return 1
    result = 1
    for value in range(1, n + 1, 2):
        result *= value
    return result


def hafnian(active: tuple[int, ...], weight: dict[Edge, int]) -> int:
    @cache
    def visit(vertices: tuple[int, ...]) -> int:
        if not vertices:
            return 1
        first = vertices[0]
        answer = 0
        for offset in range(1, len(vertices)):
            partner = vertices[offset]
            remainder = vertices[1:offset] + vertices[offset + 1 :]
            answer += weight[tuple(sorted((first, partner)))] * visit(remainder)
        return answer

    return visit(tuple(sorted(active)))


def bareiss_determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (
                row
                for row in range(pivot_index, size)
                if work[row][pivot_index] != 0
            ),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = (
                work[pivot_row],
                work[pivot_index],
            )
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
        for row in range(pivot_index + 1, size):
            work[row][pivot_index] = 0
        previous = pivot
    return sign * work[-1][-1]


def solve(matrix: list[list[int]], right: list[int]) -> list[Fraction]:
    size = len(matrix)
    augmented = [
        [Fraction(value) for value in row] + [Fraction(right[index])]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if augmented[row][column]
        )
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    value - factor * pivot_entry
                    for value, pivot_entry in zip(
                        augmented[row], augmented[column], strict=True
                    )
                ]
    return [augmented[row][-1] for row in range(size)]


def kneser(q: int, scale: int = 1) -> list[list[int]]:
    edge_order = edges(q)
    return [
        [scale * int(set(edge).isdisjoint(other)) for other in edge_order]
        for edge in edge_order
    ]


def multiply(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix]


def audit_kneser_chart() -> None:
    for q in (4, 6, 8):
        edge_order = edges(q)
        number_edges = len(edge_order)
        scale = odd_double_factorial(q - 5)
        matrix = kneser(q, scale)
        expected = (
            scale**number_edges
            * comb(q - 2, 2)
            * (-(q - 3)) ** (q - 1)
        )
        assert bareiss_determinant(matrix) == expected

        constant = [1] * number_edges
        assert multiply(matrix, constant) == [
            scale * comb(q - 2, 2)
        ] * number_edges

        vertex_weights = [1, -1, *([0] * (q - 2))]
        vertex_mode = [vertex_weights[i] + vertex_weights[j] for i, j in edge_order]
        assert multiply(matrix, vertex_mode) == [
            -scale * (q - 3) * value for value in vertex_mode
        ]

        four_cycle = {
            (0, 1): 1,
            (2, 3): 1,
            (0, 2): -1,
            (1, 3): -1,
        }
        cycle_mode = [four_cycle.get(edge, 0) for edge in edge_order]
        assert multiply(matrix, cycle_mode) == [scale * value for value in cycle_mode]


def build_integer_jet(
    q: int, weight: dict[Edge, int]
) -> tuple[int, list[int], list[list[int]]]:
    vertex_order = tuple(range(q))
    edge_order = edges(q)
    h_value = hafnian(vertex_order, weight)
    cofactors = [
        hafnian(tuple(v for v in vertex_order if v not in edge), weight)
        for edge in edge_order
    ]
    hessian: list[list[int]] = []
    for edge in edge_order:
        row: list[int] = []
        for other in edge_order:
            if set(edge).isdisjoint(other):
                deleted = set(edge + other)
                row.append(
                    hafnian(
                        tuple(v for v in vertex_order if v not in deleted), weight
                    )
                )
            else:
                row.append(0)
        hessian.append(row)
    return h_value, cofactors, hessian


def audit_nonconstant_reconstruction() -> None:
    q = 6
    m = q // 2
    edge_order = edges(q)
    weight = {
        edge: 2 + (edge[0] + 1) * (edge[1] + 1) for edge in edge_order
    }
    h_value, cofactors, hessian = build_integer_jet(q, weight)
    delta = bareiss_determinant(hessian)
    assert delta != 0

    reconstructed = solve(hessian, [(m - 1) * value for value in cofactors])
    assert reconstructed == [Fraction(weight[edge]) for edge in edge_order]

    # adj(D)c = delta D^(-1)c, computed without an adjugate routine.
    inverse_c = solve(hessian, cofactors)
    adjugate_c = [delta * value for value in inverse_c]
    b_vector = [(m - 1) * value for value in adjugate_c]
    assert b_vector == [Fraction(delta * weight[edge]) for edge in edge_order]

    index = {edge: position for position, edge in enumerate(edge_order)}
    for four_set in combinations(range(q), 4):
        i, j, k, ell = four_set
        entries = (
            hessian[index[(i, j)]][index[(k, ell)]],
            hessian[index[(i, k)]][index[(j, ell)]],
            hessian[index[(i, ell)]][index[(j, k)]],
        )
        assert entries[0] == entries[1] == entries[2]

    # Here m-2=1 and the complement has two vertices, so the cleared
    # hafnian is the corresponding B edge.
    for row, edge in enumerate(edge_order):
        for column, other in enumerate(edge_order):
            if not set(edge).isdisjoint(other):
                assert hessian[row][column] == 0
                continue
            remaining = tuple(sorted(set(range(q)) - set(edge + other)))
            remaining_edge = tuple(remaining)
            right = b_vector[index[remaining_edge]]
            assert Fraction(delta * hessian[row][column]) == right

    quadratic = sum(
        Fraction(cofactors[position]) * adjugate_c[position]
        for position in range(len(edge_order))
    )
    assert Fraction(m * delta * h_value) == (m - 1) * quadratic


def audit_false_linear_shell() -> None:
    scaled = kneser(4, 2)
    assert bareiss_determinant(scaled) != 0
    edge_order = edges(4)
    for row, edge in enumerate(edge_order):
        for column, other in enumerate(edge_order):
            if set(edge).isdisjoint(other):
                assert scaled[row][column] == 2
                # A four-vertex hafnian Hessian has haf(empty)=1 here.
                assert scaled[row][column] != 1
    assert comb(8, 4) == 70
    assert comb(8, 2) == 28


def main() -> None:
    audit_kneser_chart()
    audit_nonconstant_reconstruction()
    audit_false_linear_shell()
    print("independent residual Hessian Kneser/open-jet audit: PASS")
    print("Bareiss q=4,6,8 determinants: exact")
    print("rational nonconstant q=6 reconstruction and scalar stress: exact")
    print("scaled q=4 Kneser false control: rejected")
    print("global Krenn-Gu: UNRESOLVED")


if __name__ == "__main__":
    main()
