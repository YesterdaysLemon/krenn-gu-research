#!/usr/bin/env python3
"""Close component 23's s=0,k=infinity projective r/t boundary."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
)
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
q, lam, p, w = sp.symbols("q lam p w")
c0, c1 = sp.symbols("c0 c1")

A = (sp.Integer(1), 1, 0, 0)
C = (sp.Integer(1), -1, 0, 0)
B = (0, 0, sp.Integer(1), 1)
D = (0, 0, sp.Integer(1), -1)


def add(left, right, coefficient=1):
    return tuple(
        sp.expand(left[index] + coefficient * right[index]) for index in range(4)
    )


def boundary_rows(boundary):
    if boundary == "r_infinity":
        alpha = (A, D, D, add(B, D, q))
    elif boundary == "t_infinity":
        alpha = (A, D, add(B, D, q), D)
    elif boundary == "intersection":
        alpha = (A, D, D, D)
    else:
        raise ValueError(boundary)
    return alpha, (B, B, C, C)


def substitute_rows(rows, substitutions):
    return tuple(
        tuple(sp.sympify(entry).subs(substitutions) for entry in row) for row in rows
    )


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


def geometry_certificate(boundary):
    alpha, beta = boundary_rows(boundary)
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    profile = tuple(
        pair_matrix(planes[left], planes[right]).rank() for left, right in PAIRS
    )
    if boundary == "intersection":
        zero_profile = profile
        expected = ((3, 2, 2, 3, 3, 3),) * 2
    else:
        zero_planes = tuple(
            tuple(tuple(sp.sympify(entry).subs(q, 0) for entry in row) for row in plane)
            for plane in planes
        )
        zero_profile = tuple(
            pair_matrix(zero_planes[left], zero_planes[right]).rank()
            for left, right in PAIRS
        )
        expected = {
            "r_infinity": ((3, 2, 3, 3, 3, 4), (3, 2, 3, 3, 3, 3)),
            "t_infinity": ((3, 3, 2, 3, 3, 4), (3, 3, 2, 3, 3, 3)),
        }[boundary]
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
    assert coefficients[WORDS[-1]] == -4
    assert all(value == 0 for word, value in coefficients.items() if word != WORDS[-1])
    assert all(sp.Matrix(plane).rank() == 2 for plane in planes)
    projective_markings = tuple(
        coefficients[tuple(0 if index == mode else 1 for index in range(4))]
        for mode in range(4)
    )
    assert projective_markings == (0, 0, 0, 0)

    r, t = sp.symbols("r t")
    finite2, finite3 = add(B, D, r), add(B, D, t)
    assert tuple(sp.limit(entry / r, r, sp.oo) for entry in finite2) == D
    assert tuple(sp.limit(entry / t, t, sp.oo) for entry in finite3) == D
    return {
        "boundary": boundary,
        "profile": profile,
        "parameter_zero_profile": zero_profile,
        "pure": "T1111=-4",
    }


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def run_singular(label, program, expected, timeout=600):
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


def compare_projection(label, equations, eliminated, retained, expected):
    variables = eliminated + retained
    expected_size = len(expected)
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp({len(retained)}));",
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
    return run_singular(label, program, f"RESULT:1:{expected_size}")


def h31_projection(boundary, deletion):
    alpha, beta = boundary_rows(boundary)
    marked = shifted_beta(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    extension = sp.Matrix(x)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        w * (diagonal_b * extension)[0] - 1,
    )
    if deletion in (2, 3):
        expected = (sp.Integer(1),)
    elif boundary == "r_infinity":
        expected = (
            h[1] - q,
            h[0],
            q * h[3],
            h[2] * h[3],
            (q**2 - 1) * h[2],
        )
    elif boundary == "t_infinity":
        expected = (
            h[1] - q,
            h[0],
            q * h[2],
            h[2] * h[3],
            (q**2 - 1) * h[3],
        )
    else:
        expected = (h[0], h[2] * h[3], h[1] * h[3], h[1] * h[2])
    retained = h + (() if boundary == "intersection" else (q,))
    label = compare_projection(
        f"{boundary}_h31_d{deletion}",
        equations,
        x + (w,),
        retained,
        expected,
    )
    return f"{label}:{tuple(map(str, expected))}"


def stack(deletion, extension, alpha, beta, mode):
    neighbour = marked_extension(deletion, extension, alpha, beta, mode)
    pure = one_marked_map(mode, alpha, beta)
    columns = tuple(index for index in range(4) if index != deletion) + (4,)
    result = sp.zeros(16, 5)
    for row in range(8):
        for source, column in enumerate(columns):
            result[row, column] = neighbour[row, source]
        for column in range(4):
            result[8 + row, column] = pure[row, column]
    return result


def h31_branch(boundary, branch, deletion, sign=None):
    alpha, beta = boundary_rows(boundary)
    if branch == "central":
        marking = (0, q, 0, 0)
        substitutions = {}
    elif branch == "zero":
        marking = (0, 0, 0, p) if boundary == "r_infinity" else (0, 0, p, 0)
        substitutions = {q: 0}
    elif branch == "sign":
        assert sign in (1, -1)
        marking = (0, sign, p, 0) if boundary == "r_infinity" else (0, sign, 0, p)
        substitutions = {q: sign}
    else:
        raise ValueError(branch)
    alpha = substitute_rows(alpha, substitutions)
    marked = shifted_beta(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    assert mixed.rank() == 6
    kernel = mixed.nullspace()
    assert len(kernel) == 2
    extension = sp.Matrix.hstack(*kernel) * sp.Matrix((c0, c1))
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    matrix = stack(deletion, extension, alpha, marked, 0)
    if branch == "zero" and boundary == "t_infinity":
        rows = (0, 1, 2, 7, 10)
    else:
        rows = (0, 1, 2, 7, 9)
    determinant = sp.factor(matrix.extract(rows, range(5)).det(method="domain-ge"))
    deletion_sign = 1 if deletion == 0 else -1
    if branch == "central":
        expected = (
            deletion_sign * 32 * c0**2 * c1
            if boundary == "r_infinity"
            else -deletion_sign * 32 * q * c0**2 * c1
        )
    elif branch == "zero":
        boundary_sign = 1 if boundary == "r_infinity" else -1
        expected = boundary_sign * deletion_sign * 16 * c0**2 * (c0 * p + 2 * c1)
    else:
        boundary_sign = 1 if boundary == "r_infinity" else -sign
        expected = (
            boundary_sign * deletion_sign * 16 * (c0 - c1) ** 2 * (c0 + c1) / p**2
        )
    assert sp.cancel(determinant - expected) == 0
    return {
        "boundary": boundary,
        "branch": branch if sign is None else f"sign_{sign}",
        "deletion": deletion,
        "mixed_rank": 6,
        "A": str(actual_a),
        "B": str(actual_b),
        "rows": rows,
        "determinant": str(determinant),
    }


def h31_intersection_axis(axis, deletion):
    alpha, beta = boundary_rows("intersection")
    marking_list = [0, 0, 0, 0]
    marking_list[axis] = p
    marked = shifted_beta(alpha, beta, tuple(marking_list))
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    assert mixed.rank() == 6
    extension = sp.Matrix.hstack(*mixed.nullspace()) * sp.Matrix((c0, c1))
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    matrix = stack(deletion, extension, alpha, marked, 0)
    rows = (0, 1, 3, 7, 9)
    determinant = sp.factor(matrix.extract(rows, range(5)).det(method="domain-ge"))
    deletion_sign = 1 if deletion == 0 else -1
    expected = {
        1: deletion_sign * 64 * c0 * c1**2,
        2: -deletion_sign * 16 * (c0 - c1) * (c0 + c1) ** 2 / p,
        3: deletion_sign * 16 * (c0 - c1) * (c0 + c1) ** 2 / p,
    }[axis]
    assert sp.cancel(determinant - expected) == 0
    return {
        "axis": axis,
        "deletion": deletion,
        "A": str(actual_a),
        "B": str(actual_b),
        "rows": rows,
        "determinant": str(determinant),
    }


def h22_projection(boundary, chart, alpha_branch):
    alpha, beta = boundary_rows(boundary)
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
    if boundary == "intersection" or alpha_branch == 1:
        expected = (sp.Integer(1),)
    elif boundary == "r_infinity":
        expected = (
            h[1] - q,
            h[0],
            q * h[3],
            h[2] * h[3],
            q**3 - q,
            (q**2 - 1) * h[2],
        )
    else:
        expected = (
            h[1] - q,
            h[0],
            q * h[2],
            h[2] * h[3],
            q**3 - q,
            (q**2 - 1) * h[3],
        )
    retained = h
    if boundary != "intersection":
        retained += (q,)
    if chart == "finite":
        retained += (lam,)
    label = compare_projection(
        f"{boundary}_{chart}_h22_A{alpha_branch}",
        equations,
        x + (w,),
        retained,
        expected,
    )
    return f"{label}:{tuple(map(str, expected))}"


def gamma_matrix(alpha5, marked5, contraction_rows, mode):
    gamma = sp.symbols("gamma0:5")
    equations = []
    for contraction in contraction_rows:
        for word in itertools.product((0, 1), repeat=3):
            rows = []
            cursor = 0
            for index in range(4):
                if index == mode:
                    rows.append(gamma)
                else:
                    rows.append(marked5[index] if word[cursor] else alpha5[index])
                    cursor += 1
            equations.append(permanent5(tuple(rows) + (contraction,)))
    return sp.Matrix(
        [[sp.diff(equation, variable) for variable in gamma] for equation in equations]
    )


def h22_exceptional_branch(boundary, branch, chart, sign=None):
    alpha, beta = boundary_rows(boundary)
    if branch == "zero":
        substitutions = {q: 0}
        marking = (0, 0, 0, p) if boundary == "r_infinity" else (0, 0, p, 0)
        extension = (
            (0, 0, 0, -1, 0, 1, 0, 0)
            if boundary == "r_infinity"
            else (0, 0, -1, 0, 0, 1, 0, 0)
        )
    else:
        assert sign in (1, -1)
        substitutions = {q: sign}
        marking = (0, sign, p, 0) if boundary == "r_infinity" else (0, sign, 0, p)
        extension = (
            (0, 0, 0, -sign, 0, sign, p, 0)
            if boundary == "r_infinity"
            else (0, 0, -sign, 0, 0, sign, 0, p)
        )
    alpha = substitute_rows(alpha, substitutions)
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
    extension_vector = sp.Matrix(extension)
    assert mixed.rank() == 7
    assert all(sp.expand(value) == 0 for value in mixed * extension_vector)
    assert len(mixed.nullspace()) == 1
    raw = tuple(
        sp.factor(
            sum(
                sp.diff(model[kind], variable) * extension_vector[index]
                for index, variable in enumerate(x)
            )
        )
        for model in (d01, d23)
        for kind in ("A", "B")
    )
    diagonals = (raw[0], raw[2], raw[1], raw[3])
    assert diagonals[1] == 0
    alpha5 = tuple(tuple(alpha[index]) + (extension[index],) for index in range(4))
    marked5 = tuple(
        tuple(marked[index]) + (extension[4 + index],) for index in range(4)
    )
    contraction_rows = (
        ((1, lam, 0, 0, 0), (0, 0, 1, lam, 0))
        if chart == "finite"
        else ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0))
    )
    one_gamma = gamma_matrix(alpha5, marked5, contraction_rows, 0)
    rows = (0, 1, 2, 7, 10) if boundary == "r_infinity" else (0, 1, 2, 7, 9)
    determinant = sp.factor(one_gamma.extract(rows, range(5)).det(method="domain-ge"))
    boundary_factor = -1 if boundary == "r_infinity" else 1
    parameter_factor = 1 if branch == "zero" else sign
    weight_factor = (lam - 1) ** 4 * (lam + 1) if chart == "finite" else 1
    expected = boundary_factor * parameter_factor * 8 * p * weight_factor
    assert sp.expand(determinant - expected) == 0
    return {
        "boundary": boundary,
        "branch": branch if sign is None else f"sign_{sign}",
        "chart": chart,
        "mixed_rank": 7,
        "extension": tuple(map(str, extension)),
        "diagonal_order": ("A01", "A23", "B01", "B23"),
        "diagonals": tuple(map(str, diagonals)),
        "gamma_mode": 0,
        "gamma_rows": rows,
        "gamma_determinant": str(determinant),
    }


def main():
    boundaries = ("r_infinity", "t_infinity", "intersection")
    geometry = tuple(geometry_certificate(boundary) for boundary in boundaries)
    h31_projections = tuple(
        h31_projection(boundary, deletion)
        for boundary in boundaries
        for deletion in range(4)
    )
    h31_curves = tuple(
        h31_branch(boundary, branch, deletion, sign)
        for boundary in ("r_infinity", "t_infinity")
        for branch, sign in (
            ("central", None),
            ("zero", None),
            ("sign", 1),
            ("sign", -1),
        )
        for deletion in (0, 1)
    )
    h31_intersection = tuple(
        h31_intersection_axis(axis, deletion)
        for axis in (1, 2, 3)
        for deletion in (0, 1)
    )
    h22_projections = tuple(
        h22_projection(boundary, chart, alpha_branch)
        for boundary in boundaries
        for chart in ("finite", "infinity")
        for alpha_branch in (0, 1)
    )
    h22_branches = tuple(
        h22_exceptional_branch(boundary, branch, chart, sign)
        for boundary in ("r_infinity", "t_infinity")
        for branch, sign in (("zero", None), ("sign", 1), ("sign", -1))
        for chart in ("finite", "infinity")
    )
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "field": "Q",
                "scope": "component 23 normalized s=0,k=infinity projective r/t boundary",
                "geometry": geometry,
                "h31_projections": h31_projections,
                "h31_curve_branches": h31_curves,
                "h31_intersection": h31_intersection,
                "h22_projections": h22_projections,
                "h22_exceptional_branches": h22_branches,
                "finite_field_used": False,
                "limitations": "fixed normalized order only; arbitrary bases, arbitrary order, gluing, and global conjecture not claimed",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
