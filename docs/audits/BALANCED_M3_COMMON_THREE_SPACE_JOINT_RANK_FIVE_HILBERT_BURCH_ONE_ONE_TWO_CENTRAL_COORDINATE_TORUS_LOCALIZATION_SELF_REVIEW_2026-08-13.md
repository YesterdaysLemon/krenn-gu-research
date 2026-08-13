# Self-review: Hilbert--Burch `(1,1,2)` central-coordinate torus localization

Date: 2026-08-13

Claim under review:

[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COORDINATE_TORUS_LOCALIZATION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COORDINATE_TORUS_LOCALIZATION_THEOREM.md)

Global status after this claim: **UNRESOLVED**.

## Scope and adversarial questions

### 1. Does the theorem claim to cover all of `(1,1,2)`?

No.  It treats the central coordinate-pair chart `x=lambda e_s`,
`y=mu e_t`.  For distinct `s,t`, it excludes the two repeated outer-factor
lines `w proportional e_s` and `z proportional e_t` from its hypotheses.
It also does not treat the minimal outer coordinate-pair charts `(x,w)` or
`(y,z)`.  Its conclusion is a four-orientation ordinary-coloop
localization, not a profile exclusion.

### 2. Is the central coordinate-pair chart an invented restriction?

No.  S2AG proves the complete `(1,1,2)` coordinate atlas: the minimal
allowed coordinate pairs are `(x,y)`, `(x,w)`, and `(y,z)`, with additional
coordinate factors permitted.  This theorem selects the first of those
three exact branches and states its residual boundaries explicitly.

### 3. Is `dim span(z,w)=2` used?

Yes, in three load-bearing places: the Hilbert--Burch derivative has rank
seven; the third projection of `K` has dimension at least two, hence
`rank theta>=2`; and `z^perp intersect w^perp` is a line.  Neither replay
tests a dependent pair.

### 4. Are `R` and `P` really two-planes when `s!=t`?

Yes.  The third colour `u` supplies an untouched nonzero `(u,u,u)` target.
The remaining rows `r_t,p_s` cannot vanish because their vanishing says the
corresponding coordinate functional annihilates `K`, after which both the
all-cross term and `D_B(K)` miss the required `T_t` or `T_s` diagonal.
Untouched crossed coefficients separate each such row from the `u` row.

### 5. Why are there nine torus hyperplanes rather than seven or eight?

The free coordinates on the seven-dimensional annihilator are the two
off-`s` alpha coordinates, two off-`t` beta coordinates, and all three gamma
coordinates.  The constrained coordinates are

```text
alpha_s=-gamma(z)/lambda,
beta_t=-gamma(w)/mu.
```

Thus full root-coordinate support requires all seven free coordinates and
both recovery factors `gamma(z),gamma(w)` to be nonzero.  The exact
transpose identity has scalar `gamma(z)gamma(w)`.  No factor is dropped.

### 6. Does the finite-union argument require the nine hyperplanes to be distinct?

No.  Each is a proper linear hyperplane; some can coincide on special
supports of `z,w`.  A linear four-space over an infinite field contained in
their finite union lies in at least one member.  Duplicates do not change
the conclusion.

### 7. Why do the five gamma alternatives force `R=P`?

For `gamma_k=0`, deleting the corresponding basis row `h_k` leaves a
six-dimensional domain containing the preimages of both `R` and `P`.  Its
kernel is the four-plane `N`, so its image has dimension two.  For
`gamma(z)=0` and `gamma(w)=0`, use the corresponding six-dimensional
hyperplane of `L`; it again contains those four preimages and has kernel
`N`.  Since `R,P` are already two-planes, both must equal that image.

### 8. Is the same-colour equality case transferred correctly from S2AL?

Yes.  The complete untouched binary cube on the two complementary colours
has exactly the two diagonal targets.  Permanent symmetry makes the
change-of-basis matrix between equal `R,P` diagonal.  The two third-root
rows are independent by diagonal/crossed evaluation.  The resulting two
rank-one squares and zero mixed map on a two-plane are exactly the S2AL
two-square lemma.

### 9. Why are the exterior maps nonzero in the distinct-colour case?

The `T_s` face is controlled by the restriction of `gamma_s` to `w^perp`.
That restriction is zero exactly when `w proportional e_s`.  The analogous
`T_t` map is zero exactly when `z proportional e_t`.  These are precisely
the two explicit exclusions in the hypothesis.  No full-support assumption
on `z` or `w` is made.

### 10. Does equal `R,P` really align `span(r_t)=span(p_s)`?

Yes.  At `q_u` the untouched permanent matrix has rank one, with left
radical `span(r_t)` and right radical `span(p_s)`.  On one common plane the
permanent is symmetric, so its left and right radicals agree.  The other
core tables then give the square/mixed identities in the proof.

### 11. Is the source-support split exhaustive and exact?

Yes.

- A pure common radical fixes one source factor in every nonzero mixed
  value.
- With three active components, its square kernel is exactly the
  two-dimensional scaling plane.  Since `rank theta>=2`, the complete third
  row image is that plane, and all mixed values lie in one Segre tangent
  space.
- With two active components, square-zero puts all third rows in the sum of
  those two sources.  The exact tangent map is
  `L(q)=x tensor q_Y+q_X tensor y`; its kernel is
  `span(x,-y)`.

The primary replay expands all three cases symbolically.  The independent
audit uses a separate rational permanent implementation and a different
tensor index convention.

### 12. Could the normal `n` vanish under theta and break the last case?

No.  Once full transversality forces `n_s=n_t=0`, `n` is a nonzero multiple
of `e_u^*`.  The core square identity at `n` is a nonzero multiple of
`T_u`, so `q(n)` cannot vanish.  It is therefore a nonzero generator of
`ker L`.

### 13. Why does decomposability of the final `T_u` square force factor sharing?

At `q_u proportional (x,-y,0)`, the square is

```text
2 (x tensor d_Y-d_X tensor y) tensor d_Z.
```

If both pairs `(x,d_X)` and `(y,d_Y)` were independent, the displayed
two-by-two matrix would have rank two.  A nonzero decomposable output forces
one pair to be dependent.  It then shares `x` with the target on one tangent
ruling or `y` with the target on the other, contradicting full
transversality.

### 14. What exactly remains after the theorem?

Four ordinary coloops remain in the stated central chart, equivalently a
pure coordinate vector in the first or second root projection of `K`.
The repeated outer-factor lines, the outer coordinate-pair charts, all of
`(1,2,2)`, joint rank at most four, other physical and pole strata, and
higher orders remain open.  The theorem does not trigger a resolution audit
or a global-status change.

## Review conclusion

The nine-hyperplane cover, five equal-plane reductions, and complete
source-support obstruction survive the checks above.  The claim is
appropriately scoped as a verified localization of one exact `(1,1,2)`
branch.  Global Krenn--Gu remains **UNRESOLVED**.
