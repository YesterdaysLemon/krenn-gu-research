#!/usr/bin/env python3
"""No-import audit of component 23's k=infinity lower-pair endpoints."""

from __future__ import annotations

import functools
import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))

h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
lam = sp.Symbol("lam")
w = sp.Symbol("w")

EXPECTED_MARKINGS = {
    1: {
        0: (0, 1, sp.Rational(1, 2), 0),
        1: (0, 1, 0, sp.Rational(1, 2)),
        2: (0, 1, sp.Rational(1, 2), sp.Rational(1, 2)),
        3: None,
    },
    -1: {
        0: (0, -1, sp.Rational(1, 2), 0),
        1: (0, -1, 0, sp.Rational(1, 2)),
        2: None,
        3: (0, -1, sp.Rational(1, 2), sp.Rational(1, 2)),
    },
}

FINITE_EXPECTED_MODULE = {
    1: (
        "gen(1)",
        "gen(4)-gen(3)",
        "gen(7)",
        "gen(8)",
        "lam*gen(2)",
        "(lam-1)*gen(3)",
        "(lam-1)*gen(5)+gen(2)",
        "lam*gen(6)-gen(3)",
        "h3*gen(3)",
        "h2*gen(3)",
        "(h1-1)*gen(2)-gen(6)+gen(3)",
        "(h1-1)*gen(3)",
        "h0*gen(3)",
    ),
    -1: (
        "gen(1)",
        "gen(2)",
        "gen(4)-gen(3)",
        "gen(6)-gen(3)",
        "gen(7)",
        "gen(8)",
        "(lam-1)*gen(3)",
        "(lam-1)*gen(5)",
        "h3*gen(3)",
        "h2*gen(3)",
        "(h1+1)*gen(3)",
        "h0*gen(3)",
    ),
}

INFINITY_EXPECTED_MODULE = {
    1: tuple(f"gen({index})" for index in range(1, 9)),
    -1: (
        "gen(1)",
        "gen(3)",
        "gen(4)",
        "gen(5)+gen(2)",
        "gen(7)",
        "gen(8)",
        "(h1+1)*gen(2)-gen(6)",
    ),
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


def run_singular(label, program, expected, timeout=180):
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


def add(left, right, coefficient=1):
    return tuple(
        sp.expand(left[index] + coefficient * right[index]) for index in range(4)
    )


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def endpoint_rows(sign):
    sign = sp.Integer(sign)
    cap_a = (sp.Integer(1), 1, 0, 0)
    cap_c = (sp.Integer(1), -1, 0, 0)
    cap_b = (0, 0, sp.Integer(1), 1)
    cap_d = (0, 0, sp.Integer(1), -1)
    alpha = (
        cap_a,
        cap_d,
        add(add(cap_a, cap_c, -1), add(cap_b, cap_d, sign)),
        add(add(scale(-1, cap_a), cap_c, -1), add(cap_b, cap_d, sign)),
    )
    beta = (cap_b, add(cap_b, cap_c), cap_c, cap_c)
    return alpha, beta


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


def same_plane(left, right):
    return left.row_join(right).rank() == 2


def geometry_audit(sign):
    alpha, beta = endpoint_rows(sign)
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    profile = tuple(
        pair_matrix(planes[left], planes[right]).rank() for left, right in PAIRS
    )
    assert profile == (3, 3, 3, 4, 4, 2)
    kernel = pair_matrix(planes[2], planes[3]).nullspace()
    assert len(kernel) == 2
    assert all(sp.Matrix(2, 2, tuple(vector)).rank() == 1 for vector in kernel)

    zero_factors = (
        (alpha[2], add(scale(sp.Rational(1, 2), alpha[3]), beta[3])),
        (add(scale(sp.Rational(1, 2), alpha[2]), beta[2]), alpha[3]),
    )
    support_pairs = tuple(
        frozenset(index for index, value in enumerate(left) if value != 0)
        for left, _ in zero_factors
    )
    expected = (
        (frozenset((1, 2)), frozenset((0, 2)))
        if sign == 1
        else (frozenset((1, 3)), frozenset((0, 3)))
    )
    assert support_pairs == expected
    assert all(
        symmetric_product(left, right) == sp.zeros(6, 1) for left, right in zero_factors
    )

    source_order = (2, 1, 0, 3) if sign == 1 else (3, 1, 0, 2)
    moved = tuple(
        sp.Matrix(
            [
                [planes[mode][row][coordinate] for coordinate in source_order]
                for row in range(2)
            ]
        )
        for mode in range(4)
    )
    y0 = sp.Matrix((1, 0, 0, 0))
    y1 = sp.Matrix((0, 1, 0, 0))
    y2 = sp.Matrix((0, 0, 1, 0))
    zed = sp.Matrix((0, 0, 0, 1))
    a = y0 + y1
    a_bar = y0 - y1
    b = y0 + y2
    b_bar = y0 - y2
    c = y1 + y2
    normal = (
        sp.Matrix.vstack(a.T, b.T),
        sp.Matrix.vstack(a_bar.T, b_bar.T),
        sp.Matrix.vstack(c.T, (a + 2 * zed + a_bar).T),
        sp.Matrix.vstack((c + 2 * a_bar).T, (a - 2 * zed + a_bar).T),
    )
    reordered = tuple(moved[index] for index in (2, 3, 0, 1))
    assert all(same_plane(left, right) for left, right in zip(reordered, normal))

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
    assert coefficients[(1, 1, 1, 1)] == -4
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )
    projective_markings = tuple(
        coefficients[tuple(0 if index == mode else 1 for index in range(4))]
        for mode in range(4)
    )
    assert projective_markings == (0, 0, 0, 0)
    return {
        "sign": sign,
        "profile": profile,
        "support_pairs": tuple(tuple(sorted(value)) for value in support_pairs),
        "source_order": source_order,
        "projective_marking_coefficients": tuple(map(str, projective_markings)),
    }


