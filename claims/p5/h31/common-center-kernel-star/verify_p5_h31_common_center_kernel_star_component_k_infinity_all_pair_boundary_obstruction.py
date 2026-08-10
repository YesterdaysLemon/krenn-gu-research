#!/usr/bin/env python3
"""Close marked H31 on component 23's normalized k=infinity all-pair boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_K_INFINITY_"
    "ALL_PAIR_BOUNDARY_OBSTRUCTION.md"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
ROW_SETS = {
    (0, 0): (0, 1, 3, 7),
    (0, 1): (0, 1, 2, 7),
    (1, 0): (0, 1, 3, 7),
    (1, 1): (0, 1, 2, 7),
}

r, reciprocal_k, t, localizer = sp.symbols("r q t v")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
inverse = sp.Symbol("u")
p, w = sp.symbols("p w")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def boundary_rows():
    return (
        (
            A,
            D,
            add(A, scale(-1, C), B, scale(r, D)),
            add(scale(-1, A), scale(-1, C), B, scale(r, D)),
        ),
        (B, add(B, C), C, C),
    )


def marked_rows(alpha, beta, shifts=h):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def q_chart_certificate():
    alpha = (
        A,
        add(scale(reciprocal_k, A), D),
        add(A, scale(-1, C), B, scale(r, D)),
        add(scale(-1, A), scale(-1, C), B, scale(t, D)),
    )
    beta = (B, add(B, C), C, C)
    coefficients = {
        word: sp.factor(
            permanent(
                tuple(
                    alpha[index] if word[index] == 0 else beta[index]
                    for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    expected = {
        (0, 0, 0, 0): -4 * (t - r + reciprocal_k * (r * t - 1)),
        (1, 1, 1, 1): -4,
    }
    assert all(
        sp.factor(coefficients[word] - expected.get(word, 0)) == 0 for word in WORDS
    )
    return str(expected[(0, 0, 0, 0)])


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(symmetric_product(left[i], right[j]) for i in range(2) for j in range(2))
    )


def pair_certificate(alpha, beta):
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    matrices = tuple(pair_matrix(planes[left], planes[right]) for left, right in PAIRS)
    profile = tuple(matrix.rank() for matrix in matrices)
    assert profile == (3, 3, 3, 4, 4, 3)
    minors = []
    for rows in itertools.combinations(range(6), 3):
        for columns in itertools.combinations(range(4), 3):
            determinant = sp.factor(matrices[-1].extract(rows, columns).det())
            if determinant != 0:
                minors.append(determinant)
    gcd = sp.factor(sp.gcd_list(minors))
    assert sp.factor(gcd - 4 * (r - 1) * (r + 1)) == 0
    endpoints = tuple(
        tuple(matrix.subs(r, value).rank() for matrix in matrices) for value in (1, -1)
    )
    assert endpoints == ((3, 3, 3, 4, 4, 2), (3, 3, 3, 4, 4, 2))
    return profile, str(gcd), endpoints


def wedge(plane):
    return sp.Matrix(
        [
            sp.factor(plane[0, i] * plane[1, j] - plane[0, j] * plane[1, i])
            for i, j in PAIRS
        ]
    )


def component22_rows(A_parameter, R_parameter, D_parameter):
    u = (1 - D_parameter) / 2
    v = (1 + D_parameter) / 2
    G = -(2 * A_parameter + R_parameter) / 2
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = (2 * A_parameter, 0, 1, 1)
    mr = add(m, scale(R_parameter, c))
    d = (G, G, u, v)
    y0 = (0, D_parameter * (2 * A_parameter + R_parameter), -u, v)
    x0 = (-A_parameter * v, A_parameter * (u + 1) + R_parameter, 1, 0)
    return (y0, m, mr, c), (x0, a, a, d)


def component_placement(alpha, beta):
    old_planes = tuple(
        sp.Matrix.vstack(sp.Matrix(alpha[index]).T, sp.Matrix(beta[index]).T)
        for index in range(4)
    )
    swap01 = sp.Matrix(((0, 1, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
    source = sp.diag(1, -1, 1 / (r + 1), 1 / (1 - r)) * swap01
    transformed = tuple(old_planes[index] * source for index in (1, 2, 3, 0))
    component_alpha, component_beta = component22_rows(-1, 2, r)
    component_planes = tuple(
        sp.Matrix.vstack(
            sp.Matrix(component_alpha[index]).T, sp.Matrix(component_beta[index]).T
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
    assert component22_rows(-1, 2, 0)[0][0][1] == 0
    return tuple(map(str, factors))


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def run_singular(label, program, expected):
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=360,
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


def projection_data(distinguished, alpha, beta):
    marked = marked_rows(alpha, beta)
    mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
    vector = sp.Matrix(x)
    equations = (
        *tuple(mixed * vector),
        (diagonal0 * vector)[0] - 1,
        inverse * (diagonal1 * vector)[0] - 1,
        localizer * (r**2 - 1) - 1,
    )
    eliminated = x + (inverse,)
    variables = eliminated + (r, localizer) + h
    lines = [
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(6));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_text(value) for value in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    if distinguished in (0, 1):
        other_zero = "h2" if distinguished == 0 else "h3"
        branch_variable = "h3" if distinguished == 0 else "h2"
        common = f"v*(r^2-1)-1,h0,{other_zero}"
        lines.extend(
            (
                f"ideal B0={common},{branch_variable},4*r*h1-r^2-3; B0=std(B0);",
                f"ideal B1={common},2*{branch_variable}+1,r*h1-1; B1=std(B1);",
                "ideal E=std(intersect(B0,B1));",
            )
        )
        expected_size = 8
    else:
        lines.append("ideal E=1; E=std(E);")
        expected_size = 1
    lines.extend(
        (
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "ideal Z=std(J,r);",
            (
                'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"'
                '+string(size(J))+":"+string(reduce(1,Z)==0));'
            ),
            "quit;",
        )
    )
    run_singular(
        f"localized insertion {distinguished}",
        "\n".join(lines),
        f"RESULT:1:{expected_size}:1",
    )
    return {
        "insertion": distinguished,
        "localized_projection": "two-branch intersection"
        if distinguished in (0, 1)
        else "unit ideal",
        "r_zero_fibre_unit_from_localized_ideal": True,
    }


def direct_r_zero_certificate(distinguished, alpha, beta):
    marked = marked_rows(alpha, beta)
    mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
    vector = sp.Matrix(x)
    equations = (
        *tuple((mixed * vector).subs(r, 0)),
        ((diagonal0 * vector)[0] - 1).subs(r, 0),
        (inverse * (diagonal1 * vector)[0] - 1).subs(r, 0),
    )
    eliminated = x + (inverse,)
    variables = eliminated + h
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(singular_text(value) for value in equations) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            'print("RESULT:"+string(reduce(1,J)==0)+":"+string(size(J)));',
            "quit;",
        )
    )
    run_singular(f"r=0 insertion {distinguished}", program, "RESULT:1:1")
    return distinguished


def branch_data(alpha, beta):
    delta = r**2 - 1
    cases = (
        {
            "name": "J00",
            "insertion": 0,
            "marking": (0, (r**2 + 3) / (4 * r), 0, 0),
            "frame": (
                (0, -4 * r / delta, -2, -2, -4 / delta, 1, 0, 0),
                (1, 4 * r / delta, 2, 0, 4 / delta, 0, 1, 1),
            ),
            "diagonals": (16 * r * (p - w), -4 * w),
            "rank_rows": (0, 1, 3, 7, 11, 13),
            "rank_columns": (0, 1, 2, 3, 4, 6),
            "rank_minor": -32 * r**2 * delta**2,
            "determinant": -r,
            "power": (1, 2),
            "pure": -4 * r,
        },
        {
            "name": "J01",
            "insertion": 0,
            "marking": (0, 1 / r, 0, -sp.Rational(1, 2)),
            "frame": (
                (1, -2 * r / delta, -2, -2, -2 / delta, 1, 1, 0),
                (0, r / delta, 1, 0, 1 / delta, 0, 0, 1),
            ),
            "diagonals": (4 * r * (2 * p - w), -2 * w),
            "rank_rows": (0, 1, 3, 7, 11, 13),
            "rank_columns": (0, 1, 2, 3, 4, 5),
            "rank_minor": 128 * r**2 * delta**2,
            "determinant": -sp.Rational(1, 2),
            "power": (2, 1),
            "pure": -4 * r,
        },
        {
            "name": "J10",
            "insertion": 1,
            "marking": (0, (r**2 + 3) / (4 * r), 0, 0),
            "frame": (
                (0, -4 * r / delta, -2, -2, -4 / delta, 1, 0, 0),
                (-1, 4 * r / delta, 0, 2, 4 / delta, 0, 1, 1),
            ),
            "diagonals": (16 * r * (p - w), 4 * w),
            "rank_rows": (0, 1, 3, 7, 11, 12),
            "rank_columns": (0, 1, 2, 3, 4, 6),
            "rank_minor": 32 * r**2 * delta**2,
            "determinant": r,
            "power": (1, 2),
            "pure": 4 * r,
        },
        {
            "name": "J11",
            "insertion": 1,
            "marking": (0, 1 / r, -sp.Rational(1, 2), 0),
            "frame": (
                (0, r / delta, 0, 1, 1 / delta, 0, 1, 0),
                (-1, -2 * r / delta, -2, -2, -2 / delta, 1, 0, 1),
            ),
            "diagonals": (-4 * r * (p - 2 * w), 2 * p),
            "rank_rows": (0, 1, 3, 7, 11, 12),
            "rank_columns": (0, 1, 2, 3, 4, 5),
            "rank_minor": 128 * r**2 * delta**2,
            "determinant": sp.Rational(1, 2),
            "power": (2, 1),
            "pure": 4 * r,
        },
    )
    output = []
    for case in cases:
        marked = marked_rows(alpha, beta, case["marking"])
        mixed, diagonal0, diagonal1 = mixed_matrix(case["insertion"], alpha, marked)
        frame = tuple(sp.Matrix(entries) for entries in case["frame"])
        assert mixed.rank() == 6
        assert sp.Matrix.hstack(*frame).rank() == 2
        assert all(
            all(sp.factor(value) == 0 for value in mixed * vector) for vector in frame
        )
        rank_minor = sp.factor(
            mixed.extract(case["rank_rows"], case["rank_columns"]).det()
        )
        assert sp.factor(rank_minor - case["rank_minor"]) == 0
        extension = frame[0] * p + frame[1] * w
        observed_diagonals = (
            sp.factor((diagonal0 * extension)[0]),
            sp.factor((diagonal1 * extension)[0]),
        )
        assert all(
            sp.factor(observed - expected) == 0
            for observed, expected in zip(observed_diagonals, case["diagonals"])
        )
        one_marked = marked_extension(case["insertion"], extension, alpha, marked, 0)
        determinant = sp.factor(
            one_marked.extract(
                ROW_SETS[(case["insertion"], int(case["name"][-1]))], range(4)
            ).det()
        )
        expected_determinant = sp.factor(
            case["determinant"]
            * observed_diagonals[0] ** case["power"][0]
            * observed_diagonals[1] ** case["power"][1]
        )
        assert sp.factor(determinant - expected_determinant) == 0
        pure_map = one_marked_map(0, alpha, marked)
        assert sp.factor(pure_map[0, case["insertion"]] - case["pure"]) == 0
        output.append(
            {
                "branch": case["name"],
                "insertion": case["insertion"],
                "marking": list(map(str, case["marking"])),
                "mixed_rank": 6,
                "kernel_dimension": 2,
                "rank_minor": str(rank_minor),
                "diagonals": list(map(str, observed_diagonals)),
                "minor_rows": "".join(
                    map(str, ROW_SETS[(case["insertion"], int(case["name"][-1]))])
                ),
                "minor": str(expected_determinant),
                "pure_transverse": str(case["pure"]),
            }
        )
    return output


def main():
    pure_q_chart = q_chart_certificate()
    alpha, beta = boundary_rows()
    boundary_coefficients = {
        word: sp.factor(
            permanent(
                tuple(
                    alpha[index] if word[index] == 0 else beta[index]
                    for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert boundary_coefficients[(1, 1, 1, 1)] == -4
    assert all(
        value == 0
        for word, value in boundary_coefficients.items()
        if word != (1, 1, 1, 1)
    )
    assert all(sp.Matrix((alpha[index], beta[index])).rank() == 2 for index in range(4))

    profile, pair_gcd, endpoint_profiles = pair_certificate(alpha, beta)
    placement_factors = component_placement(alpha, beta)
    projections = tuple(projection_data(index, alpha, beta) for index in range(4))
    r_zero = tuple(direct_r_zero_certificate(index, alpha, beta) for index in range(4))
    branches = branch_data(alpha, beta)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "component_boundary": "k=infinity",
                "pure_q_chart_equation": pure_q_chart,
                "boundary_equation": "q=0,t=r",
                "base_ring": "Q[r,1/((r-1)*(r+1))]",
                "pair_profile": profile,
                "edge23_maximal_minor_gcd": pair_gcd,
                "r_plus_minus_one_profiles": endpoint_profiles,
                "component22_parameters": {"A": -1, "R": 2, "D": "r"},
                "component22_wedge_factors": placement_factors,
                "r_zero_placement": "component 13 equal-complement intersection",
                "localized_projections": projections,
                "direct_r_zero_unit_insertions": r_zero,
                "surviving_branches": branches,
                "projective_extension_normalization_complete": True,
                "projective_marking_endpoint_is_not_a_basis": True,
                "normalized_all_pair_marked_H31_boundary_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
