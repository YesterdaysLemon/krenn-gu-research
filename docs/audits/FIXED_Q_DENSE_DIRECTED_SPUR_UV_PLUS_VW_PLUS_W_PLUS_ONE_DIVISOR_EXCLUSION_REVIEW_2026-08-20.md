# Review: fixed-Q directed-spur `uv+vw+w+1=0` divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the final
`GLD26` exceptional divisor and, with `GLD25`--`GLD29`, completion of this
directed-spur coordinate family.**  The case cover includes every factor of
the new divisor detector and every residual component is either contradicted
directly or placed inside a previously proved theorem scope.  The global
conjecture is **UNRESOLVED**.

## Load-bearing checks

1. **Complete equations.**  The primary enumerates all `945` perfect
   matchings and retains the `24+54+3=81` independent variables.  The audit
   derives the rows from the three exhaustive matching types by recursive
   permanents.
2. **Legal parametrization.**  On `H=uv+vw+w+1=0`, the `v=-1` fibre forces
   `u=1`, hence lies on `GLD27`.  Only after removing it does the proof divide
   by `v+1` and use `w=-(uv+1)/(v+1)`.
3. **Exhaustive first split.**  The sixteen-row detector leaves exactly
   `u=1`, `u+v=0`, `uv=-1`, or `uv-2v-1=0` after the nonzero chart factors
   are removed.
4. **`u=1` curve.**  Its detector is `-2v(v-1)(v+1)`.  The three factors are
   respectively a chart exclusion, `GLD28`, and `GLD27`.
5. **`u+v=0` curve.**  Its detector is
   `-u(u-1)(u+1)(u^2+1)^2`.  The factors give a chart exclusion, `GLD27`,
   the excluded `w=0` boundary, or `uv=1` and hence `GLD28`.
6. **Last curve.**  `uv-2v-1=0` gives `v=1/(u-2),w=-2` and detector
   `2u(u-1)(u^2-2u-1)`.  The quadratic residual satisfies
   `uv-u-v-1=0` exactly and is therefore in the proved `GLD29` scope.
7. **Chart corollary.**  `GLD26` covers the generic complement;
   `GLD27`--`GLD30` cover all four exceptional divisors for `w!=0`; `GLD25`
   covers `w=0`.  No other cross-array chart is absorbed into this union.
8. **Audit boundary.**  The audit shares literal witness tables and SymPy
   arithmetic with the primary but independently derives and cross-checks
   all `19` distinct rows by recursive permanents.  This is not represented
   as disjoint software.

## Scope control

This result closes only
`I+uE_(0,1)+vE_(1,0)+wE_(0,2)` with `u,v!=0`.  It does not close the reverse
spur, further support entries, root-colour-changing blocks,
proper-secondary cells, broader `GLD21` branches, or any weighted-permanent
bridge.  No literature novelty claim is made.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_plus_vw_plus_w_plus_one_divisor_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_directed_spur_uv_plus_vw_plus_w_plus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_u_minus_v_minus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_amplitude_single_switch_cross_array_exclusion.py
```
