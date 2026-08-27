# Review: survivor existential principal-open first-response nonextension

Date: 2026-08-26

## Verdict

Accept `GLD80` as an **exact existential principal-open exclusion containing
the Gaussian survivor** on the scale-fixed local `GLD75` fixed-star
component.  It is a theorem about an actual finite-type survivor
neighborhood, not only a tangent or formal germ calculation.  It does not
compute the exceptional polynomial, cover another survivor component or
source presentation, or resolve Krenn--Gu.  The global conjecture remains
**UNRESOLVED**.

## Evidence and dependency replay

The portable verifier checks the three exact computational premises:

1. `GLD74`: the affine `35`-dimensional raw fibre over `F_0` has no necessary
   rank-one response point in its exhaustive three-chart cover;
2. `GLD78`: at all three sign-boundary points, the exact invariant augmented
   matrices have rank jump `8 -> 9`, with nonzero regular determinants;
3. `GLD79`: after exact transformed-coordinate nuisance, response, quotient,
   and `K_r` covariance checks, the complete geometric projective boundary
   fibre is exactly the three reduced sign points.

It also invokes the `GLD76` universal verifier, which checks at the Gaussian
specialization the exact tensor and raw intertwiners, all complete legal
response maps, and the demanded target response.  The moving transport and
matching-partition lemma are proved algebraically in the theorem rather than
reported as a four-parameter symbolic CAS expansion.

The existing standard-library no-import audit independently reconstructs the
first premise and the sign data in the second and third premises.  It does
not replay the new standard-block determinant cover in `GLD79`.  No separate
independent implementation of that cover or formalization of the algebraic-
geometry bridge exists; those evidence limits are explicit.

## Hostile audit of the geometric bridge

An early version retained affine slopes `(a,b)` while claiming the projection
was proper.  That was rejected: an affine slope can escape to infinity.  The
accepted theorem instead uses the intrinsic `2 x 2`-minor incidence in
`B x P^35`, with no slope variables.  Its strict finite-raw closure is the
`s`-saturation, and its projection is projective.

An early invocation of analytic “curve selection” was also rejected as too
informal.  The theorem now works over the algebraic closure and states the
finite-type algebraic trait lemma.  A closed point in the strict closure is
reached by the normalization DVR of an integral curve whose generic point is
affine.  This is precisely the one-parameter object to which the localized
`GLD78` determinant argument applies.

Two further hostile findings were load-bearing and are repaired.

First, in untransformed fixed-interface coordinates a moving demanded GHZ
response has mixed entries.  Therefore legal response does not directly imply
rank at most one for a fixed `65 x 3` quotient; `GLD76` explicitly keeps its
full `68 x 4` system.  `GLD80` now transports the complete nuisance and legal
response interface by `U_F` and `S_F`, constructs a regular moving kernel
frame and quotient in literal-Delta coordinates, and derives the signed
four-root relation by partitioning matchings according to the neighbor of
`q_0`.  Only in that transported presentation is the `GLD74` rank bound used.
The partition is the exact identity

```text
b_F beta-sum_r xi_r H'_(r,F)(beta)=C'_F(beta_Q,beta_(eta,u,c)),
```

valid for arbitrary transformed ports and raw `beta`, not a specialization
or sampled equality.

Second, the slopes on a specializing trait are the ratios of the full
homogenized columns

```text
a=(mathcal Z_1)_rho/(mathcal Z_0)_rho,
b=(mathcal Z_2)_rho/(mathcal Z_0)_rho,
```

not ratios of their boundary terms alone.  `GLD79` makes the closed
`K_(0,F_0)t` nonzero, so a suitable denominator has nonzero residue and is a
DVR unit.  The slopes specialize to the corresponding `GLD77` pair; the
repaired moving `GLD78` determinant therefore remains a unit and forces `s`
to vanish, contradicting an affine generic point.

## Proper-image conclusion audited

Let `C` be the reduced strict closure.  `GLD74`, `GLD79`, and the trait
argument imply that its geometric fibre over `F_0` is empty.  Because
`C->B` is proper, its image `E` is closed.  On the affine base `B=Spec A`, a
closed set missing the `K`-rational point `F_0` has an ideal element
`delta` with `delta(F_0)!=0`; `D(delta)` misses `E`.  The affine necessary
incidence is contained in `C`, so it is empty over this principal open.
The transported moving rank-one lemma then excludes the legal first response
for every raw preimage there.

This proves existence only.  Neither properness nor the Nullstellensatz
chooses a sparse or computationally useful `delta`.  The precise residual is
the base elimination of the saturated projective ideal, not an unnamed
“generic bad locus.”

## Load-bearing limits

1. `B` is a principal finite-type neighborhood inside the scale-fixed
   `GLD75` gauge where the full and equal-leaf survivor schemes agree.  Its
   complement and every other component remain open.
2. The first-response obstruction is the moving literal-Delta continuation
   of the necessary `GLD74` quotient at `q_0`.  Legal response implies this
   condition by exact complete-interface transport; no converse is asserted.
3. The theorem quantifies over every raw coefficient preimage represented by
   the regular rank-35 moving kernel bundle, including all response-rank drops.
4. `delta` exists in `A` but is not explicitly expanded.  The exceptional
   divisor is therefore geometrically named by the proper image, not
   computationally identified.
5. Frame nonuniqueness is controlled only in the certified local gauge; no
   global uniqueness or exhaustive survivor atlas is claimed.
6. Source integration, maximum-root/no-fifth-root certification, other
   contracted roots, non-star interfaces, and the global conjecture remain
   open.
7. The no-import audit does not independently replay the `GLD79` standard
   block, and no formalization of the proper-image bridge exists.

## Recommended successor

Compute the elimination ideal of the `s`-saturated intrinsic projective
incidence over the four survivor parameters.  A single explicit element
nonzero at `F_0`, or a finite exact base-divisor cover, would turn the
existential open into the explicit `delta(F)` certificate requested by the
parent program.  In parallel, the separate source/interface obligation must
show that relevant graph presentations actually pass through this fixed
effective interface before any global conclusion is possible.
