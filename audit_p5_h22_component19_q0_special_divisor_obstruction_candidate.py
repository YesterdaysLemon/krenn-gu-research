#!/usr/bin/env python3
"""Independent exact audit of component 19, q=0, weighted H22.

This file deliberately reconstructs the component from
P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md.  It imports no discovery
or candidate implementation.  The characteristic-zero incidence checks are
performed over Q(p,phi) by file-backed Singular elimination.
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
TMP = ROOT / "tmp" / "component19_q0_independent_audit_solver_inputs"

p, phi = sp.symbols("p phi")
h0, h1, h2, h3, lam = sp.symbols("h0 h1 h2 h3 lambda")
hs = (h0, h1, h2, h3)
x = sp.symbols("x0:4")
y = sp.symbols("y0:4")
w = sp.symbols("w")
zvars = x + y


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    """Permanent by subset DP; entries may be symbolic."""
    n = len(rows)
    assert all(len(row) == n for row in rows)
    dp = {0: sp.Integer(1)}
    for row in rows:
        nxt = {}
        for mask, value in dp.items():
            for col, entry in enumerate(row):
                if not (mask >> col) & 1:
                    key = mask | (1 << col)
                    nxt[key] = nxt.get(key, 0) + value * entry
        dp = {key: sp.expand(value) for key, value in nxt.items()}
    return sp.expand(dp[(1 << n) - 1])


def component_rows():
    # Original squarefree source coordinates (X0,X1,X2,X3).  General source
    # changes do not preserve the squarefree permanent tensor, so no hidden GL4
    # normalization is made here.
    A = (1, 1, 0, 0)
    Abar = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    Bbar = (0, 0, 1, -1)

    # q=0 planes, reoriented so the restriction has only T_1111=4p.
    alpha = (
        tuple(-phi * Abar[j] - phi * p * B[j] - p * Bbar[j] for j in range(4)),
        B,
        Bbar,
        Abar,
    )
    beta = (
        tuple(Abar[j] + p * B[j] for j in range(4)),
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
        + (sp.expand(y[i] + hs[i] * x[i]),)
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
        rows = [bb[i] if bits[i] else aa[i] for i in range(4)]
        coeff[bits] = permanent(rows)
    mixed = [coeff[b] for b in coeff if b not in ((0, 0, 0, 0), (1, 1, 1, 1))]
    return mixed, coeff[(0, 0, 0, 0)], coeff[(1, 1, 1, 1)]


def sympy_to_singular(expr) -> str:
    expr = sp.cancel(expr)
    num, den = sp.fraction(expr)
    if den != 1:
        # p and phi are coefficient-field units, so clear only their denominator.
        assert set(den.free_symbols) <= {p, phi}, (expr, den)
    return sp.sstr(sp.expand(num)).replace("**", "^").replace("lambda", "la")


def singular_executable():
    direct = shutil.which("Singular") or shutil.which("singular")
    if direct:
        return [direct]
    if shutil.which("wsl.exe"):
        return ["wsl.exe", "-e", "Singular"]
    raise RuntimeError("Singular is required")


def windows_to_wsl(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    tail = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{tail}"


def run_singular(label: str, source: str, timeout: int = 240) -> str:
    TMP.mkdir(parents=True, exist_ok=True)
    path = TMP / f"{label}.sing"
    path.write_text(source, encoding="utf-8")
    exe = singular_executable()
    cmd = exe + ([windows_to_wsl(path)] if exe[0].lower().endswith("wsl.exe") else [str(path)])
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    proc = subprocess.Popen(
        cmd,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=creationflags,
    )
    try:
        try:
            out, _ = proc.communicate(timeout=timeout)
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
        if proc.returncode:
            raise RuntimeError(f"Singular failed ({label}):\n{out}")
        if "AUDIT_OK" not in out:
            raise RuntimeError(f"Singular assertion failed ({label}):\n{out}")
        return out
    finally:
        path.unlink(missing_ok=True)


def ideal_text(gens):
    nonzero = [sympy_to_singular(g) for g in gens if sp.expand(g) != 0]
    return ",\n  ".join(nonzero) if nonzero else "0"


def projection_program(label, equations, eliminated, expected):
    allvars = [*x, *y, w, h0, h1, h2, h3]
    if any(lam in sp.sympify(eq).free_symbols for eq in equations) or any(lam in sp.sympify(e).free_symbols for e in expected):
        allvars.append(lam)
    names = [str(v).replace("lambda", "la") for v in allvars]
    elim_product = "*".join(str(v) for v in eliminated).replace("lambda", "la")
    eq_text = ideal_text(equations)
    exp_text = ideal_text(expected)
    return f"""
