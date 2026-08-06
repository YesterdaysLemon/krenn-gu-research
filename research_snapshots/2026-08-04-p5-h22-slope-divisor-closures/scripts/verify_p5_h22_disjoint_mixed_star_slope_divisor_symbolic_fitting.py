#!/usr/bin/env python3
"""FINAL DESIGN: chart-free ternary Fitting certificates on slope
DIVISORS of the disjoint mixed-star weighted-H22 theorem, with the
slope r kept as a ring VARIABLE and the divisor polynomial adjoined to
the ideal.  All heavy polynomial algebra is done by Singular; sympy
only replays the repo verifier's y-eliminated reduced system
(build_direction, symbolic r) and emits it.

Cases:
  r0      : divisor r=0 on the D_23 pencil; mode-0 minors
            (0,1,3,7),(0,1,5,7)  [the H31 q=2 frame shadow];
  coupled : divisor a*f*(r+1)-(r-1)=0 on the D_01 pencil; mode-3
            minors (0,2,4,7),(0,4,5,7)  [where the generic mode-0
            certificate provably fails].

Certificate per case, over (0,a,b,f) in (phi,r,t0..t3,x0..x3,w):

  ideal( divisor, Phi, G(t)x rows, det Dm[rows_1], det Dm[rows_2],
         w*A(x)*B(x)-1 ) == (1),

where G is the generic theorem's y-eliminated 10x4 system (valid on
the divisor because each of the four single-1-word own-extension
denominators is certified nonzero on {Phi=0, divisor=0} by an
auxiliary unit-ideal certificate in (phi,r)), Dm are the mode-m
one-marked 4x4 matrices on the kernel substitution (entries computed
by Singular as 3x3 permanents of the extended rows with one column
deleted -- the mode row is a coordinate basis vector), and A,B are the
two diagonal coefficients (4x4 permanents, computed by Singular).

Unit ideal => on the whole slope divisor, every genuine binary
survivor at every marking has a rank-four mode-m one-marked
contraction => no ternary H22 lift => the divisor is closed at
ternary level over the generic component point.

Timeout 550 s per Singular run; timeouts recorded as NULL results."""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "claims" / "p5" / "h22" / "disjoint-mixed-star"))

import sympy as sp

import verify_p5_h22_disjoint_mixed_star_component_generic_obstruction as V

OUT = Path(__file__).resolve().parent.parent
TIMEOUT = 550
BITS3 = tuple(itertools.product((0, 1), repeat=3))

a, b, f, phi, r = V.a, V.b, V.f, V.phi, V.r
T, X = V.T, V.X
PHI = V.PHI

PERM_PROCS = """
proc rowperm3(matrix R1, matrix R2, matrix R3,
              int c1, int c2, int c3) {
  return( R1[1,c1]*(R2[1,c2]*R3[1,c3]+R2[1,c3]*R3[1,c2])
        + R1[1,c2]*(R2[1,c1]*R3[1,c3]+R2[1,c3]*R3[1,c1])
        + R1[1,c3]*(R2[1,c1]*R3[1,c2]+R2[1,c2]*R3[1,c1]) );
}
proc rowperm4(matrix R1, matrix R2, matrix R3, matrix R4) {
  return( R1[1,1]*rowperm3(R2,R3,R4,2,3,4)
        + R1[1,2]*rowperm3(R2,R3,R4,1,3,4)
        + R1[1,3]*rowperm3(R2,R3,R4,1,2,4)
        + R1[1,4]*rowperm3(R2,R3,R4,1,2,3) );
}
"""


def emit_row(row):
    return ",".join(V.sing(entry) for entry in row)


