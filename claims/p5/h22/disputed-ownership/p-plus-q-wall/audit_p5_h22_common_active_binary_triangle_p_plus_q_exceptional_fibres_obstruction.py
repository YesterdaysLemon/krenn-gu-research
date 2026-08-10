#!/usr/bin/env python3
"""No-primary-import exact replay of the verified exceptional weighted-H22 claim."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
NOTE = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_FIBRES_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_obstruction.py"
)
P4 = REPO_ROOT / "claims/p4/boundaries/component20-p-plus-q-wall/P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
H31 = (
    REPO_ROOT / "claims/p5/h31/common-active-binary-triangle/P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md"
)
H22 = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERM3 = tuple(itertools.permutations(range(3)))
PERM4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def add(*vectors):
    return tuple(sp.expand(sum(values)) for values in zip(*vectors))


def scale(coefficient, vector):
    return tuple(sp.expand(coefficient * value) for value in vector)


def permanent3(rows, columns=(0, 1, 2)):
    return sp.expand(
        sum(
            rows[0][columns[p[0]]] * rows[1][columns[p[1]]] * rows[2][columns[p[2]]]
            for p in PERM3
        )
    )


def permanent4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERM4))


def direct_bases(chart, a, lam, h):
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    cap_c = (0, 0, 0, 1)
    alpha = (scale(2 * a + 1, cap_c), e, e, em)
    beta0 = (
        add(e, scale(lam, ell)) if chart == "B_full" else ell,
        add(scale(a + 1, ell), cap_c),
        add(scale(a, ell), cap_c),
        e,
    )
    beta = tuple(add(beta0[i], scale(h[i], alpha[i])) for i in range(4))
    return alpha, beta


def lower_bases(x, y, gamma, h):
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    cap_c = (0, 0, 0, 1)
    w = add(scale(x, ell), scale(y, em))
    alpha = (e, em, e, add(cap_c, scale(-1, w)))
    beta0 = (ell, e, add(cap_c, w), ell if gamma is None else add(ell, scale(gamma, e)))
    beta = tuple(add(beta0[i], scale(h[i], alpha[i])) for i in range(4))
    return alpha, beta


def contract(row, extension, direction, slope):
    if direction == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    return (row[0], row[2], row[3], extension)


def model(alpha, beta, direction, slope):
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        contract(alpha[i], extensions[i], direction, slope) for i in range(4)
    )
    beta_rows = tuple(
        contract(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        chosen = tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        coefficients[word] = sp.expand(
            sum(
                chosen[i][3] * permanent3(tuple(chosen[j] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    mixed = sp.Matrix(
        [
            [coefficients[word].coeff(extension) for extension in extensions]
            for word in MIXED
        ]
    )
    return {
        "extensions": extensions,
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "mixed": mixed,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def marked_matrix(data, mode):
    other = tuple(i for i in range(4) if i != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        chosen = tuple(
            data["beta_rows"][j] if bits[i] else data["alpha_rows"][j]
            for i, j in enumerate(other)
        )
        rows.append(
            tuple(
                permanent3(chosen, tuple(k for k in range(4) if k != column))
                for column in range(4)
            )
        )
    return sp.Matrix(rows)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def projection(label, data, expected, parameters=(), invert=(), finite=False):
    h = sp.symbols("h0:4")
    winv = sp.Symbol("winv")
    equations = [
        *tuple(data["mixed"] * sp.Matrix(data["extensions"])),
        data["A"] - 1,
        winv * data["B"] - 1,
    ]
    eliminated = data["extensions"] + (winv,)
    if finite:
        eliminated += (sp.Symbol("r"),)
    for parameter, inverse_name in invert:
        inverse = sp.Symbol(inverse_name)
        equations.append(inverse * parameter - 1)
        eliminated += (inverse,)
    variables = eliminated + h + tuple(parameters)
    order = f"(dp({len(eliminated)}),dp(4)"
    if parameters:
        order += f",dp({len(parameters)})"
    order += ")"
    program = "\n".join(
        (
            "ring rr=0,(" + ",".join(map(str, variables)) + ")," + order + ";",
            "option(redSB);",
            "ideal ii=" + ",".join(map(singular, equations)) + ";",
            "ii=slimgb(ii);",
            "ideal jj=std(eliminate(ii," + "*".join(map(str, eliminated)) + "));",
            "ideal ee=" + ",".join(map(singular, expected)) + "; ee=std(ee);",
            "ideal lr=simplify(reduce(jj,ee),2);",
            "ideal rl=simplify(reduce(ee,jj),2);",
            '"RESULT:"+string((size(lr)==0)&&(size(rl)==0));',
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
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed,
    )
    assert "RESULT:1" in completed.stdout, (label, completed.stdout)
    return {"label": label, "ideal": [singular(value) for value in expected]}


def projection_audit():
    h0, h1, h2, h3 = sp.symbols("h0:4")
    h = (h0, h1, h2, h3)
    lam, r = sp.symbols("lambda r")
    certificates = []
    for a in (0, -1):
        expected = (h3, h2, h0) if a == 0 else (h3, h1, h0)
        for chart in ("B_full", "B_drop"):
            alpha, beta = direct_bases(chart, sp.Integer(a), lam, h)
            for direction in ("finite", "infinity"):
                parameters = (lam,) if chart == "B_full" else ()
                inverses = ((lam, "linv"),) if chart == "B_full" else ()
                certificates.append(
                    projection(
                        f"a={a}:{chart}:{direction}",
                        model(alpha, beta, direction, r),
                        expected,
                        parameters,
                        inverses,
                        direction == "finite",
                    )
                )
    x, y, gamma = sp.symbols("x y gamma")
    for family in ("baseline", "wall"):
        alpha, beta = lower_bases(x, y, None if family == "baseline" else gamma, h)
        for direction in ("finite", "infinity"):
            expected = (
                (h3, h2, h1, h0)
                if family == "wall" and direction == "infinity"
                else (h3, h2, h1)
            )
            parameters = (x, y) if family == "baseline" else (x, y, gamma)
            inverses = () if family == "baseline" else ((gamma, "ginv"),)
            certificates.append(
                projection(
                    f"lower:{family}:{direction}",
                    model(alpha, beta, direction, r),
                    expected,
                    parameters,
                    inverses,
                    direction == "finite",
                )
            )
    assert len(certificates) == 12
    return certificates


def kernel_check(
    label, data, expected_rank, mode, rows, expected_a, expected_b, expected_det
):
    mixed = data["mixed"]
    assert mixed.rank() == expected_rank
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - expected_rank
    frame = sp.Matrix.hstack(*kernel)
    assert frame.rank() == len(kernel), label
    assert all(sp.factor(value) == 0 for value in mixed * frame), label
    coefficients = sp.symbols(f"X0:{len(kernel)}")
    substitution = dict(zip(data["extensions"], frame * sp.Matrix(coefficients)))
    actual_a = sp.factor(data["A"].subs(substitution))
    actual_b = sp.factor(data["B"].subs(substitution))
    determinant = sp.factor(
        marked_matrix(data, mode).subs(substitution).extract(rows, range(4)).det()
    )
    assert sp.factor(actual_a - expected_a(*coefficients)) == 0, (label, actual_a)
    assert sp.factor(actual_b - expected_b(*coefficients)) == 0, (label, actual_b)
    assert sp.factor(determinant - expected_det(*coefficients)) == 0, (
        label,
        determinant,
    )
    return {
        "label": label,
        "rank": expected_rank,
        "kernel_dimension": len(kernel),
        "minor": str(determinant),
    }


def no_genuine(label, data, diagonal, expected_rank):
    mixed = data["mixed"]
    assert mixed.rank() == expected_rank
    expression = data[diagonal]
    kernel = mixed.nullspace()
    assert all(
        sp.factor(expression.subs(dict(zip(data["extensions"], vector)))) == 0
        for vector in kernel
    )
    return {"label": label, "rank": expected_rank, f"{diagonal}_on_kernel": "zero"}


def kernel_audit():
    lam, r, t = sp.symbols("lambda r t", nonzero=True)
    results = []
    specs = (
        (
            0,
            "B_full",
            "finite",
            6,
            (0, 2, 4, 7),
            lambda X, Y: -2 * Y * r,
            lambda X, Y: -2 * (lam + r) * (X * r + Y * (r * t + 1)),
            lambda X, Y: -8 * Y**2 * lam * r**2 * (lam + r) * (X * r + Y * (r * t + 1)),
        ),
        (
            0,
            "B_full",
            "infinity",
            6,
            (0, 2, 4, 7),
            lambda X, Y: -2 * Y,
            lambda X, Y: -2 * (X * lam + Y),
            lambda X, Y: -8 * Y**2 * lam * (X * lam + Y),
        ),
        (
            0,
            "B_drop",
            "finite",
            6,
            (0, 2, 4, 7),
            lambda X, Y: -2 * Y * r,
            lambda X, Y: -2 * (X * r + Y * (r * t + 1)),
            lambda X, Y: -8 * Y**2 * r**2 * (X * r + Y * (r * t + 1)),
        ),
        (
            0,
            "B_drop",
            "infinity",
            5,
            (0, 2, 4, 7),
            lambda X, Y, Z: -2 * Z,
            lambda X, Y, Z: -2 * X,
            lambda X, Y, Z: -8 * X * Z**2,
        ),
        (
            -1,
            "B_full",
            "finite",
            6,
            (0, 1, 4, 7),
            lambda X, Y: 2 * Y * r,
            lambda X, Y: -2 * (X * lam * r - Y * (lam + r)),
            lambda X, Y: 8 * Y**2 * lam * r**2 * (X * lam * r - Y * (lam + r)),
        ),
        (
            -1,
            "B_full",
            "infinity",
            6,
            (0, 1, 4, 7),
            lambda X, Y: 2 * Y,
            lambda X, Y: -2 * (X * lam - Y),
            lambda X, Y: 8 * Y**2 * lam * (X * lam - Y),
        ),
        (
            -1,
            "B_drop",
            "finite",
            6,
            (0, 1, 4, 7),
            lambda X, Y: 2 * Y * r,
            lambda X, Y: -2 * (X * r - Y),
            lambda X, Y: 8 * Y**2 * r**2 * (X * r - Y),
        ),
        (
            -1,
            "B_drop",
            "infinity",
            5,
            (0, 1, 4, 7),
            lambda X, Y, Z: 2 * Z,
            lambda X, Y, Z: -2 * Y,
            lambda X, Y, Z: 8 * Y * Z**2,
        ),
    )
    for a, chart, direction, rank, rows, expected_a, expected_b, expected_det in specs:
        h = (0, t, 0, 0) if a == 0 else (0, 0, t, 0)
        alpha, beta = direct_bases(chart, sp.Integer(a), lam, h)
        results.append(
            kernel_check(
                f"a={a}:{chart}:{direction}",
                model(alpha, beta, direction, r),
                rank,
                3,
                rows,
                expected_a,
                expected_b,
                expected_det,
            )
        )
    for a in (0, -1):
        h = (0, t, 0, 0) if a == 0 else (0, 0, t, 0)
        for chart in ("B_full", "B_drop"):
            alpha, beta = direct_bases(chart, sp.Integer(a), lam, h)
            results.append(
                no_genuine(
                    f"a={a}:{chart}:r=0", model(alpha, beta, "finite", 0), "A", 1
                )
            )
    alpha, beta = direct_bases("B_full", -1, lam, (0, 0, t, 0))
    results.append(
        no_genuine("a=-1:B_full:r=-lambda", model(alpha, beta, "finite", -lam), "B", 6)
    )

    x, y, gamma = sp.symbols("x y gamma", nonzero=True)
    alpha, beta = lower_bases(x, y, None, (t, 0, 0, 0))
    results.append(
        kernel_check(
            "lower:baseline:finite",
            model(alpha, beta, "finite", r),
            6,
            1,
            (0, 1, 3, 7),
            lambda X, Y: -2 * X * r,
            lambda X, Y: -2 * X * (r * t + 1),
            lambda X, Y: 8 * X**3 * r**2 * (r * t + 1),
        )
    )
    results.append(
        kernel_check(
            "lower:baseline:infinity",
            model(alpha, beta, "infinity", r),
            5,
            1,
            (0, 1, 3, 7),
            lambda X, Y, Z: -2 * X,
            lambda X, Y, Z: -2 * (X * t + Z),
            lambda X, Y, Z: 8 * X**2 * (X * t + Z),
        )
    )
    alpha, beta = lower_bases(x, y, gamma, (t, 0, 0, 0))
    results.append(
        kernel_check(
            "lower:wall:finite",
            model(alpha, beta, "finite", r),
            6,
            1,
            (0, 1, 3, 7),
            lambda X, Y: -2 * Y * r / (gamma * (r * t + 1)),
            lambda X, Y: -2 * Y * (gamma * r + 1) / gamma,
            lambda X, Y: (
                8 * Y**3 * r**2 * (gamma * r + 1) / (gamma**3 * (r * t + 1) ** 2)
            ),
        )
    )
    alpha, beta = lower_bases(x, y, gamma, (0, 0, 0, 0))
    results.append(
        kernel_check(
            "lower:wall:infinity",
            model(alpha, beta, "infinity", r),
            5,
            1,
            (0, 1, 3, 7),
            lambda X, Y, Z: -2 * X,
            lambda X, Y, Z: -2 * Z,
            lambda X, Y, Z: 8 * X**2 * Z,
        )
    )
    alpha, beta = lower_bases(x, y, gamma, (t, 0, 0, 0))
    results.append(
        no_genuine("lower:wall:r=0", model(alpha, beta, "finite", 0), "A", 1)
    )
    alpha, beta = lower_bases(x, y, gamma, (-1 / r, 0, 0, 0))
    results.append(
        no_genuine("lower:wall:r*t+1=0", model(alpha, beta, "finite", r), "B", 6)
    )
    assert len(results) == 19
    return results


def geometry_audit():
    x, y, gamma, lam = sp.symbols("x y gamma lambda", nonzero=True)
    direct = {}
    for a in (0, -1):
        for chart in ("B_full", "B_drop"):
            alpha, beta = direct_bases(chart, a, lam, (0, 0, 0, 0))
            coefficients = {
                word: permanent4(
                    tuple(beta[i] if word[i] else alpha[i] for i in range(4))
                )
                for word in WORDS
            }
            expected = (-2 * lam if chart == "B_full" else -2) * (1 if a == 0 else -1)
            assert coefficients[WORDS[-1]] == expected
            assert all(
                value == 0 for word, value in coefficients.items() if word != WORDS[-1]
            )
            direct[f"a={a}:{chart}"] = str(expected)
    lower = {}
    for family, parameter in (("baseline", None), ("wall", gamma)):
        alpha, beta = lower_bases(x, y, parameter, (0, 0, 0, 0))
        coefficients = {
            word: permanent4(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
            for word in WORDS
        }
        assert coefficients[WORDS[-1]] == -2
        assert all(
            value == 0 for word, value in coefficients.items() if word != WORDS[-1]
        )
        lower[family] = "-2"
    return {"direct": direct, "lower": lower}


def main():
    report = {
        "status": "pass",
        "role": "proof_b",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": "no-primary-import replay of the verified a=0,-1 diagonal-DVR weighted-H22 obstruction",
        "inputs": {path.name: sha256(path) for path in (P4, H31, H22, NOTE, PRIMARY)},
        "method": "fresh permanent and contraction code, bidirectional saturated elimination, complete symbolic kernels, and fixed minors",
        "command": 'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_obstruction.py',
        "outputs": {Path(__file__).name: sha256(Path(__file__))},
        "limitations": "secondary proof_b replay; external no-import verifier separately completed; same bounded diagonal-DVR scope",
        "imports_primary": False,
        "geometry": geometry_audit(),
        "projections": projection_audit(),
        "kernels": kernel_audit(),
        "finite_field_computation_used": False,
        "verified_claim_replayed": True,
        "fresh_independent_verifier_complete": True,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
