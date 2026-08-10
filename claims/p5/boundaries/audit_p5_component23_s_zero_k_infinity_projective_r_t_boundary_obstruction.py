#!/usr/bin/env python3
"""No-import exact-Q audit of the component-23 projective r/t boundary."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
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


def permanent5(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(5))
            for permutation in PERMUTATIONS5
        )
    )


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


def h31_coefficients(deletion, alpha, beta, extension):
    common = tuple(index for index in range(4) if index != deletion)
    alpha4 = tuple(
        tuple(alpha[mode][index] for index in common) + (extension[mode],)
        for mode in range(4)
    )
    beta4 = tuple(
        tuple(beta[mode][index] for index in common) + (extension[4 + mode],)
        for mode in range(4)
    )
    return {
        word: permanent4(
            tuple(beta4[mode] if word[mode] else alpha4[mode] for mode in range(4))
        )
        for word in WORDS
    }


def h31_mixed_matrix(deletion, alpha, beta):
    coefficients = h31_coefficients(deletion, alpha, beta, x)
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in x]
            for word in MIXED_WORDS
        ]
    )
    diagonals = tuple(
        sp.Matrix([[sp.diff(coefficients[word], variable) for variable in x]])
        for word in (WORDS[0], WORDS[-1])
    )
    return mixed, *diagonals


def one_marked_map(mode, alpha, beta):
    rows = []
    for word in itertools.product((0, 1), repeat=3):
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if word[cursor] else alpha[other])
                cursor += 1
        values = []
        for coordinate in range(4):
            basis = tuple(sp.Integer(index == coordinate) for index in range(4))
            values.append(
                permanent4(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(values)
    return sp.Matrix(rows)


def marked_extension(deletion, extension, alpha, beta, mode):
    common = tuple(index for index in range(4) if index != deletion)
    alpha4 = tuple(
        tuple(alpha[row][index] for index in common) + (extension[row],)
        for row in range(4)
    )
    beta4 = tuple(
        tuple(beta[row][index] for index in common) + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(mode, alpha4, beta4)


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


def h22_model(alpha, beta, direction, chart, slope=None):
    alpha4 = tuple(
        project(alpha[index], x[index], direction, chart, slope) for index in range(4)
    )
    beta4 = tuple(
        project(beta[index], x[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta4[index] if word[index] else alpha4[index] for index in range(4)
        )
        coefficients[word] = sp.expand(
            sum(
                selected[index][3]
                * permanent3(
                    tuple(selected[other][:3] for other in range(4) if other != index)
                )
                for index in range(4)
            )
        )
    return {
        "mixed": tuple(coefficients[word] for word in MIXED_WORDS),
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
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp({len(retained)}));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    return run_singular(label, program, f"RESULT:1:{len(expected)}")


def geometry_audit(boundary):
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
            permanent4(
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
    return f"{boundary}:{profile}:{zero_profile}:pure"


def h31_projection_audit(boundary, deletion):
    alpha, beta = boundary_rows(boundary)
    marked = shifted_beta(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, marked)
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
    return compare_projection(
        f"audit_{boundary}_h31_d{deletion}",
        equations,
        x + (w,),
        retained,
        expected,
    )


def h31_curve_audit(boundary):
    alpha0, beta = boundary_rows(boundary)
    results = []
    cases = [("central", None), ("zero", None), ("sign", 1), ("sign", -1)]
    for branch, sign in cases:
        if branch == "central":
            alpha = alpha0
            marking = (0, q, 0, 0)
        elif branch == "zero":
            alpha = substitute_rows(alpha0, {q: 0})
            marking = (0, 0, 0, p) if boundary == "r_infinity" else (0, 0, p, 0)
        else:
            alpha = substitute_rows(alpha0, {q: sign})
            marking = (0, sign, p, 0) if boundary == "r_infinity" else (0, sign, 0, p)
        marked = shifted_beta(alpha, beta, marking)
        for deletion in (0, 1):
            mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, marked)
            assert mixed.rank() == 6
            extension = sp.Matrix.hstack(*mixed.nullspace()) * sp.Matrix((c0, c1))
            actual_a = sp.factor((diagonal_a * extension)[0])
            actual_b = sp.factor((diagonal_b * extension)[0])
            matrix = stack(deletion, extension, alpha, marked, 0)
            rows = (
                (0, 1, 2, 7, 10)
                if branch == "zero" and boundary == "t_infinity"
                else (0, 1, 2, 7, 9)
            )
            determinant = sp.factor(
                matrix.extract(rows, range(5)).det(method="domain-ge")
            )
            deletion_sign = 1 if deletion == 0 else -1
            if branch == "central":
                expected = (
                    deletion_sign * 32 * c0**2 * c1
                    if boundary == "r_infinity"
                    else -deletion_sign * 32 * q * c0**2 * c1
                )
            elif branch == "zero":
                boundary_sign = 1 if boundary == "r_infinity" else -1
                expected = (
                    boundary_sign * deletion_sign * 16 * c0**2 * (c0 * p + 2 * c1)
                )
            else:
                boundary_sign = 1 if boundary == "r_infinity" else -sign
                expected = (
                    boundary_sign
                    * deletion_sign
                    * 16
                    * (c0 - c1) ** 2
                    * (c0 + c1)
                    / p**2
                )
            assert sp.cancel(determinant - expected) == 0
            assert actual_a != 0 and actual_b != 0
            results.append(f"{boundary}:{branch}:{sign}:d{deletion}:{determinant}")
    return tuple(results)


def h31_intersection_audit():
    alpha, beta = boundary_rows("intersection")
    results = []
    for axis in (1, 2, 3):
        marking = [0, 0, 0, 0]
        marking[axis] = p
        marked = shifted_beta(alpha, beta, tuple(marking))
        for deletion in (0, 1):
            mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, marked)
            extension = sp.Matrix.hstack(*mixed.nullspace()) * sp.Matrix((c0, c1))
            matrix = stack(deletion, extension, alpha, marked, 0)
            determinant = sp.factor(
                matrix.extract((0, 1, 3, 7, 9), range(5)).det(method="domain-ge")
            )
            deletion_sign = 1 if deletion == 0 else -1
            expected = {
                1: deletion_sign * 64 * c0 * c1**2,
                2: -deletion_sign * 16 * (c0 - c1) * (c0 + c1) ** 2 / p,
                3: deletion_sign * 16 * (c0 - c1) * (c0 + c1) ** 2 / p,
            }[axis]
            assert sp.cancel(determinant - expected) == 0
            assert (diagonal_a * extension)[0] != 0
            assert (diagonal_b * extension)[0] != 0
            results.append(f"axis{axis}:d{deletion}:{determinant}")
    return tuple(results)


def h22_projection_audit(boundary, chart, alpha_branch):
    alpha, beta = boundary_rows(boundary)
    marked = shifted_beta(alpha, beta, h)
    slope = lam if chart == "finite" else None
    models = tuple(
        h22_model(alpha, marked, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    diagonals = (models[0]["A"], models[1]["A"], models[0]["B"], models[1]["B"])
    equations = (
        *models[0]["mixed"],
        *models[1]["mixed"],
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
    retained = h + (() if boundary == "intersection" else (q,))
    if chart == "finite":
        retained += (lam,)
    return compare_projection(
        f"audit_{boundary}_{chart}_h22_A{alpha_branch}",
        equations,
        x + (w,),
        retained,
        expected,
    )


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


def h22_branch_audit(boundary, branch, chart, sign=None):
    alpha, beta = boundary_rows(boundary)
    if branch == "zero":
        alpha = substitute_rows(alpha, {q: 0})
        marking = (0, 0, 0, p) if boundary == "r_infinity" else (0, 0, p, 0)
        extension = (
            (0, 0, 0, -1, 0, 1, 0, 0)
            if boundary == "r_infinity"
            else (0, 0, -1, 0, 0, 1, 0, 0)
        )
    else:
        alpha = substitute_rows(alpha, {q: sign})
        marking = (0, sign, p, 0) if boundary == "r_infinity" else (0, sign, 0, p)
        extension = (
            (0, 0, 0, -sign, 0, sign, p, 0)
            if boundary == "r_infinity"
            else (0, 0, -sign, 0, 0, sign, 0, p)
        )
    marked = shifted_beta(alpha, beta, marking)
    slope = lam if chart == "finite" else None
    models = tuple(
        h22_model(alpha, marked, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    mixed = sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in x]
            for model in models
            for equation in model["mixed"]
        ]
    )
    extension_vector = sp.Matrix(extension)
    assert mixed.rank() == 7
    assert all(sp.expand(value) == 0 for value in mixed * extension_vector)
    raw = tuple(
        sp.factor(
            sum(
                sp.diff(model[kind], variable) * extension_vector[index]
                for index, variable in enumerate(x)
            )
        )
        for model in models
        for kind in ("A", "B")
    )
    diagonals = (raw[0], raw[2], raw[1], raw[3])
    assert diagonals[1] == 0
    alpha5 = tuple(tuple(alpha[index]) + (extension[index],) for index in range(4))
    marked5 = tuple(
        tuple(marked[index]) + (extension[4 + index],) for index in range(4)
    )
    contractions = (
        ((1, lam, 0, 0, 0), (0, 0, 1, lam, 0))
        if chart == "finite"
        else ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0))
    )
    matrix = gamma_matrix(alpha5, marked5, contractions, 0)
    rows = (0, 1, 2, 7, 10) if boundary == "r_infinity" else (0, 1, 2, 7, 9)
    determinant = sp.factor(matrix.extract(rows, range(5)).det(method="domain-ge"))
    boundary_factor = -1 if boundary == "r_infinity" else 1
    parameter_factor = 1 if branch == "zero" else sign
    weight_factor = (lam - 1) ** 4 * (lam + 1) if chart == "finite" else 1
    expected = boundary_factor * parameter_factor * 8 * p * weight_factor
    assert sp.expand(determinant - expected) == 0
    return f"{boundary}:{branch}:{sign}:{chart}:{determinant}"


def main():
    boundaries = ("r_infinity", "t_infinity", "intersection")
    geometry = tuple(geometry_audit(boundary) for boundary in boundaries)
    h31_projections = tuple(
        h31_projection_audit(boundary, deletion)
        for boundary in boundaries
        for deletion in range(4)
    )
    h31_curves = tuple(
        h31_curve_audit(boundary) for boundary in ("r_infinity", "t_infinity")
    )
    h31_intersection = h31_intersection_audit()
    h22_projections = tuple(
        h22_projection_audit(boundary, chart, alpha_branch)
        for boundary in boundaries
        for chart in ("finite", "infinity")
        for alpha_branch in (0, 1)
    )
    h22 = tuple(
        h22_branch_audit(boundary, branch, chart, sign)
        for boundary in ("r_infinity", "t_infinity")
        for branch, sign in (("zero", None), ("sign", 1), ("sign", -1))
        for chart in ("finite", "infinity")
    )
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "field": "Q",
                "scope": "no-import reconstruction of component-23 s=0,k=infinity projective r/t boundary",
                "geometry": geometry,
                "h31_projections": h31_projections,
                "h31_curves": h31_curves,
                "h31_intersection": h31_intersection,
                "h22_projections": h22_projections,
                "h22": h22,
                "project_imports": False,
                "finite_field_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
