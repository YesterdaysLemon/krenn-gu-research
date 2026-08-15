"""Independent no-import audit of the fixed-pair kernel-support boundary."""

from __future__ import annotations

from itertools import combinations, permutations, product

Vector = tuple[int, ...]
Polynomial = dict[int, int]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (0, 1, -1, 0, 0, -1)
M2 = (0, 0, 0, 1, -1, -1)
D0 = (1, 1, 0, 0, -1, -1)
D1 = (1, 0, -1, 1, 0, -1)
D2 = (0, 0, 0, 0, 0, -2)
QUADRATICS = {"m1": M1, "m2": M2, "d0": D0, "d1": D1, "d2": D2}


def quadratic_polynomial(quadratic: Vector) -> Polynomial:
    """Encode a quadratic in the first four square-free variables."""
    return {
        (1 << first) | (1 << second): value
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }


def linear_polynomial(vector: Vector) -> Polynomial:
    """Encode a linear form."""
    return {1 << index: value for index, value in enumerate(vector) if value}


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, 0) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def full_coefficient(quadratic: Vector, vectors: tuple[Vector, ...]) -> int:
    """Compute [x0...x5] q times four local forms directly."""
    polynomial = quadratic_polynomial(quadratic)
    for vector in vectors:
        polynomial = square_free_multiply(polynomial, linear_polynomial(vector))
    return polynomial.get(FULL_MASK, 0)


def complementary_quartic(quadratic: Vector) -> Polynomial:
    """Build star(q) by complementing edge masks."""
    return {
        FULL_MASK ^ mask: value
        for mask, value in quadratic_polynomial(quadratic).items()
    }


def contracted_residual(quadratic: Vector, vector: Vector) -> Vector:
    """Contract star(q) and return its x4*x5 residual covector."""
    derivative: Polynomial = {}
    for mask, coefficient in complementary_quartic(quadratic).items():
        for index in range(6):
            if mask & (1 << index) and vector[index]:
                residual_mask = mask ^ (1 << index)
                derivative[residual_mask] = (
                    derivative.get(residual_mask, 0) + coefficient * vector[index]
                )
    a_mask = (1 << 4) | (1 << 5)
    return tuple(derivative.get(a_mask | (1 << index), 0) for index in range(4))


def j_form(left: Vector, right: Vector) -> int:
    """Evaluate the x4,x5 hyperbolic form."""
    return left[4] * right[5] + left[5] * right[4]


def c_tensor(first: Vector, second: Vector, third: Vector) -> Vector:
    """Build the first-four-coordinate C tensor without symbolic algebra."""
    return tuple(
        first[index] * j_form(second, third)
        + second[index] * j_form(first, third)
        + third[index] * j_form(first, second)
        for index in range(4)
    )


def dot(left: Vector, right: Vector) -> int:
    """Integer dot product."""
    return sum(x * y for x, y in zip(left, right, strict=True))


