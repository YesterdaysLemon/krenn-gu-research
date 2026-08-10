#!/usr/bin/env python3
"""Independent exact/modular audit of component twenty's special H31 fibres."""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass

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
p, q, t, r = sp.symbols("p q t r")
T0, T1 = sp.symbols("T0 T1")


@dataclass(frozen=True)
class Stratum:
    label: str
    distinguished: int
    marking: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]
    rows: tuple[int, int, int, int] = (0, 1, 4, 7)


@dataclass(frozen=True)
class ExactCase:
    label: str
    substitution: tuple[tuple[sp.Symbol, sp.Expr], ...]
    strata: tuple[Stratum, ...]


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS_4
        )
    )


def bases(
    p_value: sp.Expr, q_value: sp.Expr
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    one, zero = sp.Integer(1), sp.Integer(0)
    e = (one, zero, zero, zero)
    return (
        (
            (
                zero,
                -p_value * (p_value + 1),
                q_value * (q_value - 1),
                p_value - q_value + 1,
            ),
            e,
            e,
            (one, one, one, zero),
        ),
        (
            (-p_value + q_value - 1, -p_value - q_value, p_value + q_value, zero),
            (zero, p_value + 1, q_value - 1, one),
            (zero, p_value, q_value, one),
            e,
        ),
    )


def shifted(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    marking: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(sp.factor(beta[i][j] + marking[i] * alpha[i][j]) for j in range(4))
        for i in range(4)
    )


def extension_matrices(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    variables = sp.symbols("z0:8")
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_e = tuple(
        tuple(row[index] for index in retained) + (variables[mode],)
        for mode, row in enumerate(alpha)
    )
    beta_e = tuple(
        tuple(row[index] for index in retained) + (variables[4 + mode],)
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
    return (
        mixed,
        sp.Matrix([rows[(0, 0, 0, 0)]]),
        sp.Matrix([rows[(1, 1, 1, 1)]]),
    )


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
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_e = tuple(
        tuple(row[index] for index in retained) + (extension[j],)
        for j, row in enumerate(alpha)
    )
    beta_e = tuple(
        tuple(row[index] for index in retained) + (extension[4 + j],)
        for j, row in enumerate(beta)
    )
    return one_marked_map(mode, alpha_e, beta_e)


def generic_strata(p_value: sp.Expr, q_value: sp.Expr) -> tuple[Stratum, ...]:
    return (
        Stratum("C1", 1, (0, 1 - q_value, 0, 0)),
        Stratum("C2", 1, (0, 0, -q_value, 0)),
        Stratum("C3", 2, (0, -p_value - 1, 0, 0)),
        Stratum("C4", 2, (0, 0, -p_value, 0)),
    )


def exact_cases() -> tuple[ExactCase, ...]:
    cases: list[ExactCase] = []
    for label, p_value, q_value, marking, rows in (
        ("q=p", t, t, (0, 0, t, 0), (0, 1, 4, 7)),
        ("q=p+2", t, t + 2, (0, t + 1, 0, 0), (0, 2, 4, 7)),
        (
            "2pq-p+q=0",
            t,
            t / (2 * t + 1),
            (0, 0, 0, 0),
            (0, 1, 4, 7),
        ),
    ):
        cases.append(
            ExactCase(
                label,
                ((p, p_value), (q, q_value)),
                generic_strata(p_value, q_value) + (Stratum("D3", 3, marking, rows),),
            )
        )
    cases.extend(
        (
            ExactCase(
                "p=0",
                ((p, sp.Integer(0)), (q, t)),
                (
                    Stratum("C1", 1, (0, 1 - t, 0, 0), (0, 2, 4, 7)),
                    Stratum("C2", 1, (0, 0, -t, 0), (0, 2, 4, 7)),
                    Stratum("D2-line", 2, (0, r, 0, 0), (0, 2, 4, 7)),
                    Stratum("D3", 3, (0, t - 1, 0, 0), (0, 2, 4, 7)),
                ),
            ),
            ExactCase(
                "p=-1",
                ((p, sp.Integer(-1)), (q, t)),
                (
                    Stratum("C1", 1, (0, 1 - t, 0, 0)),
                    Stratum("C2", 1, (0, 0, -t, 0)),
                    Stratum("D2-line", 2, (0, 0, r, 0)),
                    Stratum("D3", 3, (0, 0, t, 0)),
                ),
            ),
            ExactCase(
                "q=0",
                ((p, t), (q, sp.Integer(0))),
                (
                    Stratum("D1-line", 1, (0, r, 0, 0), (0, 2, 4, 7)),
                    Stratum("C3", 2, (0, -t - 1, 0, 0), (0, 2, 4, 7)),
                    Stratum("C4", 2, (0, 0, -t, 0), (0, 2, 4, 7)),
                    Stratum("D3", 3, (0, t + 1, 0, 0), (0, 2, 4, 7)),
                ),
            ),
            ExactCase(
                "q=1",
                ((p, t), (q, sp.Integer(1))),
                (
                    Stratum("D1-line", 1, (0, 0, r, 0)),
                    Stratum("C3", 2, (0, -t - 1, 0, 0)),
                    Stratum("C4", 2, (0, 0, -t, 0)),
                    Stratum("D3", 3, (0, 0, t, 0)),
                ),
            ),
            ExactCase(
                "q=1/2",
                ((p, t), (q, sp.Rational(1, 2))),
                (
                    Stratum("D1-h2-axis", 1, (0, r, 0, 0)),
                    Stratum("D1-h1-axis", 1, (0, 0, r, 0)),
                    Stratum("C3", 2, (0, -t - 1, 0, 0)),
                    Stratum("C4", 2, (0, 0, -t, 0)),
                ),
            ),
            ExactCase(
                "p=-1/2",
                ((p, sp.Rational(-1, 2)), (q, t)),
                (
                    Stratum("C1", 1, (0, 1 - t, 0, 0)),
                    Stratum("C2", 1, (0, 0, -t, 0)),
                    Stratum("D2-h2-axis", 2, (0, r, 0, 0)),
                    Stratum("D2-h1-axis", 2, (0, 0, r, 0)),
                ),
            ),
        )
    )
    return tuple(cases)


def exact_residual_audit() -> list[dict[str, object]]:
    audited = []
    for case in exact_cases():
        substitution = dict(case.substitution)
        alpha, canonical = bases(substitution[p], substitution[q])
        for stratum in case.strata:
            beta = shifted(alpha, canonical, stratum.marking)
            mixed, diagonal_alpha, diagonal_beta = extension_matrices(
                stratum.distinguished, alpha, beta
            )
            assert mixed.rank() == 6
            kernel = mixed.nullspace()
            assert len(kernel) == 2
            extension = T0 * kernel[0] + T1 * kernel[1]
            first = sp.factor((diagonal_alpha * extension)[0])
            second = sp.factor((diagonal_beta * extension)[0])
            determinant = sp.factor(
                marked_extension(stratum.distinguished, extension, alpha, beta, 3)[
                    list(stratum.rows), :
                ].det()
            )
            ratio = sp.factor(sp.cancel(determinant / (first**2 * second)))
            assert ratio != 0
            assert not (ratio.free_symbols & {T0, T1, r})
            pure = one_marked_map(3, alpha, beta)
            transverse = [
                sp.factor(pure[row, stratum.distinguished]) for row in range(8)
            ]
            assert any(
                entry != 0 and r not in entry.free_symbols for entry in transverse
            )
            audited.append(
                {
                    "divisor": case.label,
                    "stratum": stratum.label,
                    "distinguished_coordinate": stratum.distinguished,
                    "mixed_rank": 6,
                    "minor_rows": list(stratum.rows),
                    "minor_over_alpha_squared_beta": str(ratio),
                    "uniform_in_marking_line_parameter": r in stratum.marking,
                    "pure_transverse_nonzero": True,
                }
            )
    return audited


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


def expected_survivors(
    prime: int, p_value: int, q_value: int
) -> tuple[set[tuple[int, ...]], ...]:
    zero = 0
    d1 = set()
    d2 = set()
    if (2 * q_value - 1) % prime == 0:
        d1 = {
            (zero, h1, h2, zero)
            for h1 in range(prime)
            for h2 in range(prime)
            if h1 * h2 % prime == 0
        }
    elif q_value % prime == 0:
        d1 = {(zero, h1, zero, zero) for h1 in range(prime)}
    elif (q_value - 1) % prime == 0:
        d1 = {(zero, zero, h2, zero) for h2 in range(prime)}
    else:
        d1 = {
            (zero, (1 - q_value) % prime, zero, zero),
            (zero, zero, -q_value % prime, zero),
        }

    if (2 * p_value + 1) % prime == 0:
        d2 = {
            (zero, h1, h2, zero)
            for h1 in range(prime)
            for h2 in range(prime)
            if h1 * h2 % prime == 0
        }
    elif p_value % prime == 0:
        d2 = {(zero, h1, zero, zero) for h1 in range(prime)}
    elif (p_value + 1) % prime == 0:
        d2 = {(zero, zero, h2, zero) for h2 in range(prime)}
    else:
        d2 = {
            (zero, -p_value - 1, zero, zero),
            (zero, zero, -p_value, zero),
        }
        d2 = {tuple(entry % prime for entry in marking) for marking in d2}

    d3 = set()
    if (q_value - p_value - 2) % prime == 0:
        d3.add((zero, q_value - 1, zero, zero))
    if (q_value - p_value) % prime == 0:
        d3.add((zero, zero, q_value, zero))
    if (2 * p_value * q_value - p_value + q_value) % prime == 0:
        d3.add((zero, zero, zero, zero))
    if p_value % prime == 0:
        d3.add((zero, q_value - 1, zero, zero))
    if (p_value + 1) % prime == 0:
        d3.add((zero, zero, q_value, zero))
    if q_value % prime == 0:
        d3.add((zero, p_value + 1, zero, zero))
    if (q_value - 1) % prime == 0:
        d3.add((zero, zero, p_value, zero))
    d3 = {tuple(entry % prime for entry in marking) for marking in d3}
    return set(), d1, d2, d3


def modular_projection_audit(
    label: str, prime: int, p_value: int, q_value: int
) -> dict[str, object]:
    symbolic_alpha, symbolic_beta = bases(sp.Integer(p_value), sp.Integer(q_value))
    alpha = [[int(entry) % prime for entry in row] for row in symbolic_alpha]
    canonical = [[int(entry) % prime for entry in row] for row in symbolic_beta]
    expected = expected_survivors(prime, p_value, q_value)
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
            label,
            distinguished,
            survivors,
            expected[distinguished],
        )
        counts.append(len(survivors))
    return {
        "divisor": label,
        "prime": prime,
        "parameter_sample": [p_value, q_value],
        "survivor_counts_by_deletion": counts,
        "expected_projected_zero_sets": True,
    }


def main() -> None:
    prime = 7
    samples = (
        ("q=p", prime, 2, 2),
        ("q=p+2", prime, 1, 3),
        ("2pq-p+q=0", prime, 1, 5),
        ("p=0", prime, 0, 3),
        ("p=-1", prime, 6, 3),
        ("q=0", prime, 2, 0),
        ("q=1", prime, 2, 1),
        ("q=1/2", prime, 1, 4),
        ("p=-1/2", prime, 3, 2),
    )
    modular = [modular_projection_audit(*sample) for sample in samples]
    residual = exact_residual_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent permanent reconstruction and modular projection audit",
                "modular_projection_audits": modular,
                "exact_residual_certificates": residual,
                "special_divisor_generic_points_H31_fibre_empty": True,
                "characteristic_zero_projection_inference_from_audit": False,
                "finite_modular_enumeration_used": True,
                "primary_verifier_imported": False,
                "divisor_intersections_closed": False,
                "projective_boundaries_closed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
