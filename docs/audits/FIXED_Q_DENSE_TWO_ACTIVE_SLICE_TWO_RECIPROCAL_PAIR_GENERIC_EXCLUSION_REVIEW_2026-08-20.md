# Review: dense two-active-slice two-reciprocal-pair generic exclusion

## Verdict

**Accept as an exact characteristic-zero generic exclusion across all five
two-reciprocal-pair support orbits.**  Every one of the `66` masks is covered;
only the displayed orbitwise exceptional divisors remain.  This is not a
pointwise completion of those divisors or of the full two-active-slice cell.

## Adversarial checks

1. **Legal GLD43 locus.**  The two transpose-paired colour-one amplitudes are
   substituted as `u/(u-1)` and `w/(w-1)` only after GLD43 forces the
   reciprocal divisor.  Nonzero support makes `u,w!=0`, while the divisor
   itself makes `u,w!=1`.
2. **Orbit exhaustiveness.**  Independent enumeration of the `66` unordered
   two-edge subsets gives counts `6,12,12,24,12` for reverse, same-tail,
   same-head, chain, and disjoint types.  These sum to `66`.
3. **Exact rather than sampled certificates.**  Each multiplier is rational
   in symbolic `u,w`, cancels every one of the `81` retained coefficients,
   and leaves exactly `1`.
4. **Exceptional-locus honesty.**  A certificate is used only where its
   denominator is nonzero.  After removing the already forbidden
   `u,w,u-1,w-1` factors, every remaining factor is displayed in the theorem
   table and left open.
5. **Independent implementation.**  The primary enumerates `945` perfect
   matchings and replays stored multipliers.  The isolated audit imports no
   project module, reconstructs recursive permanents, derives each left
   nullspace, and recomputes its denominator.
6. **No pointwise overclaim.**  The theorem proves emptiness only off the five
   exceptional divisor unions.  It neither proves residual points exist nor
   excludes them.
7. **Scope control.**  Three-or-more reciprocal pairs, proper-secondary cells,
   and every permanent bridge remain open.  Global status stays
   **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_support_divisor_reduction.py
```
