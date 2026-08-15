"""Independent no-import audit of the exceptional-kernel necessity theorem."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import permutations, product

Vector = tuple[Fraction, ...]


def add(*vectors: Vector) -> Vector:
    """Add rational vectors coordinatewise."""
    return tuple(sum((vector[i] for vector in vectors), Fraction(0)) for i in range(6))


def scale(value: int | Fraction, vector: Vector) -> Vector:
    """Scale a rational vector."""
    return tuple(Fraction(value) * entry for entry in vector)


def evaluate(covector: Vector, vector: Vector) -> Fraction:
    """Evaluate a covector on a vector."""
    return sum((x * y for x, y in zip(covector, vector, strict=True)), Fraction(0))


def polarized_product(factors: tuple[Vector, ...], vectors: tuple[Vector, ...]) -> Fraction:
    """Evaluate a four-factor polarization by an independent permanent route."""
    total = Fraction(0)
    for order in permutations(range(4)):
        term = Fraction(1)
        for row, column in enumerate(order):
            term *= evaluate(factors[row], vectors[column])
        total += term
    return total


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    """Compute a determinant by exact Gaussian elimination."""
    work = [row[:] for row in matrix]
    size = len(work)
    value = Fraction(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        pivot_value = work[column][column]
        value *= pivot_value
        for entry in range(column, size):
            work[column][entry] /= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column]
            for entry in range(column, size):
                work[row][entry] -= factor * work[column][entry]
    return value


def coordinate(index: int) -> Vector:
    """Return a coordinate covector/vector."""
    return tuple(Fraction(i == index) for i in range(6))


def fixed_quartics() -> dict[str, tuple[Fraction, tuple[Vector, ...]]]:
    """Build the quartics without importing repository code."""
    x0, x1, x2, x3, x4, x5 = (coordinate(i) for i in range(6))
    return {
        "m1": (Fraction(1), (x4, x5, x1, add(x3, scale(-1, x2), scale(-1, x0)))),
        "m2": (Fraction(1), (x4, x5, x0, add(x3, scale(-1, x2), scale(-1, x1)))),
        "d0": (Fraction(1), (x4, x5, add(x1, x2), add(x3, scale(-1, x0)))),
        "d1": (Fraction(1), (x4, x5, add(x0, x2), add(x3, scale(-1, x1)))),
        "d2": (Fraction(-2), (x4, x5, x0, x1)),
    }


def residual_column(
    quartic: tuple[Fraction, tuple[Vector, ...]],
    kernel_vector: Vector,
) -> list[Fraction]:
    """Extract the four residual coefficients using C(e_i,e4,e5)=e_i."""
    coefficient, factors = quartic
    return [
        coefficient * polarized_product(
            factors,
            (kernel_vector, coordinate(i), coordinate(4), coordinate(5)),
        )
        for i in range(4)
    ]


def audit_contraction_determinants() -> dict[str, object]:
    """Derive residual columns directly and check the determinant formula."""
    quartics = fixed_quartics()
    samples = (
        (1, 1),
        (2, 3),
        (-1, 2),
        (Fraction(3, 2), Fraction(-5, 3)),
        (0, 1),
        (1, 0),
        (1, -1),
    )
    checked = 0
    nonzero = 0
    for side, mixed in ((1, "m2"), (2, "m1")):
        for a, b in samples:
            if side == 1:
                kernel = (Fraction(a), 0, Fraction(b), Fraction(a + b), 0, 0)
            else:
                kernel = (0, Fraction(a), Fraction(b), Fraction(a + b), 0, 0)
            columns = [
                residual_column(quartics[name], kernel)
                for name in (mixed, "d0", "d1", "d2")
            ]
            matrix = [[columns[column][row] for column in range(4)] for row in range(4)]
            actual = determinant(matrix)
            expected = 8 * Fraction(a) ** 2 * Fraction(b) * Fraction(a + b)
            assert actual == expected, (side, a, b, actual, expected)
            checked += 1
            nonzero += int(bool(actual))
    return {
        "exact_parameter_samples": checked,
        "nonzero_generic_determinants": nonzero,
        "exceptional_zero_determinants": checked - nonzero,
    }


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    """Compute matrix rank modulo an odd prime."""
    work = [[value % prime for value in row] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], prime - 2, prime)
        work[row] = [(inverse * value) % prime for value in work[row]]
        for i in range(len(work)):
            if i == row:
                continue
            factor = work[i][column]
            work[i] = [
                (value - factor * pivot_value) % prime
                for value, pivot_value in zip(work[i], work[row], strict=True)
            ]
        row += 1
        if row == len(work):
            break
    return row


def j_mod(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate the hyperbolic pairing modulo prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def audit_orthogonality_core(prime: int) -> dict[str, int]:
    """Exhaust the common-orthogonal-line step over a small odd field."""
    vectors = tuple(product(range(prime), repeat=2))
    nonzero_vectors = tuple(vector for vector in vectors if vector != (0, 0))
    endpoint_pairs = 0
    orthogonal_pairs = 0
    for first in nonzero_vectors:
        for second in nonzero_vectors:
            if not j_mod(first, second, prime):
                continue
            endpoint_pairs += 1
            common = [
                vector
                for vector in vectors
                if not j_mod(first, vector, prime) and not j_mod(second, vector, prime)
            ]
            for left in common:
                for right in common:
                    assert rank_mod([list(left), list(right)], prime) <= 1
                    orthogonal_pairs += 1
    return {
        "nonzero_endpoint_pairs": endpoint_pairs,
        "common_orthogonal_vector_pairs": orthogonal_pairs,
    }


def main() -> None:
    """Run the independent exact audit."""
    report = {
        "contraction_audit": audit_contraction_determinants(),
        "orthogonality_F3": audit_orthogonality_core(3),
        "orthogonality_F5": audit_orthogonality_core(5),
        "implementation": "stdlib-only; no repository imports",
        "scope": "finite fields audit identities; theorem proof is characteristic zero",
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
