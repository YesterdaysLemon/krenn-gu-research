#!/usr/bin/env python3
"""Independent modular audit of the support-two H31 boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_h31_embedded_p3_component_support_two_boundary.py"
)
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def squarefree_top(rows, prime: int) -> int:
    size = len(rows)
    coefficients = {0: 1}
    for row in rows:
        updated: dict[int, int] = {}
        for support, coefficient in coefficients.items():
            for coordinate, entry in enumerate(row):
                bit = 1 << coordinate
                if support & bit:
                    continue
                target = support | bit
                updated[target] = (
                    updated.get(target, 0) + coefficient * entry
                ) % prime
        coefficients = updated
    return coefficients.get((1 << size) - 1, 0)


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    result = [[entry % prime for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(result[0]) if result else 0):
        selected = next(
            (
                row
                for row in range(pivot_row, len(result))
                if result[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = (
            result[selected],
            result[pivot_row],
        )
        inverse = pow(result[pivot_row][column], -1, prime)
        result[pivot_row] = [
            entry * inverse % prime for entry in result[pivot_row]
        ]
        for row in range(len(result)):
            if row == pivot_row:
                continue
            multiplier = result[row][column]
            if multiplier:
                result[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(
                        result[row], result[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == len(result):
            break
    return pivot_row


def restricted_coefficients(alpha, beta, prime: int):
    return {
        word: squarefree_top(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            ),
            prime,
        )
        for word in WORDS4
    }


def one_marked(mode, alpha, beta, prime: int):
    source_basis = tuple(
        tuple(int(left == right) for right in range(4))
        for left in range(4)
    )
    rows = []
    for word in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if word[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        rows.append(
            [
                squarefree_top(
                    tuple(
                        source_basis[coordinate]
                        if other == mode
                        else selected[other]
                        for other in range(4)
                    ),
                    prime,
                )
                for coordinate in range(4)
            ]
        )
    return rows


def full_one_marked(mode, contraction, alpha, beta, prime: int):
    source_basis = tuple(
        tuple(int(left == right) for right in range(5))
        for left in range(5)
    )
    rows = []
    for word in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if word[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        rows.append(
            [
                squarefree_top(
                    tuple(
                        source_basis[coordinate]
                        if other == mode
                        else selected[other]
                        for other in range(4)
                    )
                    + (contraction,),
                    prime,
                )
                for coordinate in range(5)
            ]
        )
    return rows


def verify_binary(alpha, beta, prime: int):
    coefficients = restricted_coefficients(alpha, beta, prime)
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    assert coefficients[(0, 0, 0, 0)]
    assert coefficients[(1, 1, 1, 1)]
    return tuple(
        rank_mod(one_marked(mode, alpha, beta, prime), prime)
        for mode in range(4)
    )


def audit_prime(prime: int) -> dict[str, object]:
    # Generic exceptional-line point, C=2 and rho=-Cp.
    cap_c, cap_p, cap_q, cap_r = 2, 1, 2, 3
    p, q, h, t1, t3, y0 = 1, 3, 1, 0, 2, 5
    rho = -cap_c * p
    x0 = (
        h
        * (
            (cap_r - cap_c * cap_p) * (t1 + t3)
            - cap_c * cap_q
        )
        * pow(cap_c, -1, prime)
    )
    generic_alpha = (
        (cap_p, cap_q, cap_r, x0),
        (0, 1, 0, -h),
        (1, 0, cap_c, 0),
        (0, 1, 0, -h),
    )
    generic_beta = (
        (p, q, rho, y0),
        (1, t1, -cap_c, h * t1),
        (0, 1, 0, h),
        (1, t3, -cap_c, h * t3),
    )
    generic_ranks = verify_binary(
        generic_alpha, generic_beta, prime
    )
    assert generic_ranks[2] == 4

    # Coordinate endpoint outside the resonance C=-1.
    coordinate_root_coefficient = squarefree_top(
        (
            (0, 1, 1, 1, 0),
            (1, 0, 1, 0, 7),
            (0, 0, 1, 0, 1),
            (0, 1, 0, cap_c, 0),
            (0, 0, 1, 0, 0),
        ),
        prime,
    )
    assert coordinate_root_coefficient == cap_c + 1

    # Resonant C=-1, transverse mode-zero alpha row.
    cap_p, cap_q, cap_r, h, k, y = 2, 4, 3, 1, 2, 3
    resonant_alpha = (
        (
            cap_p,
            cap_q,
            cap_r,
            h * (cap_p * k + cap_q + cap_r * k),
        ),
        (0, 1, 0, h),
        (1, 0, -1, 0),
        (0, 1, 0, h),
    )
    resonant_beta = (
        (0, 1, 0, y),
        (1, 0, 1, 0),
        (0, 1, 0, -h),
        (1, k, 1, -h * k),
    )
    resonant_ranks = verify_binary(
        resonant_alpha, resonant_beta, prime
    )
    assert max(resonant_ranks) == 4

    # Deepest transverse point: all neighboring ranks drop, but the
    # e0/e4 stack has full source rank.
    cap_q, k, y = 0, 0, -h
    deep_alpha = (
        (0, cap_p, cap_q, cap_r, 0),
        (0, 0, 1, 0, h),
        (0, 1, 0, -1, 0),
        (0, 0, 1, 0, h),
    )
    deep_beta = (
        (1, 0, 1, 0, y),
        (0, 1, 0, 1, 0),
        (0, 0, 1, 0, -h),
        (0, 1, 0, 1, 0),
    )
    deep_neighbor_alpha = tuple(row[1:] for row in deep_alpha)
    deep_neighbor_beta = tuple(row[1:] for row in deep_beta)
    deep_ranks = verify_binary(
        deep_neighbor_alpha, deep_neighbor_beta, prime
    )
    assert max(deep_ranks) == 3
    deep_stack = (
        full_one_marked(
            1, (1, 0, 0, 0, 0), deep_alpha, deep_beta, prime
        )
        + full_one_marked(
            1, (0, 0, 0, 0, 1), deep_alpha, deep_beta, prime
        )
    )
    assert rank_mod(deep_stack, prime) == 5

    # Antipodal resonant branch forced by the third binary contraction.
    inverse_two = pow(2, -1, prime)
    cap_p, cap_q, k, y = 2, 3, 2, 2
    antipodal_alpha = (
        (-cap_p, cap_q, cap_p, cap_q * inverse_two),
        (0, 1, 0, inverse_two),
        (1, 0, -1, 0),
        (0, 1, 0, inverse_two),
    )
    antipodal_beta = (
        (0, 1, 0, y),
        (1, 0, 1, 0),
        (0, 1, 0, -inverse_two),
        (1, k, 1, -k * inverse_two),
    )
    antipodal_ranks = verify_binary(
        antipodal_alpha, antipodal_beta, prime
    )
    assert antipodal_ranks[1] == 4

    # Deepest antipodal point: the unique mode-three completion kernel
    # gives a forbidden coefficient equal to 4.
    cap_q, k = 0, 0
    antipodal_deep_alpha = (
        (0, -cap_p, cap_q, cap_p, 0),
        (0, 0, 1, 0, inverse_two),
        (0, 1, 0, -1, 0),
        (0, 0, 1, 0, inverse_two),
    )
    antipodal_deep_beta = (
        (1, 0, 1, 0, y),
        (0, 1, 0, 1, 0),
        (0, 0, 1, 0, -inverse_two),
        (0, 1, 0, 1, 0),
    )
    antipodal_neighbor_alpha = tuple(
        row[1:] for row in antipodal_deep_alpha
    )
    antipodal_neighbor_beta = tuple(
        row[1:] for row in antipodal_deep_beta
    )
    antipodal_deep_ranks = verify_binary(
        antipodal_neighbor_alpha,
        antipodal_neighbor_beta,
        prime,
    )
    assert max(antipodal_deep_ranks) == 3
    fixed_coefficient = squarefree_top(
        (
            (0, 1, 1, 1, 0),
            antipodal_deep_beta[0],
            antipodal_deep_beta[1],
            antipodal_deep_beta[2],
            (0, 0, -2, 0, 1),
        ),
        prime,
    )
    assert fixed_coefficient == 4

    return {
        "generic_exceptional_line_neighboring_ranks": list(
            generic_ranks
        ),
        "coordinate_nonresonant_root_coefficient": (
            coordinate_root_coefficient
        ),
        "resonant_neighboring_ranks": list(resonant_ranks),
        "resonant_deepest_neighboring_ranks": list(deep_ranks),
        "resonant_deepest_stacked_rank": 5,
        "antipodal_neighboring_ranks": list(antipodal_ranks),
        "antipodal_deepest_neighboring_ranks": list(
            antipodal_deep_ranks
        ),
        "antipodal_fixed_third_coefficient": fixed_coefficient,
    }


def main() -> None:
    audits = {str(prime): audit_prime(prime) for prime in (101, 103)}
    output = {
        "verified": True,
        "method": (
            "independent squarefree subset multiplication, modular "
            "one-marked ranks, stacks, and third contractions"
        ),
        "primes": audits,
        "support_two_A_zero_boundary_H31_fibre_empty": True,
        "finite_field_audit_is_theorem": False,
        "global_problem_resolved": False,
        "dependencies": {
            THEOREM.name: sha256(THEOREM),
            PRIMARY.name: sha256(PRIMARY),
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
