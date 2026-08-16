"""Primary exact checks for the star-pair singleton N/N exclusion."""

from __future__ import annotations

from itertools import combinations

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
SOURCE_QUADRATICS = {"m1": M1, "m2": M2, "d0": D0, "d1": D1, "d2": D2}

N = (0, 1, 1, 0)
Q = (0, 0, 1, 1)


def first_four_product(left: Vector, right: Vector) -> tuple[sp.Expr, ...]:
    """Multiply first-four-coordinate forms in square-free edge order."""
    return tuple(
        sp.expand(left[first] * right[second] + left[second] * right[first])
        for first, second in EDGES
    )


def complement_core_matrix(quadratic: tuple[int, ...]) -> sp.Matrix:
    """Return the symmetric matrix of the complementary star core."""
    matrix = sp.zeros(4)
    vertices = set(range(4))
    for coefficient, edge in zip(quadratic, EDGES, strict=True):
        first, second = sorted(vertices - set(edge))
        matrix[first, second] += coefficient
        matrix[second, first] += coefficient
    return matrix


CORES = {
    name: complement_core_matrix(quadratic)
    for name, quadratic in SOURCE_QUADRATICS.items()
}


def contract(name: str, vector: Vector) -> sp.Matrix:
    """Contract one R slot of a complementary core."""
    return CORES[name] * sp.Matrix(vector)


def double_contract(name: str, first: Vector, second: Vector) -> sp.Expr:
    """Contract two distinct R slots of a complementary core."""
    return sp.expand((sp.Matrix(first).T * CORES[name] * sp.Matrix(second))[0])


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply polynomials in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return {mask: value for mask, value in result.items() if value != 0}


