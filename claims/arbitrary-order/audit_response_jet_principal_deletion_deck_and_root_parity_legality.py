"""Independent no-import audit of response-deck/root-parity identities."""

from __future__ import annotations

from functools import cache
from itertools import combinations

Edge = tuple[int, int]
Monomial = frozenset[Edge]
ScalarPolynomial = dict[Monomial, int]
VectorPolynomial = dict[Monomial, tuple[int, int]]


def edge(i: int, j: int) -> Edge:
    return (i, j) if i < j else (j, i)


def clean_scalar(polynomial: ScalarPolynomial) -> ScalarPolynomial:
    return {monomial: value for monomial, value in polynomial.items() if value}


def clean_vector(polynomial: VectorPolynomial) -> VectorPolynomial:
    return {
        monomial: value
        for monomial, value in polynomial.items()
        if value != (0, 0)
    }


def hafnian_polynomial(vertices: tuple[int, ...]) -> ScalarPolynomial:
    @cache
    def rec(remaining: tuple[int, ...]) -> tuple[tuple[Monomial, int], ...]:
        if not remaining:
            return ((frozenset(), 1),)
        if len(remaining) % 2:
            return ()
        first = remaining[0]
        total: ScalarPolynomial = {}
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            chosen = edge(first, partner)
            for monomial, coefficient in rec(rest):
                enlarged = monomial | {chosen}
                total[enlarged] = total.get(enlarged, 0) + coefficient
        return tuple(clean_scalar(total).items())

    return dict(rec(vertices))


def add_scalar_times_vector(
    target: VectorPolynomial,
    scalar: ScalarPolynomial,
    vector: tuple[int, int],
) -> None:
    for monomial, coefficient in scalar.items():
        old = target.get(monomial, (0, 0))
        target[monomial] = (
            old[0] + coefficient * vector[0],
            old[1] + coefficient * vector[1],
        )


def response(vertices: tuple[int, ...], coefficients: dict[Edge, tuple[int, int]]) -> VectorPolynomial:
    result: VectorPolynomial = {}
    add_scalar_times_vector(result, hafnian_polynomial(vertices), (2, -3))
    for pair in combinations(vertices, 2):
        remainder = tuple(vertex for vertex in vertices if vertex not in pair)
        add_scalar_times_vector(result, hafnian_polynomial(remainder), coefficients[pair])
    return clean_vector(result)


def derivative(polynomial: VectorPolynomial, chosen: Edge) -> VectorPolynomial:
    result: VectorPolynomial = {}
    for monomial, coefficient in polynomial.items():
        if chosen in monomial:
            reduced = monomial - {chosen}
            old = result.get(reduced, (0, 0))
            result[reduced] = (old[0] + coefficient[0], old[1] + coefficient[1])
    return clean_vector(result)


def audit_response_decks() -> None:
    vertices = tuple(range(6))
    edges = tuple(combinations(vertices, 2))
    coefficients = {
        pair: (3 * pair[0] + pair[1] + 1, pair[0] - 2 * pair[1] - 1)
        for pair in edges
    }
    top = response(vertices, coefficients)
    for pair in edges:
        remainder = tuple(vertex for vertex in vertices if vertex not in pair)
        assert derivative(top, pair) == response(remainder, coefficients)
    for first, second in combinations(edges, 2):
        twice = derivative(derivative(top, first), second)
        if set(first).isdisjoint(second):
            deleted = set(first) | set(second)
            remainder = tuple(vertex for vertex in vertices if vertex not in deleted)
            assert twice == response(remainder, coefficients)
        else:
            assert not twice
    scalar_edge = 7
    pure = (2, -3)
    channel = (5, 11)
    two_residual_top = (
        scalar_edge * pure[0] + channel[0],
        scalar_edge * pure[1] + channel[1],
    )
    assert (
        two_residual_top[0] - scalar_edge * pure[0],
        two_residual_top[1] - scalar_edge * pure[1],
    ) == channel
    print("independent polynomial deck/derivative audit: PASS")


def hafnian_value(vertices: tuple[int, ...], weights: dict[Edge, int]) -> int:
    @cache
    def rec(remaining: tuple[int, ...]) -> int:
        if not remaining:
            return 1
        if len(remaining) % 2:
            return 0
        first = remaining[0]
        total = 0
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += weights.get(edge(first, partner), 0) * rec(rest)
        return total

    return rec(vertices)


