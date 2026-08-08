#!/usr/bin/env python3
"""Verify the generic marked-H31 obstruction on the three 1+3 components."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from p5_high_coordinate_tree_chart_cegar import singular_command_with_timeout
from verify_p4_diagonal_quadric_one_three_components import branch_planes
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = REPO_ROOT
THEOREM = HERE / "P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = ROOT / "P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md"
COMPONENT_PRIMARY = ROOT / "verify_p4_diagonal_quadric_one_three_components.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

EXPECTED_PROJECTIONS = {
    "L1": {
        0: ("1",),
        1: ("1",),
        2: (
            "t3",
            "(S)*t2+(-S^2+S*D-S*G+D*G)",
            "t1+(-S+D)",
            "(S+G)*t0+1",
        ),
        3: (
            "t3+1",
            "t2+(-S+D)",
            "(S-D+G)*t1+(-S^2+S*D-S*G+D*G)",
            "(S+G)*t0+1",
        ),
    },
    "L2": {
        0: ("1",),
        1: ("1",),
        2: ("t3", "t1", "(D+G)*t0+1"),
        3: ("t3+1", "t2", "(D+G)*t0+1"),
    },
    "L3": {0: ("1",), 1: ("1",), 2: ("1",), 3: ("1",)},
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


def add_rows(left, right, left_scale=1, right_scale=1):
    return tuple(
        sp.factor(left_scale * left[index] + right_scale * right[index])
        for index in range(4)
    )


def canonical_basis(
    branch: str,
    S: sp.Expr,
    D: sp.Expr,
    G: sp.Expr,
):
    planes = branch_planes(branch, S, D, G)

    def row(mode: int, index: int):
        return tuple(planes[mode].row(index))

    if branch == "L1":
        alpha = (
            add_rows(row(0, 0), row(0, 1), G + S, -2 * D * G),
            row(1, 0),
            row(2, 1),
            add_rows(row(3, 0), row(3, 1), 1, -1),
        )
        beta = (row(0, 0), row(1, 1), row(2, 0), row(3, 0))
    elif branch == "L2":
        alpha = (
            add_rows(
                row(0, 0),
                row(0, 1),
                D + G,
                -2 * D * (D + G - S),
            ),
            row(1, 0),
            row(2, 1),
            add_rows(row(3, 0), row(3, 1), 1, -1),
        )
        beta = (row(0, 0), row(1, 1), row(2, 0), row(3, 0))
    else:
        alpha = (
            row(0, 1),
            row(1, 0),
            row(2, 1),
            add_rows(
                row(3, 0),
                row(3, 1),
                G * (D + G + S),
                D * S,
            ),
        )
        beta = (row(0, 0), row(1, 1), row(2, 0), row(3, 0))
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
    return str(sp.expand(expression)).replace("**", "^")


def run_function_field_projection(
    distinguished: int,
    alpha,
    beta,
    timeout: float = 120,
) -> tuple[str, ...]:
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
            "ring r=(0,S,D,G),("
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
                "Singular function-field projection failure",
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


def extension_certificate(
    distinguished: int,
    alpha,
    beta,
    rows: tuple[int, ...],
    expected_denominator: sp.Expr,
):
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, beta
    )
    assert mixed.rank() == 6
    kernel = mixed.nullspace()
    assert len(kernel) == 2
    u, v = sp.symbols("u v")
    extension = u * kernel[0] + v * kernel[1]
    first_diagonal = sp.factor((diagonal_a * extension)[0])
    second_diagonal = sp.factor((diagonal_b * extension)[0])
    marked = marked_extension(
        distinguished, extension, alpha, beta, 0
    )
    determinant = sp.factor(marked[list(rows), :].det())
    assert sp.factor(
        determinant
        - first_diagonal**2
        * second_diagonal
        / expected_denominator
    ) == 0
    pure_marked = one_marked_map(0, alpha, beta)
    expected_transverse = -1 if distinguished == 2 else 1
    assert pure_marked[2, distinguished] == expected_transverse
    return {
        "mixed_rank": mixed.rank(),
        "kernel_dimension": len(kernel),
        "first_diagonal": str(first_diagonal),
        "second_diagonal": str(second_diagonal),
        "marked_rows": list(rows),
        "marked_determinant": str(determinant),
        "factor_identity_denominator": str(expected_denominator),
        "pure_transverse_entry": str(
            pure_marked[2, distinguished]
        ),
    }


def main() -> None:
    S, D, G = sp.symbols("S D G", nonzero=True)
    t = sp.symbols("t0:4")
    canonical = {
        branch: canonical_basis(branch, S, D, G)
        for branch in ("L1", "L2", "L3")
    }

    pure_coefficients = {}
    for branch, (alpha, beta) in canonical.items():
        tensor = {
            word: permanent(
                tuple(
                    beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
            for word in WORDS
        }
        nonzero = {
            word: value for word, value in tensor.items() if value != 0
        }
        assert set(nonzero) == {(1, 1, 1, 1)}
        pure_coefficients[branch] = str(nonzero[(1, 1, 1, 1)])
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
        assert all(
            sp.factor(
                shifted_tensor[word]
                - (tensor[word] if word == (1, 1, 1, 1) else 0)
            )
            == 0
            for word in WORDS
        )

    projections = {}
    for branch, (alpha, beta) in canonical.items():
        projections[branch] = {
            distinguished: run_function_field_projection(
                distinguished, alpha, beta
            )
            for distinguished in range(4)
        }
    assert projections == EXPECTED_PROJECTIONS

    remainder = (D - S) * (S + G)
    branch_l1 = canonical["L1"]
    l1_markings = {
        2: (
            -1 / (S + G),
            S - D,
            -remainder / S,
            0,
        ),
        3: (
            -1 / (S + G),
            -remainder / (S - D + G),
            S - D,
            -1,
        ),
    }
    l1_rows = {2: (0, 4, 5, 7), 3: (0, 2, 3, 7)}
    l1_denominator = 8 * D * G * (G + S)
    l1_certificates = {}
    for distinguished, marking in l1_markings.items():
        marked_beta = shifted_basis(branch_l1[0], branch_l1[1], marking)
        l1_certificates[str(distinguished)] = extension_certificate(
            distinguished,
            branch_l1[0],
            marked_beta,
            l1_rows[distinguished],
            l1_denominator,
        )

    branch_l2 = canonical["L2"]
    p = sp.Symbol("p")
    l2_markings = {
        2: (-1 / (D + G), 0, p, 0),
        3: (-1 / (D + G), p, 0, -1),
    }
    l2_rows = {2: (0, 4, 5, 7), 3: (0, 2, 3, 7)}
    l2_denominator = 8 * D * (D + G) * (D + G - S)
    l2_certificates = {}
    for distinguished, marking in l2_markings.items():
        marked_beta = shifted_basis(branch_l2[0], branch_l2[1], marking)
        l2_certificates[f"{distinguished}_generic_p"] = (
            extension_certificate(
                distinguished,
                branch_l2[0],
                marked_beta,
                l2_rows[distinguished],
                l2_denominator,
            )
        )

    exceptional_markings = {
        2: (
            -1 / (D + G),
            0,
            G * (D + G - S) / (D + G),
            0,
        ),
        3: (-1 / (D + G), S, 0, -1),
    }
    for distinguished, marking in exceptional_markings.items():
        marked_beta = shifted_basis(branch_l2[0], branch_l2[1], marking)
        l2_certificates[f"{distinguished}_exceptional_p"] = (
            extension_certificate(
                distinguished,
                branch_l2[0],
                marked_beta,
                l2_rows[distinguished],
                l2_denominator,
            )
        )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "function-field marked projection, exact extension kernels, "
            "and all-extension one-marked factor identities"
        ),
        "canonical_pure_coefficients": pure_coefficients,
        "function_field_projection_ideals": {
            branch: {
                str(distinguished): list(ideal)
                for distinguished, ideal in branch_projections.items()
            }
            for branch, branch_projections in projections.items()
        },
        "L1_survivor_distinguished_coordinates": [2, 3],
        "L1_unique_markings": {
            str(key): [str(entry) for entry in value]
            for key, value in l1_markings.items()
        },
        "L1_extension_certificates": l1_certificates,
        "L2_survivor_distinguished_coordinates": [2, 3],
        "L2_marking_pencils": {
            str(key): [str(entry) for entry in value]
            for key, value in l2_markings.items()
        },
        "L2_exceptional_markings": {
            str(key): [str(entry) for entry in value]
            for key, value in exceptional_markings.items()
        },
        "L2_extension_certificates": l2_certificates,
        "L3_binary_Delta2_extension_exists_at_generic_point": False,
        "all_generic_binary_extensions_ternarily_excluded": True,
        "three_new_components_generic_marked_H31_fibres_excluded": True,
        "three_new_components_complete_marked_H31_fibres_excluded": False,
        "component_parameter_boundaries_closed": False,
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
        / "p5_h31_one_three_component_generic_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
