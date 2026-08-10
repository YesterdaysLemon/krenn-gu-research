#!/usr/bin/env python3
"""Close component 23's normalized k=infinity all-pair H22 boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
)



ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_K_INFINITY_"
    "ALL_PAIR_BOUNDARY_OBSTRUCTION.md"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
COORDINATE_PAIRS = PAIRS

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


def permanent4(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
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


def marked_rows(alpha, beta):
    return tuple(add(beta[index], scale(h[index], alpha[index])) for index in range(4))


def symmetric_product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in COORDINATE_PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(symmetric_product(left[i], right[j]) for i in range(2) for j in range(2))
    )


def wedge(plane):
    return sp.Matrix(
        [
            sp.factor(plane[0, i] * plane[1, j] - plane[0, j] * plane[1, i])
            for i, j in COORDINATE_PAIRS
        ]
    )


def q_chart_certificate():
    alpha_q = (
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
                    alpha_q[index] if word[index] == 0 else beta[index]
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
    return expected[(0, 0, 0, 0)]


def pair_certificate(alpha, beta):
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    matrices = tuple(pair_matrix(planes[left], planes[right]) for left, right in PAIRS)
    profile = tuple(matrix.rank() for matrix in matrices)
    assert profile == (3, 3, 3, 4, 4, 3)

    edge23 = matrices[-1]
    maximal_minors = []
    for rows in itertools.combinations(range(6), 3):
        for columns in itertools.combinations(range(4), 3):
            determinant = sp.factor(edge23.extract(rows, columns).det())
            if determinant != 0:
                maximal_minors.append(determinant)
    gcd = sp.factor(sp.gcd_list(maximal_minors))
    assert sp.factor(gcd - 4 * (r - 1) * (r + 1)) == 0
    special_profiles = tuple(
        tuple(matrix.subs(r, value).rank() for matrix in matrices) for value in (1, -1)
    )
    assert special_profiles == (
        (3, 3, 3, 4, 4, 2),
        (3, 3, 3, 4, 4, 2),
    )

    relation_ranks = []
    for edge_index in (0, 1, 2, 5):
        kernel = matrices[edge_index].subs(r, 2).nullspace()
        assert len(kernel) == 1
        relation_ranks.append(sp.Matrix(2, 2, list(kernel[0])).rank())
    assert tuple(relation_ranks) == (1, 1, 1, 2)
    return profile, gcd, special_profiles, tuple(relation_ranks)


def component_placement(alpha, beta):
    old_planes = tuple(
        sp.Matrix.vstack(sp.Matrix(alpha[index]).T, sp.Matrix(beta[index]).T)
        for index in range(4)
    )
    swap01 = sp.Matrix(((0, 1, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
    source = sp.diag(1, -1, 1 / (r + 1), 1 / (1 - r)) * swap01
    transformed = tuple(old_planes[index] * source for index in (1, 2, 3, 0))

    component_alpha, component_beta = component_rows(-1, 2, r)
    component_planes = tuple(
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
    for observed, expected, factor in zip(transformed, component_planes, factors):
        assert all(
            sp.factor(left - factor * right) == 0
            for left, right in zip(wedge(observed), wedge(expected))
        )
    assert 2 * (-1) + 2 == 0
    return tuple(map(str, factors))


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


def run_singular(label, program, expected_marker):
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
    assert markers == [expected_marker], (label, completed.stdout, expected_marker)
    return label


def module_certificate(alpha, beta, chart, slope, expected, marker):
    marked = marked_rows(alpha, beta)
    models = tuple(
        build_model(alpha, marked, x, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    generators = tuple(
        coefficient_vector(expression)
        for model in models
        for expression in model["mixed"]
    )
    diagonals = tuple(
        coefficient_vector(expression)
        for model in models
        for expression in (model["A"], model["B"])
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
    return run_singular(chart, program, marker)


def main():
    pure_equation = q_chart_certificate()
    alpha, beta = boundary_rows()
    profile, pair_gcd, special_profiles, relation_ranks = pair_certificate(alpha, beta)
    wedge_factors = component_placement(alpha, beta)

    finite = module_certificate(
        alpha,
        beta,
        "finite",
        lam,
        FINITE_EXPECTED,
        "RESULT:1:27:0:1:1:0",
    )
    coordinate_module = tuple(f"gen({index})" for index in range(1, 9))
    projective = module_certificate(
        alpha,
        beta,
        "infinity",
        None,
        coordinate_module,
        "RESULT:1:8:1:1:1:1",
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "component_boundary": "k=infinity",
                "pure_q_chart_equation": str(pure_equation),
                "boundary_equation": "q=0, t=r",
                "base_ring": "Q[r,1/((r-1)*(r+1))]",
                "pair_profile": profile,
                "edge23_maximal_minor_gcd": str(pair_gcd),
                "r_plus_minus_one_profiles": special_profiles,
                "rank_three_relation_ranks_01_02_03_23": relation_ranks,
                "component22_parameters": {"A": -1, "R": 2, "D": "r"},
                "component22_wedge_factors": wedge_factors,
                "component22_special_parameter": "2*A+R=0",
                "r_zero_placement": "component 13 equal-complement intersection",
                "r_plus_minus_one_placement": "lower-pair",
                "finite_module_certificate": finite,
                "finite_module_bidirectional_equality": True,
                "finite_module_basis_size": len(FINITE_EXPECTED),
                "finite_diagonal_order": ["A01", "B01", "A23", "B23"],
                "finite_diagonal_membership": [False, True, True, False],
                "projective_module_certificate": projective,
                "projective_module_bidirectional_equality": True,
                "projective_module_is_full": True,
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
