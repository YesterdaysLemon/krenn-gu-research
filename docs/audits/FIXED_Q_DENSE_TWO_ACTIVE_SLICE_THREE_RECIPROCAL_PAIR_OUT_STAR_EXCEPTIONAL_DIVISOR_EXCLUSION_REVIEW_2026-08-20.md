# Review: three-pair out-star exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O1`.**  Combined with the generic theorem, all `4` three-out-star masks are
empty.

## Adversarial checks

1. **Complete divisor cover.**  GLD50 leaves exactly `w=-1` and
   `v+w+1=0`; both surfaces are treated.
2. **First surface.**  At `w=-1`, the reciprocal amplitude is `1/2`; the
   fifteen-row denominator `2uv(u-1)(v-1)` vanishes only off active support.
3. **Second surface.**  On `v=-w-1`, the reciprocal amplitude is
   `(w+1)/(w+2)` and legality forbids `w=0,1,-1,-2`.
4. **Denominator exhaustion.**  The second denominator
   `uw(u-1)(w-1)(w+1)(w+2)` has no legal root.
5. **Exact contradictions.**  Both multipliers cancel all `81` retained
   variables and leave `1`; neither conclusion comes from a sampled rank.
6. **Independent implementation.**  The primary enumerates `945` perfect
   matchings and replays stored weights.  The isolated audit imports no
   project module, reconstructs recursive permanents, and derives both
   nullspaces.
7. **Orbit scope.**  GLD50's exact census carries the canonical proof to all
   `4` labelled masks.
8. **Scope control.**  Eleven three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_star_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_star_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```
