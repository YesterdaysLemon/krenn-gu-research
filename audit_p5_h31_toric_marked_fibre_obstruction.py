#!/usr/bin/env python3
"""Finite-field audit of the toric marked-fibre obstruction.

This checker is intentionally independent of the symbolic residual-factor
proof.  It evaluates every point of the exact projection strata over F_5
and F_7, computes the mixed kernel by modular row reduction, enumerates all
projective binary extension directions, and tests a small theorem-recorded
set of marked 4-minors directly.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

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
from derive_p5_h31_toric_marked_fibre_elimination import (
    marked_rows,
    toric_cases,
)


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h31_toric_marked_fibre_obstruction.py"

r, s = sp.symbols("r s")
t0, t1, t2, t3 = sp.symbols("t0:4")


PROJECTION_GENERATORS: dict[
    tuple[int, str],
    tuple[sp.Expr, ...],
] = {
    (0, "finite"): (t3, t2, t1),
    (0, "infinity"): (t2, t1, t3 * s, t0 * t3),
    (1, "finite"): (
        t3,
        t2 * s,
        t2 * (t1 + r),
        t0 * t2,
        t0 * (t1 + 1),
    ),
    (1, "infinity"): (t3, t2, t1 + 1),
    (2, "finite"): (sp.Integer(1),),
    (2, "infinity"): (sp.Integer(1),),
    (3, "finite"): (
        t3,
        t1 * s,
        t0 * t1,
        t1 * (t2 * r - 1),
        (t2 - 1) * (t0 * r + s),
    ),
    (3, "infinity"): (t3, t2, t0, t1 * s),
    (4, "finite"): (t2 + 1, t1, t3 * s, t3 * r, t0 * t3),
    (4, "infinity"): (sp.Integer(1),),
    (5, "finite"): (t2, t1 + r, t0, t3 * s),
    (5, "infinity"): (sp.Integer(1),),
    (6, "finite"): (t3, t1 + r, t0, t2 * s),
    (6, "infinity"): (sp.Integer(1),),
    (7, "finite"): (
        t3,
        t2 * s + t0 + t2,
        t1 * (s + 1),
        t2 * r - 1,
        t0 * r + s + 1,
        t0 * t1,
    ),
    (7, "infinity"): (t3, t2, t0 + 1, t1 * s),
    (8, "finite"): (
        t1,
        t3 * (s - 1),
        t2 * s + t0 - t2,
        t2 * r - 1,
        t0 * r + s - 1,
        t0 * t3,
    ),
    (8, "infinity"): (t2, t1, t0 - 1, t3 * s),
    (9, "finite"): (t3, t2, t1),
    (9, "infinity"): (t2, t1, t3 * s, t0 * t3),
    (10, "finite"): (t3, t1, t2 * s, t2 * r, t0 * t2),
    (10, "infinity"): (t3, t2, t1),
    (11, "finite"): (t3, t2, t1),
    (11, "infinity"): (t3, t2, t1 * s, t0 * t1),
    (12, "finite"): (t2, t1, t3 * s, t3 * r, t0 * t3),
    (12, "infinity"): (t3, t2, t1),
    (13, "finite"): (t2, t1 + r, t0, t3 * s),
    (13, "infinity"): (sp.Integer(1),),
    (14, "finite"): (t3, t1 + r, t0, t2 * s),
    (14, "infinity"): (sp.Integer(1),),
    (15, "finite"): (
        t3,
        t2 * s + t0,
        t1 * s,
        t2 * r - 1,
        t0 * r + s,
        t0 * t1,
    ),
    (15, "infinity"): (t3, t2, t0, t1 * s),
    (16, "finite"): (
        t1,
        t3 * s,
        t2 * s + t0,
        t2 * r - 1,
        t0 * r + s,
        t0 * t3,
    ),
    (16, "infinity"): (t2, t1, t0, t3 * s),
}

PROJECTION_OVERRIDES: dict[
    tuple[int, int, str],
    tuple[sp.Expr, ...],
] = {
    (5, 1, "finite"): (t2, t1 - r, t0, t3 * s),
    (6, 1, "finite"): (t3, t1 - r, t0, t2 * s),
    (7, 2, "finite"): (
        t3,
        t2 * s - t0 + t2,
        t1 * (s + 1),
        t2 * r + 1,
        t0 * r + s + 1,
        t0 * t1,
    ),
    (7, 3, "finite"): (
        t3,
        t2 * s - t0 + t2,
        t1 * (s + 1),
        t2 * r + 1,
        t0 * r + s + 1,
        t0 * t1,
    ),
    (8, 2, "finite"): (
        t1,
        t3 * (s - 1),
        t2 * s - t0 - t2,
        t2 * r + 1,
        t0 * r + s - 1,
        t0 * t3,
    ),
    (8, 3, "finite"): (
        t1,
        t3 * (s - 1),
        t2 * s - t0 - t2,
        t2 * r + 1,
        t0 * r + s - 1,
        t0 * t3,
    ),
}


CERTIFICATES: dict[
    tuple[int, str],
    tuple[tuple[int, tuple[int, int, int, int]], ...],
] = {
    (0, "finite"): ((2, (0, 1, 4, 7)),),
    (0, "infinity"): ((1, (0, 2, 3, 7)),),
    (1, "finite"): (
        (1, (0, 1, 3, 7)),
        (3, (0, 1, 4, 7)),
        (3, (0, 1, 3, 7)),
    ),
    (1, "infinity"): ((3, (0, 1, 3, 7)),),
    (2, "finite"): (),
    (2, "infinity"): (),
    (3, "finite"): (
        (2, (0, 1, 3, 7)),
        (2, (0, 1, 5, 7)),
        (3, (0, 2, 3, 7)),
        (3, (0, 4, 5, 7)),
    ),
    (3, "infinity"): ((3, (0, 4, 5, 7)),),
    (4, "finite"): (
        (1, (0, 1, 3, 7)),
        (2, (0, 2, 3, 7)),
    ),
    (4, "infinity"): (),
    (5, "finite"): ((2, (0, 1, 4, 7)),),
    (5, "infinity"): (),
    (6, "finite"): ((3, (0, 1, 4, 7)),),
    (6, "infinity"): (),
    (7, "finite"): ((3, (0, 2, 4, 7)),),
    (7, "infinity"): ((3, (0, 2, 4, 7)),),
    (8, "finite"): ((1, (0, 1, 4, 7)),),
    (8, "infinity"): ((1, (0, 1, 4, 7)),),
    (9, "finite"): ((2, (0, 1, 3, 7)),),
    (9, "infinity"): ((1, (0, 2, 3, 7)),),
    (10, "finite"): (
        (3, (0, 1, 3, 7)),
        (1, (0, 1, 3, 7)),
    ),
    (10, "infinity"): ((3, (0, 1, 3, 7)),),
    (11, "finite"): ((3, (0, 2, 3, 7)),),
    (11, "infinity"): ((2, (0, 1, 3, 7)),),
    (12, "finite"): (
        (1, (0, 1, 3, 7)),
        (2, (0, 2, 3, 7)),
    ),
    (12, "infinity"): ((1, (0, 1, 3, 7)),),
    (13, "finite"): ((2, (0, 1, 4, 7)),),
    (13, "infinity"): (),
    (14, "finite"): ((3, (0, 1, 4, 7)),),
    (14, "infinity"): (),
    (15, "finite"): ((3, (0, 2, 4, 7)),),
    (15, "infinity"): ((3, (0, 2, 4, 7)),),
    (16, "finite"): ((1, (0, 1, 4, 7)),),
    (16, "infinity"): ((1, (0, 1, 4, 7)),),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows_evaluator(case_id: int, chart: str):
    alpha, beta, _ = marked_rows(toric_cases()[case_id], chart)
    variables = (r, s, t0, t1, t2, t3)
    function = sp.lambdify(
        variables,
        tuple(entry for row in alpha + beta for entry in row),
        modules="math",
    )

    def evaluate(
        values: tuple[int, int, int, int, int, int],
        prime: int,
    ) -> tuple[
        tuple[tuple[int, ...], ...],
        tuple[tuple[int, ...], ...],
    ]:
        flat = tuple(int(value) % prime for value in function(*values))
        return (
            tuple(
                tuple(flat[4 * row + column] for column in range(4))
                for row in range(4)
            ),
            tuple(
                tuple(flat[16 + 4 * row + column] for column in range(4))
                for row in range(4)
            ),
        )

    return evaluate


def projected_points(
    case_id: int,
    distinguished: int,
    chart: str,
    prime: int,
) -> tuple[tuple[int, int, int, int, int, int], ...]:
    generators = PROJECTION_OVERRIDES.get(
        (case_id, distinguished, chart),
        PROJECTION_GENERATORS[(case_id, chart)],
    )
    function = sp.lambdify(
        (r, s, t0, t1, t2, t3),
        generators,
        modules="math",
    )
    if chart == "finite":
        raw = itertools.product(range(prime), repeat=6)
    else:
        raw = (
            (0, *values)
            for values in itertools.product(range(prime), repeat=5)
        )
    return tuple(
        values
        for values in raw
        if all(int(value) % prime == 0 for value in function(*values))
    )


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
            other: (
                beta[other]
                if bits[index]
                else alpha[other]
            )
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
    cases = toric_cases()
    assert len(cases) == 17
    assert sum(len(case.all_rank) for case in cases) == 39
    assert set(PROJECTION_GENERATORS) == {
        (case_id, chart)
        for case_id in range(17)
        for chart in ("finite", "infinity")
    }
    assert set(CERTIFICATES) == set(PROJECTION_GENERATORS)
    assert all(
        distinguished in cases[case_id].all_rank
        for case_id, distinguished, _chart in PROJECTION_OVERRIDES
    )

    totals = {
        "projection_points": 0,
        "marking_orientations": 0,
        "projection_closure_artifacts": 0,
        "binary_extensions": 0,
        "certificate_minor_tests": 0,
    }
    by_prime: dict[str, dict[str, int]] = {}
    for prime in (5, 7):
        prime_counts = {key: 0 for key in totals}
        for case in cases:
            for chart in ("finite", "infinity"):
                evaluator = rows_evaluator(case.case_id, chart)
                candidates = CERTIFICATES[(case.case_id, chart)]
                for distinguished in case.all_rank:
                    points = projected_points(
                        case.case_id,
                        distinguished,
                        chart,
                        prime,
                    )
                    prime_counts["projection_points"] += len(points)
                    for values in points:
                        alpha, beta = evaluator(values, prime)
                        prime_counts["marking_orientations"] += 1
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
                            prime_counts[
                                "projection_closure_artifacts"
                            ] += 1
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
                                dot(diagonal_a, list(extension), prime) == 0
                                or dot(
                                    diagonal_b,
                                    list(extension),
                                    prime,
                                )
                                == 0
                            ):
                                continue
                            prime_counts["binary_extensions"] += 1
                            alpha_p, beta_p = extended_rows(
                                distinguished,
                                alpha,
                                beta,
                                extension,
                            )
                            excluded = False
                            for mode, row_indices in candidates:
                                prime_counts[
                                    "certificate_minor_tests"
                                ] += 1
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
                                        "unexcluded binary extension",
                                        prime,
                                        case.case_id,
                                        distinguished,
                                        chart,
                                        values,
                                        extension,
                                    )
                                )
        by_prime[str(prime)] = prime_counts
        for key, value in prime_counts.items():
            totals[key] += value

    report = {
        "verified": True,
        "method": (
            "exhaust exact projection strata over F5 and F7; modular "
            "mixed kernels; all projective binary extension directions; "
            "direct marked-minor tests"
        ),
        "toric_direction_types": len(cases),
        "pure_direction_orientation_types": sum(
            len(case.all_rank) for case in cases
        ),
        "base_orbit_orientation_cases": 21,
        "charts": 2,
        "by_prime": by_prime,
        "totals": totals,
        "theorem_sha256": sha256(THEOREM),
        "primary_sha256": sha256(PRIMARY),
        "global": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
