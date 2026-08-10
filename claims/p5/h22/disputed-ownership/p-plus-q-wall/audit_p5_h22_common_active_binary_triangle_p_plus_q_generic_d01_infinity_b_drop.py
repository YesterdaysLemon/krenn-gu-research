#!/usr/bin/env python3
"""Independent verifier for only the generic B_drop D01-infinity claim."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
CLAIM = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_GENERIC_D01_INFINITY_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_obstruction.py"
REPORT = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_GENERIC_D01_INFINITY_B_DROP_AUDIT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
RANK_ROWS = (1, 2, 3, 4, 6, 9)
RANK_COLUMNS = (0, 1, 2, 3, 4, 5)
MINOR_ROWS = (0, 1, 4, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True,
        encoding="utf-8", capture_output=True, check=True,
    ).stdout.strip()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Subset-DP permanent, separate from both discovery code paths."""

    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    next_states.get(new_mask, sp.Integer(0))
                    + coefficient * entry
                )
        states = next_states
    return sp.expand(states[(1 << len(rows)) - 1])


def add(*vectors: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(entries)) for entries in zip(*vectors))


def scale(scalar: sp.Expr, vector: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(scalar * entry) for entry in vector)


def wedge(left, right):
    return tuple(
        sp.factor(left[i] * right[j] - left[j] * right[i])
        for i, j in itertools.combinations(range(4), 2)
    )


def b_drop_planes(a: sp.Expr, shifts: tuple[sp.Expr, ...]):
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, sp.Integer(1), -1, 0)
    em = (0, sp.Integer(1), 1, 0)
    cap_c = (0, 0, 0, sp.Integer(1))
    s0 = 2 * a + 1
    k0 = add(scale(s0, cap_c), scale(-a * (a + 1), ell))
    alpha = (k0, e, e, em)
    canonical_beta = (
        ell,
        add(scale(a + 1, ell), cap_c),
        add(scale(a, ell), cap_c),
        e,
    )
    beta = tuple(
        add(canonical_beta[mode], scale(shifts[mode], alpha[mode]))
        for mode in range(4)
    )
    return alpha, canonical_beta, beta


def d01_infinity(row, extension):
    return (row[0], row[2], row[3], extension)


def reconstruct(sheet: str, a: sp.Expr, t: sp.Expr) -> dict[str, object]:
    shifts = (0, 0, t, 0) if sheet == "S1" else (0, t, 0, 0)
    alpha, canonical_beta, beta = b_drop_planes(a, shifts)
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        d01_infinity(alpha[mode], extensions[mode]) for mode in range(4)
    )
    beta_rows = tuple(
        d01_infinity(beta[mode], extensions[4 + mode]) for mode in range(4)
    )
    coefficients = {
        word: permanent(tuple(
            beta_rows[mode] if word[mode] else alpha_rows[mode]
            for mode in range(4)
        ))
        for word in WORDS
    }
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], extension) for extension in extensions]
        for word in MIXED_WORDS
    ])
    return {
        "sheet": sheet,
        "shifts": shifts,
        "alpha": alpha,
        "canonical_beta": canonical_beta,
        "beta": beta,
        "extensions": extensions,
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "mixed": mixed,
        "diagonal_a": coefficients[WORDS[0]],
        "diagonal_b": coefficients[WORDS[-1]],
    }


def marked_mode_three(model: dict[str, object]) -> sp.Matrix:
    alpha_rows = model["alpha_rows"]
    beta_rows = model["beta_rows"]
    assert isinstance(alpha_rows, tuple) and isinstance(beta_rows, tuple)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_rows[mode] if bits[mode] else alpha_rows[mode]
            for mode in range(3)
        )
        rows.append(tuple(
            permanent(tuple(
                tuple(row[index] for index in range(4) if index != column)
                for row in selected
            ))
            for column in range(4)
        ))
    return sp.Matrix(rows)


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def assert_zero(values) -> None:
    assert all(sp.factor(value) == 0 for value in values), values


