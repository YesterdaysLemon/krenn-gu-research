# Review: dense two-active-slice same-head exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of the GLD44
same-head exceptional divisor union.**  Combined with the generic theorem,
all `12` same-head support masks are empty.  Only the chain orbit divisors
remain open among the five minimal two-pair orbit types.

## Adversarial checks

1. **Symmetric divisor cover.**  GLD44 gives
   `(u+1)(u-w-1)(u+w+1)=0`; pair exchange gives the equally necessary
   `(w+1)(w-u-1)(u+w+1)=0`.
2. **Exact intersection.**  Away from `u+w+1=0`, the four intersections of
   the remaining factors give `(-1,-1)`, two illegal support-drop points, or
   the characteristic-zero contradiction `u-w=1=w-u`.
3. **Curve domain.**  On `w=-u-1`, reciprocal support forbids
   `u=0,1,-1,-2`.  The eleven-row certificate denominator
   `2u^2(u+1)^2` therefore has no legal root.
4. **Point core.**  At `(-1,-1)`, both reciprocal amplitudes are exactly
   `1/2`; the fourteen-row multiplier is integral and leaves `1`.
5. **Exact contradictions.**  Both sparse multipliers cancel all `81`
   retained variables and leave `1`; neither conclusion comes from a sampled
   rank.
6. **Independent implementation.**  The primary enumerates `945` perfect
   matchings and replays stored multipliers.  The isolated audit imports no
   project module, reconstructs recursive permanents, and derives both
   nullspaces.
7. **Orbit scope.**  GLD44's exhaustive position-orbit classification carries
   the canonical proof to all `12` same-head masks.
8. **Scope control.**  Chain divisors, larger supports, and every permanent
   bridge remain open.  Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_same_head_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_same_head_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```
