# Self-review: joint-rank-three transverse two-root q=2 exceptional normal form and pole controls

Date: 2026-08-13

## Claim boundary

The theorem localizes only normalized, target-consistent physical `m=3`
common-three-space full-sensor points with exactly two transverse root
blocks, total singleton span dimension three, joint rank three, and
uninvolved-row rank two.  It gives exact physical singleton/empty controls,
then uses the exact pair-pole gate to exclude regular graph extensions of
that complete cell.  It does not exclude the rank-one-row cells, another
component, a higher order, or the global conjecture.

## Adversarial checks

1. The starting incidence `Q subset V` is the exact rank-three `q=2` cell
   proved in S2BM.  It is not inferred from the sharp fixture.
2. The higher-row exclusions are transferred only where their proofs are
   incidence-free.  The support-two `(3,3)` profile is not silently dropped:
   after the common-zero atlas puts all rows in the square target's
   three-source coordinate space, the other two target diagonals lie in
   `U`; S2BM's two-diagonal forcing makes both root blocks monomial and both
   involved projections at most two-dimensional.
3. The nonvanishing common-zero classification uses every chart of the
   exact S2AI atlas.  Nonconjugate, fully conjugate, and all three-source
   charts have zero alternating tensor.  Only the conjugate chart with a
   nonzero tangent term survives containment.
4. In that chart the tangent parameters `lambda,mu` are not assumed equal.
   S2BN's mixed identity first forces their tangent directions onto `x,y`;
   changing the second `Q` basis vector by the square-kernel vector then
   equalizes them.  Their nonzero sum is load-bearing.
5. The basis coefficients `A,B,C,D` are arbitrary with `AD-BC!=0`.
   Simultaneous vanishing of both mixed values forces all four nonzero and
   `(A/B)^2=1`, giving the unordered basis `{w+u,w-u}` without a numerical
   sample or an algebraic-closure assumption beyond characteristic zero.
6. The support-one and support-two controls differ only in the third-root
   row relation.  Both have third-row rank two and joint row rank three;
   the primary and independent audits check all 27 empty root cells for
   each control separately.
7. The root blocks and relation plane are reconstructed explicitly.  Their
   derivative has rank six, its restriction to the displayed relation
   plane has rank three, and its image is the claimed singleton plane.
8. The full sensor claim uses both facts: the three singleton columns have
   determinant `4 x y t`, and the empty root tensor `d_j` is outside their
   singleton span.  A nonzero singleton determinant alone is not called a
   full four-column certificate.
9. The pair coefficients solve the unique Cramer system exactly and expose
   the divisors `x=0`, `y=0`, `t=0`.  Their numerators are independent of
   the corresponding denominator coordinates, so each valuation is exactly
   `-1`; there is no hidden cancellation.
10. The primary verifier uses SymPy matrices and dense tensors.  The
    independent no-import audit uses sparse tensor dictionaries, a separate
    row reduction, Laurent exponent dictionaries, and `Fraction`
    arithmetic.  Neither finite replay substitutes for the arbitrary-vector
    atlas proof.
11. The graph-extension exclusion invokes the existing Cramer--Euler gate
    only after the source atlas is proved exhaustive.  The local controls
    remain valid sharpness examples for singleton/empty equations, but the
    iff pair-regularity condition prevents them and every gauge-equivalent
    survivor from being physical graphs.

## Remaining obligations

- couple the rank-three and rank-four `q=1` controls to exact pole residues
  or a retained pair/deck recurrence;
- classify lower-rank three-root derivatives;
- return to other S2T component types, S2Q pole strata, higher orders, and
  the all-rank-drop branch.

Global Krenn--Gu remains **UNRESOLVED**.
