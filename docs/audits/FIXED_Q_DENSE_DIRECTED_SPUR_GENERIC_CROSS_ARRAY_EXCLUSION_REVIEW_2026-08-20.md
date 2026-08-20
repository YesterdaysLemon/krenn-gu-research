# Hostile review: fixed-Q dense directed-spur generic exclusion

## Verdict

**Accept as an exact characteristic-zero exclusion of a Zariski-open subset
of one three-parameter larger-support chart inside the `GLD21` dense
`K_4/K_4`, `h!=0` residue.**

The result crosses the support boundary left by `GLD25`, but it is generic,
not pointwise on the whole directed-spur chart.  Four explicitly named
divisors remain open.  The global conjecture remains **UNRESOLVED**.

## Claim attacked

After the canonical dense shore gauge, two colour slices are `I_4` and the
third is

```text
I_4+uE_(0,1)+vE_(1,0)+wE_(0,2),    u,v,w!=0.
```

With all `78` root-side coefficients and three pure target scalars free, the
complete GHZ equation is claimed inconsistent when

```text
(uv-1)(uv+1)(uv-u-v-1)(uv+vw+w+1) != 0.
```

## Adversarial checks

### 1. Is this just `GLD25` with a renamed parameter?

No.  The nonzero `E_(0,2)` entry adds a seventh support position to the
active `4 x 4` colour slice.  Diagonal coordinate rescaling and index
permutation preserve support cardinality and cannot remove it.  The new edge
contributes to three-root and two-root partial permanents, even though a lone
directed spur does not create a new full `4 x 4` perfect matching.

### 2. Is `w=0` silently used?

No.  Every row is constructed with symbolic `w`, and the final detector has
a visible factor `w`.  The theorem assumes `w!=0`.  The boundary `w=0` is
not proved by this relation; it is independently and pointwise excluded by
`GLD25`.

### 3. Are graph-side variables restricted?

No.  All `24` root--residual entries, `54` root--root entries, and three pure
target scalars remain independent.  The sixteen-row relation cancels all
`81` coefficients.

### 4. Are the complete matching rows actually complete?

Yes.  The primary traverses all `945` perfect matchings on the ten vertices
for every selected word.  The audit derives the same rows independently from
the three exhaustive nonzero matching types and recursive `4 x 4`, `3 x 3`,
and `2 x 2` permanents.  In particular, it includes every occurrence of the
new `w` edge in partial matchings.

### 5. Is the detector numerical or modular evidence?

No.  Both implementations prove the polynomial identity

```text
lambda A = 0,
lambda b = uvw(uv-1)(uv+1)^2
           (uv-u-v-1)(uv+vw+w+1)^2
```

over exact characteristic-zero arithmetic.  Numerical finite-field rank
search is not part of the durable proof boundary.

### 6. Is division hiding an exceptional fibre?

No.  Every displayed multiplier is polynomial in `u,v,w`.  The final
identity has no denominator and specializes legally on all four residual
divisors.  On those divisors its right side becomes zero, so this particular
certificate proves nothing there.

### 7. Are the four divisors claimed to contain witnesses?

No.  They are residual proof obligations.  Some may be inconsistent for
other coefficient relations; this theorem neither promotes them to
solutions nor claims to have closed them.

### 8. Is “generic” being used as if it meant every field point?

No.  The theorem gives both formulations precisely:

- pointwise exclusion on the open set where the four factors are nonzero;
- equivalently, exclusion of the generic point of the three-parameter chart.

It does not make a specialization argument across the exceptional locus.

### 9. Are the two implementations independent?

They differ in derivation and algebra representation.

- The primary uses SymPy and direct enumeration of all `945` matchings.
- The audit uses only the standard library, sparse exact `Fraction`
  dictionaries for `Q[u,v,w]`, and recursive permanents for the three
  matching types.

The audit imports neither the primary nor a shared project module.

### 10. Does the result close the larger-support dense cell?

No.  Besides the four residual divisors, the reverse spur, another
nonidentity colour slice, any further support entry, root-colour-changing
cross blocks, and the proper-secondary cells remain open.  Nothing here
forces an arbitrary witness into this chart or yields a weighted-permanent
restriction.

## Required replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_generic_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_directed_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_amplitude_single_switch_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_two_amplitude_single_switch_cross_array_exclusion.py
```

The first pair is the new generic proof boundary.  The second pair protects
the pointwise `w=0` predecessor and keeps the quantifier change visible.
