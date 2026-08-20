"""Focused exact checks for the pointwise selector-failure boundary.

The owning theorem supplies the general linear- and commutative-algebra
proofs.  This verifier replays its finite controls over the rationals and
small polynomial rings.  It does not import an audit or another verifier.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def minors(matrix: sp.Matrix, size: int) -> list[sp.Expr]:
    """Return all minors of one small exact matrix."""

    if size == 0:
        return [sp.Integer(1)]
    if size > min(matrix.rows, matrix.cols):
        return [sp.Integer(0)]
    return [
        sp.expand(matrix.extract(rows, columns).det())
        for rows in combinations(range(matrix.rows), size)
        for columns in combinations(range(matrix.cols), size)
    ]


def radical_generator(polynomials: list[sp.Expr], variable: sp.Symbol) -> sp.Poly:
    """Radical generator of a univariate ideal over Q."""

    nonzero = [sp.Poly(value, variable, domain=sp.QQ) for value in polynomials if value]
    if not nonzero:
        return sp.Poly(0, variable, domain=sp.QQ)
    generator = nonzero[0]
    for value in nonzero[1:]:
        generator = sp.gcd(generator, value)
    if generator.is_ground:
        return sp.Poly(1, variable, domain=sp.QQ)
    return generator.monic().sqf_part().monic()


def is_divisible_by(value: sp.Expr, divisor: sp.Poly, variable: sp.Symbol) -> bool:
    """Test membership in a principal univariate ideal."""

    polynomial = sp.Poly(value, variable, domain=sp.QQ)
    if divisor.is_zero:
        return polynomial.is_zero
    return sp.rem(polynomial, divisor).is_zero


def check_strictness_examples() -> None:
    """Replay pointwise failure versus polynomial and generic membership."""

    s = sp.symbols("s")

    nuisance = sp.Matrix([[(s - 1) ** 2]])
    desired = sp.Matrix([s - 1])
    augmented = nuisance.row_join(desired)
    nuisance_radical = radical_generator(minors(nuisance, 1), s)
    augmented_radical = radical_generator(minors(augmented, 1), s)
    expected_radical = sp.Poly(s - 1, s, domain=sp.QQ)
    assert nuisance_radical == augmented_radical == expected_radical
    quotient, remainder = sp.div(
        sp.Poly(s - 1, s, domain=sp.QQ),
        sp.Poly((s - 1) ** 2, s, domain=sp.QQ),
    )
    assert quotient.is_zero and remainder == expected_radical
    for value in (sp.Integer(1), sp.Integer(2), sp.Integer(-3)):
        assert nuisance.subs(s, value).rank() == augmented.subs(s, value).rank()

    nuisance = sp.Matrix([[s - 1]])
    desired = sp.Matrix([1])
    augmented = nuisance.row_join(desired)
    assert sp.simplify((s - 1) * (1 / (s - 1)) - 1) == 0
    assert nuisance.subs(s, 1).rank() == 0
    assert augmented.subs(s, 1).rank() == 1
    assert radical_generator(minors(nuisance, 1), s) == expected_radical
    assert radical_generator(minors(augmented, 1), s) == sp.Poly(1, s, domain=sp.QQ)


def projected_kernel_dimension(
    nuisance: sp.Matrix, desired: sp.Matrix
) -> tuple[int, int]:
    """Compute projected-kernel dimension directly and by rank-nullity."""

    sensor = nuisance.row_join(desired)
    kernel = sensor.nullspace()
    desired_count = desired.cols
    if kernel:
        projected = sp.Matrix.hstack(*(vector[-desired_count:, :] for vector in kernel))
        direct = projected.rank()
    else:
        direct = 0
    formula = desired_count - (sensor.rank() - nuisance.rank())
    return direct, formula


def check_projected_kernel_formula() -> None:
    """Check observable, partially observable, and function-field cases."""

    nuisance = sp.Matrix([[1], [0], [0]])
    desired = sp.Matrix([[0, 0], [1, 0], [0, 1]])
    assert projected_kernel_dimension(nuisance, desired) == (0, 0)

    nuisance = sp.Matrix([[1], [0]])
    desired = sp.Matrix([[0, 0], [1, 1]])
    assert projected_kernel_dimension(nuisance, desired) == (1, 1)

    t = sp.symbols("t")
    nuisance = sp.Matrix([[1]])
    desired = sp.Matrix([[t]])
    sensor = nuisance.row_join(desired)
    assert sensor * sp.Matrix([-t, 1]) == sp.zeros(1, 1)
    assert projected_kernel_dimension(nuisance, desired) == (1, 1)
    constant_a, constant_b = sp.symbols("constant_a constant_b")
    polynomial = sp.Poly(constant_a + t * constant_b, t)
    assert polynomial.coeff_monomial(1) == constant_a
    assert polynomial.coeff_monomial(t) == constant_b


def tensor_index(left: int, right: int, right_dimension: int) -> int:
    return left * right_dimension + right


def decomposable_matrix(
    coefficients: list[sp.Expr], left_dimension: int, right_dimension: int
) -> sp.Matrix:
    """Matrix of lambda tensor id in the product basis."""

    result = sp.zeros(right_dimension, left_dimension * right_dimension)
    for left in range(left_dimension):
        for right in range(right_dimension):
            result[right, tensor_index(left, right, right_dimension)] = coefficients[
                left
            ]
    return result


def recovery_system(
    gamma: sp.Matrix, response: sp.Matrix, right_dimension: int
) -> tuple[sp.Matrix, sp.Matrix]:
    """Linear system for an unrestricted map R with R Gamma=response."""

    coefficients = sp.kronecker_product(sp.eye(right_dimension), gamma.T)
    rhs = sp.Matrix(
        [
            response[row, column]
            for row in range(response.rows)
            for column in range(response.cols)
        ]
    )
    return coefficients, rhs


def decomposable_system(
    gamma: sp.Matrix,
    response: sp.Matrix,
    left_dimension: int,
    right_dimension: int,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Linear system for lambda with (lambda tensor id) Gamma=response."""

    rows = []
    rhs = []
    for right in range(right_dimension):
        for source in range(gamma.cols):
            rows.append(
                [
                    gamma[tensor_index(left, right, right_dimension), source]
                    for left in range(left_dimension)
                ]
            )
            rhs.append(response[right, source])
    return sp.Matrix(rows), sp.Matrix(rhs)


