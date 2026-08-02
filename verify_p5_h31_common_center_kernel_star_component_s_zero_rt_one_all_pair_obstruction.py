#!/usr/bin/env python3
"""Close marked H31 on component 23's normalized s=0, rt=1 face."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)

ROOT = Path(__file__).resolve().parent
NOTE = (
    ROOT
    / "P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_S_ZERO_RT_ONE_ALL_PAIR_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))

r, k, g = sp.symbols("r k g")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
c, p, q, w = sp.symbols("c p q w")
inverse, localizer = sp.symbols("u v")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def rows():
    return (
        (A, add(A, scale(k, D)), add(B, scale(r, D)), add(B, scale(1 / r, D))),
        (B, B, C, C),
    )


def marked(alpha, beta, shifts=h):
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def pair_matrix(left, right):
    pairs = tuple(itertools.combinations(range(4), 2))
    columns = []
    for a in left:
        for b in right:
            columns.append(sp.Matrix([a[i] * b[j] + a[j] * b[i] for i, j in pairs]))
    return sp.Matrix.hstack(*columns)


def geometry(alpha, beta):
    coefficients = {
        word: sp.factor(
            permanent(tuple(alpha[i] if word[i] == 0 else beta[i] for i in range(4)))
        )
        for word in WORDS
    }
    assert coefficients[(1, 1, 1, 1)] == -4
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )
    planes = tuple((alpha[i], beta[i]) for i in range(4))
    matrices = tuple(pair_matrix(planes[i], planes[j]) for i, j in PAIRS)
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 4, 4, 3)
    assert tuple(matrix.subs(k, 0).rank() for matrix in matrices) == (3, 3, 3, 3, 3, 3)
    assert tuple(matrices[-1].subs(r, value).rank() for value in (1, -1)) == (2, 2)
    return coefficients[(1, 1, 1, 1)]


def singular_command():
    native = shutil.which("Singular")
    return (
        (native, "-q") if native else ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    )


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def projection(distinguished, alpha, beta):
    beta_h = marked(alpha, beta)
    mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, beta_h)
    vector = sp.Matrix(x)
    equations = (
        *tuple(mixed * vector),
        (diagonal0 * vector)[0] - 1,
        inverse * (diagonal1 * vector)[0] - 1,
        localizer * r * (r**2 - 1) - 1,
    )
    cleared = [sp.fraction(sp.together(value))[0] for value in equations]
    eliminated = x + (inverse,)
    variables = eliminated + (r, k, localizer) + h
    lines = [
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(3),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_text(value) for value in cleared) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    if distinguished in (2, 3):
        lines.extend(
            (
                "ideal E=v*r*(r^2-1)-1,h0,h1,h2*h3; E=std(E);",
                "ideal JE=simplify(reduce(J,E),2);",
                "ideal EJ=simplify(reduce(E,J),2);",
                'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J)));',
            )
        )
        expected = "RESULT:1:4"
    else:
        lines.append('print("RESULT:"+string(reduce(1,J)==0)+":"+string(size(J)));')
        expected = "RESULT:1:1"
    lines.append("quit;")
    completed = subprocess.run(
        singular_command(),
        input="\n".join(lines),
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
    assert markers == [expected], (distinguished, completed.stdout)
    return "unit" if distinguished in (0, 1) else "<h0,h1,h2*h3>"


def punctured_cases(alpha, beta):
    cases = (
        (
            2,
            "h2=0",
            (0, 0, 0, g),
            (0, k * q, c, p, q, w, 0, g * c / r),
            2,
            ((0, 1, 2, 7), (0, 1, 3, 7)),
            (
                8 * g * (p * r - c) * (q + w) * (r - 1) * (p * r + (r - 1) * w) / r**3,
                8 * g**2 * (p * r - c) * (q + w) * (r - 1) * (c + (r - 1) * w) / r**3,
            ),
            2 * (r - 1) / r,
            ((0, 1, 6, 10), (0, 1, 2, 6), 16 * g * (r - 1) ** 2 / r**2),
        ),
        (
            2,
            "h3=0",
            (0, 0, g, 0),
            (0, k * q, p, c, q, w, g * r * c, 0),
            3,
            ((0, 1, 2, 7), (0, 1, 3, 7)),
            (
                -8 * g * (p - c * r) * (q + w) * (r - 1) * (p - (r - 1) * w),
                8 * g**2 * (p - c * r) * (q + w) * (r - 1) * (-c * r + (r - 1) * w),
            ),
            -2 * (r - 1),
            ((0, 1, 6, 10), (0, 1, 3, 7), -16 * g * (r - 1) ** 2),
        ),
        (
            3,
            "h2=0",
            (0, 0, 0, g),
            (0, -k * q, c, p, q, w, 0, -g * c / r),
            2,
            ((0, 1, 2, 7), (0, 1, 3, 7)),
            (
                8 * g * (p * r + c) * (q + w) * (r + 1) * (p * r + (r + 1) * w) / r**3,
                8 * g**2 * (p * r + c) * (q + w) * (r + 1) * (-c + (r + 1) * w) / r**3,
            ),
            2 * (r + 1) / r,
            ((0, 1, 6, 10), (0, 1, 2, 6), 16 * g * (r + 1) ** 2 / r**2),
        ),
        (
            3,
            "h3=0",
            (0, 0, g, 0),
            (0, -k * q, p, c, q, w, -g * r * c, 0),
            3,
            ((0, 1, 2, 7), (0, 1, 3, 7)),
            (
                8 * g * (p + c * r) * (q + w) * (r + 1) * (p + (r + 1) * w),
                8 * g**2 * (p + c * r) * (q + w) * (r + 1) * (-c * r + (r + 1) * w),
            ),
            2 * (r + 1),
            ((0, 1, 6, 10), (0, 1, 3, 7), -16 * g * (r + 1) ** 2),
        ),
    )
    output = []
    for (
        d,
        name,
        shifts,
        entries,
        mode,
        rowsets,
        expected,
        transverse,
        rank_minor,
    ) in cases:
        beta_h = marked(alpha, beta, shifts)
        mixed, diagonal0, diagonal1 = mixed_matrix(d, alpha, beta_h)
        extension = sp.Matrix(entries)
        assert all(sp.factor(value) == 0 for value in mixed * extension)
        expected_diagonal0 = {
            (2, "h2=0"): 2 * (r - 1) * (c / r - p),
            (2, "h3=0"): 2 * (r - 1) * (p / r - c),
            (3, "h2=0"): 2 * (r + 1) * (p + c / r),
            (3, "h3=0"): 2 * (r + 1) * (p / r + c),
        }[(d, name)]
        assert sp.factor((diagonal0 * extension)[0] - expected_diagonal0) == 0
        assert sp.factor((diagonal1 * extension)[0] + 2 * (q + w)) == 0
        rows4, cols4, value4 = rank_minor
        assert sp.factor(mixed.extract(rows4, cols4).det() - value4) == 0
        neighbour = marked_extension(d, extension, alpha, beta_h, mode)
        observed = tuple(
            sp.factor(neighbour.extract(rows0, range(4)).det()) for rows0 in rowsets
        )
        assert all(sp.factor(a - b) == 0 for a, b in zip(observed, expected))
        pure = one_marked_map(mode, alpha, beta_h)
        assert sp.factor(pure[0, d] - transverse) == 0
        output.append(
            {
                "insertion": d,
                "branch": name,
                "mixed_rank": 4,
                "minor_rows": ["".join(map(str, rows0)) for rows0 in rowsets],
                "minors": list(map(str, expected)),
                "pure_transverse": str(transverse),
            }
        )
    return output


def stack(distinguished, extension, alpha, beta_h, mode):
    neighbour = marked_extension(distinguished, extension, alpha, beta_h, mode)
    pure = one_marked_map(mode, alpha, beta_h)
    columns = tuple(i for i in range(4) if i != distinguished) + (4,)
    result = sp.zeros(16, 5)
    for row in range(8):
        for source, column in enumerate(columns):
            result[row, column] = neighbour[row, source]
        for column in range(4):
            result[8 + row, column] = pure[row, column]
    return result


def intersection_cases(alpha, beta):
    output = []
    for d, entries, diagonal, determinant_sign, gamma_sign in (
        (2, (0, k * q, c, p, q, w, 0, 0), p * r - c, -1, 1),
        (3, (0, -k * q, c, p, q, w, 0, 0), p * r + c, 1, -1),
    ):
        extension = sp.Matrix(entries)
        matrix0 = stack(d, extension, alpha, beta, 0)
        determinant = sp.factor(matrix0.extract((0, 7, 11, 13, 15), range(5)).det())
        expected = sp.factor(
            determinant_sign * 64 * k * diagonal * (r + (1 if d == 3 else -1)) / r
        )
        assert sp.factor(determinant - expected) == 0
        generators = (
            sp.Matrix((0, 0, gamma_sign, -gamma_sign, w)),
            sp.Matrix((0, 0, gamma_sign, -gamma_sign, q)),
        )
        for mode, gamma in enumerate(generators):
            matrix = stack(d, extension, alpha, beta, mode).subs(k, 0)
            assert all(sp.factor(value) == 0 for value in matrix * gamma)
            rank_minor = sp.factor(matrix.extract((0, 7, 13, 15), (0, 1, 2, 4)).det())
            expected_rank = sp.factor(
                determinant_sign * 16 * diagonal * (r + (1 if d == 3 else -1)) / r
            )
            assert sp.factor(rank_minor - expected_rank) == 0
            local_plane = sp.Matrix(
                (
                    tuple(alpha[mode]) + (entries[mode],),
                    tuple(beta[mode]) + (entries[4 + mode],),
                    tuple(gamma),
                )
            )
            assert local_plane.rank() == 3
        coefficient = sp.factor(
            permanent(
                (tuple(generators[0][:4]), tuple(generators[1][:4]), beta[2], beta[3])
            )
        )
        assert coefficient == 4
        output.append(
            {
                "insertion": d,
                "k_nonzero_stack_minor": str(expected),
                "k_zero_rank": 4,
                "k_zero_forbidden_2211": 4,
            }
        )
    return output


def main():
    alpha, beta = rows()
    pure = geometry(alpha, beta)
    projections = tuple(projection(d, alpha, beta) for d in range(4))
    punctured = punctured_cases(alpha, beta)
    intersections = intersection_cases(alpha, beta)
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "face": "s=0,rt=1",
                "base_ring": "Q[r,k,1/(r*(r-1)*(r+1))]",
                "pure_coefficient": str(pure),
                "generic_pair_profile": (3, 3, 3, 4, 4, 3),
                "k_zero_pair_profile": (3, 3, 3, 3, 3, 3),
                "projections": projections,
                "punctured_branches": punctured,
                "intersection": intersections,
                "complete_marking": True,
                "projective_extension_complete": True,
                "marked_H31_face_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
