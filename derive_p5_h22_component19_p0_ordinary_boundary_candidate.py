#!/usr/bin/env python3
"""Exact construction replay for the finite ordinary p=0 boundary of component 19."""

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
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_P0_ORDINARY_BOUNDARY_CANDIDATE.md"
CERTIFICATE = ROOT / "p5_h22_component19_p0_ordinary_boundary_certificate.json"
INPUTS = tuple(ROOT / name for name in (
    "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md",
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md",
    "NEXT_INSTANCE_HANDOFF_2026-07-31.md",
))

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
MIXED4 = WORDS4[1:-1]
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True,
        capture_output=True, check=True, timeout=15,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.expand(sum(row[i] for row in rows)) for i in range(len(rows[0])))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def permanent(rows):
    size = len(rows)
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(size))
        for permutation in itertools.permutations(range(size))
    ))


def assert_zero(value):
    if isinstance(value, sp.MatrixBase):
        assert all(sp.factor(entry) == 0 for entry in value)
    else:
        assert sp.factor(value) == 0


def p0_basis(q, phi):
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    planes = (
        (abar, add(bbar, scale(q, cap_b))),
        (cap_b, cap_a),
        (bbar, cap_a),
        (abar, add(cap_b, scale(phi, bbar))),
    )
    alpha = (abar, cap_b, bbar, abar)
    beta = (planes[0][1], cap_a, cap_a, planes[3][1])
    return planes, alpha, beta


def shifted_beta(alpha, beta, markings):
    return tuple(add(beta[i], scale(markings[i], alpha[i])) for i in range(4))


def tensor_coefficients(alpha, beta):
    return {
        word: permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        for word in WORDS4
    }


def squarefree_product(left, right):
    return sp.Matrix(tuple(
        sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS
    ))


def pair_matrix(left_plane, right_plane):
    return sp.Matrix.hstack(*(
        squarefree_product(left_plane[i], right_plane[j])
        for i in range(2) for j in range(2)
    ))


def pair_certificates(planes, q, phi):
    witnesses = {
        "01": ((1, 2, 5), (0, 2, 3), 4 * q),
        "02": ((1, 4, 5), (0, 2, 3), -4),
        "03": ((0, 1, 2, 5), (0, 1, 2, 3), -8 * (q - phi) * (phi * q - 1)),
        "12": ((0, 2, 3), (1, 2, 3), 4),
        "13": ((1, 4, 5), (0, 1, 3), -4),
        "23": ((1, 2, 5), (0, 1, 3), 4 * phi),
    }
    output = {}
    for i, j in PAIRS:
        label = f"{i}{j}"
        matrix = pair_matrix(planes[i], planes[j])
        rows, columns, expected = witnesses[label]
        determinant = sp.factor(matrix.extract(rows, columns).det())
        assert_zero(determinant - expected)
        if label != "03":
            assert all(
                sp.factor(matrix.extract(row_set, range(4)).det()) == 0
                for row_set in itertools.combinations(range(6), 4)
            )
        output[label] = {
            "generic_rank": 4 if label == "03" else 3,
            "rows": list(rows), "columns": list(columns),
            "determinant": str(determinant),
        }
    special03 = pair_matrix(planes[0], planes[3]).subs(q, 1 / phi)
    rows, columns = (0, 1, 5), (0, 1, 3)
    special_minor = sp.factor(special03.extract(rows, columns).det())
    assert_zero(special_minor - 4 * (phi - 1) * (phi + 1) ** 2 / phi)
    assert all(
        sp.factor(special03.extract(row_set, range(4)).det()) == 0
        for row_set in itertools.combinations(range(6), 4)
    )
    return output, {
        "divisor": "q*phi=1", "rank03": 3,
        "rows": list(rows), "columns": list(columns),
        "determinant": str(special_minor),
        "note": "nonzero on q*phi=1 inside q*phi*(q-phi)!=0",
    }


def project(row, extension, direction, slope):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    raise ValueError(direction)


