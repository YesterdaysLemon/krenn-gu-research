"""Independent no-import audit of the selector-failure boundary theorem.

This audit deliberately does not import or inspect the primary verifier.  It
uses only the Python standard library, direct exact point/rank tables,
``Fraction`` row reduction, and explicit quotient-space calculations.

The finite polynomial tables below are bounded replays of the stated
pointwise equivalences.  They are not presented as a Nullstellensatz proof or
as evidence about a physical Krenn--Gu witness.
"""

from fractions import Fraction
from itertools import combinations, product

Q = Fraction
ONE = Q(1)
Vector = list[Q]
Matrix = list[list[Q]]
Polynomial = tuple[Q, ...]


def as_q_matrix(rows: list[list[int | Q]]) -> Matrix:
    return [[Q(entry) for entry in row] for row in rows]


def transpose(matrix: Matrix, column_count: int | None = None) -> Matrix:
    if matrix:
        return [list(column) for column in zip(*matrix, strict=True)]
    if column_count is None:
        return []
    return [[] for _ in range(column_count)]


def rref(matrix: Matrix, variable_count: int | None = None) -> tuple[Matrix, list[int]]:
    if not matrix:
        return [], []
    width = len(matrix[0]) if variable_count is None else variable_count
    work = [row[:width] for row in matrix]
    pivots: list[int] = []
    pivot_row = 0
    for column in range(width):
        source = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if source is None:
            continue
        work[pivot_row], work[source] = work[source], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                entry - multiple * pivot
                for entry, pivot in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, pivots


def matrix_rank(matrix: Matrix) -> int:
    if not matrix:
        return 0
    return len(rref(matrix)[1])


def nullspace(matrix: Matrix, variable_count: int | None = None) -> list[Vector]:
    if matrix:
        width = len(matrix[0])
    elif variable_count is not None:
        width = variable_count
    else:
        width = 0
    reduced, pivots = rref(matrix, width)
    free = [column for column in range(width) if column not in pivots]
    answer: list[Vector] = []
    for free_column in free:
        vector = [Q(0) for _ in range(width)]
        vector[free_column] = Q(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        answer.append(vector)
    return answer


def solve(matrix: Matrix, target: Vector) -> tuple[Vector, list[Vector]] | None:
    if len(matrix) != len(target):
        raise ValueError("row and target dimensions differ")
    variable_count = len(matrix[0]) if matrix else 0
    augmented = [row + [value] for row, value in zip(matrix, target, strict=True)]
    reduced, pivots = rref(augmented)
    for row in reduced:
        if all(entry == 0 for entry in row[:variable_count]) and row[-1] != 0:
            return None
    coefficient_pivots = [pivot for pivot in pivots if pivot < variable_count]
    particular = [Q(0) for _ in range(variable_count)]
    for row, pivot in enumerate(coefficient_pivots):
        particular[pivot] = reduced[row][-1]
    return particular, nullspace(matrix, variable_count)


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum((entry * value for entry, value in zip(row, vector, strict=True)), Q(0))
        for row in matrix
    ]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    if not left:
        return []
    right_columns = transpose(right)
    return [
        [
            sum((a * b for a, b in zip(row, column, strict=True)), Q(0))
            for column in right_columns
        ]
        for row in left
    ]


def matrix_from_columns(columns: list[Vector], row_count: int) -> Matrix:
    if not columns:
        return [[] for _ in range(row_count)]
    return [
        [columns[column][row] for column in range(len(columns))]
        for row in range(row_count)
    ]


def append_column(matrix: Matrix, column: Vector) -> Matrix:
    return [row + [entry] for row, entry in zip(matrix, column, strict=True)]


def in_column_span(vector: Vector, columns: list[Vector]) -> bool:
    matrix = matrix_from_columns(columns, len(vector))
    return solve(matrix, vector) is not None


