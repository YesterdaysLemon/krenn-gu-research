"""Primary exact checks for the triangle-pair two-sided rank-drop theorem."""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement, permutations

import sympy as sp

Vector = tuple[sp.Expr, ...]
Polynomial = dict[int, sp.Expr]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (1, -1, 0, -1, 0, 0)
M2 = (0, 0, 0, 0, 1, -1)
D0 = (0, 0, 0, 2, 0, 0)
D1 = (0, 0, 1, 0, 1, 0)
D2 = (0, 0, -1, 0, 0, 1)
B_BASIS = (M1, M2, D0, D1, D2)


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply sparse polynomials in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(
                result.get(mask, sp.Integer(0)) + left_value * right_value
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
    """Encode a first-four-coordinate quadratic in edge order."""
    return {
        (1 << first) | (1 << second): sp.Integer(value)
        for value, (first, second) in zip(vector, EDGES, strict=True)
        if value
    }


def coefficient(quadratic: tuple[int, ...], vectors: list[Vector]) -> sp.Expr:
    """Extract the full square-free coefficient of q times four forms."""
    result = quadratic_form(quadratic)
    for vector in vectors:
        result = square_free_multiply(result, linear_form(vector))
    return sp.expand(result.get(FULL_MASK, sp.Integer(0)))


def polarized_product(factors: list[Vector], vectors: list[Vector]) -> sp.Expr:
    """Evaluate the polarization of a product of four covectors."""
    assert len(factors) == len(vectors) == 4
    return sp.expand(
        sum(
            sp.prod(
                sum(
                    factors[row][coordinate] * vectors[column][coordinate]
                    for coordinate in range(6)
                )
                for row, column in enumerate(order)
            )
            for order in permutations(range(4))
        )
    )


def edge_product(left: Vector, right: Vector) -> Vector:
    """Multiply two four-coordinate forms in the square-free algebra."""
    return tuple(
        sp.expand(left[first] * right[second] + left[second] * right[first])
        for first, second in EDGES
    )


def complement_pair(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the perfect edge-complement pairing."""
    return sp.expand(sum(left[index] * right[5 - index] for index in range(6)))


def coordinate_vectors(dimension: int) -> list[Vector]:
    """Return the standard coordinate vectors."""
    return [
        tuple(sp.Integer(index == position) for index in range(dimension))
        for position in range(dimension)
    ]


def add_vectors(*vectors: Vector) -> Vector:
    """Add coordinate vectors."""
    return tuple(sum(vector[index] for vector in vectors) for index in range(len(vectors[0])))


def scale_vector(value: sp.Expr, vector: Vector) -> Vector:
    """Scale a coordinate vector."""
    return tuple(sp.expand(value * entry) for entry in vector)


def triangle_frames() -> tuple[tuple[Vector, ...], tuple[Vector, ...]]:
    """Return the two fixed local colour frames."""
    left = (
        (0, 1, -1, 0),
        (0, 0, 0, 1),
        (-1, 0, 1, 0),
    )
    right = (
        (0, -1, 1, 0),
        (1, 1, 0, 0),
        (0, 0, 0, 1),
    )
    return left, right


def assert_pair_and_quartics() -> dict[str, object]:
    """Check the product table, equality five, and all Hodge quartics."""
    left, right = triangle_frames()
    table = tuple(tuple(edge_product(u, v) for v in right) for u in left)
    expected = (
        (D0, M1, M2),
        (tuple(-value for value in M2), D1, (0, 0, 0, 0, 0, 0)),
        (M1, tuple(-value for value in M1), D2),
    )
    assert table == expected
    assert sp.Matrix(B_BASIS).rank() == 5
    assert sp.Matrix((M1, M2)).rank() == 2

    x = coordinate_vectors(6)
    ell1 = add_vectors(x[2], scale_vector(-1, x[1]), scale_vector(-1, x[0]))
    ell2 = add_vectors(x[2], scale_vector(-1, x[1]))
    factors = {
        M1: (1, [x[4], x[5], x[3], ell1]),
        M2: (1, [x[4], x[5], x[0], ell2]),
        D0: (2, [x[4], x[5], x[0], x[3]]),
        D1: (1, [x[4], x[5], x[2], add_vectors(x[0], x[1])]),
        D2: (1, [x[4], x[5], x[1], add_vectors(x[0], scale_vector(-1, x[2]))]),
    }
    symbols = sp.symbols("y0:24")
    generic = [tuple(symbols[6 * mode + index] for index in range(6)) for mode in range(4)]
    for quadratic, (scale, rows) in factors.items():
        actual = coefficient(quadratic, generic)
        expected_value = scale * polarized_product(rows, generic)
        assert sp.expand(actual - expected_value) == 0
    return {"pair_product_rank": 5, "mixed_rank": 2, "quartics_checked": 5}


def projection_matrices() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    """Return Phi_1, Phi_2, ell_1, and ell_2 matrices."""
    phi1 = sp.Matrix(
        (
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 0, 1, 0),
            (0, 0, 0, 0, 0, 1),
            (-1, -1, 1, 0, 0, 0),
        )
    )
    phi2 = sp.Matrix(
        (
            (1, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 0),
            (0, 0, 0, 0, 0, 1),
            (0, -1, 1, 0, 0, 0),
        )
    )
    return phi1, phi2, phi1.row(3), phi2.row(3)


def assert_restricted_kernels() -> dict[str, object]:
    """Check both asymmetric restricted kernels and the fixed high image."""
    phi1, phi2, ell1, ell2 = projection_matrices()
    n_vector = sp.Matrix((0, 1, 1, 0, 0, 0))
    x3_vector = sp.Matrix((0, 0, 0, 1, 0, 0))

    kernel_on_ell2 = sp.Matrix.vstack(ell2, phi1).nullspace()
    assert kernel_on_ell2 == [n_vector]

    kernel_on_ell1 = sp.Matrix.vstack(ell1, phi2).nullspace()
    assert kernel_on_ell1 == [n_vector, x3_vector]

    # On ell_1=0, ell_2=x_0, so the Phi_2 image is z_3=z_0.
    assert ell2 - phi2.row(0) == ell1
    h_bar = sp.Matrix.hstack(
        sp.Matrix((1, 0, 0, 1)),
        sp.Matrix((0, 1, 0, 0)),
        sp.Matrix((0, 0, 1, 0)),
    )
    assert h_bar.rank() == 3
    return {
        "ker_Phi1_on_ell2": tuple(n_vector),
        "ker_Phi2_on_ell1": (tuple(n_vector), tuple(x3_vector)),
        "fixed_high_equation": "z3=z0",
    }


def factor_rows() -> dict[str, list[Vector]]:
    """Return the five factored complementary quartics."""
    x = coordinate_vectors(6)
    ell1 = add_vectors(x[2], scale_vector(-1, x[1]), scale_vector(-1, x[0]))
    ell2 = add_vectors(x[2], scale_vector(-1, x[1]))
    return {
        "m1": [x[4], x[5], x[3], ell1],
        "m2": [x[4], x[5], x[0], ell2],
        "d0": [x[4], x[5], x[0], x[3]],
        "d1": [x[4], x[5], x[2], add_vectors(x[0], x[1])],
        "d2": [x[4], x[5], x[1], add_vectors(x[0], scale_vector(-1, x[2]))],
    }


def assert_contractions() -> dict[str, object]:
    """Check the N and x3+sN contraction identities symbolically."""
    rows = factor_rows()
    x = coordinate_vectors(6)
    n = add_vectors(x[1], x[2])
    y = tuple(sp.symbols("y0:6"))
    z = tuple(sp.symbols("z0:6"))
    w = tuple(sp.symbols("w0:6"))
    j_value = y[4] * z[5] + y[5] * z[4]

    assert polarized_product(rows["d0"], [n, y, z, w]) == 0
    n_doubles = {
        name: sp.factor(polarized_product(factors, [n, n, y, z]))
        for name, factors in rows.items()
    }
    assert n_doubles["m1"] == n_doubles["m2"] == n_doubles["d0"] == 0
    assert sp.expand(n_doubles["d1"] - 2 * j_value) == 0
    assert sp.expand(n_doubles["d2"] + 2 * j_value) == 0

    s_value, t_value = sp.symbols("s t")
    k_s = add_vectors(x[3], scale_vector(s_value, n))
    k_t = add_vectors(x[3], scale_vector(t_value, n))
    variable_doubles = {
        name: sp.factor(polarized_product(factors, [k_s, k_t, y, z]))
        for name, factors in rows.items()
    }
    assert variable_doubles["m1"] == variable_doubles["m2"] == 0
    assert variable_doubles["d0"] == 0
    assert sp.expand(variable_doubles["d1"] - 2 * s_value * t_value * j_value) == 0
    assert sp.expand(variable_doubles["d2"] + 2 * s_value * t_value * j_value) == 0

    assert polarized_product(rows["d1"], [x[3], y, z, w]) == 0
    assert polarized_product(rows["d2"], [x[3], y, z, w]) == 0
    return {
        "N_double": {"d0": 0, "d1": "+2J", "d2": "-2J"},
        "variable_double": {"d0": 0, "d1": "+2stJ", "d2": "-2stJ"},
    }


def assert_sensor_table() -> dict[str, object]:
    """Recompute all sixteen double common-factor sensor ranks."""
    covectors = {
        "x3": (0, 0, 0, 1, 0, 0),
        "x4": (0, 0, 0, 0, 1, 0),
        "x5": (0, 0, 0, 0, 0, 1),
        "ell1": (-1, -1, 1, 0, 0, 0),
        "x0": (1, 0, 0, 0, 0, 0),
        "ell2": (0, -1, 1, 0, 0, 0),
    }
    row_names = ("x3", "x4", "x5", "ell1")
    column_names = ("x0", "x4", "x5", "ell2")
    expected = {
        "x3": (1, 0, 0, 2),
        "x4": (0, 0, 0, 0),
        "x5": (0, 0, 0, 0),
        "ell1": (1, 0, 0, 1),
    }
    ranks: dict[str, tuple[int, ...]] = {}
    for row_name in row_names:
        row_ranks = []
        for column_name in column_names:
            defining = sp.Matrix((covectors[row_name], covectors[column_name]))
            basis = [tuple(vector) for vector in defining.nullspace()]
            sensor_rows = []
            for indices in combinations_with_replacement(range(len(basis)), 4):
                vectors = [basis[index] for index in indices]
                sensor_rows.append([coefficient(q, vectors) for q in B_BASIS])
            row_ranks.append(int(sp.Matrix(sensor_rows).rank()))
        ranks[row_name] = tuple(row_ranks)
    assert ranks == expected
    return {"columns": column_names, "rows": ranks}


def assert_profile_and_radical_geometry() -> dict[str, object]:
    """Check the exceptional HP geometry and both J-radical calculations."""
    e = coordinate_vectors(4)
    parameter = sp.symbols("t", nonzero=True)
    plane = (e[2], e[3])
    h_plus = (
        e[2],
        e[3],
        add_vectors(e[0], scale_vector(parameter, e[1])),
    )
    h_minus = (
        e[2],
        e[3],
        add_vectors(e[0], scale_vector(-parameter, e[1])),
    )
    plus_products = [edge_product(left, right) for left in h_plus for right in plane]
    minus_products = [edge_product(left, right) for left in h_minus for right in plane]
    assert sp.Matrix(plus_products).rank() == sp.Matrix(minus_products).rank() == 3
    assert all(
        complement_pair(left, right) == 0
        for left in plus_products
        for right in minus_products
    )
    assert sp.Matrix.hstack(sp.Matrix(h_plus).T, sp.Matrix(h_minus).T).rank() == 4

    j_matrix = sp.zeros(4)
    j_matrix[1, 2] = j_matrix[2, 1] = 1
    radical = [sp.eye(4).col(0), sp.eye(4).col(3)]
    assert j_matrix.rank() == 2
    assert j_matrix.nullspace() == radical

    h_bar = sp.Matrix.hstack(
        sp.Matrix((1, 0, 0, 1)),
        sp.Matrix((0, 1, 0, 0)),
        sp.Matrix((0, 0, 1, 0)),
    )
    h_bar_orthogonal = (h_bar.T * j_matrix).nullspace()
    assert h_bar_orthogonal == radical
    intersection_matrix = sp.Matrix.hstack(*radical, *h_bar.columnspace())
    intersection_dimension = len(radical) + h_bar.rank() - intersection_matrix.rank()
    assert intersection_dimension == 1
    return {
        "exceptional_highs_distinct": True,
        "J_rank": 2,
        "Hbar_orthogonal": "rad(J)",
        "Hbar_intersect_radical_dimension": intersection_dimension,
    }


def main() -> None:
    """Run all primary exact checks."""
    pair = assert_pair_and_quartics()
    kernels = assert_restricted_kernels()
    contractions = assert_contractions()
    sensors = assert_sensor_table()
    geometry = assert_profile_and_radical_geometry()
    print("triangle-pair two-sided projection-drop primary checks: PASS")
    print(f"  pair and quartics: {pair}")
    print(f"  restricted kernels: {kernels}")
    print(f"  contractions: {contractions}")
    print(f"  double common-factor sensors: {sensors}")
    print(f"  profile and radical geometry: {geometry}")


if __name__ == "__main__":
    main()
