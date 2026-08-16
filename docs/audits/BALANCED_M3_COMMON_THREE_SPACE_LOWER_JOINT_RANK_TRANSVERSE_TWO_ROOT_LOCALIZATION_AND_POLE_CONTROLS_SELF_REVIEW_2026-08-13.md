# Self-review: lower-joint-rank transverse two-root localization and pole controls

Date: 2026-08-13

## Claim boundary

The theorem localizes only the normalized, target-consistent physical `m=3`
common-three-space full-sensor stratum with exactly two transverse root
blocks and joint cross rank three or four.  It proves an exact row/block
normal form when the uninvolved row has rank one and gives physical local
incidence controls.  It does not assert that the controls have global pair
blocks, satisfy a higher-order deck recurrence, form graphs, or resolve any
other component.

## Adversarial checks

1. The argument never infers `q>=1` from row rank alone.  It uses the physical
   full-sensor condition: `q=0` makes the empty companion zero, target
   consistency puts `J` in `U`, and all four columns then lie in a
   three-space.
2. The exclusion of `q=3` is inherited only at the scope explicitly recorded
   in S2AG: S2AD gives the exhaustive relation-plane alternatives from
   `dim P=dim V=3`, and the S2AE/S2AF contradictions use only that `Q` is a
   three-plane, not a direct-sum hypothesis.
3. The support claim is made for every vector of `ker theta`, not only a
   generic vector.  The rank-one case uses irreducibility only after the
   pointwise support-at-most-two statement is established.
4. Lemma 1 uses the exact S2AD beta-zero atlas.  In its tangent case, `z` is
   noncoordinate because `ker z` meets the target torus; quotienting by
   `span(z)` therefore applies to both distinct target coordinates.
5. The two controls were reconstructed from the physical singleton and empty
   matching formulas rather than merely from displayed row identities.  The
   full sensor determinant is the nonzero polynomial `-2 x_s y_s z_s`.
6. The rational pair coefficients have the correct multidegrees but exposed
   coordinate poles.  They are deliberately not promoted to physical edge
   blocks or a six-vertex counterexample.
7. The primary verifier and no-import audit use different tensor and exact
   arithmetic implementations.  Neither finite replay substitutes for the
   arbitrary-vector support and quotient proofs in the theorem document.

## Remaining obligations

- exclude or further localize the `q=2` lower-rank cells;
- use residue or higher-deck equations to rule out the populated `q=1` pole
  controls, if such an implication is valid;
- classify the three-root lower-rank derivative cells;
- return to the other S2T component types, the other S2Q pole strata, higher
  orders, and the all-rank-drop branch.

Global Krenn--Gu remains **UNRESOLVED**.
