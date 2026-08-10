#!/usr/bin/env python3
"""Independent no-import audit of the finite component-23 corner H31 theorem."""

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


ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_S_ZERO_"
    "K_INFINITY_FINITE_CORNER_OBSTRUCTION.md"
)
PRIMARY = ROOT / (
    "verify_p5_h31_common_center_kernel_star_component_s_zero_"
    "k_infinity_finite_corner_obstruction.py"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(word for word in WORDS if word not in (WORDS[0], WORDS[-1]))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

r, t, v = sp.symbols("r t v")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
inverse = sp.Symbol("u")
c0, c1, c2 = sp.symbols("c0 c1 c2")
g, q = sp.symbols("g q")

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
            for permutation in PERMUTATIONS
        )
    )


def corner_rows(r_value=r, t_value=t):
    return (
        (A, D, add(B, scale(r_value, D)), add(B, scale(t_value, D))),
        (B, B, C, C),
    )


def shifted(alpha, beta, shifts):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def projected_rows(distinguished, extension, alpha, beta):
    common = tuple(index for index in range(4) if index != distinguished)
    return (
        tuple(
            tuple(alpha[mode][coordinate] for coordinate in common) + (extension[mode],)
            for mode in range(4)
        ),
        tuple(
            tuple(beta[mode][coordinate] for coordinate in common)
            + (extension[4 + mode],)
            for mode in range(4)
        ),
    )


def extension_coefficients(distinguished, extension, alpha, beta):
    projected_alpha, projected_beta = projected_rows(
        distinguished, extension, alpha, beta
    )
    return {
        word: permanent(
            tuple(
                projected_beta[index] if word[index] else projected_alpha[index]
                for index in range(4)
            )
        )
        for word in WORDS
    }


def mixed_system(distinguished, alpha, beta):
    coefficients = extension_coefficients(distinguished, sp.Matrix(x), alpha, beta)
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in x]
            for word in MIXED_WORDS
        ]
    )
    diagonals = tuple(
        sp.Matrix([[sp.diff(coefficients[word], variable) for variable in x]])
        for word in (WORDS[0], WORDS[-1])
    )
    return mixed, *diagonals


def one_marked_map(mode, alpha, beta):
    rows = []
    for bits in BITS3:
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        rows.append(
            [
                permanent(
                    tuple(
                        tuple(int(index == coordinate) for index in range(4))
                        if other == mode
                        else selected[other]
                        for other in range(4)
                    )
                )
                for coordinate in range(4)
            ]
        )
    return sp.Matrix(rows)


def marked_extension(distinguished, extension, alpha, beta, mode=0):
    return one_marked_map(mode, *projected_rows(distinguished, extension, alpha, beta))


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(symmetric_product(left[i], right[j]) for i in range(2) for j in range(2))
    )


def pair_audit(alpha, beta):
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
    assert tuple(matrix.subs(t, r).rank() for matrix in matrices) == (3,) * 6
    assert tuple(matrix.subs(t, 1 / r).rank() for matrix in matrices) == (3,) * 6
    for endpoint in (1, -1):
        assert tuple(
            matrix.subs({r: endpoint, t: endpoint}).rank() for matrix in matrices
        ) == (3, 3, 3, 3, 3, 2)
    return str(gcd)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def run_singular(label, program):
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
    assert markers == ["RESULT:1"], (label, completed.stdout)
    return label


