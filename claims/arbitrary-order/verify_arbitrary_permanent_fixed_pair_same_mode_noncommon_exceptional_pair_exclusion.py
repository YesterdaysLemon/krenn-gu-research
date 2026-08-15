"""Primary exact checks for the same-mode noncommon exceptional-pair theorem."""

from __future__ import annotations

import json
from itertools import permutations

import sympy as sp

Vector4 = tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]
Vector6 = tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr]


def quadratic_contraction_matrix(
    left: Vector4,
    right: Vector4,
    scale: sp.Expr = sp.Integer(1),
) -> sp.Matrix:
    """Build the contraction matrix of a square-free product of two forms."""
    matrix = sp.zeros(4)
    for i in range(4):
        for j in range(i + 1, 4):
            coefficient = sp.expand(scale * (left[i] * right[j] + left[j] * right[i]))
            matrix[i, j] = coefficient
            matrix[j, i] = coefficient
    return matrix


def fixed_matrices() -> dict[str, sp.Matrix]:
    """Derive all five residual contraction matrices from factorized quadratics."""
    x0, x1, x2, x3 = (
        tuple(sp.Integer(i == j) for i in range(4))
        for j in range(4)
    )

    def add(*vectors: Vector4) -> Vector4:
        return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(4))

    def scale(value: int, vector: Vector4) -> Vector4:
        return tuple(sp.Integer(value) * entry for entry in vector)

    return {
        "m1": quadratic_contraction_matrix(x1, add(x3, scale(-1, x2), scale(-1, x0))),
        "m2": quadratic_contraction_matrix(x0, add(x3, scale(-1, x2), scale(-1, x1))),
        "d0": quadratic_contraction_matrix(add(x1, x2), add(x3, scale(-1, x0))),
        "d1": quadratic_contraction_matrix(add(x0, x2), add(x3, scale(-1, x1))),
        "d2": quadratic_contraction_matrix(x0, x1, sp.Integer(-2)),
    }


def vector(*entries: int | sp.Expr) -> sp.Matrix:
    """Return a four-coordinate exact column vector."""
    return sp.Matrix(tuple(sp.sympify(entry) for entry in entries))


def quotient_coordinates(column: sp.Matrix) -> sp.Matrix:
    """Return coordinates in R^*/span(h2,h2')."""
    return sp.Matrix((sp.expand(column[0] + column[1]), sp.expand(column[2] + column[3])))


