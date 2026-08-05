#!/usr/bin/env python3
"""Exploratory rank-four obstruction census on component 19, p=0, q=+/-1.

This is a discovery aid, not an independent verifier.  It reuses the exact
ordinary p=0 reconstruction and asks whether the union of all eight
one-marked rank-four conditions covers the genuine shared-extension open.
"""

from __future__ import annotations

import argparse
import itertools
import shutil
import subprocess

import sympy as sp

import audit_p5_h22_component19_p0_ordinary_obstruction_open as base


def singular(expr: sp.Expr) -> str:
    numerator, denominator = sp.fraction(sp.cancel(expr))
    assert set(denominator.free_symbols) <= {base.phi}
    return sp.sstr(sp.expand(numerator)).replace("**", "^")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, choices=(-1, 1), default=1)
    args = parser.parse_args()
    q_value = sp.Integer(args.q)
    phi = base.phi
    t, X, Y, Z = sp.symbols("t X Y Z")
    r = q_value - phi
    branch = {
        base.q: q_value,
        base.lam: 1,
        base.h0: 0,
        base.h1: 0,
        base.h2: t,
        base.h3: 0,
    }

    vX = sp.Matrix((0, -1 / r, phi / r, 0, 1, 0, 0, 0))
    vY = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    vZ = sp.Matrix((0, -q_value / r, 1 / r, 0, 0, 0, 0, 1))
    extension = X * vX + Y * vY + Z * vZ
    extension_sub = dict(zip(base.zvars, extension))

    alpha5, beta5 = base.marked_extended_rows()
    all_minors: list[sp.Expr] = []
    records: dict[tuple[str, int], tuple[int, int]] = {}
    factored_minors: dict[tuple[str, int], tuple[sp.Expr, ...]] = {}
    matrices: dict[tuple[str, int], sp.Matrix] = {}
    for direction in ("01", "23"):
        aa = [base.contract(row, direction, True) for row in alpha5]
        bb = [base.contract(row, direction, True) for row in beta5]
        for mode in range(4):
            matrix = base.one_marked_map(mode, aa, bb).subs(branch).subs(extension_sub)
            minors = [
                sp.factor(matrix.extract(rows, range(4)).det())
                for rows in itertools.combinations(range(8), 4)
            ]
            nonzero = [value for value in minors if value != 0]
            all_minors.extend(nonzero)
            records[(direction, mode)] = (matrix.rank(), len(nonzero))
            factored_minors[(direction, mode)] = tuple(sorted(set(nonzero), key=str))
            matrices[(direction, mode)] = matrix

    F = phi * X + Z
    G = r * Y - t * F
    H = X + q_value * Z
    generators = sorted({singular(value) for value in all_minors})
    open_polynomial = singular(F * G * H)
    command = shutil.which("Singular")
    if command:
        argv = (command, "-q")
    elif shutil.which("wsl.exe"):
        argv = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    else:
        raise RuntimeError("Singular is required")
    program = "\n".join((
        "option(redSB);",
        "ring R=(0,phi,t),(X,Y,Z,u),dp;",
        "ideal I=" + ",".join(generators) + ";",
        f"I=I,u*({open_polynomial})-1;",
        "ideal J=std(I);",
        'if (J[1]==1) { print("OPEN_COVER_UNIT"); } else { print("OPEN_SURVIVOR"); J; }',
        "quit;",
    ))
    completed = subprocess.run(
        argv,
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=240,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed

    print("q", q_value)
    print("parameter_open", "phi*(phi^2-1)!=0")
    print("genuine_open", sp.factor(F * G * H))
    for key, value in records.items():
        print("map", key, "generic_rank_nonzero_4minors", value)
        for determinant in factored_minors[key]:
            print("  minor_factor", determinant)
    print("distinct_nonzero_minor_numerators", len(generators))
    print(completed.stdout.strip())

    survivor_substitutions = {
        "Z_axis": {Y: 0, Z: 0},
        "oblique": {Y: 0, X: -(phi * q_value + 1) * Z / (2 * phi)},
    }
    for survivor, substitution in survivor_substitutions.items():
        print("survivor", survivor)
        print("  FGH", sp.factor((F * G * H).subs(substitution)))
        for key, matrix in matrices.items():
            specialized = matrix.subs(substitution)
            rank = specialized.rank()
            witness = sp.Integer(1)
            witness_rows: tuple[int, ...] = ()
            witness_columns: tuple[int, ...] = ()
            if rank:
                for rows in itertools.combinations(range(8), rank):
                    found = False
                    for columns in itertools.combinations(range(4), rank):
                        determinant = sp.factor(specialized.extract(rows, columns).det())
                        if determinant != 0:
                            witness = determinant
                            witness_rows = rows
                            witness_columns = columns
                            found = True
                            break
                    if found:
                        break
            print("  map", key, "rank", rank, "witness", witness_rows,
                  witness_columns, witness)
        for mode in range(4):
            stacked = matrices[("01", mode)].col_join(matrices[("23", mode)]).subs(
                substitution
            )
            rank = stacked.rank()
            witness = sp.Integer(1)
            witness_rows: tuple[int, ...] = ()
            if rank >= 4:
                for rows in itertools.combinations(range(16), 4):
                    determinant = sp.factor(stacked.extract(rows, range(4)).det())
                    if determinant != 0:
                        witness = determinant
                        witness_rows = rows
                        break
            print("  stacked_mode", mode, "rank", rank,
                  "four_witness", witness_rows, witness)


if __name__ == "__main__":
    main()
