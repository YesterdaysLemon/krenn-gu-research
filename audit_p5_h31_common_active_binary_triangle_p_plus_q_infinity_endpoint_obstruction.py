#!/usr/bin/env python3
"""Separate exact audit of the two component-14 infinity-endpoint H31 faces."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import marked_extension, mixed_matrix

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md"
FIXED_ROWS = (0, 1, 2, 7)


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


def bases(gamma: int):
    e = (1, 0, 0, 0)
    w = (0, 1, 1, 1)
    u = (0, 1, -1, 0)
    v1 = (0, 1, 1, 0)
    v2 = (0, 0, 0, 1)
    alpha = (e, e, tuple(-v for v in u), tuple(2 * v2[i] - v1[i] for i in range(4)))
    beta = (w, w, e, tuple(gamma * e[i] + v1[i] for i in range(4)))
    return alpha, beta


def shift(alpha, beta, h):
    return tuple(
        tuple(sp.expand(beta[i][j] + h[i] * alpha[i][j]) for j in range(4))
        for i in range(4)
    )


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.factor(value) == 0 for value in matrix)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular(value):
    return str(sp.cancel(value)).replace("**", "^")


def projection_audit(gamma: int, distinguished: int, expected):
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inv = sp.Symbol("winv")
    alpha, beta0 = bases(gamma)
    beta = shift(alpha, beta0, h)
    mixed, diagonal_a, diagonal_b = mixed_matrix(distinguished, alpha, beta)
    extension = sp.Matrix(z)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        inv * (diagonal_b * extension)[0] - 1,
    )
    eliminated = z + (inv,)
    variables = eliminated + h
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular, expected)) + ";",
            "E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "int same=((size(JE)==0)&&(size(EJ)==0));",
            '"AUDIT:"+string(same)+":"+string(size(J));',
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
        timeout=20,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    marker = [line for line in completed.stdout.splitlines() if line.startswith("AUDIT:")]
    assert len(marker) == 1 and marker[0].split(":")[1] == "1", completed.stdout
    return {
        "gamma": gamma,
        "distinguished": distinguished,
        "ideal": [singular(value) for value in expected],
        "bidirectional_equality": True,
    }


def projection_audits():
    h0, h1, h2, h3 = sp.symbols("h0:4")
    expected = {
        0: ((1,), (h3, h2, h0 * h1), (h3, h2, h0 * h1), (1,)),
        2: ((1,), (h3, h2, h0 + h1, h1**2), (h3, h2, h0 + h1, h1**2), (1,)),
    }
    return [
        projection_audit(gamma, distinguished, expected[gamma][distinguished])
        for gamma in (0, 2)
        for distinguished in range(4)
    ]


def kernel_audit(gamma: int, distinguished: int, axis: str):
    T, x, y = sp.symbols("T x y")
    alpha, beta0 = bases(gamma)
    if gamma == 2:
        h = (0, 0, 0, 0)
        expected_b = 4 * y
        expected_minor = -32 * x**2 * y
    elif axis == "h0_axis":
        h = (T, 0, 0, 0)
        expected_b = 4 * (T * x + y)
        expected_minor = -32 * x**2 * (T * x + y)
    else:
        h = (0, T, 0, 0)
        expected_b = 4 * (T * x + y)
        expected_minor = -32 * x**2 * (T * x + y)
    beta = shift(alpha, beta0, h)
    mixed, diagonal_a, diagonal_b = mixed_matrix(distinguished, alpha, beta)
    raw = sp.Matrix.hstack(*mixed.nullspace())
    assert mixed.rank() == 6 and raw.cols == 2
    restricted = sp.Matrix.vstack(diagonal_a * raw, diagonal_b * raw)
    sign = -1 if distinguished == 1 else 1
    target = sp.Matrix(((4 * sign, 0), (4 * T if gamma == 0 else 0, 4)))
    frame = (raw * restricted.inv() * target).applyfunc(sp.cancel)
    assert frame.rank() == 2 and zero(mixed * frame)
    extension = frame * sp.Matrix((x, y))
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    assert actual_a == 4 * sign * x and sp.factor(actual_b - expected_b) == 0
    marked = marked_extension(distinguished, extension, alpha, beta, mode=2)
    minor = sp.factor(marked[list(FIXED_ROWS), :].det())
    assert sp.factor(minor - expected_minor) == 0
    return {
        "gamma": gamma,
        "distinguished": distinguished,
        "axis": axis,
        "rank": 6,
        "kernel_dimension": 2,
        "frame": [[str(frame[row, column]) for column in range(2)] for row in range(8)],
        "A": str(actual_a),
        "B": str(actual_b),
        "minor_rows": list(FIXED_ROWS),
        "minor": str(minor),
    }


def kernel_audits():
    return [
        *(kernel_audit(0, d, axis) for d in (1, 2) for axis in ("h0_axis", "h1_axis")),
        *(kernel_audit(2, d, "origin") for d in (1, 2)),
    ]


def main() -> None:
    projections = projection_audits()
    kernels = kernel_audits()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "VERIFIED",
                "role": "verifier",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "scope": "separate exact reconstruction of both component-14 infinity endpoint H31 faces",
                "inputs": {THEOREM.name: sha256(THEOREM)},
                "method": "fresh saturated elimination and complete-kernel marked-minor reconstruction",
                "command": "uv run --with sympy python audit_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py",
                "outputs": {},
                "limitations": "verified endpoint H31 only; H22, other projective limits, gluing, and the global conjecture remain open",
                "saturated_projections": projections,
                "kernel_audits": kernels,
                "imports_primary_verifier": False,
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
