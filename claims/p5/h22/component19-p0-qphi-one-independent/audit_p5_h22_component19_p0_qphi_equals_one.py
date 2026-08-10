#!/usr/bin/env python3
"""Independent exact audit of p=0, q*phi=1 for component 19."""

from __future__ import annotations

import hashlib
import itertools
import os
import shutil
import subprocess
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
TMP = ROOT / "tmp" / "component19_p0_qphi_one_independent_audit"

phi = sp.symbols("phi")
h0, h1, h2, h3, lam = sp.symbols("h0 h1 h2 h3 lambda")
hs = (h0, h1, h2, h3)
x = sp.symbols("x0:4")
y = sp.symbols("y0:4")
w = sp.symbols("w")
v = sp.symbols("v")
zvars = x + y


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    n = len(rows)
    dp = {0: sp.Integer(1)}
    for row in rows:
        nxt = {}
        for mask, value in dp.items():
            for column, entry in enumerate(row):
                if not (mask >> column) & 1:
                    key = mask | (1 << column)
                    nxt[key] = nxt.get(key, 0) + value * entry
        dp = {key: sp.expand(value) for key, value in nxt.items()}
    return sp.expand(dp[(1 << n) - 1])


def specialized_rows():
    A = (1, 1, 0, 0)
    Abar = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    Bbar = (0, 0, 1, -1)
    shared_beta = tuple(B[j] + phi * Bbar[j] for j in range(4))
    alpha = (Abar, B, Bbar, Abar)
    # beta0 is phi times the ordinary row Bbar+(1/phi)B, so it equals beta3.
    beta = (shared_beta, A, A, shared_beta)
    return alpha, beta


def marked_extended_rows():
    alpha, beta = specialized_rows()
    aa = [tuple(alpha[i]) + (x[i],) for i in range(4)]
    bb = [
        tuple(sp.expand(beta[i][j] + hs[i] * alpha[i][j]) for j in range(4))
        + (y[i],)
        for i in range(4)
    ]
    return aa, bb


def contract(row, direction: str, finite: bool):
    if direction == "01":
        if finite:
            return (sp.expand(lam * row[0] + row[1]), row[2], row[3], row[4])
        return (row[0], row[2], row[3], row[4])
    if direction == "23":
        if finite:
            return (row[0], row[1], sp.expand(lam * row[2] + row[3]), row[4])
        return (row[0], row[1], row[2], row[4])
    raise ValueError(direction)


def binary_coefficients(direction: str, finite: bool):
    aa, bb = marked_extended_rows()
    aa = [contract(row, direction, finite) for row in aa]
    bb = [contract(row, direction, finite) for row in bb]
    coeff = {}
    for bits in itertools.product((0, 1), repeat=4):
        coeff[bits] = permanent([bb[i] if bits[i] else aa[i] for i in range(4)])
    mixed = [value for bits, value in coeff.items()
             if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))]
    return mixed, coeff[(0, 0, 0, 0)], coeff[(1, 1, 1, 1)]


def one_marked_map(mode: int, alpha, beta):
    rows = []
    others = [index for index in range(4) if index != mode]
    for bits in itertools.product((0, 1), repeat=3):
        selected = {other: beta[other] if bits[k] else alpha[other]
                    for k, other in enumerate(others)}
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(permanent([
                basis if index == mode else selected[index]
                for index in range(4)
            ]))
        rows.append(row)
    return sp.Matrix(rows)


def singular_polynomial(expr) -> str:
    numerator, denominator = sp.fraction(sp.cancel(expr))
    assert set(denominator.free_symbols) <= {phi}
    return sp.sstr(sp.expand(numerator)).replace("**", "^").replace("lambda", "la")


def ideal_text(gens) -> str:
    values = [singular_polynomial(g) for g in gens if sp.expand(g) != 0]
    return ",\n  ".join(values) if values else "0"


def singular_command(path: Path):
    direct = shutil.which("Singular") or shutil.which("singular")
    if direct:
        return [direct, str(path)]
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    tail = resolved.as_posix().split(":", 1)[1]
    return ["wsl.exe", "-e", "Singular", f"/mnt/{drive}{tail}"]