def determinant(matrix: tuple[Vector, ...]) -> int:
    """Compute a small determinant by the Leibniz formula."""
    size = len(matrix)
    total = 0
    for order in permutations(range(size)):
        inversions = sum(
            order[i] > order[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        term = product_value(matrix[row][order[row]] for row in range(size))
        total += (-1 if inversions % 2 else 1) * term
    return total


def product_value(values: object) -> int:
    """Multiply an iterable of integers."""
    result = 1
    for value in values:
        result *= int(value)
    return result


def contraction_table_audit() -> dict[str, object]:
    """Rebuild the table from edge complementation and direct multiplication."""
    h0 = (-1, 1, 1, 1)
    h1 = (1, -1, 1, 1)
    h2 = (1, -1, -1, 1)
    h2_prime = (-1, 1, -1, 1)

    def expected(side: int, a: int, b: int) -> dict[str, Vector]:
        if side == 1:
            return {
                "m1": (0, 0, 0, 0),
                "m2": tuple(a * value for value in h2),
                "d0": tuple(b * value for value in h0),
                "d1": tuple((a + b) * value for value in h1),
                "d2": (0, -2 * a, 0, 0),
            }
        return {
            "m1": tuple(a * value for value in h2_prime),
            "m2": (0, 0, 0, 0),
            "d0": tuple((a + b) * value for value in h0),
            "d1": tuple(b * value for value in h1),
            "d2": (-2 * a, 0, 0, 0),
        }

    test_vectors = (
        (1, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0),
        (0, 0, 1, 0, 0, 0),
        (0, 0, 0, 1, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
        (1, -1, 2, 0, 1, 3),
        (2, 1, -1, 3, -2, 1),
    )
    coefficient_checks = 0
    determinant_checks = 0
    for a in range(-3, 4):
        for b in range(-3, 4):
            if a == b == 0:
                continue
            for side in (1, 2):
                kernel = (a, 0, b, a + b, 0, 0) if side == 1 else (
                    0, a, b, a + b, 0, 0
                )
                table = expected(side, a, b)
                for name, quadratic in QUADRATICS.items():
                    actual = contracted_residual(quadratic, kernel)
                    assert actual == table[name], (side, a, b, name, actual, table[name])
                    for first in test_vectors:
                        for second in test_vectors:
                            for third in test_vectors:
                                direct = full_coefficient(
                                    quadratic, (kernel, first, second, third)
                                )
                                factored = dot(actual, c_tensor(first, second, third))
                                assert direct == factored
                                coefficient_checks += 1
                mixed = "m2" if side == 1 else "m1"
                columns = (table[mixed], table["d0"], table["d1"], table["d2"])
                matrix = tuple(tuple(columns[column][row] for column in range(4)) for row in range(4))
                assert determinant(matrix) == 8 * a * a * b * (a + b)
                determinant_checks += 1
    return {
        "integer_parameter_pairs": 48,
        "determinants": determinant_checks,
        "direct_coefficients": coefficient_checks,
    }


def inverse(value: int, prime: int) -> int:
    """Return a nonzero modular inverse."""
    return pow(value % prime, prime - 2, prime)


def rank_mod(rows: list[Vector], width: int, prime: int) -> int:
    """Compute matrix rank with custom modular row reduction."""
    matrix = [[value % prime for value in row] for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next((
            row for row in range(pivot_row, len(matrix))
            if matrix[row][column] % prime
        ), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scalar = inverse(matrix[pivot_row][column], prime)
        matrix[pivot_row] = [value * scalar % prime for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            scalar = matrix[row][column] % prime
            if scalar:
                matrix[row] = [
                    (matrix[row][index] - scalar * matrix[pivot_row][index]) % prime
                    for index in range(width)
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def projective_pairs(prime: int) -> tuple[tuple[int, int], ...]:
    """Return normalized representatives of P^1(F_p)."""
    return tuple((1, slope) for slope in range(prime)) + ((0, 1),)


def modular_kernel_audit() -> dict[int, dict[str, int]]:
    """Check all projective kernel directions with custom row reduction."""
    ledger: dict[int, dict[str, int]] = {}
    for prime in (5, 7, 11):
        generic = exceptional = 0
        for a, b in projective_pairs(prime):
            for side in (1, 2):
                kernel = (a, 0, b, a + b, 0, 0) if side == 1 else (
                    0, a, b, a + b, 0, 0
                )
                table = {
                    name: tuple(value % prime for value in contracted_residual(q, kernel))
                    for name, q in QUADRATICS.items()
                }
                mixed = "m2" if side == 1 else "m1"
                rows = [table[name] for name in (mixed, "d0", "d1", "d2")]
                is_generic = a * b * (a + b) % prime != 0
                assert (rank_mod(rows, 4, prime) == 4) == is_generic
                if is_generic:
                    generic += 1
                else:
                    exceptional += 1
                    zero_channel = (
                        "d2" if a % prime == 0
                        else ("d0" if side == 1 else "d1") if b % prime == 0
                        else ("d1" if side == 1 else "d0")
                    )
                    assert table[zero_channel] == (0, 0, 0, 0)
        ledger[prime] = {
            "directions_per_side": prime + 1,
            "generic_both_sides": generic,
            "exceptional_both_sides": exceptional,
        }
    return ledger


def projective_a_states(prime: int) -> tuple[tuple[int, int], ...]:
    """Return zero plus a direct affine-chart list of P^1(F_p)."""
    return ((0, 0),) + projective_pairs(prime)


def modular_j(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate the A-form modulo a prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def a_level_audit(prime: int = 11) -> dict[str, int]:
    """Independently exhaust compatible projective A-arrays."""
    states = projective_a_states(prime)
    arrays = tuple(product(states, repeat=3))

    def pair_ok(first: object, second: object) -> bool:
        return all(
            i == j or modular_j(first[i], second[j], prime) == 0
            for i in range(3)
            for j in range(3)
        )

    neighbours = tuple(
        tuple(index for index, second in enumerate(arrays) if pair_ok(first, second))
        for first in arrays
    )
    neighbour_sets = tuple(set(indices) for indices in neighbours)
    compatible_count = 0
    two_active_count = 0
    for first_index, first in enumerate(arrays):
        for second_index in neighbours[first_index]:
            second = arrays[second_index]
            for third_index in neighbour_sets[first_index].intersection(
                neighbour_sets[second_index]
            ):
                third = arrays[third_index]
                compatible_count += 1
                active = [
                    colour for colour in range(3)
                    if (
                        modular_j(first[colour], second[colour], prime)
                        or modular_j(first[colour], third[colour], prime)
                        or modular_j(second[colour], third[colour], prime)
                    )
                ]
                assert len(active) <= 2
                if len(active) == 2:
                    two_active_count += 1
                    inactive = next(colour for colour in range(3) if colour not in active)
                    assert first[inactive] == second[inactive] == third[inactive] == (0, 0)
    return {
        "prime": prime,
        "states": len(states),
        "mode_arrays": len(arrays),
        "compatible_triples": compatible_count,
        "two_active_triples": two_active_count,
    }


def finite_union_rank_audit(prime: int = 5) -> dict[str, int]:
    """Stress the generic-support-one rank consequence over a finite field."""
    directions = projective_pairs(prime)
    generic = tuple(
        direction for direction in directions
        if direction[0] * direction[1] * sum(direction) % prime
    )
    full_rank_maps = 0
    false_covers = 0
    for entries in product(range(prime), repeat=6):
        rows = [entries[0:2], entries[2:4], entries[4:6]]
        if rank_mod([tuple(row) for row in rows], 2, prime) != 2:
            continue
        full_rank_maps += 1
        images = [
            tuple(sum(row[j] * direction[j] for j in range(2)) % prime for row in rows)
            for direction in generic
        ]
        if all(sum(value != 0 for value in image) == 1 for image in images):
            false_covers += 1
    assert false_covers == 0
    return {
        "prime": prime,
        "generic_directions": len(generic),
        "full_rank_maps": full_rank_maps,
        "false_coordinate_line_covers": false_covers,
    }


def main() -> None:
    """Run the independent audit."""
    contractions = contraction_table_audit()
    kernels = modular_kernel_audit()
    a_level = a_level_audit()
    finite_union = finite_union_rank_audit()

    print("fixed-pair kernel-support boundary independent audit: PASS")
    print(f"  edge-complement contraction replay: {contractions}")
    print(f"  projective kernel ranks: {kernels}")
    print(f"  A-level F_11 exhaustion: {a_level}")
    print(f"  finite-union rank stress: {finite_union}")


if __name__ == "__main__":
    main()
