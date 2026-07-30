#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on the mixed fivefold."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import sympy as sp

from p5_high_coordinate_tree_chart_cegar import singular_command_with_timeout


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = ROOT / "P4_MIXED_ORIENTATION_PURE_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    bits
    for bits in WORDS
    if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
PERMUTATIONS = tuple(itertools.permutations(range(4)))
LOW_MARKING_POLYNOMIALS = (
    "t1*t3",
    "(t0-1)*t3",
    "t1*((d+q)*t2-p*q)",
    "(t0-1)*(t2+d-p)",
    "(t0-1)*t1",
)
FITTING_ROWS = ((0, 2, 6, 7), (0, 4, 6, 7))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def canonical_basis(d, p, q):
    n = q * (d + p + q)
    planes = (
        ((-d * p, d + q, n, 0), (d * p, -d - q, 0, n)),
        ((0, 0, 1, 1), (-d, 1, -p - q, d)),
        ((p, 1, 0, q), (-1, 0, 1, 0)),
        ((1, 0, 1, 0), (0, 0, -1, 1)),
    )
    alpha = tuple(plane[1] for plane in planes)
    beta = tuple(plane[0] for plane in planes)
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


def diagonal_row(row, extension, diagonal: str, slope):
    if diagonal == "01":
        return (
            slope * row[0] + row[1],
            row[2],
            row[3],
            extension,
        )
    if diagonal == "23":
        return (
            row[0],
            row[1],
            slope * row[2] + row[3],
            extension,
        )
    raise ValueError(diagonal)


def diagonal_coefficients(
    alpha,
    beta,
    extensions,
    diagonal: str,
    slope,
) -> dict[tuple[int, ...], sp.Expr]:
    alpha_d = tuple(
        diagonal_row(
            alpha[mode],
            extensions[mode],
            diagonal,
            slope,
        )
        for mode in range(4)
    )
    beta_d = tuple(
        diagonal_row(
            beta[mode],
            extensions[4 + mode],
            diagonal,
            slope,
        )
        for mode in range(4)
    )
    return {
        bits: permanent(
            tuple(
                beta_d[mode] if bits[mode] else alpha_d[mode]
                for mode in range(4)
            )
        )
        for bits in WORDS
    }


