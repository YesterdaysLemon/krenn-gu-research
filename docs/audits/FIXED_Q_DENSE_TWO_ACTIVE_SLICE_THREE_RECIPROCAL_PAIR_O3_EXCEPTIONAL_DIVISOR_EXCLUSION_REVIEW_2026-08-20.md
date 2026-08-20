# Review: three-pair O3 exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O3`.**  Four surfaces, five residual intersections, and two terminal points
are all empty, so all `24` O3 masks are empty.

## Adversarial checks

1. **Complete cover.**  Every factor of the GLD50 O3 exceptional union is
   parametrized and checked.
2. **Intersection cover.**  Removing active-forbidden denominator factors
   leaves exactly the five displayed pairwise intersections.
3. **Terminal cover.**  The five curve cores leave only
   `(-1,-1,-1)` and `(-1/2,-1/2,-1)`; denominator lcms `4` and `6` close them.
4. **Exact contradictions.**  All eleven multipliers cancel the `81`
   nuisance variables and leave `1`; no sampled rank is promoted.
5. **Independent implementation.**  The primary uses `945`-matching rows;
   the no-import audit reconstructs recursive permanents and independently
   derives every nullspace in reverse order.
6. **Orbit scope.**  GLD50's census carries the proof to all `24` masks.
7. **Scope control.**  O2, O7, O9, larger supports, proper-secondary cells,
   and every permanent bridge remain open.  Global status stays
   **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o3_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_o3_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```