def system_has_solution(coefficients: sp.Matrix, rhs: sp.Matrix) -> bool:
    return coefficients.rank() == coefficients.row_join(rhs).rank()


def nuisance_slices(
    theta: sp.Matrix,
    nuisance_columns: tuple[int, ...],
    left_dimension: int,
    right_dimension: int,
) -> sp.Matrix:
    """Present all coefficient slices of selected nuisance source columns."""

    columns = []
    for source in nuisance_columns:
        for right in range(right_dimension):
            columns.append(
                sp.Matrix(
                    [
                        theta[tensor_index(left, right, right_dimension), source]
                        for left in range(left_dimension)
                    ]
                )
            )
    return sp.Matrix.hstack(*columns)


def check_injective_swallowed_countermodel() -> None:
    """Replay the maximal-rank swallowed-pure model and its obstruction."""

    gamma = sp.zeros(9, 6)
    gamma[tensor_index(0, 0, 3), 0] = 1
    gamma[tensor_index(0, 1, 3), 1] = 1
    gamma[tensor_index(0, 2, 3), 2] = 1
    gamma[tensor_index(1, 1, 3), 3] = 1
    gamma[tensor_index(2, 2, 3), 4] = 1
    gamma[tensor_index(0, 0, 3), 5] = 1
    gamma[tensor_index(1, 2, 3), 5] = 1

    response = sp.zeros(3, 6)
    response[:, 0:3] = sp.eye(3)
    assert gamma.rank() == 6

    g = sp.Matrix([1, 0, 0])
    theta = gamma - sp.kronecker_product(g, sp.eye(3)) * response
    assert theta[:, 0:3] == sp.zeros(9, 3)
    nuisance = nuisance_slices(theta, (3, 4, 5), 3, 3)
    assert nuisance.rank() == 3
    assert nuisance.row_join(g).rank() == nuisance.rank()

    witness = sp.Matrix([1, 0, 0, 1, 1, 0])
    target = gamma * witness
    wanted_target = sp.zeros(9, 1)
    for colour in range(3):
        wanted_target[tensor_index(colour, colour, 3)] = 1
    assert target == wanted_target
    assert response * witness == sp.Matrix([1, 0, 0])

    unrestricted_coefficients, unrestricted_rhs = recovery_system(gamma, response, 3)
    legal_coefficients, legal_rhs = decomposable_system(gamma, response, 3, 3)
    assert system_has_solution(unrestricted_coefficients, unrestricted_rhs)
    assert not system_has_solution(legal_coefficients, legal_rhs)

    explicit_recovery = sp.zeros(3, 9)
    for colour in range(3):
        explicit_recovery[colour, tensor_index(0, colour, 3)] = 1
    explicit_recovery[0, tensor_index(1, 2, 3)] = -1
    assert explicit_recovery * gamma == response


