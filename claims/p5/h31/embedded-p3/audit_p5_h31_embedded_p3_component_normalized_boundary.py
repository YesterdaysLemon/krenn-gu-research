#!/usr/bin/env python3
"""Independent modular audit of the normalized embedded-P3 H31 boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

THEOREM = (
    HERE
    / "P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md"
)
PRIMARY = (
    HERE / "verify_p5_h31_embedded_p3_component_normalized_boundary.py"
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
            (beta[mode][coordinate]
             + shifts[mode] * alpha[mode][coordinate])
            % prime
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def neighboring_rows(alpha, beta, extension, prime: int):
    alpha_neighbor = tuple(
        tuple(alpha[mode][coordinate] for coordinate in (1, 2, 3))
        + (extension[mode] % prime,)
        for mode in range(4)
    )
    beta_neighbor = tuple(
        tuple(beta[mode][coordinate] for coordinate in (1, 2, 3))
        + (extension[4 + mode] % prime,)
        for mode in range(4)
    )
    return alpha_neighbor, beta_neighbor


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
    prime: int,
) -> tuple[int, int, tuple[int, ...]]:
    beta_marked = marked_beta(alpha, beta, shifts, prime)
    neighbor_alpha, neighbor_beta = neighboring_rows(
        alpha, beta_marked, extension, prime
    )
    coefficients = restricted_coefficients(
        neighbor_alpha, neighbor_beta, prime
    )
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    first = coefficients[(0, 0, 0, 0)]
    second = coefficients[(1, 1, 1, 1)]
    assert first and second
    ranks = tuple(
        rank_mod(
            one_marked(
                mode, neighbor_alpha, neighbor_beta, prime
            ),
            prime,
        )
        for mode in range(4)
    )
    return first, second, ranks


def audit_prime(prime: int) -> dict[str, object]:
    inverse_two = pow(2, -1, prime)
    base_beta = (
        (1, 0, 1, 1),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )

    cap_s, h, y = 2, 3, 4
    alpha_l3 = (
        (0, 1, cap_s, cap_s + 1),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    l3_cases = (
        (
            (-pow(cap_s, -1, prime), -1, -h, -1),
            (0, 0, 1, 0, y, 0, 0, 0),
        ),
        ((0, 0, 0, -h), (0, 0, 0, 1, y, 0, 0, 0)),
        (
            (-pow(cap_s + 1, -1, prime), -h, -1, 0),
            (0, 1, 0, 0, y, 0, 0, 0),
        ),
    )
    l3_ranks = []
    for shifts, extension in l3_cases:
        _, _, ranks = verify_binary_and_ranks(
            alpha_l3,
            base_beta,
            shifts,
            extension,
            prime,
        )
        assert max(ranks) == 4
        l3_ranks.append(ranks)

    alpha_e1 = (
        (0, 1, cap_s, cap_s),
        *alpha_l3[1:],
    )
    _, _, e1_ranks = verify_binary_and_ranks(
        alpha_e1,
        base_beta,
        (
            -pow(cap_s, -1, prime),
            -1,
            -1,
            -inverse_two,
        ),
        (1, 1, -1, 0, y, 0, 0, 1),
        prime,
    )
    assert max(e1_ranks) == 4

    alpha_e2 = (
        (0, 1, cap_s, 1),
        *alpha_l3[1:],
    )
    beta_e2 = (
        (1, 0, 1, 0),
        *base_beta[1:],
    )
    _, _, e2_ranks = verify_binary_and_ranks(
        alpha_e2,
        beta_e2,
        (0, 0, -inverse_two, 0),
        (-cap_s, 1, 0, 1, y, 0, 1, 0),
        prime,
    )
    assert max(e2_ranks) == 4

    # Deepest point S=0,y=1: all neighboring ranks are at most three.
    alpha_deep = (
        (0, 1, 0, 1),
        *alpha_l3[1:],
    )
    shifts_deep = (0, 0, -inverse_two, 0)
    extension_deep = (0, 1, 0, 1, 1, 0, 1, 0)
    _, _, deepest_ranks = verify_binary_and_ranks(
        alpha_deep,
        beta_e2,
        shifts_deep,
        extension_deep,
        prime,
    )
    assert max(deepest_ranks) == 3

    beta_deep = marked_beta(
        alpha_deep, beta_e2, shifts_deep, prime
    )
    full_alpha = tuple(
        tuple(alpha_deep[mode])
        + (extension_deep[mode] % prime,)
        for mode in range(4)
    )
    full_beta = tuple(
        tuple(beta_deep[mode])
        + (extension_deep[4 + mode] % prime,)
        for mode in range(4)
    )
    source_basis = tuple(
        tuple(int(left == right) for right in range(5))
        for left in range(5)
    )
    stacked = (
        full_one_marked(
            1, source_basis[0], full_alpha, full_beta, prime
        )
        + full_one_marked(
            1, source_basis[4], full_alpha, full_beta, prime
        )
    )
    assert rank_mod(stacked, prime) == 5

    return {
        "L3_neighboring_ranks": [list(ranks) for ranks in l3_ranks],
        "coordinate_e1_neighboring_ranks": list(e1_ranks),
        "coordinate_e2_neighboring_ranks": list(e2_ranks),
        "deepest_neighboring_ranks": list(deepest_ranks),
        "deepest_stacked_rank": 5,
    }


def main() -> None:
    audits = {str(prime): audit_prime(prime) for prime in (101, 103)}
    output = {
        "verified": True,
        "method": (
            "independent squarefree subset multiplication, "
            "modular one-marked ranks, and stacked deep-point audit"
        ),
        "primes": audits,
        "binary_survivor_families_replayed": 5,
        "deepest_neighboring_rank_at_most_three": True,
        "deepest_stacked_full_source_rank": 5,
        "complete_normalized_chart_marked_H31_fibre_empty": True,
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
