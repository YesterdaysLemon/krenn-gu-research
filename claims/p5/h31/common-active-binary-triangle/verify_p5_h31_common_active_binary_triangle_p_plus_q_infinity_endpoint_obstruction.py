#!/usr/bin/env python3
"""Construct the candidate direct H31 obstruction on two infinity endpoints."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

from verify_p5_h31_marked_basis_open_branch import (  # noqa: E402
    marked_extension,
    mixed_matrix,
)

THEOREM = (
    HERE
    / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md"
)
P4_BOUNDARY = REPO_ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
GENERIC_COMPONENT_14 = (
    REPO_ROOT / "claims" / "p5" / "h31" / "full-support-tangent"
    / "P5_H31_FULL_SUPPORT_TANGENT_COMPONENT_GENERIC_OBSTRUCTION.md"
)
GENERIC_MINOR_ROWS = ((0, 1, 4, 7), (0, 4, 5, 7))
FIXED_MINOR_ROWS = (0, 1, 2, 7)


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


def endpoint_bases(gamma: sp.Expr):
    e = (sp.Integer(1), 0, 0, 0)
    w = (0, 1, 1, 1)
    u = (0, 1, -1, 0)
    v1 = (0, 1, 1, 0)
    v2 = (0, 0, 0, 1)
    alpha = (
        e,
        e,
        tuple(-value for value in u),
        tuple(2 * v2[index] - v1[index] for index in range(4)),
    )
    beta = (
        w,
        w,
        e,
        tuple(gamma * e[index] + v1[index] for index in range(4)),
    )
    return alpha, beta


def shifted_beta(alpha, beta, shifts):
    return tuple(
        tuple(
            sp.expand(beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def assert_zero(matrix: sp.Matrix) -> None:
    assert all(sp.factor(entry) == 0 for entry in matrix), matrix


def plane_geometry_certificate() -> dict[str, object]:
    alpha_zero, beta_zero = endpoint_bases(sp.Integer(0))
    alpha_two, beta_two = endpoint_bases(sp.Integer(2))
    assert alpha_zero == alpha_two
    e = sp.Matrix((1, 0, 0, 0))
    cap_a = sp.Matrix((0, 1, 0, 0))
    cap_b = sp.Matrix((0, 0, 1, 0))
    cap_c = sp.Matrix((0, 0, 0, 1))
    h = cap_a + cap_b
    off_wall = sp.Matrix.hstack(
        sp.Matrix(alpha_zero[3]), sp.Matrix(beta_zero[3])
    )
    off_target = sp.Matrix.hstack(h, cap_c)
    wall = sp.Matrix.hstack(sp.Matrix(alpha_two[3]), sp.Matrix(beta_two[3]))
    wall_target = sp.Matrix.hstack(2 * e + h, e + cap_c)
    assert off_wall.rank() == off_target.rank() == 2
    assert wall.rank() == wall_target.rank() == 2
    assert sp.Matrix.hstack(off_wall, off_target).rank() == 2
    assert sp.Matrix.hstack(wall, wall_target).rank() == 2
    return {
        "endpoint_mode_permutation": [1, 2, 3, 0],
        "source_normalization": ["e unchanged", "A/(P0*c1)", "-B/(P0*c2)", "C unchanged"],
        "component_14_parameters": {"p": -1, "q": 0, "S": 0},
        "off_wall_gamma": 0,
        "off_wall_U0": ["A+B", "C"],
        "off_wall_polar_parameter_t": 0,
        "wall_gamma": 2,
        "wall_U0": ["2e+A+B", "e+C"],
        "wall_polar_parameter_t": "1/2 after e scaling",
        "alpha": [list(map(str, row)) for row in alpha_zero],
        "beta_gamma_zero": [list(map(str, row)) for row in beta_zero],
        "beta_gamma_two": [list(map(str, row)) for row in beta_two],
    }


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact saturated projections")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def projection_certificate(
    gamma: int, distinguished: int, expected: tuple[sp.Expr, ...]
) -> dict[str, object]:
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inverse = sp.Symbol("wopen")
    alpha, canonical_beta = endpoint_bases(sp.Integer(gamma))
    beta = shifted_beta(alpha, canonical_beta, h)
    mixed, diagonal_a, diagonal_b = mixed_matrix(distinguished, alpha, beta)
    extension = sp.Matrix(z)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        inverse * (diagonal_b * extension)[0] - 1,
    )
    variables = z + (inverse,) + h
    lines = [
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, z + (inverse,))) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + ";",
        "E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        "int same=((size(JE)==0)&&(size(EJ)==0));",
        '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
        "quit;",
    ]
    completed = subprocess.run(
        singular_command(),
        input="\n".join(lines),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=20,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, same, size = markers[0].split(":")
    assert same == "1", completed.stdout
    return {
        "gamma": gamma,
        "distinguished_coordinate": distinguished,
        "projected_ideal": [singular(value) for value in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(size),
        "saturation_open": "A*B!=0",
    }


def projection_certificates() -> list[dict[str, object]]:
    h0, h1, h2, h3 = sp.symbols("h0:4")
    ideals = {
        0: {
            0: (sp.Integer(1),),
            1: (h3, h2, h0 * h1),
            2: (h3, h2, h0 * h1),
            3: (sp.Integer(1),),
        },
        2: {
            0: (sp.Integer(1),),
            1: (h3, h2, h0 + h1, h1**2),
            2: (h3, h2, h0 + h1, h1**2),
            3: (sp.Integer(1),),
        },
    }
    return [
        projection_certificate(gamma, distinguished, ideals[gamma][distinguished])
        for gamma in (0, 2)
        for distinguished in range(4)
    ]


def complete_kernel_frame(
    mixed: sp.Matrix,
    diagonal_a: sp.Matrix,
    diagonal_b: sp.Matrix,
    target_diagonals: sp.Matrix,
) -> tuple[sp.Matrix, dict[str, object]]:
    nullspace = mixed.nullspace()
    assert len(nullspace) == 2
    raw_frame = sp.Matrix.hstack(*nullspace)
    restricted = sp.Matrix.vstack(diagonal_a * raw_frame, diagonal_b * raw_frame)
    assert restricted.det() != 0
    frame = raw_frame * restricted.inv() * target_diagonals
    frame = frame.applyfunc(sp.cancel)
    assert frame.rank() == 2
    assert_zero(mixed * frame)
    assert_zero(diagonal_a * frame - target_diagonals[:1, :])
    assert_zero(diagonal_b * frame - target_diagonals[1:, :])
    pivot_columns = mixed.rref()[1]
    pivot_rows = mixed.T.rref()[1]
    witness = sp.factor(mixed.extract(pivot_rows[:6], pivot_columns[:6]).det())
    assert witness != 0
    return frame, {
        "mixed_rank": 6,
        "kernel_dimension": 2,
        "complete_kernel_frame": [[str(value) for value in frame.row(row)] for row in range(8)],
        "rank_witness_rows": list(pivot_rows[:6]),
        "rank_witness_columns": list(pivot_columns[:6]),
        "rank_witness_determinant": str(witness),
    }


def direct_kernel_certificate(
    gamma: int,
    distinguished: int,
    axis: str,
) -> dict[str, object]:
    T, x, y = sp.symbols("T x y")
    alpha, canonical_beta = endpoint_bases(sp.Integer(gamma))
    if gamma == 2:
        assert axis == "origin"
        shifts = (0, 0, 0, 0)
        diagonal_b_target = 4 * y
        expected_minor = -32 * x**2 * y
    elif axis == "h0_axis":
        shifts = (T, 0, 0, 0)
        diagonal_b_target = 4 * (T * x + y)
        expected_minor = -32 * x**2 * (T * x + y)
    else:
        assert axis == "h1_axis"
        shifts = (0, T, 0, 0)
        diagonal_b_target = 4 * (T * x + y)
        expected_minor = -32 * x**2 * (T * x + y)
    beta = shifted_beta(alpha, canonical_beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(distinguished, alpha, beta)
    assert mixed.rank() == 6
    sign = -1 if distinguished == 1 else 1
    target = sp.Matrix(((4 * sign, 0), (4 * T if gamma == 0 else 0, 4)))
    frame, kernel = complete_kernel_frame(mixed, diagonal_a, diagonal_b, target)
    extension = frame * sp.Matrix((x, y))
    marked = marked_extension(distinguished, extension, alpha, beta, mode=2)
    fixed_minor = sp.factor(marked[list(FIXED_MINOR_ROWS), :].det())
    assert sp.factor(fixed_minor - expected_minor) == 0
    assert sp.factor((diagonal_a * extension)[0] - 4 * sign * x) == 0
    assert sp.factor((diagonal_b * extension)[0] - diagonal_b_target) == 0
    generic_minors = tuple(
        sp.factor(marked[list(rows), :].det()) for rows in GENERIC_MINOR_ROWS
    )
    return {
        "gamma": gamma,
        "distinguished_coordinate": distinguished,
        "axis": axis,
        "shifts": [str(value) for value in shifts],
        **kernel,
        "kernel_extension": [str(value) for value in extension],
        "diagonal_A": str(sp.factor((diagonal_a * extension)[0])),
        "diagonal_B": str(sp.factor((diagonal_b * extension)[0])),
        "marked_mode": 2,
        "fixed_minor_rows": list(FIXED_MINOR_ROWS),
        "fixed_minor": str(fixed_minor),
        "generic_component_14_minor_rows": [list(rows) for rows in GENERIC_MINOR_ROWS],
        "same_row_minors_in_direct_endpoint_gauge": [str(value) for value in generic_minors],
        "same_row_minors_not_used_as_generic_specialization": True,
        "genuine_open_forces_fixed_minor_nonzero": True,
    }


def direct_kernel_certificates() -> list[dict[str, object]]:
    return [
        *(
            direct_kernel_certificate(0, distinguished, axis)
            for distinguished in (1, 2)
            for axis in ("h0_axis", "h1_axis")
        ),
        *(direct_kernel_certificate(2, distinguished, "origin") for distinguished in (1, 2)),
    ]


def generic_component_14_failure_certificate() -> dict[str, object]:
    """Record, but do not reuse, the singular generic-chart specialization."""

    p, q, t, a, b = sp.symbols("p q t a b")
    cap_s = p + q + 1
    assert cap_s.subs({p: -1, q: 0}) == 0
    generic_gauge_denominator = 2 * t * a * b
    assert generic_gauge_denominator.subs(t, 0) == 0
    return {
        "generic_source_gauge": "D00=(2*t*a*b)^-1",
        "off_wall_t": 0,
        "generic_source_gauge_defined_off_wall": False,
        "generic_minor_rows": [list(rows) for rows in GENERIC_MINOR_ROWS],
        "generic_cleared_minors_0147_0457_at_S_zero": [0, 0],
        "generic_resultant_ratios_at_endpoint": "0/0 in the singular gauge",
        "failure_source": "generic component-14 proof specialization; not a direct endpoint-matrix identity",
        "generic_formulas_used_as_endpoint_proof": False,
    }


def main() -> None:
    geometry = plane_geometry_certificate()
    projections = projection_certificates()
    kernels = direct_kernel_certificates()
    generic_failure = generic_component_14_failure_certificate()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "VERIFIED",
                "role": "construction",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "scope": "both component-14 infinity-endpoint faces arising from the component-20 p+q boundary",
                "inputs": {
                    P4_BOUNDARY.name: sha256(P4_BOUNDARY),
                    GENERIC_COMPONENT_14.name: sha256(GENERIC_COMPONENT_14),
                },
                "method": "exact saturated projections and direct complete-kernel marked-minor reconstruction",
                "command": "uv run --with sympy python claims/p5/h31/common-active-binary-triangle/verify_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py",
                "outputs": {THEOREM.name: sha256(THEOREM)},
                "limitations": "verified only for two diagonal-source-torus infinity endpoints; H22, other projective faces, arbitrary GL4, local-to-global, and global conjecture open",
                "plane_geometry": geometry,
                "saturated_projections": projections,
                "direct_kernel_certificates": kernels,
                "generic_component_14_gauge_failure": generic_failure,
                "finite_field_computation_used": False,
                "broad_scan_used": False,
                "both_endpoint_faces_H31_empty": "VERIFIED",
                "fresh_independent_verifier_complete": True,
                "global_Krenn_Gu_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
