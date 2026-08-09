#!/usr/bin/env python3
"""Exact VERIFIED replay for the exceptional lower-pair marked-H31 fibres."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

from verify_p5_h31_marked_basis_open_branch import (  # noqa: E402
    marked_extension,
    mixed_matrix,
    one_marked_map,
    permanent,
)

THEOREM = HERE / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True,
        encoding="utf-8", capture_output=True, check=True,
    ).stdout.strip()


def add(u, v):
    return tuple(sp.expand(a + b) for a, b in zip(u, v))


def scale(c, u):
    return tuple(sp.expand(c * a) for a in u)


def shifted(alpha, beta, h):
    return tuple(add(beta[i], scale(h[i], alpha[i])) for i in range(4))


def wedge(u, v):
    return tuple(
        sp.factor(u[i] * v[j] - u[j] * v[i])
        for i, j in itertools.combinations(range(4), 2)
    )


def families(x, y, gamma=None):
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    cap_c = (0, 0, 0, 1)
    w = add(scale(x, ell), scale(y, em))
    alpha = (e, em, e, add(cap_c, scale(-1, w)))
    last = ell if gamma is None else add(ell, scale(gamma, e))
    beta = (ell, e, add(cap_c, w), last)
    planes = (
        (e, ell),
        (e, em),
        (e, add(cap_c, w)),
        (last, add(cap_c, scale(-1, w))),
    )
    return alpha, beta, planes


def tensor(alpha, beta):
    return {
        word: sp.factor(permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4))))
        for word in WORDS
    }


def assert_zero(values):
    assert all(sp.factor(value) == 0 for value in values), values


def geometry_and_purity():
    x, y, gamma, pi, theta = sp.symbols("x y gamma pi theta")
    baseline_alpha, baseline_beta, baseline_planes = families(x, y)
    wall_alpha, wall_beta, wall_planes = families(x, y, gamma)
    assert wedge(*baseline_planes[3]) == (0, 0, 0, -2 * y, 1, -1)
    assert wedge(*wall_planes[3]) == (
        -gamma * (x + y), gamma * (x - y), gamma, -2 * y, 1, -1,
    )
    deepest = {x: (pi - theta) / 2, y: (pi + theta) / 2}
    assert sp.factor(wedge(*baseline_planes[3])[3].subs(deepest) + pi + theta) == 0
    for alpha, beta in ((baseline_alpha, baseline_beta), (wall_alpha, wall_beta)):
        coefficients = tensor(alpha, beta)
        assert coefficients[(1, 1, 1, 1)] == -2
        assert_zero(value for word, value in coefficients.items() if word != (1, 1, 1, 1))
        # At a=-1 swap the two lower modes and apply e -> -e; the remaining
        # nonzero wall scalar may be harmlessly reparametrized.
        order = (0, 2, 1, 3)
        swapped = tensor(tuple(alpha[i] for i in order), tuple(beta[i] for i in order))
        assert swapped == coefficients
    return {
        "baseline_V3_pluecker": ["0", "0", "0", "-2*y", "1", "-1"],
        "wall_V3_pluecker": ["-gamma*(x+y)", "gamma*(x-y)", "gamma", "-2*y", "1", "-1"],
        "deepest_parameter_map": {"x": "(pi-theta)/2", "y": "(pi+theta)/2"},
        "sole_pure_coefficient": "-2",
        "a_minus_one_lower_mode_symmetry": True,
    }


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact characteristic-zero projections")


def singular(value):
    return str(sp.cancel(value)).replace("**", "^")


def projection(kind, distinguished, expected):
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    inverse = sp.Symbol("winv")
    x, y, gamma = sp.symbols("x y gamma")
    gamma_inverse = sp.Symbol("ginv")
    alpha, beta, _ = families(x, y, None if kind == "baseline" else gamma)
    marked_beta = shifted(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = mixed_matrix(distinguished, alpha, marked_beta)
    extension = sp.Matrix(z)
    equations = [
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        inverse * (diagonal_b * extension)[0] - 1,
    ]
    if kind == "wall":
        equations.append(gamma_inverse * gamma - 1)
        eliminated = z + (inverse, gamma_inverse)
        blocks = "(dp(10),dp(4),dp(3))"
        parameters = h + (x, y, gamma)
    else:
        eliminated = z + (inverse,)
        blocks = "(dp(9),dp(4),dp(2))"
        parameters = h + (x, y)
    variables = eliminated + parameters
    program = "\n".join((
        "ring R=0,(" + ",".join(map(str, variables)) + ")," + blocks + ";",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + ";",
        "E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        '"CODEX_RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
        "quit;",
    ))
    completed = subprocess.run(
        singular_command(), input=program, cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True, timeout=30, check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [line for line in completed.stdout.splitlines() if line.startswith("CODEX_RESULT:")]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", completed.stdout
    return {
        "family": kind,
        "distinguished": distinguished,
        "ideal": [singular(value) for value in expected],
        "bidirectional_equality": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def projections():
    h0, h1, h2, h3 = sp.symbols("h0:4")
    x, y = sp.symbols("x y")
    baseline = {
        0: (sp.Integer(1),),
        1: (h1, h2, h3),
        2: (h1, h2, h3),
        3: (h3, h1, (x**2 - y**2) * h0 + x * h2, x * h2**2, h0 * h2),
    }
    wall = {
        0: (sp.Integer(1),),
        1: (h0, h1, h2, h3),
        2: (h0, h1, h2, h3),
        3: (h0, h1, h3, x * h2),
    }
    return [
        projection(kind, distinguished, ideals[distinguished])
        for kind, ideals in (("baseline", baseline), ("wall", wall))
        for distinguished in range(4)
    ]


def branch(name, alpha, beta, distinguished, h, expected_rank, expected_a,
           expected_b, minor_rows, expected_minor, transverse):
    marked_beta = shifted(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = mixed_matrix(distinguished, alpha, marked_beta)
    assert mixed.rank() == expected_rank, (name, mixed.rank())
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - expected_rank
    frame = sp.Matrix.hstack(*kernel)
    assert frame.rank() == len(kernel)
    assert_zero(mixed * frame)
    coefficients = sp.symbols(f"r0:{len(kernel)}")
    extension = frame * sp.Matrix(coefficients)
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    assert sp.factor(actual_a - expected_a(*coefficients)) == 0, (name, actual_a)
    assert sp.factor(actual_b - expected_b(*coefficients)) == 0, (name, actual_b)
    marked = marked_extension(distinguished, extension, alpha, marked_beta, 1)
    determinant = sp.factor(marked.extract(minor_rows, range(4)).det())
    assert sp.factor(determinant - expected_minor(*coefficients)) == 0, (name, determinant)
    row, column, value = transverse
    assert sp.factor(one_marked_map(1, alpha, marked_beta)[row, column] - value) == 0
    return {
        "branch": name,
        "rank": expected_rank,
        "nullity": len(kernel),
        "kernel": [[str(sp.factor(value)) for value in vector] for vector in kernel],
        "A": str(actual_a), "B": str(actual_b), "minor": str(determinant),
        "transverse": {"row": row, "column": column, "value": str(value)},
    }


def no_genuine(name, alpha, beta, distinguished, h, expected_rank):
    marked_beta = shifted(alpha, beta, h)
    mixed, diagonal_a, _ = mixed_matrix(distinguished, alpha, marked_beta)
    assert mixed.rank() == expected_rank, (name, mixed.rank())
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - expected_rank
    assert_zero(mixed * sp.Matrix.hstack(*kernel))
    assert all(sp.factor((diagonal_a * vector)[0]) == 0 for vector in kernel)
    return {"branch": name, "rank": expected_rank, "nullity": len(kernel), "A_on_kernel": "zero"}


def branch_certificates():
    x, y, gamma, t = sp.symbols("x y gamma t", nonzero=True)
    baseline_alpha, baseline_beta, _ = families(x, y)
    wall_alpha, wall_beta, _ = families(x, y, gamma)
    results = []
    results.append(branch(
        "baseline-d1-h0", baseline_alpha, baseline_beta, 1, (t, 0, 0, 0), 5,
        lambda X, Y, Z: -2 * X, lambda X, Y, Z: -2 * (X * t + Z),
        (0, 1, 3, 7), lambda X, Y, Z: 8 * X**2 * (X * t + Z), (3, 1, -1),
    ))
    results.append(branch(
        "baseline-d2-h0", baseline_alpha, baseline_beta, 2, (t, 0, 0, 0), 5,
        lambda X, Y, Z: -2 * X, lambda X, Y, Z: 2 * (X * t + Z),
        (0, 1, 3, 7), lambda X, Y, Z: -8 * X**2 * (X * t + Z), (3, 2, 1),
    ))
    d3_cases = (
        ("baseline-d3-origin", baseline_alpha, baseline_beta, (0, 0, 0, 0),
         lambda X, Y: 4 * X * y, lambda X, Y: -2 * Y,
         lambda X, Y: 32 * X**2 * Y * y),
        ("baseline-d3-x=y", *families(y, y)[:2], (t, 0, 0, 0),
         lambda X, Y: 4 * X * y, lambda X, Y: -2 * (2 * X * t * y + Y),
         lambda X, Y: 32 * X**2 * y * (2 * X * t * y + Y)),
        ("baseline-d3-x=-y", *families(-y, y)[:2], (t, 0, 0, 0),
         lambda X, Y: 4 * X * y, lambda X, Y: 2 * (2 * X * t * y - Y),
         lambda X, Y: -32 * X**2 * y * (2 * X * t * y - Y)),
        ("baseline-d3-x=0", *families(0, y)[:2], (0, 0, t, 0),
         lambda X, Y: 4 * X * y, lambda X, Y: -2 * (X * t + Y),
         lambda X, Y: 32 * X**2 * y * (X * t + Y)),
    )
    for name, alpha, beta, h, expected_a, expected_b, determinant in d3_cases:
        results.append(branch(
            name, alpha, beta, 3, h, 6, expected_a, expected_b,
            (0, 1, 5, 7), determinant, (5, 3, -2),
        ))
    results.append(branch(
        "wall-d1-origin", wall_alpha, wall_beta, 1, (0, 0, 0, 0), 5,
        lambda X, Y, Z: -2 * X, lambda X, Y, Z: -2 * Z,
        (0, 1, 3, 7), lambda X, Y, Z: 8 * X**2 * Z, (3, 1, -1),
    ))
    results.append(branch(
        "wall-d2-origin", wall_alpha, wall_beta, 2, (0, 0, 0, 0), 5,
        lambda X, Y, Z: -2 * X, lambda X, Y, Z: 2 * Z,
        (0, 1, 3, 7), lambda X, Y, Z: -8 * X**2 * Z, (3, 2, 1),
    ))
    results.append(branch(
        "wall-d3-x-nonzero", wall_alpha, wall_beta, 3, (0, 0, 0, 0), 6,
        lambda X, Y: 4 * Y * y / gamma,
        lambda X, Y: -2 * (X + 2 * Y * x),
        (0, 1, 5, 7), lambda X, Y: 32 * Y**2 * y * (X + 2 * Y * x) / gamma**2,
        (5, 3, -2),
    ))
    x0_alpha, x0_beta, _ = families(0, y, gamma)
    results.append(branch(
        "wall-d3-x=0", x0_alpha, x0_beta, 3, (0, 0, t, 0), 6,
        lambda X, Y: 4 * Y * y / gamma,
        lambda X, Y: -2 * (X * gamma + Y * t) / gamma,
        (0, 1, 5, 7), lambda X, Y: 32 * Y**2 * y * (X * gamma + Y * t) / gamma**3,
        (5, 3, -2),
    ))
    ordinary_x = sp.Symbol("ordinary_x", nonzero=True)
    results.extend((
        no_genuine("baseline-y0-x-nonzero", *families(ordinary_x, 0)[:2], 3, (0, 0, 0, 0), 4),
        no_genuine("baseline-origin-h0", *families(0, 0)[:2], 3, (t, 0, 0, 0), 2),
        no_genuine("baseline-origin-h2", *families(0, 0)[:2], 3, (0, 0, t, 0), 2),
        no_genuine("wall-y0-x-nonzero", *families(ordinary_x, 0, gamma)[:2], 3, (0, 0, 0, 0), 4),
        no_genuine("wall-origin-h2", *families(0, 0, gamma)[:2], 3, (0, 0, t, 0), 2),
    ))
    return results


def main():
    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "verified_pass": True,
        "role": "proof_a",
        "field": "Q(parameters), characteristic zero",
        "method": "exact permanent matrices, saturated elimination, complete symbolic kernels",
        "scope": "component-15 exceptional support-one lower-pair H31 fibres at a=0,-1",
        "inputs": {THEOREM.name: sha256(THEOREM)},
        "command": "uv run --with sympy python claims/p5/h31/common-active-binary-triangle/verify_p5_h31_common_active_binary_triangle_p_plus_q_exceptional_lower_pair_obstruction.py",
        "outputs": {Path(__file__).name: sha256(Path(__file__))},
        "geometry": geometry_and_purity(),
        "projections": projections(),
        "branches": branch_certificates(),
        "finite_field_computation": False,
        "fresh_independent_verifier_complete": True,
        "limitations": [
            "component-fifteen exceptional support-one lower-pair fibres only",
            "no weighted H22 conclusion",
            "no component-fourteen infinity-endpoint conclusion",
            "no global Krenn-Gu conclusion",
        ],
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
