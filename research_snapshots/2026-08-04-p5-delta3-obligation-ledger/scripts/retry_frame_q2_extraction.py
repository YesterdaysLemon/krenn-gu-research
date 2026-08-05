#!/usr/bin/env python3
"""Retry the frame-q2 chart-free extraction with alternative strategies.

Strategy A: slimgb pre-pass under (dp(13),dp(2)), then eliminate.
Strategy B: two-stage elimination -- eliminate (z,w) first (keeping t),
            then eliminate t from the contraction.
Each fail-closed under its own hard timeout; results appended to
retry_frame_q2_extraction.json.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

import sympy as sp  # noqa: E402

from verify_p5_h31_all_rank_one_triangle_component_generic_obstruction import (  # noqa: E402
    family,
    marked_extension,
    mixed_system,
    shifted_basis,
    singular_polynomial,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "retry_frame_q2_extraction.json"

MINORS = ((3, (0, 2, 3, 7)), (3, (0, 2, 6, 7)), (3, (0, 2, 4, 7)))


def run_singular(program: str, timeout: float):
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


def build_system():
    alpha, beta = family()
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diag_a, diag_b = mixed_system(
        2, alpha, marked_beta, extensions
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    a_val = (diag_a * extension)[0]
    b_val = (diag_b * extension)[0]
    equations.append(sp.expand(inverse * a_val * b_val - 1))
    for mode, rows in MINORS:
        marked = marked_extension(
            2, extension, alpha, marked_beta, mode
        )
        equations.append(
            sp.expand(marked[list(rows), :].det(method="berkowitz"))
        )
    return equations, shifts, extensions, inverse


def parse(stdout):
    if stdout is None:
        return None
    size = None
    gens = []
    factors = []
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("CODEX_SIZE:"):
            size = int(line.split(":", 1)[1])
        elif line.startswith("CODEX_GEN:"):
            gens.append(line.split(":", 1)[1])
        elif line.startswith("CODEX_FACTOR:"):
            factors.append(line.split(":", 1)[1])
    if size is None:
        return None
    return {"size": size, "generators": gens, "factors": factors}


def strategy_a(equations, shifts, extensions, inverse, timeout):
    variables = tuple(shifts) + tuple(extensions) + (inverse,)
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + ",p,q),(dp(13),dp(2));",
            "ideal I="
            + ",".join(map(singular_polynomial, equations))
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
    started = time.time()
    result = parse(run_singular(program, timeout))
    elapsed = round(time.time() - started, 1)
    return result, elapsed


def strategy_b(equations, shifts, extensions, inverse, timeout):
    zw = tuple(extensions) + (inverse,)
    variables = zw + tuple(shifts)
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + ",p,q),(dp(9),dp(4),dp(2));",
            "ideal I="
            + ",".join(map(singular_polynomial, equations))
            + ";",
            "ideal J1=eliminate(I," + "*".join(map(str, zw)) + ");",
            '"CODEX_STAGE1:"+string(size(J1));',
            "ideal J=eliminate(J1,"
            + "*".join(map(str, shifts))
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
    started = time.time()
    result = parse(run_singular(program, timeout))
    elapsed = round(time.time() - started, 1)
    return result, elapsed


def main() -> None:
    equations, shifts, extensions, inverse = build_system()
    report = {}
    result, elapsed = strategy_a(
        equations, shifts, extensions, inverse, 900.0
    )
    report["strategy_a_slimgb"] = {
        "seconds": elapsed,
        "result": result if result else "timeout_null",
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("A:", report["strategy_a_slimgb"], flush=True)
    if not result:
        result, elapsed = strategy_b(
            equations, shifts, extensions, inverse, 900.0
        )
        report["strategy_b_two_stage"] = {
            "seconds": elapsed,
            "result": result if result else "timeout_null",
        }
        OUT.write_text(json.dumps(report, indent=2) + "\n")
        print("B:", report["strategy_b_two_stage"], flush=True)


if __name__ == "__main__":
    main()
