#!/usr/bin/env python3
"""Independent finite-field audit of the a=0 disjoint P3 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_A0_DISJOINT_P3_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_q4_211_a0_disjoint_p3.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_mod(
    rows: tuple[tuple[int, ...], ...],
    prime: int,
) -> int:
    order = len(rows)
    return (
        sum(
            _permutation_product(rows, permutation, prime)
            for permutation in itertools.permutations(range(order))
        )
        % prime
    )


def _permutation_product(
    rows: tuple[tuple[int, ...], ...],
    permutation: tuple[int, ...],
    prime: int,
) -> int:
    value = 1
    for index in range(len(rows)):
        value = value * rows[index][permutation[index]] % prime
    return value


def rref_mod(
    rows: list[list[int]] | tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[tuple[tuple[int, ...], ...], int]:
    matrix = [[entry % prime for entry in row] for row in rows]
    if not matrix:
        return tuple(), 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(
            matrix[pivot_row][column] % prime,
            prime - 2,
            prime,
        )
        matrix[pivot_row] = [
            entry * inverse % prime for entry in matrix[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            multiplier = matrix[row][column] % prime
            if multiplier:
                matrix[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(
                        matrix[row],
                        matrix[pivot_row],
                        strict=True,
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    nonzero = [
        tuple(row) for row in matrix if any(entry % prime for entry in row)
    ]
    return tuple(nonzero), len(nonzero)


def rank_mod(rows: list[list[int]], prime: int) -> int:
    return rref_mod(rows, prime)[1]


def all_planes_3(prime: int) -> list[tuple[tuple[int, ...], ...]]:
    planes = []
    for pivots in itertools.combinations(range(3), 2):
        nonpivots = [index for index in range(3) if index not in pivots]
        variable_positions = [
            (row, column)
            for row in range(2)
            for column in nonpivots
            if column > pivots[row]
        ]
        for values in itertools.product(
            range(prime),
            repeat=len(variable_positions),
        ):
            rows = [[0] * 3 for _ in range(2)]
            rows[0][pivots[0]] = 1
            rows[1][pivots[1]] = 1
            for (row, column), value in zip(
                variable_positions,
                values,
                strict=True,
            ):
                rows[row][column] = value
            planes.append(tuple(tuple(row) for row in rows))
    expected = prime**2 + prime + 1
    if len(planes) != expected or len(set(planes)) != expected:
        raise AssertionError("ternary plane enumeration changed")
    return planes


def contains(
    plane: tuple[tuple[int, ...], ...],
    row: tuple[int, ...],
    prime: int,
) -> bool:
    return rank_mod(
        [list(plane[0]), list(plane[1]), list(row)],
        prime,
    ) == 2


def restricted_p3(
    first: tuple[tuple[int, ...], ...],
    second: tuple[tuple[int, ...], ...],
    third: tuple[tuple[int, ...], ...],
    prime: int,
) -> dict[tuple[int, int, int], int]:
    return {
        bits: permanent_mod(
            (
                first[bits[0]],
                second[bits[1]],
                third[bits[2]],
            ),
            prime,
        )
        for bits in itertools.product((0, 1), repeat=3)
    }


def is_nonzero_rank_one(
    tensor: dict[tuple[int, int, int], int],
    prime: int,
) -> bool:
    if not any(tensor.values()):
        return False
    for mode in range(3):
        other_modes = [index for index in range(3) if index != mode]
        flattening = []
        for bit in (0, 1):
            row = []
            for other_bits in itertools.product((0, 1), repeat=2):
                full_bits = [0, 0, 0]
                full_bits[mode] = bit
                full_bits[other_modes[0]] = other_bits[0]
                full_bits[other_modes[1]] = other_bits[1]
                row.append(tensor[tuple(full_bits)])
            flattening.append(row)
        if rank_mod(flattening, prime) != 1:
            return False
    return True


def audit_prime(prime: int) -> dict[str, object]:
    f4 = (1, 0, -1 % prime, 0)
    h4 = (1, 0, 0, -1 % prime)
    standard4 = tuple(
        tuple(1 if row == column else 0 for column in range(4))
        for row in range(4)
    )
    if permanent_mod((f4, f4, h4, h4), prime) != 0:
        raise AssertionError("marked corner changed")

    slice_checks = 0
    for row in standard4:
        expected = 2 * row[1] % prime
        placements = (
            (f4, f4, h4, row),
            (f4, h4, f4, row),
            (f4, row, h4, h4),
        )
        for placement in placements:
            if permanent_mod(placement, prime) != expected:
                raise AssertionError("zero-slice coordinate identity changed")
            slice_checks += 1

    # Check the P4-to-P3 separation on coordinate bases.  Multilinearity
    # then covers every row over the field.
    standard3 = tuple(
        tuple(1 if row == column else 0 for column in range(3))
        for row in range(3)
    )
    factorization_checks = 0
    for row_r in standard4:
        for row_b, row_c, row_d in itertools.product(
            standard3,
            repeat=3,
        ):
            lifted_b = (row_b[0], 0, row_b[1], row_b[2])
            lifted_c = (row_c[0], 0, row_c[1], row_c[2])
            lifted_d = (row_d[0], 0, row_d[1], row_d[2])
            left = permanent_mod(
                (row_r, lifted_b, lifted_c, lifted_d),
                prime,
            )
            right = (
                row_r[1]
                * permanent_mod((row_b, row_c, row_d), prime)
            ) % prime
            if left != right:
                raise AssertionError("P4-to-P3 factorization changed")
            factorization_checks += 1

    f3 = (1, -1 % prime, 0)
    h3 = (1, 0, -1 % prime)
    planes = all_planes_3(prime)
    b_planes = [
        plane
        for plane in planes
        if contains(plane, f3, prime)
        and not contains(plane, h3, prime)
    ]
    h_planes = [
        plane
        for plane in planes
        if contains(plane, h3, prime)
        and not contains(plane, f3, prime)
    ]
    if len(b_planes) != prime or len(h_planes) != prime:
        raise AssertionError("exact-incidence ternary plane count changed")

    triples_checked = 0
    rank_one_triples = 0
    nonzero_triples = 0
    for first in b_planes:
        for second in h_planes:
            for third in h_planes:
                tensor = restricted_p3(first, second, third, prime)
                triples_checked += 1
                if any(tensor.values()):
                    nonzero_triples += 1
                if is_nonzero_rank_one(tensor, prime):
                    rank_one_triples += 1
    if rank_one_triples:
        raise AssertionError("exact-disjoint ternary Segre survivor found")

    return {
        "prime": prime,
        "zero_slice_coordinate_checks": slice_checks,
        "P4_to_P3_coordinate_checks": factorization_checks,
        "ternary_planes": len(planes),
        "B_exact_planes": len(b_planes),
        "C_D_exact_planes": len(h_planes),
        "ternary_plane_triples_checked": triples_checked,
        "nonzero_ternary_triples": nonzero_triples,
        "nonzero_rank_one_triples": rank_one_triples,
    }


def main() -> None:
    audits = [audit_prime(prime) for prime in (5, 7)]
    output = {
        "audited": True,
        "fields": ["F_5", "F_7"],
        "audits": audits,
        "enumerated_ambient_maps": 0,
        "enumerated_four_dimensional_grassmannians": 0,
        "exact_disjoint_a0_excluded_over_C": True,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_a0_disjoint_p3_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
