#!/usr/bin/env python3
"""No-import normal-cone and weighted-H22 audit at component-19 Z0."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import tempfile
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
REPORT = ROOT / "P5_H22_COMPONENT19_Q_EQ_PHI_FIRST_NORMAL_NO_IMPORT_VERIFICATION.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
TRIPLETS = (
    ("A01", "B01", "A23"),
    ("A01", "B01", "B23"),
    ("A23", "B23", "A01"),
    ("A23", "B23", "B01"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def add(left, right):
    return tuple(sp.expand(left[index] + right[index]) for index in range(len(left)))


def scale(value, row):
    return tuple(sp.expand(value * entry) for entry in row)


def permanent(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if not mask & bit:
                    new_mask = mask | bit
                    next_states[new_mask] = next_states.get(new_mask, 0) + coefficient * entry
        states = {mask: sp.expand(value) for mask, value in next_states.items()}
    return sp.factor(states.get((1 << len(rows)) - 1, 0))


p, q, phi = sp.symbols("p q phi")
t, a, b, n, lam = sp.symbols("t a b n lambda")
h = sp.symbols("h0:4")
x = sp.symbols("x0:4")
y = sp.symbols("y0:4")
extensions = x + y
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)


def component_rows(p_value, q_value):
    alpha = (
        add(Abar, scale(p_value, B)),
        B,
        Bbar,
        Abar,
    )
    beta = (
        add(Bbar, scale(q_value, B)),
        A,
        A,
        add(B, scale(phi, Bbar)),
    )
    return alpha, beta


def tensor_coefficients(alpha, beta):
    return {
        word: permanent(tuple(beta[index] if word[index] else alpha[index] for index in range(4)))
        for word in WORDS
    }


def audit_normal_cone():
    alpha, beta = component_rows(p, q)
    tensor = tensor_coefficients(alpha, beta)
    support = {word: sp.factor(value) for word, value in tensor.items() if value != 0}
    assert set(support) == {(0, 1, 1, 1), (1, 1, 1, 1)}
    assert sp.expand(support[(0, 1, 1, 1)] - 4 * p) == 0
    assert sp.expand(support[(1, 1, 1, 1)] - 4 * (q - phi)) == 0

    ideal_generators = (sp.factor(support[(0, 1, 1, 1)] / 4), sp.factor(support[(1, 1, 1, 1)] / 4))
    assert sp.expand(ideal_generators[0] - p) == 0
    assert sp.expand(ideal_generators[1] - (q - phi)) == 0
    jacobian = sp.Matrix(ideal_generators).jacobian((p, q, phi))
    assert jacobian == sp.Matrix(((1, 0, 0), (0, 1, -1)))
    assert jacobian[:, :2].det() == 1
    assert all(value.subs({p: 0, q: phi}) == 0 for value in tensor.values())

    arc_tensor = {
        word: sp.factor(value.subs({p: a * t, q: phi + b * t}) / t)
        for word, value in tensor.items()
    }
    arc_support = {word: value for word, value in arc_tensor.items() if value != 0}
    assert set(arc_support) == {(0, 1, 1, 1), (1, 1, 1, 1)}
    assert sp.expand(arc_support[(0, 1, 1, 1)] - 4 * a) == 0
    assert sp.expand(arc_support[(1, 1, 1, 1)] - 4 * b) == 0

    # The two standard charts [a:b]=[n:1] and [a:b]=[1:n].
    assert tuple(sp.expand(n * value) for value in (1, 1 / n)) == (n, 1)
    old_alpha, old_beta = component_rows(0, phi)
    b_beta0 = add(old_beta[0], scale(n, old_alpha[0]))
    assert b_beta0 == add(scale(n, old_alpha[0]), old_beta[0])
    a_beta0 = add(old_alpha[0], scale(n, old_beta[0]))
    assert a_beta0 == add(old_alpha[0], scale(n, old_beta[0]))
    assert sp.Matrix(((1, 0), (n, 1))).det() == 1
    assert sp.Matrix(((0, 1), (1, n))).det() == -1

    return {
        "tensor_support": {"0111": "4*p", "1111": "4*(q-phi)"},
        "zero_ideal": ["p", "q-phi"],
        "jacobian": [[1, 0, 0], [0, 1, -1]],
        "normal_rank": 2,
        "projectivized_normal": "P1 with charts [n:1] and [1:n]",
        "first_normal_support": {"0111": "4*a", "1111": "4*b"},
    }


def normal_rows(chart):
    """Rows on the exceptional divisor after ray normalization and s=0."""
    old_alpha, old_beta = component_rows(0, phi)
    alpha = list(old_alpha)
    beta = list(old_beta)
    if chart == "b":
        # p=n*s, q=phi+s; beta0' = beta0+n*alpha0.
        beta[0] = add(beta[0], scale(n, alpha[0]))
    elif chart == "a":
        # p=s, q=phi+n*s; alpha0'=beta0, beta0'=alpha0+n*beta0.
        old_alpha0, old_beta0 = alpha[0], beta[0]
        alpha[0] = old_beta0
        beta[0] = add(old_alpha0, scale(n, old_beta0))
    else:
        raise ValueError(chart)
    beta = [add(beta[index], scale(h[index], alpha[index])) for index in range(4)]
    return tuple(alpha), tuple(beta)


def project(row, extension, direction, weight):
    row5 = tuple(row) + (extension,)
    if direction == "01":
        if weight == "finite":
            return (lam * row5[0] + row5[1], row5[2], row5[3], row5[4])
        return (row5[0], row5[2], row5[3], row5[4])
    if direction == "23":
        if weight == "finite":
            return (row5[0], row5[1], lam * row5[2] + row5[3], row5[4])
        return (row5[0], row5[1], row5[2], row5[4])
    raise ValueError(direction)


def contraction_coefficients(chart, weight, direction):
    alpha, beta = normal_rows(chart)
    alpha4 = tuple(project(alpha[index], x[index], direction, weight) for index in range(4))
    beta4 = tuple(project(beta[index], y[index], direction, weight) for index in range(4))
    values = {
        word: permanent(tuple(beta4[index] if word[index] else alpha4[index] for index in range(4)))
        for word in WORDS
    }
    mixed = tuple(values[word] for word in WORDS[1:-1])
    return mixed, values[WORDS[0]], values[WORDS[-1]]


def assert_extension_homogeneity(expressions):
    scale_symbol = sp.symbols("extension_scale")
    substitution = {value: scale_symbol * value for value in extensions}
    for expression in expressions:
        assert sp.expand(expression.subs(substitution) - scale_symbol * expression) == 0


def singular_expression(expression):
    numerator, denominator = sp.fraction(sp.cancel(expression))
    assert denominator == 1
    return sp.sstr(sp.expand(numerator)).replace("**", "^").replace("lambda", "la")


def wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    tail = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{tail}"


def singular_source(chart, weight, triplet):
    mixed01, a01, b01 = contraction_coefficients(chart, weight, "01")
    mixed23, a23, b23 = contraction_coefficients(chart, weight, "23")
    diagonals = {"A01": a01, "B01": b01, "A23": a23, "B23": b23}
    chosen = tuple(diagonals[name] for name in triplet)
    assert_extension_homogeneity((*mixed01, *mixed23, *chosen))

    u, v, w = sp.symbols("u v w")
    equations = (
        *mixed01,
        *mixed23,
        chosen[0] - 1,
        u * chosen[1] - 1,
        v * chosen[2] - 1,
        w * phi - 1,
    )
    generators = ",\n".join(singular_expression(value) for value in equations if value != 0)
    variables = [*[str(value) for value in extensions], "u", "v", "w", *[str(value) for value in h], "n"]
    if weight == "finite":
        variables.append("la")
    variables.append("phi")
    trailing = 7 if weight == "finite" else 6
    label = f"{chart}_{weight}_{'_'.join(triplet)}"
    source = f"""
