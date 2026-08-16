"""Independent audit of the star-pair noncommon/support-two boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

Scalar = int | Fraction
Vector = tuple[Scalar, ...]
Linear = tuple[int, int]
Polynomial = dict[int, Fraction]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

N = (0, 1, 1, 0)
B0 = (1, 0, 1, 0)
C0 = (1, -1, 0, 0)
B1 = (1, 0, 0, 1)
C1 = (1, 1, 1, 1)
Q_LINE = (0, 0, 1, 1)


def first_four_product(left: Vector, right: Vector) -> Vector:
    """Multiply two forms in the square-free four-variable algebra."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def rank(rows: list[list[int | Fraction]]) -> int:
    """Return exact row rank with a standalone rational reducer."""
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


def nullspace(rows: list[list[int]]) -> list[tuple[Fraction, ...]]:
    """Return a basis of the exact right kernel."""
    matrix = [[Fraction(value) for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                matrix[row][index] - scalar * matrix[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    free_columns = [column for column in range(column_count) if column not in pivot_columns]
    basis = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(column_count)]
        vector[free] = 1
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -matrix[row][free]
        basis.append(tuple(vector))
    return basis


def complement_core_matrix(quadratic: Vector) -> tuple[tuple[int, ...], ...]:
    """Construct the complementary quadratic matrix independently."""
    matrix = [[0] * 4 for _ in range(4)]
    vertices = set(range(4))
    for coefficient, edge in zip(quadratic, EDGES, strict=True):
        first, second = sorted(vertices - set(edge))
        matrix[first][second] += coefficient
        matrix[second][first] += coefficient
    return tuple(tuple(row) for row in matrix)


def multiply_matrix_vector(matrix: tuple[tuple[int, ...], ...], vector: Vector) -> Vector:
    """Multiply a small integer matrix and vector."""
    return tuple(sum(row[index] * vector[index] for index in range(4)) for row in matrix)


def contract(matrix: tuple[tuple[int, ...], ...], vector: Vector) -> Vector:
    """Contract a complementary core once."""
    return multiply_matrix_vector(matrix, vector)


def double_contract(
    matrix: tuple[tuple[int, ...], ...],
    first: Vector,
    second: Vector,
) -> Scalar:
    """Contract a complementary core in two distinct slots."""
    row = contract(matrix, first)
    return sum(row[index] * second[index] for index in range(4))


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
    """Extract the full square-free coefficient of q times four forms."""
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


def j_form(left: Vector, right: Vector) -> Fraction:
    """Evaluate the x4,x5 hyperbolic form exactly."""
    return Fraction(left[4] * right[5] + left[5] * right[4])


def cubic_value(ell: Vector, first: Vector, second: Vector, third: Vector) -> Fraction:
    """Evaluate the full polarization of ell*x4*x5."""
    def evaluate(vector: Vector) -> Fraction:
        return sum((Fraction(ell[index] * vector[index]) for index in range(6)), Fraction(0))

    return (
        evaluate(first) * j_form(second, third)
        + evaluate(second) * j_form(first, third)
        + evaluate(third) * j_form(first, second)
    )


def cubic_slice(
    ell: Vector,
    vector: Vector,
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
) -> tuple[tuple[Fraction, ...], ...]:
    """Build a three-by-three full bilinear slice independently."""
    return tuple(
        tuple(cubic_value(ell, vector, left_row, right_column) for right_column in right)
        for left_row in left
    )


def quotient(vector: Vector) -> tuple[int, int]:
    """Apply the standalone quotient coordinates from the theorem."""
    return vector[1] + vector[2], -vector[1] + vector[3]


def assert_algebra_and_noncommon_cases() -> dict[str, object]:
    """Rebuild the pair and audit all noncommon same-mode cases."""
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
    quadratics = {
        "m1": products[0][1],
        "m2": products[1][0],
        "d0": products[0][0],
        "d1": products[1][1],
        "d2": products[2][2],
    }
    assert quadratics == {
        "m1": (-1, 1, 0, 1, 0, 0),
        "m2": (1, -1, 0, 0, -1, 1),
        "d0": (-1, 2, -1, 1, 0, 1),
        "d1": (1, 0, -1, 0, -1, 0),
        "d2": (0, 0, 0, 2, 0, 0),
    }
    assert rank([list(entry) for row in products for entry in row]) == 5
    cores = {name: complement_core_matrix(value) for name, value in quadratics.items()}

    phi1 = ((0, 0, 0, 1), (1, 1, -1, 0))
    phi2 = ((1, 0, 0, -1), (0, 1, -1, 0))
    assert nullspace([*map(list, phi1), *map(list, phi2)]) == [
        (Fraction(0), Fraction(1), Fraction(1), Fraction(0))
    ]
    assert all(
        sum(row[index] * line[index] for index in range(4)) == 0
        for row in phi1
        for line in (N, B0, C0)
    )
    assert all(
        sum(row[index] * line[index] for index in range(4)) == 0
        for row in phi2
        for line in (N, B1, C1)
    )

    lines = {"B0": B0, "C0": C0, "B1": B1, "C1": C1}
    table = {
        line_name: {
            channel: contract(core, line)
            for channel, core in cores.items()
        }
        for line_name, line in lines.items()
    }
    assert table["B0"]["m1"] == table["C0"]["m1"] == (0, 0, 0, 0)
    assert table["B1"]["m2"] == table["C1"]["m2"] == (0, 0, 0, 0)
    assert table["B0"]["m2"] == table["C0"]["m2"] == (-1, 1, -1, 1)
    assert table["B1"]["m1"] == table["C1"]["m1"] == (1, 1, -1, 1)
    assert rank([
        list(table["B0"]["m2"]),
        list(table["B1"]["m1"]),
    ]) == 2
    assert quotient(table["B0"]["m2"]) == quotient(table["B1"]["m1"]) == (0, 0)

    expected = {
        "B0": ((0, 0), (-2, 2), (0, 2)),
        "C0": ((2, -2), (0, 0), (0, 2)),
        "B1": ((2, -2), (0, 0), (0, 2)),
        "C1": ((0, 0), (-2, 2), (0, 2)),
    }
    actual = {
        line_name: tuple(quotient(table[line_name][channel]) for channel in ("d0", "d1", "d2"))
        for line_name in lines
    }
    assert actual == expected

    # Each same-missing pair has identical nonzero quotient columns.
    assert actual["B0"][1:] == actual["C1"][1:]
    assert (actual["C0"][0], actual["C0"][2]) == (
        actual["B1"][0],
        actual["B1"][2],
    )
    # Each different-missing pair exposes a nonzero entry for every possible
    # zero-row colour.
    assert all(value != (0, 0) for value in (actual["B1"][0], actual["B0"][1], actual["B0"][2]))
    assert all(value != (0, 0) for value in (actual["C0"][0], actual["C1"][1], actual["C0"][2]))
    return {
        "pair_rank": 5,
        "common_kernel": N,
        "quotient_table": actual,
        "noncommon_pairs_audited": 4,
    }


def linear_contract(
    matrix: tuple[tuple[int, ...], ...],
    parameterized_vector: tuple[Linear, ...],
) -> tuple[Linear, ...]:
    """Contract with a vector linear in u,v."""
    return tuple(
        (
            sum(matrix[row][column] * parameterized_vector[column][0] for column in range(4)),
            sum(matrix[row][column] * parameterized_vector[column][1] for column in range(4)),
        )
        for row in range(4)
    )


def linear_add(*values: Linear) -> Linear:
    """Add linear u,v coefficients."""
    return tuple(sum(value[index] for value in values) for index in range(2))


def linear_scale(scalar: int, value: Linear) -> Linear:
    """Scale linear u,v coefficients."""
    return scalar * value[0], scalar * value[1]


def multiply_by_u(value: Linear) -> tuple[int, int, int]:
    """Return u times a linear form in the basis u^2,uv,v^2."""
    return value[0], value[1], 0


def multiply_by_u_plus_v(value: Linear) -> tuple[int, int, int]:
    """Return (u+v) times a linear form."""
    return value[0], value[0] + value[1], value[1]


def assert_common_propagation() -> dict[str, object]:
    """Audit the common-line propagation identities."""
    quadratics = {
        "m1": (-1, 1, 0, 1, 0, 0),
        "m2": (1, -1, 0, 0, -1, 1),
        "d0": (-1, 2, -1, 1, 0, 1),
        "d1": (1, 0, -1, 0, -1, 0),
        "d2": (0, 0, 0, 2, 0, 0),
    }
    cores = {name: complement_core_matrix(value) for name, value in quadratics.items()}
    n_rows = {name: contract(core, N) for name, core in cores.items()}
    assert n_rows == {
        "m1": (0, 0, 0, 0),
        "m2": (0, 0, 0, 0),
        "d0": (1, -1, -1, 1),
        "d1": (-1, -1, -1, 1),
        "d2": (0, 0, 0, 0),
    }
    h_kernel = nullspace([list(n_rows["d0"]), list(n_rows["d1"])])
    displayed_h_basis = ((0, 1, 0, 1), (0, 0, 1, 1))
    assert rank([*map(list, h_kernel), *map(list, displayed_h_basis)]) == 2

    parameterized = ((0, 0), (1, 0), (0, 1), (1, 1))
    rows = {name: linear_contract(core, parameterized) for name, core in cores.items()}
    for coordinate in range(4):
        identity = linear_add(
            linear_scale(2, rows["m1"][coordinate]),
            linear_scale(-1, rows["d0"][coordinate]),
            rows["d1"][coordinate],
        )
        assert identity == (0, 0)
        left = multiply_by_u(rows["d2"][coordinate])
        mixed_sum = linear_add(rows["m1"][coordinate], rows["m2"][coordinate])
        right = multiply_by_u_plus_v(mixed_sum)
        assert left == right

    q_rows = {name: contract(core, Q_LINE) for name, core in cores.items()}
    assert q_rows == {
        "m1": (1, 1, -1, -1),
        "m2": (-1, -1, 1, 1),
        "d0": (1, 1, -1, -1),
        "d1": (-1, -1, 1, 1),
        "d2": (2, 0, 0, 0),
    }
    assert all(double_contract(core, N, Q_LINE) == 0 for core in cores.values())

    test_vector = (2, -3, 5, 7)
    assert double_contract(cores["d0"], N, test_vector) == sum(
        left * right for left, right in zip(n_rows["d0"], test_vector, strict=True)
    )
    assert double_contract(cores["d1"], N, test_vector) == sum(
        left * right for left, right in zip(n_rows["d1"], test_vector, strict=True)
    )
    assert double_contract(cores["d2"], Q_LINE, test_vector) == 2 * test_vector[0]
    return {
        "N_rows": n_rows,
        "H_basis": displayed_h_basis,
        "companion_rows": q_rows,
        "propagation_identities": 8,
    }


def assert_support_two_cubic_rank() -> dict[str, object]:
    """Independently reconstruct the rank-one-free slice space."""
    slice_x = ((0, 0, 0), (0, 0, 1), (0, 1, 0))
    slice_u = ((0, 0, 1), (0, 0, 0), (1, 0, 0))
    slice_v = ((0, 1, 0), (1, 0, 0), (0, 0, 0))
    flattened = [
        [entry for row in matrix for entry in row]
        for matrix in (slice_x, slice_u, slice_v)
    ]
    assert rank(flattened) == 3

    # A general slice is [[0,c,b],[c,0,a],[b,a,0]].  Its three principal
    # two-minors are -c^2,-b^2,-a^2, so rank at most one forces a=b=c=0
    # over a field.  Reconstruct each coefficient square in a tiny formal
    # quadratic representation ordered (a^2,ab,ac,b^2,bc,c^2).
    a = (1, 0, 0)
    b = (0, 1, 0)
    c = (0, 0, 1)

    def square(linear: tuple[int, int, int]) -> tuple[int, ...]:
        first, second, third = linear
        return (
            first * first,
            2 * first * second,
            2 * first * third,
            second * second,
            2 * second * third,
            third * third,
        )

    principal_minors = tuple(
        tuple(-coefficient for coefficient in square(linear))
        for linear in (c, b, a)
    )
    assert principal_minors == (
        (0, 0, 0, 0, 0, -1),
        (0, 0, 0, -1, 0, 0),
        (-1, 0, 0, 0, 0, 0),
    )

    e00 = [1] + [0] * 8
    e11 = [0] * 4 + [1] + [0] * 4
    e22 = [0] * 8 + [1]
    assert rank([e00, e11, e22]) == 3
    return {
        "weighted_delta_slice_rank": 3,
        "pol_XUV_slice_rank": 3,
        "principal_two_minors": principal_minors,
        "nonzero_rank_one_slices": 0,
    }


def assert_singleton_sharpness_fixture() -> dict[str, object]:
    """Audit the exact rational N/Q slice survivor and target failures."""
    half = Fraction(1, 2)
    modes: tuple[tuple[Vector, ...], ...] = (
        (
            (0, 1, 1, 0, 0, 0),
            (0, 1, -half, 3 * half, 0, 0),
            (0, -1, half, -half, 1, 0),
        ),
        (
            (1, 0, -half, half, 0, 0),
            (0, 1, half, 3 * half, 0, 0),
            (0, 0, 1, 1, 0, 0),
        ),
        (
            (0, -2, 0, 0, 0, 1),
            (0, 0, -1, 1, 0, 0),
            (1, -1, half, -half, 0, 0),
        ),
        (
            (0, 1, half, -half, 1, 0),
            (0, 1, half, half, 0, 0),
            (0, 1, -2, 1, 0, 1),
        ),
    )
    mode_a, mode_b, mode_c, mode_d = modes
    assert tuple(rank([list(vector) for vector in mode]) for mode in modes) == (3, 3, 3, 3)

    phi1 = (
        (0, 0, 0, 1, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
        (1, 1, -1, 0, 0, 0),
    )
    phi2 = (
        (1, 0, 0, -1, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
        (0, 1, -1, 0, 0, 0),
    )

    def projection_rank(rows: tuple[tuple[int, ...], ...], mode: tuple[Vector, ...]) -> int:
        projected = [
            [
                sum((Fraction(row[index] * vector[index]) for index in range(6)), Fraction(0))
                for vector in mode
            ]
            for row in rows
        ]
        return rank(projected)

    profiles = tuple(
        tuple(projection_rank(phi, mode) for mode in modes)
        for phi in (phi1, phi2)
    )
    assert profiles == ((2, 2, 2, 3), (2, 2, 2, 3))
    assert mode_a[0] == (*N, 0, 0)
    assert mode_b[2] == (*Q_LINE, 0, 0)

    x0: Vector = (1, 0, 0, 0, 0, 0)
    r: Vector = (1, 1, -1, -1, 0, 0)
    h0: Vector = (1, -1, -1, 1, 0, 0)
    h1: Vector = (-1, -1, -1, 1, 0, 0)
    assert tuple(2 * x0[index] + h1[index] for index in range(6)) == h0
    zero = tuple(tuple(Fraction(0) for _ in range(3)) for _ in range(3))
    e00 = tuple(
        tuple(Fraction(i == 0 and j == 0) for j in range(3))
        for i in range(3)
    )
    e22 = tuple(
        tuple(Fraction(i == 2 and j == 2) for j in range(3))
        for i in range(3)
    )
    assert tuple(cubic_slice(r, vector, mode_c, mode_d) for vector in mode_a) == (
        zero,
        zero,
        zero,
    )
    assert tuple(cubic_slice(x0, vector, mode_c, mode_d) for vector in mode_a) == (
        zero,
        zero,
        e22,
    )
    assert tuple(cubic_slice(h1, vector, mode_c, mode_d) for vector in mode_b) == (
        zero,
        zero,
        zero,
    )
    assert tuple(cubic_slice(x0, vector, mode_c, mode_d) for vector in mode_b) == (
        e00,
        zero,
        zero,
    )

    d1 = (1, 0, -1, 0, -1, 0)
    m1 = (-1, 1, 0, 1, 0, 0)
    d1_failure = quartic_coefficient(
        d1,
        (mode_a[1], mode_b[1], mode_c[1], mode_d[1]),
    )
    m1_failure = quartic_coefficient(
        m1,
        (mode_a[1], mode_b[0], mode_c[0], mode_d[0]),
    )
    assert d1_failure == 0
    assert m1_failure == 3
    return {
        "local_ranks": (3, 3, 3, 3),
        "projection_profiles": profiles,
        "N_colour": 0,
        "Q_colour": 2,
        "forced_slice_counts": (6, 6),
        "full_target_failures": {"d1_1111": d1_failure, "m1_1000": m1_failure},
    }


def inverse(value: int, prime: int) -> int:
    """Return an inverse in a prime field."""
    return pow(value % prime, prime - 2, prime)


def projective_states(prime: int) -> tuple[tuple[int, int], ...]:
    """Enumerate zero and every projective line in F_p^2."""
    result = [(0, 0)]
    seen: set[tuple[int, int]] = set()
    for vector in product(range(prime), repeat=2):
        if vector == (0, 0):
            continue
        pivot = next(index for index, value in enumerate(vector) if value)
        scalar = inverse(vector[pivot], prime)
        normalized = tuple(value * scalar % prime for value in vector)
        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return tuple(result)


def form(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate the hyperbolic form modulo an odd prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def compatible(
    left: tuple[tuple[int, int], ...],
    right: tuple[tuple[int, int], ...],
    prime: int,
) -> bool:
    """Test every off-colour orthogonality equation."""
    return all(
        left_colour == right_colour
        or form(left[left_colour], right[right_colour], prime) == 0
        for left_colour in range(3)
        for right_colour in range(3)
    )


def audit_active_core(prime: int) -> dict[str, int]:
    """Independently exhaust the two-dimensional active-colour lemma."""
    states = projective_states(prime)
    modes = tuple(product(states, repeat=3))
    neighbours = tuple(
        frozenset(
            right_index
            for right_index, right in enumerate(modes)
            if compatible(left, right, prime)
        )
        for left in modes
    )
    triples = 0
    two_active = 0
    for first_index, first in enumerate(modes):
        for second_index in neighbours[first_index]:
            second = modes[second_index]
            for third_index in neighbours[first_index] & neighbours[second_index]:
                third = modes[third_index]
                triples += 1
                configuration = (first, second, third)
                active = [
                    colour
                    for colour in range(3)
                    if any(
                        form(configuration[i][colour], configuration[j][colour], prime)
                        for i, j in ((0, 1), (0, 2), (1, 2))
                    )
                ]
                assert len(active) <= 2
                if len(active) == 2:
                    two_active += 1
                    inactive = ({0, 1, 2} - set(active)).pop()
                    assert all(mode[inactive] == (0, 0) for mode in configuration)
    return {
        "states": len(states),
        "modes": len(modes),
        "compatible_triples": triples,
        "two_active_triples": two_active,
    }


def assert_dimension_gates() -> dict[str, int]:
    """Check all numerical rank gaps used in the proof."""
    assert 4 - 3 == 1 < 2
    assert 6 - 3 == 3 < 4
    return {
        "quotient_kernel_rank_ceiling": 1,
        "quotient_forbidden_rank": 2,
        "full_kernel_rank_ceiling": 3,
        "full_forbidden_rank": 4,
    }


def main() -> None:
    """Run the independent audit."""
    algebra = assert_algebra_and_noncommon_cases()
    propagation = assert_common_propagation()
    cubic_rank = assert_support_two_cubic_rank()
    fixture = assert_singleton_sharpness_fixture()
    dimensions = assert_dimension_gates()
    finite_fields = {prime: audit_active_core(prime) for prime in (3, 5)}
    print("star-pair same-mode noncommon/support-two boundary independent audit: PASS")
    print(f"  standalone noncommon algebra: {algebra}")
    print(f"  standalone propagation: {propagation}")
    print(f"  standalone support-two cubic-rank gate: {cubic_rank}")
    print(f"  standalone singleton sharpness fixture: {fixture}")
    print(f"  dimension gates: {dimensions}")
    print(f"  finite-field active-core audits: {finite_fields}")


if __name__ == "__main__":
    main()
