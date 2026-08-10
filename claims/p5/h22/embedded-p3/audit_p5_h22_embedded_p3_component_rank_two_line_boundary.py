#!/usr/bin/env python3
"""Independent modular audit of the weighted H22 rank-two boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_h22_embedded_p3_component_rank_two_line_boundary.py"
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


def marked_beta(alpha, beta, shifts, prime: int):
    return tuple(
        tuple(
            (
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            % prime
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def weighted_neighboring_rows(
    alpha, beta, extension, slope: int, prime: int
):
    def project(row, extra):
        return (
            (slope * row[0] + row[1]) % prime,
            row[2] % prime,
            row[3] % prime,
            extra % prime,
        )

    return (
        tuple(
            project(alpha[mode], extension[mode])
            for mode in range(4)
        ),
        tuple(
            project(beta[mode], extension[4 + mode])
            for mode in range(4)
        ),
    )


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


def verify_binary_and_ranks(
    alpha,
    beta,
    shifts,
    extension,
    slope: int,
    prime: int,
):
    beta_marked = marked_beta(alpha, beta, shifts, prime)
    neighbor_alpha, neighbor_beta = weighted_neighboring_rows(
        alpha, beta_marked, extension, slope, prime
    )
    coefficients = restricted_coefficients(
        neighbor_alpha, neighbor_beta, prime
    )
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    assert coefficients[(0, 0, 0, 0)]
    assert coefficients[(1, 1, 1, 1)]
    ranks = tuple(
        rank_mod(
            one_marked(
                mode, neighbor_alpha, neighbor_beta, prime
            ),
            prime,
        )
        for mode in range(4)
    )
    return beta_marked, ranks


def embedded_bases(cap_s: int, slope: int):
    alpha = (
        (0, 1, cap_s, cap_s + 1),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    beta = (
        (1, 0, 1, slope + 1),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    return alpha, beta


def audit_prime(prime: int) -> dict[str, object]:
    inverse_two = pow(2, -1, prime)
    cap_s, slope, h, y = 2, 3, 4, 5
    alpha_l3, beta_l3 = embedded_bases(cap_s, slope)
    l3_cases = (
        (
            "101",
            (-pow(cap_s, -1, prime), -1, -h, -1),
            (0, 0, 1, 0, y, 0, 0, 0),
        ),
        (
            "011",
            (-slope, 0, 0, -h),
            (0, 0, 0, 1, y, 0, 0, 0),
        ),
        (
            "1m10",
            (
                -(slope + 1) * pow(cap_s + 1, -1, prime),
                -h,
                -1,
                0,
            ),
            (0, 1, 0, 0, y, 0, 0, 0),
        ),
    )
    l3_ranks = {}
    for name, shifts, extension in l3_cases:
        _, ranks = verify_binary_and_ranks(
            alpha_l3,
            beta_l3,
            shifts,
            extension,
            slope,
            prime,
        )
        assert max(ranks) == 4
        l3_ranks[name] = list(ranks)

    # The two endpoint families are replayed on both factor branches h=0,1.
    alpha_zero, beta_zero = embedded_bases(0, slope)
    endpoint_ranks = {}
    for endpoint_h in (0, 1):
        for name, shifts, extension in (
            (
                "011",
                (-slope, 0, 0, -endpoint_h),
                (0, 0, 0, 1, y, 0, 0, 0),
            ),
            (
                "1m10",
                (-(slope + 1), -endpoint_h, -1, 0),
                (0, 1, 0, 0, y, 0, 0, 0),
            ),
        ):
            _, ranks = verify_binary_and_ranks(
                alpha_zero,
                beta_zero,
                shifts,
                extension,
                slope,
                prime,
            )
            assert max(ranks) == 4
            endpoint_ranks[f"{name}_h{endpoint_h}"] = list(ranks)

    # Coordinate stratum II: U=S,T=1.
    cap_s, slope, y = 2, 3, 4
    alpha_base, beta_base = embedded_bases(cap_s, slope)
    alpha_e1 = ((0, 1, cap_s, cap_s), *alpha_base[1:])
    beta_e1 = ((1, 0, 1, 1), *beta_base[1:])
    _, e1_ranks = verify_binary_and_ranks(
        alpha_e1,
        beta_e1,
        (-pow(cap_s, -1, prime), -1, -1, -inverse_two),
        (1, 1, -1, 0, y, 0, 0, 1),
        slope,
        prime,
    )
    assert max(e1_ranks) == 4

    # Coordinate stratum III: U=1,T=r.
    alpha_e2 = ((0, 1, cap_s, 1), *alpha_base[1:])
    beta_e2 = ((1, 0, 1, slope), *beta_base[1:])
    _, e2_ranks = verify_binary_and_ranks(
        alpha_e2,
        beta_e2,
        (-slope, 0, -inverse_two, 0),
        (-cap_s, 1, 0, 1, y, 0, 1, 0),
        slope,
        prime,
    )
    assert max(e2_ranks) == 4

    # Deep III endpoint S=0,y=1: neighboring maps drop to rank three,
    # but the two source contractions together still have rank five.
    alpha_deep_e2 = ((0, 1, 0, 1), *alpha_base[1:])
    beta_deep_e2 = ((1, 0, 1, slope), *beta_base[1:])
    extension_deep_e2 = (0, 1, 0, 1, 1, 0, 1, 0)
    marked_deep_e2, deepest_e2_ranks = verify_binary_and_ranks(
        alpha_deep_e2,
        beta_deep_e2,
        (-slope, 0, -inverse_two, 0),
        extension_deep_e2,
        slope,
        prime,
    )
    assert max(deepest_e2_ranks) == 3
    full_alpha_e2 = tuple(
        tuple(alpha_deep_e2[mode])
        + (extension_deep_e2[mode] % prime,)
        for mode in range(4)
    )
    full_beta_e2 = tuple(
        tuple(marked_deep_e2[mode])
        + (extension_deep_e2[4 + mode] % prime,)
        for mode in range(4)
    )
    stacked_e2 = (
        full_one_marked(
            1,
            (1, slope, 0, 0, 0),
            full_alpha_e2,
            full_beta_e2,
            prime,
        )
        + full_one_marked(
            1,
            (0, 0, 0, 0, 1),
            full_alpha_e2,
            full_beta_e2,
            prime,
        )
    )
    assert rank_mod(stacked_e2, prime) == 5

    # Coordinate stratum IV: S=r=-1, first dense and then U=0.
    slope_e3, cap_t, cap_u, y = -1, 3, 2, 4
    alpha_e3 = (
        (0, 1, -1, cap_u),
        *alpha_base[1:],
    )
    beta_e3 = (
        (1, 0, 1, cap_t),
        *beta_base[1:],
    )
    shifts_e3 = (1, -inverse_two, 0, -1)
    _, e3_ranks = verify_binary_and_ranks(
        alpha_e3,
        beta_e3,
        shifts_e3,
        (-cap_u, 0, 1, 1, y, 1, 0, 0),
        slope_e3,
        prime,
    )
    assert max(e3_ranks) == 4

    cap_u, y = 0, 4
    alpha_e3_zero = (
        (0, 1, -1, cap_u),
        *alpha_base[1:],
    )
    beta_e3_zero = (
        (1, 0, 1, cap_t),
        *beta_base[1:],
    )
    _, e3_endpoint_ranks = verify_binary_and_ranks(
        alpha_e3_zero,
        beta_e3_zero,
        shifts_e3,
        (0, 0, 1, 1, y, 1, 0, 0),
        slope_e3,
        prime,
    )
    assert max(e3_endpoint_ranks) == 4

    y = cap_t
    extension_deep_e3 = (0, 0, 1, 1, y, 1, 0, 0)
    marked_deep_e3, deepest_e3_ranks = verify_binary_and_ranks(
        alpha_e3_zero,
        beta_e3_zero,
        shifts_e3,
        extension_deep_e3,
        slope_e3,
        prime,
    )
    assert max(deepest_e3_ranks) == 3
    full_alpha_e3 = tuple(
        tuple(alpha_e3_zero[mode])
        + (extension_deep_e3[mode] % prime,)
        for mode in range(4)
    )
    full_beta_e3 = tuple(
        tuple(marked_deep_e3[mode])
        + (extension_deep_e3[4 + mode] % prime,)
        for mode in range(4)
    )
    stacked_e3 = (
        full_one_marked(
            2,
            (1, -1, 0, 0, 0),
            full_alpha_e3,
            full_beta_e3,
            prime,
        )
        + full_one_marked(
            2,
            (0, 0, 0, 0, 1),
            full_alpha_e3,
            full_beta_e3,
            prime,
        )
    )
    assert rank_mod(stacked_e3, prime) == 5

    return {
        "L3_neighboring_ranks": l3_ranks,
        "L3_endpoint_neighboring_ranks": endpoint_ranks,
        "coordinate_e1_neighboring_ranks": list(e1_ranks),
        "coordinate_e2_neighboring_ranks": list(e2_ranks),
        "coordinate_e2_deepest_neighboring_ranks": list(
            deepest_e2_ranks
        ),
        "coordinate_e2_deepest_stacked_rank": 5,
        "coordinate_e3_neighboring_ranks": list(e3_ranks),
        "coordinate_e3_endpoint_neighboring_ranks": list(
            e3_endpoint_ranks
        ),
        "coordinate_e3_deepest_neighboring_ranks": list(
            deepest_e3_ranks
        ),
        "coordinate_e3_deepest_stacked_rank": 5,
    }


def main() -> None:
    audits = {str(prime): audit_prime(prime) for prime in (101, 103)}
    output = {
        "verified": True,
        "method": (
            "independent squarefree subset multiplication, weighted "
            "projection, modular one-marked ranks, and stacked audits"
        ),
        "primes": audits,
        "binary_survivor_families_replayed": 6,
        "endpoint_factor_branches_replayed": 4,
        "deepest_neighboring_rank_at_most_three": True,
        "deepest_stacked_full_source_rank": 5,
        "rank_two_projected_line_weighted_H22_fibre_empty": True,
        "rank_one_projection_collapse_claimed_by_this_theorem": False,
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
