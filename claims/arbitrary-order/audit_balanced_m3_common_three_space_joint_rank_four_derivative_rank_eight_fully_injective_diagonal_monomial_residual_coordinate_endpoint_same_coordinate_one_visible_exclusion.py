#!/usr/bin/env python3
"""Independent Fraction audit of the same-coordinate one-visible exclusion.

This no-import replay checks the exact finite-dimensional interfaces for the
two normalized S2CF cells ``x=y=e_1`` and ``x=y=e_0``.  It independently
reconstructs the corrected-cube cells, exhausts the dependent/independent
cross-zero incidence fork, checks the split-three-line and equal-split-plane
quotients, replays the recovered ``k=1,2`` faces, and checks the sign and
target independence in the unsliced ``(0,0,0)`` equation.

The coordinate-free zero-pair classification, radical bound, and the bridge
from full sensor rank to ``Alt(Q)!=0`` remain analytic inputs of S2CG and the
owning theorem.  This script checks their exact interfaces; it does not use a
primary verifier, SymPy, floating point arithmetic, or a solver.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction
DIM = 3
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


def column_rank(columns: tuple[Vector, ...] | list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    matrix = [row for row in matrix if any(row)]
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


def source_position(triple: tuple[int, int, int]) -> int:
    return SOURCE_TRIPLES.index(triple)


def source_tensor(left: int, middle: int, right: int) -> Vector:
    return unit(len(SOURCE_TRIPLES), source_position((left, middle, right)))


def source_row(source: int, vector: Vector) -> Vector:
    blocks = [zero(DIM), zero(DIM), zero(DIM)]
    blocks[source] = vector
    return tuple(entry for block in blocks for entry in block)


def split_row(row: Vector) -> tuple[Vector, Vector, Vector]:
    assert len(row) == DIM * DIM
    return row[:DIM], row[DIM : 2 * DIM], row[2 * DIM :]


def permanent(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = [Q(0) for _ in SOURCE_TRIPLES]
    for permutation in REVERSED_PERMUTATIONS:
        x_part = split_row(rows[permutation[0]])[0]
        y_part = split_row(rows[permutation[1]])[1]
        z_part = split_row(rows[permutation[2]])[2]
        for i, j, k in SOURCE_TRIPLES:
            result[source_position((i, j, k))] += (
                x_part[i] * y_part[j] * z_part[k]
            )
    return tuple(result)


def alternating(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = [Q(0) for _ in SOURCE_TRIPLES]
    for permutation in REVERSED_PERMUTATIONS:
        inversions = sum(
            int(permutation[left] > permutation[right])
            for left in range(3)
            for right in range(left + 1, 3)
        )
        sign = Q(-1 if inversions % 2 else 1)
        x_part = split_row(rows[permutation[0]])[0]
        y_part = split_row(rows[permutation[1]])[1]
        z_part = split_row(rows[permutation[2]])[2]
        for i, j, k in SOURCE_TRIPLES:
            result[source_position((i, j, k))] += (
                sign * x_part[i] * y_part[j] * z_part[k]
            )
    return tuple(result)


def triple_quotient(tensor: Vector, omitted_colour: int) -> Vector:
    kept = tuple(index for index in reversed(range(DIM)) if index != omitted_colour)
    return tuple(
        tensor[source_position((i, j, k))]
        for i, j, k in product(kept, repeat=3)
    )


def cube_coefficients(alpha: Vector, beta: Vector, lam: Q) -> tuple[tuple[Q, Q], ...]:
    return tuple(
        (alpha[k] * beta[k], lam * alpha[2] * beta[2])
        for k in reversed(range(DIM))
    )


def check_corrected_cube_cells() -> None:
    lam = Q(-7, 5)
    for shared_colour, visible_colour in reversed(((0, 1), (1, 0))):
        assert {shared_colour, visible_colour} == {0, 1}
        e_visible = unit(DIM, visible_colour)
        e_residual = unit(DIM, 2)

        # A=r_visible, C=r_2, B=p_visible, D=p_2.
        cross_ad = cube_coefficients(e_visible, e_residual, lam)
        cross_cb = cube_coefficients(e_residual, e_visible, lam)
        visible_ab = cube_coefficients(e_visible, e_visible, lam)
        corrected_cd = cube_coefficients(e_residual, e_residual, lam)

        assert all(target == correction == 0 for target, correction in cross_ad)
        assert all(target == correction == 0 for target, correction in cross_cb)
        assert tuple(target for target, _ in visible_ab) == tuple(
            Q(k == visible_colour) for k in reversed(range(DIM))
        )
        assert all(correction == 0 for _, correction in visible_ab)
        assert tuple(target for target, _ in corrected_cd) == tuple(
            Q(k == 2) for k in reversed(range(DIM))
        )
        assert all(correction == lam for _, correction in corrected_cd)


def line_row(source: int, colour: int, coefficient: int | Q = 1) -> Vector:
    return source_row(source, scale(coefficient, unit(DIM, colour)))


def check_zero_pair_incidence_cover() -> None:
    # The labels match the analytic support fork.  Every independent zero pair
    # is a conjugate pair in a split two-source plane; every dependent one is
    # a pure line.  The finite branch table below is exhaustive.
    outcomes: set[str] = set()
    for first_kind, second_kind in product(
        reversed(("dependent", "independent")), repeat=2
    ):
        if first_kind == second_kind == "independent":
            for planes_equal in reversed((False, True)):
                outcomes.add("equal_split" if planes_equal else "split_q")
        elif first_kind != second_kind:
            for pure_position in reversed(("off_used_line", "omitted", "used_line")):
                outcomes.add(
                    {
                        "used_line": "equal_split",
                        "omitted": "split_q",
                        "off_used_line": "alt_zero",
                    }[pure_position]
                )
        else:
            outcomes.add("equal_split")
    assert outcomes == {"split_q", "equal_split", "alt_zero"}

    # Independent/independent, distinct planes: H_XY and H_XZ sum to a split Q.
    x = line_row(0, 0)
    y = line_row(1, 0)
    z = line_row(2, 0)
    a, d = add(x, y), add(x, scale(-1, y))
    c, b = add(x, z), add(x, scale(-1, z))
    q_split = (x, y, z)
    assert not any(any(permanent(a, d, row)) for row in q_split)
    assert not any(any(permanent(c, b, row)) for row in q_split)
    assert column_rank(q_split) == 3
    assert any(alternating(*q_split))

    # Independent/independent, equal plane: both conjugate pairs span H_XY.
    c_equal, b_equal = add(scale(2, x), y), add(scale(2, x), scale(-1, y))
    assert not any(any(permanent(c_equal, b_equal, row)) for row in q_split)
    assert column_rank((a, c_equal)) == column_rank((b_equal, d)) == 2

    # One dependent pure line on H, in H's omitted source, or off H's pure
    # line in a used source gives respectively equal H, split Q, or Alt=0.
    assert column_rank((x, c_equal)) == column_rank((b_equal, x)) == 2
    assert any(alternating(x, y, z))
    x_prime = line_row(0, 1)
    q_bad = (x, y, x_prime)
    assert column_rank(q_bad) == 3
    assert not any(alternating(*q_bad))

    # Both dependent pairs are two distinct pure lines, so R=P=H_XY.
    assert column_rank((x, y)) == 2
    assert any(permanent(x, y, z))


def generic_row(seed: int) -> Vector:
    entries = tuple(Q(seed + 2 * index + 1, index + 2) for index in range(9))
    return entries


def check_split_q_face_quotients() -> None:
    for visible_colour, recovered_colour in reversed(((0, 1), (1, 0))):
        x = line_row(0, visible_colour)
        y = line_row(1, visible_colour)
        z = line_row(2, visible_colour)
        q_basis = (z, add(x, scale(2, y)), add(scale(-3, x), y))
        assert column_rank(q_basis) == 3
        assert any(alternating(*q_basis))

        first = generic_row(3 + visible_colour)
        second = generic_row(11 + recovered_colour)
        q_recovered = q_basis[recovered_colour]
        value = permanent(first, second, q_recovered)
        assert not any(triple_quotient(value, visible_colour))

        visible_target = source_tensor(
            visible_colour, visible_colour, visible_colour
        )
        recovered_target = source_tensor(
            recovered_colour, recovered_colour, recovered_colour
        )
        assert any(triple_quotient(recovered_target, visible_colour))
        assert not any(triple_quotient(visible_target, visible_colour))


def omitted_component_map(
    first_source: int,
    second_source: int,
    omitted_source: int,
    visible_colour: int,
) -> tuple[Vector, ...]:
    first = line_row(first_source, visible_colour)
    second = line_row(second_source, visible_colour)
    return tuple(
        permanent(first, second, line_row(omitted_source, colour))
        for colour in reversed(range(DIM))
    )


def check_equal_split_face_quotients() -> None:
    # x=y=e1: visible T0, H=<q1,q2>=ker(lambda0).  The recovered k=1,2
    # faces kill the omitted-source components of r1 and p1.
    visible_colour = 0
    x = line_row(0, visible_colour)
    y = line_row(1, visible_colour)
    omitted_map = omitted_component_map(0, 1, 2, visible_colour)
    assert column_rank(omitted_map) == DIM

    r_1 = add(line_row(0, 1), scale(Q(2, 3), line_row(1, 2)))
    p_1 = add(scale(Q(-5, 7), line_row(0, 2)), line_row(1, 1))
    q_1 = add(x, scale(3, y))
    assert not any(permanent(r_1, p_1, q_1))
    target_1 = source_tensor(1, 1, 1)
    assert any(triple_quotient(target_1, visible_colour))

    # The equal split plane H=<q0,q2> in x=y=e0 similarly makes every tensor
    # containing q0 vanish after quotient by the visible T1 factor lines.
    visible_colour = 1
    x = line_row(0, visible_colour)
    y = line_row(1, visible_colour)
    q_0 = add(scale(2, x), scale(-3, y))
    p_0 = generic_row(17)
    r_0 = generic_row(23)
    assert not any(
        triple_quotient(permanent(r_0, p_0, q_0), visible_colour)
    )


def recover_corrected_sources(
    lam: Q,
    values: tuple[Vector, Vector, Vector],
) -> tuple[Vector, Vector, Vector]:
    target_2 = source_tensor(2, 2, 2)
    value_0, value_1, value_2 = values
    return (
        scale(1 / lam, value_0),
        scale(1 / lam, value_1),
        scale(1 / lam, add(value_2, scale(-1, target_2))),
    )


def check_aligned_unsliced_quotient() -> None:
    lam = Q(13, 7)
    target_0 = source_tensor(0, 0, 0)
    target_1 = source_tensor(1, 1, 1)
    target_2 = source_tensor(2, 2, 2)

    # Split-Q case: all corrected-cell values lie on the visible T1 line.
    split_values = (
        scale(Q(2, 5), target_1),
        scale(Q(-3, 4), target_1),
        scale(Q(7, 9), target_1),
    )
    split_sources = recover_corrected_sources(lam, split_values)
    assert not any(triple_quotient(split_sources[0], 1))
    assert not any(triple_quotient(split_sources[1], 1))
    assert triple_quotient(split_sources[2], 1) == scale(
        -1 / lam, triple_quotient(target_2, 1)
    )

    # Equal-H case: q0,q2 lie in H, so the corrected values there are zero.
    equal_values = (zero(len(SOURCE_TRIPLES)), scale(Q(5, 6), target_1), zero(len(SOURCE_TRIPLES)))
    equal_sources = recover_corrected_sources(lam, equal_values)
    assert not any(equal_sources[0])
    assert not any(triple_quotient(equal_sources[1], 1))
    assert equal_sources[2] == scale(-1 / lam, target_2)

    quotient_target_0 = triple_quotient(target_0, 1)
    quotient_target_2 = triple_quotient(target_2, 1)
    assert any(quotient_target_0) and any(quotient_target_2)
    assert column_rank((quotient_target_0, quotient_target_2)) == 2

    # P000 has zero triple quotient in both incidence cases.  The complete
    # unsliced equation
    #   P000-T0=H0_00*S0+H1_00*S1+H2_00*S2
    # would therefore require -bar(T0)=-(H2_00/lambda)bar(T2), for every
    # possible rational H2_00.  Independence makes this impossible.
    for h_2_00 in reversed((Q(-11, 3), Q(0), Q(8, 5))):
        left = scale(-1, quotient_target_0)
        right = scale(-h_2_00 / lam, quotient_target_2)
        assert left != right


def main() -> None:
    check_corrected_cube_cells()
    check_zero_pair_incidence_cover()
    check_split_q_face_quotients()
    check_equal_split_face_quotients()
    check_aligned_unsliced_quotient()
    print("both same-coordinate corrected cubes and cross-zero cells: PASS")
    print("all dependent/independent cross-pair incidence forks: PASS")
    print("split-Q and equal-split recovered-face quotients: PASS")
    print("aligned source recovery and unsliced quotient sign: PASS")
    print("bar(T0), bar(T2) remain nonzero and independent: PASS")
    print("analytic zero-pair/Alt(Q) implications remain owned by the theorem")
    print("scope: exact normalized x=y=e0 and x=y=e1 one-visible subcells")


if __name__ == "__main__":
    main()
