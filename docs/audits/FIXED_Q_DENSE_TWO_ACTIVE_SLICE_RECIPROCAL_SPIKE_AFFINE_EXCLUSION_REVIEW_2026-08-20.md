# Review: dense two-active-slice reciprocal-spike affine exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the stated
two-parameter reciprocal-spike chart.**  The divisor relation, generic curve
certificate, exceptional-point core, and GLD41 boundary cover every point.
The global conjecture remains open.

## Adversarial checks

1. **Genuinely two active slices.**  On `u,v!=0`, both `A^0` and `A^1` are
   nonprivate.  Neither primary calculation specializes one amplitude away.
2. **Exact divisor.**  Three complete rows over `Z[u,v]` cancel all `81`
   retained variables and leave `-(uv-u-v)`.  This is an equality forced on a
   hypothetical witness, not a sampled or generic observation.
3. **Boundary cover.**  On the divisor, `u=0` or `v=0` forces `u=v=0`.
   Independently, every support-drop face lies in the proved GLD41
   single-active-slice cell.
4. **Legal parametrization.**  On the nonzero divisor, `u!=1`, so
   `v=u/(u-1)` loses no point.  The displayed generic multiplier has only
   `u`, `u-1`, and `u+1` as denominator factors.
5. **Exceptional locus.**  Nonzero divisor hypotheses remove `u=0,1`; the
   only denominator exception is `u=-1`, which forces `v=1/2` and is closed
   by a separate exact eleven-row integer certificate.
6. **Independent implementation.**  The primary enumerates `945` perfect
   matchings.  The isolated audit imports no project module, reconstructs
   recursive permanents, and derives all three nullspaces symbolically.
7. **Scope control.**  Only the reciprocal support pair `E_(0,2)` in colour
   zero and `E_(2,0)` in colour one is allowed.  Additional two-slice support,
   general cross arrays, proper-secondary cells, and every permanent bridge
   remain open.  Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_spike_affine_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_reciprocal_spike_affine_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_single_active_slice_affine_cross_array_completion.py
```
