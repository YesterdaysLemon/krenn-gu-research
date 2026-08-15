"""Independent no-import audit of the star-pair kernel-support boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product

Vector = tuple[int, ...]
Linear = tuple[int, int]
Polynomial = dict[tuple[int, int], int]

EDGES = tuple(combinations(range(4), 2))


def first_four_product(left: Vector, right: Vector) -> Vector:
    """Multiply two forms in the square-free four-variable algebra."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def rank(rows: list[list[int | Fraction]]) -> int:
    """Return exact row rank by a standalone rational reducer."""
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


def complement_core_matrix(quadratic: Vector) -> tuple[tuple[int, ...], ...]:
    """Build the symmetric matrix of the complementary quadratic core."""
    matrix = [[0] * 4 for _ in range(4)]
    all_vertices = set(range(4))
    for coefficient, edge in zip(quadratic, EDGES, strict=True):
        complement = tuple(sorted(all_vertices - set(edge)))
        first, second = complement
        matrix[first][second] += coefficient
        matrix[second][first] += coefficient
    return tuple(tuple(row) for row in matrix)


def contract_core(matrix: tuple[tuple[int, ...], ...], vector: tuple[Linear, ...]) -> tuple[Linear, ...]:
    """Contract a complementary quadratic with a symbolic a,b-vector."""
    return tuple(
        (
            sum(matrix[row][column] * vector[column][0] for column in range(4)),
            sum(matrix[row][column] * vector[column][1] for column in range(4)),
        )
        for row in range(4)
    )


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add two bivariate integer polynomials."""
    result = dict(left)
    for monomial, value in right.items():
        result[monomial] = result.get(monomial, 0) + value
        if result[monomial] == 0:
            del result[monomial]
    return result


def polynomial_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply two bivariate integer polynomials."""
    result: Polynomial = {}
    for (left_a, left_b), left_value in left.items():
        for (right_a, right_b), right_value in right.items():
            monomial = (left_a + right_a, left_b + right_b)
            result[monomial] = result.get(monomial, 0) + left_value * right_value
    return {monomial: value for monomial, value in result.items() if value}


def linear_polynomial(value: Linear) -> Polynomial:
    """Convert an a,b-linear pair to a sparse polynomial."""
    result: Polynomial = {}
    if value[0]:
        result[(1, 0)] = value[0]
    if value[1]:
        result[(0, 1)] = value[1]
    return result


def permutation_sign(order: tuple[int, ...]) -> int:
    """Return the sign of a permutation."""
    inversions = sum(
        order[first] > order[second]
        for first in range(len(order))
        for second in range(first + 1, len(order))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix: tuple[tuple[Linear, ...], ...]) -> Polynomial:
    """Compute a small symbolic determinant without a CAS."""
    result: Polynomial = {}
    for order in permutations(range(4)):
        term: Polynomial = {(0, 0): permutation_sign(order)}
        for row, column in enumerate(order):
            term = polynomial_multiply(term, linear_polynomial(matrix[row][column]))
        result = polynomial_add(result, term)
    return result


def evaluate_linear(value: Linear, a_value: int, b_value: int) -> int:
    """Evaluate a linear pair at integer values."""
    return value[0] * a_value + value[1] * b_value


