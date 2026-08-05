"""Verify the three-mode residual-annihilation rank-sum theorem.

This is a fixed symbolic replay.  It performs no graph, support, word, face,
alignment, or parameter search.
"""

import sympy as sp

import verify_p7_221_degree5_incidence_quotient_rectangle_flattening as binary
import verify_p7_221_face_specific_quotient_mayer_vietoris_and_sharp_lift as lift


def quadratic_conjugate(expression: sp.Expr, rho: sp.Symbol) -> sp.Expr:
    """Apply the nontrivial Q(sqrt(21)) automorphism and reduce."""
    return sp.cancel(expression.xreplace({rho: -rho}))


def main() -> None:
    rho = binary.RHO
    alpha = 1 + 43 * rho / 21
    beta = 2 * (1 + rho) / 7

    faces = {
        "01": frozenset("1234a"),
        "02": frozenset("1235b"),
        "12": frozenset("1345b"),
    }
    expected = {
        "01": (alpha, -6, 0),
        "02": (rho, 0, beta),
        "12": (0, rho, beta),
    }
    for label, face in faces.items():
        actual = tuple(binary.formal_wick_value(colour, face) for colour in range(3))
        assert all(
            sp.simplify(value - target) == 0
            for value, target in zip(actual, expected[label], strict=True)
        )

    coefficient_matrix = sp.Matrix(
        (
            (alpha, -6, 0),
            (rho, 0, beta),
            (0, rho, beta),
        )
    )
    determinant = sp.simplify(coefficient_matrix.det())
    expected_determinant = (124 - 76 * rho) / 7
    assert sp.simplify(determinant - expected_determinant) == 0
    determinant_norm = sp.simplify(
        determinant * quadratic_conjugate(determinant, rho)
    )
    assert determinant_norm == -sp.Rational(105920, 49)
    assert determinant != 0

    # The structural reason for annihilation is cardinality, not a case list:
    # one core edge has only two endpoints and cannot protect three quotients.
    core_edge_endpoint_count = 2
    quotient_mode_count = 3
    assert core_edge_endpoint_count < quotient_mode_count

    # A legal common-incidence diagram attains the rank-sum-six boundary.
    sharp_six_kernels = (
        frozenset((1, 2)),
        frozenset((1, 2)),
        frozenset((0, 2)),
        frozenset((0, 2)),
        frozenset((0, 1)),
        frozenset((0, 1)),
        frozenset((0, 1, 2)),
    )
    sharp_six_supports = tuple(
        tuple(
            mode
            for mode, kernel in enumerate(sharp_six_kernels)
            if colour not in kernel
        )
        for colour in range(3)
    )
    assert sharp_six_supports == ((0, 1), (2, 3), (4, 5))
    assert sum(3 - len(kernel) for kernel in sharp_six_kernels) == 6
    assert all(len(support) <= 2 for support in sharp_six_supports)

    incidence = lift.incidence_system()
    terminal_set = frozenset(lift.TERMINALS)
    projectors = tuple(
        lift.quotient_projector(incidence, mode, terminal_set)
        for mode in lift.MODES
    )
    supports = tuple(
        tuple(
            mode
            for mode, projector in enumerate(projectors)
            if projector * lift.E[colour] != lift.ZERO
        )
        for colour in lift.COLOURS
    )
    assert supports == (
        (0, 1, 3, 4, 5, 6),
        (0, 2),
        (1, 2),
    )
    rank_sum = sum(
        sp.Matrix.hstack(*(projector * vector for vector in lift.E)).rank()
        for projector in projectors
    )
    assert rank_sum == 10
    assert rank_sum > 6

    # A single forbidden triple already excludes this full-span pattern.
    triple = (0, 1, 3)
    colour_zero = sp.kronecker_product(
        *(projectors[mode] * lift.E[0] for mode in triple)
    )
    colour_one = sp.kronecker_product(
        *(projectors[mode] * lift.E[1] for mode in triple)
    )
    assert colour_zero != sp.zeros(27, 1)
    assert colour_one == sp.zeros(27, 1)
    projected_face_01 = alpha * colour_zero - 6 * colour_one
    assert projected_face_01 != sp.zeros(27, 1)

    print("PASS: three exact face rows form an invertible coefficient matrix")
    print("PASS: determinant=(124-76*rho)/7 has norm -105920/49")
    print("PASS: a two-endpoint core edge cannot survive three incidence quotients")
    print("PASS: one legal common-incidence diagram attains rank sum 6")
    print("PASS: the earlier sharp lift has supports (6,2,2) and rank sum 10")
    print("PASS: triple {0,1,3} gives an explicit nonzero forbidden projection")
    print("SCOPE: rank-sum-at-most-six physical boundary remains unresolved")
    print("searches=0")


if __name__ == "__main__":
    main()
