#!/usr/bin/env python3
"""No-repository-import audit of the component-23 s=1 infinity curves."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import sys
from pathlib import Path

import sympy as sp

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "verify_p5_component23_s_one_parameter_infinity_curves_obstruction.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))
PERM3 = tuple(itertools.permutations(range(3)))
PERM4 = tuple(itertools.permutations(range(4)))

k, lam, inverse = sp.symbols("k lam u")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
w, z = sp.symbols("w z")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def curve_rows(curve):
    beta = (B, add(B, C), C, C)
    if curve == "Dr":
        alpha = (
            A,
            add(A, scale(k, D)),
            D,
            add(scale(-1, A), scale(-1, C), B, scale(k, D)),
        )
    else:
        alpha = (A, add(A, scale(k, D)), add(A, scale(-1, C), B, scale(-k, D)), D)
    return alpha, beta


def shifted(alpha, beta, marking=h):
    return tuple(add(beta[i], scale(marking[i], alpha[i])) for i in range(4))


def permanent4(rows):
    return sp.expand(
        sum(sp.prod(rows[i][permutation[i]] for i in range(4)) for permutation in PERM4)
    )


def permanent3(rows):
    return sp.expand(
        sum(sp.prod(rows[i][permutation[i]] for i in range(3)) for permutation in PERM3)
    )


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(*(symmetric_product(a, b) for a in left for b in right))


def pure_pair_and_involution_audit():
    reports = []
    for curve in ("Dr", "Dt"):
        alpha, beta = curve_rows(curve)
        coefficients = {
            word: sp.factor(
                permanent4(
                    tuple(
                        alpha[i] if bit == 0 else beta[i] for i, bit in enumerate(word)
                    )
                )
            )
            for word in WORDS
        }
        assert coefficients[(1, 1, 1, 1)] == -4
        assert all(
            value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
        )
        assert all(sp.Matrix((alpha[i], beta[i])).rank() == 2 for i in range(4))
        planes = tuple((alpha[i], beta[i]) for i in range(4))
        matrices = tuple(pair_matrix(planes[i], planes[j]) for i, j in PAIRS)
        profile = (3, 2, 3, 3, 4, 4) if curve == "Dr" else (3, 3, 2, 4, 3, 4)
        special = (3, 2, 3, 3, 3, 4) if curve == "Dr" else (3, 3, 2, 3, 3, 4)
        assert tuple(matrix.rank() for matrix in matrices) == profile
        assert all(
            tuple(matrix.subs(k, value).rank() for matrix in matrices) == special
            for value in (0, 1, -1)
        )
        edge = 4 if curve == "Dr" else 3
        minors = [
            sp.factor(matrices[edge].extract(rows, range(4)).det())
            for rows in itertools.combinations(range(6), 4)
        ]
        minors = [value for value in minors if value != 0]
        assert sp.factor(sp.gcd_list(minors) - 8 * k * (k - 1) * (k + 1)) == 0
        rank_two = 1 if curve == "Dr" else 2
        assert matrices[rank_two].nullspace() == [
            sp.Matrix((0, 1, 0, 0)),
            sp.Matrix((0, 0, 1, 0)),
        ]
        reports.append((curve, profile, special))

    dr_alpha, dr_beta = curve_rows("Dr")
    dt_alpha, dt_beta = curve_rows("Dt")
    involution = lambda row: (-row[1], -row[0], row[3], row[2])
    order, signs = (0, 1, 3, 2), (-1, -1, 1, -1)
    assert all(
        involution(dr_alpha[order[i]]) == scale(signs[i], dt_alpha[i]) for i in range(4)
    )
    assert all(involution(dr_beta[order[i]]) == dt_beta[i] for i in range(4))
    v = sp.symbols("v0:4")
    moved = involution(v)
    assert sp.factor((moved[0] / lam + moved[1]) + (lam * v[0] + v[1]) / lam) == 0
    assert sp.factor((moved[2] / lam + moved[3]) - (lam * v[2] + v[3]) / lam) == 0
    return reports


def extension_coefficients(deletion, alpha, beta, extension):
    common = tuple(index for index in range(4) if index != deletion)
    alpha_p = tuple(
        tuple(alpha[i][coordinate] for coordinate in common) + (extension[i],)
        for i in range(4)
    )
    beta_p = tuple(
        tuple(beta[i][coordinate] for coordinate in common) + (extension[4 + i],)
        for i in range(4)
    )
    return {
        bits: permanent4(
            tuple(alpha_p[i] if bit == 0 else beta_p[i] for i, bit in enumerate(bits))
        )
        for bits in WORDS
    }


def mixed_matrix(deletion, alpha, beta):
    coefficients = extension_coefficients(deletion, alpha, beta, sp.Matrix(x))
    mixed = sp.Matrix(
        [[sp.diff(coefficients[word], variable) for variable in x] for word in MIXED]
    )
    diagonals = tuple(
        sp.Matrix([[sp.diff(coefficients[word], variable) for variable in x]])
        for word in (WORDS[0], WORDS[-1])
    )
    return mixed, *diagonals


def one_marked_map(mode, alpha, beta):
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected, cursor = [], 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        rows.append(
            [
                permanent4(
                    tuple(
                        tuple(int(j == coordinate) for j in range(4))
                        if other == mode
                        else selected[other]
                        for other in range(4)
                    )
                )
                for coordinate in range(4)
            ]
        )
    return sp.Matrix(rows)


def marked_extension(deletion, extension, alpha, beta, mode):
    common = tuple(index for index in range(4) if index != deletion)
    alpha_p = tuple(
        tuple(alpha[i][coordinate] for coordinate in common) + (extension[i],)
        for i in range(4)
    )
    beta_p = tuple(
        tuple(beta[i][coordinate] for coordinate in common) + (extension[4 + i],)
        for i in range(4)
    )
    return one_marked_map(mode, alpha_p, beta_p)


def global_one_marked(deletion, extension, alpha, beta):
    pure = one_marked_map(1, alpha, beta).row_join(sp.zeros(8, 1))
    neighbour = marked_extension(deletion, extension, alpha, beta, 1)
    embedded = sp.zeros(8, 5)
    for column, coordinate in enumerate(
        index for index in range(4) if index != deletion
    ):
        embedded[:, coordinate] = neighbour[:, column]
    embedded[:, 4] = neighbour[:, 3]
    return pure.col_join(embedded)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


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


EXPECTED_PROJECTIONS = {
    0: (h[3], h[1] - 1, h[0], (k**2 - 1) * h[2]),
    1: (h[3], h[1] - 1, h[0], (k**2 - 1) * h[2]),
    2: (h[2] - h[3], h[1] - 1, h[0], h[3] ** 2 - h[3], k * h[3] - h[3]),
    3: (h[2] + h[3], h[1] - 1, h[0], h[3] ** 2 - h[3], k * h[3] + h[3]),
}


def projection_audit():
    alpha, beta = curve_rows("Dr")
    marked = shifted(alpha, beta)
    output = []
    for deletion in range(4):
        mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
        vector = sp.Matrix(x)
        equations = (
            *tuple(mixed * vector),
            (diagonal_a * vector)[0] - 1,
            w * (diagonal_b * vector)[0] - 1,
        )
        eliminated, variables = x + (w,), x + (w, k) + h
        expected = EXPECTED_PROJECTIONS[deletion]
        program = "\n".join(
            (
                "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(5));",
                "option(redSB);",
                "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
                "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
                "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
                "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
                'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J)));',
                "quit;",
            )
        )
        run_singular(f"projection {deletion}", program, f"RESULT:1:{len(expected)}")
        output.append(deletion)

    for deletion in (0, 1):
        mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
        vector = sp.Matrix(x)
        equations = tuple(
            value.subs(k, 0)
            for value in (
                *tuple(mixed * vector),
                (diagonal_a * vector)[0] - 1,
                w * (diagonal_b * vector)[0] - 1,
            )
        )
        eliminated, variables = x + (w,), x + (w,) + h
        program = "\n".join(
            (
                "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
                "option(redSB);",
                "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
                "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
                'print("RESULT:"+string(reduce(1,J)==0)+":"+string(size(J)));',
                "quit;",
            )
        )
        run_singular(f"k0 {deletion}", program, "RESULT:1:1")
    return output


def branch_audit():
    cases = [
        (f"generic_d{deletion}", deletion, (0, 1, 0, 0), {}) for deletion in range(4)
    ]
    cases += [
        (f"k_{sign}_z_d{deletion}", deletion, (0, 1, z, 0), {k: sign})
        for sign in (1, -1)
        for deletion in (0, 1)
    ]
    cases += [
        ("extra_plus", 2, (0, 1, 1, 1), {k: 1}),
        ("extra_minus", 3, (0, 1, -1, 1), {k: -1}),
    ]
    alpha0, beta = curve_rows("Dr")
    output = []
    for label, deletion, marking, substitutions in cases:
        alpha = tuple(
            tuple(sp.sympify(value).subs(substitutions) for value in row)
            for row in alpha0
        )
        marked = shifted(alpha, beta, marking)
        mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
        assert mixed.rank() == 6
        frame = mixed.nullspace()
        assert len(frame) == 2 and sp.Matrix.hstack(*frame).rank() == 2
        c0, c1 = sp.symbols("c0 c1")
        extension = frame[0] * c0 + frame[1] * c1
        actual_a = sp.factor((diagonal_a * extension)[0])
        actual_b = sp.factor((diagonal_b * extension)[0])
        determinant = sp.factor(
            global_one_marked(deletion, extension, alpha, marked)
            .extract((0, 6, 7, 8, 14), range(5))
            .det(method="domain-ge")
        )
        sign = 1 if deletion == 0 else -1
        assert sp.factor(determinant - sign * 32 * actual_a) == 0
        output.append((label, str(actual_a), str(actual_b), str(determinant)))
    return output


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
    alpha_p = tuple(project(alpha[i], x[i], direction, chart, slope) for i in range(4))
    beta_p = tuple(
        project(beta[i], x[4 + i], direction, chart, slope) for i in range(4)
    )
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
    return {
        "mixed": tuple(coefficients[word] for word in MIXED),
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def coefficient_row(expression):
    return (
        "["
        + ",".join(singular_text(sp.diff(expression, variable)) for variable in x)
        + "]"
    )


EXPECTED = {
    "Dr": {
        "l1nz": (
            "gen(1)",
            "gen(2)",
            "gen(3)",
            "gen(6)-gen(4)",
            "gen(7)",
            "gen(8)",
            "h3*gen(4)",
            "h2*gen(4)",
            "(h1+1)*gen(4)",
            "h0*gen(4)",
        ),
        "l1z": ("gen(1)", "gen(2)", "gen(3)", "gen(6)-gen(4)", "gen(7)"),
        "lm1": (
            "gen(1)",
            "gen(2)",
            "gen(3)",
            "gen(5)",
            "gen(6)+gen(4)",
            "gen(8)",
            "h3*gen(4)",
            "h2*gen(4)",
            "(h1+1)*gen(4)",
            "h0*gen(4)",
        ),
    },
    "Dt": {
        "l1nz": (
            "gen(1)",
            "gen(2)",
            "gen(4)",
            "gen(6)-gen(3)",
            "gen(7)",
            "gen(8)",
            "h3*gen(3)",
            "h2*gen(3)",
            "(h1-1)*gen(3)",
            "h0*gen(3)",
        ),
        "l1z": ("gen(1)", "gen(2)", "gen(4)", "gen(6)-gen(3)", "gen(8)"),
        "lm1": (
            "gen(1)",
            "gen(2)",
            "gen(4)",
            "gen(5)",
            "gen(6)+gen(3)",
            "gen(7)",
            "h3*gen(3)",
            "h2*gen(3)",
            "(h1-1)*gen(3)",
            "h0*gen(3)",
        ),
    },
}


def h22_case(curve, case):
    alpha, beta = curve_rows(curve)
    marked = shifted(alpha, beta)
    if case == "generic":
        chart, slope, substitutions, localizer = (
            "finite",
            lam,
            {},
            (lam - 1) * (lam + 1),
        )
        expected, membership = tuple(f"gen({i})" for i in range(1, 9)), (1, 1, 1, 1)
    elif case == "l1nz":
        chart, slope, substitutions, localizer = "finite", sp.Integer(1), {}, k
        expected, membership = EXPECTED[curve][case], (0, 1, 1, 0)
    elif case == "l1z":
        chart, slope, substitutions, localizer = (
            "finite",
            sp.Integer(1),
            {k: 0},
            sp.Integer(1),
        )
        expected, membership = EXPECTED[curve][case], (1, 1, 1, 0)
    elif case == "lm1":
        chart, slope, substitutions, localizer = (
            "finite",
            sp.Integer(-1),
            {},
            sp.Integer(1),
        )
        expected, membership = EXPECTED[curve][case], (1, 0, 0, 1)
    else:
        chart, slope, substitutions, localizer = "infinity", None, {}, sp.Integer(1)
        expected, membership = tuple(f"gen({i})" for i in range(1, 9)), (1, 1, 1, 1)
    models = tuple(
        build_model(alpha, marked, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    generators = ",".join(
        coefficient_row(expression.subs(substitutions, simultaneous=True))
        for model in models
        for expression in model["mixed"]
    )
    diagonals = tuple(
        coefficient_row(model[key].subs(substitutions, simultaneous=True))
        for model in models
        for key in ("A", "B")
    )
    variables = (
        (() if k in substitutions else (k,))
        + h
        + ((lam,) if slope == lam else ())
        + (inverse,)
    )
    program = "\n".join(
        (
            "ring P=0,(" + ",".join(map(str, variables)) + "),dp;",
            "ideal Q=u*(" + singular_text(localizer) + ")-1; Q=std(Q); qring R=Q;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + ",".join(expected) + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2); module EM=simplify(reduce(E,M),2);",
            *(f"vector d{i}={value};" for i, value in enumerate(diagonals)),
            *(f"int z{i}=reduce(d{i},M)==0;" for i in range(4)),
            'print("RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"+string(z0)+":"+string(z1)+":"+string(z2)+":"+string(z3)+":"+string(size(M)));',
            "quit;",
        )
    )
    marker = "RESULT:1:" + ":".join(map(str, membership)) + f":{len(expected)}"
    run_singular(f"{curve} {case}", program, marker)
    return (curve, case, membership)


def main():
    geometry = pure_pair_and_involution_audit()
    projections = projection_audit()
    branches = branch_audit()
    modules = tuple(
        h22_case(curve, case)
        for curve in ("Dr", "Dt")
        for case in ("generic", "l1nz", "l1z", "lm1", "infinity")
    )
    replay = subprocess.run(
        (sys.executable, str(PRIMARY)),
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=360,
        check=False,
    )
    assert replay.returncode == 0, (replay.stdout, replay.stderr)
    primary_payload = json.loads(replay.stdout)
    assert primary_payload["status"] == "pass"
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "repository_imports_used": False,
                "geometry": geometry,
                "projection_insertions": projections,
                "branch_certificates": branches,
                "h22_module_cases": modules,
                "primary_replay": "pass",
                "marked_H31_empty": True,
                "weighted_H22_empty": True,
                "triple_parameter_infinity_included": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
