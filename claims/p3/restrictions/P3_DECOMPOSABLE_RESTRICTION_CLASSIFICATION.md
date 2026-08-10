# Classification of decomposable rank-at-least-two restrictions of `P_3`

## Status

This is an exact tensor theorem over `C`.

Let

```text
L_r : C^3 -> W_r,   rank(L_r)>=2,   r=0,1,2.
```

If

```text
(L_0 tensor L_1 tensor L_2)P_3
```

is nonzero and decomposable, then all three maps have rank exactly two.
Dually write the two-dimensional row spaces as

```text
U_r=a_r^perp subset (C^3)^*.
```

After permuting the three modes and the three source coordinates, and
rescaling the three projective normals, there are parameters `A,B`, not
both zero, such that

```text
a_0=(1, A, B),
a_1=(1,-A,-B),
a_2=(1,-A, B).                                       (1)
```

Conversely every normal triple in (1) gives a nonzero decomposable
restriction.  Thus, on each source-coordinate chart, the locus consists
of six oriented-edge two-parameter sign charts, including their
one-parameter boundaries; source-coordinate permutations cover the full
rank-at-least-two locus.

Its four-plane corollary is a structural input in the exact exclusion of
normalized `q5_311`.  The classification does not itself exclude
`P_5 -> Delta_3` or the arbitrary-order Krenn--Gu prize conjecture.

## Rank-three maps are impossible

Use the pair map

```text
mu(v,w)=(
  v_1 w_2+v_2 w_1,
  v_0 w_2+v_2 w_0,
  v_0 w_1+v_1 w_0
)
```

from
[`P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md`](P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md).
If, say, `U_0=C^3`, the `0|12` flattening rank equals
`dim mu(U_1,U_2)`.  Decomposability would force this dimension to be
one.  The pair-image classification then gives

```text
U_1=U_2=e_s^perp
```

for one coordinate `s`.  But the remaining bilinear factor is the
order-two permanent

```text
v_p w_q+v_q w_p,
```

which has matrix rank two.  The full tensor is therefore not
decomposable.  By symmetry every `U_r` has dimension two.

## The common-coordinate chart

First suppose the three plane normals share a coordinate on which all
are nonzero.  Permute source coordinates and normalize that coordinate:

```text
a_0=(1,A,B),   a_1=(1,C,D),   a_2=(1,E,F).
```

Use plane bases

```text
(-A,1,0), (-B,0,1);
(-C,1,0), (-D,0,1);
(-E,1,0), (-F,0,1).
```

In the corresponding binary basis, the restricted `2 x 2 x 2` tensor
has zero antipodal corners and the six remaining coefficients

```text
T_001=-(A+C)        T_110=-(B+D)
T_010=-(A+E)        T_101=-(B+F)
T_100=-(C+E)        T_011=-(D+F).                    (2)
```

A nonzero decomposable binary tensor whose `000` and `111`
coefficients vanish must be supported on one of the six edges joining a
weight-one cube vertex to a weight-two cube vertex.  Indeed, one
lower coordinate of one factor and one upper coordinate of a different
factor must vanish.

For the representative edge `{100,101}`, the four off-edge equations in
(2) give

```text
C=E=-A,   D=-B,   F=B.                               (3)
```

The two edge coefficients are `2A` and `-2B`, so the tensor is nonzero
exactly when `(A,B)!=(0,0)`.  Equations (3) are precisely (1).  The
other five edges are obtained by permuting the tensor modes.

## Zero-coordinate boundary

It remains to justify that every nonzero decomposable restriction enters
the chart above.

First, no plane normal can have coordinate support one.  Suppose
`a_0=e_0`, so `U_0=span(e_1,e_2)`.  If the other two normals are both
nonzero in coordinate zero, the common-coordinate calculation applies
with `A=B=0` and makes the alleged tensor zero.  Otherwise suppose the
normal of `U_1` vanishes in coordinate zero.  The subtensor obtained
from the source vector `e_0 in U_1` is the nondegenerate order-two
permanent between `U_0` and the projection of `U_2` to
`span(e_1,e_2)`.  Rank one forces that projection to be one-dimensional,
so `e_0 in U_2` as well.

