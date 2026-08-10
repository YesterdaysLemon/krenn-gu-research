#!/usr/bin/env python3
"""No-import audit of component 22's finite-D23 h0=0 residual."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import shutil
import subprocess
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / (
    "verify_p5_h22_unequal_complement_common_kernel_component_"
    "d23_h0_zero_residual_obstruction.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))

A, R, D = sp.symbols("A R D")
h2, rho = sp.symbols("h2 rho")
x = sp.symbols("x0:8")
w, z = sp.symbols("w z")
s = 2 * A + R


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def component_rows():
    u = (1 - D) / 2
    v = (1 + D) / 2
    g = -s / 2
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = (2 * A, 0, 1, 1)
    mr = add(m, c, R)
    d = (g, g, u, v)
    y0 = (0, D * s, -u, v)
    x0 = (-A * v, A * (u + 1) + R, 1, 0)
    alpha = (y0, m, mr, c)
    canonical = (x0, a, a, d)
    marking = (0, 0, h2, s / 2)
    marked = tuple(add(canonical[i], alpha[i], marking[i]) for i in range(4))
    assert all(sp.Matrix((alpha[i], marked[i])).rank() == 2 for i in range(4))
    return alpha, marked


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def project(row, extension):
    return (row[0], row[1], rho * row[2] + row[3], extension)


def finite_d23_model():
    alpha, beta = component_rows()
    alpha_p = tuple(project(alpha[i], x[i]) for i in range(4))
    beta_p = tuple(project(beta[i], x[4 + i]) for i in range(4))
    coefficients = {}
    for word in WORDS:
        selected = tuple(beta_p[i] if word[i] else alpha_p[i] for i in range(4))
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    return (
        tuple(coefficients[word] for word in MIXED),
        coefficients[WORDS[0]],
        coefficients[WORDS[-1]],
    )


def residual_data():
    f2 = s * h2 + 1
    f6 = (D - 1) * rho + D + 1
    f7 = (A * D + A + R) * rho + A * D - A - R
    f8 = (A * D + A + R * D) * rho + A * D - A + R * D
    L0 = R * rho + s
    T = (
        (A**2 * D - 3 * A**2 - 3 * A * R - R**2) * rho
        + A**2 * D
        + 3 * A**2
        + 3 * A * R
        + R**2
    )
    G0 = (
        (
            2 * A**3 * D**2
            + 2 * A**3 * D
            + 4 * A**2 * R * D**2
            + 2 * A**2 * R
            + A * R**2 * D**2
            + A * R**2
        )
        * h2
        * rho
        + (
            -2 * A**3 * D**2
            + 2 * A**3 * D
            - 4 * A**2 * R * D**2
            - 2 * A**2 * R
            - A * R**2 * D**2
            - A * R**2
        )
        * h2
        + (-(A**2) * D**2 + 5 * A**2 * D - 2 * A**2 + 4 * A * R * D - A * R + R**2 * D)
        * rho
        + A**2 * D**2
        - 3 * A**2 * D
        + 2 * A**2
        - 4 * A * R * D
        + A * R
        - R**2 * D
    )
    G20 = (
        (2 * A**2 * D - 6 * A**2 - A * R * D**2 + 2 * A * R * D - 5 * A * R - R**2)
        * h2
        * rho
        + (2 * A**2 * D - 6 * A**2 + A * R * D**2 + 2 * A * R * D - 5 * A * R - R**2)
        * h2
        + (A * D**2 - A * D - 2 * A - R) * rho
        - A * D**2
        - A * D
        - 2 * A
        - R
    )
    multiplier = sp.factor(
        h2 * f2 * rho * (rho - 1) * (rho + 1) * f6 * f7 * f8 * L0 * T * (R * h2 - 1)
    )
    return G0, G20, multiplier


def clear(expression):
    return sp.factor(sp.fraction(sp.together(expression))[0])


def singular_text(expression):
    return str(clear(expression)).replace("**", "^")


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def run_singular(label, program, expected):
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [expected], (label, completed.stdout, expected)
    return label


def parameter_certificate(G0, G20, multiplier):
    program = "\n".join(
        (
            "ring K=(0,A,R,D),(h2,rho,z),dp;",
            "option(redSB);",
            "ideal P="
            + ",".join(map(singular_text, (G0, G20, z * multiplier - 1)))
            + ";",
            "P=std(P);",
            'print("RESULT:"+string(reduce(1,P)!=0)+":"+string(dim(P)));',
            "quit;",
        )
    )
    return run_singular("parameter", program, "RESULT:1:0")


def incidence_certificate(G0, G20, multiplier):
    mixed, diagonal_a, diagonal_b = finite_d23_model()
    equations = (
        *mixed,
        diagonal_a - 1,
        w * diagonal_b - 1,
        G0,
        G20,
        z * multiplier - 1,
    )
    variables = x + (h2, rho, w, z)
    program = "\n".join(
        (
            "ring K=(0,A,R,D),(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + ";",
            "I=slimgb(I); ideal J=std(I);",
            'print("RESULT:"+string(reduce(1,J)==0)+":"+string(size(J)));',
            "quit;",
        )
    )
    return run_singular("incidence", program, "RESULT:1:1")


def main():
    G0, G20, multiplier = residual_data()
    parameter = parameter_certificate(G0, G20, multiplier)
    incidence = incidence_certificate(G0, G20, multiplier)
    replay = subprocess.run(
        (sys.executable, str(PRIMARY)),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=360,
        check=False,
    )
    assert replay.returncode == 0, (replay.stdout, replay.stderr)
    assert json.loads(replay.stdout)["status"] == "pass"
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "repository_imports_used": False,
                "parameter_residual_certificate": parameter,
                "parameter_residual_dimension": 0,
                "binary_incidence_certificate": incidence,
                "primary_replay": "pass",
                "refined_residual_binary_empty": True,
                "finite_field_proof_used": False,
                "generic_weighted_H22_fibre_closed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
