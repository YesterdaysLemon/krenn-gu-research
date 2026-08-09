#!/usr/bin/env python3
"""Finite-field audit of the complete marked fibre at infinity."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from audit_p5_h31_marked_basis_fibre_classification import (
    binary_extension_data,
    dot,
    extended_rows,
    linear_combination,
    marked_matrix,
    permanent3,
    projective_vectors,
    rank_mod,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT / "verify_p5_h31_component_fibre_infinity_marked_fibre.py"
)

CERTIFICATES = {
    0: (
        (1, (0, 1, 5, 7)),
        (2, (0, 4, 6, 7)),
        (3, (0, 1, 3, 7)),
        (2, (0, 2, 3, 7)),
        (0, (0, 1, 3, 7)),
        (2, (0, 2, 6, 7)),
    ),
    1: ((0, (0, 1, 3, 7)),),
    2: (
        (3, (0, 1, 5, 7)),
        (1, (0, 1, 5, 7)),
        (3, (0, 1, 4, 7)),
        (1, (0, 4, 5, 7)),
        (3, (0, 1, 3, 7)),
        (0, (0, 1, 3, 7)),
        (0, (0, 1, 5, 7)),
        (2, (0, 2, 6, 7)),
    ),
    3: (
        (0, (0, 2, 6, 7)),
        (3, (0, 1, 3, 7)),
        (1, (0, 1, 5, 7)),
        (3, (0, 1, 5, 7)),
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def family_rows(
    A: int,
    D: int,
    E: int,
    shifts: tuple[int, int, int, int],
    prime: int,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    canonical_alpha = (
        (0, 0, 1, 1),
        (0, 0, 1, 1),
        (0, 1, 0, E),
        (1, 0, 1, 0),
    )
    canonical_beta = (
        (-D, A, 0, D - A * E),
        (E, 1, -E, -E),
        (-1, 0, 1, 0),
        (0, 0, -1, 1),
    )
    beta = tuple(
        tuple(entry % prime for entry in row)
        for row in canonical_beta
    )
    alpha = tuple(
        tuple(
            (
                canonical_alpha[mode][coordinate]
                + shifts[mode] * beta[mode][coordinate]
            )
            % prime
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def projection_holds(
    distinguished: int,
    A: int,
    D: int,
    E: int,
    shifts: tuple[int, int, int, int],
    prime: int,
) -> bool:
    t0, t1, t2, t3 = shifts
    if distinguished == 0:
        generators = (
            E - t2,
            t3 * (t3 - 1),
            t1 * t3,
            A * t3,
            t0 * t1,
            t0 * t2 * (t3 - 1),
            t3 * (D * t0 + 1),
            t2 * (t1 * t2 + t3 - 1),
            t2 * (A * t2 + D * t3 - D),
            t2 * (D * t1 - A),
            t1 * (A * t2 - D),
            t2 * (D * t0 + t3),
            A * t0 * t2,
            D * D * t1 - A * A * t2,
        )
    elif distinguished == 1:
        generators = (
            t3,
            t0 * t2,
            t2 * (E - t2),
            2 * E * t1 - t1 * t2 - 1,
            t2 * (t1 * t2 - 1),
            t2 * (A * t2 - D),
            t2 * (D * t1 - A),
            A * (A * t2 - D),
            4 * D * t0 * t1 - 4 * t1 * t1 * t2 - A * t0
            + 4 * t1,
            A * E * t0 - 2 * D * t0 + 2 * t1 * t2 - 2,
            D * D * t0 - A * t2 + D,
            A * D * t0,
            A * D * (E - t2),
            4 * A * t1 * t1 * t2 + A * A * t0
            - 4 * A * t1,
            A * D * (D * t1 - A),
            A * t0 * (A * t0 - 4 * t1),
            A * (A * A * t0 + 4 * D * t1 * t1 - 4 * A * t1),
        )
    elif distinguished == 2:
        generators = (
            t1 * t3,
            t3 * (E - t2),
            A * t3,
            t0 * t1,
            t0 * (E - t2),
            t3 * (D * t0 + 1),
            t1 * (A * t2 + D),
            A * t0 * t2 * t2,
            D * E * E * t1 - A * E * t2 - D * E + D * t2,
            A * A * E * t2 * t2 + 2 * A * D * E * t2
            - A * D * t2 * t2 + D * D * E - D * D * t2,
            E * E * t1 * t1 * t2 + t1 * t2 * t2,
        )
    elif distinguished == 3:
        generators = (
            t0 * t1,
            t0 * (E - t2),
            t2 * t3 * (t3 - 1),
            t1 * t3 * t3,
            t1 * t2 * t3,
            t0 * t2 * (t3 - 1),
            t1 * t1 * t3,
            E * t1 * t3,
            D * t1 * t3,
            t0 * A * t3 - t1 * t3,
            t2 * (E * t1 + t3 - 1),
            t1 * (A * t2 + D),
            A * t0 * t2,
            D * E * t1 - A * t2 * t3 + A * t2,
            t0 * t3 * t3 * (t3 - 1),
            t0 * t0 * t3 * (t3 - 1),
            D * t0 * t3 * (t3 - 1),
            D * E * t3 * (t3 - 1),
            t2 * (A * t2 * t3 - A * t2 + D * t3 - D),
            t3 * (A * E * t2 + D * E - D * t2),
            t2 * (A * E * t2 - D * t2 * t3 + D * E),
        )
    else:
        raise ValueError(distinguished)
    return all(generator % prime == 0 for generator in generators)


def selected_marked_rows(
    mode: int,
    row_indices: tuple[int, int, int, int],
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> list[list[int]]:
    other_modes = tuple(other for other in range(4) if other != mode)
    bit_rows = tuple(itertools.product((0, 1), repeat=3))
    result: list[list[int]] = []
    for row_index in row_indices:
        bits = bit_rows[row_index]
        selected = {
            other: beta[other] if bits[index] else alpha[other]
            for index, other in enumerate(other_modes)
        }
        coefficient_row = []
        for coordinate in range(4):
            remaining_columns = tuple(
                column for column in range(4) if column != coordinate
            )
            permanent_rows = tuple(
                tuple(
                    selected[other][column]
                    for column in remaining_columns
                )
                for other in other_modes
            )
            coefficient_row.append(permanent3(permanent_rows, prime))
        result.append(coefficient_row)
    return result


def main() -> None:
    totals = {
        "projection_points": 0,
        "projection_closure_artifacts": 0,
        "binary_extensions": 0,
        "certificate_minor_tests": 0,
    }
    by_prime: dict[str, dict[str, int]] = {}
    for prime in (5, 7):
        counts = {key: 0 for key in totals}
        for distinguished in range(4):
            candidates = CERTIFICATES[distinguished]
            candidate_modes = {mode for mode, _rows in candidates}
            for A, D in projective_vectors(2, prime):
                for E in range(prime):
                    for shifts in itertools.product(
                        range(prime),
                        repeat=4,
                    ):
                        if not projection_holds(
                            distinguished,
                            A,
                            D,
                            E,
                            shifts,
                            prime,
                        ):
                            continue
                        counts["projection_points"] += 1
                        alpha, beta = family_rows(
                            A,
                            D,
                            E,
                            shifts,
                            prime,
                        )
                        (
                            _mixed,
                            diagonal_a,
                            diagonal_b,
                            kernel,
                        ) = binary_extension_data(
                            distinguished,
                            alpha,
                            beta,
                            prime,
                        )
                        if not (
                            any(
                                dot(diagonal_a, vector, prime)
                                for vector in kernel
                            )
                            and any(
                                dot(diagonal_b, vector, prime)
                                for vector in kernel
                            )
                        ):
                            counts["projection_closure_artifacts"] += 1
                            continue
                        transverse = {
                            mode: any(
                                row[distinguished] % prime
                                for row in marked_matrix(
                                    mode,
                                    alpha,
                                    beta,
                                    prime,
                                )
                            )
                            for mode in candidate_modes
                        }
                        for coefficients in projective_vectors(
                            len(kernel),
                            prime,
                        ):
                            extension = linear_combination(
                                coefficients,
                                kernel,
                                prime,
                            )
                            if (
                                dot(
                                    diagonal_a,
                                    list(extension),
                                    prime,
                                )
                                == 0
                                or dot(
                                    diagonal_b,
                                    list(extension),
                                    prime,
                                )
                                == 0
                            ):
                                continue
                            counts["binary_extensions"] += 1
                            alpha_p, beta_p = extended_rows(
                                distinguished,
                                alpha,
                                beta,
                                extension,
                            )
                            excluded = False
                            for mode, row_indices in candidates:
                                counts["certificate_minor_tests"] += 1
                                if not transverse[mode]:
                                    continue
                                selected = selected_marked_rows(
                                    mode,
                                    row_indices,
                                    alpha_p,
                                    beta_p,
                                    prime,
                                )
                                if rank_mod(selected, prime) == 4:
                                    excluded = True
                                    break
                            if not excluded:
                                raise AssertionError(
                                    (
                                        "unexcluded extension",
                                        prime,
                                        distinguished,
                                        A,
                                        D,
                                        E,
                                        shifts,
                                        extension,
                                    )
                                )
        by_prime[str(prime)] = counts
        for key, value in counts.items():
            totals[key] += value

    report = {
        "verified": True,
        "method": (
            "exhaust exact projection strata over F5 and F7; "
            "modular mixed kernels; every projective extension "
            "direction; direct selected-minor tests"
        ),
        "projective_first_plane_points_per_field": "p+1",
        "orientations": 4,
        "by_prime": by_prime,
        "totals": totals,
        "complete_first_plane_infinity_marked_fibre_excluded": True,
        "global": False,
        "theorem_sha256": sha256(THEOREM),
        "primary_sha256": sha256(PRIMARY),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
