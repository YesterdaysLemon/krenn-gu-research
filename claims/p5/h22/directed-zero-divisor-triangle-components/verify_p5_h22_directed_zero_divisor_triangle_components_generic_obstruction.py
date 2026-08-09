#!/usr/bin/env python3
"""Verify generic H22 exclusion on directed-triangle components 16 and 17."""

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
expose_claim_package(REPO_ROOT, "claims/p4/classifications")
ROOT = REPO_ROOT

from verify_p4_directed_zero_divisor_triangle_components import (
    coefficients,
    raw_family,
)


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    word for word in WORDS if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))


def permanent3(rows, columns=(0, 1, 2)):
    return sp.expand(
        sum(
            rows[0][columns[permutation[0]]]
            * rows[1][columns[permutation[1]]]
            * rows[2][columns[permutation[2]]]
            for permutation in PERMUTATIONS3
        )
    )


def pure_bases(kind: str, u: sp.Expr, v: sp.Expr):
    planes = raw_family(kind, u, v)
    alpha = []
    beta = []
    for mode, plane in enumerate(planes):
        if kind == "path" and mode == 0:
            alpha.append(tuple(plane.row(0) + plane.row(1)))
            beta.append(tuple(plane.row(1)))
        else:
            alpha.append(tuple(plane.row(0)))
            beta.append(tuple(plane.row(1)))
    return tuple(alpha), tuple(beta)


