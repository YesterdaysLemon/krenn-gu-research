# Review: three-pair directed-path exceptional-divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise closure of GLD50 orbit
`O10`.**  Combined with the generic theorem, all `24` directed length-three
path masks are empty.

## Adversarial checks

1. **Complete orbit residue.**  GLD50 leaves exactly `uv+v+1=0` for `O10`;
   there is no omitted second component.
2. **Exact parametrization.**  Solving the surface gives
   `v=-1/(u+1)` and reciprocal amplitude `v/(v-1)=1/(u+2)`.
3. **Legal domain.**  Active reciprocal support forbids
   `u=0,1,-1,-2` and `w=0,1` on this surface.
4. **Denominator exhaustion.**  The fourteen-row certificate denominator is
   `uw(u-1)`, whose entire zero locus is already forbidden.
5. **Exact contradiction.**  The multiplier cancels all `81` retained
   variables and leaves `1`; the result does not come from a sampled rank.
6. **Independent implementation.**  The primary expands all `945` perfect
   matchings and replays stored weights.  The isolated audit imports no
   project module, reconstructs recursive permanents, and derives the
   nullspace.
7. **Orbit scope.**  GLD50's exact census carries the canonical proof to all
   `24` labelled directed-path masks.
8. **Scope control.**  Twelve three-pair exceptional unions, larger supports,
   proper-secondary cells, and every permanent bridge remain open.  Global
   status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_directed_path_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_directed_path_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```
