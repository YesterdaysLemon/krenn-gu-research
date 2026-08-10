#!/usr/bin/env python3
"""No-import exact audit of component 23's k=infinity marked-H31 theorem."""

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
    "P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_K_INFINITY_"
    "ALL_PAIR_BOUNDARY_OBSTRUCTION.md"
)
PRIMARY = ROOT / (
    "verify_p5_h31_common_center_kernel_star_component_k_infinity_"
    "all_pair_boundary_obstruction.py"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

r, localizer = sp.symbols("r v")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
inverse = sp.Symbol("u")
p, w = sp.symbols("p w")

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


def boundary_rows():
    alpha = (
        A,
        D,
        add(A, scale(-1, C), B, scale(r, D)),
        add(scale(-1, A), scale(-1, C), B, scale(r, D)),
    )
    beta = (B, add(B, C), C, C)
    return alpha, beta


def shifted(alpha, beta, shifts):
    return tuple(
        add(beta[index], scale(shifts[index], alpha[index])) for index in range(4)
    )


def projected_rows(distinguished, extension, alpha, beta):
    common = tuple(index for index in range(4) if index != distinguished)
    alpha_projected = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common) + (extension[mode],)
        for mode in range(4)
    )
    beta_projected = tuple(
        tuple(beta[mode][coordinate] for coordinate in common) + (extension[4 + mode],)
        for mode in range(4)
    )
    return alpha_projected, beta_projected


def extension_coefficients(distinguished, extension, alpha, beta):
    alpha_projected, beta_projected = projected_rows(
        distinguished, extension, alpha, beta
    )
    return {
        word: permanent(
            tuple(
                beta_projected[index] if word[index] else alpha_projected[index]
                for index in range(4)
            )
        )
        for word in WORDS
    }


def mixed_system(distinguished, alpha, beta):
    coefficients = extension_coefficients(distinguished, sp.Matrix(x), alpha, beta)
    mixed_words = tuple(word for word in WORDS if word not in (WORDS[0], WORDS[-1]))
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in x]
            for word in mixed_words
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
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(row)
    return sp.Matrix(rows)


def marked_extension(distinguished, extension, alpha, beta, mode):
    projected = projected_rows(distinguished, extension, alpha, beta)
    return one_marked_map(mode, *projected)


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(symmetric_product(left[i], right[j]) for i in range(2) for j in range(2))
    )


def pair_audit(alpha, beta):
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    matrices = tuple(pair_matrix(planes[left], planes[right]) for left, right in PAIRS)
    assert tuple(matrix.rank() for matrix in matrices) == (3, 3, 3, 4, 4, 3)
    minors = tuple(
        sp.factor(matrices[-1].extract(rows, columns).det())
        for rows in itertools.combinations(range(6), 3)
        for columns in itertools.combinations(range(4), 3)
        if matrices[-1].extract(rows, columns).det() != 0
    )
    assert sp.factor(sp.gcd_list(minors) - 4 * (r - 1) * (r + 1)) == 0
    endpoints = tuple(
        tuple(matrix.subs(r, value).rank() for matrix in matrices) for value in (1, -1)
    )
    assert endpoints == ((3, 3, 3, 4, 4, 2), (3, 3, 3, 4, 4, 2))
    return endpoints


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def run_singular(label, program, expected):
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


def opposite_diagonal_projection(distinguished, alpha, beta):
    marked = shifted(alpha, beta, h)
    mixed, diagonal0, diagonal1 = mixed_system(distinguished, alpha, marked)
    vector = sp.Matrix(x)
    # This audit reverses the primary normalization: b_d z=1 and a_d z is inverted.
    equations = (
        *tuple(mixed * vector),
        (diagonal1 * vector)[0] - 1,
        inverse * (diagonal0 * vector)[0] - 1,
        localizer * (r**2 - 1) - 1,
    )
    eliminated = x + (inverse,)
    variables = eliminated + (r, localizer) + h
    lines = [
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(6));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_text(value) for value in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    if distinguished in (0, 1):
        zero_variable = "h2" if distinguished == 0 else "h3"
        branch_variable = "h3" if distinguished == 0 else "h2"
        common = f"v*(r^2-1)-1,h0,{zero_variable}"
        lines.extend(
            (
                f"ideal B0={common},{branch_variable},4*r*h1-r^2-3; B0=std(B0);",
                f"ideal B1={common},2*{branch_variable}+1,r*h1-1; B1=std(B1);",
                "ideal E=std(intersect(B0,B1));",
            )
        )
        expected_size = 8
    else:
        lines.append("ideal E=1; E=std(E);")
        expected_size = 1
    lines.extend(
        (
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "ideal Z=std(J,r);",
            (
                'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"'
                '+string(size(J))+":"+string(reduce(1,Z)==0));'
            ),
            "quit;",
        )
    )
    run_singular(
        f"opposite normalization insertion {distinguished}",
        "\n".join(lines),
        f"RESULT:1:{expected_size}:1",
    )


def direct_r_zero_projection(distinguished, alpha, beta):
    marked = shifted(alpha, beta, h)
    mixed, diagonal0, diagonal1 = mixed_system(distinguished, alpha, marked)
    vector = sp.Matrix(x)
    equations = (
        *tuple((mixed * vector).subs(r, 0)),
        ((diagonal1 * vector)[0] - 1).subs(r, 0),
        (inverse * (diagonal0 * vector)[0] - 1).subs(r, 0),
    )
    eliminated = x + (inverse,)
    variables = eliminated + h
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(singular_text(value) for value in equations) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            'print("RESULT:"+string(reduce(1,J)==0)+":"+string(size(J)));',
            "quit;",
        )
    )
    run_singular(f"opposite r=0 insertion {distinguished}", program, "RESULT:1:1")


