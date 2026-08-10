#!/usr/bin/env python3
"""No-import audit of component 23's r,t=+/-1 corner-line H22 obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))

u, lam, H = sp.symbols("u lam H")
h = sp.symbols("h0:4")
x = sp.symbols("z0:8")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def rows(r, t):
    return (A, D, add(B, D, r), add(B, D, t)), (B, B, C, C)


alpha, beta = rows(1, u)
marked = tuple(add(beta[i], alpha[i], h[i]) for i in range(4))


def permanent_dp(matrix):
    states = {0: sp.Integer(1)}
    for row in matrix:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = following
    return sp.expand(states[(1 << len(matrix)) - 1])


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


def model(alpha_rows, marked_rows, extensions, direction, chart, slope=None):
    projected_alpha = tuple(
        project(alpha_rows[i], extensions[i], direction, chart, slope) for i in range(4)
    )
    projected_marked = tuple(
        project(marked_rows[i], extensions[4 + i], direction, chart, slope)
        for i in range(4)
    )
    return {
        word: permanent_dp(
            tuple(
                projected_marked[i] if word[i] else projected_alpha[i] for i in range(4)
            )
        )
        for word in WORDS
    }


def base_models(chart, slope=None):
    return tuple(
        model(alpha, marked, x, direction, chart, slope) for direction in ("D01", "D23")
    )


def matrix(chart, slope=None, substitutions=None):
    substitutions = substitutions or {}
    tensors = base_models(chart, slope)
    equations = tuple(
        tensor[word].subs(substitutions, simultaneous=True)
        for tensor in tensors
        for word in MIXED_WORDS
    )
    return tensors, sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in equations]
    )


def pure_pair_audit():
    pure = {
        word: permanent_dp(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        for word in WORDS
    }
    assert pure[WORDS[-1]] == -4
    assert sum(value != 0 for value in pure.values()) == 1

    def product(left, right):
        return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])

    planes = tuple(zip(alpha, beta))
    matrices = tuple(
        sp.Matrix.hstack(
            *(
                product(planes[left][i], planes[right][j])
                for i in range(2)
                for j in range(2)
            )
        )
        for left, right in PAIRS
    )
    assert tuple(item.rank() for item in matrices) == (3, 3, 3, 3, 3, 4)
    edge23 = matrices[-1]
    minors = [
        sp.factor(edge23.extract(rows, range(4)).det())
        for rows in itertools.combinations(range(6), 4)
    ]
    gcd = sp.factor(sp.gcd_list([value for value in minors if value]))
    assert sp.expand(gcd - 8 * (u - 1) ** 2) == 0
    return gcd


def ordinary_audit():
    _tensors, mixed = matrix("finite", lam)
    common = 256 * (lam - 1) ** 4 * (lam + 1) ** 4 * (u - 1) ** 2 * (u + 1)
    cases = (
        ((0, 1, 2, 3, 8, 9, 13, 16), {}, common * h[2] * h[3] * u),
        (
            (0, 1, 3, 5, 8, 9, 13, 16),
            {},
            -common * h[2] * (h[1] * u - 1),
        ),
        (
            (0, 1, 3, 4, 8, 9, 13, 16),
            {},
            -common * h[3] * u * (h[1] - 1),
        ),
        ((0, 1, 3, 7, 8, 9, 13, 16), {}, common * h[0] * u),
        (
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[3]: 0, h[1]: 1 / u},
            -256 * (lam - 1) ** 5 * (lam + 1) ** 3 * (u - 1) ** 2 * (u + 1),
        ),
        (
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[2]: 0, h[3]: 0},
            256 * u * (lam - 1) ** 5 * (lam + 1) ** 3 * (h[1] - 1) * (u - 1) * (u + 1),
        ),
    )
    for rows, substitutions, expected in cases:
        observed = sp.factor(
            mixed.subs(substitutions, simultaneous=True)
            .extract(rows, range(8))
            .det(method="domain-ge")
        )
        assert sp.expand(observed - expected) == 0
    return tuple(rows for rows, _substitutions, _expected in cases)


def contraction_rows(chart, slope=None):
    if chart == "finite":
        return ((1, slope, 0, 0, 0), (0, 0, 1, slope, 0))
    return ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0))


def residual_audit(chart, slope=None):
    substitutions = {h[0]: 0, h[1]: 1, h[2]: 0, h[3]: H}
    tensors, mixed = matrix(chart, slope, substitutions)
    kernel = sp.Matrix((0, 0, -1, -1, 0, 1, 0, H * u))
    assert all(sp.expand(value) == 0 for value in mixed * kernel)
    rows = (0, 1, 3, 8, 9, 13, 16)
    columns = (0, 1, 2, 3, 4, 6, 7)
    rank_minor = sp.factor(mixed.extract(rows, columns).det(method="domain-ge"))
    if chart == "finite":
        expected_rank = 128 * u * (slope - 1) ** 4 * (slope + 1) ** 3 * (u - 1) ** 2
        expected_diagonals = (
            2 * (slope + 1) * (u + 1),
            2 * H * (slope - 1) * (u + 1),
            0,
            -2 * (slope + 1),
        )
        expected_gamma = 8 * H * (slope - 1) ** 4 * (slope + 1) * (u - 1) * (u + 1) ** 2
    else:
        expected_rank = 128 * u * (u - 1) ** 2
        expected_diagonals = (2 * (u + 1), 2 * H * (u + 1), 0, -2)
        expected_gamma = 8 * H * (u - 1) * (u + 1) ** 2
    assert sp.expand(rank_minor - expected_rank) == 0
    diagonal_rows = tuple(
        tensor[word].subs(substitutions, simultaneous=True)
        for tensor in tensors
        for word in (WORDS[0], WORDS[-1])
    )
    values = tuple(
        sp.factor(
            sum(
                sp.diff(diagonal, variable) * kernel[index]
                for index, variable in enumerate(x)
            )
        )
        for diagonal in diagonal_rows
    )
    assert all(
        sp.expand(observed - target) == 0
        for observed, target in zip(values, expected_diagonals, strict=True)
    )
    marked_rows = tuple(add(beta[i], alpha[i], substitutions[h[i]]) for i in range(4))
    alpha5 = tuple((*alpha[i], kernel[i]) for i in range(4))
    marked5 = tuple((*marked_rows[i], kernel[4 + i]) for i in range(4))
    gamma = sp.symbols("gamma0:5")
    equations = []
    for contraction in contraction_rows(chart, slope):
        for word in itertools.product((0, 1), repeat=3):
            selected = (gamma,) + tuple(
                marked5[i] if word[i - 1] else alpha5[i] for i in range(1, 4)
            )
            equations.append(permanent_dp(selected + (contraction,)))
    gamma_matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in gamma] for equation in equations]
    )
    gamma_minor = sp.factor(
        gamma_matrix.extract((0, 1, 2, 7, 9), range(5)).det(method="domain-ge")
    )
    assert sp.expand(gamma_minor - expected_gamma) == 0
    return str(rank_minor), tuple(map(str, values)), str(gamma_minor)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    assert shutil.which("wsl.exe")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def vector(expression):
    return (
        "["
        + ",".join(singular_text(sp.diff(expression, variable)) for variable in x)
        + "]"
    )


def module_audit(label, slope, expected, expected_size):
    tensors = base_models("finite", slope)
    generators = [vector(tensor[word]) for tensor in tensors for word in MIXED_WORDS]
    diagonals = [
        vector(tensor[word]) for tensor in tensors for word in (WORDS[0], WORDS[-1])
    ]
    program = "\n".join(
        (
            "ring R=(0,u),(" + ",".join(map(str, h)) + "),dp;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
            *(f"vector d{i}={value};" for i, value in enumerate(diagonals)),
            *(f"int z{i}=reduce(d{i},M)==0;" for i in range(4)),
            (
                'print("RESULT:'
                + label
                + ':"+string(z0)+":"+string(z1)+":"+string(z2)+":"+string(z3)+":"+string(size(M)));'
            ),
            "quit;",
        )
    )
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
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    expected_marker = (
        "RESULT:"
        + label
        + ":"
        + ":".join("1" if value else "0" for value in expected)
        + f":{expected_size}"
    )
    assert markers == [expected_marker], (completed.stdout, expected_marker)
    return label


def projective_projection_audit():
    tensors = base_models("infinity", None)
    mixed = tuple(tensor[word] for tensor in tensors for word in MIXED_WORDS)
    diagonals = tuple(
        tensor[word] for tensor in tensors for word in (WORDS[0], WORDS[-1])
    )
    w = sp.symbols("w")
    product = sp.expand(diagonals[0] * diagonals[1] * diagonals[3])
    variables = (*x, w, *h)
    program = "\n".join(
        (
            "ring R=(0,u),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular_text, mixed))
            + ","
            + singular_text(w * product - 1)
            + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I,z0*z1*z2*z3*z4*z5*z6*z7*w); J=std(J);",
            "ideal E=h2,h1-1,h0; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "int same=(size(JE)==0)&&(size(EJ)==0);",
            'print("RESULT:"+string(same)+":"+string(size(J))+":"+string(reduce(1,I)==0));',
            "quit;",
        )
    )
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
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:3:0"], completed.stdout
    return markers[0]


def j5(row):
    return (-row[1], -row[0], row[3], row[2], row[4])


def symmetry_audit():
    r0, t0, mu, nu = sp.symbols("r0 t0 mu nu")
    q = sp.symbols("q0:4")
    e = sp.symbols("e0:8")
    old_alpha, old_beta = rows(r0, t0)
    old_marked = tuple(add(old_beta[i], old_alpha[i], q[i]) for i in range(4))
    old_alpha5 = tuple((*old_alpha[i], e[i]) for i in range(4))
    old_marked5 = tuple((*old_marked[i], e[4 + i]) for i in range(4))

    swap_alpha, swap_beta = rows(t0, r0)
    swap_q = (q[0], q[1], q[3], q[2])
    swap_marked = tuple(add(swap_beta[i], swap_alpha[i], swap_q[i]) for i in range(4))
    swap_e = (e[0], e[1], e[3], e[2], e[4], e[5], e[7], e[6])
    swap_alpha5 = tuple((*swap_alpha[i], swap_e[i]) for i in range(4))
    swap_marked5 = tuple((*swap_marked[i], swap_e[4 + i]) for i in range(4))

    signs = (-1, -1, 1, 1)
    sign_alpha, sign_beta = rows(-r0, -t0)
    sign_q = (-q[0], -q[1], q[2], q[3])
    sign_marked = tuple(add(sign_beta[i], sign_alpha[i], sign_q[i]) for i in range(4))
    sign_e = (-e[0], -e[1], e[2], e[3], e[4], e[5], e[6], e[7])
    sign_alpha5 = tuple((*sign_alpha[i], sign_e[i]) for i in range(4))
    sign_marked5 = tuple((*sign_marked[i], sign_e[4 + i]) for i in range(4))

    contractions_old = {
        "D01": (nu, mu, 0, 0, 0),
        "D23": (0, 0, nu, mu, 0),
    }
    contractions_reciprocal = {
        "D01": (mu, nu, 0, 0, 0),
        "D23": (0, 0, mu, nu, 0),
    }
    counts = {"mode_swap": 0, "signed_weight_reciprocity": 0}
    for direction, projected_sign in (("D01", -1), ("D23", 1)):
        old_q = contractions_old[direction]
        reciprocal_q = contractions_reciprocal[direction]
        for word in WORDS:
            pulled = (word[0], word[1], word[3], word[2])
            old_selected = tuple(
                old_marked5[i] if word[i] else old_alpha5[i] for i in range(4)
            )
            old_pulled = tuple(
                old_marked5[i] if pulled[i] else old_alpha5[i] for i in range(4)
            )
            swap_selected = tuple(
                swap_marked5[i] if word[i] else swap_alpha5[i] for i in range(4)
            )
            sign_selected = tuple(
                sign_marked5[i] if word[i] else sign_alpha5[i] for i in range(4)
            )
            assert (
                sp.expand(
                    permanent_dp(swap_selected + (old_q,))
                    - permanent_dp(old_pulled + (old_q,))
                )
                == 0
            )
            row_sign = sp.prod(signs[i] for i in range(4) if word[i] == 0)
            assert (
                sp.expand(
                    permanent_dp(sign_selected + (reciprocal_q,))
                    - projected_sign * row_sign * permanent_dp(old_selected + (old_q,))
                )
                == 0
            )
            counts["mode_swap"] += 1
            counts["signed_weight_reciprocity"] += 1

    # Independent generic 5x5 permanent invariance under J on the four source
    # coordinates and identity on the extension coordinate.
    generic = sp.symbols("g0:25")
    generic_rows = tuple(
        tuple(generic[5 * i + column] for column in range(5)) for i in range(5)
    )
    assert permanent_dp(tuple(j5(row) for row in generic_rows)) == permanent_dp(
        generic_rows
    )
    return counts


def main():
    edge23_gcd = pure_pair_audit()
    ordinary = ordinary_audit()
    finite = residual_audit("finite", lam)
    special = (
        module_audit("lambda_one", sp.Integer(1), (False, True, True, False), 12),
        module_audit("lambda_minus_one", sp.Integer(-1), (True, False, True, True), 5),
    )
    projection = projective_projection_audit()
    projective = residual_audit("infinity", None)
    symmetries = symmetry_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP permanent rebuild",
                "field": "Q(u)",
                "component": 23,
                "corner": "s=0,k=infinity",
                "base_line": "r=1; u=t; u*(u-1)*(u+1) != 0",
                "pair_profile": (3, 3, 3, 3, 3, 4),
                "edge23_maximal_minor_gcd": str(edge23_gcd),
                "ordinary_minor_rows": ordinary,
                "finite_residual": finite,
                "special_weights": special,
                "projective_projection": "<h2,h1-1,h0>",
                "projective_projection_certificate": projection,
                "projective_residual": projective,
                "symmetry_words_checked": symmetries,
                "four_unit_parameter_lines_weighted_H22": "empty",
                "excluded_intersections": "u=0,+1,-1,infinity",
                "finite_field_proof_used": False,
                "global_conjecture": "UNRESOLVED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
