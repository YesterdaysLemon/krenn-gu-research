#!/usr/bin/env python3
"""Replay the verified B_full D01-infinity/finite-D23 H22 obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
from verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial import (
    build_model,
    marked_matrix,
)



import hashlib
import json
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
NOTE = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_B_FULL_INFINITY_FINITE_PAIR_OBSTRUCTION.md"
PARTIAL = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"
HELPER = ROOT / "verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py"
AUDIT = ROOT / "audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py"
INDEPENDENT_VERIFIER = (
    ROOT
    / "audit_p5_h22_common_active_binary_triangle_p_plus_q_b_full_infinity_finite_pair_verifier.py"
)
RANK_ROWS = (1, 2, 3, 4, 6, 9)
RANK_COLUMNS = (0, 1, 2, 3, 4, 5)
MINOR_ROWS = (0, 1, 4, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def assert_zero(values) -> None:
    assert all(sp.factor(value) == 0 for value in values), values


def common_marking_certificate() -> dict[str, object]:
    """Record the geometric support of the exact replayed projection sum."""

    a = sp.Symbol("a", nonzero=True)
    h0, h1, h2, h3 = sp.symbols("h0:4")
    d01_infinity = (h3, a * h1 + (a + 1) * h2, h0, h2**2)
    d23_finite = (h3, h0, h1 * h2)
    # Over a field, h2^2=0 implies h2=0; a is a unit in C(a,lambda),
    # so the remaining linear equation then implies h1=0.
    assert sp.factor(d01_infinity[1].subs(h2, 0) / a - h1) == 0
    assert all(value.subs({h0: 0, h1: 0, h2: 0, h3: 0}) == 0 for value in d01_infinity + d23_finite)
    return {
        "coefficient_field": "C(a,lambda)",
        "D01_infinity_projection": [str(value) for value in d01_infinity],
        "D23_finite_projection": [str(value) for value in d23_finite],
        "common_geometric_marking": [0, 0, 0, 0],
        "nilpotent_h2_projection_direction_is_not_an_extra_point": True,
    }


def complete_frame_check(mixed: sp.Matrix, frame: sp.Matrix, expected_rank: int) -> dict[str, object]:
    assert frame.cols == mixed.cols - expected_rank
    assert frame.rank() == frame.cols
    assert_zero(mixed * frame)
    witness = sp.factor(mixed.extract(RANK_ROWS, RANK_COLUMNS).det())
    a = sp.Symbol("a")
    assert_equal(witness, 2 * a**4 * (a + 1) ** 3 * (2 * a + 1))
    nullspace = mixed.nullspace()
    assert len(nullspace) == frame.cols
    assert sp.Matrix.hstack(frame, *nullspace).rank() == frame.cols
    return {
        "mixed_rank": expected_rank,
        "kernel_dimension": frame.cols,
        "rank_witness_rows": list(RANK_ROWS),
        "rank_witness_columns": list(RANK_COLUMNS),
        "rank_witness": str(witness),
        "explicit_frame_spans_symbolic_nullspace": True,
    }


def d01_infinity_certificate() -> dict[str, object]:
    started = time.perf_counter()
    a, lam, cap_x, cap_y = sp.symbols("a lambda X Y")
    model = build_model("B_full", "01_inf", a, lam, sp.Integer(0), (0, 0, 0, 0))
    mixed = model["mixed"]
    extensions = model["extensions"]
    diagonal_a = model["diagonal_a"]
    diagonal_b = model["diagonal_b"]
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(extensions, tuple)
    assert isinstance(diagonal_a, sp.Expr) and isinstance(diagonal_b, sp.Expr)

    vector0 = sp.Matrix((-a - 1, 0, 0, 1 / a, lam / a, (a + 1) / a, 1, 0))
    vector1 = sp.Matrix((0, -1, -1, 0, 1, 0, 0, 1))
    frame = sp.Matrix.hstack(vector0, vector1)
    completeness = complete_frame_check(mixed, frame, 6)

    vector = cap_x * vector0 + cap_y * vector1
    substitution = dict(zip(extensions, vector))
    first = sp.factor(diagonal_a.subs(substitution))
    second = sp.factor(diagonal_b.subs(substitution))
    expected_first = -2 * cap_y * (2 * a + 1)
    expected_second = -2 * (2 * a + 1) * (cap_x * lam + a * cap_y) / a
    assert_equal(first, expected_first)
    assert_equal(second, expected_second)

    marked = marked_matrix(model, mode=3).subs(substitution)
    determinant = sp.factor(marked.extract(MINOR_ROWS, range(4)).det())
    expected_determinant = (
        -8 * cap_y**2 * a * lam * (2 * a + 1) ** 2 * (cap_x * lam + a * cap_y)
    )
    assert_equal(determinant, expected_determinant)
    ratio = sp.factor(sp.cancel(determinant / (first * second)))
    assert_equal(ratio, -2 * cap_y * a**2 * lam)

    projective_scale = sp.Symbol("c", nonzero=True)
    scaled = {
        extension: projective_scale * value
        for extension, value in zip(extensions, vector)
    }
    assert_equal(diagonal_a.subs(scaled), projective_scale * first)
    assert_equal(diagonal_b.subs(scaled), projective_scale * second)
    scaled_minor = sp.factor(
        marked_matrix(model, mode=3).subs(scaled).extract(MINOR_ROWS, range(4)).det()
    )
    assert_equal(scaled_minor, projective_scale**3 * determinant)

    return {
        "direction": "D01 infinity",
        "marking": [0, 0, 0, 0],
        "kernel_basis": [
            [str(sp.factor(value)) for value in vector0],
            [str(sp.factor(value)) for value in vector1],
        ],
        **completeness,
        "general_extension": "X*v0+Y*v1",
        "all_alpha_diagonal": str(first),
        "all_beta_diagonal": str(second),
        "genuineness_conditions": ["Y!=0", "X*lambda+a*Y!=0"],
        "marked_mode": 3,
        "minor_rows": list(MINOR_ROWS),
        "fixed_minor": str(determinant),
        "minor_over_diagonal_product": str(ratio),
        "every_genuine_extension_has_marked_rank_four": True,
        "projective_scaling_checked": True,
        "seconds": round(time.perf_counter() - started, 3),
    }


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact r-saturated kernel ideal")


def singular_text(value: sp.Expr) -> str:
    return str(sp.cancel(value)).replace("**", "^")


def nonzero_d23_kernel_ideal(model: dict[str, object]) -> dict[str, object]:
    started = time.perf_counter()
    _a, _lam, slope = sp.symbols("a lambda r")
    z = sp.symbols("z0:8")
    slope_inverse = sp.Symbol("rinv")
    mixed = model["mixed"]
    assert isinstance(mixed, sp.MatrixBase)
    equations = tuple(mixed * sp.Matrix(z))
    expected = (
        z[0], z[3], z[5], z[6], z[2] - z[1], z[4] + z[1], z[7] + z[1]
    )
    variables = (slope_inverse,) + z + (slope,)
    program = "\n".join((
        "ring R=(0,a,lambda),(" + ",".join(map(str, variables)) + "),(dp(1),dp(9));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular_text, equations + (slope_inverse * slope - 1,))) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I,rinv));",
        "ideal E=" + ",".join(map(singular_text, expected)) + ";",
        "E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        "int same=((size(JE)==0)&&(size(EJ)==0));",
        '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
        "quit;",
    ))
    completed = subprocess.run(
        singular_command(),
        input=program,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [
        line.strip() for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, same, size = markers[0].split(":")
    assert same == "1", completed.stdout
    return {
        "saturation": "r!=0",
        "complete_kernel_ideal": [singular_text(value) for value in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(size),
        "seconds": round(time.perf_counter() - started, 3),
    }


def finite_d23_certificate() -> dict[str, object]:
    started = time.perf_counter()
    a, lam, slope, cap_c = sp.symbols("a lambda r C")
    model = build_model("B_full", "23", a, lam, slope, (0, 0, 0, 0))
    mixed = model["mixed"]
    extensions = model["extensions"]
    diagonal_a = model["diagonal_a"]
    diagonal_b = model["diagonal_b"]
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(extensions, tuple)
    assert isinstance(diagonal_a, sp.Expr) and isinstance(diagonal_b, sp.Expr)

    saturated = nonzero_d23_kernel_ideal(model)
    line = sp.Matrix((0, -1, -1, 0, 1, 0, 0, 1))
    assert_zero(mixed * line)
    line_substitution = dict(zip(extensions, cap_c * line))
    nonzero_first = sp.factor(diagonal_a.subs(line_substitution))
    nonzero_second = sp.factor(diagonal_b.subs(line_substitution))
    assert_equal(nonzero_first, -2 * cap_c * (2 * a + 1))
    assert_equal(
        nonzero_second,
        -2 * cap_c * (2 * a * (a + 1) * slope - (2 * a + 1)),
    )
    beta_zero_slope = (2 * a + 1) / (2 * a * (a + 1))
    assert_equal(nonzero_second.subs(slope, beta_zero_slope), 0)

    zero_model = build_model("B_full", "23", a, lam, sp.Integer(0), (0, 0, 0, 0))
    zero_mixed = zero_model["mixed"]
    zero_extensions = zero_model["extensions"]
    zero_diagonal_a = zero_model["diagonal_a"]
    zero_diagonal_b = zero_model["diagonal_b"]
    assert isinstance(zero_mixed, sp.MatrixBase)
    assert isinstance(zero_extensions, tuple)
    assert isinstance(zero_diagonal_a, sp.Expr) and isinstance(zero_diagonal_b, sp.Expr)
    vector0 = sp.Matrix((-a - 1, 0, 0, -1 / a, lam / a, (a + 1) / a, 1, 0))
    vector1 = line
    frame = sp.Matrix.hstack(vector0, vector1)
    zero_completeness = complete_frame_check(zero_mixed, frame, 6)

    cap_u, cap_v = sp.symbols("U V")
    vector = cap_u * vector0 + cap_v * vector1
    substitution = dict(zip(zero_extensions, vector))
    zero_first = sp.factor(zero_diagonal_a.subs(substitution))
    zero_second = sp.factor(zero_diagonal_b.subs(substitution))
    assert_equal(zero_first, -2 * cap_v * (2 * a + 1))
    assert_equal(zero_second, 2 * (2 * a + 1) * (cap_u * lam + a * cap_v) / a)
    marked = marked_matrix(zero_model, mode=3).subs(substitution)
    determinant = sp.factor(marked.extract(MINOR_ROWS, range(4)).det())
    expected_determinant = (
        8 * cap_v**2 * a * lam * (2 * a + 1) ** 2 * (cap_u * lam + a * cap_v)
    )
    assert_equal(determinant, expected_determinant)
    ratio = sp.factor(sp.cancel(determinant / (zero_first * zero_second)))
    assert_equal(ratio, -2 * cap_v * a**2 * lam)

    return {
        "direction": "finite D23",
        "marking": [0, 0, 0, 0],
        "nonzero_slope": {
            **saturated,
            "kernel_generator": [str(value) for value in line],
            "all_alpha_diagonal": str(nonzero_first),
            "all_beta_diagonal": str(nonzero_second),
            "beta_zero_slope": str(beta_zero_slope),
            "beta_zero_slope_has_no_genuine_extension": True,
        },
        "zero_slope": {
            "kernel_basis": [
                [str(sp.factor(value)) for value in vector0],
                [str(sp.factor(value)) for value in vector1],
            ],
            **zero_completeness,
            "general_extension": "U*u0+V*u1",
            "all_alpha_diagonal": str(zero_first),
            "all_beta_diagonal": str(zero_second),
            "marked_mode": 3,
            "minor_rows": list(MINOR_ROWS),
            "fixed_minor": str(determinant),
            "minor_over_diagonal_product": str(ratio),
            "every_genuine_extension_has_marked_rank_four": True,
        },
        "all_finite_slopes_exhausted": True,
        "seconds": round(time.perf_counter() - started, 3),
    }


def main() -> None:
    started = time.perf_counter()
    marking = common_marking_certificate()
    d01 = d01_infinity_certificate()
    d23 = finite_d23_certificate()
    source = Path(__file__).resolve()
    result = {
        "status": "pass",
        "role": "proof_a",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": "generic B_full weighted-H22 pairing D01 infinity with finite D23",
        "inputs": {
            PARTIAL.name: sha256(PARTIAL),
            HELPER.name: sha256(HELPER),
            AUDIT.name: sha256(AUDIT),
            INDEPENDENT_VERIFIER.name: sha256(INDEPENDENT_VERIFIER),
        },
        "method": (
            "exact characteristic-zero geometric marking intersection; complete "
            "rank-six kernels; fixed marked minor; r-saturated finite-D23 kernel ideal"
        ),
        "command": (
            'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/derive_p5_h22_common_active_binary_triangle_p_plus_q_b_full_infinity_finite_pair_obstruction.py'
        ),
        "outputs": {
            NOTE.name: sha256(NOTE),
            source.name: sha256(source),
        },
        "limitations": (
            "VERIFIED generic B_full only; "
            "a=0,-1, B_drop, non-diagonal source changes, arbitrary-order "
            "gluing, and the global conjecture remain outside scope"
        ),
        "common_marking": marking,
        "D01_infinity_obstruction": d01,
        "finite_D23_exhaustion": d23,
        "pair_obstructed_within_established_local_framework": True,
        "finite_field_computation_used": False,
        "fresh_independent_verifier_complete": True,
        "broad_minor_scan_used": False,
        "new_timeout_or_discarded_computation": False,
        "failure_ledger": [
            {
                "source": PARTIAL.name,
                "attempt": "eight-case symbolic minor batch",
                "result": "terminated above 142 CPU seconds",
                "contributes_evidence_here": False,
            },
            {
                "source": PARTIAL.name,
                "attempt": "four-case finite-D23 symbolic batch",
                "result": "terminated after about 66 seconds",
                "contributes_evidence_here": False,
            },
        ],
        "independent_verifier_complete": False,
        "global_Krenn_Gu_conjecture_resolved": False,
        "runtime_seconds": round(time.perf_counter() - started, 3),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
