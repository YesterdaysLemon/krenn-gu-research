#!/usr/bin/env python3
"""Direct exact replay for component 19 on p=0, q*phi=1, phi^2!=1."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_P0_QPHI_ONE_ORDINARY_OBSTRUCTION_CANDIDATE.md"
CERTIFICATE = ROOT / "p5_h22_component19_p0_qphi_one_ordinary_obstruction_certificate.json"
INPUTS = tuple(REPO_ROOT / name for name in (
    "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md",
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md",
    "docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md",
))

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
MIXED4 = WORDS4[1:-1]
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True,
        capture_output=True, check=True, timeout=15,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.expand(sum(row[i] for row in rows)) for i in range(len(rows[0])))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def permanent(rows):
    size = len(rows)
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(size))
        for permutation in itertools.permutations(range(size))
    ))


def assert_zero(value):
    if isinstance(value, sp.MatrixBase):
        assert all(sp.factor(entry) == 0 for entry in value)
    else:
        assert sp.factor(value) == 0


def divisor_basis(phi):
    """Reconstruct q=1/phi directly; no generic p=0 formula is imported."""
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    common_beta = add(cap_b, scale(phi, bbar))
    planes = (
        (abar, common_beta),
        (cap_b, cap_a),
        (bbar, cap_a),
        (abar, common_beta),
    )
    alpha = (abar, cap_b, bbar, abar)
    beta = (common_beta, cap_a, cap_a, common_beta)
    # The original first beta row is bbar+phi^{-1}B.  Multiplication by phi
    # gives common_beta, a unit change over Q(phi).
    return planes, alpha, beta


def shifted_beta(alpha, beta, markings):
    return tuple(add(beta[i], scale(markings[i], alpha[i])) for i in range(4))


def coefficients(alpha, beta):
    return {
        word: permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        for word in WORDS4
    }


def squarefree_product(left, right):
    return sp.Matrix(tuple(
        sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS
    ))


def pair_matrix(left_plane, right_plane):
    return sp.Matrix.hstack(*(
        squarefree_product(left_plane[i], right_plane[j])
        for i in range(2) for j in range(2)
    ))


def pair_certificates(planes, phi):
    fixed = {
        "01": ((1, 2, 5), (0, 2, 3), 4 * phi),
        "02": ((1, 2, 5), (0, 2, 3), 4 * phi),
        "03": ((0, 1, 5), (0, 1, 3), 4 * (phi - 1) * (phi + 1) ** 2),
        "12": ((0, 1, 2), (1, 2, 3), -4),
        "13": ((1, 2, 5), (0, 1, 3), 4 * phi),
        "23": ((1, 2, 5), (0, 1, 3), 4 * phi),
    }
    output = {}
    for i, j in PAIRS:
        label = f"{i}{j}"
        matrix = pair_matrix(planes[i], planes[j])
        assert all(
            sp.factor(matrix.extract(rows, range(4)).det()) == 0
            for rows in itertools.combinations(range(6), 4)
        )
        rows, columns, expected = fixed[label]
        determinant = sp.factor(matrix.extract(rows, columns).det())
        assert_zero(determinant - expected)
        output[label] = {
            "rank": 3, "rows": list(rows), "columns": list(columns),
            "determinant": str(determinant),
            "all_four_minors_zero": True,
        }
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
    raise ValueError((direction, chart))


def model(alpha, beta, extensions, direction, chart, slope=None):
    projected_alpha = tuple(
        project(alpha[i], extensions[i], direction, chart, slope) for i in range(4)
    )
    projected_beta = tuple(
        project(beta[i], extensions[4 + i], direction, chart, slope) for i in range(4)
    )
    tensor = {
        word: permanent(tuple(
            projected_beta[i] if word[i] else projected_alpha[i]
            for i in range(4)
        ))
        for word in WORDS4
    }
    mixed = sp.Matrix([
        [sp.diff(tensor[word], extension) for extension in extensions]
        for word in MIXED4
    ])
    return {
        "alpha": projected_alpha,
        "beta": projected_beta,
        "coefficients": tensor,
        "mixed": mixed,
    }


def one_marked(binary_model, mode):
    rows = []
    for word in WORDS3:
        selected = []
        bit = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    binary_model["beta"][other]
                    if word[bit] else binary_model["alpha"][other]
                )
                bit += 1
        rows.append([
            permanent(tuple(
                tuple(int(coordinate == column) for coordinate in range(4))
                if other == mode else selected[other]
                for other in range(4)
            ))
            for column in range(4)
        ])
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


def eliminate(label, equations, eliminated, retained, expected):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=(0,phi),(" + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + "; E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        '"CODEX_RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
        "quit;",
    ]
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
        timeout=120, check=False,
    )
    markers = [
        line for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stdout, completed.stderr
    )
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        label, completed.stdout
    )
    return {
        "label": label,
        "coefficient_field": "Q(phi)",
        "projected_ideal": [str(sp.factor(value)) for value in expected],
        "bidirectional_ideal_equality": True,
    }


def incidence_certificates(alpha, unmarked_beta):
    markings = sp.symbols("h0:4")
    slope = sp.Symbol("lam")
    extensions = sp.symbols("x0:8")
    inverse0, inverse1 = sp.symbols("u v")
    beta = shifted_beta(alpha, unmarked_beta, markings)
    expected = {
        ("D01_binary", "finite"): (sp.Integer(1),),
        ("D23_binary", "finite"): (markings[3], markings[0], markings[1] * markings[2]),
        ("shared_A01", "finite"): (sp.Integer(1),),
        ("shared_A23", "finite"): (slope - 1, markings[3], markings[1], markings[0]),
        ("D01_binary", "infinity"): (sp.Integer(1),),
        ("D23_binary", "infinity"): (markings[3], markings[0], markings[1] * markings[2]),
        ("shared_A01", "infinity"): (sp.Integer(1),),
        ("shared_A23", "infinity"): (sp.Integer(1),),
    }
    output = []
    for chart in ("finite", "infinity"):
        d01 = model(alpha, beta, extensions, "D01", chart, slope)
        d23 = model(alpha, beta, extensions, "D23", chart, slope)
        common_mixed = (
            *tuple(d01["mixed"] * sp.Matrix(extensions)),
            *tuple(d23["mixed"] * sp.Matrix(extensions)),
        )
        systems = {
            "D01_binary": (
                *tuple(d01["mixed"] * sp.Matrix(extensions)),
                d01["coefficients"][WORDS4[0]] - 1,
                inverse0 * d01["coefficients"][WORDS4[-1]] - 1,
            ),
            "D23_binary": (
                *tuple(d23["mixed"] * sp.Matrix(extensions)),
                d23["coefficients"][WORDS4[0]] - 1,
                inverse0 * d23["coefficients"][WORDS4[-1]] - 1,
            ),
            "shared_A01": (
                *common_mixed,
                d01["coefficients"][WORDS4[0]] - 1,
                inverse0 * d01["coefficients"][WORDS4[-1]] - 1,
                inverse1 * d23["coefficients"][WORDS4[-1]] - 1,
            ),
            "shared_A23": (
                *common_mixed,
                d23["coefficients"][WORDS4[0]] - 1,
                inverse0 * d01["coefficients"][WORDS4[-1]] - 1,
                inverse1 * d23["coefficients"][WORDS4[-1]] - 1,
            ),
        }
        retained = markings + ((slope,) if chart == "finite" else ())
        for name, equations in systems.items():
            eliminated = extensions + (
                (inverse0, inverse1) if name.startswith("shared") else (inverse0,)
            )
            output.append(eliminate(
                f"{name}_{chart}", equations, eliminated, retained,
                expected[(name, chart)],
            ))
    return output


def shared_branch(alpha, unmarked_beta, phi):
    t, cap_c, cap_d, cap_e = sp.symbols("t C D E")
    extensions = sp.symbols("x0:8")
    beta = shifted_beta(alpha, unmarked_beta, (0, 0, t, 0))
    d01 = model(alpha, beta, extensions, "D01", "finite", sp.Integer(1))
    d23 = model(alpha, beta, extensions, "D23", "finite", sp.Integer(1))
    combined = d01["mixed"].col_join(d23["mixed"])
    rows, columns = (2, 9, 10, 12, 15), (0, 1, 2, 3, 6)
    determinant = sp.factor(combined.extract(rows, columns).det())
    expected_determinant = -1024 * (phi - 1) ** 2 * (phi + 1) ** 2
    assert_zero(determinant - expected_determinant)
    assert combined.rank() == 5

    divisor = phi ** 2 - 1
    cap_s = cap_c + cap_e
    cap_g = divisor * cap_d + phi * t * cap_s
    extension = sp.Matrix((
        0,
        cap_s / divisor,
        -phi * cap_s / divisor,
        0,
        cap_c,
        cap_d,
        0,
        cap_e,
    ))
    assert_zero(combined * extension)
    kernel_basis = (
        sp.Matrix((0, 1 / divisor, -phi / divisor, 0, 1, 0, 0, 0)),
        sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0)),
        sp.Matrix((0, 1 / divisor, -phi / divisor, 0, 0, 0, 0, 1)),
    )
    assert sp.Matrix.hstack(*kernel_basis).rank() == 3
    for vector in kernel_basis:
        assert_zero(combined * vector)

    substitution = dict(zip(extensions, extension))
    diagonals = {
        "A01": sp.factor(d01["coefficients"][WORDS4[0]].subs(substitution)),
        "B01": sp.factor(d01["coefficients"][WORDS4[-1]].subs(substitution)),
        "A23": sp.factor(d23["coefficients"][WORDS4[0]].subs(substitution)),
        "B23": sp.factor(d23["coefficients"][WORDS4[-1]].subs(substitution)),
    }
    expected_diagonals = {
        "A01": sp.Integer(0),
        "B01": -4 * cap_g,
        "A23": 4 * phi * cap_s / divisor,
        "B23": 4 * cap_s,
    }
    for key, value in diagonals.items():
        assert_zero(value - expected_diagonals[key])

    mode0 = one_marked(d01, 0).subs(substitution)
    mode3 = one_marked(d01, 3).subs(substitution)
    rows0, rows3 = (1, 3, 5, 7), (4, 5, 6, 7)
    minor0 = sp.factor(mode0.extract(rows0, range(4)).det())
    minor3 = sp.factor(mode3.extract(rows3, range(4)).det())
    expected0 = -128 * cap_e * phi * cap_s * cap_g / divisor
    expected3 = -128 * cap_c * phi * cap_s * cap_g / divisor
    assert_zero(minor0 - expected0)
    assert_zero(minor3 - expected3)

    # On phi*(phi^2-1)*S*G != 0, simultaneous rank <=3 forces E=C=0,
    # contradicting S=C+E!=0.  This is the exact compatibility obstruction.
    return {
        "weight": "[lambda:1]=[1:1]",
        "marking": "h=(0,0,t,0)",
        "mixed_rank": 5,
        "rank_witness": {
            "rows": list(rows), "columns": list(columns),
            "determinant": str(determinant),
        },
        "complete_kernel_basis": [
            [str(sp.factor(value)) for value in vector] for vector in kernel_basis
        ],
        "extension_parameterization": [str(sp.factor(value)) for value in extension],
        "S": "C+E",
        "G": "(phi^2-1)*D+phi*t*(C+E)",
        "diagonals": {key: str(value) for key, value in diagonals.items()},
        "genuine_condition": "(C+E)*((phi^2-1)*D+phi*t*(C+E))!=0",
        "one_marked_obstruction": {
            "D01_mode0": {"rows": list(rows0), "determinant": str(minor0)},
            "D01_mode3": {"rows": list(rows3), "determinant": str(minor3)},
            "deduction": "rank<=3 in both modes forces E=C=0, contradicting C+E!=0",
        },
        "survivor_found": False,
    }


def main():
    phi = sp.Symbol("phi")
    planes, alpha, beta = divisor_basis(phi)
    markings = sp.symbols("h0:4")
    pure = coefficients(alpha, shifted_beta(alpha, beta, markings))
    support = {
        "".join(map(str, word)): str(sp.factor(value))
        for word, value in pure.items() if value != 0
    }
    assert support == {"1111": "-4*(phi - 1)*(phi + 1)"}
    pairs = pair_certificates(planes, phi)
    incidence = incidence_certificates(alpha, beta)
    branch = shared_branch(alpha, beta, phi)
    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "discovery_claim_label": "CANDIDATE",
        "scope": "component 19 finite ordinary divisor p=0, q*phi=1, phi^2!=1",
        "inputs": {path.name: sha256(path) for path in INPUTS},
        "method": "direct Q(phi) reconstruction, exact permanents and pair minors, complete finite/infinity incidence elimination, shared-kernel basis, and two fixed one-marked minors",
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
            CERTIFICATE.name: sha256(CERTIFICATE),
        },
        "regular_specialized_basis": {
            "field": "Q(phi)",
            "relation": "p=0, q=1/phi",
            "mode0_rescaling": "beta0 is multiplied by phi",
            "mode0_change_determinant": "phi",
            "alpha": [[str(value) for value in row] for row in alpha],
            "beta": [[str(value) for value in row] for row in beta],
        },
        "pure_support_after_all_affine_markings": support,
        "exact_ordinary_open": "phi*(phi^2-1)!=0; phi!=0 is automatic from q*phi=1",
        "pair_profile": [3, 3, 3, 3, 3, 3],
        "pair_certificates": pairs,
        "incidence_eliminations": incidence,
        "shared_branch": branch,
        "weighted_H22_fibre_empty": True,
        "survivor_found": False,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "generic_p0_specialization_used_as_proof": False,
        "limitations": [
            "Independently verified; construction discovery label remains CANDIDATE.",
            "The endpoints phi=+1 and phi=-1 lie on q=phi, where the ordinary tensor vanishes; they are separate zero fibres and are not covered.",
            "No claim is made about projective or valuative boundaries, component exhaustiveness, arbitrary-order reduction, or the global conjecture.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