def determinant(matrix: Matrix) -> Q:
    size = len(matrix)
    if size == 0:
        return Q(1)
    work = [row[:] for row in matrix]
    value = Q(1)
    for column in range(size):
        source = next((row for row in range(column, size) if work[row][column]), None)
        if source is None:
            return Q(0)
        if source != column:
            work[column], work[source] = work[source], work[column]
            value = -value
        pivot = work[column][column]
        value *= pivot
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            multiple = work[row][column] / pivot
            for entry_column in range(column, size):
                work[row][entry_column] -= multiple * work[column][entry_column]
    return value


def minors(matrix: Matrix, size: int) -> list[Q]:
    row_count = len(matrix)
    column_count = len(matrix[0]) if matrix else 0
    if size == 0:
        return [Q(1)]
    if size > row_count or size > column_count:
        return []
    answer: list[Q] = []
    for rows in combinations(range(row_count), size):
        for columns in combinations(range(column_count), size):
            answer.append(
                determinant(
                    [[matrix[row][column] for column in columns] for row in rows]
                )
            )
    return answer


def poly_trim(polynomial: Polynomial) -> Polynomial:
    entries = list(polynomial)
    while len(entries) > 1 and entries[-1] == 0:
        entries.pop()
    return tuple(entries)


def poly_eval(polynomial: Polynomial, value: Q) -> Q:
    answer = Q(0)
    for coefficient in reversed(polynomial):
        answer = answer * value + coefficient
    return answer


def poly_add(left: Polynomial, right: Polynomial, scale: Q = ONE) -> Polynomial:
    width = max(len(left), len(right))
    answer = []
    for index in range(width):
        first = left[index] if index < len(left) else Q(0)
        second = right[index] if index < len(right) else Q(0)
        answer.append(first + scale * second)
    return poly_trim(tuple(answer))


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = [Q(0) for _ in range(len(left) + len(right) - 1)]
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            answer[left_degree + right_degree] += left_value * right_value
    return poly_trim(tuple(answer))


def poly_divmod(
    dividend: Polynomial, divisor: Polynomial
) -> tuple[Polynomial, Polynomial]:
    numerator = list(poly_trim(dividend))
    denominator = poly_trim(divisor)
    if denominator == (Q(0),):
        raise ZeroDivisionError
    if len(numerator) < len(denominator):
        return (Q(0),), tuple(numerator)
    quotient = [Q(0) for _ in range(len(numerator) - len(denominator) + 1)]
    while len(numerator) >= len(denominator) and any(numerator):
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[degree] = coefficient
        for index, value in enumerate(denominator):
            numerator[degree + index] -= coefficient * value
        while len(numerator) > 1 and numerator[-1] == 0:
            numerator.pop()
    return poly_trim(tuple(quotient)), poly_trim(tuple(numerator))


def polynomial_determinant_2(matrix: list[list[Polynomial]]) -> Polynomial:
    return poly_add(
        poly_multiply(matrix[0][0], matrix[1][1]),
        poly_multiply(matrix[0][1], matrix[1][0]),
        Q(-1),
    )


def audit_strictness_examples() -> None:
    points = tuple(map(Q, (-3, -2, -1, 1, 2, 3)))

    square = (Q(1), Q(-2), Q(1))
    linear = (Q(-1), Q(1))
    for point in points:
        a_value = poly_eval(square, point)
        g_value = poly_eval(linear, point)
        assert matrix_rank([[a_value]]) == matrix_rank([[a_value, g_value]])
    quotient, remainder = poly_divmod(linear, square)
    assert quotient == (Q(0),)
    assert remainder == linear

    one = (Q(1),)
    quotient, remainder = poly_divmod(one, linear)
    assert remainder != (Q(0),)
    # Nevertheless 1=(1/(s-1))(s-1) in Q(s), while the s=1 fiber fails.
    assert poly_multiply(one, linear) == linear
    assert matrix_rank([[poly_eval(linear, Q(1))]]) == 0
    assert matrix_rank([[poly_eval(linear, Q(1)), Q(1)]]) == 1


