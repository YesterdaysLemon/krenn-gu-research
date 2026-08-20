# Review: dense two-active-slice three-reciprocal-pair generic exclusion

## Verdict

**Accept as an exact characteristic-zero generic exclusion of all `220`
three-pair support masks.**  The result leaves a finite explicit exceptional
hypersurface atlas; it is not a pointwise closure.

## Adversarial checks

1. **Exact orbit cover.**  All `C(12,3)=220` directed three-arc supports are
   canonically relabelled under all `24` position permutations.  Exactly `13`
   representatives occur, with orbit sizes summing to `220`.
2. **Reciprocal semantics.**  Each ordered arc has amplitudes
   `a,a/(a-1)` in the two active colours.  Only `a=0,1` is removed as the
   standing active-support domain before the exceptional factors are listed.
3. **No sampled ranks.**  Every orbit uses an exact rational-function row
   core.  Its left-nullspace multiplier cancels all `81` nuisance variables
   and pairs with the right-hand side to exactly `1`.
4. **Denominator accounting.**  The theorem displays every factor remaining
   after deleting only constants and the always-forbidden
   `u,v,w,u-1,v-1,w-1` factors.  The two long factors `P_7,P_9` are written
   explicitly rather than hidden behind a genericity label.
5. **Primary implementation.**  The primary expands each row through all
   `945` perfect matchings on the ten-vertex auxiliary graph, derives the
   nullspaces, and asserts all thirteen factorized denominator lcms.
6. **Independent implementation.**  The isolated audit imports no project
   module, reconstructs recursive permanents and minors, reverses orbit, row,
   variable, and permutation traversal, and independently obtains the same
   census and denominators.
7. **Predecessor boundary.**  GLD43 supplies the reciprocal-support reduction.
   GLD45--GLD49 close the smaller two-pair masks but do not justify any
   specialization from three pairs to two.
8. **Scope control.**  Every displayed divisor, every support with four or
   more pairs, proper-secondary cells, and all permanent bridges remain open.
   Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_support_divisor_reduction.py
```
