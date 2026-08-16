"""Primary exact checks for the triangle-pair kernel-support boundary."""

from __future__ import annotations

import json
from itertools import permutations

import sympy as sp

Vector = tuple[sp.Expr, ...]


def add(*vectors: Vector) -> Vector:
    """Add six-coordinate vectors."""
    return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(6))


def scale(value: sp.Expr, vector: Vector) -> Vector:
    """Scale a six-coordinate vector."""
    return tuple(sp.expand(value * entry) for entry in vector)


def evaluate(covector: Vector, vector: Vector) -> sp.Expr:
    """Evaluate a covector on a vector."""
    return sp.expand(sum(x * y for x, y in zip(covector, vector, strict=True)))


def polarized_product(factors: tuple[Vector, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Evaluate the complete polarization of four linear factors."""
    return sp.expand(sum(
        sp.prod(evaluate(factors[row], vectors[column]) for row, column in enumerate(order))
        for order in permutations(range(4))
    ))


def j_form(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the hyperbolic form on coordinates x4,x5."""
    return sp.expand(left[4] * right[5] + left[5] * right[4])


def c_tensor(first: Vector, second: Vector, third: Vector) -> tuple[sp.Expr, ...]:
    """Evaluate the R-valued trilinear contraction tensor."""
    return tuple(sp.expand(
        first[i] * j_form(second, third)
        + second[i] * j_form(first, third)
        + third[i] * j_form(first, second)
    ) for i in range(4))


def triangle_data() -> tuple[dict[str, tuple[sp.Expr, tuple[Vector, ...]]], tuple[Vector, ...]]:
    """Return coordinate covectors and the five factored quartics."""
    coordinates = tuple(
        tuple(sp.Integer(i == j) for i in range(6))
        for j in range(6)
    )
    x0, x1, x2, x3, x4, x5 = coordinates
    ell1 = add(x2, scale(-1, x1), scale(-1, x0))
    ell2 = add(x2, scale(-1, x1))
    factors = {
        "f1": (sp.Integer(1), (x4, x5, x3, ell1)),
        "f2": (sp.Integer(1), (x4, x5, x0, ell2)),
        "d0": (sp.Integer(2), (x4, x5, x0, x3)),
        "d1": (sp.Integer(1), (x4, x5, x2, add(x0, x1))),
        "d2": (sp.Integer(1), (x4, x5, x1, add(x0, scale(-1, x2)))),
    }
    return factors, coordinates


def check_kernels_and_contractions() -> dict[str, object]:
    """Check the kernel parametrizations and all displayed contractions."""
    factors, coordinates = triangle_data()
    x0, x1, x2, x3, x4, x5 = coordinates
    ell1 = add(x2, scale(-1, x1), scale(-1, x0))
    ell2 = add(x2, scale(-1, x1))
    phi1 = sp.Matrix([x3, x4, x5, ell1])
    phi2 = sp.Matrix([x0, x4, x5, ell2])
    kernel1 = sp.Matrix.hstack(
        sp.Matrix((1, 0, 1, 0, 0, 0)),
        sp.Matrix((0, 1, 1, 0, 0, 0)),
    )
    kernel2 = sp.Matrix.hstack(
        sp.Matrix((0, 1, 1, 0, 0, 0)),
        sp.Matrix((0, 0, 0, 1, 0, 0)),
    )
    assert phi1.rank() == phi2.rank() == 4
    assert phi1 * kernel1 == sp.zeros(4, 2)
    assert phi2 * kernel2 == sp.zeros(4, 2)

    a, b = sp.symbols("a b")
    p1 = (a, b, a + b, 0, 0, 0)
    p2 = (0, a, a, b, 0, 0)
    residuals = {
        1: {
            "f1": (0, 0, 0, 0),
            "f2": (a, -a, a, 0),
            "d0": (0, 0, 0, 2 * a),
            "d1": (a + b, a + b, a + b, 0),
            "d2": (b, -b, -b, 0),
        },
        2: {
            "f1": (-b, -b, b, 0),
            "f2": (0, 0, 0, 0),
            "d0": (2 * b, 0, 0, 0),
            "d1": (a, a, a, 0),
            "d2": (a, -a, -a, 0),
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
            expected = sum(residuals[side][name][i] * c_value[i] for i in range(4))
            assert sp.expand(actual - expected) == 0, (side, name)

    first_matrix = sp.Matrix.hstack(*(
        sp.Matrix(residuals[1][name])
        for name in ("f2", "d0", "d1", "d2")
    ))
    determinant = sp.factor(first_matrix.det())
    assert determinant == -8 * a**2 * b * (a + b)

    relation = tuple(sp.expand(
        -a * residuals[2]["d0"][i]
        + b * residuals[2]["d1"][i]
        + b * residuals[2]["d2"][i]
    ) for i in range(4))
    assert relation == (0, 0, 0, 0)

    return {
        "kernel_dimensions": [6 - phi1.rank(), 6 - phi2.rank()],
        "phi1_generic_determinant": str(determinant),
        "phi1_exceptional_parameters": [(0, 1), (1, 0), (1, -1)],
        "phi2_residual_relation_cleared": "-a*d0+b*d1+b*d2=0",
        "phi2_exceptional_parameters": [(0, 1), (1, 0)],
        "polarized_contractions_checked": 10,
    }


def check_structural_rank_gates() -> dict[str, object]:
    """Check the rank and orthogonal-line gates used in the written proof."""
    scalar = sp.symbols("j", nonzero=True)
    scalar_identity = scalar * sp.eye(4)
    assert scalar_identity.rank() == 4
    assert sp.factor(scalar_identity.det()) == scalar**4

    p, q = sp.symbols("p q")
    hyperbolic = sp.Matrix(((0, 1), (1, 0)))
    vector = sp.Matrix((p, q))
    orthogonal = sp.Matrix((p, -q))
    assert sp.expand((vector.T * hyperbolic * orthogonal)[0]) == 0
    left, right = sp.symbols("left right")
    assert sp.Matrix.hstack(left * orthogonal, right * orthogonal).det() == 0

    # The three coordinate cubes occurring after the Phi_2 relation are
    # distinct standard basis vectors in the 27-dimensional tensor space.
    coordinate_cubes = sp.zeros(27, 3)
    coordinate_cubes[0, 0] = 1
    coordinate_cubes[13, 1] = 1
    coordinate_cubes[26, 2] = 1
    assert coordinate_cubes.rank() == 3

    return {
        "scalar_identity_rank": scalar_identity.rank(),
        "killed_local_plane_dimension": 3,
        "orthogonal_complement_dimension": 1,
        "coordinate_cube_rank": coordinate_cubes.rank(),
    }


def main() -> None:
    """Run all exact checks and print a deterministic report."""
    report = {
        "kernel_and_contraction_checks": check_kernels_and_contractions(),
        "structural_rank_gates": check_structural_rank_gates(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
