#!/usr/bin/env python3
"""Exact rank-7 witness for the D_23 mixed matrix at r=1, marking t=0:
pick the pivot rows of the modular rref (p=11) and evaluate that
single 7x7 minor (columns x0..x3,y0..y2; the y3 column is the
universal kernel) symbolically mod Phi.  Nonzero => rank exactly 7 at
t=0 over K (upper bound from the universal kernel).  The all-t rank-7
statement stays modular-only (p=11,13: rank 7 at every marking)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sympy as sp

from explore_p5_h22_disjoint_mixed_star_slope_divisors_modular import (
    build_rows,
    component_basis,
    pattern_table,
    rref_nullspace,
    weighted3 as w3mod,
)
from slope_common import MIXED, T, Z, build_system, phi_normal_form

# modular pivot rows at t=0
p = 11
_, alpha_p, beta_p = component_basis(p)
wa = [w3mod(alpha_p[m], "23", 1, p) for m in range(4)]
wb = [w3mod(beta_p[m], "23", 1, p) for m in range(4)]
table = pattern_table(wa, wb, p)
mixed, _, _ = build_rows((0, 0, 0, 0), table, p)
pivot_rows = []
current = []
for i, row in enumerate(mixed):
    trial = current + [row[:7]]
    rank, _ = rref_nullspace(trial, p)
    if rank == len(trial):
        current = trial
        pivot_rows.append(i)
    if len(pivot_rows) == 7:
        break
assert len(pivot_rows) == 7, pivot_rows
print("modular pivot rows:", pivot_rows)

# symbolic minor at t=0
data = build_system("23", sp.Integer(1))
tzero = {tv: 0 for tv in T}
M = sp.Matrix([
    [sp.expand(c.subs(tzero)) for c in data["rows"][bits][:7]]
    for bits in MIXED
])
sub = M[pivot_rows, list(range(7))]
det = sp.expand(sub.det(method="berkowitz"))
reduced = phi_normal_form(det)
assert reduced != 0
print("7x7 minor rows", pivot_rows, "columns x0..y2:")
print("  factored (mod Phi, nonzero):", sp.factor(reduced))
