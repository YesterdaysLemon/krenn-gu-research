#!/usr/bin/env python3
"""Per-survivor detail on the coupled divisor af(r+1)-(r-1)=0 (D_01):
which sheet each survivor lies on, one-marked ranks at all four modes,
and which 4x4 minors are nonzero per mode -- to select the certificate
mode/rows for the characteristic-zero closure."""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from explore_p5_h22_disjoint_mixed_star_slope_divisors_modular import (
    ROWS4,
    SAMPLES,
    build_rows,
    component_basis,
    det_mod,
    dot,
    one_marked_map,
    pattern_table,
    projective_directions,
    combine,
    rref_nullspace,
    weighted3,
)


def main():
    for p in (11, 13):
        a, b, f, phi = SAMPLES[p]
        af = a * f % p
        r = (af + 1) * pow(1 - af, -1, p) % p
        _, alpha, beta = component_basis(p)
        wa = [weighted3(alpha[m], "01", r, p) for m in range(4)]
        wb = [weighted3(beta[m], "01", r, p) for m in range(4)]
        table = pattern_table(wa, wb, p)
        print(f"== p={p}, divisor slope r={r} ==")
        for t in itertools.product(range(p), repeat=4):
            mixed, dA, dB = build_rows(t, table, p)
            rank, kernel = rref_nullspace(mixed, p)
            if not kernel:
                continue
            restA = [dot(dA, v, p) for v in kernel]
            restB = [dot(dB, v, p) for v in kernel]
            if not any(restA) or not any(restB):
                print(f"  t={t}: kernel but not genuine")
                continue
            genuine = [
                combine(d, kernel, p)
                for d in projective_directions(len(kernel), p)
            ]
            genuine = [
                z for z in genuine
                if dot(dA, z, p) and dot(dB, z, p)
            ]
            # sheet tests
            sheets = []
            if t[1] == 0 and t[2] == 0:
                sheets.append("t1=t2=0")
            if t[1] == 0 and (phi * (t[0] - 1) - f) % p == 0:
                sheets.append("t1=0,phi(t0-1)=f")
            if t[2] == 0 and t[3] == 0:
                sheets.append("t2=t3=0")
            for z in genuine:
                walpha_e = [wa[m] + (z[m],) for m in range(4)]
                wbeta_e = []
                for m in range(4):
                    marked = tuple(
                        (beta[m][c] + t[m] * alpha[m][c]) % p
                        for c in range(4)
                    )
                    wbeta_e.append(
                        weighted3(marked, "01", r, p) + (z[4 + m],)
                    )
                ranks = {}
                nonzero_sets = {}
                for mode in range(4):
                    mm = one_marked_map(mode, walpha_e, wbeta_e, p)
                    rk, _ = rref_nullspace(mm, p)
                    ranks[mode] = rk
                    nonzero_sets[mode] = [
                        rows for rows in ROWS4
                        if det_mod([mm[i] for i in rows], p)
                    ]
                print(
                    f"  t={t} sheets={sheets} marked ranks={ranks}"
                )
                for mode in range(4):
                    sample = nonzero_sets[mode][:6]
                    print(
                        f"    mode {mode}: rank {ranks[mode]}, "
                        f"nonzero minors {len(nonzero_sets[mode])}, "
                        f"e.g. {sample}"
                    )


if __name__ == "__main__":
    main()
