# Review: dense two-active-slice same-tail exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of the GLD44
same-tail exceptional divisor.**  Combined with the generic theorem, all
`12` same-tail support masks are empty.  The other four two-pair orbit
divisors remain open.

## Adversarial checks

1. **Exact inherited divisor.**  GLD44 leaves only `u=-1` on the canonical
   same-tail chart.  GLD43 then forces its reciprocal amplitude to `1/2`;
   no additional specialization is hidden.
2. **Active-domain cover.**  The second pair has `w!=0`, and its reciprocal
   divisor forbids `w=1`.  These are exactly the two denominator roots of the
   new certificate.
3. **Complete legal rows.**  All twelve displayed pairs are complete
   port/root word equations in the same `81`-variable system.
4. **Exact contradiction.**  The rational multiplier cancels every retained
   coefficient and leaves `1`; it is not a numerical rank observation.
5. **Independent implementation.**  The primary enumerates `945` perfect
   matchings and replays the stored multiplier.  The isolated audit imports no
   project module, reconstructs recursive permanents, and derives the
   nullspace.
6. **Orbit conclusion.**  Position relabelling covers all `12` same-tail
   masks.  GLD44 handles `u!=-1`; this theorem handles `u=-1`, so the orbit is
   pointwise empty.
7. **Scope control.**  Reverse, same-head, chain, and disjoint exceptional
   divisors, all larger supports, and every permanent bridge remain open.
   Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_same_tail_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_same_tail_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```
