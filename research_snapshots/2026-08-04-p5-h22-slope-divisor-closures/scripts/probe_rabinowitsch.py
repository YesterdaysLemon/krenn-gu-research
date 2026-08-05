#!/usr/bin/env python3
"""Probe: Singular Rabinowitsch binary-emptiness certificates at special
slopes.  ideal(14 mixed rows, Phi, w*A*B-1) == (1) proves that the
pencil has NO genuine binary survivor for ANY marking t at that slope,
over the component function field.

Usage: probe_rabinowitsch.py <direction> <slope> [timeout_s]
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sympy as sp

from slope_common import PHI, T, Z, build_system, sing


def main():
    direction = sys.argv[1]
    slope = sp.Integer(sys.argv[2])
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 550
    data = build_system(direction, slope)
    rows = data["rows"]
    lin = []
    for bits, row in rows.items():
        if bits in ((0, 0, 0, 0), (1, 1, 1, 1)):
            continue
        lin.append(sum(c * zv for c, zv in zip(row, Z)))
    A = sum(c * zv for c, zv in zip(data["A"], Z))
    B = sum(c * zv for c, zv in zip(data["B"], Z))
    w = sp.Symbol("w")
    variables = "phi," + ",".join(str(t) for t in T) + "," + ",".join(
        str(z) for z in Z
    ) + ",w"
    program = "\n".join(
        [
            f"ring R=(0,a,b,f),({variables}),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(sing(e) for e in lin) + ";",
            f"I=I,{sing(PHI)};",
            f"I=I,w*({sing(A)})*({sing(B)})-1;",
            "I=std(I);",
            '"CODEX_RESULT:"+string(reduce(1,I)==0);',
            "quit;",
        ]
    )
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ("Singular", "-q"),
            input=program,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        print(
            f"D_{direction} slope {slope}: TIMEOUT after {timeout}s "
            "(null result)"
        )
        return
    elapsed = time.monotonic() - started
    out = completed.stdout.strip()
    print(
        f"D_{direction} slope {slope}: rc={completed.returncode} "
        f"elapsed={elapsed:.1f}s output={out!r} stderr={completed.stderr[:200]!r}"
    )


if __name__ == "__main__":
    main()