def build_model(alpha, beta, extensions, direction, slope):
    projected_alpha = tuple(
        project(alpha[i], extensions[i], direction, slope) for i in range(4)
    )
    projected_beta = tuple(
        project(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )
    coefficients = {
        word: permanent(tuple(
            projected_beta[i] if word[i] else projected_alpha[i]
            for i in range(4)
        ))
        for word in WORDS4
    }
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], extension) for extension in extensions]
        for word in MIXED4
    ])
    return {
        "alpha": projected_alpha, "beta": projected_beta,
        "coefficients": coefficients, "mixed": mixed,
    }


def one_marked(model, mode):
    rows = []
    for word in WORDS3:
        selected = []
        bit = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(model["beta"][other] if word[bit] else model["alpha"][other])
                bit += 1
        rows.append([
            permanent(tuple(
                tuple(int(coordinate == column) for coordinate in range(4))
                if other == mode else selected[other]
                for other in range(4)
            ))
            for column in range(4)
        ])
    return sp.Matrix(rows)


def full_one_marked(alpha5, beta5, mode, contraction):
    basis = tuple(tuple(int(i == j) for j in range(5)) for i in range(5))
    rows = []
    for word in WORDS3:
        selected = []
        bit = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta5[other] if word[bit] else alpha5[other])
                bit += 1
        rows.append([
            permanent(tuple(
                basis[column] if other == mode else selected[other]
                for other in range(4)
            ) + (contraction,))
            for column in range(5)
        ])
    return sp.Matrix(rows)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def eliminate(label, equations, eliminated, retained, coefficient_ring, expected):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=" + coefficient_ring + ",(" + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + "; E=std(E);",
        "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
        '"CODEX_RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
        "quit;",
    ]
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), cwd=ROOT, text=True,
        capture_output=True, timeout=120, check=False,
    )
    markers = [line for line in completed.stdout.splitlines() if line.startswith("CODEX_RESULT:")]
    assert completed.returncode == 0 and not completed.stderr.strip()
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (label, completed.stdout)
    return {"label": label, "ideal": [str(sp.factor(value)) for value in expected]}


def incidence_certificates(alpha, unmarked_beta, q, phi):
    h = sp.symbols("h0:4")
    lam = sp.Symbol("lam")
    x = sp.symbols("x0:8")
    u, v = sp.symbols("u v")
    beta = shifted_beta(alpha, unmarked_beta, h)
    results = []
    expected = {
        "D01_binary": (sp.Integer(1),),
        "D23_binary": (h[3], h[0], h[1] * h[2]),
        "shared_A01": (sp.Integer(1),),
        "shared_A23": (lam - 1, h[3], h[1], h[0]),
    }
    for chart, slope in (("finite", lam), ("infinity", sp.Integer(0))):
        # At infinity the omitted coordinate is reconstructed directly.
        if chart == "infinity":
            def endpoint(row, extension, direction):
                return ((row[0], row[2], row[3], extension) if direction == "D01"
                        else (row[0], row[1], row[2], extension))
            def endpoint_model(direction):
                aa = tuple(endpoint(alpha[i], x[i], direction) for i in range(4))
                bb = tuple(endpoint(beta[i], x[4+i], direction) for i in range(4))
                coefficients = {word: permanent(tuple(bb[i] if word[i] else aa[i] for i in range(4))) for word in WORDS4}
                return {"coefficients": coefficients, "mixed": sp.Matrix([[sp.diff(coefficients[word], z) for z in x] for word in MIXED4])}
            d01, d23 = endpoint_model("D01"), endpoint_model("D23")
        else:
            d01 = build_model(alpha, beta, x, "D01", slope)
            d23 = build_model(alpha, beta, x, "D23", slope)
        common = tuple(d01["mixed"] * sp.Matrix(x)) + tuple(d23["mixed"] * sp.Matrix(x))
        systems = {
            "D01_binary": (*tuple(d01["mixed"] * sp.Matrix(x)), d01["coefficients"][WORDS4[0]] - 1, u * d01["coefficients"][WORDS4[-1]] - 1),
            "D23_binary": (*tuple(d23["mixed"] * sp.Matrix(x)), d23["coefficients"][WORDS4[0]] - 1, u * d23["coefficients"][WORDS4[-1]] - 1),
            "shared_A01": (*common, d01["coefficients"][WORDS4[0]] - 1, u * d01["coefficients"][WORDS4[-1]] - 1, v * d23["coefficients"][WORDS4[-1]] - 1),
            "shared_A23": (*common, d23["coefficients"][WORDS4[0]] - 1, u * d01["coefficients"][WORDS4[-1]] - 1, v * d23["coefficients"][WORDS4[-1]] - 1),
        }
        retained = h + ((lam,) if chart == "finite" else ())
        for name, equations in systems.items():
            eliminated = x + ((u, v) if name.startswith("shared") else (u,))
            wanted = expected[name] if chart == "finite" else (
                (h[3], h[0], h[1] * h[2]) if name == "D23_binary" else (sp.Integer(1),)
            )
            results.append(eliminate(
                f"{name}_{chart}_over_Q(q,phi)", equations, eliminated,
                retained, "(0,q,phi)", wanted,
            ))
    return results


