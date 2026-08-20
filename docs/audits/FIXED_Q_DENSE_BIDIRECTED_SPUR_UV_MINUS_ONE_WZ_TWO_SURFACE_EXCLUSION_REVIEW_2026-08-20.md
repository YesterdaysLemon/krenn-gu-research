# Review: bidirected-spur `uv=-1`, `wz=2` surface exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the last
GLD32 residual surface.**  With GLD33--GLD35, this completes pointwise
exclusion of the nonzero `uv=-1` divisor.  The other four GLD31 divisors and
the global conjecture remain open.

## Load-bearing checks

1. The GLD32 chart has `u,w,z!=0`; imposing `wz=2` legally gives `w=2/z`,
   while `uv=-1` gives `v=-1/u`.
2. The complete rows `(0100;1000)` and `(1222;1222)`, with multipliers
   `(1,u^(-1))`, cancel all `81` retained variables and leave `-u^(-1)`.
3. The nonzero-chart hypothesis `u!=0` makes this a pointwise contradiction,
   with no residual specialization.
4. GLD32's four-surface case cover and the pointwise GLD33--GLD35 closures
   are exact dependencies; together with this result they exhaust `uv=-1`.
5. The primary reuses the direct `945`-matching engine.  The audit runs under
   isolated Python, imports no project module or primary witness table,
   reconstructs recursive permanents, and derives the left nullspace.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_wz_two_surface_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_minus_one_wz_two_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_u_one_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_z_one_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_z_minus_one_surface_exclusion.py
```