def audit_bounded_pointwise_and_response_tables() -> tuple[int, int]:
    coefficients = tuple(map(Q, (-1, 0, 1)))
    polynomials = tuple(product(coefficients, repeat=2))
    points = tuple(map(Q, (-2, -1, 1, 2)))
    matrix_families = 0
    response_families = 0

    for a_top, a_bottom, g_top, g_bottom in product(polynomials, repeat=4):
        evaluations = []
        for point in points:
            a = [[poly_eval(a_top, point)], [poly_eval(a_bottom, point)]]
            g = [poly_eval(g_top, point), poly_eval(g_bottom, point)]
            b = append_column(a, g)
            rank_a = matrix_rank(a)
            rank_b = matrix_rank(b)
            evaluations.append((a, b, rank_a, rank_b))

        absorbed = all(rank_a == rank_b for _, _, rank_a, rank_b in evaluations)
        equal_rank_threshold_tables = all(
            (rank_a < size) == (rank_b < size)
            for _, _, rank_a, rank_b in evaluations
            for size in (1, 2)
        )
        assert absorbed == equal_rank_threshold_tables
        matrix_families += 1

        for response in polynomials:
            no_response_and_survival = True
            gated_minor_products_vanish = True
            for point, (a, b, rank_a, rank_b) in zip(points, evaluations, strict=True):
                rho = poly_eval(response, point)
                if rho and rank_b > rank_a:
                    no_response_and_survival = False
                for size in (1, 2):
                    if all(value == 0 for value in minors(a, size)) and any(
                        rho * value != 0 for value in minors(b, size)
                    ):
                        gated_minor_products_vanish = False
            assert no_response_and_survival == gated_minor_products_vanish
            response_families += 1

    assert matrix_families == 9**4
    assert response_families == 9**5
    return matrix_families, response_families


def function_field_rank_2(matrix: list[list[Polynomial]]) -> int:
    if all(poly_trim(entry) == (Q(0),) for row in matrix for entry in row):
        return 0
    if poly_trim(polynomial_determinant_2(matrix)) != (Q(0),):
        return 2
    return 1


def audit_coefficientwise_rank_tables() -> int:
    coefficients = tuple(map(Q, (-1, 0, 1)))
    polynomials = tuple(product(coefficients, repeat=2))
    count = 0
    for entries in product(polynomials, repeat=4):
        matrix = [[entries[0], entries[1]], [entries[2], entries[3]]]
        rank = function_field_rank_2(matrix)
        nonzero_first_coefficient = any(
            poly_trim(entry) != (Q(0),) for row in matrix for entry in row
        )
        nonzero_second_coefficient = poly_trim(polynomial_determinant_2(matrix)) != (
            Q(0),
        )
        assert (rank >= 1) == nonzero_first_coefficient
        assert (rank >= 2) == nonzero_second_coefficient
        count += 1
    assert count == 9**4

    # The function-field kernel (-t,1) of [1,t] is not a constant kernel.
    one = (Q(1),)
    t = (Q(0), Q(1))
    minus_t = (Q(0), Q(-1))
    assert poly_add(poly_multiply(one, minus_t), poly_multiply(t, one)) == (Q(0),)
    constant_kernel_coefficient_matrix = as_q_matrix([[1, 0], [0, 1]])
    assert nullspace(constant_kernel_coefficient_matrix) == []
    return count


def audit_projected_kernel_formula() -> int:
    entries = tuple(map(Q, (-1, 0, 1)))
    count = 0
    for flat in product(entries, repeat=6):
        gamma = [list(flat[:3]), list(flat[3:])]
        gamma_n = [[row[0]] for row in gamma]
        kernel = nullspace(gamma)
        projected_vectors = [vector[1:] for vector in kernel]
        projected_dimension = matrix_rank(projected_vectors)
        expected = 2 - (matrix_rank(gamma) - matrix_rank(gamma_n))
        assert projected_dimension == expected

        # Direct quotient test: c belongs to the projected kernel precisely
        # when Gamma_C c belongs to im Gamma_N.
        for c0, c1 in product(entries, repeat=2):
            c = [c0, c1]
            gamma_c = [[row[1], row[2]] for row in gamma]
            image = matvec(gamma_c, c)
            quotient_zero = solve(gamma_n, image) is not None
            projected_space = matrix_from_columns(projected_vectors, 2)
            projected_membership = solve(projected_space, c) is not None
            assert quotient_zero == projected_membership
        count += 1
    assert count == 3**6
    return count