def branch_certificate(alpha, beta0, q, phi):
    t, cap_c, cap_d, cap_e, cap_k = sp.symbols("t C D E K")
    x = sp.symbols("x0:8")
    beta = shifted_beta(alpha, beta0, (0, 0, t, 0))
    d01 = build_model(alpha, beta, x, "D01", sp.Integer(1))
    d23 = build_model(alpha, beta, x, "D23", sp.Integer(1))
    combined = d01["mixed"].col_join(d23["mixed"])
    rows, columns = (2, 9, 10, 12, 15), (0, 1, 2, 3, 6)
    rank_minor = sp.factor(combined.extract(rows, columns).det())
    assert_zero(rank_minor + 1024 * q * (q - phi) ** 2)
    cap_x = phi * cap_c + cap_e
    cap_y = cap_c + q * cap_e
    cap_r = (q - phi) * cap_d - t * cap_x
    extension = sp.Matrix((
        0, -cap_y / (q - phi), cap_x / (q - phi), 0,
        cap_c, cap_d, 0, cap_e,
    ))
    assert_zero(combined * extension)
    assert combined.rank() == 5
    diagonal = {}
    substitution = dict(zip(x, extension))
    for label, model in (("D01", d01), ("D23", d23)):
        diagonal[label] = tuple(sp.factor(model["coefficients"][word].subs(substitution)) for word in (WORDS4[0], WORDS4[-1]))
    expected_diagonal = {
        "D01": (0, 4 * cap_r),
        "D23": (-4 * cap_x / (q - phi), 4 * cap_y),
    }
    for label, actual_values in diagonal.items():
        for actual, expected in zip(actual_values, expected_diagonal[label]):
            assert_zero(actual - expected)

    projected = {}
    expected_minors = {
        ("D01", 0, (1, 3, 5, 7)): 64 * cap_e * (phi ** 2 - 1) * (2 * phi * cap_c + (phi * q + 1) * cap_e) * cap_r / (q - phi) ** 2,
        ("D01", 3, (4, 5, 6, 7)): -64 * cap_c * (q ** 2 - 1) * ((phi * q + 1) * cap_c + 2 * q * cap_e) * cap_r / (q - phi) ** 2,
        ("D23", 2, (0, 1, 2, 7)): 64 * cap_d * (cap_c + phi * cap_e) * cap_y / (q - phi),
        ("D23", 2, (0, 2, 3, 7)): 64 * cap_d ** 2 * cap_y,
        ("D23", 2, (0, 2, 4, 7)): -64 * cap_d * cap_y * (phi * cap_c + q ** 2 * cap_e) / (q - phi),
        ("D23", 2, (0, 2, 6, 7)): 64 * cap_d ** 2 * q * cap_y,
    }
    for label, model in (("D01", d01), ("D23", d23)):
        for mode in range(4):
            matrix = one_marked(model, mode).subs(substitution)
            nonzero = 0
            for row_set in itertools.combinations(range(8), 4):
                determinant = sp.factor(matrix.extract(row_set, range(4)).det())
                if determinant != 0:
                    nonzero += 1
                    assert (label, mode, row_set) in expected_minors
                    expected_minor = expected_minors[(label, mode, row_set)]
                    difference = sp.factor(determinant - expected_minor)
                    if difference != 0:
                        raise AssertionError(
                            (label, mode, row_set, determinant, expected_minor, difference)
                        )
            projected[f"{label}_mode{mode}"] = nonzero
    assert projected == {
        "D01_mode0": 1, "D01_mode1": 0, "D01_mode2": 0, "D01_mode3": 1,
        "D23_mode0": 0, "D23_mode1": 0, "D23_mode2": 4, "D23_mode3": 0,
    }

    # Full two-contraction compatibility.  These fixed minors remove all
    # projected survivors except the explicitly listed rank-safe families.
    alpha5 = tuple(tuple(alpha[i]) + (extension[i],) for i in range(4))
    beta5 = tuple(tuple(beta[i]) + (extension[4 + i],) for i in range(4))
    contraction01 = (1, 1, 0, 0, 0)
    contraction23 = (0, 0, 1, 1, 0)
    stacks = tuple(
        full_one_marked(alpha5, beta5, mode, contraction01).col_join(
            full_one_marked(alpha5, beta5, mode, contraction23)
        ) for mode in range(4)
    )

    def fixed(mode, row_set, values, expected):
        determinant = sp.factor(stacks[mode].subs(values).extract(row_set, range(5)).det())
        difference = sp.factor(determinant - expected)
        if difference != 0:
            raise AssertionError((mode, row_set, determinant, expected, difference))
        return str(determinant)

    stack_witnesses = {
        "qphi_minus_one_C_axis": fixed(3, (5, 6, 7, 8, 13),
            {cap_c: cap_k, cap_e: 0, cap_d: 0, q: -1 / phi},
            256 * cap_k ** 4 * t * phi ** 4 * (phi ** 2 - 1) / (phi ** 2 + 1) ** 3),
        "qphi_minus_one_E_axis": fixed(0, (3, 5, 7, 8, 11),
            {cap_c: 0, cap_e: cap_k, cap_d: 0, q: -1 / phi},
            256 * cap_k ** 4 * t * phi ** 4 * (phi ** 2 - 1) / (phi ** 2 + 1) ** 3),
        "phi_plus_one_L3": fixed(3, (0, 1, 3, 8, 14),
            {phi: 1, cap_c: -2 * q * cap_k, cap_e: (q + 1) * cap_k, cap_d: 0},
            -32 * cap_k ** 4 * t * (q - 1) * (q + 1) * (q + 2) / q ** 2),
        "phi_minus_one_L3": fixed(3, (0, 1, 3, 8, 14),
            {phi: -1, cap_c: -2 * q * cap_k, cap_e: (1 - q) * cap_k, cap_d: 0},
            32 * cap_k ** 4 * t * (q - 2) * (q - 1) * (q + 1) / q ** 2),
        "q_plus_one_L0": fixed(0, (0, 1, 3, 8, 14),
            {q: 1, cap_c: -(phi + 1) * cap_k, cap_e: 2 * phi * cap_k, cap_d: 0},
            32 * cap_k ** 4 * t * (phi - 1) * (phi + 1) * (2 * phi + 1) / phi),
        "q_minus_one_L0": fixed(0, (0, 1, 3, 8, 14),
            {q: -1, cap_c: -(1 - phi) * cap_k, cap_e: 2 * phi * cap_k, cap_d: 0},
            32 * cap_k ** 4 * t * (phi - 1) * (phi + 1) * (2 * phi - 1) / phi),
    }

    rank_safe_checks = {}
    families = {
        "phi=1_C_axis": {phi: 1, cap_c: 0, cap_e: cap_k, cap_d: 0},
        "phi=-1_C_axis": {phi: -1, cap_c: 0, cap_e: cap_k, cap_d: 0},
        "q=1_E_axis": {q: 1, cap_c: cap_k, cap_e: 0, cap_d: 0},
        "q=-1_E_axis": {q: -1, cap_c: cap_k, cap_e: 0, cap_d: 0},
        "q=-1_phi=1_full_line": {q: -1, phi: 1, cap_d: 0},
        "q=1_phi=-1_full_line": {q: 1, phi: -1, cap_d: 0},
    }
    for label, values in families.items():
        ranks = [matrix.subs(values).rank() for matrix in stacks]
        assert ranks == [4, 4, 4, 4]
        rank_safe_checks[label] = ranks

    return {
        "shared_mixed_rank": 5,
        "rank_witness": {"rows": list(rows), "columns": list(columns), "determinant": str(rank_minor)},
        "kernel_parameterization": [str(sp.factor(value)) for value in extension],
        "diagonals": {key: [str(value) for value in values] for key, values in diagonal.items()},
        "genuine_condition": "(phi*C+E)*(C+q*E)*((q-phi)*D-t*(phi*C+E))!=0",
        "projected_nonzero_four_minor_counts": projected,
        "projected_rank_safe_equations_after_D_zero": [
            "E*(phi^2-1)*(2*phi*C+(phi*q+1)*E)=0",
            "C*(q^2-1)*((phi*q+1)*C+2*q*E)=0",
        ],
        "stack_witnesses": stack_witnesses,
        "rank_safe_stack_ranks": rank_safe_checks,
    }


