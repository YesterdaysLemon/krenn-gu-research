#!/usr/bin/env python3
"""Exact characteristic-zero closure of the slope divisor r=-1 for
BOTH weighted H22 pencils on the disjoint mixed-star component.

Structure (exact sympy congruences mod Phi, every marking t):
  * D_23 at r=-1: the entire slot-0 column pair (x_0 AND y_0) of all
    sixteen binary words vanishes identically.  Hence every marking
    has the marking-independent kernel PLANE span(e_{x0},e_{y0}), on
    which A=B=0 (a reconstruction plane; the generic mixed rank drops
    to six).  The diagonals lose their slot-0 entries.
  * D_01 at r=-1: same with the slot-3 column pair (x_3, y_3).

Closure (Singular Rabinowitsch, exact):
    ideal(14 mixed rows, Phi, w*A(z)*B(z)-1) = (1)
for each pencil: NO genuine binary survivor exists at r=-1 for any
marking, over the generic component point.  The r=-1 slope divisor of
the generic weighted-H22 theorem is closed at binary level, before
any third target row is considered.

Corroboration: full F_11/F_13 marking censuses (0 genuine survivors).
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

def _repo_root():
    for candidate in Path(__file__).resolve().parents:
        if (candidate / ".git").exists():
            return candidate
    return Path(__file__).resolve().parent


_REPO_ROOT = _repo_root()
sys.path.insert(0, str(_REPO_ROOT / "research_snapshots" / "2026-08-04-p5-h22-slope-divisor-closures" / "scripts"))

import sympy as sp

from slope_common import (
    BITS4,
    PHI,
    T,
    Z,
    build_system,
    phi_normal_form,
    sing,
)

OUT = _REPO_ROOT / "research_snapshots" / "2026-08-04-p5-h22-slope-divisor-closures"
TIMEOUT = 550


def rabinowitsch(data, label):
    lin = []
    for bits, row in data["rows"].items():
        if bits in ((0, 0, 0, 0), (1, 1, 1, 1)):
            continue
        lin.append(sum(c * zv for c, zv in zip(row, Z)))
    A = sum(c * zv for c, zv in zip(data["A"], Z))
    B = sum(c * zv for c, zv in zip(data["B"], Z))
    variables = (
        "phi,"
        + ",".join(str(t) for t in T)
        + ","
        + ",".join(str(z) for z in Z)
        + ",w"
    )
    program = "\n".join(
        [
            f"ring R=(0,a,b,f),({variables}),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(sing(e) for e in lin) + ";",
            f"I=I,{sing(PHI)};",
            f"I=I,w*({sing(A)})*({sing(B)})-1;",
            "I=std(I);",
            f'"CODEX_RESULT:{label}:"+string(reduce(1,I)==0);',
            "quit;",
        ]
    )
    completed = subprocess.run(
        ("Singular", "-q"),
        input=program,
        text=True,
        capture_output=True,
        timeout=TIMEOUT,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stderr[-500:]
    )
    assert f"CODEX_RESULT:{label}:1" in completed.stdout, (
        label, completed.stdout[-500:]
    )


def main() -> None:
    started = time.monotonic()
    certificates = {}

    d23 = build_system("23", sp.Integer(-1))
    # dead slot-0 column pair in ALL sixteen words
    for bits in BITS4:
        row = d23["rows"][bits]
        assert phi_normal_form(row[0]) == 0, bits
        assert phi_normal_form(row[4]) == 0, bits
    certificates["d23_dead_columns"] = (
        "slot-0 pair (x0,y0) of all sixteen words vanishes mod Phi "
        "for every marking: universal kernel plane span(e_x0,e_y0), "
        "A=B=0 on it"
    )
    rabinowitsch(d23, "d23-rm1")
    certificates["d23_rabinowitsch"] = (
        "ideal(14 rows, Phi, w*A*B-1) = (1): no genuine binary "
        "survivor for any marking"
    )

    d01 = build_system("01", sp.Integer(-1))
    for bits in BITS4:
        row = d01["rows"][bits]
        assert phi_normal_form(row[3]) == 0, bits
        assert phi_normal_form(row[7]) == 0, bits
    certificates["d01_dead_columns"] = (
        "slot-3 pair (x3,y3) of all sixteen words vanishes mod Phi "
        "for every marking: universal kernel plane span(e_x3,e_y3), "
        "A=B=0 on it"
    )
    rabinowitsch(d01, "d01-rm1")
    certificates["d01_rabinowitsch"] = (
        "ideal(14 rows, Phi, w*A*B-1) = (1): no genuine binary "
        "survivor for any marking"
    )

    # modular replay
    from explore_p5_h22_disjoint_mixed_star_slope_divisors_modular import (
        build_rows,
        component_basis,
        dot,
        pattern_table,
        rref_nullspace,
        weighted3 as w3mod,
    )

    replay = {}
    for p in (11, 13):
        _, alpha_p, beta_p = component_basis(p)
        for direction in ("23", "01"):
            wa = [
                w3mod(alpha_p[m], direction, p - 1, p)
                for m in range(4)
            ]
            wb = [
                w3mod(beta_p[m], direction, p - 1, p)
                for m in range(4)
            ]
            table = pattern_table(wa, wb, p)
            genuine = 0
            for t in itertools.product(range(p), repeat=4):
                mixed, dA, dB = build_rows(t, table, p)
                _, kernel = rref_nullspace(mixed, p)
                restA = [dot(dA, v, p) for v in kernel]
                restB = [dot(dB, v, p) for v in kernel]
                if any(restA) and any(restB):
                    genuine += 1
            assert genuine == 0, (p, direction)
            replay[f"p{p}_D{direction}"] = "no genuine survivor"
    certificates["modular_replay"] = replay

    result = {
        "verified": True,
        "field": "C(a,b,f)[phi]/(Phi), slope fixed at r=-1",
        "component": "disjoint mixed-star fivefold (eighth orbit)",
        "statement": (
            "at slope r=-1 neither weighted H22 pencil has a genuine "
            "binary Delta_2 extension for any marking; the r=-1 slope "
            "divisor is closed at binary level for both pencils over "
            "the generic component point"
        ),
        "certificates": certificates,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    path = OUT / "rm1_binary_obstruction_verified.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
