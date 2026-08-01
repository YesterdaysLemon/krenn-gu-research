#!/usr/bin/env python3
"""Verify four divisor-generic P5 obstructions on component twenty-one."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

from derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate import (
    WORDS,
    build_model,
)
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def shifted(beta, alpha, h):
    return tuple(add(beta[i], alpha[i], h[i]) for i in range(4))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def bases(kind, parameters):
    A = (1, 1, 0, 0)
    C = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    D = (0, 0, 1, -1)
    if kind == "p0":
        endpoint, k, ell = parameters
        return (A, add(C, A, ell), C, D), (
            add(C, B, endpoint),
            A,
            add(B, A, k),
            add(A, C, ell),
        )
    if kind == "q0":
        endpoint, k, ell = parameters
        return (C, add(C, A, ell), C, D), (
            add(A, B, endpoint),
            A,
            add(B, A, k),
            add(A, C, ell),
        )
    if kind == "vertical":
        aa, k, ell = parameters
        return (add(A, C, -aa), add(C, A, ell), C, D), (
            B,
            A,
            add(B, A, k),
            add(A, C, ell),
        )
    raise ValueError(kind)


def mode3_bases(p, q, k):
    A = (1, 1, 0, 0)
    C = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    D = (0, 0, 1, -1)
    return (add(tuple(q * x for x in A), C, -p), A, C, D), (
        add(A, B, p),
        C,
        add(B, A, k),
        C,
    )


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def clear(expression):
    return sp.expand(sp.fraction(sp.cancel(expression))[0])


def clear_row(entries):
    denominators = [sp.fraction(sp.cancel(entry))[1] for entry in entries]
    multiplier = sp.prod(denominators)
    return tuple(clear(multiplier * entry) for entry in entries)


def module_certificate(label, field, alpha, canonical):
    h = sp.symbols("h0:4")
    beta = shifted(canonical, alpha, h)
    results = []
    for q in range(4):
        mixed, d0, d1 = mixed_matrix(q, alpha, beta)
        generators = ",".join(
            "[" + ",".join(map(sg, clear_row(tuple(mixed[row, col] for col in range(8))))) + "]"
            for row in range(14)
        )
        row0 = "[" + ",".join(map(sg, clear_row(tuple(d0[0, col] for col in range(8))))) + "]"
        row1 = "[" + ",".join(map(sg, clear_row(tuple(d1[0, col] for col in range(8))))) + "]"
        program = "\n".join(
            (
                "ring R=(0," + ",".join(field) + "),(h0,h1,h2,h3),dp;",
                "option(redSB);",
                "module M=" + generators + "; M=std(M);",
                "vector a=" + row0 + "; vector b=" + row1 + ";",
                "vector ra=reduce(a,M); vector rb=reduce(b,M);",
                '"RESULT:"+string(ra==0)+":"+string(rb!=0)+":"+string(size(M));',
                "quit;",
            )
        )
        completed = subprocess.run(
            singular_command(), input=program, text=True, capture_output=True, timeout=60, check=False
        )
        assert completed.returncode == 0 and not completed.stderr.strip(), (label, q, completed.stdout, completed.stderr)
        markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
        assert len(markers) == 1 and markers[0].split(":")[1:3] == ["1", "1"], (label, q, completed.stdout)
        size = int(markers[0].split(":")[3])
        results.append(size)
    return results


def hall_d01(alpha):
    rho, sigma = sp.symbols("rho sigma")
    extensions = sp.symbols("e0:4")
    rows = tuple(
        (rho * alpha[i][0] + sigma * alpha[i][1], alpha[i][2], alpha[i][3], extensions[i])
        for i in range(4)
    )
    assert permanent(rows) == 0
    return True


def finite_d23_projection(label, field, alpha, canonical, expected):
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    lam = sp.Symbol("lam")
    beta = shifted(canonical, alpha, h)
    model = build_model(alpha, beta, z, "D23", "finite", lam)
    equations = (*tuple(model["mixed"] * sp.Matrix(z)), model["A"] - 1)
    variables = z + h + (lam,)
    program = "\n".join(
        (
            "ring R=(0," + ",".join(field) + "),(" + ",".join(map(str, variables)) + "),(dp(8),dp(5));",
            "option(redSB);",
            "ideal I=" + ",".join(sg(clear(value)) for value in equations) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, z)) + "));",
            "ideal E=" + ",".join(sg(clear(value)) for value in expected) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
            "poly b=" + sg(clear(model["B"])) + "; poly rb=reduce(b,I);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(rb==0)+":"+string(size(J));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=120, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (label, completed.stdout, completed.stderr)
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:1:5"], (label, completed.stdout)
    return True


def infinity_d23_module(label, field, alpha, canonical):
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    beta = shifted(canonical, alpha, h)
    model = build_model(alpha, beta, z, "D23", "infinity")
    mixed = model["mixed"]
    d0 = sp.Matrix([[sp.diff(model["A"], value) for value in z]])
    d1 = sp.Matrix([[sp.diff(model["B"], value) for value in z]])
    generators = ",".join(
        "[" + ",".join(sg(clear(mixed[row, col])) for col in range(8)) + "]"
        for row in range(14)
    )
    row0 = "[" + ",".join(sg(clear(value)) for value in d0) + "]"
    row1 = "[" + ",".join(sg(clear(value)) for value in d1) + "]"
    program = "\n".join(
        (
            "ring R=(0," + ",".join(field) + "),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "vector a=" + row0 + "; vector b=" + row1 + ";",
            '"RESULT:"+string(reduce(a,M)==0)+":"+string(reduce(b,M)!=0)+":"+string(size(M));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=60, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (label, completed.stdout, completed.stderr)
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:1:7"], (label, completed.stdout)
    return True


def vertical_h31(alpha, canonical, aa, k, ell):
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inverse = sp.Symbol("v")
    E = 2 * aa * ell + ell**2 + 1
    beta = shifted(canonical, alpha, h)
    expected = (h[3], h[2] - k * ell, E * h[1] + aa + ell, h[0])
    outputs = []
    for q in (2, 3):
        mixed, d0, d1 = mixed_matrix(q, alpha, beta)
        vector = sp.Matrix(z)
        equations = (*tuple(mixed * vector), (d0 * vector)[0] - 1, inverse * (d1 * vector)[0] - 1)
        eliminated = z + (inverse,)
        variables = eliminated + h
        program = "\n".join(
            (
                "ring R=(0,a,k,ell),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
                "option(redSB);",
                "ideal I=" + ",".join(sg(clear(value)) for value in equations) + "; I=slimgb(I);",
                "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
                "ideal E=" + ",".join(sg(clear(value)) for value in expected) + "; E=std(E);",
                "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
                '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
                "quit;",
            )
        )
        completed = subprocess.run(
            singular_command(), input=program, text=True, capture_output=True, timeout=120, check=False
        )
        assert completed.returncode == 0 and not completed.stderr.strip(), (q, completed.stdout, completed.stderr)
        markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
        assert markers == ["RESULT:1:4"], (q, completed.stdout)
        outputs.append(q)

    marking = (0, -(aa + ell) / E, k * ell, 0)
    marked = shifted(canonical, alpha, marking)
    branch_data = []
    s, w = sp.symbols("s w")
    for q, sign in ((2, 1), (3, -1)):
        mixed, d0row, d1row = mixed_matrix(q, alpha, marked)
        e0 = sp.Matrix((-aa * ell - 1, 0, ell, 0, 0, 1, 0, 0))
        e1 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        vector = s * e0 + w * e1
        assert all(sp.factor(value) == 0 for value in mixed * vector)
        d0 = sp.factor((d0row * vector)[0])
        d1 = sp.factor((d1row * vector)[0])
        assert sp.factor(d0 - (-sign) * 2 * E * s) == 0
        assert sp.factor(d1 + 2 * (k * (ell**2 - 1) * s - 2 * w)) == 0
        matrix = marked_extension(q, vector, alpha, marked, 3).extract((0, 4, 6, 7), range(4))
        determinant_identity(matrix, (-sign) * 2 * s * d0 * d1, ("a", "k", "ell"), ("s", "w"))
        assert one_marked_map(3, alpha, marked)[4, q] == -2
        branch_data.append(q)
    return outputs, branch_data


def determinant_identity(matrix, expected, field, variables):
    program = "\n".join(
        (
            "ring R=(0," + ",".join(field) + "),(" + ",".join(variables) + "),dp;",
            "matrix M[4][4]=" + ",".join(sg(value) for value in matrix) + ";",
            "poly f=det(M); poly e=" + sg(expected) + ";",
            '"RESULT:"+string(f-e==0);',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=30, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (completed.stdout, completed.stderr)
    assert [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")] == ["RESULT:1"]


def vertical_h22(alpha, canonical, aa, k, ell):
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inv0, inv1 = sp.symbols("u v")
    lam = sp.Symbol("lam")
    E = 2 * aa * ell + ell**2 + 1
    beta = shifted(canonical, alpha, h)
    expected = (h[3], h[2] - k * ell, E * h[1] + aa + ell, h[0])
    charts = []
    for chart in ("finite", "infinity"):
        slope = lam if chart == "finite" else None
        d01 = build_model(alpha, beta, z, "D01", chart, slope)
        d23 = build_model(alpha, beta, z, "D23", chart, slope)
        equations = (
            *(d01["coefficients"][word] for word in WORDS[:-1]),
            d01["B"] - 1,
            *tuple(d23["mixed"] * sp.Matrix(z)),
            inv0 * d23["A"] - 1,
            inv1 * d23["B"] - 1,
        )
        eliminated = z + (inv0, inv1)
        retained = h + ((lam,) if chart == "finite" else ())
        variables = eliminated + retained
        program = "\n".join(
            (
                "ring R=(0,a,k,ell),(" + ",".join(map(str, variables)) + f"),(dp(10),dp({len(retained)}));",
                "option(redSB);",
                "ideal I=" + ",".join(sg(clear(value)) for value in equations) + "; I=slimgb(I);",
                "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
                "ideal E=" + ",".join(sg(clear(value)) for value in expected) + "; E=std(E);",
                "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
                '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
                "quit;",
            )
        )
        completed = subprocess.run(
            singular_command(), input=program, text=True, capture_output=True, timeout=120, check=False
        )
        assert completed.returncode == 0 and not completed.stderr.strip(), (chart, completed.stdout, completed.stderr)
        assert [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")] == ["RESULT:1:4"]
        charts.append(chart)

    marking = (0, -(aa + ell) / E, k * ell, 0)
    beta = shifted(canonical, alpha, marking)
    Cvar = sp.Symbol("C0")
    e0 = sp.Matrix((-aa * ell - 1, 0, ell, 0, 0, 1, 0, 0))
    diagnostics = []
    for chart in ("finite", "infinity"):
        slope = lam if chart == "finite" else None
        d01 = build_model(alpha, beta, z, "D01", chart, slope)
        d23 = build_model(alpha, beta, z, "D23", chart, slope)
        unwanted = [*(d01["coefficients"][word] for word in WORDS[:-1]), *tuple(d23["mixed"] * sp.Matrix(z))]
        shared = sp.Matrix([[sp.diff(value, variable) for variable in z] for value in unwanted])
        assert all(sp.factor(value) == 0 for value in shared * e0)
        sample = {aa: 1, k: 2, ell: 2} | ({lam: 3} if chart == "finite" else {})
        assert shared.subs(sample).rank() == 7
        substitution = dict(zip(z, Cvar * e0, strict=True))
        b01 = sp.factor(d01["B"].subs(substitution))
        a23 = sp.factor(d23["A"].subs(substitution))
        b23 = sp.factor(d23["B"].subs(substitution))
        marked_map = one_marked_map(3, d23["alpha_rows"], d23["beta_rows"]).subs(substitution)
        matrix = marked_map.extract((0, 4, 6, 7), range(4))
        if chart == "finite":
            assert sp.factor(b01 - 2 * Cvar * ((ell + 1) * lam + 1 - ell)) == 0
            assert sp.factor(a23 - 2 * Cvar * (lam - 1) * E) == 0
            assert sp.factor(b23 + 2 * Cvar * k * (ell**2 - 1) * (lam + 1)) == 0
            expected_det = -8 * Cvar**3 * k * (ell**2 - 1) * (lam + 1) ** 3 * E
            determinant_identity(matrix, expected_det, ("a", "k", "ell"), ("C0", "lam"))
        else:
            assert sp.factor(b01 - 2 * Cvar * (ell + 1)) == 0
            assert sp.factor(a23 - 2 * Cvar * E) == 0
            assert sp.factor(b23 + 2 * Cvar * k * (ell**2 - 1)) == 0
            expected_det = -8 * Cvar**3 * k * (ell**2 - 1) * E
            determinant_identity(matrix, expected_det, ("a", "k", "ell"), ("C0",))
        diagnostics.append(chart)
    return charts, diagnostics


def main():
    p, q, k, ell, aa = sp.symbols("p q k ell a")
    endpoint_cases = []
    for label, parameter, kind in (("p=0", q, "p0"), ("q=0", p, "q0")):
        alpha, beta = bases(kind, (parameter, k, ell))
        pure = {word: sp.factor(permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))) for word in WORDS}
        assert pure[WORDS[-1]] == 4 * parameter
        assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])
        sizes = module_certificate(label, (str(parameter), "k", "ell"), alpha, beta)
        assert sizes == [2, 2, 7, 7]
        hall_d01(alpha)
        E = ell**2 - 1
        h = sp.symbols("h0:4")
        lam = sp.Symbol("lam")
        f1 = k * E * h[0] * h[1] - h[0] * h[2] + E * h[1] * h[2] + k * ell * h[0] + ell * h[2] - k
        f2 = (h[2] ** 2 - k**2) * (h[0] + (1 - ell**2) * h[1] - ell)
        f3 = (h[2] ** 2 - k**2) * (((ell - 1) * h[1] + 1) * ((ell + 1) * h[1] + 1))
        finite_d23_projection(label, (str(parameter), "k", "ell"), alpha, beta, (lam + 1, h[3], f1, f2, f3))
        infinity_d23_module(label, (str(parameter), "k", "ell"), alpha, beta)
        endpoint_cases.append(label)

    alpha3, beta3 = mode3_bases(p, q, k)
    pure3 = {word: sp.factor(permanent(tuple(beta3[i] if word[i] else alpha3[i] for i in range(4)))) for word in WORDS}
    assert pure3[WORDS[-1]] == -4 * p
    assert all(value == 0 for word, value in pure3.items() if word != WORDS[-1])
    sizes3 = module_certificate("mode3 projective", ("p", "q", "k"), alpha3, beta3)
    assert sizes3 == [2, 2, 7, 7]
    hall_d01(alpha3)
    h = sp.symbols("h0:4")
    lam = sp.Symbol("lam")
    delta = p**2 - q**2
    g1 = delta * k * h[0] * h[1] + delta * h[0] * h[2] - p * h[1] * h[2] - q * k * h[1] - q * h[2] - p * k
    g2 = (h[2] ** 2 - k**2) * (delta * h[0] - p * h[1] - q)
    g3 = (h[1] ** 2 - 1) * (h[2] ** 2 - k**2)
    finite_d23_projection("mode3 projective", ("p", "q", "k"), alpha3, beta3, (lam + 1, h[3], g1, g2, g3))
    infinity_d23_module("mode3 projective", ("p", "q", "k"), alpha3, beta3)

    alphav, betav = bases("vertical", (aa, k, ell))
    purev = {word: sp.factor(permanent(tuple(betav[i] if word[i] else alphav[i] for i in range(4)))) for word in WORDS}
    assert purev[WORDS[-1]] == 4
    assert all(value == 0 for word, value in purev.items() if word != WORDS[-1])
    hall_d01(alphav)
    vertical_h31_data = vertical_h31(alphav, betav, aa, k, ell)
    vertical_h22_data = vertical_h22(alphav, betav, aa, k, ell)
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic-zero function fields",
                "component": 21,
                "finite_endpoint_divisors": endpoint_cases,
                "mode3_projective_H31_module_sizes": sizes3,
                "mode3_projective_H31_empty": True,
                "mode3_projective_H22_empty": True,
                "vertical_H31": vertical_h31_data,
                "vertical_H22": vertical_h22_data,
                "vertical_H31_generic_open": "E!=0",
                "vertical_H22_generic_open": "E*k*(ell^2-1)!=0",
                "all_exceptional_intersections_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
