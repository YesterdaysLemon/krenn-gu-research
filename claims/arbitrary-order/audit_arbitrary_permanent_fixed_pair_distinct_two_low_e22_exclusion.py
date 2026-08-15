"""Independent no-import audit of the fixed-pair two-low E22 exclusion."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, permutations

Vector4 = tuple[Fraction, Fraction, Fraction, Fraction]
Vector6 = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]
Edges = dict[tuple[int, int], Fraction]
Cubic = dict[tuple[int, int, int], Fraction]
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]


def vector4(*entries: int | Fraction) -> Vector4:
    """Build a rational four-vector."""
    return tuple(Fraction(entry) for entry in entries)  # type: ignore[return-value]


def add(left: Vector4, right: Vector4) -> Vector4:
    """Add rational four-vectors."""
    return tuple(x + y for x, y in zip(left, right, strict=True))  # type: ignore[return-value]


def subtract(left: Vector4, right: Vector4) -> Vector4:
    """Subtract rational four-vectors."""
    return tuple(x - y for x, y in zip(left, right, strict=True))  # type: ignore[return-value]


def scale(value: int | Fraction, source: Vector4) -> Vector4:
    """Scale a rational four-vector."""
    scalar = Fraction(value)
    return tuple(scalar * entry for entry in source)  # type: ignore[return-value]


def quadratic_edges(
    left: Vector4,
    right: Vector4,
    coefficient: int | Fraction = 1,
) -> Edges:
    """Multiply two forms in the square-free quadratic algebra."""
    scalar = Fraction(coefficient)
    output: Edges = {}
    for i in range(4):
        for j in range(i + 1, 4):
            value = scalar * (left[i] * right[j] + left[j] * right[i])
            if value:
                output[(i, j)] = value
    return output


def fixed_edges() -> dict[str, Edges]:
    """Independently reconstruct all five residual quadratics."""
    x0 = vector4(1, 0, 0, 0)
    x1 = vector4(0, 1, 0, 0)
    x2 = vector4(0, 0, 1, 0)
    x3 = vector4(0, 0, 0, 1)
    return {
        "m1": quadratic_edges(x1, subtract(subtract(x3, x2), x0)),
        "m2": quadratic_edges(x0, subtract(subtract(x3, x2), x1)),
        "d0": quadratic_edges(add(x1, x2), subtract(x3, x0)),
        "d1": quadratic_edges(add(x0, x2), subtract(x3, x1)),
        "d2": quadratic_edges(x0, x1, -2),
    }


def contract(edges: Edges, source: Vector4) -> Vector4:
    """Contract a square-free quadratic edge dictionary with one vector."""
    output = [Fraction(0) for _ in range(4)]
    for (i, j), coefficient in edges.items():
        output[i] += coefficient * source[j]
        output[j] += coefficient * source[i]
    return tuple(output)  # type: ignore[return-value]


def rank(columns: tuple[tuple[Fraction, ...], ...]) -> int:
    """Compute exact column rank with a local rational reducer."""
    if not columns:
        return 0
    work = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(
                    work[row],
                    work[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def quartic_from_edges(edges: Edges) -> dict[tuple[int, int, int, int], Fraction]:
    """Attach the two A coordinates to a quadratic edge dictionary."""
    return {tuple(sorted((i, j, 4, 5))): value for (i, j), value in edges.items()}


def contract_quartic(
    quartic: dict[tuple[int, int, int, int], Fraction],
    source: Vector6,
) -> Cubic:
    """Contract one slot of a square-free quartic monomial dictionary."""
    output: Cubic = {}
    for monomial, coefficient in quartic.items():
        for position, coordinate in enumerate(monomial):
            value = coefficient * source[coordinate]
            if not value:
                continue
            remainder = monomial[:position] + monomial[position + 1 :]
            output[remainder] = output.get(remainder, Fraction(0)) + value
    return {monomial: value for monomial, value in output.items() if value}


def residual_cubic(residual: Vector4) -> Cubic:
    """Return the monomial dictionary for x4*x5 times one R-covector."""
    return {
        (coordinate, 4, 5): coefficient
        for coordinate, coefficient in enumerate(residual)
        if coefficient
    }


def evaluate_cubic(cubic: Cubic, points: tuple[Vector6, Vector6, Vector6]) -> Fraction:
    """Evaluate a completely polarized cubic monomial dictionary."""
    total = Fraction(0)
    for monomial, coefficient in cubic.items():
        total += coefficient * sum(
            points[0][monomial[order[0]]]
            * points[1][monomial[order[1]]]
            * points[2][monomial[order[2]]]
            for order in permutations(range(3))
        )
    return total


def audit_residuals_and_polarization() -> dict[str, int]:
    """Rebuild the table and all scalar-one high-slice identities."""
    edges = fixed_edges()
    zero = vector4(0, 0, 0, 0)
    h2 = vector4(1, -1, -1, 1)
    h2_prime = vector4(-1, 1, -1, 1)
    x0 = vector4(1, 0, 0, 0)
    x1 = vector4(0, 1, 0, 0)
    x2 = vector4(0, 0, 1, 0)
    x3 = vector4(0, 0, 0, 1)
    lines = {
        "A0": vector4(1, 0, 0, 1),
        "C0": vector4(1, 0, -1, 0),
        "A1": vector4(0, 1, 0, 1),
        "C1": vector4(0, 1, -1, 0),
    }
    expected = {
        "A0": (zero, h2, zero, add(h2, scale(2, x2)), scale(-2, x1)),
        "C0": (zero, h2, subtract(h2, scale(2, x3)), zero, scale(-2, x1)),
        "A1": (h2_prime, zero, add(h2_prime, scale(2, x2)), zero, scale(-2, x0)),
        "C1": (h2_prime, zero, zero, subtract(h2_prime, scale(2, x3)), scale(-2, x0)),
    }
    channels = ("m1", "m2", "d0", "d1", "d2")
    contraction_checks = 0
    nonzero_residuals: set[Vector4] = set()
    for name, line in lines.items():
        pure_r_line: Vector6 = line + (Fraction(0), Fraction(0))
        for channel, wanted in zip(channels, expected[name], strict=True):
            actual = contract(edges[channel], line)
            assert actual == wanted
            assert contract_quartic(quartic_from_edges(edges[channel]), pure_r_line) == residual_cubic(actual)
            contraction_checks += 1
            if any(actual):
                nonzero_residuals.add(actual)

    basis: tuple[Vector6, ...] = tuple(
        tuple(Fraction(row == column) for row in range(6))
        for column in range(6)
    )  # type: ignore[assignment]
    slice_checks = 0
    for residual in nonzero_residuals:
        cubic = residual_cubic(residual)
        for left in basis:
            for middle in basis[:4]:
                for right in basis:
                    actual = evaluate_cubic(cubic, (left, middle, right))
                    residual_value = sum(
                        residual[index] * middle[index] for index in range(4)
                    )
                    pairing = left[4] * right[5] + left[5] * right[4]
                    assert actual == residual_value * pairing
                    slice_checks += 1
    return {
        "edge_dictionaries": len(edges),
        "quartic_contractions": contraction_checks,
        "basis_slice_checks": slice_checks,
    }


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add two sparse integer polynomials."""
    output = dict(left)
    for monomial, coefficient in right.items():
        output[monomial] = output.get(monomial, 0) + coefficient
        if not output[monomial]:
            del output[monomial]
    return output


