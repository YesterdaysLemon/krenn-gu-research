#!/usr/bin/env python3
"""Independent finite-field audit of component nineteen's generic H31 closure.

This audit deliberately imports no project verifier.  It reconstructs the
permanents, exhausts every affine marking at two good finite-field samples,
checks the four residual-line kernel parametrizations, and verifies the
punctured-line and line-intersection minor identities as polynomial identities.
The modular calculations corroborate, but do not imply, the characteristic-zero
theorem.
"""

from __future__ import annotations

import itertools
import json
from collections.abc import Iterable, Sequence

MODULI = (7, 11)
SAMPLES = {
    7: (2, 5, 2),
    11: (2, 3, 2),
}  # (p, q, phi); avoid accidental special fibres in each audit field
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = {size: tuple(itertools.permutations(range(size))) for size in (3, 4)}

# Polynomial variables are ordered (u,a,b,c,r).
NVARIABLES = 5
ZERO_EXPONENT = (0,) * NVARIABLES
Poly = dict[tuple[int, ...], int]


def inv(value: int, modulus: int) -> int:
    return pow(value % modulus, -1, modulus)


def add_rows(*rows: Sequence[int], modulus: int) -> tuple[int, ...]:
    return tuple(sum(row[index] for row in rows) % modulus for index in range(4))


def scale_row(coefficient: int, row: Sequence[int], modulus: int) -> tuple[int, ...]:
    return tuple(coefficient * value % modulus for value in row)