def shifted_beta(alpha, beta, marking):
    return tuple(add(beta[index], alpha[index], marking[index]) for index in range(4))


def h31_coefficients(deletion, alpha, beta, extension):
    common = tuple(index for index in range(4) if index != deletion)
    coefficients = {}
    for word in WORDS:
        rows = []
        for mode in range(4):
            row = beta[mode] if word[mode] else alpha[mode]
            extension_index = 4 + mode if word[mode] else mode
            rows.append(
                tuple(row[index] for index in common) + (extension[extension_index],)
            )
        coefficients[word] = permanent4(tuple(rows))
    return coefficients


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
    for bits in itertools.product((0, 1), repeat=3):
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[bit_index] else alpha[other])
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            coefficient_row.append(
                permanent4(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def marked_extension(deletion, extension, alpha, beta, mode):
    common = tuple(index for index in range(4) if index != deletion)
    alpha_projected = tuple(
        tuple(alpha[row][index] for index in common) + (extension[row],)
        for row in range(4)
    )
    beta_projected = tuple(
        tuple(beta[row][index] for index in common) + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(mode, alpha_projected, beta_projected)


def projection_audit(sign, deletion):
    alpha, beta = endpoint_rows(sign)
    marked = shifted_beta(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, marked)
    extension = sp.Matrix(x)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        w * (diagonal_b * extension)[0] - 1,
    )
    marking = EXPECTED_MARKINGS[sign][deletion]
    expected = (
        (sp.Integer(1),)
        if marking is None
        else tuple(h[index] - marking[index] for index in range(4))
    )
    eliminated = x + (w,)
    variables = eliminated + h
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    label = f"audit_r_{sign}_deletion_{deletion}_projection"
    run_singular(label, program, f"RESULT:1:{len(expected)}")
    return label


def h31_minor_audit(sign, deletion, marking):
    alpha, beta = endpoint_rows(sign)
    marked = shifted_beta(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = h31_mixed_matrix(deletion, alpha, marked)
    assert mixed.rank() == 5
    kernel = mixed.nullspace()
    assert len(kernel) == 3
    coefficients = sp.symbols("c0:3")
    extension = sp.Matrix.hstack(*kernel) * sp.Matrix(coefficients)
    _c0, c1, c2 = coefficients
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    if deletion == 0:
        expected_a = sign * sp.Rational(16, 3) * (c1 - c2)
        expected_b = -sp.Rational(4, 3) * (2 * c1 + c2)
        mode = 0
        rows = ((0, 1, 3, 7),)
        expected_minors = (-sp.Rational(256, 27) * (c1 - c2) * (2 * c1 + c2) ** 2,)
    elif deletion == 1:
        expected_a = -sign * sp.Rational(16, 3) * (c1 - c2)
        expected_b = sp.Rational(4, 3) * (c1 + 2 * c2)
        mode = 0
        rows = ((0, 2, 3, 7),)
        expected_minors = (-sp.Rational(256, 27) * (c1 - c2) * (c1 + 2 * c2) ** 2,)
    else:
        expected_a = -sign * 8 * (c1 - c2)
        expected_b = -2 * (c1 + c2)
        mode = 2
        rows = ((0, 1, 2, 7), (0, 1, 3, 7))
        expected_minors = (
            -32 * c1 * (c1 - c2) * (c1 + c2),
            -16 * c2 * (c1 - c2) * (c1 + c2),
        )
    assert sp.expand(actual_a - expected_a) == 0
    assert sp.expand(actual_b - expected_b) == 0
    marked_map = marked_extension(deletion, extension, alpha, marked, mode)
    actual_minors = tuple(
        sp.factor(marked_map.extract(row_set, range(4)).det(method="domain-ge"))
        for row_set in rows
    )
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(actual_minors, expected_minors)
    )
    return f"r_{sign}_d_{deletion}_rank_four"


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
    alpha_rows = tuple(
        project(alpha[index], x[index], direction, chart, slope) for index in range(4)
    )
    beta_rows = tuple(
        project(beta[index], x[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
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


def coefficient_row(expression):
    entries = tuple(sp.diff(expression, variable) for variable in x)
    denominators = tuple(sp.denom(sp.together(entry)) for entry in entries)
    multiplier = functools.reduce(sp.lcm, denominators, sp.Integer(1))
    cleared = tuple(sp.cancel(multiplier * entry) for entry in entries)
    assert all(sp.denom(entry) == 1 for entry in cleared)
    return "[" + ",".join(map(singular_text, cleared)) + "]"


def h22_module_audit(sign, chart):
    alpha, beta = endpoint_rows(sign)
    marked = shifted_beta(alpha, beta, h)
    slope = lam if chart == "finite" else None
    d01 = h22_model(alpha, marked, "D01", chart, slope)
    d23 = h22_model(alpha, marked, "D23", chart, slope)
    generators = ",".join(
        coefficient_row(expression) for expression in (*d01["mixed"], *d23["mixed"])
    )
    diagonals = tuple(
        coefficient_row(expression)
        for expression in (d01["A"], d23["A"], d01["B"], d23["B"])
    )
    expected_module = (
        FINITE_EXPECTED_MODULE[sign]
        if chart == "finite"
        else INFINITY_EXPECTED_MODULE[sign]
    )
    expected_membership = (
        (False, True, True, False) if chart == "finite" else (True,) * 4
    )
    variables = h + ((lam,) if chart == "finite" else ())
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + ",".join(expected_module) + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2);",
            "module EM=simplify(reduce(E,M),2);",
            *(f"vector d{index}={value};" for index, value in enumerate(diagonals)),
            "int sameModule=(size(ME)==0)&&(size(EM)==0);",
            *(f"int diagonal{index}=reduce(d{index},M)==0;" for index in range(4)),
            (
                '"RESULT:"+string(sameModule)+":"+'
                + '+":"+'.join(f"string(diagonal{index})" for index in range(4))
                + '+":"+string(size(M));'
            ),
            "quit;",
        )
    )
    marker = (
        "RESULT:1:"
        + ":".join("1" if value else "0" for value in expected_membership)
        + f":{len(expected_module)}"
    )
    label = f"audit_r_{sign}_{chart}_module"
    run_singular(label, program, marker, timeout=300)
    return {
        "label": label,
        "diagonal_order": ("A01", "A23", "B01", "B23"),
        "diagonal_membership": expected_membership,
    }


def main():
    geometry = tuple(geometry_audit(sign) for sign in (1, -1))
    projections = tuple(
        projection_audit(sign, deletion) for sign in (1, -1) for deletion in range(4)
    )
    h31_minors = tuple(
        h31_minor_audit(sign, deletion, marking)
        for sign in (1, -1)
        for deletion, marking in EXPECTED_MARKINGS[sign].items()
        if marking is not None
    )
    h22_modules = tuple(
        h22_module_audit(sign, chart)
        for sign in (1, -1)
        for chart in ("finite", "infinity")
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "no_project_imports": True,
                "geometry": geometry,
                "h31_projection_audits": projections,
                "h31_minor_audits": h31_minors,
                "h22_module_audits": h22_modules,
                "claim_label": "AUDITED_FIXED_ORDER_ENDPOINT_FIBRES_EMPTY",
                "marked_H31_empty": True,
                "weighted_H22_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
