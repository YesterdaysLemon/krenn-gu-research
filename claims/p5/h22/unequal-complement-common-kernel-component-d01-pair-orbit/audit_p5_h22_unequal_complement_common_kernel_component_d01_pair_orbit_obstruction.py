#!/usr/bin/env python3
"""Independent rational audit of the component-22 finite-D01 H22 cover."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D01_PAIR_ORBIT_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h22_unequal_complement_common_kernel_component_d01_pair_orbit_obstruction.py"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def component_rows():
    A = R = 1
    D = 2
    u0 = sp.Rational(1 - D, 2)
    v0 = sp.Rational(1 + D, 2)
    G = sp.Rational(-(2 * A + R), 2)
    alpha = (
        (0, D * (2 * A + R), -u0, v0),
        (2 * A, 0, 1, 1),
        (2 * A + R, -R, 1, 1),
        (1, -1, 0, 0),
    )
    beta = (
        (-A * v0, A * (u0 + 1) + R, 1, 0),
        (1, 1, 0, 0),
        (1, 1, 0, 0),
        (G, G, u0, v0),
    )
    return alpha, beta


def marked_rows(alpha, beta, marking):
    return tuple(
        tuple(beta[i][j] + marking[i] * alpha[i][j] for j in range(4))
        for i in range(4)
    )


def projected(rows, extensions, rho):
    return tuple(
        (rho * rows[i][0] + rows[i][1], rows[i][2], rows[i][3], extensions[i])
        for i in range(4)
    )


def one_marked(mode, alpha, beta):
    result = []
    for bits in BITS3:
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(
                permanent(
                    tuple(basis if other == mode else selected[other] for other in range(4))
                )
            )
        result.append(row)
    return sp.Matrix(result)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def specialized_unit(label, rho, marking, minors):
    z = sp.symbols("z0:8")
    inverse = sp.Symbol("u")
    alpha, canonical = component_rows()
    beta = marked_rows(alpha, canonical, marking)
    alpha_p = projected(alpha, z[:4], rho)
    beta_p = projected(beta, z[4:], rho)
    tensor = {
        bits: permanent(tuple(beta_p[i] if bits[i] else alpha_p[i] for i in range(4)))
        for bits in BITS4
    }
    equations = [
        *(tensor[bits] for bits in BITS4 if bits not in (BITS4[0], BITS4[-1])),
        tensor[BITS4[0]] - 1,
        inverse * tensor[BITS4[-1]] - 1,
    ]
    lines = ["ring R=0,(" + ",".join(map(str, z + (inverse,))) + "),dp;"]
    minor_names = []
    for index, (mode, rows) in enumerate(minors):
        matrix = one_marked(mode, alpha_p, beta_p).extract(rows, range(4))
        lines.extend(
            (
                f"matrix N{index}[4][4]=" + ",".join(sg(value) for value in matrix) + ";",
                f"poly f{index}=det(N{index});",
            )
        )
        minor_names.append(f"f{index}")
    lines.extend(
        (
            "ideal I=" + ",".join((*[sg(value) for value in equations], *minor_names)) + ";",
            "I=slimgb(I);",
            '"RESULT:"+string(reduce(1,I)==0)+":"+string(size(I));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), text=True, capture_output=True, timeout=30, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (label, completed.stdout, completed.stderr)
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:1"], (label, completed.stdout)
    return {"label": label, "rho": str(rho), "marking": list(map(str, marking)), "unit_ideal": True}


def main():
    theorem = THEOREM.read_text(encoding="utf-8")
    primary = PRIMARY.read_text(encoding="utf-8")
    for phrase in (
        "does **not** close the full generic weighted-`H22` fibre",
        "second pair orbit remains **UNKNOWN**",
        "timed out and is not theorem evidence",
    ):
        assert phrase in theorem
    assert '"complementary_D23_pair_orbit_closed": False' in primary
    cases = (
        specialized_unit(
            "P1",
            2,
            (sp.Rational(-1, 2), sp.Rational(-3, 4), 0, sp.Rational(3, 2)),
            ((0, (0, 1, 3, 7)), (3, (0, 1, 2, 7))),
        ),
        specialized_unit(
            "P2",
            2,
            (sp.Rational(-1, 2), 0, sp.Rational(-3, 5), sp.Rational(3, 2)),
            ((3, (0, 1, 2, 7)), (2, (0, 1, 5, 7))),
        ),
        specialized_unit(
            "P3a",
            -2,
            (1, 0, 0, -1),
            ((0, (0, 1, 3, 7)), (3, (0, 1, 3, 7))),
        ),
        specialized_unit(
            "P3b",
            3,
            (0, 0, 0, 1),
            ((0, (0, 1, 3, 7)), (3, (0, 1, 3, 7))),
        ),
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import rational audit",
                "field": "Q",
                "cases": cases,
                "complementary_D23_pair_orbit_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
