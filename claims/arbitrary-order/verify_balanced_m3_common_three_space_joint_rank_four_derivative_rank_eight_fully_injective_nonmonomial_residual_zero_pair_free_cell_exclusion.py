#!/usr/bin/env python3
"""Exact replay for the nonmonomial zero-pair-free cell exclusion.

The written proof owns two analytic inputs: S2BQ's exhaustive shared-factor
root-torus split and S2CK's two-transverse mixed-map obstruction.  This
deterministic SymPy replay checks the algebra between them.  It exhausts the
support walls in the noncoordinate quotient-monomial case, constructs every
required perpendicular covector, and checks the rank-one/rank-two ``2 x 2``
restricted-block witnesses in the coordinate case and its root exchange.
It uses no solver and does not claim that finite fixtures prove either
analytic input.
"""

from __future__ import annotations

from itertools import product

import sympy as sp

Support = frozenset[int]


def unit(size: int, index: int) -> sp.Matrix:
    value = sp.zeros(size, 1)
    value[index] = 1
    return value


def support(mask: int) -> Support:
    return frozenset(index for index in range(3) if mask & (1 << index))


def support_vector(support_set: Support, prefix: str) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.symbols(f"{prefix}{index}", nonzero=True)
            if index in support_set
            else 0
            for index in range(3)
        ]
    )


def complement(index: int) -> tuple[int, int]:
    return tuple(value for value in range(3) if value != index)  # type: ignore[return-value]


def assert_zero(value: sp.Expr | sp.Matrix) -> None:
    if isinstance(value, sp.MatrixBase):
        assert all(sp.factor(entry) == 0 for entry in value)
    else:
        assert sp.factor(value) == 0


def assert_nonzero(value: sp.Expr) -> None:
    assert sp.factor(value).is_zero is False


