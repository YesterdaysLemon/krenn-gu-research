#!/usr/bin/env python3
"""No-import audit of component 23's s=0,k=inf,rt=1 H22 obstruction."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))

r, lam = sp.symbols("r lam")
h = sp.symbols("h0:4")
x = sp.symbols("z0:8")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


alpha = (A, D, add(B, D, r), add(B, D, 1 / r))
beta = (B, B, C, C)
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


def model(direction, chart, slope=None):
    alpha_rows = tuple(
        project(alpha[i], x[i], direction, chart, slope) for i in range(4)
    )
    marked_rows = tuple(
        project(marked[i], x[4 + i], direction, chart, slope) for i in range(4)
    )
    coefficients = {
        word: permanent_dp(
            tuple(marked_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }
    return coefficients


def matrix_and_tensors(chart, slope=None, substitutions=None):
    substitutions = substitutions or {}
    tensors = tuple(model(direction, chart, slope) for direction in ("D01", "D23"))
    mixed = tuple(
        tensor[word].subs(substitutions, simultaneous=True)
        for tensor in tensors
        for word in MIXED_WORDS
    )
    matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in mixed]
    )
    return tensors, matrix


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
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 3, 3, 3)
    edge23 = matrices[-1]
    minors = [
        sp.factor(edge23.extract(rows, columns).det())
        for rows in itertools.combinations(range(6), 3)
        for columns in itertools.combinations(range(4), 3)
    ]
    gcd = sp.factor(sp.gcd_list([value for value in minors if value]))
    assert sp.cancel(gcd - 4 * (r - 1) * (r + 1) / r) == 0
    return gcd


def ordinary_audit():
    _tensors, matrix = matrix_and_tensors("finite", lam)
    common = 256 * (lam - 1) ** 4 * (lam + 1) ** 4 * (r - 1) ** 2 * (r + 1) ** 2
    cases = (
        (
            (0, 1, 2, 3, 8, 9, 12, 16),
            {},
            common * h[2] * h[3] / r**2,
        ),
        (
            (0, 1, 3, 5, 8, 9, 12, 16),
            {},
            common * h[2] * (r - h[1]) / r**2,
        ),
        (
            (0, 1, 3, 4, 8, 9, 12, 16),
            {},
            -common * h[3] * (r * h[1] - 1) / r**3,
        ),
        ((0, 1, 3, 7, 8, 9, 12, 16), {}, common * h[0] / r**2),
        (
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[3]: 0, h[1]: r},
            -256 * (lam - 1) ** 5 * (lam + 1) ** 3 * (r - 1) ** 2 * (r + 1) ** 2 / r,
        ),
        (
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[2]: 0, h[1]: 1 / r},
            256 * (lam - 1) ** 5 * (lam + 1) ** 3 * (r - 1) ** 2 * (r + 1) ** 2 / r**3,
        ),
        (
            (0, 1, 3, 8, 9, 12, 13, 16),
            {h[0]: 0, h[2]: 0, h[3]: 0},
            -256
            * (lam - 1) ** 5
            * (lam + 1) ** 3
            * (r - 1)
            * (r + 1)
            * (h[1] * (r**2 + 1) - 2 * r)
            / r**2,
        ),
    )
    for rows, substitutions, expected in cases:
        observed = sp.factor(
            matrix.subs(substitutions, simultaneous=True)
            .extract(rows, range(8))
            .det(method="domain-ge")
        )
        assert sp.cancel(observed - expected) == 0
    return tuple(rows for rows, _substitutions, _expected in cases)


def residual_audit():
    substitutions = {
        h[0]: 0,
        h[1]: 2 * r / (r**2 + 1),
        h[2]: 0,
        h[3]: 0,
    }
    tensors, matrix = matrix_and_tensors("finite", lam, substitutions)
    kernel = sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0))
    assert all(sp.cancel(value) == 0 for value in matrix * kernel)
    rows = (0, 1, 3, 8, 9, 12, 16)
    columns = (0, 1, 2, 3, 4, 6, 7)
    minor = sp.factor(matrix.extract(rows, columns).det(method="domain-ge"))
    expected_minor = (
        128
        * (lam - 1) ** 4
        * (lam + 1) ** 3
        * (r - 1) ** 2
        * (r + 1) ** 2
        / (r * (r**2 + 1))
    )
    assert sp.cancel(minor - expected_minor) == 0
    diagonals = tuple(
        tensor[word].subs(substitutions, simultaneous=True)
        for tensor in tensors
        for word in (WORDS[0], WORDS[-1])
    )
    diagonal_values = tuple(
        sp.factor(
            sum(
                sp.diff(diagonal, variable) * kernel[index]
                for index, variable in enumerate(x)
            )
        )
        for diagonal in diagonals
    )
    expected = (
        2 * (lam + 1) * (r**2 + 1) / r,
        0,
        0,
        -2 * (lam + 1),
    )
    assert all(
        sp.cancel(observed - target) == 0
        for observed, target in zip(diagonal_values, expected, strict=True)
    )
    return tuple(kernel), str(minor), tuple(map(str, diagonal_values))


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    assert shutil.which("wsl.exe")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def vector(expression):
    entries = tuple(sp.cancel(sp.diff(expression, variable)) for variable in x)
    denominator = sp.factor(sp.lcm([sp.denom(entry) for entry in entries]))
    polynomial = sp.Poly(denominator, r)
    assert len(polynomial.terms()) == 1 and polynomial.LC() != 0
    cleared = tuple(sp.cancel(denominator * entry) for entry in entries)
    assert all(sp.denom(entry) == 1 for entry in cleared)
    return "[" + ",".join(map(singular_text, cleared)) + "]"


def module_audit(label, chart, slope, expected, expected_size):
    tensors = tuple(model(direction, chart, slope) for direction in ("D01", "D23"))
    generators = [vector(tensor[word]) for tensor in tensors for word in MIXED_WORDS]
    diagonals = [
        vector(tensor[word]) for tensor in tensors for word in (WORDS[0], WORDS[-1])
    ]
    u = sp.symbols("u")
    variables = (r, *h, u)
    program = "\n".join(
        (
            "ring P=0,(" + ",".join(map(str, variables)) + "),dp;",
            "ideal Q=u*(r*(r-1)*(r+1))-1; Q=std(Q);",
            "qring R=Q;",
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


def main():
    edge23_gcd = pure_pair_audit()
    ordinary = ordinary_audit()
    kernel, residual_minor, residual_diagonals = residual_audit()
    special = (
        module_audit(
            "lambda_one", "finite", sp.Integer(1), (False, True, True, False), 16
        ),
        module_audit(
            "lambda_minus_one",
            "finite",
            sp.Integer(-1),
            (True, False, True, True),
            5,
        ),
        module_audit(
            "projective_weight", "infinity", None, (False, True, True, False), 13
        ),
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP permanent rebuild",
                "field": "Q",
                "component": 23,
                "corner": "s=0,k=infinity,rt=1,t=1/r",
                "pair_profile": (3, 3, 3, 3, 3, 3),
                "edge23_three_minor_gcd": str(edge23_gcd),
                "ordinary_minor_rows": ordinary,
                "residual_kernel": tuple(map(str, kernel)),
                "residual_rank_minor": residual_minor,
                "diagonal_order": ("A01", "B01", "A23", "B23"),
                "residual_diagonals": residual_diagonals,
                "residual_genuine": False,
                "special_module_certificates": special,
                "normalized_rt_one_weighted_H22": "empty",
                "parameter_endpoints_covered": False,
                "finite_field_proof_used": False,
                "global_conjecture": "UNRESOLVED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
