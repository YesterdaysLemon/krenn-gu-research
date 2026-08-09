#!/usr/bin/env python3
"""Finite-field audit of the rank-two-M single-gate H31 exclusion."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path

from audit_p5_h31_single_gate_p3_reduction import (
    extension_system,
    p3_rows,
    permanent,
    projective_points_2,
    rank_mod,
)


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md"
AUDIT_DEPENDENCY = ROOT / "audit_p5_h31_single_gate_p3_reduction.py"
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nullspace_basis(
    matrix: list[list[int]],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    work = [[entry % prime for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    pivots = []
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
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break

    free = [
        column for column in range(columns)
        if column not in pivots
    ]
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[row][free_column] % prime
        basis.append(tuple(vector))
    return tuple(basis)


def projective_coefficients(
    prime: int,
    dimension: int,
) -> tuple[tuple[int, ...], ...]:
    output = []
    for vector in itertools.product(range(prime), repeat=dimension):
        if not any(vector):
            continue
        if next(entry for entry in vector if entry) == 1:
            output.append(vector)
    return tuple(output)


def linear_combination(
    basis: tuple[tuple[int, ...], ...],
    coefficients: tuple[int, ...],
    prime: int,
) -> tuple[int, ...]:
    return tuple(
        sum(
            coefficient * vector[index]
            for coefficient, vector in zip(coefficients, basis)
        )
        % prime
        for index in range(len(basis[0]))
    )


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> list[list[int]]:
    output = []
    for bits in BITS3:
        selected: list[tuple[int, ...] | None] = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if bits[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate)
                for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis
                        if other == mode
                        else selected[other]  # type: ignore[arg-type]
                        for other in range(4)
                    ),
                    prime,
                )
            )
        output.append(coefficient_row)
    return output


def hp_rows(
    A: int,
    B: int,
    v: tuple[int, int, int],
    extension: tuple[int, ...],
    prime: int,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    t, x1, x2, x3, y1, y2, y3 = extension
    alpha_shared, beta_shared = p3_rows(A, B, prime)
    alpha = (
        (0, 0, 0, 1),
        alpha_shared[0] + (x1,),
        alpha_shared[1] + (x2,),
        alpha_shared[2] + (x3,),
    )
    beta = (
        v + (t,),
        beta_shared[0] + (y1,),
        beta_shared[1] + (y2,),
        beta_shared[2] + (y3,),
    )
    return alpha, beta


def source_transverse_column(
    mode: int,
    A: int,
    B: int,
    v: tuple[int, int, int],
    prime: int,
) -> tuple[int, ...]:
    alpha_shared, beta_shared = p3_rows(A, B, prime)
    alpha = (
        (0, 0, 0, 0),
        alpha_shared[0] + (0,),
        alpha_shared[1] + (0,),
        alpha_shared[2] + (0,),
    )
    beta = (
        v + (0,),
        beta_shared[0] + (0,),
        beta_shared[1] + (0,),
        beta_shared[2] + (0,),
    )
    matrix = one_marked_map(mode, alpha, beta, prime)
    return tuple(row[3] for row in matrix)


def certificate_case(
    A: int,
    B: int,
    v: tuple[int, int, int],
    extension: tuple[int, ...],
    prime: int,
) -> tuple[str, int, tuple[int, ...]] | None:
    _, _, _, _, y1, _, _ = extension
    v0, v1, v2 = v
    S = (v0 + A * v1) % prime
    P = (v0 - B * v2) % prime
    if B == 0:
        if S:
            return "B0_S_nonzero", 3, (0, 3, 4, 7)
        if v2:
            return "B0_S0_v2_nonzero", 1, (0, 1, 4, 7)
        if y1:
            return "B0_deep_y1_nonzero", 0, (0, 4, 5, 7)
        return None
    if v1 == 0:
        if v2 and P:
            return "v1_zero_generic", 3, (0, 3, 4, 7)
        if v2:
            return "v1_zero_P_zero", 1, (0, 1, 4, 7)
        return "v1_v2_zero", 3, (0, 3, 4, 7)
    if v2 == 0:
        if S:
            return "v2_zero_generic", 3, (0, 3, 4, 7)
        return "v2_zero_S_zero", 2, (0, 3, 5, 7)
    return "component_IV", 2, (0, 3, 5, 7)


def lift_combined(
    source: list[list[int]],
    partial: list[list[int]],
) -> list[list[int]]:
    return (
        [row[:3] + [row[3], 0] for row in source]
        + [row[:3] + [0, row[3]] for row in partial]
    )


def audit_prime(prime: int) -> dict[str, object]:
    cases: Counter[str] = Counter()
    viable_bases = 0
    viable_extensions = 0
    deep_by_base: dict[
        tuple[int, tuple[int, int, int]],
        list[tuple[int, ...]],
    ] = defaultdict(list)

    for A in range(1, prime):
        for B in range(prime):
            for v in projective_points_2(prime):
                matrix, desired = extension_system(A, B, v, prime)
                rank = rank_mod(matrix, prime)
                if rank_mod(matrix + [desired], prime) <= rank:
                    continue
                viable_bases += 1
                basis = nullspace_basis(matrix, prime)
                for coefficients in projective_coefficients(
                    prime,
                    len(basis),
                ):
                    extension = linear_combination(
                        basis,
                        coefficients,
                        prime,
                    )
                    wanted = sum(
                        left * right
                        for left, right in zip(desired, extension)
                    ) % prime
                    if not wanted:
                        continue
                    viable_extensions += 1
                    certificate = certificate_case(
                        A,
                        B,
                        v,
                        extension,
                        prime,
                    )
                    if certificate is None:
                        v0, v1, v2 = v
                        _, _, x2, x3, y1, _, _ = extension
                        assert B == 0
                        assert v2 == 0
                        assert (v0 + A * v1) % prime == 0
                        assert x2 == x3 == y1 == 0
                        deep_by_base[(A, v)].append(extension)
                        cases["deepest"] += 1
                        continue

                    name, mode, rows = certificate
                    alpha, beta = hp_rows(
                        A,
                        B,
                        v,
                        extension,
                        prime,
                    )
                    marked = one_marked_map(
                        mode,
                        alpha,
                        beta,
                        prime,
                    )
                    minor = [marked[row] for row in rows]
                    assert rank_mod(minor, prime) == 4
                    transverse = source_transverse_column(
                        mode,
                        A,
                        B,
                        v,
                        prime,
                    )
                    assert any(transverse)
                    cases[name] += 1

    deepest_pairs = 0
    for (A, v), extensions in deep_by_base.items():
        assert len(extensions) == prime**2
        alpha_shared, beta_shared = p3_rows(A, 0, prime)
        for source_extension in extensions:
            for partial_extension in extensions:
                deepest_pairs += 1
                _, X, _, _, _, U, W = source_extension
                _, x, _, _, _, u, w = partial_extension
                alpha_s = (
                    (0, 0, 0, 0),
                    alpha_shared[0] + (X,),
                    alpha_shared[1] + (0,),
                    alpha_shared[2] + (0,),
                )
                beta_s = (
                    v + (0,),
                    beta_shared[0] + (0,),
                    beta_shared[1] + (U,),
                    beta_shared[2] + (W,),
                )
                alpha_p = (
                    (0, 0, 0, 1),
                    alpha_shared[0] + (x,),
                    alpha_shared[1] + (0,),
                    alpha_shared[2] + (0,),
                )
                beta_p = (
                    v + (0,),
                    beta_shared[0] + (0,),
                    beta_shared[1] + (u,),
                    beta_shared[2] + (w,),
                )

                candidates = {
                    2: (0, 0, -A % prime, W, w),
                    3: (0, 0, -1 % prime, U, u),
                }
                for mode, candidate in candidates.items():
                    source_marked = one_marked_map(
                        mode,
                        alpha_s,
                        beta_s,
                        prime,
                    )
                    partial_marked = one_marked_map(
                        mode,
                        alpha_p,
                        beta_p,
                        prime,
                    )
                    combined = lift_combined(
                        source_marked,
                        partial_marked,
                    )
                    assert all(
                        sum(
                            left * right
                            for left, right in zip(row, candidate)
                        )
                        % prime
                        == 0
                        for row in combined
                    )
                    selected = [
                        [combined[row][column] for column in (0, 1, 3, 4)]
                        for row in (7, 8, 11, 15)
                    ]
                    assert rank_mod(selected, prime) == 4

                gamma2_s = (0, 0, -A % prime, W)
                gamma3_s = (0, 0, -1 % prime, U)
                mixed = permanent(
                    (
                        beta_s[0],
                        beta_s[1],
                        gamma2_s,
                        gamma3_s,
                    ),
                    prime,
                )
                beta_diagonal = permanent(beta_s, prime)
                assert mixed
                assert beta_diagonal
                assert (mixed + beta_diagonal) % prime == 0

    expected_deep_bases = prime - 1
    expected_deep_extensions = (prime - 1) * prime**2
    expected_deep_pairs = (prime - 1) * prime**4
    assert len(deep_by_base) == expected_deep_bases
    assert cases["deepest"] == expected_deep_extensions
    assert deepest_pairs == expected_deep_pairs

    return {
        "prime": prime,
        "viable_binary_bases": viable_bases,
        "viable_projective_extensions": viable_extensions,
        "transverse_certificate_counts": dict(sorted(cases.items())),
        "deepest_bases": len(deep_by_base),
        "deepest_extensions": cases["deepest"],
        "deepest_ordered_extension_pairs": deepest_pairs,
        "unclassified_extensions": 0,
        "surviving_ternary_lifts": 0,
    }


def main() -> None:
    audits = [audit_prime(prime) for prime in (5, 7)]
    output = {
        "verified": True,
        "method": (
            "independent modular permanents and row reduction on "
            "projective arrangement strata"
        ),
        "fields": audits,
        "ambient_local_maps_enumerated": False,
        "Grassmannians_enumerated": False,
        "finite_field_audit_is_characteristic_zero_proof": False,
        "rank_two_M_single_gate_H31_lift_possible": False,
        "all_single_gate_H31_excluded": False,
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "dependency": {
            "file": AUDIT_DEPENDENCY.name,
            "sha256": sha256(AUDIT_DEPENDENCY),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_single_gate_rank_two_m_exclusion_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
