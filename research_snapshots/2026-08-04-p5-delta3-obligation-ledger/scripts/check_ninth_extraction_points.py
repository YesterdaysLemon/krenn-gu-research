#!/usr/bin/env python3
"""Point checks for the ninth-component H31 specialization divisors.

1. WITNESS check: at the rational point (p,q)=(-1,3) ON the newly
   extracted frame-q1 curve pq-p+2=0 (and OFF every divisor displayed
   in the theorem document), decide by exact Groebner whether the
   frame-q1 binary-survivor system {14 mixed rows, w*A*B-1} is
   feasible.  Feasible = the curve carries genuine binary survivors =
   the new obligation is real, not a certificate artifact.
   Also test a second point (5,?) on the curve: p=5 -> q=3/5.

2. REPLAY check: at (p,q)=(2,1), which lies OFF all extracted
   contraction generators and off all displayed divisors, replay each
   frame's chart-free system (with certificate minors) as the unit
   ideal over Q -- the pointwise emptiness the specialization theorem
   asserts, verified independently at the point.

Fail-closed: any Singular failure/timeout is recorded as null and the
check reports it; nothing is claimed on a null.
"""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
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
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "check_ninth_extraction_points.json"

FRAME_MINORS = {
    0: ((1, (0, 2, 3, 7)), (1, (0, 3, 6, 7))),
    1: (),
    2: ((3, (0, 2, 3, 7)), (3, (0, 2, 6, 7)), (3, (0, 2, 4, 7))),
    3: ((1, (0, 1, 4, 7)),),
}

DISPLAYED = [P, Q, Q + 1, P - 1, P * Q + 1, P * Q - P + 1,
             P * Q + P + 1]


def run_singular(program: str, timeout: float = 300.0):
    try:
        completed = subprocess.run(
            ("timeout", "--signal=KILL", f"{timeout:.1f}s",
             "Singular", "-q"),
            input=program,
            text=True,
            capture_output=True,
            timeout=timeout + 10,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout


def poly_str(expression) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def frame_system_at_point(frame, p0, q0, with_minors):
    alpha, beta = family()
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diag_a, diag_b = mixed_system(
        frame, alpha, marked_beta, extensions
    )
    extension = sp.Matrix(extensions)
    equations = [
        eq.subs({P: p0, Q: q0}) for eq in (mixed * extension)
    ]
    a_val = (diag_a * extension)[0].subs({P: p0, Q: q0})
    b_val = (diag_b * extension)[0].subs({P: p0, Q: q0})
    equations.append(sp.expand(inverse * a_val * b_val - 1))
    if with_minors:
        for mode, rows in FRAME_MINORS[frame]:
            marked = marked_extension(
                frame, extension, alpha, marked_beta, mode
            )
            det = marked[list(rows), :].det(method="berkowitz")
            equations.append(
                sp.expand(det.subs({P: p0, Q: q0}))
            )
    variables = tuple(shifts) + tuple(extensions) + (inverse,)
    return equations, variables


def groebner_feasible(equations, variables):
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "ideal I=" + ",".join(map(poly_str, equations)) + ";",
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
        return False  # unit ideal -> infeasible
    if hits == ["CODEX_UNIT:0"]:
        return True  # feasible
    return None


def survivor_marking_locus(frame, p0, q0):
    """Eliminate (z,w) at the point to see the survivor markings."""
    equations, variables = frame_system_at_point(
        frame, p0, q0, with_minors=False
    )
    shifts = variables[:4]
    others = variables[4:]
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, others + shifts))
            + "),(dp(9),dp(4));",
            "ideal I=" + ",".join(map(poly_str, equations)) + ";",
            "ideal J=eliminate(I,"
            + "*".join(map(str, others))
            + ");",
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
    gens = [ln.strip().split(":", 1)[1]
            for ln in stdout.splitlines()
            if ln.startswith("CODEX_GEN:")]
    return gens


def main() -> None:
    report: dict = {}

    # 1. WITNESS on the new curve pq-p+2=0.
    witness_points = [
        (sp.Integer(-1), sp.Integer(3)),
        (sp.Integer(5), sp.Rational(3, 5)),
    ]
    report["witness_on_new_curve"] = []
    for p0, q0 in witness_points:
        assert sp.simplify(p0 * q0 - p0 + 2) == 0
        displayed_values = {
            str(d): str(sp.simplify(d.subs({P: p0, Q: q0})))
            for d in DISPLAYED
        }
        off_displayed = all(
            sp.simplify(d.subs({P: p0, Q: q0})) != 0
            for d in DISPLAYED
        )
        equations, variables = frame_system_at_point(
            1, p0, q0, with_minors=False
        )
        feasible = groebner_feasible(equations, variables)
        entry = {
            "point": [str(p0), str(q0)],
            "on_curve_pq_minus_p_plus_2": True,
            "off_all_displayed_divisors": bool(off_displayed),
            "displayed_divisor_values": displayed_values,
            "frame_q1_binary_survivor_feasible": feasible,
        }
        if feasible:
            entry["survivor_marking_locus_generators"] = (
                survivor_marking_locus(1, p0, q0)
            )
            # and: is the FULL system with a ternary certificate
            # empty there?  Try adjoining each single mode's
            # [0,...]-minors is out of scope here; record feasibility
            # only (the new curve is an honest ternary obligation).
        report["witness_on_new_curve"].append(entry)
        OUT.write_text(json.dumps(report, indent=2) + "\n")
        print("witness", (str(p0), str(q0)), "->", feasible,
              flush=True)

    # 2. REPLAY at a point off everything.
    p0, q0 = sp.Integer(2), sp.Integer(1)
    replay = {"point": [str(p0), str(q0)], "frames": {}}
    for frame in range(4):
        equations, variables = frame_system_at_point(
            frame, p0, q0, with_minors=True
        )
        feasible = groebner_feasible(equations, variables)
        replay["frames"][f"q{frame}"] = {
            "system": (
                "mixed + w*A*B-1"
                + ("" if frame == 1 else " + certificate minors")
            ),
            "feasible": feasible,
            "pointwise_empty_replayed": feasible is False,
        }
        print("replay frame", frame, "-> feasible:", feasible,
              flush=True)
    report["replay_off_all_divisors"] = replay
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("done", flush=True)


if __name__ == "__main__":
    main()
