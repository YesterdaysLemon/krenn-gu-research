#!/usr/bin/env python3
"""Independent exact/modular audit of component twenty's H31 obstruction."""

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
# Keep every generic certificate factor p*q*(p+q)*(p-q+1) nonzero and avoid
# the audited special-base divisors.  F_7 is too small to avoid all extra
# specialization coincidences at once.
MODULAR_SAMPLES = ((11, 2, 5), (13, 2, 5))


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS_4
        )
    )


def bases(
    p: sp.Expr, q: sp.Expr
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    one, zero = sp.Integer(1), sp.Integer(0)
    e = (one, zero, zero, zero)
    return (
        ((zero, -p * (p + 1), q * (q - 1), p - q + 1), e, e, (one, one, one, zero)),
        (
            (-p + q - 1, -p - q, p + q, zero),
            (zero, p + 1, q - 1, one),
            (zero, p, q, one),
            e,
        ),
    )


def shifted(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(beta[i][j] + shifts[i] * alpha[i][j] for j in range(4)) for i in range(4)
    )


def extension_matrices(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    variables = sp.symbols("z0:8")
    retained = tuple(i for i in range(4) if i != distinguished)
    alpha_e = tuple(
        tuple(row[i] for i in retained) + (variables[mode],)
        for mode, row in enumerate(alpha)
    )
    beta_e = tuple(
        tuple(row[i] for i in retained) + (variables[4 + mode],)
        for mode, row in enumerate(beta)
    )
    coefficients = {
        word: permanent(tuple(beta_e[i] if word[i] else alpha_e[i] for i in range(4)))
        for word in WORDS
    }
    rows = {
        word: [sp.diff(coefficients[word], variable) for variable in variables]
        for word in WORDS
    }
    mixed = sp.Matrix(
        [rows[word] for word in WORDS if word not in ((0, 0, 0, 0), (1, 1, 1, 1))]
    )
    return mixed, sp.Matrix([rows[(0, 0, 0, 0)]]), sp.Matrix([rows[(1, 1, 1, 1)]])


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    result = []
    for bits in itertools.product((0, 1), repeat=3):
        selected: list[tuple[sp.Expr, ...] | None] = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        result.append(
            [
                permanent(
                    tuple(
                        tuple(int(index == coordinate) for index in range(4))
                        if other == mode
                        else selected[other]
                        for other in range(4)
                    )
                )
                for coordinate in range(4)
            ]
        )
    return sp.Matrix(result)


def marked_extension(
    distinguished: int,
    extension: sp.Matrix,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    mode: int,
) -> sp.Matrix:
    retained = tuple(i for i in range(4) if i != distinguished)
    alpha_e = tuple(
        tuple(row[i] for i in retained) + (extension[j],) for j, row in enumerate(alpha)
    )
    beta_e = tuple(
        tuple(row[i] for i in retained) + (extension[4 + j],)
        for j, row in enumerate(beta)
    )
    return one_marked_map(mode, alpha_e, beta_e)


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    columns = len(work[0])
    for column in range(columns):
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
                    (work[row][j] - multiplier * work[rank][j]) % prime
                    for j in range(columns)
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
    retained = [i for i in range(4) if i != distinguished]
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


def modular_projection_audit(prime: int, p: int, q: int) -> dict[str, object]:
    symbolic_alpha, symbolic_beta = bases(sp.Integer(p), sp.Integer(q))
    alpha = [[int(entry) % prime for entry in row] for row in symbolic_alpha]
    canonical = [[int(entry) % prime for entry in row] for row in symbolic_beta]
    expected = {
        0: set(),
        1: {(0, 0, -q % prime, 0), (0, (1 - q) % prime, 0, 0)},
        2: {(0, 0, -p % prime, 0), (0, (-p - 1) % prime, 0, 0)},
        3: set(),
    }
    counts = []
    for distinguished in range(4):
        survivors = set()
        for marking in itertools.product(range(prime), repeat=4):
            beta = [
                [(canonical[i][j] + marking[i] * alpha[i][j]) % prime for j in range(4)]
                for i in range(4)
            ]
            rows = modular_rows(distinguished, alpha, beta, prime)
            mixed, diagonal_alpha, diagonal_beta = rows[1:15], rows[0], rows[15]
            mixed_rank = rank_mod(mixed, prime)
            if (
                mixed_rank < 8
                and rank_mod(mixed + [diagonal_alpha], prime) > mixed_rank
                and rank_mod(mixed + [diagonal_beta], prime) > mixed_rank
            ):
                survivors.add(marking)
        assert survivors == expected[distinguished], (
            prime,
            p,
            q,
            distinguished,
            survivors,
            expected[distinguished],
        )
        counts.append(len(survivors))
    return {
        "prime": prime,
        "parameter_sample": [p, q],
        "survivor_counts_by_deletion": counts,
        "expected_projected_zero_sets": True,
    }


def exact_residual_audit() -> list[dict[str, object]]:
    p, q, parameter = sp.symbols("p q T")
    residual = p - q + 1
    alpha, canonical = bases(p, q)
    cases = (
        (
            1,
            (0, 1 - q, 0, 0),
            (-p * (p + 1), 0, 0, 1, -p - q, p + 1, p, 0),
            (p * q, -1, -1, 0, 2 * q - 1, -q, 0, 1),
        ),
        (
            1,
            (0, 0, -q, 0),
            (-p * (p + 1), 0, 0, 1, -p - q, p + 1, p, 0),
            (0, -1, -1, (q - 1) / p, q * residual / p, (p + 1) * (q - 1) / p, 0, 1),
        ),
        (
            2,
            (0, -p - 1, 0, 0),
            (q * (q - 1), 0, 0, 1, p + q, q - 1, q, 0),
            (-p * q, -1, -1, 0, -2 * p - 1, -p, 0, 1),
        ),
        (
            2,
            (0, 0, -p, 0),
            (q * (q - 1), 0, 0, 1, p + q, q - 1, q, 0),
            (0, -1, -1, (p + 1) / q, p * residual / q, (p + 1) * (q - 1) / q, 0, 1),
        ),
    )
    audited = []
    for distinguished, marking, vector0, vector1 in cases:
        beta = shifted(alpha, canonical, marking)
        mixed, diagonal_alpha, diagonal_beta = extension_matrices(
            distinguished, alpha, beta
        )
        frame = sp.Matrix.hstack(sp.Matrix(vector0), sp.Matrix(vector1))
        assert all(sp.factor(entry) == 0 for entry in mixed * frame)
        assert mixed.rank() == 6
        extension = parameter * frame[:, 0] + frame[:, 1]
        first = sp.factor((diagonal_alpha * extension)[0])
        second = sp.factor((diagonal_beta * extension)[0])
        assert sp.factor(first + 2 * residual) == 0
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, beta, 3)[
                [0, 1, 4, 7], :
            ].det()
        )
        ratio = sp.factor(sp.cancel(determinant / second))
        assert sp.factor(ratio - 4 * p * q * (p + q) * residual) == 0
        transverse = sp.factor(one_marked_map(3, alpha, beta)[1, distinguished])
        expected_transverse = p * q if distinguished == 1 else -p * q
        assert sp.factor(transverse - expected_transverse) == 0
        audited.append(
            {
                "distinguished_coordinate": distinguished,
                "marking": [str(entry) for entry in marking],
                "mixed_rank": 6,
                "minor_over_beta_diagonal": str(ratio),
                "pure_transverse_entry": str(transverse),
            }
        )
    return audited


def main() -> None:
    modular = [modular_projection_audit(*sample) for sample in MODULAR_SAMPLES]
    residual = exact_residual_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent modular projection and exact permanent audit",
                "modular_projection_audits": modular,
                "exact_residual_certificates": residual,
                "generic_marked_H31_fibre_empty": True,
                "characteristic_zero_projection_inference_from_audit": False,
                "finite_modular_enumeration_used": True,
                "symbolic_parameter_search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
