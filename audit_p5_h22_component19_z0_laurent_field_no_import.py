#!/usr/bin/env python3
"""Independent Laurent-field weighted-H22 audit near component-19 Z0."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_Z0_LAURENT_FIELD_NO_IMPORT_VERIFICATION.md"
COMPONENT = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
P0_SCRIPT = ROOT / "audit_p5_h22_component19_p0_finite_ordinary_aggregate.py"
P0_REPORT = ROOT / "P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
TRIPLETS = (
    ("A01", "B01", "A23"),
    ("A01", "B01", "B23"),
    ("A23", "B23", "A01"),
    ("A23", "B23", "B01"),
)

p, q, phi, r, s, lam = sp.symbols("p q phi r s lambda")
h = sp.symbols("h0:4")
x = sp.symbols("x0:4")
y = sp.symbols("y0:4")
extensions = x + y
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)


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


def rows(p_value, q_value, phi_value):
    alpha = (
        add(Abar, scale(p_value, B)),
        B,
        Bbar,
        Abar,
    )
    unmarked_beta = (
        add(Bbar, scale(q_value, B)),
        A,
        A,
        add(B, scale(phi_value, Bbar)),
    )
    beta = tuple(add(unmarked_beta[index], scale(h[index], alpha[index])) for index in range(4))
    return alpha, beta


def project(row, extension, direction, weight):
    row5 = tuple(row) + (extension,)
    if direction == "01":
        if weight == "finite":
            return (lam * row5[0] + row5[1], row5[2], row5[3], row5[4])
        return (row5[0], row5[2], row5[3], row5[4])
    if weight == "finite":
        return (row5[0], row5[1], lam * row5[2] + row5[3], row5[4])
    return (row5[0], row5[1], row5[2], row5[4])


def coefficients(p_value, q_value, phi_value, direction, weight):
    alpha, beta = rows(p_value, q_value, phi_value)
    alpha4 = tuple(project(alpha[index], x[index], direction, weight) for index in range(4))
    beta4 = tuple(project(beta[index], y[index], direction, weight) for index in range(4))
    values = {
        word: permanent(tuple(beta4[index] if word[index] else alpha4[index] for index in range(4)))
        for word in WORDS
    }
    return tuple(values[word] for word in WORDS[1:-1]), values[WORDS[0]], values[WORDS[-1]]


def singular_expression(expression):
    numerator, denominator = sp.fraction(sp.cancel(expression))
    assert denominator.free_symbols <= {phi}
    return sp.sstr(sp.expand(numerator)).replace("**", "^").replace("lambda", "la")


def wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    tail = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{tail}"


def parameter_case_sources(name, p_value, q_value, phi_value, retained, saturation, expectations):
    records = []
    for weight in ("finite", "infinity"):
        mixed01, a01, b01 = coefficients(p_value, q_value, phi_value, "01", weight)
        mixed23, a23, b23 = coefficients(p_value, q_value, phi_value, "23", weight)
        diagonals = {"A01": a01, "B01": b01, "A23": a23, "B23": b23}
        for triplet in TRIPLETS:
            u, v, w = sp.symbols("u v w")
            chosen = tuple(diagonals[key] for key in triplet)
            equations = (
                *mixed01,
                *mixed23,
                chosen[0] - 1,
                u * chosen[1] - 1,
                v * chosen[2] - 1,
                w * saturation - 1,
            )
            generators = ",\n".join(singular_expression(value) for value in equations if value != 0)
            eliminated = [*[str(value) for value in extensions], "u", "v", "w"]
            kept = [*[str(value) for value in h]]
            if weight == "finite":
                kept.append("la")
            kept.extend(str(value) for value in retained)
            label = f"{name}_{weight}_{'_'.join(triplet)}"
            expected = expectations.get((weight, triplet), ("1",))
            expected_text = ",".join(expected)
            source = f"""
