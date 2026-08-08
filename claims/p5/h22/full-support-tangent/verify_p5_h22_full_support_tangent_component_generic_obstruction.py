#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on P4 component fourteen."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT
expose_claim_package(REPO_ROOT, "claims/p5/h31/full-support-tangent")  # noqa: E402

from verify_p5_h31_full_support_tangent_component_generic_obstruction import (
    normalized_family,
    shifted_beta,
    singular,
)
from verify_p5_h31_marked_basis_open_branch import mixed_matrix as h31_mixed_matrix
from verify_p5_h31_marked_basis_open_branch import marked_extension


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    word for word in WORDS if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
MINOR_ROWS = ((0, 1, 4, 7), (0, 4, 5, 7))


def permanent3(rows, columns=(0, 1, 2)):
    return sp.expand(
        sum(
            rows[0][columns[permutation[0]]]
            * rows[1][columns[permutation[1]]]
            * rows[2][columns[permutation[2]]]
            for permutation in PERMUTATIONS3
        )
    )


def weighted_row(row, extension, direction, slope):
    if direction == "01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "01_inf":
        return (row[0], row[2], row[3], extension)
    if direction == "23_inf":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def build_model(direction, p, q, slope, shifts):
    _, alpha, canonical_beta = normalized_family(p, q)
    beta = shifted_beta(alpha, canonical_beta, shifts)
    extensions = sp.symbols("z0:8")
    alpha_d = tuple(
        weighted_row(alpha[mode], extensions[mode], direction, slope)
        for mode in range(4)
    )
    beta_d = tuple(
        weighted_row(beta[mode], extensions[4 + mode], direction, slope)
        for mode in range(4)
    )

    def coefficient(word):
        selected = tuple(
            beta_d[mode] if word[mode] else alpha_d[mode]
            for mode in range(4)
        )
        return sp.expand(
            sum(
                selected[mode][3]
                * permanent3(
                    tuple(
                        selected[other]
                        for other in range(4)
                        if other != mode
                    )
                )
                for mode in range(4)
            )
        )

    mixed = tuple(coefficient(word) for word in MIXED_WORDS)
    mixed_matrix = sp.Matrix(
        [
            [sp.diff(expression, extension) for extension in extensions]
            for expression in mixed
        ]
    )
    return {
        "alpha": alpha,
        "beta": beta,
        "extensions": extensions,
        "alpha_d": alpha_d,
        "beta_d": beta_d,
        "mixed_matrix": mixed_matrix,
        "diagonal_a": coefficient((0, 0, 0, 0)),
        "diagonal_b": coefficient((1, 1, 1, 1)),
    }


def marked_matrix(model, marked_mode):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            model["beta_d"][mode]
            if bits[index]
            else model["alpha_d"][mode]
            for index, mode in enumerate(other_modes)
        )
        rows.append(
            tuple(
                permanent3(
                    selected,
                    tuple(
                        coordinate
                        for coordinate in range(4)
                        if coordinate != marked_coordinate
                    ),
                )
                for marked_coordinate in range(4)
            )
        )
    return sp.Matrix(rows)


def compare_ideals(left, right):
    return (
        f"ideal LR=reduce({left},{right});",
        f"ideal RL=reduce({right},{left});",
        "LR=simplify(LR,2);",
        "RL=simplify(RL,2);",
        "int same=((size(LR)==0)&&(size(RL)==0));",
    )


