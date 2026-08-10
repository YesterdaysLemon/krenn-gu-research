#!/usr/bin/env python3
"""Finite-field audit of the complete chart-boundary marked fibre."""

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
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/disputed-ownership/first-second-component-provenance/marked-basis-fibre-classification")

from audit_p5_h31_marked_basis_fibre_classification import (  # noqa: E402
    binary_extension_data,
    dot,
    extended_rows,
    linear_combination,
    marked_matrix,
    permanent3,
    projective_vectors,
    rank_mod,
)


THEOREM = (
    HERE / "P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md"
)
PRIMARY = HERE / "verify_p5_h31_component_chart_boundary_marked_fibre.py"

CERTIFICATES = {
    0: (
        (2, (0, 2, 3, 7)),
        (2, (0, 3, 6, 7)),
        (2, (0, 2, 6, 7)),
        (0, (0, 4, 5, 7)),
    ),
    1: (
        (0, (0, 3, 5, 7)),
        (0, (0, 4, 5, 7)),
    ),
    2: (
        (2, (0, 2, 3, 7)),
        (2, (0, 3, 6, 7)),
        (2, (0, 2, 6, 7)),
    ),
    3: (
        (2, (0, 2, 3, 7)),
        (2, (0, 3, 6, 7)),
        (0, (0, 4, 5, 7)),
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def family_rows(
    A: int,
    R: int,
    shifts: tuple[int, int, int, int],
    prime: int,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    canonical_alpha = (
        (1, 0, A, A - 1),
        (0, 0, 1, 1),
        (0, 1, 0, R),
        (1, 0, 1, 0),
    )
    canonical = (
        (0, 1, 0, -R),
        (R, 1, -R, -R),
        (-1, 0, 1, 0),
        (0, 0, -1, 1),
    )
    beta = tuple(
        tuple(entry % prime for entry in row)
        for row in canonical
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
    R: int,
    shifts: tuple[int, int, int, int],
    prime: int,
) -> bool:
    t0, t1, t2, t3 = shifts
    if distinguished == 0:
        generators = (
            t3,
            t2,
            t0 * t1,
            R * (R * t1 + A - 1),
            R * t0 * (A - 1),
        )
    elif distinguished == 1:
        generators = (
            t3,
            t2,
            t1,
            2 * R * t0 - A + 1,
            (A + 1) * t0,
            A * A - 1,
        )
    elif distinguished == 2:
        generators = (t3, t2, t1, R * t0 * (A - 1))
    elif distinguished == 3:
        generators = (
            t2,
            t1,
            t3 * (A - t3 + 1),
            t3 * (R * t0 + 1),
            R * t0 * (A + 1) + t3,
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
            for A in range(1, prime):
                for R in range(prime):
                    for shifts in itertools.product(
                        range(prime),
                        repeat=4,
                    ):
                        if not projection_holds(
                            distinguished,
                            A,
                            R,
                            shifts,
                            prime,
                        ):
                            continue
                        counts["projection_points"] += 1
                        alpha, beta = family_rows(
                            A,
                            R,
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
                            for mode in {
                                mode for mode, _rows in candidates
                            }
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
                                        R,
                                        shifts,
                                        extension,
                                    )
                                )
        by_prime[str(prime)] = counts
        for key, value in counts.items():
            totals[key] += value

    report = {
        "modular_qa_passed": True,
        "method": (
            "exhaust exact projection-ideal points over F5 and F7; "
            "modular mixed kernels; all projective extension "
            "directions; direct selected-minor tests"
        ),
        "orientations": 4,
        "by_prime": by_prime,
        "totals": totals,
        "complete_modular_projection_point_qa": True,
        "characteristic_zero_exhaustiveness_proved_here": False,
        "characteristic_zero_role": (
            "independent finite-field QA only; see the theorem, primary "
            "component/record reconciliation, four selected unit-ideal "
            "runs, and reconciliation audit"
        ),
        "global": False,
        "theorem_sha256": sha256(THEOREM),
        "primary_sha256": sha256(PRIMARY),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