option(redSB);
ring R=(0,p,phi),({','.join(names)}),(dp({len(eliminated)}),dp({len(names)-len(eliminated)}));
ideal I={eq_text};
ideal J=std(eliminate(std(I),{elim_product}));
ideal E=std(ideal({exp_text}));
ideal a=reduce(J,E);
ideal b=reduce(E,J);
if (size(a)==0 and size(b)==0) {{
  print(\"AUDIT_OK {label}\");
  print(\"PROJECTED\"); J;
}} else {{
  print(\"AUDIT_FAIL {label}\");
  print(\"PROJECTED\"); J;
  print(\"J_MOD_E\"); a;
  print(\"E_MOD_J\"); b;
}}
quit;
"""


def exact_projections():
    results = []
    # Direct binary incidence: normalize A=1 and invert B.
    direct_expected = {
        ("01", True): [1],
        ("01", False): [1],
        ("23", True): [h3, phi * h0 - 1, h1 * h2 * (lam - 1), h1**2 * h2],
        ("23", False): [h3, phi * h0 - 1, h1 * h2],
    }
    for (direction, finite), expected in direct_expected.items():
        mixed, A, B = binary_coefficients(direction, finite)
        equations = mixed + [A - 1, w * B - 1]
        eliminated = [*x, *y, w]
        label = f"direct_d{direction}_{'finite' if finite else 'infinity'}"
        program = projection_program(label, equations, eliminated, expected)
        results.append(run_singular(label, program))

    # Shared system: impose both mixed kernels while retaining a genuine D23
    # binary neighbor (A23,B23 nonzero).  Normalize A23=1 and invert B23.  This
    # removes the rank-drop-only lambda=-1 false lead, whose D23 all-alpha
    # diagonal vanishes identically.
    for finite in (True, False):
        m01, _, _ = binary_coefficients("01", finite)
        m23, A23, B23 = binary_coefficients("23", finite)
        expected = [lam - 1, h3, h1, phi * h0 - 1] if finite else [1]
        equations = m01 + m23 + [A23 - 1, w * B23 - 1]
        eliminated = [*zvars, w]
        label = f"shared_{'finite' if finite else 'infinity'}"
        results.append(run_singular(label, projection_program(label, equations, eliminated, expected)))
    return results


def essential_embedded_generator():
    """Prove h1^2*h2 is not generated by the other finite D23 equations."""
    label = "essential_h1_squared_h2"
    source = """
ring R=(0,p,phi),(h0,h1,h2,h3,la),dp;
ideal E0=h3,phi*h0-1,h1*h2*(la-1);
poly r=reduce(h1^2*h2,std(E0));
if (r!=0) { print("AUDIT_OK essential_h1_squared_h2"); print("REMAINDER"); r; }
else { print("AUDIT_FAIL essential_h1_squared_h2"); }
quit;
"""
    return run_singular(label, source)


def one_marked_map(mode: int, alpha, beta):
    """Standard 8x4 coefficient map with an arbitrary row at `mode`."""
    rows = []
    others = [index for index in range(4) if index != mode]
    for bits in itertools.product((0, 1), repeat=3):
        selected = {
            other: beta[other] if bits[k] else alpha[other]
            for k, other in enumerate(others)
        }
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            coefficient_row.append(permanent([
                basis if index == mode else selected[index]
                for index in range(4)
            ]))
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def branch_frame_rank_and_boundaries():
    t, C, D = sp.symbols("t C D")
    branch = {lam: 1, h0: 1 / phi, h1: 0, h2: t, h3: 0}

    mixed01, A01, B01 = binary_coefficients("01", True)
    mixed23, A23, B23 = binary_coefficients("23", True)
    mixed = mixed01 + mixed23
    matrix = sp.Matrix([
        [sp.expand(equation).coeff(variable) for variable in zvars]
        for equation in mixed
    ]).subs(branch)

    # A polynomial two-frame valid also at t=0.  Its coordinates are the
    # pre-marking fifth-coordinate extensions (x0..x3,y0..y3).
    vC = sp.Matrix((0, -1 / p, phi / p, 0, 1, 0, -phi * t / p, 0))
    vD = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    assert all(sp.cancel(value) == 0 for value in matrix * vC)
    assert all(sp.cancel(value) == 0 for value in matrix * vD)

    complete_rows = (1, 2, 4, 10, 12, 15)
    complete_cols = (0, 1, 2, 3, 6, 7)
    completeness_minor = sp.factor(matrix.extract(complete_rows, complete_cols).det())
    assert sp.expand(completeness_minor - 4096 * p**4 * phi**2 * (phi**2 - 1)) == 0
    assert matrix.rank() == 6

    extension = C * vC + D * vD
    extension_sub = dict(zip(zvars, extension))
    diagonal_values = tuple(
        sp.factor(value.subs(branch).subs(extension_sub))
        for value in (A01, B01, A23, B23)
    )
    expected_diagonals = (
        0,
        4 * (p * D - phi * t * C),
        4 * C * phi**2 / p,
        4 * C,
    )
    assert all(sp.cancel(a - b) == 0 for a, b in zip(diagonal_values, expected_diagonals))

    # The nonzero marked-rank certificate is in the D01 contraction at mode 3.
    alpha5, beta5 = marked_extended_rows()
    alpha01 = [contract(row, "01", True) for row in alpha5]
    beta01 = [contract(row, "01", True) for row in beta5]
    marked3 = one_marked_map(3, alpha01, beta01).subs(branch).subs(extension_sub)
    fixed_rows = (1, 2, 5, 7)
    fixed_minor = sp.factor(marked3.extract(fixed_rows, range(4)).det())
    assert sp.expand(fixed_minor + 64 * C * p * (p * D - phi * t * C) ** 2) == 0

    # At phi=+/-1 the same shared matrix has rank five, so the two-frame is
    # incomplete and the open theorem must not be extended across this wall.
    boundary_ranks = {
        +1: matrix.subs(phi, 1).rank(),
        -1: matrix.subs(phi, -1).rank(),
    }
    assert boundary_ranks == {+1: 5, -1: 5}

    # A concrete unshared false lead: this is a genuine finite D23 binary
    # extension at lambda=0,h=(1/phi,0,1,0), but it violates D01 mixed rows.
    false_marking = {lam: 0, h0: 1 / phi, h1: 0, h2: 1, h3: 0}
    false_extension = sp.Matrix((0, 1, 0, 0, 1, 0, 1, 0))
    false_sub = dict(zip(zvars, false_extension))
    false23 = [sp.factor(e.subs(false_marking).subs(false_sub)) for e in mixed23]
    false01 = [sp.factor(e.subs(false_marking).subs(false_sub)) for e in mixed01]
    assert all(value == 0 for value in false23)
    assert any(value != 0 for value in false01)
    false_diagonals = (
        sp.factor(A23.subs(false_marking).subs(false_sub)),
        sp.factor(B23.subs(false_marking).subs(false_sub)),
    )
    assert all(sp.expand(a - b) == 0 for a, b in zip(false_diagonals, (-2 * phi, -2 * (phi - 1))))

    # A second tempting locus is shared-mixed at lambda=-1, but its D23
    # all-alpha diagonal is zero on the same marking branch.
    minus_branch = dict(branch)
    minus_branch[lam] = -1
    minus_matrix = sp.Matrix([
        [sp.expand(equation).coeff(variable) for variable in zvars]
        for equation in mixed
    ]).subs(minus_branch)
    assert minus_matrix.rank() == 6
    for kernel_vector in minus_matrix.nullspace():
        assert sp.factor(A23.subs(minus_branch).subs(dict(zip(zvars, kernel_vector)))) == 0

    return {
        "frame_vC": tuple(vC),
        "frame_vD": tuple(vD),
        "completeness_minor": completeness_minor,
        "diagonals_A01_B01_A23_B23": diagonal_values,
        "fixed_minor_rows_1257": fixed_minor,
        "boundary_ranks": boundary_ranks,
        "false_lead_D23_diagonals": false_diagonals,
    }


def pure_support_and_pair_profile():
    alpha, beta = component_rows()
    coeff = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows = [beta[i] if bits[i] else alpha[i] for i in range(4)]
        coeff[bits] = sp.factor(permanent(rows))
    nonzero = {bits: value for bits, value in coeff.items() if value != 0}
    assert nonzero == {(1, 1, 1, 1): 4 * p}, nonzero

    profile = []
    witnesses = []
    for i, j in itertools.combinations(range(4), 2):
        products = []
        for ri in (alpha[i], beta[i]):
            for rj in (alpha[j], beta[j]):
                products.append([sp.expand(ri[a] * rj[b] + ri[b] * rj[a])
                                 for a, b in itertools.combinations(range(4), 2)])
        M = sp.Matrix(products)
        rank = M.rank(iszerofunc=lambda e: sp.factor(e) == 0)
        profile.append(rank)
        nz = []
        for rows in itertools.combinations(range(4), rank):
            for cols in itertools.combinations(range(M.cols), rank):
                d = sp.factor(M.extract(rows, cols).det())
                if d != 0:
                    nz.append(d)
        witnesses.append(nz[0] if nz else sp.Integer(1))
    assert tuple(profile) == (3, 4, 4, 3, 3, 3), profile
    return nonzero, profile, witnesses


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    nonzero, profile, witnesses = pure_support_and_pair_profile()
    outputs = exact_projections()
    outputs.append(essential_embedded_generator())
    branch_data = branch_frame_rank_and_boundaries()
    print("source_sha256", sha256(SOURCE))
    print("pure_support", nonzero)
    print("pair_profile", tuple(profile))
    print("pair_witnesses", witnesses)
    for out in outputs:
        print(out.strip())
    for key, value in branch_data.items():
        print(key, value)
    if TMP.exists():
        for stale_solver_input in TMP.glob("*.sing"):
            stale_solver_input.unlink()
        TMP.rmdir()
    print("AUDIT_VERIFIED")


if __name__ == "__main__":
    main()
