#!/usr/bin/env python3
"""Exact q=0 weighted-H22 special-divisor candidate for component nineteen."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import sympy as sp

ROOT = HERE
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_OBSTRUCTION_CANDIDATE.md"
CERTIFICATE = ROOT / "p5_h22_component19_q0_special_divisor_certificate.json"
INPUTS = tuple(REPO_ROOT / name for name in (
    "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md",
    'claims/p5/h22/common-kernel-vertical-triangle-component-generic/P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md',
    'claims/p5/h22/common-kernel-vertical-triangle-component-generic/P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md',
    'claims/p5/h22/common-kernel-vertical-triangle-component-generic/p5_h22_common_kernel_vertical_triangle_component_generic_certificate.json',
    "claims/p5/h22/common-singleton/P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md",
))

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True, encoding="utf-8",
        capture_output=True, check=True, timeout=15,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def permanent3(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(3))
        for permutation in PERMUTATIONS3
    ))


def permanent4(rows):
    return sp.factor(sum(
        sp.prod(rows[i][permutation[i]] for i in range(4))
        for permutation in PERMUTATIONS4
    ))


def specialized_planes(p, phi):
    """Reconstruct the q=0 planes directly, before choosing a pure basis."""
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    planes = (
        (add(abar, scale(p, cap_b)), bbar),
        (cap_b, cap_a),
        (bbar, cap_a),
        (abar, add(cap_b, scale(phi, bbar))),
    )
    return planes, (cap_a, abar, cap_b, bbar)


def intrinsic_basis(p, phi):
    planes, (cap_a, abar, cap_b, bbar) = specialized_planes(p, phi)
    first, second = planes[0]
    alpha0 = add(scale(-phi, first), scale(-p, second))
    alpha = (alpha0, cap_b, bbar, abar)
    beta = (first, cap_a, cap_a, add(cap_b, scale(phi, bbar)))
    # Relative to (first,second), columns (alpha0,beta0) have determinant p.
    change = sp.Matrix(((-phi, 1), (-p, 0)))
    assert sp.factor(change.det() - p) == 0
    return planes, alpha, beta


def shifted_beta(alpha, beta, shifts):
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def original_coefficients(alpha, beta):
    return {
        word: permanent4(tuple(
            beta[i] if word[i] else alpha[i] for i in range(4)
        ))
        for word in WORDS
    }


def pure_flattening_certificates(coefficients):
    """Recover each intrinsic pure-kernel line from the specialized tensor."""
    output = []
    for mode in range(4):
        other = tuple(index for index in range(4) if index != mode)
        columns = tuple(itertools.product((0, 1), repeat=3))
        matrix = sp.Matrix([
            [
                coefficients[tuple(
                    bit if index == mode else column[other.index(index)]
                    for index in range(4)
                )]
                for column in columns
            ]
            for bit in (0, 1)
        ])
        assert matrix.rank() == 1
        kernel = matrix.T.nullspace()
        assert kernel == [sp.Matrix((1, 0))]
        output.append({
            "mode": mode, "flattening_rank": 1,
            "kernel_in_alpha_beta_coordinates": [1, 0],
        })
    return output


def squarefree_product(left, right):
    return sp.Matrix(tuple(
        sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS
    ))


def pair_matrix(left_plane, right_plane):
    return sp.Matrix.hstack(*(
        squarefree_product(left_plane[i], right_plane[j])
        for i in range(2) for j in range(2)
    ))


def pair_rank_certificates(planes):
    # Fixed witnesses use only units on p*phi!=0; phi^2-1 is not needed here.
    selections = {
        "01": (3, (1, 2, 3), (0, 1, 3), "4*p"),
        "02": (4, (1, 2, 3, 5), (0, 1, 2, 3), "8*p"),
        "03": (4, (0, 1, 2, 5), (0, 1, 2, 3), "-8*phi"),
        "12": (3, (0, 1, 2), (1, 2, 3), "-4"),
        "13": (3, (1, 2, 5), (0, 1, 3), "4*phi"),
        "23": (3, (1, 2, 5), (0, 1, 3), "4*phi"),
    }
    output = {}
    for i, j in PAIRS:
        label = f"{i}{j}"
        expected_rank, rows, columns, expected_minor = selections[label]
        matrix = pair_matrix(planes[i], planes[j])
        minor = sp.factor(matrix.extract(rows, columns).det())
        assert str(minor) == expected_minor
        higher_checked = 0
        if expected_rank == 3:
            for row_set in itertools.combinations(range(6), 4):
                assert sp.factor(matrix.extract(row_set, range(4)).det()) == 0
                higher_checked += 1
        output[label] = {
            "rank": expected_rank,
            "nonzero_minor": {
                "rows": list(rows), "columns": list(columns),
                "determinant": str(minor),
            },
            "higher_minors_checked_zero": higher_checked,
        }
    assert [output[f"{i}{j}"]["rank"] for i, j in PAIRS] == [3, 4, 4, 3, 3, 3]
    return output


def project(row, extension, direction, chart, slope=None):
    if direction == "D01" and chart == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23" and chart == "finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart, slope))


def homogeneous_project(row, extension, direction, rho, sigma):
    if direction == "D01":
        return (rho * row[0] + sigma * row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], rho * row[2] + sigma * row[3], extension)
    raise ValueError(direction)


def build_model(alpha, beta, extensions, direction, chart, slope=None):
    alpha_rows = tuple(
        project(alpha[i], extensions[i], direction, chart, slope) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extensions[4 + i], direction, chart, slope)
        for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[i] if word[i] else alpha_rows[i] for i in range(4)
        )
        coefficients[word] = sp.factor(sum(
            selected[i][3] * permanent3(tuple(
                selected[j][:3] for j in range(4) if j != i
            ))
            for i in range(4)
        ))
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], value) for value in extensions]
        for word in MIXED
    ])
    return {
        "alpha_rows": alpha_rows, "beta_rows": beta_rows,
        "coefficients": coefficients, "mixed": mixed,
        "A": coefficients[WORDS[0]], "B": coefficients[WORDS[-1]],
    }


def homogeneous_model(alpha, beta, extension, direction, rho, sigma):
    alpha_rows = tuple(
        homogeneous_project(alpha[i], extension[i], direction, rho, sigma)
        for i in range(4)
    )
    beta_rows = tuple(
        homogeneous_project(beta[i], extension[4 + i], direction, rho, sigma)
        for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[i] if word[i] else alpha_rows[i] for i in range(4)
        )
        coefficients[word] = sp.factor(sum(
            selected[i][3] * permanent3(tuple(
                selected[j][:3] for j in range(4) if j != i
            ))
            for i in range(4)
        ))
    return {
        "alpha_rows": alpha_rows, "beta_rows": beta_rows,
        "coefficients": coefficients,
    }


def one_marked_matrix(model, mode):
    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            model["beta_rows"][index] if bits[position]
            else model["alpha_rows"][index]
            for position, index in enumerate(other)
        )
        rows.append(tuple(
            permanent3(tuple(
                tuple(row[column] for column in range(4) if column != omitted)
                for row in selected
            ))
            for omitted in range(4)
        ))
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


def projection_check(label, equations, eliminated, retained, expected=None):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=(0,p,phi),(" + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    if expected is None:
        lines.append('"CODEX_RESULT:"+string(reduce(1,J)==0)+":"+string(size(J));')
    else:
        lines.extend((
            "ideal E=" + ",".join(map(singular, expected)) + ";",
            "E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            '"CODEX_RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
        ))
    lines.append("quit;")
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
        timeout=120, check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stdout, completed.stderr
    )
    markers = [
        line for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        label, completed.stdout
    )
    return {
        "label": label,
        "projected_ideal": ["1"] if expected is None else [
            str(sp.factor(value)) for value in expected
        ],
        "bidirectional_ideal_equality": expected is not None,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def projection_certificates(alpha, unmarked_beta):
    phi = sp.Symbol("phi")
    slope = sp.Symbol("lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverse0, inverse1 = sp.symbols("u v")
    beta = shifted_beta(alpha, unmarked_beta, shifts)
    output = []
    for chart in ("finite", "infinity"):
        retained = shifts + ((slope,) if chart == "finite" else ())
        d01 = build_model(alpha, beta, extensions, "D01", chart, slope)
        d23 = build_model(alpha, beta, extensions, "D23", chart, slope)
        output.append(projection_check(
            f"D01_binary_{chart}",
            (*tuple(d01["mixed"] * sp.Matrix(extensions)),
             d01["A"] - 1, inverse0 * d01["B"] - 1),
            extensions + (inverse0,), retained,
        ))
        if chart == "finite":
            expected_binary = (
                shifts[3], phi * shifts[0] - 1,
                shifts[1] * shifts[2] * (slope - 1),
                shifts[1] ** 2 * shifts[2],
            )
        else:
            expected_binary = (
                shifts[3], phi * shifts[0] - 1,
                shifts[1] * shifts[2],
            )
        output.append(projection_check(
            f"D23_binary_{chart}",
            (*tuple(d23["mixed"] * sp.Matrix(extensions)),
             d23["A"] - 1, inverse0 * d23["B"] - 1),
            extensions + (inverse0,), retained, expected_binary,
        ))
        compatibility = (
            *(d01["coefficients"][word] for word in WORDS[:-1]),
            d01["B"] - 1,
            *tuple(d23["mixed"] * sp.Matrix(extensions)),
            inverse0 * d23["A"] - 1,
            inverse1 * d23["B"] - 1,
        )
        expected_shared = None
        if chart == "finite":
            expected_shared = (
                slope - 1, shifts[3], shifts[1], phi * shifts[0] - 1,
            )
        output.append(projection_check(
            f"shared_pure_D01_binary_D23_{chart}", compatibility,
            extensions + (inverse0, inverse1), retained, expected_shared,
        ))
    return output


def shared_branch_certificate(alpha, unmarked_beta, p, phi):
    cap_c, cap_d, t = sp.symbols("C D t")
    extensions = sp.symbols("x0:8")
    shifts = (1 / phi, 0, t, 0)
    beta = shifted_beta(alpha, unmarked_beta, shifts)
    d01 = build_model(alpha, beta, extensions, "D01", "finite", sp.Integer(1))
    d23 = build_model(alpha, beta, extensions, "D23", "finite", sp.Integer(1))
    combined = sp.Matrix([
        [sp.diff(expression, value) for value in extensions]
        for expression in (
            *(d01["coefficients"][word] for word in WORDS[:-1]),
            *tuple(d23["coefficients"][word] for word in MIXED),
        )
    ])
    witness_rows = (2, 3, 5, 11, 13, 16)
    witness_columns = (0, 1, 2, 3, 6, 7)
    witness = sp.factor(combined.extract(witness_rows, witness_columns).det())
    expected_witness = 4096 * p ** 4 * phi ** 2 * (phi - 1) * (phi + 1)
    assert sp.factor(witness - expected_witness) == 0

    vector_c = sp.Matrix((0, -1 / p, phi / p, 0, 1, 0, 0, 0))
    vector_d = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    frame = sp.Matrix.hstack(vector_c, vector_d)
    assert frame.rank() == 2
    assert all(sp.factor(value) == 0 for value in combined * frame)

    extension = cap_c * vector_c + cap_d * vector_d
    substitutions = dict(zip(extensions, extension, strict=True))
    coefficients01 = {
        word: sp.factor(value.subs(substitutions))
        for word, value in d01["coefficients"].items()
    }
    coefficients23 = {
        word: sp.factor(value.subs(substitutions))
        for word, value in d23["coefficients"].items()
    }
    assert all(
        value == 0 for word, value in coefficients01.items() if word != WORDS[-1]
    )
    assert all(
        value == 0 for word, value in coefficients23.items()
        if word not in (WORDS[0], WORDS[-1])
    )
    expected_b01 = 4 * (p * cap_d - phi * t * cap_c)
    expected_a23 = 4 * phi ** 2 * cap_c / p
    expected_b23 = 4 * cap_c
    assert sp.factor(coefficients01[WORDS[-1]] - expected_b01) == 0
    assert sp.factor(coefficients23[WORDS[0]] - expected_a23) == 0
    assert sp.factor(coefficients23[WORDS[-1]] - expected_b23) == 0

    marked = one_marked_matrix(d01, 3).subs(substitutions)
    fixed_minor = sp.factor(marked.extract((1, 2, 5, 7), range(4)).det())
    expected_minor = -64 * cap_c * p * (p * cap_d - phi * t * cap_c) ** 2
    assert sp.factor(fixed_minor - expected_minor) == 0

    # The excluded parameter divisor is real: the shared kernel jumps there.
    ranks_on_excluded_divisor = {
        "phi=1": combined.subs(phi, 1).rank(),
        "phi=-1": combined.subs(phi, -1).rank(),
    }
    assert ranks_on_excluded_divisor == {"phi=1": 5, "phi=-1": 5}
    return {
        "marking": "h=(1/phi,0,t,0)",
        "homogeneous_weight": "[1:1]",
        "combined_unwanted_matrix_shape": list(combined.shape),
        "rank_on_open": 6,
        "rank_witness": {
            "rows": list(witness_rows), "columns": list(witness_columns),
            "determinant": str(witness),
        },
        "complete_kernel_frame": [
            [str(sp.factor(value)) for value in vector_c],
            [str(sp.factor(value)) for value in vector_d],
        ],
        "D01_pure_diagonal": str(sp.factor(expected_b01)),
        "D23_binary_diagonals": [
            str(sp.factor(expected_a23)), str(sp.factor(expected_b23)),
        ],
        "common_genuine_condition": "C*(p*D-phi*t*C)!=0 on p*phi!=0",
        "fixed_transverse_minor": {
            "direction": "D01", "marked_mode": 3,
            "rows": [1, 2, 5, 7], "columns": [0, 1, 2, 3],
            "determinant": str(fixed_minor),
        },
        "excluded_phi_squared_one_ranks": ranks_on_excluded_divisor,
    }


def false_lead_certificate(alpha, unmarked_beta, p, phi):
    beta = shifted_beta(alpha, unmarked_beta, (1 / phi, 0, 0, 0))
    rho, sigma = 1 - phi, phi + 1
    extension23 = (0, 1, 0, 0, 0, 0, 0, 1)
    extension01 = (-phi ** 2, 0, 0, phi, 0, 1, 1, 0)
    d23 = homogeneous_model(alpha, beta, extension23, "D23", rho, sigma)
    d01 = homogeneous_model(alpha, beta, extension01, "D01", rho, sigma)
    assert {
        word: value for word, value in d23["coefficients"].items() if value != 0
    } == {WORDS[0]: -4 * phi ** 2, WORDS[-1]: 4 * p}
    assert {
        word: value for word, value in d01["coefficients"].items() if value != 0
    } == {WORDS[-1]: 8 * p}
    ranks23 = [one_marked_matrix(d23, mode).rank() for mode in range(4)]
    ranks01 = [one_marked_matrix(d01, mode).rank() for mode in range(4)]
    assert ranks23 == [3, 3, 3, 3]
    assert ranks01 == [2, 3, 3, 3]
    assert sp.Matrix((extension23, extension01)).extract((0, 1), (1, 5)).det() == 1
    return {
        "status": "REFUTED as a shared H22 lift",
        "marking": "h=(1/phi,0,0,0)",
        "homogeneous_weight": "[1-phi:phi+1]",
        "D23_extension": list(extension23),
        "D01_extension": [str(value) for value in extension01],
        "extension_proportionality_minor": "1",
        "D23_one_marked_ranks": ranks23,
        "D01_one_marked_ranks": ranks01,
        "reason": "the low-rank extensions differ and shared compatibility requires [1:1]",
    }


def main():
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert stored["claim_label"] == "VERIFIED"
    assert stored["discovery_claim_label"] == "CANDIDATE"
    p, phi = sp.symbols("p phi")
    planes, alpha, beta = intrinsic_basis(p, phi)

    shifts = sp.symbols("h0:4")
    coefficients = original_coefficients(alpha, shifted_beta(alpha, beta, shifts))
    support = {"".join(map(str, word)): str(value) for word, value in coefficients.items() if value != 0}
    assert support == {"1111": "4*p"}
    flattenings = pure_flattening_certificates(coefficients)
    pairs = pair_rank_certificates(planes)
    projections = projection_certificates(alpha, beta)
    branch = shared_branch_certificate(alpha, beta, p, phi)
    false_lead = false_lead_certificate(alpha, beta, p, phi)

    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "discovery_claim_label": "CANDIDATE",
        "scope": stored["scope"],
        "inputs": {path.name: sha256(path) for path in INPUTS},
        "method": stored["method"],
        "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT), CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "specialized_normal_form": {
            "field": "Q(p,phi)", "divisor": "q=0",
            "open": "p*phi*(phi^2-1)!=0",
            "alpha": [[str(value) for value in row] for row in alpha],
            "beta": [[str(value) for value in row] for row in beta],
            "mode0_basis_change_determinant": "p",
            "pure_support_after_all_affine_markings": support,
            "pure_point_unique": True,
            "flattening_kernel_certificates": flattenings,
            "pair_profile": [pairs[f"{i}{j}"]["rank"] for i, j in PAIRS],
            "pair_certificates": pairs,
        },
        "projective_weight_exhaustion": projections,
        "orientation_exhaustion": {
            "D23_pure_D01_binary": "empty because D01 binary is empty on both weight charts",
            "D01_pure_D23_binary": "unique shared finite branch, then transverse rank obstruction",
        },
        "shared_branch": branch,
        "specialization_failure_retained": {
            "naive_specialized_D23_finite_ideal": [
                "h3", "phi*h0-1", "h1*h2*(lam-1)"
            ],
            "actual_direct_D23_finite_ideal_adds": "h1^2*h2",
            "effect": "naive substitution creates false scheme/set survivors at lam=1",
        },
        "unshared_low_rank_false_lead": false_lead,
        "parameter_and_extension_boundaries": stored["boundaries"],
        "weighted_H22_fibre_empty_on_stated_open": True,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": stored["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
