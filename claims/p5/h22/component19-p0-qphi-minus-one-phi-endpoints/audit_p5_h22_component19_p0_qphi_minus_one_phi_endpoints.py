#!/usr/bin/env python3
"""Independent exact audit of the q*phi=-1, phi^2=1 p=0 intersections.

The regular component basis is rebuilt from the P4 component theorem.  No
q-endpoint exploration, candidate, proof-B, or construction file is imported.
"""

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
SOURCE = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
REPORT = (
    ROOT
    / "P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_PHI_ENDPOINTS_VERIFICATION.md"
)
TMP = ROOT / "tmp" / "component19_p0_qphim1_phi_endpoints_verifier"

h0, h1, h2, h3, lam = sp.symbols("h0 h1 h2 h3 lambda")
hs = (h0, h1, h2, h3)
x = sp.symbols("x0:4")
y = sp.symbols("y0:4")
zvars = x + y
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit():
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def permanent(rows):
    """Permanent by subset DP, without permutation expansion."""

    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if not mask & bit:
                    new_mask = mask | bit
                    next_states[new_mask] = (
                        next_states.get(new_mask, 0) + coefficient * entry
                    )
        states = {
            mask: sp.expand(value) for mask, value in next_states.items()
        }
    return sp.expand(states[(1 << len(rows)) - 1])


def component_rows(phi):
    q = -phi
    cap_a = (1, 1, 0, 0)
    cap_abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_bbar = (0, 0, 1, -1)
    alpha = (cap_abar, cap_b, cap_bbar, cap_abar)
    beta = (
        tuple(cap_bbar[j] + q * cap_b[j] for j in range(4)),
        cap_a,
        cap_a,
        tuple(cap_b[j] + phi * cap_bbar[j] for j in range(4)),
    )
    return alpha, beta


def marked_extended_rows(phi):
    alpha, beta = component_rows(phi)
    alpha5 = tuple(alpha[mode] + (x[mode],) for mode in range(4))
    beta5 = tuple(
        tuple(
            beta[mode][column] + hs[mode] * alpha[mode][column]
            for column in range(4)
        )
        + (y[mode],)
        for mode in range(4)
    )
    return alpha5, beta5


def projection(direction):
    if direction == "01":
        return sp.Matrix(
            (
                (lam, 1, 0, 0, 0),
                (0, 0, 1, 0, 0),
                (0, 0, 0, 1, 0),
                (0, 0, 0, 0, 1),
            )
        )
    if direction == "23":
        return sp.Matrix(
            (
                (1, 0, 0, 0, 0),
                (0, 1, 0, 0, 0),
                (0, 0, lam, 1, 0),
                (0, 0, 0, 0, 1),
            )
        )
    raise ValueError(direction)


def coefficients(phi, direction):
    alpha5, beta5 = marked_extended_rows(phi)
    project = projection(direction)
    alpha4 = tuple(tuple(project * sp.Matrix(row)) for row in alpha5)
    beta4 = tuple(tuple(project * sp.Matrix(row)) for row in beta5)
    values = {
        word: permanent(
            tuple(
                beta4[mode] if word[mode] else alpha4[mode]
                for mode in range(4)
            )
        )
        for word in WORDS4
    }
    return (
        tuple(values[word] for word in WORDS4[1:-1]),
        values[WORDS4[0]],
        values[WORDS4[-1]],
    )


def complementary_permanent(rows, omitted_column):
    retained = tuple(
        column for column in range(len(rows) + 1) if column != omitted_column
    )
    return permanent(
        tuple(tuple(row[column] for column in retained) for row in rows)
    )


def one_marked(alpha, beta, mode):
    other = tuple(index for index in range(4) if index != mode)
    return sp.Matrix(
        [
            [
                complementary_permanent(
                    tuple(
                        beta[index] if word[position] else alpha[index]
                        for position, index in enumerate(other)
                    ),
                    column,
                )
                for column in range(4)
            ]
            for word in WORDS3
        ]
    )


def full_one_marked(alpha5, beta5, mode, contraction):
    other = tuple(index for index in range(4) if index != mode)
    return sp.Matrix(
        [
            [
                complementary_permanent(
                    tuple(
                        beta5[index] if word[position] else alpha5[index]
                        for position, index in enumerate(other)
                    )
                    + (contraction,),
                    column,
                )
                for column in range(5)
            ]
            for word in WORDS3
        ]
    )