def plane_and_purity_audit() -> dict[str, object]:
    a = sp.Symbol("a")
    shifts = sp.symbols("h0:4")
    alpha, canonical_beta, beta = b_drop_planes(a, shifts)
    assert all(
        wedge(alpha[mode], canonical_beta[mode]) == wedge(alpha[mode], beta[mode])
        for mode in range(4)
    )
    coefficients = {
        word: sp.factor(permanent(tuple(
            beta[mode] if word[mode] else alpha[mode]
            for mode in range(4)
        )))
        for word in WORDS
    }
    assert_equal(coefficients[(1, 1, 1, 1)], -2 * (2 * a + 1))
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word != (1, 1, 1, 1)
    )
    return {
        "alpha": [[str(value) for value in row] for row in alpha],
        "canonical_beta": [[str(value) for value in row] for row in canonical_beta],
        "marking_preserves_all_four_pluecker_tuples": True,
        "sole_pure_coefficient": "-2*(2*a+1)",
    }


def claimed_frame(sheet: str, a: sp.Expr, t: sp.Expr) -> sp.Matrix:
    vector0 = sp.Matrix(
        (-a - 1, 0, 0, 1 / a, 1 / a, (a + 1) / a, 1, 0)
    )
    if sheet == "S1":
        vector1 = sp.Matrix((
            0, -1, -1,
            -t * (2 * a + 1) / a**2,
            -t * (2 * a + 1) / a**2,
            -t * (a + 1) ** 2 / a**2,
            0, 1,
        ))
    else:
        vector1 = sp.Matrix((
            -a**2 * t / (a + 1), -1, -1,
            -t / (a + 1), -t / (a + 1),
            a * t / (a + 1), 0, 1,
        ))
    return sp.Matrix.hstack(vector0, vector1)


def sheet_audit(sheet: str) -> dict[str, object]:
    started = time.perf_counter()
    a, t, cap_x, cap_y = sp.symbols("a t X Y")
    model = reconstruct(sheet, a, t)
    mixed = model["mixed"]
    extensions = model["extensions"]
    diagonal_a = model["diagonal_a"]
    diagonal_b = model["diagonal_b"]
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(extensions, tuple)
    assert isinstance(diagonal_a, sp.Expr) and isinstance(diagonal_b, sp.Expr)

    frame = claimed_frame(sheet, a, t)
    assert frame.rank() == 2
    assert_zero(mixed * frame)
    witness = sp.factor(mixed.extract(RANK_ROWS, RANK_COLUMNS).det())
    assert_equal(witness, 2 * a**4 * (a + 1) ** 3 * (2 * a + 1))
    # Six independent rows plus two independent kernel vectors establish
    # exact rank six and completeness without trusting a solver rank label.
    nullspace = mixed.nullspace()
    assert len(nullspace) == 2
    assert sp.Matrix.hstack(frame, *nullspace).rank() == 2

    vector = frame * sp.Matrix((cap_x, cap_y))
    substitution = dict(zip(extensions, vector))
    first = sp.factor(diagonal_a.subs(substitution))
    second = sp.factor(diagonal_b.subs(substitution))
    assert_equal(first, -2 * cap_y * (2 * a + 1))
    if sheet == "S1":
        expected_second = (
            2 * (2 * a + 1) * (-cap_x * a + cap_y * t * (a + 1)) / a**2
        )
        expected_determinant = (
            8 * cap_y**2 * (2 * a + 1) ** 2
            * (-cap_x * a + cap_y * t * (a + 1))
        )
    else:
        expected_second = -2 * cap_x * (2 * a + 1) / a
        expected_determinant = -8 * cap_x * cap_y**2 * a * (2 * a + 1) ** 2
    assert_equal(second, expected_second)

    marked = marked_mode_three(model).subs(substitution)
    determinant = sp.factor(marked.extract(MINOR_ROWS, range(4)).det())
    assert_equal(determinant, expected_determinant)
    ratio = sp.factor(sp.cancel(determinant / (first * second)))
    assert_equal(ratio, -2 * cap_y * a**2)

    projective_scale = sp.Symbol("c", nonzero=True)
    scaled_substitution = {
        extension: projective_scale * value
        for extension, value in zip(extensions, vector)
    }
    scaled_first = sp.factor(diagonal_a.subs(scaled_substitution))
    scaled_second = sp.factor(diagonal_b.subs(scaled_substitution))
    scaled_minor = sp.factor(
        marked_mode_three(model).subs(scaled_substitution)
        .extract(MINOR_ROWS, range(4)).det()
    )
    assert_equal(scaled_first, projective_scale * first)
    assert_equal(scaled_second, projective_scale * second)
    assert_equal(scaled_minor, projective_scale**3 * determinant)
    scaled_ratio = sp.factor(sp.cancel(scaled_minor / (scaled_first * scaled_second)))
    assert_equal(scaled_ratio, projective_scale * ratio)

    return {
        "sheet": sheet,
        "marking": [str(value) for value in model["shifts"]],
        "kernel_basis": [
            [str(sp.factor(value)) for value in frame.col(column)]
            for column in range(2)
        ],
        "mixed_rank": 6,
        "kernel_dimension": 2,
        "rank_witness_rows": list(RANK_ROWS),
        "rank_witness_columns": list(RANK_COLUMNS),
        "rank_witness": str(witness),
        "explicit_kernel_equals_symbolic_nullspace": True,
        "all_alpha_diagonal": str(first),
        "all_beta_diagonal": str(second),
        "genuineness_forces_Y_nonzero": True,
        "marked_mode": 3,
        "minor_rows": list(MINOR_ROWS),
        "fixed_minor": str(determinant),
        "minor_over_diagonal_product": str(ratio),
        "projective_scaling": {
            "diagonals": "c",
            "minor": "c^3",
            "ratio": "c",
        },
        "every_genuine_extension_has_rank_four": True,
        "seconds": round(time.perf_counter() - started, 3),
    }


