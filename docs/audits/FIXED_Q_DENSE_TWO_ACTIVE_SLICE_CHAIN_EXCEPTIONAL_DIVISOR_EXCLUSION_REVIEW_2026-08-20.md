# Review: dense two-active-slice chain exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of the GLD44
directed-chain exceptional divisor union.**  Combined with the generic
theorem, all `24` chain support masks are empty.  With GLD45--GLD48, this
closes all `66` minimal two-pair masks.

## Adversarial checks

1. **Exhaustive divisor cover.**  GLD44 leaves exactly `u=-1` and
   `uw+w+1=0` on the canonical chain.  Both components are treated.
2. **First curve.**  At `u=-1`, the fifteen-row certificate denominator is
   `2w^2`; active reciprocal support forbids its only root.
3. **Second curve.**  On `w=-1/(u+1)`, the second reciprocal amplitude is
   exactly `1/(u+2)`, and legal support forbids `u=0,1,-1,-2`.
4. **Denominator exhaustion.**  Those four forbidden values are exactly the
   roots of the second certificate denominator `2u(u-1)(u+1)(u+2)`.
5. **Exact contradictions.**  The two sparse rational multipliers cancel all
   `81` retained variables and leave `1`; neither conclusion comes from a
   sampled rank.
6. **Independent implementation.**  The primary enumerates `945` perfect
   matchings and replays stored multipliers.  The isolated audit imports no
   project module, reconstructs recursive permanents, and derives both
   nullspaces.
7. **Orbit census.**  GLD44 proves that the directed-chain orbit has `24`
   masks and that the five orbit counts sum to `66`.  GLD45--GLD49 now close
   each orbit pointwise.
8. **Scope control.**  Larger supports, proper-secondary cells, and every
   permanent bridge remain open.  Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_chain_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_chain_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```