def legal_selector_map(gamma: Matrix, l_dim: int, w_dim: int) -> Matrix:
    e_dim = len(gamma[0]) if gamma else 0
    return [
        [gamma[a * w_dim + output][source] for a in range(l_dim)]
        for output in range(w_dim)
        for source in range(e_dim)
    ]


def recovery_map(gamma: Matrix, w_dim: int) -> Matrix:
    tensor_dim = len(gamma)
    e_dim = len(gamma[0]) if gamma else 0
    rows: Matrix = []
    for output in range(w_dim):
        for source in range(e_dim):
            row = [Q(0) for _ in range(w_dim * tensor_dim)]
            for tensor_coordinate in range(tensor_dim):
                row[output * tensor_dim + tensor_coordinate] = gamma[tensor_coordinate][
                    source
                ]
            rows.append(row)
    return rows


def decomposable_basis(l_dim: int, w_dim: int) -> list[Vector]:
    tensor_dim = l_dim * w_dim
    basis: list[Vector] = []
    for selected_a in range(l_dim):
        operator = [Q(0) for _ in range(w_dim * tensor_dim)]
        for output in range(w_dim):
            tensor_coordinate = selected_a * w_dim + output
            operator[output * tensor_dim + tensor_coordinate] = Q(1)
        basis.append(operator)
    return basis


def flatten_rows(matrix: Matrix) -> Vector:
    return [entry for row in matrix for entry in row]


def audit_decomposable_obstruction_enumeration() -> int:
    values = (Q(0), Q(1))
    l_dim = w_dim = e_dim = 2
    tensor_dim = l_dim * w_dim
    d_basis = decomposable_basis(l_dim, w_dim)
    count = 0

    for gamma_flat in product(values, repeat=tensor_dim * e_dim):
        gamma = [
            list(gamma_flat[row * e_dim : (row + 1) * e_dim])
            for row in range(tensor_dim)
        ]
        rho = recovery_map(gamma, w_dim)
        ann_basis = nullspace(rho)
        legal_map = legal_selector_map(gamma, l_dim, w_dim)

        quotient_dimension = w_dim * tensor_dim - matrix_rank(
            matrix_from_columns(d_basis + ann_basis, w_dim * tensor_dim)
        )
        image_quotient_dimension = matrix_rank(rho) - matrix_rank(legal_map)
        assert quotient_dimension == image_quotient_dimension

        for p_flat in product(values, repeat=w_dim * e_dim):
            p = [list(p_flat[row * e_dim : (row + 1) * e_dim]) for row in range(w_dim)]
            p_vector = flatten_rows(p)
            kernel_condition = all(
                matvec(p, kernel_vector) == [Q(0)] * w_dim
                for kernel_vector in nullspace(gamma)
            )
            recovery_solution = solve(rho, p_vector)
            assert (recovery_solution is not None) == kernel_condition
            if recovery_solution is not None:
                recovery, _ = recovery_solution
                delta_zero = in_column_span(recovery, d_basis + ann_basis)
                legal = solve(legal_map, p_vector) is not None
                assert delta_zero == legal
            count += 1

    assert count == 2**12
    return count


def left_annihilator(matrix: Matrix) -> list[Vector]:
    return nullspace(transpose(matrix))


def dot(left: Vector, right: Vector) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def pure_profile_certificate(
    nuisance: Matrix, pure_columns: list[Vector]
) -> tuple[Vector, Vector] | None:
    annihilators = left_annihilator(nuisance)
    for y in annihilators:
        for color, pure in enumerate(pure_columns):
            pairing = dot(y, pure)
            if pairing:
                weights = [Q(0) for _ in pure_columns]
                weights[color] = Q(1) / pairing
                return y, weights
    return None


