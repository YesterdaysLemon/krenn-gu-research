#!/usr/bin/env python3
"""No-import audit of marked H31 on component 23's s=0, rt=1 face."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
PRIMARY = (
    ROOT
    / "verify_p5_h31_common_center_kernel_star_component_s_zero_rt_one_all_pair_obstruction.py"
)
BITS = tuple(itertools.product((0, 1), repeat=4))
PERMS = tuple(itertools.permutations(range(4)))
r, k, g = sp.symbols("r k g")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
c, p, q, w = sp.symbols("c p q w")
u, v = sp.symbols("u v")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*vectors):
    return tuple(sp.expand(sum(vector[j] for vector in vectors)) for j in range(4))


def scale(a, vector):
    return tuple(sp.expand(a * value) for value in vector)


def permanent(vectors):
    return sp.expand(
        sum(sp.prod(vectors[i][sigma[i]] for i in range(4)) for sigma in PERMS)
    )


def face_rows():
    alpha = (A, add(A, scale(k, D)), add(B, scale(r, D)), add(B, scale(1 / r, D)))
    beta = (B, B, C, C)
    return alpha, beta


def shifted(alpha, beta, shifts=h):
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def extension_coefficients(d, alpha, beta, z):
    common = tuple(i for i in range(4) if i != d)
    aa = tuple(tuple(alpha[i][j] for j in common) + (z[i],) for i in range(4))
    bb = tuple(tuple(beta[i][j] for j in common) + (z[4 + i],) for i in range(4))
    return {
        word: permanent(tuple(bb[i] if word[i] else aa[i] for i in range(4)))
        for word in BITS
    }


def mixed_data(d, alpha, beta):
    coefficients = extension_coefficients(d, alpha, beta, sp.Matrix(x))
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in x]
            for word in BITS
            if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
        ]
    )
    diagonals = tuple(
        sp.Matrix([[sp.diff(coefficients[word], variable) for variable in x]])
        for word in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    return mixed, *diagonals


def one_marked(mode, alpha, beta):
    result = []
    for bits in itertools.product((0, 1), repeat=3):
        selected, bit = [], 0
        for i in range(4):
            if i == mode:
                selected.append(None)
            else:
                selected.append(beta[i] if bits[bit] else alpha[i])
                bit += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(j == coordinate) for j in range(4))
            row.append(
                permanent(tuple(basis if i == mode else selected[i] for i in range(4)))
            )
        result.append(row)
    return sp.Matrix(result)


def neighbour_marked(d, z, alpha, beta, mode):
    common = tuple(i for i in range(4) if i != d)
    aa = tuple(tuple(alpha[i][j] for j in common) + (z[i],) for i in range(4))
    bb = tuple(tuple(beta[i][j] for j in common) + (z[4 + i],) for i in range(4))
    return one_marked(mode, aa, bb)


def stacked(d, z, alpha, beta, mode):
    neighbour = neighbour_marked(d, z, alpha, beta, mode)
    pure = one_marked(mode, alpha, beta)
    common = tuple(i for i in range(4) if i != d) + (4,)
    result = sp.zeros(16, 5)
    for row in range(8):
        for j, coordinate in enumerate(common):
            result[row, coordinate] = neighbour[row, j]
        for coordinate in range(4):
            result[8 + row, coordinate] = pure[row, coordinate]
    return result


def singular_command():
    native = shutil.which("Singular")
    return (
        (native, "-q") if native else ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    )


def projection_audit(d, alpha, beta):
    mixed, da, db = mixed_data(d, alpha, shifted(alpha, beta))
    z = sp.Matrix(x)
    equations = (
        *tuple(mixed * z),
        (da * z)[0] - 1,
        u * (db * z)[0] - 1,
        v * r * (r * r - 1) - 1,
    )
    equations = tuple(sp.fraction(sp.together(value))[0] for value in equations)
    eliminated = x + (u,)
    variables = eliminated + (r, k, v) + h
    source = [
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(3),dp(4));",
        "option(redSB);",
        "ideal I="
        + ",".join(str(sp.expand(value)).replace("**", "^") for value in equations)
        + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    if d < 2:
        source.append('print("RESULT:"+string(reduce(1,J)==0));')
    else:
        source.extend(
            (
                "ideal E=v*r*(r^2-1)-1,h0,h1,h2*h3; E=std(E);",
                "ideal A=simplify(reduce(J,E),2); ideal B=simplify(reduce(E,J),2);",
                'print("RESULT:"+string((size(A)==0)&&(size(B)==0)));',
            )
        )
    source.append("quit;")
    completed = subprocess.run(
        singular_command(),
        input="\n".join(source),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=360,
        check=False,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    assert markers == ["RESULT:1"], (d, completed.stdout)
    return d


def punctured_audit(alpha, beta):
    cases = (
        (
            2,
            (0, 0, 0, g),
            (0, k * q, c, p, q, w, 0, g * c / r),
            2,
            (
                8 * g * (p * r - c) * (q + w) * (r - 1) * (p * r + (r - 1) * w) / r**3,
                8 * g**2 * (p * r - c) * (q + w) * (r - 1) * (c + (r - 1) * w) / r**3,
            ),
            2 * (r - 1) / r,
        ),
        (
            2,
            (0, 0, g, 0),
            (0, k * q, p, c, q, w, g * r * c, 0),
            3,
            (
                -8 * g * (p - c * r) * (q + w) * (r - 1) * (p - (r - 1) * w),
                8 * g**2 * (p - c * r) * (q + w) * (r - 1) * (-c * r + (r - 1) * w),
            ),
            -2 * (r - 1),
        ),
        (
            3,
            (0, 0, 0, g),
            (0, -k * q, c, p, q, w, 0, -g * c / r),
            2,
            (
                8 * g * (p * r + c) * (q + w) * (r + 1) * (p * r + (r + 1) * w) / r**3,
                8 * g**2 * (p * r + c) * (q + w) * (r + 1) * (-c + (r + 1) * w) / r**3,
            ),
            2 * (r + 1) / r,
        ),
        (
            3,
            (0, 0, g, 0),
            (0, -k * q, p, c, q, w, -g * r * c, 0),
            3,
            (
                8 * g * (p + c * r) * (q + w) * (r + 1) * (p + (r + 1) * w),
                8 * g**2 * (p + c * r) * (q + w) * (r + 1) * (-c * r + (r + 1) * w),
            ),
            2 * (r + 1),
        ),
    )
    for d, shifts, entries, mode, expected_minors, transverse in cases:
        beta_h = shifted(alpha, beta, shifts)
        mixed, da, db = mixed_data(d, alpha, beta_h)
        z = sp.Matrix(entries)
        assert all(sp.factor(value) == 0 for value in mixed * z)
        expected_da = {
            (2, True): 2 * (r - 1) * (c / r - p),
            (2, False): 2 * (r - 1) * (p / r - c),
            (3, True): 2 * (r + 1) * (p + c / r),
            (3, False): 2 * (r + 1) * (p / r + c),
        }[(d, shifts[2] == 0)]
        assert sp.factor((da * z)[0] - expected_da) == 0
        assert sp.factor((db * z)[0] + 2 * (q + w)) == 0
        neighbour = neighbour_marked(d, z, alpha, beta_h, mode)
        minors = tuple(
            sp.factor(neighbour.extract(rows, range(4)).det())
            for rows in ((0, 1, 2, 7), (0, 1, 3, 7))
        )
        assert all(
            sp.factor(value - expected) == 0
            for value, expected in zip(minors, expected_minors)
        )
        assert sp.factor(one_marked(mode, alpha, beta_h)[0, d] - transverse) == 0
    return len(cases)


def intersection_audit(alpha, beta):
    output = []
    for d, entries, diagonal, determinant_sign, gamma_sign in (
        (2, (0, k * q, c, p, q, w, 0, 0), p * r - c, -1, 1),
        (3, (0, -k * q, c, p, q, w, 0, 0), p * r + c, 1, -1),
    ):
        z = sp.Matrix(entries)
        matrix = stacked(d, z, alpha, beta, 0)
        observed = sp.factor(matrix.extract((0, 7, 11, 13, 15), range(5)).det())
        expected = sp.factor(
            determinant_sign * 64 * k * diagonal * (r + (1 if d == 3 else -1)) / r
        )
        assert sp.factor(observed - expected) == 0
        gammas = (
            sp.Matrix((0, 0, gamma_sign, -gamma_sign, w)),
            sp.Matrix((0, 0, gamma_sign, -gamma_sign, q)),
        )
        for mode, gamma in enumerate(gammas):
            matrix0 = stacked(d, z, alpha, beta, mode).subs(k, 0)
            assert all(sp.factor(value) == 0 for value in matrix0 * gamma)
            minor = sp.factor(matrix0.extract((0, 7, 13, 15), (0, 1, 2, 4)).det())
            expected4 = sp.factor(
                determinant_sign * 16 * diagonal * (r + (1 if d == 3 else -1)) / r
            )
            assert sp.factor(minor - expected4) == 0
            plane = sp.Matrix(
                (
                    tuple(alpha[mode]) + (entries[mode],),
                    tuple(beta[mode]) + (entries[4 + mode],),
                    tuple(gamma),
                )
            )
            assert plane.rank() == 3
        forbidden = sp.factor(
            permanent((tuple(gammas[0][:4]), tuple(gammas[1][:4]), beta[2], beta[3]))
        )
        assert forbidden == 4
        output.append((d, str(expected), int(forbidden)))
    return output


def main():
    alpha, beta = face_rows()
    pure = {
        word: sp.factor(
            permanent(tuple(alpha[i] if word[i] == 0 else beta[i] for i in range(4)))
        )
        for word in BITS
    }
    assert pure[(1, 1, 1, 1)] == -4
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))
    projections = tuple(projection_audit(d, alpha, beta) for d in range(4))
    branches = punctured_audit(alpha, beta)
    intersections = intersection_audit(alpha, beta)
    replay = subprocess.run(
        [sys.executable, str(PRIMARY)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=420,
        check=False,
    )
    assert replay.returncode == 0, (replay.stdout, replay.stderr)
    primary = json.loads(replay.stdout)
    assert primary["marked_H31_face_empty"] is True
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "no_repository_imports": True,
                "projection_insertions": projections,
                "punctured_branches": branches,
                "intersection_certificates": intersections,
                "primary_replay": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