def permanent_value(matrix: list[list[int]]) -> int:
    size = len(matrix)

    @cache
    def rec(row: int, available: tuple[int, ...]) -> int:
        if row == size:
            return 1
        total = 0
        for position, column in enumerate(available):
            rest = available[:position] + available[position + 1 :]
            total += matrix[row][column] * rec(row + 1, rest)
        return total

    return rec(0, tuple(range(size)))


def audit_augmented_hafnians() -> None:
    roots = tuple(range(4))
    pair = (4, 5)
    weights: dict[Edge, int] = {}
    for i, j in combinations(roots, 2):
        weights[(i, j)] = 2 + 2 * i + j
    for root in roots:
        for deleted in pair:
            weights[edge(root, deleted)] = 1 + 3 * root - deleted
    block_value = hafnian_value(roots + pair, weights)
    explicit = 0
    for internal in combinations(roots, 2):
        remaining = tuple(root for root in roots if root not in internal)
        explicit += weights[internal] * (
            weights[edge(remaining[0], pair[0])]
            * weights[edge(remaining[1], pair[1])]
            + weights[edge(remaining[0], pair[1])]
            * weights[edge(remaining[1], pair[0])]
        )
    assert block_value == explicit
    zero_root_edges = {
        chosen: (0 if chosen[0] in roots and chosen[1] in roots else value)
        for chosen, value in weights.items()
    }
    assert hafnian_value(roots + pair, zero_root_edges) == 0

    deleted_four = tuple(range(4, 8))
    weights_four = {
        edge(root, deleted): 1 + root + 2 * (deleted - 4)
        for root in roots
        for deleted in deleted_four
    }
    for internal in combinations(roots, 2):
        weights_four[internal] = 7 + internal[0] + internal[1]
    block_four = hafnian_value(roots + deleted_four, weights_four)
    incidence = [
        [weights_four[edge(root, deleted)] for deleted in deleted_four]
        for root in roots
    ]
    assert block_four == permanent_value(incidence)
    assert hafnian_value((0, 1, 2, 3, 4), weights_four) == 0
    print("independent augmented-hafnian/parity audit: PASS")


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                row
                for row in range(pivot_index + 1, size)
                if work[row][pivot_index] != 0
            )
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
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
        previous = pivot
    return sign * work[-1][-1]


def tensor_product(left: list[int], right: list[int]) -> list[int]:
    return [x * y for x in left for y in right]


def audit_fan_certificate() -> None:
    matrix_a = [[1, 0, 1, 1], [0, 1, 0, 1]]
    matrix_b = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    columns: list[list[int]] = []
    for i, j in combinations(range(4), 2):
        a_i = [row[i] for row in matrix_a]
        a_j = [row[j] for row in matrix_a]
        b_i = [row[i] for row in matrix_b]
        b_j = [row[j] for row in matrix_b]
        first = tensor_product(a_i, b_j)
        second = tensor_product(a_j, b_i)
        columns.append([x + y for x, y in zip(first, second, strict=True)])
    fan = [[columns[column][row] for column in range(6)] for row in range(6)]
    assert bareiss_determinant(fan) == -2

    pair_order = tuple(combinations(range(4), 2))
    complement = [[0 for _ in range(6)] for _ in range(6)]
    for row, pair in enumerate(pair_order):
        opposite = tuple(vertex for vertex in range(4) if vertex not in pair)
        complement[row][pair_order.index(opposite)] = 1
    assert bareiss_determinant(complement) == -1
    print("independent 2x3 fan determinant audit: PASS")


def audit_pair_vacuum_fibre() -> None:
    fixed = {(0, 2): 2, (1, 3): -3, (4, 5): 5}
    full_values: list[int] = []
    deleted_values: list[int] = []
    for parameter in (2, 7):
        weights = {**fixed, (2, 3): parameter}
        full_values.append(hafnian_value(tuple(range(6)), weights))
        deleted_values.append(hafnian_value((2, 3, 4, 5), weights))
    assert full_values == [-30, -30]
    assert deleted_values == [10, 35]
    print("independent complete-tensor fibre audit: PASS")


def main() -> None:
    audit_response_decks()
    audit_augmented_hafnians()
    audit_fan_certificate()
    audit_pair_vacuum_fibre()
    print("response-jet principal-deletion/root-parity independent audit: PASS")


if __name__ == "__main__":
    main()