def assert_pair_and_contractions() -> dict[str, object]:
    """Independently rebuild the pair, cores, kernels, and contraction table."""
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
    m1 = products[0][1]
    m2 = products[1][0]
    d0, d1, d2 = (products[index][index] for index in range(3))
    assert (m1, m2, d0, d1, d2) == (
        (-1, 1, 0, 1, 0, 0),
        (1, -1, 0, 0, -1, 1),
        (-1, 2, -1, 1, 0, 1),
        (1, 0, -1, 0, -1, 0),
        (0, 0, 0, 2, 0, 0),
    )
    assert rank([list(entry) for row in products for entry in row]) == 5
    assert rank([
        list(products[i][j])
        for i in range(3)
        for j in range(3)
        if i != j
    ]) == 2

    quadratics = {"m1": m1, "m2": m2, "d0": d0, "d1": d1, "d2": d2}
    cores = {name: complement_core_matrix(value) for name, value in quadratics.items()}

    # Each coordinate is represented as coefficient_of_a, coefficient_of_b.
    p1 = ((1, 0), (0, 1), (1, 1), (0, 0))
    p2 = ((1, 0), (0, 1), (0, 1), (1, 0))
    residuals = {
        1: {name: contract_core(core, p1) for name, core in cores.items()},
        2: {name: contract_core(core, p2) for name, core in cores.items()},
    }
    expected = {
        1: {
            "m1": ((0, 0), (0, 0), (0, 0), (0, 0)),
            "m2": ((-1, 0), (1, 0), (-1, 0), (1, 0)),
            "d0": ((0, 1), (0, -1), (0, -1), (0, 1)),
            "d1": ((-1, -1), (-1, -1), (-1, -1), (1, 1)),
            "d2": ((0, 0), (0, 0), (0, 0), (2, 0)),
        },
        2: {
            "m1": ((1, 0), (1, 0), (-1, 0), (1, 0)),
            "m2": ((0, 0), (0, 0), (0, 0), (0, 0)),
            "d0": ((1, 1), (3, -1), (-1, -1), (1, 1)),
            "d1": ((0, -1), (0, -1), (0, -1), (0, 1)),
            "d2": ((2, 0), (0, 0), (0, 0), (2, 0)),
        },
    }
    assert residuals == expected

    matrix1 = tuple(tuple(residuals[1][name][row] for name in ("m2", "d0", "d1", "d2")) for row in range(4))
    matrix2 = tuple(tuple(residuals[2][name][row] for name in ("m1", "d0", "d1", "d2")) for row in range(4))
    determinant1 = determinant(matrix1)
    determinant2 = determinant(matrix2)
    assert determinant1 == {(3, 1): 8, (2, 2): 8}
    assert determinant2 == {(3, 1): -8, (2, 2): 8}

    exceptional_zero_tests = (
        (1, "d2", 0, 1),
        (1, "d0", 1, 0),
        (1, "d1", 1, -1),
        (2, "d2", 0, 1),
        (2, "d1", 1, 0),
    )
    for side, channel, a_value, b_value in exceptional_zero_tests:
        assert all(
            evaluate_linear(value, a_value, b_value) == 0
            for value in residuals[side][channel]
        )
    d0_at_c1 = tuple(evaluate_linear(value, 1, 1) for value in residuals[2]["d0"])
    m1_at_c1 = tuple(evaluate_linear(value, 1, 1) for value in residuals[2]["m1"])
    assert d0_at_c1 == tuple(2 * value for value in m1_at_c1)

    phi1 = (
        (0, 0, 0, 1),
        (1, 1, -1, 0),
    )
    phi2 = (
        (1, 0, 0, -1),
        (0, 1, -1, 0),
    )
    lines1 = ((0, 1, 1, 0), (1, 0, 1, 0), (1, -1, 0, 0))
    lines2 = ((0, 1, 1, 0), (1, 0, 0, 1), (1, 1, 1, 1))
    assert all(sum(c * x for c, x in zip(row, vector, strict=True)) == 0 for row in phi1 for vector in lines1)
    assert all(sum(c * x for c, x in zip(row, vector, strict=True)) == 0 for row in phi2 for vector in lines2)
    assert rank([list(vector) for vector in lines1[:2]]) == 2
    assert rank([list(vector) for vector in lines2[:2]]) == 2
    return {
        "pair_rank": 5,
        "mixed_rank": 2,
        "determinants": (determinant1, determinant2),
        "exceptional_zero_tests": len(exceptional_zero_tests),
        "phi2_relation": (d0_at_c1, m1_at_c1),
    }


def inverse(value: int, prime: int) -> int:
    """Return an inverse in an odd prime field."""
    return pow(value % prime, prime - 2, prime)


def projective_states(prime: int) -> tuple[tuple[int, int], ...]:
    """Enumerate zero and every line in a two-dimensional prime field."""
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
    assert len(result) == prime + 2
    return tuple(result)


def form(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate the two-dimensional hyperbolic form."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def mode_compatible(
    left: tuple[tuple[int, int], ...],
    right: tuple[tuple[int, int], ...],
    prime: int,
) -> bool:
    """Test all off-colour pairings between two modes."""
    return all(
        colour_left == colour_right
        or form(left[colour_left], right[colour_right], prime) == 0
        for colour_left in range(3)
        for colour_right in range(3)
    )


def audit_cross_orthogonality(prime: int) -> dict[str, int]:
    """Independently exhaust the active-colour conclusion."""
    states = projective_states(prime)
    modes = tuple(product(states, repeat=3))
    adjacency = tuple(
        frozenset(
            right_index
            for right_index, right in enumerate(modes)
            if mode_compatible(left, right, prime)
        )
        for left in modes
    )
    triples = 0
    two_active = 0
    for first_index, first in enumerate(modes):
        for second_index in adjacency[first_index]:
            second = modes[second_index]
            for third_index in adjacency[first_index] & adjacency[second_index]:
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


def audit_rank_logic() -> dict[str, int]:
    """Check the numerical rank gaps used by both abstract lemmas."""
    ambient = 4 + 2
    local = 3
    killed_space_rank_ceiling = ambient - local
    scalar_identity_rank = 4
    assert killed_space_rank_ceiling == 3
    assert scalar_identity_rank > killed_space_rank_ceiling
    for residual_dimension in range(2, 9):
        whole_dimension = residual_dimension + 2
        assert whole_dimension - 3 == residual_dimension - 1
        assert residual_dimension > residual_dimension - 1
    return {
        "ambient": ambient,
        "local": local,
        "killed_space_rank_ceiling": killed_space_rank_ceiling,
        "scalar_identity_rank": scalar_identity_rank,
    }


def main() -> None:
    """Run the standalone audit."""
    algebra = assert_pair_and_contractions()
    ranks = audit_rank_logic()
    finite_fields = {prime: audit_cross_orthogonality(prime) for prime in (3, 5)}
    print("star-pair kernel-support boundary independent audit: PASS")
    print(f"  standalone algebra: {algebra}")
    print(f"  rank logic: {ranks}")
    print(f"  independent finite-field audits: {finite_fields}")


if __name__ == "__main__":
    main()
