# Hostile review: support-one higher-row-rank exclusion

## Claim under review

The proposed theorem excludes only the transverse two-root, joint-rank-five
support-one profiles whose involved row ranks are `(3,3)`, `(3,2)`, or
`(2,3)`.  It does not exclude support-one `(2,2)`, any three-root
Hilbert--Burch coordinate atlas, joint rank at most four, another physical
component, another pole stratum, a higher order, or the global conjecture.

Global status remains **UNRESOLVED**.

## Adversarial questions

### 1. Is support one being confused with a zero third row?

No.  The kernel generator of the rank-two map `theta` is a coordinate
covector.  After relabelling it is `e_2^*`, so the exact row relation is
`q_2=0`; the other two rows span `image theta`.  This does not say that the
root--root contractions `b,c` vanish.

### 2. Does the `(3,3)` proof silently assume both contractions are nonzero?

No.  The diagonal-cover lemma says at least one of `b,c` is the nonzero
coordinate line `e_2`.  Root exchange puts that line on `b`.  If `c=0`, the
contracted graph map is visibly injective.  If `c!=0`, its only possible
kernel vector would satisfy `Lc=-beta e_2`; applying `L` to an actual
`E_22` preimage contradicts that identity.  Both cases are written.

### 3. Why does injectivity of the contracted graph control every correction?

The full derivative is injective on `P`, so each nonroot monomial has a
unique correction vector in `P`.  Contracting by `e_2^*` kills the physical
all-cross tensor.  Every monomial other than `T_2` therefore maps to zero
under `Phi|P`, and injectivity makes its correction vector zero.  This is a
coefficientwise use of all 27 root rows, not a selected quotient slice.

### 4. Is the mixed-profile zero-row equation missing the `C` block?

No.  If `p_d=0`, every graph vector has second component in `e_d^perp`.
On the root row with second coordinate `d`, the `C tensor L e_i` term is
therefore zero.  The target-kernel theorem gives the exact remaining block
row `B_(d,-)=kappa e_d`.  The complete row forces
`S_a=0` for `a!=d` and `S_d=-T_d/kappa`.

### 5. Why must the missing involved-row colour equal the support-one colour?

At third-root row two, `q_2=0`, so the all-cross permanent cannot supply
`T_2 E_222`.  The zero-row calculation says the only available correction
line is `T_d`.  Distinct diagonal target tensors are linearly independent;
therefore `d=2`.  This conclusion is not inferred merely from the contracted
root blocks.

### 6. Is permanent symmetry used with the correct matrix orientation?

Yes.  With `p_b=sum_i L_(b,i)r_i`, the physical matrix is `F=S L^T`, where
`S` is symmetric.  Hence `L F=L S L^T` is symmetric.  For the unaffected
`T_i` coefficient, `F=E_ii`, so `L E_ii` symmetric means the **column**
`L e_i` lies on `e_i`.  The verifier checks this orientation separately.

### 7. Are the repeated-row contractions legitimate target contractions?

Yes.  In the invertible graph take `beta_i=lambda_i^(-1)e_i^*` and
`alpha_i=L^T beta_i`.  Then `p_(beta_i)=r_(alpha_i)`.  Because `beta_i` has
only coordinate `i` and `alpha_i(e_i)=1`, their target contraction retains
exactly `T_i`.  The cross contraction retains no target because the two
fixed graph columns are coordinate-aligned.  In the equal-kernel mixed
chart this reduces to `p_i=lambda_i r_i`.

### 8. Does tangent-line separation assume every tangent tensor is pure?

No.  It uses only the classification of **decomposable points** in a Segre
tangent space.  A two-source square image fixes two factor lines.  A
three-source square image is a Segre tangent space, and each decomposable
point shares at least two base factor lines.  Thus two fully transverse
decomposable lines cannot both lie in one square image.  Arbitrary
nondecomposable tangent values are not discarded.

### 9. Is mixed factor sharing being transferred from a three-plane to a
two-plane without proof?

No.  The theorem proves a pointwise factor-sharing statement first.  A
common point where the square and mixed rank-one maps are both nonzero is
obtained by avoiding finitely many scalars.  The two-source case follows
after quotienting by the active third factor.  In the three-source case a
decomposable square value `xi tensor y tensor z` forces the square
preimage's `Y,Z` components onto `y,z`; every mixed value lies in
`X tensor y tensor Z+X tensor Y tensor z`, so a decomposable one shares
`y` or `z`.  This argument works for an arbitrary subspace `Q`.

### 10. Is the two-plane square-pencil atlas exhaustive?

Yes.  A nonzero square has a row with two or three source components.

- For two components, the square kernel line either gives a nonzero
  `x tensor b+a tensor y`, forcing the other row onto `x-y`, or is the
  conjugate line `x-y`.  The latter splits exactly according as the active
  third factors are independent or proportional; a common factor remains
  in both cases.
- For three components, the square kernel is the scaling plane.  A
  decomposable active value `xi tensor y tensor z` aligns the active
  preimage in `Y,Z`.  On the kernel line, equation (24) either aligns all
  three components of the other row with the base lines, or, when one
  scaling coefficient is zero, aligns the other two.  Its square therefore
  shares at least one factor with the active target in every case.

Characteristic zero in particular keeps the polarized square factors
nonzero.

### 11. Does the unequal-kernel mixed chart satisfy the older lemma's scope?

Yes.  The sole `T_2` correction is killed by projecting each nonroot source
onto the two other coordinate lines.  The projected binary target has
root-three flattening rank two, so the projected `Qbar` has dimension at
least two.  S2AF's binary five-product lemma assumes only that dimension
floor, not an injective three-dimensional third row.  Its five displayed
maps match the present root-pair table.

### 12. Why is `(2,2)` not included?

With both involved projections rank two, their two zero rows determine two
correction directions but leave a third relation-plane direction.  The
injectivity argument of `(3,3)` and the full zero-row pinning of `(3,2)` both
fail on that residual.  Treating it as zero would be an unjustified
strengthening, so the theorem records it as the next open transverse case.

### 13. What do the scripts prove and not prove?

The primary verifier replays the graph and zero-row matrices, row-profile
normal forms, tangent intersections, both source-support parts of the new
two-plane lemma, and the inherited binary boundary charts.  The independent
audit reconstructs sparse permanent tensors using only `Fraction` and a
different representation.  Neither script replaces the arbitrary-vector
arguments, the finite-scalar avoidance, or the proof that the displayed
case split is exhaustive; those are in the theorem.

## Verdict

The proof supports the exact characteristic-zero exclusion of support-one
profiles `(3,3)`, `(3,2)`, and `(2,3)`.  The support-one `(2,2)` residual,
the Hilbert--Burch coordinate atlases, lower joint ranks, other physical
branches, higher orders, and the global Krenn--Gu conjecture remain open.
