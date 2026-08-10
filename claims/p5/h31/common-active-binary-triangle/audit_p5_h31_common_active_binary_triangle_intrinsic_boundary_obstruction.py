#!/usr/bin/env python3
"""Independent permanent/modular audit of the p-q+1=0 boundary."""

from __future__ import annotations

import itertools
import json

import sympy as sp
import sys
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS_3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS_4 = tuple(itertools.permutations(range(4)))


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS_4
        )
    )


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for row in range(rank + 1, len(work)):
            if work[row][column]:
                multiplier = work[row][column]
                work[row] = [
                    (work[row][index] - multiplier * work[rank][index]) % prime
                    for index in range(len(work[row]))
                ]
        rank += 1
    return rank


def permanent3_mod(rows: list[list[int]], prime: int) -> int:
    return (
        sum(
            rows[0][permutation[0]] * rows[1][permutation[1]] * rows[2][permutation[2]]
            for permutation in PERMUTATIONS_3
        )
        % prime
    )


def modular_rows(
    distinguished: int,
    alpha: list[list[int]],
    beta: list[list[int]],
    prime: int,
) -> list[list[int]]:
    retained = [index for index in range(4) if index != distinguished]
    result = []
    for word in WORDS:
        row = [0] * 8
        for mode in range(4):
            other_rows = [
                [
                    (beta[other] if word[other] else alpha[other])[coordinate] % prime
                    for coordinate in retained
                ]
                for other in range(4)
                if other != mode
            ]
            row[mode + 4 * word[mode]] = permanent3_mod(other_rows, prime)
        result.append(row)
    return result


def modular_projection_audit() -> dict[str, object]:
    prime, p_value = 11, 2
    inverse = pow(2 * p_value + 1, -1, prime)
    alpha = [
        [0, -1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
    ]
    beta = [
        [p_value * (p_value + 1) * inverse, -2 * p_value - 1, 0, 1],
        [0, p_value + 1, p_value, 1],
        [0, p_value, p_value + 1, 1],
        [1, 0, 0, 0],
    ]
    alpha = [[entry % prime for entry in row] for row in alpha]
    beta = [[entry % prime for entry in row] for row in beta]
    counts = []
    for distinguished in range(4):
        survivors = set()
        for marking in itertools.product(range(prime), repeat=4):
            marked_beta = [
                [(beta[i][j] + marking[i] * alpha[i][j]) % prime for j in range(4)]
                for i in range(4)
            ]
            rows = modular_rows(distinguished, alpha, marked_beta, prime)
            mixed, diagonal_alpha, diagonal_beta = rows[1:15], rows[0], rows[15]
            mixed_rank = rank_mod(mixed, prime)
            if (
                mixed_rank < 8
                and rank_mod(mixed + [diagonal_alpha], prime) > mixed_rank
                and rank_mod(mixed + [diagonal_beta], prime) > mixed_rank
            ):
                survivors.add(marking)
        assert not survivors, (distinguished, survivors)
        counts.append(0)
    return {
        "prime": prime,
        "parameter_sample": [p_value, p_value + 1],
        "survivor_counts_by_deletion": counts,
        "expected_empty_projection": True,
    }


def main() -> None:
    p = sp.Symbol("p")
    one, zero = sp.Integer(1), sp.Integer(0)
    e = (one, zero, zero, zero)
    alpha = ((zero, -one, one, zero), e, e, (one, one, one, zero))
    beta = (
        (p * (p + 1) / (2 * p + 1), -2 * p - 1, zero, one),
        (zero, p + 1, p, one),
        (zero, p, p + 1, one),
        e,
    )
    tensor = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert sp.factor(tensor[(1, 1, 1, 1)] + 2 * p * (p + 1)) == 0
    assert all(value == 0 for word, value in tensor.items() if word != (1, 1, 1, 1))
    modular = modular_projection_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent permanent reconstruction and modular projection audit",
                "base_divisor": "q=p+1",
                "pure_support": {"1111": "-2*p*(p+1)"},
                "replacement_intrinsic_basis_reconstructed": True,
                "modular_projection_audit": modular,
                "finite_modular_enumeration_used": True,
                "characteristic_zero_projection_inference_from_audit": False,
                "primary_verifier_imported": False,
                "projective_boundaries_closed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
