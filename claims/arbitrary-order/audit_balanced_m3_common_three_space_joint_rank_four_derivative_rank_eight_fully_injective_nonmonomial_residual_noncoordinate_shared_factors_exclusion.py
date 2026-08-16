#!/usr/bin/env python3
"""Independent Fraction audit of the S2CN noncoordinate exclusion.

This standard-library-only audit reverses the support, source, and incidence
traversals used by the primary checker.  It reconstructs the singleton
kernel gate and one-sided target table, uses separate exact permanent
fixtures for both independent zero-pair incidences, checks the dependent
one-factor slabs and proportional restricted coordinate forms, manufactures
the opposite structural corner in every colour order, replays both two-cross
incidence outcomes, and checks every allowed retained-face sign.

S2BQ's exhaustive tangent-quotient atlas, S2CG's zero-pair classification,
S2CI's exhaustive two-cross incidence dichotomy, and S2CK's mixed-map
obstruction remain analytic inputs of the owning theorem.  This audit checks
their exact finite algebraic interfaces; it imports no primary verifier,
SymPy, or solver.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction
DIM = 3
COLOURS = tuple(reversed(range(DIM)))
MASKS = tuple(reversed(range(1, 1 << DIM)))
NONCOORDINATE_MASKS = tuple(
    mask for mask in MASKS if (mask & (mask - 1)) != 0
)
ROW_PERMUTATIONS = tuple(reversed(tuple(permutations(range(DIM)))))
SOURCE_PERMUTATIONS = tuple(reversed(tuple(permutations(range(DIM)))))

Vector = tuple[Q, ...]
Matrix = tuple[Q, ...]


def zero(size: int) -> Vector:
    return (Q(0),) * size


def unit(size: int, index: int) -> Vector:
    return tuple(Q(candidate == index) for candidate in range(size))


def add(*vectors: Vector) -> Vector:
    assert vectors
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(scalar: int | Q, vector: Vector) -> Vector:
    coefficient = Q(scalar)
    return tuple(coefficient * entry for entry in vector)


def dot(left: Vector, right: Vector) -> Q:
    return sum(
        (first * second for first, second in zip(left, right, strict=True)),
        Q(0),
    )


def support(vector: Vector) -> tuple[int, ...]:
    return tuple(index for index, entry in enumerate(vector) if entry)


def mask_support(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(DIM) if mask & (1 << index))


def representative(mask: int, side: str) -> Vector:
    weights = {
        "x": (Q(7), Q(-11), Q(13)),
        "y": (Q(-17), Q(19), Q(23)),
    }[side]
    result = tuple(
        weights[index] if mask & (1 << index) else Q(0)
        for index in range(DIM)
    )
    assert support(result) == mask_support(mask)
    return result


def complement(index: int) -> tuple[int, int]:
    result = tuple(candidate for candidate in range(DIM) if candidate != index)
    assert len(result) == 2
    return result[0], result[1]


def boundary_covector(root: Vector, omitted: int) -> Vector:
    """Return a nonzero vector in root^perp with omitted coordinate zero."""
    first, second = complement(omitted)
    result = [Q(0)] * DIM
    result[first] = root[second]
    result[second] = -root[first]
    value = tuple(result)
    assert any(value)
    assert value[omitted] == 0
    assert dot(value, root) == 0
    return value


def two_visible_partner(root: Vector, first: int, second: int) -> Vector:
    """Choose beta in root^perp nonzero at both named coordinates."""
    third = next(
        colour for colour in range(DIM) if colour not in {first, second}
    )
    result = [Q(0)] * DIM
    if root[third]:
        result[first] = Q(2)
        result[second] = Q(-3)
        result[third] = -(
            result[first] * root[first] + result[second] * root[second]
        ) / root[third]
    else:
        assert root[first] and root[second]
        result[first] = root[second]
        result[second] = -root[first]
    value = tuple(result)
    assert dot(value, root) == 0
    assert value[first] and value[second]
    return value


def off_kernel_covector(root: Vector, coordinate: int) -> Vector:
    """Choose b in root^perp with b_coordinate nonzero."""
    partner = next(
        candidate
        for candidate in reversed(range(DIM))
        if candidate != coordinate and root[candidate]
    )
    result = [Q(0)] * DIM
    result[coordinate] = root[partner]
    result[partner] = -root[coordinate]
    value = tuple(result)
    assert dot(value, root) == 0
    assert value[coordinate]
    return value


def target_coefficients(alpha: Vector, beta: Vector) -> Vector:
    return tuple(alpha[colour] * beta[colour] for colour in range(DIM))


def quotient_correction(
    alpha: Vector,
    beta: Vector,
    d: int,
    e: int,
    coefficient: int | Q = 1,
) -> Q:
    return Q(coefficient) * alpha[d] * beta[e]


def column_rank(columns: tuple[Vector, ...]) -> int:
    if not columns:
        return 0
    row_count = len(columns[0])
    assert all(len(column) == row_count for column in columns)
    matrix = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in reversed(range(len(columns))):
        pivot = next(
            (
                row
                for row in reversed(range(pivot_row, row_count))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for row in reversed(range(row_count)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def perpendicular_basis(root: Vector) -> tuple[Vector, Vector]:
    pivot = next(index for index in reversed(range(DIM)) if root[index])
    basis: list[Vector] = []
    for index in reversed(tuple(i for i in range(DIM) if i != pivot)):
        value = [Q(0)] * DIM
        value[index] = root[pivot]
        value[pivot] = -root[index]
        basis.append(tuple(value))
    result = basis[0], basis[1]
    assert column_rank(result) == 2
    assert all(dot(root, vector) == 0 for vector in result)
    return result


def restricted_evaluation(root: Vector, coordinate: int) -> Vector:
    return tuple(vector[coordinate] for vector in perpendicular_basis(root))


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(first * second for first in left for second in right)


def proportional(left: Vector, right: Vector) -> bool:
    assert any(left) and any(right) and len(left) == len(right)
    return all(
        left[first] * right[second] == left[second] * right[first]
        for first in range(len(left))
        for second in range(first)
    )


def check_singleton_kernel_gate() -> tuple[int, int, tuple[tuple[int, int, int], ...]]:
    singleton_records: list[tuple[int, int, int]] = []
    secant_count = 0
    for d in COLOURS:
        for x_mask in NONCOORDINATE_MASKS:
            x = representative(x_mask, "x")
            alpha = boundary_covector(x, d)
            alpha_support = support(alpha)
            if len(alpha_support) == 1:
                a = alpha_support[0]
                assert a != d
                assert x_mask == sum(1 << colour for colour in complement(a))
                singleton_records.append((x_mask, d, a))
                continue

            assert alpha_support == complement(d)
            first, second = alpha_support
            for y_mask in NONCOORDINATE_MASKS:
                y = representative(y_mask, "y")
                beta = two_visible_partner(y, first, second)
                for e in COLOURS:
                    assert quotient_correction(alpha, beta, d, e) == 0
                    coefficients = target_coefficients(alpha, beta)
                    assert coefficients[first] and coefficients[second]
                    assert coefficients[d] == 0
                    secant_count += 1

    records = tuple(reversed(singleton_records))
    assert len(records) == 6
    assert secant_count == 72
    return len(records), secant_count, records


def check_one_sided_tables(
    singleton_records: tuple[tuple[int, int, int], ...],
) -> int:
    table_count = 0
    for x_mask, d, a in reversed(singleton_records):
        x = representative(x_mask, "x")
        alpha = unit(DIM, a)
        assert dot(alpha, x) == 0 and alpha[d] == 0
        for y_mask in NONCOORDINATE_MASKS:
            y = representative(y_mask, "y")
            beta = boundary_covector(y, a)
            b = off_kernel_covector(y, a)
            assert beta[a] == 0 and b[a]
            assert column_rank((beta, b)) == 2
            for e in COLOURS:
                assert quotient_correction(alpha, beta, d, e) == 0
                assert not any(target_coefficients(alpha, beta))
                assert quotient_correction(alpha, b, d, e) == 0
                visible = target_coefficients(alpha, b)
                assert visible[a] == b[a]
                assert all(
                    not visible[colour]
                    for colour in range(DIM)
                    if colour != a
                )
                for beta_probe in (
                    b,
                    add(scale(Q(-5, 3), b), scale(Q(7, 4), beta)),
                    add(b, scale(Q(-11, 6), beta)),
                ):
                    assert quotient_correction(alpha, beta_probe, d, e) == 0
                    probe = target_coefficients(alpha, beta_probe)
                    assert all(
                        not probe[colour]
                        for colour in range(DIM)
                        if colour != a
                    )
                table_count += 1
    assert table_count == 72
    return table_count


SOURCE_DIM = 2
TENSOR_DIM = SOURCE_DIM**DIM


def source_row(*blocks: Vector) -> Vector:
    assert len(blocks) == DIM
    assert all(len(block) == SOURCE_DIM for block in blocks)
    return tuple(entry for block in blocks for entry in block)


def row_blocks(value: Vector) -> tuple[Vector, Vector, Vector]:
    assert len(value) == DIM * SOURCE_DIM
    return (
        value[:SOURCE_DIM],
        value[SOURCE_DIM : 2 * SOURCE_DIM],
        value[2 * SOURCE_DIM :],
    )


def permute_sources(value: Vector, permutation: tuple[int, int, int]) -> Vector:
    blocks = row_blocks(value)
    return source_row(*(blocks[index] for index in permutation))


def tensor_position(index: tuple[int, int, int]) -> int:
    return (index[0] * SOURCE_DIM + index[1]) * SOURCE_DIM + index[2]


def tensor_product(first: Vector, second: Vector, third: Vector) -> Vector:
    result = [Q(0)] * TENSOR_DIM
    for i, j, k in product(range(SOURCE_DIM), repeat=DIM):
        result[tensor_position((i, j, k))] = first[i] * second[j] * third[k]
    return tuple(result)


def permanent(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = zero(TENSOR_DIM)
    for permutation in ROW_PERMUTATIONS:
        term = tensor_product(
            row_blocks(rows[permutation[0]])[0],
            row_blocks(rows[permutation[1]])[1],
            row_blocks(rows[permutation[2]])[2],
        )
        result = add(result, term)
    return result


def permutation_sign(permutation: tuple[int, int, int]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(DIM)
        for right in range(left + 1, DIM)
    )
    return -1 if inversions % 2 else 1


def alternating(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = zero(TENSOR_DIM)
    for permutation in ROW_PERMUTATIONS:
        term = tensor_product(
            row_blocks(rows[permutation[0]])[0],
            row_blocks(rows[permutation[1]])[1],
            row_blocks(rows[permutation[2]])[2],
        )
        result = add(result, scale(permutation_sign(permutation), term))
    return result


def pure_source(source: int, coordinate: int = 0) -> Vector:
    blocks = [zero(SOURCE_DIM) for _ in range(DIM)]
    blocks[source] = unit(SOURCE_DIM, coordinate)
    return source_row(*blocks)


def quotient_target_scalar(value: Vector) -> Q:
    """Quotient every source by its coordinate-zero factor line."""
    return value[tensor_position((1, 1, 1))]


def deterministic_rows(seed: int) -> tuple[Vector, ...]:
    return tuple(
        tuple(Q(seed + 7 * row - 3 * index, 5 + index) for index in range(6))
        for row in reversed(range(DIM))
    )


def check_independent_incidence_fixtures() -> int:
    base_x = pure_source(0)
    base_y = pure_source(1)
    base_z = pure_source(2)
    arbitrary_first = deterministic_rows(11)
    arbitrary_second = deterministic_rows(-13)
    fixture_count = 0

    for source_permutation in SOURCE_PERMUTATIONS:
        x, y, z = (
            permute_sources(row_value, source_permutation)
            for row_value in (base_x, base_y, base_z)
        )
        u = add(x, y)
        v = add(x, scale(-1, y))
        assert any(alternating(x, y, z))
        for q in reversed((x, y, z)):
            assert not any(permanent(u, v, q))

        # Equal-plane fixture: P=H and the visible map has kernel H.
        equal_b = u
        equal_map = tuple(permanent(u, equal_b, q) for q in (x, y, z))
        assert not any(equal_map[0]) and not any(equal_map[1])
        assert equal_map[2] == scale(2, tensor_product(
            unit(SOURCE_DIM, 0),
            unit(SOURCE_DIM, 0),
            unit(SOURCE_DIM, 0),
        ))
        q_equal = add(x, scale(Q(-3, 2), y))
        for first, second in reversed(
            tuple(product(arbitrary_first, arbitrary_second))
        ):
            assert quotient_target_scalar(permanent(first, second, q_equal)) == 0

        # Split-Q fixture: B is the omitted pure row and every q is a sum
        # of the three aligned source lines.
        split_map = tuple(permanent(u, z, q) for q in (x, y, z))
        assert any(split_map[0]) and any(split_map[1])
        assert not any(split_map[2])
        q_split = add(scale(2, x), scale(-3, y), scale(5, z))
        for first, second in reversed(
            tuple(product(arbitrary_second, arbitrary_first))
        ):
            assert quotient_target_scalar(permanent(first, second, q_split)) == 0
        fixture_count += 2

    assert fixture_count == 12
    return fixture_count


def slab_component_zero(value: Vector, source: int) -> bool:
    return all(
        not value[tensor_position(index)]
        for index in product(range(SOURCE_DIM), repeat=DIM)
        if index[source] == 1
    )


def check_dependent_one_factor_slabs() -> int:
    base_x = pure_source(0)
    base_y = pure_source(1)
    base_z = pure_source(2)
    second_y = pure_source(1, 1)
    second_x = pure_source(0, 1)
    case_count = 0

    base_cases = (
        # B_Y!=0, B_Z=0; Q has fixed Z projection.
        (base_y, (base_x, base_y, add(second_x, second_y, base_z)), 2),
        # B_Y=0, B_Z!=0; Q has fixed Y projection.
        (base_z, (base_x, base_z, add(second_x, base_y, pure_source(2, 1))), 1),
        # Both components survive and both projections are fixed.
        (
            add(base_y, base_z),
            (
                base_x,
                add(base_y, base_z),
                add(second_x, scale(2, base_y), scale(3, base_z)),
            ),
            2,
        ),
    )

    for source_permutation in SOURCE_PERMUTATIONS:
        for base_b, base_q, slab_source in reversed(base_cases):
            u = permute_sources(base_x, source_permutation)
            b_row = permute_sources(base_b, source_permutation)
            q_rows = tuple(
                permute_sources(value, source_permutation) for value in base_q
            )
            permuted_slab = source_permutation.index(slab_source)
            assert column_rank(q_rows) == 3
            assert any(alternating(*q_rows))
            values = tuple(permanent(u, b_row, q) for q in q_rows)
            assert any(any(value) for value in values)
            assert all(slab_component_zero(value, permuted_slab) for value in values)
            for rows in reversed(tuple(product(q_rows, repeat=3))):
                assert slab_component_zero(permanent(*rows), permuted_slab)
            case_count += 1

    assert case_count == 18
    return case_count


def check_proportional_forms_and_support_recovery() -> tuple[int, int]:
    checked = 0
    recovered = 0
    for a in COLOURS:
        i, j = complement(a)
        x_mask = (1 << i) | (1 << j)
        x = representative(x_mask, "x")
        for y_mask in NONCOORDINATE_MASKS:
            y = representative(y_mask, "y")
            b_i = outer(
                restricted_evaluation(x, i),
                restricted_evaluation(y, i),
            )
            b_j = outer(
                restricted_evaluation(x, j),
                restricted_evaluation(y, j),
            )
            expected = y_mask == x_mask
            assert proportional(b_i, b_j) == expected
            recovered += int(expected)
            checked += 1

    assert checked == 12 and recovered == 3

    # Independent exact simple-tensor fixtures for b=c*C and S=-c*T.
    correction = (Q(2), Q(-3), Q(5), Q(7))
    target_bar = (Q(11), Q(-13))
    for coefficient in reversed((Q(-7, 3), Q(5, 2), Q(9, 4))):
        bilinear = scale(coefficient, correction)
        source_bar = scale(-coefficient, target_bar)
        left = tuple(entry * value for entry in bilinear for value in target_bar)
        right = tuple(entry * value for entry in correction for value in source_bar)
        assert add(left, right) == zero(len(left))
        assert scale(1 / coefficient, bilinear) == correction
        assert source_bar == scale(-coefficient, target_bar)
    return checked, recovered


def check_manufactured_opposite_corners() -> int:
    checked = 0
    for a, i, j in reversed(tuple(permutations(range(DIM)))):
        x = representative((1 << i) | (1 << j), "x")
        y = representative((1 << i) | (1 << j), "y")
        alpha = boundary_covector(x, a)
        beta = boundary_covector(y, a)
        singleton = unit(DIM, a)
        assert column_rank((singleton, alpha)) == 2
        assert column_rank((beta, singleton)) == 2
        for d, e in reversed(tuple(product((i, j), repeat=2))):
            # Original shore, manufactured opposite shore, and visible
            # diagonal corner have separately vanishing quotient corrections.
            assert quotient_correction(singleton, beta, d, e) == 0
            assert quotient_correction(alpha, singleton, d, e) == 0
            assert quotient_correction(singleton, singleton, d, e) == 0
            assert not any(target_coefficients(singleton, beta))
            assert not any(target_coefficients(alpha, singleton))
            assert target_coefficients(singleton, singleton) == singleton

        shift = Q(-5, 7)
        off_kernel = add(singleton, scale(shift, beta))
        assert off_kernel[a] == 1
        assert add(singleton, scale(shift, beta)) == off_kernel
        checked += 1

    assert checked == 6
    return checked


def check_two_cross_incidence_fixtures() -> int:
    base_x = pure_source(0)
    base_y = pure_source(1)
    base_z = pure_source(2)
    arbitrary_first = deterministic_rows(29)
    arbitrary_second = deterministic_rows(-31)
    checked = 0

    for source_permutation in SOURCE_PERMUTATIONS:
        x, y, z = (
            permute_sources(value, source_permutation)
            for value in (base_x, base_y, base_z)
        )

        # Split-Q fork: zero corners (u,u) and (A,p_a), visible (u,p_a).
        u = x
        a_row = add(y, z)
        p_a = add(y, scale(-1, z))
        q_rows = (z, y, x)
        assert column_rank((u, a_row)) == 2
        assert column_rank((p_a, u)) == 2
        assert any(alternating(*q_rows))
        for q in reversed(q_rows):
            assert not any(permanent(u, u, q))
            assert not any(permanent(a_row, p_a, q))
        assert any(any(permanent(u, p_a, q)) for q in q_rows)
        q_split = add(x, scale(2, y), scale(-3, z))
        for first, second in reversed(
            tuple(product(arbitrary_first, arbitrary_second))
        ):
            assert quotient_target_scalar(permanent(first, second, q_split)) == 0

        # Equal split-plane fork: R=P=span(x,y), ker(lambda_a)=H.
        a_equal = y
        p_equal = y
        q_equal_rows = (z, add(x, y), add(x, scale(-1, y)))
        assert column_rank((u, a_equal)) == 2
        assert column_rank((p_equal, u)) == 2
        assert any(alternating(*q_equal_rows))
        for q in reversed(q_equal_rows):
            assert not any(permanent(u, u, q))
            assert not any(permanent(a_equal, p_equal, q))
        visible = tuple(permanent(u, p_equal, q) for q in q_equal_rows)
        assert any(visible[0])
        assert not any(visible[1]) and not any(visible[2])
        q_equal = q_equal_rows[1]
        for first, second in reversed(
            tuple(product(arbitrary_second, arbitrary_first))
        ):
            assert quotient_target_scalar(permanent(first, second, q_equal)) == 0
        checked += 2

    assert checked == 12
    return checked


def matrix_unit(row: int, column: int) -> Matrix:
    return unit(DIM * DIM, DIM * row + column)


def check_retained_face_signs() -> int:
    checked = 0
    target_bar = (Q(2), Q(-5), Q(7))
    for a in COLOURS:
        for tangent_colour in COLOURS:
            retained_colours = tuple(
                colour
                for colour in COLOURS
                if colour != a and colour != tangent_colour
            )
            for retained in reversed(retained_colours):
                coefficient = Q(3 + a + 2 * tangent_colour + retained, 5)
                diagonal = matrix_unit(retained, retained)
                residual = scale(1 / coefficient, diagonal)
                source_bar = scale(-coefficient, target_bar)
                left = tuple(
                    entry * value
                    for entry in scale(-1, diagonal)
                    for value in target_bar
                )
                right = tuple(
                    entry * value
                    for entry in residual
                    for value in source_bar
                )
                assert left == right
                assert residual == scale(1 / coefficient, diagonal)

                perturbation = matrix_unit(
                    (retained + 1) % DIM,
                    retained,
                )
                nonmonomial = add(residual, perturbation)
                wrong = tuple(
                    entry * value
                    for entry in nonmonomial
                    for value in source_bar
                )
                assert wrong != left
                assert retained != tangent_colour and retained != a
                checked += 1

    assert checked == 12
    return checked


def main() -> None:
    singleton_count, secant_count, records = check_singleton_kernel_gate()
    table_count = check_one_sided_tables(records)
    independent_count = check_independent_incidence_fixtures()
    slab_count = check_dependent_one_factor_slabs()
    form_count, recovered_count = check_proportional_forms_and_support_recovery()
    corner_count = check_manufactured_opposite_corners()
    incidence_count = check_two_cross_incidence_fixtures()
    retained_count = check_retained_face_signs()

    print(
        "reversed singleton-kernel gate "
        f"singletons={singleton_count}, secants={secant_count}: PASS"
    )
    print(f"one-sided target tables ({table_count} exact tables): PASS")
    print(
        "independent equal/split source fixtures "
        f"({independent_count} source-ordered cases): PASS"
    )
    print(f"dependent one-factor slabs ({slab_count} cases): PASS")
    print(
        "proportional restricted forms/support recovery "
        f"({form_count} checked, {recovered_count} survivors): PASS"
    )
    print(f"manufactured opposite corners ({corner_count} colour orders): PASS")
    print(f"two-cross incidence fixtures ({incidence_count} cases): PASS")
    print(f"retained complete-face signs ({retained_count} choices): PASS")
    print("analytic owners: S2BQ, S2CG, S2CI, and S2CK")
    print("scope: actual-nonmonomial noncoordinate shared-factor cell")


if __name__ == "__main__":
    main()
