#!/usr/bin/env python3
"""Independent exact audit of ordinary component-19 weighted H22 at p=0.

No p=0 construction, candidate, proof-B, or certificate artifact is imported.
The marked bases are reconstructed from the component theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import os
import shutil
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
TMP = ROOT / "tmp" / "component19_p0_ordinary_h22_independent_audit"

q, phi = sp.symbols("q phi")
h0, h1, h2, h3, lam = sp.symbols("h0 h1 h2 h3 lambda")
hs = (h0, h1, h2, h3)
x = sp.symbols("x0:4")
y = sp.symbols("y0:4")
w = sp.symbols("w")
zvars = x + y


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    n = len(rows)
    assert all(len(row) == n for row in rows)
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


def component_rows():
    A = (1, 1, 0, 0)
    Abar = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    Bbar = (0, 0, 1, -1)
    alpha = (Abar, B, Bbar, Abar)
    beta = (
        tuple(Bbar[j] + q * B[j] for j in range(4)),
        A,
        A,
        tuple(B[j] + phi * Bbar[j] for j in range(4)),
    )
    return alpha, beta


def marked_extended_rows():
    alpha, beta = component_rows()
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


def singular_polynomial(expr) -> str:
    numerator, denominator = sp.fraction(sp.cancel(expr))
    assert set(denominator.free_symbols) <= {q, phi}
    return sp.sstr(sp.expand(numerator)).replace("**", "^").replace("lambda", "la")


def ideal_text(gens) -> str:
    values = [singular_polynomial(g) for g in gens if sp.expand(g) != 0]
    return ",\n  ".join(values) if values else "0"


def singular_command(path: Path):
    direct = shutil.which("Singular") or shutil.which("singular")
    if direct:
        return [direct, str(path)]
    if shutil.which("wsl.exe"):
        resolved = path.resolve()
        drive = resolved.drive.rstrip(":").lower()
        tail = resolved.as_posix().split(":", 1)[1]
        return ["wsl.exe", "-e", "Singular", f"/mnt/{drive}{tail}"]
    raise RuntimeError("Singular is required")


def run_singular(label: str, source: str, timeout: int = 240) -> str:
    TMP.mkdir(parents=True, exist_ok=True)
    path = TMP / f"{label}.sing"
    path.write_text(source, encoding="utf-8")
    proc = subprocess.Popen(
        singular_command(path),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
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


def projection_program(label, equations, expected, variables):
    eliminated = [*zvars, w]
    names = [str(variable).replace("lambda", "la") for variable in variables]
    return f"""
option(redSB);
ring R=(0,q,phi),({','.join(names)}),(dp(9),dp({len(variables)-9}));
ideal I={ideal_text(equations)};
ideal J=std(eliminate(std(I),{'*'.join(str(v) for v in eliminated)}));
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
        models = {"01": (A01, B01), "23": (A23, B23)}
        for orientation in ("01", "23"):
            A, B = models[orientation]
            equations = mixed01 + mixed23 + [A - 1, w * B - 1]
            expected = [lam - 1, h3, h1, h0] if finite and orientation == "23" else [1]
            variables = [*zvars, w, h0, h1, h2, h3] + ([lam] if finite else [])
            label = f"shared_orientation_{orientation}_{chart}"
            outputs.append(run_singular(
                label,
                projection_program(label, equations, expected, variables),
            ))
    return outputs


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


