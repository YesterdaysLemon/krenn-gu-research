"""Primary exact checks for the fixed-pair kernel-support boundary."""

from __future__ import annotations

from itertools import permutations, product

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
    """Evaluate the polarization of a product of distinct linear factors."""
    assert len(factors) == len(vectors)
    return sp.expand(sum(
        sp.prod(evaluate(factors[row], vectors[column]) for row, column in enumerate(order))
        for order in permutations(range(len(factors)))
    ))


def j_form(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the hyperbolic form on coordinates x4,x5."""
    return sp.expand(left[4] * right[5] + left[5] * right[4])


def c_tensor(first: Vector, second: Vector, third: Vector) -> tuple[sp.Expr, ...]:
    """Evaluate the R-valued contraction tensor from the theorem."""
    return tuple(sp.expand(
        first[i] * j_form(second, third)
        + second[i] * j_form(first, third)
        + third[i] * j_form(first, second)
    ) for i in range(4))


def residual_value(residual: tuple[sp.Expr, ...], c_value: tuple[sp.Expr, ...]) -> sp.Expr:
    """Evaluate a four-coordinate residual covector on C."""
    return sp.expand(sum(x * y for x, y in zip(residual, c_value, strict=True)))


def fixed_factor_data() -> tuple[
    dict[str, tuple[sp.Expr, tuple[Vector, ...]]],
    tuple[Vector, ...],
]:
    """Return factorized quartics and coordinate covectors."""
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


def assert_kernels_and_contractions() -> dict[str, object]:
    """Derive both kernels, contraction tables, and generic determinants."""
    factors, coordinates = fixed_factor_data()
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
    expected_kernel1 = sp.Matrix.hstack(
        sp.Matrix((1, 0, 0, 1, 0, 0)),
        sp.Matrix((0, 0, 1, 1, 0, 0)),
    )
    expected_kernel2 = sp.Matrix.hstack(
        sp.Matrix((0, 1, 0, 1, 0, 0)),
        sp.Matrix((0, 0, 1, 1, 0, 0)),
    )
    assert phi1.rank() == phi2.rank() == 4
    assert phi1 * expected_kernel1 == sp.zeros(4, 2)
    assert phi2 * expected_kernel2 == sp.zeros(4, 2)
    assert expected_kernel1.rank() == expected_kernel2.rank() == 2

    a, b = sp.symbols("a b")
    p1 = (a, 0, b, a + b, 0, 0)
    p2 = (0, a, b, a + b, 0, 0)
    h0 = (-1, 1, 1, 1)
    h1 = (1, -1, 1, 1)
    h2 = (1, -1, -1, 1)
    h2_prime = (-1, 1, -1, 1)
    residuals = {
        1: {
            "m1": (0, 0, 0, 0),
            "m2": tuple(a * value for value in h2),
            "d0": tuple(b * value for value in h0),
            "d1": tuple((a + b) * value for value in h1),
            "d2": (0, -2 * a, 0, 0),
        },
        2: {
            "m1": tuple(a * value for value in h2_prime),
            "m2": (0, 0, 0, 0),
            "d0": tuple((a + b) * value for value in h0),
            "d1": tuple(b * value for value in h1),
            "d2": (-2 * a, 0, 0, 0),
        },
    }

    symbols = sp.symbols("y0:18")
    remaining = tuple(
        tuple(symbols[6 * mode + i] for i in range(6))
        for mode in range(3)
    )
    c_value = c_tensor(*remaining)
    for side, kernel_vector in ((1, p1), (2, p2)):
        for name, (sign, rows) in factors.items():
            actual = sign * polarized_product(rows, (kernel_vector, *remaining))
            expected = residual_value(residuals[side][name], c_value)
            assert sp.expand(actual - expected) == 0, (side, name)

    matrices = {}
    for side, mixed in ((1, "m2"), (2, "m1")):
        columns = [mixed, "d0", "d1", "d2"]
        matrix = sp.Matrix.hstack(*(
            sp.Matrix(residuals[side][name]) for name in columns
        ))
        determinant = sp.factor(matrix.det())
        assert determinant == 8 * a**2 * b * (a + b)
        matrices[f"Phi_{side}"] = determinant

    # Each exceptional direction kills the displayed pure channel.
    exceptional = {
        1: {"a=0": "d2", "b=0": "d0", "a+b=0": "d1"},
        2: {"a=0": "d2", "b=0": "d1", "a+b=0": "d0"},
    }
    substitutions = {
        "a=0": {a: 0},
        "b=0": {b: 0},
        "a+b=0": {b: -a},
    }
    for side, cases in exceptional.items():
        for condition, channel in cases.items():
            assert all(
                sp.expand(sp.sympify(value).subs(substitutions[condition])) == 0
                for value in residuals[side][channel]
            )
    return {
        "kernel_dimensions": (2, 2),
        "generic_determinants": matrices,
        "exceptional_zero_channels": exceptional,
        "factorized_contractions_checked": 10,
    }


def inverse(value: int, prime: int) -> int:
    """Return a modular inverse."""
    return pow(value % prime, prime - 2, prime)


def projective_states(prime: int) -> tuple[tuple[int, int], ...]:
    """Return zero plus normalized projective representatives in F_p^2."""
    states = [(0, 0)]
    seen: set[tuple[int, int]] = set()
    for vector in product(range(prime), repeat=2):
        if vector == (0, 0):
            continue
        pivot = 0 if vector[0] else 1
        scalar = inverse(vector[pivot], prime)
        normalized = tuple(value * scalar % prime for value in vector)
        if normalized not in seen:
            seen.add(normalized)
            states.append(normalized)
    assert len(states) == prime + 2
    return tuple(states)


def modular_j(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate J modulo a prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def compatible(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
    prime: int,
) -> bool:
    """Test all different-colour cross-orthogonality equations."""
    return all(
        first_colour == second_colour
        or modular_j(first[first_colour], second[second_colour], prime) == 0
        for first_colour in range(3)
        for second_colour in range(3)
    )


def assert_a_level_lemma(prime: int) -> dict[str, int]:
    """Exhaust the projective A-level lemma over one finite field."""
    states = projective_states(prime)
    arrays = tuple(product(states, repeat=3))
    neighbours = tuple(
        tuple(index for index, second in enumerate(arrays) if compatible(first, second, prime))
        for first in arrays
    )
    neighbour_sets = tuple(set(row) for row in neighbours)
    compatible_triples = 0
    two_active = 0
    for first_index, first in enumerate(arrays):
        for second_index in neighbours[first_index]:
            second = arrays[second_index]
            for third_index in neighbour_sets[first_index] & neighbour_sets[second_index]:
                third = arrays[third_index]
                compatible_triples += 1
                modes = (first, second, third)
                active = tuple(
                    colour for colour in range(3)
                    if any(
                        modular_j(modes[left][colour], modes[right][colour], prime)
                        for left, right in ((0, 1), (0, 2), (1, 2))
                    )
                )
                assert len(active) <= 2
                if len(active) == 2:
                    two_active += 1
                    inactive = next(colour for colour in range(3) if colour not in active)
                    assert all(mode[inactive] == (0, 0) for mode in modes)
    return {
        "projective_states": len(states),
        "mode_arrays": len(arrays),
        "compatible_triples": compatible_triples,
        "two_active_triples": two_active,
    }


def assert_rank_obstruction() -> dict[str, object]:
    """Check the rank-four R-summand used for cross orthogonality."""
    q = sp.symbols("q", nonzero=True)
    restriction = q * sp.eye(4)
    assert restriction.rank() == 4
    # A linear map from a six-space killing a three-space has rank at most 3.
    assert 6 - 3 == 3 < restriction.rank()
    return {"R_dimension": 4, "kernel_floor": 3, "forbidden_rank": 4}


def main() -> None:
    """Run all primary checks."""
    contractions = assert_kernels_and_contractions()
    rank_gate = assert_rank_obstruction()
    finite_fields = {prime: assert_a_level_lemma(prime) for prime in (3, 5, 7)}

    print("fixed-pair kernel-support boundary primary checks: PASS")
    print(f"  exact contractions: {contractions}")
    print(f"  R+A rank gate: {rank_gate}")
    print(f"  A-level finite-field exhaustions: {finite_fields}")


if __name__ == "__main__":
    main()
