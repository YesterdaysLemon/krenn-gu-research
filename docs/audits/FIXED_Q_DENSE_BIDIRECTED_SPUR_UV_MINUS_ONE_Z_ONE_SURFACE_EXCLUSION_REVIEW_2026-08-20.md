# Review: bidirected-spur `uv=-1`, `z=1` surface exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of one complete
GLD32 residual surface.**  Together with GLD33, this leaves `z=-1` and
`wz=2` open inside the `uv=-1` divisor.  The global conjecture remains open.

## Load-bearing checks

1. The GLD32 chart has `u,w,z!=0`; imposing `z=1` and `uv=-1` legally gives
   `v=-1/u`.
2. The complete rows `(1202;0212)` and `(2212;2212)`, with multipliers
   `(1,-w)`, cancel all `81` retained variables and leave `w`.
3. The nonzero-chart hypothesis `w!=0` makes this a pointwise contradiction,
   with no specialization or denominator issue.
4. A disjoint two-row relation leaves `-u^(-1)`, providing an exact redundant
   check under the independently required hypothesis `u!=0`.
5. The primary reuses the direct `945`-matching engine.  The audit runs under
   isolated Python, imports no project module or primary witness table,
   reconstructs the recursive permanents, and derives both left nullspaces.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_z_one_surface_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_minus_one_z_one_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
```
