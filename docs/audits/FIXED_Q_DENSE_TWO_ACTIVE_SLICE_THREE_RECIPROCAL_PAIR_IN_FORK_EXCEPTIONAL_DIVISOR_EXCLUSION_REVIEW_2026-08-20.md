# Review: three-pair in-fork exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O11`.**  All four exceptional surfaces and their three legal residual
intersections are empty, so all `12` in-fork masks are empty.

## Adversarial checks

1. **Complete cover.**  GLD50 leaves exactly
   `(u+1)(u-w-1)(u+w+1)(uv+v+1)=0`; every factor is treated.
2. **Surface residues.**  After active factors are removed, the four surface
   denominators leave only `u=-1,w=-2` and the product surface's intersections
   with `w=u-1` or `w=-u-1`.
3. **Overlap cores.**  Their denominators are `8v^3`,
   `4u^2(u-2)(u-1)^3(u+1)`, and `4u^2(u+1)^2(u+2)`; every root is forbidden
   by the corresponding active parametrization.
4. **Exact contradictions.**  All seven normalized multipliers cancel the
   `81` nuisance variables and leave `1`; no sampled rank is promoted.
5. **Independent implementation.**  The primary enumerates `945` perfect
   matchings.  The no-import audit reconstructs recursive permanents in the
   opposite row/column order and independently derives all seven nullspaces.
6. **Orbit scope.**  GLD50's census carries the proof to all `12` masks.
7. **Scope control.**  Six three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_fork_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_fork_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```
