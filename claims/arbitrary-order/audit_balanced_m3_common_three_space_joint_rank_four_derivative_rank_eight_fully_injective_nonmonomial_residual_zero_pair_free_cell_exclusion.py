#!/usr/bin/env python3
"""Independent Fraction audit of the nonmonomial zero-pair-free exclusion.

This standard-library-only replay reverses the support and coordinate-wall
traversals used by the primary checker.  It reconstructs the S2BQ branch
census, every exact noncoordinate and coordinate structural-zero
construction, the two ``2 x 2`` determinant branches on coordinate walls,
the correction-zero/two-target coefficient interface, and the exchanged-root
cases with independent rational fixtures.

S2BQ's root-torus exhaustiveness and S2CK's two-transverse mixed-map lemma
remain analytic inputs of the owning theorem.  This script checks the exact
finite support, bilinear, and cube interfaces to those results.  It imports
no primary verifier, SymPy, or solver.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

Q = Fraction
DIM = 3
COLOURS = tuple(reversed(range(DIM)))
MASKS = tuple(reversed(range(1, 1 << DIM)))

Vector = tuple[Q, ...]
Matrix2 = tuple[Q, Q, Q, Q]


def zero(size: int) -> Vector:
    return (Q(0),) * size


def unit(size: int, index: int) -> Vector:
    return tuple(Q(candidate == index) for candidate in range(size))


def dot(left: Vector, right: Vector) -> Q:
    return sum(
        (first * second for first, second in zip(left, right, strict=True)),
        Q(0),
    )


def support(vector: Vector) -> tuple[int, ...]:
    return tuple(index for index, entry in enumerate(vector) if entry)


def mask_support(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(DIM) if mask & (1 << index))


def is_coordinate_mask(mask: int) -> bool:
    return len(mask_support(mask)) == 1


def representative(mask: int, side: str) -> Vector:
    weights = {
        "x": (Q(-2), Q(3), Q(5)),
        "y": (Q(7), Q(-11), Q(13)),
    }[side]
    value = tuple(
        weights[index] if mask & (1 << index) else Q(0)
        for index in range(DIM)
    )
    assert support(value) == mask_support(mask)
    return value


def coordinate_kernel(vector: Vector, coordinate: int) -> Vector:
    """A nonzero vector in vector^perp with this coordinate zero."""
    other = tuple(index for index in range(DIM) if index != coordinate)
    result = [Q(0)] * DIM
    result[other[0]] = vector[other[1]]
    result[other[1]] = -vector[other[0]]
    candidate = tuple(result)
    assert dot(candidate, vector) == 0
    assert candidate[coordinate] == 0
    assert any(candidate)
    return candidate


def beta_with_two_nonzero_coordinates(
    y: Vector,
    first: int,
    second: int,
) -> Vector:
    """Choose beta in y^perp with beta_first beta_second nonzero."""
    third = next(index for index in range(DIM) if index not in {first, second})
    result = [Q(0)] * DIM
    if y[third]:
        result[first] = Q(1)
        result[second] = Q(1)
        result[third] = -(y[first] + y[second]) / y[third]
    else:
        # Noncoordinate y and y_third=0 force both displayed coordinates
        # to be nonzero.
        assert y[first] != 0 and y[second] != 0
        result[first] = y[second]
        result[second] = -y[first]
    beta = tuple(result)
    assert dot(beta, y) == 0
    assert beta[first] != 0 and beta[second] != 0
    return beta


def cube_target_coefficients(alpha: Vector, beta: Vector, correction: Q) -> Vector:
    """Target coefficients when the common S_k correction is displayed."""
    assert correction == 0
    return tuple(alpha[k] * beta[k] for k in range(DIM))


def assert_structural_zero(alpha: Vector, beta: Vector, correction: Q) -> None:
    assert any(alpha) and any(beta)
    assert correction == 0
    assert cube_target_coefficients(alpha, beta, correction) == zero(DIM)
    assert set(support(alpha)).isdisjoint(support(beta))


def assert_two_target_secant(
    alpha: Vector,
    beta: Vector,
    correction: Q,
    first: int,
    second: int,
) -> None:
    coefficients = cube_target_coefficients(alpha, beta, correction)
    assert coefficients[first] != 0 and coefficients[second] != 0
    assert all(
        coefficient == 0
        for index, coefficient in enumerate(coefficients)
        if index not in {first, second}
    )


def check_s2bq_branch_census() -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    all_pairs = set(product(MASKS, repeat=2))
    both_noncoordinate = {
        pair
        for pair in all_pairs
        if not is_coordinate_mask(pair[0]) and not is_coordinate_mask(pair[1])
    }
    coordinate_union = all_pairs - both_noncoordinate
    first_coordinate = {pair for pair in coordinate_union if is_coordinate_mask(pair[0])}
    second_only = coordinate_union - first_coordinate
    assert len(all_pairs) == 49
    assert len(both_noncoordinate) == 16
    assert len(coordinate_union) == 33
    assert len(first_coordinate) == 21
    assert len(second_only) == 12
    assert all(is_coordinate_mask(pair[1]) for pair in second_only)
    return both_noncoordinate, coordinate_union


def check_noncoordinate_monomial_quotient_branch() -> tuple[int, int]:
    structural_count = 0
    secant_count = 0
    noncoordinate_masks = tuple(mask for mask in MASKS if not is_coordinate_mask(mask))
    for x_mask, y_mask in reversed(tuple(product(noncoordinate_masks, repeat=2))):
        x = representative(x_mask, "x")
        y = representative(y_mask, "y")
        for d, e in reversed(tuple(product(COLOURS, repeat=2))):
            # S2BQ supplies Cbar=lambda ev_d tensor ev_e.  Noncoordinate
            # x,y ensure both restricted evaluation forms are nonzero.
            alpha = coordinate_kernel(x, d)
            assert alpha[d] == 0
            if len(support(alpha)) == 1:
                singleton = support(alpha)[0]
                assert singleton != d
                beta = coordinate_kernel(y, singleton)
                correction = alpha[d] * beta[e]
                assert_structural_zero(alpha, beta, correction)
                structural_count += 1
                continue

            assert len(support(alpha)) == 2
            first, second = support(alpha)
            beta = beta_with_two_nonzero_coordinates(y, first, second)
            correction = alpha[d] * beta[e]
            assert correction == 0
            assert_two_target_secant(alpha, beta, correction, first, second)
            secant_count += 1

    assert structural_count > 0 and secant_count > 0
    assert structural_count + secant_count == 16 * 9
    return structural_count, secant_count


def determinant_2(matrix: Matrix2) -> Q:
    return matrix[0] * matrix[3] - matrix[1] * matrix[2]


def rank_2(matrix: Matrix2) -> int:
    if determinant_2(matrix):
        return 2
    return int(any(matrix))


def transpose_2(matrix: Matrix2) -> Matrix2:
    return matrix[0], matrix[2], matrix[1], matrix[3]


def bilinear_2(left: Vector, matrix: Matrix2, right: Vector) -> Q:
    assert len(left) == len(right) == 2
    return (
        left[0] * matrix[0] * right[0]
        + left[0] * matrix[1] * right[1]
        + left[1] * matrix[2] * right[0]
        + left[1] * matrix[3] * right[1]
    )


def lift_projected_beta(y: Vector, s: int, projected: Vector) -> Vector:
    other = tuple(index for index in range(DIM) if index != s)
    assert len(projected) == 2 and y[s] != 0
    beta = [Q(0)] * DIM
    beta[other[0]], beta[other[1]] = projected
    beta[s] = -(
        y[other[0]] * projected[0] + y[other[1]] * projected[1]
    ) / y[s]
    result = tuple(beta)
    assert dot(result, y) == 0
    return result


def lift_projected_alpha(s: int, projected: Vector) -> Vector:
    other = tuple(index for index in range(DIM) if index != s)
    assert len(projected) == 2
    alpha = [Q(0)] * DIM
    alpha[other[0]], alpha[other[1]] = projected
    return tuple(alpha)


def choose_rank_two_witness(matrix: Matrix2) -> tuple[Vector, Vector]:
    assert determinant_2(matrix) != 0
    slopes = tuple(reversed((Q(1), Q(2), Q(3), Q(5))))
    for slope in slopes:
        alpha = (Q(1), slope)
        row = (
            alpha[0] * matrix[0] + alpha[1] * matrix[2],
            alpha[0] * matrix[1] + alpha[1] * matrix[3],
        )
        if row[0] and row[1]:
            beta = row[1], -row[0]
            assert all(alpha) and all(beta)
            assert bilinear_2(alpha, matrix, beta) == 0
            return alpha, beta
    raise AssertionError("four slopes cannot all lie on two forbidden lines")


def choose_rank_one_witness(matrix: Matrix2) -> tuple[Vector, Vector]:
    assert rank_2(matrix) == 1
    # The coordinate-wall branch reaches this function only after both
    # cross entries have been proved nonzero.  Then det=0 also makes both
    # diagonal entries nonzero.
    assert matrix[1] != 0 and matrix[2] != 0
    assert matrix[0] != 0 and matrix[3] != 0
    alpha = matrix[2], -matrix[0]
    beta = Q(1), Q(-2)
    assert all(alpha) and all(beta)
    assert bilinear_2(alpha, matrix, beta) == 0
    return alpha, beta


def sample_matrices() -> tuple[Matrix2, ...]:
    values = tuple(reversed((Q(-2), Q(-1), Q(0), Q(1), Q(2))))
    return tuple(matrix for matrix in reversed(tuple(product(values, repeat=4))) if any(matrix))


def coordinate_first_wall(
    s: int,
    y: Vector,
    matrix: Matrix2,
) -> tuple[str, Vector, Vector]:
    """Return the exact pair for x=e_s and the given quotient matrix."""
    other = tuple(index for index in range(DIM) if index != s)
    if y[s] == 0:
        # Use the y^perp basis whose first vector is e_s.  The functional
        # Cbar(-,e_s) is the first column of D and always has a kernel.
        column = matrix[0], matrix[2]
        if any(column):
            alpha_projected = column[1], -column[0]
        else:
            alpha_projected = Q(1), Q(0)
        alpha = lift_projected_alpha(s, alpha_projected)
        beta = unit(DIM, s)
        assert bilinear_2(alpha_projected, matrix, (Q(1), Q(0))) == 0
        assert dot(beta, y) == 0
        assert_structural_zero(alpha, beta, Q(0))
        return "structural_y_s_zero", alpha, beta

    # Projection y^perp -> (beta_i,beta_j) is now an isomorphism.  A zero
    # cross entry immediately supplies a disjoint-support structural pair.
    if matrix[1] == 0:
        alpha_projected = Q(1), Q(0)
        beta_projected = Q(0), Q(1)
        alpha = lift_projected_alpha(s, alpha_projected)
        beta = lift_projected_beta(y, s, beta_projected)
        assert bilinear_2(alpha_projected, matrix, beta_projected) == 0
        assert_structural_zero(alpha, beta, Q(0))
        return "structural_ij", alpha, beta
    if matrix[2] == 0:
        alpha_projected = Q(0), Q(1)
        beta_projected = Q(1), Q(0)
        alpha = lift_projected_alpha(s, alpha_projected)
        beta = lift_projected_beta(y, s, beta_projected)
        assert bilinear_2(alpha_projected, matrix, beta_projected) == 0
        assert_structural_zero(alpha, beta, Q(0))
        return "structural_ji", alpha, beta

    if rank_2(matrix) == 2:
        alpha_projected, beta_projected = choose_rank_two_witness(matrix)
        branch = "rank_two_secant"
    else:
        alpha_projected, beta_projected = choose_rank_one_witness(matrix)
        branch = "rank_one_secant"
    alpha = lift_projected_alpha(s, alpha_projected)
    beta = lift_projected_beta(y, s, beta_projected)
    assert bilinear_2(alpha_projected, matrix, beta_projected) == 0
    assert_two_target_secant(alpha, beta, Q(0), other[0], other[1])
    return branch, alpha, beta


def check_coordinate_walls_and_root_exchange() -> dict[str, int]:
    matrices = sample_matrices()
    counts: dict[str, int] = {}
    for s in COLOURS:
        for other_mask in MASKS:
            other_vector = representative(other_mask, "y")
            for matrix in matrices:
                branch, alpha, beta = coordinate_first_wall(
                    s,
                    other_vector,
                    matrix,
                )
                counts[branch] = counts.get(branch, 0) + 1
                assert dot(alpha, unit(DIM, s)) == 0
                assert dot(beta, other_vector) == 0

                # Root exchange: y=e_s, x=other_vector, and Cbar is D^T in
                # the exchanged coordinate bases.  Swap the constructed
                # covectors back and recheck every target coefficient.
                exchanged_branch, exchanged_beta, exchanged_alpha = coordinate_first_wall(
                    s,
                    other_vector,
                    transpose_2(matrix),
                )
                counts[f"exchange_{exchanged_branch}"] = (
                    counts.get(f"exchange_{exchanged_branch}", 0) + 1
                )
                assert dot(exchanged_alpha, other_vector) == 0
                assert dot(exchanged_beta, unit(DIM, s)) == 0
                coefficients = cube_target_coefficients(
                    exchanged_alpha,
                    exchanged_beta,
                    Q(0),
                )
                if exchanged_branch.startswith("structural"):
                    assert_structural_zero(
                        exchanged_alpha,
                        exchanged_beta,
                        Q(0),
                    )
                else:
                    other = tuple(index for index in range(DIM) if index != s)
                    assert_two_target_secant(
                        exchanged_alpha,
                        exchanged_beta,
                        Q(0),
                        other[0],
                        other[1],
                    )
                assert sum(bool(value) for value in coefficients) in {0, 2}

    for name in (
        "structural_y_s_zero",
        "structural_ij",
        "structural_ji",
        "rank_one_secant",
        "rank_two_secant",
    ):
        assert counts.get(name, 0) > 0
        assert counts.get(f"exchange_{name}", 0) > 0
    return counts


def check_rank_witness_formulas_exhaustively() -> tuple[int, int]:
    rank_one = 0
    rank_two = 0
    for matrix in reversed(sample_matrices()):
        if matrix[1] == 0 or matrix[2] == 0:
            continue
        if rank_2(matrix) == 2:
            alpha, beta = choose_rank_two_witness(matrix)
            rank_two += 1
        else:
            alpha, beta = choose_rank_one_witness(matrix)
            rank_one += 1
        assert all(alpha) and all(beta)
        assert bilinear_2(alpha, matrix, beta) == 0
    assert rank_one == 48
    assert rank_two == 352
    return rank_one, rank_two


def main() -> None:
    both_noncoordinate, coordinate_union = check_s2bq_branch_census()
    structural, secants = check_noncoordinate_monomial_quotient_branch()
    counts = check_coordinate_walls_and_root_exchange()
    rank_one, rank_two = check_rank_witness_formulas_exhaustively()

    print(
        "S2BQ support partition "
        f"noncoordinate={len(both_noncoordinate)}, coordinate={len(coordinate_union)}: PASS"
    )
    print(
        f"noncoordinate quotient walls structural={structural}, secants={secants}: PASS"
    )
    print(
        "coordinate/root-exchanged structural and secant constructions "
        f"({sum(counts.values())} exact cases): PASS"
    )
    print(f"2x2 determinant witnesses rank1={rank_one}, rank2={rank_two}: PASS")
    print("all correction-zero cube maps have exactly zero or two targets: PASS")
    print("S2BQ exhaustiveness and S2CK mixed-map obstruction remain analytic inputs")
    print("scope: actual-nonmonomial fully-injective zero-pair-free cell")


if __name__ == "__main__":
    main()