def projection(direction, slope_mode, expected, comparisons=()):
    p, q, r = sp.symbols("p q r")
    shifts = sp.symbols("h0:4")
    if slope_mode == "infinity":
        slope = sp.Integer(0)
        model_direction = f"{direction}_inf"
    else:
        slope = r
        model_direction = direction
    model = build_model(model_direction, p, q, slope, shifts)
    extensions = model["extensions"]
    inverse = sp.Symbol("w")
    equations = (
        *tuple(model["mixed_matrix"] * sp.Matrix(extensions)),
        model["diagonal_a"] - 1,
        inverse * model["diagonal_b"] - 1,
    )
    if slope_mode == "finite_union":
        eliminated = extensions + (inverse, r)
        target = shifts
        blocks = "(dp(10),dp(4))"
    elif slope_mode == "finite_total":
        eliminated = extensions + (inverse,)
        target = (r,) + shifts
        blocks = "(dp(9),dp(5))"
    elif slope_mode == "infinity":
        eliminated = extensions + (inverse,)
        target = shifts
        blocks = "(dp(9),dp(4))"
    else:
        raise ValueError(slope_mode)
    variables = eliminated + target
    lines = [
        "ring R=(0,p,q),(" + ",".join(map(str, variables)) + f"),{blocks};",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
        "J=std(J);",
        "ideal E=" + ",".join(map(singular, expected)) + ";",
        "E=std(E);",
        *compare_ideals("J", "E"),
        '"CODEX_EXPECTED:"+string(same)+":"+string(size(J));',
    ]
    for index, (other, target_ideal) in enumerate(comparisons):
        lines.extend(
            (
                f"ideal O{index}=" + ",".join(map(singular, other)) + ";",
                f"ideal S{index}=std(J+O{index});",
            )
        )
        if target_ideal is None:
            lines.extend(
                (
                    f"int comparison{index}=(reduce(1,S{index})==0);",
                    f'"CODEX_COMPARISON:{index}:"+string(comparison{index});',
                )
            )
        else:
            lines.extend(
                (
                    f"ideal T{index}="
                    + ",".join(map(singular, target_ideal))
                    + ";",
                    f"T{index}=std(T{index});",
                    *compare_ideals(f"S{index}", f"T{index}"),
                    f'"CODEX_COMPARISON:{index}:"+string(same);',
                )
            )
    lines.append("quit;")
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=100,
        check=False,
    )
    assert completed.returncode == 0, completed
    assert not completed.stderr.strip(), completed.stderr
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_")
    ]
    assert len(markers) == 1 + len(comparisons), completed.stdout
    assert all(marker.split(":")[-1] == "1" for marker in markers if "COMPARISON" in marker)
    assert markers[0].split(":")[-2] == "1", completed.stdout
    return {
        "direction": direction,
        "slope_mode": slope_mode,
        "basis_size": int(markers[0].split(":")[-1]),
        "comparison_count": len(comparisons),
    }


def finite_branch_certificate():
    p, q, r = sp.symbols("p q r")
    cap_p = p + q
    cap_s = cap_p + 1
    k = q / ((p - q) * (cap_p - 1))
    h = r * cap_s / (r * cap_p - 1)
    model = build_model("01", p, q, r, (h, 0, 0, k))
    denominator = (p - 1) * (r + 1)
    extension = sp.Matrix(
        (
            (1 - r * cap_p) / denominator,
            (1 - r * cap_p) / denominator,
            cap_s * (r - 1) / denominator,
            0,
            0,
            -r * cap_s / denominator,
            (r * cap_p - 1) / denominator,
            1,
        )
    )
    assert all(
        sp.cancel(value) == 0 for value in model["mixed_matrix"] * extension
    )
    diagonal_a = sp.factor(
        model["diagonal_a"].subs(
            dict(zip(model["extensions"], extension, strict=True))
        )
    )
    diagonal_b = sp.factor(
        model["diagonal_b"].subs(
            dict(zip(model["extensions"], extension, strict=True))
        )
    )
    expected_a = (
        2
        * r
        * (p - q)
        * cap_p
        * (cap_p - 1)
        * (r * cap_p - 1)
        / denominator
    )
    expected_b = -2 * (r * (cap_p - 1) - 1)
    assert sp.factor(diagonal_a - expected_a) == 0
    assert sp.factor(diagonal_b - expected_b) == 0

    marked = marked_matrix(model, 0).subs(
        dict(zip(model["extensions"], extension, strict=True))
    )
    clearing = (p - 1) * (p - q) * (cap_p - 1) * (r + 1)
    cleared_matrices = []
    for rows in MINOR_ROWS:
        matrix = marked.extract(rows, range(4))
        cleared = matrix.applyfunc(lambda entry: sp.cancel(clearing * entry))
        assert all(sp.denom(entry) == 1 for entry in cleared)
        cleared_matrices.append(cleared)
    declarations = []
    for index, matrix in enumerate(cleared_matrices):
        declarations.append(
            f"matrix N{index}[4][4]="
            + ",".join(
                singular(matrix[row, column])
                for row in range(4)
                for column in range(4)
            )
            + ";"
        )
    expected_gcd = (
        r
        * (r * cap_p - 1)
        * (r * (cap_p - 1) - 1)
        * (r + 1) ** 2
    )
    lines = [
        "ring R=(0,p,q),r,dp;",
        *declarations,
        "poly D0=det(N0);",
        "poly D1=det(N1);",
        "ideal G=gcd(D0,D1);",
        "G=std(G);",
        "ideal E=" + singular(expected_gcd) + ";",
        "E=std(E);",
        *compare_ideals("G", "E"),
        '"CODEX_RESULT:"+string(same);',
        "quit;",
    ]
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=80,
        check=False,
    )
    assert completed.returncode == 0, completed
    assert not completed.stderr.strip(), completed.stderr
    assert "CODEX_RESULT:1" in completed.stdout, completed.stdout
    return {
        "branch": "h0=H,h1=0",
        "kernel_dimension": 1,
        "extension": [str(sp.factor(value)) for value in extension],
        "diagonal_a": str(diagonal_a),
        "diagonal_b": str(diagonal_b),
        "marked_mode": 0,
        "minor_rows": [list(rows) for rows in MINOR_ROWS],
        "cleared_minor_gcd": str(sp.factor(expected_gcd)),
    }


