#!/usr/bin/env python3
"""Finite-field audit of the complete internal E=0 marked fibre."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from audit_p5_h31_marked_basis_fibre_classification import (  # noqa: E402
    binary_extension_data,
    dot,
    extended_rows,
    linear_combination,
    marked_matrix,
    projective_vectors,
    rank_mod,
)
from derive_p5_h31_toric_marked_fibre_elimination import (  # noqa: E402
    marked_rows,
    toric_cases,
)


THEOREM = HERE / "P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md"
PRIMARY = HERE / "verify_p5_h31_internal_e0_marked_fibre.py"

r, s = sp.symbols("r s")
t0, t1, t2, t3 = sp.symbols("t0:4")

PROJECTION = {
    (0, 0, "finite"): (t3 - 1, t2, t1 * r, t0 * t1),
    (0, 0, "infinity"): (s, t3, t2, t1, t0),
    (0, 2, "finite"): (
        t3 - 1, t2, t1 * (s + 1), t1 * r, t0 * t1,
    ),
    (0, 2, "infinity"): (t2, t1, s * (t3 - 1), t0 * (t3 - 1)),
    (0, 3, "finite"): (
        t2, t1 * (s + 1), t1 * r, t1 * (t3 - 1), t0 * t1,
        (t3 - 1) * (t0 * r + s + 1),
    ),
    (0, 3, "infinity"): (t3, t2, t1, s * (t0 + 1)),
    (1, 0, "finite"): (
        t1, t2 * s, t2 * r, t2 * t3, t0 * t2,
        t3 * (t0 * r + s),
    ),
    (1, 0, "infinity"): (t3 - 1, t2, t1, t0 * s),
    (1, 2, "finite"): (t3, t1, t2 * s, t2 * r, t0 * t2),
    (1, 2, "infinity"): (t2, t1, t3 * s, t3 * (t0 - 1)),
    (1, 3, "finite"): (t3, t1, t2 * r, t0 * t2),
    (1, 3, "infinity"): (s, t3 - 1, t2, t1, t0 - 1),
}

ROW_POOL = (
    (0, 1, 3, 7),
    (0, 1, 4, 7),
    (0, 1, 5, 7),
    (0, 2, 3, 7),
    (0, 2, 4, 7),
    (0, 2, 6, 7),
    (0, 3, 5, 7),
    (0, 3, 6, 7),
    (0, 4, 5, 7),
    (0, 4, 6, 7),
)
CERTIFICATES = tuple(
    (mode, row_indices)
    for mode in range(4)
    for row_indices in ROW_POOL
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows_evaluator(case, chart: str):
    alpha, beta, _ = marked_rows(case, chart)
    function = sp.lambdify(
        (r, s, t0, t1, t2, t3),
        tuple(entry for row in alpha + beta for entry in row),
        modules="math",
    )

    def evaluate(values, prime):
        entries = tuple(int(value) % prime for value in function(*values))
        return (
            tuple(
                tuple(entries[4 * row + column] for column in range(4))
                for row in range(4)
            ),
            tuple(
                tuple(entries[16 + 4 * row + column] for column in range(4))
                for row in range(4)
            ),
        )

    return evaluate


def projected_points(direction, q, chart, prime):
    function = sp.lambdify(
        (r, s, t0, t1, t2, t3),
        PROJECTION[(direction, q, chart)],
        modules="math",
    )
    raw = (
        itertools.product(range(prime), repeat=6)
        if chart == "finite"
        else (
            (0, *values)
            for values in itertools.product(range(prime), repeat=5)
        )
    )
    return tuple(
        values for values in raw
        if all(int(value) % prime == 0 for value in function(*values))
    )


def main() -> None:
    cases = [
        case
        for case in toric_cases(include_internal_e0=True)
        if case.incident_normals == ((-1, 0, 0),)
    ]
    assert len(cases) == 2
    totals = {
        "projection_points": 0,
        "projection_closure_artifacts": 0,
        "binary_extensions": 0,
        "certificate_minor_tests": 0,
    }
    by_prime: dict[str, dict[str, int]] = {}
    for prime in (5, 7):
        counts = {key: 0 for key in totals}
        for direction, case in enumerate(cases):
            for q in case.all_rank:
                for chart in ("finite", "infinity"):
                    evaluator = rows_evaluator(case, chart)
                    for values in projected_points(
                        direction, q, chart, prime,
                    ):
                        counts["projection_points"] += 1
                        alpha, beta = evaluator(values, prime)
                        (
                            _mixed,
                            diagonal_a,
                            diagonal_b,
                            kernel,
                        ) = binary_extension_data(
                            q, alpha, beta, prime,
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
                                row[q] % prime
                                for row in marked_matrix(
                                    mode, alpha, beta, prime,
                                )
                            )
                            for mode in range(4)
                        }
                        for coefficients in projective_vectors(
                            len(kernel), prime,
                        ):
                            extension = linear_combination(
                                coefficients, kernel, prime,
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
                                q, alpha, beta, extension,
                            )
                            matrices = {
                                mode: marked_matrix(
                                    mode, alpha_p, beta_p, prime,
                                )
                                for mode in range(4)
                                if transverse[mode]
                            }
                            excluded = False
                            for mode, row_indices in CERTIFICATES:
                                counts["certificate_minor_tests"] += 1
                                if mode not in matrices:
                                    continue
                                if rank_mod(
                                    [
                                        matrices[mode][row]
                                        for row in row_indices
                                    ],
                                    prime,
                                ) == 4:
                                    excluded = True
                                    break
                            if not excluded:
                                raise AssertionError(
                                    (
                                        "unexcluded extension",
                                        prime,
                                        direction,
                                        q,
                                        chart,
                                        values,
                                        extension,
                                    )
                                )
        by_prime[str(prime)] = counts
        for key, value in counts.items():
            totals[key] += value

    report = {
        "verified": True,
        "method": (
            "exhaust all twelve exact projections over F5 and F7; "
            "modular mixed kernels; every projective extension "
            "direction; direct selected-minor tests"
        ),
        "pure_directions": 2,
        "orientations": (0, 2, 3),
        "charts": 2,
        "by_prime": by_prime,
        "totals": totals,
        "complete_internal_E0_marked_fibre_excluded": True,
        "known_component_marked_fibre_excluded": True,
        "global": False,
        "theorem_sha256": sha256(THEOREM),
        "primary_sha256": sha256(PRIMARY),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
