"""Independent no-SymPy audit of the star singleton N/N exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

Scalar = int | Fraction
Vector = tuple[Scalar, ...]
Linear = tuple[int, int, int]
Quadratic = tuple[int, int, int, int, int, int]
Polynomial = dict[int, Fraction]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (-1, 1, 0, 1, 0, 0)
M2 = (1, -1, 0, 0, -1, 1)
D0 = (-1, 2, -1, 1, 0, 1)
D1 = (1, 0, -1, 0, -1, 0)
D2 = (0, 0, 0, 2, 0, 0)
SOURCE_QUADRATICS = {"m1": M1, "m2": M2, "d0": D0, "d1": D1, "d2": D2}

N = (0, 1, 1, 0)
Q = (0, 0, 1, 1)


def first_four_product(left: Vector, right: Vector) -> tuple[Scalar, ...]:
    """Multiply two forms in the four-variable square-free algebra."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def rational_rank(rows: list[list[Scalar]]) -> int:
    """Return exact row rank using standalone Fraction elimination."""
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                matrix[row][index] - scalar * matrix[pivot_row][index]
                for index in range(len(matrix[0]))
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def complement_core_matrix(quadratic: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Build the complementary core without symbolic software."""
    matrix = [[0] * 4 for _ in range(4)]
    vertices = set(range(4))
    for coefficient, edge in zip(quadratic, EDGES, strict=True):
        first, second = sorted(vertices - set(edge))
        matrix[first][second] += coefficient
        matrix[second][first] += coefficient
    return tuple(tuple(row) for row in matrix)


CORES = {
    name: complement_core_matrix(quadratic)
    for name, quadratic in SOURCE_QUADRATICS.items()
}


def matrix_vector(matrix: tuple[tuple[int, ...], ...], vector: Vector) -> Vector:
    """Multiply a four-by-four integer matrix by a vector."""
    return tuple(
        sum((row[index] * vector[index] for index in range(4)), 0)
        for row in matrix
    )


def double_contract(name: str, first: Vector, second: Vector) -> Scalar:
    """Contract a complementary core in two distinct slots."""
    row = matrix_vector(CORES[name], first)
    return sum((row[index] * second[index] for index in range(4)), 0)


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, Fraction(0)) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def quartic_coefficient(quadratic: tuple[int, ...], vectors: tuple[Vector, ...]) -> Fraction:
    """Extract the full coefficient of q times four linear forms."""
    polynomial: Polynomial = {
        (1 << first) | (1 << second): Fraction(value)
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        linear = {
            1 << index: Fraction(value)
            for index, value in enumerate(vector)
            if value
        }
        polynomial = square_free_multiply(polynomial, linear)
    return polynomial.get(FULL_MASK, Fraction(0))


def unit(dimension: int, index: int) -> tuple[int, ...]:
    """Return a standard basis vector."""
    return tuple(int(position == index) for position in range(dimension))


def j_form(left: Vector, right: Vector) -> Scalar:
    """Evaluate the x4,x5 hyperbolic form."""
    return left[4] * right[5] + left[5] * right[4]


def p_xuv(first: Vector, second: Vector, third: Vector) -> Scalar:
    """Evaluate the full polarization of XUV."""
    return (
        first[0] * (second[1] * third[2] + second[2] * third[1])
        + first[1] * (second[0] * third[2] + second[2] * third[0])
        + first[2] * (second[0] * third[1] + second[1] * third[0])
    )


def assert_star_rows_and_core_identity() -> dict[str, object]:
    """Rebuild the star data and the x0-hyperplane identity."""
    u = (
        (-1, 0, 1, 0),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
    )
    v = (
        (1, 1, -1, 1),
        (1, 1, 0, 0),
        (0, -1, 1, 0),
    )
    products = tuple(tuple(first_four_product(left, right) for right in v) for left in u)
    assert products[0][1] == M1
    assert products[1][0] == M2
    assert products[0][0] == D0
    assert products[1][1] == D1
    assert products[2][2] == D2
    assert rational_rank([list(entry) for row in products for entry in row]) == 5

    n_rows = {name: matrix_vector(core, N) for name, core in CORES.items()}
    assert n_rows == {
        "m1": (0, 0, 0, 0),
        "m2": (0, 0, 0, 0),
        "d0": (1, -1, -1, 1),
        "d1": (-1, -1, -1, 1),
        "d2": (0, 0, 0, 0),
    }
    q_rows = {name: matrix_vector(core, Q) for name, core in CORES.items()}
    assert q_rows["d2"] == (2, 0, 0, 0)
    assert tuple((n_rows["d0"][index] - n_rows["d1"][index]) // 2 for index in range(4)) == (
        1,
        0,
        0,
        0,
    )

    difference = tuple(
        tuple(
            CORES["d0"][row][column]
            - CORES["d1"][row][column]
            - 2 * CORES["m1"][row][column]
            for column in range(4)
        )
        for row in range(4)
    )
    expected = (
        (0, 1, 1, -1),
        (1, 0, 0, 0),
        (1, 0, 0, 0),
        (-1, 0, 0, 0),
    )
    assert difference == expected
    assert all(difference[row][column] == 0 for row in (1, 2, 3) for column in (1, 2, 3))
    return {
        "source_rank": 5,
        "N_rows": n_rows,
        "Q_d2_row": q_rows["d2"],
        "core_difference": difference,
    }


def multiply_linear(left: Linear, right: Linear) -> Quadratic:
    """Multiply linear forms in order X^2,XU,XV,U^2,UV,V^2."""
    x1, u1, v1 = left
    x2, u2, v2 = right
    return (
        x1 * x2,
        x1 * u2 + u1 * x2,
        x1 * v2 + v1 * x2,
        u1 * u2,
        u1 * v2 + v1 * u2,
        v1 * v2,
    )


def quadratic_subtract(left: Quadratic, right: Quadratic) -> Quadratic:
    """Subtract formal quadratic coefficient tuples."""
    return tuple(left[index] - right[index] for index in range(6))  # type: ignore[return-value]


def assert_formal_annihilator() -> dict[str, object]:
    """Derive the kappa matrix and its principal minors formally."""
    basis = tuple(unit(3, index) for index in range(3))
    formal_matrix: tuple[tuple[Linear, ...], ...] = tuple(
        tuple(
            tuple(int(p_xuv(basis[row], basis[column], basis[coefficient])) for coefficient in range(3))
            for column in range(3)
        )
        for row in range(3)
    )
    zero = (0, 0, 0)
    x = (1, 0, 0)
    u = (0, 1, 0)
    v = (0, 0, 1)
    assert formal_matrix == (
        (zero, v, u),
        (v, zero, x),
        (u, x, zero),
    )

    principal_minors = []
    for first, second in ((0, 1), (0, 2), (1, 2)):
        diagonal = multiply_linear(
            formal_matrix[first][first],
            formal_matrix[second][second],
        )
        off_diagonal = multiply_linear(
            formal_matrix[first][second],
            formal_matrix[second][first],
        )
        principal_minors.append(quadratic_subtract(diagonal, off_diagonal))
    expected = (
        (0, 0, 0, 0, 0, -1),
        (0, 0, 0, -1, 0, 0),
        (-1, 0, 0, 0, 0, 0),
    )
    assert tuple(principal_minors) == expected

    coordinate_lines = [
        [1 if row == column == colour else 0 for row in range(3) for column in range(3)]
        for colour in range(3)
    ]
    assert rational_rank([coordinate_lines[0], coordinate_lines[2]]) == 2
    assert rational_rank([coordinate_lines[1], coordinate_lines[2]]) == 2
    return {
        "formal_kappa_matrix": formal_matrix,
        "principal_two_minors": expected,
        "forced_slice_ranks": (2, 2),
    }


def assert_basis_factorizations() -> dict[str, object]:
    """Exhaust both full-quartic identities on multilinear bases."""
    basis6 = tuple(unit(6, index) for index in range(6))
    hyperplane_basis = tuple(basis6[index] for index in (1, 2, 3))
    checked_rank_three = 0
    checked_rank_two = 0

    for name, quadratic in SOURCE_QUADRATICS.items():
        for first, second, third, fourth in product(
            hyperplane_basis,
            hyperplane_basis,
            basis6,
            basis6,
        ):
            actual = quartic_coefficient(quadratic, (first, second, third, fourth))
            expected = double_contract(name, first[:4], second[:4]) * j_form(third, fourth)
            assert actual == expected
            checked_rank_three += 1

        for first, second, third, fourth in product(
            basis6,
            basis6,
            hyperplane_basis,
            hyperplane_basis,
        ):
            actual = quartic_coefficient(quadratic, (first, second, third, fourth))
            expected = j_form(first, second) * double_contract(name, third[:4], fourth[:4])
            assert actual == expected
            checked_rank_two += 1

    assert checked_rank_three == checked_rank_two == 5 * 3 * 3 * 6 * 6
    return {
        "rank_three_basis_entries": checked_rank_three,
        "rank_two_basis_entries": checked_rank_two,
        "channels": tuple(SOURCE_QUADRATICS),
    }


def modular_rank(rows: list[list[int]], prime: int) -> int:
    """Return row rank over F_p."""
    matrix = [[value % prime for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], prime - 2, prime)
        matrix[pivot_row] = [value * inverse % prime for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                (matrix[row][index] - scalar * matrix[pivot_row][index]) % prime
                for index in range(len(matrix[0]))
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def kappa_mod(first: Vector, second: Vector, prime: int) -> tuple[int, int, int]:
    """Return kappa(first,second) over F_p in the coordinate dual basis."""
    basis = tuple(unit(3, index) for index in range(3))
    return tuple(int(p_xuv(test, first, second)) % prime for test in basis)


def audit_finite_annihilators(prime: int) -> dict[str, int]:
    """Search for an annihilator-dimension countermodel over F_p."""
    vectors = tuple(product(range(prime), repeat=3))
    nonzero = tuple(vector for vector in vectors if vector != (0, 0, 0))
    map_checks = 0
    for vector in nonzero:
        matrix = [
            list(kappa_mod(unit(3, column), vector, prime))
            for column in range(3)
        ]
        assert modular_rank(matrix, prime) >= 2
        map_checks += 1

    independent_pairs = 0
    common_annihilator_tests = 0
    for first in nonzero:
        for second in nonzero:
            if modular_rank([list(first), list(second)], prime) != 2:
                continue
            independent_pairs += 1
            common = [
                vector
                for vector in vectors
                if kappa_mod(vector, first, prime) == (0, 0, 0)
                and kappa_mod(vector, second, prime) == (0, 0, 0)
            ]
            assert common == [(0, 0, 0)]
            common_annihilator_tests += len(vectors)
    return {
        "nonzero_map_checks": map_checks,
        "independent_pairs": independent_pairs,
        "candidate_common_annihilators": common_annihilator_tests,
    }


def main() -> None:
    """Run the genuine standalone audit."""
    star = assert_star_rows_and_core_identity()
    annihilator = assert_formal_annihilator()
    factorizations = assert_basis_factorizations()
    finite = {prime: audit_finite_annihilators(prime) for prime in (3, 5)}
    print("star-pair singleton N/N exclusion independent audit: PASS")
    print(f"  standalone star/core identity: {star}")
    print(f"  formal annihilator: {annihilator}")
    print(f"  basis-exhaustive full factorizations: {factorizations}")
    print(f"  finite-field countermodel searches: {finite}")


if __name__ == "__main__":
    main()
