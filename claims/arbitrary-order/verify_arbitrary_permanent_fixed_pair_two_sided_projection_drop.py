"""Primary exact checks for the fixed-pair two-sided projection-drop theorem."""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement, permutations

import sympy as sp

Vector = tuple[sp.Expr, ...]
Polynomial = dict[int, sp.Expr]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (0, 1, -1, 0, 0, -1)
M2 = (0, 0, 0, 1, -1, -1)
D0 = (1, 1, 0, 0, -1, -1)
D1 = (1, 0, -1, 1, 0, -1)
D2 = (0, 0, 0, 0, 0, -2)
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
    """Encode a first-four-coordinate quadratic in edge order."""
    return {
        (1 << first) | (1 << second): sp.Integer(value)
        for value, (first, second) in zip(vector, EDGES, strict=True)
        if value
    }


def coefficient(quadratic: tuple[int, ...], vectors: list[Vector]) -> sp.Expr:
    """Return the full square-free coefficient of q times four forms."""
    result: Polynomial = quadratic_form(quadratic)
    for vector in vectors:
        result = square_free_multiply(result, linear_form(vector))
    return sp.expand(result.get(FULL_MASK, 0))


def polarized_product(factors: list[Vector], vectors: list[Vector]) -> sp.Expr:
    """Evaluate the polarization of a product of four covectors."""
    assert len(factors) == len(vectors) == 4
    return sp.expand(sum(
        sp.prod(
            sum(factors[row][coordinate] * vectors[column][coordinate]
                for coordinate in range(6))
            for row, column in enumerate(order)
        )
        for order in permutations(range(4))
    ))


def edge_product(left: Vector, right: Vector) -> Vector:
    """Multiply two four-coordinate forms in the square-free algebra."""
    return tuple(
        sp.expand(left[first] * right[second] + left[second] * right[first])
        for first, second in EDGES
    )


