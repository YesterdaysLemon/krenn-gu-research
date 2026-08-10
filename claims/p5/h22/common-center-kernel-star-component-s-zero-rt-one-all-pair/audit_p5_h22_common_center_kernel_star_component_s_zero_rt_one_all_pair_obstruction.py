#!/usr/bin/env python3
"""No-import audit of component 23's s=0, rt=1 all-pair H22 face."""

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
PAIRS = tuple(itertools.combinations(range(4), 2))

r, k, lam = sp.symbols("r k lam")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


alpha = (
    A,
    add(A, scale(k, D)),
    add(B, scale(r, D)),
    add(B, scale(1 / r, D)),
)
beta = (B, B, C, C)
marked = tuple(add(beta[index], scale(h[index], alpha[index])) for index in range(4))


def permanent_dp(rows):
    """Subset-DP permanent, independent of the construction verifier."""
    states = {0: sp.Integer(1)}
    for row in rows:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = following
    return sp.expand(states[(1 << len(rows)) - 1])


def project(row, extension, direction, chart, slope=None):
    if chart == "finite" and direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if chart == "finite" and direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if chart == "infinity" and direction == "D01":
        return (row[0], row[2], row[3], extension)
    if chart == "infinity" and direction == "D23":
        return (row[0], row[1], row[2], extension)
    raise AssertionError((direction, chart))


