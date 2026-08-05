#!/usr/bin/env python3
"""Finer modular analysis of the D_23 pencil at slope r=1 on the
disjoint mixed-star component.

Questions answered at finite-field component points:
  1. For every marking t, is the desired 0000 diagonal A in the row
     span of the mixed matrix M(t)?  (Then A|ker = 0 identically and
     no genuine survivor can exist, closing the divisor at binary
     level.)
  2. Same question for the 1111 diagonal B.
  3. What is the kernel line?  Is it a universal reconstruction-type
     direction (compare the six-dimensional q=1 story)?
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from explore_p5_h22_disjoint_mixed_star_slope_divisors_modular import (
    SAMPLES,
    build_rows,
    component_basis,
    dot,
    pattern_table,
    rank_mod,
    rref_nullspace,
    weighted3,
)


def analyze(p, direction, r):
    params, alpha, beta = component_basis(p)
    walpha = [weighted3(alpha[m], direction, r, p) for m in range(4)]
    wbeta = [weighted3(beta[m], direction, r, p) for m in range(4)]
    table = pattern_table(walpha, wbeta, p)
    a_in_span = 0
    b_in_span = 0
    neither = 0
    a_zero_on_ker = 0
    b_zero_on_ker = 0
    kernels = set()
    kernel_samples = []
    for t in itertools.product(range(p), repeat=4):
        mixed, dA, dB = build_rows(t, table, p)
        rank, kernel = rref_nullspace(mixed, p)
        assert rank == 7 and len(kernel) == 1, (t, rank)
        v = kernel[0]
        va = dot(dA, v, p)
        vb = dot(dB, v, p)
        if va == 0:
            a_zero_on_ker += 1
        if vb == 0:
            b_zero_on_ker += 1
        if rank_mod(mixed + [dA], p) == rank:
            a_in_span += 1
        if rank_mod(mixed + [dB], p) == rank:
            b_in_span += 1
        if va and vb:
            neither += 1
        kernels.add(v)
        if len(kernel_samples) < 8:
            kernel_samples.append((t, v, va, vb))
    print(
        f"p={p} D_{direction} r={r}: A in row span for "
        f"{a_in_span}/{p**4} markings; B in row span for "
        f"{b_in_span}/{p**4}; A|ker=0 for {a_zero_on_ker}; "
        f"B|ker=0 for {b_zero_on_ker}; genuine {neither}"
    )
    print(f"  distinct kernel lines: {len(kernels)}")
    for t, v, va, vb in kernel_samples:
        print(f"  t={t} ker={v} A.v={va} B.v={vb}")


def main():
    for p in (11, 13):
        analyze(p, "23", 1)


if __name__ == "__main__":
    main()