def minus_one_binary_obstruction():
    p, q = sp.symbols("p q")
    cap_p = p + q
    k = q / ((p - q) * (cap_p - 1))
    model = build_model("01", p, q, sp.Integer(-1), (1, 0, 0, k))
    extensions = model["extensions"]
    inverse_a, inverse_b = sp.symbols("wa wb")
    equations = (
        *tuple(model["mixed_matrix"] * sp.Matrix(extensions)),
        inverse_a * model["diagonal_a"] - 1,
        inverse_b * model["diagonal_b"] - 1,
    )
    variables = extensions + (inverse_a, inverse_b)
    lines = [
        "ring R=(0,p,q),(" + ",".join(map(str, variables)) + "),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "int empty=(reduce(1,I)==0);",
        '"CODEX_RESULT:"+string(empty);',
        "quit;",
    ]
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=80,
        check=False,
    )
    assert completed.returncode == 0, completed
    assert not completed.stderr.strip(), completed.stderr
    assert "CODEX_RESULT:1" in completed.stdout, completed.stdout
    return {"slope": -1, "genuine_binary_incidence": "empty"}


def mode_swap_certificate():
    p, q, r = sp.symbols("p q r")
    cap_p = p + q
    cap_s = cap_p + 1
    k = q / ((p - q) * (cap_p - 1))
    h = r * cap_s / (r * cap_p - 1)
    left = build_model("01", p, q, r, (h, 0, 0, k))
    right = build_model("01", p, q, r, (0, h, 0, k))
    row_permutation = tuple(
        MIXED_WORDS.index((word[1], word[0], word[2], word[3]))
        for word in MIXED_WORDS
    )
    column_permutation = (1, 0, 2, 3, 5, 4, 6, 7)
    assert all(
        sp.cancel(value) == 0
        for value in right["mixed_matrix"]
        - left["mixed_matrix"].extract(row_permutation, column_permutation)
    )
    extension = sp.Matrix(right["extensions"])
    permuted = sp.Matrix([extension[index] for index in column_permutation])
    extension_substitution = dict(
        zip(left["extensions"], permuted, strict=True)
    )
    assert sp.cancel(
        right["diagonal_a"]
        - left["diagonal_a"].subs(extension_substitution, simultaneous=True)
    ) == 0
    assert sp.cancel(
        right["diagonal_b"]
        - left["diagonal_b"].subs(extension_substitution, simultaneous=True)
    ) == 0
    left_marked = marked_matrix(left, 0).subs(
        extension_substitution, simultaneous=True
    )
    right_marked = marked_matrix(right, 1)
    assert all(
        sp.cancel(value) == 0 for value in right_marked - left_marked
    )
    return {
        "mode_permutation": "0<->1",
        "extension_permutation": list(column_permutation),
        "prototype_marked_mode": 0,
        "partner_marked_mode": 1,
    }