def check_legal_selector_with_supply_failure() -> None:
    """Replay the legal-selector / projected-kernel independence model."""

    gamma = sp.zeros(4, 4)
    gamma[tensor_index(0, 0, 2), 0] = 1
    gamma[tensor_index(0, 1, 2), 1] = 1
    gamma[tensor_index(1, 0, 2), 2] = 1
    gamma[tensor_index(1, 0, 2), 3] = 1
    response = sp.zeros(2, 4)
    response[:, 0:2] = sp.eye(2)

    selector = decomposable_matrix([1, 0], 2, 2)
    assert selector * gamma == response
    legal_coefficients, legal_rhs = decomposable_system(gamma, response, 2, 2)
    assert system_has_solution(legal_coefficients, legal_rhs)

    nuisance = gamma[:, [0, 1, 3]]
    desired = gamma[:, [2]]
    assert projected_kernel_dimension(nuisance, desired) == (1, 1)
    assert gamma * sp.Matrix([0, 0, 1, -1]) == sp.zeros(4, 1)

    g = sp.Matrix([1, 0])
    nuisance_class = sp.Matrix([[0], [1]])
    assert nuisance_class.row_join(g).rank() == 2


def left_quotient_map(nuisance: sp.Matrix) -> sp.Matrix:
    """Rows spanning the annihilator of the nuisance column space."""

    basis = nuisance.T.nullspace()
    if not basis:
        return sp.zeros(0, nuisance.rows)
    return sp.Matrix.hstack(*basis).T


def check_witness_pure_profile_replacement() -> None:
    """Check attachment iff some pure target class survives."""

    e0, e1, e2 = (sp.eye(3)[:, index] for index in range(3))

    # Nonzero rank-one target quotient.
    nuisance = sp.Matrix.hstack(e0 - e1, e2)
    desired = e0
    pure = sp.Matrix.hstack(e0, e1, 2 * e0)
    physical_response = sp.Matrix([[1, 1, 2]])
    quotient = left_quotient_map(nuisance)
    assert quotient * pure == (quotient * desired) * physical_response
    attached = nuisance.row_join(
        desired
    ).rank() > nuisance.rank() and physical_response != sp.zeros(1, 3)
    pure_survives = nuisance.row_join(pure).rank() > nuisance.rank()
    assert attached and pure_survives

    # Response-zero branch: g survives, but every pure class is swallowed.
    pure_zero = sp.Matrix.hstack(e0 - e1, e2, e0 - e1 + e2)
    zero_response = sp.zeros(1, 3)
    assert quotient * pure_zero == (quotient * desired) * zero_response
    attached = nuisance.row_join(
        desired
    ).rank() > nuisance.rank() and zero_response != sp.zeros(1, 3)
    assert not attached
    assert nuisance.row_join(pure_zero).rank() == nuisance.rank()

    # Swallowed-g branch: a nonzero response has zero quotient on both sides.
    full_nuisance = sp.eye(3)
    nonzero_response = sp.Matrix([[2, 3, 5]])
    full_quotient = left_quotient_map(full_nuisance)
    assert full_quotient.rows == 0
    assert full_quotient * pure == (full_quotient * desired) * nonzero_response
    assert full_nuisance.row_join(desired).rank() == full_nuisance.rank()
    assert full_nuisance.row_join(pure).rank() == full_nuisance.rank()


def incidence_witness(
    nuisance: sp.Matrix, pure: sp.Matrix
) -> tuple[sp.Matrix, sp.Matrix] | None:
    """Solve y^T A=0 and 1-sum_c u_c y^T d_c=0 when possible."""

    annihilator = nuisance.T.nullspace()
    for y in annihilator:
        pairings = y.T * pure
        for colour in range(pure.cols):
            value = pairings[0, colour]
            if value:
                u = sp.zeros(pure.cols, 1)
                u[colour] = 1 / value
                assert y.T * nuisance == sp.zeros(1, nuisance.cols)
                assert (u.T * pairings.T)[0] == 1
                return y, u
    return None


