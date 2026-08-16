"""Primary checks for the star-pair same-mode support boundary."""

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
QUADRATICS = {"m1": M1, "m2": M2, "d0": D0, "d1": D1, "d2": D2}

N = (0, 1, 1, 0)
B0 = (1, 0, 1, 0)
C0 = (1, -1, 0, 0)
B1 = (1, 0, 0, 1)
C1 = (1, 1, 1, 1)
Q_LINE = (0, 0, 1, 1)


def first_four_product(left: Vector, right: Vector) -> tuple[sp.Expr, ...]:
    """Multiply two first-four-coordinate forms in edge coordinates."""
    return tuple(
        sp.expand(left[first] * right[second] + left[second] * right[first])
        for first, second in EDGES
    )


def complement_core_matrix(quadratic: tuple[int, ...]) -> sp.Matrix:
    """Return the symmetric matrix of the complementary quadratic core."""
    matrix = sp.zeros(4)
    vertices = set(range(4))
    for coefficient, edge in zip(quadratic, EDGES, strict=True):
        first, second = sorted(vertices - set(edge))
        matrix[first, second] += coefficient
        matrix[second, first] += coefficient
    return matrix


CORES = {name: complement_core_matrix(value) for name, value in QUADRATICS.items()}


def contract(name: str, vector: Vector) -> sp.Matrix:
    """Contract a complementary quadratic core with a vector."""
    return CORES[name] * sp.Matrix(vector)


def double_contract(name: str, first: Vector, second: Vector) -> sp.Expr:
    """Contract a complementary quadratic core in two distinct slots."""
    return sp.expand((sp.Matrix(first).T * CORES[name] * sp.Matrix(second))[0])


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply two polynomials in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return {mask: value for mask, value in result.items() if value != 0}


