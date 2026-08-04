#!/usr/bin/env python3
"""Descent step: close the newly discovered ninth-component curve.

The extraction found the frame-q1 binary-survivor curve

    W := { p*q - p + 2 = 0 }   (rational: q = (p-2)/p, p != 0)

with genuine binary survivors (witness points (-1,3) and (5,3/5),
isolated survivor markings).  This script executes the meta-theorem's
certificate move AT the curve:

  1. parametrize W by p (q = (p-2)/p), clear denominators;
  2. compute the exact survivor marking locus over Q(p) by
     eliminating (z,w) from {mixed rows, w*A*B-1};
  3. find a ternary certificate: for each mode m, adjoin a battery of
     one-marked 4x4 minors of P_m and test unit over Q(p)
     (sound: an H31 lift forces rank P_m <= 3 for every m);
  4. extract the contraction J ⊂ Q[p] of the successful system with p
     as a ring variable (Theorem 1) -> finite exceptional point set;
  5. close each exceptional rational point by exact feasibility
     (0-dimensional leaves; a feasible point is recorded OPEN).

Fail-closed throughout: Singular under hard timeouts, nulls recorded,
nothing claimed on a null.  Ledger: close_new_curve_descent.json.
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = "/home/user/open-graph-theory-with-prize"
sys.path.insert(0, REPO)

import sympy as sp  # noqa: E402

from verify_p5_h31_all_rank_one_triangle_component_generic_obstruction import (  # noqa: E402
    P,
    Q,
    family,
    marked_extension,
    mixed_system,
    shifted_basis,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "close_new_curve_descent.json"

MINOR_ROW_SETS = (
    (0, 1, 4, 7), (0, 2, 3, 7), (0, 2, 6, 7), (0, 3, 6, 7),
    (0, 2, 4, 7), (0, 1, 3, 7), (0, 1, 5, 7), (0, 4, 5, 7),
    (0, 1, 2, 7),
)


def run_singular(program: str, timeout: float = 420.0):
    try:
        completed = subprocess.run(
            ("timeout", "--signal=KILL", f"{timeout:.1f}s",
             "Singular", "-q"),
            input=program,
            text=True,
            capture_output=True,
            timeout=timeout + 15,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout


def poly_str(expression) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def curve_system():
    """Frame q=1 system on the curve q=(p-2)/p, denominators cleared."""
    alpha, beta = family()
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diag_a, diag_b = mixed_system(
        1, alpha, marked_beta, extensions
    )
    extension = sp.Matrix(extensions)
    substitution = {Q: (P - 2) / P}

    def clear(expr):
        expr = sp.together(expr.subs(substitution))
        numerator, denominator = sp.fraction(expr)
        # denominator is a power of p (p != 0 on the curve chart)
        assert sp.simplify(
            denominator / P ** sp.degree(denominator, P)
        ) == 1, denominator
        return sp.expand(numerator)

    equations = [clear(eq) for eq in (mixed * extension)]
    a_val = clear((diag_a * extension)[0])
    b_val = clear((diag_b * extension)[0])
    equations.append(sp.expand(inverse * a_val * b_val - 1))

    def clear_row(row):
        """Multiply a whole row by one p-power (SOUND: row scaling
        rescales every 4x4 minor by that unit on the chart p!=0,
        unlike entry-wise clearing, which would destroy the rank
        relation)."""
        cleared = [sp.together(entry.subs(substitution))
                   for entry in row]
        powers = []
        for entry in cleared:
            _, denominator = sp.fraction(entry)
            degree = sp.degree(denominator, P)
            assert sp.simplify(denominator / P**degree) == 1, (
                denominator
            )
            powers.append(degree)
        scale = P ** max(powers) if powers else sp.Integer(1)
        return [sp.expand(sp.cancel(entry * scale))
                for entry in cleared]

    minors = {}
    for mode in range(4):
        marked = marked_extension(
            1, extension, alpha, marked_beta, mode
        )
        rows_cleared = [
            clear_row([marked[i, j] for j in range(4)])
            for i in range(8)
        ]
        marked = sp.Matrix(rows_cleared)
        minors[mode] = {
            rows: sp.expand(
                marked[list(rows), :].det(method="berkowitz")
            )
            for rows in MINOR_ROW_SETS
        }
    return equations, minors, shifts, extensions, inverse


def marking_locus(equations, shifts, extensions, inverse):
    zw = tuple(extensions) + (inverse,)
    variables = zw + tuple(shifts)
    program = "\n".join(
        (
            "ring R=(0,p),("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
            "ideal I=" + ",".join(map(poly_str, equations)) + ";",
            "ideal J=eliminate(I," + "*".join(map(str, zw)) + ");",
            "J=interred(J);",
            '"CODEX_SIZE:"+string(size(J));',
            "int gi;",
            "for(gi=1;gi<=size(J);gi++)"
            '{ "CODEX_GEN:"+string(J[gi]); }',
            "quit;",
        )
    )
    stdout = run_singular(program)
    if stdout is None:
        return None
    return [ln.strip().split(":", 1)[1]
            for ln in stdout.splitlines()
            if ln.startswith("CODEX_GEN:")]


def unit_over_Qp(equations, minor_polys, variables):
    program = "\n".join(
        (
            "ring R=(0,p),("
            + ",".join(map(str, variables))
            + "),dp;",
            "ideal I="
            + ",".join(map(poly_str,
                           list(equations) + list(minor_polys)))
            + ";",
            "I=slimgb(I);",
            "int unit=(reduce(1,I)==0);",
            '"CODEX_UNIT:"+string(unit);',
            "quit;",
        )
    )
    stdout = run_singular(program)
    if stdout is None:
        return None
    hits = [ln.strip() for ln in stdout.splitlines()
            if ln.startswith("CODEX_UNIT:")]
    if hits == ["CODEX_UNIT:1"]:
        return True
    if hits == ["CODEX_UNIT:0"]:
        return False
    return None


def extract_over_Zp(equations, minor_polys, variables):
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + ",p),(dp(" + str(len(variables)) + "),dp(1));",
            "ideal I="
            + ",".join(map(poly_str,
                           list(equations) + list(minor_polys)))
            + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I,"
            + "*".join(map(str, variables))
            + ");",
            "J=interred(J);",
            '"CODEX_SIZE:"+string(size(J));',
            "int gi;",
            "for(gi=1;gi<=size(J);gi++)"
            '{ "CODEX_GEN:"+string(J[gi]); }',
            "if(size(J)>0)",
            "{ list F=factorize(J[1]); int fi;",
            "  for(fi=1;fi<=size(F[1]);fi++)"
            '  { "CODEX_FACTOR:"+string(F[1][fi]); } }',
            "quit;",
        )
    )
    stdout = run_singular(program)
    if stdout is None:
        return None
    gens, factors = [], []
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("CODEX_GEN:"):
            gens.append(line.split(":", 1)[1])
        elif line.startswith("CODEX_FACTOR:"):
            factors.append(line.split(":", 1)[1])
    return {"generators": gens, "factors": factors}


def point_feasible(equations, minor_polys, variables, p_value):
    """Exact rational feasibility at p = p_value (0-dim leaf)."""
    substituted = [
        sp.expand(eq.subs({P: p_value}))
        for eq in list(equations) + list(minor_polys)
    ]
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + "),dp;",
            "ideal I=" + ",".join(map(poly_str, substituted)) + ";",
            "I=std(I);",
            "int unit=(reduce(1,I)==0);",
            '"CODEX_UNIT:"+string(unit);',
            "quit;",
        )
    )
    stdout = run_singular(program)
    if stdout is None:
        return None
    hits = [ln.strip() for ln in stdout.splitlines()
            if ln.startswith("CODEX_UNIT:")]
    if hits == ["CODEX_UNIT:1"]:
        return False
    if hits == ["CODEX_UNIT:0"]:
        return True
    return None


def main() -> None:
    report: dict = {
        "curve": "p*q-p+2=0, parametrized q=(p-2)/p (p!=0)",
        "frame": 1,
    }
    equations, minors, shifts, extensions, inverse = curve_system()
    variables = tuple(shifts) + tuple(extensions) + (inverse,)

    # 2. survivor marking locus over Q(p)
    report["survivor_marking_locus_over_Q(p)"] = marking_locus(
        equations, shifts, extensions, inverse
    )
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("marking locus:",
          report["survivor_marking_locus_over_Q(p)"], flush=True)

    # 3. ternary certificate search, one mode at a time
    certificate = None
    for mode in range(4):
        minor_polys = list(minors[mode].values())
        unit = unit_over_Qp(equations, minor_polys, variables)
        report[f"mode_{mode}_battery_unit_over_Q(p)"] = unit
        OUT.write_text(json.dumps(report, indent=2) + "\n")
        print(f"mode {mode} battery unit:", unit, flush=True)
        if unit:
            certificate = (mode, minor_polys)
            break
    if certificate is None:
        # try all modes together (still sound)
        minor_polys = [poly
                       for mode in range(4)
                       for poly in minors[mode].values()]
        unit = unit_over_Qp(equations, minor_polys, variables)
        report["all_modes_battery_unit_over_Q(p)"] = unit
        OUT.write_text(json.dumps(report, indent=2) + "\n")
        if unit:
            certificate = ("all", minor_polys)
    if certificate is None:
        report["verdict"] = (
            "OPEN: no ternary battery certificate found over Q(p) "
            "(or Singular null); the curve remains an obligation"
        )
        OUT.write_text(json.dumps(report, indent=2) + "\n")
        print(report["verdict"], flush=True)
        return

    mode, minor_polys = certificate
    report["certificate_mode"] = str(mode)

    # 4. contraction in Q[p]
    extraction = extract_over_Zp(equations, minor_polys, variables)
    report["contraction_in_Q[p]"] = extraction
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("contraction:", extraction, flush=True)
    if not extraction or not extraction.get("generators"):
        report["verdict"] = "extraction null; curve remains OPEN"
        OUT.write_text(json.dumps(report, indent=2) + "\n")
        return

    # 5. exceptional points: factor the gcd of ALL contraction
    # generators (the exceptional set is V(J) = common zeros).
    gens = [
        sp.sympify(g.replace("^", "**"))
        for g in extraction["generators"]
    ]
    combined = gens[0]
    for other in gens[1:]:
        combined = sp.gcd(combined, other)
    report["contraction_gcd"] = str(sp.factor(combined))
    factor_list = sp.factor_list(combined, P)[1]
    points = []
    unresolved_factors = []
    for factor, _multiplicity in factor_list:
        poly = sp.Poly(factor, P)
        if poly.degree() == 0:
            continue
        roots = poly.all_roots()
        for root in roots:
            if root.is_rational:
                feasible = point_feasible(
                    equations, minor_polys, variables, root
                )
                points.append({
                    "p": str(root),
                    "q": str(sp.nsimplify((root - 2) / root))
                    if root != 0 else "n/a (p=0 outside chart)",
                    "system_with_minors_feasible": feasible,
                })
                OUT.write_text(json.dumps(report, indent=2) + "\n")
            else:
                unresolved_factors.append(
                    {"factor": str(factor), "root": str(root)}
                )
    report["exceptional_rational_points"] = points
    report["exceptional_nonrational_roots"] = unresolved_factors
    open_points = [pt for pt in points
                   if pt["system_with_minors_feasible"] is not False]
    if not open_points and not unresolved_factors:
        report["verdict"] = (
            "curve CLOSED pointwise: certificate valid off finitely "
            "many rational points, each closed by exact feasibility"
        )
    else:
        report["verdict"] = (
            "curve closed off V(contraction); remaining open: "
            f"{len(open_points)} feasible/null rational points, "
            f"{len(unresolved_factors)} non-rational roots "
            "(each a 0-dimensional obligation)"
        )
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("verdict:", report["verdict"], flush=True)


if __name__ == "__main__":
    main()