option(redSB);
ring R=0,({','.join(variables)}),(dp(11),dp({trailing}));
ideal I={generators};
ideal J=std(eliminate(std(I),x0*x1*x2*x3*y0*y1*y2*y3*u*v*w));
print(\"RESULT {label}\"); J;
quit;
"""
    return label, source


def run_singular(path: Path, label: str):
    completed = subprocess.run(
        ("wsl.exe", "-e", "Singular", wsl_path(path)),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=240,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"Singular failed for {label}: {completed.stderr}")
    marker = f"RESULT {label}"
    assert marker in completed.stdout
    after = completed.stdout.split(marker, 1)[1]
    assert "J[1]=1" in after and "J[2]=" not in after, completed.stdout
    return completed.stdout


def audit_h22_incidence():
    certificates = []
    with tempfile.TemporaryDirectory(prefix="component19-first-normal-") as temporary:
        temp_root = Path(temporary)
        for chart in ("b", "a"):
            for weight in ("finite", "infinity"):
                for triplet in TRIPLETS:
                    label, source = singular_source(chart, weight, triplet)
                    path = temp_root / f"{label}.sing"
                    path.write_text(source, encoding="utf-8")
                    stdout = run_singular(path, label)
                    certificates.append(
                        {
                            "case": label,
                            "source_sha256": text_sha256(source),
                            "stdout_sha256": text_sha256(stdout),
                            "projected_ideal": ["1"],
                        }
                    )
    assert len(certificates) == 16
    return certificates


def main():
    component_text = COMPONENT.read_text(encoding="utf-8")
    assert "T_0111=4p" in component_text
    assert "T_1111=4(q-phi)" in component_text
    assert "phi!=0" in component_text

    normal = audit_normal_cone()
    certificates = audit_h22_incidence()
    payload = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "component-19 Z0={p=0,q=phi}, phi!=0: smooth normal cone, its "
            "projectivized first-normal P1, and empty necessary shared weighted-H22 "
            "incidence on every first-normal and weight direction"
        ),
        "inputs": {COMPONENT.name: sha256(COMPONENT)},
        "method": (
            "fresh squarefree permanents; Jacobian/regular-sequence normal geometry; "
            "two normalized normal-ray charts; exact characteristic-zero Singular "
            "elimination over Q[phi] saturated only by phi, retaining normal slope, "
            "Borel markings, and finite weight"
        ),
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
        "normal_cone": normal,
        "h22_cases": certificates,
        "h22_case_count": len(certificates),
        "genuine_shared_first_normal_incidence": "empty",
        "phi_nonzero_specializations_included": True,
        "finite_and_infinity_weight_charts_included": True,
        "all_affine_borel_markings_retained": True,
        "construction_or_proof_b_artifacts_read_or_imported": False,
        "discarded_false_start": (
            "An exploratory run incorrectly kept the transverse ray parameter s "
            "invertible and therefore audited punctured rays. Its outputs are not used; "
            "the certified 16 cases normalize the ray bases first and then set s=0."
        ),
        "formal_arc_status": "UNKNOWN",
        "first_normal_only_not_all_formal_arcs": True,
        "limitations": (
            "This is an associated-graded/projectivized first-normal calculation. "
            "Although every non-base formal arc has a leading normal direction because "
            "the tensor coordinates are exactly 4p and 4(q-phi), higher/tangent arc "
            "coefficients and t-dependent extension/marking rescalings can affect the "
            "limiting P5 data. No Rees-saturation, properness, or valuative lifting "
            "theorem proving higher terms irrelevant is supplied. No all-formal-arc, "
            "arbitrary-order local-to-global, or global conjecture claim."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
