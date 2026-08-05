#!/usr/bin/env python3
"""Independent verifier for the generic B_full infinity--finite H22 pair.

This file imports neither discovery script nor either partial-checkpoint helper.
It reconstructs the planes, tensor contractions, incidence eliminations, complete
kernels, diagonals, and marked minors directly over characteristic zero.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
REPORT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_B_FULL_INFINITY_FINITE_PAIR_VERIFICATION.md"
)
GENERIC_NOTE = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_GENERIC_D01_INFINITY_OBSTRUCTION.md"
)
PAIR_NOTE = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_B_FULL_INFINITY_FINITE_PAIR_OBSTRUCTION.md"
)
P4_BOUNDARY = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
H22_PARTIAL = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PERMUTATIONS_3 = tuple(itertools.permutations(range(3)))
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


def add(*vectors):
    return tuple(sp.expand(sum(values)) for values in zip(*vectors))


def scale(coefficient, vector):
    return tuple(sp.expand(coefficient * value) for value in vector)


def permanent3(rows, columns=(0, 1, 2)):
    return sp.expand(
        sum(
            rows[0][columns[permutation[0]]]
            * rows[1][columns[permutation[1]]]
            * rows[2][columns[permutation[2]]]
            for permutation in PERMUTATIONS_3
        )
    )


def b_full_bases(a, lam, marking):
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    cap_c = (0, 0, 0, 1)
    s0 = 2 * a + 1
    k0 = add(scale(s0, cap_c), scale(-a * (a + 1), ell))
    alpha = (k0, e, e, em)
    beta0 = (
        add(e, scale(lam, ell)),
        add(scale(a + 1, ell), cap_c),
        add(scale(a, ell), cap_c),
        e,
    )
    beta = tuple(
        add(beta0[index], scale(marking[index], alpha[index])) for index in range(4)
    )
    return alpha, beta


def contract(row, extension, direction, slope):
    if direction == "D01_infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23_finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    raise ValueError(direction)


def build_model(direction, a, lam, slope, marking):
    alpha, beta = b_full_bases(a, lam, marking)
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        contract(alpha[index], extensions[index], direction, slope)
        for index in range(4)
    )
    beta_rows = tuple(
        contract(beta[index], extensions[index + 4], direction, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
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
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def marked_matrix(model, marked_mode=3):
    other_modes = tuple(index for index in range(4) if index != marked_mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            model["beta_rows"][mode] if bits[position] else model["alpha_rows"][mode]
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


def assert_zero(expressions, label):
    assert all(sp.factor(expression) == 0 for expression in expressions), label


def assert_equal(actual, expected, label):
    assert sp.factor(actual - expected) == 0, (label, sp.factor(actual), expected)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def projection_certificate(direction, expected):
    a, lam, r = sp.symbols("a lambda r")
    markings = sp.symbols("h0:4")
    model = build_model(direction, a, lam, r, markings)
    winv = sp.Symbol("winv")
    equations = [
        *tuple(model["mixed"] * sp.Matrix(model["extensions"])),
        model["A"] - 1,
        winv * model["B"] - 1,
    ]
    eliminated = model["extensions"] + (winv,)
    if direction == "D23_finite":
        eliminated += (r,)
    variables = eliminated + markings
    program = "\n".join(
        (
            "ring rr=(0,a,lambda),("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp(4));",
            "option(redSB);",
            "ideal ii=" + ",".join(map(singular, equations)) + ";",
            "ii=slimgb(ii);",
            "ideal jj=std(eliminate(ii," + "*".join(map(str, eliminated)) + "));",
            "ideal ee=" + ",".join(map(singular, expected)) + "; ee=std(ee);",
            "ideal lr=simplify(reduce(jj,ee),2);",
            "ideal rl=simplify(reduce(ee,jj),2);",
            '"RESULT:"+string((size(lr)==0)&&(size(rl)==0))+":"+string(size(jj));',
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
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        direction,
        completed.stdout,
    )
    return {
        "direction": direction,
        "projected_ideal": [singular(value) for value in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
        "coefficient_field": "Q(a,lambda)",
    }


def marking_certificate():
    a = sp.Symbol("a", nonzero=True)
    h0, h1, h2, h3 = sp.symbols("h0:4")
    d01 = (h3, a * h1 + (a + 1) * h2, h0, h2**2)
    d23 = (h3, h0, h1 * h2)
    projections = (
        projection_certificate("D01_infinity", d01),
        projection_certificate("D23_finite", d23),
    )
    assert_equal((a * h1 + (a + 1) * h2).subs(h2, 0), a * h1, "linear marking")
    return {
        "projections": projections,
        "common_geometric_marking": [0, 0, 0, 0],
        "reason": "h2^2=0 forces h2=0, then a*h1=0 forces h1=0, while h0=h3=0",
        "nilpotent_direction_counted_as_geometric_point": False,
    }


def complete_frame(model, frame, expected_witness, label):
    mixed = model["mixed"]
    assert_zero(mixed * frame, f"{label}: frame")
    assert frame.rank() == frame.cols, label
    witness = sp.factor(mixed.extract(RANK_ROWS, RANK_COLUMNS).det())
    assert_equal(witness, expected_witness, f"{label}: witness")
    assert len(mixed.nullspace()) == frame.cols, label
    return {
        "mixed_rank": 8 - frame.cols,
        "kernel_dimension": frame.cols,
        "rank_witness_rows": list(RANK_ROWS),
        "rank_witness_columns": list(RANK_COLUMNS),
        "rank_witness": str(witness),
        "explicit_frame_annihilated": True,
        "frame_complete": True,
    }


def d01_infinity_certificate():
    a, lam, cap_x, cap_y = sp.symbols("a lambda X Y")
    model = build_model("D01_infinity", a, lam, 0, (0, 0, 0, 0))
    vector0 = sp.Matrix((-a - 1, 0, 0, 1 / a, lam / a, (a + 1) / a, 1, 0))
    vector1 = sp.Matrix((0, -1, -1, 0, 1, 0, 0, 1))
    frame = sp.Matrix.hstack(vector0, vector1)
    witness = 2 * a**4 * (a + 1) ** 3 * (2 * a + 1)
    completeness = complete_frame(model, frame, witness, "D01 infinity")
    vector = cap_x * vector0 + cap_y * vector1
    substitution = dict(zip(model["extensions"], vector))
    diagonal_a = sp.factor(model["A"].subs(substitution))
    diagonal_b = sp.factor(model["B"].subs(substitution))
    expected_a = -2 * cap_y * (2 * a + 1)
    expected_b = -2 * (2 * a + 1) * (cap_x * lam + a * cap_y) / a
    assert_equal(diagonal_a, expected_a, "D01 A")
    assert_equal(diagonal_b, expected_b, "D01 B")
    determinant = sp.factor(
        marked_matrix(model).subs(substitution).extract(MINOR_ROWS, range(4)).det()
    )
    expected_determinant = (
        -8 * cap_y**2 * a * lam * (2 * a + 1) ** 2 * (cap_x * lam + a * cap_y)
    )
    assert_equal(determinant, expected_determinant, "D01 marked minor")
    ratio = sp.factor(sp.cancel(determinant / (diagonal_a * diagonal_b)))
    assert_equal(ratio, -2 * cap_y * a**2 * lam, "D01 ratio")
    projective_scale = sp.Symbol("c", nonzero=True)
    scaled = dict(zip(model["extensions"], projective_scale * vector))
    scaled_a = sp.factor(model["A"].subs(scaled))
    scaled_b = sp.factor(model["B"].subs(scaled))
    scaled_minor = sp.factor(
        marked_matrix(model).subs(scaled).extract(MINOR_ROWS, range(4)).det()
    )
    assert_equal(scaled_a, projective_scale * diagonal_a, "scaled A")
    assert_equal(scaled_b, projective_scale * diagonal_b, "scaled B")
    assert_equal(scaled_minor, projective_scale**3 * determinant, "scaled minor")
    return {
        **completeness,
        "kernel_basis": [
            [str(sp.factor(value)) for value in vector0],
            [str(sp.factor(value)) for value in vector1],
        ],
        "A": str(diagonal_a),
        "B": str(diagonal_b),
        "marked_mode": 3,
        "minor_rows": list(MINOR_ROWS),
        "minor": str(determinant),
        "minor_over_A_B": str(ratio),
        "genuine_forces_minor_nonzero": True,
        "projective_scaling": {"A": "degree 1", "B": "degree 1", "minor": "degree 3"},
    }


def saturated_d23_kernel(model):
    r = sp.Symbol("r")
    rinv = sp.Symbol("rinv")
    z = model["extensions"]
    equations = tuple(model["mixed"] * sp.Matrix(z)) + (rinv * r - 1,)
    expected = (z[0], z[3], z[5], z[6], z[2] - z[1], z[4] + z[1], z[7] + z[1])
    variables = (rinv,) + z + (r,)
    program = "\n".join(
        (
            "ring rr=(0,a,lambda),("
            + ",".join(map(str, variables))
            + "),(dp(1),dp(9));",
            "option(redSB);",
            "ideal ii=" + ",".join(map(singular, equations)) + ";",
            "ii=slimgb(ii);",
            "ideal jj=std(eliminate(ii,rinv));",
            "ideal ee=" + ",".join(map(singular, expected)) + "; ee=std(ee);",
            "ideal lr=simplify(reduce(jj,ee),2);",
            "ideal rl=simplify(reduce(ee,jj),2);",
            '"RESULT:"+string((size(lr)==0)&&(size(rl)==0))+":"+string(size(jj));',
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
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", completed.stdout
    return {
        "saturation": "r != 0",
        "kernel_ideal": [singular(value) for value in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def finite_d23_certificate():
    a, lam, r, cap_c = sp.symbols("a lambda r C")
    model = build_model("D23_finite", a, lam, r, (0, 0, 0, 0))
    saturation = saturated_d23_kernel(model)
    line = sp.Matrix((0, -1, -1, 0, 1, 0, 0, 1))
    assert_zero(model["mixed"] * line, "D23 nonzero line")
    substitution = dict(zip(model["extensions"], cap_c * line))
    diagonal_a = sp.factor(model["A"].subs(substitution))
    diagonal_b = sp.factor(model["B"].subs(substitution))
    assert_equal(diagonal_a, -2 * cap_c * (2 * a + 1), "D23 nonzero A")
    assert_equal(
        diagonal_b,
        -2 * cap_c * (2 * a * (a + 1) * r - (2 * a + 1)),
        "D23 nonzero B",
    )
    beta_zero_slope = (2 * a + 1) / (2 * a * (a + 1))
    assert_equal(diagonal_b.subs(r, beta_zero_slope), 0, "D23 zero diagonal")

    zero_model = build_model("D23_finite", a, lam, 0, (0, 0, 0, 0))
    vector0 = sp.Matrix((-a - 1, 0, 0, -1 / a, lam / a, (a + 1) / a, 1, 0))
    vector1 = line
    frame = sp.Matrix.hstack(vector0, vector1)
    witness = 2 * a**4 * (a + 1) ** 3 * (2 * a + 1)
    completeness = complete_frame(zero_model, frame, witness, "D23 r=0")
    cap_u, cap_v = sp.symbols("U V")
    vector = cap_u * vector0 + cap_v * vector1
    zero_substitution = dict(zip(zero_model["extensions"], vector))
    zero_a = sp.factor(zero_model["A"].subs(zero_substitution))
    zero_b = sp.factor(zero_model["B"].subs(zero_substitution))
    assert_equal(zero_a, -2 * cap_v * (2 * a + 1), "D23 r=0 A")
    assert_equal(
        zero_b,
        2 * (2 * a + 1) * (cap_u * lam + a * cap_v) / a,
        "D23 r=0 B",
    )
    determinant = sp.factor(
        marked_matrix(zero_model)
        .subs(zero_substitution)
        .extract(MINOR_ROWS, range(4))
        .det()
    )
    expected_determinant = (
        8 * cap_v**2 * a * lam * (2 * a + 1) ** 2 * (cap_u * lam + a * cap_v)
    )
    assert_equal(determinant, expected_determinant, "D23 r=0 minor")
    ratio = sp.factor(sp.cancel(determinant / (zero_a * zero_b)))
    assert_equal(ratio, -2 * cap_v * a**2 * lam, "D23 r=0 ratio")
    return {
        "r_nonzero": {
            **saturation,
            "kernel_generator": [str(value) for value in line],
            "A": str(diagonal_a),
            "B": str(diagonal_b),
            "beta_zero_slope": str(beta_zero_slope),
            "beta_zero_slope_is_nongenuine": True,
        },
        "r_zero": {
            **completeness,
            "kernel_basis": [
                [str(sp.factor(value)) for value in vector0],
                [str(sp.factor(value)) for value in vector1],
            ],
            "A": str(zero_a),
            "B": str(zero_b),
            "marked_mode": 3,
            "minor_rows": list(MINOR_ROWS),
            "minor": str(determinant),
            "minor_over_A_B": str(ratio),
            "genuine_forces_minor_nonzero": True,
        },
        "finite_slopes_exhausted": True,
    }


def main():
    marking = marking_certificate()
    d01 = d01_infinity_certificate()
    d23 = finite_d23_certificate()
    script = Path(__file__).resolve()
    result = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": "generic B_full over Q(a,lambda), a(a+1)(2a+1)lambda != 0: D01 infinity obstruction and paired finite D23 exhaustion",
        "inputs": {
            P4_BOUNDARY.name: sha256(P4_BOUNDARY),
            H22_PARTIAL.name: sha256(H22_PARTIAL),
            GENERIC_NOTE.name: sha256(GENERIC_NOTE),
            PAIR_NOTE.name: sha256(PAIR_NOTE),
        },
        "method": "no-import reconstruction of planes and marked tensors; exact normalized projection elimination; complete kernels and fixed minors; exact r-saturation",
        "command": "uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_b_full_infinity_finite_pair_verifier.py",
        "outputs": {REPORT.name: sha256(REPORT), script.name: sha256(script)},
        "limitations": "VERIFIED only for the frozen generic B_full diagonal-DVR local framework; no a=0,-1,-1/2, B_drop, non-diagonal changes, arbitrary-order gluing, or global Krenn-Gu claim",
        "imports_discovery_or_partial_helpers": False,
        "common_marking": marking,
        "D01_infinity": d01,
        "finite_D23": d23,
        "generic_B_full_D01_infinity_subclaim": "VERIFIED",
        "generic_B_full_infinity_finite_pair_subclaim": "VERIFIED",
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