def corrected_cube(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    correction: sp.Expr,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    targets = tuple(unit(6, index) for index in range(3))
    sources = tuple(unit(6, 3 + index) for index in range(3))
    return tuple(
        sp.simplify(
            alpha[index] * beta[index] * targets[index]
            + correction * sources[index]
        )
        for index in range(3)
    )


def check_cube_support(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    correction: sp.Expr,
    active_colours: set[int],
) -> None:
    assert_zero(correction)
    values = corrected_cube(alpha, beta, correction)
    for index, value in enumerate(values):
        coefficient = sp.factor(alpha[index] * beta[index])
        if index in active_colours:
            assert_nonzero(coefficient)
            assert value[index] == coefficient
            assert all(value[row] == 0 for row in range(6) if row != index)
        else:
            assert_zero(value)
    assert sp.Matrix.hstack(*values).rank() == len(active_colours)


def boundary_covector(vector: sp.Matrix, omitted: int) -> sp.Matrix:
    """Span ``vector^perp intersect ker(ev_omitted)`` exactly."""

    first, second = complement(omitted)
    value = sp.zeros(3, 1)
    value[first] = vector[second]
    value[second] = -vector[first]
    assert_zero(value.dot(vector))
    assert value[omitted] == 0
    return value


def full_partner_covector(vector: sp.Matrix, omitted: int) -> sp.Matrix:
    """Construct a perpendicular covector nonzero off ``omitted``."""

    first, second = complement(omitted)
    value = sp.zeros(3, 1)
    if vector[omitted] != 0:
        value[first] = 1
        value[second] = 1
        value[omitted] = -(
            vector[first] + vector[second]
        ) / vector[omitted]
    else:
        value[first] = vector[second]
        value[second] = -vector[first]
    assert_zero(value.dot(vector))
    assert_nonzero(value[first])
    assert_nonzero(value[second])
    return value


def check_s2bq_support_split() -> None:
    """Check that the two proof cases exhaust all nonzero support masks."""

    supports = tuple(support(mask) for mask in range(1, 8))
    noncoordinate = {value for value in supports if len(value) >= 2}
    coordinate = {value for value in supports if len(value) == 1}
    both_noncoordinate = {
        pair
        for pair in product(supports, repeat=2)
        if pair[0] in noncoordinate and pair[1] in noncoordinate
    }
    at_least_one_coordinate = set(product(supports, repeat=2))
    at_least_one_coordinate -= both_noncoordinate
    assert len(both_noncoordinate) == 16
    assert len(at_least_one_coordinate) == 33
    assert all(
        left in coordinate or right in coordinate
        for left, right in at_least_one_coordinate
    )
    assert all(
        left in coordinate
        or (right, left) in {
            (first, second)
            for first, second in at_least_one_coordinate
            if first in coordinate
        }
        for left, right in at_least_one_coordinate
    )


def check_noncoordinate_quotient_monomial_case() -> None:
    """Exhaust ``[C]=lambda ev_d tensor ev_e`` for noncoordinate x,y."""

    noncoordinate_supports = tuple(
        support(mask) for mask in range(1, 8) if len(support(mask)) >= 2
    )
    scale = sp.symbols("quotient_scale", nonzero=True)
    structural_count = 0
    secant_count = 0

    for case_index, (x_support, y_support, d, e) in enumerate(
        product(noncoordinate_supports, noncoordinate_supports, range(3), range(3))
    ):
        x = support_vector(x_support, f"nx{case_index}_")
        y = support_vector(y_support, f"ny{case_index}_")
        alpha = boundary_covector(x, d)
        assert alpha != sp.zeros(3, 1)
        alpha_support = {
            index for index in range(3) if alpha[index] != 0
        }
        assert alpha_support <= set(complement(d))
        correction_factor = scale * alpha[d]

        if len(alpha_support) == 1:
            # A singleton alpha produces a structural zero against the
            # nonzero line y^perp intersect ker(ev_a).
            singleton = next(iter(alpha_support))
            beta = boundary_covector(y, singleton)
            assert beta != sp.zeros(3, 1)
            assert beta[singleton] == 0
            correction = correction_factor * beta[e]
            check_cube_support(alpha, beta, correction, set())
            structural_count += 1
        else:
            # The only zero-pair-free possibility is full support on the two
            # colours off d.  This explicit beta avoids both coordinate lines.
            assert alpha_support == set(complement(d))
            beta = full_partner_covector(y, d)
            correction = correction_factor * beta[e]
            check_cube_support(alpha, beta, correction, set(complement(d)))
            secant_count += 1

    # Four noncoordinate supports for each root, three d and three e choices.
    # Exactly half of the x,d walls are singleton and half are two-supported.
    assert structural_count == secant_count == 72


def embed_complement(value: sp.Matrix, coordinate: int) -> sp.Matrix:
    first, second = complement(coordinate)
    result = sp.zeros(3, 1)
    result[first] = value[0]
    result[second] = value[1]
    return result


def perpendicular_lift(
    value: sp.Matrix,
    root: sp.Matrix,
    coordinate: int,
) -> sp.Matrix:
    """Invert ``root^perp -> coordinates complement {coordinate}``."""

    first, second = complement(coordinate)
    assert root[coordinate] != 0
    result = embed_complement(value, coordinate)
    result[coordinate] = -(
        root[first] * value[0] + root[second] * value[1]
    ) / root[coordinate]
    assert_zero(result.dot(root))
    return result


def coordinate_embedding(
    coordinate: int,
    coordinate_first: bool,
    left: sp.Matrix,
    right: sp.Matrix,
    partner_root: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    """Embed the restricted pair and also replay first/second-root exchange."""

    if coordinate_first:
        x = unit(3, coordinate)
        y = partner_root
        alpha = embed_complement(left, coordinate)
        beta = perpendicular_lift(right, y, coordinate)
    else:
        x = partner_root
        y = unit(3, coordinate)
        alpha = perpendicular_lift(left, x, coordinate)
        beta = embed_complement(right, coordinate)
    assert_zero(alpha.dot(x))
    assert_zero(beta.dot(y))
    return x, y, alpha, beta


def check_coordinate_partner_wall() -> None:
    """If the other root has zero s-coordinate, a structural zero exists."""

    g0 = sp.symbols("wall_g0", nonzero=True)
    g1 = sp.symbols("wall_g1", nonzero=True)
    functionals = (
        sp.Matrix([g0, g1]),
        sp.Matrix([g0, 0]),
        sp.Matrix([0, g1]),
        sp.zeros(2, 1),
    )
    for coordinate, coordinate_first, functional in product(
        range(3),
        (True, False),
        functionals,
    ):
        first, second = complement(coordinate)
        partner_support = sp.Matrix([2, 3, 5])
        partner_support[coordinate] = 0
        if functional == sp.zeros(2, 1):
            kernel = unit(2, 0)
        else:
            kernel = sp.Matrix([functional[1], -functional[0]])
        assert kernel != sp.zeros(2, 1)
        assert_zero(functional.dot(kernel))

        if coordinate_first:
            x = unit(3, coordinate)
            y = partner_support
            alpha = embed_complement(kernel, coordinate)
            beta = unit(3, coordinate)
        else:
            x = partner_support
            y = unit(3, coordinate)
            alpha = unit(3, coordinate)
            beta = embed_complement(kernel, coordinate)
        if coordinate_first:
            assert y[first] != 0 and y[second] != 0
        else:
            assert x[first] != 0 and x[second] != 0
        assert_zero(alpha.dot(x))
        assert_zero(beta.dot(y))
        check_cube_support(alpha, beta, functional.dot(kernel), set())


def check_cross_entry_structural_walls() -> None:
    """A zero cross entry of the restricted D gives a structural zero."""

    partner = sp.Matrix([2, 3, 5])
    for coordinate, coordinate_first, row_index, column_index in product(
        range(3),
        (True, False),
        range(2),
        range(2),
    ):
        if row_index == column_index:
            continue
        left = unit(2, row_index)
        right = unit(2, column_index)
        _, _, alpha, beta = coordinate_embedding(
            coordinate,
            coordinate_first,
            left,
            right,
            partner,
        )
        restricted = sp.Matrix(
            [
                [sp.symbols("wall_d00"), sp.symbols("wall_d01")],
                [sp.symbols("wall_d10"), sp.symbols("wall_d11")],
            ]
        )
        restricted[row_index, column_index] = 0
        correction = (left.T * restricted * right)[0]
        check_cube_support(alpha, beta, correction, set())


def check_rank_one_restricted_block() -> None:
    """Cross-nonzero rank one gives a full left-kernel covector."""

    u0, u1, v0, v1 = sp.symbols("rank1_u0 rank1_u1 rank1_v0 rank1_v1", nonzero=True)
    left_factor = sp.Matrix([u0, u1])
    right_factor = sp.Matrix([v0, v1])
    restricted = left_factor * right_factor.T
    alpha_two = sp.Matrix([u1, -u0])
    beta_two = sp.ones(2, 1)
    assert_nonzero(restricted[0, 1])
    assert_nonzero(restricted[1, 0])
    assert_zero(alpha_two.T * restricted)
    assert_zero((alpha_two.T * restricted * beta_two)[0])

    partner = sp.Matrix([2, 3, 5])
    for coordinate, coordinate_first in product(range(3), (True, False)):
        _, _, alpha, beta = coordinate_embedding(
            coordinate,
            coordinate_first,
            alpha_two,
            beta_two,
            partner,
        )
        correction = (alpha_two.T * restricted * beta_two)[0]
        check_cube_support(alpha, beta, correction, set(complement(coordinate)))


def choose_integer_avoiding_parameter(restricted: sp.Matrix) -> int:
    for parameter in range(-4, 5):
        alpha = sp.Matrix([1, parameter])
        image = alpha.T * restricted
        if parameter != 0 and image[0] != 0 and image[1] != 0:
            return parameter
    raise AssertionError("three forbidden affine values cannot fill nine choices")


def check_rank_two_four_line_avoidance() -> None:
    """Replay the four-line argument symbolically and on exact integer data."""

    d00, d01, d10, d11, parameter = sp.symbols(
        "rank2_d00 rank2_d01 rank2_d10 rank2_d11 rank2_parameter"
    )
    restricted = sp.Matrix([[d00, d01], [d10, d11]])
    alpha = sp.Matrix([1, parameter])
    image = alpha.T * restricted
    beta = sp.Matrix([image[1], -image[0]])
    forbidden_polynomial = sp.factor(parameter * image[0] * image[1])
    assert_zero((alpha.T * restricted * beta)[0])
    assert sp.Poly(forbidden_polynomial, parameter).degree() == 3
    # The four projective forbidden lines are alpha_0=0, alpha_1=0, and
    # the inverse images of the two coordinate lines under D^T.  If det D
    # is nonzero all four are proper; infinitude supplies a point off them.
    assert_zero(restricted.det().subs({d00: 0, d10: 0}))
    assert_zero(restricted.det().subs({d01: 0, d11: 0}))

    entries = (-2, -1, 0, 1, 2)
    cross_entries = (-2, -1, 1, 2)
    fixture_count = 0
    partner = sp.Matrix([2, 3, 5])
    for top_left, top_right, bottom_left, bottom_right in product(
        entries,
        cross_entries,
        cross_entries,
        entries,
    ):
        fixture = sp.Matrix(
            [[top_left, top_right], [bottom_left, bottom_right]]
        )
        if fixture.det() == 0:
            continue
        chosen = choose_integer_avoiding_parameter(fixture)
        alpha_two = sp.Matrix([1, chosen])
        image_two = alpha_two.T * fixture
        beta_two = sp.Matrix([image_two[1], -image_two[0]])
        assert chosen != 0
        assert image_two[0] != 0 and image_two[1] != 0
        assert_zero((alpha_two.T * fixture * beta_two)[0])

        # Every coordinate and both root orientations replay the exact c=0
        # cube, without using a label-symmetry shortcut in the executable.
        for coordinate, coordinate_first in product(
            range(3),
            (True, False),
        ):
            _, _, alpha_three, beta_three = coordinate_embedding(
                coordinate,
                coordinate_first,
                alpha_two,
                beta_two,
                partner,
            )
            correction = (alpha_two.T * fixture * beta_two)[0]
            check_cube_support(
                alpha_three,
                beta_three,
                correction,
                set(complement(coordinate)),
            )
        fixture_count += 1
    assert fixture_count == 352


def check_root_exchange_scalar_identity() -> None:
    """Transposition exactly implements exchange of the first two roots."""

    entries = sp.symbols("exchange_D0:4")
    restricted = sp.Matrix(2, 2, entries)
    alpha = sp.Matrix(sp.symbols("exchange_alpha0:2"))
    beta = sp.Matrix(sp.symbols("exchange_beta0:2"))
    assert_zero(
        (alpha.T * restricted * beta)[0]
        - (beta.T * restricted.T * alpha)[0]
    )
    assert_zero(alpha[0] * beta[0] - beta[0] * alpha[0])
    assert_zero(alpha[1] * beta[1] - beta[1] * alpha[1])


def main() -> None:
    check_s2bq_support_split()
    check_noncoordinate_quotient_monomial_case()
    check_coordinate_partner_wall()
    check_cross_entry_structural_walls()
    check_rank_one_restricted_block()
    check_rank_two_four_line_avoidance()
    check_root_exchange_scalar_identity()
    print("S2BQ support split: PASS (16 noncoordinate + 33 coordinate)")
    print("noncoordinate quotient-monomial walls and beta witnesses: PASS")
    print("coordinate partner/cross-entry structural walls: PASS")
    print("rank-one and rank-two restricted-block witnesses: PASS")
    print("first/second-root exchange: PASS")
    print("analytic owners: S2BQ exhaustive reduction and S2CK obstruction")


if __name__ == "__main__":
    main()
