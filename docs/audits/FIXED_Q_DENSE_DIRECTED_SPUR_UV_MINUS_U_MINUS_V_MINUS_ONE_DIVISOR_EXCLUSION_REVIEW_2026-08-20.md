# Review: fixed-Q directed-spur `uv-u-v-1=0` divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the full
`uv-u-v-1=0` exceptional divisor of `GLD26`.**  The case cover includes all
five factors of the first detector, uses `GLD28` only for the identified
`uv=1` residuals, and closes the remaining quadratic cylinder.  Only one
`GLD26` divisor remains open.  The global conjecture is **UNRESOLVED**.

## Load-bearing checks

1. **Complete equations.**  The primary enumerates all `945` perfect
   matchings and retains the `24+54+3=81` independent variables.  The audit
   derives the same rows from the three exhaustive matching types.
2. **Legal parametrization.**  On `uv-u-v-1=0`, `u=1` is impossible and
   `v=(u+1)/(u-1)`.  Nonzero `u,v` excludes `u=0,-1`.
3. **Exhaustive first split.**  The eighteen-row detector leaves exactly
   `u+w=0`, `w=-2`, `u+w+1=0`, `q_1=0`, or `q_2=0` after chart factors are
   removed.
4. **Curve reductions.**  The first three curves leave only `q_a q_1`; the
   fifth leaves `q_a q_b q_1`.  On `q_a`, the divisor parametrization gives
   `v=-u`, hence `uv=1`, exactly the proved `GLD28` scope.
5. **Overlap, not omission.**  The `q_b` branch of `q_2=0` has `w=-2` and is
   contradicted by the `w=-2` curve detector.  The required chart factors are
   nonzero there.
6. **Quadratic cylinder.**  Modulo `q_1`, the fourteen-row detector is
   `2w(w+2)L`.  The coefficient `3u+7` is a unit with inverse `(3u-1)/2`, so
   `L=0` is exactly `w=-u`.  The `w=-u` and `w=-2` quotient cores each leave
   `4`.
7. **Audit boundary.**  The audit shares literal witness tables and SymPy
   arithmetic with the primary but independently derives each row by
   recursive permanents.  This is not represented as disjoint software.

## Scope control

This result closes only `uv-u-v-1=0` inside
`I+uE_(0,1)+vE_(1,0)+wE_(0,2)`, with all parameters nonzero.  It does not
close `uv+vw+w+1=0`, reverse or larger spurs, root-colour-changing blocks,
proper-secondary cells, or any weighted-permanent bridge.  No literature
novelty claim is made.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_u_minus_v_minus_one_divisor_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_directed_spur_uv_minus_u_minus_v_minus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_one_divisor_exclusion.py
```