def intersection_audit() -> dict[str, object]:
    a, t = sp.symbols("a t")
    first = reconstruct("S1", a, t)
    second = reconstruct("S2", a, t)
    first_frame = claimed_frame("S1", a, t)
    second_frame = claimed_frame("S2", a, t)
    assert first["shifts"] == (0, 0, t, 0)
    assert second["shifts"] == (0, t, 0, 0)
    assert first["mixed"].subs(t, 0) == second["mixed"].subs(t, 0)
    assert first_frame.subs(t, 0) == second_frame.subs(t, 0)
    intersection_mixed = first["mixed"].subs(t, 0)
    intersection_frame = first_frame.subs(t, 0)
    assert_zero(intersection_mixed * intersection_frame)
    assert intersection_frame.rank() == 2
    return {
        "intersection_marking": [0, 0, 0, 0],
        "S1_and_S2_mixed_matrices_equal_at_t0": True,
        "S1_and_S2_kernel_frames_equal_at_t0": True,
        "intersection_kernel_dimension": 2,
    }


def main() -> None:
    started = time.perf_counter()
    claim_hash_before = sha256(CLAIM)
    primary_hash_before = sha256(PRIMARY)
    geometry = plane_and_purity_audit()
    sheets = [sheet_audit("S1"), sheet_audit("S2")]
    intersection = intersection_audit()
    # Fail closed if a concurrent edit changed either audited input.
    assert sha256(CLAIM) == claim_hash_before
    assert sha256(PRIMARY) == primary_hash_before
    source = Path(__file__).resolve()
    report = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": "only generic B_drop S1/S2 D01-infinity obstruction",
        "inputs": {
            CLAIM.name: claim_hash_before,
            PRIMARY.name: primary_hash_before,
        },
        "method": (
            "no-import reconstruction of B_drop planes, subset-DP permanents, "
            "D01-infinity contractions, all 14 mixed rows, complete kernels, "
            "rank witness, diagonals, fixed marked minor, and scaling"
        ),
        "command": (
            'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_b_drop.py'
        ),
        "outputs": {
            REPORT.name: sha256(REPORT),
            source.name: sha256(source),
        },
        "limitations": (
            "VERIFIED only for generic B_drop D01-infinity S1/S2 over "
            "C(a,t) on a(a+1)(2a+1)!=0; no B_full, finite-D23, a=0,-1, "
            "half-centre, non-diagonal, arbitrary-order, or global claim"
        ),
        "verdict": "VERIFIED",
        "plane_and_purity": geometry,
        "sheet_certificates": sheets,
        "t_zero_intersection": intersection,
        "primary_or_partial_helper_imported": False,
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "claim_inputs_unchanged_during_audit": True,
        "global_Krenn_Gu_conjecture_resolved": False,
        "runtime_seconds": round(time.perf_counter() - started, 3),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
