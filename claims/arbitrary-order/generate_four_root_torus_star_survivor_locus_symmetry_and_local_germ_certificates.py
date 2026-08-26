#!/usr/bin/env python3
"""Generate the exact ideal-equivalence certificate for the survivor germ.

The portable verifiers do not require Singular.  This optional producer uses
Singular 4.x to replace the 37 equal-leaf incidence equations (11 of which
are zero) by ten generators and records sparse transformations in both
directions.  It emits canonical JSON on stdout; repository updates should add
that output through the normal review/edit path.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
from itertools import chain
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
VERIFIER = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py"
)


def load_verifier():
    spec = importlib.util.spec_from_file_location("survivor_germ_verifier", VERIFIER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def singular_expression(expression: sp.Expr, variables) -> str:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=sp.QQ_I)
    rendered = []
    for exponents, coefficient in polynomial.terms():
        monomial = "*".join(
            (str(variable) if power == 1 else f"{variable}^{power}")
            for variable, power in zip(variables, exponents, strict=True)
            if power
        )
        scalar = str(coefficient).replace("I", "i")
        rendered.append(f"({scalar})*{monomial}" if monomial else f"({scalar})")
    return "+".join(rendered) if rendered else "0"


def certificate_program() -> str:
    verifier = load_verifier()
    survivor = verifier.load_gld72()
    gate = survivor.load_gate()
    parent = gate.load_parent()
    xi, eta, ports = parent.canonical_torus_star(1)
    layers = parent.full_q_layer_columns(xi, eta, ports)
    columns = list(chain.from_iterable(layers))
    nuisance = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    left_relations = sp.Matrix.hstack(*nuisance.T.nullspace()).T
    variables, full_equations, basepoint, _centre, _leaf = verifier.gauge_incidence(
        parent, left_relations, survivor
    )
    shifts, equations = verifier.symmetric_shifted_system(
        variables, full_equations, basepoint
    )
    names = [f"f{index}" for index in range(len(equations))]
    declarations = [
        f"poly {name}={singular_expression(equation, shifts)};"
        for name, equation in zip(names, equations, strict=True)
    ]
    lines = [
        f"ring r=(0,i),({','.join(str(shift) for shift in shifts)}),ds;",
        "minpoly=i2+1;",
        *declarations,
        f"ideal I={','.join(names)};",
        "matrix forward;",
        "ideal G=liftstd(I,forward);",
        "matrix reverse=lift(G,I);",
        "poly check;",
        "poly entry;",
        "int row;",
        "int column;",
        "intvec exponent;",
        "for (column=1;column<=ncols(forward);column++)",
        "{",
        "  check=0;",
        "  for (row=1;row<=nrows(forward);row++)",
        "  { check=check+I[row]*forward[row,column]; }",
        '  if (simplify(check-G[column],2)!=0) { print("ERROR|forward"); }',
        "}",
        "for (column=1;column<=ncols(reverse);column++)",
        "{",
        "  check=0;",
        "  for (row=1;row<=nrows(reverse);row++)",
        "  { check=check+G[row]*reverse[row,column]; }",
        '  if (simplify(check-I[column],2)!=0) { print("ERROR|reverse"); }',
        "}",
        'print("META|"+string(nrows(forward))+"|"+string(ncols(forward))+"|"',
        '      +string(nrows(reverse))+"|"+string(ncols(reverse)));',
        "for (column=1;column<=size(G);column++)",
        "{",
        "  entry=G[column];",
        "  while (entry!=0)",
        "  {",
        "    exponent=leadexp(entry);",
        '    print("BASIS|"+string(column)+"|"+string(leadcoef(entry))+"|"+string(exponent));',
        "    entry=entry-lead(entry);",
        "  }",
        "}",
        "for (row=1;row<=nrows(forward);row++)",
        "{",
        "  for (column=1;column<=ncols(forward);column++)",
        "  {",
        "    entry=forward[row,column];",
        "    while (entry!=0)",
        "    {",
        "      exponent=leadexp(entry);",
        '      print("FORWARD|"+string(row)+"|"+string(column)+"|"',
        '            +string(leadcoef(entry))+"|"+string(exponent));',
        "      entry=entry-lead(entry);",
        "    }",
        "  }",
        "}",
        "for (row=1;row<=nrows(reverse);row++)",
        "{",
        "  for (column=1;column<=ncols(reverse);column++)",
        "  {",
        "    entry=reverse[row,column];",
        "    while (entry!=0)",
        "    {",
        "      exponent=leadexp(entry);",
        '      print("REVERSE|"+string(row)+"|"+string(column)+"|"',
        '            +string(leadcoef(entry))+"|"+string(exponent));',
        "      entry=entry-lead(entry);",
        "    }",
        "  }",
        "}",
    ]
    return "\n".join(lines) + "\n"


def run_singular(program: str) -> str:
    direct = shutil.which("Singular")
    if direct:
        command = [direct, "-q"]
    elif shutil.which("wsl"):
        command = ["wsl", "bash", "--noprofile", "--norc", "-lc", "Singular -q"]
    else:
        raise SystemExit("Singular 4.x was not found directly or through WSL")
    completed = subprocess.run(
        command, input=program, text=True, capture_output=True, check=False
    )
    if completed.returncode or "ERROR|" in completed.stdout:
        raise SystemExit(
            f"Singular certificate generation failed:\n{completed.stdout}\n{completed.stderr}"
        )
    return completed.stdout


def sparse_term(coefficient: str, raw_exponents: str) -> list[object]:
    exponents = [int(value) for value in raw_exponents.split(",")]
    assert len(exponents) == 15
    sparse = [[index, power] for index, power in enumerate(exponents) if power]
    return [coefficient, sparse]


def parse(stdout: str) -> dict[str, object]:
    basis = [[] for _ in range(10)]
    forward: dict[tuple[int, int], list[list[object]]] = {}
    reverse: dict[tuple[int, int], list[list[object]]] = {}
    meta = None
    for raw_line in stdout.splitlines():
        fields = raw_line.strip().split("|")
        if not fields or not fields[0]:
            continue
        if fields[0] == "META":
            meta = [int(value) for value in fields[1:]]
        elif fields[0] == "BASIS":
            basis[int(fields[1]) - 1].append(sparse_term(fields[2], fields[3]))
        elif fields[0] in {"FORWARD", "REVERSE"}:
            target = forward if fields[0] == "FORWARD" else reverse
            key = (int(fields[1]) - 1, int(fields[2]) - 1)
            target.setdefault(key, []).append(sparse_term(fields[3], fields[4]))
    assert meta == [37, 10, 10, 37]

    def entries(values):
        return [
            {"row": row, "column": column, "terms": terms}
            for (row, column), terms in sorted(values.items())
        ]

    return {
        "format": "sparse-bidirectional-ideal-Qi-v1",
        "variable_order": [f"x{index}" for index in range(15)],
        "incidence_generator_count": 37,
        "basis_generator_count": 10,
        "basis": basis,
        "forward_shape": [37, 10],
        "forward": entries(forward),
        "reverse_shape": [10, 37],
        "reverse": entries(reverse),
    }


def main() -> None:
    data = parse(run_singular(certificate_program()))
    print(json.dumps(data, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
