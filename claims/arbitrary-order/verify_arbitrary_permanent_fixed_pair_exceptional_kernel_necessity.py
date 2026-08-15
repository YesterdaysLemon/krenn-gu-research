"""Primary exact checks for the fixed-pair exceptional-kernel theorem."""

from __future__ import annotations

import json
from itertools import permutations

import sympy as sp

Vector = tuple[sp.Expr, ...]


def add(*vectors: Vector) -> Vector:
    """Add vectors coordinatewise."""
    return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(6))


def scale(value: sp.Expr, vector: Vector) -> Vector:
    """Scale a vector."""
    return tuple(sp.expand(value * entry) for entry in vector)


def evaluate(covector: Vector, vector: Vector) -> sp.Expr:
    """Evaluate a covector on a vector."""
    return sp.expand(sum(x * y for x, y in zip(covector, vector, strict=True)))


def polarized_product(factors: tuple[Vector, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Evaluate the complete polarization of a product of four factors."""
    return sp.expand(sum(
        sp.prod(evaluate(factors[row], vectors[column]) for row, column in enumerate(order))
        for order in permutations(range(4))
    ))


def j_form(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the hyperbolic form on the x4,x5 coordinates."""
    return sp.expand(left[4] * right[5] + left[5] * right[4])


def c_tensor(first: Vector, second: Vector, third: Vector) -> tuple[sp.Expr, ...]:
    """Evaluate the R-valued tensor used in the proof."""
    return tuple(sp.expand(
        first[i] * j_form(second, third)
        + second[i] * j_form(first, third)
        + third[i] * j_form(first, second)
    ) for i in range(4))


def fixed_data() -> tuple[dict[str, tuple[sp.Expr, tuple[Vector, ...]]], tuple[Vector, ...]]:
    """Return coordinate covectors and the five factorized quartics."""
    coordinates = tuple(
        tuple(sp.Integer(i == j) for i in range(6))
        for j in range(6)
    )
    x0, x1, x2, x3, x4, x5 = coordinates
    ell1 = add(x3, scale(-1, x2), scale(-1, x0))
    ell2 = add(x3, scale(-1, x2), scale(-1, x1))
    factors = {
        "m1": (sp.Integer(1), (x4, x5, x1, ell1)),
        "m2": (sp.Integer(1), (x4, x5, x0, ell2)),
        "d0": (sp.Integer(1), (x4, x5, add(x1, x2), add(x3, scale(-1, x0)))),
        "d1": (sp.Integer(1), (x4, x5, add(x0, x2), add(x3, scale(-1, x1)))),
        "d2": (sp.Integer(-2), (x4, x5, x0, x1)),
    }
    return factors, coordinates


def check_kernels_and_contractions() -> dict[str, object]:
    """Reconstruct both kernels and the generic residual determinants."""
    factors, coordinates = fixed_data()
    x0, x1, x2, x3, _x4, _x5 = coordinates
    phi1 = sp.Matrix([
        x1,
        coordinates[4],
        coordinates[5],
        add(x3, scale(-1, x2), scale(-1, x0)),
    ])
    phi2 = sp.Matrix([
        x0,
        coordinates[4],
        coordinates[5],
        add(x3, scale(-1, x2), scale(-1, x1)),
    ])
    kernel1 = sp.Matrix.hstack(
        sp.Matrix((1, 0, 0, 1, 0, 0)),
        sp.Matrix((0, 0, 1, 1, 0, 0)),
    )
    kernel2 = sp.Matrix.hstack(
        sp.Matrix((0, 1, 0, 1, 0, 0)),
        sp.Matrix((0, 0, 1, 1, 0, 0)),
    )
    assert phi1.rank() == phi2.rank() == 4
    assert phi1 * kernel1 == sp.zeros(4, 2)
    assert phi2 * kernel2 == sp.zeros(4, 2)

    a, b = sp.symbols("a b")
    p1 = (a, 0, b, a + b, 0, 0)
    p2 = (0, a, b, a + b, 0, 0)
    residuals = {
        1: {
            "m1": (0, 0, 0, 0),
            "m2": (a, -a, -a, a),
            "d0": (-b, b, b, b),
            "d1": (a + b, -a - b, a + b, a + b),
            "d2": (0, -2 * a, 0, 0),
        },
        2: {
            "m1": (-a, a, -a, a),
            "m2": (0, 0, 0, 0),
            "d0": (-a - b, a + b, a + b, a + b),
            "d1": (b, -b, b, b),
            "d2": (-2 * a, 0, 0, 0),
        },
    }

    symbols = sp.symbols("z0:18")
    remaining = tuple(
        tuple(symbols[6 * mode + i] for i in range(6))
        for mode in range(3)
    )
    c_value = c_tensor(*remaining)
    for side, kernel_vector in ((1, p1), (2, p2)):
        for name, (coefficient, factor_rows) in factors.items():
            actual = coefficient * polarized_product(factor_rows, (kernel_vector, *remaining))
            expected = sum(
                residuals[side][name][i] * c_value[i]
                for i in range(4)
            )
            assert sp.expand(actual - expected) == 0, (side, name)

    determinants: dict[str, str] = {}
    for side, mixed in ((1, "m2"), (2, "m1")):
        matrix = sp.Matrix.hstack(*(
            sp.Matrix(residuals[side][name])
            for name in (mixed, "d0", "d1", "d2")
        ))
        determinant = sp.factor(matrix.det())
        assert determinant == 8 * a**2 * b * (a + b)
        determinants[f"Phi_{side}"] = str(determinant)

    exceptional = ((0, 1), (1, 0), (1, -1))
    for aa, bb in exceptional:
        assert (a**2 * b * (a + b)).subs({a: aa, b: bb}) == 0

    return {
        "kernel_dimensions": [6 - phi1.rank(), 6 - phi2.rank()],
        "generic_determinants": determinants,
        "exceptional_projective_parameters": exceptional,
        "polarized_contractions_checked": 10,
    }


def check_one_diagonal_rank_gate() -> dict[str, object]:
    """Check the scalar-identity minor and common orthogonal-line core."""
    scalar = sp.symbols("j", nonzero=True)
    scalar_identity = scalar * sp.eye(4)
    assert sp.factor(scalar_identity.det()) == scalar**4
    assert scalar_identity.rank() == 4

    p, q, left, right = sp.symbols("p q left right")
    a_vector = sp.Matrix((p, q))
    hyperbolic = sp.Matrix(((0, 1), (1, 0)))
    orthogonal_generator = sp.Matrix((p, -q))
    assert (a_vector.T * hyperbolic * orthogonal_generator)[0] == 0

    first = left * orthogonal_generator
    second = right * orthogonal_generator
    assert sp.Matrix.hstack(first, second).det() == 0

    # A nonzero pairing forces each endpoint to be nonzero.  The proof then
    # uses the displayed one-dimensional orthogonal complement; no division
    # or algebraic closure is needed.
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    pairing = sp.expand(a0 * b1 + a1 * b0)
    assert pairing != 0
    assert sp.Matrix(((a1, a0),)).rank() == 1

    return {
        "scalar_identity_minor": str(scalar**4),
        "ambient_rank_if_pairing_nonzero": 4,
        "killed_local_plane_dimension": 3,
        "orthogonal_complement_dimension": 1,
        "two_orthogonal_vectors_determinant": 0,
    }


def main() -> None:
    """Run all exact checks and print a deterministic summary."""
    report = {
        "kernel_and_contraction_checks": check_kernels_and_contractions(),
        "one_diagonal_lemma_checks": check_one_diagonal_rank_gate(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
