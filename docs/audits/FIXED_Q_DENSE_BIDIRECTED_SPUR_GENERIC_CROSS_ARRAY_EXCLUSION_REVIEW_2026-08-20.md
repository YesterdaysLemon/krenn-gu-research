# Review: fixed-Q dense bidirected-spur generic exclusion

## Verdict

**Accept as an exact characteristic-zero generic/open-subset exclusion on
the four-parameter bidirected-spur chart.**  The detector is a polynomial
identity in the complete coefficient system and leaves five explicit
hypersurfaces open.  It is not a pointwise exclusion of the chart and does
not change the global **UNRESOLVED** status.

## Load-bearing checks

1. **Complete equations.**  The primary enumerates all `945` ten-vertex
   perfect matchings and retains the `24+54+3=81` independent variables.
   The new `zE_(2,0)` entry is included only in the active colour-zero cross
   slice.
2. **Exact cancellation.**  Sixteen stored polynomial multipliers cancel
   every variable coefficient and leave exactly
   `2uv wz(uv+1)(uv+wz-1)(uv+wz+1)(uv+vw+w+1)p`.
3. **Legal nonvanishing.**  Characteristic zero makes `2` nonzero and the
   chart explicitly assumes `u,v,w,z!=0`.  The theorem excludes only the
   complement of the other five displayed factors.
4. **Boundary control.**  The `z=0` boundary is exactly the completed `GLD30`
   directed-spur family.  None of the five new divisors is silently replaced
   by its `z=0` specialization.
5. **Audit boundary.**  The audit shares the literal witness table and SymPy
   arithmetic with the primary but independently reconstructs and compares
   every selected row by recursive permanents.  This is not represented as
   disjoint software.

## Scope control

This theorem concerns only
`I+uE_(0,1)+vE_(1,0)+wE_(0,2)+zE_(2,0)` with all four parameters nonzero
and all five detector factors nonzero.  Its five hypersurfaces, further
support entries, root-colour-changing blocks, proper-secondary cells, and
every weighted-permanent bridge remain open.  No literature novelty claim is
made.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_plus_vw_plus_w_plus_one_divisor_exclusion.py
```