def component_and_pair_data():
    alpha, beta = component_rows()
    coeff = {
        bits: sp.factor(permanent([beta[i] if bits[i] else alpha[i]
                                   for i in range(4)]))
        for bits in itertools.product((0, 1), repeat=4)
    }
    nonzero = {bits: value for bits, value in coeff.items() if value != 0}
    assert set(nonzero) == {(1, 1, 1, 1)}
    assert sp.expand(nonzero[(1, 1, 1, 1)] - 4 * (q - phi)) == 0

    matrices = []
    for i, j in itertools.combinations(range(4), 2):
        rows = []
        for row_i in (alpha[i], beta[i]):
            for row_j in (alpha[j], beta[j]):
                rows.append([
                    sp.expand(row_i[a] * row_j[b] + row_i[b] * row_j[a])
                    for a, b in itertools.combinations(range(4), 2)
                ])
        matrices.append(sp.Matrix(rows))
    profile = tuple(matrix.rank() for matrix in matrices)
    assert profile == (3, 3, 4, 3, 3, 3)
    rank_three_witnesses = (
        sp.factor(matrices[0].extract((0, 2, 3), (1, 2, 5)).det()),
        sp.factor(matrices[1].extract((0, 2, 3), (1, 4, 5)).det()),
        sp.factor(matrices[3].extract((1, 2, 3), (0, 1, 2)).det()),
        sp.factor(matrices[4].extract((0, 1, 3), (1, 4, 5)).det()),
        sp.factor(matrices[5].extract((0, 1, 3), (1, 2, 5)).det()),
    )
    assert rank_three_witnesses == (4 * q, -4, -4, -4, 4 * phi)
    edge03_witness = sp.factor(matrices[2].extract(range(4), (0, 1, 2, 5)).det())
    assert sp.expand(edge03_witness + 8 * (q - phi) * (phi * q - 1)) == 0
    reciprocal_profile = tuple(matrix.subs(q, 1 / phi).rank() for matrix in matrices)
    assert reciprocal_profile == (3, 3, 3, 3, 3, 3)
    return nonzero, profile, rank_three_witnesses, edge03_witness, reciprocal_profile


def shared_frame_and_minors():
    t, X, Y, Z = sp.symbols("t X Y Z")
    r = q - phi
    branch = {lam: 1, h0: 0, h1: 0, h2: t, h3: 0}
    mixed01, A01, B01 = binary_coefficients("01", True)
    mixed23, A23, B23 = binary_coefficients("23", True)
    combined = sp.Matrix([
        [sp.expand(equation).coeff(variable) for variable in zvars]
        for equation in mixed01 + mixed23
    ]).subs(branch)

    vX = sp.Matrix((0, -1 / r, phi / r, 0, 1, 0, 0, 0))
    vY = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    vZ = sp.Matrix((0, -q / r, 1 / r, 0, 0, 0, 0, 1))
    for vector in (vX, vY, vZ):
        assert all(sp.cancel(value) == 0 for value in combined * vector)
    complete_rows = (2, 9, 10, 12, 15)
    complete_cols = (0, 1, 2, 3, 6)
    complete_minor = sp.factor(combined.extract(complete_rows, complete_cols).det())
    assert sp.expand(complete_minor + 1024 * q * r**2) == 0
    assert combined.rank() == 5

    extension = X * vX + Y * vY + Z * vZ
    extension_sub = dict(zip(zvars, extension))
    F = phi * X + Z
    G = r * Y - t * F
    H = X + q * Z
    diagonals = tuple(sp.factor(value.subs(branch).subs(extension_sub))
                      for value in (A01, B01, A23, B23))
    expected_diagonals = (0, 4 * G, -4 * F / r, 4 * H)
    assert all(sp.cancel(a - b) == 0 for a, b in zip(diagonals, expected_diagonals))

    alpha5, beta5 = marked_extended_rows()
    alpha01 = [contract(row, "01", True) for row in alpha5]
    beta01 = [contract(row, "01", True) for row in beta5]
    marked0 = one_marked_map(0, alpha01, beta01).subs(branch).subs(extension_sub)
    marked3 = one_marked_map(3, alpha01, beta01).subs(branch).subs(extension_sub)
    M0 = sp.factor(marked0.extract((1, 3, 5, 7), range(4)).det())
    M3 = sp.factor(marked3.extract((4, 5, 6, 7), range(4)).det())
    expected_M0 = 64 * Z * (phi**2 - 1) * (2 * phi * X + (phi * q + 1) * Z) * G / r**2
    expected_M3 = -64 * X * (q**2 - 1) * ((phi * q + 1) * X + 2 * q * Z) * G / r**2
    assert sp.cancel(M0 - expected_M0) == 0
    assert sp.cancel(M3 - expected_M3) == 0

    # Complete case certificate on the stated open.  If both minors vanish
    # with X,Z nonzero, the two remaining linear forms have determinant
    # -(phi*q-1)^2.  Axis cases use phi*q+1.
    linear_determinant = sp.factor(
        sp.Matrix(((2 * phi, phi * q + 1), (phi * q + 1, 2 * q))).det()
    )
    assert linear_determinant == -(phi * q - 1) ** 2

    # On phi*q=-1 the two axis subloci X=0 and Z=0 retain F,H,G opens while
    # both selected minors vanish; preserve them as UNKNOWN.
    minus_axis_M0 = sp.factor(M0.subs(q, -1 / phi))
    minus_axis_M3 = sp.factor(M3.subs(q, -1 / phi))
    assert sp.factor(minus_axis_M0).has(X * Z) or sp.cancel(minus_axis_M0.subs(X, 0)) == 0
    assert sp.cancel(minus_axis_M0.subs(X, 0)) == 0
    assert sp.cancel(minus_axis_M0.subs(Z, 0)) == 0
    assert sp.cancel(minus_axis_M3.subs(X, 0)) == 0
    assert sp.cancel(minus_axis_M3.subs(Z, 0)) == 0

    return {
        "frame_vX": tuple(vX),
        "frame_vY": tuple(vY),
        "frame_vZ": tuple(vZ),
        "complete_minor": complete_minor,
        "diagonals_A01_B01_A23_B23": diagonals,
        "M0_D01_mode0_rows_1357": M0,
        "M3_D01_mode3_rows_4567": M3,
        "linear_form_determinant": linear_determinant,
        "qphi_minus_one_M0": minus_axis_M0,
        "qphi_minus_one_M3": minus_axis_M3,
    }