def build_model(direction, chart, slope=None):
    left = tuple(
        project(alpha[index], x[index], direction, chart, slope) for index in range(4)
    )
    right = tuple(
        project(marked[index], x[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {
        word: permanent_dp(
            tuple(right[index] if word[index] else left[index] for index in range(4))
        )
        for word in WORDS
    }
    return {
        "mixed": tuple(coefficients[word] for word in WORDS[1:-1]),
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def audit_pure_and_pairs():
    pure = {
        word: sp.factor(
            permanent_dp(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == -4
    assert sum(value != 0 for value in pure.values()) == 1

    matrices = []
    for left, right in PAIRS:
        matrices.append(
            sp.Matrix.hstack(
                symmetric_product(alpha[left], alpha[right]),
                symmetric_product(alpha[left], beta[right]),
                symmetric_product(beta[left], alpha[right]),
                symmetric_product(beta[left], beta[right]),
            )
        )
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 4, 4, 3)
    assert tuple(matrix.subs(k, 0).rank() for matrix in matrices) == (3,) * 6
    assert matrices[5].subs(r, 1).rank() == 2
    assert matrices[5].subs(r, -1).rank() == 2

    pair23_witness = sp.factor(matrices[5].extract((0, 1, 2), (1, 2, 3)).det())
    assert pair23_witness in {
        sp.factor(4 * (r - 1) * (r + 1) / r),
        sp.factor(-4 * (r - 1) * (r + 1) / r),
    }
    rank_four_witnesses = (
        sp.factor(matrices[3].extract((1, 2, 3, 5), range(4)).det()),
        sp.factor(matrices[4].extract((1, 2, 3, 5), range(4)).det()),
    )
    assert all(
        value != 0 and sp.factor(value / k).subs(k, 0) != 0
        for value in rank_four_witnesses
    )


finite_models = (build_model("D01", "finite", lam), build_model("D23", "finite", lam))
finite_mixed = sp.Matrix(
    [
        [sp.diff(equation, variable) for variable in x]
        for model in finite_models
        for equation in model["mixed"]
    ]
)


def factor_equal(left, right):
    return sp.cancel(left - right) == 0


def audit_ordinary_minors():
    qm = lam * (r + 1) - (r - 1)
    qp = lam * (r + 1) + (r - 1)
    assert sp.expand(qp - qm) == 2 * (r - 1)
    common = 256 * (lam - 1) ** 4 * (lam + 1) ** 3 * (r - 1) ** 2 * (r + 1) ** 2
    cases = (
        (
            {},
            (0, 1, 2, 3, 8, 9, 12),
            common * h[2] * h[3] * k**4 / r**2,
            common * h[2] * h[3] * k**4 / r**3,
        ),
        (
            {},
            (0, 1, 3, 5, 8, 9, 12),
            common * h[2] * k**3 * (r - k * h[1]) / r**2,
            common * h[2] * k**3 * (r - k * h[1]) / r**3,
        ),
        (
            {h[2]: 0},
            (0, 1, 3, 7, 8, 9, 12),
            common * k**4 * (h[0] - h[1]) / r**2,
            common * k**4 * (h[0] - h[1]) / r**3,
        ),
        (
            {h[2]: 0, h[0]: h[1]},
            (0, 1, 3, 8, 9, 11, 12),
            -common * h[1] ** 2 * k**4 / r**2,
            -common * h[1] ** 2 * k**4 / r**3,
        ),
        (
            {h[3]: 0, h[1]: r / k},
            (0, 1, 3, 8, 9, 11, 12),
            -common * k**2,
            -common * k**2 / r,
        ),
        (
            {h[0]: 0, h[1]: 0, h[2]: 0},
            (0, 1, 3, 8, 9, 12, 13),
            512 * k**3 * (lam - 1) ** 5 * (lam + 1) ** 2 * (r - 1) * (r + 1) / r,
            512 * k**3 * (lam - 1) ** 5 * (lam + 1) ** 2 * (r - 1) * (r + 1) / r**2,
        ),
    )
    for substitutions, rows, left_prefactor, right_prefactor in cases:
        matrix = finite_mixed.subs(substitutions, simultaneous=True)
        left = matrix.extract((*rows, 14), range(8)).det(method="domain-ge")
        right = matrix.extract((*rows, 15), range(8)).det(method="domain-ge")
        assert factor_equal(left, left_prefactor * qm)
        assert factor_equal(right, right_prefactor * qp)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    assert shutil.which("wsl.exe")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def fixed_r_cleared_vector(expression, substitutions):
    entries = tuple(
        sp.cancel(
            r * sp.diff(expression.subs(substitutions, simultaneous=True), variable)
        )
        for variable in x
    )
    assert all(sp.denom(entry) == 1 for entry in entries)
    return "[" + ",".join(map(singular_text, entries)) + "]"


def audit_module(
    label,
    chart,
    slope,
    substitutions,
    variables,
    localizer,
    target_index,
    expected_size,
):
    models = (build_model("D01", chart, slope), build_model("D23", chart, slope))
    generators = [
        fixed_r_cleared_vector(equation, substitutions)
        for model in models
        for equation in model["mixed"]
    ]
    target_model = target_index // 2
    target_kind = ("A", "B")[target_index % 2]
    target = fixed_r_cleared_vector(models[target_model][target_kind], substitutions)
    program = "\n".join(
        (
            "ring P=0,(" + ",".join(map(str, variables)) + "),dp;",
            "ideal Q=u*(" + singular_text(localizer) + ")-1; Q=std(Q);",
            "qring R=Q;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
            "vector d=" + target + ";",
            '"RESULT:' + label + ':"+string(reduce(d,M)==0)+":"+string(size(M));',
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
        label,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [f"RESULT:{label}:1:{expected_size}"], (label, completed.stdout)
    return label


def audit_special_modules():
    u = sp.Symbol("u")
    base = r * (r - 1) * (r + 1)
    return (
        audit_module(
            "k_zero_ordinary_B01",
            "finite",
            lam,
            {k: 0},
            (r, *h, lam, u),
            base * (lam - 1) * (lam + 1),
            1,
            7,
        ),
        audit_module(
            "lambda_one_B01", "finite", sp.Integer(1), {}, (r, k, *h, u), base, 1, 15
        ),
        audit_module(
            "lambda_minus_one_B23",
            "finite",
            sp.Integer(-1),
            {},
            (r, k, *h, u),
            base,
            3,
            30,
        ),
        audit_module("projective_B01", "infinity", None, {}, (r, k, *h, u), base, 1, 8),
    )


def main():
    audit_pure_and_pairs()
    audit_ordinary_minors()
    modules = audit_special_modules()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "scope": "component 23 normalized s=0, rt=1 all-pair H22 face",
                "method": "no-import subset-DP permanents, fixed-r row clearing, exact Singular modules",
                "module_certificates": modules,
                "all_pair_face_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
