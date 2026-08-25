#!/usr/bin/env python3
"""Regenerate the optional exact Singular atlas for the GLD71 one-word gate.

The primary verifier is the portable proof replay.  This generator feeds the
same pinned syndrome equations to a second computer-algebra implementation
and retains all 108 ordered choices of two binary-visible leaves.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import shutil
import subprocess
from itertools import combinations, product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
PRIMARY = HERE / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)


def load_primary():
    spec = importlib.util.spec_from_file_location("gld71_primary", PRIMARY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def singular_expression(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def singular_program() -> tuple[str, int]:
    primary = load_primary()
    parent = primary.load_parent()
    supports = tuple(
        primary.SPARSE_RELATIONS[index] for index in primary.ATLAS_RELATION_INDICES
    )
    variables, (centre, b, c, d), equations = primary.incidence_equations(
        parent, supports
    )
    leaf_groups = (b, c, d)
    lines = [
        "ring r=0,(" + ",".join(str(variable) for variable in variables) + "),dp;",
        "option(redSB);",
        "ideal F="
        + ",".join(singular_expression(equation) for equation in equations)
        + ";",
        "int passed=0;",
        "int attempted=0;",
        "ideal I,G;",
    ]
    chart_count = 0
    for binary_pair in combinations(range(3), 2):
        third = next(index for index in range(3) if index not in binary_pair)
        for first_pivot, second_pivot, third_pivot, centre_pivot in product(
            range(2), range(2), range(3), range(3)
        ):
            pivots = (
                centre[centre_pivot],
                leaf_groups[binary_pair[0]][first_pivot],
                leaf_groups[binary_pair[1]][second_pivot],
                leaf_groups[third][third_pivot],
            )
            lines.extend(
                [
                    "attempted=attempted+1;",
                    "I=F," + ",".join(f"{pivot}-1" for pivot in pivots) + ";",
                    "G=std(I);",
                    "if (reduce(1,G)==0) { passed=passed+1; }",
                ]
            )
            chart_count += 1
    lines.extend(
        [
            'print("ATLAS_COUNTS");',
            "attempted;",
            "passed;",
            'print("DONE");',
            "quit;",
        ]
    )
    return "\n".join(lines) + "\n", chart_count


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
            "-c",
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
    return completed.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--print-program",
        action="store_true",
        help="print the generated Singular source instead of executing it",
    )
    args = parser.parse_args()
    program, expected_charts = singular_program()
    digest = hashlib.sha256(program.encode("utf-8")).hexdigest()
    print("program_sha256", digest)
    print("expected_charts", expected_charts)
    if args.print_program:
        print(program, end="")
        return
    output = run_singular(program)
    compact = [line.strip() for line in output.splitlines() if line.strip()]
    marker = compact.index("ATLAS_COUNTS")
    attempted = int(compact[marker + 1])
    passed = int(compact[marker + 2])
    assert compact[marker + 3] == "DONE"
    assert attempted == passed == expected_charts == 108
    print("singular_atlas", attempted, passed)
    print("GLD71 optional Singular atlas: PASS")


if __name__ == "__main__":
    main()