def check_contraction_table() -> dict[str, object]:
    """Derive the complete noncommon-line contraction table."""
    matrices = fixed_matrices()
    lines = {
        "A0": vector(1, 0, 0, 1),
        "C0": vector(1, 0, -1, 0),
        "A1": vector(0, 1, 0, 1),
        "C1": vector(0, 1, -1, 0),
    }
    h2 = vector(1, -1, -1, 1)
    h2_prime = vector(-1, 1, -1, 1)
    w0 = vector(1, -1, -1, -1)
    w1 = vector(1, -1, 1, 1)
    x0 = vector(1, 0, 0, 0)
    x1 = vector(0, 1, 0, 0)
    expected = {
        "A0": (vector(0, 0, 0, 0), h2, vector(0, 0, 0, 0), w1, -2 * x1),
        "C0": (vector(0, 0, 0, 0), h2, w0, vector(0, 0, 0, 0), -2 * x1),
        "A1": (h2_prime, vector(0, 0, 0, 0), -w0, vector(0, 0, 0, 0), -2 * x0),
        "C1": (h2_prime, vector(0, 0, 0, 0), vector(0, 0, 0, 0), -w1, -2 * x0),
    }
    channels = ("m1", "m2", "d0", "d1", "d2")
    for name, line in lines.items():
        actual = tuple(matrices[channel] * line for channel in channels)
        assert actual == expected[name], (name, actual)

    phi1 = sp.Matrix((
        (0, 1, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (-1, 0, -1, 1),
    ))
    phi2 = sp.Matrix((
        (1, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, -1, -1, 1),
    ))
    # The zero x4,x5 rows are suppressed in this R-only display.
    assert phi1 * lines["A0"] == sp.zeros(4, 1)
    assert phi1 * lines["C0"] == sp.zeros(4, 1)
    assert phi2 * lines["A1"] == sp.zeros(4, 1)
    assert phi2 * lines["C1"] == sp.zeros(4, 1)

    u_matrix = sp.Matrix.hstack(h2, h2_prime)
    assert u_matrix.rank() == 2
    for outside in (w0, w1, x0, x1):
        assert sp.Matrix.hstack(u_matrix, outside).rank() == 3
    assert quotient_coordinates(h2) == sp.zeros(2, 1)
    assert quotient_coordinates(h2_prime) == sp.zeros(2, 1)

    return {
        "channels_derived": len(channels),
        "exceptional_lines_checked": len(lines),
        "mixed_kernel_rank": u_matrix.rank(),
        "outside_vectors_checked": 4,
        "quotient_formula": ["v0+v1", "v2+v3"],
    }


def check_immediate_pairs_and_normal_forms() -> dict[str, object]:
    """Replay the two direct exclusions and derive both surviving normal forms."""
    matrices = fixed_matrices()
    lines = {
        "A0": vector(1, 0, 0, 1),
        "C0": vector(1, 0, -1, 0),
        "A1": vector(0, 1, 0, 1),
        "C1": vector(0, 1, -1, 0),
    }
    h2 = matrices["m2"] * lines["A0"]
    h2_prime = matrices["m1"] * lines["A1"]
    u_matrix = sp.Matrix.hstack(h2, h2_prime)

    immediate_witnesses = {
        ("A0", "A1"): (
            matrices["d0"] * lines["A1"],
            matrices["d1"] * lines["A0"],
            matrices["d2"] * lines["A0"],
        ),
        ("C0", "C1"): (
            matrices["d0"] * lines["C0"],
            matrices["d1"] * lines["C1"],
            matrices["d2"] * lines["C0"],
        ),
    }
    for witnesses in immediate_witnesses.values():
        for witness in witnesses:
            assert sp.Matrix.hstack(u_matrix, witness).rank() == 3

    a, b, c, d = sp.symbols("a b c d")
    normal_form_checks: dict[str, dict[str, str]] = {}
    for pair, first_channel, first_sign in (
        ("A0_C1", "d1", 1),
        ("C0_A1", "d0", -1),
    ):
        first_name, second_name = pair.split("_")
        p = lines[first_name]
        q = lines[second_name]
        first_kernel = c * p - a * q
        second_kernel = d * p - b * q
        first_obstruction = sp.simplify(quotient_coordinates(matrices[first_channel] * first_kernel))
        second_obstruction = sp.simplify(quotient_coordinates(matrices["d2"] * second_kernel))
        assert first_obstruction == sp.Matrix((0, first_sign * 2 * (a + c)))
        assert second_obstruction == sp.Matrix((2 * (b - d), 0))
        determinant = sp.factor(a * d - b * c)
        specialized = sp.factor(determinant.subs({c: -a, d: b}))
        assert specialized == 2 * a * b

        alpha = sp.Matrix((0, a, b)) if pair == "A0_C1" else sp.Matrix((a, 0, b))
        beta = sp.Matrix((0, -a, b)) if pair == "A0_C1" else sp.Matrix((-a, 0, b))
        y_first = sp.simplify((p - q) / (2 * a))
        y_second = sp.simplify((p + q) / (2 * b))
        assert a * y_first + b * y_second == p
        assert -a * y_first + b * y_second == q

        normal_form_checks[pair] = {
            "first_quotient_obstruction": str(tuple(first_obstruction)),
            "second_quotient_obstruction": str(tuple(second_obstruction)),
            "specialized_coordinate_minor": str(specialized),
            "alpha": str(tuple(alpha)),
            "beta": str(tuple(beta)),
        }

    # Guard the corrected projective-scaling convention.  Ambient vectors,
    # local coordinate columns, and contractions must all scale together.
    s, t = sp.symbols("s t")
    p = lines["A0"]
    q = lines["C1"]
    alpha_c, beta_c = sp.symbols("alpha_c beta_c")
    original = beta_c * p - alpha_c * q
    scaled = (t * beta_c) * (s * p) - (s * alpha_c) * (t * q)
    assert scaled == s * t * original
    for matrix in matrices.values():
        assert sp.simplify(matrix * scaled - s * t * (matrix * original)) == sp.zeros(4, 1)

    return {
        "immediate_pairs_excluded": ["A0_A1", "C0_C1"],
        "zero_row_cases_per_immediate_pair": 3,
        "normal_forms": normal_form_checks,
        "scaling_covariance_channels": len(matrices),
    }


def evaluate(covector: Vector6, point: Vector6) -> sp.Expr:
    """Evaluate one six-coordinate covector."""
    return sp.expand(sum(x * y for x, y in zip(covector, point, strict=True)))


def polarized_product(factors: tuple[Vector6, ...], points: tuple[Vector6, ...]) -> sp.Expr:
    """Evaluate the complete polarization of a four-factor quartic."""
    return sp.expand(sum(
        sp.prod(evaluate(factors[row], points[column]) for row, column in enumerate(order))
        for order in permutations(range(4))
    ))


def check_two_active_and_supplier_gates() -> dict[str, object]:
    """Replay the rank-four cross-pair gate and the one-A-supplier zero."""
    scalar = sp.symbols("j", nonzero=True)
    scalar_identity = scalar * sp.eye(4)
    assert sp.factor(scalar_identity.det()) == scalar**4

    j_matrix = sp.Matrix(((0, 1), (1, 0)))
    assert j_matrix.det() == -1
    r, s = sp.symbols("r s")
    first = sp.Matrix((r, s))
    orthogonal = sp.Matrix((r, -s))
    assert (first.T * j_matrix * orthogonal)[0] == 0
    assert sp.Matrix.hstack(orthogonal, 2 * orthogonal).det() == 0

    symbols = sp.symbols("z0:24")
    points = tuple(
        tuple(symbols[6 * mode + coordinate] for coordinate in range(6))
        for mode in range(4)
    )
    # Only the shared mode may have an A-part.  The other three points are
    # projected to R before evaluating each fixed diagonal quartic.
    one_a_supplier = (points[0],) + tuple(
        point[:4] + (sp.Integer(0), sp.Integer(0))
        for point in points[1:]
    )
    coordinates = tuple(
        tuple(sp.Integer(i == j) for i in range(6))
        for j in range(6)
    )
    x0, x1, x2, x3, x4, x5 = coordinates

    def add(*vectors: Vector6) -> Vector6:
        return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(6))

    def scale(value: int, vector: Vector6) -> Vector6:
        return tuple(sp.Integer(value) * entry for entry in vector)

    d0_factors = (x4, x5, add(x1, x2), add(x3, scale(-1, x0)))
    d1_factors = (x4, x5, add(x0, x2), add(x3, scale(-1, x1)))
    assert polarized_product(d0_factors, one_a_supplier) == 0
    assert polarized_product(d1_factors, one_a_supplier) == 0

    return {
        "cross_pair_scalar_minor": str(scalar**4),
        "killed_plane_rank_ceiling": 3,
        "ambient_scalar_rank": 4,
        "hyperbolic_form_determinant": int(j_matrix.det()),
        "one_A_supplier_diagonal_quartics_zero": ["d0", "d1"],
    }


def main() -> None:
    """Run all exact checks and print a deterministic report."""
    report = {
        "contraction_table": check_contraction_table(),
        "pair_classification": check_immediate_pairs_and_normal_forms(),
        "two_active_and_supplier_gates": check_two_active_and_supplier_gates(),
        "scope": {
            "noncommon_same_mode_pairs": "EXCLUDED",
            "N_plus_noncommon": "OPEN",
            "N_with_N": "OPEN",
            "global_krenn_gu": "UNRESOLVED",
        },
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
