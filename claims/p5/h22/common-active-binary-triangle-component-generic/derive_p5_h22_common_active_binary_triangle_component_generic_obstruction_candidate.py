#!/usr/bin/env python3
"""Exact generic weighted-H22 obstruction candidate for component twenty."""

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
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_"
    "OBSTRUCTION_CANDIDATE.md"
)
CERTIFICATE = ROOT / (
    "p5_h22_common_active_binary_triangle_component_generic_certificate.json"
)
COMPONENT = ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
H31 = ROOT / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
H22_WALL = ROOT / (
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


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


def permanent4(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(4))
        for permutation in PERMUTATIONS4
    ))


def pure_bases(p, q):
    s = p - q + 1
    e = (1, 0, 0, 0)
    alpha = (
        (0, -p * (p + 1), q * (q - 1), s),
        e,
        e,
        (1, 1, 1, 0),
    )
    beta = (
        (-s, -(p + q), p + q, 0),
        (0, p + 1, q - 1, 1),
        (0, p, q, 1),
        e,
    )
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
    return {
        "coefficients": coefficients,
        "mixed": tuple(coefficients[word] for word in MIXED),
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


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
        "ring R=(0,p,q),(" + ",".join(map(str, variables))
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
            (
                '"CODEX_RESULT:"'
                '+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));'
            ),
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
        line for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        label, completed.stdout
    )
    return {
        "label": label,
        "projected_ideal": (
            ["1"] if expected is None else [str(sp.factor(x)) for x in expected]
        ),
        "bidirectional_ideal_equality": expected is not None,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def projection_certificates(alpha, beta, p, q):
    slope = sp.Symbol("lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverse_0, inverse_1 = sp.symbols("u v")
    marked = shifted_beta(alpha, beta, shifts)
    finite_01 = build_model(
        alpha, marked, extensions, "D01", "finite", slope
    )
    finite_23 = build_model(
        alpha, marked, extensions, "D23", "finite", slope
    )

    marking_relation = sp.expand(
        slope * shifts[1] * shifts[2] * q * (q - 1)
        + slope * shifts[1] * p * q * (p + 1)
        + slope * shifts[2] * p * (p + 1) * (q - 1)
        + shifts[1] * p * q * (p + q)
        + shifts[2] * (p + q) * (p + 1) * (q - 1)
        + slope * p * q * (p + 1) * (q - 1)
    )
    d01_binary = projection_check(
        "finite_D01_binary_marking_projection",
        (
            *finite_01["mixed"], finite_01["A"] - 1,
            inverse_0 * finite_01["B"] - 1,
        ),
        extensions + (inverse_0,),
        shifts + (slope,),
        (shifts[3], shifts[0], marking_relation),
    )

    restricted_shifts = (sp.Integer(0), shifts[1], shifts[2], sp.Integer(0))
    restricted_marked = shifted_beta(alpha, beta, restricted_shifts)
    restricted_01 = build_model(
        alpha, restricted_marked, extensions, "D01", "finite", slope
    )
    restricted_23 = build_model(
        alpha, restricted_marked, extensions, "D23", "finite", slope
    )
    shared_d01_finite = projection_check(
        "finite_shared_D01_binary_after_exact_marking_restriction",
        (
            *restricted_01["mixed"], *restricted_23["mixed"],
            restricted_01["A"] - 1,
            inverse_0 * restricted_01["B"] - 1,
            inverse_1 * restricted_23["B"] - 1,
            marking_relation,
        ),
        extensions + (inverse_0, inverse_1),
        (shifts[1], shifts[2], slope),
    )
    shared_d23_finite = projection_check(
        "finite_shared_D23_binary",
        (
            *finite_01["mixed"], *finite_23["mixed"],
            finite_23["A"] - 1,
            inverse_0 * finite_23["B"] - 1,
            inverse_1 * finite_01["B"] - 1,
        ),
        extensions + (inverse_0, inverse_1),
        shifts + (slope,),
    )

    infinity_01 = build_model(alpha, marked, extensions, "D01", "infinity")
    infinity_23 = build_model(alpha, marked, extensions, "D23", "infinity")
    shared_d01_infinity = projection_check(
        "infinity_shared_D01_binary",
        (
            *infinity_01["mixed"], *infinity_23["mixed"],
            infinity_01["A"] - 1,
            inverse_0 * infinity_01["B"] - 1,
            inverse_1 * infinity_23["B"] - 1,
        ),
        extensions + (inverse_0, inverse_1),
        shifts,
    )
    shared_d23_infinity = projection_check(
        "infinity_shared_D23_binary",
        (
            *infinity_01["mixed"], *infinity_23["mixed"],
            infinity_23["A"] - 1,
            inverse_0 * infinity_23["B"] - 1,
            inverse_1 * infinity_01["B"] - 1,
        ),
        extensions + (inverse_0, inverse_1),
        shifts,
    )
    return {
        "finite_D01_binary_marking_projection": d01_binary,
        "finite_shared_D01_binary": shared_d01_finite,
        "finite_shared_D23_binary": shared_d23_finite,
        "infinity_shared_D01_binary": shared_d01_infinity,
        "infinity_shared_D23_binary": shared_d23_infinity,
        "marking_relation": str(sp.factor(marking_relation)),
    }


def main():
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["claim_label"] == "VERIFIED"
    p, q = sp.symbols("p q")
    alpha, beta = pure_bases(p, q)
    pure = {
        word: sp.factor(permanent4(tuple(
            beta[i] if word[i] else alpha[i] for i in range(4)
        )))
        for word in WORDS
    }
    expected_pure = 2 * (p + q) * (p - q + 1)
    assert sp.factor(pure[WORDS[-1]] - expected_pure) == 0
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    projections = projection_certificates(alpha, beta, p, q)
    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "discovery_claim_label": "CANDIDATE",
        "scope": certificate["scope"],
        "inputs": {
            COMPONENT.name: sha256(COMPONENT),
            H31.name: sha256(H31),
            H22_WALL.name: sha256(H22_WALL),
        },
        "method": certificate["method"],
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "pure_support": {"1111": str(sp.factor(expected_pure))},
        "projection_certificates": projections,
        "generic_weighted_H22_fibre_empty": True,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": certificate["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