def endpoint_frame(phi):
    cap_x, cap_y, cap_z, t = sp.symbols("X Y Z t")
    extension = sp.Matrix(
        (
            0,
            (phi * cap_x - cap_z) / 2,
            -(cap_x + phi * cap_z) / 2,
            0,
            cap_x,
            cap_y,
            0,
            cap_z,
        )
    )
    branch = {lam: 1, h0: 0, h1: 0, h2: t, h3: 0}
    substitution = {**branch, **dict(zip(zvars, extension))}
    cap_f = phi * cap_x + cap_z
    cap_g = -2 * phi * cap_y - t * cap_f
    cap_h = cap_x - phi * cap_z
    return (
        (cap_x, cap_y, cap_z, t),
        extension,
        branch,
        substitution,
        (cap_f, cap_g, cap_h),
    )


def singular_command(path):
    direct = shutil.which("Singular") or shutil.which("singular")
    if direct:
        return [direct, str(path)]
    if shutil.which("wsl.exe"):
        resolved = path.resolve()
        drive = resolved.drive.rstrip(":").lower()
        tail = resolved.as_posix().split(":", 1)[1]
        return ["wsl.exe", "-e", "Singular", f"/mnt/{drive}{tail}"]
    raise RuntimeError("Singular is required for the exact incidence replay")


def singular_text(expression):
    numerator, denominator = sp.fraction(sp.cancel(expression))
    assert denominator.free_symbols == set()
    return (
        sp.sstr(sp.expand(numerator))
        .replace("**", "^")
        .replace("lambda", "la")
    )


def run_singular(label, source):
    TMP.mkdir(parents=True, exist_ok=True)
    path = TMP / f"{label}.sing"
    path.write_text(source, encoding="utf-8")
    try:
        completed = subprocess.run(
            singular_command(path),
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=240,
            check=False,
        )
        output = completed.stdout + completed.stderr
        if completed.returncode != 0 or f"AUDIT_OK {label}" not in output:
            raise RuntimeError(f"Singular failure ({label}):\n{output}")
        return f"AUDIT_OK {label}"
    finally:
        path.unlink(missing_ok=True)


def exact_genuine_incidence(phi):
    mixed01, _, b01 = coefficients(phi, "01")
    mixed23, a23, b23 = coefficients(phi, "23")
    u, v = sp.symbols("u v")
    equations = (*mixed01, *mixed23, a23 - 1, u * b01 - 1, v * b23 - 1)
    generators = ",\n  ".join(
        singular_text(value) for value in equations if value != 0
    )
    names = (
        *[str(value) for value in zvars],
        "u",
        "v",
        "h0",
        "h1",
        "h2",
        "h3",
        "la",
    )
    label = f"endpoint_phi_{phi}_genuine_incidence"
    source = f"""
option(redSB);
ring R=0,({','.join(names)}),(dp(10),dp(5));
ideal I={generators};
ideal J=std(eliminate(std(I),x0*x1*x2*x3*y0*y1*y2*y3*u*v));
ideal E=std(ideal(la-1,h3,h1,h0));
ideal a=reduce(J,E); ideal b=reduce(E,J);
if (size(a)==0 and size(b)==0) {{ print("AUDIT_OK {label}"); J; }}
else {{ print("AUDIT_FAIL {label}"); J; a; b; }}
quit;
"""
    return run_singular(label, source)


def complete_shared_frame(phi):
    variables, extension, branch, substitution, gates = endpoint_frame(phi)
    cap_x, cap_y, cap_z, _ = variables
    mixed01, a01, b01 = coefficients(phi, "01")
    mixed23, a23, b23 = coefficients(phi, "23")
    combined = sp.Matrix(
        [
            [sp.expand(equation.subs(branch)).coeff(variable) for variable in zvars]
            for equation in (*mixed01, *mixed23)
        ]
    )
    frame = tuple(extension.diff(variable) for variable in (cap_x, cap_y, cap_z))
    assert all(
        all(sp.factor(value) == 0 for value in combined * vector)
        for vector in frame
    )
    witness_rows = (2, 9, 10, 12, 15)
    witness_columns = (0, 1, 2, 3, 6)
    witness = sp.factor(
        combined.extract(witness_rows, witness_columns).det()
    )
    assert witness == 4096 * phi
    assert combined.rank() == 5 and len(combined.nullspace()) == 3

    diagonals = tuple(
        sp.factor(value.subs(substitution)) for value in (a01, b01, a23, b23)
    )
    cap_f, cap_g, cap_h = gates
    expected = (0, 4 * cap_g, 2 * phi * cap_f, 4 * cap_h)
    assert all(sp.expand(left - right) == 0 for left, right in zip(diagonals, expected))
    return {
        "extension_frame": [[str(value) for value in vector] for vector in frame],
        "complete_rank_five_minor": str(witness),
        "complete_minor_rows": list(witness_rows),
        "complete_minor_columns": list(witness_columns),
        "combined_mixed_rank": 5,
        "kernel_dimension": 3,
        "diagonals_A01_B01_A23_B23": [str(value) for value in diagonals],
        "genuine_condition": "F*G*H!=0",
    }