def component_rows(
    modulus: int,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    p, q, phi = (value % modulus for value in SAMPLES[modulus])
    a = (1, 1, 0, 0)
    a_bar = (1, -1 % modulus, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1 % modulus)
    row_zero = add_rows(a_bar, scale_row(p, b, modulus), modulus=modulus)
    row_one = add_rows(b_bar, scale_row(q, b, modulus), modulus=modulus)
    alpha_zero = add_rows(
        scale_row(q - phi, row_zero, modulus),
        scale_row(-p, row_one, modulus),
        modulus=modulus,
    )
    alpha = (alpha_zero, b, b_bar, a_bar)
    canonical_beta = (
        row_zero,
        a,
        a,
        add_rows(b, scale_row(phi, b_bar, modulus), modulus=modulus),
    )
    return alpha, canonical_beta


def shifted_beta(
    alpha: Sequence[Sequence[int]],
    canonical_beta: Sequence[Sequence[int]],
    shifts: Sequence[int],
    modulus: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            (canonical_beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            % modulus
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def permanent_numeric(rows: Sequence[Sequence[int]], modulus: int) -> int:
    size = len(rows)
    return (
        sum(
            product_mod((rows[row][permutation[row]] for row in range(size)), modulus)
            for permutation in PERMUTATIONS[size]
        )
        % modulus
    )


def product_mod(values: Iterable[int], modulus: int) -> int:
    result = 1
    for value in values:
        result = result * value % modulus
    return result


def extension_rows_numeric(
    distinguished: int,
    alpha: Sequence[Sequence[int]],
    beta: Sequence[Sequence[int]],
    modulus: int,
) -> tuple[list[list[int]], list[int], list[int]]:
    retained = tuple(index for index in range(4) if index != distinguished)
    coefficient_rows: dict[tuple[int, ...], list[int]] = {}
    for word in WORDS4:
        selected = tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
        coefficient_row = [0] * 8
        for omitted_mode in range(4):
            three_rows = tuple(
                tuple(selected[mode][coordinate] for coordinate in retained)
                for mode in range(4)
                if mode != omitted_mode
            )
            coefficient = permanent_numeric(three_rows, modulus)
            column = omitted_mode if word[omitted_mode] == 0 else 4 + omitted_mode
            coefficient_row[column] = coefficient
        coefficient_rows[word] = coefficient_row
    mixed = [
        coefficient_rows[word]
        for word in WORDS4
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
    return (
        mixed,
        coefficient_rows[(0, 0, 0, 0)],
        coefficient_rows[(1, 1, 1, 1)],
    )


def one_marked_numeric(
    mode: int,
    alpha: Sequence[Sequence[int]],
    beta: Sequence[Sequence[int]],
    modulus: int,
) -> list[list[int]]:
    result = []
    for word in WORDS3:
        selected: list[Sequence[int] | None] = []
        bit_index = 0
        for other_mode in range(4):
            if other_mode == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other_mode] if word[bit_index] else alpha[other_mode]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            rows = tuple(
                basis if other_mode == mode else selected[other_mode]
                for other_mode in range(4)
            )
            assert all(row is not None for row in rows)
            coefficient_row.append(
                permanent_numeric(rows, modulus)  # type: ignore[arg-type]
            )
        result.append(coefficient_row)
    return result


def rank_mod(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    if not matrix:
        return 0
    work = [[value % modulus for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = inv(work[pivot_row][column], modulus)
        work[pivot_row] = [value * inverse % modulus for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [
                (left - coefficient * right) % modulus
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def row_times_matrix(
    row: Sequence[int], matrix: Sequence[Sequence[int]], modulus: int
) -> list[int]:
    return [
        sum(row[index] * matrix[index][column] for index in range(len(row))) % modulus
        for column in range(len(matrix[0]))
    ]


def matrix_product_zero(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]], modulus: int
) -> bool:
    return all(
        sum(left[row][middle] * right[middle][column] for middle in range(len(right)))
        % modulus
        == 0
        for row in range(len(left))
        for column in range(len(right[0]))
    )


def genuine_binary_projection(modulus: int) -> dict[str, object]:
    p, q, phi = (value % modulus for value in SAMPLES[modulus])
    delta = (q - phi) % modulus
    assert p * q * phi * delta * (phi * q - 1) % modulus
    assert (phi - 1) * (phi + 1) * (q - 1) * (q + 1) % modulus
    alpha, canonical_beta = component_rows(modulus)

    marking_chart_checks = 0
    for mode in range(4):
        canonical_plueckers = tuple(
            (
                alpha[mode][left] * canonical_beta[mode][right]
                - alpha[mode][right] * canonical_beta[mode][left]
            )
            % modulus
            for left, right in itertools.combinations(range(4), 2)
        )
        assert any(canonical_plueckers)
        for shift in range(modulus):
            shifted = tuple(
                (canonical_beta[mode][coordinate] + shift * alpha[mode][coordinate])
                % modulus
                for coordinate in range(4)
            )
            shifted_plueckers = tuple(
                (
                    alpha[mode][left] * shifted[right]
                    - alpha[mode][right] * shifted[left]
                )
                % modulus
                for left, right in itertools.combinations(range(4), 2)
            )
            assert shifted_plueckers == canonical_plueckers
            marking_chart_checks += 1
        # The sole point at infinity has beta proportional to alpha and is not a basis.
        assert rank_mod((alpha[mode], alpha[mode]), modulus) == 1

    pure_support = {}
    for word in WORDS4:
        value = permanent_numeric(
            tuple(
                beta if bit else kernel
                for bit, kernel, beta in zip(word, alpha, canonical_beta, strict=True)
            ),
            modulus,
        )
        if value:
            pure_support["".join(map(str, word))] = value
    assert pure_support == {"1111": 4 * p % modulus}

    observed: dict[int, set[tuple[int, ...]]] = {index: set() for index in range(4)}
    for shifts in itertools.product(range(modulus), repeat=4):
        beta = shifted_beta(alpha, canonical_beta, shifts, modulus)
        for distinguished in range(4):
            mixed, diagonal_alpha, diagonal_beta = extension_rows_numeric(
                distinguished, alpha, beta, modulus
            )
            mixed_rank = rank_mod(mixed, modulus)
            if (
                mixed_rank < 8
                and rank_mod([*mixed, diagonal_alpha], modulus) > mixed_rank
                and rank_mod([*mixed, diagonal_beta], modulus) > mixed_rank
            ):
                observed[distinguished].add(shifts)

    h0 = -inv(delta, modulus) % modulus
    expected_residual = {
        (h0, h1, h2, 0)
        for h1 in range(modulus)
        for h2 in range(modulus)
        if h1 * h2 % modulus == 0
    }
    assert observed[0] == set()
    assert observed[1] == set()
    assert observed[2] == expected_residual
    assert observed[3] == expected_residual
    return {
        "modulus": modulus,
        "sample": {"p": p, "q": q, "phi": phi},
        "pure_support": pure_support,
        "projected_marking_counts": {
            str(index): len(observed[index]) for index in range(4)
        },
        "expected_residual_union_count": 2 * modulus - 1,
        "affine_marking_chart_values_checked": marking_chart_checks,
        "projective_marking_endpoint_is_degenerate": True,
    }


def kernel_parametrization(
    distinguished: int,
    line: int,
    u: int,
    modulus: int,
) -> list[list[int]]:
    p = SAMPLES[modulus][0] % modulus
    zero = [0, 0, 0, 0]
    if (distinguished, line) == (2, 1):
        rows = (
            (0, 0, 0, -p),
            (1, 0, 0, 0),
            (0, 0, 1, 0),
            zero,
            (0, 1, 0, 0),
            zero,
            (u, 0, 0, 0),
            (0, 0, 0, 1),
        )
    elif (distinguished, line) == (2, 2):
        rows = (
            (0, 0, 0, -p),
            (0, 0, 1, 0),
            (1, 0, 0, 0),
            zero,
            (0, 1, 0, 0),
            (u, 0, 0, 0),
            zero,
            (0, 0, 0, 1),
        )
    elif (distinguished, line) == (3, 1):
        rows = (
            (0, 0, 0, p),
            (-1, 0, 0, 0),
            (0, 0, 1, 0),
            zero,
            (0, 1, 0, 0),
            zero,
            (u, 0, 0, 0),
            (0, 0, 0, 1),
        )
    elif (distinguished, line) == (3, 2):
        rows = (
            (0, 0, 0, p),
            (0, 0, 1, 0),
            (-1, 0, 0, 0),
            zero,
            (0, 1, 0, 0),
            (u, 0, 0, 0),
            zero,
            (0, 0, 0, 1),
        )
    else:
        raise AssertionError((distinguished, line))
    return [[value % modulus for value in row] for row in rows]


def expected_diagonal_coefficients(
    distinguished: int, line: int, modulus: int
) -> tuple[list[int], list[int]]:
    p, q, phi = (value % modulus for value in SAMPLES[modulus])
    delta = (q - phi) % modulus
    if distinguished == 2:
        alpha_sign = 1 if line == 1 else -1
        diagonal_alpha = [
            2 * delta * alpha_sign,
            0,
            -2 * delta * alpha_sign,
            0,
        ]
        diagonal_beta = [
            0,
            -2 * (phi - 1),
            0,
            2 * p * (q - 1) * inv(delta, modulus),
        ]
    else:
        diagonal_alpha = [2 * delta, 0, -2 * delta, 0]
        diagonal_beta = [
            0,
            2 * (phi + 1),
            0,
            2 * p * (q + 1) * inv(delta, modulus),
        ]
    return (
        [value % modulus for value in diagonal_alpha],
        [value % modulus for value in diagonal_beta],
    )


def kernel_audit(modulus: int) -> dict[str, object]:
    p, q, phi = (value % modulus for value in SAMPLES[modulus])
    delta = (q - phi) % modulus
    h0 = -inv(delta, modulus) % modulus
    alpha, canonical_beta = component_rows(modulus)
    checked = 0
    transverse_entries: dict[str, int] = {}
    for distinguished in (2, 3):
        for line in (1, 2):
            for u in range(modulus):
                shifts = (h0, 0, u, 0) if line == 1 else (h0, u, 0, 0)
                beta = shifted_beta(alpha, canonical_beta, shifts, modulus)
                mixed, diagonal_alpha, diagonal_beta = extension_rows_numeric(
                    distinguished, alpha, beta, modulus
                )
                kernel = kernel_parametrization(distinguished, line, u, modulus)
                assert rank_mod(mixed, modulus) == 4
                assert rank_mod(kernel, modulus) == 4
                assert matrix_product_zero(mixed, kernel, modulus)
                expected_alpha, expected_beta = expected_diagonal_coefficients(
                    distinguished, line, modulus
                )
                assert (
                    row_times_matrix(diagonal_alpha, kernel, modulus) == expected_alpha
                )
                assert row_times_matrix(diagonal_beta, kernel, modulus) == expected_beta
                marked_mode = 1 if line == 1 else 2
                pure_marked = one_marked_numeric(marked_mode, alpha, beta, modulus)
                expected_transverse = {
                    (2, 1): 2 * delta,
                    (2, 2): -2 * delta,
                    (3, 1): -2 * delta,
                    (3, 2): -2 * delta,
                }[distinguished, line] % modulus
                assert pure_marked[0][distinguished] == expected_transverse
                assert expected_transverse
                transverse_entries[
                    f"punctured_d{distinguished}_L{line}_mode{marked_mode}_row0"
                ] = expected_transverse
                checked += 1

    for distinguished in (2, 3):
        beta = shifted_beta(alpha, canonical_beta, (h0, 0, 0, 0), modulus)
        pure_marked = one_marked_numeric(3, alpha, beta, modulus)
        epsilon = phi - 1 if distinguished == 2 else phi + 1
        expected_transverse = -2 * p * epsilon % modulus
        assert pure_marked[3][distinguished] == expected_transverse
        assert expected_transverse
        transverse_entries[f"endpoint_d{distinguished}_mode3_row3"] = (
            expected_transverse
        )
    assert len(transverse_entries) == 6
    return {
        "modulus": modulus,
        "residual_line_kernel_charts_checked": checked,
        "mixed_rank": 4,
        "kernel_dimension": 4,
        "pure_transverse_entries": transverse_entries,
        "pure_transverse_entries_nonzero": True,
    }


def pconst(value: int, modulus: int) -> Poly:
    value %= modulus
    return {} if value == 0 else {ZERO_EXPONENT: value}


def pvar(index: int) -> Poly:
    exponent = [0] * NVARIABLES
    exponent[index] = 1
    return {tuple(exponent): 1}


def padd(left: Poly, right: Poly, modulus: int) -> Poly:
    result = dict(left)
    for exponent, coefficient in right.items():
        value = (result.get(exponent, 0) + coefficient) % modulus
        if value:
            result[exponent] = value
        else:
            result.pop(exponent, None)
    return result


def pscale(coefficient: int, value: Poly, modulus: int) -> Poly:
    coefficient %= modulus
    if coefficient == 0:
        return {}
    return {
        exponent: coefficient * entry % modulus
        for exponent, entry in value.items()
        if coefficient * entry % modulus
    }


def psub(left: Poly, right: Poly, modulus: int) -> Poly:
    return padd(left, pscale(-1, right, modulus), modulus)


def pmul(left: Poly, right: Poly, modulus: int) -> Poly:
    result: Poly = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                left_value + right_value
                for left_value, right_value in zip(
                    left_exponent, right_exponent, strict=True
                )
            )
            coefficient = (
                result.get(exponent, 0) + left_coefficient * right_coefficient
            ) % modulus
            if coefficient:
                result[exponent] = coefficient
            else:
                result.pop(exponent, None)
    return result


def pproduct(values: Iterable[Poly], modulus: int) -> Poly:
    result = pconst(1, modulus)
    for value in values:
        result = pmul(result, value, modulus)
    return result


def permanent_poly(rows: Sequence[Sequence[Poly]], modulus: int) -> Poly:
    return poly_permutation_sum(rows, modulus, determinant=False)


def determinant_poly(rows: Sequence[Sequence[Poly]], modulus: int) -> Poly:
    return poly_permutation_sum(rows, modulus, determinant=True)


def permutation_sign(permutation: Sequence[int]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def poly_permutation_sum(
    rows: Sequence[Sequence[Poly]], modulus: int, *, determinant: bool
) -> Poly:
    result: Poly = {}
    for permutation in PERMUTATIONS[len(rows)]:
        term = pproduct(
            (rows[row][permutation[row]] for row in range(len(rows))), modulus
        )
        if determinant:
            term = pscale(permutation_sign(permutation), term, modulus)
        result = padd(result, term, modulus)
    return result


def polynomial_certificate_inputs(
    distinguished: int,
    line: int,
    modulus: int,
    *,
    intersection: bool,
) -> tuple[
    tuple[tuple[Poly, ...], ...],
    tuple[tuple[Poly, ...], ...],
    tuple[Poly, ...],
]:
    p, q, phi = (value % modulus for value in SAMPLES[modulus])
    delta = (q - phi) % modulus
    alpha_numeric, canonical_numeric = component_rows(modulus)
    alpha = tuple(
        tuple(pconst(value, modulus) for value in row) for row in alpha_numeric
    )
    canonical = tuple(
        tuple(pconst(value, modulus) for value in row) for row in canonical_numeric
    )
    u, a, b, c, r = (pvar(index) for index in range(NVARIABLES))
    line_parameter = pconst(0, modulus) if intersection else u
    shifts = [pconst(-inv(delta, modulus), modulus), {}, {}, {}]
    shifts[2 if line == 1 else 1] = line_parameter
    beta = tuple(
        tuple(
            padd(
                canonical[mode][coordinate],
                pmul(shifts[mode], alpha[mode][coordinate], modulus),
                modulus,
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    zero: Poly = {}
    pr = pscale(p, r, modulus)
    ua = pmul(line_parameter, a, modulus)
    if (distinguished, line) == (2, 1):
        extension = (pscale(-1, pr, modulus), a, c, zero, b, zero, ua, r)
    elif (distinguished, line) == (2, 2):
        extension = (pscale(-1, pr, modulus), c, a, zero, b, ua, zero, r)
    elif (distinguished, line) == (3, 1):
        extension = (pr, pscale(-1, a, modulus), c, zero, b, zero, ua, r)
    elif (distinguished, line) == (3, 2):
        extension = (pr, c, pscale(-1, a, modulus), zero, b, ua, zero, r)
    else:
        raise AssertionError((distinguished, line))
    return alpha, beta, extension


def one_marked_poly(
    distinguished: int,
    mode: int,
    alpha: Sequence[Sequence[Poly]],
    beta: Sequence[Sequence[Poly]],
    extension: Sequence[Poly],
    modulus: int,
) -> list[list[Poly]]:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_extended = tuple(
        tuple(alpha[row][coordinate] for coordinate in retained) + (extension[row],)
        for row in range(4)
    )
    beta_extended = tuple(
        tuple(beta[row][coordinate] for coordinate in retained) + (extension[4 + row],)
        for row in range(4)
    )
    result = []
    for word in WORDS3:
        selected: list[Sequence[Poly] | None] = []
        bit_index = 0
        for other_mode in range(4):
            if other_mode == mode:
                selected.append(None)
            else:
                selected.append(
                    beta_extended[other_mode]
                    if word[bit_index]
                    else alpha_extended[other_mode]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                pconst(int(index == coordinate), modulus) for index in range(4)
            )
            rows = tuple(
                basis if other_mode == mode else selected[other_mode]
                for other_mode in range(4)
            )
            assert all(row is not None for row in rows)
            coefficient_row.append(permanent_poly(rows, modulus))  # type: ignore[arg-type]
        result.append(coefficient_row)
    return result


def selected_minor(matrix: Sequence[Sequence[Poly]], rows: str, modulus: int) -> Poly:
    return determinant_poly([matrix[int(index)] for index in rows], modulus)


def diagonal_polynomials(
    distinguished: int, line: int, modulus: int
) -> tuple[Poly, Poly]:
    p, q, phi = (value % modulus for value in SAMPLES[modulus])
    delta = (q - phi) % modulus
    _, a, b, c, r = (pvar(index) for index in range(NVARIABLES))
    if distinguished == 2:
        alpha = pscale(
            2 * delta * (1 if line == 1 else -1),
            psub(a, c, modulus),
            modulus,
        )
        numerator = padd(
            pscale(p * (q - 1), r, modulus),
            pscale(-delta * (phi - 1), b, modulus),
            modulus,
        )
    else:
        alpha = pscale(2 * delta, psub(a, c, modulus), modulus)
        numerator = padd(
            pscale(p * (q + 1), r, modulus),
            pscale(delta * (phi + 1), b, modulus),
            modulus,
        )
    beta = pscale(2 * inv(delta, modulus), numerator, modulus)
    return alpha, beta


def minor_identity_audit(modulus: int) -> dict[str, object]:
    p, q, phi = (value % modulus for value in SAMPLES[modulus])
    delta = (q - phi) % modulus
    u, a, b, c, r = (pvar(index) for index in range(NVARIABLES))
    punctured_identities = 0
    punctured_points = 0
    intersection_identities = 0
    intersection_points = 0

    for distinguished in (2, 3):
        epsilon = phi - 1 if distinguished == 2 else phi + 1
        for line in (1, 2):
            alpha, beta, extension = polynomial_certificate_inputs(
                distinguished, line, modulus, intersection=False
            )
            mode = 1 if line == 1 else 2
            marked = one_marked_poly(
                distinguished, mode, alpha, beta, extension, modulus
            )
            actual_first = selected_minor(marked, "0127", modulus)
            actual_second = selected_minor(marked, "0237", modulus)
            diagonal_alpha, diagonal_beta = diagonal_polynomials(
                distinguished, line, modulus
            )
            if distinguished == 2 and line == 2:
                first_linear = padd(
                    pscale(epsilon, c, modulus), pscale(-1, r, modulus), modulus
                )
                second_linear = padd(
                    pscale(epsilon, a, modulus), pscale(-1, r, modulus), modulus
                )
            else:
                first_linear = padd(pscale(epsilon, c, modulus), r, modulus)
                second_linear = padd(pscale(epsilon, a, modulus), r, modulus)
            expected_first = pproduct(
                (
                    diagonal_alpha,
                    diagonal_beta,
                    pscale(-2 * delta * delta, u, modulus),
                    first_linear,
                ),
                modulus,
            )
            expected_second = pproduct(
                (
                    diagonal_alpha,
                    diagonal_beta,
                    pscale(2 * delta * delta, pmul(u, u, modulus), modulus),
                    second_linear,
                ),
                modulus,
            )
            assert actual_first == expected_first
            assert actual_second == expected_second
            punctured_identities += 2

            for values in itertools.product(range(modulus), repeat=4):
                a_value, b_value, c_value, r_value = values
                for u_value in range(1, modulus):
                    if distinguished == 2:
                        alpha_value = (
                            2 * delta * (1 if line == 1 else -1) * (a_value - c_value)
                        ) % modulus
                        beta_value = (
                            -2 * (phi - 1) * b_value
                            + 2 * p * (q - 1) * inv(delta, modulus) * r_value
                        ) % modulus
                    else:
                        alpha_value = 2 * delta * (a_value - c_value) % modulus
                        beta_value = (
                            2 * (phi + 1) * b_value
                            + 2 * p * (q + 1) * inv(delta, modulus) * r_value
                        ) % modulus
                    if not alpha_value or not beta_value:
                        continue
                    sign = -1 if distinguished == 2 and line == 2 else 1
                    first = u_value * (epsilon * c_value + sign * r_value) % modulus
                    second = (
                        u_value
                        * u_value
                        * (epsilon * a_value + sign * r_value)
                        % modulus
                    )
                    assert first or second
                    punctured_points += 1

        alpha, beta, extension = polynomial_certificate_inputs(
            distinguished, 1, modulus, intersection=True
        )
        marked = one_marked_poly(distinguished, 3, alpha, beta, extension, modulus)
        actual_first = selected_minor(marked, "0137", modulus)
        actual_second = selected_minor(marked, "0357", modulus)
        diagonal_alpha, diagonal_beta = diagonal_polynomials(distinguished, 1, modulus)
        first_linear = padd(pscale(epsilon, a, modulus), r, modulus)
        if distinguished == 2:
            second_linear = padd(
                pscale(p * (q - 1), a, modulus),
                pscale(delta, b, modulus),
                modulus,
            )
        else:
            second_linear = padd(
                pscale(p * (q + 1), a, modulus),
                pscale(-delta, b, modulus),
                modulus,
            )
        expected_first = pproduct(
            (
                diagonal_alpha,
                diagonal_beta,
                pconst(2 * p * p, modulus),
                first_linear,
            ),
            modulus,
        )
        expected_second = pproduct(
            (
                diagonal_alpha,
                diagonal_beta,
                pconst(2 * p * inv(delta, modulus), modulus),
                second_linear,
            ),
            modulus,
        )
        assert actual_first == expected_first
        assert actual_second == expected_second
        intersection_identities += 2

        for a_value, b_value, c_value, r_value in itertools.product(
            range(modulus), repeat=4
        ):
            alpha_value = 2 * delta * (a_value - c_value) % modulus
            if distinguished == 2:
                numerator = (
                    p * (q - 1) * r_value - delta * (phi - 1) * b_value
                ) % modulus
                first = (epsilon * a_value + r_value) % modulus
                second = (p * (q - 1) * a_value + delta * b_value) % modulus
                assert numerator == (p * (q - 1) * first - epsilon * second) % modulus
            else:
                numerator = (
                    p * (q + 1) * r_value + delta * (phi + 1) * b_value
                ) % modulus
                first = (epsilon * a_value + r_value) % modulus
                second = (p * (q + 1) * a_value - delta * b_value) % modulus
                assert numerator == (p * (q + 1) * first - epsilon * second) % modulus
            beta_value = 2 * inv(delta, modulus) * numerator % modulus
            if not alpha_value or not beta_value:
                continue
            assert first or second
            intersection_points += 1

    return {
        "modulus": modulus,
        "punctured_line_polynomial_identities": punctured_identities,
        "punctured_genuine_extension_points_checked": punctured_points,
        "intersection_polynomial_identities": intersection_identities,
        "intersection_genuine_extension_points_checked": intersection_points,
        "projective_marking_endpoints": "excluded because beta proportional to alpha is not a basis",
    }


def main() -> None:
    projections = [genuine_binary_projection(modulus) for modulus in MODULI]
    kernels = [kernel_audit(modulus) for modulus in MODULI]
    minors = [minor_identity_audit(modulus) for modulus in MODULI]
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import finite-field audit",
                "projection_audits": projections,
                "kernel_audits": kernels,
                "minor_audits": minors,
                "all_affine_markings_exhausted": True,
                "residual_line_intersection_included": True,
                "generic_H31_fibre_empty_modular_audit": True,
                "characteristic_zero_inference_from_modular_data": False,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
