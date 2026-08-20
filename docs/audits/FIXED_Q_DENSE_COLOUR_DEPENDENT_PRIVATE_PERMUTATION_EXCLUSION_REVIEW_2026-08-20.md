# Hostile review: fixed-Q dense colour-dependent private-permutation exclusion

## Verdict

**Accept as an exact characteristic-zero exclusion of the full private
colour-diagonal permutation chart inside the `GLD21` dense `K_4/K_4`,
`h!=0` residue.**

The result closes the colour-dependent private-permutation residual left by
`GLD22`.  It does not close the dense cell, because a general root-to-port
colour slice need not be monomial.  It changes neither any weighted-
permanent claim nor the global Krenn--Gu status, which remains
**UNRESOLVED**.

## Claim attacked

The theorem assumes that each of the three root-to-port colour slices is a
nonzero monomial `4 x 4` array and is diagonal in the corresponding root
colour.  The three supporting permutations may differ.  It claims that no
single physical graph in the dense `GLD21` cell can satisfy the complete
fixed-`Q` GHZ coefficient equations on that chart.

This is stronger than `GLD22`, whose elementary `-2hP` detector required one
common permutation.  It is weaker than excluding arbitrary invertible or
arbitrary nonprivate cross arrays.

## Adversarial checks

### 1. Does the shore normalization silently impose a special dense point?

No.  The proof first derives, rather than assumes, that all active `c` shores
lie on one nonisotropic line and all active `d` shores on its orthogonal
nonisotropic line.  Four ports are load-bearing here: comparing the three
orthogonality conditions away from two different ports identifies the
lines.  The dense `K_4/K_4` nonvanishing guarantees that neither line nor any
port multiplier vanishes.

Residual contraction rescaling fixes the two line directions and `h`.
Port-colour rescaling removes shore multipliers, and the bijectivity of each
private permutation lets independent root-colour rescaling remove every
private edge scalar.  A square root may be needed to set `h=1`, but extending
to an algebraic closure is legitimate for a nonexistence proof.  A witness
over the original field would remain a witness after extension.

### 2. Do the coordinate changes destroy the GHZ target?

No.  All external changes are diagonal by vertex and colour.  They change
the three pure coefficients but create no mixed target coefficient.  The
affine system goes further and treats all three pure coefficients as free
unknowns, even permitting zero.  The contradiction therefore does not rely
on an unrecorded target normalization or nonzero target scalar.

### 3. Are graph variables accidentally identified or omitted?

No.  The normalized system includes all `24` evaluations of the eight
root--residual covectors and all `54` evaluations of the six root--root
blocks.  They are independent unknowns.  The only omitted root-side data
would multiply a direct port--port block, and all such blocks are exactly
zero in the `GLD21` dense cell.

This makes the computation conservative: it ignores any additional
same-block tensor structure that could only shrink the solution set.

### 4. Are the three matching types exhaustive?

Yes.  With ten vertices and no port--port edge, a nonzero perfect matching
has exactly one of:

1. the two residual vertices paired together and four root--port edges;
2. one residual--root, one residual--port, and three root--port edges;
3. two residual--port, two root--port, and one root--root edge.

A matching with both residual vertices on roots leaves too many ports unless
a zero direct port block is used.  Any second unrestricted root block has the
same deficit.  The primary checker nevertheless avoids trusting this prose:
it independently enumerates all `945` perfect matchings and obtains the same
systems certified by the theorem.

### 5. Is the permutation case split exact?

Yes.  Relabelling roots and ports together after `pi_a=id` acts by simultaneous
conjugation on `(pi_c,pi_d)`.  Swapping active colours exchanges the ordered
pair.  The primary reconstructs the resulting `28` orbits and pins their
sizes, whose sum is `576=24^2`.  The independent audit bypasses this quotient
entirely and checks all `576` ordered pairs.

### 6. Is modular evidence being promoted to characteristic zero?

No.  Both routes use exact `Fraction` arithmetic.  The primary produces an
explicit left combination with `lambda A=0` and `lambda b=1` for every orbit;
the cores use `5` to `20` coefficient rows and their combined digest is
pinned.  The audit independently performs exact rational elimination on all
ordered pairs.  No floating-point, random specialization, or finite-field
rank is load-bearing.

### 7. Are the two checkers genuinely independent?

They differ in the material derivation that is most vulnerable to error.

- The primary starts from recursive ten-vertex perfect matchings, builds
  coefficient rows from the actual edge types, uses symmetry reduction, and
  replays explicit left-combination certificates.
- The audit starts from a closed three-type formula, performs no symmetry
  reduction, and runs a separately written sparse elimination for every pair.

The audit imports neither the primary nor a shared project module.  Agreement
therefore tests both the perfect-matching ledger and the group-action cover,
not merely two random seeds of one computation.

## Boundaries that must remain visible

1. **Private is load-bearing.**  A nonprivate colour slice can contain
   several root--port entries in a row or column.  The permutation map
   `f_omega` no longer describes its companion support, and the finite system
   here is not applicable.
2. **Dense `K_4/K_4` is load-bearing.**  Proper-secondary cells do not have
   the same two nonisotropic global shore lines, and direct blocks may remain.
3. **The result is local and fixed-`Q`.**  It excludes a same-graph chart for
   one four-port contraction.  It does not force such a chart to occur in an
   arbitrary global witness.
4. **No permanent bridge is supplied.**  The result neither proves a weighted
   permanent identity nor closes universal extraction or local-to-global
   synchronization.
5. **The computation is a proof leaf, not the whole proof.**  Exact
   elimination discharges the finite normalized permutation family.  The
   written shore-line and gauge lemmas are the bridge that makes those
   certificates relevant to arbitrary chart scalars.

## Required replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_private_cross_matching_root_companion_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_private_cross_matching_root_companion_exclusion.py
```

The first pair is the new primary/audit boundary.  The second pair protects
the elementary `GLD22` predecessor and confirms that the common-permutation
subchart remains independently replayable rather than being silently
replaced by the finite certificate.
