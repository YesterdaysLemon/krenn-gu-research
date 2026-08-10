#!/usr/bin/env python3
"""Exact generic weighted-H22 obstruction candidate for component twenty-one."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
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
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / (
    "P5_H22_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_"
    "OBSTRUCTION_CANDIDATE.md"
)
CERTIFICATE = ROOT / (
    "p5_h22_coincident_support_rank_one_star_component_generic_certificate.json"
)
COMPONENT = REPO_ROOT / "claims/p4/classifications/star/coincident-support-rank-one-star/P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md"
H31 = REPO_ROOT / "claims/p5/h31/coincident-support-rank-one-star/P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
H22_DEFINITION = REPO_ROOT / "claims/p5/h22/common-singleton/P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True, encoding="utf-8",
        capture_output=True, check=True,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent3(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(3))
        for permutation in PERMUTATIONS3
    ))


def permanent4(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(4))
        for permutation in PERMUTATIONS4
    ))


def pure_bases(p, q, kappa, ell):
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


def shifted_beta(alpha, beta, shifts):
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


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


def build_model(alpha, beta, extensions, direction, chart, slope=None):
    alpha_rows = tuple(
        project(alpha[i], extensions[i], direction, chart, slope) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extensions[4 + i], direction, chart, slope)
        for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[i] if word[i] else alpha_rows[i] for i in range(4)
        )
        coefficients[word] = sp.expand(sum(
            selected[i][3]
            * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
            for i in range(4)
        ))
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], value) for value in extensions]
        for word in MIXED
    ])
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "mixed": mixed,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def verify_d01_hall(alpha):
    rho, sigma = sp.symbols("rho sigma")
    extensions = sp.symbols("u0:4")
    rows = tuple(
        (rho * alpha[i][0] + sigma * alpha[i][1], alpha[i][2], alpha[i][3], extensions[i])
        for i in range(4)
    )
    supports = tuple(
        tuple(index for index, entry in enumerate(row) if entry != 0)
        for row in rows[:3]
    )
    assert supports == ((0, 3), (0, 3), (0, 3))
    summands = tuple(
        sp.expand(sp.prod(rows[i][permutation[i]] for i in range(4)))
        for permutation in PERMUTATIONS4
    )
    assert all(value == 0 for value in summands)
    assert permanent4(rows) == 0
    return {
        "hall_row_set_size": 3,
        "hall_column_neighborhood_size": 2,
        "common_supports": [list(support) for support in supports],
        "homogeneous_all_alpha_diagonal": "0",
        "permanent_summands_checked": len(summands),
    }


def finite_d23_certificate(alpha, beta, p, q, kappa, ell):
    slope = sp.Symbol("lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    marked_beta = shifted_beta(alpha, beta, shifts)
    model = build_model(
        alpha, marked_beta, extensions, "D23", "finite", slope
    )
    equations = (*tuple(model["mixed"] * sp.Matrix(extensions)), model["A"] - 1)

    delta = p**2 - q**2
    eps = ell**2 - 1
    f1 = sp.expand(
        kappa * delta * eps * shifts[0] * shifts[1]
        - delta * shifts[0] * shifts[2]
        - p * eps * shifts[1] * shifts[2]
        + kappa * ell * delta * shifts[0]
        - q * kappa * eps * shifts[1]
        + (q - p * ell) * shifts[2]
        + kappa * (p - q * ell)
    )
    f2 = sp.expand(
        (shifts[2] - kappa)
        * (shifts[2] + kappa)
        * (p * eps * shifts[1] + p * ell + delta * shifts[0] - q)
    )
    f3 = sp.expand(
        (shifts[2] - kappa)
        * (shifts[2] + kappa)
        * ((ell - 1) * shifts[1] + 1)
        * ((ell + 1) * shifts[1] + 1)
    )
    expected = (slope + 1, shifts[3], f1, f2, f3)
    variables = extensions + shifts + (slope,)
    program = "\n".join((
        "ring R=(0,p,q,kappa,ell),("
        + ",".join(map(str, variables)) + "),(dp(8),dp(5));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, extensions)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + ";",
        "E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        "poly b=" + singular(model["B"]) + ";",
        "poly rb=reduce(b,I);",
        (
            '"CODEX_RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"'
            '+string(rb==0)+":"+string(size(I))+":"+string(size(J));'
        ),
        "quit;",
    ))
    completed = subprocess.run(
        singular_command(), input=program, cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True, timeout=120, check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1
    _, same, beta_zero, ideal_size, projection_size = markers[0].split(":")
    assert same == "1" and beta_zero == "1", completed.stdout
    return {
        "chart": "finite [lambda:1]",
        "normalized_all_alpha_projection": [
            "lambda+1", "h3", "F1", "F2", "F3"
        ],
        "F1": str(sp.factor(f1)),
        "F2": str(sp.factor(f2)),
        "F3": str(sp.factor(f3)),
        "bidirectional_projection_equality": True,
        "normalized_mixed_ideal_basis_size": int(ideal_size),
        "projection_basis_size": int(projection_size),
        "all_beta_remainder_in_normalized_mixed_ideal": "0",
        "genuine_binary_incidence_empty": True,
    }


def infinity_d23_certificate(alpha, beta):
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    marked_beta = shifted_beta(alpha, beta, shifts)
    model = build_model(alpha, marked_beta, extensions, "D23", "infinity")
    mixed = model["mixed"]
    diagonal_a = sp.Matrix([[sp.diff(model["A"], value) for value in extensions]])
    diagonal_b = sp.Matrix([[sp.diff(model["B"], value) for value in extensions]])
    generators = ",".join(
        "[" + ",".join(singular(mixed[row, column]) for column in range(8)) + "]"
        for row in range(14)
    )
    alpha_row = "[" + ",".join(singular(value) for value in diagonal_a.row(0)) + "]"
    beta_row = "[" + ",".join(singular(value) for value in diagonal_b.row(0)) + "]"
    program = "\n".join((
        "ring R=(0,p,q,kappa,ell),(h0,h1,h2,h3),dp;",
        "option(redSB);",
        "module M=" + generators + ";",
        "M=std(M);",
        "vector a=" + alpha_row + ";",
        "vector b=" + beta_row + ";",
        "vector ra=reduce(a,M);",
        "vector rb=reduce(b,M);",
        '"CODEX_RESULT:"+string(ra==0)+":"+string(rb!=0)+":"+string(size(M));',
        "quit;",
    ))
    completed = subprocess.run(
        singular_command(), input=program, cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True, timeout=120, check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1
    _, alpha_zero, beta_nonzero, size = markers[0].split(":")
    assert alpha_zero == "1" and beta_nonzero == "1", completed.stdout
    return {
        "chart": "infinity [1:0]",
        "all_alpha_in_mixed_row_module": True,
        "all_beta_normal_form_nonzero": True,
        "standard_module_basis_size": int(size),
        "genuine_binary_incidence_empty": True,
    }


def alpha_only_survivor(alpha, beta, p, q, kappa, ell):
    extensions = sp.symbols("x0:8")
    shifts = (1 / (p - q), 0, kappa, 0)
    marked_beta = shifted_beta(alpha, beta, shifts)
    model = build_model(
        alpha, marked_beta, extensions, "D23", "finite", sp.Integer(-1)
    )
    vector = sp.Matrix((
        -q / kappa,
        -1 / kappa,
        0,
        0,
        -p / (kappa * (p - q)),
        0,
        1,
        0,
    ))
    values = dict(zip(extensions, vector, strict=True))
    assert all(
        sp.factor(value.subs(values)) == 0
        for word, value in model["coefficients"].items()
        if word not in (WORDS[0], WORDS[-1])
    )
    alpha_value = sp.factor(model["A"].subs(values))
    beta_value = sp.factor(model["B"].subs(values))
    assert sp.factor(alpha_value - 4 * (p - q) / kappa) == 0
    assert beta_value == 0
    specialized_mixed = model["mixed"].subs(values)
    assert all(
        sp.factor(value) == 0 for value in specialized_mixed * vector
    )
    return {
        "weight": "[-1:1]",
        "marking": "h0=1/(p-q), h1=0, h2=kappa, h3=0",
        "extension": [str(sp.factor(value)) for value in vector],
        "all_alpha_diagonal": str(alpha_value),
        "all_beta_diagonal": str(beta_value),
        "status": "exact one-diagonal survivor, not binary",
    }


def main():
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["claim_label"] == "VERIFIED"
    p, q, kappa, ell = sp.symbols("p q kappa ell")
    alpha, beta = pure_bases(p, q, kappa, ell)
    pure = {
        word: sp.factor(permanent4(tuple(
            beta[i] if word[i] else alpha[i] for i in range(4)
        )))
        for word in WORDS
    }
    assert pure[WORDS[-1]] == 4 * p
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    hall = verify_d01_hall(alpha)
    finite = finite_d23_certificate(alpha, beta, p, q, kappa, ell)
    infinity = infinity_d23_certificate(alpha, beta)
    survivor = alpha_only_survivor(alpha, beta, p, q, kappa, ell)
    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "discovery_claim_label": "CANDIDATE",
        "scope": certificate["scope"],
        "inputs": {
            COMPONENT.name: sha256(COMPONENT),
            H31.name: sha256(H31),
            H22_DEFINITION.name: sha256(H22_DEFINITION),
        },
        "method": certificate["method"],
        "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "pure_support": {"1111": "4*p"},
        "D01_hall_certificate": hall,
        "D23_finite_certificate": finite,
        "D23_infinity_certificate": infinity,
        "retained_alpha_only_survivor": survivor,
        "shared_D01_pure_D23_binary_compatibility": "empty because D23 has no genuine binary point",
        "generic_weighted_H22_fibre_empty": True,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": certificate["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
