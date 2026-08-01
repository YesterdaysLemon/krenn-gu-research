#!/usr/bin/env python3
"""Independent exact audit of component 19 at q=0, phi=+/-1.

No endpoint discovery, proof-B, or certificate artifact is imported.  The
component rows come directly from P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md.
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
TMP = ROOT / "tmp" / "component19_q0_phi_endpoints_independent_audit"

p = sp.symbols("p")
phi = sp.symbols("phi")
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
    """Append x,y after choosing the marked rows beta+h*alpha."""
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
    assert set(denominator.free_symbols) <= {p}
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


def projection_program(label, equations, eliminated, expected, variables):
    names = [str(variable).replace("lambda", "la") for variable in variables]
    return f"""
option(redSB);
ring R=(0,p),({','.join(names)}),(dp({len(eliminated)}),dp({len(variables)-len(eliminated)}));
ideal I={ideal_text(equations)};
ideal J=std(eliminate(std(I),{'*'.join(str(v) for v in eliminated)}));
ideal E=std(ideal({ideal_text(expected)}));
ideal a=reduce(J,E); ideal b=reduce(E,J);
if (size(a)==0 and size(b)==0) {{ print(\"AUDIT_OK {label}\"); J; }}
else {{ print(\"AUDIT_FAIL {label}\"); J; a; b; }}
quit;
"""


def exact_endpoint_projections():
    outputs = []
    for epsilon in (+1, -1):
        direct_expected = {
            ("01", True): [p * h3 + 1, h1, h0 - epsilon],
            ("01", False): [p * h3 + 1, h1, h0 - epsilon],
            ("23", True): [h3, h0 - epsilon, h1 * h2 * (lam - 1), h1**2 * h2],
            ("23", False): [h3, h0 - epsilon, h1 * h2],
        }
        for (direction, finite), expected in direct_expected.items():
            mixed, A, B = binary_coefficients(direction, finite)
            equations = [e.subs(phi, epsilon) for e in mixed + [A - 1, w * B - 1]]
            variables = [*zvars, w, h0, h1, h2, h3] + ([lam] if finite else [])
            eliminated = [*zvars, w]
            label = f"epsilon_{epsilon}_direct_d{direction}_{'finite' if finite else 'infinity'}"
            outputs.append(run_singular(
                label,
                projection_program(label, equations, eliminated, expected, variables),
            ))

        for finite in (True, False):
            mixed01, _, _ = binary_coefficients("01", finite)
            mixed23, A23, B23 = binary_coefficients("23", finite)
            equations = [e.subs(phi, epsilon) for e in mixed01 + mixed23 + [A23 - 1, w * B23 - 1]]
            expected = [lam - 1, h3, h1, h0 - epsilon] if finite else [1]
            variables = [*zvars, w, h0, h1, h2, h3] + ([lam] if finite else [])
            eliminated = [*zvars, w]
            label = f"epsilon_{epsilon}_shared_{'finite' if finite else 'infinity'}"
            outputs.append(run_singular(
                label,
                projection_program(label, equations, eliminated, expected, variables),
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


def coefficient_matrix(equations):
    return sp.Matrix([
        [sp.expand(equation).coeff(variable) for variable in zvars]
        for equation in equations
    ])


def endpoint_kernel_and_obstructions():
    t, C, D, E = sp.symbols("t C D E")
    records = {}
    for epsilon in (+1, -1):
        branch = {phi: epsilon, lam: 1, h0: epsilon, h1: 0, h2: t, h3: 0}
        mixed01, A01, B01 = binary_coefficients("01", True)
        mixed23, A23, B23 = binary_coefficients("23", True)
        combined = coefficient_matrix(mixed01 + mixed23).subs(branch)

        vC = sp.Matrix((0, -1 / p, epsilon / p, 0, 1, 0, 0, 0))
        vD = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
        vE = sp.Matrix((epsilon * p, 0, -epsilon, 0, 0, 0, 0, 1))
        for vector in (vC, vD, vE):
            assert all(sp.cancel(value) == 0 for value in combined * vector)

        complete_rows = (1, 2, 10, 12, 15)
        complete_cols = (0, 1, 2, 3, 6)
        complete_minor = sp.factor(combined.extract(complete_rows, complete_cols).det())
        assert complete_minor == 1024 * p**3
        assert combined.rank() == 5

        extension = C * vC + D * vD + E * vE
        extension_sub = dict(zip(zvars, extension))
        diagonals = tuple(sp.factor(value.subs(branch).subs(extension_sub))
                          for value in (A01, B01, A23, B23))
        Q = C - p * E
        expected_diagonals = (0, 4 * (p * D - epsilon * t * Q), 4 * Q / p, 4 * C)
        assert all(sp.cancel(a - b) == 0 for a, b in zip(diagonals, expected_diagonals))

        alpha5, beta5 = marked_extended_rows()
        alpha23 = [contract(row, "23", True) for row in alpha5]
        beta23 = [contract(row, "23", True) for row in beta5]
        marked3 = one_marked_map(3, alpha23, beta23).subs(branch).subs(extension_sub)
        fixed_minor = sp.factor(marked3.extract((0, 2, 3, 7), range(4)).det())
        assert sp.expand(fixed_minor + 64 * epsilon * C * Q**2) == 0

        # Direct D01 false-lead branch and its projective slope behavior.
        false_branch = {phi: epsilon, h0: epsilon, h1: 0, h2: t, h3: -1 / p}
        false_finite = coefficient_matrix(mixed01).subs(false_branch)
        generic_minor = sp.factor(false_finite.extract(
            (1, 2, 3, 7, 10, 12), (0, 1, 2, 3, 4, 5)
        ).det())
        assert generic_minor == 64 * p**4 * (lam - 1)**2 * (lam + 1)**4
        assert false_finite.subs(lam, 1).rank() == 4
        assert false_finite.subs(lam, -1).rank() == 3
        plus_minor = sp.factor(false_finite.subs(lam, 1).extract(
            (1, 2, 10, 12), (0, 1, 2, 3)
        ).det())
        minus_minor = sp.factor(false_finite.subs(lam, -1).extract(
            (1, 3, 7), (1, 5, 6)
        ).det())
        assert plus_minor == 256 * epsilon * p**3
        assert minus_minor == -64 * p**3

        A_false = A01.subs(false_branch)
        B_false = B01.subs(false_branch)
        for vector in false_finite.subs(lam, 1).nullspace():
            assert sp.factor(A_false.subs(lam, 1).subs(dict(zip(zvars, vector)))) == 0
        for vector in false_finite.subs(lam, -1).nullspace():
            assert sp.factor(B_false.subs(lam, -1).subs(dict(zip(zvars, vector)))) == 0

        mixed01_infinity, A01_infinity, B01_infinity = binary_coefficients("01", False)
        false_infinity = coefficient_matrix(mixed01_infinity).subs(false_branch)
        infinity_minor = sp.factor(false_infinity.extract(
            (1, 2, 3, 7, 10, 12), (0, 1, 2, 3, 4, 5)
        ).det())
        assert infinity_minor == 64 * p**4
        assert false_infinity.rank() == 6
        # Both diagonal functionals are nonzero on this two-dimensional kernel,
        # hence a vector avoiding their two zero hyperplanes exists over Q(p,t).
        infinity_kernel = false_infinity.nullspace()
        assert any(sp.factor(A01_infinity.subs(false_branch).subs(dict(zip(zvars, v)))) != 0
                   for v in infinity_kernel)
        assert any(sp.factor(B01_infinity.subs(false_branch).subs(dict(zip(zvars, v)))) != 0
                   for v in infinity_kernel)

        records[epsilon] = {
            "complete_minor_rows_1_2_10_12_15_cols_0_1_2_3_6": complete_minor,
            "frame_vC": tuple(vC),
            "frame_vD": tuple(vD),
            "frame_vE": tuple(vE),
            "diagonals_A01_B01_A23_B23": diagonals,
            "fixed_D23_mode3_minor_rows_0_2_3_7": fixed_minor,
            "D01_finite_generic_rank_minor": generic_minor,
            "D01_lambda_plus1_rank_and_minor": (4, plus_minor),
            "D01_lambda_minus1_rank_and_minor": (3, minus_minor),
            "D01_infinity_rank_and_minor": (6, infinity_minor),
        }
    return records


def pure_support():
    alpha, beta = component_rows()
    coeff = {}
    for bits in itertools.product((0, 1), repeat=4):
        coeff[bits] = sp.factor(permanent([beta[i] if bits[i] else alpha[i]
                                           for i in range(4)]))
    nonzero = {bits: value for bits, value in coeff.items() if value != 0}
    assert nonzero == {(1, 1, 1, 1): 4 * p}
    return nonzero


def main():
    projections = exact_endpoint_projections()
    records = endpoint_kernel_and_obstructions()
    print("source_sha256", sha256(SOURCE))
    print("pure_support", pure_support())
    for output in projections:
        for line in output.splitlines():
            if "AUDIT_OK" in line or line.startswith("J["):
                print(line)
    for epsilon, record in records.items():
        print("epsilon", epsilon)
        for key, value in record.items():
            print(key, value)
    if TMP.exists():
        for stale in TMP.glob("*.sing"):
            stale.unlink()
        TMP.rmdir()
    print("ENDPOINT_AUDIT_VERIFIED")


if __name__ == "__main__":
    main()
