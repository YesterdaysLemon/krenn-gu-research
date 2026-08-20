# Review: bidirected-spur `uv+wz+1=0` divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of a complete
GLD31 divisor.**  Together with GLD36 and GLD37, this leaves two GLD31
divisors open.  The global conjecture remains open.

## Load-bearing checks

1. The nonzero divisor is legally parametrized by `v=-(1+wz)/u`; its `v!=0`
   hypothesis is exactly `wz!=-1`.
2. The complete rows `(0100;1000)` and `(1222;1222)` cancel all `81`
   retained variables and leave `-(1+wz)/u=v`.
3. A disjoint two-row relation leaves `-w(1+wz)/u=wv`, nonzero because
   `w,v!=0`.
4. Neither relation divides by `1+wz`; only the chart parameter `u` is
   inverted, and `u!=0` is an original hypothesis.
5. The primary reuses the direct `945`-matching engine.  The audit runs under
   isolated Python, imports no project module or primary witness table,
   reconstructs recursive permanents, and derives both left nullspaces.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_plus_wz_plus_one_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_plus_wz_plus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
```