def projected_maps_on_frame(phi):
    _, _, _, substitution, _ = endpoint_frame(phi)
    alpha5, beta5 = marked_extended_rows(phi)
    maps = {}
    for direction in ("01", "23"):
        project = projection(direction)
        alpha4 = tuple(tuple(project * sp.Matrix(row)) for row in alpha5)
        beta4 = tuple(tuple(project * sp.Matrix(row)) for row in beta5)
        for mode in range(4):
            maps[(direction, mode)] = one_marked(
                alpha4, beta4, mode
            ).subs(substitution)
    return maps


def all_maximal_minors(matrix):
    return tuple(
        sp.factor(matrix.extract(rows, range(4)).det())
        for rows in itertools.combinations(range(8), 4)
    )


def rank_witness_specs(phi, cap_x, cap_z, t):
    if phi == -1:
        return {
            ("01", 0): ((3, 5, 7), (0, 1, 3), 8 * t**2 * (cap_x - cap_z) * (cap_x + cap_z)),
            ("01", 1): ((7,), (0,), 2 * t * (cap_x - cap_z)),
            ("01", 2): ((7,), (3,), 8),
            ("01", 3): ((5, 6, 7), (0, 2, 3), 8 * t**2 * (cap_x - cap_z) * (cap_x + cap_z)),
            ("23", 0): ((0, 3, 7), (0, 1, 3), -8 * (cap_x - cap_z) ** 2),
            ("23", 1): ((0, 1, 7), (0, 1, 2), 4 * (cap_x - cap_z) ** 2 * (cap_x + cap_z)),
            ("23", 2): ((0, 1, 7), (0, 1, 2), 4 * (cap_x - cap_z) * (cap_x + cap_z) ** 2),
            ("23", 3): ((0, 5, 7), (0, 1, 3), 8 * (cap_x - cap_z) ** 2),
        }
    return {
        ("01", 0): ((3, 5, 7), (0, 2, 3), -8 * t**2 * (cap_x - cap_z) * (cap_x + cap_z)),
        ("01", 1): ((7,), (0,), -2 * t * (cap_x + cap_z)),
        ("01", 2): ((7,), (3,), -8),
        ("01", 3): ((5, 6, 7), (0, 1, 3), 8 * t**2 * (cap_x - cap_z) * (cap_x + cap_z)),
        ("23", 0): ((0, 3, 7), (0, 1, 3), 8 * (cap_x + cap_z) ** 2),
        ("23", 1): ((0, 1, 7), (0, 1, 2), 4 * (cap_x - cap_z) * (cap_x + cap_z) ** 2),
        ("23", 2): ((0, 1, 7), (0, 1, 2), 4 * (cap_x - cap_z) ** 2 * (cap_x + cap_z)),
        ("23", 3): ((0, 5, 7), (0, 1, 3), -8 * (cap_x + cap_z) ** 2),
    }


def individual_rank_classification(phi):
    variables, _, _, _, gates = endpoint_frame(phi)
    cap_x, cap_y, cap_z, t = variables
    cap_f, _, cap_h = gates
    maps = projected_maps_on_frame(phi)
    fixed = sp.factor(maps[("23", 2)].extract((0, 1, 2, 7), range(4)).det())
    assert sp.expand(fixed + 32 * cap_y * cap_f * cap_h) == 0

    survivor_maps = {key: matrix.subs(cap_y, 0) for key, matrix in maps.items()}
    assert all(
        all(value == 0 for value in all_maximal_minors(matrix))
        for matrix in survivor_maps.values()
    )
    specs = rank_witness_specs(phi, cap_x, cap_z, t)
    expected_ranks = {
        ("01", 0): 3,
        ("01", 1): 1,
        ("01", 2): 1,
        ("01", 3): 3,
        ("23", 0): 3,
        ("23", 1): 3,
        ("23", 2): 3,
        ("23", 3): 3,
    }
    witnesses = {}
    for key, (rows, columns, expected) in specs.items():
        actual = sp.factor(survivor_maps[key].extract(rows, columns).det())
        assert sp.expand(actual - expected) == 0
        assert len(rows) == expected_ranks[key]
        witnesses[f"{key[0]}_mode_{key[1]}"] = {
            "rows": list(rows),
            "columns": list(columns),
            "determinant": str(actual),
        }
    return {
        "forcing_minor": {
            "map": "D23_mode_2",
            "rows": [0, 1, 2, 7],
            "determinant": str(fixed),
        },
        "complete_survivor_equations": "Y=0, t*F*H!=0",
        "projective_extension_locus": "[X:Z] in P1 minus {F=0,H=0}",
        "includes_nonaxis_points": True,
        "D01_rank_profile": [3, 1, 1, 3],
        "D23_rank_profile": [3, 3, 3, 3],
        "rank_witnesses": witnesses,
    }


