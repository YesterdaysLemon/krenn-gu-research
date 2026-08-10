#!/usr/bin/env python3
"""No-import audit of component 23's k=infinity all-pair H22 theorem."""

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
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_K_INFINITY_"
    "ALL_PAIR_BOUNDARY_OBSTRUCTION.md"
)
PRIMARY = ROOT / (
    "verify_p5_h22_common_center_kernel_star_component_k_infinity_"
    "all_pair_boundary_obstruction.py"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))

r, q, t, lam, u = sp.symbols("r q t lam u")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def permanent4(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS4
        )
    )


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


def build_model(alpha, beta, direction, chart, slope=None):
    alpha_rows = tuple(
        project(alpha[index], x[index], direction, chart, slope) for index in range(4)
    )
    beta_rows = tuple(
        project(beta[index], x[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        rows = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
        )
        coefficients[word] = sp.expand(
            sum(
                rows[index][3]
                * permanent3(
                    tuple(rows[other][:3] for other in range(4) if other != index)
                )
                for index in range(4)
            )
        )
    return (
        tuple(coefficients[word] for word in MIXED),
        coefficients[WORDS[0]],
        coefficients[WORDS[-1]],
    )


def boundary_rows():
    alpha = (
        A,
        D,
        add(A, scale(-1, C), B, scale(r, D)),
        add(scale(-1, A), scale(-1, C), B, scale(r, D)),
    )
    beta = (B, add(B, C), C, C)
    return alpha, beta


def q_chart_audit():
    alpha = (
        A,
        add(scale(q, A), D),
        add(A, scale(-1, C), B, scale(r, D)),
        add(scale(-1, A), scale(-1, C), B, scale(t, D)),
    )
    beta = (B, add(B, C), C, C)
    coefficients = {
        word: sp.factor(
            permanent4(
                [
                    alpha[index] if word[index] == 0 else beta[index]
                    for index in range(4)
                ]
            )
        )
        for word in WORDS
    }
    expected = {
        (0, 0, 0, 0): -4 * (t - r + q * (r * t - 1)),
        (1, 1, 1, 1): -4,
    }
    assert all(
        sp.factor(coefficients[word] - expected.get(word, 0)) == 0 for word in WORDS
    )


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_audit(alpha, beta):
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    matrices = tuple(
        sp.Matrix.hstack(
            *(
                symmetric_product(planes[left][i], planes[right][j])
                for i in range(2)
                for j in range(2)
            )
        )
        for left, right in PAIRS
    )
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 4, 4, 3)
    edge23_minors = tuple(
        determinant
        for rows in itertools.combinations(range(6), 3)
        for columns in itertools.combinations(range(4), 3)
        if (determinant := sp.factor(matrices[-1].extract(rows, columns).det())) != 0
    )
    assert sp.factor(sp.gcd_list(edge23_minors) - 4 * (r - 1) * (r + 1)) == 0
    for value in (1, -1):
        assert tuple(matrix.subs(r, value).rank() for matrix in matrices) == (
            3,
            3,
            3,
            4,
            4,
            2,
        )


def wedge(plane):
    return sp.Matrix(
        [
            sp.factor(plane[0, i] * plane[1, j] - plane[0, j] * plane[1, i])
            for i, j in PAIRS
        ]
    )


def component22_rows():
    component_a = (1, 1, 0, 0)
    component_c = (1, -1, 0, 0)
    component_A = sp.Integer(-1)
    component_R = sp.Integer(2)
    component_D = r
    direction_u = (1 - component_D) / 2
    direction_v = (1 + component_D) / 2
    component_G = -(2 * component_A + component_R) / 2
    m = (2 * component_A, 0, 1, 1)
    mr = add(m, scale(component_R, component_c))
    d = (component_G, component_G, direction_u, direction_v)
    y0 = (
        0,
        component_D * (2 * component_A + component_R),
        -direction_u,
        direction_v,
    )
    x0 = (
        -component_A * direction_v,
        component_A * (direction_u + 1) + component_R,
        1,
        0,
    )
    return (y0, m, mr, component_c), (x0, component_a, component_a, d)


def placement_audit(alpha, beta):
    planes = tuple(
        sp.Matrix.vstack(sp.Matrix(alpha[index]).T, sp.Matrix(beta[index]).T)
        for index in range(4)
    )
    swap01 = sp.Matrix(((0, 1, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
    source = sp.diag(1, -1, 1 / (r + 1), 1 / (1 - r)) * swap01
    observed = tuple(planes[index] * source for index in (1, 2, 3, 0))
    component_alpha, component_beta = component22_rows()
    expected = tuple(
        sp.Matrix.vstack(
            sp.Matrix(component_alpha[index]).T,
            sp.Matrix(component_beta[index]).T,
        )
        for index in range(4)
    )
    factors = (
        4 / ((r - 1) * (r + 1) ** 2),
        sp.Integer(1),
        sp.Integer(1),
        2 / ((r - 1) * (r + 1)),
    )
    assert all(
        sp.factor(left - factor * right) == 0
        for observed_plane, expected_plane, factor in zip(observed, expected, factors)
        for left, right in zip(wedge(observed_plane), wedge(expected_plane))
    )


FINITE_EXPECTED = (
    "gen(1)",
    "gen(4)-gen(3)",
    "gen(7)",
    "gen(8)",
    "lam*gen(5)+lam*gen(2)-gen(5)+gen(2)",
    "2*lam*gen(6)+lam*gen(3)-2*gen(6)-gen(3)",
    "h3*gen(2)",
    "h3*gen(3)",
    "h3*gen(6)",
    "h2*gen(2)",
    "h2*gen(3)",
    "h2*gen(6)",
    "h1*gen(2)+lam*gen(3)-gen(6)-gen(2)",
    "h0*gen(2)",
    "h0*gen(3)",
    "h0*gen(6)",
    "4*u*gen(6)-4*u*gen(3)-3*lam*gen(3)+4*gen(6)-gen(3)+3*gen(2)",
    "r*gen(2)+lam*gen(3)-gen(3)-gen(2)",
    "lam^2*gen(3)-2*lam*gen(2)-gen(3)",
    "3*h1*lam*gen(3)-r*gen(6)+r*gen(3)-3*h1*gen(3)+3*lam*gen(3)-3*gen(6)",
    "4*u*lam*gen(2)+lam^2*gen(2)+2*lam*gen(2)+gen(2)",
    "2*u*lam*gen(3)-2*u*gen(3)+lam*gen(2)+gen(2)",
    "3*r*lam*gen(3)-4*r*gen(6)+r*gen(3)+3*lam*gen(3)-3*gen(3)",
    "2*r*u*gen(3)-2*u*h1*gen(3)-r*gen(6)-2*h1*gen(3)",
    "r^2*gen(3)+4*r*h1*gen(6)-2*r*h1*gen(3)-4*gen(6)+gen(3)",
    "r^2*gen(6)+2*r*h1*gen(3)-gen(6)-2*gen(3)",
    "2*u*h1^2*gen(3)+r*h1*gen(6)+2*h1^2*gen(3)-2*u*gen(3)+gen(6)",
)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def coefficient_vector(expression):
    return (
        "["
        + ",".join(singular_text(sp.diff(expression, variable)) for variable in x)
        + "]"
    )


def module_audit(alpha, beta, chart, slope, expected, marker):
    marked = tuple(
        add(beta[index], scale(h[index], alpha[index])) for index in range(4)
    )
    models = tuple(
        build_model(alpha, marked, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    generators = tuple(
        coefficient_vector(expression)
        for mixed, _diagonal_a, _diagonal_b in models
        for expression in mixed
    )
    diagonals = tuple(
        coefficient_vector(expression)
        for _mixed, diagonal_a, diagonal_b in models
        for expression in (diagonal_a, diagonal_b)
    )
    variables = (r, u, *h) + ((lam,) if chart == "finite" else ())
    program = "\n".join(
        (
            "ring P=0,(" + ",".join(map(str, variables)) + "),dp;",
            "ideal Q=u*(r-1)*(r+1)-1; Q=std(Q);",
            "qring R=Q;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
            "module E=" + ",".join(expected) + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2);",
            "module EM=simplify(reduce(E,M),2);",
            *(f"vector d{index}={value};" for index, value in enumerate(diagonals)),
            "int sameModule=(size(ME)==0)&&(size(EM)==0);",
            *(f"int diagonal{index}=reduce(d{index},M)==0;" for index in range(4)),
            (
                'print("RESULT:"+string(sameModule)+":"+string(size(M))+":"'
                '+string(diagonal0)+":"+string(diagonal1)+":"'
                '+string(diagonal2)+":"+string(diagonal3));'
            ),
            "quit;",
        )
    )
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
        chart,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [marker], (chart, completed.stdout, marker)


def replay_primary():
    completed = subprocess.run(
        (sys.executable, str(PRIMARY)),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=600,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    result = json.loads(completed.stdout)
    assert result["status"] == "pass"
    assert result["finite_module_bidirectional_equality"] is True
    assert result["finite_diagonal_membership"] == [False, True, True, False]
    assert result["projective_module_bidirectional_equality"] is True
    assert result["projective_module_is_full"] is True
    assert result["theorem_sha256"] == hashlib.sha256(NOTE.read_bytes()).hexdigest()
    return result


def main():
    q_chart_audit()
    alpha, beta = boundary_rows()
    pair_audit(alpha, beta)
    placement_audit(alpha, beta)
    module_audit(
        alpha,
        beta,
        "finite",
        lam,
        FINITE_EXPECTED,
        "RESULT:1:27:0:1:1:0",
    )
    module_audit(
        alpha,
        beta,
        "infinity",
        None,
        tuple(f"gen({index})" for index in range(1, 9)),
        "RESULT:1:8:1:1:1:1",
    )
    primary = replay_primary()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "audit_style": "no repository imports; independent reconstruction",
                "pure_q_chart_rebuilt": True,
                "pair_locus_rebuilt": True,
                "component22_mapping_rebuilt": True,
                "finite_module_bidirectional_equality_rebuilt": True,
                "finite_diagonal_order": ["A01", "B01", "A23", "B23"],
                "finite_diagonal_membership": [False, True, True, False],
                "projective_full_module_rebuilt": True,
                "primary_replayed": primary["status"] == "pass",
                "normalized_all_pair_weighted_H22_boundary_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