def generic_open_unit_certificate():
    # This exact function-field saturation corroborates the hand case split.
    X, Y, Z, t, u = sp.symbols("X Y Z t u")
    r = q - phi
    F = phi * X + Z
    G = r * Y - t * F
    H = X + q * Z
    m0 = Z * (phi**2 - 1) * (2 * phi * X + (phi * q + 1) * Z) * G
    m3 = X * (q**2 - 1) * ((phi * q + 1) * X + 2 * q * Z) * G
    label = "generic_open_rank_obstruction"
    source = f"""
option(redSB);
ring R=(0,q,phi,t),(X,Y,Z,u),dp;
ideal I={singular_polynomial(m0)},{singular_polynomial(m3)},{singular_polynomial(u*F*G*H-1)};
ideal J=std(I);
if (J[1]==1) {{ print(\"AUDIT_OK {label}\"); J; }}
else {{ print(\"AUDIT_FAIL {label}\"); J; }}
quit;
"""
    return run_singular(label, source)


def main():
    nonzero, profile, rank_three_witnesses, witness, reciprocal_profile = component_and_pair_data()
    projections = exact_shared_projections()
    frame = shared_frame_and_minors()
    projections.append(generic_open_unit_certificate())
    print("source_sha256", sha256(SOURCE))
    print("pure_support", nonzero)
    print("generic_pair_profile", profile)
    print("rank_three_pair_witnesses_edges_01_02_12_13_23", rank_three_witnesses)
    print("edge03_rank4_witness", witness)
    print("qphi_equals_one_pair_profile", reciprocal_profile)
    for output in projections:
        for line in output.splitlines():
            if "AUDIT_OK" in line or line.startswith("J["):
                print(line)
    for key, value in frame.items():
        print(key, value)
    if TMP.exists():
        for stale in TMP.glob("*.sing"):
            stale.unlink()
        TMP.rmdir()
    print("P0_ORDINARY_H22_OPEN_VERIFIED")
    print("EXCEPTIONAL_AXES_STATUS_UNKNOWN")


if __name__ == "__main__":
    main()
