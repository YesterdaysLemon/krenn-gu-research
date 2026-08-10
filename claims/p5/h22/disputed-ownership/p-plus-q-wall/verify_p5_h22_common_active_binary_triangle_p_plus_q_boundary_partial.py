#!/usr/bin/env python3
"""Verify the partial weighted-H22 checkpoint on component 20's p+q boundary."""

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
THEOREM = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"
P4_BOUNDARY = REPO_ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
INDEPENDENT_AUDIT = (
    ROOT / "audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:15]
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


def permanent3(
    rows: tuple[tuple[sp.Expr, ...], ...], columns: tuple[int, ...] = (0, 1, 2)
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


def add(*vectors: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(entries)) for entries in zip(*vectors))


def scale(scalar: sp.Expr, vector: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(scalar * entry) for entry in vector)


def chart_bases(
    chart: str, a: sp.Expr, lam: sp.Expr
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, sp.Integer(1), -1, 0)
    em = (0, sp.Integer(1), 1, 0)
    cap_c = (0, 0, 0, sp.Integer(1))
    s0 = 2 * a + 1
    k0 = add(scale(s0, cap_c), scale(-a * (a + 1), ell))
    alpha = (k0, e, e, em)
    beta = (
        add(e, scale(lam, ell)) if chart == "B_full" else ell,
        add(scale(a + 1, ell), cap_c),
        add(scale(a, ell), cap_c),
        e,
    )
    return alpha, beta


def shifted_basis(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def weighted_row(
    row: tuple[sp.Expr, ...], extension: sp.Expr, direction: str, slope: sp.Expr
) -> tuple[sp.Expr, ...]:
    if direction == "01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "01_inf":
        return (row[0], row[2], row[3], extension)
    if direction == "23_inf":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def build_model(
    chart: str,
    direction: str,
    a: sp.Expr,
    lam: sp.Expr,
    slope: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> dict[str, object]:
    alpha, canonical_beta = chart_bases(chart, a, lam)
    beta = shifted_basis(alpha, canonical_beta, shifts)
    extensions = sp.symbols("z0:8")
    alpha_d = tuple(
        weighted_row(alpha[i], extensions[i], direction, slope) for i in range(4)
    )
    beta_d = tuple(
        weighted_row(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )

    def coefficient(word: tuple[int, ...]) -> sp.Expr:
        selected = tuple(beta_d[i] if word[i] else alpha_d[i] for i in range(4))
        return sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j] for j in range(4) if j != i))
                for i in range(4)
            )
        )

    coefficients = {word: coefficient(word) for word in WORDS}
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], extension) for extension in extensions]
            for word in MIXED_WORDS
        ]
    )
    return {
        "alpha": alpha,
        "beta": beta,
        "extensions": extensions,
        "alpha_d": alpha_d,
        "beta_d": beta_d,
        "mixed": mixed,
        "diagonal_a": coefficients[WORDS[0]],
        "diagonal_b": coefficients[WORDS[-1]],
    }


def marked_matrix(model: dict[str, object], mode: int) -> sp.Matrix:
    alpha_d = model["alpha_d"]
    beta_d = model["beta_d"]
    assert isinstance(alpha_d, tuple) and isinstance(beta_d, tuple)
    other_modes = tuple(index for index in range(4) if index != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_d[other] if bits[index] else alpha_d[other]
            for index, other in enumerate(other_modes)
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


def assert_zero(matrix: sp.Matrix) -> None:
    assert all(sp.factor(entry) == 0 for entry in matrix)


def hall_certificate() -> dict[str, object]:
    rho, sigma = sp.symbols("rho sigma")
    source_scales = sp.symbols("s0:4", nonzero=True)
    extensions = sp.symbols("x0:4")
    ell = (0, sp.Integer(1), -1, 0)
    e = (sp.Integer(1), 0, 0, 0)
    em = (0, sp.Integer(1), 1, 0)
    alpha = (ell, e, e, em)
    rows = tuple(
        (
            rho * source_scales[0] * row[0] + sigma * source_scales[1] * row[1],
            source_scales[2] * row[2],
            source_scales[3] * row[3],
            extensions[mode],
        )
        for mode, row in enumerate(alpha)
    )
    expected = (
        (sigma * source_scales[1], -source_scales[2], 0, extensions[0]),
        (rho * source_scales[0], 0, 0, extensions[1]),
        (rho * source_scales[0], 0, 0, extensions[2]),
        (sigma * source_scales[1], source_scales[2], 0, extensions[3]),
    )
    assert rows == expected
    supports = tuple(
        tuple(index for index, entry in enumerate(row) if entry != 0) for row in rows
    )
    assert all(2 not in support for support in supports)
    diagonal = permanent4(rows)
    assert diagonal == 0
    return {
        "family": "a=-1/2 replacement, all k",
        "direction": "D01 homogeneous (rho:sigma)",
        "kernel_row_supports": [list(support) for support in supports],
        "missing_channel": 2,
        "all_kernel_diagonal_identically_zero": True,
        "all_markings_and_extensions": True,
        "both_projective_slope_endpoints": True,
        "weighted_H22_fibre_empty_within_local_framework": True,
    }


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact projection replay")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def projection_certificate(
    chart: str, direction: str, expected: tuple[sp.Expr, ...]
) -> dict[str, object]:
    started = time.perf_counter()
    a, lam, slope = sp.symbols("a lambda r")
    shifts = sp.symbols("h0:4")
    model = build_model(chart, direction, a, lam, slope, shifts)
    extensions = model["extensions"]
    mixed = model["mixed"]
    diagonal_a = model["diagonal_a"]
    diagonal_b = model["diagonal_b"]
    assert isinstance(extensions, tuple)
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(diagonal_a, sp.Expr) and isinstance(diagonal_b, sp.Expr)
    inverse = sp.Symbol("w")
    equations = (
        *tuple(mixed * sp.Matrix(extensions)),
        diagonal_a - 1,
        inverse * diagonal_b - 1,
    )
    finite = direction in ("01", "23")
    eliminated = extensions + ((inverse, slope) if finite else (inverse,))
    variables = eliminated + shifts
    parameters = (a, lam) if chart == "B_full" else (a,)
    blocks = "(dp(10),dp(4))" if finite else "(dp(9),dp(4))"
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
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular, expected)) + ";",
            "E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "int same=((size(JE)==0)&&(size(EJ)==0));",
            '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
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
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, same, size = markers[0].split(":")
    assert same == "1", completed.stdout
    return {
        "chart": chart,
        "direction": direction,
        "projected_ideal": [singular(entry) for entry in expected],
        "bidirectional_exact_equality": True,
        "standard_basis_size": int(size),
        "projection_is_closure": True,
        "seconds": round(time.perf_counter() - started, 3),
    }