Write

```text
U_1=span(e_0,(0,C,-B)),
U_2=span(e_0,(0,F,-E)).
```

Both displayed second vectors are nonzero.  In these bases the two
nonzero `U_1` flattening rows occupy disjoint `U_2` coordinates:

```text
(-E,F) on the e_0 tensor (second U_2 vector) slice,
(-B,C) on the (second U_1 vector) tensor e_0 slice.
```

They are linearly independent, so the flattening rank is two, a
contradiction.

Now assume all three normals have support at least two.  If they had no
common nonzero coordinate, each would have support exactly two and the
three missing coordinates would be distinct.  After rescaling, write

```text
a_0=(a,b,0),   a_1=(0,c,d),   a_2=(e,0,f),
```

with all six entries nonzero.  Use the plane bases

```text
e_2,(b,-a,0);
e_0,(0,d,-c);
e_1,(f,0,-e).
```

The `000` coefficient is one and its three adjacent coefficients are
zero.  Rank one would force every other coefficient to vanish, but the
`110` coefficient is `-bc`, which is nonzero.  This final contradiction
shows that a common nonzero normal coordinate always exists and
completes the classification.

## Geometry of the normal forms

If `A` and `B` are both nonzero, the normals in (1) are three distinct
projective sign variants of one fully supported vector.  They are three
vertices of a four-point sign rectangle in `P^2`.

If exactly one of `A,B` is zero, all normals have the same
two-coordinate support and exactly two projective sign variants occur,
one of them twice.  The excluded point `A=B=0` is the common coordinate
plane and gives the zero restriction classified separately in
`P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md`.

## Four-plane corollary

Let `U_0,U_1,U_2,U_3` be planes in `C^3`.  Suppose every one of the four
triple restrictions of `P_3` is either zero or nonzero decomposable.
Then exactly one of the following holds:

1. all four planes are the same coordinate plane, and all four triple
   restrictions are zero;
2. all four triple restrictions are nonzero decomposable, and the four
   projective normals form a complete sign rectangle.

For common normal support two, the rectangle consists of two copies of
each of the two sign variants.  For support three, it consists of all
four distinct sign variants.

To prove the corollary, if one triple is zero, the zero theorem makes its
three planes one common coordinate plane.  Any triple containing two of
them and the fourth plane cannot belong to the nonzero normal form,
whose normals all have common support at least two.  It is therefore
zero as well, forcing the fourth plane to be the same coordinate plane.

Otherwise every triple belongs to (1).  Start with any three normals.
Every overlapping valid triple containing two of these normals must have
the same common coordinate support and coordinatewise absolute ratios:
the two fixed projective normals determine those data, while the third
normal may only change the permitted signs.  In support two the first
three use both sign variants with multiplicities `2+1`;
the fourth normal must be the underrepresented variant so that each
other triple has the same property.  In support three the first triple
uses three vertices of the four-point sign rectangle, and the fourth
normal must be the missing vertex.  This proves the all-or-nothing
claim.

## Verification

Run:

```text
python claims/p3/restrictions/verify_p3_decomposable_restriction_classification.py
python claims/p3/restrictions/audit_p3_decomposable_restriction_classification.py
```

The primary verifier reconstructs (2), all six oriented-edge systems,
the canonical family, both zero-coordinate boundary calculations, and
the four-plane sign rectangles symbolically.  The independent audit
enumerates every rank-at-least-two subspace triple and every admissible
plane quadruple over `F_3` and `F_5`.  It finds only rank profile `222`;
the nonzero decomposable triple counts are `42` and `132`, exactly

```text
9(p-1) + 6(p-1)^2
```

for the support-two and support-three sign families.  The finite-field
census finds respectively `45=3+42` and `135=3+132` admissible plane
quadruples, with no mixed zero/nonzero pattern.  It audits the formulas;
the written proof above is over `C`.
