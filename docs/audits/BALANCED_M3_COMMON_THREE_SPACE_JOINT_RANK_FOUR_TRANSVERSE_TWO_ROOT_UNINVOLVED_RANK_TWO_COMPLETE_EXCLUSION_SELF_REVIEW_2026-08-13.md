# Self-review: joint-rank-four transverse two-root uninvolved-rank-two complete exclusion

Date: 2026-08-13

## Claim boundary

The theorem excludes only normalized, target-consistent physical `m=3`
common-three-space full-sensor points with exactly two transverse root
blocks, total singleton span dimension three, joint rank four, and
uninvolved-row rank two.  It does not exclude the populated rank-four
rank-one-row pole control, any joint-rank-three point, a three-root
derivative, another physical component, another pole stratum, or a higher
order.

## Adversarial checks

1. The joint-rank-four incidence is taken from S2BM rather than inferred
   from the rank-five splitting: `dim V=3`, `dim Q=2`, `V+Q=K^*`, and hence
   `dim(V intersect Q)=1`.  In particular `Q` is not contained in `V`.
2. The involved-row profile census includes no silent lower-rank case.  A
   contraction by a kernel vector shows that every involved-row kernel
   vector has support at most one if the row rank were at most one; a
   two-plane cannot lie in the union of the three coordinate lines.  Thus
   each involved rank is two or three.
3. The new lemma does not claim that all intersecting planes are excluded.
   It proves vanishing only for `Q not subset V` and supplies an exact
   `Q subset V` fixture with nonzero alternating singleton tensor.
4. The target subspace `D` is spanned only by target tensors fully
   transverse to the square target.  Its intersection with the mixed
   tangent space and, in the exceptional chart, with
   `X tensor Y tensor span(t)` is zero because the three target factor
   triples are independent in every source.
5. The only old common-zero chart where disjointness was used is the
   two-source conjugate chart with nonzero tangent term.  The proof retains
   arbitrary tangent components `d,e` and an arbitrary invertible basis
   matrix `[[A,B],[C,D]]`; it does not normalize them to a sampled value.
6. In that chart, vanishing of the `q_0` mixed value first forces `B D!=0`
   from the nonzero basis determinant, and then forces
   `d in span(x), e in span(y)` by two quotient projections.  This puts the
   second generator of `Q` in `V`, contradicting only `Q not subset V`.
7. The support-one S2AL and support-two S2AJ transfers use no `V,Q`
   incidence.  The `(2,2)` and support-two `(3,3)` transfers replace only
   the final disjoint-plane common-zero lemma; their relation-plane and
   complete-target-table reductions depend on `P`, `dim Q=2`, and the
   physical coefficient equation, all available at rank four.
8. The primary verifier checks the formal chart over symbolic coefficients.
   The independent no-import audit uses a separate sparse-polynomial
   representation, reversed tensor-key order, and `Fraction` arithmetic.
   Neither replay is used as a substitute for the quotient or exhaustion
   arguments in the theorem document.

## Remaining obligations

- classify or exclude the joint-rank-three `Q subset V`, `q=2` exceptional
  chart using the rest of the complete target equation;
- couple the exact rank-three and rank-four `q=1` controls to their pair-pole
  residues or to a higher-deck identity;
- classify lower-rank three-root derivatives;
- return to the other S2T component types, S2Q pole strata, higher orders,
  and the all-rank-drop branch.

Global Krenn--Gu remains **UNRESOLVED**.
