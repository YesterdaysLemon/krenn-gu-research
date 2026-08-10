#!/usr/bin/env python3
"""No-import exact-Q audit of component 23's projective face endpoints."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp
import sys
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
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
    alpha = (
        (A, add(A, D, k), D, B) if endpoint == "r_infinity" else (A, add(A, D, k), B, D)
    )
    return alpha, (B, B, C, C)


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
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables + (u,))) + "),dp;",
            "option(redSB);",
            *declarations,
            "ideal I="
            + ",".join(f"minor(M{index},{size})" for index in range(len(matrices)))
            + ","
            + singular_text(u * inverse_product - 1)
            + ";",
            "I=slimgb(I);",
            "int unit=reduce(1,std(I))==0;",
            '"RESULT:"+string(unit);',
            "quit;",
        )
    )
    return run_singular(label, program)


def geometry_audit(endpoint):
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
    return f"{endpoint}:{profile}:{zero_profile}:pure"


def h31_projection_audit(endpoint, deletion):
    alpha, beta = endpoint_rows(endpoint)
    marked = shifted_beta(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, marked)
    extension = sp.Matrix(x)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        w * (diagonal_b * extension)[0] - 1,
    )
    expected = (
        (h[0], h[1], h[2] if endpoint == "r_infinity" else h[3])
        if deletion in (0, 1)
        else (h[0], h[1], h[2] * h[3])
    )
    eliminated = x + (w,)
    variables = eliminated + h + (k,)
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(5));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    return run_singular(
        f"audit_{endpoint}_h31_d{deletion}", program, f"RESULT:1:{len(expected)}"
    )


def h31_fibre_audit(endpoint):
    alpha, beta = endpoint_rows(endpoint)
    results = []
    active = 3 if endpoint == "r_infinity" else 2
    lone_marking = (0, 0, 0, p) if active == 3 else (0, 0, p, 0)
    for deletion in (0, 1):
        marked = shifted_beta(alpha, beta, lone_marking)
        mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, marked)
        assert mixed.rank() == 6
        kernel = mixed.nullspace()
        extension = sp.Matrix.hstack(*kernel) * sp.Matrix(c[:2])
        actual_a = sp.factor((diagonal_a * extension)[0])
        actual_b = sp.factor((diagonal_b * extension)[0])
        assert actual_a == 2 * c[0] * k
        matrix = stack(deletion, extension, alpha, marked, 0)
        rows = (0, 1, 2, 7, 9 if endpoint == "r_infinity" else 10)
        determinant = sp.factor(matrix.extract(rows, range(5)).det(method="domain-ge"))
        assert sp.cancel(determinant / (actual_a * actual_b)) != 0
        # The observed determinant has no factor outside the genuine diagonal
        # product and k, which is already forced by actual_a.
        residual = sp.factor(determinant / (actual_a * actual_b))
        assert sp.factor(residual / (c[0] * k**3)) in (4, -4)
        results.append(f"{endpoint}:d{deletion}:d01-stack")

    for deletion in (2, 3):
        for active_mode in (2, 3):
            marking = (0, 0, p, 0) if active_mode == 2 else (0, 0, 0, p)
            marked = shifted_beta(alpha, beta, marking)
            mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, marked)
            assert mixed.rank() == 4
            extension = sp.Matrix.hstack(*mixed.nullspace()) * sp.Matrix(c)
            actual_a = sp.factor((diagonal_a * extension)[0])
            actual_b = sp.factor((diagonal_b * extension)[0])
            alpha_numerator = sp.cancel(p * actual_a)
            generic = (p * stack(deletion, extension, alpha, marked, 0)).applyfunc(
                sp.cancel
            )
            maximal_minor_unit(
                f"audit_{endpoint}_d{deletion}_h{active_mode}_k_nonzero",
                (generic,),
                c + (p, k),
                p * k * alpha_numerator * actual_b,
            )
            extension0 = extension.subs(k, 0)
            zero_matrices = tuple(
                (
                    p * stack(deletion, extension0, alpha, marked, mode).subs(k, 0)
                ).applyfunc(sp.cancel)
                for mode in range(4)
            )
            maximal_minor_unit(
                f"audit_{endpoint}_d{deletion}_h{active_mode}_k_zero",
                zero_matrices,
                c + (p,),
                p * alpha_numerator.subs(k, 0) * actual_b.subs(k, 0),
            )
            results.append(f"{endpoint}:d{deletion}:h{active_mode}:punctured")

        mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, beta)
        extension = sp.Matrix.hstack(*mixed.nullspace()) * sp.Matrix(c)
        actual_a = sp.factor((diagonal_a * extension)[0])
        actual_b = sp.factor((diagonal_b * extension)[0])
        maximal_minor_unit(
            f"audit_{endpoint}_d{deletion}_intersection_k_nonzero",
            (stack(deletion, extension, alpha, beta, 0),),
            c + (k,),
            k * actual_a * actual_b,
        )
        extension0 = extension.subs(k, 0)
        stacks0 = tuple(
            stack(deletion, extension0, alpha, beta, mode).subs(k, 0)
            for mode in range(4)
        )
        zero_a, zero_b = actual_a.subs(k, 0), actual_b.subs(k, 0)
        for mode in (0, 1):
            maximal_minor_unit(
                f"audit_{endpoint}_d{deletion}_intersection_rank4_mode{mode}",
                (stacks0[mode],),
                c,
                zero_a * zero_b,
                size=4,
            )
        sign = 1 if deletion == 2 else -1
        gammas = (
            sp.Matrix((0, 0, sign, -sign, c[3])),
            sp.Matrix((0, 0, sign, -sign, c[2])),
        )
        assert stacks0[0] * gammas[0] == sp.zeros(16, 1)
        assert stacks0[1] * gammas[1] == sp.zeros(16, 1)
        assert (
            sp.factor(
                permanent4(
                    (tuple(gammas[0][:4]), tuple(gammas[1][:4]), beta[2], beta[3])
                )
            )
            == 4
        )
        results.append(f"{endpoint}:d{deletion}:intersection:forbidden4")
    return tuple(results)


def h22_projection_audit(endpoint, chart, alpha_branch):
    alpha, beta = endpoint_rows(endpoint)
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
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    return run_singular(
        f"audit_{endpoint}_{chart}_h22_A{alpha_branch}",
        program,
        f"RESULT:1:{len(expected)}",
    )


def h22_survivor_audit(endpoint, chart):
    alpha, beta = endpoint_rows(endpoint)
    marking = (0, 0, 0, p) if endpoint == "r_infinity" else (0, 0, p, 0)
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
    extension = sp.Matrix(
        (0, 0, 0, -1, 0, 1, 0, 0)
        if endpoint == "r_infinity"
        else (0, 0, -1, 0, 0, 1, 0, 0)
    )
    assert mixed.rank() == 7 and mixed * extension == sp.zeros(28, 1)
    diagonals_raw = tuple(
        sp.factor(
            sum(
                sp.diff(model[kind], variable) * extension[index]
                for index, variable in enumerate(x)
            )
        )
        for model in models
        for kind in ("A", "B")
    )
    diagonals = (diagonals_raw[0], diagonals_raw[2], diagonals_raw[1], diagonals_raw[3])
    expected = (
        (2 * k * (lam + 1), -2 * (lam - 1), 2 * p * (lam - 1), -2 * (lam + 1))
        if chart == "finite"
        else (2 * k, -2, 2 * p, -2)
    )
    assert all(sp.expand(left - right) == 0 for left, right in zip(diagonals, expected))
    alpha5 = tuple(tuple(alpha[index]) + (extension[index],) for index in range(4))
    marked5 = tuple(
        tuple(marked[index]) + (extension[4 + index],) for index in range(4)
    )
    contractions = (
        ((1, lam, 0, 0, 0), (0, 0, 1, lam, 0))
        if chart == "finite"
        else ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0))
    )
    gamma = sp.symbols("gamma0:5")
    equations = []
    for contraction in contractions:
        for word in itertools.product((0, 1), repeat=3):
            rows = []
            cursor = 0
            for mode in range(4):
                if mode == 1:
                    rows.append(gamma)
                else:
                    rows.append(marked5[mode] if word[cursor] else alpha5[mode])
                    cursor += 1
            equations.append(permanent5(tuple(rows) + (contraction,)))
    matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in gamma] for equation in equations]
    )
    rows = (0, 6, 7, 8, 14) if endpoint == "r_infinity" else (0, 5, 7, 8, 13)
    determinant = sp.factor(matrix.extract(rows, range(5)).det(method="domain-ge"))
    expected_det = (
        -8 * p * (lam - 1) ** 3 * (lam + 1) ** 2 if chart == "finite" else -8 * p
    )
    assert sp.expand(determinant - expected_det) == 0
    return f"{endpoint}:{chart}:rank7:gamma={determinant}"


def main():
    endpoints = ("r_infinity", "t_infinity")
    geometry = tuple(geometry_audit(endpoint) for endpoint in endpoints)
    h31_projections = tuple(
        h31_projection_audit(endpoint, deletion)
        for endpoint in endpoints
        for deletion in range(4)
    )
    h31 = tuple(h31_fibre_audit(endpoint) for endpoint in endpoints)
    h22_projections = tuple(
        h22_projection_audit(endpoint, chart, alpha_branch)
        for endpoint in endpoints
        for chart in ("finite", "infinity")
        for alpha_branch in (0, 1)
    )
    h22 = tuple(
        h22_survivor_audit(endpoint, chart)
        for endpoint in endpoints
        for chart in ("finite", "infinity")
    )
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "field": "Q",
                "scope": "no-import reconstruction of component-23 s=0 projective parameter endpoints",
                "geometry": geometry,
                "h31_projections": h31_projections,
                "h31": h31,
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