def run_singular(label: str, source: str, timeout: int = 240) -> str:
    TMP.mkdir(parents=True, exist_ok=True)
    path = TMP / f"{label}.sing"
    path.write_text(source, encoding="utf-8")
    proc = subprocess.Popen(
        singular_command(path), cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
    )
    try:
        try:
            output, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                    capture_output=True,
                    check=False,
                )
            else:
                proc.kill()
            proc.communicate()
            raise RuntimeError(f"Singular timeout: {label}")
        if proc.returncode or "AUDIT_OK" not in output:
            raise RuntimeError(f"Singular failure ({label}):\n{output}")
        return output
    finally:
        path.unlink(missing_ok=True)


def projection_program(label, equations, expected, variables, eliminated):
    names = [str(variable).replace("lambda", "la") for variable in variables]
    return f"""
option(redSB);
ring R=(0,phi),({','.join(names)}),(dp({len(eliminated)}),dp({len(variables)-len(eliminated)}));
ideal I={ideal_text(equations)};
ideal J=std(eliminate(std(I),{'*'.join(str(variable) for variable in eliminated)}));
ideal E=std(ideal({ideal_text(expected)}));
ideal a=reduce(J,E); ideal b=reduce(E,J);
if (size(a)==0 and size(b)==0) {{ print(\"AUDIT_OK {label}\"); J; }}
else {{ print(\"AUDIT_FAIL {label}\"); J; a; b; }}
quit;
"""


def exact_shared_projections():
    outputs = []
    for finite in (True, False):
        chart = "finite" if finite else "infinity"
        mixed01, A01, B01 = binary_coefficients("01", finite)
        mixed23, A23, B23 = binary_coefficients("23", finite)
        for orientation, A, B in (("01", A01, B01), ("23", A23, B23)):
            other_required_beta = B23 if orientation == "01" else B01
            equations = mixed01 + mixed23 + [A - 1, w * B - 1, v * other_required_beta - 1]
            expected = [lam - 1, h3, h1, h0] if finite and orientation == "23" else [1]
            variables = [*zvars, w, v, h0, h1, h2, h3] + ([lam] if finite else [])
            eliminated = [*zvars, w, v]
            label = f"shared_A{orientation}_{chart}"
            outputs.append(run_singular(
                label, projection_program(label, equations, expected, variables, eliminated)
            ))
    return outputs


def pure_and_pair_geometry():
    alpha, beta = specialized_rows()
    coeff = {
        bits: sp.factor(permanent([beta[i] if bits[i] else alpha[i]
                                   for i in range(4)]))
        for bits in itertools.product((0, 1), repeat=4)
    }
    nonzero = {bits: value for bits, value in coeff.items() if value != 0}
    assert set(nonzero) == {(1, 1, 1, 1)}
    assert sp.expand(nonzero[(1, 1, 1, 1)] - 4 * (1 - phi**2)) == 0

    matrices = []
    for i, j in itertools.combinations(range(4), 2):
        matrices.append(sp.Matrix([
            [sp.expand(row_i[a] * row_j[b] + row_i[b] * row_j[a])
             for a, b in itertools.combinations(range(4), 2)]
            for row_i in (alpha[i], beta[i])
            for row_j in (alpha[j], beta[j])
        ]))
    generic_profile = tuple(matrix.rank() for matrix in matrices)
    assert generic_profile == (3, 3, 3, 3, 3, 3)
    endpoint_profiles = {
        epsilon: tuple(matrix.subs(phi, epsilon).rank() for matrix in matrices)
        for epsilon in (+1, -1)
    }
    assert endpoint_profiles == {
        +1: (3, 3, 2, 3, 3, 3),
        -1: (3, 3, 2, 3, 3, 3),
    }
    endpoint_tensor = {
        epsilon: sp.factor(nonzero[(1, 1, 1, 1)].subs(phi, epsilon))
        for epsilon in (+1, -1)
    }
    assert endpoint_tensor == {+1: 0, -1: 0}
    return nonzero, generic_profile, endpoint_profiles


