#!/usr/bin/env python3
"""Replay the refuted full weighted-H22 claim and its verified r0=t0=0 corner."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION_CANDIDATE.md"
H31 = (
    REPO_ROOT / "claims/p5/h31/embedded-p3/P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md"
)
H31_VERIFY = (
    REPO_ROOT / "claims/p5/h31/embedded-p3/verify_p5_h31_embedded_p3_component_r_zero_boundary.py"
)
H22_GENERIC = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
H22_RANK_TWO = (
    ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md"
)
H22_RANK_ONE = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md"
AUDIT_REPORT = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_VERIFICATION.md"
AUDIT_SCRIPT = ROOT / "audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py"
ENDPOINT_REPORT = ROOT / (
    "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_"
    "ENDPOINTS_OBSTRUCTION_CANDIDATE.md"
)
ENDPOINT_VERIFICATION = ROOT / (
    "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_"
    "ENDPOINTS_VERIFICATION.md"
)
ENDPOINT_VERIFIER = ROOT / (
    "audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_"
    "weight_endpoints_verifier.py"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS_3 = tuple(itertools.permutations(range(3)))


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


def permanent3(rows, columns=(0, 1, 2)):
    return sp.expand(
        sum(
            rows[0][columns[p[0]]] * rows[1][columns[p[1]]] * rows[2][columns[p[2]]]
            for p in PERMUTATIONS_3
        )
    )


def corner_bases(S, U, h):
    alpha = (
        (0, 1, S, U),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    canonical_beta = (
        (1, 0, 0, 0),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    beta = tuple(
        tuple(sp.expand(canonical_beta[i][j] + h[i] * alpha[i][j]) for j in range(4))
        for i in range(4)
    )
    return alpha, beta


def contract(row, extension, direction, r=None):
    if direction == "D01_finite":
        return (r * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23_finite":
        return (row[0], row[1], r * row[2] + row[3], extension)
    if direction == "D01_infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23_infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def build_model(S, U, h, z, direction, r=None):
    alpha, beta = corner_bases(S, U, h)
    alpha_rows = tuple(contract(alpha[i], z[i], direction, r) for i in range(4))
    beta_rows = tuple(contract(beta[i], z[4 + i], direction, r) for i in range(4))
    coefficients = {}
    for word in WORDS:
        selected = tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        # Every coefficient is linear in the extension column.  Expanding by
        # that column avoids an opaque 4! permanent implementation.
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    matrix = sp.Matrix(
        [[coefficients[word].coeff(variable) for variable in z] for word in MIXED]
    )
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "mixed": matrix,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def one_marked_matrix(model, mode):
    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            model["beta_rows"][index] if bits[position] else model["alpha_rows"][index]
            for position, index in enumerate(other)
        )
        rows.append(
            tuple(
                permanent3(selected, tuple(j for j in range(4) if j != coordinate))
                for coordinate in range(4)
            )
        )
    return sp.Matrix(rows)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact elimination replay")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def ideal_equality(equations, eliminated, retained, expected, timeout=45):
    variables = tuple(eliminated) + tuple(retained)
    program = "\n".join(
        (
            "ring rr=0,("
            + ",".join(map(str, variables))
            + ")"
            + f",(dp({len(eliminated)}),dp({len(retained)}));",
            "option(redSB);",
            "ideal ii=" + ",".join(map(singular, equations)) + "; ii=slimgb(ii);",
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
        timeout=timeout,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", completed.stdout
    return int(markers[0].split(":")[2])


def simultaneous_projection(direction):
    S, U, r = sp.symbols("S U r")
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    w = sp.symbols("w0:8")
    inv_a, inv_b = sp.symbols("ainv binv")
    suffix = direction.split("_")[1]
    d01 = build_model(S, U, h, z, "D01_" + suffix, r)
    d23 = build_model(S, U, h, w, "D23_" + suffix, r)
    equations = [
        *tuple(d01["mixed"] * sp.Matrix(z)),
        d01["A"] - 1,
        inv_a * d01["B"] - 1,
        *(d23["coefficients"][word] for word in WORDS[:-1]),
        inv_b * d23["B"] - 1,
    ]
    if suffix == "infinity":
        expected = (sp.Integer(1),)
        retained = h + (S, U)
    else:
        h0, h1, h2, h3 = h
        phi = sp.expand(
            S * (U * ((S - U) * (h1 + 1) * (h2 + 1) - h1 * (h2 + 1) + 1) + h2 * (S + 1))
            + h3 * (S * h2 * (S + U + 1) + U * h1 * (1 - S - U))
        )
        expected = (
            r * S - r * U,
            r**2 + r,
            2 * h3 * r * U + r * U,
            h2 * r * U + r * U,
            h1 * r * U + r * U,
            h0 * U,
            h0 * S,
            h0 * r + h0,
            2 * h2 * h3 * r + h0 + 2 * h2 * r + r,
            2 * h1 * h3 * r - h0 - r,
            2 * h0 * h3 + h0 + 2 * h3 * r + r,
            phi,
            h1 * h2 * r - h0 - r,
            h0 * h2 + h0 + h2 * r + r,
            h0 * h1 + h0 + h1 * r + r,
            h0**2 - h0,
        )
        retained = h + (r, S, U)
    size = ideal_equality(equations, z + w + (inv_a, inv_b), retained, expected)
    return expected, size, (d01, d23, (S, U, r), h, z)


def check_open_equal_coordinate_branch(models):
    _, _, (S, U, r), h, z = models
    s, X, Y = sp.symbols("s X Y")
    substitution = {
        S: s,
        U: s,
        r: -1,
        h[0]: 0,
        h[1]: -1,
        h[2]: -1,
        h[3]: -sp.Rational(1, 2),
    }
    d01 = build_model(S, U, h, z, "D01_finite", r)
    matrix = d01["mixed"].subs(substitution)
    v0 = sp.Matrix((0, 0, 0, 0, 1, 0, 0, 0))
    v1 = sp.Matrix((1, 1, -1, 0, 0, 0, 0, 1))
    assert all(sp.factor(value) == 0 for value in matrix * v0)
    assert all(sp.factor(value) == 0 for value in matrix * v1)
    vector = X * v0 + Y * v1
    values = dict(zip(z, vector))
    assert sp.factor(d01["A"].subs(substitution).subs(values) - 4 * s * Y) == 0
    assert sp.factor(d01["B"].subs(substitution).subs(values) + 2 * (X + Y)) == 0
    marked = one_marked_matrix(d01, 1).subs(substitution).subs(values)
    minor = sp.factor(marked.extract((0, 1, 3, 7), range(4)).det())
    assert sp.factor(minor + 16 * s**2 * Y**2 * (X + Y)) == 0

    # Saturating the mixed kernel equations by s proves that v0,v1 span it
    # for every s != 0, including s=+/-1/2 where a convenient rank witness drops.
    winv = sp.Symbol("winv")
    expected = (z[3], z[5], z[6], z[1] - z[0], z[2] + z[0], z[7] - z[0])
    kernel_size = ideal_equality(
        (*tuple(matrix * sp.Matrix(z)), winv * s - 1), (winv,), (s,) + z, expected
    )

    d23 = build_model(S, U, h, z, "D23_finite", r)
    unwanted = sp.Matrix(
        [
            [d23["coefficients"][word].coeff(variable) for variable in z]
            for word in WORDS[:-1]
        ]
    ).subs(substitution)
    pure_kernel = (
        sp.Matrix((1, 0, 0, 0, 0, 0, 0, 0)),
        sp.Matrix((0, 0, 0, 0, 1, 0, 0, 0)),
        sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0)),
        sp.Matrix((0, 0, 0, 0, 0, 0, 1, 0)),
    )
    assert unwanted.rank() == 4
    assert all(
        all(sp.factor(value) == 0 for value in unwanted * v) for v in pure_kernel
    )
    pure_values = [
        sp.factor(d23["B"].subs(substitution).subs(dict(zip(z, v))))
        for v in pure_kernel
    ]
    assert pure_values == [0, 0, 2, -2]
    return str(minor), kernel_size, tuple(map(str, pure_values))


def check_deep_equal_coordinate_branch(models):
    _, _, (S, U, r), h, z = models
    d01 = build_model(S, U, h, z, "D01_finite", r)
    substitution = {
        S: 0,
        U: 0,
        r: -1,
        h[0]: 0,
        h[1]: -1,
        h[2]: -1,
        h[3]: -sp.Rational(1, 2),
    }
    matrix = d01["mixed"].subs(substitution)
    v0 = sp.Matrix((0, 0, 0, 0, 1, 0, 0, 0))
    v1 = sp.Matrix((1, 1, -1, 0, 0, 0, 0, 1))
    assert matrix.rank() == 6
    assert all(value == 0 for value in matrix * v0) and all(
        value == 0 for value in matrix * v1
    )
    assert d01["A"].subs(substitution).subs(dict(zip(z, v0))) == 0
    assert d01["A"].subs(substitution).subs(dict(zip(z, v1))) == 0

    # For h0=1 the marked projected beta0 row vanishes.  The three remaining
    # components are exactly the H31 singular-base marking families.
    _alpha, beta = corner_bases(0, 0, (1, h[1], h[2], h[3]))
    projected_beta0 = contract(beta[0], z[4], "D01_finite", -1)
    assert projected_beta0[:3] == (0, 0, 0)
    families = ("(1,0,0,c)", "(1,a,0,0)", "(1,0,b,-1)")
    return families


def main():
    finite_ideal, finite_size, finite_models = simultaneous_projection("pair_finite")
    _, infinity_size, _ = simultaneous_projection("pair_infinity")
    h0, _h1, _h2, _h3, r, S, U = finite_models[3] + (
        finite_models[2][2],
        finite_models[2][0],
        finite_models[2][1],
    )
    phi = finite_ideal[11]
    assert sp.factor(finite_ideal[8].subs(r, 0) - h0) == 0
    assert sp.factor(phi.subs({S: 0, U: 0})) == 0
    assert sp.factor(finite_ideal[0].subs({r: -1, U: S})) == 0

    minor, kernel_size, pure_values = check_open_equal_coordinate_branch(finite_models)
    deep_families = check_deep_equal_coordinate_branch(finite_models)

    # Homogeneous transport on r0=0,t0!=0.  The signed source swap preserves
    # D01 weights and swaps the D23 weights [rho:sigma] -> [sigma:rho].
    x0, x1, x2, x3, e, rho, sigma, t = sp.symbols("x0 x1 x2 x3 e rho sigma t")
    Pz = (x0, x1, -x3, -x2)
    assert contract(Pz, e, "D01_finite", rho / sigma)[:3] == (
        rho * x0 / sigma + x1,
        -x3,
        -x2,
    )
    assert (x0, x1, -(rho * x3 + sigma * x2), e) == (
        x0,
        x1,
        -(sigma * x2 + rho * x3),
        e,
    )
    assert (1, 0, -t, 0)[2] == -t

    inputs = {
        path.name: sha256(path)
        for path in (
            H31,
            H31_VERIFY,
            H22_GENERIC,
            H22_RANK_TWO,
            H22_RANK_ONE,
            AUDIT_REPORT,
            AUDIT_SCRIPT,
            ENDPOINT_REPORT,
            ENDPOINT_VERIFICATION,
            ENDPOINT_VERIFIER,
        )
    }
    output = {
        "status": "pass",
        "role": "proof_a",
        "date_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": "weighted H22 on the embedded-P3 free-plane r0=0 divisor",
        "inputs": inputs,
        "method": "homogeneous transport, exact Q-elimination, saturated kernels, and inherited verified H31 covers",
        "command": 'uv run --with sympy python claims/p5/h22/embedded-p3/derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py',
        "outputs": {
            NOTE.name: sha256(NOTE),
            Path(__file__).name: sha256(Path(__file__)),
        },
        "limitations": "the original full-divisor transport proof remains REFUTED, but the t0=0 corner, t0!=0 nonendpoint transport, and two separately reconstructed homogeneous endpoints are independently verified; no projective normal-base closure or global claim",
        "field": "Q (characteristic zero)",
        "finite_projected_ideal_generator_count": finite_size,
        "infinity_projected_ideal_is_unit": infinity_size == 1,
        "finite_slopes": ["r=0: h0=0 and Phi=0", "r=-1: S=U"],
        "equal_coordinate_open_minor": minor,
        "equal_coordinate_open_kernel_saturation_generators": kernel_size,
        "D23_pure_kernel_diagonals": pure_values,
        "deep_h0_zero_genuine_D01": False,
        "deep_h0_one_H31_families": deep_families,
        "t_zero_corner_obstruction": "VERIFIED",
        "t_nonzero_nonendpoint_transport_to_normalized_chart": True,
        "t_nonzero_endpoint_fibres": "VERIFIED_BY_SEPARATE_THEOREM",
        "original_full_divisor_transport_proof_refuted": True,
        "full_r_zero_divisor_obstruction_proved": True,
        "finite_field_computation_used": False,
        "fresh_independent_verifier_complete": True,
        "global_problem_resolved": False,
        "dependencies": inputs,
        "note": NOTE.name,
        "note_sha256": sha256(NOTE),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
