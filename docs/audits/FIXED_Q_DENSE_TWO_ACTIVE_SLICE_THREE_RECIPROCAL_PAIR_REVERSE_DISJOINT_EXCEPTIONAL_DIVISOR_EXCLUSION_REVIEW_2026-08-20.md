# Review: three-pair reverse-disjoint exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O8`.**  Combined with the generic theorem, all `12` reverse-disjoint masks
are empty.

## Adversarial checks

1. **Complete cover.**  GLD50 leaves exactly
   `(u+1)(w+1)(2w-1)(uv+1)=0`; all four surfaces and the only legal residual
   overlaps are treated.
2. **Product surface first.**  On `uv=-1`, the eleven-row denominator
   `2uw(u-1)(w-1)` has no legal root, including at intersections with the
   other three factors.
3. **First-parameter surface.**  On `u=-1`, the fourteen-row denominator
   leaves only `w=-1` and `w=1/2` after active factors are removed.
4. **Third-parameter surfaces.**  On `w=-1` and `w=1/2`, the respective
   twelve- and fourteen-row denominators leave only `u=-1` or `uv=-1`.
   The product branch is already closed.
5. **Overlap cores.**  At `(u,w)=(-1,-1)` and `(-1,1/2)`, the nine- and
   thirteen-row denominators are `4v(v-1)` and `4v^2(v-1)`, with only
   active-forbidden roots.
6. **Exact contradictions.**  Every multiplier cancels all `81` retained
   variables and leaves `1`; no sampled rank is promoted.
7. **Independent implementation.**  The primary enumerates `945` perfect
   matchings and replays stored weights.  The no-import audit reconstructs
   recursive permanents and independently derives all six nullspaces.
8. **Orbit scope.**  GLD50's census carries the proof to all `12` masks.
9. **Scope control.**  Nine three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_reverse_disjoint_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_reverse_disjoint_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```
