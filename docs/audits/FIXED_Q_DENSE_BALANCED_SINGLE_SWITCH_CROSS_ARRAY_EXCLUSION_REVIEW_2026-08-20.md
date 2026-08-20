# Hostile review: fixed-Q dense balanced single-switch exclusion

## Verdict

**Accept as an exact characteristic-zero exclusion of one genuinely
nonprivate positive-dimensional chart inside the `GLD21` dense `K_4/K_4`,
`h!=0` residue.**

The result is the first nonmonomial root-to-port cut after `GLD23`.  Its
balanced normalization is a substantive chart hypothesis.  It does not
exclude a general two-amplitude `2 x 2` switch, a general colour-diagonal
cross array, or a non-colour-diagonal block.  The global conjecture remains
**UNRESOLVED**.

## Claim attacked

After the exact dense shore gauge, two colour slices are identity private
arrays and the third is

```text
I_4+E_(0,1)+tE_(1,0),    t!=0.
```

The chart is nonprivate for every allowed `t`: its switched rows and columns
each have two nonzero entries, and both the identity and transposition
root--port matchings are supported.  The theorem claims that the complete
ten-vertex GHZ equation is inconsistent for all `t` in characteristic zero.

## Adversarial checks

### 1. Is the result merely a private-permutation case in disguise?

No.  A diagonal change of root and port colour coordinates preserves the
zero pattern of a matrix.  It cannot remove either nonzero switch entry.
Consequently the chart is outside every monomial support excluded by
`GLD23`.

### 2. Is the balanced form being asserted for every switch block?

No.  The theorem explicitly assumes the normalized diagonal entries and one
off-diagonal amplitude are one.  Once the dense shore multipliers have been
normalized, a general `2 x 2` switch can retain two independent continuous
amplitudes.  The proof does not silently identify them.  That larger chart is
recorded as open.

### 3. Are root-side graph entries restricted to manufacture the detector?

No.  All `24` root--residual covector entries, all `54` root--root block
entries, and all three pure target coefficients are independent variables.
The certificate is a left relation among coefficient rows that cancels every
one of these `81` variables.

### 4. Are the matching rows complete?

Yes for each selected root/port word.  The primary enumerates all `945`
perfect matchings of the ten vertices.  Direct port blocks vanish in the
dense cell, leaving the same three vertex-count types proved in `GLD23`.
Unlike a support-only calculation, the switched root--port matrix can
contribute both identity and transposition terms, and both are included in
the recursive matching sum.

### 5. Is division by an exceptional factor hidden?

No.  The generic certificate is cleared to a polynomial identity in `Z[t]`:

```text
lambda(t) A(t)=0,
lambda(t) b(t)=-4t(t+1).
```

There is no denominator at `t=-2` or elsewhere.  The chart assumption removes
`t=0`.  The sole zero of the displayed obstruction inside the chart is
`t=-1`, and the theorem supplies a separate exact ten-row certificate there.

### 6. Does the exceptional proof assume the switched permanent is nonzero?

No.  At `t=-1`, the `2 x 2` permanent is `1+t=0`.  The ten-row combination
still cancels all `81` variables and leaves `1`.  This is an important
boundary check: the exceptional certificate is not a generic-rank statement
reused where its pivot vanished.

### 7. Are the two implementations independent?

They differ in algebra representation and row derivation.

- The primary uses SymPy expressions and builds each row by traversing all
  `945` perfect matchings.
- The audit uses only standard-library `Fraction`, represents polynomials by
  coefficient tuples, and derives each row from recursive `4 x 4`, `3 x 3`,
  and `2 x 2` permanents for the three possible matching types.

The audit imports neither the primary nor a shared project module.  Agreement
tests both the graph matching ledger and the polynomial arithmetic.

## Boundaries that must remain visible

1. The independent second switch amplitude is open.
2. Extra nonzero entries outside one `2 x 2` block are open.
3. A root-to-port edge that changes root colour is open.
4. Proper-secondary-clique and other `GLD21` cells are open.
5. The result is one fixed-`Q`, four-port, same-graph obstruction; it does not
   force this chart to occur in an arbitrary global witness.
6. No weighted-permanent restriction or local-to-global bridge follows.

## Required replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_balanced_single_switch_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_balanced_single_switch_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
```

The first pair is the new proof boundary.  The second pair protects the exact
private-permutation predecessor and makes the strict extension in support
visible.
