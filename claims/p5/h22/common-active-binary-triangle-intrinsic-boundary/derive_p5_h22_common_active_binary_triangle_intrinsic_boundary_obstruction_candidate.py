#!/usr/bin/env python3
"""Exact weighted-H22 obstruction candidate on component twenty's s=0 wall."""

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
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / (
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_"
    "OBSTRUCTION_CANDIDATE.md"
)
CERTIFICATE = ROOT / (
    "p5_h22_common_active_binary_triangle_intrinsic_boundary_certificate.json"
)
H31_WALL = REPO_ROOT / "claims/p5/h31/common-active-binary-triangle/P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md"
GENERIC_H22 = REPO_ROOT / "claims/p5/h22/common-active-binary-triangle-component-generic/P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md"
P_PLUS_Q_WALL = REPO_ROOT / "claims/p5/h22/disputed-ownership/p-plus-q-wall/P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md"

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
    return tuple(sp.factor(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.factor(coefficient * entry) for entry in row)


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


def replacement_bases(p):
    zero, one = sp.Integer(0), sp.Integer(1)
    e = (one, zero, zero, zero)
    alpha = (
        (zero, -one, one, zero),
        e,
        e,
        (one, one, one, zero),
    )
    beta = (
        (p * (p + 1) / (2 * p + 1), -2 * p - 1, zero, one),
        (zero, p + 1, p, one),
        (zero, p, p + 1, one),
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
        coefficients[word] = sp.factor(sum(
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
    numerator = sp.together(expression).as_numer_denom()[0]
    return str(sp.expand(numerator)).replace("**", "^")


def unit_projection(label, equations, eliminated, retained):
    variables = tuple(eliminated) + tuple(retained)
    program = "\n".join((
        "ring R=(0,p),(" + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=1;",
        "E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        (
            '"CODEX_RESULT:"'
            '+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));'
        ),
        "quit;",
    ))
    completed = subprocess.run(
        singular_command(), input=program, cwd=ROOT, text=True,
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
        "projected_ideal": ["1"],
        "bidirectional_unit_ideal_equality": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def projection_certificates(alpha, beta):
    slope = sp.Symbol("lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverse_0, inverse_1 = sp.symbols("u v")
    marked = shifted_beta(alpha, beta, shifts)
    individual = []
    shared = []
    for chart in ("finite", "infinity"):
        retained = shifts + ((slope,) if chart == "finite" else ())
        models = {
            direction: build_model(
                alpha, marked, extensions, direction, chart, slope
            )
            for direction in ("D01", "D23")
        }
        for direction in ("D01", "D23"):
            model = models[direction]
            individual.append(unit_projection(
                f"{chart}_{direction}_binary",
                (
                    *model["mixed"], model["A"] - 1,
                    inverse_0 * model["B"] - 1,
                ),
                extensions + (inverse_0,),
                retained,
            ))
        for direction, other_direction in (("D01", "D23"), ("D23", "D01")):
            model = models[direction]
            other = models[other_direction]
            shared.append(unit_projection(
                f"{chart}_shared_{direction}_binary",
                (
                    *model["mixed"], *other["mixed"],
                    model["A"] - 1,
                    inverse_0 * model["B"] - 1,
                    inverse_1 * other["B"] - 1,
                ),
                extensions + (inverse_0, inverse_1),
                retained,
            ))
    return {"individual_binary": individual, "shared_H22": shared}


def main():
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["claim_label"] == "VERIFIED"
    assert certificate["discovery_claim_label"] == "CANDIDATE"
    p = sp.Symbol("p")
    alpha, beta = replacement_bases(p)
    assert all(sp.Matrix((alpha[i], beta[i])).rank() == 2 for i in range(4))
    pure = {
        word: permanent4(tuple(
            beta[i] if word[i] else alpha[i] for i in range(4)
        ))
        for word in WORDS
    }
    assert sp.factor(pure[WORDS[-1]] + 2 * p * (p + 1)) == 0
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    projections = projection_certificates(alpha, beta)
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
            H31_WALL.name: sha256(H31_WALL),
            GENERIC_H22.name: sha256(GENERIC_H22),
            P_PLUS_Q_WALL.name: sha256(P_PLUS_Q_WALL),
        },
        "method": certificate["method"],
        "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "replacement_intrinsic_basis_used": True,
        "pure_support": {"1111": "-2*p*(p+1)"},
        "projection_certificates": projections,
        "generic_intrinsic_wall_weighted_H22_fibre_empty": True,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": certificate["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