def one_marked_map(mode: int, alpha, beta) -> sp.Matrix:
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other] if bits[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_singular(program: str, timeout: int, label: str) -> str:
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
                f"Singular failure in {label}",
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return completed.stdout


def run_d01_chart(
    stage: str,
    chart: int,
) -> dict[str, object]:
    d, p, q, r = sp.symbols("d p q r")
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    alpha, beta = canonical_basis(d, p, q)
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        "01",
        r,
    )
    zero_indices = {
        "first": (),
        "middle": (2, 3),
        "residual": (2, 3, 6, 7),
    }[stage]
    substitutions = {
        **{extensions[index]: 0 for index in zero_indices},
        extensions[chart]: 1,
    }
    equations = [
        sp.expand(coefficients[bits].subs(substitutions))
        for bits in MIXED_WORDS
    ]
    affine_extensions = tuple(
        extension
        for index, extension in enumerate(extensions)
        if index not in zero_indices and index != chart
    )
    variables = affine_extensions + shifts
    algorithm = "std" if (stage, chart) == ("first", 3) else "slimgb"
    program = "\n".join(
        (
            "ring R=(0,d,p,q,r),("
            + ",".join(map(str, variables))
            + f"),(dp({len(affine_extensions)}),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            f"I={algorithm}(I);",
            "int unit=(reduce(1,I)==0);",
            (
                f'"CODEX_RESULT:{stage}:{chart}:"+string(unit)+":"'
                '+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        program,
        600,
        f"D01 {stage} chart {chart}",
    )
    expected = f"CODEX_RESULT:{stage}:{chart}:1:1"
    markers = [
        line.strip()
        for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert markers == [expected], (stage, chart, output)
    return {
        "stage": stage,
        "normalized_coordinate": str(extensions[chart]),
        "coordinates_already_zero": [
            str(extensions[index]) for index in zero_indices
        ],
        "algorithm": algorithm,
        "ideal_unit": True,
    }


def run_d01_projective_cover() -> list[dict[str, object]]:
    charts = (
        ("first", 2),
        ("first", 3),
        ("middle", 6),
        ("middle", 7),
        ("residual", 0),
        ("residual", 1),
        ("residual", 4),
        ("residual", 5),
    )
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda item: run_d01_chart(*item), charts))
    return results


def run_d23_projection() -> dict[str, object]:
    d, p, q, r = sp.symbols("d p q r")
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    alpha, beta = canonical_basis(d, p, q)
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        "23",
        r,
    )
    equations = [coefficients[bits] for bits in MIXED_WORDS]
    equations.extend(
        (
            coefficients[(0, 0, 0, 0)] - 1,
            inverse * coefficients[(1, 1, 1, 1)] - 1,
        )
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    low = (
        shifts[1] * shifts[3],
        (shifts[0] - 1) * shifts[3],
        shifts[1] * ((d + q) * shifts[2] - p * q),
        (shifts[0] - 1) * (shifts[2] + d - p),
        (shifts[0] - 1) * shifts[1],
    )
    program = "\n".join(
        (
            "ring R=(0,d,p,q,r),("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal incidence=" + ",".join(map(singular, equations)) + ";",
            "ideal basis=std(incidence);",
            "ideal marking=eliminate(basis,"
            + "*".join(map(str, eliminated))
            + ");",
            "marking=std(marking);",
            "int proper=(reduce(1,marking)!=0);",
            *(
                f"poly low{index}={singular(expression)};"
                for index, expression in enumerate(low)
            ),
            *(
                f"int member{index}=(reduce(low{index},marking)==0);"
                for index in range(len(low))
            ),
            (
                '"CODEX_RESULT:"+string(proper)'
                + "".join(
                    f'+":"+string(member{index})'
                    for index in range(len(low))
                )
                + ";"
            ),
            "quit;",
        )
    )
    output = run_singular(program, 600, "D23 marking projection")
    markers = [
        line.strip()
        for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert markers == ["CODEX_RESULT:1:1:1:1:1:1"], output
    return {
        "projected_marking_ideal_proper": True,
        "certified_members": list(LOW_MARKING_POLYNOMIALS),
        "covering_closures": {
            "A": ["t0-1", "t1"],
            "B": ["t0-1", "t3", "(d+q)*t2-p*q"],
            "C": ["t1", "t3", "t2+d-p"],
        },
    }


def run_d23_fitting_branch(branch: str) -> dict[str, object]:
    d, p, q, r = sp.symbols("d p q r")
    t = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    alpha, beta = canonical_basis(d, p, q)
    branch_shifts, free_shifts = {
        "A": ((1, 0, t[2], t[3]), (t[2], t[3])),
        "B": ((1, t[1], p * q / (d + q), 0), (t[1],)),
        "C": ((t[0], 0, p - d, 0), (t[0],)),
    }[branch]
    marked_beta = shifted_basis(alpha, beta, branch_shifts)
    coefficients = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        "23",
        r,
    )
    mixed = [coefficients[bits] for bits in MIXED_WORDS]
    first = coefficients[(0, 0, 0, 0)]
    second = coefficients[(1, 1, 1, 1)]
    alpha_d = tuple(
        diagonal_row(alpha[mode], extensions[mode], "23", r)
        for mode in range(4)
    )
    beta_d = tuple(
        diagonal_row(
            marked_beta[mode],
            extensions[4 + mode],
            "23",
            r,
        )
        for mode in range(4)
    )
    marked = one_marked_map(3, alpha_d, beta_d)
    determinant_matrices = tuple(
        marked[list(rows), :] for rows in FITTING_ROWS
    )
    determinant_offset = len(mixed)
    inverse_index = determinant_offset + len(determinant_matrices)
    variables = extensions + free_shifts + (inverse,)
    program = "\n".join(
        (
            "ring R=(0,d,p,q,r),("
            + ",".join(map(str, variables))
            + "),dp;",
            "option(redSB);",
            *(
                f"poly g{index}={singular(generator)};"
                for index, generator in enumerate(mixed)
            ),
            *tuple(
                "matrix D"
                + str(index)
                + "[4][4]="
                + ",".join(
                    singular(matrix[row, column])
                    for row in range(4)
                    for column in range(4)
                )
                + ";\npoly g"
                + str(determinant_offset + index)
                + "=det(D"
                + str(index)
                + ");"
                for index, matrix in enumerate(determinant_matrices)
            ),
            f"poly g{inverse_index}="
            + singular(inverse * first * second - 1)
            + ";",
            "ideal I="
            + ",".join(
                f"g{index}" for index in range(inverse_index + 1)
            )
            + ";",
            "I=std(I);",
            "int unit=(reduce(1,I)==0);",
            (
                f'"CODEX_RESULT:{branch}:"+string(unit)+":"'
                '+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(program, 600, f"D23 Fitting branch {branch}")
    markers = [
        line.strip()
        for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert markers == [f"CODEX_RESULT:{branch}:1:1"], output
    return {
        "branch": branch,
        "free_marking_parameters": [str(value) for value in free_shifts],
        "saturated_two_minor_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "ker M_01(t)=0 for every t in Kbar^4" in theorem_text
    assert "component exhaustiveness" in theorem_text
    assert "global prize problem" in theorem_text

    d, p, q = sp.symbols("d p q")
    alpha, beta = canonical_basis(d, p, q)
    pure = {
        bits: permanent(
            tuple(
                beta[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for bits in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] - 2 * q * (d + p + q)) == 0
    assert all(
        sp.factor(value) == 0
        for bits, value in pure.items()
        if bits != (1, 1, 1, 1)
    )

    d01_cover = run_d01_projective_cover()
    projection = run_d23_projection()
    with ThreadPoolExecutor(max_workers=3) as executor:
        fitting = list(
            executor.map(run_d23_fitting_branch, ("A", "B", "C"))
        )

    result = {
        "verified": True,
        "field": "C(d,p,q,r)",
        "component": "mixed-orientation fivefold",
        "pure_nonzero_coefficient": "2*q*(d+p+q)",
        "D01": {
            "mixed_matrix_shape": [14, 8],
            "projective_kernel_cover": d01_cover,
            "full_column_rank_for_every_marking": True,
            "generic_binary_incidence_empty": True,
        },
        "D23": {
            "marking_projection": projection,
            "marked_mode": 3,
            "minor_rows": [list(rows) for rows in FITTING_ROWS],
            "fitting_branches": fitting,
            "generic_ternary_incidence_empty": True,
        },
        "generic_weighted_H22_component_incidence_empty": True,
        "parameter_and_slope_divisors_closed": False,
        "projective_boundary_closed": False,
        "other_components_closed_for_H22": False,
        "all_H22_excluded": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            "theorem": {
                "path": THEOREM.name,
                "sha256": sha256(THEOREM),
            },
            "component": {
                "path": COMPONENT.name,
                "sha256": sha256(COMPONENT),
            },
        },
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h22_mixed_orientation_component_generic_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