def main():
    q, phi = sp.symbols("q phi")
    planes, alpha, beta = p0_basis(q, phi)
    markings = sp.symbols("h0:4")
    coefficients = tensor_coefficients(alpha, shifted_beta(alpha, beta, markings))
    support = {"".join(map(str, word)): str(sp.factor(value)) for word, value in coefficients.items() if value != 0}
    assert set(support) == {"1111"}
    assert sp.expand(sp.sympify(support["1111"]) - 4 * (q - phi)) == 0
    pair_data, qphi_one = pair_certificates(planes, q, phi)
    incidence = incidence_certificates(alpha, beta, q, phi)
    branch = branch_certificate(alpha, beta, q, phi)
    result = {
        "status": "refuted", "role": "construction", "claim_label": "REFUTED",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "scope": "component 19 finite ordinary p=0 boundary on q*phi*(q-phi)!=0",
        "inputs": {path.name: sha256(path) for path in INPUTS},
        "method": "regular intrinsic basis, exact characteristic-zero permanents and pair minors, finite/infinity elimination, complete shared kernel, projected and stacked one-marked minors",
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {REPORT.name: sha256(REPORT), CERTIFICATE.name: sha256(CERTIFICATE), SCRIPT.name: sha256(SCRIPT)},
        "ordinary_tensor": {"support_after_all_affine_markings": support, "zero_subdivisor": "q=phi"},
        "exact_nonzero_all_pair_open": "q*phi*(q-phi)!=0",
        "generic_pair_profile": [3, 3, 4, 3, 3, 3],
        "pair_certificates": pair_data,
        "qphi_one_pair03_drop": qphi_one,
        "incidence_eliminations": incidence,
        "shared_branch": branch,
        "uniform_obstruction_open": "q*phi*(q-phi)*(q^2-1)*(phi^2-1)!=0",
        "ordinary_weighted_H22_status": "WITHDRAWN: frozen stacked witness fails exact replay",
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "limitations": [
            "Construction evidence only; an independent verifier has not promoted this candidate.",
            "Rank-safe families satisfy the tested necessary conditions but are not constructed H22 lifts.",
            "The zero sub-divisor q=phi and its projectivized or valuative directions are deferred.",
            "No claim is made about projective component boundaries, component exhaustiveness, arbitrary-order reduction, or the global conjecture.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
