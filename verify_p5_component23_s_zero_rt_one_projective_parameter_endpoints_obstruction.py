#!/usr/bin/env python3
"""Close component 23's s=0, rt=1 projective parameter endpoints."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

import sys
from pathlib import Path

for _repo_parent in Path(__file__).resolve().parents:
    if (_repo_parent / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_repo_parent / "src"))
        break
else:
    raise RuntimeError("could not locate repository src directory")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model
REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star")

from verify_p5_h22_common_center_kernel_star_component_partial import singular_command
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
    permanent,
)



WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS5 = tuple(itertools.permutations(range(5)))

h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
k, lam, p, u, w = sp.symbols("k lam p u w")
c = sp.symbols("c0:4")

A = (sp.Integer(1), 1, 0, 0)
C = (sp.Integer(1), -1, 0, 0)
B = (0, 0, sp.Integer(1), 1)
D = (0, 0, sp.Integer(1), -1)


def add(left, right, coefficient=1):
    return tuple(
        sp.expand(left[index] + coefficient * right[index]) for index in range(4)
    )


def endpoint_rows(endpoint):
    if endpoint == "r_infinity":
        alpha = (A, add(A, D, k), D, B)
    elif endpoint == "t_infinity":
        alpha = (A, add(A, D, k), B, D)
    else:
        raise ValueError(endpoint)
    return alpha, (B, B, C, C)


def shifted_beta(alpha, beta, marking):
    return tuple(add(beta[index], alpha[index], marking[index]) for index in range(4))


def symmetric_product(left, right):
    return sp.Matrix(
        [
            left[first] * right[second] + left[second] * right[first]
            for first, second in PAIRS
        ]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(
            symmetric_product(left_row, right_row)
            for left_row in left
            for right_row in right
        )
    )


def permanent5(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(5))
            for permutation in PERMUTATIONS5
        )
    )


def geometry_certificate(endpoint):
    alpha, beta = endpoint_rows(endpoint)
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    profile = tuple(
        pair_matrix(planes[left], planes[right]).rank() for left, right in PAIRS
    )
    zero_planes = tuple(
        tuple(tuple(sp.sympify(entry).subs(k, 0) for entry in row) for row in plane)
        for plane in planes
    )
    zero_profile = tuple(
        pair_matrix(zero_planes[left], zero_planes[right]).rank()
        for left, right in PAIRS
    )
    expected = {
        "r_infinity": ((3, 2, 3, 3, 4, 3), (3, 2, 3, 2, 3, 3)),
        "t_infinity": ((3, 3, 2, 4, 3, 3), (3, 3, 2, 3, 2, 3)),
    }[endpoint]
    assert (profile, zero_profile) == expected
    coefficients = {
        word: sp.factor(
            permanent(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert coefficients[(1, 1, 1, 1)] == -4
    assert all(value == 0 for word, value in coefficients.items() if word != WORDS[-1])
    projective_markings = tuple(
        coefficients[tuple(0 if index == mode else 1 for index in range(4))]
        for mode in range(4)
    )
    assert projective_markings == (0, 0, 0, 0)
    assert all(sp.Matrix(plane).rank() == 2 for plane in planes)
    # The finite face tends to the two endpoint formulas after the stated row
    # rescalings.
    r, t = sp.symbols("r t")
    affine_alpha2 = add(B, D, r)
    affine_alpha3 = add(B, D, t)
    assert tuple(sp.limit(entry / r, r, sp.oo) for entry in affine_alpha2) == D
    assert (
        tuple(
            sp.limit(sp.sympify(entry).subs(t, 1 / r), r, sp.oo)
            for entry in affine_alpha3
        )
        == B
    )
    assert (
        tuple(
            sp.limit(sp.sympify(entry).subs(r, 1 / t), t, sp.oo)
            for entry in affine_alpha2
        )
        == B
    )
    assert tuple(sp.limit(entry / t, t, sp.oo) for entry in affine_alpha3) == D
    return {
        "endpoint": endpoint,
        "generic_profile": profile,
        "k_zero_profile": zero_profile,
        "pure": "T1111=-4",
    }


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def run_singular(label, program, expected="RESULT:1", timeout=600):
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
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


def projection_ideal(endpoint, deletion):
    alpha, beta = endpoint_rows(endpoint)
    marked = shifted_beta(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    extension = sp.Matrix(x)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        w * (diagonal_b * extension)[0] - 1,
    )
    if deletion in (0, 1):
        expected = (h[0], h[1], h[2] if endpoint == "r_infinity" else h[3])
    else:
        expected = (h[0], h[1], h[2] * h[3])
    eliminated = x + (w,)
    variables = eliminated + h + (k,)
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(5));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    run_singular(
        f"{endpoint}_h31_projection_d{deletion}",
        program,
        f"RESULT:1:{len(expected)}",
    )
    return tuple(map(str, expected))


def stack(distinguished, extension, alpha, beta, mode):
    neighbour = marked_extension(distinguished, extension, alpha, beta, mode)
    pure = one_marked_map(mode, alpha, beta)
    columns = tuple(index for index in range(4) if index != distinguished) + (4,)
    result = sp.zeros(16, 5)
    for row in range(8):
        for source, column in enumerate(columns):
            result[row, column] = neighbour[row, source]
        for column in range(4):
            result[8 + row, column] = pure[row, column]
    return result


def matrix_declaration(name, matrix):
    return (
        f"matrix {name}[{matrix.rows}][{matrix.cols}]="
        + ",".join(singular_text(entry) for entry in list(matrix))
        + ";"
    )


def maximal_minor_unit(label, matrices, variables, inverse_product, size=5):
    declarations = tuple(
        matrix_declaration(f"M{index}", matrix) for index, matrix in enumerate(matrices)
    )
    minors = ",".join(f"minor(M{index},{size})" for index in range(len(matrices)))
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables + (u,))) + "),dp;",
            "option(redSB);",
            *declarations,
            "ideal I=" + minors + "," + singular_text(u * inverse_product - 1) + ";",
            "I=slimgb(I);",
            "int unit=reduce(1,std(I))==0;",
            '"RESULT:"+string(unit);',
            "quit;",
        )
    )
    run_singular(label, program)
    return label


def h31_d01_lines(endpoint, deletion):
    active_mode = 3 if endpoint == "r_infinity" else 2
    marking = (0, 0, 0, p) if active_mode == 3 else (0, 0, p, 0)
    alpha, beta = endpoint_rows(endpoint)
    marked = shifted_beta(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    assert mixed.rank() == 6
    kernel = mixed.nullspace()
    assert len(kernel) == 2
    c0, c1 = c[:2]
    extension = sp.Matrix.hstack(*kernel) * sp.Matrix((c0, c1))
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    assert actual_a == 2 * c0 * k
    expected_b = (-2 if deletion == 0 else 2) * (c0 * p + 2 * c1)
    assert sp.expand(actual_b - expected_b) == 0
    matrix = stack(deletion, extension, alpha, marked, 0)
    rows = (0, 1, 2, 7, 9 if endpoint == "r_infinity" else 10)
    determinant = sp.factor(matrix.extract(rows, range(5)).det(method="domain-ge"))
    expected_sign = 1 if (endpoint == "r_infinity") == (deletion == 0) else -1
    expected = expected_sign * 16 * c0**2 * k**4 * (c0 * p + 2 * c1)
    assert sp.expand(determinant - expected) == 0
    return {
        "endpoint": endpoint,
        "deletion": deletion,
        "mixed_rank": 6,
        "A": str(actual_a),
        "B": str(actual_b),
        "stack_rows": rows,
        "stack_determinant": str(determinant),
    }


def punctured_marking(endpoint, deletion, active_mode):
    marking = (0, 0, p, 0) if active_mode == 2 else (0, 0, 0, p)
    alpha, beta = endpoint_rows(endpoint)
    marked = shifted_beta(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    assert mixed.rank() == 4
    kernel = mixed.nullspace()
    assert len(kernel) == 4
    extension = sp.Matrix.hstack(*kernel) * sp.Matrix(c)
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    assert sp.factor(abs(sp.cancel(actual_a * p / (2 * (c[0] * p - c[3]))))) == 1
    assert sp.expand(actual_b + 2 * (c[1] + c[2])) == 0
    alpha_numerator = sp.cancel(p * actual_a)
    scaled_generic = p * stack(deletion, extension, alpha, marked, 0)
    assert all(sp.fraction(sp.cancel(entry))[1] == 1 for entry in scaled_generic)
    generic_label = maximal_minor_unit(
        f"{endpoint}_d{deletion}_h{active_mode}_punctured_k_nonzero",
        (scaled_generic.applyfunc(sp.cancel),),
        c + (p, k),
        p * k * alpha_numerator * actual_b,
    )
    zero_extension = extension.subs(k, 0)
    zero_matrices = tuple(
        (p * stack(deletion, zero_extension, alpha, marked, mode).subs(k, 0)).applyfunc(
            sp.cancel
        )
        for mode in range(4)
    )
    assert all(
        sp.fraction(entry)[1] == 1 for matrix in zero_matrices for entry in matrix
    )
    zero_label = maximal_minor_unit(
        f"{endpoint}_d{deletion}_h{active_mode}_punctured_k_zero",
        zero_matrices,
        c + (p,),
        p * alpha_numerator.subs(k, 0) * actual_b.subs(k, 0),
    )
    return {
        "endpoint": endpoint,
        "deletion": deletion,
        "active_marking": active_mode,
        "mixed_rank": 4,
        "A": str(actual_a),
        "B": str(actual_b),
        "k_nonzero": generic_label,
        "k_zero": zero_label,
    }


def intersection_case(endpoint, deletion):
    alpha, beta = endpoint_rows(endpoint)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, beta)
    assert mixed.rank() == 4
    kernel = mixed.nullspace()
    assert len(kernel) == 4
    extension = sp.Matrix.hstack(*kernel) * sp.Matrix(c)
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    generic = stack(deletion, extension, alpha, beta, 0)
    generic_label = maximal_minor_unit(
        f"{endpoint}_d{deletion}_intersection_k_nonzero",
        (generic,),
        c + (k,),
        k * actual_a * actual_b,
    )
    zero_extension = extension.subs(k, 0)
    zero_stacks = tuple(
        stack(deletion, zero_extension, alpha, beta, mode).subs(k, 0)
        for mode in range(4)
    )
    zero_a = actual_a.subs(k, 0)
    zero_b = actual_b.subs(k, 0)
    rank_labels = tuple(
        maximal_minor_unit(
            f"{endpoint}_d{deletion}_intersection_k_zero_rank4_mode{mode}",
            (zero_stacks[mode],),
            c,
            zero_a * zero_b,
            size=4,
        )
        for mode in (0, 1)
    )
    sign = 1 if deletion == 2 else -1
    gammas = (
        sp.Matrix((0, 0, sign, -sign, c[3])),
        sp.Matrix((0, 0, sign, -sign, c[2])),
    )
    for mode, gamma in enumerate(gammas):
        assert zero_stacks[mode] * gamma == sp.zeros(16, 1)
        local_alpha = tuple(alpha[mode]) + (zero_extension[mode],)
        local_beta = tuple(beta[mode]) + (zero_extension[4 + mode],)
        assert sp.Matrix((local_alpha, local_beta, tuple(gamma))).rank() == 3
    forbidden = sp.factor(
        permanent((tuple(gammas[0][:4]), tuple(gammas[1][:4]), beta[2], beta[3]))
    )
    assert forbidden == 4
    return {
        "endpoint": endpoint,
        "deletion": deletion,
        "A": str(actual_a),
        "B": str(actual_b),
        "k_nonzero": generic_label,
        "k_zero_rank4": rank_labels,
        "k_zero_forbidden_2211": str(forbidden),
    }


def h22_projection(endpoint, chart, alpha_branch):
    alpha, beta = endpoint_rows(endpoint)
    marked = shifted_beta(alpha, beta, h)
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, marked, x, "D01", chart, slope)
    d23 = build_model(alpha, marked, x, "D23", chart, slope)
    diagonals = (d01["A"], d23["A"], d01["B"], d23["B"])
    equations = (
        *d01["mixed"],
        *d23["mixed"],
        diagonals[alpha_branch] - 1,
        w * diagonals[2] * diagonals[3] - 1,
    )
    expected = (h[0], h[1], h[2]) if endpoint == "r_infinity" else (h[0], h[1], h[3])
    eliminated = x + (w,)
    retained = h + ((k, lam) if chart == "finite" else (k,))
    variables = eliminated + retained
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + f"),(dp(9),dp({len(retained)}));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    run_singular(
        f"{endpoint}_{chart}_h22_A{alpha_branch}_projection",
        program,
        f"RESULT:1:{len(expected)}",
    )
    return f"{endpoint}:{chart}:A{alpha_branch}:{tuple(map(str, expected))}"


def gamma_matrix(alpha5, marked5, contraction_rows, mode):
    gamma = sp.symbols("gamma0:5")
    equations = []
    for contraction in contraction_rows:
        for word in itertools.product((0, 1), repeat=3):
            selected = []
            cursor = 0
            for index in range(4):
                if index == mode:
                    selected.append(gamma)
                else:
                    selected.append(marked5[index] if word[cursor] else alpha5[index])
                    cursor += 1
            equations.append(permanent5(tuple(selected) + (contraction,)))
    return sp.Matrix(
        [[sp.diff(equation, variable) for variable in gamma] for equation in equations]
    )


def h22_survivor(endpoint, chart):
    alpha, beta = endpoint_rows(endpoint)
    active_mode = 3 if endpoint == "r_infinity" else 2
    marking = (0, 0, 0, p) if active_mode == 3 else (0, 0, p, 0)
    marked = shifted_beta(alpha, beta, marking)
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, marked, x, "D01", chart, slope)
    d23 = build_model(alpha, marked, x, "D23", chart, slope)
    mixed = sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in x]
            for equation in (*d01["mixed"], *d23["mixed"])
        ]
    )
    extension = sp.Matrix(
        (0, 0, 0, -1, 0, 1, 0, 0)
        if endpoint == "r_infinity"
        else (0, 0, -1, 0, 0, 1, 0, 0)
    )
    assert mixed.rank() == 7
    assert mixed * extension == sp.zeros(28, 1)
    assert len(mixed.nullspace()) == 1
    diagonals = tuple(
        sp.factor(
            sum(
                sp.diff(model[kind], variable) * extension[index]
                for index, variable in enumerate(x)
            )
        )
        for model in (d01, d23)
        for kind in ("A", "B")
    )
    # build_model order above is A01,B01,A23,B23; reorder for the theorem.
    reordered = (diagonals[0], diagonals[2], diagonals[1], diagonals[3])
    expected = (
        (2 * k * (lam + 1), -2 * (lam - 1), 2 * p * (lam - 1), -2 * (lam + 1))
        if chart == "finite"
        else (2 * k, -2, 2 * p, -2)
    )
    assert all(sp.expand(left - right) == 0 for left, right in zip(reordered, expected))
    alpha5 = tuple(tuple(alpha[index]) + (extension[index],) for index in range(4))
    marked5 = tuple(
        tuple(marked[index]) + (extension[4 + index],) for index in range(4)
    )
    contraction_rows = (
        ((1, lam, 0, 0, 0), (0, 0, 1, lam, 0))
        if chart == "finite"
        else ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0))
    )
    one_gamma = gamma_matrix(alpha5, marked5, contraction_rows, 1)
    rows = (0, 6, 7, 8, 14) if endpoint == "r_infinity" else (0, 5, 7, 8, 13)
    determinant = sp.factor(one_gamma.extract(rows, range(5)).det(method="domain-ge"))
    expected_determinant = (
        -8 * p * (lam - 1) ** 3 * (lam + 1) ** 2 if chart == "finite" else -8 * p
    )
    assert sp.expand(determinant - expected_determinant) == 0
    return {
        "endpoint": endpoint,
        "chart": chart,
        "mixed_rank": 7,
        "extension": tuple(map(str, extension)),
        "diagonal_order": ("A01", "A23", "B01", "B23"),
        "diagonals": tuple(map(str, reordered)),
        "one_gamma_mode": 1,
        "one_gamma_rows": rows,
        "one_gamma_determinant": str(determinant),
    }


def main():
    endpoints = ("r_infinity", "t_infinity")
    geometry = tuple(geometry_certificate(endpoint) for endpoint in endpoints)
    projections = tuple(
        projection_ideal(endpoint, deletion)
        for endpoint in endpoints
        for deletion in range(4)
    )
    d01 = tuple(
        h31_d01_lines(endpoint, deletion)
        for endpoint in endpoints
        for deletion in (0, 1)
    )
    punctured = tuple(
        punctured_marking(endpoint, deletion, active_mode)
        for endpoint in endpoints
        for deletion in (2, 3)
        for active_mode in (2, 3)
    )
    intersections = tuple(
        intersection_case(endpoint, deletion)
        for endpoint in endpoints
        for deletion in (2, 3)
    )
    h22_projections = tuple(
        h22_projection(endpoint, chart, alpha_branch)
        for endpoint in endpoints
        for chart in ("finite", "infinity")
        for alpha_branch in (0, 1)
    )
    h22 = tuple(
        h22_survivor(endpoint, chart)
        for endpoint in endpoints
        for chart in ("finite", "infinity")
    )
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "field": "Q",
                "scope": "component 23 normalized s=0,rt=1 projective parameter endpoints, finite k",
                "geometry": geometry,
                "h31_projections": projections,
                "h31_d01_lines": d01,
                "h31_punctured": punctured,
                "h31_intersections": intersections,
                "h22_projections": h22_projections,
                "h22_survivors_and_compatibility": h22,
                "finite_field_used": False,
                "limitations": "fixed normalized order; arbitrary source/ambient bases, arbitrary order, gluing, and global conjecture not claimed",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
