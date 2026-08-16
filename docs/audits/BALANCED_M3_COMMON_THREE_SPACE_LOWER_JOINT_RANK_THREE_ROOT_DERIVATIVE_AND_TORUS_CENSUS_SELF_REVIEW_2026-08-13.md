# Self-review: lower-joint-rank three-root derivative and torus census

Date: 2026-08-13

## Claim boundary

The theorem classifies the shared derivative and root-torus boundary only for
normalized, target-consistent physical `m=3` common-three-space full-sensor
points with all three root blocks nonzero, singleton span dimension three,
and joint rank three or four.  It excludes derivative rank nine at joint rank
four and the Hilbert--Burch `(2,2,2)` profile at both ranks.  It localizes,
but does not exclude, the remaining rank-nine, rank-eight, and rank-seven
cells.  It does not claim that its algebraic sharpness fixtures are physical
incidences or graphs.

## Adversarial checks

1. The shared derivative formula and `D(K)=U` are the exact physical
   singleton interface.  The incidence arithmetic uses only rank--nullity:
   `dim(K intersect ker D)=r-3` and
   `dim D^(-1)(U)=dim ker D+3`.
2. The S2X bound `dim ker D<=2` is used only when all three blocks are
   nonzero.  A one-dimensional kernel cannot have a one-supported syzygy.
   An all-supported syzygy would generate the second Hilbert--Burch row, so
   the unique syzygy has exactly two nonzero components.
3. In the rank-eight normal form, the first two derivative images span
   `(A_1 tensor y+x tensor A_2) tensor w`, of dimension five.  Its
   intersection with `C tensor A_3` is nonzero exactly when `C` lies in that
   tangent plane.  The strict noncontainment is therefore equivalent to rank
   eight, not merely sufficient.
4. For a two-dimensional kernel, the proof does not assume an all-supported
   vector.  It first rules out containment in a component-zero hyperplane by
   the pairwise shared-factor intersection bound, then uses the infinite-field
   finite-union argument.  Only then is the Hilbert--Burch formula invoked.
5. The rank-four rank-nine cell is excluded by the exact intersection count:
   a four-plane `K` mapping to three-dimensional `U` needs a one-dimensional
   derivative kernel intersection, impossible for an injective derivative.
6. Rank-four rank eight has `K=D^(-1)(U)` and contains the unique syzygy.
   Rank-four rank seven contains only one selected line of the kernel plane;
   rank-three cells are transverse to the entire kernel.  The review does not
   import any rank-five result that used full kernel containment.
7. In the rank-eight torus gate, the branch `gamma(w)=0` separates completely:
   a fully supported gamma exists exactly when `w` is noncoordinate, and a
   nonzero bilinear Laurent polynomial has no product-torus zero exactly when
   it is one coordinate monomial.
8. On `gamma(w)!=0`, the residual block is restricted to
   `P(x^perp) x P(y^perp)`.  When `x,y` are noncoordinate these are projective
   lines with only finitely many boundary points removed.  A rank-two
   bilinear restriction has a genuine `(1,1)` curve meeting the torus.  A
   rank-one restriction avoids it only when both factor zeros are coordinate
   boundary points.
9. Equality of restricted bilinear forms is lifted correctly: the kernel of
   restriction to `x^perp tensor y^perp` is
   `A_1 tensor y+x tensor A_2`.  The rank-eight noncontainment makes the
   coordinate-monomial quotient class nonzero.
10. Sufficiency of the two torus conditions is checked branch by branch; the
    result is an iff classification for product annihilators of the full
    derivative image.  It does not assert target consistency from those
    conditions.
11. The Hilbert--Burch `(2,2,2)` exclusion and coordinate atlases are
    rank-independent because their forbidden product functionals annihilate
    `image D`, hence `U`, before `K` is used.  Later rank-five profile
    exclusions are explicitly not transferred.
12. The rank-nine, rank-eight, and rank-seven fixtures certify only derivative
    rank and root-torus blocking.  No `K`, empty permanent, fourth sensor
    column, global pair layer, or graph is inferred from them.
13. The primary verifier uses dense SymPy derivative matrices, independent
    kernel representatives, and symbolic contraction gates.  The no-import
    audit rebuilds the matrices in a row-oriented `Fraction` implementation.
    Neither finite replay substitutes for the Laurent-unit or projective-line
    proof.

## Remaining obligations

- couple the rank-four shared-factor and selected Hilbert--Burch-line cells
  to the full empty-permanent target;
- couple the rank-three injective/shared-factor/transverse-kernel cells to
  that target and pair regularity;
- resolve other S2T components and S2Q pole strata;
- resolve higher orders and the all-balanced rank-drop branch;
- keep the global status `UNRESOLVED` until the dedicated resolution gate
  validates a complete proof or exact counterexample.

Global Krenn--Gu remains **UNRESOLVED**.