def complement_pair(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the perfect edge-complement pairing in four variables."""
    return sp.expand(sum(left[index] * right[5 - index] for index in range(6)))


def assert_fixed_tensors_and_symmetry() -> dict[str, object]:
    """Check the five displayed quartics and the x0/x1 symmetry."""
    x = [tuple(sp.Integer(i == j) for i in range(6)) for j in range(6)]
    ell1 = tuple(x[3][i] - x[2][i] - x[0][i] for i in range(6))
    ell2 = tuple(x[3][i] - x[2][i] - x[1][i] for i in range(6))
    factors = {
        M1: [x[4], x[5], x[1], ell1],
        M2: [x[4], x[5], x[0], ell2],
        D0: [x[4], x[5], tuple(x[1][i] + x[2][i] for i in range(6)),
             tuple(x[3][i] - x[0][i] for i in range(6))],
        D1: [x[4], x[5], tuple(x[0][i] + x[2][i] for i in range(6)),
             tuple(x[3][i] - x[1][i] for i in range(6))],
        D2: [x[4], x[5], x[0], x[1]],
    }

    symbols = sp.symbols("y0:24")
    generic = [tuple(symbols[6 * mode + i] for i in range(6)) for mode in range(4)]
    signs = {M1: 1, M2: 1, D0: 1, D1: 1, D2: -2}
    for quadratic, factor_rows in factors.items():
        actual = coefficient(quadratic, generic)
        expected = signs[quadratic] * polarized_product(factor_rows, generic)
        assert sp.expand(actual - expected) == 0

    swap = (1, 0, 2, 3, 4, 5)

    def swap_quadratic(quadratic: tuple[int, ...]) -> tuple[int, ...]:
        edge_values = {edge: value for edge, value in zip(EDGES, quadratic, strict=True)}
        transformed = []
        for first, second in EDGES:
            source = tuple(sorted((swap[first], swap[second])))
            transformed.append(edge_values[source])
        return tuple(transformed)

    assert swap_quadratic(M1) == M2
    assert swap_quadratic(M2) == M1
    assert swap_quadratic(D0) == D1
    assert swap_quadratic(D1) == D0
    assert swap_quadratic(D2) == D2
    return {"quartics_checked": 5, "x0_x1_swap": "m1<->m2, d0<->d1"}


def assert_common_kernel_and_contractions() -> dict[str, object]:
    """Check the kernel N and all single/double contraction identities."""
    phi1 = sp.Matrix([
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [-1, 0, -1, 1, 0, 0],
    ])
    phi2 = sp.Matrix([
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, -1, -1, 1, 0, 0],
    ])
    ell1 = phi1.row(3)
    restricted_kernel = sp.Matrix.vstack(ell1, phi2)
    kernel = restricted_kernel.nullspace()
    n_vector = sp.Matrix([0, 0, 1, 1, 0, 0])
    assert len(kernel) == 1
    assert kernel[0] == n_vector

    x = [tuple(sp.Integer(i == j) for i in range(6)) for j in range(6)]
    factors = {
        "m1": [x[4], x[5], x[1], tuple(x[3][i] - x[2][i] - x[0][i] for i in range(6))],
        "m2": [x[4], x[5], x[0], tuple(x[3][i] - x[2][i] - x[1][i] for i in range(6))],
        "d0": [x[4], x[5], tuple(x[1][i] + x[2][i] for i in range(6)),
               tuple(x[3][i] - x[0][i] for i in range(6))],
        "d1": [x[4], x[5], tuple(x[0][i] + x[2][i] for i in range(6)),
               tuple(x[3][i] - x[1][i] for i in range(6))],
        "d2": [x[4], x[5], x[0], x[1]],
    }
    n = tuple(n_vector)
    y_symbols = sp.symbols("y0:6")
    z_symbols = sp.symbols("z0:6")
    w_symbols = sp.symbols("w0:6")
    y = tuple(y_symbols)
    z = tuple(z_symbols)
    w = tuple(w_symbols)

    assert polarized_product(factors["d2"], [n, y, z, w]) == 0
    doubles = {
        name: sp.factor(polarized_product(rows, [n, n, y, z]))
        for name, rows in factors.items()
    }
    j_value = y[4] * z[5] + y[5] * z[4]
    assert doubles["m1"] == doubles["m2"] == doubles["d2"] == 0
    assert sp.expand(doubles["d0"] - 2 * j_value) == 0
    assert sp.expand(doubles["d1"] - 2 * j_value) == 0

    j_matrix = sp.zeros(4)
    j_matrix[1, 2] = j_matrix[2, 1] = 1
    assert j_matrix.rank() == 2
    assert j_matrix.nullspace() == [sp.eye(4).col(0), sp.eye(4).col(3)]
    return {
        "rank_phi1": phi1.rank(),
        "rank_phi2": phi2.rank(),
        "restricted_kernel": tuple(n_vector),
        "double_contractions": doubles,
        "J_radical_dimension": len(j_matrix.nullspace()),
    }


def assert_product_space_geometry() -> dict[str, object]:
    """Check both HP equality models and the exceptional orthogonal pair."""
    e = [tuple(sp.Integer(i == j) for i in range(4)) for j in range(4)]
    t = sp.symbols("t", nonzero=True)

    def product_space(left: list[Vector], right: list[Vector]) -> sp.Matrix:
        return sp.Matrix.hstack(*(
            sp.Matrix(edge_product(x, y)) for x in left for y in right
        )).T.rref()[0]

    h_type_a = [e[1], e[2], e[3]]
    p_type_a = [e[1], e[2]]
    q_type_a = product_space(h_type_a, p_type_a)
    assert q_type_a.rank() == 3

    p = [e[2], e[3]]
    h_plus = [e[2], e[3], tuple(e[0][i] + t * e[1][i] for i in range(4))]
    h_minus = [e[2], e[3], tuple(e[0][i] - t * e[1][i] for i in range(4))]
    q_plus_vectors = [edge_product(x, y) for x in h_plus for y in p]
    q_minus_vectors = [edge_product(x, y) for x in h_minus for y in p]
    q_plus = sp.Matrix(q_plus_vectors)
    q_minus = sp.Matrix(q_minus_vectors)
    assert q_plus.rank() == q_minus.rank() == 3
    assert all(complement_pair(x, y) == 0 for x in q_plus_vectors for y in q_minus_vectors)

    # The exceptional hyperplanes intersect in exactly P.
    h_plus_matrix = sp.Matrix(h_plus).T
    h_minus_matrix = sp.Matrix(h_minus).T
    assert sp.Matrix.hstack(h_plus_matrix, h_minus_matrix).rank() == 4
    assert h_plus_matrix.rank() == h_minus_matrix.rank() == 3
    return {
        "type_A_rank": q_type_a.rank(),
        "type_B_ranks": (q_plus.rank(), q_minus.rank()),
        "exceptional_pairing": "Q(t) perpendicular Q(-t)",
    }


def assert_sensor_rank_row() -> dict[str, object]:
    """Recompute the ell1 row of the predecessor's 16-cell rank table."""
    covectors = {
        "ell1": (-1, 0, -1, 1, 0, 0),
        "x0": (1, 0, 0, 0, 0, 0),
        "x4": (0, 0, 0, 0, 1, 0),
        "x5": (0, 0, 0, 0, 0, 1),
        "ell2": (0, -1, -1, 1, 0, 0),
    }
    ranks: dict[str, int] = {}
    for name in ("x0", "x4", "x5", "ell2"):
        defining = sp.Matrix([covectors["ell1"], covectors[name]])
        basis = [tuple(vector) for vector in defining.nullspace()]
        assert len(basis) == 4
        rows = []
        for indices in combinations_with_replacement(range(4), 4):
            vectors = [basis[index] for index in indices]
            rows.append([coefficient(q, vectors) for q in B_BASIS])
        ranks[name] = sp.Matrix(rows).rank()
    assert ranks == {"x0": 2, "x4": 0, "x5": 0, "ell2": 2}
    return ranks


def main() -> None:
    tensors = assert_fixed_tensors_and_symmetry()
    contractions = assert_common_kernel_and_contractions()
    products = assert_product_space_geometry()
    sensor_ranks = assert_sensor_rank_row()

    print("fixed-pair two-sided projection-drop primary checks: PASS")
    print(f"  fixed tensors and symmetry: {tensors}")
    print(f"  common-kernel contractions: {contractions}")
    print(f"  HP and exceptional geometry: {products}")
    print(f"  ell1 sensor-rank row: {sensor_ranks}")


if __name__ == "__main__":
    main()
