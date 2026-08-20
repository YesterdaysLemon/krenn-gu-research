# Review: dense two-active-slice reciprocal-support divisor reduction

## Verdict

**Accept as an exact characteristic-zero pointwise reduction of the complete
24-parameter two-active-slice affine cell.**  The twelve divisor equations
force transpose-matched support; GLD41 and GLD42 remove the zero- and one-pair
strata.  The remaining `4083` support patterns are open, not proved nonempty.

## Adversarial checks

1. **All amplitudes simultaneous.**  Each selected row is expanded over the
   polynomial ring in all twenty-four off-diagonal amplitudes.  No other
   coordinate is set to zero to obtain a reciprocal divisor.
2. **All ordered pairs.**  The primary and audit each check all `12` ordered
   pairs `i!=j`; neither promotes one representative solely by symmetry.
3. **Complete legal rows.**  Every relation uses three complete port/root
   word equations in the existing `81`-variable system.
4. **No division in the theorem edge.**  The polynomial multiplier
   `(1,-x_(ij),-y_(ji))` leaves `-(x_(ij)y_(ji)-x_(ij)-y_(ji))` exactly.
   Division is used only afterward to describe a nonzero divisor component.
5. **Support logic.**  Setting either reciprocal amplitude to zero in the
   divisor forces the other to zero.  Therefore the two supports are exact
   transposes, not merely one contained in the other.
6. **Lower-support dependencies.**  The empty matched mask is a GLD41/GLD23
   boundary.  Every one-pair matched mask is a position relabelling of GLD42;
   no stronger two-pair claim is imported.
7. **Census boundary.**  There are exactly `4096` matched masks, of which one
   has size zero and twelve have size one, leaving `4083`.  These are residual
   candidates only; the theorem does not claim they satisfy the equations.
8. **Independent implementation.**  The primary enumerates `945` perfect
   matchings.  The isolated audit imports no project module, uses recursive
   permanents, derives each nullspace, and recomputes the support census.
9. **Scope control.**  The theorem concerns two unit-diagonal active colour
   slices and one identity slice.  Proper-secondary cells, root-colour-
   changing blocks, and every weighted-permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_support_divisor_reduction.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_reciprocal_support_divisor_reduction.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_spike_affine_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_single_active_slice_affine_cross_array_completion.py
```
