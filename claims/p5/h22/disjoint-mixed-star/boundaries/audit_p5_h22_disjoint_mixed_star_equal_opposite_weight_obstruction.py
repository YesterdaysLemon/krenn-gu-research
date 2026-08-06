#!/usr/bin/env python3
"""Independent finite-field audit of the r=+/-1 H22 obstruction.

This exhaustive small-field audit is corroboration only.  It does not
prove the characteristic-zero theorem.
"""

from __future__ import annotations

import itertools
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=[".."])

import audit_p5_h31_disjoint_mixed_star_component_generic_obstruction as A
import explore_p5_h22_disjoint_mixed_star_modular as E


SAMPLES = {
    7: (1, 1, 1, 1),
    11: (1, 2, 7, 3),
}
SLOPES = (1, -1)
DIRECTIONS = ("01", "23")


def audit_field(modulus: int) -> dict[str, object]:
    A.SAMPLES[modulus] = SAMPLES[modulus]
    parameters, alpha, canonical_beta = A.component_basis(modulus)
    cases = []
    for slope in SLOPES:
        reduced_slope = slope % modulus
        for direction in DIRECTIONS:
            rank_drop_count = 0
            first_diagonal_zero_count = 0
            second_diagonal_zero_count = 0
            genuine_count = 0
            marking_count = 0
            for shifts in itertools.product(range(modulus), repeat=4):
                marking_count += 1
                beta = tuple(
                    tuple(
                        (
                            canonical_beta[mode][coordinate]
                            + shifts[mode] * alpha[mode][coordinate]
                        )
                        % modulus
                        for coordinate in range(4)
                    )
                    for mode in range(4)
                )
                mixed, first, second = E.matrices(
                    alpha,
                    beta,
                    direction,
                    reduced_slope,
                    modulus,
                )
                rank, kernel = A.rref_nullspace(mixed, modulus)
                if rank == 8:
                    continue
                rank_drop_count += 1
                first_active = any(
                    A.dot(first, vector, modulus) for vector in kernel
                )
                second_active = any(
                    A.dot(second, vector, modulus) for vector in kernel
                )
                if not first_active:
                    first_diagonal_zero_count += 1
                if not second_active:
                    second_diagonal_zero_count += 1
                if first_active and second_active:
                    genuine_count += 1
            assert marking_count == modulus**4
            assert genuine_count == 0
            assert rank_drop_count > 0
            cases.append(
                {
                    "direction": direction,
                    "slope": slope,
                    "markings": marking_count,
                    "rank_drop_markings": rank_drop_count,
                    "first_diagonal_zero_on_kernel": (
                        first_diagonal_zero_count
                    ),
                    "second_diagonal_zero_on_kernel": (
                        second_diagonal_zero_count
                    ),
                    "genuine_binary_incidence": genuine_count,
                }
            )
    return {
        "modulus": modulus,
        "component_point": list(parameters),
        "cases": cases,
    }


def main() -> None:
    with ThreadPoolExecutor(max_workers=2) as executor:
        fields = list(executor.map(audit_field, (7, 11)))
    result = {
        "scope": "finite-field corroboration only",
        "imports_primary_verifier": False,
        "fields": fields,
        "audited": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_equal_opposite_weight_audited.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
