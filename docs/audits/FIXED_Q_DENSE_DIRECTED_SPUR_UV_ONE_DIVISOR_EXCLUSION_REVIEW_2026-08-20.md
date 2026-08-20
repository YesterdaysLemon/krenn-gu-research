# Review: fixed-Q dense directed-spur `uv=1` divisor exclusion

## Verdict

**Accept as an exact characteristic-zero pointwise exclusion of the full
`uv=1` exceptional divisor of `GLD26`.**  The case cover includes the four
curve components of the first detector, all rational residual points, and the
shared quadratic family.  The other two `GLD26` divisors remain open.  The
global conjecture is **UNRESOLVED**.

## Load-bearing checks

1. **Complete equations.**  The primary enumerates all `945` perfect
   matchings on the ten vertices and retains the `24+54+3=81` independent
   coefficient variables.  The audit derives the same coefficient rows from
   the three exhaustive matching types using recursive permanents.
2. **Legal divisor substitution.**  The chart has `u!=0`, hence `uv=1`
   permits `v=1/u`.  The first exact relation leaves
   `-4u(u+w)(w+2)(u+w+1)(uw+2u+w)`.
3. **Exhaustive curve split.**  Because `u!=0`, the four named factors are
   the complete residual locus.  Their exact detectors are `4(u+1)`,
   `2u(u-1)^2(u+1)`, `4u(u-1)(u^2+1)`, and
   `2(u-1)(u^2+1)`.
4. **No illegal denominator on the fourth curve.**  At `u=-1`,
   `uw+2u+w=-2`; therefore solving it as `w=-2u/(u+1)` loses no point.
5. **Residual cover.**  The curve detectors leave exactly four rational
   points and `u^2+1=0, v=-u, w=-u-1`.  Modulo `u^2+1`, the fourth curve's
   expression for `w` agrees with `-u-1`, so there is one shared quadratic
   family rather than an omitted second branch.
6. **Terminal contradictions.**  The point certificates leave `4,2,4,2`.
   The twelve-row quotient certificate leaves `2` modulo `u^2+1`.  These are
   nonzero in characteristic zero.
7. **Audit boundary.**  The audit shares the literal certificate tables and
   SymPy backend with the primary, but its row derivation is a separate
   matching-type/permanent implementation.  This supports an independent
   derivation check, not a claim of no shared code or arithmetic.

## Scope control

This result closes only `uv=1` inside
`I+uE_(0,1)+vE_(1,0)+wE_(0,2)`, with all three parameters nonzero.  It does
not close `uv-u-v-1=0`, `uv+vw+w+1=0`, reverse or larger spurs,
root-colour-changing blocks, proper-secondary cells, or any
weighted-permanent bridge.  No literature novelty claim is made.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_one_divisor_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_directed_spur_uv_one_divisor_exclusion.py
```
