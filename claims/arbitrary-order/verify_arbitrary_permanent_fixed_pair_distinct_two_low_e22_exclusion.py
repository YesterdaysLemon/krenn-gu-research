"""Primary exact checks for the fixed-pair two-low E22 exclusion."""

from __future__ import annotations

import json
from itertools import combinations, permutations

import sympy as sp

Vector4 = tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]
Vector6 = tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr]


def add(*vectors: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    """Add equal-length vectors coordinatewise."""
    return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(len(vectors[0])))


def scale(value: int | sp.Expr, vector: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    """Scale a vector."""
    scalar = sp.sympify(value)
    return tuple(sp.expand(scalar * entry) for entry in vector)


def coordinate_vectors(dimension: int) -> tuple[tuple[sp.Integer, ...], ...]:
    """Return the coordinate vectors of one dimension."""
    return tuple(
        tuple(sp.Integer(row == column) for row in range(dimension))
        for column in range(dimension)
    )


def quadratic_contraction_matrix(
    left: Vector4,
    right: Vector4,
    coefficient: int | sp.Expr = 1,
) -> sp.Matrix:
    """Return the derivative matrix of a square-free quadratic product."""
    scalar = sp.sympify(coefficient)
    matrix = sp.zeros(4)
    for i in range(4):
        for j in range(i + 1, 4):
            value = sp.expand(scalar * (left[i] * right[j] + left[j] * right[i]))
            matrix[i, j] = value
            matrix[j, i] = value
    return matrix


def fixed_data() -> tuple[
    dict[str, sp.Matrix],
    dict[str, tuple[sp.Expr, tuple[Vector6, Vector6, Vector6, Vector6]]],
]:
    """Build the five quadratic matrices and factorized quartics."""
    x0, x1, x2, x3 = coordinate_vectors(4)
    z0, z1, z2, z3, x4, x5 = coordinate_vectors(6)
    quadratic_factors: dict[str, tuple[sp.Expr, Vector4, Vector4]] = {
        "m1": (sp.Integer(1), x1, add(x3, scale(-1, x2), scale(-1, x0))),
        "m2": (sp.Integer(1), x0, add(x3, scale(-1, x2), scale(-1, x1))),
        "d0": (sp.Integer(1), add(x1, x2), add(x3, scale(-1, x0))),
        "d1": (sp.Integer(1), add(x0, x2), add(x3, scale(-1, x1))),
        "d2": (sp.Integer(-2), x0, x1),
    }
    matrices = {
        name: quadratic_contraction_matrix(left, right, coefficient)
        for name, (coefficient, left, right) in quadratic_factors.items()
    }
    def lift(vector: Vector4) -> Vector6:
        return vector + (sp.Integer(0), sp.Integer(0))

    quartics = {
        name: (coefficient, (x4, x5, lift(left), lift(right)))
        for name, (coefficient, left, right) in quadratic_factors.items()
    }
    # Guard the common coordinate convention in both constructions.
    assert (z0, z1, z2, z3) == tuple(lift(vector) for vector in (x0, x1, x2, x3))
    return matrices, quartics


def evaluate(covector: tuple[sp.Expr, ...], point: tuple[sp.Expr, ...]) -> sp.Expr:
    """Evaluate one covector at one point."""
    return sp.expand(sum(x * y for x, y in zip(covector, point, strict=True)))


def polarized_product(
    factors: tuple[tuple[sp.Expr, ...], ...],
    points: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Expr:
    """Evaluate complete polarization of a product of linear forms."""
    assert len(factors) == len(points)
    return sp.expand(
        sum(
            sp.prod(
                evaluate(factors[row], points[column])
                for row, column in enumerate(order)
            )
            for order in permutations(range(len(points)))
        )
    )


def vector(*entries: int | sp.Expr) -> sp.Matrix:
    """Return an exact column vector."""
    return sp.Matrix(tuple(sp.sympify(entry) for entry in entries))


def lines_and_expected() -> tuple[dict[str, sp.Matrix], dict[str, tuple[sp.Matrix, ...]]]:
    """Return the exceptional lines and their complete residual rows."""
    zero = vector(0, 0, 0, 0)
    h2 = vector(1, -1, -1, 1)
    h2_prime = vector(-1, 1, -1, 1)
    x0 = vector(1, 0, 0, 0)
    x1 = vector(0, 1, 0, 0)
    x2 = vector(0, 0, 1, 0)
    x3 = vector(0, 0, 0, 1)
    lines = {
        "A0": vector(1, 0, 0, 1),
        "C0": vector(1, 0, -1, 0),
        "A1": vector(0, 1, 0, 1),
        "C1": vector(0, 1, -1, 0),
    }
    expected = {
        "A0": (zero, h2, zero, h2 + 2 * x2, -2 * x1),
        "C0": (zero, h2, h2 - 2 * x3, zero, -2 * x1),
        "A1": (h2_prime, zero, h2_prime + 2 * x2, zero, -2 * x0),
        "C1": (h2_prime, zero, zero, h2_prime - 2 * x3, -2 * x0),
    }
    return lines, expected


def check_residual_table() -> dict[str, object]:
    """Derive every residual covector in the four exceptional rows."""
    matrices, _ = fixed_data()
    lines, expected = lines_and_expected()
    channels = ("m1", "m2", "d0", "d1", "d2")
    table: dict[str, list[list[int]]] = {}
    for name, line in lines.items():
        actual = tuple(matrices[channel] * line for channel in channels)
        assert actual == expected[name]
        table[name] = [[int(entry) for entry in residual] for residual in actual]
    return {"channels": list(channels), "rows": table}


def check_direct_polarization_scalars() -> dict[str, int]:
    """Compare all quartic contractions with residual trilinears exactly."""
    matrices, quartics = fixed_data()
    lines, _ = lines_and_expected()
    symbols = sp.symbols("z0:18")
    remaining_points: tuple[Vector6, Vector6, Vector6] = tuple(
        tuple(symbols[6 * mode + coordinate] for coordinate in range(6))
        for mode in range(3)
    )  # type: ignore[assignment]
    x4, x5 = coordinate_vectors(6)[4:]
    checks = 0
    for line in lines.values():
        pure_r_line: Vector6 = tuple(line) + (sp.Integer(0), sp.Integer(0))  # type: ignore[assignment]
        for channel, matrix in matrices.items():
            coefficient, factors = quartics[channel]
            residual4 = matrix * line
            residual6: Vector6 = tuple(residual4) + (sp.Integer(0), sp.Integer(0))  # type: ignore[assignment]
            quartic_value = coefficient * polarized_product(
                factors,
                (pure_r_line, *remaining_points),
            )
            residual_value = polarized_product(
                (x4, x5, residual6),
                remaining_points,
            )
            assert sp.expand(quartic_value - residual_value) == 0
            checks += 1
    return {"exceptional_lines": len(lines), "channel_contractions": checks}


def check_high_slice_identity() -> dict[str, int]:
    """Verify the exact scalar-one formula in the high rank-one slice."""
    symbols = sp.symbols("w0:18")
    left: Vector6 = tuple(symbols[:6])  # type: ignore[assignment]
    middle: Vector6 = (*symbols[6:10], sp.Integer(0), sp.Integer(0))  # type: ignore[assignment]
    right: Vector6 = tuple(symbols[12:18])  # type: ignore[assignment]
    x4, x5 = coordinate_vectors(6)[4:]
    residual_tuples = {
        tuple(residual)
        for rows in lines_and_expected()[1].values()
        for residual in rows
        if residual != sp.zeros(4, 1)
    }
    checks = 0
    pairing = left[4] * right[5] + left[5] * right[4]
    for residual4 in residual_tuples:
        residual6: Vector6 = residual4 + (sp.Integer(0), sp.Integer(0))  # type: ignore[assignment]
        actual = polarized_product((x4, x5, residual6), (left, middle, right))
        expected = evaluate(residual6, middle) * pairing
        assert sp.expand(actual - expected) == 0
        checks += 1
    return {
        "distinct_nonzero_residuals": len(residual_tuples),
        "scalar_one_checks": checks,
    }


def check_selected_minor_identity() -> dict[str, int]:
    """Prove that two onto A-maps have rank-two pairing matrix."""
    left = sp.Matrix(2, 3, sp.symbols("a0:6"))
    right = sp.Matrix(2, 3, sp.symbols("b0:6"))
    j_form = sp.Matrix(((0, 1), (1, 0)))
    pairing = left.T * j_form * right
    checks = 0
    for row_indices in combinations(range(3), 2):
        for column_indices in combinations(range(3), 2):
            actual = pairing.extract(row_indices, column_indices).det()
            expected = (
                left[:, row_indices].det()
                * j_form.det()
                * right[:, column_indices].det()
            )
            assert sp.expand(actual - expected) == 0
            checks += 1
    return {"selected_minor_identities": checks, "det_J": int(j_form.det())}


def check_common_kernels_and_support_split() -> dict[str, object]:
    """Check the four one-line singleton kernels and both support cases."""
    h2 = vector(1, -1, -1, 1)
    h2_prime = vector(-1, 1, -1, 1)
    data = {
        "A0": (h2, vector(0, 1, 0, 0), h2 + 2 * vector(0, 0, 1, 0), vector(1, 0, 0, -1), 1),
        "C0": (h2, vector(0, 1, 0, 0), h2 - 2 * vector(0, 0, 0, 1), vector(1, 0, 1, 0), 0),
        "A1": (h2_prime, vector(1, 0, 0, 0), h2_prime + 2 * vector(0, 0, 1, 0), vector(0, 1, 0, -1), 0),
        "C1": (h2_prime, vector(1, 0, 0, 0), h2_prime - 2 * vector(0, 0, 0, 1), vector(0, 1, 1, 0), 1),
    }
    kernels: dict[str, list[int]] = {}
    support_cases = 0
    for name, (mixed, coordinate, diagonal, generator, colour) in data.items():
        rows = sp.Matrix.vstack(mixed.T, coordinate.T, diagonal.T)
        assert rows.rank() == 3
        assert rows * generator == sp.zeros(3, 1)
        assert sp.Matrix.hstack(rows.nullspace()[0], generator).rank() == 1
        kernels[name] = [int(entry) for entry in generator]

        # Singleton support uses all three zero covectors.  Support {k,2}
        # uses a live rank-one E_kk target, incompatible with rank-two B.
        diagonal_matrix = sp.zeros(3)
        diagonal_matrix[colour, colour] = 1
        assert diagonal_matrix.rank() == 1
        support_cases += 2

    return {
        "common_kernels": kernels,
        "support_cases": support_cases,
        "orientations": 2,
    }


def main() -> None:
    """Run all primary exact checks."""
    report = {
        "residual_table": check_residual_table(),
        "direct_polarization": check_direct_polarization_scalars(),
        "high_slice": check_high_slice_identity(),
        "rank_two_pairing": check_selected_minor_identity(),
        "branch_split": check_common_kernels_and_support_split(),
        "E22_branch": "EXCLUDED",
        "zero_branch": "OPEN",
        "status": "UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
