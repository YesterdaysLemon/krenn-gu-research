#!/usr/bin/env python3
"""Generate the optional Singular lift certificates for GLD74.

Replay does not require Singular.  This generator reconstructs the full
affine quotient system through the primary verifier, asks Singular 4.x for
liftstd unit identities, checks the lifts inside Singular, and writes only
the sparse exact multipliers needed by the portable verifiers.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

import verify_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension as primary

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / (
    "four_root_torus_star_gaussian_survivor_full_coefficient_fibre_"
    "first_response_nonextension_certificates.json"
)


def singular_expression(expression: sp.Expr) -> str:
    return sp.sstr(sp.expand(expression)).replace("**", "^").replace("I", "i")


def certificate_block(name: str, ideal_name: str, equations) -> list[str]:
    rendered = ",".join(singular_expression(equation) for equation in equations)
    return [
        f"ideal {ideal_name}={rendered};",
        "matrix transform;",
        f"ideal basis=liftstd({ideal_name},transform);",
        "int unit_column=0;",
        "int generator;",
        "for (generator=1;generator<=size(basis);generator++)",
        "{",
        "  if ((basis[generator]!=0)&&(deg(basis[generator])==0))",
        "  { unit_column=generator; }",
        "}",
        "if (unit_column==0)",
        f'{{ print("ERROR|nonunit|{name}"); }}',
        "poly unit_value=basis[unit_column];",
        "poly check=0;",
        "poly multiplier;",
        "intvec exponent;",
        "for (generator=1;generator<=nrows(transform);generator++)",
        "{",
        "  multiplier=transform[generator,unit_column]/unit_value;",
        f"  check=check+{ideal_name}[generator]*multiplier;",
        "}",
        "if (simplify(check-1,2)!=0)",
        f'{{ print("ERROR|bad_lift|{name}"); }}',
        f'print("CASE|{name}|"+string(nrows(transform))+"|"+string(size({ideal_name})));',
        "for (generator=1;generator<=nrows(transform);generator++)",
        "{",
        "  multiplier=transform[generator,unit_column]/unit_value;",
        "  while (multiplier!=0)",
        "  {",
        "    exponent=leadexp(multiplier);",
        '    print("TERM|"+string(generator)+"|"+string(leadcoef(multiplier))',
        '          +"|"+string(exponent));',
        "    multiplier=multiplier-lead(multiplier);",
        "  }",
        "}",
        "kill transform,basis,unit_column,generator,unit_value,check,multiplier,exponent;",
    ]


def singular_program() -> str:
    data = primary.quotient_forms()
    systems = primary.polynomial_systems(data["forms"])
    lines = [
        f"ring r=(0,i),({','.join(primary.VARIABLES)}),dp;",
        "minpoly=i2+1;",
        "option(redSB);",
    ]
    lines.extend(certificate_block("z0_nonzero", "I", systems["z0_nonzero"]))
    lines.extend(
        certificate_block("z0_zero_z1_nonzero", "J", systems["z0_zero_z1_nonzero"])
    )
    return "\n".join(lines) + "\n"


def run_singular(program: str) -> str:
    direct = shutil.which("Singular")
    if direct:
        command = [direct, "-q"]
    elif shutil.which("wsl"):
        command = [
            "wsl",
            "bash",
            "--noprofile",
            "--norc",
            "-lc",
            "Singular -q",
        ]
    else:
        raise SystemExit("Singular 4.x was not found directly or through WSL")
    completed = subprocess.run(
        command,
        input=program,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise SystemExit(
            f"Singular failed with code {completed.returncode}:\n"
            f"{completed.stdout}\n{completed.stderr}"
        )
    if "ERROR|" in completed.stdout:
        raise SystemExit(completed.stdout)
    return completed.stdout


def parse_output(stdout: str) -> dict[str, object]:
    expected = {"z0_nonzero", "z0_zero_z1_nonzero"}
    charts = {}
    profiles = {}
    current = None
    for raw_line in stdout.splitlines():
        fields = raw_line.strip().split("|")
        if not fields[0]:
            continue
        if fields[0] == "CASE":
            name = fields[1]
            if name not in expected or name in charts:
                raise SystemExit(f"unexpected certificate case: {raw_line}")
            original_rows = int(fields[2])
            stored_generators = int(fields[3])
            if original_rows != 130:
                raise SystemExit(f"bad lift row count: {raw_line}")
            current = [[] for _ in range(130)]
            charts[name] = current
            profiles[name] = {
                "original_generator_rows": original_rows,
                "nonzero_ideal_generators": stored_generators,
            }
        elif fields[0] == "TERM":
            if current is None:
                raise SystemExit("TERM appeared before CASE")
            generator_index = int(fields[1]) - 1
            if not 0 <= generator_index < 130:
                raise SystemExit(f"bad generator index: {raw_line}")
            exponent = [int(value) for value in fields[3].split(",")]
            if len(exponent) != len(primary.VARIABLES):
                raise SystemExit(f"bad exponent length: {raw_line}")
            sparse = [[index, power] for index, power in enumerate(exponent) if power]
            current[generator_index].append([fields[2], sparse])
    if set(charts) != expected:
        raise SystemExit(
            f"certificate chart mismatch: expected={sorted(expected)}, "
            f"actual={sorted(charts)}"
        )
    return {
        "format": "sparse-nullstellensatz-Qi-v1",
        "variable_order": list(primary.VARIABLES),
        "generator_order": "quotient_row_then_equation",
        "profiles": profiles,
        "charts": charts,
    }


def main() -> None:
    data = parse_output(run_singular(singular_program()))
    OUTPUT.write_text(
        json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    term_counts = {
        name: sum(len(multiplier) for multiplier in chart)
        for name, chart in data["charts"].items()
    }
    print(f"wrote {OUTPUT}")
    print(f"multiplier_terms={term_counts}")


if __name__ == "__main__":
    main()
