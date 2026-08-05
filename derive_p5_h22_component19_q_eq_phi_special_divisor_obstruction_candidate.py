#!/usr/bin/env python3
"""Exact component-19 q=phi weighted-H22 special-divisor candidate."""

from __future__ import annotations

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
REPORT = ROOT / "P5_H22_COMPONENT19_Q_EQ_PHI_SPECIAL_DIVISOR_OBSTRUCTION_CANDIDATE.md"
CERTIFICATE = ROOT / "p5_h22_component19_q_eq_phi_special_divisor_certificate.json"
INPUTS = tuple(ROOT / name for name in (
    "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md",
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md",
    "P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md",
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


def regular_q_equals_phi_basis(p, phi):
    """Reconstruct q=phi directly and choose a denominator-free pure basis."""
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    row00 = add(abar, scale(p, cap_b))
    row01 = add(bbar, scale(phi, cap_b))
    planes = (
        (row00, row01),
        (cap_b, cap_a),
        (bbar, cap_a),
        (abar, add(cap_b, scale(phi, bbar))),
    )
    # Swap the two mode-zero rows.  This has constant determinant -1 and
    # remains regular exactly where the original plane is regular.
    alpha = (row01, cap_b, bbar, abar)
    beta = (row00, cap_a, cap_a, planes[3][1])
    change = sp.Matrix(((0, 1), (1, 0)))
    assert change.det() == -1
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


def pair_certificates(planes, p, phi):
    selections = {
        "01": (4, (1, 3, 4, 5), (0, 1, 2, 3), 8 * p * phi),
        "02": (4, (1, 2, 3, 5), (0, 1, 2, 3), 8 * p),
        "03": (3, (1, 2, 5), (0, 1, 2), 4 * p ** 2),
        "12": (3, (0, 2, 3), (1, 2, 3), 4),
        "13": (3, (1, 4, 5), (0, 1, 3), -4),
        "23": (3, (1, 2, 5), (0, 1, 3), 4 * phi),
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

    # The only extra parameter boundary on a nonzero tensor is phi=0: edge
    # 23 then has rank exactly two, proved without a generic-rank inference.
    matrix23_at_phi0 = pair_matrix(planes[2], planes[3]).subs(phi, 0)
    assert matrix23_at_phi0.rank() == 2
    boundary_minor = sp.factor(
        matrix23_at_phi0.extract((1, 2), (0, 3)).det()
    )
    assert boundary_minor == 2
    assert [output[f"{i}{j}"]["rank"] for i, j in PAIRS] == [4, 4, 3, 3, 3, 3]
    return output, {
        "parameter": "phi=0", "edge": "23", "rank": 2,
        "rank_two_witness": {
            "rows": [1, 2], "columns": [0, 3],
            "determinant": str(boundary_minor),
        },
    }


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
        "coefficients": coefficients, "mixed": mixed,
        "A": coefficients[WORDS[0]], "B": coefficients[WORDS[-1]],
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


def ideal_check(
    label, equations, eliminated, retained, coefficient_ring, expected=None
):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=" + coefficient_ring + ",(" + ",".join(map(str, variables))
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
        "coefficient_ring": coefficient_ring,
        "projected_ideal": ["1"] if expected is None else [
            str(sp.factor(value)) for value in expected
        ],
        "bidirectional_ideal_equality": expected is not None,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def incidence_certificates(alpha, unmarked_beta, p, phi):
    slope = sp.Symbol("lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverse0, inverse1 = sp.symbols("u v")
    beta = shifted_beta(alpha, unmarked_beta, shifts)
    output = []
    for chart in ("finite", "infinity"):
        retained_field = shifts + ((slope,) if chart == "finite" else ())
        retained_polynomial = (p, phi) + retained_field
        d01 = build_model(alpha, beta, extensions, "D01", chart, slope)
        d23 = build_model(alpha, beta, extensions, "D23", chart, slope)
        systems = {
            "D01_binary": (
                *tuple(d01["mixed"] * sp.Matrix(extensions)),
                d01["A"] - 1, inverse0 * d01["B"] - 1,
            ),
            "D23_binary": (
                *tuple(d23["mixed"] * sp.Matrix(extensions)),
                d23["A"] - 1, inverse0 * d23["B"] - 1,
            ),
        }
        common_mixed = (
            *tuple(d01["mixed"] * sp.Matrix(extensions)),
            *tuple(d23["mixed"] * sp.Matrix(extensions)),
        )
        systems["shared_A01"] = (
            *common_mixed, d01["A"] - 1,
            inverse0 * d01["B"] - 1, inverse1 * d23["B"] - 1,
        )
        systems["shared_A23"] = (
            *common_mixed, d23["A"] - 1,
            inverse0 * d01["B"] - 1, inverse1 * d23["B"] - 1,
        )

        for name, equations in systems.items():
            inverse_variables = (
                extensions + (inverse0, inverse1)
                if name.startswith("shared_") else extensions + (inverse0,)
            )
            output.append(ideal_check(
                f"{name}_{chart}_over_Q(p,phi)", equations,
                inverse_variables, retained_field, "(0,p,phi)",
            ))
            expected_polynomial = None
            if name == "D01_binary":
                expected_polynomial = (
                    shifts[3], shifts[2], shifts[0], phi,
                )
            output.append(ideal_check(
                f"{name}_{chart}_parameter_aware", equations,
                inverse_variables, retained_polynomial, "0",
                expected_polynomial,
            ))
    return output


def main():
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert stored["claim_label"] == "VERIFIED"
    assert stored["discovery_claim_label"] == "CANDIDATE"
    p, phi = sp.symbols("p phi")
    planes, alpha, beta = regular_q_equals_phi_basis(p, phi)
    shifts = sp.symbols("h0:4")
    coefficients = original_coefficients(alpha, shifted_beta(alpha, beta, shifts))
    support = {
        "".join(map(str, word)): str(value)
        for word, value in coefficients.items() if value != 0
    }
    assert support == {"1111": "4*p"}
    pairs, phi0_boundary = pair_certificates(planes, p, phi)
    incidence = incidence_certificates(alpha, beta, p, phi)

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
        "regular_intrinsic_basis": {
            "field": "Q(p,phi)", "divisor": "q=phi",
            "mode0_change_determinant": "-1",
            "alpha": [[str(value) for value in row] for row in alpha],
            "beta": [[str(value) for value in row] for row in beta],
            "contains_q_minus_phi_denominator": False,
        },
        "pure_and_pair_open": {
            "pure_support_after_all_affine_markings": support,
            "flattening_kernels": flattening_certificates(coefficients),
            "exact_nonzero_all_pair_open": "p*phi!=0",
            "pair_profile": [pairs[f"{i}{j}"]["rank"] for i, j in PAIRS],
            "pair_certificates": pairs,
            "phi_zero_boundary": phi0_boundary,
            "p_zero_boundary": "pure coefficient 4*p vanishes",
        },
        "projective_incidence_certificates": incidence,
        "incidence_count": len(incidence),
        "orientation_cover": (
            "B01 and B23 are saturated nonzero; normalized A01 and A23 "
            "orientations cover the required disjunction"
        ),
        "false_lead_boundary": {
            "parameter": "phi=0",
            "D01_binary_projection_closure": ["h3", "h2", "h0", "phi"],
            "why_not_in_scope": "edge 23 has rank two, so the P4 point is not all-pair-open",
            "shared_A01_and_A23": "both parameter-aware unit ideals",
        },
        "weighted_H22_fibre_empty_on_p_phi_nonzero": True,
        "genuine_survivor_found": False,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": stored["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
