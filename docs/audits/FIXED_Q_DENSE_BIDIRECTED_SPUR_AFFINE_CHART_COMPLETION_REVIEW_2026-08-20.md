# Review: dense bidirected-spur affine-chart completion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the complete
four-parameter affine coordinate family.**  The case split removes all
nonzero hypotheses from GLD39 and closes every support mask of the displayed
four-edge star.  The global conjecture remains open.

## Adversarial checks

1. **Boundary legality.**  Setting an off-diagonal amplitude to zero merely
   deletes the corresponding root--port matchings.  The complete coefficient
   equations are polynomial in `u,v,w,z`; no normalization or division is
   used in the four identities.
2. **Global outgoing-edge detectors.**  The `(1022;0122)/(2122;2122)` pair
   leaves `u` and the `(1202;0212)/(2212;2212)` pair leaves `w`, without any
   substitution.
3. **Residual incoming-edge detectors.**  After the proved consequences
   `u=w=0`, the `(0100;1000)/(1222;1222)` pair leaves `v` and the
   `(0010;1000)/(1222;1222)` pair leaves `z`.
4. **Exact case cover.**  The order `u`, `w`, `v`, `z`, all-zero assigns all
   `16` support masks.  The audit enumerates these masks independently.
5. **All-zero endpoint.**  At `u=v=w=z=0`, every colour slice is `I_4`, an
   explicit member of the GLD23 private-permutation chart.  This is a proved
   dependency, not an inferred limiting argument.
6. **Independent implementation.**  The primary enumerates `945` perfect
   matchings directly.  The isolated audit imports no project module,
   reconstructs recursive permanents, and derives each two-row nullspace.
   GLD23 has its own exhaustive `28`-orbit certificate replay.
7. **Scope control.**  This completes one affine four-edge coordinate family,
   not general nonprivate cross arrays, root-colour-changing blocks,
   proper-secondary cells, or a weighted-permanent bridge.  Global status
   remains **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_affine_chart_completion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_affine_chart_completion.py
python claims/arbitrary-order/verify_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_nonzero_chart_completion.py
```
