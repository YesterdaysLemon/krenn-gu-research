#!/usr/bin/env python3
"""Independent no-repository-import audit of component-21 ell endpoints."""

from __future__ import annotations

import ast
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_Q_PLUS_MINUS_P_ELL_ENDPOINT_COMPLETE_OBSTRUCTION.md"
PRIMARY = (
    ROOT / "verify_p5_component21_q_plus_minus_p_ell_endpoint_complete_obstruction.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def bases(p, q, kappa, ell):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    row_00 = add(cap_a, scale(p, cap_b))
    row_01 = add(cap_c, scale(q, cap_b))
    return (
        (
            add(scale(q, row_00), scale(-p, row_01)),
            add(scale(ell, cap_a), cap_c),
            cap_c,
            cap_d,
        ),
        (
            row_00,
            cap_a,
            add(cap_b, scale(kappa, cap_a)),
            add(cap_a, scale(ell, cap_c)),
        ),
    )


def shifted(beta, alpha, marking):
    return tuple(
        add(beta[index], scale(marking[index], alpha[index])) for index in range(4)
    )


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
        project(alpha[index], extensions[index], direction, chart, slope)
        for index in range(4)
    )
    beta_rows = tuple(
        project(beta[index], extensions[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {
        word: permanent(
            tuple(
                beta_rows[index] if word[index] else alpha_rows[index]
                for index in range(4)
            )
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
    result = []
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
        result.append(row)
    return sp.Matrix(result)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def projection(sign, side, chart, kappa_zero):
    p, kappa = sp.symbols("p kappa")
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inv_a, inv_b = sp.symbols("u v")
    lam = sp.Symbol("lambda")
    ell = sign if side == "same" else -sign
    active_kappa = 0 if kappa_zero else kappa
    alpha, canonical = bases(p, sign * p, active_kappa, ell)
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
    if side == "same" and not kappa_zero:
        expected = (h[3], 2 * h[1] + sign, 2 * p * h[0] + sign)
    elif side == "same":
        expected = (h[3], h[2], 2 * h[1] + sign, 2 * p * h[0] + sign)
    elif not kappa_zero:
        expected = (h[3], h[2] + sign * kappa, h[1], 2 * p * h[0] + sign)
    else:
        expected = (h[3], h[2], h[1])
    field = "p" if kappa_zero else "p,kappa"
    program = "\n".join(
        (
            f"ring R=(0,{field}),("
            + ",".join(map(str, variables))
            + f"),(dp(10),dp({len(retained)}));",
            "option(redSB);",
            "ideal I=" + ",".join(map(sg, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(sg, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
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
        timeout=360,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        sign,
        side,
        chart,
        kappa_zero,
        completed.stdout,
        completed.stderr,
    )
    expected_marker = f"AUDIT:1:{len(expected)}"
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("AUDIT:")
    ]
    assert markers == [expected_marker], (
        sign,
        side,
        chart,
        kappa_zero,
        completed.stdout,
    )
    return {"sign": sign, "side": side, "chart": chart, "kappa_zero": kappa_zero}


def common_matrix(d01, d23, extensions):
    equations = (
        *(d01["coefficients"][word] for word in WORDS[:-1]),
        *tuple(d23["mixed"] * sp.Matrix(extensions)),
    )
    return sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in extensions]
            for equation in equations
        ]
    )


def complete_kernel(matrix, vectors, label):
    for vector in vectors:
        assert all(sp.factor(value) == 0 for value in matrix * vector), label
    assert sp.Matrix.hstack(*vectors).rank() == len(vectors), label
    assert len(matrix.nullspace()) == len(vectors), label


def zero(expression, label):
    assert sp.factor(sp.cancel(expression)) == 0, label


def symbolic_case(sign, side, chart, kappa_zero):
    p, kappa, t, r, lam, cap_c, cap_x, cap_y = sp.symbols("p kappa t r lambda C X Y")
    z = sp.symbols("z0:8")
    slope = lam if chart == "finite" else None
    if side == "same" and not kappa_zero:
        alpha, canonical = bases(p, sign * p, kappa, sign)
        beta = shifted(
            canonical,
            alpha,
            (-sign / (2 * p), -sp.Rational(sign, 2), t, 0),
        )
        d = t - sign * kappa
        vectors = (
            sp.Matrix(
                (
                    -2 * sign * p * (t + sign * kappa),
                    -2 * sign * d,
                    2 * kappa,
                    0,
                    d,
                    t + sign * kappa,
                    0,
                    2 * d,
                )
            ),
        )
        expected_minor = (
            sign
            * 512
            * cap_c**3
            * kappa
            * p**3
            * d**2
            * ((lam + 1) ** 3 if chart == "finite" else 1)
        )
        rows = (0, 1, 4, 7)
    elif side == "same":
        alpha, canonical = bases(p, sign * p, 0, sign)
        beta = shifted(
            canonical,
            alpha,
            (-sign / (2 * p), -sp.Rational(sign, 2), 0, 0),
        )
        vector_x = sp.Matrix((-2 * sign * p, 0, sign, 0, 0, 1, 0, 0))
        vector_y = sp.Matrix(
            (0, -sign, -sp.Rational(sign, 2), 0, sp.Rational(1, 2), 0, 0, 1)
        )
        vectors = (vector_x, vector_y)
        expected_minor = (
            32
            * cap_y**2
            * p**3
            * (2 * cap_x - cap_y)
            * ((lam + 1) ** 3 if chart == "finite" else 1)
        )
        rows = (0, 1, 4, 7)
    elif not kappa_zero:
        alpha, canonical = bases(p, sign * p, kappa, -sign)
        beta = shifted(canonical, alpha, (-sign / (2 * p), 0, -sign * kappa, 0))
        vectors = (sp.Matrix((-sign * p, sign, 0, 0, -sp.Rational(1, 2), 0, kappa, 1)),)
        expected_minor = (
            -sign
            * 64
            * cap_c**3
            * kappa
            * p**4
            * ((lam + 1) ** 3 if chart == "finite" else 1)
        )
        rows = (0, 1, 3, 7)
    else:
        alpha, canonical = bases(p, sign * p, 0, -sign)
        beta = shifted(canonical, alpha, (r, 0, 0, 0))
        vectors = (sp.Matrix((-sign * p, sign, 0, 0, sign * p * r, 0, 0, 1)),)
        expected_minor = (
            -32
            * cap_c**3
            * p**3
            * (2 * p * r + sign)
            * ((lam + 1) ** 3 if chart == "finite" else 1)
        )
        rows = (0, 1, 3, 7)
    d01 = model(alpha, beta, z, "D01", chart, slope)
    d23 = model(alpha, beta, z, "D23", chart, slope)
    matrix = common_matrix(d01, d23, z)
    complete_kernel(matrix, vectors, (sign, side, chart, kappa_zero))
    if side == "same" and not kappa_zero:
        vector = cap_c * vectors[0]
    elif side == "same":
        vector = cap_x * vectors[0] + cap_y * vectors[1]
    else:
        vector = cap_c * vectors[0]
    substitution = dict(zip(z, vector, strict=True))
    marked = one_marked(3, d23["alpha"], d23["beta"]).subs(substitution)
    determinant = sp.factor(marked.extract(rows, range(4)).det())
    zero(determinant - expected_minor, (sign, side, chart, kappa_zero, "minor"))

    diagonals = tuple(
        sp.factor(value.subs(substitution)) for value in (d01["B"], d23["A"], d23["B"])
    )
    if side == "same" and not kappa_zero:
        d = t - sign * kappa
        if chart == "finite":
            expected_diagonals = (
                4 * cap_c * p * (kappa * (lam - 1) + t * (lam + 1)),
                16 * cap_c * kappa * p * (lam - 1),
                4 * cap_c * d * (lam + 1),
            )
        else:
            expected_diagonals = (
                4 * cap_c * p * (t + kappa),
                16 * cap_c * kappa * p,
                4 * cap_c * d,
            )
    elif side == "same" and chart == "finite" and sign == 1:
        expected_diagonals = (
            2 * p * (2 * cap_x * lam + cap_y),
            4 * p * (2 * cap_x - cap_y) * (lam - 1),
            2 * cap_y * (lam + 1),
        )
    elif side == "same" and chart == "finite":
        expected_diagonals = (
            2 * p * (2 * cap_x + cap_y * lam),
            -4 * p * (2 * cap_x - cap_y) * (lam - 1),
            2 * cap_y * (lam + 1),
        )
    elif side == "same" and sign == 1:
        expected_diagonals = (
            4 * cap_x * p,
            4 * p * (2 * cap_x - cap_y),
            2 * cap_y,
        )
    elif side == "same":
        expected_diagonals = (
            2 * cap_y * p,
            -4 * p * (2 * cap_x - cap_y),
            2 * cap_y,
        )
    elif not kappa_zero:
        weight = lam + 1 if chart == "finite" else 1
        expected_diagonals = (
            2 * cap_c * p * weight,
            4 * sign * cap_c * p * ((lam - 1) if chart == "finite" else 1),
            4 * cap_c * kappa * p * weight,
        )
    else:
        weight = lam + 1 if chart == "finite" else 1
        expected_diagonals = (
            2 * cap_c * p * weight,
            4 * sign * cap_c * p * ((lam - 1) if chart == "finite" else 1),
            2 * sign * cap_c * weight * (2 * p * r + sign),
        )
    for actual, expected in zip(diagonals, expected_diagonals, strict=True):
        zero(actual - expected, (sign, side, chart, kappa_zero, "diagonal"))

    if side == "same" and not kappa_zero:
        special_beta = shifted(
            canonical,
            alpha,
            (-sign / (2 * p), -sp.Rational(sign, 2), sign * kappa, 0),
        )
        special_d01 = model(alpha, special_beta, z, "D01", chart, slope)
        special_d23 = model(alpha, special_beta, z, "D23", chart, slope)
        special_matrix = common_matrix(special_d01, special_d23, z)
        special_vector = sp.Matrix((-2 * p, 0, 1, 0, 0, sign, 0, 0))
        complete_kernel(special_matrix, (special_vector,), (sign, "d=0", chart))
        special_substitution = dict(zip(z, cap_c * special_vector, strict=True))
        zero(special_d23["B"].subs(special_substitution), (sign, "d=0 B23", chart))

    if chart == "finite" and (
        (side == "same" and sign == 1) or (side == "opposite" and sign == -1)
    ):
        matrix_zero_weight = matrix.subs(lam, 0)
        complete_kernel(
            matrix_zero_weight, vectors, (sign, side, "lambda=0", kappa_zero)
        )
    return {
        "sign": sign,
        "side": side,
        "chart": chart,
        "kappa_zero": kappa_zero,
        "kernel_dimension": len(vectors),
        "kernel_complete": True,
        "diagonals": [str(value) for value in diagonals],
        "ternary_minor": str(determinant),
    }


def main():
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero endpoint theorem",
        "zero-basis degeneration of the displayed chart",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
        "all sixteen saturated eliminations",
    ):
        assert phrase in theorem
    source = Path(__file__).read_text(encoding="utf-8")
    imports = {
        node.module.split(".")[0]
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.ImportFrom) and node.module
    } | {
        alias.name.split(".")[0]
        for node in ast.walk(ast.parse(source))
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

    kappa, ell = sp.symbols("kappa ell")
    zero_alpha, zero_beta = bases(0, 0, kappa, ell)
    assert zero_alpha[0] == (0, 0, 0, 0)
    assert all(
        permanent(
            tuple(
                zero_beta[index] if word[index] else zero_alpha[index]
                for index in range(4)
            )
        )
        == 0
        for word in WORDS
    )

    jobs = [
        (sign, side, chart, kappa_zero)
        for sign in (1, -1)
        for side in ("same", "opposite")
        for chart in ("finite", "infinity")
        for kappa_zero in (False, True)
    ]
    projections = [projection(*job) for job in jobs]
    certificates = [symbolic_case(*job) for job in jobs]
    completed = subprocess.run(
        ("uv", "run", "--with", "sympy", "python", str(PRIMARY)),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=1200,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    replay = json.loads(completed.stdout)
    assert replay["status"] == "pass"
    assert replay["ell_endpoint_H22_fibres_empty_for_p_nonzero"] is True
    assert replay["raw_p_equals_q_equals_zero_chart_pure_coefficients"] == "all zero"
    assert replay["p_equals_q_equals_zero_closed"] is False
    assert replay["finite_field_proof_used"] is False
    assert replay["global_conjecture_resolved"] is False
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-repository-import characteristic-zero audit",
                "repository_imports_used": False,
                "projection_certificates": projections,
                "symbolic_certificates": certificates,
                "primary_replay": "pass",
                "ell_endpoint_H22_fibres_empty_for_p_nonzero": True,
                "raw_p_equals_q_equals_zero_chart_pure_coefficients": "all zero",
                "p_equals_q_equals_zero_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
