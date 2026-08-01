#!/usr/bin/env python3
"""Independent characteristic-zero audit of component 19 on q=phi.

The construction is rebuilt from P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md.
No q=phi candidate, proof-B, discovery script, or certificate is imported.
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
TMP = ROOT / "tmp" / "component19_q_equals_phi_independent_audit"

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

    # At q=phi the displayed U0 rows are (beta0,alpha0).  Reversing them
    # has determinant -1 and stays regular at phi=0.
    alpha = (
        tuple(Bbar[j] + phi * B[j] for j in range(4)),
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
    assert denominator == 1
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


def projection_program(label, equations, expected, variables, parameter_aware):
    eliminated = [*zvars, w]
    names = [str(variable).replace("lambda", "la") for variable in variables]
    coefficient_field = "(0,p)" if parameter_aware else "(0,p,phi)"
    return f"""
option(redSB);
ring R={coefficient_field},({','.join(names)}),(dp(9),dp({len(variables)-9}));
ideal I={ideal_text(equations)};
ideal J=std(eliminate(std(I),{'*'.join(str(v) for v in eliminated)}));
ideal E=std(ideal({ideal_text(expected)}));
ideal a=reduce(J,E); ideal b=reduce(E,J);
if (size(a)==0 and size(b)==0) {{ print(\"AUDIT_OK {label}\"); J; }}
else {{ print(\"AUDIT_FAIL {label}\"); J; a; b; }}
quit;
"""


def exact_incidence_ideals():
    outputs = []
    for parameter_aware in (False, True):
        suffix = "parameter_aware" if parameter_aware else "function_field"
        for finite in (True, False):
            chart = "finite" if finite else "infinity"
            models = {}
            for direction in ("01", "23"):
                mixed, A, B = binary_coefficients(direction, finite)
                models[direction] = (mixed, A, B)
                if parameter_aware and direction == "01":
                    expected = [h3, h2, h0, phi]
                else:
                    expected = [1]
                equations = mixed + [A - 1, w * B - 1]
                variables = [*zvars, w, h0, h1, h2, h3] + ([lam] if finite else [])
                if parameter_aware:
                    variables.append(phi)
                label = f"{suffix}_direct_d{direction}_{chart}"
                outputs.append(run_singular(
                    label,
                    projection_program(label, equations, expected, variables, parameter_aware),
                ))

            # Check both shared orientations.  In each, impose both mixed
            # systems and normalize/invert the chosen direction's diagonals.
            for orientation in ("01", "23"):
                mixed01, _, _ = models["01"]
                mixed23, _, _ = models["23"]
                _, A, B = models[orientation]
                equations = mixed01 + mixed23 + [A - 1, w * B - 1]
                variables = [*zvars, w, h0, h1, h2, h3] + ([lam] if finite else [])
                if parameter_aware:
                    variables.append(phi)
                label = f"{suffix}_shared_orientation_{orientation}_{chart}"
                outputs.append(run_singular(
                    label,
                    projection_program(label, equations, [1], variables, parameter_aware),
                ))
    return outputs


def pure_and_pair_data():
    alpha, beta = component_rows()
    coeff = {}
    for bits in itertools.product((0, 1), repeat=4):
        coeff[bits] = sp.factor(permanent([beta[i] if bits[i] else alpha[i]
                                           for i in range(4)]))
    nonzero = {bits: value for bits, value in coeff.items() if value != 0}
    assert nonzero == {(1, 1, 1, 1): 4 * p}

    targets = (8 * p * phi, 8 * p, 4 * p**2, 4, -4, 4 * phi)
    witness_indices = (
        ((0, 1, 2, 3), (1, 3, 4, 5)),
        ((0, 1, 2, 3), (1, 2, 3, 5)),
        ((0, 2, 3), (1, 2, 5)),
        ((1, 2, 3), (0, 2, 3)),
        ((0, 1, 3), (1, 4, 5)),
        ((0, 1, 3), (1, 2, 5)),
    )
    profile = []
    witnesses = []
    pair_matrices = []
    for edge, (i, j) in enumerate(itertools.combinations(range(4), 2)):
        rows = []
        for row_i in (alpha[i], beta[i]):
            for row_j in (alpha[j], beta[j]):
                rows.append([
                    sp.expand(row_i[u] * row_j[v] + row_i[v] * row_j[u])
                    for u, v in itertools.combinations(range(4), 2)
                ])
        matrix = sp.Matrix(rows)
        rank = matrix.rank()
        row_indices, column_indices = witness_indices[edge]
        witness = sp.factor(matrix.extract(row_indices, column_indices).det())
        assert sp.expand(witness - targets[edge]) == 0
        profile.append(rank)
        witnesses.append(witness)
        pair_matrices.append(matrix)
    assert tuple(profile) == (4, 4, 3, 3, 3, 3)

    pair23_zero = pair_matrices[5].subs(phi, 0)
    assert pair23_zero.rank() == 2
    rank_two_witness = sp.factor(pair23_zero.extract((0, 3), (1, 2)).det())
    assert rank_two_witness == 2
    for rows in itertools.combinations(range(4), 3):
        for columns in itertools.combinations(range(6), 3):
            assert sp.factor(pair23_zero.extract(rows, columns).det()) == 0

    return {
        "pure_support": nonzero,
        "pair_profile": tuple(profile),
        "pair_witnesses": tuple(witnesses),
        "phi_zero_pair23_rank": 2,
        "phi_zero_pair23_rank_two_witness": rank_two_witness,
    }


def main():
    data = pure_and_pair_data()
    outputs = exact_incidence_ideals()
    print("source_sha256", sha256(SOURCE))
    for key, value in data.items():
        print(key, value)
    for output in outputs:
        for line in output.splitlines():
            if "AUDIT_OK" in line or line.startswith("J["):
                print(line)
    if TMP.exists():
        for stale in TMP.glob("*.sing"):
            stale.unlink()
        TMP.rmdir()
    print("Q_EQUALS_PHI_AUDIT_VERIFIED")


if __name__ == "__main__":
    main()
