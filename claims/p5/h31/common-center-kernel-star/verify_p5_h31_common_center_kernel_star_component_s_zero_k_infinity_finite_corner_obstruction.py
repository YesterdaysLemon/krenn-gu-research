#!/usr/bin/env python3
"""Close marked H31 on component 23's finite s=0,k=infinity corner."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_S_ZERO_"
    "K_INFINITY_FINITE_CORNER_OBSTRUCTION.md"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))

r, t, v = sp.symbols("r t v")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
inverse = sp.Symbol("u")
p, w, g, q = sp.symbols("p w g q")

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


def corner_rows(r_value=r, t_value=t):
    return (
        (A, D, add(B, scale(r_value, D)), add(B, scale(t_value, D))),
        (B, B, C, C),
    )


def shifted(alpha, beta, shifts=h):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(symmetric_product(left[i], right[j]) for i in range(2) for j in range(2))
    )


def pair_certificate(alpha, beta):
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    matrices = tuple(pair_matrix(planes[i], planes[j]) for i, j in PAIRS)
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 3, 3, 4)
    maximal = tuple(
        sp.factor(matrices[-1].extract(rows, range(4)).det())
        for rows in itertools.combinations(range(6), 4)
        if matrices[-1].extract(rows, range(4)).det() != 0
    )
    gcd = sp.factor(sp.gcd_list(maximal))
    assert sp.factor(gcd - 8 * (r - t) * (r * t - 1)) == 0
    profiles = {}
    for name, substitutions, expected in (
        ("r=t", {t: r}, (3, 3, 3, 3, 3, 3)),
        ("rt=1", {t: 1 / r}, (3, 3, 3, 3, 3, 3)),
        ("plus", {r: 1, t: 1}, (3, 3, 3, 3, 3, 2)),
        ("minus", {r: -1, t: -1}, (3, 3, 3, 3, 3, 2)),
    ):
        observed = tuple(matrix.subs(substitutions).rank() for matrix in matrices)
        assert observed == expected
        profiles[name] = observed
    return str(gcd), profiles


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def run_singular(label, program, expected="RESULT:1"):
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=360,
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
    assert markers == [expected], (label, completed.stdout, expected)
    return label


def projection_system(distinguished, alpha, beta, parameters, localizer=None):
    marked = shifted(alpha, beta)
    mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
    vector = sp.Matrix(x)
    equations = [
        *tuple(mixed * vector),
        (diagonal0 * vector)[0] - 1,
        inverse * (diagonal1 * vector)[0] - 1,
    ]
    if localizer is not None:
        equations.append(localizer)
    eliminated = x + (inverse,)
    variables = eliminated + tuple(parameters) + h
    header = [
        "ring R=0,("
        + ",".join(map(str, variables))
        + f"),(dp(9),dp({len(parameters) + 4}));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_text(value) for value in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    return header


def compare_projection(
    label, distinguished, alpha, beta, parameters, localizer, ideals
):
    lines = projection_system(
        distinguished, alpha, beta, parameters, localizer=localizer
    )
    names = []
    for name, generators in ideals:
        names.append(name)
        lines.append(f"ideal {name}=" + ",".join(generators) + f"; {name}=std({name});")
    lines.extend(
        (
            "ideal E=std(intersect(" + ",".join(names) + "));",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0)));',
            "quit;",
        )
    )
    return run_singular(label, "\n".join(lines))


def unit_projection(label, distinguished, alpha, beta, parameters=(), localizer=None):
    lines = projection_system(
        distinguished, alpha, beta, parameters, localizer=localizer
    )
    lines.extend(('print("RESULT:"+string(reduce(1,J)==0));', "quit;"))
    return run_singular(label, "\n".join(lines))


def projection_certificates(alpha, beta):
    output = []
    for distinguished in (2, 3):
        output.append(
            unit_projection(
                f"universal insertion {distinguished}",
                distinguished,
                alpha,
                beta,
                parameters=(r, t),
            )
        )

    open_localizer = "v*(r-t)*(r+t)-1"
    open_ideals = (
        ("C0", (open_localizer, "h0", "h2", "h3", "(r+t)*h1-r*t-1")),
        ("B20", (open_localizer, "r", "h0", "h3", "t*h1-1")),
        ("B2p", (open_localizer, "t-1", "h0", "h3", "h1-1")),
        ("B2m", (open_localizer, "t+1", "h0", "h3", "h1+1")),
        ("B30", (open_localizer, "t", "h0", "h2", "r*h1-1")),
        ("B3p", (open_localizer, "r-1", "h0", "h2", "h1-1")),
        ("B3m", (open_localizer, "r+1", "h0", "h2", "h1+1")),
    )
    for distinguished in (0, 1):
        output.append(
            compare_projection(
                f"seven-branch open insertion {distinguished}",
                distinguished,
                alpha,
                beta,
                (r, t, v),
                v * (r - t) * (r + t) - 1,
                open_ideals,
            )
        )

    anti_alpha, anti_beta = corner_rows(r, -r)
    for distinguished in (0, 1):
        output.append(
            unit_projection(
                f"antidiagonal insertion {distinguished}",
                distinguished,
                anti_alpha,
                anti_beta,
                parameters=(r, v),
                localizer=v * r - 1,
            )
        )

    diagonal_alpha, diagonal_beta = corner_rows(r, r)
    diagonal_localizer = "v*r*(r-1)*(r+1)-1"
    diagonal_ideals = (
        ("Cdiag", (diagonal_localizer, "h0", "h2", "h3")),
        ("B2diag", (diagonal_localizer, "h0", "h3", "r*h1-1")),
        ("B3diag", (diagonal_localizer, "h0", "h2", "r*h1-1")),
    )
    for distinguished in (0, 1):
        output.append(
            compare_projection(
                f"diagonal insertion {distinguished}",
                distinguished,
                diagonal_alpha,
                diagonal_beta,
                (r, v),
                v * r * (r - 1) * (r + 1) - 1,
                diagonal_ideals,
            )
        )

    zero_alpha, zero_beta = corner_rows(0, 0)
    for distinguished in (0, 1):
        output.append(
            unit_projection(
                f"central point insertion {distinguished}",
                distinguished,
                zero_alpha,
                zero_beta,
            )
        )

    for sign, label in ((1, "plus"), (-1, "minus")):
        endpoint_alpha, endpoint_beta = corner_rows(sign, sign)
        endpoint_ideals = (
            ("E2", ("h0", f"h1-({sign})", "h3")),
            ("E3", ("h0", f"h1-({sign})", "h2")),
        )
        for distinguished in (0, 1):
            output.append(
                compare_projection(
                    f"{label} endpoint insertion {distinguished}",
                    distinguished,
                    endpoint_alpha,
                    endpoint_beta,
                    (),
                    None,
                    endpoint_ideals,
                )
            )
    return output


def check_frame(mixed, frame, rank_rows, rank_columns, expected_rank_minor):
    assert sp.Matrix.hstack(*frame).rank() == len(frame)
    assert all(
        all(sp.factor(entry) == 0 for entry in mixed * vector) for vector in frame
    )
    observed = sp.factor(mixed.extract(rank_rows, rank_columns).det())
    assert sp.factor(observed - expected_rank_minor) == 0
    return observed


def central_open_cases():
    alpha, beta = corner_rows()
    marking = (0, (r * t + 1) / (r + t), 0, 0)
    marked = shifted(alpha, beta, marking)
    results = []
    rank_rows = (
        (1, 3, 4, 8, 9, 12),
        (0, 3, 5, 8, 9, 13),
    )
    rank_columns = (0, 1, 2, 3, 4, 6)
    expected_rank_minors = (
        64 * t**3 * (r - 1) ** 2 * (r + 1) ** 2 * (r - t) / (r + t) ** 2,
        64 * r**3 * (r - t) * (t - 1) ** 2 * (t + 1) ** 2 / (r + t) ** 2,
    )
    rank_cover_program = """ring R=0,(r,t,v),dp;
