# Review: three-pair out-fork colour-exchange exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O5`.**  The complete out-fork system is isomorphic to the pointwise-empty
GLD57 in-fork system, so all `12` O5 masks are empty.

## Adversarial checks

1. **Covariance dependency.**  GLD55 proves active-colour exchange for the
   complete equation system, including the asymmetric helper sign.
2. **Parameter scope.**  `t->t/(t-1)` is an involution of the exact active
   domain; no exceptional value is lost.
3. **Orbit map.**  Reversing `01,12,31` gives `10,21,13`; the explicit
   permutation `(0,1,2,3)->(1,0,3,2)` gives the O5 representative `01,02,30`.
4. **Complete equations.**  The primary checks every coefficient and right-
   hand side in all `6561` rows for the two supports.
5. **Independent implementation.**  The no-import audit enumerates all `945`
   matching topologies and independently rederives the sign cancellation.
6. **Pointwise source.**  The conclusion uses GLD57's full seven-stratum O11
   exclusion, not merely a generic certificate.
7. **Scope control.**  Five three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_fork_colour_exchange_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_fork_colour_exchange_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_fork_exceptional_divisor_exclusion.py
```
