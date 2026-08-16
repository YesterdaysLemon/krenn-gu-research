"""Primary exact checks for the fixed-pair radius-two compression exclusion."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

import sympy as sp

Polynomial = dict[int, sp.Expr]
Vector = tuple[sp.Expr, ...]

EDGES = list(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (0, 1, -1, 0, 0, -1)
M2 = (0, 0, 0, 1, -1, -1)
D0 = (1, 1, 0, 0, -1, -1)
D1 = (1, 0, -1, 1, 0, -1)
D2 = (0, 0, 0, 0, 0, -2)


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply sparse polynomials in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return {mask: value for mask, value in result.items() if value != 0}


def product_of(polynomials: list[Polynomial]) -> Polynomial:
    """Multiply a list of square-free polynomials."""
    result: Polynomial = {0: sp.Integer(1)}
    for polynomial in polynomials:
        result = square_free_multiply(result, polynomial)
    return result


def linear_form(vector: Vector | tuple[int, ...]) -> Polynomial:
    """Encode one degree-one form."""
    return {
        1 << index: sp.sympify(value)
        for index, value in enumerate(vector)
        if value != 0
    }


def quadratic_form(vector: tuple[int, ...]) -> Polynomial:
    """Encode a first-four-variable quadratic in edge order."""
    return {
        (1 << first) | (1 << second): sp.Integer(value)
        for value, (first, second) in zip(vector, EDGES, strict=True)
        if value
    }


def coefficient(
    quadratic: tuple[int, ...],
    linear_vectors: list[Vector],
) -> sp.Expr:
    """Return the full square-free coefficient of q times four forms."""
    polynomial = product_of([
        quadratic_form(quadratic),
        *(linear_form(vector) for vector in linear_vectors),
    ])
    return sp.factor(polynomial.get(FULL_MASK, 0))


def j_pair(left: tuple[sp.Expr, sp.Expr], right: tuple[sp.Expr, sp.Expr]) -> sp.Expr:
    """Evaluate the special-coordinate hyperbolic pairing J."""
    return sp.expand(left[0] * right[1] + left[1] * right[0])


def w_vector(prefix: str) -> tuple[Vector, tuple[sp.Symbol, sp.Symbol], tuple[sp.Symbol, sp.Symbol]]:
    """Create a symbolic vector in W and its R,A coordinates."""
    alpha, beta, first, second = sp.symbols(
        f"{prefix}_alpha {prefix}_beta {prefix}_a {prefix}_b"
    )
    vector = (0, alpha, beta, alpha + beta, first, second)
    return vector, (alpha, beta), (first, second)


def v_vector() -> tuple[Vector, tuple[sp.Symbol, sp.Symbol, sp.Symbol]]:
    """Create a symbolic vector in V."""
    gamma, delta, epsilon = sp.symbols("gamma delta epsilon")
    return (
        gamma,
        delta,
        epsilon,
        gamma - delta + epsilon,
        0,
        0,
    ), (gamma, delta, epsilon)


def c_tensor(
    r_vectors: list[tuple[sp.Expr, sp.Expr]],
    a_vectors: list[tuple[sp.Expr, sp.Expr]],
) -> tuple[sp.Expr, sp.Expr]:
    """Evaluate the R-valued trilinear map C."""
    result = [sp.Integer(0), sp.Integer(0)]
    for mode in range(3):
        others = [index for index in range(3) if index != mode]
        scalar = j_pair(a_vectors[others[0]], a_vectors[others[1]])
        result[0] += r_vectors[mode][0] * scalar
        result[1] += r_vectors[mode][1] * scalar
    return sp.expand(result[0]), sp.expand(result[1])


def assert_coordinate_spaces() -> dict[str, object]:
    """Check the displayed bases and all defining compression equations."""
    w_basis = [
        (0, 1, 0, 1, 0, 0),
        (0, 0, 1, 1, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
    ]
    v_basis = [
        (1, 0, 0, 1, 0, 0),
        (0, 1, 0, -1, 0, 0),
        (0, 0, 1, 1, 0, 0),
    ]
    assert sp.Matrix(w_basis).T.rank() == 4
    assert sp.Matrix(v_basis).T.rank() == 3

    def ell1(vector: tuple[int, ...]) -> int:
        return vector[3] - vector[2] - vector[0]

    def ell2(vector: tuple[int, ...]) -> int:
        return vector[3] - vector[2] - vector[1]

    assert all(vector[0] == 0 and ell2(vector) == 0 for vector in w_basis)
    assert all(
        vector[4] == vector[5] == 0 and ell1(vector) == -vector[1]
        for vector in v_basis
    )

    q_matrix = sp.Matrix([
        [0, 0, 1],
        [1, -1, 1],
        [1, 0, 0],
    ])
    assert q_matrix.det() == 1
    p_matrix = sp.Matrix([
        [1, 1],
        [0, 1],
        [1, 0],
    ])
    assert p_matrix.rank() == 2
    assert p_matrix.row(0) == p_matrix.row(1) + p_matrix.row(2)
    assert all(p_matrix.extract(rows, (0, 1)).det() != 0 for rows in combinations(range(3), 2))
    return {
        "dim_W": 4,
        "dim_V": 3,
        "q_determinant": q_matrix.det(),
        "p_pair_minors": [
            p_matrix.extract(rows, (0, 1)).det()
            for rows in combinations(range(3), 2)
        ],
    }


def assert_sensor_factorization() -> dict[str, object]:
    """Check all five four-linear tensors with fully symbolic local vectors."""
    w_data = [w_vector(f"y{mode}") for mode in range(2, 5)]
    y_vectors = [entry[0] for entry in w_data]
    r_vectors = [entry[1] for entry in w_data]
    a_vectors = [entry[2] for entry in w_data]
    z, (gamma, delta, epsilon) = v_vector()
    c_value = c_tensor(r_vectors, a_vectors)

    p_values = (
        sp.expand(c_value[0] + c_value[1]),
        c_value[1],
        c_value[0],
    )
    q_values = (epsilon, gamma - delta + epsilon, gamma)
    sigmas = (2, 2, -2)

    diagonal_actual = []
    diagonal_expected = []
    for quadratic, sigma, p_value, q_value in zip(
        (D0, D1, D2), sigmas, p_values, q_values, strict=True
    ):
        actual = coefficient(quadratic, [*y_vectors, z])
        expected = sp.factor(sigma * q_value * p_value)
        assert sp.expand(actual - expected) == 0
        diagonal_actual.append(actual)
        diagonal_expected.append(expected)

    radical_values = [
        coefficient(quadratic, [*y_vectors, z])
        for quadratic in (M1, M2)
    ]
    assert radical_values == [0, 0]
    return {
        "diagonal_actual": diagonal_actual,
        "diagonal_expected": diagonal_expected,
        "mixed_radicals": radical_values,
    }


def assert_shell_reduction() -> dict[str, object]:
    """Check all 54 shell equations and their colour-diagonal implication."""
    p_rows = {
        0: (1, 1),
        1: (0, 1),
        2: (1, 0),
    }
    shell_histogram: Counter[tuple[int, int]] = Counter()
    covered_by_word: dict[tuple[int, int, int], tuple[int, ...]] = {}

    for anchor in range(3):
        for word in product(range(3), repeat=3):
            distance = sum(colour != anchor for colour in word)
            if distance in (1, 2):
                shell_histogram[(anchor, distance)] += 1

    assert sum(shell_histogram.values()) == 54
    assert all(shell_histogram[(anchor, 1)] == 6 for anchor in range(3))
    assert all(shell_histogram[(anchor, 2)] == 12 for anchor in range(3))

    for word in product(range(3), repeat=3):
        if word[0] == word[1] == word[2]:
            continue
        anchors = tuple(
            anchor
            for anchor in range(3)
            if sum(colour != anchor for colour in word) in (1, 2)
        )
        row_matrix = sp.Matrix([p_rows[anchor] for anchor in anchors])
        assert row_matrix.rank() == 2
        covered_by_word[word] = anchors
    assert len(covered_by_word) == 24
    return {
        "shell_histogram": dict(sorted(shell_histogram.items())),
        "nonconstant_words_forced_zero": len(covered_by_word),
    }


def assert_offdiagonal_rank_map() -> dict[str, object]:
    """Derive the rank-two R-block inside the off-diagonal contraction map."""
    r0, r1, a0, a1 = sp.symbols("r0 r1 a0 a1")
    s0, s1, b0, b1 = sp.symbols("s0 s1 b0 b1")
    w0, w1, c0, c1 = sp.symbols("w0 w1 c0 c1")
    c_value = c_tensor(
        [(r0, r1), (s0, s1), (w0, w1)],
        [(a0, a1), (b0, b1), (c0, c1)],
    )
    variables = (w0, w1, c0, c1)
    matrix = sp.Matrix([
        [sp.diff(component, variable) for variable in variables]
        for component in c_value
    ])
    scalar = sp.expand(a0 * b1 + a1 * b0)
    assert matrix[:, :2] == scalar * sp.eye(2)
    assert sp.factor(matrix[:, :2].det()) == scalar**2
    return {"contraction_matrix": matrix, "R_block_determinant": scalar**2}


def assert_rank_case_algebra() -> dict[str, object]:
    """Check the hyperbolic-line and normalized rank-two Hall calculations."""
    first, second = sp.symbols("first second")
    line_generator = (first, -second)
    source = (first, second)
    assert j_pair(source, line_generator) == 0
    line_square = sp.factor(j_pair(line_generator, line_generator))
    assert line_square == -2 * first * second

    # Normalize two independent columns of the second rank-two array to
    # b_0=(1,0), b_1=(0,1), leaving b_2=(u,v).  Cross-label orthogonality
    # forces a_2=0 and then b_2=0 once the first array has rank two.
    x0, y0, x1, y1, x2, y2, u, v = sp.symbols(
        "x0 y0 x1 y1 x2 y2 u v"
    )
    a_columns = ((x0, y0), (x1, y1), (x2, y2))
    b_columns = ((1, 0), (0, 1), (u, v))
    cross_equations = {
        (i, j): sp.expand(j_pair(a_columns[i], b_columns[j]))
        for i in range(3)
        for j in range(3)
        if i != j
    }
    assert cross_equations[(1, 0)] == y1
    assert cross_equations[(2, 0)] == y2
    assert cross_equations[(0, 1)] == x0
    assert cross_equations[(2, 1)] == x2

    normalized = {
        expression: sp.expand(value.subs({y1: 0, y2: 0, x0: 0, x2: 0}))
        for expression, value in cross_equations.items()
    }
    assert normalized[(0, 2)] == y0 * u
    assert normalized[(1, 2)] == x1 * v
    # Rank two of (a_0,a_1,0) means x1*y0 is nonzero, so the last two
    # equations force u=v=0.
    first_rank_minor = sp.factor(
        sp.Matrix([[0, x1], [y0, 0]]).det()
    )
    assert first_rank_minor == -x1 * y0
    return {
        "J_determinant": sp.Matrix([[0, 1], [1, 0]]).det(),
        "orthogonal_line_square": line_square,
        "normalized_cross_equations": normalized,
        "rank_two_minor": first_rank_minor,
    }


def assert_fixture_inclusion() -> dict[str, object]:
    """Check that the previous sharp fixture is a point of the W/V component."""
    h = (0, 1, -2, -1, 0, 0)
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    b_vectors = [
        (0, 2, 2, 0, 0, 0),
        (0, 2, 0, -2, 0, 0),
        (1, 1, 0, 0, 0, 0),
    ]
    h_plane = [x4, x5, h]
    assert sp.Matrix(h_plane).T.rank() == 3
    assert sp.Matrix(b_vectors).T.rank() == 3

    def ell1(vector: tuple[int, ...]) -> int:
        return vector[3] - vector[2] - vector[0]

    def ell2(vector: tuple[int, ...]) -> int:
        return vector[3] - vector[2] - vector[1]

    assert all(vector[0] == 0 and ell2(vector) == 0 for vector in h_plane)
    assert all(
        vector[4] == vector[5] == 0 and ell1(vector) == -vector[1]
        for vector in b_vectors
    )
    return {"sharp_H_rank": 3, "sharp_V_rank": 3}


def main() -> None:
    coordinates = assert_coordinate_spaces()
    sensors = assert_sensor_factorization()
    shell = assert_shell_reduction()
    rank_map = assert_offdiagonal_rank_map()
    rank_cases = assert_rank_case_algebra()
    fixture = assert_fixture_inclusion()

    print("fixed-pair Hamming-radius-two compression primary checks: PASS")
    print(f"  compression coordinates: {coordinates}")
    print(f"  diagonal sensor identities: {sensors['diagonal_actual']}")
    print(f"  automatic mixed radicals: {sensors['mixed_radicals']}")
    print(f"  shell reduction: {shell}")
    print(f"  off-diagonal R-block determinant: {rank_map['R_block_determinant']}")
    print(f"  projection-rank algebra: {rank_cases}")
    print(f"  prior sharp fixture inclusion: {fixture}")


if __name__ == "__main__":
    main()
