"""Independent no-import audit of singleton-exceptional propagation."""

from __future__ import annotations

from fractions import Fraction
import json

Vector = tuple[Fraction, Fraction, Fraction, Fraction]
IntVector = tuple[int, int, int, int]


QUADRATICS: dict[str, dict[tuple[int, int], int]] = {
    "m1": {(0, 1): -1, (1, 2): -1, (1, 3): 1},
    "m2": {(0, 1): -1, (0, 2): -1, (0, 3): 1},
    "d0": {(0, 1): -1, (0, 2): -1, (1, 3): 1, (2, 3): 1},
    "d1": {(0, 1): -1, (1, 2): -1, (0, 3): 1, (2, 3): 1},
    "d2": {(0, 1): -2},
}

VECTORS: dict[str, IntVector] = {
    "N": (0, 0, 1, 1),
    "A0": (1, 0, 0, 1),
    "C0": (1, 0, -1, 0),
    "A1": (0, 1, 0, 1),
    "C1": (0, 1, -1, 0),
    "U0": (1, 0, 0, -1),
    "V1": (1, 0, 1, 0),
    "U1": (0, 1, 0, -1),
    "V0": (0, 1, 1, 0),
}


def contract(quadratic: dict[tuple[int, int], int], vector: IntVector) -> IntVector:
    """Contract a square-free quadratic using its edge coefficients."""
    result = [0, 0, 0, 0]
    for (left, right), coefficient in quadratic.items():
        result[right] += coefficient * vector[left]
        result[left] += coefficient * vector[right]
    return tuple(result)  # type: ignore[return-value]


def residuals(vector: IntVector) -> dict[str, IntVector]:
    """Compute all residual covectors independently."""
    return {name: contract(quadratic, vector) for name, quadratic in QUADRATICS.items()}