def projection_header(distinguished, alpha, beta, parameters, localizer=None):
    marked = shifted(alpha, beta, h)
    mixed, diagonal0, diagonal1 = mixed_system(distinguished, alpha, marked)
    vector = sp.Matrix(x)
    # Reverse the primary normalization: b_d z=1 and a_d z is inverted.
    equations = [
        *tuple(mixed * vector),
        (diagonal1 * vector)[0] - 1,
        inverse * (diagonal0 * vector)[0] - 1,
    ]
    if localizer is not None:
        equations.append(localizer)
    eliminated = x + (inverse,)
    variables = eliminated + tuple(parameters) + h
    return [
        "ring R=0,("
        + ",".join(map(str, variables))
        + f"),(dp(9),dp({len(parameters) + 4}));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_text(value) for value in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]


def compare_projection(
    label, distinguished, alpha, beta, parameters, localizer, ideals
):
    lines = projection_header(distinguished, alpha, beta, parameters, localizer)
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
    lines = projection_header(distinguished, alpha, beta, parameters, localizer)
    lines.extend(('print("RESULT:"+string(reduce(1,J)==0));', "quit;"))
    return run_singular(label, "\n".join(lines))


def projection_audit(alpha, beta):
    output = []
    for distinguished in (2, 3):
        output.append(
            unit_projection(
                f"reverse universal {distinguished}",
                distinguished,
                alpha,
                beta,
                (r, t),
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
                f"reverse seven-branch {distinguished}",
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
                f"reverse antidiagonal {distinguished}",
                distinguished,
                anti_alpha,
                anti_beta,
                (r, v),
                v * r - 1,
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
                f"reverse diagonal {distinguished}",
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
                f"reverse center {distinguished}",
                distinguished,
                zero_alpha,
                zero_beta,
            )
        )
    for endpoint in (1, -1):
        endpoint_alpha, endpoint_beta = corner_rows(endpoint, endpoint)
        endpoint_ideals = (
            ("E2", ("h0", f"h1-({endpoint})", "h3")),
            ("E3", ("h0", f"h1-({endpoint})", "h2")),
        )
        for distinguished in (0, 1):
            output.append(
                compare_projection(
                    f"reverse endpoint {endpoint} insertion {distinguished}",
                    distinguished,
                    endpoint_alpha,
                    endpoint_beta,
                    (),
                    None,
                    endpoint_ideals,
                )
            )
    return output


def rank_minor(matrix, rows, columns, expected):
    observed = sp.factor(matrix.extract(rows, columns).det())
    assert sp.factor(observed - expected) == 0
    return observed


def rank_two_audit(
    name,
    r_value,
    t_value,
    marking,
    rank_certificates,
    one_marked_rows,
    powers,
    quotient,
    pure_row,
    pure_expected,
):
    alpha, beta = corner_rows(r_value, t_value)
    marked = shifted(alpha, beta, marking)
    output = []
    for distinguished in (0, 1):
        mixed, diagonal0, diagonal1 = mixed_system(distinguished, alpha, marked)
        kernel = tuple(mixed.nullspace())
        assert len(kernel) == 2 and sp.Matrix.hstack(*kernel).rank() == 2
        minors = tuple(
            rank_minor(mixed, rows, columns, expected)
            for rows, columns, expected in rank_certificates
        )
        extension = kernel[0] * c0 + kernel[1] * c1
        diagonals = (
            sp.factor((diagonal0 * extension)[0]),
            sp.factor((diagonal1 * extension)[0]),
        )
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, marked)
            .extract(one_marked_rows, range(4))
            .det()
        )
        ratio = sp.factor(
            determinant / (diagonals[0] ** powers[0] * diagonals[1] ** powers[1])
        )
        assert sp.factor(ratio - quotient(distinguished)) == 0
        pure = sp.factor(one_marked_map(0, alpha, marked)[pure_row, distinguished])
        assert sp.factor(pure - pure_expected(distinguished)) == 0
        output.append(
            {
                "branch": name,
                "insertion": distinguished,
                "rank_minors": list(map(str, minors)),
                "diagonal_ratio": str(ratio),
                "pure_transverse": str(pure),
            }
        )
    return output


