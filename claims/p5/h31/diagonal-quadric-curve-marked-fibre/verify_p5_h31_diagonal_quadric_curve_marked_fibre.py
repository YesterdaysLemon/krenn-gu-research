#!/usr/bin/env python3
"""Verify the marked H31 obstruction on a diagonal-quadric curve."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.singular_runtime import singular_command_with_timeout
from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md"
)
COMPONENT = (
    REPO_ROOT / 'claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md')
COMPONENT_PRIMARY = (
    REPO_ROOT / 'claims/p4/components/diagonal-quadric/verify_p4_diagonal_quadric_pure_component.py')
POINT_THEOREM = (
    REPO_ROOT / 'claims/p5/h31/diagonal-quadric-component-point/P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md'
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

ALPHA = (
    (1, -1, 0, 0),
    (1, 0, 0, -1),
    (0, 1, -1, 0),
    (1, -1, -1, 1),
)

EXPECTED_GENERIC_PROJECTIONS = {
    0: ("t3-1", "t2-1", "t1-1", "(c-1)*t0+(2*c)"),
    1: ("1",),
    2: ("t3", "t2-1", "t1-1", "t0+1"),
    3: ("1",),
}
EXPECTED_RELATIVE_PROJECTIONS = {
    0: ("t3-1", "t2-1", "t1-1", "t0*c-t0+2*c"),
    1: ("1",),
    2: ("t3", "t2-1", "t1-1", "t0+1"),
    3: ("t3-1", "t2-1", "t1-2*c+1", "t0+c", "c^2-c"),
}
EXPECTED_SPECIAL_PROJECTIONS = {
    0: {
        0: ("t3-1", "t2-1", "t1-1", "t0"),
        1: ("1",),
        2: ("t3", "t2-1", "t1-1", "t0+1"),
        3: ("t3-1", "t2-1", "t1+1", "t0"),
    },
    1: {
        0: ("1",),
        1: ("1",),
        2: ("t3", "t2-1", "t1-1", "t0+1"),
        3: ("t3-1", "t2-1", "t1-1", "t0+1"),
    },
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


def run_projection(
    distinguished: int,
    alpha,
    beta,
    *,
    parameter: sp.Symbol | None = None,
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
    coefficient_field = (
        f"(0,{parameter})" if parameter is not None else "0"
    )
    program = "\n".join(
        (
            "ring r="
            + coefficient_field
            + ",("
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
                parameter,
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


def run_relative_projection(
    distinguished: int,
    alpha,
    beta,
    parameter: sp.Symbol,
    timeout: float = 120,
) -> tuple[str, ...]:
    """Project with c retained and the nonzero-pure locus saturated."""
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    diagonal_inverse = sp.Symbol("ub")
    pure_inverse = sp.Symbol("uc")
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
            pure_inverse * (parameter + 1) - 1,
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


def verify_case(
    *,
    label: str,
    distinguished: int,
    alpha,
    beta,
    shifts,
    kernel,
    expected_diagonals,
    marked_mode: int,
    marked_rows: list[int],
    expected_minor,
) -> dict:
    t = sp.symbols("t0:4")
    u, v = sp.symbols("u v")
    substitutions = dict(zip(t, shifts, strict=True))
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
    assert all(
        all(sp.factor(entry) == 0 for entry in mixed * vector)
        for vector in kernel
    )
    assert sp.Matrix.hstack(*kernel).rank() == 2

    extension = u * kernel[0] + v * kernel[1]
    actual_diagonals = (
        sp.factor((diagonal_a * extension)[0]),
        sp.factor((diagonal_b * extension)[0]),
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(
            actual_diagonals,
            expected_diagonals,
            strict=True,
        )
    )

    marked = marked_extension(
        distinguished,
        extension,
        alpha,
        marked_beta,
        marked_mode,
    )
    actual_minor = sp.factor(marked[marked_rows, :].det())
    assert sp.factor(actual_minor - expected_minor) == 0

    pure_column = one_marked_map(
        marked_mode,
        alpha,
        marked_beta,
    )[:, distinguished]
    assert any(entry != 0 for entry in pure_column)
    return {
        "label": label,
        "distinguished_coordinate": distinguished,
        "marking": [str(entry) for entry in shifts],
        "mixed_rank": mixed.rank(),
        "kernel_dimension": 2,
        "binary_diagonals": [str(entry) for entry in actual_diagonals],
        "marked_mode": marked_mode,
        "marked_rows": marked_rows,
        "marked_minor": str(actual_minor),
        "pure_transverse_column": [str(entry) for entry in pure_column],
    }


def main() -> None:
    c = sp.Symbol("c")
    t = sp.symbols("t0:4")
    u, v = sp.symbols("u v")
    alpha = tuple(tuple(map(sp.Integer, row)) for row in ALPHA)
    canonical = (
        (1, -1, 1, 1),
        (1, c + 1, c - 1, 1),
        (2, 1, 1, 0),
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

    pure = {
        word: permanent(
            tuple(
                canonical[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] - 4 * (c + 1)) == 0
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    c_curve_planes = (
        sp.Matrix(((1, -1, -1, -1), (1, -1, 1, 1))),
        sp.Matrix(((1, 0, 0, -1), (1, c + 1, c - 1, 1))),
        sp.Matrix(((2, 1, 1, 0), (0, 1, -1, 0))),
        sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0))),
    )
    h_curve_planes = (
        sp.Matrix(((1, -1, -1, -1), (1, -1, 1, 1))),
        sp.Matrix(((1, 0, 0, -1), (1, 2, 0, 1))),
        sp.Matrix(((c + 1, 1, 1, c - 1), (0, 1, -1, 0))),
        sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0))),
    )
    source_permutation = sp.Matrix(
        (
            (0, 1, 0, 0),
            (1, 0, 0, 0),
            (0, 0, 0, 1),
            (0, 0, 1, 0),
        )
    )
    mode_permutation = (0, 2, 1, 3)
    assert all(
        proportional(
            pluecker(
                c_curve_planes[mode] * source_permutation
            ),
            pluecker(h_curve_planes[mode_permutation[mode]]),
        )
        for mode in range(4)
    )

    generic_projections = {
        distinguished: run_projection(
            distinguished,
            alpha,
            beta,
            parameter=c,
        )
        for distinguished in range(4)
    }
    assert generic_projections == EXPECTED_GENERIC_PROJECTIONS

    relative_projections = {
        distinguished: run_relative_projection(
            distinguished,
            alpha,
            beta,
            c,
        )
        for distinguished in range(4)
    }
    assert relative_projections == EXPECTED_RELATIVE_PROJECTIONS

    special_projections = {}
    for specialization in (0, 1):
        specialized_beta = tuple(
            tuple(sp.factor(entry.subs(c, specialization)) for entry in row)
            for row in beta
        )
        special_projections[specialization] = {
            distinguished: run_projection(
                distinguished,
                alpha,
                specialized_beta,
            )
            for distinguished in range(4)
        }
    assert special_projections == EXPECTED_SPECIAL_PROJECTIONS

    generic_q0_kernel = (
        sp.Matrix(
            (
                sp.Rational(1, 2),
                0,
                -1 / (2 * c),
                sp.Rational(1, 2),
                -(c + 1) / (2 * (c - 1)),
                (c + 1) / (2 * c),
                1,
                0,
            )
        ),
        sp.Matrix((0, 1, 1 / c, 0, 0, (c - 1) / c, 0, 1)),
    )
    linear_factor = (c + 1) * u + 2 * (c - 1) * v
    cases = [
        verify_case(
            label="generic_q0",
            distinguished=0,
            alpha=alpha,
            beta=beta,
            shifts=(-2 * c / (c - 1), 1, 1, 1),
            kernel=generic_q0_kernel,
            expected_diagonals=(
                -(c - 1) * (u - 2 * v) / (2 * c),
                (c + 1) * linear_factor / c,
            ),
            marked_mode=1,
            marked_rows=[0, 4, 5, 7],
            expected_minor=(
                -(c + 1)
                * (u - 2 * v) ** 2
                * linear_factor
                / (2 * c**3)
            ),
        ),
        verify_case(
            label="generic_q2",
            distinguished=2,
            alpha=alpha,
            beta=beta,
            shifts=(-1, 1, 1, 0),
            kernel=(
                sp.Matrix((0, 1, 0, -1, 1, 0, 0, 0)),
                sp.Matrix((0, -1, -1, 0, 0, c - 1, 0, 1)),
            ),
            expected_diagonals=(2 * (u - v), 4 * v * (c + 1)),
            marked_mode=0,
            marked_rows=[0, 2, 3, 7],
            expected_minor=64 * v * (c + 1) * (u - v) ** 2,
        ),
    ]

    beta_c0 = tuple(
        tuple(sp.factor(entry.subs(c, 0)) for entry in row) for row in beta
    )
    cases.extend(
        (
            verify_case(
                label="c0_q0",
                distinguished=0,
                alpha=alpha,
                beta=beta_c0,
                shifts=(0, 1, 1, 1),
                kernel=(
                    sp.Matrix((0, 0, -1, 0, 0, 1, 0, 0)),
                    sp.Matrix((1, 1, 2, 1, 1, 0, 2, 1)),
                ),
                expected_diagonals=(u - 2 * v, 2 * u),
                marked_mode=1,
                marked_rows=[0, 1, 5, 7],
                expected_minor=-2 * u * (u - 2 * v) ** 2,
            ),
            verify_case(
                label="c0_q2",
                distinguished=2,
                alpha=alpha,
                beta=beta_c0,
                shifts=(-1, 1, 1, 0),
                kernel=(
                    sp.Matrix((0, 1, 0, -1, 1, 0, 0, 0)),
                    sp.Matrix((0, -1, -1, 0, 0, -1, 0, 1)),
                ),
                expected_diagonals=(2 * (u - v), 4 * v),
                marked_mode=0,
                marked_rows=[0, 2, 3, 7],
                expected_minor=64 * v * (u - v) ** 2,
            ),
            verify_case(
                label="c0_q3",
                distinguished=3,
                alpha=alpha,
                beta=beta_c0,
                shifts=(0, -1, 1, 1),
                kernel=(
                    sp.Matrix((0, 0, -1, 0, 0, 1, 0, 0)),
                    sp.Matrix((0, -1, 2, 1, 1, 0, 0, 1)),
                ),
                expected_diagonals=(-(u - 2 * v), 2 * u),
                marked_mode=1,
                marked_rows=[0, 1, 5, 7],
                expected_minor=-2 * u * (u - 2 * v) ** 2,
            ),
        )
    )

    beta_c1 = tuple(
        tuple(sp.factor(entry.subs(c, 1)) for entry in row) for row in beta
    )
    cases.extend(
        (
            verify_case(
                label="c1_q2",
                distinguished=2,
                alpha=alpha,
                beta=beta_c1,
                shifts=(-1, 1, 1, 0),
                kernel=(
                    sp.Matrix((0, 1, 0, -1, 1, 0, 0, 0)),
                    sp.Matrix((0, -1, -1, 0, 0, 0, 0, 1)),
                ),
                expected_diagonals=(2 * (u - v), 8 * v),
                marked_mode=0,
                marked_rows=[0, 2, 3, 7],
                expected_minor=128 * v * (u - v) ** 2,
            ),
            verify_case(
                label="c1_q3",
                distinguished=3,
                alpha=alpha,
                beta=beta_c1,
                shifts=(-1, 1, 1, 1),
                kernel=(
                    sp.Matrix((0, 0, 1, 1, 1, 0, 0, 0)),
                    sp.Matrix((0, -1, -1, 0, 0, 0, 0, 1)),
                ),
                expected_diagonals=(2 * (u - v), 8 * v),
                marked_mode=1,
                marked_rows=[0, 1, 4, 7],
                expected_minor=-16 * v * (u - v) ** 2,
            ),
        )
    )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "relative saturated binary projection, function-field and "
            "special-fibre kernels, and all-extension one-marked minors"
        ),
        "curve_parameter": "c",
        "nonzero_pure_locus": "c!=-1",
        "pure_coefficient": "4*(c+1)",
        "H_curve_in_source_mode_symmetry_orbit": True,
        "H_curve_parameters": "A=B=C=E=F=1,H=c",
        "relative_projection_runs": len(relative_projections),
        "relative_binary_projection_ideals": {
            str(key): list(value)
            for key, value in relative_projections.items()
        },
        "relative_projection_saturation": "c+1!=0",
        "hidden_complex_special_fibres_possible": False,
        "generic_projection_runs": len(generic_projections),
        "generic_binary_projection_ideals": {
            str(key): list(value)
            for key, value in generic_projections.items()
        },
        "special_projection_runs": sum(
            len(projections) for projections in special_projections.values()
        ),
        "special_binary_projection_ideals": {
            str(specialization): {
                str(key): list(value)
                for key, value in projections.items()
            }
            for specialization, projections in special_projections.items()
        },
        "verified_survivor_cases": cases,
        "all_curve_markings_binary_classified": True,
        "all_genuine_binary_extensions_ternarily_excluded": True,
        "curve_H31_lift_possible": False,
        "second_component_generic_fibre_closed": False,
        "second_component_complete_marked_fibre_closed": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            COMPONENT_PRIMARY.name: sha256(COMPONENT_PRIMARY),
            POINT_THEOREM.name: sha256(POINT_THEOREM),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_diagonal_quadric_curve_marked_fibre_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