def infinity_h31_identity():
    p, q = sp.symbols("p q")
    cap_p = p + q
    cap_s = cap_p + 1
    k = q / ((p - q) * (cap_p - 1))
    point = (cap_s / cap_p, 0, 0, k)
    h22 = build_model("01_inf", p, q, sp.Integer(0), point)
    _, alpha, canonical_beta = normalized_family(p, q)
    beta = shifted_beta(alpha, canonical_beta, point)
    h31_mixed, h31_a, h31_b = h31_mixed_matrix(1, alpha, beta)
    assert all(
        sp.cancel(value) == 0 for value in h22["mixed_matrix"] - h31_mixed
    )
    extension = sp.Matrix(h22["extensions"])
    assert sp.cancel(h22["diagonal_a"] - (h31_a * extension)[0]) == 0
    assert sp.cancel(h22["diagonal_b"] - (h31_b * extension)[0]) == 0
    h31_marked = marked_extension(1, extension, alpha, beta, 0)
    assert h22["alpha_d"] == tuple(
        tuple(alpha[mode][coordinate] for coordinate in (0, 2, 3))
        + (h22["extensions"][mode],)
        for mode in range(4)
    )
    assert all(
        sp.cancel(value) == 0 for value in marked_matrix(h22, 0) - h31_marked
    )
    return {
        "slope": "infinity",
        "identified_H31_deleted_coordinate": 1,
        "identified_H31_sheet": 0,
    }


def main():
    p, q, r = sp.symbols("p q r", nonzero=True)
    h0, h1, h2, h3 = sp.symbols("h0:4")
    cap_p = p + q
    cap_s = cap_p + 1
    a = (p - q) * (cap_p - 1)
    finite_d01 = (a * h3 - q, h2)
    finite_d23 = (h2, h0 * h1)
    common = (a * h3 - q, h2, h0 * h1)
    total_d01 = (
        a * h3 - q,
        h2,
        r * h0 * h1
        + cap_s * (1 - r * cap_p) * (h0 + h1)
        + r * cap_s**2,
    )
    infinity_d01 = (
        a * h3 - q,
        h2,
        cap_p * (h0 + h1) - cap_s,
        cap_p * h1**2 - cap_s * h1,
    )
    infinity_d23 = (
        cap_p * (p - q + 1) * h3 - q,
        h2,
        (p + 1) * (h0 + h1) - cap_s,
        (p + 1) * h1**2 - cap_s * h1,
    )

    projections = (
        projection(
            "01",
            "finite_union",
            finite_d01,
            ((finite_d23, common), (infinity_d23, None)),
        ),
        projection("23", "finite_union", finite_d23),
        projection("01", "finite_total", total_d01),
        projection(
            "01",
            "infinity",
            infinity_d01,
            ((infinity_d23, None),),
        ),
        projection("23", "infinity", infinity_d23),
    )
    finite_certificate = finite_branch_certificate()
    boundary_certificate = minus_one_binary_obstruction()
    symmetry = mode_swap_certificate()
    infinity = infinity_h31_identity()

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "C(p,q)",
                "proof_method": "projective Fitting projection and two-minor slope gcd",
                "projections": projections,
                "finite_common_marking_locus": "h2=0, h3=q/((p-q)(p+q-1)), h0*h1=0",
                "finite_branch_certificate": finite_certificate,
                "minus_one_boundary": boundary_certificate,
                "mode_swap_certificate": symmetry,
                "infinity_certificate": infinity,
                "generic_H22_fibre_component_14": "empty",
                "global_conjecture": "unresolved",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
