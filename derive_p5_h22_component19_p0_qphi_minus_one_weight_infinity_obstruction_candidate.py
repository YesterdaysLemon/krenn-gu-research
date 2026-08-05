#!/usr/bin/env python3
"""Direct exact q*phi=-1 homogeneous weight-infinity H22 obstruction."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_WEIGHT_INFINITY_OBSTRUCTION_CANDIDATE.md"
CERTIFICATE = ROOT / "p5_h22_component19_p0_qphi_minus_one_weight_infinity_certificate.json"
SOURCE = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
MIXED4 = WORDS4[1:-1]
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
    states = {0: sp.Integer(1)}
    for row in rows:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not (mask >> column) & 1:
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = {mask: sp.expand(value) for mask, value in following.items()}
    return sp.factor(states[(1 << len(rows)) - 1])


def assert_zero(value):
    if isinstance(value, sp.MatrixBase):
        assert all(sp.cancel(entry) == 0 for entry in value)
    else:
        assert sp.cancel(value) == 0


def divisor_rows(phi, markings):
    """Direct denominator-free q=-1/phi basis; beta0 is scaled by phi."""
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    alpha = (abar, cap_b, bbar, abar)
    unmarked_beta = (
        add(scale(phi, bbar), scale(-1, cap_b)),
        cap_a,
        cap_a,
        add(cap_b, scale(phi, bbar)),
    )
    beta = tuple(
        add(unmarked_beta[i], scale(markings[i], alpha[i])) for i in range(4)
    )
    return alpha, beta, unmarked_beta


def project_infinity(row, extension, direction):
    if direction == "D01":
        return (row[0], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def infinity_model(alpha, beta, extensions, direction):
    projected_alpha = tuple(
        project_infinity(alpha[i], extensions[i], direction) for i in range(4)
    )
    projected_beta = tuple(
        project_infinity(beta[i], extensions[4 + i], direction) for i in range(4)
    )
    coefficients = {
        word: permanent(tuple(
            projected_beta[i] if word[i] else projected_alpha[i]
            for i in range(4)
        ))
        for word in WORDS4
    }
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], extension) for extension in extensions]
        for word in MIXED4
    ])
    return {"coefficients": coefficients, "mixed": mixed}


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def eliminate(label, equations, eliminated, retained, coefficient_ring, expected):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=" + coefficient_ring + ",(" + ",".join(map(str, variables))
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
    markers = [line for line in completed.stdout.splitlines() if line.startswith("CODEX_RESULT:")]
    assert completed.returncode == 0 and not completed.stderr.strip(), (label, completed.stdout, completed.stderr)
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (label, completed.stdout)
    return {
        "label": label,
        "coefficient_ring": coefficient_ring,
        "projected_ideal": [str(sp.factor(value)) for value in expected],
        "bidirectional_ideal_equality": True,
    }


def incidence_systems(phi, markings, extensions, d01, d23):
    inverse0, inverse1 = sp.symbols("u v")
    common = tuple(d01["mixed"] * sp.Matrix(extensions)) + tuple(d23["mixed"] * sp.Matrix(extensions))
    systems = {
        "D01_binary": (
            (*tuple(d01["mixed"] * sp.Matrix(extensions)), d01["coefficients"][WORDS4[0]] - 1, inverse0 * d01["coefficients"][WORDS4[-1]] - 1),
            extensions + (inverse0,), (sp.Integer(1),),
        ),
        "D23_binary": (
            (*tuple(d23["mixed"] * sp.Matrix(extensions)), d23["coefficients"][WORDS4[0]] - 1, inverse0 * d23["coefficients"][WORDS4[-1]] - 1),
            extensions + (inverse0,), (markings[3], markings[0], markings[1] * markings[2]),
        ),
        "shared_A01": (
            (*common, d01["coefficients"][WORDS4[0]] - 1, inverse0 * d01["coefficients"][WORDS4[-1]] - 1, inverse1 * d23["coefficients"][WORDS4[-1]] - 1),
            extensions + (inverse0, inverse1), (sp.Integer(1),),
        ),
        "shared_A23": (
            (*common, d23["coefficients"][WORDS4[0]] - 1, inverse0 * d01["coefficients"][WORDS4[-1]] - 1, inverse1 * d23["coefficients"][WORDS4[-1]] - 1),
            extensions + (inverse0, inverse1), (sp.Integer(1),),
        ),
    }
    return systems


def function_field_elimination(phi, markings, extensions, d01, d23):
    output = []
    for name, (equations, eliminated, expected) in incidence_systems(
        phi, markings, extensions, d01, d23
    ).items():
        output.append(eliminate(
            f"{name}_over_Q(phi)", equations, eliminated, markings,
            "(0,phi)", expected,
        ))
    return output


def parameter_aware_elimination(phi, markings, extensions, d01, d23):
    open_inverse = sp.Symbol("o")
    open_equation = open_inverse * phi * (phi ** 2 + 1) - 1
    output = []
    systems = incidence_systems(phi, markings, extensions, d01, d23)
    # The structural syzygy already settles both shared orientations.  Retain
    # only the two directly relevant saturated eliminations as an audit; the
    # individual binary projections were classified over Q(phi) above.
    for name in ("shared_A01", "shared_A23"):
        equations, eliminated, expected = systems[name]
        output.append(eliminate(
            f"{name}_over_Q[phi]_on_open",
            (*equations, open_equation), eliminated + (open_inverse,),
            (phi,) + markings, "0", expected,
        ))
    return output


def pure_and_pairs(phi):
    markings = sp.symbols("m0:4")
    alpha, beta, unmarked_beta = divisor_rows(phi, markings)
    support = {
        "".join(map(str, word)): str(permanent(tuple(
            beta[i] if word[i] else alpha[i] for i in range(4)
        )))
        for word in WORDS4
        if permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4))) != 0
    }
    assert support == {"1111": "-4*(phi**2 + 1)"}

    def squarefree(left, right):
        return sp.Matrix([
            sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS
        ])

    planes = tuple((alpha[i], unmarked_beta[i]) for i in range(4))
    witnesses = {
        "01": ((1, 2, 5), (0, 2, 3), -4 * phi),
        "02": ((1, 2, 5), (0, 2, 3), -4 * phi),
        "03": ((0, 1, 2, 5), (0, 1, 2, 3), -16 * phi * (phi ** 2 + 1)),
        "12": ((0, 1, 2), (1, 2, 3), -4),
        "13": ((1, 2, 5), (0, 1, 3), 4 * phi),
        "23": ((1, 2, 5), (0, 1, 3), 4 * phi),
    }
    output = {}
    for i, j in PAIRS:
        label = f"{i}{j}"
        matrix = sp.Matrix.hstack(*(
            squarefree(planes[i][a], planes[j][b]) for a in range(2) for b in range(2)
        ))
        rows, columns, expected = witnesses[label]
        determinant = sp.factor(matrix.extract(rows, columns).det())
        assert_zero(determinant - expected)
        rank = matrix.rank()
        assert rank == (4 if label == "03" else 3)
        output[label] = {
            "rank": rank,
            "rows": list(rows), "columns": list(columns),
            "determinant": str(determinant),
        }
    return support, output


def main():
    phi = sp.Symbol("phi")
    markings = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    alpha, beta, _ = divisor_rows(phi, markings)
    d01 = infinity_model(alpha, beta, extensions, "D01")
    d23 = infinity_model(alpha, beta, extensions, "D23")

    # Compact structural contradiction, valid before any elimination.
    structural = {
        "A01": sp.factor(d01["coefficients"][WORDS4[0]]),
        "A23": sp.factor(d23["coefficients"][WORDS4[0]]),
        "D01_0001": sp.factor(d01["coefficients"][(0, 0, 0, 1)]),
        "D01_1000": sp.factor(d01["coefficients"][(1, 0, 0, 0)]),
    }
    expected = {
        "A01": sp.Integer(0),
        "A23": -2 * (extensions[1] + extensions[2]),
        "D01_0001": -2 * (phi * extensions[1] - extensions[2]),
        "D01_1000": -2 * (phi * extensions[1] + extensions[2]),
    }
    for key, value in expected.items():
        assert_zero(structural[key] - value)
    # On phi!=0, the two mixed equations force x1=x2=0 and hence A23=0.
    structural_syzygies = {
        "phi_x1": sp.factor(-(structural["D01_0001"] + structural["D01_1000"]) / 4),
        "x2": sp.factor((structural["D01_0001"] - structural["D01_1000"]) / 4),
        "A23_from_D01_mixed": sp.factor(
            (1 - phi) * structural["D01_0001"] / (2 * phi)
            + (1 + phi) * structural["D01_1000"] / (2 * phi)
        ),
    }
    assert_zero(structural_syzygies["phi_x1"] - phi * extensions[1])
    assert_zero(structural_syzygies["x2"] - extensions[2])
    assert_zero(structural_syzygies["A23_from_D01_mixed"] - structural["A23"])
    crossing_checks = {
        "phi=1": sp.factor(
            structural["A23"].subs(phi, 1)
            - structural["D01_1000"].subs(phi, 1)
        ),
        "phi=-1": sp.factor(
            structural["A23"].subs(phi, -1)
            + structural["D01_0001"].subs(phi, -1)
        ),
    }
    for value in crossing_checks.values():
        assert_zero(value)

    support, pairs = pure_and_pairs(phi)
    result = {
        "status": "pass", "role": "construction", "claim_label": "CANDIDATE",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "scope": "component 19 p=0, q*phi=-1 homogeneous weight-at-infinity chart on phi*(phi^2+1)!=0",
        "inputs": {SOURCE.name: sha256(SOURCE)},
        "method": "direct denominator-free divisor basis, compact coefficient syzygy, bounded function-field incidence classification, saturated shared-incidence audit, and direct phi=+/-1 substitutions",
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT), CERTIFICATE.name: sha256(CERTIFICATE)},
        "relation": "p=0, q=-1/phi",
        "exact_ordinary_open": "phi*(phi^2+1)!=0",
        "weight_chart": {
            "homogeneous_weight": "[1:0]",
            "D01_contraction_row": [0, 1, 0, 0, 0],
            "D23_contraction_row": [0, 0, 0, 1, 0],
        },
        "regular_basis": {
            "mode0_rescaling_determinant": "phi",
            "pure_support_after_all_markings": support,
            "pair_profile": [3, 3, 4, 3, 3, 3],
            "pair_witnesses": pairs,
        },
        "structural_contradiction": {
            "coefficients": {key: str(value) for key, value in structural.items()},
            "syzygies": {key: str(value) for key, value in structural_syzygies.items()},
            "exact_identity": "A23=((1-phi)/(2*phi))*D01_0001+((1+phi)/(2*phi))*D01_1000",
            "deduction": "A01=0 identically, while A23 lies in the D01 mixed ideal on phi!=0; therefore neither shared binary orientation exists",
        },
        "function_field_eliminations": function_field_elimination(phi, markings, extensions, d01, d23),
        "parameter_aware_eliminations": parameter_aware_elimination(phi, markings, extensions, d01, d23),
        "direct_crossing_checks": {
            "phi=1": "A23=D01_1000",
            "phi=-1": "A23=-D01_0001",
            "symbolic_residuals": {key: str(value) for key, value in crossing_checks.items()},
        },
        "complete_genuine_shared_incidence": "empty",
        "actual_target_compatibility": "empty because no shared binary extension exists",
        "weighted_H22_fibre_empty_candidate": True,
        "finite_field_computation_used": False,
        "generic_specialization_used_as_proof": False,
        "broad_brute_force_used": False,
        "limitations": [
            "Construction result remains CANDIDATE pending independent verification.",
            "Only the homogeneous weight-at-infinity chart on q*phi=-1 is covered; the finite chart is not reused as proof.",
            "The zero-tensor points phi^2=-1, other component boundaries, arbitrary-order reduction, and the global conjecture are excluded.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
