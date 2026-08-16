"""Primary exact checks for the star-pair kernel-support boundary theorem."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

Vector = tuple[sp.Expr, ...]
Polynomial = dict[int, sp.Expr]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (-1, 1, 0, 1, 0, 0)
M2 = (1, -1, 0, 0, -1, 1)
D0 = (-1, 2, -1, 1, 0, 1)
D1 = (1, 0, -1, 0, -1, 0)
D2 = (0, 0, 0, 2, 0, 0)
B_BASIS = (M1, M2, D0, D1, D2)


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(
                result.get(mask, 0) + left_value * right_value
            )
    return {mask: value for mask, value in result.items() if value != 0}


def linear_form(vector: Vector) -> Polynomial:
    """Encode a degree-one form."""
    return {
        1 << index: sp.sympify(value)
        for index, value in enumerate(vector)
        if value != 0
    }


def quadratic_form(vector: tuple[int, ...]) -> Polynomial:
    """Encode a first-four-coordinate quadratic."""
    return {
        (1 << first) | (1 << second): sp.Integer(value)
        for value, (first, second) in zip(vector, EDGES, strict=True)
        if value
    }


def coefficient(quadratic: tuple[int, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Return the coefficient of x0...x5 in q times four forms."""
    result = quadratic_form(quadratic)
    for vector in vectors:
        result = square_free_multiply(result, linear_form(vector))
    return sp.expand(result.get(FULL_MASK, 0))


def first_four_product(left: Vector, right: Vector) -> tuple[sp.Expr, ...]:
    """Multiply two first-four-coordinate forms in edge coordinates."""
    return tuple(
        sp.expand(left[first] * right[second] + left[second] * right[first])
        for first, second in EDGES
    )


def add(*vectors: Vector) -> Vector:
    """Add vectors coordinatewise."""
    return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(6))


def scale(value: sp.Expr, vector: Vector) -> Vector:
    """Scale a vector."""
    return tuple(sp.expand(value * entry) for entry in vector)