def complete_frame_and_obstruction():
    t, C, D, E = sp.symbols("t C D E")
    delta = phi**2 - 1
    branch = {lam: 1, h0: 0, h1: 0, h2: t, h3: 0}
    mixed01, A01, B01 = binary_coefficients("01", True)
    mixed23, A23, B23 = binary_coefficients("23", True)
    combined = sp.Matrix([
        [sp.expand(equation).coeff(variable) for variable in zvars]
        for equation in mixed01 + mixed23
    ]).subs(branch)

    vC = sp.Matrix((0, 1 / delta, -phi / delta, 0, 1, 0, 0, 0))
    vD = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    vE = sp.Matrix((0, 1 / delta, -phi / delta, 0, 0, 0, 0, 1))
    for vector in (vC, vD, vE):
        assert all(sp.cancel(value) == 0 for value in combined * vector)
    complete_minor = sp.factor(combined.extract(
        (2, 9, 10, 12, 15), (0, 1, 2, 3, 6)
    ).det())
    assert sp.expand(complete_minor + 1024 * delta**2) == 0
    assert combined.rank() == 5

    extension = C * vC + D * vD + E * vE
    extension_sub = dict(zip(zvars, extension))
    S = C + E
    G = delta * D + phi * t * S
    diagonals = tuple(sp.factor(value.subs(branch).subs(extension_sub))
                      for value in (A01, B01, A23, B23))
    expected_diagonals = (0, -4 * G, 4 * phi * S / delta, 4 * S)
    assert all(sp.cancel(a - b) == 0 for a, b in zip(diagonals, expected_diagonals))

    alpha5, beta5 = marked_extended_rows()
    alpha01 = [contract(row, "01", True) for row in alpha5]
    beta01 = [contract(row, "01", True) for row in beta5]
    marked0 = one_marked_map(0, alpha01, beta01).subs(branch).subs(extension_sub)
    marked3 = one_marked_map(3, alpha01, beta01).subs(branch).subs(extension_sub)
    M0 = sp.factor(marked0.extract((1, 3, 5, 7), range(4)).det())
    M3 = sp.factor(marked3.extract((4, 5, 6, 7), range(4)).det())
    expected_M0 = -128 * E * phi * S * G / delta
    expected_M3 = -128 * C * phi * S * G / delta
    assert sp.cancel(M0 - expected_M0) == 0
    assert sp.cancel(M3 - expected_M3) == 0

    # Exact saturation: on S*G!=0, M0=M3=0 forces C=E=0 and hence S=0.
    label = "rank_minor_open_saturation"
    source = f"""
ring R=(0,phi,t),(C,D,E,u),dp;
ideal I=E*(C+E)*(({singular_polynomial(delta)})*D+phi*t*(C+E)),
        C*(C+E)*(({singular_polynomial(delta)})*D+phi*t*(C+E)),
        u*(C+E)*(({singular_polynomial(delta)})*D+phi*t*(C+E))-1;
ideal J=std(I);
if (J[1]==1) {{ print(\"AUDIT_OK {label}\"); J; }}
else {{ print(\"AUDIT_FAIL {label}\"); J; }}
quit;
"""
    saturation = run_singular(label, source)
    return {
        "frame_vC": tuple(vC), "frame_vD": tuple(vD), "frame_vE": tuple(vE),
        "complete_minor": complete_minor,
        "diagonals_A01_B01_A23_B23": diagonals,
        "M0_D01_mode0_rows_1357": M0,
        "M3_D01_mode3_rows_4567": M3,
    }, saturation


