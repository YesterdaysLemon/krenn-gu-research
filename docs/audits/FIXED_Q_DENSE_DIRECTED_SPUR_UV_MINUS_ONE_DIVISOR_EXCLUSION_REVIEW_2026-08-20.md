# Hostile review: directed-spur `uv=-1` divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the complete
`uv=-1` exceptional divisor of `GLD26`.**  The case cover includes the
residual line, its two exceptional points, and the quadratic family.  Three
other `GLD26` divisors remain open.  The global conjecture is **UNRESOLVED**.

## Adversarial checks

1. **No illegal division.**  The substitution `v=-u^(-1)` uses the chart
   hypothesis `u!=0`.  The displayed divisor certificate is polynomial-
   cleared and leaves `2uw(u-1)(u^2+2u-1)`.

2. **Exhaustive residual split.**  Since `u,w!=0`, the detector vanishes only
   at `u=1` or `q(u)=u^2+2u-1=0`.  No third component is discarded.

3. **Line exceptions closed separately.**  At `u=1,v=-1`, the line detector
   is `2w(w+1)(w+2)`.  The chart removes `w=0`; independent twelve-row cores
   give `0=1` at `w=-1` and `w=-2`.

4. **Quadratic family is not sampled.**  In `K[u,w]/(q)`, a twelve-row
   certificate leaves `4w`.  This excludes the whole family for `w!=0`, even
   if `q` is irreducible over `K`.

5. **All nuisance variables remain free.**  Every certificate cancels all
   `24+54+3=81` root-side and pure-target variables.

6. **Complete rows.**  The primary enumerates all `945` perfect matchings.
   The audit independently derives rows from the three exhaustive matching
   types and recursive permanents.

7. **Independence is accurately scoped.**  The audit imports neither the
   primary nor project code and uses a different row derivation.  Both use
   SymPy exact arithmetic, so the review does not claim distinct algebra
   libraries.

8. **No quantifier promotion.**  This closes only `uv=-1`.  The divisors
   `uv=1`, `uv-u-v-1=0`, and `uv+vw+w+1=0`, broader support charts, other
   `GLD21` cells, and all permanent consequences remain open.

## Required replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_one_divisor_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_directed_spur_uv_minus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_generic_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_directed_spur_generic_cross_array_exclusion.py
```