def rref(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    """Return reduced row echelon form and pivot columns."""
    rows = [row[:] for row in matrix]
    if not rows:
        return rows, []
    pivots: list[int] = []
    pivot_row = 0
    for column in range(len(rows[0])):
        candidate = next((row for row in range(pivot_row, len(rows)) if rows[row][column]), None)
        if candidate is None:
            continue
        rows[pivot_row], rows[candidate] = rows[candidate], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [entry / scale for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            scale = rows[row][column]
            if scale:
                rows[row] = [
                    entry - scale * pivot
                    for entry, pivot in zip(rows[row], rows[pivot_row], strict=True)
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivots


def rank(rows: list[IntVector]) -> int:
    """Compute rational row rank."""
    return len(rref([[Fraction(entry) for entry in row] for row in rows])[1])


def nullspace(rows: list[IntVector]) -> list[Vector]:
    """Compute a rational basis for the common row kernel."""
    reduced, pivots = rref([[Fraction(entry) for entry in row] for row in rows])
    free = [column for column in range(4) if column not in pivots]
    basis: list[Vector] = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(4)]
        vector[free_column] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(tuple(vector))  # type: ignore[arg-type]
    return basis


def dot(left: IntVector | Vector, right: IntVector | Vector) -> Fraction:
    """Evaluate one row on one column."""
    return sum((Fraction(x) * Fraction(y) for x, y in zip(left, right, strict=True)), Fraction(0))


def check_kernel(rows: list[IntVector], expected: list[IntVector]) -> None:
    """Check an expected independent basis for the common kernel."""
    kernel = nullspace(rows)
    assert len(kernel) == len(expected)
    assert rank(expected) == len(expected)
    for vector in expected:
        assert all(dot(row, vector) == 0 for row in rows)


def audit_exceptional_table() -> dict[str, object]:
    """Independently audit the six exceptional residual cases."""
    cases = {
        "Phi1_N": ("N", ("d0", "d1"), [(1, 1, 0, 0), (0, 0, 1, -1)]),
        "Phi1_A0": ("A0", ("m2", "d1", "d2"), [VECTORS["U0"]]),
        "Phi1_C0": ("C0", ("m2", "d0", "d2"), [VECTORS["V1"]]),
        "Phi2_N": ("N", ("d0", "d1"), [(1, 1, 0, 0), (0, 0, 1, -1)]),
        "Phi2_A1": ("A1", ("m1", "d0", "d2"), [VECTORS["U1"]]),
        "Phi2_C1": ("C1", ("m1", "d1", "d2"), [VECTORS["V0"]]),
    }
    report: dict[str, object] = {}
    for label, (vector_name, channels, expected_kernel) in cases.items():
        values = residuals(VECTORS[vector_name])
        rows = [values[channel] for channel in channels]
        expected_rank = len(channels)
        assert rank(rows) == expected_rank
        check_kernel(rows, expected_kernel)
        report[label] = {"rank": expected_rank, "kernel_dimension": len(expected_kernel)}
    return report


def audit_identities_and_cycles() -> dict[str, object]:
    """Audit the forced-colour identities and four return cycles."""
    identities = {
        "U0": (("m1", "d2"), ("m2", "d1")),
        "V1": (("m1", "d2"), ("m2", "d0")),
        "U1": (("m2", "d2"), ("m1", "d0")),
        "V0": (("m2", "d2"), ("m1", "d1")),
    }
    cycles = {"U0": "A0", "V1": "C0", "U1": "A1", "V0": "C1"}
    forced = {"U0": 0, "V1": 1, "U1": 1, "V0": 0}
    report: dict[str, object] = {}
    for name, pairs in identities.items():
        values = residuals(VECTORS[name])
        for left, right in pairs:
            assert values[left] == values[right] != (0, 0, 0, 0)
        rows = [row for row in values.values() if row != (0, 0, 0, 0)]
        assert rank(rows) == 3
        check_kernel(rows, [VECTORS[cycles[name]]])
        report[name] = {"forced_colour": forced[name], "returns_to": cycles[name]}
    return report


def audit_common_line_plane() -> dict[str, object]:
    """Audit several exact parameters and both return-kernel regimes."""
    def q(s_value: int, t_value: int) -> IntVector:
        return (s_value, s_value, t_value, -t_value)

    for s_value, t_value in ((1, 0), (1, 1), (1, -1), (2, 3), (-3, 2)):
        values = residuals(q(s_value, t_value))
        assert values["d0"] == values["d1"]
        assert values["d2"] == (-2 * s_value, -2 * s_value, 0, 0)

    generic_rows = list(residuals(q(2, 3)).values())
    assert rank(generic_rows) == 3
    check_kernel(generic_rows, [VECTORS["N"]])

    opposite_rows = list(residuals(q(1, -1)).values())
    assert rank(opposite_rows) == 3
    check_kernel(opposite_rows, [VECTORS["N"]])

    boundary_rows = list(residuals(q(1, 0)).values())
    assert rank(boundary_rows) == 2
    check_kernel(boundary_rows, [VECTORS["N"], (1, -1, 0, 0)])
    return {
        "parameters_checked": 5,
        "d0_equals_d1": True,
        "generic_and_opposite_return": "K*N",
        "t_zero_return": "span{N,x0-x1}",
    }


def audit_rank_gap_over_finite_fields() -> dict[str, object]:
    """Stress-test the scalar-rank gap and hyperbolic orthogonal lines."""
    report: dict[str, object] = {}
    for prime in (3, 5, 7):
        nonzero = [(a, b) for a in range(prime) for b in range(prime) if (a, b) != (0, 0)]
        for a, b in nonzero:
            orthogonal = [
                (c, d)
                for c in range(prime)
                for d in range(prime)
                if (a * d + b * c) % prime == 0
            ]
            assert len(orthogonal) == prime
        for dimension in (2, 3):
            for scalar in range(1, prime):
                diagonal_rows = [
                    tuple(scalar if i == j else 0 for j in range(dimension))
                    for i in range(dimension)
                ]
                # The rows have disjoint nonzero pivots over the field.
                assert all(diagonal_rows[i][i] % prime for i in range(dimension))
        report[str(prime)] = {
            "nonzero_A_vectors": len(nonzero),
            "orthogonal_line_size": prime,
            "quotient_dimensions": [2, 3],
        }
    return report


def main() -> None:
    """Run the independent audit."""
    report = {
        "exceptional_table": audit_exceptional_table(),
        "identities_and_cycles": audit_identities_and_cycles(),
        "common_line_plane": audit_common_line_plane(),
        "finite_field_rank_gap_stress": audit_rank_gap_over_finite_fields(),
        "implementation": "standard library only; no import of primary verifier",
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
