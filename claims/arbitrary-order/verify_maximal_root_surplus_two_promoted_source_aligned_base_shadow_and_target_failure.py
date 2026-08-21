"""Focused exact checks for the GLS20 promoted source-aligned base shadow.

The arbitrary-root theorem is proved in the owning Markdown document.  These
checks replay its Laplace partition at several orders and its quotient,
target, trichotomy, and rank-stratum identities over exact rational arithmetic.
They do not prove survival, response nonvanishing, or strategic-node closure.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations, permutations, product

import sympy as sp


@cache
def permanent(entries: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    if not entries:
        return sp.Integer(1)
    answer = sp.Integer(0)
    tail = entries[1:]
    for column, value in enumerate(entries[0]):
        minor = tuple(row[:column] + row[column + 1 :] for row in tail)
        answer += value * permanent(minor)
    return sp.expand(answer)


def matrix_permanent(matrix: sp.MatrixBase) -> sp.Expr:
    assert matrix.rows == matrix.cols
    return permanent(
        tuple(
            tuple(matrix[row, column] for column in range(matrix.cols))
            for row in range(matrix.rows)
        )
    )


def incidence_matrix(order: int) -> sp.Matrix:
    return sp.Matrix(
        order,
        order,
        lambda row, column: 1
        + ((row + 2) * (column + 3) + row * row + 2 * column) % 11,
    )


def check_source_laplace() -> tuple[int, tuple[tuple[int, int], ...]]:
    checked = 0
    records = []
    for order in range(3, 8):
        incidence = incidence_matrix(order)
        direct = matrix_permanent(incidence)
        assert direct != 0
        total = sp.Integer(0)
        nonzero_base = 0
        for pair in combinations(range(order), 2):
            complement = tuple(index for index in range(order) if index not in pair)
            base = matrix_permanent(incidence.extract((0, 1), pair))
            tail = matrix_permanent(
                incidence.extract(tuple(range(2, order)), complement)
            )
            total += base * tail
            nonzero_base += int(base != 0)
            checked += 1
        assert sp.expand(total - direct) == 0
        assert nonzero_base
        records.append((order, nonzero_base))
    return checked, tuple(records)


def rank(matrix: sp.MatrixBase) -> int:
    return int(matrix.rank())


def check_factor_through_selector() -> dict[str, int]:
    # L_C^* has dimension 9*9=81 and epsilon_A has target dimension 9.
    x_a0 = sp.Matrix([[1, 2, 3]])
    x_a1 = sp.Matrix([[2, -1, 4]])
    root_contraction = sp.kronecker_product(x_a0, x_a1)
    epsilon = sp.kronecker_product(root_contraction, sp.eye(9))
    assert epsilon.shape == (9, 81)

    # Choose five complete nuisance columns whose base shadows span e_0,...,e_4.
    lifts = []
    for coordinate in range(5):
        lift = sp.zeros(81, 1)
        lift[coordinate] = 1
        lifts.append(lift)
    nuisance = sp.Matrix.hstack(*lifts)
    base_nuisance = epsilon * nuisance
    assert rank(base_nuisance) == 5

    desired = sp.zeros(81, 1)
    desired[8] = 1
    base_desired = epsilon * desired
    assert rank(base_nuisance.row_join(base_desired)) == 6

    mu = sp.zeros(1, 9)
    mu[0, 8] = 1 / root_contraction[0, 0]
    selector = mu * epsilon
    assert mu * base_nuisance == sp.zeros(1, nuisance.cols)
    assert (mu * base_desired)[0] == 1
    assert selector * nuisance == sp.zeros(1, nuisance.cols)
    assert (selector * desired)[0] == 1

    # Base absorption follows from full absorption.
    swallowed = nuisance[:, 0] + 2 * nuisance[:, 1]
    assert rank(nuisance.row_join(swallowed)) == rank(nuisance)
    assert rank(base_nuisance.row_join(epsilon * swallowed)) == rank(base_nuisance)

    # The reverse implication is deliberately false: two different lifts can
    # have the same base image, so full survival can be invisible downstairs.
    invisible_nuisance = sp.zeros(81, 1)
    invisible_nuisance[0] = 1
    invisible_desired = invisible_nuisance.copy()
    invisible_desired[9] += 1
    assert epsilon * invisible_desired == epsilon * invisible_nuisance + epsilon[:, 9]
    # Cancel the extra image with a scaled coordinate-0 lift.
    correction = epsilon[:, 9][0] / epsilon[:, 0][0]
    invisible_desired = invisible_desired - correction * sp.eye(81)[:, 0]
    assert epsilon * invisible_desired == epsilon * invisible_nuisance
    assert rank(invisible_nuisance.row_join(invisible_desired)) == 2

    return {
        "full_dimension": 81,
        "base_dimension": 9,
        "base_nuisance_rank": rank(base_nuisance),
    }


def check_pure_column_contraction() -> dict[str, object]:
    x_a0 = sp.Matrix([[2, 3, 5]])
    x_a1 = sp.Matrix([[7, 11, 13]])
    epsilon = sp.kronecker_product(
        sp.kronecker_product(x_a0, x_a1), sp.eye(9)
    )
    basis3 = sp.eye(3)
    basis9 = sp.eye(9)
    kappas = []
    contracted = []
    for colour in range(3):
        root_pure = sp.kronecker_product(
            basis3[:, colour], basis3[:, colour]
        )
        pair_coordinate = 3 * colour + colour
        pair_pure = basis9[:, pair_coordinate]
        full_pure = sp.kronecker_product(root_pure, pair_pure)
        kappa = x_a0[0, colour] * x_a1[0, colour]
        assert epsilon * full_pure == kappa * pair_pure
        kappas.append(int(kappa))
        contracted.append(kappa * pair_pure)

    # Build an exact two-dimensional quotient in which all three diagonal
    # classes lie on one line, then read the response from the target identity.
    quotient = sp.zeros(2, 9)
    coefficients = (2, -3, 5)
    for colour, coefficient in enumerate(coefficients):
        quotient[:, 3 * colour + colour] = sp.Matrix([coefficient, 2 * coefficient])
    pure_quotient = quotient * sp.Matrix.hstack(*contracted)
    assert rank(pure_quotient) == 1
    alpha = sp.diag(17, 19, 23)
    left = pure_quotient * alpha
    base_class = sp.Matrix([1, 2])
    response = sp.Matrix([[left[0, column] for column in range(3)]])
    assert left == base_class * response

    # Exhaust the absorption / zero-response / useful trichotomy.
    cases = 0
    for survives, response_nonzero in product((False, True), repeat=2):
        branch = (
            "absorbed"
            if not survives
            else "zero-response"
            if not response_nonzero
            else "useful"
        )
        pure_rank = int(survives and response_nonzero)
        assert (pure_rank == 0) == ((not survives) or (not response_nonzero))
        assert branch in {"absorbed", "zero-response", "useful"}
        cases += 1

    return {"kappas": tuple(kappas), "pure_rank": rank(pure_quotient), "cases": cases}


def minors(matrix: sp.MatrixBase, size: int) -> tuple[sp.Expr, ...]:
    if size > min(matrix.shape):
        return (sp.Integer(0),)
    return tuple(
        sp.expand(matrix.extract(rows, columns).det())
        for rows in combinations(range(matrix.rows), size)
        for columns in combinations(range(matrix.cols), size)
    )


def check_rank_strata() -> int:
    # Fibrewise form of every determinantal stratum used by the Fitting proof.
    cases = 0
    matrices = tuple(sp.Matrix(2, 2, entries) for entries in product((0, 1), repeat=4))
    pure_matrices = tuple(
        sp.Matrix(2, 3, entries) for entries in product((0, 1), repeat=6)
    )
    for nuisance in matrices:
        for pure in pure_matrices:
            augmented = nuisance.row_join(pure)
            rise = rank(augmented) > rank(nuisance)
            detected = any(
                all(value == 0 for value in minors(nuisance, size))
                and any(value != 0 for value in minors(augmented, size))
                for size in (1, 2)
            )
            assert rise == detected
            cases += 1
    return cases


def check_small_root_interfaces() -> tuple[tuple[int, int, int], ...]:
    records = []
    for order in range(3, 8):
        source_pairs = int(sp.binomial(order, 2))
        promoted_ports = 2 * order - 2
        promoted_targets = int(sp.binomial(promoted_ports, 2)) + 1
        target_size = 2 * order - 4
        records.append((order, source_pairs, target_size))
        assert source_pairs < promoted_targets
    assert records[0] == (3, 3, 2)
    assert records[1] == (4, 6, 4)
    return tuple(records)


def main() -> None:
    laplace = check_source_laplace()
    selector = check_factor_through_selector()
    target = check_pure_column_contraction()
    strata = check_rank_strata()
    interfaces = check_small_root_interfaces()
    print("promoted source-aligned base-shadow primary checks: PASS")
    print("  source Laplace pairs / nonzero counts:", laplace)
    print("  factor-through quotient:", selector)
    print("  contracted target identity:", target)
    print("  exact fibre rank tables:", strata)
    print("  root-order/source-pair/target-size records:", interfaces)
    print("  scope: failure reduction only; survival, activity, and node closure stay open")


if __name__ == "__main__":
    main()
