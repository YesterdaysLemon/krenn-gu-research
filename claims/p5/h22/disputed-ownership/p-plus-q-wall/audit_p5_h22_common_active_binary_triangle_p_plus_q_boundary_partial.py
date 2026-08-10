#!/usr/bin/env python3
"""Independent exact audit of the partial weighted-H22 checkpoint.

This file deliberately does not import the primary verifier.  It reconstructs
the chart bases, weighted contractions, elimination ideals, mixed kernels, and
marked minors directly from the formulas in the theorem note.  All algebra is
over characteristic zero; the one numerical calculation uses exact rationals
and is reported as audit-only.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
AUDIT = Path(__file__).resolve()
THEOREM = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"
PRIMARY = ROOT / "verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py"
P4_BOUNDARY = REPO_ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PERMUTATIONS_3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS_4 = tuple(itertools.permutations(range(4)))
RANK_ROWS = (1, 2, 3, 4, 6, 9, 13)
RANK_COLUMNS = (0, 1, 2, 3, 4, 5, 6)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def vector_add(*vectors: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(coordinates)) for coordinates in zip(*vectors))


def vector_scale(
    scalar: sp.Expr, vector: tuple[sp.Expr, ...]
) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(scalar * coordinate) for coordinate in vector)


def permanent3(
    rows: tuple[tuple[sp.Expr, ...], ...],
    columns: tuple[int, ...] = (0, 1, 2),
) -> sp.Expr:
    return sp.expand(
        sum(
            rows[0][columns[permutation[0]]]
            * rows[1][columns[permutation[1]]]
            * rows[2][columns[permutation[2]]]
            for permutation in PERMUTATIONS_3
        )
    )


def permanent4(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS_4
        )
    )


def chart_planes(
    chart: str,
    a: sp.Expr,
    lam: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, sp.Integer(1), -1, 0)
    em = (0, sp.Integer(1), 1, 0)
    cap_c = (0, 0, 0, sp.Integer(1))
    k0 = vector_add(
        vector_scale(2 * a + 1, cap_c),
        vector_scale(-a * (a + 1), ell),
    )
    alpha = (k0, e, e, em)
    beta_zero = (
        vector_add(e, vector_scale(lam, ell)) if chart == "B_full" else ell,
        vector_add(vector_scale(a + 1, ell), cap_c),
        vector_add(vector_scale(a, ell), cap_c),
        e,
    )
    beta = tuple(
        vector_add(beta_zero[index], vector_scale(shifts[index], alpha[index]))
        for index in range(4)
    )
    return alpha, beta


def contract(
    row: tuple[sp.Expr, ...], extension: sp.Expr, direction: str, slope: sp.Expr
) -> tuple[sp.Expr, ...]:
    if direction == "D01_finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23_finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01_infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23_infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def reconstruct_model(
    chart: str,
    direction: str,
    a: sp.Expr,
    lam: sp.Expr,
    slope: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> dict[str, object]:
    alpha, beta = chart_planes(chart, a, lam, shifts)
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        contract(alpha[index], extensions[index], direction, slope)
        for index in range(4)
    )
    beta_rows = tuple(
        contract(beta[index], extensions[index + 4], direction, slope)
        for index in range(4)
    )

    coefficients: dict[tuple[int, ...], sp.Expr] = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index]
            for index in range(4)
        )
        coefficients[word] = sp.expand(
            sum(
                selected[index][3]
                * permanent3(
                    tuple(selected[other] for other in range(4) if other != index)
                )
                for index in range(4)
            )
        )

    mixed = sp.Matrix(
        [
            [coefficients[word].coeff(extension) for extension in extensions]
            for word in MIXED_WORDS
        ]
    )
    return {
        "extensions": extensions,
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "mixed": mixed,
        "diagonal_alpha": coefficients[WORDS[0]],
        "diagonal_beta": coefficients[WORDS[-1]],
    }


def marked_matrix(model: dict[str, object], marked_mode: int = 3) -> sp.Matrix:
    alpha_rows = model["alpha_rows"]
    beta_rows = model["beta_rows"]
    assert isinstance(alpha_rows, tuple) and isinstance(beta_rows, tuple)
    other_modes = tuple(index for index in range(4) if index != marked_mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_rows[mode] if bits[position] else alpha_rows[mode]
            for position, mode in enumerate(other_modes)
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


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def hall_support_audit() -> dict[str, object]:
    rho, sigma = sp.symbols("rho sigma")
    source_scales = sp.symbols("s0:4", nonzero=True)
    extensions = sp.symbols("x0:4")
    rows = (
        (sigma * source_scales[1], -source_scales[2], 0, extensions[0]),
        (rho * source_scales[0], 0, 0, extensions[1]),
        (rho * source_scales[0], 0, 0, extensions[2]),
        (sigma * source_scales[1], source_scales[2], 0, extensions[3]),
    )
    supports = tuple(
        tuple(index for index, entry in enumerate(row) if entry != 0) for row in rows
    )
    assert all(2 not in support for support in supports)
    assert permanent4(rows) == 0
    assert permanent4(
        tuple(
            tuple(sp.sympify(entry).subs({rho: 1, sigma: 0}) for entry in row)
            for row in rows
        )
    ) == 0
    assert permanent4(
        tuple(
            tuple(sp.sympify(entry).subs({rho: 0, sigma: 1}) for entry in row)
            for row in rows
        )
    ) == 0
    return {
        "verdict": "VERIFIED",
        "family": "a=-1/2 replacement, every k",
        "direction": "homogeneous D01",
        "row_supports": [list(support) for support in supports],
        "missing_retained_channel": 2,
        "permanent_identically_zero": True,
        "projective_slope_endpoints_checked": True,
        "scope": "established local weighted-H22 framework",
    }


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact projection replay")


def singular_text(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def normalization_audit(model: dict[str, object]) -> dict[str, object]:
    """Check homogeneity behind A=1 and w*B=1 on the genuine locus."""

    extensions = model["extensions"]
    mixed = model["mixed"]
    diagonal_alpha = model["diagonal_alpha"]
    diagonal_beta = model["diagonal_beta"]
    assert isinstance(extensions, tuple)
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(diagonal_alpha, sp.Expr)
    assert isinstance(diagonal_beta, sp.Expr)
    scale = sp.Symbol("c")
    substitutions = {
        extension: scale * extension for extension in extensions
    }
    for equation in mixed * sp.Matrix(extensions):
        assert_equal(equation.subs(substitutions), scale * equation)
    assert_equal(diagonal_alpha.subs(substitutions), scale * diagonal_alpha)
    assert_equal(diagonal_beta.subs(substitutions), scale * diagonal_beta)
    return {
        "mixed_and_diagonals_linear_in_extension_vector": True,
        "normalization": "A=1 and w*B=1",
        "lossless_when_A_times_B_is_nonzero": True,
        "argument": "rescale a genuine kernel vector by 1/A, then set w=A/B",
    }


def projection_audit(
    chart: str, direction: str, expected: tuple[sp.Expr, ...]
) -> dict[str, object]:
    started = time.perf_counter()
    a, lam, slope = sp.symbols("a lambda r")
    shifts = sp.symbols("h0:4")
    model = reconstruct_model(chart, direction, a, lam, slope, shifts)
    extensions = model["extensions"]
    mixed = model["mixed"]
    diagonal_alpha = model["diagonal_alpha"]
    diagonal_beta = model["diagonal_beta"]
    assert isinstance(extensions, tuple)
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(diagonal_alpha, sp.Expr)
    assert isinstance(diagonal_beta, sp.Expr)

    normalization = normalization_audit(model)
    inverse = sp.Symbol("w")
    equations = (
        *tuple(mixed * sp.Matrix(extensions)),
        diagonal_alpha - 1,
        inverse * diagonal_beta - 1,
    )
    finite = direction.endswith("finite")
    eliminated = extensions + ((inverse, slope) if finite else (inverse,))
    variables = eliminated + shifts
    parameters = (a, lam) if chart == "B_full" else (a,)
    blocks = f"(dp({len(eliminated)}),dp(4))"
    program = "\n".join(
        (
            "ring R=(0,"
            + ",".join(map(str, parameters))
            + "),("
            + ",".join(map(str, variables))
            + "),"
            + blocks
            + ";",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + ";",
            "E=std(E);",
            "ideal left=simplify(reduce(J,E),2);",
            "ideal right=simplify(reduce(E,J),2);",
            "int same=((size(left)==0)&&(size(right)==0));",
            '"AUDIT_RESULT:"+string(same)+":"+string(size(J));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=60,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (chart, direction, completed.returncode, completed.stdout, completed.stderr)
        )
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("AUDIT_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, same, basis_size = markers[0].split(":")
    assert same == "1", completed.stdout
    return {
        "verdict": "VERIFIED",
        "chart": chart,
        "direction": direction,
        "coefficient_field": "C(a,lambda)" if chart == "B_full" else "C(a)",
        "projected_ideal": [singular_text(entry) for entry in expected],
        "bidirectional_ideal_reduction_zero": True,
        "standard_basis_size": int(basis_size),
        "projection_is_closure_only": True,
        "normalization": normalization,
        "seconds": round(time.perf_counter() - started, 3),
    }


def projection_audits() -> list[dict[str, object]]:
    a = sp.Symbol("a")
    h0, h1, h2, h3 = sp.symbols("h0:4")
    finite = (h3, h0, h1 * h2)
    expected = {
        ("B_full", "D01_finite"): finite,
        ("B_full", "D23_finite"): finite,
        ("B_full", "D01_infinity"): (
            h3,
            a * h1 + (a + 1) * h2,
            h0,
            h2**2,
        ),
        ("B_full", "D23_infinity"): (sp.Integer(1),),
        ("B_drop", "D01_finite"): finite,
        ("B_drop", "D23_finite"): finite,
        ("B_drop", "D01_infinity"): finite,
        ("B_drop", "D23_infinity"): (sp.Integer(1),),
    }
    return [
        projection_audit(chart, direction, ideal)
        for (chart, direction), ideal in expected.items()
    ]


def kernel_generator(
    chart: str,
    sheet: str,
    a: sp.Expr,
    lam: sp.Expr,
    slope: sp.Expr,
    t: sp.Expr,
) -> sp.Matrix:
    s0 = 2 * a + 1
    if chart == "B_full" and sheet == "S1":
        return sp.Matrix(
            (
                -t * (a + 1) * (2 * a * lam + a * slope + lam) / (a * lam),
                -1,
                -1,
                slope * t / (a * lam),
                (a + slope * t) / a,
                t * (a + 1) * (lam + slope) / (a * lam),
                t * (2 * a * lam + a * slope + lam) / (a * lam),
                1,
            )
        )
    if chart == "B_full" and sheet == "S2":
        return sp.Matrix(
            (
                -a
                * t
                * (2 * a * lam + a * slope + lam + slope)
                / (lam * (a + 1)),
                -1,
                -1,
                slope * t / (lam * (a + 1)),
                (a + slope * t + 1) / (a + 1),
                t
                * (2 * a * lam + a * slope + lam + slope)
                / (lam * (a + 1)),
                a * t * (lam + slope) / (lam * (a + 1)),
                1,
            )
        )
    if chart == "B_drop" and sheet == "S1":
        return sp.Matrix(
            (
                -t * (a + 1) * s0 / a,
                -1,
                -1,
                0,
                0,
                t * (a + 1) / a,
                t * s0 / a,
                1,
            )
        )
    return sp.Matrix(
        (
            -a * t * s0 / (a + 1),
            -1,
            -1,
            0,
            0,
            t * s0 / (a + 1),
            a * t / (a + 1),
            1,
        )
    )


def finite_d01_audit(chart: str, sheet: str) -> dict[str, object]:
    started = time.perf_counter()
    a, lam, slope, t = sp.symbols("a lambda r t")
    shifts = (0, 0, t, 0) if sheet == "S1" else (0, t, 0, 0)
    model = reconstruct_model(chart, "D01_finite", a, lam, slope, shifts)
    extensions = model["extensions"]
    mixed = model["mixed"]
    diagonal_alpha = model["diagonal_alpha"]
    diagonal_beta = model["diagonal_beta"]
    assert isinstance(extensions, tuple)
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(diagonal_alpha, sp.Expr)
    assert isinstance(diagonal_beta, sp.Expr)

    vector = kernel_generator(chart, sheet, a, lam, slope, t)
    assert all(sp.factor(entry) == 0 for entry in mixed * vector)
    witness = sp.factor(mixed.extract(RANK_ROWS, RANK_COLUMNS).det())
    expected_witness = -4 * a**3 * slope**6 * (a + 1) ** 3 * (2 * a + 1) ** 2
    if chart == "B_full":
        expected_witness *= lam
    assert_equal(witness, expected_witness)
    assert vector[1] == vector[2] == -1

    substitution = dict(zip(extensions, vector))
    first = sp.factor(diagonal_alpha.subs(substitution))
    second = sp.factor(diagonal_beta.subs(substitution))
    assert_equal(first, -2 * slope * (2 * a + 1))
    if chart == "B_full" and sheet == "S1":
        expected_second = (
            -2 * (a + slope * t) * (2 * a + 1) * (lam + slope) / a
        )
    elif chart == "B_full":
        expected_second = (
            -2
            * (2 * a + 1)
            * (lam + slope)
            * (a + slope * t + 1)
            / (a + 1)
        )
    elif sheet == "S1":
        expected_second = -2 * (a + slope * t) * (2 * a + 1) / a
    else:
        expected_second = (
            -2 * (2 * a + 1) * (a + slope * t + 1) / (a + 1)
        )
    assert_equal(second, expected_second)

    marked = marked_matrix(model, marked_mode=3)
    minor = sp.factor(marked.subs(substitution)[[0, 1, 4, 7], :].det())
    normalized_ratio = sp.factor(sp.cancel(minor / (first * second)))
    expected_ratio = -2 * a**2 * slope * (lam if chart == "B_full" else 1)
    assert_equal(normalized_ratio, expected_ratio)

    projective_scale = sp.Symbol("c", nonzero=True)
    scaled_substitution = {
        extension: projective_scale * entry
        for extension, entry in zip(extensions, vector)
    }
    scaled_first = sp.factor(diagonal_alpha.subs(scaled_substitution))
    scaled_second = sp.factor(diagonal_beta.subs(scaled_substitution))
    scaled_minor = sp.factor(
        marked.subs(scaled_substitution)[[0, 1, 4, 7], :].det()
    )
    assert_equal(scaled_first, projective_scale * first)
    assert_equal(scaled_second, projective_scale * second)
    assert_equal(scaled_minor, projective_scale**3 * minor)
    scaled_ratio = sp.factor(
        sp.cancel(scaled_minor / (scaled_first * scaled_second))
    )
    assert_equal(scaled_ratio, projective_scale * expected_ratio)

    open_factors = ["a", "a+1", "2*a+1", "r"]
    if chart == "B_full":
        open_factors.append("lambda")
    beta_factors = (
        ["lambda+r", "a+r*t" if sheet == "S1" else "a+r*t+1"]
        if chart == "B_full"
        else ["a+r*t" if sheet == "S1" else "a+r*t+1"]
    )
    return {
        "verdict": "VERIFIED",
        "chart": chart,
        "direction": "finite D01",
        "sheet": sheet,
        "kernel_generator": [str(sp.factor(entry)) for entry in vector],
        "kernel_annihilated": True,
        "rank_witness_rows": list(RANK_ROWS),
        "rank_witness_columns": list(RANK_COLUMNS),
        "rank_witness": str(witness),
        "mixed_rank_on_open": 7,
        "kernel_dimension_on_open": 1,
        "all_alpha_diagonal": str(first),
        "all_beta_diagonal": str(second),
        "marked_mode": 3,
        "minor_rows": [0, 1, 4, 7],
        "normalized_minor_over_diagonal_product": str(normalized_ratio),
        "projective_scaling": {
            "extension_vector": "c*v with c nonzero",
            "diagonals_scale_as": "c",
            "fixed_minor_scales_as": "c^3",
            "ratio_scales_as": str(scaled_ratio),
            "rank_four_conclusion_is_scale_invariant": True,
        },
        "explicit_chart_and_rank_open_factors": open_factors,
        "additional_factors_for_beta_genuineness": beta_factors,
        "no_condition_on_t": True,
        "every_genuine_projective_extension_has_marked_rank_four": True,
        "exceptional_a=0_or_minus1_covered": False,
        "seconds": round(time.perf_counter() - started, 3),
    }


def d23_rational_audit() -> dict[str, object]:
    a, lam, slope, t = sp.symbols("a lambda r t")
    sample = {a: 2, lam: 3, slope: 5, t: 7}
    ranks: dict[str, dict[str, int]] = {}
    for chart in ("B_full", "B_drop"):
        ranks[chart] = {}
        for sheet, shifts in (
            ("S1", (0, 0, t, 0)),
            ("S2", (0, t, 0, 0)),
        ):
            model = reconstruct_model(
                chart, "D23_finite", a, lam, slope, shifts
            )
            mixed = model["mixed"]
            assert isinstance(mixed, sp.MatrixBase)
            rank = mixed.subs(sample).rank()
            assert rank == (8 if chart == "B_full" else 7)
            ranks[chart][sheet] = rank
    return {
        "verdict": "VERIFIED_AS_AUDIT_ONLY",
        "sample": {str(symbol): value for symbol, value in sample.items()},
        "ranks": ranks,
        "exact_rational_arithmetic": True,
        "characteristic_zero_nonexistence_inference": False,
        "finite_D23_closed": False,
    }


def main() -> None:
    started = time.perf_counter()
    hall = hall_support_audit()
    projections = projection_audits()
    finite_d01 = [
        finite_d01_audit(chart, sheet)
        for chart in ("B_full", "B_drop")
        for sheet in ("S1", "S2")
    ]
    d23 = d23_rational_audit()
    report = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "UNKNOWN",
        "scope": (
            "independent audit of the partial weighted-H22 checkpoint on the "
            "component-20 p+q boundary charts"
        ),
        "inputs": {
            THEOREM.name: sha256(THEOREM),
            PRIMARY.name: sha256(PRIMARY),
            P4_BOUNDARY.name: sha256(P4_BOUNDARY),
        },
        "method": (
            "independent exact Hall support; characteristic-zero bidirectional "
            "elimination; kernel, rank-witness, diagonal, marked-minor, and "
            "projective-scaling reconstruction; exact-rational D23 audit"
        ),
        "command": (
            'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py'
        ),
        "outputs": {AUDIT.name: sha256(AUDIT)},
        "limitations": (
            "overall UNKNOWN; conditional on the p+q chart classification; "
            "a=0,-1, D01 infinity, finite D23, closure beyond the displayed "
            "charts, arbitrary-order gluing, and global Krenn-Gu remain open"
        ),
        "subclaim_verdicts": {
            "half_replacement_Hall_obstruction": hall,
            "eight_generic_projection_ideals": projections,
            "four_generic_finite_D01_certificates": finite_d01,
            "D23_rational_sample": d23,
        },
        "independent_verifier_complete_for_stated_partial_subclaims": True,
        "overall_weighted_H22_resolved": False,
        "projection_closures_treated_as_actual_fibres": False,
        "exceptional_a=0_or_minus1_closed": False,
        "D01_infinity_closed": False,
        "finite_D23_closed": False,
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
        "runtime_seconds": round(time.perf_counter() - started, 3),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
