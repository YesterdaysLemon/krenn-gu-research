# Self-review: rank-four/rank-eight same-missing-colour coordinate split-lift exclusion

Date: 2026-08-13

## Claim reviewed

The claim excludes the exact coordinate split-lift four-space displayed in
the theorem on the joint-rank-four, derivative-rank-eight, all-three-root-
blocks-nonzero common-three-space cell.  It also proves a reusable
characteristic-zero eight-product obstruction for the polarized permanent.

The claim does not assert that every same-missing-colour point has the
displayed split-lift normal form.  That distinction is load-bearing.

## Load-bearing checks

- The shared derivative has rank eight and its kernel is exactly the first
  displayed basis vector of `K`.
- The other three derivative images are independent, so `D(K)=U` has the
  required dimension three.
- All three coordinate projections of `K` have dimension two and give the
  stated kernel colours `(d,d,s)`.
- The polarized root permanent has exactly eight nonzero unordered basis
  products.  They are a basis of one `2 x 2 x 2` root box.
- That root box meets `U` trivially.  Each of the three generators of `U`
  has a component outside the box that no other generator can cancel.
- Modulo `U`, the `d` target diagonal is the negative `ssd` box vector, the
  `s` target diagonal vanishes, and the `t` target diagonal is unchanged.
- Repeated-index factors of two agree on the root and source polarizations;
  the table does not lose a factorial.
- The resulting six zeros and two nonzero products match the eight-product
  lemma exactly, and the two surviving source tensors use distinct target
  colours, so they are fully transverse.

## Eight-product lemma audit

The proof splits by the number of source summands of the repeated vector
`v`; a pure `v` has zero square.

- With two source summands, `P(u,u,v)=0` puts `u` on one scaling-difference
  line plus its nonzero third component.  Both mixed zeros put `r,q` in the
  same family, `P(q,v,v)=0` removes the third component of `q`, and
  `P(u,u,r)=0` either makes the first target share all factors of the second
  or makes it zero.
- With three source summands, a decomposable tangent vector shares at least
  two base factors.  The second square-zero equation makes `u` either pure
  or a three-line scaling vector.  In the scaling case both mixed zeros put
  `r,q` on the same three factor lines.  In the pure case the remaining
  square and mixed zero force `q` onto a scaling difference and then force
  `r` into the same pure source as `u`, killing the first target.
- If one scaling coefficient or pairwise sum vanishes in the three-source
  relation, the relation collapses to the pure case; no boundary is omitted.

The case split is rank-free in the ambient source spaces and uses only
rank-one tensor equality, quotienting by factor lines, and characteristic
different from two.  The theorem states the narrower characteristic-zero
scope used by the repository.

## Falsification attempts

1. **Allow a pure repeated vector.**  Its square is zero, contradicting the
   nonzero second target.
2. **Take the two-source scaling coefficient to be zero.**  The first target
   then either vanishes or shares all three factor lines with the second.
3. **Let a three-source scaling pair sum vanish.**  The quadratic relation
   forces two coefficients to vanish, reducing to the separately checked
   pure case.
4. **Cancel an `U` component inside the eight-dimensional box.**  The unique
   outside coordinates of the three `U` generators force all three
   coefficients to vanish before any box cancellation is possible.
5. **Use a nonsurjective cross map.**  The physical hypothesis is joint rank
   four, so `H^*` is injective on `K^*`; weakening this would leave the
   claimed cell and is not silently allowed.
6. **Promote the split-lift exclusion to the full same-colour cell.**  The
   theorem, README, frontier, and ledger all keep nonsplit lifts open.

No falsification attempt invalidated the stated local conclusion.

## Computational evidence and independence

The primary SymPy replay constructs the dense derivative, the split-lift
four-space, all 20 unordered root-permanent products, the direct quotient,
and symbolic normal-form identities for the two-/three-source proof.

The independent audit imports no repository or third-party module.  It uses
`Fraction`, sparse dictionaries, reversed tensor flattening, its own row
reduction, all 64 ordered basis placements through the unordered census, and
separate exact rational fixtures for every support branch.  The scripts
replay the algebra; the arbitrary-vector case exhaustion in the theorem is
the proof.

## Status decision

The eight-product lemma and displayed split-lift exclusion are suitable for
`verified` status after focused and repository-wide validation pass.  Every
wider cell named above and global Krenn--Gu remain **UNRESOLVED**.
