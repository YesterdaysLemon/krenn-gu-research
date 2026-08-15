#!/usr/bin/env python3
"""Independent no-import audit of the S2CF zero-visible wall interface.

The audit uses only standard-library ``Fraction`` arithmetic.  It exhausts
the support-mask form of the two visibility failures, reconstructs the exact
diagonal-endpoint derivative and kernel-incidence dimensions, and replays
every corrected-cube coefficient which puts a two-plane in one row's
radical.  The coordinate-free radical-line bound is the analytic S2CG
theorem; this script checks its hypotheses and does not claim to reprove it.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction
DIM = 3
ROOT_TRIPLES = tuple(product(reversed(range(DIM)), repeat=3))
SOURCE_TRIPLES = tuple(product(reversed(range(DIM)), repeat=3))
REVERSED_PERMUTATIONS = tuple(reversed(tuple(permutations(range(3)))))

Vector = tuple[Q, ...]


def zero(size: int) -> Vector:
    return (Q(0),) * size


def unit(size: int, index: int) -> Vector:
    return tuple(Q(int(candidate == index)) for candidate in range(size))


def add(*vectors: Vector) -> Vector:
    assert vectors
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: int | Q, vector: Vector) -> Vector:
    scalar = Q(coefficient)
    return tuple(scalar * entry for entry in vector)


def dot(left: Vector, right: Vector) -> Q:
    return sum(
        (first * second for first, second in zip(left, right, strict=True)),
        Q(0),
    )


def concatenate(*vectors: Vector) -> Vector:
    return tuple(entry for vector in vectors for entry in vector)


def row_rank(rows: list[list[Q]]) -> int:
    matrix = [row[:] for row in rows if any(row)]
    if not matrix:
        return 0
    pivot_row = 0
    for column in reversed(range(len(matrix[0]))):
        pivot = next(
            (
                candidate
                for candidate in reversed(range(pivot_row, len(matrix)))
                if matrix[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for candidate in reversed(range(len(matrix))):
            if candidate == pivot_row or not matrix[candidate][column]:
                continue
            multiplier = matrix[candidate][column]
            matrix[candidate] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[candidate], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def column_rank(columns: tuple[Vector, ...] | list[Vector]) -> int:
    if not columns:
        return 0
    return row_rank([list(row) for row in zip(*columns, strict=True)])


def in_span(vector: Vector, columns: tuple[Vector, ...]) -> bool:
    return column_rank((*columns, vector)) == column_rank(columns)


def support_mask(vector: Vector) -> int:
    return sum((1 << index) for index, entry in enumerate(vector) if entry)


def mask_representative(mask: int) -> Vector:
    return tuple(Q(int(bool(mask & (1 << index)))) for index in range(DIM))


def is_coordinate(vector: Vector, index: int) -> bool:
    return support_mask(vector) == 1 << index


def target_visible(x: Vector, y: Vector, index: int) -> bool:
    assert index in (0, 1)
    complementary = 1 - index
    return (
        not is_coordinate(x, index)
        and not is_coordinate(y, index)
        and bool(x[complementary] or y[complementary])
    )


def check_boolean_visibility_cover() -> None:
    # The visibility census depends only on support.  These six nonempty
    # masks are every projective support allowed by x,y not proportional e2.
    masks = tuple(mask for mask in reversed(range(1, 8)) if mask != 1 << 2)
    assert len(masks) == 6
    zero_visible = []
    for x_mask, y_mask in product(masks, repeat=2):
        x = mask_representative(x_mask)
        y = mask_representative(y_mask)
        visible = target_visible(x, y, 0), target_visible(x, y, 1)
        if not any(visible):
            zero_visible.append((x_mask, y_mask))
    assert sorted(zero_visible) == sorted(((1 << 0, 1 << 1), (1 << 1, 1 << 0)))

    e_0, e_1 = unit(3, 0), unit(3, 1)
    assert (target_visible(e_0, e_0, 0), target_visible(e_0, e_0, 1)) == (
        False,
        True,
    )
    assert (target_visible(e_1, e_1, 0), target_visible(e_1, e_1, 1)) == (
        True,
        False,
    )


def split_domain(vector: Vector) -> tuple[Vector, Vector, Vector]:
    assert len(vector) == 9
    return vector[:3], vector[3:6], vector[6:9]


def endpoint_derivative(x: Vector, y: Vector, lam: Q, domain: Vector) -> Vector:
    a, b, c = split_domain(domain)
    result = []
    for i, j, k in ROOT_TRIPLES:
        tangent = (a[i] * y[j] - x[i] * b[j]) * Q(k == 0)
        residual = lam * Q(i == 2 and j == 2) * c[k]
        result.append(tangent + residual)
    return tuple(result)


def domain_basis_vector(block: int, index: int) -> Vector:
    blocks = [zero(3), zero(3), zero(3)]
    blocks[block] = unit(3, index)
    return concatenate(*blocks)


def annihilator_basis(vector: Vector) -> tuple[Vector, ...]:
    pivot = next(index for index in reversed(range(len(vector))) if vector[index])
    basis = []
    for index in reversed(range(len(vector))):
        if index == pivot:
            continue
        candidate = add(
            unit(len(vector), index),
            scale(-vector[index] / vector[pivot], unit(len(vector), pivot)),
        )
        basis.append(candidate)
    return tuple(basis)


def root_projection(vector: Vector, block: int) -> Vector:
    return split_domain(vector)[block]


def check_endpoint_rank_and_radical_interface() -> None:
    lam = Q(11, 5)
    for source_colour, partner_colour in reversed(((0, 1), (1, 0))):
        x = scale(Q(2, 3), unit(3, source_colour))
        y = scale(Q(-5, 7), unit(3, partner_colour))
        n = concatenate(x, y, zero(3))

        derivative_columns = tuple(
            endpoint_derivative(x, y, lam, domain_basis_vector(block, index))
            for block in reversed(range(3))
            for index in reversed(range(3))
        )
        assert column_rank(derivative_columns) == 8
        assert not any(endpoint_derivative(x, y, lam, n))

        # A denominator-free graph basis supplies an exact rank-four K with
        # full three-dimensional projections.  It is a root-side incidence
        # control, not a physical target solution.
        graph_lifts = tuple(
            concatenate(unit(3, index), unit(3, index), unit(3, index))
            for index in reversed(range(3))
        )
        k_basis = (n, *graph_lifts)
        assert column_rank(k_basis) == 4
        assert all(
            column_rank(tuple(root_projection(vector, block) for vector in k_basis)) == 3
            for block in reversed(range(3))
        )
        assert column_rank(
            tuple(endpoint_derivative(x, y, lam, vector) for vector in k_basis)
        ) == 3

        l_basis = annihilator_basis(n)
        assert len(l_basis) == column_rank(l_basis) == 8
        assert all(dot(functional, n) == 0 for functional in l_basis)

        def transpose_row(
            functional: Vector,
            basis: tuple[Vector, ...] = k_basis,
        ) -> Vector:
            return tuple(dot(functional, vector) for vector in basis)

        l_image = tuple(transpose_row(functional) for functional in l_basis)
        third_covectors = tuple(
            domain_basis_vector(2, index) for index in reversed(range(3))
        )
        q_image = tuple(transpose_row(functional) for functional in third_covectors)
        assert column_rank(l_image) == column_rank(q_image) == 3
        assert all(in_span(vector, q_image) for vector in l_image)
        # dim K^perp=5, so dim N^perp/K^perp=8-5=3.
        assert 9 - column_rank(k_basis) == 5
        assert len(l_basis) - column_rank(l_image) == 5

        alpha = unit(3, partner_colour)
        beta_basis = (unit(3, source_colour), unit(3, 2))
        alpha_functional = concatenate(alpha, zero(3), zero(3))
        beta_functionals = tuple(
            concatenate(zero(3), beta, zero(3)) for beta in beta_basis
        )
        assert dot(alpha, x) == 0 and alpha[2] == 0
        assert all(dot(beta, y) == 0 for beta in beta_basis)

        r_alpha = transpose_row(alpha_functional)
        p_plane = tuple(transpose_row(functional) for functional in beta_functionals)
        assert any(r_alpha)
        assert column_rank(p_plane) == 2
        assert in_span(r_alpha, q_image)
        assert all(in_span(row, q_image) for row in p_plane)

        # S2CF (7): target coefficient alpha_k beta_k and correction
        # coefficient lambda alpha_2 beta_2 both vanish for every one of the
        # six beta/k cells.  Hence this independent p-plane lies in the
        # radical of the nonzero row r_alpha.
        coefficients = []
        for beta, k in product(reversed(beta_basis), reversed(range(3))):
            target_coefficient = alpha[k] * beta[k]
            correction_coefficient = lam * alpha[2] * beta[2]
            coefficients.append((target_coefficient, correction_coefficient))
            assert target_coefficient == correction_coefficient == 0
        assert len(coefficients) == 6


def permutation_sign(permutation: tuple[int, ...]) -> Q:
    inversions = sum(
        int(permutation[left] > permutation[right])
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return Q(-1 if inversions % 2 else 1)


def pure_source(block: int, index: int) -> Vector:
    return unit(9, 3 * block + index)


def source_position(triple: tuple[int, int, int]) -> int:
    return SOURCE_TRIPLES.index(triple)


def alternating_separated(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = [Q(0) for _ in SOURCE_TRIPLES]
    for permutation in REVERSED_PERMUTATIONS:
        sign = permutation_sign(permutation)
        left = rows[permutation[0]][:3]
        middle = rows[permutation[1]][3:6]
        right = rows[permutation[2]][6:9]
        for i, j, k in SOURCE_TRIPLES:
            result[source_position((i, j, k))] += (
                sign * left[i] * middle[j] * right[k]
            )
    return tuple(result)


def determinant_three(matrix: tuple[tuple[Q, Q, Q], ...]) -> Q:
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def check_alternating_interface() -> None:
    # Full sensor supplies Alt(Q)!=0 analytically.  This exact replay checks
    # the separated determinant and its basis-change law, the interface used
    # when Q=H^T(N^perp) has dimension three.
    q_basis = pure_source(0, 0), pure_source(1, 0), pure_source(2, 0)
    alternating = alternating_separated(*q_basis)
    assert any(alternating)

    change = (
        (Q(2), Q(1), Q(0)),
        (Q(0), Q(-1), Q(1)),
        (Q(1), Q(0), Q(1)),
    )
    determinant = determinant_three(change)
    assert determinant
    changed_basis = tuple(
        add(*(scale(change[row][column], q_basis[column]) for column in range(3)))
        for row in reversed(range(3))
    )
    # The reversed row traversal reverses the new basis once, contributing
    # the sign of that reversal in addition to det(change).
    reversal_sign = Q(-1)
    assert alternating_separated(*changed_basis) == scale(
        reversal_sign * determinant,
        alternating,
    )


def main() -> None:
    check_boolean_visibility_cover()
    check_endpoint_rank_and_radical_interface()
    check_alternating_interface()
    print("all allowed support masks: zero-visible iff (e0,e1) or (e1,e0): PASS")
    print("rank-eight kernel and rank-four/three-space incidence interface: PASS")
    print("all 12 corrected-cube cells force a two-dimensional radical: PASS")
    print("full-sensor alternating determinant interface and basis law: PASS")
    print("analytic radical-line impossibility remains owned by S2CG")
    print("scope: S2CF zero-visible wall only; one-visible walls remain open")


if __name__ == "__main__":
    main()