def branch_audit():
    output = []
    central_rank = (
        (
            (1, 3, 4, 8, 9, 12),
            (0, 1, 2, 3, 4, 6),
            64 * t**3 * (r - 1) ** 2 * (r + 1) ** 2 * (r - t) / (r + t) ** 2,
        ),
        (
            (0, 3, 5, 8, 9, 13),
            (0, 1, 2, 3, 4, 6),
            64 * r**3 * (r - t) * (t - 1) ** 2 * (t + 1) ** 2 / (r + t) ** 2,
        ),
    )
    output.extend(
        rank_two_audit(
            "C",
            r,
            t,
            (0, (r * t + 1) / (r + t), 0, 0),
            central_rank,
            (0, 1, 2, 7),
            (2, 1),
            lambda d: -(r - t) / (r + t),
            1,
            lambda d: (2 if d == 0 else -2) * r,
        )
    )
    rank_cover = """ring R=0,(r,t,v),dp;
ideal I=v*(r-t)*(r+t)-1,t^3*(r-1)^2*(r+1)^2,r^3*(t-1)^2*(t+1)^2;
I=std(I);
print("RESULT:"+string(reduce(1,I)==0));
quit;"""
    run_singular("audit central rank cover", rank_cover)
    output.extend(
        rank_two_audit(
            "B20",
            0,
            t,
            (0, 1 / t, g, 0),
            (((1, 3, 4, 8, 9, 12), (0, 1, 2, 3, 4, 6), -64 * t**2),),
            (0, 1, 2, 7),
            (2, 1),
            lambda d: 1,
            2,
            lambda d: (2 if d == 0 else -2) * t,
        )
    )
    output.extend(
        rank_two_audit(
            "B30",
            r,
            0,
            (0, 1 / r, 0, g),
            (((0, 3, 5, 8, 9, 13), (0, 1, 2, 3, 4, 6), 64 * r**2),),
            (0, 1, 2, 7),
            (2, 1),
            lambda d: -1,
            1,
            lambda d: (2 if d == 0 else -2) * r,
        )
    )
    sign_cases = (
        (
            "B2+",
            r,
            1,
            (0, 1, g, 0),
            (0, 1, 3, 8, 9, 12),
            -64 * g * r**2 * (r - 1) ** 2,
            -(r - 1) / (r + 1),
            2,
            2,
        ),
        (
            "B2-",
            r,
            -1,
            (0, -1, g, 0),
            (0, 1, 3, 8, 9, 12),
            64 * g * r**2 * (r + 1) ** 2,
            -(r + 1) / (r - 1),
            2,
            -2,
        ),
        (
            "B3+",
            1,
            t,
            (0, 1, 0, g),
            (0, 1, 3, 8, 9, 13),
            64 * g * t**2 * (t - 1) ** 2,
            (t - 1) / (t + 1),
            1,
            2,
        ),
        (
            "B3-",
            -1,
            t,
            (0, -1, 0, g),
            (0, 1, 3, 8, 9, 13),
            -64 * g * t**2 * (t + 1) ** 2,
            (t + 1) / (t - 1),
            1,
            -2,
        ),
    )
    for (
        name,
        rv,
        tv,
        marking,
        rows,
        expected_rank,
        quotient,
        pure_row,
        pure_value,
    ) in sign_cases:
        output.extend(
            rank_two_audit(
                name,
                rv,
                tv,
                marking,
                ((rows, (0, 1, 2, 3, 4, 5), expected_rank),),
                (0, 1, 2, 7),
                (2, 1),
                lambda d, value=quotient: value,
                pure_row,
                lambda d, value=pure_value: (1 if d == 0 else -1) * value,
            )
        )

    output.extend(
        rank_two_audit(
            "Cdiag_qr_ne_1",
            r,
            r,
            (0, q, 0, 0),
            (
                (
                    (0, 1, 3, 8, 12, 13),
                    (0, 1, 2, 3, 4, 6),
                    128 * r**2 * (q * r - 1) ** 2,
                ),
            ),
            (0, 1, 3, 7),
            (1, 2),
            lambda d: (-1 if d == 0 else 1) * r,
            1,
            lambda d: (2 if d == 0 else -2) * r,
        )
    )
    output.extend(
        rank_two_audit(
            "Cdiag_qr_eq_1",
            r,
            r,
            (0, 1 / r, 0, 0),
            (
                (
                    (0, 1, 3, 8, 12, 13),
                    (0, 1, 2, 3, 5, 6),
                    64 * r**2 * (r - 1) * (r + 1),
                ),
            ),
            (0, 1, 3, 7),
            (1, 2),
            lambda d: (-1 if d == 0 else 1) * r,
            1,
            lambda d: (2 if d == 0 else -2) * r,
        )
    )
    for side, marking, rank_value in (
        (2, (0, 1 / r, g, 0), -64 * g * r**2 * (r - 1) ** 2 * (r + 1) ** 2),
        (3, (0, 1 / r, 0, g), 64 * g * r**2 * (r - 1) ** 2 * (r + 1) ** 2),
    ):
        output.extend(
            rank_two_audit(
                f"B{side}diag",
                r,
                r,
                marking,
                (((0, 1, 3, 8, 12, 13), (0, 1, 2, 3, 4, 5), rank_value),),
                (0, 1, 3, 7),
                (1, 2),
                lambda d: (-1 if d == 0 else 1) * r,
                1,
                lambda d: (2 if d == 0 else -2) * r,
            )
        )
    output.extend(endpoint_audit())
    return output


