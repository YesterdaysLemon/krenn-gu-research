#!/usr/bin/env python3
"""Independent modular audit of weighted H22 on the first component."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from audit_p5_h22_mixed_orientation_component_generic_obstruction import (
    determinant_mod,
    diagonal_row,
    dot,
    extension_matrices,
    one_marked_map,
    permanent,
    rref_nullspace,
)
from audit_p5_h31_marked_basis_fibre_classification import family_rows


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h22_first_rank_two_component_generic_obstruction.py"
SAMPLES = {
    5: (1, 1, 3, 2),
    7: (1, 1, 2, 2),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sheet_marking(L, Q, C, r, sheet: str, modulus: int):
    Z = Q * (L + C) * (r + 1) % modulus
    H = (Z - r + 1) % modulus
    U = (
        L * Q * Z + 2 * L * Q + Q * C * (r + 1) - r + 1
    ) % modulus
    P = (
        C
        * (
            L * Q * (r + 1) * (Z - r + 2)
            + Q * C * (r + 1)
            - r
            + 1
        )
    ) % modulus
    R = L**2 * (r - 1) * (Z + 1) % modulus
    E = L * C * (r - 1 - Z) % modulus
    assert P and Q and U and r != 1
    t3 = 0 if sheet == "A" else -H * pow(r - 1, -1, modulus) % modulus
    t2 = -(R * t3 + E) * pow(P, -1, modulus) % modulus
    t0 = -((r - 1) * t3 + U) * pow(Q * U, -1, modulus) % modulus
    return (t0, 0, t2, t3)


def audit_sample(modulus: int):
    L, Q, C, slope = SAMPLES[modulus]
    d01_distribution = {}
    for shifts in itertools.product(range(modulus), repeat=4):
        alpha, beta = family_rows(L, Q, C, shifts, modulus)
        mixed, _first, _second = extension_matrices(
            alpha,
            beta,
            "01",
            slope,
            modulus,
        )
        rank, kernel = rref_nullspace(mixed, modulus)
        assert rank == 8 and not kernel
        d01_distribution[rank] = d01_distribution.get(rank, 0) + 1

    sheets = []
    for sheet, minor_rows in (
        ("A", (0, 1, 4, 7)),
        ("B", (0, 1, 3, 7)),
    ):
        shifts = sheet_marking(L, Q, C, slope, sheet, modulus)
        alpha, beta = family_rows(L, Q, C, shifts, modulus)
        mixed, first, second = extension_matrices(
            alpha,
            beta,
            "23",
            slope,
            modulus,
        )
        rank, kernel = rref_nullspace(mixed, modulus)
        assert rank == 7 and len(kernel) == 1
        direction = kernel[0]
        assert dot(first, direction, modulus)
        assert dot(second, direction, modulus)
        alpha_d = tuple(
            diagonal_row(
                alpha[mode],
                direction[mode],
                "23",
                slope,
                modulus,
            )
            for mode in range(4)
        )
        beta_d = tuple(
            diagonal_row(
                beta[mode],
                direction[4 + mode],
                "23",
                slope,
                modulus,
            )
            for mode in range(4)
        )
        marked = one_marked_map(2, alpha_d, beta_d, modulus)
        marked_rank, _ = rref_nullspace(marked, modulus)
        determinant = determinant_mod(
            [marked[row] for row in minor_rows],
            modulus,
        )
        assert marked_rank == 4
        assert determinant
        sheets.append(
            {
                "sheet": sheet,
                "shifts": list(shifts),
                "mixed_rank": rank,
                "kernel_dimension": 1,
                "minor_rows": list(minor_rows),
                "selected_minor": determinant,
                "mode_two_marked_rank": marked_rank,
            }
        )

    return {
        "modulus": modulus,
        "sample_L_Q_C_slope": [L, Q, C, slope],
        "D01": {
            "markings_tested": modulus**4,
            "rank_distribution": {
                str(rank): count
                for rank, count in sorted(d01_distribution.items())
            },
            "all_mixed_ranks_eight": True,
        },
        "D23": {
            "exact_sheets_checked": sheets,
            "both_sheets_rank_four": True,
        },
    }


def main() -> None:
    audits = []
    for modulus in SAMPLES:
        L, Q, C, _slope = SAMPLES[modulus]
        alpha, beta = family_rows(
            L,
            Q,
            C,
            (0, 0, 0, 0),
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
            for bits in itertools.product((0, 1), repeat=4)
        }
        assert pure[(1, 1, 1, 1)] == 2 * (C + L) % modulus != 0
        assert all(
            value == 0
            for bits, value in pure.items()
            if bits != (1, 1, 1, 1)
        )
        audits.append(audit_sample(modulus))

    result = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "full modular D01 marking census and direct reconstruction "
            "of the two exact D23 sheets"
        ),
        "audits": audits,
        "D01_full_rank_replayed": True,
        "D23_two_sheet_rank_four_obstruction_replayed": True,
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
        / "p5_h22_first_rank_two_component_generic_obstruction_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