def audit_pure_profile_incidence() -> int:
    values = tuple(map(Q, (-1, 0, 1)))
    count = 0
    for entries in product(values, repeat=6):
        nuisance = [[entries[0]], [entries[1]]]
        pure_columns = [list(entries[2:4]), list(entries[4:6])]
        nuisance_rank = matrix_rank(nuisance)
        survives = any(
            matrix_rank(append_column(nuisance, pure)) > nuisance_rank
            for pure in pure_columns
        )
        certificate = pure_profile_certificate(nuisance, pure_columns)
        assert (certificate is not None) == survives
        if certificate is not None:
            y, weights = certificate
            assert matvec(transpose(nuisance), y) == [Q(0)]
            normalization = sum(
                (
                    weight * dot(y, pure)
                    for weight, pure in zip(weights, pure_columns, strict=True)
                ),
                Q(0),
            )
            assert normalization == 1
        count += 1
    assert count == 3**6
    return count


def audit_rank_one_pure_target_identity() -> int:
    # In an independent response basis, the left side of the GLD7 quotient
    # identity has columns alpha_c [d_c].  Nonzero alpha_c therefore preserve
    # both its column rank and whether a pure class survives.
    values = tuple(map(Q, (-1, 0, 1)))
    alpha = [Q(1), Q(2), Q(-1)]
    count = 0
    for entries in product(values, repeat=6):
        pure_matrix = [list(entries[:3]), list(entries[3:])]
        if matrix_rank(pure_matrix) > 1:
            continue
        quotient_target = [
            [alpha[column] * pure_matrix[row][column] for column in range(3)]
            for row in range(2)
        ]
        pure_survives = any(entry for row in pure_matrix for entry in row)
        assert matrix_rank(quotient_target) == matrix_rank(pure_matrix)
        assert (any(entry for row in quotient_target for entry in row)) == (
            pure_survives
        )
        count += 1
    assert count == 105
    return count


def audit_shared_residual_incidence() -> int:
    # Encode each target's survival table by A=[0], d=[1] (survival) or
    # A=[1], d=[0] (absorption).  Exhausting all tables verifies that using
    # one residual point for all target incidences is exactly intersection,
    # not a target-by-target choice of different points.
    target_count = 3
    residual_points = 3
    tables = 0
    for bits in product((False, True), repeat=target_count * residual_points):
        table = [
            list(bits[target * residual_points : (target + 1) * residual_points])
            for target in range(target_count)
        ]
        direct_common = any(
            all(table[target][point] for target in range(target_count))
            for point in range(residual_points)
        )
        incidence_common = False
        for point in range(residual_points):
            all_certificates = True
            for target in range(target_count):
                if table[target][point]:
                    nuisance = [[Q(0)]]
                    pure = [[Q(1)]]
                else:
                    nuisance = [[Q(1)]]
                    pure = [[Q(0)]]
                if pure_profile_certificate(nuisance, pure) is None:
                    all_certificates = False
                    break
            incidence_common |= all_certificates
        assert incidence_common == direct_common
        tables += 1
    assert tables == 2**9
    return tables


def tensor_coordinate(a: int, w: int, w_dim: int) -> int:
    return a * w_dim + w


def audit_countermodel_four() -> None:
    l_dim = w_dim = 3
    e_dim = 6
    gamma = [[Q(0) for _ in range(e_dim)] for _ in range(l_dim * w_dim)]
    gamma[tensor_coordinate(0, 0, w_dim)][0] = 1
    gamma[tensor_coordinate(0, 1, w_dim)][1] = 1
    gamma[tensor_coordinate(0, 2, w_dim)][2] = 1
    gamma[tensor_coordinate(1, 1, w_dim)][3] = 1
    gamma[tensor_coordinate(2, 2, w_dim)][4] = 1
    gamma[tensor_coordinate(0, 0, w_dim)][5] = 1
    gamma[tensor_coordinate(1, 2, w_dim)][5] = 1

    p = [[Q(0) for _ in range(e_dim)] for _ in range(w_dim)]
    for index in range(3):
        p[index][index] = 1

    assert matrix_rank(gamma) == e_dim

    nuisance_slices: list[Vector] = []
    for source in (3, 4, 5):
        for response_coordinate in range(w_dim):
            nuisance_slices.append(
                [
                    gamma[tensor_coordinate(a, response_coordinate, w_dim)][source]
                    for a in range(l_dim)
                ]
            )
    assert matrix_rank(nuisance_slices) == l_dim

    h = as_q_matrix([[1, 0, 0, 1, 1, 0]])[0]
    expected_diagonal = [Q(0) for _ in range(l_dim * w_dim)]
    for index in range(3):
        expected_diagonal[tensor_coordinate(index, index, w_dim)] = 1
    assert matvec(gamma, h) == expected_diagonal
    assert matvec(p, h) == [Q(1), Q(0), Q(0)]

    p_vector = flatten_rows(p)
    legal_map = legal_selector_map(gamma, l_dim, w_dim)
    assert solve(legal_map, p_vector) is None

    recovery = [[Q(0) for _ in range(l_dim * w_dim)] for _ in range(w_dim)]
    for index in range(3):
        recovery[index][tensor_coordinate(0, index, w_dim)] = 1
    recovery[0][tensor_coordinate(1, 2, w_dim)] = -1
    assert matmul(recovery, gamma) == p

    rho = recovery_map(gamma, w_dim)
    ann_basis = nullspace(rho)
    d_basis = decomposable_basis(l_dim, w_dim)
    assert not in_column_span(flatten_rows(recovery), d_basis + ann_basis)


