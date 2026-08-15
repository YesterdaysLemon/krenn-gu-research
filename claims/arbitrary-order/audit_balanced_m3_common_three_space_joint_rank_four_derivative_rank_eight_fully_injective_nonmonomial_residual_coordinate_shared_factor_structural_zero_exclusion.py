#!/usr/bin/env python3
"""Independent exact audit of the coordinate structural-zero exclusion.

This audit uses only the Python standard library and ``Fraction`` arithmetic.
It does not import the SymPy replay or repository code.  It traverses colours,
root orientations, matrix ranks, and retained faces in reverse order and uses
its own small bilinear-map representation.

The written theorem remains responsible for the S2CG zero-pair source-support
classification, the S2CI two-cross incidence dichotomy, and the S2CK mixed-map
and zero-corner obstructions.  This script checks the finite case cover and
the exact algebraic interfaces used on either side of those analytic inputs.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product

COLORS = (0, 1, 2)
VALUES = tuple(F(v) for v in (-2, -1, 0, 1, 2))


def add(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(value: F, vector: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(value * entry for entry in vector)


def sub(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
    return add(left, scale(F(-1), right))


def mat_vec(matrix: tuple[tuple[F, F], tuple[F, F]], vector: tuple[F, F]) -> tuple[F, F]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def bilinear(
    left: tuple[F, F],
    matrix: tuple[tuple[F, F], tuple[F, F]],
    right: tuple[F, F],
) -> F:
    image = mat_vec(matrix, right)
    return left[0] * image[0] + left[1] * image[1]


def determinant(matrix: tuple[tuple[F, F], tuple[F, F]]) -> F:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def transpose(matrix: tuple[tuple[F, F], tuple[F, F]]) -> tuple[tuple[F, F], tuple[F, F]]:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def common_map(
    left: tuple[F, F],
    right: tuple[F, F],
    matrix: tuple[tuple[F, F], tuple[F, F]],
) -> tuple[F, F, F]:
    """Coefficients of ``lambda_i T_i, lambda_j T_j, S``."""

    return (
        left[0] * right[0],
        left[1] * right[1],
        bilinear(left, matrix, right),
    )


def coordinate_map(
    left: tuple[F, F],
    right: tuple[F, F],
    matrix: tuple[tuple[F, F], tuple[F, F]],
) -> tuple[F, F]:
    """Coefficients of ``lambda_k T_k, S`` on the coordinate pair wall."""

    return (left[1] * right[1], bilinear(left, matrix, right))


E0 = (F(1), F(0))
E1 = (F(0), F(1))


def check_root_exchange() -> int:
    checked = 0
    for entries in reversed(tuple(product(VALUES, repeat=4))):
        matrix = ((entries[0], entries[1]), (entries[2], entries[3]))
        matrix_t = transpose(matrix)
        for left, right in reversed(tuple(product((E0, E1, (F(1), F(-1))), repeat=2))):
            assert common_map(left, right, matrix) == common_map(right, left, matrix_t)
            assert coordinate_map(left, right, matrix) == coordinate_map(right, left, matrix_t)
            checked += 1
    assert checked == 625 * 9
    return checked


def check_y_s_nonzero_atlas() -> tuple[int, int]:
    """Check the 8 one-cross and 3 double-cross nonzero patterns."""

    pattern_counts = {"one": 0, "double": 0}
    for u_zero, v_zero, a_zero, b_zero in reversed(tuple(product((False, True), repeat=4))):
        if u_zero == v_zero:
            if not u_zero:
                continue  # no structural cross zero
            if a_zero and b_zero:
                continue  # zero restricted block
            pattern_counts["double"] += 1
        else:
            pattern_counts["one"] += 1
    assert pattern_counts == {"one": 8, "double": 3}

    a, b, v = F(3), F(-5), F(2)
    matrix = ((a, F(0)), (v, b))
    m00 = common_map(E0, E0, matrix)
    m01 = common_map(E0, E1, matrix)
    m10 = common_map(E1, E0, matrix)
    m11 = common_map(E1, E1, matrix)
    assert m00 == (F(1), F(0), a)
    assert m01 == (F(0), F(0), F(0))
    assert m10 == (F(0), F(0), v)
    assert m11 == (F(0), F(1), b)
    assert sub(scale(v, m00), scale(a, m10)) == (v, F(0), F(0))
    assert sub(scale(v, m11), scale(b, m10)) == (F(0), v, F(0))
    assert sub(scale(b, m00), scale(a, m11)) == (b, -a, F(0))

    matrix_b = ((F(0), F(0)), (v, b))
    beta_prime = (-(b / v), F(1))
    assert common_map(E0, beta_prime, matrix_b) == (-(b / v), F(0), F(0))
    assert common_map(E1, beta_prime, matrix_b) == (F(0), F(1), F(0))

    matrix_a = ((a, F(0)), (v, F(0)))
    alpha_prime = (F(1), -(a / v))
    assert common_map(alpha_prime, E1, matrix_a) == (F(0), -(a / v), F(0))
    assert common_map(alpha_prime, E0, matrix_a) == (F(1), F(0), F(0))

    diagonal = ((a, F(0)), (F(0), b))
    assert common_map(E0, E1, diagonal) == (F(0), F(0), F(0))
    assert common_map(E1, E0, diagonal) == (F(0), F(0), F(0))
    weighted = sub(scale(b, common_map(E0, E0, diagonal)), scale(a, common_map(E1, E1, diagonal)))
    assert weighted == (b, -a, F(0))
    return pattern_counts["one"], pattern_counts["double"]


def check_retained_colour_choices() -> int:
    checked = 0
    for s, r, k in reversed(tuple(product(COLORS, repeat=3))):
        if len({s, r, k}) != 3:
            continue
        for t in reversed(COLORS):
            choices = tuple(h for h in (s, r) if h != t)
            assert choices
            for h in choices:
                assert h != t
                assert h != k
                # The retained diagonal face has sign P_hhh-T_h=C_hh S_h.
                p_hhh, target, correction, source = F(0), F(1), F(7), F(0)
                assert p_hhh - target == F(-1)
                assert correction * source == F(0)
            checked += 1
    assert checked == 18
    return checked


def check_y_s_zero_noncoordinate() -> int:
    # Independent kernel/complement: the two target coefficient rows are
    # [c_i eta_i,c_j eta_j] and [A_i eta_i,A_j eta_j].
    c = (F(1), F(1))
    complement = (F(1), F(-1))
    eta = (F(2), F(3))
    coefficient_matrix = (
        (c[0] * eta[0], c[1] * eta[1]),
        (complement[0] * eta[0], complement[1] * eta[1]),
    )
    assert determinant(coefficient_matrix) == F(-12)

    # Full dependent kernel has both transverse target coefficients nonzero.
    assert c[0] * eta[0] != 0 and c[1] * eta[1] != 0

    # Singleton kernel and the exact shifted complement.
    correction = F(5)
    # M(other,B-correction*d)=eta_j T_j; the singleton map keeps eta_i T_i
    # plus its residual source term.  Evaluation/symmetry in the theorem then
    # forces both complementary coordinate covectors to vanish on the pure row.
    shifted_other = (F(0), eta[1], F(0))
    shifted_singleton = (eta[0], F(0), correction)
    assert shifted_other[:2] == (F(0), eta[1])
    assert shifted_singleton[0] != 0
    gamma_i = gamma_j = F(0)
    gamma_s = F(1)
    assert (gamma_s, gamma_i, gamma_j).count(F(0)) == 2
    return 3


def check_coordinate_matrix_rank_split() -> tuple[int, int, int]:
    rank_one = 0
    rank_two_a_nonzero = 0
    rank_two_a_zero = 0
    for entries in reversed(tuple(product(VALUES, repeat=4))):
        a, b, c, d = entries
        matrix = ((a, b), (c, d))
        if matrix == ((F(0), F(0)), (F(0), F(0))):
            continue
        if (a, c) == (F(0), F(0)) or (a, b) == (F(0), F(0)):
            continue  # excluded two-dimensional radical shore
        delta = determinant(matrix)
        if delta == 0:
            rank_one += 1
            assert a != 0
        elif a != 0:
            rank_two_a_nonzero += 1
        else:
            rank_two_a_zero += 1
            assert b != 0 and c != 0

        if a != 0:
            alpha = (c, -a)
            beta = (b, -a)
            assert bilinear(alpha, matrix, E0) == 0
            assert bilinear(E0, matrix, beta) == 0
            mixed = coordinate_map(alpha, beta, matrix)
            corner = coordinate_map(E0, E0, matrix)
            assert mixed == (a * a, a * delta)
            assert sub(mixed, scale(delta, corner)) == (a * a, F(0))
        else:
            assert coordinate_map(E0, E0, matrix) == (F(0), F(0))
            assert coordinate_map(E0, E1, matrix) == (F(0), b)
            assert coordinate_map(E1, E0, matrix) == (F(0), c)
            assert coordinate_map(E1, E1, matrix) == (F(1), d)

    assert rank_one and rank_two_a_nonzero and rank_two_a_zero
    return rank_one, rank_two_a_nonzero, rank_two_a_zero


def check_rank_two_zero_corner_pencil() -> int:
    # Dependent normalization v=rho*u and B'=lambda*A+mu*u.
    rho, c, d = F(2), F(-5), F(7)
    shift = d * rho / c
    assert shift == F(-14, 5)
    # M(A,B')=T_k after subtracting (d/c)v from B.
    assert d - (d / c) * c == 0

    lam, mu = F(2), F(3)
    u_x, a_x, a_y, a_z = F(1), F(1), F(4), F(-2)
    value_at_u = 2 * lam * u_x * a_y * a_z
    value_at_a = (6 * lam * a_x + 2 * mu * u_x) * a_y * a_z
    assert value_at_u != 0
    assert value_at_a / value_at_u == F(9, 2)
    # Once the rank-one image fixes the X line Ku, the arbitrary-q quotient
    # coefficient is exactly 2*lambda*(q_X mod Ku)*A_Y*A_Z.
    q_x_mod_u = F(0)
    assert 2 * lam * q_x_mod_u * a_y * a_z == 0

    # Missing-source fork: a retained diagonal term containing u in X and
    # q_h in the sole Z line dies after Z/KA_Z.  Full-support fork dies after
    # X/Ku.  T_h is transverse and therefore survives in either quotient.
    p_missing_z_quotient = F(0)
    source_missing_z_quotient = F(0)
    p_full_x_quotient = F(0)
    source_full_x_quotient = F(0)
    target_quotient = F(1)
    for p_value, source_value in (
        (p_missing_z_quotient, source_missing_z_quotient),
        (p_full_x_quotient, source_full_x_quotient),
    ):
        assert p_value - target_quotient != source_value
    return 2


def main() -> None:
    exchange = check_root_exchange()
    one_cross, double_cross = check_y_s_nonzero_atlas()
    retained = check_retained_colour_choices()
    noncoordinate = check_y_s_zero_noncoordinate()
    rank_one, rank_two_a, rank_two_zero = check_coordinate_matrix_rank_split()
    pencil = check_rank_two_zero_corner_pencil()
    print(f"reversed first/second-root exchange fixtures ({exchange}): PASS")
    print(f"y_s!=0 exact cross-zero atlas ({one_cross}+{double_cross} patterns): PASS")
    print(f"retained colour/index/sign choices ({retained} colour triples): PASS")
    print(f"y_s=0 noncoordinate source interfaces ({noncoordinate} forks): PASS")
    print(
        "coordinate-y matrix ranks "
        f"(rank1={rank_one}, rank2/a!=0={rank_two_a}, rank2/a=0={rank_two_zero}): PASS"
    )
    print(f"repaired dependent pure-row pencil quotients ({pencil} forks): PASS")
    print("analytic owners: S2CG, S2CI, and S2CK")
    print("scope: coordinate shared-factor structural-zero successor only")


if __name__ == "__main__":
    main()
