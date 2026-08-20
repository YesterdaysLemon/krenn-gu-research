# Review: three-pair O6 exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O6`.**  All four exceptional surfaces and both legal residual curves are
empty, so all `24` O6 masks are empty.

## Adversarial checks

1. **Complete cover.**  GLD50 leaves exactly
   `(u+1)(v+1)(u+v+1)(u+vw+v+w+1)=0`; every factor is treated.
2. **Surface residues.**  The `u+v+1=0` certificate closes outright.  The
   other surface denominators leave only `u=v=-1` and
   `u=-1,vw+v+w=0` after active factors are removed.
3. **Curve cores.**  Their denominator lcms are `2w^2` and
   `2w^3(2w+1)`; their roots force an inactive amplitude.
4. **Exact contradictions.**  All six normalized multipliers cancel the
   `81` nuisance variables and leave `1`; no sampled rank is promoted.
5. **Independent implementation.**  The primary enumerates `945` perfect
   matchings; the no-import audit reconstructs recursive permanents in the
   opposite order and independently derives all six nullspaces.
6. **Orbit scope.**  GLD50's census carries the proof to all `24` masks.
7. **Scope control.**  Four three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o6_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_o6_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```
