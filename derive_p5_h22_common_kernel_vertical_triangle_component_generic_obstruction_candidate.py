#!/usr/bin/env python3
"""Exact generic weighted-H22 obstruction candidate for component nineteen."""

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
REPORT = ROOT / (
    "P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_"
    "OBSTRUCTION_CANDIDATE.md"
)
CERTIFICATE = ROOT / (
    "p5_h22_common_kernel_vertical_triangle_component_generic_certificate.json"
)
COMPONENT = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
H31 = ROOT / "P5_H31_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
H22_DEFINITION = ROOT / "P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True, encoding="utf-8",
        capture_output=True, check=True,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent3(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(3))
        for permutation in PERMUTATIONS3
    ))


def pure_bases(p, q, phi):
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    row_00 = add(abar, scale(p, cap_b))
    row_01 = add(bbar, scale(q, cap_b))
    alpha_0 = add(scale(q - phi, row_00), scale(-p, row_01))
    alpha = (alpha_0, cap_b, bbar, abar)
    beta = (row_00, cap_a, cap_a, add(cap_b, scale(phi, bbar)))
    return alpha, beta


def shifted_beta(alpha, beta, shifts):
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def project(row, extension, direction, chart, slope=None):
    if chart == "finite" and direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if chart == "finite" and direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if chart == "infinity" and direction == "D01":
        return (row[0], row[2], row[3], extension)
    if chart == "infinity" and direction == "D23":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


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
        coefficients[word] = sp.expand(sum(
            selected[i][3]
            * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
            for i in range(4)
        ))
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], value) for value in extensions]
        for word in MIXED
    ])
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "mixed": mixed,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def homogeneous_model(alpha, beta, extensions, direction, rho, sigma):
    def homogeneous_project(row, extension):
        if direction == "D01":
            return (rho * row[0] + sigma * row[1], row[2], row[3], extension)
        return (row[0], row[1], rho * row[2] + sigma * row[3], extension)

    alpha_rows = tuple(homogeneous_project(alpha[i], extensions[i]) for i in range(4))
    beta_rows = tuple(
        homogeneous_project(beta[i], extensions[4 + i]) for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[i] if word[i] else alpha_rows[i] for i in range(4)
        )
        coefficients[word] = sp.factor(sum(
            selected[i][3]
            * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
            for i in range(4)
        ))
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
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
        "ring R=(0,p,q,phi),("
        + ",".join(map(str, variables))
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
        encoding="utf-8", errors="replace", capture_output=True, timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stdout, completed.stderr
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        label, completed.stdout
    )
    return {
        "label": label,
        "projected_ideal": ["1"] if expected is None else [str(sp.factor(x)) for x in expected],
        "bidirectional_ideal_equality": expected is not None,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def projection_certificates(alpha, unmarked_beta, p, q, phi):
    slope = sp.Symbol("lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    marked_beta = shifted_beta(alpha, unmarked_beta, shifts)
    inverse_0, inverse_1 = sp.symbols("u v")
    certificates = []

    for chart in ("finite", "infinity"):
        retained = shifts + ((slope,) if chart == "finite" else ())
        d01 = build_model(alpha, marked_beta, extensions, "D01", chart, slope)
        binary_equations = (
            *tuple(d01["mixed"] * sp.Matrix(extensions)),
            d01["A"] - 1,
            inverse_0 * d01["B"] - 1,
        )
        certificates.append(projection_check(
            f"D01_binary_{chart}", binary_equations,
            extensions + (inverse_0,), retained,
        ))

        d23 = build_model(alpha, marked_beta, extensions, "D23", chart, slope)
        if chart == "finite":
            expected_binary = (
                shifts[3],
                (q - phi) * shifts[0] + 1,
                shifts[1] * shifts[2] * ((q + 1) * slope + q - 1),
            )
        else:
            expected_binary = (
                shifts[3], (q - phi) * shifts[0] + 1, shifts[1] * shifts[2]
            )
        d23_binary_equations = (
            *tuple(d23["mixed"] * sp.Matrix(extensions)),
            d23["A"] - 1,
            inverse_0 * d23["B"] - 1,
        )
        certificates.append(projection_check(
            f"D23_binary_{chart}", d23_binary_equations,
            extensions + (inverse_0,), retained, expected_binary,
        ))

        compatibility_equations = (
            *(d01["coefficients"][word] for word in WORDS[:-1]),
            d01["B"] - 1,
            *tuple(d23["mixed"] * sp.Matrix(extensions)),
            inverse_0 * d23["A"] - 1,
            inverse_1 * d23["B"] - 1,
        )
        expected_compatibility = None
        if chart == "finite":
            expected_compatibility = (
                slope - 1,
                shifts[3],
                shifts[1],
                (q - phi) * shifts[0] + 1,
            )
        certificates.append(projection_check(
            f"shared_pure_D01_binary_D23_{chart}", compatibility_equations,
            extensions + (inverse_0, inverse_1), retained,
            expected_compatibility,
        ))
    return certificates


def shared_branch_certificate(alpha, unmarked_beta, p, q, phi):
    cap_c, cap_d, t = sp.symbols("C D t")
    extensions = sp.symbols("x0:8")
    shifts = (-(q - phi) ** -1, 0, t, 0)
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
    vector_c = sp.Matrix((0, -1 / p, phi / p, 0, 1, 0, 0, 0))
    vector_d = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    frame = sp.Matrix.hstack(vector_c, vector_d)
    assert combined.rank() == 6
    assert frame.rank() == 2
    assert all(sp.factor(value) == 0 for value in combined * frame)

    extension = cap_c * vector_c + cap_d * vector_d
    values = dict(zip(extensions, extension, strict=True))
    d01_coefficients = {
        word: sp.factor(value.subs(values))
        for word, value in d01["coefficients"].items()
    }
    d23_coefficients = {
        word: sp.factor(value.subs(values))
        for word, value in d23["coefficients"].items()
    }
    assert all(
        value == 0 for word, value in d01_coefficients.items() if word != WORDS[-1]
    )
    assert all(
        value == 0 for word, value in d23_coefficients.items()
        if word not in (WORDS[0], WORDS[-1])
    )
    expected_b01 = 4 * (p * cap_d - phi * t * cap_c)
    expected_a23 = -4 * phi * (q - phi) * cap_c / p
    expected_b23 = 4 * cap_c
    assert sp.factor(d01_coefficients[WORDS[-1]] - expected_b01) == 0
    assert sp.factor(d23_coefficients[WORDS[0]] - expected_a23) == 0
    assert sp.factor(d23_coefficients[WORDS[-1]] - expected_b23) == 0

    marked = one_marked_matrix(d01, 3).subs(values)
    fixed_minor = sp.factor(marked.extract((1, 2, 5, 7), range(4)).det())
    expected_minor = -64 * cap_c * p * (p * cap_d - phi * t * cap_c) ** 2
    assert sp.factor(fixed_minor - expected_minor) == 0
    return {
        "marking": "h0=-1/(q-phi), h1=0, h2=t, h3=0",
        "homogeneous_weight": "[1:1]",
        "complete_shared_kernel_rank": 2,
        "kernel_frame": [
            [str(sp.factor(value)) for value in vector_c],
            [str(sp.factor(value)) for value in vector_d],
        ],
        "D01_pure_diagonal": str(sp.factor(expected_b01)),
        "D23_binary_diagonals": [
            str(sp.factor(expected_a23)), str(sp.factor(expected_b23))
        ],
        "common_genuine_condition": "C*p*phi*(q-phi)*(p*D-phi*t*C)!=0",
        "fixed_minor": {
            "direction": "D01",
            "mode": 3,
            "rows": [1, 2, 5, 7],
            "columns": [0, 1, 2, 3],
            "determinant": str(fixed_minor),
        },
        "genuine_locus_rank_four": True,
    }


def unshared_false_lead(alpha, unmarked_beta, p, q, phi):
    shifts = (-(q - phi) ** -1, 0, 0, 0)
    beta = shifted_beta(alpha, unmarked_beta, shifts)
    rho, sigma = 1 - phi, phi + 1
    d23_extension = (0, 1, 0, 0, 0, 0, 0, 1)
    d01_extension = (phi * (q - phi), 0, 0, phi, 0, 1, 1, 0)
    d23 = homogeneous_model(alpha, beta, d23_extension, "D23", rho, sigma)
    d01 = homogeneous_model(alpha, beta, d01_extension, "D01", rho, sigma)
    assert {
        word: value for word, value in d23["coefficients"].items() if value != 0
    } == {WORDS[0]: 4 * phi * (q - phi), WORDS[-1]: 4 * p}
    assert {
        word: value for word, value in d01["coefficients"].items() if value != 0
    } == {WORDS[-1]: 8 * p}
    d23_ranks = [one_marked_matrix(d23, mode).rank() for mode in range(4)]
    d01_ranks = [one_marked_matrix(d01, mode).rank() for mode in range(4)]
    assert d23_ranks == [3, 3, 3, 3]
    assert d01_ranks == [2, 3, 3, 3]
    assert d23_extension != d01_extension
    return {
        "homogeneous_weight": "[1-phi:phi+1]",
        "marking": "h0=-1/(q-phi), h1=h2=h3=0",
        "D23_extension": list(d23_extension),
        "D01_extension": [str(value) for value in d01_extension],
        "D23_one_marked_ranks": d23_ranks,
        "D01_one_marked_ranks": d01_ranks,
        "failure": "the extension vectors differ; shared compatibility is absent generically",
    }


def main():
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["claim_label"] == "VERIFIED"
    p, q, phi = sp.symbols("p q phi")
    alpha, beta = pure_bases(p, q, phi)
    pure = homogeneous_model(alpha, beta, (0,) * 8, "D01", 0, 1)["coefficients"]
    # The zero extensions make the contracted tensor zero; verify the original
    # four-source restriction separately by appending no column.
    original = {}
    permutations4 = tuple(itertools.permutations(range(4)))
    for word in WORDS:
        rows = tuple(beta[i] if word[i] else alpha[i] for i in range(4))
        original[word] = sp.factor(sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in permutations4
        ))
    assert all(value == 0 for word, value in original.items() if word != WORDS[-1])
    assert sp.factor(original[WORDS[-1]] - 4 * p) == 0
    del pure

    projections = projection_certificates(alpha, beta, p, q, phi)
    branch = shared_branch_certificate(alpha, beta, p, q, phi)
    false_lead = unshared_false_lead(alpha, beta, p, q, phi)
    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "discovery_claim_label": "CANDIDATE",
        "scope": certificate["scope"],
        "inputs": {
            COMPONENT.name: sha256(COMPONENT),
            H31.name: sha256(H31),
            H22_DEFINITION.name: sha256(H22_DEFINITION),
        },
        "method": certificate["method"],
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "pure_coefficient": "4*p",
        "projection_certificates": projections,
        "complete_shared_branch": branch,
        "unshared_low_rank_false_lead": false_lead,
        "generic_weighted_H22_fibre_empty": True,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": certificate["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
