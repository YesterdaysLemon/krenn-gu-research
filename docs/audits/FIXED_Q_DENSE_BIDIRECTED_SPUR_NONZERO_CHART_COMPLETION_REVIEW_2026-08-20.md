# Review: dense bidirected-spur nonzero-chart completion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the complete
nonzero GLD31 chart.**  The two-row identity closes all five exceptional
divisors and subsumes GLD31--GLD38 on this chart.  The global conjecture
remains open.

## Adversarial consolidation checks

1. **Row legality.**  Both rows belong to the complete GLD31 coefficient
   system, which contains every port/root word pair and leaves all `81`
   root-side and pure-target variables independent.
2. **No hidden specialization.**  The rows are expanded over
   `Z[u,v,w,z]`.  Neither `uv=-1`, `z=1`, nor any other divisor equation is
   substituted.
3. **Transparent support.**  The first row is exactly
   `-w p_(0,2,1)+w p_(1,2,1)=0`; the second is exactly
   `-p_(0,2,1)+p_(1,2,1)=-1`.  All other coefficients vanish.
4. **Exact contradiction.**  The multipliers `(1,-w)` cancel the two
   remaining variables and leave `w`.  The original GLD31 chart assumes
   `w!=0`; there is no division or exceptional fibre.
5. **Independent implementation.**  The primary directly enumerates the
   `945` ten-vertex perfect matchings.  The isolated audit imports no project
   module, reconstructs recursive permanents, and derives `[1,-w]` as the
   unique two-row left-null vector.
6. **Prior-specialization issue.**  GLD34 used the same pair only after
   setting `v=-1/u,z=1`.  This review does not remove those substitutions by
   analogy: both implementations freshly verify that the unspecialized rows
   contain neither `u`, `v`, nor `z`.
7. **Scope control.**  The result completes the nonzero bidirected-spur
   coordinate chart only.  Broader arrays, support-drop boundaries,
   root-colour-changing blocks, proper-secondary cells, and all permanent
   implications remain open.  Global status stays **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_nonzero_chart_completion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_nonzero_chart_completion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
```