def quartic_coefficient(quadratic: tuple[int, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Extract the full coefficient after multiplying q by four forms."""
    polynomial: Polynomial = {
        (1 << first) | (1 << second): sp.Integer(value)
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        linear = {
            1 << index: sp.sympify(value)
            for index, value in enumerate(vector)
            if value != 0
        }
        polynomial = square_free_multiply(polynomial, linear)
    return sp.expand(polynomial.get(FULL_MASK, 0))


def j_form(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the x4,x5 hyperbolic form."""
    return sp.expand(left[4] * right[5] + left[5] * right[4])


def p_xuv(first: Vector, second: Vector, third: Vector) -> sp.Expr:
    """Evaluate the full polarization of XUV on E=K^3."""
    return sp.expand(
        first[0] * (second[1] * third[2] + second[2] * third[1])
        + first[1] * (second[0] * third[2] + second[2] * third[0])
        + first[2] * (second[0] * third[1] + second[1] * third[0])
    )


def assert_star_and_forced_rows() -> dict[str, object]:
    """Reconstruct the five cores and the exact N/Q contractions."""
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
    assert products[0][1] == M1
    assert products[1][0] == M2
    assert products[0][0] == D0
    assert products[1][1] == D1
    assert products[2][2] == D2
    assert sp.Matrix([entry for row in products for entry in row]).rank() == 5

    n_rows = {name: tuple(contract(name, N)) for name in SOURCE_QUADRATICS}
    assert n_rows == {
        "m1": (0, 0, 0, 0),
        "m2": (0, 0, 0, 0),
        "d0": (1, -1, -1, 1),
        "d1": (-1, -1, -1, 1),
        "d2": (0, 0, 0, 0),
    }
    q_rows = {name: tuple(contract(name, Q)) for name in SOURCE_QUADRATICS}
    assert q_rows["d2"] == (2, 0, 0, 0)
    h0 = sp.Matrix(n_rows["d0"])
    h1 = sp.Matrix(n_rows["d1"])
    assert (h0 - h1) / 2 == sp.Matrix((1, 0, 0, 0))
    return {
        "source_rank": 5,
        "N_rows": n_rows,
        "Q_d2_row": q_rows["d2"],
        "x0_from_h_rows": tuple((h0 - h1) / 2),
    }


def assert_slice_dichotomy_and_annihilator() -> dict[str, object]:
    """Check the two forced image lines and the XUV annihilator minors."""
    coordinate_matrices = []
    for colour in range(3):
        matrix = sp.zeros(3)
        matrix[colour, colour] = 1
        coordinate_matrices.append(matrix)
    for singleton_colour in (0, 1):
        assert sp.Matrix.hstack(
            coordinate_matrices[singleton_colour].reshape(9, 1),
            coordinate_matrices[2].reshape(9, 1),
        ).rank() == 2

    x, u, v = sp.symbols("x u v")
    basis = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    d = (x, u, v)
    matrix = sp.Matrix(3, 3, lambda row, column: p_xuv(basis[row], basis[column], d))
    expected = sp.Matrix(((0, v, u), (v, 0, x), (u, x, 0)))
    assert matrix == expected
    principal_minors = tuple(
        sp.factor(matrix.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert principal_minors == (-v**2, -u**2, -x**2)
    assert sp.factor(matrix.det()) == 2 * u * v * x
    return {
        "forced_image_rank": 2,
        "slice_rank_cases": (2, 3),
        "annihilator_matrix": matrix,
        "principal_two_minors": principal_minors,
    }


def assert_core_identity() -> dict[str, object]:
    """Verify g_d0-g_d1=2g_m1 on the x0 hyperplane."""
    difference = CORES["d0"] - CORES["d1"] - 2 * CORES["m1"]
    expected = sp.zeros(4)
    expected[0, 1] = expected[1, 0] = 1
    expected[0, 2] = expected[2, 0] = 1
    expected[0, 3] = expected[3, 0] = -1
    assert difference == expected
    assert difference.extract((1, 2, 3), (1, 2, 3)) == sp.zeros(3)

    p1, p2, p3, q1, q2, q3 = sp.symbols("p1 p2 p3 q1 q2 q3")
    first = (0, p1, p2, p3)
    second = (0, q1, q2, q3)
    identity = sp.expand(
        double_contract("d0", first, second)
        - double_contract("d1", first, second)
        - 2 * double_contract("m1", first, second)
    )
    assert identity == 0
    return {
        "global_difference_matrix": difference,
        "x0_hyperplane_difference_rank": 0,
        "singleton_colours_checked": (0, 1),
    }


def assert_full_quartic_factorizations() -> dict[str, object]:
    """Check both all-colour factorizations in the full square-free algebra."""
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    c = sp.symbols("c0:6")
    d = sp.symbols("d0:6")

    # Rank-three case: the a,b vectors have zero x0,x4,x5 coordinates.
    rank_three_a: Vector = (0, a[1], a[2], a[3], 0, 0)
    rank_three_b: Vector = (0, b[1], b[2], b[3], 0, 0)
    generic_c: Vector = tuple(c)
    generic_d: Vector = tuple(d)

    # Rank-two case: the c,d vectors have zero x0,x4,x5 coordinates.
    generic_a: Vector = tuple(a)
    generic_b: Vector = tuple(b)
    rank_two_c: Vector = (0, c[1], c[2], c[3], 0, 0)
    rank_two_d: Vector = (0, d[1], d[2], d[3], 0, 0)

    checked = 0
    for name, quadratic in SOURCE_QUADRATICS.items():
        actual_rank_three = quartic_coefficient(
            quadratic,
            (rank_three_a, rank_three_b, generic_c, generic_d),
        )
        expected_rank_three = sp.expand(
            double_contract(name, rank_three_a[:4], rank_three_b[:4])
            * j_form(generic_c, generic_d)
        )
        assert sp.expand(actual_rank_three - expected_rank_three) == 0

        actual_rank_two = quartic_coefficient(
            quadratic,
            (generic_a, generic_b, rank_two_c, rank_two_d),
        )
        expected_rank_two = sp.expand(
            j_form(generic_a, generic_b)
            * double_contract(name, rank_two_c[:4], rank_two_d[:4])
        )
        assert sp.expand(actual_rank_two - expected_rank_two) == 0
        checked += 2
    return {
        "channels": tuple(SOURCE_QUADRATICS),
        "symbolic_full_factorizations": checked,
        "same_mode_double_contractions_used": 0,
    }


def main() -> None:
    """Run all primary exact checks."""
    star = assert_star_and_forced_rows()
    slices = assert_slice_dichotomy_and_annihilator()
    core_identity = assert_core_identity()
    factorizations = assert_full_quartic_factorizations()
    print("star-pair singleton N/N exclusion primary checks: PASS")
    print(f"  star and forced rows: {star}")
    print(f"  slice dichotomy and annihilator: {slices}")
    print(f"  star-core identity: {core_identity}")
    print(f"  full quartic factorizations: {factorizations}")


if __name__ == "__main__":
    main()
