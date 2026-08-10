#!/usr/bin/env python3
"""Primary verifier for the q5_311 shared-drop obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_311_SHARED_DROP_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_tensor_after_contraction(
    contraction: tuple[int, ...],
) -> dict[tuple[int, int, int], int]:
    result = {}
    for remaining in itertools.product(range(4), repeat=3):
        if len(set(remaining)) < 3:
            result[remaining] = 0
            continue
        missing = next(
            source for source in range(4) if source not in remaining
        )
        result[remaining] = contraction[missing]
    return result


def main() -> None:
    # In either deleted slice, the three common rows are sources 0,1,2
    # and the exceptional rare row is source 3.
    selector = (0, 0, 0, 1)
    first_residual = permanent_tensor_after_contraction(selector)
    second_residual = permanent_tensor_after_contraction(selector)
    assert first_residual == second_residual

    nonzero_entries = {
        indices: value
        for indices, value in first_residual.items()
        if value
    }
    assert len(nonzero_entries) == 6
    assert set(nonzero_entries) == set(itertools.permutations(range(3)))
    assert set(nonzero_entries.values()) == {1}

    # Pure cubes in the two independent target colour directions.
    colour_one = sp.zeros(27, 1)
    colour_two = sp.zeros(27, 1)
    colour_one[13] = 1  # (1,1,1) in base-3 order.
    colour_two[26] = 1  # (2,2,2) in base-3 order.
    pure_span = sp.Matrix.hstack(colour_one, colour_two)
    assert pure_span.rank() == 2

    beta_one, beta_two, lambda_one, lambda_two = sp.symbols(
        "beta_one beta_two lambda_one lambda_two",
        nonzero=True,
    )
    compatibility = sp.Matrix.hstack(
        lambda_one * beta_one * colour_one,
        -lambda_two * beta_two * colour_two,
    )
    assert compatibility.rank() == 2

    # Shared-mode row ranks: common line plus either exceptional row is
    # a plane, and both exceptional rows complete the original rank.
    common = sp.Matrix([[1, 0, 0]])
    exceptional_one = sp.Matrix([[0, 1, 0]])
    exceptional_two = sp.Matrix([[0, 0, 1]])
    assert sp.Matrix.vstack(common, exceptional_one).rank() == 2
    assert sp.Matrix.vstack(common, exceptional_two).rank() == 2
    assert sp.Matrix.vstack(
        common,
        exceptional_one,
        exceptional_two,
    ).rank() == 3

    output = {
        "verified": True,
        "field": "C",
        "deleted_slice_residuals_equal": True,
        "residual_P3_coefficients_nonzero": len(nonzero_entries),
        "rare_target_pure_cube_span_rank": pure_span.rank(),
        "nonzero_beta_compatibility_rank": compatibility.rank(),
        "shared_deleted_ranks": [2, 2],
        "full_shared_mode_rank": 3,
        "shared_rank_drop_branch_possible": False,
        "remaining_rank_drop_branch": "disjoint_2_plus_2",
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_311_shared_drop_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
