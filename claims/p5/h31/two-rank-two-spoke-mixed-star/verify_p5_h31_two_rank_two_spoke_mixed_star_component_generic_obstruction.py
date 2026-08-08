#!/usr/bin/env python3
"""Verify the generic H31 obstruction on the tenth pure-P4 component."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sys

import sympy as sp

# The two-rank-two-spoke mixed-star P4 classification package moved in
# Stage 6; expose it through the shared helper so the bare-name import
# below resolves.
for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(
    REPO_ROOT,
    "claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component")
from verify_p4_two_rank_two_spoke_mixed_star_component import family  # noqa: E402
from verify_p5_h31_marked_basis_open_branch import mixed_matrix


ROOT = REPO_ROOT
THEOREM = (
    HERE
    / "P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = ROOT / "claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md"
CLASSIFICATION = ROOT / "claims/p4/classifications/star/two-rank-two-spoke-mixed-star-classification/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def marked_rows(planes, shifts):
    alpha = tuple(
        tuple(planes[mode][0, coordinate] for coordinate in range(4))
        for mode in range(4)
    )
    beta = tuple(
        tuple(
            sp.expand(
                planes[mode][1, coordinate]
                + shifts[mode] * planes[mode][0, coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def row_module_test(
    distinguished: int,
    mixed: sp.Matrix,
    diagonal_alpha: sp.Matrix,
    diagonal_beta: sp.Matrix,
) -> dict[str, int | bool]:
    generators = ",".join(
        "[" + ",".join(singular(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_vector = "[" + ",".join(
        singular(diagonal_alpha[0, column]) for column in range(8)
    ) + "]"
    beta_vector = "[" + ",".join(
        singular(diagonal_beta[0, column]) for column in range(8)
    ) + "]"
    program = "\n".join(
        (
            "ring R=(0,s,t),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "vector a=" + alpha_vector + ";",
            "vector b=" + beta_vector + ";",
            "vector ra=reduce(a,M);",
            "vector rb=reduce(b,M);",
            "int azero=(ra==0);",
            "int bnonzero=(rb!=0);",
            (
                '"CODEX_RESULT:"+string(azero)+":"'
                '+string(bnonzero)+":"+string(size(M));'
            ),
            "quit;",
        )
    )
    completed = subprocess.run(
        SINGULAR,
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=60,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular row-module failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(results) == 1, completed.stdout
    _, alpha_zero, beta_nonzero, basis_size = results[0].split(":")
    assert alpha_zero == "1"
    assert beta_nonzero == "1"
    assert basis_size == "10"
    return {
        "all_alpha_remainder_zero": True,
        "all_beta_remainder_nonzero": True,
        "reduced_module_basis_size": int(basis_size),
    }


def main() -> None:
    s, t = sp.symbols("s t")
    shifts = sp.symbols("h0:4")
    planes = family(s, t)
    alpha, beta = marked_rows(planes, shifts)

    pure = {
        word: sp.factor(
            permanent(
                tuple(
                    beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] + 4 * (s + t)) == 0
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    kernels = (
        sp.Matrix(
            (
                -1,
                s - 1,
                t - 1,
                0,
                -shifts[0],
                shifts[1] * (s - 1) + s,
                shifts[2] * (t - 1) + t,
                (s - 1) * (t - 1),
            )
        ),
        sp.Matrix(
            (
                -1,
                -s - 1,
                -t - 1,
                0,
                -shifts[0],
                -shifts[1] * (s + 1) - s,
                -shifts[2] * (t + 1) - t,
                -(s + 1) * (t + 1),
            )
        ),
        sp.Matrix(
            (
                -1,
                0,
                -2,
                -1,
                -shifts[0] - 1,
                -1,
                -2 * shifts[2] - 1,
                -shifts[3] + s + t,
            )
        ),
        sp.Matrix(
            (
                1,
                2,
                0,
                -1,
                shifts[0] + 1,
                2 * shifts[1] + 1,
                1,
                -shifts[3] - s - t,
            )
        ),
    )
    expected_beta = (4 * (s + t),) * 3 + (-4 * (s + t),)

    module_results = []
    for distinguished, (kernel, expected) in enumerate(
        zip(kernels, expected_beta, strict=True)
    ):
        mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
            distinguished, alpha, beta
        )
        assert all(sp.factor(entry) == 0 for entry in mixed * kernel)
        assert sp.factor((diagonal_alpha * kernel)[0]) == 0
        assert sp.factor((diagonal_beta * kernel)[0] - expected) == 0
        module_results.append(
            row_module_test(
                distinguished,
                mixed,
                diagonal_alpha,
                diagonal_beta,
            )
        )

    result = {
        "all_four_deleted_coordinates": True,
        "all_markings_over_component_function_field": True,
        "binary_neighbour_excluded": True,
        "component_function_field": "C(s,t)",
        "explicit_kernel_beta_diagonals": [
            "4*(s+t)",
            "4*(s+t)",
            "4*(s+t)",
            "-4*(s+t)",
        ],
        "marking_ring": "C(s,t)[h0,h1,h2,h3]",
        "method": "exact polynomial row-module membership",
        "module_results": module_results,
        "search_used": False,
        "theorem": THEOREM.name,
        "verified": True,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            CLASSIFICATION.name: sha256(CLASSIFICATION),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