def endpoint_audit():
    output = []
    for endpoint in (1, -1):
        alpha, beta = corner_rows(endpoint, endpoint)
        for side, marking, rank_columns, rank_value in (
            (0, (0, endpoint, 0, 0), (0, 1, 2, 3, 6), -32),
            (2, (0, endpoint, g, 0), (0, 1, 2, 3, 5), 32 * g),
            (3, (0, endpoint, 0, g), (0, 1, 2, 3, 5), -32 * g),
        ):
            marked = shifted(alpha, beta, marking)
            for distinguished in (0, 1):
                mixed, diagonal0, diagonal1 = mixed_system(distinguished, alpha, marked)
                kernel = tuple(mixed.nullspace())
                assert len(kernel) == 3 and sp.Matrix.hstack(*kernel).rank() == 3
                rank_minor(
                    mixed,
                    (0, 1, 8, 12, 13),
                    rank_columns,
                    rank_value,
                )
                extension = kernel[0] * c0 + kernel[1] * c1 + kernel[2] * c2
                diagonals = (
                    sp.factor((diagonal0 * extension)[0]),
                    sp.factor((diagonal1 * extension)[0]),
                )
                determinant = sp.factor(
                    marked_extension(distinguished, extension, alpha, marked)
                    .extract((0, 1, 3, 7), range(4))
                    .det()
                )
                ratio = sp.factor(determinant / (diagonals[0] * diagonals[1] ** 2))
                assert (
                    sp.factor(ratio - (-1 if distinguished == 0 else 1) * endpoint) == 0
                )
                pure = sp.factor(one_marked_map(0, alpha, marked)[1, distinguished])
                assert (
                    sp.factor(pure - (1 if distinguished == 0 else -1) * 2 * endpoint)
                    == 0
                )
                output.append(
                    {
                        "endpoint": endpoint,
                        "side": side,
                        "insertion": distinguished,
                        "rank": 5,
                        "diagonal_ratio": str(ratio),
                        "pure_transverse": str(pure),
                    }
                )
    return output


def main():
    theorem = NOTE.read_text(encoding="utf-8")
    primary = PRIMARY.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero normalized-corner theorem",
        "seven branch ideals",
        "r=infinity",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    assert "normalized_finite_corner_marked_H31_empty" in primary

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
    pair_gcd = pair_audit(alpha, beta)
    projections = projection_audit(alpha, beta)
    branches = branch_audit()

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import exact characteristic-zero audit",
                "field": "Q",
                "corner": "s=0,k=infinity,finite (r,t)",
                "edge23_maximal_minor_gcd": pair_gcd,
                "reverse_normalization_projection_checks": projections,
                "branch_checks": branches,
                "all_marked_bases_covered": True,
                "all_four_insertions_covered": True,
                "projective_extensions_covered": True,
                "r_or_t_infinity_covered": False,
                "normalized_finite_corner_marked_H31_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
                "primary_sha256": hashlib.sha256(PRIMARY.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