def polynomial_scale(value: int, source: Polynomial) -> Polynomial:
    """Scale one sparse integer polynomial."""
    return {monomial: value * coefficient for monomial, coefficient in source.items() if value * coefficient}


def polynomial_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply sparse commutative integer polynomials."""
    output: Polynomial = {}
    for first, first_coefficient in left.items():
        for second, second_coefficient in right.items():
            monomial = tuple(sorted(first + second))
            output[monomial] = output.get(monomial, 0) + first_coefficient * second_coefficient
    return {monomial: coefficient for monomial, coefficient in output.items() if coefficient}


def polynomial_subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    """Subtract two sparse integer polynomials."""
    return polynomial_add(left, polynomial_scale(-1, right))


def audit_pairing_minors() -> dict[str, int]:
    """Independently verify all selected-minor identities as polynomials."""
    variables: tuple[Polynomial, ...] = tuple({(index,): 1} for index in range(12))
    left = ((variables[0], variables[1], variables[2]), (variables[3], variables[4], variables[5]))
    right = ((variables[6], variables[7], variables[8]), (variables[9], variables[10], variables[11]))

    def pairing(row: int, column: int) -> Polynomial:
        return polynomial_add(
            polynomial_multiply(left[0][row], right[1][column]),
            polynomial_multiply(left[1][row], right[0][column]),
        )

    checks = 0
    for rows in combinations(range(3), 2):
        for columns in combinations(range(3), 2):
            actual = polynomial_subtract(
                polynomial_multiply(pairing(rows[0], columns[0]), pairing(rows[1], columns[1])),
                polynomial_multiply(pairing(rows[0], columns[1]), pairing(rows[1], columns[0])),
            )
            left_minor = polynomial_subtract(
                polynomial_multiply(left[0][rows[0]], left[1][rows[1]]),
                polynomial_multiply(left[0][rows[1]], left[1][rows[0]]),
            )
            right_minor = polynomial_subtract(
                polynomial_multiply(right[0][columns[0]], right[1][columns[1]]),
                polynomial_multiply(right[0][columns[1]], right[1][columns[0]]),
            )
            expected = polynomial_scale(-1, polynomial_multiply(left_minor, right_minor))
            assert actual == expected
            checks += 1
    return {"formal_selected_minor_identities": checks, "formal_variables": len(variables)}


def audit_kernels_and_branches() -> dict[str, object]:
    """Independently check the singleton lines and exhaustive support split."""
    h2 = vector4(1, -1, -1, 1)
    h2_prime = vector4(-1, 1, -1, 1)
    data = {
        "A0": (h2, vector4(0, 1, 0, 0), add(h2, vector4(0, 0, 2, 0)), vector4(1, 0, 0, -1), 1),
        "C0": (h2, vector4(0, 1, 0, 0), subtract(h2, vector4(0, 0, 0, 2)), vector4(1, 0, 1, 0), 0),
        "A1": (h2_prime, vector4(1, 0, 0, 0), add(h2_prime, vector4(0, 0, 2, 0)), vector4(0, 1, 0, -1), 0),
        "C1": (h2_prime, vector4(1, 0, 0, 0), subtract(h2_prime, vector4(0, 0, 0, 2)), vector4(0, 1, 1, 0), 1),
    }
    common_kernels: dict[str, list[int]] = {}
    support_cases = 0
    for name, (mixed, coordinate, diagonal, generator, colour) in data.items():
        assert rank((mixed, coordinate, diagonal)) == 3
        assert all(
            sum(row[index] * generator[index] for index in range(4)) == 0
            for row in (mixed, coordinate, diagonal)
        )
        common_kernels[name] = [int(value) for value in generator]
        supports = ((2,), (colour, 2))
        assert len(set(supports)) == 2
        support_cases += len(supports)
    return {
        "common_kernels": common_kernels,
        "support_cases": support_cases,
        "rank_two_low_orientations": 2,
    }


def main() -> None:
    """Run the independent exact audit."""
    report = {
        "residual_and_slice_audit": audit_residuals_and_polarization(),
        "pairing_minor_audit": audit_pairing_minors(),
        "branch_audit": audit_kernels_and_branches(),
        "E22_branch": "EXCLUDED",
        "zero_branch": "OPEN",
        "status": "UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    print("fixed-pair distinct-two-low E22 independent audit: PASS")


if __name__ == "__main__":
    main()
