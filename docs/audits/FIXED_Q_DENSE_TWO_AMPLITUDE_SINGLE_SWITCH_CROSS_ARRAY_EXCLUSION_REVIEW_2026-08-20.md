# Hostile review: fixed-Q dense two-amplitude single-switch exclusion

## Verdict

**Accept as an exact characteristic-zero exclusion of the full
two-independent-off-diagonal-amplitude `2 x 2` switch chart inside the
`GLD21` dense `K_4/K_4`, `h!=0` residue.**

The theorem strictly extends `GLD24`: setting `u=1`, `v=t` recovers its
balanced chart.  The new proof closes every exceptional component of its
generic bivariate detector.  It does not exclude a larger-support nonprivate
colour slice, a root-colour-changing cross block, or any other `GLD21` cell.
The global conjecture remains **UNRESOLVED**.

## Claim attacked

After the exact dense shore gauge, two colour slices are identity private
arrays and the third is

```text
I_4+uE_(0,1)+vE_(1,0),    u,v!=0.
```

The complete ten-vertex GHZ equation is claimed inconsistent at every point
of this two-dimensional chart, with all `78` root-side entries and all three
pure target scalars left free.

## Adversarial checks

### 1. Is one off-diagonal amplitude silently normalized away?

No.  Both `u` and `v` remain independent throughout the row construction.
The generic obstruction is genuinely bivariate:

```text
2uv(u+1)(uv+1)(uv-u-v-1).
```

The theorem does retain the four unit diagonal entries as a chart
normalization.  It therefore does not claim that an arbitrary nonprivate
`2 x 2` block, after the already-used dense shore gauge, has only these two
parameters.

### 2. Is this merely a monomial/private chart?

No.  Since `u,v!=0`, the switched rows and columns each contain two nonzero
entries.  The identity and transposition root--port matchings are both
supported.  Diagonal coordinate rescaling preserves this zero pattern and
cannot turn the slice into a private permutation.

### 3. Are root-side variables restricted to manufacture the relation?

No.  Every one of the `24` root--residual entries, `54` root--root entries,
and three pure target scalars is independent.  Each displayed certificate
annihilates all `81` coefficients.

### 4. Are the selected coefficient rows complete?

Yes.  The primary verifier traverses all `945` perfect matchings on the ten
vertices for each selected word.  The independent audit instead derives the
same rows from the three exhaustive nonzero matching types and recursive
permanents.  Both switch entries can occur in these permanents, including
simultaneously; neither implementation truncates to the balanced slice.

### 5. Does the generic detector prove the exceptional divisors?

No, and the theorem does not claim that it does.  With `u,v!=0`, its remaining
zero set is exactly

```text
u=-1,    uv=-1,    uv-u-v-1=0.
```

Separate exact relations leave, respectively,

```text
2v(v-1),    2(u^2+2u-1),    -2u(u+1)^2(u^2+2u-1).
```

These relations are replayed after the relevant substitution rather than by
dividing the generic relation by a vanishing factor.

### 6. Is the divisor cover exhaustive at intersections?

Yes.  On `u=-1`, nonzero `v` leaves only `v=1`; a seven-row certificate gives
`0=1` there.  On `uv=-1`, only `q=u^2+2u-1=0` survives; a thirteen-row
certificate gives `0=1` modulo `q`.  On `f=uv-u-v-1=0`, the legal
parameterization `v=(u+1)/(u-1)` leaves the same `q`.  The identity

```text
uv+1=q/(u-1)
```

shows that `f=q=0` is already the quadratic part of `uv=-1`.  Thus no pairwise
or triple intersection is omitted.

### 7. Are denominator assumptions valid?

Yes.  The `uv=-1` substitution divides only by `u`, which is nonzero by the
chart.  The `f=0` substitution divides by `u-1`, and `f(1,v)=-2` in
characteristic zero.  The quadratic certificate is an identity in
`K[u]/(q)` after setting `v=-u-2`; it does not assume that `q` splits over
`K`.

### 8. Does characteristic zero matter?

Yes.  The contradiction constants contain factors of two and the point and
quadratic certificates contain `1/2`.  The theorem states characteristic
zero and makes no positive-characteristic claim.

### 9. Are the two implementations independent?

They differ in row derivation and algebra representation.

- The primary uses SymPy expressions and a direct enumeration of all `945`
  perfect matchings.
- The audit uses only the Python standard library, sparse bivariate
  `Fraction` dictionaries, recursive permanents for the three matching
  types, Laurent substitution, rational-curve numerator clearing, and a
  separately implemented quadratic quotient reduction.

The audit imports neither the primary verifier nor any shared project module.

### 10. Does the result close the dense nonprivate cell?

No.  It excludes exactly a two-dimensional support chart.  Extra entries in
the active `4 x 4` slice, nonidentity second slices, colour-changing cross
blocks, and the proper-secondary-clique cells remain open.  No theorem here
forces an arbitrary witness into this chart or implies a weighted-permanent
restriction.

## Required replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_amplitude_single_switch_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_two_amplitude_single_switch_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_balanced_single_switch_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_balanced_single_switch_cross_array_exclusion.py
```

The first pair is the new proof boundary.  The second pair protects the
strictly subsumed `GLD24` slice and its independently documented certificate.
