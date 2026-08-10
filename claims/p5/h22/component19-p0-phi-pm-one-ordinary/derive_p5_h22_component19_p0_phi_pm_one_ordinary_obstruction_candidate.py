#!/usr/bin/env python3
"""Exact construction replay on component 19 p=0, phi=+1 and phi=-1."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_P0_PHI_PM_ONE_ORDINARY_OBSTRUCTION_CANDIDATE.md"
CERTIFICATE = ROOT / "p5_h22_component19_p0_phi_pm_one_ordinary_obstruction_certificate.json"
SOURCE = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
H22_THEORY = REPO_ROOT / "claims/p5/coordinate-cegar/P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md"

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
    return tuple(sp.factor(sum(row[i] for row in rows)) for i in range(len(rows[0])))


def scale(coefficient, row):
    return tuple(sp.factor(coefficient * value) for value in row)


def permanent(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not (mask >> column) & 1:
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = {mask: sp.expand(value) for mask, value in following.items()}
    return sp.factor(states[(1 << len(rows)) - 1])


def assert_zero(value):
    if isinstance(value, sp.MatrixBase):
        assert all(sp.cancel(entry) == 0 for entry in value)
    else:
        assert sp.cancel(value) == 0


def component_rows(q, sign, markings):
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    alpha = (abar, cap_b, bbar, abar)
    unmarked_beta = (
        add(bbar, scale(q, cap_b)),
        cap_a,
        cap_a,
        add(cap_b, scale(sign, bbar)),
    )
    beta = tuple(
        add(unmarked_beta[i], scale(markings[i], alpha[i])) for i in range(4)
    )
    return alpha, beta, unmarked_beta


def project(row, extension, direction, slope):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    raise ValueError(direction)


def binary_model(alpha, beta, extensions, direction, slope):
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


def projected_one_marked(model, mode):
    basis = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
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
                basis[column] if other == mode else selected[other]
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


def eliminate(label, equations, eliminated, retained, expected):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=(0,q),(" + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + "; E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        '"CODEX_RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
        "quit;",
    ]
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
        timeout=120, check=False,
    )
    markers = [line for line in completed.stdout.splitlines() if line.startswith("CODEX_RESULT:")]
    assert completed.returncode == 0 and not completed.stderr.strip(), (label, completed.stdout, completed.stderr)
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (label, completed.stdout)
    return {"label": label, "ideal": [str(sp.factor(value)) for value in expected]}


def finite_incidence(sign, q):
    markings = sp.symbols("h0:4")
    slope = sp.Symbol("lam")
    extensions = sp.symbols("u0:8")
    inverse0, inverse1 = sp.symbols("w0 w1")
    alpha, beta, _ = component_rows(q, sign, markings)
    d01 = binary_model(alpha, beta, extensions, "D01", slope)
    d23 = binary_model(alpha, beta, extensions, "D23", slope)
    common = tuple(d01["mixed"] * sp.Matrix(extensions)) + tuple(d23["mixed"] * sp.Matrix(extensions))
    systems = {
        "D01_binary": (
            (*tuple(d01["mixed"] * sp.Matrix(extensions)), d01["coefficients"][WORDS4[0]] - 1, inverse0 * d01["coefficients"][WORDS4[-1]] - 1),
            extensions + (inverse0,), (sp.Integer(1),),
        ),
        "D23_binary": (
            (*tuple(d23["mixed"] * sp.Matrix(extensions)), d23["coefficients"][WORDS4[0]] - 1, inverse0 * d23["coefficients"][WORDS4[-1]] - 1),
            extensions + (inverse0,), (markings[3], markings[0], markings[1] * markings[2]),
        ),
        "shared_A01": (
            (*common, d01["coefficients"][WORDS4[0]] - 1, inverse0 * d01["coefficients"][WORDS4[-1]] - 1, inverse1 * d23["coefficients"][WORDS4[-1]] - 1),
            extensions + (inverse0, inverse1), (sp.Integer(1),),
        ),
        "shared_A23": (
            (*common, d23["coefficients"][WORDS4[0]] - 1, inverse0 * d01["coefficients"][WORDS4[-1]] - 1, inverse1 * d23["coefficients"][WORDS4[-1]] - 1),
            extensions + (inverse0, inverse1), (slope - 1, markings[3], markings[1], markings[0]),
        ),
    }
    retained = markings + (slope,)
    return [
        eliminate(f"phi={sign}_{name}", equations, eliminated, retained, expected)
        for name, (equations, eliminated, expected) in systems.items()
    ]


def pure_and_pairs(sign, q):
    alpha, beta, unmarked_beta = component_rows(q, sign, (0, 0, 0, 0))
    support = {
        "".join(map(str, word)): str(permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4))))
        for word in WORDS4
        if permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4))) != 0
    }
    assert support == {"1111": str(sp.factor(4 * (q - sign)))}
    def squarefree(left, right):
        return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])
    planes = tuple((alpha[i], unmarked_beta[i]) for i in range(4))
    matrices = {
        f"{i}{j}": sp.Matrix.hstack(*(
            squarefree(planes[i][a], planes[j][b]) for a in range(2) for b in range(2)
        )) for i, j in PAIRS
    }
    expected_profile = [3, 3, 4, 3, 3, 3]
    assert [matrix.rank() for matrix in matrices.values()] == expected_profile
    edge03 = sp.factor(matrices["03"].extract((0, 1, 2, 5), range(4)).det())
    assert_zero(edge03 + 8 * sign * (q - sign) ** 2)
    return support, expected_profile, str(edge03)


def sign_certificate(sign, q):
    t, cap_x, cap_y, cap_z, cap_k = sp.symbols("t X Y Z K")
    extensions = sp.symbols("x0:8")
    alpha, beta, _ = component_rows(q, sign, (0, 0, t, 0))
    d01 = binary_model(alpha, beta, extensions, "D01", sp.Integer(1))
    d23 = binary_model(alpha, beta, extensions, "D23", sp.Integer(1))
    combined = d01["mixed"].col_join(d23["mixed"])
    r = q - sign
    rank_rows, rank_columns = (2, 9, 10, 12, 15), (0, 1, 2, 3, 6)
    rank_minor = sp.factor(combined.extract(rank_rows, rank_columns).det())
    assert_zero(rank_minor + 1024 * q * r ** 2)
    assert combined.rank() == 5
    vector_x = sp.Matrix((0, -1 / r, sign / r, 0, 1, 0, 0, 0))
    vector_y = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    vector_z = sp.Matrix((0, -q / r, 1 / r, 0, 0, 0, 0, 1))
    for vector in (vector_x, vector_y, vector_z):
        assert_zero(combined * vector)
    extension = cap_x * vector_x + cap_y * vector_y + cap_z * vector_z
    substitution = dict(zip(extensions, extension))
    cap_f = sign * cap_x + cap_z
    cap_g = r * cap_y - t * cap_f
    cap_h = cap_x + q * cap_z
    diagonals = {
        "A01": sp.factor(d01["coefficients"][WORDS4[0]].subs(substitution)),
        "B01": sp.factor(d01["coefficients"][WORDS4[-1]].subs(substitution)),
        "A23": sp.factor(d23["coefficients"][WORDS4[0]].subs(substitution)),
        "B23": sp.factor(d23["coefficients"][WORDS4[-1]].subs(substitution)),
    }
    wanted = {"A01": 0, "B01": 4 * cap_g, "A23": -4 * cap_f / r, "B23": 4 * cap_h}
    for key, value in wanted.items():
        assert_zero(diagonals[key] - value)

    d23_mode2 = projected_one_marked(d23, 2).subs(substitution)
    d01_mode3 = projected_one_marked(d01, 3).subs(substitution)
    y_minor = sp.factor(d23_mode2.extract((0, 2, 3, 7), range(4)).det())
    line_factor = (sign * q + 1) * cap_x + 2 * q * cap_z
    line_minor = sp.factor(d01_mode3.extract((4, 5, 6, 7), range(4)).det())
    assert_zero(y_minor - 64 * cap_y ** 2 * cap_h)
    assert_zero(line_minor + 64 * cap_x * (q ** 2 - 1) * line_factor * cap_g / r ** 2)

    axis_extension = cap_k * vector_z
    line_extension = 2 * q * cap_k * vector_x - (sign * q + 1) * cap_k * vector_z
    projected_profiles = {}
    for label, value in (("axis_X_zero", axis_extension), ("line_L3_zero", line_extension)):
        sub = dict(zip(extensions, value))
        profiles = {
            name: [projected_one_marked(model, mode).subs(sub).rank() for mode in range(4)]
            for name, model in (("D01", d01), ("D23", d23))
        }
        assert profiles == {"D01": [3, 1, 1, 3], "D23": [3, 3, 3, 3]}
        projected_profiles[label] = profiles

    contraction01 = (1, 1, 0, 0, 0)
    contraction23 = (0, 0, 1, 1, 0)
    def full_rows(value):
        return (
            tuple(tuple(alpha[i]) + (sp.factor(value[i]),) for i in range(4)),
            tuple(tuple(beta[i]) + (sp.factor(value[4 + i]),) for i in range(4)),
        )
    line_alpha, line_beta = full_rows(line_extension)
    line_stack = full_one_marked(line_alpha, line_beta, 3, contraction01).col_join(
        full_one_marked(line_alpha, line_beta, 3, contraction23)
    )
    line_rows = (5, 6, 7, 8, 14)
    line_stack_minor = sp.factor(line_stack.extract(line_rows, range(5)).det())
    assert_zero(line_stack_minor + 512 * sign * cap_k ** 4 * q ** 2 * t * (q ** 2 - 1))
    assert line_stack.rank() == 5

    axis_alpha, axis_beta = full_rows(axis_extension)
    axis_stacks = tuple(
        full_one_marked(axis_alpha, axis_beta, mode, contraction01).col_join(
            full_one_marked(axis_alpha, axis_beta, mode, contraction23)
        ) for mode in range(4)
    )
    if sign == 1:
        gamma = (
            sp.Matrix((0, 0, -2 / cap_k, 0, 1)),
            sp.Matrix((0, 0, (q - 1) / cap_k, -(q - 1) / cap_k, 1)),
            sp.Matrix((0, 0, (q - 1) * (2 * q + 1) / (cap_k * q), -(q - 1) * (2 * q - 1) / (cap_k * q), 1)),
            sp.Matrix((0, 0, -(q + 1) / (q - 1), 1, 0)),
        )
        witnesses = (
            ((1, 3, 7, 8), (0, 1, 2, 3), -64 * cap_k ** 4 * t * (q + 1) / (q - 1) ** 3),
            ((7, 8, 9, 15), (0, 1, 2, 3), -64 * cap_k ** 4 * q / (q - 1) ** 2),
            ((7, 8, 9, 15), (0, 1, 2, 3), -64 * cap_k ** 4 * q ** 2 / (q - 1) ** 2),
            ((4, 5, 7, 8), (0, 1, 2, 4), 128 * cap_k ** 3 * q ** 2 * t / (q - 1) ** 2),
        )
    else:
        gamma = (
            sp.Matrix((0, 0, 0, -2 / cap_k, 1)),
            sp.Matrix((0, 0, (q + 1) / cap_k, -(q + 1) / cap_k, 1)),
            sp.Matrix((0, 0, (q + 1) * (2 * q + 1) / (cap_k * q), -(q + 1) * (2 * q - 1) / (cap_k * q), 1)),
            sp.Matrix((0, 0, -(q + 1) / (q - 1), 1, 0)),
        )
        witnesses = (
            ((1, 3, 7, 8), (0, 1, 2, 3), -64 * cap_k ** 4 * t * (q - 1) / (q + 1) ** 3),
            ((7, 8, 9, 15), (0, 1, 2, 3), -64 * cap_k ** 4 * q / (q + 1) ** 2),
            ((7, 8, 9, 15), (0, 1, 2, 3), 64 * cap_k ** 4 * q ** 2 / (q + 1) ** 2),
            ((4, 5, 7, 8), (0, 1, 2, 4), 128 * cap_k ** 3 * q ** 2 * t * (q - 1) / (q + 1) ** 3),
        )
    axis_witnesses = []
    for mode, (stack, kernel, witness) in enumerate(zip(axis_stacks, gamma, witnesses)):
        rows, columns, expected = witness
        determinant = sp.factor(stack.extract(rows, columns).det())
        assert_zero(determinant - expected)
        assert_zero(stack * kernel)
        assert stack.rank() == 4
        axis_witnesses.append({
            "mode": mode, "rows": list(rows), "columns": list(columns),
            "determinant": str(determinant),
            "kernel": [str(sp.factor(value)) for value in kernel],
        })
    gamma_diagonal = permanent(tuple(tuple(vector) for vector in gamma) + (contraction01,))
    assert gamma_diagonal == 0
    assert all(vector[0] == 0 and vector[1] == 0 for vector in gamma)

    return {
        "sign": sign,
        "finite_incidence": finite_incidence(sign, q),
        "shared_branch": {
            "weight": "[lambda:1]=[1:1]", "marking": "h=(0,0,t,0)",
            "mixed_rank": 5,
            "rank_witness": {"rows": list(rank_rows), "columns": list(rank_columns), "determinant": str(rank_minor)},
            "kernel_basis": [[str(sp.factor(value)) for value in vector] for vector in (vector_x, vector_y, vector_z)],
            "F_G_H": [str(cap_f), str(cap_g), str(cap_h)],
            "genuine_condition": "F*G*H!=0",
            "diagonals": {key: str(value) for key, value in diagonals.items()},
        },
        "individual_one_marked": {
            "D23_mode2_rows_0237": str(y_minor),
            "D01_mode3_rows_4567": str(line_minor),
            "deduction": "on F*G*H!=0 and q*(q^2-1)!=0: Y=0, t!=0, and X*((sign*q+1)*X+2*q*Z)=0",
            "complete_survivor_union": [
                "axis X=Y=0, Z*t!=0",
                "line Y=0, (sign*q+1)*X+2*q*Z=0, X*t!=0",
            ],
            "rank_profiles": projected_profiles,
        },
        "target_local_compatibility": {
            "line_mode3_stack": {
                "rows": list(line_rows), "determinant": str(line_stack_minor),
                "rank": 5, "obstructed_for_all_q_on_open": True,
                "q=-2*sign_checked": True,
            },
            "axis_stacks": axis_witnesses,
            "axis_all_stack_ranks": [4, 4, 4, 4],
            "axis_D01_gamma4_diagonal": str(gamma_diagonal),
            "axis_obstruction": "all shared gamma kernels lie in x0=x1=0, so the required D01 gamma^4 diagonal is zero",
        },
        "weighted_H22_fibre_empty_candidate": True,
    }


def main():
    q = sp.Symbol("q")
    theory = H22_THEORY.read_text(encoding="utf-8")
    assert "Phi(v_0)=lambda_0 E_0^4" in theory
    pure_pair = {}
    signs = []
    for sign in (1, -1):
        support, profile, edge03 = pure_and_pairs(sign, q)
        pure_pair[str(sign)] = {
            "pure_support": support, "pair_profile": profile,
            "edge03_rank4_witness": edge03,
        }
        signs.append(sign_certificate(sign, q))
    result = {
        "status": "pass", "role": "construction", "claim_label": "CANDIDATE",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "scope": "component 19 ordinary p=0, phi=+1 and phi=-1 on q*(q^2-1)!=0",
        "inputs": {SOURCE.name: sha256(SOURCE), H22_THEORY.name: sha256(H22_THEORY)},
        "method": "direct sign-specialized finite incidence elimination, exact shared frame, individual one-marked classification, full two-contraction stacks, and third-colour diagonal obstruction",
        "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
        "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT), CERTIFICATE.name: sha256(CERTIFICATE)},
        "exact_parameter_open": "phi in {+1,-1}, q*(q^2-1)!=0",
        "pure_and_pair_data": pure_pair,
        "sign_certificates": signs,
        "weighted_H22_fibre_empty_candidate": True,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "limitations": [
            "Construction result remains CANDIDATE pending independent verification.",
            "The intersections q=0, q=phi, q=+/-1, and q*phi=+/-1 are excluded; for phi=+/-1 these are contained in q=0 or q=+/-1.",
            "No claim is made about projective weights, other component boundaries, arbitrary-order reduction, or the global conjecture.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
