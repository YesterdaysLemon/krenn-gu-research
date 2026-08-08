#!/usr/bin/env python3
"""Bonus extraction: explicit specialization divisors, tenth component H31.

The tenth (coincident-support) component's generic H31 theorem
(P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md) proves,
over K = C(b,e,m,c) at the k=1 gauge:
  frames q=0,1: A_q == 0 identically (dead at EVERY chart point);
  frames q=2,3: unit binary marking projection (13) -- no survivors.

The corpus records that "full survivor-locus eliminations with
parameters as ring variables exceeded the 550-second budget"
(timeout-nulls).  This script retries exactly that extraction with the
slimgb pre-pass that unblocked the ninth component's frame q2:
for q in {2,3}, eliminate (z,w,t) from

    { 14 mixed word forms,  A_q(z) - 1,  w*B_q(t,z) - 1 }

over Q[b,e,m,c] (ring variables).  A successful contraction
J_q ⊂ Q[b,e,m,c] gives: at every chart point OFF V(J_q), frame q has
no genuine binary survivor for any marking -- pointwise.  Combined
with the identity-dead frames q=0,1 (pointwise everywhere), that
makes the complete marked H31 fibre of the tenth component pointwise
empty off V(J_2) ∪ V(J_3) -- upgrading the generic theorem.

Fail-closed: hard timeouts; nulls recorded, nothing claimed on null.
Ledger: extract_p5_h31_tenth_explicit_divisors.json.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "extract_p5_h31_tenth_explicit_divisors.json"

spec = importlib.util.spec_from_file_location(
    "tenth_verifier",
    REPO / "claims/p5/h31/coincident-support/verify_p5_h31_coincident_support_component_generic_obstruction.py",
)
tenth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tenth)

import sympy as sp  # noqa: E402

TIMEOUT = 840.0


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


def extract(q: int) -> dict:
    alpha, beta = tenth.concentrated_basis(sp.Integer(1))
    betat = tenth.marked_beta(alpha, beta)
    coeffs = tenth.h31_word_coefficients(q, alpha, betat)
    equations = [tenth.word_form(coeffs, wd) for wd in tenth.MIXED]
    equations.append(
        tenth.word_form(coeffs, (0, 0, 0, 0)) - 1
    )
    equations.append(
        tenth.W * tenth.word_form(coeffs, (1, 1, 1, 1)) - 1
    )
    variables = tenth.Z + (tenth.W,) + tenth.T
    program = "\n".join(
        (
            "ring R=0,("
            + ",".join(map(str, variables))
            + ",b,e,m,c),(dp(" + str(len(variables)) + "),dp(4));",
            "ideal I="
            + ",".join(tenth.singular_str(x) for x in equations)
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
    stdout = run_singular(program, TIMEOUT)
    elapsed = round(time.time() - started, 1)
    if stdout is None:
        return {"status": "timeout_null", "seconds": elapsed}
    gens, factors, size = [], [], None
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("CODEX_SIZE:"):
            size = int(line.split(":", 1)[1])
        elif line.startswith("CODEX_GEN:"):
            gens.append(line.split(":", 1)[1])
        elif line.startswith("CODEX_FACTOR:"):
            factors.append(line.split(":", 1)[1])
    if size is None:
        return {"status": "parse_failure", "seconds": elapsed}
    if size == 0:
        return {"status": "zero_contraction_failure",
                "seconds": elapsed}
    return {
        "status": "extracted",
        "seconds": elapsed,
        "generators": gens,
        "first_generator_factors": factors,
    }


def main() -> None:
    report = {
        "component": "tenth (coincident-support), H31, k=1 gauge",
        "frames_q01": (
            "identity-dead at every chart point (verified doc (8)); "
            "no extraction needed"
        ),
        "frames": {},
    }
    for q in (2, 3):
        report["frames"][f"q{q}"] = extract(q)
        OUT.write_text(json.dumps(report, indent=2) + "\n")
        print(f"q{q}:", report["frames"][f"q{q}"].get("status"),
              flush=True)


if __name__ == "__main__":
    main()
