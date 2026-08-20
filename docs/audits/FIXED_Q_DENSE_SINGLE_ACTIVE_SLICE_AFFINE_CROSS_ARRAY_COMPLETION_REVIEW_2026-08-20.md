# Review: dense single-active-slice affine cross-array completion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the complete
12-parameter single-active-slice affine cell.**  The twelve entry detectors
and the GLD23 origin exhaust all `4096` support masks.  The global conjecture
remains open.

## Adversarial checks

1. **Simultaneous amplitudes.**  Each row is expanded with all twelve
   off-diagonal variables present.  The cancellation does not set the other
   eleven entries to zero.
2. **All ordered entries.**  The primary and audit each check all `12`
   ordered pairs `i!=j`; neither infers untested equations from a single
   symmetry representative.
3. **Row legality.**  Every displayed pair consists of complete port/root
   word equations in the existing `81`-variable system.
4. **Sparse exact form.**  For entry `a_(ij)`, the two rows contain only a
   selected pair `P_0,P_1`, with coefficients
   `(-a_(ij),a_(ij))` and `(-1,1)` and right sides `0,-1`.
5. **No division or exceptional locus.**  Multipliers `(1,-a_(ij))` leave
   `a_(ij)`.  Thus every nonzero entry is excluded pointwise over the full
   simultaneous parameter ring.
6. **All-zero endpoint.**  With every amplitude zero, all three slices equal
   `I_4`, an exact GLD23 private-permutation instance.  The dependency has
   its own exhaustive `28`-orbit replay.
7. **Independent implementation.**  The primary enumerates `945` perfect
   matchings.  The isolated audit imports no project module, reconstructs
   recursive permanents, derives all twelve nullspaces, and enumerates the
   `4096` support masks.
8. **Scope control.**  Only one colour slice is allowed to be nonprivate.
   Multiple nonprivate slices, root-colour-changing blocks,
   proper-secondary cells, and all permanent implications remain open.
   Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_single_active_slice_affine_cross_array_completion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_single_active_slice_affine_cross_array_completion.py
python claims/arbitrary-order/verify_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_affine_chart_completion.py
```
