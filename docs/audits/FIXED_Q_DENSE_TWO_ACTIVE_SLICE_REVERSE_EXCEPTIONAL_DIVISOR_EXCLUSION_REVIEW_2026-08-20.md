# Review: dense two-active-slice reverse exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of the GLD44
reverse exceptional divisor union.**  Combined with the generic theorem, all
`6` reverse support masks are empty.  Same-head and chain orbit divisors remain
open.

## Adversarial checks

1. **Exhaustive divisor cover.**  GLD44 leaves exactly `u=-1`, `w=-1`, and
   `uw=-1`.  No other reverse-orbit denominator factor is omitted.
2. **First curve.**  The `u=-1` certificate has denominator
   `2w^2(w-1)`; nonzero reciprocal support forbids every root.
3. **Pair-exchange symmetry.**  The position swap `(0 2)` exchanges the two
   reverse directed pairs and maps `w=-1` to the proved `u=-1` curve.
4. **Product curve.**  On `w=-1/u`, legal reciprocal parametrization forbids
   `u=0,1,-1`.  These are exactly the roots of the second certificate's
   denominator `2u(u-1)(u+1)`.
5. **Exact contradictions.**  The two sparse rational multipliers cancel all
   `81` retained variables and leave `1`; neither conclusion comes from a
   sampled rank.
6. **Independent implementation.**  The primary enumerates `945` perfect
   matchings and replays stored multipliers.  The isolated audit imports no
   project module, reconstructs recursive permanents, and derives both
   nullspaces.
7. **Scope control.**  Same-head and chain divisors, larger supports, and
   every permanent bridge remain open.  Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reverse_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_reverse_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```