def certify(case, direction, divisor, mode, minor_rows):
    import os

    dump = os.environ.get("DUMP_PROGRAM")
    data = V.build_direction(direction)
    # (i) denominators are nonzero on {Phi=0, divisor=0}: auxiliary
    # unit-ideal certificates in variables (phi, r).  In dump mode
    # these blocks are prepended to the single dumped program (one
    # Singular session, separate rings) instead of run here.
    denominator_certs = {}
    denominator_blocks = []
    for m, den in sorted(data["denominators"].items()):
        block = [
            f"ring Rden{m}=(0,a,b,f),(phi,r),dp;",
            "option(redSB);",
            f"ideal Iden{m}={V.sing(PHI)},{V.sing(divisor)},"
            f"{V.sing(den)};",
            f"Iden{m}=std(Iden{m});",
            f'"CODEX_DEN:{m}:"+string(reduce(1,Iden{m})==0);',
        ]
        if dump:
            denominator_blocks.extend(block)
            denominator_certs[str(m)] = (
                "checked inside the dumped program (CODEX_DEN marker)"
            )
            continue
        completed = subprocess.run(
            ("Singular", "-q"), input="\n".join(block + ["quit;"]),
            text=True, capture_output=True, timeout=120,
        )
        assert f"CODEX_DEN:{m}:1" in completed.stdout, (
            m, completed.stdout[-400:], completed.stderr[-200:]
        )
        denominator_certs[str(m)] = "unit on {Phi=0, divisor=0}"

    # (ii) the main certificate; all algebra in Singular.
    others = tuple(mm for mm in range(4) if mm != mode)
    used_words = sorted({
        index for selected in minor_rows for index in selected
    })
    lines = [
        "ring R=(0,a,b,f),(phi,r,t0,t1,t2,t3,"
        + ",".join(str(x) for x in X) + ",w),dp;",
        "option(redSB);",
        PERM_PROCS,
        # extended rows (4 columns: 3 weighted + kernel-substituted
        # extension), exactly the repo verifier's alpha_rows/beta_rows
    ]
    for mm in range(4):
        lines.append(
            f"matrix AR{mm}[1][4]={emit_row(data['alpha_rows'][mm])};"
        )
        lines.append(
            f"matrix BR{mm}[1][4]={emit_row(data['beta_rows'][mm])};"
        )
    # G rows
    g_polys = []
    for grow in data["g_matrix"]:
        g_polys.append(
            "+".join(
                f"({V.sing(entry)})*{xv}"
                for entry, xv in zip(grow, X)
            )
        )
    lines.append("ideal I=" + ",".join(g_polys) + ";")
    lines.append(f"I=I,{V.sing(PHI)};")
    lines.append(f"I=I,{V.sing(divisor)};")
    # one-marked matrices for the selected words: entry(word, col) =
    # 3x3 permanent of the three chosen extended rows with column col
    # deleted (the mode row is a coordinate basis vector).
    for word_index in used_words:
        bits = BITS3[word_index]
        chosen = [
            (f"BR{mm}" if bit else f"AR{mm}")
            for mm, bit in zip(others, bits)
        ]
        triple = ",".join(chosen)
        for col in range(1, 5):
            keep = [c for c in range(1, 5) if c != col]
            keeps = ",".join(str(c) for c in keep)
            lines.append(
                f"poly e{word_index}c{col}="
                f"rowperm3({triple},{keeps});"
            )
    for index, selected in enumerate(minor_rows):
        rows_ = []
        for word_index in selected:
            rows_.append(
                ",".join(
                    f"e{word_index}c{col}" for col in range(1, 5)
                )
            )
        lines.append(
            f"matrix D{index}[4][4]=" + ",".join(rows_) + ";"
        )
        lines.append(f"I=I,det(D{index});")
    lines.extend([
        "poly AB=rowperm4(AR0,AR1,AR2,AR3)"
        "*rowperm4(BR0,BR1,BR2,BR3);",
        "I=I,w*AB-1;",
        "I=std(I);",
        f'"CODEX_RESULT:{case}:"+string(reduce(1,I)==0);',
        "quit;",
    ])
    program = "\n".join(denominator_blocks + lines)
    if dump:
        Path(dump).write_text(program)
        return {
            "case": case,
            "direction": direction,
            "divisor": str(divisor),
            "mode": mode,
            "minor_rows": [list(m_) for m_ in minor_rows],
            "denominator_certificates_on_divisor": denominator_certs,
            "status": {"result": "program-dumped", "path": dump},
        }
    try:
        completed = subprocess.run(
            ("Singular", "-q"), input=program, text=True,
            capture_output=True, timeout=TIMEOUT,
        )
        if completed.returncode != 0 or completed.stderr.strip():
            status = {
                "result": "error",
                "stderr": completed.stderr[-800:],
                "stdout": completed.stdout[-400:],
            }
        elif f"CODEX_RESULT:{case}:1" in completed.stdout:
            status = {"result": "unit"}
        else:
            status = {
                "result": "not-unit",
                "stdout": completed.stdout[-800:],
            }
    except subprocess.TimeoutExpired:
        subprocess.run(("pkill", "-9", "Singular"), check=False)
        status = {"result": "timeout-null", "timeout_s": TIMEOUT}
    return {
        "case": case,
        "direction": direction,
        "divisor": str(divisor),
        "mode": mode,
        "minor_rows": [list(m_) for m_ in minor_rows],
        "denominator_certificates_on_divisor": denominator_certs,
        "status": status,
    }


def main() -> None:
    started = time.monotonic()
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    results = {}
    if which in ("r0", "both"):
        results["d23_r0"] = certify(
            "r0", "23", r, 0, ((0, 1, 3, 7), (0, 1, 5, 7)),
        )
        print(json.dumps(results["d23_r0"]["status"]))
        sys.stdout.flush()
    if which in ("coupled", "both"):
        results["d01_coupled"] = certify(
            "coupled", "01",
            sp.expand(a * f * (r + 1) - (r - 1)), 3,
            ((0, 2, 4, 7), (0, 4, 5, 7)),
        )
        print(json.dumps(results["d01_coupled"]["status"]))
    results["elapsed_seconds"] = round(time.monotonic() - started, 3)
    path = OUT / "special_slope_reduced_fitting_results.json"
    merged = {}
    if path.exists():
        merged = json.loads(path.read_text())
    merged.update(results)
    path.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