def audit_countermodel_five() -> None:
    l_dim = w_dim = 2
    e_dim = 4
    gamma = [[Q(0) for _ in range(e_dim)] for _ in range(l_dim * w_dim)]
    gamma[tensor_coordinate(0, 0, w_dim)][0] = 1
    gamma[tensor_coordinate(0, 1, w_dim)][1] = 1
    gamma[tensor_coordinate(1, 0, w_dim)][2] = 1
    gamma[tensor_coordinate(1, 0, w_dim)][3] = 1

    p = [[Q(0) for _ in range(e_dim)] for _ in range(w_dim)]
    p[0][0] = 1
    p[1][1] = 1
    p_vector = flatten_rows(p)

    legal_map = legal_selector_map(gamma, l_dim, w_dim)
    legal_solution = solve(legal_map, p_vector)
    assert legal_solution is not None
    assert legal_solution[0] == [Q(1), Q(0)]

    nuisance_slices = [
        [gamma[tensor_coordinate(a, response, w_dim)][source] for a in range(l_dim)]
        for source in (2, 3)
        for response in range(w_dim)
    ]
    assert matrix_rank(nuisance_slices) == 1
    assert not in_column_span([Q(1), Q(0)], nuisance_slices)

    gamma_rest = [[row[index] for index in (0, 1, 3)] for row in gamma]
    gamma_with_u = append_column(gamma_rest, [row[2] for row in gamma])
    assert matrix_rank(gamma_with_u) == matrix_rank(gamma_rest)
    kernel = [Q(0), Q(0), Q(1), Q(-1)]
    assert matvec(gamma, kernel) == [Q(0)] * (l_dim * w_dim)
    assert kernel[2] != 0


def main() -> None:
    audit_strictness_examples()
    pointwise_count, response_count = audit_bounded_pointwise_and_response_tables()
    coefficient_count = audit_coefficientwise_rank_tables()
    projected_count = audit_projected_kernel_formula()
    obstruction_count = audit_decomposable_obstruction_enumeration()
    pure_count = audit_pure_profile_incidence()
    rank_one_count = audit_rank_one_pure_target_identity()
    shared_count = audit_shared_residual_incidence()
    audit_countermodel_four()
    audit_countermodel_five()

    print("PASS: independent selector-failure boundary audit")
    print(f"  bounded pointwise matrix families: {pointwise_count}")
    print(f"  bounded response-gated families: {response_count}")
    print(f"  coefficientwise rank tables: {coefficient_count}")
    print(f"  projected-kernel matrices: {projected_count}")
    print(f"  recovery/obstruction pairs: {obstruction_count}")
    print(f"  pure-profile quotient tables: {pure_count}")
    print(f"  rank-one pure-target tables: {rank_one_count}")
    print(f"  shared-residual incidence tables: {shared_count}")
    print("  strictness examples and both rational countermodels: exact")
    print("  physical Krenn--Gu bridge: not audited and not claimed")


if __name__ == "__main__":
    main()
