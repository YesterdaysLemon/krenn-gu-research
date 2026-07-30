#!/usr/bin/env python3
"""Verify the generic H31 obstruction on the six-dimensional component."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

from p5_high_coordinate_tree_chart_cegar import singular_command_with_timeout
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = ROOT / "P4_SIX_DIMENSIONAL_PURE_COMPONENT.md"
COMPONENT_PRIMARY = ROOT / "verify_p4_six_dimensional_pure_component.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

EXPECTED_PROJECTIONS = {
    0: (
        "t3",
        "(u-v)*t2+(-s*v)",
        "(u-v)*t1+(u-1)",
        "t0-1",
    ),
    1: ("1",),
    2: (
        "t3-1",
        "(u-v)*t2+(-s*v)",
        "(u-v)*t1+(u-1)",
        "t0",
    ),
    3: (
        "t3",
        "(u-v)*t2+(-s*v)",
        "(u-v)*t1+(u-1)",
        "t0",
    ),
}

FITTING_ROWS = {
    0: ((0, 1, 2, 7), (0, 1, 3, 7), (0, 1, 4, 7)),
    2: ((0, 2, 6, 7), (0, 3, 6, 7), (0, 4, 6, 7)),
    3: ((0, 1, 2, 7), (0, 1, 3, 7), (0, 1, 4, 7)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def canonical_basis():
    s, d, u, v = sp.symbols("s d u v")
    h = s - d
    planes = (
        ((1, 0, 0, -1), (0, 0, 1, 1)),
        ((s, 1 - u, 0, d + u * h), (0, 1 - v, s, d + v * h)),
        ((1, 0, -1, 0), (0, 1, -s, -d)),
        ((1, 0, 0, 1), (0, 0, 1, -1)),
    )
    alpha = (
        planes[0][0],
        tuple(
            sp.expand(
                v * planes[1][0][coordinate]
                - u * planes[1][1][coordinate]
            )
            for coordinate in range(4)
        ),
        planes[2][0],
        planes[3][1],
    )
    beta = (
        planes[0][1],
        planes[1][0],
        planes[2][1],
        planes[3][0],
    )
    return alpha, beta


def shifted_basis(alpha, beta, shifts):
    return tuple(
        tuple(
            sp.factor(
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_projection(distinguished: int, alpha, beta) -> tuple[str, ...]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("ub")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    equations.extend(
        (
            (diagonal_a * extension)[0] - 1,
            inverse * (diagonal_b * extension)[0] - 1,
        )
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    program = "\n".join(
        (
            "ring r=(0,s,d,u,v),("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal incidence="
            + ",".join(map(singular, equations))
            + ";",
            "ideal basis=std(incidence);",
            "ideal marking=eliminate(basis,"
            + "*".join(map(str, eliminated))
            + ");",
            "marking=std(marking);",
            '"MARKING";',
            "marking;",
            "quit;",
        )
    )
    timeout = 600 if distinguished == 1 else 180
    completed = subprocess.run(
        singular_command_with_timeout(timeout),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 5,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular projection failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in completed.stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )


def fitting_certificate(
    distinguished: int,
    alpha,
    beta,
    marking,
) -> dict[str, object]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    extension = sp.Matrix(extensions)
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    marked = marked_extension(
        distinguished, extension, alpha, marked_beta, 0
    )
    determinants = tuple(
        sp.factor(marked[list(rows), :].det())
        for rows in FITTING_ROWS[distinguished]
    )
    first = (diagonal_a * extension)[0]
    second = (diagonal_b * extension)[0]
    program = "\n".join(
        (
            "ring r=(0,s,d,u,v),("
            + ",".join(map(str, extensions + (inverse,)))
            + "),dp;",
            "ideal I="
            + ",".join(
                map(
                    singular,
                    (
                        *list(mixed * extension),
                        *determinants,
                        inverse * first * second - 1,
                    ),
                )
            )
            + ";",
            "I=std(I);",
            "int unit=(reduce(1,I)==0);",
            '"CODEX_RESULT:"+string(unit)+":"+string(size(I));',
        )
    )
    completed = subprocess.run(
        singular_command_with_timeout(180),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=185,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular Fitting-certificate failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    lines = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert lines == ["CODEX_RESULT:1:1"], completed.stdout
    return {
        "marked_mode": 0,
        "minor_rows": [list(rows) for rows in FITTING_ROWS[distinguished]],
        "saturated_fitting_ideal_unit": True,
    }


def main() -> None:
    s, d, u, v = sp.symbols("s d u v")
    alpha, beta = canonical_basis()
    expected_middle_kernel = (s * v, v - u, -s * u, d * (v - u))
    assert all(
        sp.factor(observed - expected) == 0
        for observed, expected in zip(
            alpha[1], expected_middle_kernel, strict=True
        )
    )

    tensor = {
        word: permanent(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert tensor[(1, 1, 1, 1)] == 2 * s * u
    assert all(
        value == 0
        for word, value in tensor.items()
        if word != (1, 1, 1, 1)
    )

    t = sp.symbols("t0:4")
    shifted = shifted_basis(alpha, beta, t)
    shifted_tensor = {
        word: permanent(
            tuple(
                shifted[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert shifted_tensor == tensor

    # Restoring coordinate one always reconstructs the original pure
    # restriction: a conceptual kernel line for q=1.
    reconstruction = sp.Matrix(
        tuple(alpha[mode][1] for mode in range(4))
        + tuple(shifted[mode][1] for mode in range(4))
    )
    mixed_one, diagonal_a_one, diagonal_b_one = mixed_matrix(
        1, alpha, shifted
    )
    assert all(
        sp.factor(value) == 0 for value in mixed_one * reconstruction
    )
    assert sp.factor((diagonal_a_one * reconstruction)[0]) == 0
    assert sp.factor(
        (diagonal_b_one * reconstruction)[0] - 2 * s * u
    ) == 0

    projections = {
        distinguished: run_projection(distinguished, alpha, beta)
        for distinguished in range(4)
    }
    assert projections == EXPECTED_PROJECTIONS

    common_t1 = (1 - u) / (u - v)
    common_t2 = s * v / (u - v)
    markings = {
        0: (1, common_t1, common_t2, 0),
        2: (0, common_t1, common_t2, 1),
        3: (0, common_t1, common_t2, 0),
    }
    certificates = {
        str(distinguished): fitting_certificate(
            distinguished, alpha, beta, marking
        )
        for distinguished, marking in markings.items()
    }

    output = {
        "verified": True,
        "field": "C(s,d,u,v)",
        "method": (
            "apolar reparameterization, exact function-field marked "
            "projection, and three-minor Fitting certificates"
        ),
        "pure_coefficient": str(2 * s * u),
        "reconstruction_kernel_coordinate": 1,
        "reconstruction_first_diagonal": "0",
        "reconstruction_second_diagonal": str(2 * s * u),
        "projections": {
            str(key): list(value) for key, value in projections.items()
        },
        "surviving_marking_sheets": 3,
        "fitting_certificates": certificates,
        "generic_marked_fibre_excluded": True,
        "complete_boundary_marked_fibre_excluded": False,
        "known_pure_component_orbits_at_least": 7,
        "all_seven_known_components_generic_marked_fibres_excluded": True,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            COMPONENT_PRIMARY.name: sha256(COMPONENT_PRIMARY),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_six_dimensional_component_generic_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
