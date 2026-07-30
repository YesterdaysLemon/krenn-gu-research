#!/usr/bin/env python3
"""Verify the H31 obstruction at a point of the second P4 component."""

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
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md"
COMPONENT = ROOT / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md"
COMPONENT_PRIMARY = ROOT / "verify_p4_diagonal_quadric_pure_component.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

ALPHA = (
    (3, -2, 0, -1),
    (1, 0, 0, -1),
    (0, 1, -1, 0),
    (1, -1, -1, 1),
)
CANONICAL_BETA = (
    (1, -1, 1, 1),
    (1, 1, -1, 1),
    (3, 1, 1, -1),
    (0, 1, 1, 0),
)
EXPECTED_PROJECTIONS = {
    0: ("t3-1", "t2-1", "t1-1", "t0"),
    1: ("1",),
    2: ("1",),
    3: ("t3-1", "t2-1", "t1+1", "t0"),
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


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def run_projection(
    distinguished: int,
    alpha,
    beta,
    timeout: float = 30,
) -> tuple[str, ...]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("ub")
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        beta,
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
            "ring r=0,("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal incidence=" + ",".join(map(singular, equations)) + ";",
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
    output = completed.stdout.replace("\r\n", "\n")
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.splitlines()
        if line.startswith("marking[")
    )


def main() -> None:
    t = sp.symbols("t0:4")
    alpha = tuple(tuple(map(sp.Integer, row)) for row in ALPHA)
    canonical = tuple(
        tuple(map(sp.Integer, row)) for row in CANONICAL_BETA
    )
    beta = tuple(
        tuple(
            canonical[mode][coordinate]
            + t[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    pure = {
        word: permanent(
            tuple(
                canonical[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == 4
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    projections = {
        distinguished: run_projection(
            distinguished,
            alpha,
            beta,
        )
        for distinguished in range(4)
    }
    assert projections == EXPECTED_PROJECTIONS

    u, v = sp.symbols("u v")
    survivor_data = {
        0: {
            "shifts": (0, 1, 1, 1),
            "kernel": (
                sp.Matrix((0, 0, -1, 0, 0, 1, 0, 0)),
                sp.Matrix((3, 1, 2, 1, 1, 0, 3, 1)),
            ),
            "diagonals": (2 * (u - 2 * v), 2 * u),
        },
        3: {
            "shifts": (0, -1, 1, 1),
            "kernel": (
                sp.Matrix((0, 0, -1, 0, 0, 1, 0, 0)),
                sp.Matrix((-1, -1, 2, 1, 1, 0, -1, 1)),
            ),
            "diagonals": (-2 * (u - 2 * v), 2 * u),
        },
    }
    marked_determinants = {}
    pure_transverse_entries = {}
    for distinguished, data in survivor_data.items():
        substitutions = dict(zip(t, data["shifts"], strict=True))
        marked_beta = tuple(
            tuple(sp.factor(entry.subs(substitutions)) for entry in row)
            for row in beta
        )
        mixed, diagonal_a, diagonal_b = mixed_matrix(
            distinguished,
            alpha,
            marked_beta,
        )
        assert mixed.rank() == 6
        basis = data["kernel"]
        assert all(mixed * vector == sp.zeros(14, 1) for vector in basis)
        basis_matrix = sp.Matrix.hstack(*basis)
        assert basis_matrix.rank() == 2
        extension = u * basis[0] + v * basis[1]
        actual_diagonals = (
            sp.factor((diagonal_a * extension)[0]),
            sp.factor((diagonal_b * extension)[0]),
        )
        assert all(
            sp.factor(actual - expected) == 0
            for actual, expected in zip(
                actual_diagonals, data["diagonals"], strict=True
            )
        )

        marked = marked_extension(
            distinguished,
            extension,
            alpha,
            marked_beta,
            1,
        )
        determinant = sp.factor(marked[[0, 1, 5, 7], :].det())
        expected_determinant = -8 * u * (u - 2 * v) ** 2
        assert sp.factor(determinant - expected_determinant) == 0
        marked_determinants[distinguished] = str(determinant)

        pure_column = one_marked_map(1, alpha, marked_beta)[:, distinguished]
        assert any(entry == 2 for entry in pure_column)
        pure_transverse_entries[distinguished] = [
            str(entry) for entry in pure_column
        ]

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "exact binary projection and all-extension one-marked minor"
        ),
        "projection_runs": len(projections),
        "binary_projection_ideals": {
            str(distinguished): list(projection)
            for distinguished, projection in projections.items()
        },
        "binary_survivor_distinguished_coordinates": [0, 3],
        "binary_survivor_markings": {
            str(distinguished): list(data["shifts"])
            for distinguished, data in survivor_data.items()
        },
        "survivor_mixed_rank": 6,
        "survivor_kernel_dimension": 2,
        "binary_nonzero_condition": "u*(u-2*v)!=0",
        "marked_mode": 1,
        "marked_rows": [0, 1, 5, 7],
        "marked_determinants": marked_determinants,
        "pure_transverse_columns": pure_transverse_entries,
        "all_binary_extensions_ternarily_excluded": True,
        "rational_point_H31_lift_possible": False,
        "second_component_generic_fibre_closed": False,
        "second_component_complete_marked_fibre_closed": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
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
        / "p5_h31_diagonal_quadric_component_point_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