def check_pure_survival_incidence() -> None:
    """Replay the kernel-witness incidence equivalence."""

    e0, e1, e2 = (sp.eye(3)[:, index] for index in range(3))
    nuisance = sp.Matrix.hstack(e0 - e1, e2)
    pure = sp.Matrix.hstack(e0, e1, 2 * e0)
    assert nuisance.row_join(pure).rank() > nuisance.rank()
    assert incidence_witness(nuisance, pure) is not None

    swallowed = sp.Matrix.hstack(e0 - e1, e2, e0 - e1 + e2)
    assert nuisance.row_join(swallowed).rank() == nuisance.rank()
    assert incidence_witness(nuisance, swallowed) is None


def check_shared_contraction_incidence() -> None:
    """A shared z enforces one contraction across copied target systems."""

    z, y1, u1, y2, u2 = sp.symbols("z y1 u1 y2 u2")
    shared = sp.groebner(
        [y1 * (z - 1), 1 - u1 * y1, y2 * (z - 2), 1 - u2 * y2],
        y1,
        u1,
        y2,
        u2,
        z,
        order="grevlex",
        domain=sp.QQ,
    )
    assert shared.contains(sp.Integer(1))

    z1, z2 = sp.symbols("z1 z2")
    separate_equations = [
        y1 * (z1 - 1),
        1 - u1 * y1,
        y2 * (z2 - 2),
        1 - u2 * y2,
    ]
    separate = sp.groebner(
        separate_equations,
        y1,
        u1,
        y2,
        u2,
        z1,
        z2,
        order="grevlex",
        domain=sp.QQ,
    )
    assert not separate.contains(sp.Integer(1))
    exact_point = {z1: 1, z2: 2, y1: 1, u1: 1, y2: 1, u2: 1}
    assert all(
        sp.expand(equation.subs(exact_point)) == 0 for equation in separate_equations
    )


def response_containment_holds(
    nuisance: sp.Matrix,
    desired: sp.Matrix,
    response: list[sp.Expr],
    variable: sp.Symbol,
) -> bool:
    """Check Rho I_j([A|g]) subset sqrt(I_j(A)) in Q[s]."""

    augmented = nuisance.row_join(desired)
    for size in range(1, nuisance.rows + 1):
        radical = radical_generator(minors(nuisance, size), variable)
        for rho in response:
            for determinant in minors(augmented, size):
                if not is_divisible_by(rho * determinant, radical, variable):
                    return False
    return True


def check_response_gated_rank_controls() -> None:
    """Replay positive and negative response-gated polynomial controls."""

    s = sp.symbols("s")
    nuisance = sp.Matrix([[s - 1, 0], [0, 1]])
    desired = sp.Matrix([1, 0])

    vanishing_response = [s - 1, (s - 1) ** 2]
    assert response_containment_holds(nuisance, desired, vanishing_response, s)
    for value in (sp.Integer(1), sp.Integer(2), sp.Integer(-2)):
        evaluated_nuisance = nuisance.subs(s, value)
        evaluated_augmented = evaluated_nuisance.row_join(desired)
        survives = evaluated_augmented.rank() > evaluated_nuisance.rank()
        response_nonzero = any(rho.subs(s, value) != 0 for rho in vanishing_response)
        assert not (survives and response_nonzero)

    live_response = [sp.Integer(1), s - 1]
    assert not response_containment_holds(nuisance, desired, live_response, s)
    assert nuisance.subs(s, 1).rank() == 1
    assert nuisance.row_join(desired).subs(s, 1).rank() == 2
    assert live_response[0] != 0


def main() -> None:
    check_strictness_examples()
    check_projected_kernel_formula()
    check_injective_swallowed_countermodel()
    check_legal_selector_with_supply_failure()
    check_witness_pure_profile_replacement()
    check_pure_survival_incidence()
    check_shared_contraction_incidence()
    check_response_gated_rank_controls()
    print("pointwise selector-failure and decomposable-retraction verifier: PASS")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
