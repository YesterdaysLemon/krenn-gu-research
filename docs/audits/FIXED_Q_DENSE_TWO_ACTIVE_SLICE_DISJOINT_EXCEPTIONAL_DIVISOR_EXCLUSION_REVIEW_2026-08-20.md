# Review: dense two-active-slice disjoint exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of the GLD44
disjoint exceptional divisor union.**  Combined with the generic theorem, all
`12` disjoint support masks are empty.  Three other two-pair orbit divisor
families remain open.

## Adversarial checks

1. **Exact inherited branch.**  The canonical curve is the GLD44 component
   `u=-1`, with reciprocal amplitude `1/2`; the other active pair retains its
   exact GLD43 parametrization.
2. **Active-domain cover.**  The only new denominator roots are `w=0,1`, both
   already forbidden by nonzero reciprocal support.
3. **Exact contradiction.**  Eleven complete rows and the displayed rational
   multiplier cancel all `81` variables and leave `1`.
4. **Second branch symmetry.**  `(0 1)(2 3)` exchanges the two disjoint
   directed edges while preserving their orientations.  It maps `w=-1` to
   the proved `u=-1` branch, so the full union is covered.
5. **Independent implementation.**  The primary enumerates `945` perfect
   matchings.  The isolated audit imports no project module, reconstructs
   recursive permanents, and derives the left nullspace.
6. **Scope control.**  Reverse, same-head, and chain exceptional divisors,
   larger supports, and every permanent bridge remain open.  Global status
   stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_disjoint_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_disjoint_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```