ideal I=v*(r-t)*(r+t)-1,t^3*(r-1)^2*(r+1)^2,r^3*(t-1)^2*(t+1)^2;
I=std(I);
print("RESULT:"+string(reduce(1,I)==0));
quit;"""
    run_singular("central rank cover", rank_cover_program)
    for distinguished in (0, 1):
        mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
        frame = (
            sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0)),
            sp.Matrix(((1 if distinguished == 0 else -1), 0, 0, 0, 0, 0, 1, 1)),
        )
        assert all(
            all(sp.factor(entry) == 0 for entry in mixed * vector) for vector in frame
        )
        minors = tuple(
            sp.factor(mixed.extract(rows, rank_columns).det()) for rows in rank_rows
        )
        assert all(
            sp.factor(left - right) == 0
            for left, right in zip(minors, expected_rank_minors)
        )
        extension = frame[0] * p + frame[1] * w
        diagonals = (
            sp.factor((diagonal0 * extension)[0]),
            sp.factor((diagonal1 * extension)[0]),
        )
        expected_diagonals = (2 * p * (r + t), (-4 if distinguished == 0 else 4) * w)
        assert all(
            sp.factor(left - right) == 0
            for left, right in zip(diagonals, expected_diagonals)
        )
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, marked, 0)
            .extract((0, 1, 2, 7), range(4))
            .det()
        )
        expected = (1 if distinguished == 0 else -1) * 16 * p**2 * w * (r - t) * (r + t)
        assert sp.factor(determinant - expected) == 0
        pure = one_marked_map(0, alpha, marked)
        assert (
            sp.factor(
                pure[1, distinguished] - (1 if distinguished == 0 else -1) * 2 * r
            )
            == 0
        )
        assert (
            sp.factor(
                pure[2, distinguished] - (1 if distinguished == 0 else -1) * 2 * t
            )
            == 0
        )
        results.append(
            {"branch": "C", "insertion": distinguished, "minor": str(determinant)}
        )
    return results


def two_vector_branch(
    name,
    r_value,
    t_value,
    marking,
    frame0,
    frame1,
    rank_data,
    determinant_data,
    pure_entry,
):
    alpha, beta = corner_rows(r_value, t_value)
    marked = shifted(alpha, beta, marking)
    output = []
    for distinguished in (0, 1):
        mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
        adjusted0 = sp.Matrix(frame0(distinguished) if callable(frame0) else frame0)
        adjusted1 = sp.Matrix(frame1(distinguished))
        frame = (adjusted0, adjusted1)
        rank_rows, rank_columns, rank_minor = rank_data(distinguished)
        check_frame(mixed, frame, rank_rows, rank_columns, rank_minor)
        extension = frame[0] * p + frame[1] * w
        diagonals = (
            sp.factor((diagonal0 * extension)[0]),
            sp.factor((diagonal1 * extension)[0]),
        )
        rows, expected_diagonals, expected_determinant = determinant_data(distinguished)
        assert all(
            sp.factor(left - right) == 0
            for left, right in zip(diagonals, expected_diagonals)
        )
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, marked, 0)
            .extract(rows, range(4))
            .det()
        )
        assert sp.factor(determinant - expected_determinant) == 0
        pure = sp.factor(one_marked_map(0, alpha, marked)[pure_entry[0], distinguished])
        assert sp.factor(pure - pure_entry[1](distinguished)) == 0
        output.append(
            {
                "branch": name,
                "insertion": distinguished,
                "rank_minor": str(rank_minor),
                "diagonals": list(map(str, diagonals)),
                "one_marked_minor": str(determinant),
                "pure_transverse": str(pure),
            }
        )
    return output


def coordinate_cases():
    results = []
    common0 = (0, 0, -1, -1, 0, 1, 0, 0)
    results.extend(
        two_vector_branch(
            "B20",
            0,
            t,
            (0, 1 / t, g, 0),
            common0,
            lambda d: ((1 if d == 0 else -1), 0, 0, 0, 0, 0, 1, 1),
            lambda d: ((1, 3, 4, 8, 9, 12), (0, 1, 2, 3, 4, 6), -64 * t**2),
            lambda d: (
                (0, 1, 2, 7),
                (2 * p * t, (-2 if d == 0 else 2) * (g * p + 2 * w)),
                (-8 if d == 0 else 8) * p**2 * t**2 * (g * p + 2 * w),
            ),
            (2, lambda d: (2 if d == 0 else -2) * t),
        )
    )
    results.extend(
        two_vector_branch(
            "B30",
            r,
            0,
            (0, 1 / r, 0, g),
            common0,
            lambda d: ((1 if d == 0 else -1), 0, 0, 0, 0, 0, 1, 1),
            lambda d: ((0, 3, 5, 8, 9, 13), (0, 1, 2, 3, 4, 6), 64 * r**2),
            lambda d: (
                (0, 1, 2, 7),
                (2 * p * r, (-2 if d == 0 else 2) * (g * p + 2 * w)),
                (8 if d == 0 else -8) * p**2 * r**2 * (g * p + 2 * w),
            ),
            (1, lambda d: (2 if d == 0 else -2) * r),
        )
    )
    return results


def sign_side_case(
    name,
    r_value,
    t_value,
    marking,
    frame0,
    frame1,
    rank_rows,
    rank_minor,
    diagonals,
    determinant,
    pure,
):
    return two_vector_branch(
        name,
        r_value,
        t_value,
        marking,
        frame0,
        frame1,
        lambda d: (rank_rows, (0, 1, 2, 3, 4, 5), rank_minor),
        lambda d: ((0, 1, 2, 7), diagonals(d), determinant(d)),
        pure,
    )


def sign_side_cases():
    results = []
    # The variable r is free on B2+ and B2-; g is nonzero (g=0 belongs to C).
    results.extend(
        sign_side_case(
            "B2+",
            r,
            1,
            (0, 1, g, 0),
            (0, 0, -1 / (g * r), -1 / (g * r), 0, 1 / (g * r), 1, 0),
            lambda d: (
                (1 if d == 0 else -1),
                0,
                1 / (g * r),
                1 / (g * r),
                0,
                -1 / (g * r),
                0,
                1,
            ),
            (0, 1, 3, 8, 9, 12),
            -64 * g * r**2 * (r - 1) ** 2,
            lambda d: (
                2 * (p - w) * (r + 1) / (g * r),
                (-2 if d == 0 else 2) * (p * r + p + r * w - w) / r,
            ),
            lambda d: (
                (8 if d == 0 else -8)
                * (p - w) ** 2
                * (r - 1)
                * (r + 1)
                * (p * r + p + r * w - w)
                / (g**2 * r**3)
            ),
            (2, lambda d: 2 if d == 0 else -2),
        )
    )
    results.extend(
        sign_side_case(
            "B2-",
            r,
            -1,
            (0, -1, g, 0),
            (0, 0, 1 / (g * r), 1 / (g * r), 0, -1 / (g * r), 1, 0),
            lambda d: (
                (1 if d == 0 else -1),
                0,
                -1 / (g * r),
                -1 / (g * r),
                0,
                1 / (g * r),
                0,
                1,
            ),
            (0, 1, 3, 8, 9, 12),
            64 * g * r**2 * (r + 1) ** 2,
            lambda d: (
                -2 * (p - w) * (r - 1) / (g * r),
                (-2 if d == 0 else 2) * (p * r - p + r * w + w) / r,
            ),
            lambda d: (
                (8 if d == 0 else -8)
                * (p - w) ** 2
                * (r - 1)
                * (r + 1)
                * (p * r - p + r * w + w)
                / (g**2 * r**3)
            ),
            (2, lambda d: -2 if d == 0 else 2),
        )
    )
    # The variable t is free on B3+ and B3-.
    results.extend(
        sign_side_case(
            "B3+",
            1,
            t,
            (0, 1, 0, g),
            lambda d: (
                (1 if d == 0 else -1),
                0,
                1 / (g * t),
                1 / (g * t),
                0,
                -1 / (g * t),
                1,
                0,
            ),
            lambda d: (0, 0, -1 / (g * t), -1 / (g * t), 0, 1 / (g * t), 0, 1),
            (0, 1, 3, 8, 9, 13),
            64 * g * t**2 * (t - 1) ** 2,
            lambda d: (
                -2 * (p - w) * (t + 1) / (g * t),
                (-2 if d == 0 else 2) * (p * t - p + t * w + w) / t,
            ),
            lambda d: (
                (-8 if d == 0 else 8)
                * (p - w) ** 2
                * (t - 1)
                * (t + 1)
                * (p * t - p + t * w + w)
                / (g**2 * t**3)
            ),
            (1, lambda d: 2 if d == 0 else -2),
        )
    )
    results.extend(
        sign_side_case(
            "B3-",
            -1,
            t,
            (0, -1, 0, g),
            lambda d: (
                (1 if d == 0 else -1),
                0,
                -1 / (g * t),
                -1 / (g * t),
                0,
                1 / (g * t),
                1,
                0,
            ),
            lambda d: (0, 0, 1 / (g * t), 1 / (g * t), 0, -1 / (g * t), 0, 1),
            (0, 1, 3, 8, 9, 13),
            -64 * g * t**2 * (t + 1) ** 2,
            lambda d: (
                2 * (p - w) * (t - 1) / (g * t),
                (-2 if d == 0 else 2) * (p * t + p + t * w - w) / t,
            ),
            lambda d: (
                (-8 if d == 0 else 8)
                * (p - w) ** 2
                * (t - 1)
                * (t + 1)
                * (p * t + p + t * w - w)
                / (g**2 * t**3)
            ),
            (1, lambda d: -2 if d == 0 else 2),
        )
    )
    return results


def diagonal_cases():
    alpha, beta = corner_rows(r, r)
    results = []
    for distinguished in (0, 1):
        sign = 1 if distinguished == 0 else -1
        marked = shifted(alpha, beta, (0, q, 0, 0))
        mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
        frame = (
            sp.Matrix(
                (
                    0,
                    r * (2 * q * r - r**2 - 1) / (2 * (q * r - 1) ** 2),
                    -(r - 1) * (r + 1) / (2 * (q * r - 1)),
                    -(r - 1) * (r + 1) / (2 * (q * r - 1)),
                    (2 * q * r - r**2 - 1) / (2 * (q * r - 1) ** 2),
                    1,
                    0,
                    0,
                )
            ),
            sp.Matrix((sign, 0, 0, 0, 0, 0, 1, 1)),
        )
        check_frame(
            mixed,
            frame,
            (0, 1, 3, 8, 12, 13),
            (0, 1, 2, 3, 4, 6),
            128 * r**2 * (q * r - 1) ** 2,
        )
        extension = frame[0] * p + frame[1] * w
        diagonals = (
            sp.factor((diagonal0 * extension)[0]),
            sp.factor((diagonal1 * extension)[0]),
        )
        expected_diagonals = (
            p * r * (r - 1) ** 2 * (r + 1) ** 2 / (q * r - 1) ** 2,
            (-4 if distinguished == 0 else 4) * w,
        )
        assert all(sp.factor(a - b) == 0 for a, b in zip(diagonals, expected_diagonals))
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, marked, 0)
            .extract((0, 1, 3, 7), range(4))
            .det()
        )
        expected = (
            (-16 if distinguished == 0 else 16)
            * p
            * r**2
            * w**2
            * (r - 1) ** 2
            * (r + 1) ** 2
            / (q * r - 1) ** 2
        )
        assert sp.factor(determinant - expected) == 0
        assert (
            sp.factor(one_marked_map(0, alpha, marked)[1, distinguished] - sign * 2 * r)
            == 0
        )
        results.append(
            {
                "branch": "Cdiag_qr_ne_1",
                "insertion": distinguished,
                "minor": str(determinant),
            }
        )

        marked_equal = shifted(alpha, beta, (0, 1 / r, 0, 0))
        mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked_equal)
        frame = (
            sp.Matrix((0, r, 0, 0, 1, 0, 0, 0)),
            sp.Matrix((sign, 0, 0, 0, 0, 0, 1, 1)),
        )
        check_frame(
            mixed,
            frame,
            (0, 1, 3, 8, 12, 13),
            (0, 1, 2, 3, 5, 6),
            64 * r**2 * (r - 1) * (r + 1),
        )
        extension = frame[0] * p + frame[1] * w
        diagonals = (
            sp.factor((diagonal0 * extension)[0]),
            sp.factor((diagonal1 * extension)[0]),
        )
        assert sp.factor(diagonals[0] + 2 * p * r * (r - 1) * (r + 1)) == 0
        assert sp.factor(diagonals[1] - (-4 if distinguished == 0 else 4) * w) == 0
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, marked_equal, 0)
            .extract((0, 1, 3, 7), range(4))
            .det()
        )
        expected = (
            (32 if distinguished == 0 else -32) * p * w**2 * r**2 * (r - 1) * (r + 1)
        )
        assert sp.factor(determinant - expected) == 0
        results.append(
            {
                "branch": "Cdiag_qr_eq_1",
                "insertion": distinguished,
                "minor": str(determinant),
            }
        )

    for side in (2, 3):
        marking = (0, 1 / r, g, 0) if side == 2 else (0, 1 / r, 0, g)
        marked = shifted(alpha, beta, marking)
        for distinguished in (0, 1):
            sign = 1 if distinguished == 0 else -1
            mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
            if side == 2:
                frame0 = (
                    0,
                    -r / (g * (r - 1) * (r + 1)),
                    0,
                    0,
                    -1 / (g * (r - 1) * (r + 1)),
                    0,
                    1,
                    0,
                )
                frame1 = (
                    sign,
                    r / (g * (r - 1) * (r + 1)),
                    0,
                    0,
                    1 / (g * (r - 1) * (r + 1)),
                    0,
                    0,
                    1,
                )
                expected_a = 2 * r * (p - w) / g
                expected_det = (
                    (-8 if distinguished == 0 else 8)
                    * r**2
                    * (p - w)
                    * (p + w) ** 2
                    / g
                )
                rank_minor = -64 * g * r**2 * (r - 1) ** 2 * (r + 1) ** 2
            else:
                frame0 = (
                    sign,
                    r / (g * (r - 1) * (r + 1)),
                    0,
                    0,
                    1 / (g * (r - 1) * (r + 1)),
                    0,
                    1,
                    0,
                )
                frame1 = (
                    0,
                    -r / (g * (r - 1) * (r + 1)),
                    0,
                    0,
                    -1 / (g * (r - 1) * (r + 1)),
                    0,
                    0,
                    1,
                )
                expected_a = -2 * r * (p - w) / g
                expected_det = (
                    (8 if distinguished == 0 else -8)
                    * r**2
                    * (p - w)
                    * (p + w) ** 2
                    / g
                )
                rank_minor = 64 * g * r**2 * (r - 1) ** 2 * (r + 1) ** 2
            frame = (sp.Matrix(frame0), sp.Matrix(frame1))
            check_frame(
                mixed, frame, (0, 1, 3, 8, 12, 13), (0, 1, 2, 3, 4, 5), rank_minor
            )
            extension = frame[0] * p + frame[1] * w
            diagonals = (
                sp.factor((diagonal0 * extension)[0]),
                sp.factor((diagonal1 * extension)[0]),
            )
            assert sp.factor(diagonals[0] - expected_a) == 0
            assert (
                sp.factor(diagonals[1] - (-2 if distinguished == 0 else 2) * (p + w))
                == 0
            )
            determinant = sp.factor(
                marked_extension(distinguished, extension, alpha, marked, 0)
                .extract((0, 1, 3, 7), range(4))
                .det()
            )
            assert sp.factor(determinant - expected_det) == 0
            assert (
                sp.factor(
                    one_marked_map(0, alpha, marked)[1, distinguished] - sign * 2 * r
                )
                == 0
            )
            results.append(
                {
                    "branch": f"B{side}diag",
                    "insertion": distinguished,
                    "minor": str(determinant),
                }
            )
    return results


def endpoint_cases():
    results = []
    coefficients = sp.symbols("c0:3")
    for endpoint in (1, -1):
        alpha, beta = corner_rows(endpoint, endpoint)
        for side in (0, 2, 3):
            marking = (
                (0, endpoint, 0, 0)
                if side == 0
                else ((0, endpoint, g, 0) if side == 2 else (0, endpoint, 0, g))
            )
            marked = shifted(alpha, beta, marking)
            for distinguished in (0, 1):
                sign = 1 if distinguished == 0 else -1
                if side == 0:
                    frame = (
                        sp.Matrix((0, endpoint, 0, 0, 1, 0, 0, 0)),
                        sp.Matrix((0, 0, -1, -1, 0, 1, 0, 0)),
                        sp.Matrix((sign, 0, 0, 0, 0, 0, 1, 1)),
                    )
                    rank_columns = (0, 1, 2, 3, 6)
                    rank_minor = -32
                elif side == 2:
                    frame = (
                        sp.Matrix((0, endpoint, 0, 0, 1, 0, 0, 0)),
                        sp.Matrix((0, 0, -1 / g, -1 / g, 0, 1 / g, 1, 0)),
                        sp.Matrix((sign, 0, 1 / g, 1 / g, 0, -1 / g, 0, 1)),
                    )
                    rank_columns = (0, 1, 2, 3, 5)
                    rank_minor = 32 * g
                else:
                    frame = (
                        sp.Matrix((0, endpoint, 0, 0, 1, 0, 0, 0)),
                        sp.Matrix((sign, 0, 1 / g, 1 / g, 0, -1 / g, 1, 0)),
                        sp.Matrix((0, 0, -1 / g, -1 / g, 0, 1 / g, 0, 1)),
                    )
                    rank_columns = (0, 1, 2, 3, 5)
                    rank_minor = -32 * g
                mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
                check_frame(mixed, frame, (0, 1, 8, 12, 13), rank_columns, rank_minor)
                extension = sum(
                    (frame[i] * coefficients[i] for i in range(3)), sp.zeros(8, 1)
                )
                diagonals = (
                    sp.factor((diagonal0 * extension)[0]),
                    sp.factor((diagonal1 * extension)[0]),
                )
                if side == 0:
                    expected_a = 4 * endpoint * coefficients[1]
                    expected_b = (-4 if distinguished == 0 else 4) * coefficients[2]
                    expected_det = (
                        (-64 if distinguished == 0 else 64)
                        * coefficients[1]
                        * coefficients[2] ** 2
                    )
                elif side == 2:
                    expected_a = 4 * endpoint * (coefficients[1] - coefficients[2]) / g
                    expected_b = (-4 if distinguished == 0 else 4) * coefficients[1]
                    expected_det = (
                        (-64 if distinguished == 0 else 64)
                        * coefficients[1] ** 2
                        * (coefficients[1] - coefficients[2])
                        / g
                    )
                else:
                    expected_a = -4 * endpoint * (coefficients[1] - coefficients[2]) / g
                    expected_b = (-4 if distinguished == 0 else 4) * coefficients[2]
                    expected_det = (
                        (64 if distinguished == 0 else -64)
                        * coefficients[2] ** 2
                        * (coefficients[1] - coefficients[2])
                        / g
                    )
                assert sp.factor(diagonals[0] - expected_a) == 0
                assert sp.factor(diagonals[1] - expected_b) == 0
                determinant = sp.factor(
                    marked_extension(distinguished, extension, alpha, marked, 0)
                    .extract((0, 1, 3, 7), range(4))
                    .det()
                )
                assert sp.factor(determinant - expected_det) == 0
                pure = sp.factor(one_marked_map(0, alpha, marked)[1, distinguished])
                assert sp.factor(pure - sign * 2 * endpoint) == 0
                results.append(
                    {
                        "endpoint": endpoint,
                        "side": side,
                        "insertion": distinguished,
                        "minor": str(determinant),
                    }
                )
    return results


def main():
    alpha, beta = corner_rows()
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
    assert all(sp.Matrix((alpha[index], beta[index])).rank() == 2 for index in range(4))
    pair_gcd, profiles = pair_certificate(alpha, beta)
    projections = projection_certificates(alpha, beta)
    branches = [
        *central_open_cases(),
        *coordinate_cases(),
        *sign_side_cases(),
        *diagonal_cases(),
        *endpoint_cases(),
    ]
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "corner": "s=0,k=infinity,finite (r,t)",
                "base": "A^2_Q",
                "pair_profile": (3, 3, 3, 3, 3, 4),
                "edge23_maximal_minor_gcd": pair_gcd,
                "special_pair_profiles": profiles,
                "projection_checks": projections,
                "branch_checks": branches,
                "all_marked_bases_covered": True,
                "all_four_insertions_covered": True,
                "projective_extensions_covered": True,
                "r_or_t_infinity_covered": False,
                "normalized_finite_corner_marked_H31_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