def branch_audit(alpha, beta):
    delta = r**2 - 1
    rank_certificates = {
        "J00": ((0, 1, 3, 7, 11, 13), (0, 1, 2, 3, 4, 6), -32 * r**2 * delta**2),
        "J01": ((0, 1, 3, 7, 11, 13), (0, 1, 2, 3, 4, 5), 128 * r**2 * delta**2),
        "J10": ((0, 1, 3, 7, 11, 12), (0, 1, 2, 3, 4, 6), 32 * r**2 * delta**2),
        "J11": ((0, 1, 3, 7, 11, 12), (0, 1, 2, 3, 4, 5), 128 * r**2 * delta**2),
    }
    cases = (
        (
            "J00",
            0,
            (0, (r**2 + 3) / (4 * r), 0, 0),
            (0, -4 * r / delta, -2, -2, -4 / delta, 1, 0, 0),
            (1, 4 * r / delta, 2, 0, 4 / delta, 0, 1, 1),
            (16 * r * (p - w), -4 * w),
            (0, 1, 3, 7),
            -r,
            (1, 2),
            -4 * r,
        ),
        (
            "J01",
            0,
            (0, 1 / r, 0, -sp.Rational(1, 2)),
            (1, -2 * r / delta, -2, -2, -2 / delta, 1, 1, 0),
            (0, r / delta, 1, 0, 1 / delta, 0, 0, 1),
            (4 * r * (2 * p - w), -2 * w),
            (0, 1, 2, 7),
            -sp.Rational(1, 2),
            (2, 1),
            -4 * r,
        ),
        (
            "J10",
            1,
            (0, (r**2 + 3) / (4 * r), 0, 0),
            (0, -4 * r / delta, -2, -2, -4 / delta, 1, 0, 0),
            (-1, 4 * r / delta, 0, 2, 4 / delta, 0, 1, 1),
            (16 * r * (p - w), 4 * w),
            (0, 1, 3, 7),
            r,
            (1, 2),
            4 * r,
        ),
        (
            "J11",
            1,
            (0, 1 / r, -sp.Rational(1, 2), 0),
            (0, r / delta, 0, 1, 1 / delta, 0, 1, 0),
            (-1, -2 * r / delta, -2, -2, -2 / delta, 1, 0, 1),
            (-4 * r * (p - 2 * w), 2 * p),
            (0, 1, 2, 7),
            sp.Rational(1, 2),
            (2, 1),
            4 * r,
        ),
    )
    result = []
    for (
        name,
        distinguished,
        marking,
        e0,
        e1,
        diagonals,
        rows,
        factor,
        powers,
        pure,
    ) in cases:
        marked = shifted(alpha, beta, marking)
        mixed, diagonal0, diagonal1 = mixed_system(distinguished, alpha, marked)
        frame = (sp.Matrix(e0), sp.Matrix(e1))
        assert mixed.rank() == 6
        assert all(
            all(sp.factor(value) == 0 for value in mixed * vector) for vector in frame
        )
        rank_rows, rank_columns, expected_rank_minor = rank_certificates[name]
        rank_minor = sp.factor(mixed.extract(rank_rows, rank_columns).det())
        assert sp.factor(rank_minor - expected_rank_minor) == 0
        extension = frame[0] * p + frame[1] * w
        observed = (
            sp.factor((diagonal0 * extension)[0]),
            sp.factor((diagonal1 * extension)[0]),
        )
        assert all(
            sp.factor(left - right) == 0 for left, right in zip(observed, diagonals)
        )
        matrix = marked_extension(distinguished, extension, alpha, marked, 0)
        determinant = sp.factor(matrix.extract(rows, range(4)).det())
        expected = sp.factor(
            factor * observed[0] ** powers[0] * observed[1] ** powers[1]
        )
        assert sp.factor(determinant - expected) == 0
        transverse = sp.factor(one_marked_map(0, alpha, marked)[0, distinguished])
        assert sp.factor(transverse - pure) == 0
        result.append(
            {
                "branch": name,
                "rank_minor": str(rank_minor),
                "one_marked_minor": str(determinant),
                "pure_transverse": str(pure),
            }
        )
    return result


def main():
    theorem = NOTE.read_text(encoding="utf-8")
    primary = PRIMARY.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero normalized-boundary theorem",
        "projective extension direction",
        "component thirteen",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    assert "normalized_all_pair_marked_H31_boundary_empty" in primary

    alpha, beta = boundary_rows()
    coefficients = {
        word: sp.factor(
            permanent(
                tuple(
                    alpha[index] if word[index] == 0 else beta[index]
                    for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert coefficients[(1, 1, 1, 1)] == -4
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )
    assert all(sp.Matrix((alpha[index], beta[index])).rank() == 2 for index in range(4))
    endpoints = pair_audit(alpha, beta)
    for distinguished in range(4):
        opposite_diagonal_projection(distinguished, alpha, beta)
        direct_r_zero_projection(distinguished, alpha, beta)
    branches = branch_audit(alpha, beta)

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import exact characteristic-zero audit",
                "field": "Q",
                "base_ring": "Q[r,1/((r-1)*(r+1))]",
                "projection_normalization": "B diagonal normalized; A diagonal inverted",
                "all_four_localized_projections_verified": True,
                "all_four_direct_r_zero_unit_ideals": True,
                "r_plus_minus_one_profiles": endpoints,
                "branches": branches,
                "projective_extension_normalization_complete": True,
                "projective_marking_endpoint_is_not_a_basis": True,
                "normalized_all_pair_marked_H31_boundary_empty": True,
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
