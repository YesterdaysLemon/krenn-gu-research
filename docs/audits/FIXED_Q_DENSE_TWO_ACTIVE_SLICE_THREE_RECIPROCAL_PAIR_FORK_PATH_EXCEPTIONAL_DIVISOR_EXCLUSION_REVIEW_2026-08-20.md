# Review: three-pair fork-path exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O4`.**  Combined with the generic theorem, all `24` fork-path masks are
empty.

## Adversarial checks

1. **Complete cover.**  GLD50 leaves exactly `u=-1` and
   `uw+vw+v+w+1=0`; both surfaces and their intersection are treated.
2. **First surface.**  Its fourteen-row denominator leaves only
   `vw+v+1=0` after active factors are removed, precisely the intersection.
3. **Second surface.**  Its parametrization and reciprocal amplitude are
   exact; all denominator factors except `u+1` are forbidden by legality.
4. **Intersection.**  Substitution gives `v=-1/(w+1)` with
   `w!=0,1,-1,-2`; the thirteen-row denominator `w(w+2)` has no legal root.
5. **Exact contradictions.**  All three multipliers cancel the `81` retained
   variables and leave `1`; no sampled rank is promoted.
6. **Independent implementation.**  The primary enumerates `945` perfect
   matchings and replays stored weights.  The no-import audit reconstructs
   recursive permanents and independently derives all three nullspaces.
7. **Orbit scope.**  GLD50's census carries the proof to all `24` masks.
8. **Scope control.**  Ten three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_fork_path_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_fork_path_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```
