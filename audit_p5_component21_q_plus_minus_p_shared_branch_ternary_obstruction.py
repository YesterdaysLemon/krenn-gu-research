#!/usr/bin/env python3
"""Independent no-import audit of the component-21 q=+/-p obstruction."""

from __future__ import annotations

import ast
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_Q_PLUS_MINUS_P_SHARED_BRANCH_TERNARY_OBSTRUCTION.md"
PRIMARY = (
    ROOT / "verify_p5_component21_q_plus_minus_p_shared_branch_ternary_obstruction.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def bases(p, q, kappa, ell):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    row_00 = add(cap_a, scale(p, cap_b))
    row_01 = add(cap_c, scale(q, cap_b))
    alpha = (
        add(scale(q, row_00), scale(-p, row_01)),
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    )
    beta = (
        row_00,
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
    )
    return alpha, beta


def shifted(beta, alpha, marking):
    return tuple(add(beta[i], scale(marking[i], alpha[i])) for i in range(4))


def project(row, extension, direction, chart, slope):
    if chart == "finite" and direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if chart == "finite" and direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if chart == "infinity" and direction == "D01":
        return (row[0], row[2], row[3], extension)
    if chart == "infinity" and direction == "D23":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def model(alpha, beta, extensions, direction, chart, slope=None):
    alpha_rows = tuple(
        project(alpha[i], extensions[i], direction, chart, slope) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extensions[4 + i], direction, chart, slope) for i in range(4)
    )
    coefficients = {
        word: permanent(
            tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in extensions]
            for word in WORDS[1:-1]
        ]
    )
    return {
        "alpha": alpha_rows,
        "beta": beta_rows,
        "coefficients": coefficients,
        "mixed": mixed,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def one_marked(mode, alpha, beta):
    rows = []
    for word in itertools.product((0, 1), repeat=3):
        selected = []
        cursor = 0
        for index in range(4):
            if index == mode:
                selected.append(None)
            else:
                selected.append(beta[index] if word[cursor] else alpha[index])
                cursor += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(
                permanent(
                    tuple(
                        basis if index == mode else selected[index]
                        for index in range(4)
                    )
                )
            )
        rows.append(row)
    return sp.Matrix(rows)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def exact_projection(sign, chart):
    p, kappa, ell = sp.symbols("p kappa ell")
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inv_a, inv_b = sp.symbols("u v")
    lam = sp.Symbol("lambda")
    alpha, canonical = bases(p, sign * p, kappa, ell)
    beta = shifted(canonical, alpha, h)
    slope = lam if chart == "finite" else None
    d01 = model(alpha, beta, z, "D01", chart, slope)
    d23 = model(alpha, beta, z, "D23", chart, slope)
    equations = (
        *(d01["coefficients"][word] for word in WORDS[:-1]),
        d01["B"] - 1,
        *tuple(d23["mixed"] * sp.Matrix(z)),
        inv_a * d23["A"] - 1,
        inv_b * d23["B"] - 1,
    )
    eliminated = z + (inv_a, inv_b)
    retained = h + ((lam,) if chart == "finite" else ())
    variables = eliminated + retained
    expected = (
        h[3],
        h[2] - sign * kappa,
        (ell + sign) * h[1] + 1,
        p * (ell + sign) * h[0] + sign * ell,
    )
    program = "\n".join(
        (
            "ring R=(0,p,kappa,ell),("
            + ",".join(map(str, variables))
            + f"),(dp(10),dp({len(retained)}));",
            "option(redSB);",
            "ideal I=" + ",".join(map(sg, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(sg, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            'print("AUDIT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J)));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        sign,
        chart,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("AUDIT:")
    ]
    assert markers == ["AUDIT:1:4"], (sign, chart, completed.stdout)
    return {"sign": sign, "chart": chart, "projection_equal": True}


def zero(expression):
    assert sp.factor(sp.cancel(expression)) == 0


def symbolic_certificate(sign, chart):
    p, kappa, ell, lam, cap_c = sp.symbols("p kappa ell lambda C0")
    z = sp.symbols("z0:8")
    alpha, canonical = bases(p, sign * p, kappa, ell)
    marking = (
        -sign * ell / (p * (ell + sign)),
        -1 / (ell + sign),
        sign * kappa,
        0,
    )
    beta = shifted(canonical, alpha, marking)
    slope = lam if chart == "finite" else None
    d01 = model(alpha, beta, z, "D01", chart, slope)
    d23 = model(alpha, beta, z, "D23", chart, slope)
    zero(d01["A"])
    equations = (
        *(d01["coefficients"][word] for word in WORDS[:-1]),
        *tuple(d23["mixed"] * sp.Matrix(z)),
    )
    matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in z] for equation in equations]
    )
    vector = sp.Matrix(
        (
            -sign * p * (ell + sign),
            0,
            sign * ell,
            0,
            0,
            sign,
            kappa * (ell - sign),
            0,
        )
    )
    assert all(sp.factor(value) == 0 for value in matrix * vector)
    columns = (0, 1, 2, 3, 4, 6, 7)
    if chart == "finite" and sign == 1:
        rows = (11, 14, 16, 17, 18, 22, 26)
        rank_values = (sp.factor(matrix.extract(rows, columns).det()),)
        zero(
            rank_values[0]
            - 512 * p**4 * (lam - 1) ** 4 * (lam + 1) * (ell - 1) / (ell + 1)
        )
    elif chart == "finite":
        rows_a = (11, 14, 16, 17, 18, 22, 26)
        rows_b = (10, 11, 16, 18, 22, 23, 26)
        rank_values = (
            sp.factor(matrix.extract(rows_a, columns).det()),
            sp.factor(matrix.extract(rows_b, columns).det()),
        )
        cap_h = lam * ell + lam + ell - 1
        zero(
            rank_values[0]
            + 512 * lam**2 * p**4 * (lam - 1) ** 4 * (lam + 1) * (ell + 1) / (ell - 1)
        )
        zero(
            rank_values[1]
            - 128 * p**4 * (lam - 1) ** 4 * (lam + 1) ** 2 * (ell + 1) * cap_h
        )
        zero(cap_h.subs(lam, 0) - (ell - 1))
    elif sign == 1:
        rows = (10, 11, 16, 18, 22, 23, 26)
        rank_values = (sp.factor(matrix.extract(rows, columns).det()),)
        zero(rank_values[0] - 128 * p**4 * (ell - 1) * (ell + 1))
    else:
        rows = (10, 11, 16, 17, 18, 22, 26)
        rank_values = (sp.factor(matrix.extract(rows, columns).det()),)
        zero(rank_values[0] + 256 * p**4 * (ell + 1) ** 2)

    substitution = dict(zip(z, cap_c * vector, strict=True))
    diagonals = tuple(
        sp.factor(expression.subs(substitution))
        for expression in (d01["B"], d23["A"], d23["B"])
    )
    cap_f = lam * ell + lam - ell + 1
    if chart == "finite":
        expected_diagonals = (
            2 * sign * cap_c * p * cap_f,
            2 * cap_c * p * (ell + sign) ** 2 * (lam - 1),
            -2 * cap_c * (ell - sign) * (lam + 1),
        )
        weight = (lam + 1) ** 3
    else:
        expected_diagonals = (
            2 * sign * cap_c * p * (ell + 1),
            2 * cap_c * p * (ell + sign) ** 2,
            -2 * cap_c * (ell - sign),
        )
        weight = 1
    for actual, expected in zip(diagonals, expected_diagonals, strict=True):
        zero(actual - expected)
    marked = one_marked(3, d23["alpha"], d23["beta"]).subs(substitution)
    minor = sp.factor(marked.extract((0, 1, 4, 7), range(4)).det())
    expected_minor = (
        8 * cap_c**3 * p**3 * (ell + sign) ** 3 * (ell - sign) ** 2 * weight
    )
    zero(minor - expected_minor)
    return {
        "sign": sign,
        "chart": chart,
        "rank_minor_values": [str(value) for value in rank_values],
        "diagonals": [str(value) for value in diagonals],
        "ternary_minor": str(minor),
    }


def main():
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero generic-divisor theorem",
        "both `ell=+/-1` intersections",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
        "No finite-field computation is used",
    ):
        assert phrase in theorem

    imports = {
        node.module.split(".")[0]
        for node in ast.walk(ast.parse(Path(__file__).read_text(encoding="utf-8")))
        if isinstance(node, ast.ImportFrom) and node.module
    } | {
        alias.name.split(".")[0]
        for node in ast.walk(ast.parse(Path(__file__).read_text(encoding="utf-8")))
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert imports <= {
        "__future__",
        "ast",
        "itertools",
        "json",
        "pathlib",
        "shutil",
        "subprocess",
        "sympy",
    }

    p, kappa, ell = sp.symbols("p kappa ell")
    supports = {}
    for sign in (1, -1):
        alpha, beta = bases(p, sign * p, kappa, ell)
        support = {
            word: sp.factor(
                permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
            )
            for word in WORDS
        }
        assert support[WORDS[-1]] == 4 * p
        assert all(value == 0 for word, value in support.items() if word != WORDS[-1])
        supports[str(sign)] = "T_1111=4*p only"

    jobs = [(sign, chart) for sign in (1, -1) for chart in ("finite", "infinity")]
    projections = [exact_projection(*job) for job in jobs]
    certificates = [symbolic_certificate(sign, chart) for sign, chart in jobs]

    completed = subprocess.run(
        ("uv", "run", "--with", "sympy", "python", str(PRIMARY)),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=420,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    replay = json.loads(completed.stdout)
    assert replay["status"] == "pass"
    assert replay["generic_q_sign_divisor_H22_empty"] is True
    assert replay["ell_plus_minus_one_intersections_closed"] is False
    assert replay["finite_field_proof_used"] is False
    assert replay["global_conjecture_resolved"] is False

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import characteristic-zero audit",
                "repository_imports_used": False,
                "pure_supports": supports,
                "independent_projections": projections,
                "independent_symbolic_certificates": certificates,
                "primary_replay": "pass",
                "generic_q_sign_divisor_H22_empty": True,
                "displayed_branch_obstructed_at_kappa_zero": True,
                "ell_plus_minus_one_intersections_closed": False,
                "all_kappa_zero_specialization_branches_classified": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