def discarded_lambda_minus_one_nongenuine_branch():
    P, C, E = sp.symbols("P C E")
    branch = {lam: -1, h0: 0, h1: 0, h2: 0, h3: 0}
    mixed01, A01, B01 = binary_coefficients("01", True)
    mixed23, A23, B23 = binary_coefficients("23", True)
    combined = sp.Matrix([
        [sp.expand(equation).coeff(variable) for variable in zvars]
        for equation in mixed01 + mixed23
    ]).subs(branch)
    vP = sp.Matrix((0, 1 / phi, 1, 0, 0, 0, 0, 0))
    vC = sp.Matrix((0, 0, 0, 0, 1, 0, 0, 0))
    vE = sp.Matrix((0, 0, 0, 0, 0, 0, 0, 1))
    for vector in (vP, vC, vE):
        assert all(sp.cancel(value) == 0 for value in combined * vector)
    complete_minor = sp.factor(combined.extract(
        (0, 2, 4, 20, 27), (0, 1, 3, 5, 6)
    ).det())
    assert complete_minor == -1024 * phi**4
    assert combined.rank() == 5

    extension = P * vP + C * vC + E * vE
    extension_sub = dict(zip(zvars, extension))
    diagonals = tuple(sp.factor(value.subs(branch).subs(extension_sub))
                      for value in (A01, B01, A23, B23))
    assert diagonals == (0, 0, 4 * P / phi, -4 * phi * (C + E))

    rank_profiles = {}
    all_four_minors_zero = True
    alpha5, beta5 = marked_extended_rows()
    for direction in ("01", "23"):
        alpha_d = [contract(row, direction, True) for row in alpha5]
        beta_d = [contract(row, direction, True) for row in beta5]
        ranks = []
        for mode in range(4):
            marked = one_marked_map(mode, alpha_d, beta_d).subs(branch).subs(extension_sub)
            ranks.append(marked.rank())
            for rows in itertools.combinations(range(8), 4):
                if sp.factor(marked.extract(rows, range(4)).det()) != 0:
                    all_four_minors_zero = False
        rank_profiles[direction] = tuple(ranks)
    assert rank_profiles == {"01": (1, 3, 3, 1), "23": (3, 3, 3, 3)}
    assert all_four_minors_zero

    # One exact rank-three witness is forced nonzero throughout the genuine
    # D23 open P*(C+E)!=0.
    alpha23 = [contract(row, "23", True) for row in alpha5]
    beta23 = [contract(row, "23", True) for row in beta5]
    mode2 = one_marked_map(2, alpha23, beta23).subs(branch).subs(extension_sub)
    mode2_witness = sp.factor(mode2.extract((0, 1, 7), (0, 1, 2)).det())
    assert mode2_witness == 16 * P**2 * (C + E)
    return {
        "branch": "lambda=-1,h=(0,0,0,0)",
        "frame_vP": tuple(vP), "frame_vC": tuple(vC), "frame_vE": tuple(vE),
        "complete_minor": complete_minor,
        "diagonals_A01_B01_A23_B23": diagonals,
        "D23_binary_open": "P*(C+E)!=0",
        "required_D01_B_diagonal": 0,
        "shared_H22_genuine": False,
        "generic_rank_profiles": rank_profiles,
        "all_4x4_one_marked_minors_zero": all_four_minors_zero,
        "D23_mode2_rank3_witness": mode2_witness,
    }


def main():
    pure, profile, endpoints = pure_and_pair_geometry()
    projections = exact_shared_projections()
    frame, saturation = complete_frame_and_obstruction()
    minus_one = discarded_lambda_minus_one_nongenuine_branch()
    projections.append(saturation)
    print("source_sha256", sha256(SOURCE))
    print("pure_support", pure)
    print("pair_profile", profile)
    print("phi_endpoint_pair_profiles", endpoints)
    for output in projections:
        for line in output.splitlines():
            if "AUDIT_OK" in line or line.startswith("J["):
                print(line)
    for key, value in frame.items():
        print(key, value)
    print("discarded_nongenuine_projection_component")
    for key, value in minus_one.items():
        print(key, value)
    if TMP.exists():
        for stale in TMP.glob("*.sing"):
            stale.unlink()
        TMP.rmdir()
    print("P0_QPHI_ONE_FULL_OBSTRUCTION_VERIFIED")
    print("LAMBDA_MINUS_ONE_NONGENUINE_COMPONENT_DISCARDED")
    print("PHI_PLUS_MINUS_ONE_ZERO_ENDPOINTS_EXCLUDED")


if __name__ == "__main__":
    main()
