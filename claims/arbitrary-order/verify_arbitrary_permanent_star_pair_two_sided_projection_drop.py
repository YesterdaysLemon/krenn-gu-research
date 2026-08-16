"""Primary exact checks for the star-pair two-sided projection-drop theorem."""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement

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


def coefficient(quadratic: tuple[int, ...], vectors: list[Vector]) -> sp.Expr:
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


def row_rank(rows: list[tuple[sp.Expr, ...]]) -> int:
    """Return exact row rank."""
    return sp.Matrix(rows).rank() if rows else 0


def complement_core(quadratic: tuple[int, ...], variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    """Return the first-four-coordinate core of star(q)."""
    return sp.expand(sum(
        value * sp.prod(
            variables[index]
            for index in range(4)
            if index not in (first, second)
        )
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
    ))


def assert_pair_and_quartics() -> dict[str, object]:
    """Reconstruct the pair products, radical plane, and five star cores."""
    u = [
        (-1, 0, 1, 0),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
    ]
    v = [
        (1, 1, -1, 1),
        (1, 1, 0, 0),
        (0, -1, 1, 0),
    ]
    products = [[first_four_product(u[i], v[j]) for j in range(3)] for i in range(3)]
    assert products[0][0] == D0
    assert products[1][1] == D1
    assert products[2][2] == D2
    assert products[0][1] == M1
    assert products[1][0] == M2
    assert products[0][2] == tuple(-value for value in M1)
    assert products[1][2] == tuple(-value for value in M2)
    assert products[2][0] == tuple(-2 * M1[i] - M2[i] for i in range(6))
    assert products[2][1] == tuple(-value for value in M1)
    assert row_rank([entry for row in products for entry in row]) == 5
    assert row_rank([products[i][j] for i in range(3) for j in range(3) if i != j]) == 2
    assert row_rank(list(B_BASIS)) == 5

    x = sp.symbols("x0:4")
    cores = {quadratic: sp.factor(complement_core(quadratic, x)) for quadratic in B_BASIS}
    assert cores[M1] == x[3] * (x[0] + x[1] - x[2])
    assert cores[M2] == (x[0] - x[3]) * (x[1] - x[2])
    assert cores[D0] == (
        x[0] * x[1] + x[0] * x[3] - x[1] * x[2]
        + 2 * x[1] * x[3] - x[2] * x[3]
    )
    assert cores[D1] == -x[2] * (x[0] + x[1] - x[3])
    assert cores[D2] == 2 * x[0] * x[3]
    return {
        "pair_product_rank": 5,
        "mixed_rank": 2,
        "star_cores": {str(key): value for key, value in cores.items()},
    }


def projection_covectors() -> dict[str, tuple[int, ...]]:
    """Return the six-coordinate covectors used by the projections."""
    return {
        "x3": (0, 0, 0, 1, 0, 0),
        "x4": (0, 0, 0, 0, 1, 0),
        "x5": (0, 0, 0, 0, 0, 1),
        "ell1": (1, 1, -1, 0, 0, 0),
        "z0": (1, 0, 0, -1, 0, 0),
        "ell2": (0, 1, -1, 0, 0, 0),
    }


def assert_projection_kernels() -> dict[str, object]:
    """Check all projection ranks and the three restricted kernels."""
    covectors = projection_covectors()
    phi1 = sp.Matrix([covectors[name] for name in ("x3", "x4", "x5", "ell1")])
    phi2 = sp.Matrix([covectors[name] for name in ("z0", "x4", "x5", "ell2")])
    assert phi1.rank() == phi2.rank() == 4
    n_vector = sp.Matrix([0, 1, 1, 0, 0, 0])
    restricted = {
        "ker(ell1) cap ker(Phi2)": sp.Matrix([
            covectors["ell1"], *phi2.tolist()
        ]).nullspace(),
        "ker(z0) cap ker(Phi1)": sp.Matrix([
            covectors["z0"], *phi1.tolist()
        ]).nullspace(),
        "ker(ell2) cap ker(Phi1)": sp.Matrix([
            covectors["ell2"], *phi1.tolist()
        ]).nullspace(),
    }
    assert all(kernel == [n_vector] for kernel in restricted.values())
    return {
        "projection_ranks": (phi1.rank(), phi2.rank()),
        "restricted_kernels": {name: tuple(kernel[0]) for name, kernel in restricted.items()},
    }


def assert_missing_factor_table() -> dict[str, object]:
    """Recompute all sixteen common-missing-factor sensor ranks."""
    covectors = projection_covectors()
    table: dict[str, list[int]] = {}
    for phi in ("x3", "x4", "x5", "ell1"):
        ranks = []
        for psi in ("z0", "x4", "x5", "ell2"):
            kernel = sp.Matrix([covectors[phi], covectors[psi]]).nullspace()
            assert len(kernel) in (4, 5)
            basis = [tuple(vector) for vector in kernel]
            rows = []
            for indices in combinations_with_replacement(range(len(basis)), 4):
                vectors = [basis[index] for index in indices]
                rows.append([coefficient(q, vectors) for q in B_BASIS])
            ranks.append(sp.Matrix(rows).rank())
        table[phi] = ranks
    expected = {
        "x3": [1, 0, 0, 2],
        "x4": [0, 0, 0, 0],
        "x5": [0, 0, 0, 0],
        "ell1": [3, 0, 0, 1],
    }
    assert table == expected
    return {"columns": ("z0", "x4", "x5", "ell2"), "rows": table}


def assert_common_kernel_contractions() -> dict[str, object]:
    """Check the single d2 contraction and all five double contractions."""
    n_vector = (0, 1, 1, 0, 0, 0)
    y_symbols = sp.symbols("y0:6")
    z_symbols = sp.symbols("z0:6")
    w_symbols = sp.symbols("w0:6")
    y = tuple(y_symbols)
    z = tuple(z_symbols)
    w = tuple(w_symbols)
    assert coefficient(D2, [n_vector, y, z, w]) == 0
    doubles = {
        name: sp.factor(coefficient(q, [n_vector, n_vector, y, z]))
        for name, q in zip(("m1", "m2", "d0", "d1", "d2"), B_BASIS, strict=True)
    }
    j_value = y[4] * z[5] + y[5] * z[4]
    assert doubles["m1"] == doubles["m2"] == doubles["d2"] == 0
    assert sp.expand(doubles["d0"] + 2 * j_value) == 0
    assert sp.expand(doubles["d1"] + 2 * j_value) == 0
    return {"single_d2": 0, "double_contractions": doubles}


def assert_exceptional_product_geometry() -> dict[str, object]:
    """Replay the opposite-hyperplane HP product and J-radical geometry."""
    basis = [tuple(sp.Integer(i == j) for i in range(4)) for j in range(4)]
    parameter = sp.symbols("tau", nonzero=True)
    plane = [basis[2], basis[3]]
    plus = [basis[2], basis[3], tuple(basis[0][i] + parameter * basis[1][i] for i in range(4))]
    minus = [basis[2], basis[3], tuple(basis[0][i] - parameter * basis[1][i] for i in range(4))]
    plus_products = [first_four_product(x, y) for x in plus for y in plane]
    minus_products = [first_four_product(x, y) for x in minus for y in plane]
    assert row_rank(plus_products) == row_rank(minus_products) == 3

    def complement_pair(left: Vector, right: Vector) -> sp.Expr:
        return sp.expand(sum(left[index] * right[5 - index] for index in range(6)))

    assert all(complement_pair(x, y) == 0 for x in plus_products for y in minus_products)
    j_matrix = sp.zeros(4)
    j_matrix[1, 2] = j_matrix[2, 1] = 1
    assert j_matrix.rank() == 2
    assert j_matrix.nullspace() == [sp.eye(4).col(0), sp.eye(4).col(3)]
    return {"HP_ranks": (3, 3), "J_radical": (0, 3)}


def assert_dangerous_cell_and_slice_obstruction() -> dict[str, object]:
    """Check the rational square and the rank-one-free first slice space."""
    s, t = sp.symbols("s t")
    x = (s, t, s + t, s)
    cores = [complement_core(q, sp.symbols("x0:4")) for q in (D0, D1, D2)]
    substitutions = dict(zip(sp.symbols("x0:4"), x, strict=True))
    restricted = [sp.expand(core.subs(substitutions)) for core in cores]
    assert restricted == [s * t - t**2, -s * t - t**2, 2 * s**2]

    c0, c1, c2 = sp.symbols("c0 c1 c2")
    general = sp.expand(c0 * restricted[0] + c1 * restricted[1] + c2 * restricted[2])
    expected = 2 * c2 * s**2 + (c0 - c1) * s * t - (c0 + c1) * t**2
    assert sp.expand(general - expected) == 0
    special = sp.factor(general.subs({c0: 1, c1: 2, c2: -sp.Rational(1, 24)}))
    assert special == -sp.Rational(1, 12) * (s + 6 * t) ** 2

    # Symmetric cubic monomial order:
    # r^3,r^2u,r^2v,ru^2,ruv,rv^2,u^3,u^2v,uv^2,v^3.
    slice_rows = [
        (0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
        (0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    ]
    assert row_rank(slice_rows) == 3
    alpha, beta, gamma, r, u, v = sp.symbols("alpha beta gamma r u v")
    cube = sp.Poly((alpha * r + beta * u + gamma * v) ** 3, r, u, v)
    pure_cube_coefficients = (
        cube.coeff_monomial(r**3),
        cube.coeff_monomial(u**3),
        cube.coeff_monomial(v**3),
    )
    assert pure_cube_coefficients == (alpha**3, beta**3, gamma**3)
    assert all(row[index] == 0 for row in slice_rows for index in (0, 6, 9))
    return {
        "restricted_diagonal_basis": restricted,
        "special_square": special,
        "slice_space_rank": 3,
        "cube_pure_coefficients": pure_cube_coefficients,
    }


def main() -> None:
    pair = assert_pair_and_quartics()
    kernels = assert_projection_kernels()
    missing = assert_missing_factor_table()
    contractions = assert_common_kernel_contractions()
    exceptional = assert_exceptional_product_geometry()
    dangerous = assert_dangerous_cell_and_slice_obstruction()

    print("star-pair two-sided projection-drop primary checks: PASS")
    print(f"  pair and complemented quartics: {pair}")
    print(f"  projection kernels: {kernels}")
    print(f"  common-missing-factor table: {missing}")
    print(f"  common-kernel contractions: {contractions}")
    print(f"  exceptional product geometry: {exceptional}")
    print(f"  dangerous-cell slice obstruction: {dangerous}")


if __name__ == "__main__":
    main()
