# Review: three-pair reverse-fork colour-exchange exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O12`.**  The complete reverse-fork system is isomorphic to the pointwise-
empty GLD53 fork-path system, so all `24` O12 masks are empty.

## Adversarial checks

1. **Covariance dependency.**  GLD55 proves the active-colour exchange on the
   complete equation system, including the asymmetric sign of helper `y`.
2. **Parameter scope.**  `t->t/(t-1)` is an involution of the exact legal
   active domain; no exceptional value is lost or introduced.
3. **Orbit map.**  Reversing `01,02,13` gives `10,20,31`; the explicit
   position permutation `(0,1,2,3)->(2,1,3,0)` gives the O12 representative
   `01,12,32`.
4. **Complete equations.**  The primary checks all coefficients and right-
   hand sides in all `6561` rows for these two supports.
5. **Independent implementation.**  The no-import audit enumerates all `945`
   matching topologies and rederives the helper/coordinate sign cancellation,
   rather than calling either row constructor.
6. **Pointwise source.**  The conclusion uses GLD53's full pointwise O4
   exclusion, including both surfaces and their intersection.
7. **Scope control.**  Seven three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_reverse_fork_colour_exchange_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_reverse_fork_colour_exchange_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_fork_path_exceptional_divisor_exclusion.py
```
