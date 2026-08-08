#!/usr/bin/env python3
"""Independent modular audit of weighted H22 on the 1+3 components."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

import sys

# Stage 9 moved the H22 mixed-orientation generic package into
# claims/p5/h22/mixed-orientation/; expose it through the shared
# helper so the bare-name import below resolves.
for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import expose_claim_package  # noqa: E402

expose_claim_package(
    Path(__file__).resolve().parent, "claims/p5/h22/mixed-orientation")
from audit_p5_h22_mixed_orientation_component_generic_obstruction import (
    determinant_mod,
    diagonal_row,
    dot,
    extension_matrices,
    one_marked_map,
    permanent,
    rref_nullspace,
)
from audit_p5_h31_one_three_component_generic_obstruction import (
    canonical_basis_mod,
    shifted_basis_mod,
)


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h22_one_three_components_generic_obstruction.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PARAMETERS = {
    "L1": (1, 2, 2),
    "L2": (1, 2, 1),
    "L3": (1, 2, 2),
}
EXPECTED_SURVIVORS = {
    5: {"L1": {"01": 0, "23": 1}, "L2": {"01": 0, "23": 10},
        "L3": {"01": 0, "23": 0}},
    7: {"L1": {"01": 0, "23": 2}, "L2": {"01": 0, "23": 16},
        "L3": {"01": 0, "23": 0}},
}
FITTING_ROWS = (0, 2, 4, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def projection_values(branch, shifts, S, D, G, modulus: int):
    t0, t1, t2, t3 = shifts
    if branch == "L1":
        return (
            S * t2
            + G * (D - S) * t3
            + (D - S) * (S + G),
            (S - D + G) * t1
            + D * (S - D) * t3
            + (D - S) * (S - D + G),
            (S + G) * t0 + 1,
            t3 * (t3 + 1),
        )
    if branch == "L2":
        return (
            (D + G) * t0 + 1,
            t2 * t3,
            t1 * (t3 + 1),
            t1 * t2,
        )
    raise ValueError(branch)


def sheet_membership(branch, shifts, S, D, G, modulus: int):
    t0, t1, t2, t3 = shifts
    if branch == "L1":
        return {
            "A": (
                ((S + G) * t0 + 1) % modulus == 0
                and (t1 - (S - D)) % modulus == 0
                and (
                    S * t2 - (S - D) * (S + G)
                )
                % modulus
                == 0
                and t3 == 0
            ),
            "B": (
                ((S + G) * t0 + 1) % modulus == 0
                and (
                    (S - D + G) * t1
                    - (S - D) * (S + G)
                )
                % modulus
                == 0
                and (t2 - (S - D)) % modulus == 0
                and (t3 + 1) % modulus == 0
            ),
        }
    if branch == "L2":
        common = ((D + G) * t0 + 1) % modulus == 0
        return {
            "A": common and t1 == 0 and t2 == 0,
            "B": common and t1 == 0 and t3 == 0,
            "C": common and t2 == 0 and (t3 + 1) % modulus == 0,
        }
    raise ValueError(branch)


def marked_minor(
    alpha,
    beta,
    extension,
    slope,
    modulus: int,
):
    alpha_d = tuple(
        diagonal_row(
            alpha[mode],
            extension[mode],
            "23",
            slope,
            modulus,
        )
        for mode in range(4)
    )
    beta_d = tuple(
        diagonal_row(
            beta[mode],
            extension[4 + mode],
            "23",
            slope,
            modulus,
        )
        for mode in range(4)
    )
    marked = one_marked_map(0, alpha_d, beta_d, modulus)
    rank, _ = rref_nullspace(marked, modulus)
    determinant = determinant_mod(
        [marked[row] for row in FITTING_ROWS],
        modulus,
    )
    return rank, determinant


def audit_branch(branch: str, modulus: int):
    S, D, G = PARAMETERS[branch]
    slope = 2
    alpha, beta = canonical_basis_mod(branch, S, D, G, modulus)
    diagonals = {}
    for diagonal in ("01", "23"):
        rank_distribution = Counter()
        survivors = []
        for shifts in itertools.product(range(modulus), repeat=4):
            marked_beta = shifted_basis_mod(
                alpha,
                beta,
                shifts,
                modulus,
            )
            mixed, first, second = extension_matrices(
                alpha,
                marked_beta,
                diagonal,
                slope,
                modulus,
            )
            rank, kernel = rref_nullspace(mixed, modulus)
            rank_distribution[(rank, len(kernel))] += 1
            first_live = any(
                dot(first, vector, modulus) for vector in kernel
            )
            second_live = any(
                dot(second, vector, modulus) for vector in kernel
            )
            if not (first_live and second_live):
                continue
            assert diagonal == "23"
            assert branch in ("L1", "L2")
            assert rank == 7 and len(kernel) == 1
            assert all(
                value % modulus == 0
                for value in projection_values(
                    branch,
                    shifts,
                    S,
                    D,
                    G,
                    modulus,
                )
            )
            sheets = sheet_membership(
                branch,
                shifts,
                S,
                D,
                G,
                modulus,
            )
            assert any(sheets.values())
            marked_rank, determinant = marked_minor(
                alpha,
                marked_beta,
                kernel[0],
                slope,
                modulus,
            )
            assert marked_rank == 4
            assert determinant != 0
            survivors.append(
                {
                    "shifts": list(shifts),
                    "mixed_rank": rank,
                    "covering_sheets": [
                        sheet
                        for sheet, contains in sheets.items()
                        if contains
                    ],
                    "mode_zero_0247_minor": determinant,
                    "mode_zero_marked_rank": marked_rank,
                }
            )
        expected = EXPECTED_SURVIVORS[modulus][branch][diagonal]
        assert len(survivors) == expected
        diagonals[diagonal] = {
            "markings_tested": modulus**4,
            "rank_distribution": {
                f"{rank}/{kernel_dimension}": count
                for (rank, kernel_dimension), count
                in sorted(rank_distribution.items())
            },
            "genuine_survivor_count": len(survivors),
            "survivors": survivors,
        }
    return {
        "parameters_S_D_G": [S, D, G],
        "slope": slope,
        "diagonals": diagonals,
    }


def main() -> None:
    audits = {}
    for modulus in (5, 7):
        branch_audits = {}
        for branch in ("L1", "L2", "L3"):
            S, D, G = PARAMETERS[branch]
            alpha, beta = canonical_basis_mod(
                branch,
                S,
                D,
                G,
                modulus,
            )
            pure = {
                bits: permanent(
                    tuple(
                        beta[mode] if bits[mode] else alpha[mode]
                        for mode in range(4)
                    ),
                    modulus,
                )
                for bits in WORDS
            }
            expected = {
                "L1": 4 * D * G,
                "L2": 4 * D * (D + G - S),
                "L3": -4 * D * S,
            }[branch] % modulus
            assert pure[(1, 1, 1, 1)] == expected != 0
            assert all(
                value == 0
                for bits, value in pure.items()
                if bits != (1, 1, 1, 1)
            )
            branch_audits[branch] = audit_branch(branch, modulus)
        audits[str(modulus)] = branch_audits

    result = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "finite-field marked-basis census using independent modular "
            "canonical bases, DP permanents, nullspaces, and one minor"
        ),
        "moduli": [5, 7],
        "audits": audits,
        "all_empty_binary_projections_replayed": True,
        "L1_two_sheet_pattern_replayed": True,
        "L2_three_line_cover_replayed": True,
        "mode_zero_0247_nonzero_on_every_genuine_survivor": True,
        "finite_field_results_are_corroboration_only": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h22_one_three_components_generic_obstruction_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
