#!/usr/bin/env python3
"""Explicit specialization-divisor extraction for the ninth component's H31.

Demonstration computation for the pointwise-specialization meta-theorem
(deliverable 2 of the P5 -> Delta_3 obligation-ledger session).

The verified generic theorem
P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md proves,
over the function field K = C(p,q) of the ninth (all-rank-one triangle)
pure-P_4 component, that the complete marked H31 fibre is empty:
  * frame q=1: binary marking projection = (1);
  * frames q=0,2,3: binary survivors confined to explicit sheets, and on
    each sheet the saturated ideal
      (14 mixed rows, selected one-marked 4x4 minors, w*A*B-1)
    is the unit ideal over K.

Function-field unit certificates specialize: if 1 lies in the ideal over
K = Frac(Q[p,q]), then the contraction J = I cap Q[p,q] of the same
ideal I over the polynomial ring Q[p,q] is NONZERO, and for every point
(p0,q0) with some g in J nonvanishing, the specialized system is
infeasible -- the fibre statement holds POINTWISE at (p0,q0).

This script computes those contractions J explicitly by elimination
over Q[p,q] (parameters as ring variables, not field parameters):

  A. chart-free frame systems (marking t FREE, certificate minors of the
     frame's killing modes adjoined, Rabinowitsch w*A*B-1):
     eliminating (t,z,w) yields J_q in Q[p,q].  A nonzero g in J_q
     certifies: at every (p0,q0) with g != 0, NO marking and NO
     extension in frame q satisfies mixed=0, A*B != 0, and the adjoined
     necessary rank-<=3 minors -- i.e. the frame-q H31 fibre is empty
     pointwise.  (Adjoining minors is sound: an H31 lift forces every
     one-marked mode map to have rank <= 3, hence every 4x4 minor of
     every mode to vanish; we adjoin a subset.)
     Frame q=1 needs no minors (binary stage already infeasible).

  B. per-sheet systems (sheet ideal adjoined as linear generators, so no
     denominators): eliminating (t,z,w) yields J_sheet in Q[p,q]
     (pointwise upgrade of the sheet Fitting certificates only).

Every Singular run is fail-closed under a hard timeout; a timeout or
error is recorded as null, never as success.  Before each ring-variable
elimination the same system is re-certified unit over K=(0,p,q) (also
fail-closed).

Output ledger: extract_p5_h31_ninth_explicit_divisors.json next to this
script.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

import sympy as sp  # noqa: E402

from verify_p5_h31_all_rank_one_triangle_component_generic_obstruction import (  # noqa: E402
    P,
    Q,
    family,
    marked_extension,
    mixed_system,
    shifted_basis,
    singular_polynomial,
)

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "extract_p5_h31_ninth_explicit_divisors.json"

UNIT_TIMEOUT = 420
ELIM_TIMEOUT = 520

# frame -> (certificate modes with minor row sets)
# Sound necessary conditions: an H31 lift forces rank<=3 of EVERY
# one-marked mode map; we adjoin the generic proof's certificate minors
# (union over that frame's survivor sheets).
FRAME_MINORS = {
    0: ((1, (0, 2, 3, 7)), (1, (0, 3, 6, 7))),
    1: (),
    2: ((3, (0, 2, 3, 7)), (3, (0, 2, 6, 7)), (3, (0, 2, 4, 7))),
    3: ((1, (0, 1, 4, 7)),),
}

# sheet name -> (frame, sheet ideal generators in t (polynomial!),
#                certificate minors)
SHEET_SYSTEMS = {
    "q0_t0_line": (
        0,
        ("t1", "t2", "t3"),
        ((1, (0, 2, 3, 7)), (1, (0, 3, 6, 7))),
    ),
    "q2_t0_line": (
        2,
        ("t1", "t3", "t2"),
        ((3, (0, 2, 3, 7)), (3, (0, 2, 6, 7))),
    ),
    "q2_t2_line": (
        2,
        ("t1", "t3", "t0"),
        ((3, (0, 2, 4, 7)), (3, (0, 2, 6, 7))),
    ),
    "q3_point": (
        3,
        (
            "(p*q+p+1)*t0+(q+1)",
            "t1",
            "t2",
            "(p*q+1)*t3+(p*q+p+1)",
        ),
        ((1, (0, 1, 4, 7)),),
    ),
}


def run_singular(program: str, timeout: float):
    try:
        completed = subprocess.run(
            (
                "timeout",
                "--signal=KILL",
                f"{timeout:.1f}s",
                "Singular",
                "-q",
            ),
            input=program,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout + 15,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout


def frame_equations(frame: int):
    """Build the chart-free system of the frame over Z[p,q,t,z,w]."""
    alpha, beta = family()
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_system(
        frame, alpha, marked_beta, extensions
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    first = (diagonal_a * extension)[0]
    second = (diagonal_b * extension)[0]
    equations.append(sp.expand(inverse * first * second - 1))
    minors = []
    for mode, rows in FRAME_MINORS[frame]:
        marked = marked_extension(
            frame, extension, alpha, marked_beta, mode
        )
        minors.append(
            sp.expand(marked[list(rows), :].det(method="berkowitz"))
        )
    return equations, minors, shifts, extensions, inverse


def unit_over_K(equations, minors, variables) -> bool | None:
    program = "\n".join(
        (
            "ring R=(0,p,q),("
            + ",".join(map(str, variables))
            + "),dp;",
            "ideal I="
            + ",".join(
                singular_polynomial(eq) for eq in equations + minors
            )
            + ";",
            "I=std(I);",
            "int unit=(reduce(1,I)==0);",
            '"CODEX_UNIT:"+string(unit);',
            "quit;",
        )
    )
    stdout = run_singular(program, UNIT_TIMEOUT)
    if stdout is None:
        return None
    hits = [
        line.strip()
        for line in stdout.splitlines()
        if line.startswith("CODEX_UNIT:")
    ]
    if hits == ["CODEX_UNIT:1"]:
        return True
    if hits == ["CODEX_UNIT:0"]:
        return False
    return None


def eliminate_to_params(equations, minors, variables, label):
    """Eliminate `variables` over Q[p,q]; return factored generators."""
    nvars = len(variables)
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + ",p,q),(dp("
            + str(nvars)
            + "),dp(2));",
            "ideal I="
            + ",".join(
                singular_polynomial(eq) for eq in equations + minors
            )
            + ";",
            "ideal J=eliminate(I,"
            + "*".join(map(str, variables))
            + ");",
            "J=interred(J);",
            '"CODEX_SIZE:"+string(size(J));',
            "int gi;",
            "for(gi=1;gi<=size(J);gi++)",
            "{",
            '  "CODEX_GEN:"+string(J[gi]);',
            "}",
            "if(size(J)>0)",
            "{",
            "  list F=factorize(J[1]);",
            "  int fi;",
            "  for(fi=1;fi<=size(F[1]);fi++)",
            "  {",
            '    "CODEX_FACTOR:"+string(F[1][fi])+"^"+string(F[2][fi]);',
            "  }",
            "}",
            "quit;",
        )
    )
    started = time.time()
    stdout = run_singular(program, ELIM_TIMEOUT)
    elapsed = round(time.time() - started, 1)
    if stdout is None:
        return {"status": "timeout_null", "seconds": elapsed}
    size = None
    generators = []
    factors = []
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("CODEX_SIZE:"):
            size = int(line.split(":", 1)[1])
        elif line.startswith("CODEX_GEN:"):
            generators.append(line.split(":", 1)[1])
        elif line.startswith("CODEX_FACTOR:"):
            factors.append(line.split(":", 1)[1])
    if size is None:
        return {"status": "parse_failure", "seconds": elapsed}
    if size == 0:
        # elimination ideal zero: no specialization divisor extracted
        return {
            "status": "zero_contraction",
            "seconds": elapsed,
            "note": (
                "J = I cap Q[p,q] returned zero: inconsistent with a "
                "verified unit certificate over K; recorded as failure"
            ),
        }
    return {
        "status": "extracted",
        "seconds": elapsed,
        "contraction_size": size,
        "generators": generators,
        "first_generator_factors": factors,
        "label": label,
    }


def main() -> None:
    ledger: dict = {
        "purpose": (
            "explicit specialization divisors for the ninth "
            "component's generic H31 theorem (pointwise upgrade)"
        ),
        "field_versus_ring": (
            "generic theorem over K=C(p,q); this extraction works over "
            "Q[p,q] with p,q as ring variables and eliminates all "
            "marking/extension/inverse variables"
        ),
        "frames": {},
        "sheets": {},
    }

    # A. chart-free frames
    for frame in (1, 0, 3, 2):
        equations, minors, shifts, extensions, inverse = (
            frame_equations(frame)
        )
        variables = tuple(shifts) + tuple(extensions) + (inverse,)
        record: dict = {"minors": [
            {"mode": mode, "rows": list(rows)}
            for mode, rows in FRAME_MINORS[frame]
        ]}
        unit = unit_over_K(equations, minors, variables)
        record["unit_over_K"] = unit
        if unit is True:
            record["elimination"] = eliminate_to_params(
                equations, minors, variables, f"frame_q{frame}"
            )
        else:
            record["elimination"] = {
                "status": "skipped_unit_not_certified",
            }
        ledger["frames"][f"q{frame}"] = record
        LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
        print(f"frame q{frame}: {record['elimination'].get('status')}",
              flush=True)

    # B. per-sheet fallbacks (only if the frame run did not extract)
    for name, (frame, sheet_ideal, minor_spec) in SHEET_SYSTEMS.items():
        frame_status = (
            ledger["frames"]
            .get(f"q{frame}", {})
            .get("elimination", {})
            .get("status")
        )
        if frame_status == "extracted":
            ledger["sheets"][name] = {
                "status": "subsumed_by_frame_extraction"
            }
            LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
            continue
        alpha, beta = family()
        shifts = sp.symbols("t0:4")
        extensions = sp.symbols("z0:8")
        inverse = sp.Symbol("w")
        marked_beta = shifted_basis(alpha, beta, shifts)
        mixed, diagonal_a, diagonal_b = mixed_system(
            frame, alpha, marked_beta, extensions
        )
        extension = sp.Matrix(extensions)
        equations = list(mixed * extension)
        first = (diagonal_a * extension)[0]
        second = (diagonal_b * extension)[0]
        equations.append(sp.expand(inverse * first * second - 1))
        equations.extend(sp.sympify(g.replace("^", "**"))
                         for g in sheet_ideal)
        minors = []
        for mode, rows in minor_spec:
            marked = marked_extension(
                frame, extension, alpha, marked_beta, mode
            )
            minors.append(
                sp.expand(
                    marked[list(rows), :].det(method="berkowitz")
                )
            )
        variables = tuple(shifts) + tuple(extensions) + (inverse,)
        record = {
            "frame": frame,
            "sheet_ideal": list(sheet_ideal),
            "minors": [
                {"mode": mode, "rows": list(rows)}
                for mode, rows in minor_spec
            ],
        }
        unit = unit_over_K(equations, minors, variables)
        record["unit_over_K"] = unit
        if unit is True:
            record["elimination"] = eliminate_to_params(
                equations, minors, variables, f"sheet_{name}"
            )
        else:
            record["elimination"] = {
                "status": "skipped_unit_not_certified",
            }
        ledger["sheets"][name] = record
        LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
        print(f"sheet {name}: {record['elimination'].get('status')}",
              flush=True)

    extracted = [
        key
        for key, rec in ledger["frames"].items()
        if rec.get("elimination", {}).get("status") == "extracted"
    ]
    ledger["frames_with_explicit_divisor"] = extracted
    ledger["all_four_frames_extracted"] = len(extracted) == 4
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
    print("done:", extracted, flush=True)


if __name__ == "__main__":
    main()
