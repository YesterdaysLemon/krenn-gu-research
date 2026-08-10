#!/usr/bin/env python3
"""Exact component-19 q=0, phi=+/-1 weighted-H22 endpoint candidate."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import sympy as sp

ROOT = HERE
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_Q0_PHI_ENDPOINTS_OBSTRUCTION_CANDIDATE.md"
CERTIFICATE = ROOT / "p5_h22_component19_q0_phi_endpoints_certificate.json"
INPUTS = tuple(REPO_ROOT / name for name in (
    "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md",
    "P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_OBSTRUCTION_CANDIDATE.md",
    "p5_h22_component19_q0_special_divisor_certificate.json",
    "derive_p5_h22_component19_q0_special_divisor_obstruction_candidate.py",
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md",
))

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True, encoding="utf-8",
        capture_output=True, check=True, timeout=15,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def permanent3(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(3))
        for permutation in PERMUTATIONS3
    ))


def permanent4(rows):
    return sp.factor(sum(
        sp.prod(rows[i][permutation[i]] for i in range(4))
        for permutation in PERMUTATIONS4
    ))


def endpoint_planes_and_basis(p, epsilon):
    """Reconstruct q=0, phi=epsilon directly over Q(p)."""
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    planes = (
        (add(abar, scale(p, cap_b)), bbar),
        (cap_b, cap_a),
        (bbar, cap_a),
        (abar, add(cap_b, scale(epsilon, bbar))),
    )
    first, second = planes[0]
    alpha0 = add(scale(-epsilon, first), scale(-p, second))
    alpha = (alpha0, cap_b, bbar, abar)
    beta = (first, cap_a, cap_a, planes[3][1])
    change = sp.Matrix(((-epsilon, 1), (-p, 0)))
    assert sp.factor(change.det() - p) == 0
    return planes, alpha, beta


def shifted_beta(alpha, beta, shifts):
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def original_coefficients(alpha, beta):
    return {
        word: permanent4(tuple(
            beta[i] if word[i] else alpha[i] for i in range(4)
        ))
        for word in WORDS
    }


def flattening_certificates(coefficients):
    output = []
    for mode in range(4):
        other = tuple(index for index in range(4) if index != mode)
        columns = tuple(itertools.product((0, 1), repeat=3))
        matrix = sp.Matrix([
            [
                coefficients[tuple(
                    bit if index == mode else column[other.index(index)]
                    for index in range(4)
                )]
                for column in columns
            ]
            for bit in (0, 1)
        ])
        assert matrix.rank() == 1
        assert matrix.T.nullspace() == [sp.Matrix((1, 0))]
        output.append({
            "mode": mode, "rank": 1,
            "kernel_in_alpha_beta_coordinates": [1, 0],
        })
    return output


def squarefree_product(left, right):
    return sp.Matrix(tuple(
        sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS
    ))


def pair_matrix(left_plane, right_plane):
    return sp.Matrix.hstack(*(
        squarefree_product(left_plane[i], right_plane[j])
        for i in range(2) for j in range(2)
    ))


def pair_certificates(planes, p, epsilon):
    selections = {
        "01": (3, (1, 2, 3), (0, 1, 3), 4 * p),
        "02": (4, (1, 2, 3, 5), (0, 1, 2, 3), 8 * p),
        "03": (4, (0, 1, 2, 5), (0, 1, 2, 3), -8 * epsilon),
        "12": (3, (0, 1, 2), (1, 2, 3), -4),
        "13": (3, (1, 2, 5), (0, 1, 3), 4 * epsilon),
        "23": (3, (1, 2, 5), (0, 1, 3), 4 * epsilon),
    }
    output = {}
    for i, j in PAIRS:
        label = f"{i}{j}"
        rank, rows, columns, expected = selections[label]
        matrix = pair_matrix(planes[i], planes[j])
        determinant = sp.factor(matrix.extract(rows, columns).det())
        assert sp.factor(determinant - expected) == 0
        higher_checked = 0
        if rank == 3:
            for row_set in itertools.combinations(range(6), 4):
                assert sp.factor(matrix.extract(row_set, range(4)).det()) == 0
                higher_checked += 1
        output[label] = {
            "rank": rank,
            "witness": {
                "rows": list(rows), "columns": list(columns),
                "determinant": str(determinant),
            },
            "higher_minors_checked_zero": higher_checked,
        }
    assert [output[f"{i}{j}"]["rank"] for i, j in PAIRS] == [3, 4, 4, 3, 3, 3]
    return output


def project(row, extension, direction, chart, slope=None):
    if direction == "D01" and chart == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23" and chart == "finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart, slope))


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
        coefficients[word] = sp.factor(sum(
            selected[i][3] * permanent3(tuple(
                selected[j][:3] for j in range(4) if j != i
            ))
            for i in range(4)
        ))
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], value) for value in extensions]
        for word in MIXED
    ])
    return {
        "alpha_rows": alpha_rows, "beta_rows": beta_rows,
        "coefficients": coefficients, "mixed": mixed,
        "A": coefficients[WORDS[0]], "B": coefficients[WORDS[-1]],
    }


def one_marked_matrix(model, mode):
    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            model["beta_rows"][index] if bits[position]
            else model["alpha_rows"][index]
            for position, index in enumerate(other)
        )
        rows.append(tuple(
            permanent3(tuple(
                tuple(row[column] for column in range(4) if column != omitted)
                for row in selected
            ))
            for omitted in range(4)
        ))
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


def ideal_check(label, equations, eliminated, retained, expected=None):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=(0,p),(" + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    if expected is None:
        lines.append('"CODEX_RESULT:"+string(reduce(1,J)==0)+":"+string(size(J));')
    else:
        lines.extend((
            "ideal Expected=" + ",".join(map(singular, expected)) + ";",
            "Expected=std(Expected);",
            "ideal JE=simplify(reduce(J,Expected),2);",
            "ideal EJ=simplify(reduce(Expected,J),2);",
            '"CODEX_RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
        ))
    lines.append("quit;")
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
        timeout=120, check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stdout, completed.stderr
    )
    markers = [
        line for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        label, completed.stdout
    )
    return {
        "label": label,
        "ideal": ["1"] if expected is None else [
            str(sp.factor(value)) for value in expected
        ],
        "bidirectional_ideal_equality": expected is not None,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def projective_incidence(alpha, unmarked_beta, epsilon):
    slope = sp.Symbol("lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverse0, inverse1 = sp.symbols("u v")
    beta = shifted_beta(alpha, unmarked_beta, shifts)
    output = []
    for chart in ("finite", "infinity"):
        retained = shifts + ((slope,) if chart == "finite" else ())
        d01 = build_model(alpha, beta, extensions, "D01", chart, slope)
        d23 = build_model(alpha, beta, extensions, "D23", chart, slope)
        for label, model, direction in (
            ("D01_binary", d01, "D01"), ("D23_binary", d23, "D23")
        ):
            if direction == "D01":
                expected = (
                    sp.Symbol("p") * shifts[3] + 1,
                    shifts[1], shifts[0] - epsilon,
                )
            elif chart == "finite":
                expected = (
                    shifts[3], shifts[0] - epsilon,
                    shifts[1] * shifts[2] * (slope - 1),
                    shifts[1] ** 2 * shifts[2],
                )
            else:
                expected = (
                    shifts[3], shifts[0] - epsilon, shifts[1] * shifts[2],
                )
            output.append(ideal_check(
                f"phi_{epsilon:+d}_{label}_{chart}",
                (*tuple(model["mixed"] * sp.Matrix(extensions)),
                 model["A"] - 1, inverse0 * model["B"] - 1),
                extensions + (inverse0,), retained, expected,
            ))

        common_mixed = (
            *tuple(d01["mixed"] * sp.Matrix(extensions)),
            *tuple(d23["mixed"] * sp.Matrix(extensions)),
        )
        for orientation, normalized in (("A01", d01["A"]), ("A23", d23["A"])):
            expected = None
            if orientation == "A23" and chart == "finite":
                expected = (
                    slope - 1, shifts[3], shifts[1], shifts[0] - epsilon,
                )
            output.append(ideal_check(
                f"phi_{epsilon:+d}_shared_{orientation}_{chart}",
                (*common_mixed, normalized - 1,
                 inverse0 * d01["B"] - 1,
                 inverse1 * d23["B"] - 1),
                extensions + (inverse0, inverse1), retained, expected,
            ))
    return output


def rank_drop_check(label, minors, genuine_product, expected=None):
    inverse = sp.Symbol("w")
    cap_c, cap_d, cap_e, t = sp.symbols("C D E t")
    return ideal_check(
        label, (*minors, inverse * genuine_product - 1), (inverse,),
        (cap_c, cap_d, cap_e, t), expected,
    )


def all_minors(matrix, size):
    output = []
    for rows in itertools.combinations(range(matrix.rows), size):
        for columns in itertools.combinations(range(matrix.cols), size):
            determinant = sp.factor(matrix.extract(rows, columns).det())
            if determinant != 0:
                output.append(determinant)
    return output


def shared_branch(alpha, unmarked_beta, p, epsilon):
    cap_c, cap_d, cap_e, t = sp.symbols("C D E t")
    extensions = sp.symbols("x0:8")
    beta = shifted_beta(alpha, unmarked_beta, (epsilon, 0, t, 0))
    d01 = build_model(alpha, beta, extensions, "D01", "finite", 1)
    d23 = build_model(alpha, beta, extensions, "D23", "finite", 1)
    combined = sp.Matrix.vstack(d01["mixed"], d23["mixed"])
    rank_rows = (1, 2, 10, 12, 15)
    rank_columns = (0, 1, 2, 3, 6)
    rank_minor = sp.factor(combined.extract(rank_rows, rank_columns).det())
    assert sp.factor(rank_minor - 1024 * p ** 3) == 0

    vector_c = sp.Matrix((0, -1 / p, epsilon / p, 0, 1, 0, 0, 0))
    vector_d = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    vector_e = sp.Matrix((epsilon * p, 0, -epsilon, 0, 0, 0, 0, 1))
    frame = sp.Matrix.hstack(vector_c, vector_d, vector_e)
    assert frame.rank() == 3
    assert all(sp.factor(value) == 0 for value in combined * frame)

    extension = cap_c * vector_c + cap_d * vector_d + cap_e * vector_e
    substitutions = dict(zip(extensions, extension, strict=True))
    a01 = sp.factor(d01["A"].subs(substitutions))
    b01 = sp.factor(d01["B"].subs(substitutions))
    a23 = sp.factor(d23["A"].subs(substitutions))
    b23 = sp.factor(d23["B"].subs(substitutions))
    cap_q = cap_c - p * cap_e
    cap_r = p * cap_d - epsilon * t * cap_q
    assert a01 == 0
    assert sp.factor(b01 - 4 * cap_r) == 0
    assert sp.factor(a23 - 4 * cap_q / p) == 0
    assert sp.factor(b23 - 4 * cap_c) == 0
    genuine = cap_c * cap_q * cap_r

    matrices = {
        f"D01_mode_{mode}": one_marked_matrix(d01, mode).subs(substitutions)
        for mode in range(4)
    }
    matrices.update({
        f"D23_mode_{mode}": one_marked_matrix(d23, mode).subs(substitutions)
        for mode in range(4)
    })

    # Exact upper ranks and fixed lower-rank witnesses.
    assert not all_minors(matrices["D01_mode_0"], 4)
    for mode in (1, 2):
        assert not all_minors(matrices[f"D01_mode_{mode}"], 2)
        assert matrices[f"D01_mode_{mode}"][7, 3] == 4 * p
    for mode in (0, 1):
        assert not all_minors(matrices[f"D23_mode_{mode}"], 4)

    q0_rows = (0, 5, 7) if epsilon == 1 else (0, 3, 7)
    fixed = {
        "D01_mode_1_rank1": ((7,), (3,), 4 * p),
        "D01_mode_2_rank1": ((7,), (3,), 4 * p),
        "D23_mode_0_rank3": (q0_rows, (0, 1, 3), -32 * cap_q ** 2 / p ** 2),
        "D23_mode_1_rank3": (
            (0, 1, 7), (0, 1, 2), 16 * cap_c * cap_q ** 2 / p ** 2,
        ),
        "D23_mode_2_rank3": (
            (0, 4, 7), (0, 1, 3), -32 * epsilon * cap_c ** 2,
        ),
        "D23_mode_2_rank4_if_D_nonzero": (
            (0, 1, 2, 7), (0, 1, 2, 3),
            -64 * epsilon * cap_c * cap_d * cap_q / p,
        ),
        "D23_mode_3_rank4": (
            (0, 2, 3, 7), (0, 1, 2, 3),
            -64 * epsilon * cap_c * cap_q ** 2,
        ),
    }
    fixed_output = {}
    for label, (rows, columns, expected) in fixed.items():
        matrix_label = label.split("_rank")[0]
        determinant = sp.factor(matrices[matrix_label].extract(rows, columns).det())
        assert sp.factor(determinant - expected) == 0
        fixed_output[label] = {
            "rows": list(rows), "columns": list(columns),
            "determinant": str(determinant),
        }

    drop_checks = []
    drop_checks.append(rank_drop_check(
        f"phi_{epsilon:+d}_D01_mode0_rank_below_3_on_genuine",
        all_minors(matrices["D01_mode_0"], 3), genuine,
        (2 * cap_c - p * cap_e, cap_e * t - 2 * epsilon * cap_d),
    ))
    drop_checks.append(rank_drop_check(
        f"phi_{epsilon:+d}_D01_mode3_rank_below_4_on_genuine",
        all_minors(matrices["D01_mode_3"], 4), genuine,
    ))
    drop_checks.append(rank_drop_check(
        f"phi_{epsilon:+d}_D23_mode2_rank_below_4_on_genuine",
        all_minors(matrices["D23_mode_2"], 4), genuine, (cap_d,),
    ))
    drop_checks.append(rank_drop_check(
        f"phi_{epsilon:+d}_D23_mode3_rank_below_4_on_genuine",
        all_minors(matrices["D23_mode_3"], 4), genuine,
    ))

    # On the D01 mode-zero rank-drop locus, genuineness forces C*t != 0,
    # and this fixed 2-minor proves the rank is exactly two.
    rankdrop_substitution = {
        cap_e: 2 * cap_c / p,
        cap_d: epsilon * cap_c * t / p,
    }
    mode0_drop = matrices["D01_mode_0"].subs(rankdrop_substitution)
    drop_columns = (2, 3) if epsilon == 1 else (1, 3)
    drop_minor = sp.factor(mode0_drop.extract((3, 7), drop_columns).det())
    assert sp.factor(drop_minor + 32 * epsilon * cap_c * t / p) == 0
    assert not all_minors(mode0_drop, 3)

    return {
        "weight": "[1:1]", "marking": f"h=({epsilon},0,t,0)",
        "mixed_matrix_shape": list(combined.shape), "mixed_rank": 5,
        "rank_witness": {
            "rows": list(rank_rows), "columns": list(rank_columns),
            "determinant": str(rank_minor),
        },
        "complete_kernel_frame": [
            [str(sp.factor(value)) for value in vector]
            for vector in (vector_c, vector_d, vector_e)
        ],
        "diagonals": {
            "A01": str(a01), "B01": str(b01),
            "A23": str(a23), "B23": str(b23),
        },
        "genuine_locus": "C*(C-p*E)*(p*D-epsilon*t*(C-p*E))!=0",
        "fixed_minors": fixed_output,
        "rank_drop_ideal_checks": drop_checks,
        "one_marked_rank_classification": {
            "D01": [
                "rank 3 except rank 2 on 2*C-p*E=E*t-2*epsilon*D=0",
                "rank 1", "rank 1", "rank 4 everywhere genuine",
            ],
            "D23": [
                "rank 3", "rank 3",
                "rank 4 iff D!=0, otherwise rank 3",
                "rank 4 everywhere genuine",
            ],
        },
        "D01_mode0_rankdrop_fixed_2minor": {
            "rows": [3, 7], "columns": list(drop_columns),
            "determinant": str(drop_minor),
        },
        "obstruction": (
            "D23 mode 3 has rank 4 on every genuine point by the fixed minor "
            "-64*epsilon*C*(C-p*E)^2"
        ),
    }


def endpoint_certificate(p, epsilon):
    planes, alpha, beta = endpoint_planes_and_basis(p, epsilon)
    shifts = sp.symbols("h0:4")
    coefficients = original_coefficients(alpha, shifted_beta(alpha, beta, shifts))
    support = {
        "".join(map(str, word)): str(value)
        for word, value in coefficients.items() if value != 0
    }
    assert support == {"1111": "4*p"}
    return {
        "epsilon": epsilon,
        "field": "Q(p)", "open": "p!=0",
        "planes": [
            [[str(value) for value in row] for row in plane] for plane in planes
        ],
        "alpha": [[str(value) for value in row] for row in alpha],
        "beta": [[str(value) for value in row] for row in beta],
        "mode0_basis_change_determinant": "p",
        "pure_support_after_all_affine_markings": support,
        "flattening_kernels": flattening_certificates(coefficients),
        "pair_profile": [3, 4, 4, 3, 3, 3],
        "pair_certificates": pair_certificates(planes, p, epsilon),
        "projective_incidence": projective_incidence(alpha, beta, epsilon),
        "shared_branch": shared_branch(alpha, beta, p, epsilon),
        "weighted_H22_fibre_empty": True,
    }


def main():
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert stored["claim_label"] == "VERIFIED"
    assert stored["discovery_claim_label"] == "CANDIDATE"
    p = sp.Symbol("p")
    endpoints = {
        "phi_plus_1": endpoint_certificate(p, 1),
        "phi_minus_1": endpoint_certificate(p, -1),
    }
    result = {
        "status": "pass", "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "git_commit": git_commit(), "claim_label": "VERIFIED",
        "discovery_claim_label": "CANDIDATE",
        "scope": stored["scope"],
        "inputs": {path.name: sha256(path) for path in INPUTS},
        "method": stored["method"],
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT), CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "endpoints": endpoints,
        "signs_replayed_separately": True,
        "genuine_survivor_found": False,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": stored["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