def compatibility_obstruction(phi):
    variables, _, _, substitution, gates = endpoint_frame(phi)
    _, cap_y, _, _ = variables
    cap_f, _, cap_h = gates
    alpha5, beta5 = marked_extended_rows(phi)

    def specialize(rows):
        return tuple(
            tuple(
                sp.factor(sp.sympify(value).subs(substitution).subs(cap_y, 0))
                for value in row
            )
            for row in rows
        )

    alpha5 = specialize(alpha5)
    beta5 = specialize(beta5)
    project01 = projection("01").subs(lam, 1)
    project23 = projection("23").subs(lam, 1)
    projected = projected_maps_on_frame(phi)
    q01 = (1, 1, 0, 0, 0)
    q23 = (0, 0, 1, 1, 0)
    records = []
    for mode in range(4):
        full01 = full_one_marked(alpha5, beta5, mode, q01)
        full23 = full_one_marked(alpha5, beta5, mode, q23)
        assert all(
            sp.factor(value) == 0
            for value in full01 - projected[("01", mode)].subs(cap_y, 0) * project01
        )
        assert all(
            sp.factor(value) == 0
            for value in full23 - projected[("23", mode)].subs(cap_y, 0) * project23
        )
        stack = full01.col_join(full23)
        records.append({"mode": mode, "stack_rank_over_function_field": stack.rank()})

    full01 = full_one_marked(alpha5, beta5, 1, q01)
    full23 = full_one_marked(alpha5, beta5, 1, q23)
    stack = full01.col_join(full23)
    rows = (7, 8, 9, 15)
    columns = (0, 1, 2, 3)
    witness = sp.factor(stack.extract(rows, columns).det())
    assert sp.expand(witness + 16 * cap_f**3 * cap_h) == 0
    return {
        "factorization_equations": (
            "N01_i=U01_i*R_i and N23_i=U23_i*R_i with shared R_i in Mat(3,5)"
        ),
        "equivalent_rank_condition": "rank(stack(N01_i,N23_i))<=3",
        "obstructing_mode": 1,
        "stacked_rows": list(rows),
        "stacked_columns": list(columns),
        "stacked_determinant": str(witness),
        "stack_records": records,
        "common_three_column_factorization_exists": False,
    }


def endpoint_certificate(phi):
    assert phi in (-1, 1)
    return {
        "phi": phi,
        "q": -phi,
        "incidence_elimination": exact_genuine_incidence(phi),
        "complete_genuine_marking_ideal": ["lambda-1", "h3", "h1", "h0"],
        "free_marking": "h2=t",
        "shared_frame": complete_shared_frame(phi),
        "individual_rank_classification": individual_rank_classification(phi),
        "target_local_compatibility": compatibility_obstruction(phi),
        "finite_ordinary_weighted_H22_fibre_empty": True,
    }


def main():
    endpoints = [endpoint_certificate(phi) for phi in (-1, 1)]
    if TMP.exists() and not any(TMP.iterdir()):
        TMP.rmdir()
    script = Path(__file__).resolve()
    outputs = {script.name: sha256(script)}
    if REPORT.exists():
        outputs[REPORT.name] = sha256(REPORT)
    result = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "complete finite ordinary component-19 p=0 intersections "
            "q*phi=-1, phi^2=1, namely (q,phi)=(1,-1),(-1,1)"
        ),
        "inputs": {SOURCE.name: sha256(SOURCE)},
        "method": (
            "fresh regular-basis reconstruction; exact three-diagonal-saturated "
            "incidence elimination; complete shared kernel; exhaustive local "
            "4x4 minors; fixed exact rank witnesses; full 8x5 two-slice stack"
        ),
        "command": (
            'uv run --with sympy python claims/p5/h22/component19-p0-qphi-minus-one-phi-endpoints/audit_p5_h22_component19_p0_qphi_minus_one_phi_endpoints.py'
        ),
        "outputs": outputs,
        "limitations": (
            "finite ordinary lambda chart at the two stated parameter points; "
            "no weight infinity/projective boundary, other parameter fibre, "
            "other component, arbitrary-order reduction, or global claim"
        ),
        "endpoints": endpoints,
        "survivor_jump": (
            "VERIFIED full Y=0 sheet with t*(phi*X+Z)*(X-phi*Z)!=0, "
            "including X*Z!=0 nonaxis points"
        ),
        "finite_ordinary_intersections_closed": True,
        "remaining_unknown_locus_in_scope": None,
        "imports_q_endpoint_exploration_or_candidate": False,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
