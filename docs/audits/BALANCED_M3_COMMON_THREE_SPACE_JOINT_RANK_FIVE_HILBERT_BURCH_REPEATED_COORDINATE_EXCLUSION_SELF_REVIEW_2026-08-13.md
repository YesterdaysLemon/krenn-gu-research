# Self-review: repeated-coordinate Hilbert--Burch exclusion

Date: 2026-08-13

## Verdict

**Pass for the stated characteristic-zero repeated-coordinate `(1,1,1)`
scope.**  The proof excludes the discrete residual `(s,s,t)`, `s!=t`, left
by S2AN--S2AO.  It does not close coordinate-distinct `(1,1,1)`, other
Hilbert--Burch profiles, lower joint rank, other physical strata, higher
orders, or global Krenn--Gu.  Global status remains **UNRESOLVED**.

## Adversarial checks

### 1. Does the S2R application really see a fully supported product?

Yes.  In the discrete normal form the derivative-kernel annihilator is

```text
lambda alpha_s+nu gamma_t=0,
mu beta_s+nu gamma_t=0.
```

The seven coordinates used for this linear space are exactly
`alpha_t,alpha_u,beta_t,beta_u,gamma_u,gamma_s,gamma_t` (with the last
coordinate represented by the combined row `h`).  If all seven are nonzero,
the two equations also make `alpha_s,beta_s` nonzero.  Thus all nine root
coordinate evaluations are nonzero.  Direct substitution gives
`D_B^T(alpha tensor beta tensor gamma)=nu^2 gamma_t^2
(alpha,beta,gamma)`, so a point of `K^perp` would produce the forbidden
fully supported product annihilator of `U=D_B(K)`.

### 2. Is the finite-union step valid pointwise rather than generically?

Yes.  The four-dimensional linear space `K^perp` has no point outside the
union of seven coordinate hyperplanes.  Over the infinite characteristic-
zero base field, an irreducible linear space contained in a finite union of
closed hyperplanes is contained in one member.  No generic member is promoted
to a pointwise statement; the conclusion is an exact containment.

### 3. Is hyperplane containment really equivalent to a coloop?

Yes.  The seven displayed annihilator coordinates form a basis of the
seven-space `(ker D_B)^perp`.  Their transposed rows give a surjective map to
the three-space `H^T((ker D_B)^perp)` with four-dimensional kernel `K^perp`.
If the kernel has zero coordinate `j`, its restriction to the other six
basis vectors still has a four-dimensional kernel and hence rank two.  The
omitted row is outside that two-plane because the full rank is three.

### 4. Are all seven coloop orientations covered?

Yes.  The rows are `r_t,r_u,p_t,p_u,q_u,q_s,h`.  A coloop among
`h,q_u,q_s` makes `R=P`; a coloop among `r_t,r_u` makes `P=Q`; a coloop among
`p_t,p_u` makes `R=Q`.  The first/second-root symmetry exchanges the last
two groups, and the proof separately handles the two colours within the
`P=Q` group.

### 5. Does the `R=P` step reuse S2AL with the right hypotheses?

Yes.  `q_t` is outside the common three-space because its quotient is the
sum of the two independent quotient directions supplied by `r_s,p_s`.
Hence `span(q_t,q_u)` is a two-plane.  Coefficientwise symmetry makes the
change matrix between `R` and `P` diagonal.  The untouched grid then has
zero mixed polarization and two nonzero rank-one square maps onto `T_t,T_u`,
which are fully transverse.  These are exactly the hypotheses of the S2AL
two-plane square lemma.

### 6. Does the `r_u` coloop contradiction use a touched coefficient?

No.  All vanishing identities used there are from the explicit untouched
rectangles with third-root colours `u,s`.  The only appearance of `q_t` is
after substituting the exact quotient relation `q_t=A+B-h`; its three terms
are killed separately by those untouched identities.

### 7. Does the quadratic-annihilator lemma assume that every restriction is nonzero?

No.  It uses nonzero restrictions only for the three target-`1` forms, which
are forced by the nonzero `T_1` coefficient.  If an off-target restriction
is zero, it simply does not count as an active source family.  If active
off-target forms occur in two source families, unique factorization forces
all three target-`1` forms onto the derivative-kernel line, contradicting
their nonzero derivative.  Thus at most one source family is active.  The
subsequent quotient projections use the nonzero target forms `x,z` (or their
symmetric alternatives), again forced by `T_1`, so multiplication is
injective in the binary polynomial ring.

### 8. Could the mixed image in the final lemma be zero?

The application supplies a nonzero rank-one image `span(T_t)`, so no.  The
lemma proves that any nonzero mixed image of the two quadratic annihilators
shares two source factor lines with `T_u`; it therefore cannot equal the
fully transverse `T_t`.

### 9. Are the computational checks independent?

The primary verifier uses SymPy matrices, Kronecker products, and symbolic
parameters.  The audit imports no repository or third-party module, uses a
third-index-major sparse tensor convention, standard-library `Fraction`
arithmetic, and separately coded elimination.  Both replay displayed exact
identities; neither replaces the finite-union, UFD, or inherited square
proofs.

## Scope boundary

The theorem closes only the branch in which two Hilbert--Burch triangle
factors use the same target-coordinate line.  It must not be cited as a
complete `(1,1,1)`, joint-rank-five, `m=3`, or global exclusion.
