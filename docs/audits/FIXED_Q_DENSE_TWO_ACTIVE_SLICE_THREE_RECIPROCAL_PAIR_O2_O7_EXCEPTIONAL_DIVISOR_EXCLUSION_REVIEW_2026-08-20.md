# Review: three-pair O2/O7 exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbits
`O2` and `O7`.**  The six-factor O2 exceptional union is exhausted by exact
complementary-denominator covers and one terminal rational point.  Exact
active-colour covariance transfers the result to O7.  All `48` masks are
empty.

## Adversarial checks

1. **Complete factor cover.**  Every factor of the GLD50 O2 exceptional union
   is parametrized.  The `v=-2` calculation is explicitly localized away
   from `uw=-1`, and the independent `uw=-1` surface cover supplies that
   omitted intersection.
2. **No generic-to-pointwise jump.**  Five exact saturated Groebner ideals
   contain `1` after localization by precisely the active factors.  This
   proves that at least one displayed multiplier is regular at every legal
   point of those strata.
3. **Terminal cover.**  The sixth saturated ideal has reduced basis
   `(9z-8,2u+1,w-2)`.  The resulting point
   `(-1/2,-1/2,2)` is active and is closed by a nine-row rational core with
   denominator lcm `6`.
4. **Exact contradictions.**  All seventeen normalized multipliers cancel
   the `81` nuisance variables and leave `1`; no sampled or modular rank is
   promoted.
5. **Independent implementation.**  The primary expands all `945` matching
   topologies.  The no-import audit recursively derives permanents and takes
   nullspaces in reverse row and variable order before independently
   repeating the saturated cover.
6. **O7 transfer.**  Arrow reversal carries `{01,02,10}` exactly to the O7
   representative `{01,10,20}`.  GLD55's all-`6561` covariance and its
   independent `945`-topology audit are replayed; the active parameter map is
   involutive.
7. **Orbit scope.**  GLD50's exact census carries the two representative
   exclusions to `24+24=48` masks.
8. **Scope control.**  O9's `8` masks, four-or-more supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o2_o7_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_o2_o7_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion.py
```
