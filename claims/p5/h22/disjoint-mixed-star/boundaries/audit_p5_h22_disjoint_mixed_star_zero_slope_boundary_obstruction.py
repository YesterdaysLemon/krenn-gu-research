#!/usr/bin/env python3
"""Independent modular audit of the zero-slope H22 boundary.

The finite-field census is corroboration only, not a proof over C.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import (  # noqa: E402
    bootstrap,
    expose_claim_package,
)

REPO_ROOT, HERE = bootstrap(__file__, also=[".."])

# Stage 9 moved the H31 disjoint-mixed-star generic package into
# claims/p5/h31/disjoint-mixed-star/; expose it through the shared
# helper so the bare-name import below resolves.
expose_claim_package(REPO_ROOT, "claims/p5/h31/disjoint-mixed-star")
expose_claim_package(REPO_ROOT, "claims/p5/h31/marked-basis-open-branch")

import audit_p5_h31_disjoint_mixed_star_component_generic_obstruction as A
from audit_p5_h31_marked_basis_open_branch import rank_mod
import explore_p5_h22_disjoint_mixed_star_modular as E


SAMPLES = (
    (11, (1, 2, 7, 3)),
    (13, (1, 3, 5, 10)),
)
SLOPE = 0
MINORS = ((0, 1, 3, 7), (0, 1, 5, 7))


def audit_case(modulus: int, sample, direction: str) -> dict[str, object]:
    A.SAMPLES[modulus] = sample
    parameters, alpha, canonical_beta = A.component_basis(modulus)
    genuine_markings = 0
    genuine_directions = 0
    mixed_ranks: set[int] = set()
    marked_ranks: set[int] = set()
    for shifts in itertools.product(range(modulus), repeat=4):
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
            SLOPE,
            modulus,
        )
        rank, kernel = A.rref_nullspace(mixed, modulus)
        local_genuine = 0
        for projective in A.projective_directions(
            len(kernel), modulus
        ):
            extension = A.combine(projective, kernel, modulus)
            if not (
                A.dot(first, extension, modulus)
                and A.dot(second, extension, modulus)
            ):
                continue
            local_genuine += 1
            genuine_directions += 1
            if direction == "01":
                raise AssertionError(
                    (
                        "D01 zero-slope binary obstruction failed",
                        modulus,
                        shifts,
                        extension,
                    )
                )
            _values, alpha_d, beta_d = E.coefficients(
                alpha,
                beta,
                direction,
                SLOPE,
                extension,
                modulus,
            )
            marked = A.one_marked_map(
                0,
                alpha_d,
                beta_d,
                modulus,
            )
            marked_rank = rank_mod(marked, modulus)
            marked_ranks.add(marked_rank)
            minors = tuple(
                A.determinant_mod(
                    [
                        [
                            marked[row][column]
                            for column in range(4)
                        ]
                        for row in rows
                    ],
                    modulus,
                )
                for rows in MINORS
            )
            assert any(minors), (
                modulus,
                shifts,
                extension,
                minors,
            )
            assert marked_rank == 4
        if local_genuine:
            genuine_markings += 1
            mixed_ranks.add(rank)
    if direction == "01":
        assert genuine_markings == genuine_directions == 0
    else:
        assert genuine_markings == 1
        assert genuine_directions == modulus - 1
        assert mixed_ranks == {6}
        assert marked_ranks == {4}
    return {
        "modulus": modulus,
        "component_point": list(parameters),
        "direction": direction,
        "slope": SLOPE,
        "markings": modulus**4,
        "genuine_markings": genuine_markings,
        "genuine_projective_directions": genuine_directions,
        "mixed_ranks_on_genuine_markings": sorted(mixed_ranks),
        "mode_zero_marked_ranks": sorted(marked_ranks),
    }


def main() -> None:
    cases = [
        audit_case(modulus, sample, direction)
        for modulus, sample in SAMPLES
        for direction in ("01", "23")
    ]
    result = {
        "scope": "finite-field corroboration only",
        "imports_primary_verifier": False,
        "cases": cases,
        "audited": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_zero_slope_audited.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