def projection_certificates() -> list[dict[str, object]]:
    a = sp.Symbol("a")
    h0, h1, h2, h3 = sp.symbols("h0:4")
    finite = (h3, h0, h1 * h2)
    expectations = {
        "B_full": {
            "01": finite,
            "23": finite,
            "01_inf": (h3, a * h1 + (a + 1) * h2, h0, h2**2),
            "23_inf": (sp.Integer(1),),
        },
        "B_drop": {
            "01": finite,
            "23": finite,
            "01_inf": finite,
            "23_inf": (sp.Integer(1),),
        },
    }
    return [
        projection_certificate(chart, direction, expected)
        for chart, chart_expectations in expectations.items()
        for direction, expected in chart_expectations.items()
    ]


def expected_kernel(
    chart: str, sheet: str, a: sp.Expr, lam: sp.Expr, slope: sp.Expr, t: sp.Expr
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
                -a * t * (2 * a * lam + a * slope + lam + slope) / (lam * (a + 1)),
                -1,
                -1,
                slope * t / (lam * (a + 1)),
                (a + slope * t + 1) / (a + 1),
                t * (2 * a * lam + a * slope + lam + slope) / (lam * (a + 1)),
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


def finite_d01_certificate(chart: str, sheet: str) -> dict[str, object]:
    started = time.perf_counter()
    a, lam, slope, t = sp.symbols("a lambda r t")
    shifts = (0, 0, t, 0) if sheet == "S1" else (0, t, 0, 0)
    model = build_model(chart, "01", a, lam, slope, shifts)
    mixed = model["mixed"]
    extensions = model["extensions"]
    diagonal_a = model["diagonal_a"]
    diagonal_b = model["diagonal_b"]
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(extensions, tuple)
    assert isinstance(diagonal_a, sp.Expr) and isinstance(diagonal_b, sp.Expr)
    vector = expected_kernel(chart, sheet, a, lam, slope, t)
    assert_zero(mixed * vector)
    nullspace = mixed.nullspace()
    assert len(nullspace) == 1
    assert sp.Matrix.hstack(vector).rank() == 1
    witness = sp.factor(mixed.extract(RANK_ROWS, RANK_COLUMNS).det())
    expected_witness = -4 * a**3 * slope**6 * (a + 1) ** 3 * (2 * a + 1) ** 2
    if chart == "B_full":
        expected_witness *= lam
    assert_equal(witness, expected_witness)
    substitutions = dict(zip(extensions, vector))
    first = sp.factor(diagonal_a.subs(substitutions))
    second = sp.factor(diagonal_b.subs(substitutions))
    assert_equal(first, -2 * slope * (2 * a + 1))
    if chart == "B_full" and sheet == "S1":
        expected_second = -2 * (a + slope * t) * (2 * a + 1) * (lam + slope) / a
    elif chart == "B_full":
        expected_second = (
            -2 * (2 * a + 1) * (lam + slope) * (a + slope * t + 1) / (a + 1)
        )
    elif sheet == "S1":
        expected_second = -2 * (a + slope * t) * (2 * a + 1) / a
    else:
        expected_second = -2 * (2 * a + 1) * (a + slope * t + 1) / (a + 1)
    assert_equal(second, expected_second)
    marked = marked_matrix(model, mode=3).subs(substitutions)
    determinant = sp.factor(marked[[0, 1, 4, 7], :].det())
    ratio = sp.factor(sp.cancel(determinant / (first * second)))
    expected_ratio = -2 * a**2 * slope * (lam if chart == "B_full" else 1)
    assert_equal(ratio, expected_ratio)
    return {
        "chart": chart,
        "direction": "finite D01",
        "marking_sheet": sheet,
        "kernel_generator": [str(sp.factor(entry)) for entry in vector],
        "mixed_rank": 7,
        "kernel_dimension": 1,
        "rank_witness_rows": list(RANK_ROWS),
        "rank_witness_columns": list(RANK_COLUMNS),
        "rank_witness_determinant": str(witness),
        "all_alpha_diagonal": str(first),
        "all_beta_diagonal": str(second),
        "marked_mode": 3,
        "minor_rows": [0, 1, 4, 7],
        "minor_over_diagonal_product": str(ratio),
        "every_genuine_projective_extension_has_rank_four": True,
        "exceptional_a=0_or_minus1_covered": False,
        "seconds": round(time.perf_counter() - started, 3),
    }


def d23_rational_diagnosis() -> dict[str, object]:
    a, lam, slope, t = sp.symbols("a lambda r t")
    sample = {a: 2, lam: 3, slope: 5, t: 7}
    ranks = {}
    for chart in ("B_full", "B_drop"):
        ranks[chart] = {}
        for sheet, shifts in (
            ("S1", (0, 0, t, 0)),
            ("S2", (0, t, 0, 0)),
        ):
            model = build_model(chart, "23", a, lam, slope, shifts)
            mixed = model["mixed"]
            assert isinstance(mixed, sp.MatrixBase)
            rank = mixed.subs(sample).rank()
            expected = 8 if chart == "B_full" else 7
            assert rank == expected
            ranks[chart][sheet] = {
                "rank": rank,
                "kernel_dimension": 8 - rank,
            }
    return {
        "sample": {str(symbol): value for symbol, value in sample.items()},
        "ranks": ranks,
        "exact_rational_arithmetic": True,
        "audit_only": True,
        "characteristic_zero_inference": False,
        "B_full_generic_rank_seven_ansatz_valid": False,
    }


def main() -> None:
    started = time.perf_counter()
    hall = hall_certificate()
    projections = projection_certificates()
    finite_d01 = [
        finite_d01_certificate(chart, sheet)
        for chart in ("B_full", "B_drop")
        for sheet in ("S1", "S2")
    ]
    d23 = d23_rational_diagnosis()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "UNKNOWN",
                "role": "construction",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "scope": (
                    "partial weighted H22 checkpoint on component-20 p+q "
                    "boundary charts"
                ),
                "inputs": {P4_BOUNDARY.name: sha256(P4_BOUNDARY)},
                "method": (
                    "exact Hall support, characteristic-zero projection, complete "
                    "finite-D01 kernels, rank witnesses, and fixed minors"
                ),
                "command": (
                    'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py'
                ),
                "outputs": {THEOREM.name: sha256(THEOREM)},
                "limitations": (
                    "overall UNKNOWN; no exceptional a=0,-1, D01 infinity, finite "
                    "D23, H31, arbitrary-order, or global closure"
                ),
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "exact_partial_subclaims": {
                    "half_replacement_Hall_obstruction": hall,
                    "generic_projection_ideals": projections,
                    "generic_finite_D01_obstruction": finite_d01,
                },
                "D23_exact_rational_diagnosis": d23,
                "failure_ledger": [
                    {
                        "attempt": "eight-case symbolic minor batch",
                        "result": "terminated above 142 CPU seconds",
                        "retained_output": False,
                        "contributes_evidence": False,
                    },
                    {
                        "attempt": "four-case finite-D23 symbolic batch",
                        "result": "terminated after about 66 seconds",
                        "retained_output": False,
                        "contributes_evidence": False,
                    },
                    {
                        "attempt": "generic-rank-seven B_full/D23 ansatz",
                        "result": "refuted by exact rational rank-eight diagnosis",
                        "silently_repaired": False,
                    },
                ],
                "independent_verifier": {
                    "file": INDEPENDENT_AUDIT.name,
                    "sha256": sha256(INDEPENDENT_AUDIT),
                    "complete_for_stated_partial_subclaims": True,
                },
                "projection_closure_treated_as_actual_fibre": False,
                "exceptional_a=0_or_minus1_closed": False,
                "D01_infinity_closed": False,
                "finite_D23_closed": False,
                "finite_field_computation_used": False,
                "finite_field_inference_used": False,
                "H31_claim_made": False,
                "global_Krenn_Gu_conjecture_resolved": False,
                "runtime_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
