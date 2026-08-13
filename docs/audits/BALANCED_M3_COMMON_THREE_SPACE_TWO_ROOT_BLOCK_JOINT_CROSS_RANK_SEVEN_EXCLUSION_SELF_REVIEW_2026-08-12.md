# Self-review: balanced `m=3` two-root-block joint-rank-seven exclusion

Date: 2026-08-12

## Claimed advance

The theorem excludes `rank H=7` on the part of the common-three-space
stratum with at least two nonzero root--root blocks.  S2Z separately excludes
the one-root-block case, and zero root blocks give zero singleton span.
Consequently this chain now proves `rank H<=6` on the common-three-space
stratum.  It does not exclude rank at most six or any other S2Q/S2T branch.
Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing checks

1. Restriction to a codimension-two space loses at most two derivative-rank
   directions.  Rank seven and singleton dimension three therefore bound the
   full shared derivative by five.
2. Rank five is not assumed to mean two monomial blocks.  The arbitrary
   rank-one flattening argument from S2U makes two nonzero blocks share one
   endpoint factor.  A third block would introduce a tensor with an
   independent endpoint direction and raise the rank above five.
3. Rank--nullity is used at equality: the four-dimensional derivative kernel
   lies inside the seven-dimensional column image of `H`, and the latter is
   exactly the preimage of the three-dimensional singleton span.
4. The common shared factor is made a target coordinate only by the S2R
   no-torus-annihilator theorem.  No arbitrary target basis change is used;
   such a change would not preserve the fixed GHZ coordinates.
5. The two unaffected root-3 colours give exact polynomial identities, not
   numerical or quotient identities.  They are the only target slices used
   in the final pointwise contradiction.
6. A rank-two root-1 block row has kernel exactly the missing coordinate
   covector.  This both makes the corresponding row of `H` zero and forces
   the tangent singleton image to have no matching first-factor coordinate,
   so the exceptional pure target term cannot be absorbed by `U`.  The
   root-2 argument is symmetric.
7. Global linear independence of the three root-row vectors does not by
   itself make the evaluated `3 x 3` matrix generically invertible: a
   singular matrix space could intervene.  The proof instead uses both
   nonexceptional target slices.  If generic evaluated rank were two, their
   two fixed column lines would make the missing physical row vanish
   identically, contradicting the already-proved global row rank three.
8. At a point where both evaluated block rows are invertible, the permanent
   slice is an invertible left/right transform of the zero-diagonal matrix
   `M(q)`.  A nonzero such matrix has a nonzero principal `2 x 2` minor and
   rank at least two, contradicting the required rank-one target slice.
9. The dense-open choice is legitimate over characteristic zero: the product
   of the two target monomials and the two nonzero determinant polynomials is
   nonzero in an integral polynomial ring.
10. The proof does not use a finite-field lift, numerical optimizer, or an
    assumed normal form for the seven active output rows.

## Mistakes and discarded routes

An early diagnostic set two physical output rows to zero.  That is only a
coordinate tangent subcase; arbitrary root-row `GL` is not a symmetry of the
fixed GHZ target.  The final theorem uses the invariant column image and its
annihilator instead.

A monomial support census also failed as a proof route.  Some partial
permutation supports realize both nonexceptional pure GHZ slices plus one
allowed exceptional row, although they miss the third pure target
coefficient.  Thus support counting alone does not establish the theorem.

Real least-squares experiments stalled at the missing pure coefficient, and
a characteristic-two SAT encoding of the row-deletion subcase was
unsatisfiable.  Neither result is used: the former is numerical and may see
only a boundary, while characteristic two collapses signs and cannot be
promoted across fields.

## Computational evidence boundary

The primary replay checks canonical exact representatives of the sharp
derivative and pointwise matrix calculations with SymPy.  The independent
audit constructs the derivative, six-term permanent, matrix product, and
rank floors separately with standard-library `Fraction` arithmetic.  These
scripts replay displayed identities; the arbitrary-tensor and dense-open
arguments in the theorem are the proof.

## Remaining boundary

The result changes the common-three-space joint-rank frontier from at most
seven to at most six.  Nothing here excludes rank six: a codimension-three
column image can hide more derivative directions, and the two unaffected
target slices need not force both involved block rows to have the same rank
profile used above.  The other multi-boundary, `beta=0`, and collapsed
cross-column components, the rank-one/pair-plane pole strata, higher orders,
and the all-balanced rank-drop branch remain separate open obligations.
