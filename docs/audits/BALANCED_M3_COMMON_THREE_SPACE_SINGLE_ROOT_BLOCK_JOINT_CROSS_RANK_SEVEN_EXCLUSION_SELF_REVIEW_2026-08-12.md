# Self-review: balanced `m=3` single-root-block joint-rank-seven exclusion

Date: 2026-08-12

## Claimed advance

The new theorem excludes `rank H=7` only on the common-three-space branch
where exactly one **root--root edge block** is nonzero.  S2X and S2Y already
exclude ranks nine and eight without this extra hypothesis.  The surviving
rank-seven case with at least two nonzero root--root blocks and every rank at
most six remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing checks

1. The single-root-block hypothesis is not inferred from rank seven.  A
   codimension-two image can hide two root-block derivative directions, so
   that is explicitly left as the next case.
2. Physical full-sensor rank is used twice.  It makes the exceptional root
   block row a three-plane, and it makes all three source projections of that
   row nonzero.  Without those facts the marked root rows need not be a basis
   and the full-support derivative dichotomy would not apply.
3. The torus argument is applied only after the singleton image is proved to
   be the whole space `A_1 tensor B_23`.  The argument would be invalid for a
   proper three-dimensional image inside a larger shared-factor sum.
4. S2U's off-diagonal-root-edge globalization was reread: its explicit
   `2 x 2` permanent pair blocks do not require invertibility of the joint
   cross map.  It is therefore valid at rank seven.
5. The regular derivative chart and exceptional derivative chart are kept
   separate.  The off-diagonal products vanish as quadratic triples only in
   the regular chart.  The exceptional chart is instead excluded by the
   one-covector-versus-two-covectors argument from S2Y.
6. Equality `rank H=7` forces both `dim span(P,Q)=4` and
   `R intersect span(P,Q)=0`; only the first is needed in the marked-grid
   classification.  No stronger complementarity is silently assumed.
7. The proof that the third marked rows vanish uses the complete
   pure/mixed/full zero-divisor classification.  A common nonzero zero
   divisor for two mixed rows forces those rows to be proportional; a common
   zero divisor for two pure rows forces the same source.  Either alternative
   kills one required diagonal product.
8. The `P/M` all-three-source argument uses injectivity of the pair
   `(L_+,L_-)`, not injectivity of either map separately.  Rank one for both
   restrictions forces the projected two-plane to contain both distinct
   kernel lines and hence forces a shared pair of target factor lines.
9. In the different-edge `M/M` case, complementarity of the marked planes is
   exactly what makes the two shared-source component lines independent.
   Their derivative pair then has zero common kernel.  Without that
   independence the claimed injectivity would fail.
10. Every sign separation uses characteristic different from two.  The
    theorem is stated only in characteristic zero and makes no modular-lift
    claim.

## Computational evidence boundary

The primary replay realizes the five normal-form families over `Q`, checks
the sharp four-dimensional zero grid, and verifies the exact ranks and
kernels used in the case analysis.  The independent audit constructs the
three-source permanent maps directly with standard-library `Fraction`
arithmetic and separate elimination.  These scripts replay the displayed
identities; the arbitrary-vector classification and tensor arguments in the
theorem are the proof.

The four-dimensional off-diagonal grid itself is attainable.  The theorem
excludes it only after imposing both surviving GHZ diagonal rows, so it does
not overstate the sharp S2Y rank bound.

## Known boundary

With two root--root blocks, the shared derivative has rank at least five.
At joint rank seven its codimension-two input image can in principle reduce
that to the observed three-dimensional singleton span.  Neither the sparse
one-root equation nor the marked-grid equality classification follows in
that branch.  Treating it requires a new codimension-two incidence argument,
not a relabeling of this proof.
