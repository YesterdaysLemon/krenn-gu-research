# Review: three-pair O9 exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O9`.**  Fourteen exact cores exhaust its six-factor exceptional union.  All
`8` O9 masks, and therefore all `220` exactly-three-pair masks in this fixed-Q
cell, are empty.

## Adversarial checks

1. **Complete factor cover.**  Every factor in the GLD50 O9 exceptional union
   is rationally parametrized, including `P9`, which is linear in `u`.
2. **No generic-to-pointwise jump.**  Five exact saturated denominator ideals
   contain `1` after localization by precisely the active factors and product
   intersections already closed in the same theorem.
3. **Intersection ownership.**  The common factors `vw+w-1`, `uw+u-1`,
   `2vw^2-vw+w-1`, and `v^2w-2vw+w+1` are verified substitutions of the
   `uvw=-1` intersection, not silently discarded poles.
4. **Long-surface cover.**  On the only remaining shared pole,
   `w=-1/(v-1)`, exact substitution gives nonzero factors `-2/(v-1)` and `3`;
   the other two factors are coprime because
   `gcd(v^3-v-3,v-2)=1`.
5. **Exact contradictions.**  All fourteen normalized multipliers cancel the
   `81` nuisance variables and leave `1`; no sampled or modular rank is
   promoted.
6. **Independent implementation.**  The primary expands all `945` matching
   topologies.  The no-import audit recursively derives permanents, reverses
   row and variable order, and repeats the exact coverage calculations.
7. **Orbit scope.**  GLD50's exact census carries the representative proof to
   all `8` O9 masks.  Combined with GLD51--GLD61, this closes all `220`
   exactly-three-pair masks.
8. **Scope control.**  Four-or-more supports, proper-secondary cells, and
   every permanent bridge remain open.  Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o9_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_o9_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```