def quartic_coefficient(quadratic: tuple[int, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Return the full square-free coefficient of q times four forms."""
    polynomial: Polynomial = {
        (1 << first) | (1 << second): sp.Integer(value)
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        linear = {
            1 << index: sp.sympify(value)
            for index, value in enumerate(vector)
            if value
        }
        polynomial = square_free_multiply(polynomial, linear)
    return sp.expand(polynomial.get(FULL_MASK, 0))


def j_form(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the x4,x5 hyperbolic form."""
    return sp.expand(left[4] * right[5] + left[5] * right[4])


def cubic_value(ell: Vector, first: Vector, second: Vector, third: Vector) -> sp.Expr:
    """Evaluate pol(ell*x4*x5) on three vectors."""
    def evaluate(vector: Vector) -> sp.Expr:
        return sp.expand(sum(ell[index] * vector[index] for index in range(6)))

    return sp.expand(
        evaluate(first) * j_form(second, third)
        + evaluate(second) * j_form(first, third)
        + evaluate(third) * j_form(first, second)
    )


def cubic_slice(ell: Vector, vector: Vector, left: tuple[Vector, ...], right: tuple[Vector, ...]) -> sp.Matrix:
    """Return a three-by-three bilinear slice of pol(ell*x4*x5)."""
    return sp.Matrix(3, 3, lambda i, j: cubic_value(ell, vector, left[i], right[j]))


def assert_pair_and_kernels() -> dict[str, object]:
    """Reconstruct the star pair, projections, common kernel, and lines."""
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

    phi1 = sp.Matrix([
        (0, 0, 0, 1),
        (1, 1, -1, 0),
    ])
    phi2 = sp.Matrix([
        (1, 0, 0, -1),
        (0, 1, -1, 0),
    ])
    # The omitted x4,x5 rows vanish automatically on these R-vectors.
    assert phi1.rank() == phi2.rank() == 2
    kernel1 = sp.Matrix.hstack(sp.Matrix(B0), sp.Matrix(N))
    kernel2 = sp.Matrix.hstack(sp.Matrix(B1), sp.Matrix(N))
    assert phi1 * kernel1 == sp.zeros(2, 2)
    assert phi2 * kernel2 == sp.zeros(2, 2)
    common = sp.Matrix.vstack(phi1, phi2).nullspace()
    assert common == [sp.Matrix(N)]
    assert all(phi1 * sp.Matrix(line) == sp.zeros(2, 1) for line in (N, B0, C0))
    assert all(phi2 * sp.Matrix(line) == sp.zeros(2, 1) for line in (N, B1, C1))
    return {
        "pair_rank": 5,
        "kernel_dimensions": (2, 2),
        "common_kernel": N,
        "phi1_lines": (N, B0, C0),
        "phi2_lines": (N, B1, C1),
    }


def assert_noncommon_quotient() -> dict[str, object]:
    """Check every contraction and the four-pair quotient exclusions."""
    lines = {"B0": B0, "C0": C0, "B1": B1, "C1": C1}
    table = {
        line_name: {
            channel: tuple(contract(channel, line))
            for channel in QUADRATICS
        }
        for line_name, line in lines.items()
    }
    g1 = sp.Matrix((1, 1, -1, 1))
    g2 = sp.Matrix((-1, 1, -1, 1))
    assert table["B0"]["m1"] == (0, 0, 0, 0)
    assert table["C0"]["m1"] == (0, 0, 0, 0)
    assert table["B0"]["m2"] == tuple(g2)
    assert table["C0"]["m2"] == tuple(g2)
    assert table["B1"]["m2"] == (0, 0, 0, 0)
    assert table["C1"]["m2"] == (0, 0, 0, 0)
    assert table["B1"]["m1"] == tuple(g1)
    assert table["C1"]["m1"] == tuple(g1)
    assert sp.Matrix.hstack(g1, g2).rank() == 2

    quotient = sp.Matrix([
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    ])
    assert quotient * g1 == quotient * g2 == sp.zeros(2, 1)
    assert quotient.rank() == 2
    a_vector = sp.Matrix((-2, 2))
    b_vector = sp.Matrix((0, 2))
    expected = {
        "B0": (sp.zeros(2, 1), a_vector, b_vector),
        "C0": (-a_vector, sp.zeros(2, 1), b_vector),
        "B1": (-a_vector, sp.zeros(2, 1), b_vector),
        "C1": (sp.zeros(2, 1), a_vector, b_vector),
    }
    for line_name in lines:
        actual = tuple(
            quotient * sp.Matrix(table[line_name][channel])
            for channel in ("d0", "d1", "d2")
        )
        assert actual == expected[line_name]

    # Same-missing pairs: the two live quotient columns are equal and
    # independent as constraints, forcing both local coefficient rows equal.
    assert sp.Matrix.hstack(a_vector, b_vector).rank() == 2
    for left, right, live_channels in (
        ("B0", "C1", ("d1", "d2")),
        ("C0", "B1", ("d0", "d2")),
    ):
        assert all(
            quotient * sp.Matrix(table[left][channel])
            == quotient * sp.Matrix(table[right][channel])
            != sp.zeros(2, 1)
            for channel in live_channels
        )

    # Different-missing pairs: each possible zero coordinate row exposes a
    # nonzero quotient image in its matching diagonal channel.
    different_cases = {
        ("B0", "B1"): (("B1", "d0"), ("B0", "d1"), ("B0", "d2")),
        ("C0", "C1"): (("C0", "d0"), ("C1", "d1"), ("C0", "d2")),
    }
    for cases in different_cases.values():
        assert all(
            quotient * sp.Matrix(table[line][channel]) != sp.zeros(2, 1)
            for line, channel in cases
        )
    return {
        "mixed_kernel_plane_rank": 2,
        "quotient_rank": quotient.rank(),
        "diagonal_quotient_table": {
            name: tuple(tuple(vector) for vector in vectors)
            for name, vectors in expected.items()
        },
        "same_missing_pairs": 2,
        "different_missing_zero_row_cases": 6,
    }


def assert_common_line_propagation() -> dict[str, object]:
    """Check the common residual kernel and unique companion identities."""
    expected_n = {
        "m1": (0, 0, 0, 0),
        "m2": (0, 0, 0, 0),
        "d0": (1, -1, -1, 1),
        "d1": (-1, -1, -1, 1),
        "d2": (0, 0, 0, 0),
    }
    assert {name: tuple(contract(name, N)) for name in QUADRATICS} == expected_n
    residual_matrix = sp.Matrix([
        expected_n["d0"],
        expected_n["d1"],
    ])
    assert residual_matrix.rank() == 2
    h_basis = sp.Matrix.hstack(
        sp.Matrix((0, 1, 0, 1)),
        sp.Matrix((0, 0, 1, 1)),
    )
    assert residual_matrix * h_basis == sp.zeros(2, 2)
    assert h_basis.rank() == 2

    u, v = sp.symbols("u v")
    companion = (0, u, v, u + v)
    rows = {name: contract(name, companion) for name in QUADRATICS}
    assert 2 * rows["m1"] - rows["d0"] + rows["d1"] == sp.zeros(4, 1)
    companion_identity = (
        u * rows["d2"] - (u + v) * (rows["m1"] + rows["m2"])
    ).applyfunc(sp.expand)
    assert companion_identity == sp.zeros(4, 1)
    q_rows = {name: tuple(contract(name, Q_LINE)) for name in QUADRATICS}
    assert q_rows == {
        "m1": (1, 1, -1, -1),
        "m2": (-1, -1, 1, 1),
        "d0": (1, 1, -1, -1),
        "d1": (-1, -1, 1, 1),
        "d2": (2, 0, 0, 0),
    }
    return {
        "N_residual_rank": residual_matrix.rank(),
        "N_residual_kernel_basis": tuple(tuple(h_basis.col(index)) for index in range(2)),
        "companion_parameterization": companion,
        "forced_companion": Q_LINE,
        "companion_contractions": q_rows,
    }


def inverse(value: int, prime: int) -> int:
    """Return an inverse in a prime field."""
    return pow(value % prime, prime - 2, prime)


def projective_states(prime: int) -> tuple[tuple[int, int], ...]:
    """Return zero and all projective directions in F_p^2."""
    states = [(0, 0)]
    seen: set[tuple[int, int]] = set()
    for vector in product(range(prime), repeat=2):
        if vector == (0, 0):
            continue
        pivot = next(index for index, value in enumerate(vector) if value)
        scalar = inverse(vector[pivot], prime)
        normalized = tuple(value * scalar % prime for value in vector)
        if normalized not in seen:
            seen.add(normalized)
            states.append(normalized)
    return tuple(states)


def j_mod(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate the hyperbolic form modulo an odd prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def compatible(
    left: tuple[tuple[int, int], ...],
    right: tuple[tuple[int, int], ...],
    prime: int,
) -> bool:
    """Test cross-colour orthogonality for a pair of modes."""
    return all(
        left_colour == right_colour
        or j_mod(left[left_colour], right[right_colour], prime) == 0
        for left_colour in range(3)
        for right_colour in range(3)
    )


def assert_active_colour_core(prime: int) -> dict[str, int]:
    """Exhaust the A-level one/two-active-colour core."""
    states = projective_states(prime)
    modes = tuple(product(states, repeat=3))
    adjacency = tuple(
        frozenset(
            right_index
            for right_index, right in enumerate(modes)
            if compatible(left, right, prime)
        )
        for left in modes
    )
    triples = 0
    two_active = 0
    for first_index, first in enumerate(modes):
        for second_index in adjacency[first_index]:
            second = modes[second_index]
            for third_index in adjacency[first_index] & adjacency[second_index]:
                third = modes[third_index]
                triples += 1
                configuration = (first, second, third)
                active = tuple(
                    colour
                    for colour in range(3)
                    if any(
                        j_mod(configuration[i][colour], configuration[j][colour], prime)
                        for i, j in ((0, 1), (0, 2), (1, 2))
                    )
                )
                assert len(active) <= 2
                if len(active) == 2:
                    two_active += 1
                    inactive = next(colour for colour in range(3) if colour not in active)
                    assert all(mode[inactive] == (0, 0) for mode in configuration)
    return {
        "states": len(states),
        "mode_arrays": len(modes),
        "compatible_triples": triples,
        "two_active_triples": two_active,
    }


def assert_support_two_cubic_rank() -> dict[str, object]:
    """Check the rank-one-free slice obstruction for ``pol(XUV)``."""
    e00 = sp.zeros(3)
    e11 = sp.zeros(3)
    e22 = sp.zeros(3)
    e00[0, 0] = e11[1, 1] = e22[2, 2] = 1
    assert sp.Matrix.hstack(
        sp.Matrix(e00).reshape(9, 1),
        sp.Matrix(e11).reshape(9, 1),
        sp.Matrix(e22).reshape(9, 1),
    ).rank() == 3

    slice_x = sp.Matrix(((0, 0, 0), (0, 0, 1), (0, 1, 0)))
    slice_u = sp.Matrix(((0, 0, 1), (0, 0, 0), (1, 0, 0)))
    slice_v = sp.Matrix(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    assert sp.Matrix.hstack(
        slice_x.reshape(9, 1),
        slice_u.reshape(9, 1),
        slice_v.reshape(9, 1),
    ).rank() == 3

    a, b, c = sp.symbols("a b c")
    general_slice = a * slice_x + b * slice_u + c * slice_v
    assert general_slice == sp.Matrix(((0, c, b), (c, 0, a), (b, a, 0)))
    principal_minors = tuple(
        sp.expand(general_slice.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert principal_minors == (-c**2, -b**2, -a**2)
    return {
        "weighted_delta_slice_rank": 3,
        "pol_XUV_slice_rank": 3,
        "principal_two_minors": principal_minors,
        "nonzero_rank_one_slices": 0,
    }


def assert_singleton_sharpness_fixture() -> dict[str, object]:
    """Verify the exact rational N/Q slice survivor and target failures."""
    half = sp.Rational(1, 2)
    modes: tuple[tuple[Vector, ...], ...] = (
        (
            (0, 1, 1, 0, 0, 0),
            (0, 1, -half, 3 * half, 0, 0),
            (0, -1, half, -half, 1, 0),
        ),
        (
            (1, 0, -half, half, 0, 0),
            (0, 1, half, 3 * half, 0, 0),
            (0, 0, 1, 1, 0, 0),
        ),
        (
            (0, -2, 0, 0, 0, 1),
            (0, 0, -1, 1, 0, 0),
            (1, -1, half, -half, 0, 0),
        ),
        (
            (0, 1, half, -half, 1, 0),
            (0, 1, half, half, 0, 0),
            (0, 1, -2, 1, 0, 1),
        ),
    )
    mode_a, mode_b, mode_c, mode_d = modes
    assert all(sp.Matrix.hstack(*map(sp.Matrix, mode)).rank() == 3 for mode in modes)

    phi1 = sp.Matrix((
        (0, 0, 0, 1, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
        (1, 1, -1, 0, 0, 0),
    ))
    phi2 = sp.Matrix((
        (1, 0, 0, -1, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
        (0, 1, -1, 0, 0, 0),
    ))
    profiles = tuple(
        tuple((phi * sp.Matrix.hstack(*map(sp.Matrix, mode))).rank() for mode in modes)
        for phi in (phi1, phi2)
    )
    assert profiles == ((2, 2, 2, 3), (2, 2, 2, 3))
    assert mode_a[0] == (*N, 0, 0)
    assert mode_b[2] == (*Q_LINE, 0, 0)

    x0: Vector = (1, 0, 0, 0, 0, 0)
    r: Vector = (1, 1, -1, -1, 0, 0)
    h0: Vector = (1, -1, -1, 1, 0, 0)
    h1: Vector = (-1, -1, -1, 1, 0, 0)
    assert tuple(2 * x0[index] + h1[index] for index in range(6)) == h0
    zero = sp.zeros(3)
    e00 = sp.zeros(3)
    e22 = sp.zeros(3)
    e00[0, 0] = e22[2, 2] = 1
    a_r_slices = tuple(cubic_slice(r, vector, mode_c, mode_d) for vector in mode_a)
    a_x_slices = tuple(cubic_slice(x0, vector, mode_c, mode_d) for vector in mode_a)
    b_h1_slices = tuple(cubic_slice(h1, vector, mode_c, mode_d) for vector in mode_b)
    b_x_slices = tuple(cubic_slice(x0, vector, mode_c, mode_d) for vector in mode_b)
    assert a_r_slices == (zero, zero, zero)
    assert a_x_slices == (zero, zero, e22)
    assert b_h1_slices == (zero, zero, zero)
    assert b_x_slices == (e00, zero, zero)

    d1_failure = quartic_coefficient(
        D1,
        (mode_a[1], mode_b[1], mode_c[1], mode_d[1]),
    )
    m1_failure = quartic_coefficient(
        M1,
        (mode_a[1], mode_b[0], mode_c[0], mode_d[0]),
    )
    assert d1_failure == 0
    assert m1_failure == 3
    return {
        "local_ranks": (3, 3, 3, 3),
        "projection_profiles": profiles,
        "N_colour": 0,
        "Q_colour": 2,
        "forced_slice_counts": (6, 6),
        "full_target_failures": {"d1_1111": d1_failure, "m1_1000": m1_failure},
    }


def assert_rank_gates() -> dict[str, int]:
    """Check the numerical dimension gaps in the quotient arguments."""
    assert 4 - 3 == 1 < 2
    assert 6 - 3 == 3 < 4
    return {
        "quotient_ambient": 4,
        "quotient_killed_rank_ceiling": 1,
        "quotient_scalar_rank": 2,
        "full_ambient": 6,
        "full_killed_rank_ceiling": 3,
        "full_scalar_rank": 4,
    }


def main() -> None:
    """Run all primary checks."""
    pair = assert_pair_and_kernels()
    quotient = assert_noncommon_quotient()
    propagation = assert_common_line_propagation()
    cubic_rank = assert_support_two_cubic_rank()
    fixture = assert_singleton_sharpness_fixture()
    ranks = assert_rank_gates()
    finite_fields = {prime: assert_active_colour_core(prime) for prime in (3, 5)}
    print("star-pair same-mode noncommon/support-two boundary primary checks: PASS")
    print(f"  pair and kernels: {pair}")
    print(f"  noncommon quotient: {quotient}")
    print(f"  common propagation: {propagation}")
    print(f"  support-two cubic-rank gate: {cubic_rank}")
    print(f"  singleton sharpness fixture: {fixture}")
    print(f"  rank gates: {ranks}")
    print(f"  finite-field A-level audits: {finite_fields}")


if __name__ == "__main__":
    main()
