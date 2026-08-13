# Self-review: transverse-rank-six beta-zero localization

Date: 2026-08-13

## Claimed advance

The theorem does not exclude joint rank six.  It identifies the exact linear
normal form of its sole transverse two-root mechanism, classifies the two
root-block geometries that can keep the automatic beta-zero locus off the
root torus, and reduces a non-coordinate relation plane to an aligned
rank-two root-row boundary.  Coordinate relation planes and the aligned
rank-two cases remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing checks

1. Rank six, not merely disjoint notation, makes the derivative kernel
   exactly the third root space.  Rank--nullity then puts that full kernel in
   `image H` and splits off a three-plane `K_12`.
2. The beta-zero locus is automatic because the third root block vanishes.
   It is not automatically a torus locus: coordinate monomials and the
   boundary-pencil tangent family are genuine sharp obstructions.
3. The root-block atlas uses two irreducibility steps.  First one block has a
   fixed coordinate image on the third-root torus.  On its zero hyperplane,
   the other block has a fixed coordinate image.  The common kernel of the
   two remaining forms must then be a coordinate line.
4. `L=K_12^perp` is mathematical relation data, not a row-space gauge.  No
   root-side `GL` is applied to the fixed GHZ target.
5. For a full-support relation `(u,v)`, the form
   `B^T v-C^T u` exactly measures equality of the two root-block
   contractions.  Its kernel therefore supplies genuine product
   annihilators of `U`.
6. S2R makes that form coordinate.  S2S is then used only when its boundary
   point has exactly one zero coordinate and the common contraction is
   nonzero: target support is two but `beta_root=(lambda,lambda,0)` has
   support two, contradicting the proved full-support requirement.
7. The fixed-coordinate conclusion follows from density and a finite union;
   it is not inferred from finitely many samples.
8. Projection dimensions of `L` equal the two involved row ranks.  If both
   were three, both internal blocks would share one third-root factor and the
   derivative rank would be five.
9. A row-kernel covector kills the corresponding permanent row.  Target
   consistency then forces all of its nonzero target coordinates into one
   fixed third-root line.  Hence the kernel is one coordinate line and the
   row rank is exactly two.
10. All arguments are over an algebraically closed characteristic-zero field;
    descent to the complex prize field is the same finite-coefficient descent
    used by S2R and S2AC.

## Mistake retained

The first proposed shortcut claimed that two transverse root blocks always
have a fully supported simultaneous contraction zero.  This is false even
for `B=e_i tensor e_s`: its contraction is nonzero everywhere on the torus.
The exact failure classification also uncovered the less obvious
boundary-pencil tangent family (16)--(17).  An initial draft overstated this
as a two-coordinate plane.  Hostile review found the wider case where the
common kernel has one zero and two nonzero coordinates; a dedicated exact
control now prevents that narrower claim from returning.  The theorem records
the full sharp exception instead of hiding either failed route.

## Computational evidence boundary

The SymPy replay and independent `Fraction` audit check canonical
representatives, ranks, tensor indexing, the relation-annihilator identity,
support counts, and the shared-factor rank-five boundary.  They do not prove
the irreducibility or arbitrary-vector classification; those are the written
proof.  No finite-field, numerical, or sampled calculation is used as a
global claim.

## Remaining boundary

The full uncontracted permanent equations must now be imposed on two exact
types: a coordinate relation plane (equivalently, a coloop among the six
involved root rows), or an aligned rank-two row with coordinate kernel and
diagonal internal-block contraction.  Joint rank at most five and the other
S2T/S2Q components remain separate obligations.