option(redSB);
ring R=0,({','.join(eliminated + kept)}),(dp(11),dp({len(kept)}));
ideal I={generators};
ideal J=std(eliminate(std(I),x0*x1*x2*x3*y0*y1*y2*y3*u*v*w));
ideal E=std(ideal({expected_text}));
ideal Acheck=reduce(J,E); ideal Bcheck=reduce(E,J);
if (size(Acheck)==0 && size(Bcheck)==0) {{ print("AUDIT_OK {label}"); J; }}
else {{ print("AUDIT_FAIL {label}"); J; Acheck; Bcheck; }}
quit;
"""
            records.append((label, source, list(expected)))
    return records


def run_parameter_cases():
    qeqphi_expected = {
        ("finite", ("A23", "B23", "A01")): (
            "la+1", "h3", "h2", "h1", "h0", "phi^2-1"
        )
    }
    qphi1_expected = {
        ("finite", ("A23", "B23", "A01")): ("la+1", "h3", "h2", "h1", "h0")
    }
    cases = []
    cases.extend(parameter_case_sources("qeqphi", p, phi, phi, (p, phi), p * phi, qeqphi_expected))
    cases.extend(
        parameter_case_sources(
            "qphi1", p, 1 / phi, phi, (p, phi), p * phi * (phi**2 - 1), qphi1_expected
        )
    )
    cases.extend(parameter_case_sources("phi_plus", p, 1 + r, 1, (p, r), p * r * (1 + r), {}))
    cases.extend(parameter_case_sources("phi_minus", p, -1 + r, -1, (p, r), p * r * (-1 + r), {}))
    cases.extend(
        parameter_case_sources(
            "generic_away_reverse",
            p,
            q,
            phi,
            (p, q, phi),
            p * (q - phi) * phi * (phi**2 - 1) * (q * phi - 1),
            {},
        )
    )
    assert len(cases) == 40

    certificates = []
    with tempfile.TemporaryDirectory(prefix="component19-laurent-") as temporary:
        temp_root = Path(temporary)
        for label, source, expected in cases:
            path = temp_root / f"{label}.sing"
            path.write_text(source, encoding="utf-8")
            completed = subprocess.run(
                ("wsl.exe", "-e", "Singular", wsl_path(path)),
                cwd=ROOT,
                text=True,
                encoding="utf-8",
                capture_output=True,
                timeout=120,
                check=False,
            )
            assert completed.returncode == 0, (label, completed.stderr)
            assert f"AUDIT_OK {label}" in completed.stdout, completed.stdout
            certificates.append(
                {
                    "case": label,
                    "expected_projected_ideal": expected,
                    "source_sha256": text_sha256(source),
                    "stdout_sha256": text_sha256(completed.stdout),
                }
            )
    return certificates


def projected_one_marked(alpha4, beta4, mode):
    other = tuple(index for index in range(4) if index != mode)
    output = []
    for word in itertools.product((0, 1), repeat=3):
        selected = {index: beta4[index] if word[position] else alpha4[index] for position, index in enumerate(other)}
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(permanent(tuple(basis if index == mode else selected[index] for index in range(4))))
        output.append(row)
    return sp.Matrix(output)


def complementary_permanent(rows3, omitted_column):
    retained = tuple(column for column in range(len(rows3) + 1) if column != omitted_column)
    return permanent(tuple(tuple(row[column] for column in retained) for row in rows3))


def full_one_marked(alpha5, beta5, mode, contraction):
    other = tuple(index for index in range(4) if index != mode)
    output = []
    for word in itertools.product((0, 1), repeat=3):
        selected = tuple(beta5[index] if word[position] else alpha5[index] for position, index in enumerate(other))
        selected += (contraction,)
        output.append(tuple(complementary_permanent(selected, column) for column in range(5)))
    return sp.Matrix(output)


def reverse_branch_compatibility():
    mixed01, a01, b01 = coefficients(p, 1 / phi, phi, "01", "finite")
    mixed23, a23, b23 = coefficients(p, 1 / phi, phi, "23", "finite")
    branch = {lam: -1, **{value: 0 for value in h}}
    mixed = tuple(value.subs(branch) for value in (*mixed01, *mixed23))
    matrix = sp.Matrix([[sp.expand(value).coeff(variable) for variable in extensions] for value in mixed])
    rows5 = (0, 1, 4, 20, 27)
    cols5 = (0, 1, 3, 5, 6)
    assert sp.factor(matrix.extract(rows5, cols5).det()) == -1024 * p * phi**3

    v0 = sp.Matrix((0, 1 / phi, 1, 0, 0, 0, 0, 0))
    v1 = sp.Matrix((0, 0, 0, 0, 1, 0, 0, 0))
    v2 = sp.Matrix((0, 0, 0, 0, 0, 0, 0, 1))
    for vector in (v0, v1, v2):
        assert all(sp.cancel(value) == 0 for value in matrix * vector)

    cap_x, cap_y, cap_z = sp.symbols("X Y Z")
    extension = cap_x * v0 + cap_y * v1 + cap_z * v2
    substitution = dict(zip(extensions, extension))
    diagonals = tuple(sp.factor(value.subs(branch).subs(substitution)) for value in (a01, b01, a23, b23))
    expected_diagonals = (-4 * cap_x * p, 0, 4 * cap_x / phi, -4 * (cap_y * phi + cap_z))
    assert all(sp.cancel(actual - expected) == 0 for actual, expected in zip(diagonals, expected_diagonals))

    alpha, beta = rows(p, 1 / phi, phi)
    alpha4 = tuple(project(alpha[index], x[index], "01", "finite") for index in range(4))
    beta4 = tuple(project(beta[index], y[index], "01", "finite") for index in range(4))
    mode1 = projected_one_marked(alpha4, beta4, 1).subs(branch).subs(substitution)
    mode2 = projected_one_marked(alpha4, beta4, 2).subs(branch).subs(substitution)
    determinant1 = sp.factor(mode1.extract((0, 1, 4, 5), range(4)).det())
    determinant2 = sp.factor(mode2.extract((0, 1, 4, 5), range(4)).det())
    cap_d = cap_y * phi - cap_z
    cap_k = cap_y * phi + cap_z
    expected1 = -64 * cap_x * p * cap_d * (cap_x * (phi**2 - 1) + phi * cap_k) / phi
    expected2 = 64 * cap_x * p * cap_d * (cap_x * (phi**2 - 1) - phi * cap_k) / phi**3
    assert sp.cancel(determinant1 - expected1) == 0
    assert sp.cancel(determinant2 - expected2) == 0

    alpha5 = tuple(tuple(alpha[index]) + (x[index],) for index in range(4))
    beta5 = tuple(tuple(beta[index]) + (y[index],) for index in range(4))
    stack = full_one_marked(alpha5, beta5, 1, (-1, 1, 0, 0, 0)).col_join(
        full_one_marked(alpha5, beta5, 1, (0, 0, -1, 1, 0))
    )
    stack = stack.subs(branch).subs(substitution).subs(cap_z, cap_y * phi)
    stacked_determinant = sp.factor(stack.extract((0, 1, 4, 8, 15), range(5)).det())
    assert sp.cancel(stacked_determinant + 512 * cap_x**2 * cap_y**2 * p**2 * phi) == 0
    return {
        "mixed_rank_witness": "-1024*p*phi^3",
        "diagonals_A01_B01_A23_B23": [str(value) for value in diagonals],
        "genuine_open": "X*(phi*Y+Z)*p*phi!=0",
        "off_collision_individual_minors": [str(determinant1), str(determinant2)],
        "collision": "phi*Y-Z=0",
        "collision_stacked_minor": str(stacked_determinant),
        "verdict": "target-local compatibility empty",
    }


def pole_escape_profile():
    alpha, beta = rows(0, phi + s, phi)
    branch = {lam: 1, **{value: 0 for value in h}}
    mixed01, a01, b01 = coefficients(0, phi + s, phi, "01", "finite")
    mixed23, a23, b23 = coefficients(0, phi + s, phi, "23", "finite")
    mixed = tuple(value.subs(branch) for value in (*mixed01, *mixed23))
    extension = sp.Matrix((0, -1 / s, phi / s, 0, 1, 1, 0, 0))
    substitution = dict(zip(extensions, extension))
    assert all(sp.cancel(value.subs(substitution)) == 0 for value in mixed)
    diagonals = tuple(sp.factor(value.subs(branch).subs(substitution)) for value in (a01, b01, a23, b23))
    expected_diagonals = (0, 4 * s, -4 * phi / s, 4)
    assert all(sp.cancel(actual - expected) == 0 for actual, expected in zip(diagonals, expected_diagonals))

    alpha4 = tuple(project(alpha[index], x[index], "01", "finite") for index in range(4))
    beta4 = tuple(project(beta[index], y[index], "01", "finite") for index in range(4))
    marked3 = projected_one_marked(alpha4, beta4, 3).subs(branch).subs(substitution)
    target_minor = sp.factor(marked3.extract((4, 5, 6, 7), range(4)).det())
    expected = -64 * ((phi + s) ** 2 - 1) * (phi * (phi + s) + 1) / s
    assert sp.cancel(target_minor - expected) == 0
    return {
        "arc": "p=0, q=phi+s, lambda=1, h=(0,0,0,0)",
        "extension": [str(value) for value in extension],
        "generic_diagonals_A01_B01_A23_B23": [str(value) for value in diagonals],
        "generic_diagonal_valuations": ["infinity", 1, -1, 0],
        "projective_scaling": "multiply all extension coordinates by s",
        "scaled_extension_limit": [0, -1, "phi", 0, 0, 0, 0, 0],
        "scaled_diagonals": [0, "4*s^2", "-4*phi", "4*s"],
        "scaled_diagonal_valuations": ["infinity", 2, 0, 1],
        "next_orders_needed_for_genuine_triple": {"B23": 1, "B01": 2},
        "target_local_minor": str(target_minor),
        "binary_incidence_escape_real": True,
        "full_weighted_H22_arc": False,
    }


def replay_p0_aggregate():
    completed = subprocess.run(
        ("uv", "run", "--with", "sympy", "python", P0_SCRIPT.name),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=180,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["status"] == "pass"
    assert payload["claim_label"] == "VERIFIED"
    assert payload["finite_ordinary_divisor_exhausted"] is True
    assert payload["ordinary_projective_weight_fibre_exhausted"] is True
    assert payload["remaining_unknown_inside_scope"] is None
    return {
        "script_sha256": sha256(P0_SCRIPT),
        "report_sha256": sha256(P0_REPORT),
        "stdout_sha256": text_sha256(completed.stdout),
        "status": "VERIFIED complete on p=0,q*phi*(q-phi)!=0",
    }


def main():
    component_text = COMPONENT.read_text(encoding="utf-8")
    assert "T_0111=4p" in component_text
    assert "T_1111=4(q-phi)" in component_text
    p0 = replay_p0_aggregate()
    parameter_cases = run_parameter_cases()
    reverse = reverse_branch_compatibility()
    pole = pole_escape_profile()
    payload = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "all characteristic-zero formal arcs centered on component-19 "
            "Z0={p=0,q=phi}, phi!=0, whose generic restriction is nonzero and "
            "all-pair-open inside the displayed affine component chart"
        ),
        "inputs": {
            COMPONENT.name: sha256(COMPONENT),
            P0_SCRIPT.name: sha256(P0_SCRIPT),
            P0_REPORT.name: sha256(P0_REPORT),
        },
        "method": (
            "direct Laurent-field zero/nonzero partition; live p0 aggregate replay; "
            "40 parameter-aware exact saturated Singular projections; direct reverse-"
            "branch individual and stacked compatibility minors; exact 1/s escape audit"
        ),
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
        "p0_aggregate": p0,
        "parameter_case_count": len(parameter_cases),
        "parameter_cases": parameter_cases,
        "reverse_qphi_one_branch": reverse,
        "necessary_incidence_pole_escape": pole,
        "field_partition": [
            "p=0,r!=0: verified ordinary p0 aggregate (q and phi are units)",
            "p!=0,r=0,phi^2!=1: necessary incidence empty",
            "p!=0,r=0,phi^2=1: reverse branch compatibility-obstructed",
            "p*r!=0,phi^2=1: necessary incidence empty",
            "p*r!=0,phi^2!=1,q*phi!=1: necessary incidence empty",
            "p*r!=0,phi^2!=1,q*phi=1: reverse branch compatibility-obstructed",
        ],
        "formal_arc_weighted_H22_fibre": "empty",
        "properness": {
            "genuine_binary_incidence_morphism": "not proper; exact 1/s arc fails the valuative criterion",
            "full_target_compatible_H22_morphism_in_scope": "empty, hence proper",
            "proof_route": "field-valued exhaustion, not first-normal properness",
        },
        "projective_chart_ledger": {
            "normal_direction": "P1, two standard charts",
            "weight": "P1, finite and infinity charts",
            "markings_if_compactified": "(P1)^4, two charts per factor",
            "plane_lifts_if_compactified": "(P2)^4 via Gr(2,U_i plus vertical line), three charts per factor",
            "genuine_diagonal_open": "four triple opens",
            "maximal_diagonal_boundary_strata": [
                "A01=B01=0", "A23=B23=0", "A01=A23=0",
                "A01=B23=0", "B01=A23=0", "B01=B23=0",
            ],
        },
        "fitting_escape_checklist": [
            "D01 rank drops on lambda=+/-1 or phi=+/-1",
            "D23 finite rank drops on lambda=+/-1 and (phi+1)*lambda=+/-(phi-1)",
            "D23 infinity has the phi=-1 endpoint drop",
            "marking-pole divisors and vertical-plane lift divisors occur in compactified special fibres",
        ],
        "construction_or_proof_b_artifacts_read_or_imported": False,
        "limitations": (
            "Only the displayed component-19 affine chart with phi a unit and generic "
            "nonzero all-pair-open restriction. Excludes the identically zero arc, "
            "phi=0 and lower-pair/projective chart boundaries, other components, the "
            "arbitrary-order local-to-global reduction, and the global conjecture."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
