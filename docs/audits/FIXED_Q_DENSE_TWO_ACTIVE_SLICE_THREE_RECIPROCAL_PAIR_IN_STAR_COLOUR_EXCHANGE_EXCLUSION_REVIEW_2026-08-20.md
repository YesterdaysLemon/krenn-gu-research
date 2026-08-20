# Review: three-pair in-star colour-exchange exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O13`.**  The complete in-star system is isomorphic to the already excluded
GLD52 out-star system, so all `4` in-star masks are empty.

## Adversarial checks

1. **Parameter map.**  Active-colour exchange sends `t` to `t/(t-1)`; this
   is an involution and preserves exactly the legal domain `t!=0,1`.
2. **Support map.**  All three out-star arrows reverse.  A position swap
   sends the reversed star to the GLD50 `O13` representative.
3. **Helper asymmetry.**  The exchange fixes `x=(1,1,0)` but negates
   `y=(1,-1,0)`.  The proof does not silently treat both helpers as fixed.
4. **Nuisance covariance.**  The signed colour permutation on all `81`
   coordinates is bijective and involutive: `P0` and `W` acquire the needed
   minus signs, while `P1` and the target coordinates do not.
5. **Complete equations.**  The primary reconstructs recursive permanents
   and checks every coefficient and right-hand side in all `6561` rows.
6. **Independent implementation.**  The no-import audit does not call the
   row constructor.  It enumerates all `945` perfect matchings and proves that
   the only surviving topologies are constant/no-`y`, `P0`/one-`y`,
   `P1`/no-`y`, and `W`/one-`y`, with counts `24,96,96,144`.
7. **Dependency scope.**  The conclusion uses GLD52's pointwise out-star
   exclusion, not merely GLD50's generic O13 certificate.
8. **Scope control.**  Eight three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_star_exceptional_divisor_exclusion.py
```
