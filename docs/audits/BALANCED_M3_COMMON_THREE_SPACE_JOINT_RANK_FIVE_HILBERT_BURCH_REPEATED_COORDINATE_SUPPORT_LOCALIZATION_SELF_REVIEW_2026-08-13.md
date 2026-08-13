# Hostile review: Hilbert--Burch repeated-coordinate support localization

## Claim under review

The proposed successor treats only the repeated-coordinate part of the
joint-rank-five Hilbert--Burch `(1,1,1)` profile.  S2AN already forces the
third factor into the coordinate plane complementary to the repeated colour.
The new theorem excludes a genuinely two-supported vector in that plane and
therefore localizes the residual to the discrete factor-line pattern
`(s,s,t)` with `s!=t`.

It does not exclude those discrete patterns or the complete Hilbert--Burch
profile.  Global status remains **UNRESOLVED**.

## Adversarial questions

### 1. Is the theorem silently strengthening S2AN's hypothesis?

No.  It assumes the same normalized, target-consistent physical `m=3`
common-three-space full-sensor stratum, `dim U=3`, `rank H=5`, the S2AG
Hilbert--Burch `(1,1,1)` normal form, and two factors proportional to the
same target coordinate.  S2AN supplies only `z_s=0`; the new argument begins
with that exact conclusion.

### 2. Why are there only two remaining support coefficients?

The third root space is ternary.  Once `z_s=0`, write uniquely
`z=a e_u+b e_v` in the other two coordinate lines.  Because every root block
in the `(1,1,1)` profile is nonzero, `z` itself is nonzero.  Thus exclusion
of `a b!=0` leaves exactly one nonzero coefficient and makes `z` coordinate.

### 3. Does the untouched grid survive at `z_s=0`?

Yes.  Every derivative term contains `e_s` in the first root, `e_s` in the
second root, or both.  Every coefficient whose first two colours lie in
`{u,v}` is therefore zero for all three third-root colours, independently of
the support of `z`.  Since `U=D_B(K)`, the complete `2 x 2 x 3` target grid is
the bare all-cross permanent.

### 4. Is the contracted row really in the kernel annihilator?

Yes.  For `z=a e_u+b e_v`, the covector
`gamma=b e_u^*-a e_v^*` satisfies `gamma(z)=0`.  Hence
`q'=theta(gamma)` comes from a covector annihilating both Hilbert--Burch
kernel generators.  Its target table has `b T_u` and `-a T_v` on the two
diagonal root pairs and zero on the crossed pairs.

### 5. Could the zero-table row `q_s` vanish?

No.  If `q_s=H^T(0,0,e_s^*)` vanished, then `e_s^*` would annihilate
`K=image H`; every `(A,B,C) in K` would have `C_s=0`.  Because `z_s=0`, the
`(s,s,s)` coefficient of

```text
D_B(A,B,C)
 =-mu A tensor e_s tensor z
  -lambda e_s tensor B tensor z
  +lambda mu e_s tensor e_s tensor C
```

would vanish for all of `K`.  Thus every tensor in `U=D_B(K)` has zero
same-colour coefficient.  The all-cross coefficient also vanishes when
`q_s=0`, whereas target consistency requires the nonzero coefficient `T_s`
modulo `U`.  This is a contradiction.  Both scripts replay the derivative
row, but the target-consistency implication is the proof just given.

### 6. Could `q_s` be nonzero but proportional to `q'`?

No.  Its entire `R x P` table is zero, while the table of `q'` contains the
nonzero value `b T_u`.  Proportionality would first force the scalar to zero
and then force `q_s=0`.  Consequently `Q=span(q',q_s)` is a genuine
two-plane.  The two diagonal targets similarly show that `R` and `P` are
two-planes.

### 7. Why do all three two-planes lie in one three-space?

The covectors defining `r_u,r_v,p_u,p_v,q',q_s` annihilate `ker D_B`.
S2AG proves `ker D_B subset K`, so their images under `H^T` lie in
`V=H^T((ker D_B)^perp)`.  Its dimension is exactly `7-4=3`, because
`dim ker D_B=2`, `dim K=5`, and the kernel of `H^T` is `K^perp`.

### 8. Why do the pairwise-distinct plane cases reuse S2AN?

Choose source-coordinate bases along the factor lines of the two fully
transverse targets.  Although both target tensors now occur at the same
third-row basis vector, the only nonzero source tensor coefficients are still
`(0,0,0)` and `(1,1,1)`.  The mixed split cubics used by S2AN therefore still
belong to the same restriction kernel.  Independent normals give
`span(A^3,B^3,C^3)` and the shared-quadratic divisor argument.  Three
distinct pencil normals give `span(A^3,B^3,AB(A+B))` and the
unique-factorization argument.  Neither proof used the binary location of
the two nonzero tensor values.

### 9. Are all equal-plane orientations covered?

Yes.  If `R=P`, symmetry of `L F` separately at the `T_u E_00` and
`T_v E_11` coefficients makes `L` diagonal.  The table becomes two
rank-one squares with zero mixed polarization on a two-plane, which S2AL
forbids.  If `R=Q`, the fixed-`p_u` table is `E_00` and the fixed-`p_v`
table is `E_10`; symmetry kills `L_10` and `L_11`, making `L` singular.
The case `P=Q` is identical.  Both checkers replay these matrix
orientations.

### 10. Does the conclusion construct or exclude `(s,s,t)`?

Neither.  The theorem proves only that a repeated-coordinate chart can
survive this argument only on one of those discrete coordinate-line
patterns.  It does not prove that the remaining target equations admit such
a pattern or that a physical graph realizes it.

### 11. What do the scripts prove and not prove?

The primary verifier replays the scalar-general derivative, its kernel and
rank, the untouched grid, the complementary contraction, the same-colour
row support, both distinct-plane kernels, the diagonal divisor ratio, all
equal-plane orientations, and representative inherited square charts.  The
independent audit imports no repository or third-party module and rebuilds
the exact identities with `Fraction`, a different coefficient ordering, and
separate elimination.  Neither script replaces the arbitrary-field divisor
and unique-factorization arguments, S2AL's square lemma, S2AN's upstream
localization, or the target-consistency argument at `(s,s,s)`.

## Verdict

The proof supports the exact conclusion that a repeated-coordinate
Hilbert--Burch `(1,1,1)` chart has factor-line pattern `(s,s,t)` with
`s!=t`.  Those discrete patterns, the other `(1,1,1)` charts, the other
Hilbert--Burch profiles, lower joint ranks, other physical branches, higher
orders, and the global Krenn--Gu conjecture remain open.