def weighted_row(row, extension, direction: str, slope):
    if direction == "01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "01_inf":
        return (row[0], row[2], row[3], extension)
    if direction == "23_inf":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def build_model(kind, direction, u, v, slope, shifts):
    alpha, canonical_beta = pure_bases(kind, u, v)
    beta = tuple(
        tuple(
            canonical_beta[mode][coordinate]
            + shifts[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )
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
    alpha_d = model["alpha_d"]
    beta_d = model["beta_d"]
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_d[mode] if bits[index] else alpha_d[mode]
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


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def compare_ideals_lines(left_name, right_name):
    return (
        f"ideal LR=reduce({left_name},{right_name});",
        f"ideal RL=reduce({right_name},{left_name});",
        "LR=simplify(LR,2);",
        "RL=simplify(RL,2);",
        "int same=((size(LR)==0)&&(size(RL)==0));",
    )


def finite_union_projection(kind, direction, expected, comparisons=()):
    u, v, r = sp.symbols("u v r")
    shifts = sp.symbols("t0:4")
    model = build_model(kind, direction, u, v, r, shifts)
    extensions = model["extensions"]
    inverse = sp.Symbol("w")
    equations = (
        *tuple(model["mixed_matrix"] * sp.Matrix(extensions)),
        model["diagonal_a"] - 1,
        inverse * model["diagonal_b"] - 1,
    )
    eliminated = extensions + (inverse, r)
    variables = eliminated + shifts
    lines = [
        "ring R=(0,u,v),("
        + ",".join(map(str, variables))
        + "),(dp(10),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
        "J=std(J);",
    ]
    checks = []
    if expected is not None:
        lines.extend(
            (
                "ideal E=" + ",".join(map(singular, expected)) + ";",
                "E=std(E);",
                *compare_ideals_lines("J", "E"),
                '"CODEX_EXPECTED:"+string(same)+":"+string(size(J));',
            )
        )
        checks.append("expected")
    for index, (other, target) in enumerate(comparisons):
        lines.extend(
            (
                f"ideal O{index}=" + ",".join(map(singular, other)) + ";",
                f"ideal S{index}=std(J+O{index});",
            )
        )
        if target is None:
            lines.extend(
                (
                    f"int comparison{index}=(reduce(1,S{index})==0);",
                    f'"CODEX_COMPARISON:{index}:"+string(comparison{index});',
                )
            )
        else:
            lines.extend(
                (
                    f"ideal T{index}=" + ",".join(map(singular, target)) + ";",
                    f"T{index}=std(T{index});",
                    *compare_ideals_lines(f"S{index}", f"T{index}"),
                    f'"CODEX_COMPARISON:{index}:"+string(same);',
                )
            )
        checks.append(f"comparison_{index}")
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
    assert len(markers) == len(checks), completed.stdout
    assert all(marker.split(":")[-1 if "COMPARISON" in marker else -2] == "1" for marker in markers), completed.stdout
    return {
        "component": kind,
        "direction": direction,
        "slope_chart": "finite union",
        "checks": checks,
    }


def fixed_projection(kind, direction, expected, comparisons=()):
    u, v = sp.symbols("u v")
    shifts = sp.symbols("t0:4")
    model = build_model(kind, direction, u, v, sp.Integer(0), shifts)
    extensions = model["extensions"]
    inverse = sp.Symbol("w")
    equations = (
        *tuple(model["mixed_matrix"] * sp.Matrix(extensions)),
        model["diagonal_a"] - 1,
        inverse * model["diagonal_b"] - 1,
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    lines = [
        "ring R=(0,u,v),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
        "J=std(J);",
    ]
    checks = []
    if expected is None:
        lines.extend(
            (
                "int empty=(reduce(1,J)==0);",
                '"CODEX_EXPECTED:"+string(empty);',
            )
        )
    else:
        lines.extend(
            (
                "ideal E=" + ",".join(map(singular, expected)) + ";",
                "E=std(E);",
                *compare_ideals_lines("J", "E"),
                '"CODEX_EXPECTED:"+string(same)+":"+string(size(J));',
            )
        )
    checks.append("expected")
    for index, other in enumerate(comparisons):
        lines.extend(
            (
                f"ideal O{index}=" + ",".join(map(singular, other)) + ";",
                f"ideal S{index}=std(J+O{index});",
                f"int comparison{index}=(reduce(1,S{index})==0);",
                f'"CODEX_COMPARISON:{index}:"+string(comparison{index});',
            )
        )
        checks.append(f"comparison_{index}")
    lines.append("quit;")
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
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_")
    ]
    assert len(markers) == len(checks), completed.stdout
    assert all(marker.split(":")[-1 if "COMPARISON" in marker else -2 if marker.count(":") == 2 else -1] == "1" for marker in markers), completed.stdout
    return {
        "component": kind,
        "direction": direction,
        "slope_chart": "infinity",
        "checks": checks,
    }


def specialize_model(direction, slope, h, u, v):
    return build_model("path", direction, u, v, slope, (h, 0, 0, 0))


def substitute_extension(expression, extensions, extension):
    return sp.factor(expression.subs(dict(zip(extensions, extension, strict=True))))


def generic_path_certificate(direction):
    u, v, r, h, zeta = sp.symbols("u v r h zeta", nonzero=True)
    model = specialize_model(direction, r, h, u, v)
    kernel = model["mixed_matrix"].nullspace()
    assert len(kernel) == 1
    extension = zeta * kernel[0]
    diagonal_a = substitute_extension(
        model["diagonal_a"], model["extensions"], extension
    )
    diagonal_b = substitute_extension(
        model["diagonal_b"], model["extensions"], extension
    )
    marked = marked_matrix(model, 1).subs(
        dict(zip(model["extensions"], extension, strict=True))
    )
    determinant = sp.factor(marked[[0, 2, 3, 7], :].det())
    ratio = sp.factor(determinant / (diagonal_a**2 * diagonal_b))
    if direction == "01":
        assert sp.factor(diagonal_a + 2 * zeta * (r + 1) / (r - 1)) == 0
        assert sp.factor(diagonal_b - 2 * zeta * (h + r)) == 0
        assert sp.factor(
            determinant - 8 * r * zeta**3 * (h + r) * (u + v)
        ) == 0
        assert sp.factor(
            ratio - r * (u + v) * (r - 1) ** 2 / (r + 1) ** 2
        ) == 0
    else:
        assert sp.factor(
            diagonal_a + 2 * zeta * (r - 1) * (u + v) / (r + 1)
        ) == 0
        assert sp.factor(diagonal_b + 2 * zeta * (h * (u + v) + r + v)) == 0
        assert sp.factor(
            determinant
            - 8
            * zeta**3
            * (r - 1) ** 3
            * (u + v) ** 2
            * (r + u + v)
            * (h * (u + v) + r + v)
            / (r + 1) ** 3
        ) == 0
        assert sp.factor(ratio + (r - 1) * (r + u + v) / (r + 1)) == 0
    return {
        "direction": direction,
        "kernel_dimension": 1,
        "diagonal_a": str(diagonal_a),
        "diagonal_b": str(diagonal_b),
        "minor_over_A_squared_B": str(ratio),
    }


def kernel_diagonal_boundary(direction, slope, h, vanishing):
    u, v = sp.symbols("u v", nonzero=True)
    model = specialize_model(direction, slope, h, u, v)
    kernel = model["mixed_matrix"].nullspace()
    assert kernel
    diagonal = model[f"diagonal_{vanishing}"]
    restrictions = tuple(
        substitute_extension(diagonal, model["extensions"], vector)
        for vector in kernel
    )
    assert all(restriction == 0 for restriction in restrictions)
    return {
        "direction": direction,
        "slope": str(slope),
        "mark": str(h),
        "kernel_dimension": len(kernel),
        "vanishing_diagonal": vanishing.upper(),
    }


def two_dimensional_gcd_certificate(direction):
    u, v, h = sp.symbols("u v h", nonzero=True)
    if direction == "01":
        slope = sp.Integer(0)
        mark = h
        rows = ((0, 2, 3, 7), (0, 2, 6, 7))
        expected_ratio = sp.Integer(2)
    else:
        slope = sp.Integer(0)
        mark = -v / (u + v)
        rows = ((0, 2, 3, 7), (0, 2, 4, 7))
        expected_ratio = sp.Integer(-2)
    model = specialize_model(direction, slope, mark, u, v)
    kernel = model["mixed_matrix"].nullspace()
    assert len(kernel) == 2
    x, y = sp.symbols("x y")
    extension = x * kernel[0] + y * kernel[1]
    substitutions = dict(zip(model["extensions"], extension, strict=True))
    diagonal_a = sp.factor(model["diagonal_a"].subs(substitutions))
    diagonal_b = sp.factor(model["diagonal_b"].subs(substitutions))
    marked = marked_matrix(model, 1).subs(substitutions)
    determinants = tuple(
        sp.factor(marked[list(row_set), :].det()) for row_set in rows
    )
    common = sp.factor(sp.gcd(*determinants))
    ratio = sp.factor(common / (diagonal_a * diagonal_b))
    assert ratio == expected_ratio
    return {
        "direction": direction,
        "kernel_dimension": 2,
        "minor_rows": [list(row_set) for row_set in rows],
        "diagonal_a": str(diagonal_a),
        "diagonal_b": str(diagonal_b),
        "gcd_over_A_B": str(ratio),
    }


def d23_secondary_slope_certificate(mark):
    u, v, zeta = sp.symbols("u v zeta", nonzero=True)
    h = sp.symbols("h", nonzero=True) if mark == "nonzero" else sp.Integer(0)
    slope = -(u + v)
    model = specialize_model("23", slope, h, u, v)
    kernel = model["mixed_matrix"].nullspace()
    assert len(kernel) == 1
    extension = zeta * kernel[0]
    substitutions = dict(zip(model["extensions"], extension, strict=True))
    diagonal_a = sp.factor(model["diagonal_a"].subs(substitutions))
    diagonal_b = sp.factor(model["diagonal_b"].subs(substitutions))
    if mark == "nonzero":
        marked_mode = 1
        rows = (0, 2, 4, 7)
        expected = -h * (u + v + 1) ** 2 / (u + v - 1)
    else:
        marked_mode = 2
        rows = (0, 1, 3, 7)
        expected = -(u + v) * (u + v - 1) / (u + v + 1)
    marked = marked_matrix(model, marked_mode).subs(substitutions)
    determinant = sp.factor(marked[list(rows), :].det())
    ratio = sp.factor(determinant / (diagonal_a**2 * diagonal_b))
    assert sp.factor(ratio - expected) == 0
    return {
        "mark": mark,
        "marked_mode": marked_mode,
        "minor_rows": list(rows),
        "minor_over_A_squared_B": str(ratio),
    }


def main():
    u, v, r = sp.symbols("u v r", nonzero=True)
    shifts = sp.symbols("t0:4")

    for kind in ("star", "path"):
        alpha, beta = pure_bases(kind, u, v)
        tensor = coefficients(
            tuple(sp.Matrix((alpha[mode], beta[mode])) for mode in range(4))
        )
        assert tensor[(1, 1, 1, 1)] != 0
        assert all(
            value == 0
            for word, value in tensor.items()
            if word != (1, 1, 1, 1)
        )

    t0, t1, t2, t3 = shifts
    star_d23_finite = (
        t1,
        t3 * ((u - 1) * t0 + v - 1),
        t2 * ((u - 1) * t0 + v - 1),
    )
    star_d01_infinity = (
        t2,
        (u - v) * t1 + (1 - u) * t3 + u - v,
        u * t0 + v,
        t3 * (t3 + 1),
    )
    star_d23_infinity = (
        t2 + (v - 1) * (t3 + 1),
        t1,
        (u - 1) * t0 + v - 1,
        (t3 + 1) * ((v - 1) * t3 + v - 2),
    )
    path_d01_finite = (t2, t1, t3 * ((u + v) * t0 + v))
    path_coefficient = u * v - 2 * u + v**2 - v
    path_d23_finite = (
        t1,
        t2 * t3,
        t3 * ((u + v - 1) * t0 + v - 1),
        t0 * t2 * (path_coefficient * t0 + v * (v - 1)),
    )
    path_line = (t1, t2, t3)
    path_d23_infinity = (
        (u + v) * t3 + u + v - 1,
        t2,
        t1,
        (u + v - 1) * t0 + v - 1,
    )

    finite_projections = (
        finite_union_projection(
            "star",
            "01",
            None,
            (
                (star_d23_finite, None),
                (star_d23_infinity, None),
            ),
        ),
        finite_union_projection("star", "23", star_d23_finite),
        finite_union_projection(
            "path",
            "01",
            path_d01_finite,
            ((path_d23_finite, path_line),),
        ),
        finite_union_projection("path", "23", path_d23_finite),
    )
    infinity_projections = (
        fixed_projection(
            "star",
            "01_inf",
            star_d01_infinity,
            (star_d23_finite, star_d23_infinity),
        ),
        fixed_projection("star", "23_inf", star_d23_infinity),
        fixed_projection("path", "01_inf", None),
        fixed_projection(
            "path",
            "23_inf",
            path_d23_infinity,
            (path_d01_finite,),
        ),
    )

    generic_certificates = tuple(
        generic_path_certificate(direction) for direction in ("01", "23")
    )

    h = sp.symbols("h", nonzero=True)
    boundary_certificates = (
        kernel_diagonal_boundary("01", sp.Integer(1), h, "b"),
        kernel_diagonal_boundary("01", sp.Integer(-1), h, "a"),
        kernel_diagonal_boundary("01", r, -r, "b"),
        kernel_diagonal_boundary("23", sp.Integer(1), h, "a"),
        kernel_diagonal_boundary("23", sp.Integer(-1), h, "b"),
        kernel_diagonal_boundary("23", r, -(r + v) / (u + v), "b"),
    )
    zero_slope_certificates = tuple(
        two_dimensional_gcd_certificate(direction) for direction in ("01", "23")
    )
    secondary_slope_certificates = tuple(
        d23_secondary_slope_certificate(mark) for mark in ("nonzero", "zero")
    )

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "characteristic zero component function fields",
                "proof_method": "Fitting projection plus symbolic kernel minors",
                "finite_slope_projections": finite_projections,
                "infinity_slope_projections": infinity_projections,
                "star_projective_slope_intersection": "empty",
                "path_common_marking_line": "t1=t2=t3=0, t0=h",
                "generic_path_certificates": generic_certificates,
                "boundary_certificates": boundary_certificates,
                "zero_slope_certificates": zero_slope_certificates,
                "secondary_slope_certificates": secondary_slope_certificates,
                "generic_H22_fibre_component_16": "empty",
                "generic_H22_fibre_component_17": "empty",
                "global_conjecture": "unresolved",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
