#!/usr/bin/env python3
"""Verify the generic marked H31 obstruction on P4 component fourteen."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys

import sympy as sp

from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

from verify_p4_directed_zero_divisor_triangle_components import coefficients
from verify_p5_h31_marked_basis_open_branch import marked_extension, mixed_matrix


PIVOT_ROWS = (3, 4, 5, 7, 8, 11)
PIVOT_COLUMNS = tuple(range(6))
FREE_COLUMNS = (6, 7)
MINOR_ROWS = ((0, 1, 4, 7), (0, 4, 5, 7))


def normalized_family(p, q):
    e = (1, 0, 0, 0)
    w = (0, 1, 1, 1)
    u = (0, 1, p, q)
    s1 = (1 - p, 1 + q, -p - q, 0)
    s2 = (1 - q, 1 + p, 0, -p - q)
    cap_s = p + q + 1
    planes = ((e, w), (e, w), (e, u), (s1, s2))
    alpha = (
        e,
        e,
        tuple(cap_s * e[index] - u[index] for index in range(4)),
        tuple(
            (q - 1) * s1[index] - (p - 1) * s2[index]
            for index in range(4)
        ),
    )
    beta = (w, w, e, s1)
    return planes, alpha, beta


def sheet_data(p, q):
    cap_s = p + q + 1
    return {
        1: (
            cap_s / (p + q),
            q / ((p - q) * (p + q - 1)),
        ),
        2: (
            cap_s / (q + 1),
            q * (q + 1) / ((p + q) * (q - 1) * (p - q - 1)),
        ),
        3: (
            cap_s / (p + 1),
            q / ((p + q) * (p - q + 1)),
        ),
    }


def shifted_beta(alpha, beta, point):
    return tuple(
        tuple(
            beta[mode][coordinate] + point[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def projection_ideal(distinguished, alpha, beta, expected):
    p, q = sp.symbols("p q")
    shifts = sp.symbols("t0:4")
    marked_beta = shifted_beta(alpha, beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        inverse * (diagonal_b * extension)[0] - 1,
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    lines = [
        "ring R=(0,p,q),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
        "J=std(J);",
    ]
    if expected is None:
        lines.extend(
            (
                "int same=(reduce(1,J)==0);",
                '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
            )
        )
    else:
        lines.extend(
            (
                "ideal E=" + ",".join(map(singular, expected)) + ";",
                "E=std(E);",
                "ideal JE=reduce(J,E);",
                "ideal EJ=reduce(E,J);",
                "JE=simplify(JE,2);",
                "EJ=simplify(EJ,2);",
                "int same=((size(JE)==0)&&(size(EJ)==0));",
                '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
            )
        )
    lines.append("quit;")
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=80,
        check=False,
    )
    assert completed.returncode == 0, completed
    assert not completed.stderr.strip(), completed.stderr
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(results) == 1, completed.stdout
    fields = results[0].split(":")
    assert fields[1] == "1", completed.stdout
    return {
        "distinguished": distinguished,
        "unit": expected is None,
        "basis_size": int(fields[2]),
    }


def sheet_certificate(distinguished, side):
    assert side == 0
    p, q = sp.symbols("p q")
    x, y = sp.symbols("x y")
    _, alpha, beta = normalized_family(p, q)
    shift, t3 = sheet_data(p, q)[distinguished]
    point = (shift, 0, 0, t3) if side == 0 else (0, shift, 0, t3)
    marked_beta = shifted_beta(alpha, beta, point)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    pivot = mixed.extract(PIVOT_ROWS, PIVOT_COLUMNS)
    free = mixed.extract(PIVOT_ROWS, FREE_COLUMNS)
    solved = -pivot.inv() * free * sp.Matrix((x, y))
    extension = sp.Matrix((*solved, x, y))
    assert all(sp.cancel(value) == 0 for value in mixed * extension)
    left = sp.factor((diagonal_a * extension)[0])
    right = sp.factor((diagonal_b * extension)[0])
    marked = marked_extension(
        distinguished, extension, alpha, marked_beta, 0
    )
    determinants = tuple(
        sp.factor(marked[list(rows), :].det()) for rows in MINOR_ROWS
    )
    common = sp.factor(sp.gcd(*determinants))
    ratio = sp.factor(common / (left * right))
    expected_ratio = {
        1: -2 * (p + q) * (p + q + 1),
        2: -2 * p / ((p + q) * (p - q - 1) ** 2),
        3: 2 * q / ((p + q) * (p - q + 1) ** 2),
    }[distinguished]
    assert sp.factor(ratio - expected_ratio) == 0
    assert not (ratio.free_symbols & {x, y})
    return {
        "distinguished": distinguished,
        "side": side,
        "point": [str(value) for value in point],
        "pivot_determinant": str(sp.factor(pivot.det())),
        "diagonal_a": str(left),
        "diagonal_b": str(right),
        "marked_mode": 0,
        "minor_rows": [list(rows) for rows in MINOR_ROWS],
        "gcd_over_A_B": str(ratio),
    }


def mode_swap_certificate(distinguished, p, q, alpha, beta):
    shift, t3 = sheet_data(p, q)[distinguished]
    beta_left = shifted_beta(alpha, beta, (shift, 0, 0, t3))
    beta_right = shifted_beta(alpha, beta, (0, shift, 0, t3))
    mixed_left, a_left, b_left = mixed_matrix(
        distinguished, alpha, beta_left
    )
    mixed_right, a_right, b_right = mixed_matrix(
        distinguished, alpha, beta_right
    )
    mixed_words = tuple(
        word
        for word in itertools.product((0, 1), repeat=4)
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    row_permutation = tuple(
        mixed_words.index((word[1], word[0], word[2], word[3]))
        for word in mixed_words
    )
    column_permutation = (1, 0, 2, 3, 5, 4, 6, 7)
    assert all(
        sp.cancel(entry) == 0
        for entry in mixed_right
        - mixed_left.extract(row_permutation, column_permutation)
    )
    assert all(
        sp.cancel(entry) == 0
        for entry in a_right - a_left[:, column_permutation]
    )
    assert all(
        sp.cancel(entry) == 0
        for entry in b_right - b_left[:, column_permutation]
    )
    extension = sp.Matrix(sp.symbols("z0:8"))
    permuted_extension = sp.Matrix(
        [extension[index] for index in column_permutation]
    )
    marked_left = marked_extension(
        distinguished, permuted_extension, alpha, beta_left, 0
    )
    marked_right = marked_extension(
        distinguished, extension, alpha, beta_right, 1
    )
    assert all(
        sp.cancel(entry) == 0 for entry in marked_right - marked_left
    )
    return {
        "distinguished": distinguished,
        "mode_permutation": "0<->1",
        "left_sheet_marked_mode": 0,
        "right_sheet_marked_mode": 1,
        "extension_permutation": list(column_permutation),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", nargs=2, type=int)
    arguments = parser.parse_args()
    if arguments.sheet is not None:
        print(json.dumps(sheet_certificate(*arguments.sheet), indent=2))
        return

    p, q = sp.symbols("p q", nonzero=True)
    planes, alpha, beta = normalized_family(p, q)
    tensor = coefficients(tuple(sp.Matrix(plane) for plane in planes))
    expected_tensor = {
        (1, 1, 0, 0): -2 * (p - 1),
        (1, 1, 0, 1): -2 * (q - 1),
        (1, 1, 1, 0): -2 * (p - 1) * (p + q + 1),
        (1, 1, 1, 1): -2 * (q - 1) * (p + q + 1),
    }
    assert all(
        sp.factor(value - expected_tensor.get(word, 0)) == 0
        for word, value in tensor.items()
    )
    pure_tensor = coefficients(
        tuple(sp.Matrix((alpha[mode], beta[mode])) for mode in range(4))
    )
    assert sp.factor(pure_tensor[(1, 1, 1, 1)] + 2 * (p - 1)) == 0
    assert all(
        value == 0
        for word, value in pure_tensor.items()
        if word != (1, 1, 1, 1)
    )

    t0, t1, t2, t3 = sp.symbols("t0:4")
    cap_s = p + q + 1
    expected_projection = {
        0: None,
        1: (
            (p**2 - p - q**2 + q) * t3 - q,
            t2,
            (p + q) * (t0 + t1) - cap_s,
            (p + q) * t1**2 - cap_s * t1,
        ),
        2: (
            (p**2 * q - p**2 - p * q + p - q**3 + q) * t3
            - q * (q + 1),
            t2,
            (q + 1) * (t0 + t1) - cap_s,
            (q + 1) * t1**2 - cap_s * t1,
        ),
        3: (
            (p**2 + p - q**2 + q) * t3 - q,
            t2,
            (p + 1) * (t0 + t1) - cap_s,
            (p + 1) * t1**2 - cap_s * t1,
        ),
    }
    projections = tuple(
        projection_ideal(distinguished, alpha, beta, expected_projection[distinguished])
        for distinguished in range(4)
    )

    certificates = []
    symmetry_certificates = []
    for distinguished in (1, 2, 3):
        completed = subprocess.run(
            (
                sys.executable,
                __file__,
                "--sheet",
                str(distinguished),
                "0",
            ),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=100,
            check=False,
        )
        assert completed.returncode == 0, completed
        certificate = json.loads(completed.stdout)
        certificate["covers_sheet_side_one_by_mode_swap"] = True
        certificates.append(certificate)
        symmetry_certificates.append(
            mode_swap_certificate(distinguished, p, q, alpha, beta)
        )

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "C(p,q)",
                "source_torus_quotient_dimension": 2,
                "projected_marking_sheets": 6,
                "projections": projections,
                "sheet_certificates": certificates,
                "mode_swap_certificates": symmetry_certificates,
                "generic_H31_fibre_component_14": "empty",
                "global_conjecture": "unresolved",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
