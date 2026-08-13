# Self-review: balanced `m=3` joint-rank-six shared-factor exclusion

Date: 2026-08-12

## Claimed advance

The theorem excludes exactly the `rank H=6`, `rank D_B=5` part of the
common-three-space stratum with at least two nonzero root--root blocks.  With
the complete single-root theorem and the three-nonzero derivative-rank floor,
the sole surviving rank-six mechanism has exactly two root blocks whose
three-dimensional derivative summands are disjoint, so `rank D_B=6`.
Joint rank at most five, that transverse rank-six mechanism, and every other
physical branch remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing checks

1. Codimension three gives only `rank D_B<=6`; it does not itself force the
   derivative rank to be five.  The theorem assumes the rank-five branch and
   separately records rank six as open.
2. Equality in the S2U pairwise-intersection bound makes exactly two nonzero
   blocks rank one with a shared endpoint factor.  Three nonzero derivative
   summands have rank at least seven by the S2X two-syzygy argument and are
   therefore incompatible with codimension three.
3. Rank--nullity gives `dim(K intersect ker D_B)=3`, not containment of the
   full four-dimensional derivative kernel.  No rank-seven kernel-containment
   claim is imported.
4. The S2R torus obstruction, rather than an arbitrary change of target
   basis, makes the shared endpoint factor one GHZ coordinate.  This leaves
   two exact unaffected target slices.
5. Those slices force both involved root-row maps to have rank at least two.
   In profile `(2,2)`, both missing rows vanish, so the singleton image has no
   `(s,s)` coefficient while the missing root coefficient forces precisely
   that pure tensor.  This argument does not require the derivative kernel to
   lie in `K`.
6. In profile `(3,3)`, global row independence alone is not used to infer
   pointwise invertibility.  The two fixed target row and column lines force a
   generically singular evaluation to have the fixed plane
   `span(e_t,e_u)`, which would make its colour-`s` row vanish identically.
7. In the mixed profile `(2,3)`, the full-rank side is generically invertible
   by the same fixed-plane argument.  Multiplication by its inverse promotes
   each zero slice to a polynomial row equation `r M(q)=0`; coefficientwise,
   this is exactly the quadratic zero-product equation.
8. The two surviving diagonal slice maps restrict to rank-one maps on the
   same three-plane with independent coordinate covectors.  The complete
   single-root pure/mixed classification applies to any three-plane and does
   not use a complementarity or joint-rank hypothesis.
9. The six crossed-pair cases retain their lower-dimensional boundaries:
   pure/pure and shared pure/mixed force one coefficient covector; disjoint
   pure/mixed forces shared target factors; same-pair mixed/mixed gives
   proportional products; different-pair mixed/mixed is injective or lies in
   one Segre tangent.
10. Characteristic zero is load-bearing for dense-open polynomial promotion,
    conjugate mixed pairs, and sum/difference separation.

## Mistakes and discarded routes

The first verifier draft used an invalid pure/mixed-shared control: one of its
claimed crossed products was nonzero.  The replay failed immediately.  The
control was replaced by a genuine pure `X` pair crossed with a conjugate
`X+Y` pair, and both implementations now check all four required zero/nonzero
relations.  The written arbitrary-vector case is independent of that sample.

Earlier rank-six experiments that fixed output rows by a root-side `GL`, used
monomial support counts, characteristic-two SAT, or real least squares are not
used.  Those operations either fail to preserve the fixed GHZ target or supply
only bounded/numerical evidence.

## Computational evidence boundary

The primary verifier checks the rank-five derivative, its nullity, the four
row-rank profiles, the pointwise permanent factorization, the nonzero
zero-diagonal rank floor, slice-zero promotion, and six crossed-pair controls.
The no-import audit independently reconstructs the derivative, permanent,
matrix product, and crossed derivatives with `Fraction` elimination.  These
scripts replay identities; the arbitrary-tensor intersection, density, and
six-case arguments in the theorem are the proof.

## Remaining boundary

At joint rank six the only surviving common-three-space mechanism has exactly
two nonzero root blocks and two disjoint three-dimensional derivative
summands.  Its derivative has rank six, its three-dimensional kernel is
contained in `image H`, and the singleton three-plane is the image of a
three-plane complementary to that kernel.  This transverse case is the next
local obligation.  Joint rank at most five and the other S2T/S2Q branches
remain separate.
