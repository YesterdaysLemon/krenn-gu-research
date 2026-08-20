# Review: bidirected-spur `uv=-1`, `u=1` surface exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of one complete
GLD32 residual surface.**  Three other residual surfaces and the global
conjecture remain open.

## Load-bearing checks

1. `u=1` and `uv=-1` force `v=-1`; only nonzero `w,z` remain.
2. Two complete-system detectors leave exactly `wz=2` or `(w,z)=(1,-1)`.
3. A polynomial-cleared curve certificate leaves `24`; a point certificate
   leaves `6`.  Both are nonzero in characteristic zero.
4. The primary uses direct enumeration of all `945` matchings.
5. The audit runs under isolated Python, imports no project module or primary
   witness table, independently derives recursive permanents and nullspaces,
   and reproduces all four contradictions.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_u_one_surface_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_minus_one_u_one_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
```
