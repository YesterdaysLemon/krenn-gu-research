#!/usr/bin/env python3
"""Verify the H31 obstruction on the pure-direction boundary curve."""

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
THEOREM = (
    ROOT
    / "P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md"
)
COMPONENT = (
    ROOT / "claims" / "p4" / "components" / "diagonal-quadric"
    / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md")
C_CURVE_THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md"
)
E_CURVE_THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
EXPECTED_RELATIVE_PROJECTIONS = {
    0: ("1",),
    1: ("1",),
    2: ("t3", "t2+1", "t0-1", "2*t1*e+e^2+1"),
    3: ("1",),
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


def run_relative_projection(
    distinguished: int,
    alpha,
    beta,
    parameter: sp.Symbol,
    timeout: float = 120,
) -> tuple[str, ...]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    diagonal_inverse = sp.Symbol("ub")
    pure_inverse = sp.Symbol("up")
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
            diagonal_inverse * (diagonal_b * extension)[0] - 1,
            pure_inverse * (parameter**2 - 1) - 1,
        )
    )
    eliminated = extensions + (diagonal_inverse, pure_inverse)
    retained = shifts + (parameter,)
    variables = eliminated + retained
    program = "\n".join(
        (
            "ring r=0,("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp({len(retained)}));",
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
                "Singular relative projection failure",
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


def pluecker(plane: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.factor(plane[:, (left, right)].det())
        for left, right in itertools.combinations(range(4), 2)
    )


def proportional(left, right) -> bool:
    return all(
        sp.factor(left[i] * right[j] - left[j] * right[i]) == 0
        for i in range(len(left))
        for j in range(len(left))
    )


def main() -> None:
    e = sp.Symbol("e")
    t = sp.symbols("t0:4")
    u, v = sp.symbols("u v")
    alpha = (
        (1, -1, 1, 1),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
        (1, 0, 0, 1),
    )
    canonical = (
        (e, -1, -1, -e),
        (1, 0, -2, 1),
        (1 + e, 1, 1, 1 - e),
        (0, 1, 1, 0),
    )
    beta = tuple(
        tuple(
            canonical[mode][coordinate]
            + t[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    planes = tuple(
        sp.Matrix.vstack(
            sp.Matrix(alpha[mode]).T,
            sp.Matrix(canonical[mode]).T,
        )
        for mode in range(4)
    )
    fixed_minors = (
        planes[0][:, (1, 2)].det(),
        planes[1][:, (0, 3)].det(),
        planes[2][:, (1, 2)].det(),
        planes[3][:, (0, 1)].det(),
    )
    assert fixed_minors == (2, 2, 2, 1)

    pure = {
        word: permanent(
            tuple(
                canonical[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert sp.factor(
        pure[(1, 1, 1, 1)] - 4 * (e**2 - 1)
    ) == 0
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    relative_projections = {
        distinguished: run_relative_projection(
            distinguished,
            alpha,
            beta,
            e,
        )
        for distinguished in range(4)
    }
    assert relative_projections == EXPECTED_RELATIVE_PROJECTIONS

    shifts = (1, -(e**2 + 1) / (2 * e), -1, 0)
    marked_beta = tuple(
        tuple(
            sp.factor(entry.subs(dict(zip(t, shifts, strict=True))))
            for entry in row
        )
        for row in beta
    )
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        2,
        alpha,
        marked_beta,
    )
    assert mixed.rank() == 6
    denominator = e**2 - 1
    kernel = (
        sp.Matrix(
            (
                -2 / denominator,
                -2 * e / denominator,
                0,
                -2 / denominator,
                1,
                4 / denominator,
                1,
                0,
            )
        ),
        sp.Matrix(
            (
                (e**2 + 3) / denominator,
                4 * e / denominator,
                -1,
                4 / denominator,
                -2,
                -2 * (e**2 + 3) / denominator,
                0,
                1,
            )
        ),
    )
    assert all(
        all(sp.factor(entry) == 0 for entry in mixed * vector)
        for vector in kernel
    )
    extension = u * kernel[0] + v * kernel[1]
    diagonals = (
        sp.factor((diagonal_a * extension)[0]),
        sp.factor((diagonal_b * extension)[0]),
    )
    expected_diagonals = (
        -4 * e * (u - 2 * v) / denominator,
        2 * u * denominator,
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(
            diagonals,
            expected_diagonals,
            strict=True,
        )
    )
    marked = marked_extension(
        2,
        extension,
        alpha,
        marked_beta,
        1,
    )
    marked_minor = sp.factor(marked[[0, 4, 6, 7], :].det())
    assert sp.factor(
        marked_minor + 64 * e * u * (u - 2 * v) ** 2
    ) == 0
    pure_column = one_marked_map(1, alpha, marked_beta)[:, 2]
    assert any(entry != 0 for entry in pure_column)

    C, E = sp.symbols("C E")
    factored_slice = sp.factor(
        1 + C - 1 - C**2 * E**2 + C**2 - C * E**2
    )
    assert factored_slice == -C * (C + 1) * (E - 1) * (E + 1)

    def slice_planes(E_value):
        return (
            sp.Matrix(((E_value, -1, -1, -E_value), (1, -1, 1, 1))),
            sp.Matrix(((1, 0, 0, -1), (1, C + 1, C - 1, 1))),
            sp.Matrix(((1 + E_value, 1, 1, 1 - E_value), (0, 1, -1, 0))),
            sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0))),
        )

    source_swap = sp.Matrix(
        (
            (0, 0, 0, 1),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (1, 0, 0, 0),
        )
    )
    plus_planes = slice_planes(1)
    minus_planes = slice_planes(-1)
    assert all(
        proportional(
            pluecker(plus_planes[mode] * source_swap),
            pluecker(minus_planes[mode]),
        )
        for mode in range(4)
    )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "saturated relative binary projection, all-extension marked "
            "minor, and factored-slice symmetry"
        ),
        "curve_parameter": "e",
        "nonzero_pure_locus": "e^2!=1",
        "pure_coefficient": "4*(e^2-1)",
        "relative_projection_runs": len(relative_projections),
        "relative_binary_projection_ideals": {
            str(key): list(value)
            for key, value in relative_projections.items()
        },
        "unique_survivor_marking": [str(entry) for entry in shifts],
        "survivor_mixed_rank": mixed.rank(),
        "survivor_kernel_dimension": len(kernel),
        "binary_diagonals": [str(entry) for entry in diagonals],
        "marked_mode": 1,
        "marked_rows": [0, 4, 6, 7],
        "marked_minor": str(marked_minor),
        "pure_transverse_column": [str(entry) for entry in pure_column],
        "all_genuine_binary_extensions_ternarily_excluded": True,
        "factored_slice_equation": str(factored_slice),
        "E_minus_one_source_symmetric_to_E_plus_one": True,
        "complete_nonzero_factored_slice_excluded": True,
        "second_component_generic_fibre_closed": False,
        "second_component_complete_marked_fibre_closed": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            C_CURVE_THEOREM.name: sha256(C_CURVE_THEOREM),
            E_CURVE_THEOREM.name: sha256(E_CURVE_THEOREM),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_diagonal_quadric_pure_direction_curve_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
