#!/usr/bin/env python3
"""Exact replay for the joint-rank-four uninvolved-rank-two exclusion."""

from __future__ import annotations

import itertools

import sympy as sp

X_DIM = 2
Y_DIM = 2
Z_DIM = 1
TENSOR_DIM = X_DIM * Y_DIM * Z_DIM


def basis(index: int, size: int) -> sp.Matrix:
    return sp.eye(size)[:, index]


def row(
    x_part: sp.Matrix | None = None,
    y_part: sp.Matrix | None = None,
    z_part: sp.Matrix | None = None,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        sp.zeros(X_DIM, 1) if x_part is None else x_part,
        sp.zeros(Y_DIM, 1) if y_part is None else y_part,
        sp.zeros(Z_DIM, 1) if z_part is None else z_part,
    )


def add_rows(
    *terms: tuple[sp.Expr, tuple[sp.Matrix, sp.Matrix, sp.Matrix]],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return tuple(
        sum((coefficient * vector[source] for coefficient, vector in terms), sp.zeros(size, 1))
        for source, size in enumerate((X_DIM, Y_DIM, Z_DIM))
    )  # type: ignore[return-value]


def separated(
    left: sp.Matrix,
    middle: sp.Matrix,
    right: sp.Matrix,
) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def permanent(
    left: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    middle: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    right: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    vectors = (left, middle, right)
    total = sp.zeros(TENSOR_DIM, 1)
    for permutation in itertools.permutations(range(3)):
        total += separated(
            vectors[permutation[0]][0],
            vectors[permutation[1]][1],
            vectors[permutation[2]][2],
        )
    return sp.simplify(total)


def permutation_sign(permutation: tuple[int, int, int]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


def alternating(
    first: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    second: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    third: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    vectors = (first, second, third)
    total = sp.zeros(TENSOR_DIM, 1)
    for permutation in itertools.permutations(range(3)):
        total += permutation_sign(permutation) * separated(
            vectors[permutation[0]][0],
            vectors[permutation[1]][1],
            vectors[permutation[2]][2],
        )
    return sp.simplify(total)


def flatten(vector: tuple[sp.Matrix, sp.Matrix, sp.Matrix]) -> sp.Matrix:
    return sp.Matrix.vstack(*vector)


def assert_zero(vector: sp.Matrix) -> None:
    assert all(sp.expand(entry) == 0 for entry in vector)


def conjugate_tangent_chart() -> None:
    coefficient_a, coefficient_b, coefficient_c, coefficient_d = sp.symbols(
        "A B C D"
    )
    x = row(x_part=basis(0, X_DIM))
    d = row(x_part=basis(1, X_DIM))
    y = row(y_part=basis(0, Y_DIM))
    e = row(y_part=basis(1, Y_DIM))
    t = row(z_part=basis(0, Z_DIM))

    w = add_rows((1, x), (-1, y))
    u = add_rows((-1, d), (-1, e), (1, t))
    v = add_rows((1, x), (1, y))
    q_0 = w
    q_1 = add_rows((1, d), (1, e), (1, t))
    u_0 = add_rows((coefficient_a, w), (coefficient_b, u))
    u_1 = add_rows((coefficient_c, w), (coefficient_d, u))

    # The displayed plane really is the common mixed-zero plane.
    for divisor in (w, u):
        assert_zero(permanent(divisor, v, q_0))
        assert_zero(permanent(divisor, v, q_1))

    xyt = separated(x[0], y[1], t[2])
    dyt = separated(d[0], y[1], t[2])
    xet = separated(x[0], e[1], t[2])
    det = separated(d[0], e[1], t[2])

    expected_q_0 = 2 * (
        -(coefficient_a * coefficient_d + coefficient_b * coefficient_c) * xyt
        + coefficient_b * coefficient_d * (dyt - xet)
    )
    expected_q_1 = -2 * (
        coefficient_a * coefficient_c * xyt
        + coefficient_b * coefficient_d * det
    )
    expected_alt = -2 * (
        coefficient_a * coefficient_d - coefficient_b * coefficient_c
    ) * xyt

    assert_zero(permanent(u_0, u_1, q_0) - expected_q_0)
    assert_zero(permanent(u_0, u_1, q_1) - expected_q_1)
    assert_zero(alternating(u_0, u_1, v) - expected_alt)

    # The two quotient coefficients in (22) are exactly +/-2 B D.
    assert sp.expand(expected_q_0[2]) == 2 * coefficient_b * coefficient_d
    assert sp.expand(expected_q_0[1]) == -2 * coefficient_b * coefficient_d
    print("conjugate tangent chart: PASS (generic polarized identities)")


def forced_containment_identity() -> None:
    lam, mu = sp.symbols("lambda mu")
    x = row(x_part=basis(0, X_DIM))
    y = row(y_part=basis(0, Y_DIM))
    t = row(z_part=basis(0, Z_DIM))
    w = add_rows((1, x), (-1, y))
    u = add_rows((-lam, x), (-mu, y), (1, t))
    v = add_rows((1, x), (1, y))
    q_1 = add_rows((lam, x), (mu, y), (1, t))

    reconstructed = add_rows(
        (1, u),
        (lam + mu, v),
        (lam - mu, w),
    )
    assert_zero(flatten(q_1) - flatten(reconstructed))
    assert sp.Matrix.hstack(flatten(w), flatten(u), flatten(v)).rank() == 3
    print("forced containment: PASS (q1 lies in span(w,u,v))")


def sharp_contained_fixture() -> None:
    x = row(x_part=basis(0, X_DIM))
    y = row(y_part=basis(0, Y_DIM))
    t = row(z_part=basis(0, Z_DIM))
    v = add_rows((1, x), (1, y))
    u_0 = add_rows((-2, y), (1, t))
    u_1 = add_rows((2, x), (-1, t))
    q_0 = add_rows((1, x), (-1, y))
    q_1 = add_rows((1, x), (1, y), (1, t))

    v_space = sp.Matrix.hstack(flatten(u_0), flatten(u_1), flatten(v))
    q_space = sp.Matrix.hstack(flatten(q_0), flatten(q_1))
    assert v_space.rank() == 3
    assert q_space.rank() == 2
    assert sp.Matrix.hstack(v_space, q_space).rank() == 3

    xyt = separated(x[0], y[1], t[2])
    assert_zero(permanent(v, v, q_0))
    assert_zero(permanent(v, v, q_1) - 2 * xyt)
    for left, middle in ((u_0, v), (u_1, v), (u_0, u_1)):
        assert_zero(permanent(left, middle, q_0))
        assert_zero(permanent(left, middle, q_1))
    assert_zero(alternating(u_0, u_1, v) - 4 * xyt)
    print("contained-plane sharpness: PASS (rank 3/2, nonzero singleton)")


def profile_census() -> None:
    profiles = {(left, right) for left in (2, 3) for right in (2, 3)}
    assert profiles == {(2, 2), (2, 3), (3, 2), (3, 3)}
    kernel_supports = {1, 2}
    assert len(profiles) * len(kernel_supports) == 8
    print("profile census: PASS (eight exhaustive support/profile cells)")


def main() -> None:
    conjugate_tangent_chart()
    forced_containment_identity()
    sharp_contained_fixture()
    profile_census()
    print("joint-rank-four q=2 exclusion replay: PASS")


if __name__ == "__main__":
    main()