def j_form(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the hyperbolic form on coordinates x4,x5."""
    return sp.expand(left[4] * right[5] + left[5] * right[4])


def c_tensor(first: Vector, second: Vector, third: Vector) -> tuple[sp.Expr, ...]:
    """Evaluate the R-valued residual contraction tensor."""
    return tuple(
        sp.expand(
            first[index] * j_form(second, third)
            + second[index] * j_form(first, third)
            + third[index] * j_form(first, second)
        )
        for index in range(4)
    )


def residual_value(residual: Vector, c_value: tuple[sp.Expr, ...]) -> sp.Expr:
    """Evaluate a first-four-coordinate residual covector on C."""
    return sp.expand(sum(residual[i] * c_value[i] for i in range(4)))


def assert_pair() -> dict[str, int]:
    """Reconstruct the displayed star-pair product table."""
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
    assert products[0][0] == D0
    assert products[1][1] == D1
    assert products[2][2] == D2
    assert products[0][1] == M1
    assert products[1][0] == M2
    assert sp.Matrix([entry for row in products for entry in row]).rank() == 5
    assert sp.Matrix(
        [products[i][j] for i in range(3) for j in range(3) if i != j]
    ).rank() == 2
    return {"pair_product_rank": 5, "mixed_rank": 2}


def assert_kernels_and_contractions() -> dict[str, object]:
    """Derive kernels, all contractions, determinants, and exceptional relations."""
    coordinates = tuple(
        tuple(sp.Integer(i == j) for i in range(6))
        for j in range(6)
    )
    x0, x1, x2, x3, x4, x5 = coordinates
    ell1 = add(x0, x1, scale(-1, x2))
    z0 = add(x0, scale(-1, x3))
    ell2 = add(x1, scale(-1, x2))
    phi1 = sp.Matrix([x3, x4, x5, ell1])
    phi2 = sp.Matrix([z0, x4, x5, ell2])
    kernel1 = sp.Matrix.hstack(
        sp.Matrix((1, 0, 1, 0, 0, 0)),
        sp.Matrix((0, 1, 1, 0, 0, 0)),
    )
    kernel2 = sp.Matrix.hstack(
        sp.Matrix((1, 0, 0, 1, 0, 0)),
        sp.Matrix((0, 1, 1, 0, 0, 0)),
    )
    assert phi1.rank() == phi2.rank() == 4
    assert phi1 * kernel1 == sp.zeros(4, 2)
    assert phi2 * kernel2 == sp.zeros(4, 2)

    a, b = sp.symbols("a b")
    p1 = (a, b, a + b, 0, 0, 0)
    p2 = (a, b, b, a, 0, 0)
    residuals: dict[int, dict[str, Vector]] = {
        1: {
            "m1": (0, 0, 0, 0),
            "m2": (-a, a, -a, a),
            "d0": (b, -b, -b, b),
            "d1": (-a - b, -a - b, -a - b, a + b),
            "d2": (0, 0, 0, 2 * a),
        },
        2: {
            "m1": (a, a, -a, a),
            "m2": (0, 0, 0, 0),
            "d0": (a + b, 3 * a - b, -a - b, a + b),
            "d1": (-b, -b, -b, b),
            "d2": (2 * a, 0, 0, 2 * a),
        },
    }
    quadratics = dict(zip(("m1", "m2", "d0", "d1", "d2"), B_BASIS, strict=True))
    symbols = sp.symbols("y0:18")
    remaining = tuple(
        tuple(symbols[6 * mode + i] for i in range(6))
        for mode in range(3)
    )
    c_value = c_tensor(*remaining)
    for side, kernel_vector in ((1, p1), (2, p2)):
        for name, quadratic in quadratics.items():
            actual = coefficient(quadratic, (kernel_vector, *remaining))
            expected = residual_value(residuals[side][name], c_value)
            assert sp.expand(actual - expected) == 0, (side, name)

    determinant1 = sp.factor(sp.Matrix.hstack(*(
        sp.Matrix(residuals[1][name])
        for name in ("m2", "d0", "d1", "d2")
    )).det())
    determinant2 = sp.factor(sp.Matrix.hstack(*(
        sp.Matrix(residuals[2][name])
        for name in ("m1", "d0", "d1", "d2")
    )).det())
    assert determinant1 == 8 * a**2 * b * (a + b)
    assert determinant2 == -8 * a**2 * b * (a - b)

    zero_channels = {
        1: (({a: 0}, "d2"), ({b: 0}, "d0"), ({b: -a}, "d1")),
        2: (({a: 0}, "d2"), ({b: 0}, "d1")),
    }
    for side, cases in zero_channels.items():
        for substitution, channel in cases:
            assert all(
                sp.expand(sp.sympify(value).subs(substitution)) == 0
                for value in residuals[side][channel]
            )
    c1_relation = tuple(
        sp.expand((residuals[2]["d0"][i] - 2 * residuals[2]["m1"][i]).subs(b, a))
        for i in range(4)
    )
    assert c1_relation == (0, 0, 0, 0)

    lines = {
        "Phi1": ((0, 1, 1, 0), (1, 0, 1, 0), (1, -1, 0, 0)),
        "Phi2": ((0, 1, 1, 0), (1, 0, 0, 1), (1, 1, 1, 1)),
    }
    for vector in lines["Phi1"]:
        assert phi1 * sp.Matrix((*vector, 0, 0)) == sp.zeros(4, 1)
    for vector in lines["Phi2"]:
        assert phi2 * sp.Matrix((*vector, 0, 0)) == sp.zeros(4, 1)
    return {
        "kernel_dimensions": (2, 2),
        "generic_determinants": (determinant1, determinant2),
        "exceptional_lines": lines,
        "phi2_nonvanishing_exceptional_identity": "i_p(d0)=2*i_p(m1)",
        "square_free_contractions_checked": 10,
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
    return tuple(states)


def modular_j(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate the hyperbolic form modulo a prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def compatible(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
    prime: int,
) -> bool:
    """Test every different-colour cross-orthogonality equation."""
    return all(
        first_colour == second_colour
        or modular_j(first[first_colour], second[second_colour], prime) == 0
        for first_colour in range(3)
        for second_colour in range(3)
    )


def assert_cross_orthogonality_lemma(prime: int) -> dict[str, int]:
    """Exhaust the projective A-level lemma over one odd finite field."""
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
                    colour
                    for colour in range(3)
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
        "states": len(states),
        "arrays": len(arrays),
        "compatible_triples": compatible_triples,
        "two_active_triples": two_active,
    }


def assert_rank_gates() -> dict[str, int]:
    """Replay the two dimension inequalities used in the written proof."""
    ambient_dimension = 6
    local_dimension = 3
    residual_dimension = 4
    kernel_rank_ceiling = ambient_dimension - local_dimension
    assert kernel_rank_ceiling == 3 < residual_dimension

    general_d = sp.symbols("d", integer=True, positive=True)
    assert sp.simplify((general_d + 2 - 3) - (general_d - 1)) == 0
    return {
        "ambient_dimension": ambient_dimension,
        "local_dimension": local_dimension,
        "kernel_rank_ceiling": kernel_rank_ceiling,
        "forbidden_scalar_rank": residual_dimension,
    }


def main() -> None:
    """Run all exact primary checks."""
    pair = assert_pair()
    contractions = assert_kernels_and_contractions()
    ranks = assert_rank_gates()
    finite_fields = {
        prime: assert_cross_orthogonality_lemma(prime)
        for prime in (3, 5)
    }
    print("star-pair kernel-support boundary primary checks: PASS")
    print(f"  pair: {pair}")
    print(f"  contractions: {contractions}")
    print(f"  rank gates: {ranks}")
    print(f"  finite-field lemma audits: {finite_fields}")


if __name__ == "__main__":
    main()
