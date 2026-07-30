#!/usr/bin/env python3
"""Independent finite-field audit of the single-gate H31 reduction."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_SINGLE_GATE_P3_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    size = len(rows)
    return (
        sum(
            _product(
                rows[row][permutation[row]]
                for row in range(size)
            )
            for permutation in itertools.permutations(range(size))
        )
        % prime
    )


def _product(values: object) -> int:
    result = 1
    for value in values:
        result *= int(value)
    return result


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [
            entry * inverse % prime
            for entry in work[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(
                        work[row],
                        work[pivot_row],
                    )
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def projective_points_2(prime: int) -> tuple[tuple[int, int, int], ...]:
    points = []
    for vector in itertools.product(range(prime), repeat=3):
        if vector == (0, 0, 0):
            continue
        first = next(entry for entry in vector if entry)
        inverse = pow(first, -1, prime)
        normalized = tuple(entry * inverse % prime for entry in vector)
        if normalized == vector:
            points.append(vector)
    return tuple(points)


def p3_rows(
    A: int,
    B: int,
    prime: int,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    alpha = (
        ((-B) % prime, 0, 1),
        (A, 1, 0),
        (A, 1, 0),
    )
    beta = (
        ((-A) % prime, 1, 0),
        (B, 0, 1),
        (0, B, A),
    )
    return alpha, beta


def extension_system(
    A: int,
    B: int,
    v: tuple[int, int, int],
    prime: int,
) -> tuple[list[list[int]], list[int]]:
    alpha, beta = p3_rows(A, B, prime)
    matrix = []
    desired = []
    for bits in itertools.product((0, 1), repeat=3):
        coefficient_row = []
        for variable in range(7):
            extras = [0] * 7
            extras[variable] = 1
            t, x1, x2, x3, y1, y2, y3 = extras
            alpha_extended = (
                alpha[0] + (x1,),
                alpha[1] + (x2,),
                alpha[2] + (x3,),
            )
            beta_extended = (
                beta[0] + (y1,),
                beta[1] + (y2,),
                beta[2] + (y3,),
            )
            rows = (v + (t,),) + tuple(
                beta_extended[mode]
                if bits[mode]
                else alpha_extended[mode]
                for mode in range(3)
            )
            coefficient_row.append(permanent(rows, prime))
        if bits == (1, 1, 1):
            desired = coefficient_row
        else:
            matrix.append(coefficient_row)
    return matrix, desired


def arrangement_factors(
    A: int,
    B: int,
    v: tuple[int, int, int],
    prime: int,
) -> tuple[int, ...]:
    v0, v1, v2 = v
    return tuple(
        value % prime
        for value in (
            B,
            v1,
            v2,
            -A * v1 - B * v2 + v0,
            -A * v1 + B * v2 + v0,
            A * v1 - B * v2 + v0,
            A * v1 + B * v2 + v0,
        )
    )


def predicted_viable(
    A: int,
    B: int,
    v: tuple[int, int, int],
    prime: int,
) -> bool:
    v0, v1, v2 = v
    first = B == 0 and (v0 - A * v1) % prime != 0
    second = (
        v1 == 0
        and v0 % prime != 0
        and (v0 + B * v2) % prime != 0
    )
    third = (
        B != 0
        and v2 == 0
        and v0 % prime != 0
        and (v0 - A * v1) % prime != 0
    )
    fourth = (
        (v0 + A * v1 - B * v2) % prime == 0
        and v0 % prime != 0
    )
    return first or second or third or fourth


def audit_prime(prime: int) -> dict[str, object]:
    points = projective_points_2(prime)
    total = 0
    arrangement = 0
    viable = 0
    viable_off_arrangement = 0
    classification_mismatches = 0
    matrix_ranks: Counter[int] = Counter()
    viable_ranks: Counter[int] = Counter()
    viable_zero_patterns: Counter[str] = Counter()

    for A in range(1, prime):
        for B in range(prime):
            alpha, beta = p3_rows(A, B, prime)
            p3_coefficients = {}
            for bits in itertools.product((0, 1), repeat=3):
                rows = tuple(
                    beta[mode] if bits[mode] else alpha[mode]
                    for mode in range(3)
                )
                p3_coefficients[bits] = permanent(rows, prime)
            assert p3_coefficients[(0, 0, 0)] == 2 * A % prime
            assert all(
                value == 0
                for bits, value in p3_coefficients.items()
                if bits != (0, 0, 0)
            )

            for v in points:
                total += 1
                matrix, desired = extension_system(A, B, v, prime)
                rank = rank_mod(matrix, prime)
                augmented_rank = rank_mod(matrix + [desired], prime)
                factors = arrangement_factors(A, B, v, prime)
                on_arrangement = 0 in factors
                is_viable = augmented_rank > rank
                matrix_ranks[rank] += 1
                arrangement += int(on_arrangement)
                viable += int(is_viable)
                if is_viable:
                    viable_ranks[rank] += 1
                    pattern = "".join(
                        str(index)
                        for index, factor in enumerate(factors)
                        if factor == 0
                    )
                    viable_zero_patterns[pattern] += 1
                    viable_off_arrangement += int(not on_arrangement)
                classification_mismatches += int(
                    is_viable
                    != predicted_viable(A, B, v, prime)
                )

    assert viable_off_arrangement == 0
    assert classification_mismatches == 0
    expected_total = (
        (prime - 1)
        * prime
        * (prime**2 + prime + 1)
    )
    assert total == expected_total
    return {
        "prime": prime,
        "projective_points": len(points),
        "parameter_configurations": total,
        "arrangement_configurations": arrangement,
        "viable_configurations": viable,
        "viable_off_arrangement": viable_off_arrangement,
        "exact_classification_mismatches": classification_mismatches,
        "matrix_rank_histogram": dict(sorted(matrix_ranks.items())),
        "viable_rank_histogram": dict(sorted(viable_ranks.items())),
        "viable_zero_factor_patterns": dict(
            sorted(viable_zero_patterns.items())
        ),
    }


def main() -> None:
    audits = [audit_prime(prime) for prime in (5, 7)]
    output = {
        "verified": True,
        "method": (
            "independent modular permanents and row reduction on "
            "(A,B,[v]) only"
        ),
        "fields": audits,
        "ambient_local_maps_enumerated": False,
        "Grassmannians_enumerated": False,
        "finite_field_audit_is_characteristic_zero_proof": False,
        "viable_locus_classified": True,
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_h31_single_gate_p3_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
