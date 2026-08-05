# WITHDRAWN: overstrong rank-two-relation star obstruction

## Status

**WITHDRAWN.**  The generic-center step invokes the withdrawn complete
flat-triangle classification, whose full-`GL_2` normalization moved
the purity-fixed kernel line.  The tree gauge, synchronizer pencil,
rank-drop matching, and constant balanced-chart coefficient remain
exact local lemmas, but they did not prove the advertised global star
obstruction by that route.

The star obstruction has since been reproved with the corrected Borel
triangle classification and a separate full-support `2+2` chart:
[`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md`](P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md).
This file remains withdrawn because its original proof route is invalid;
use the replacement theorem for the current result.

The withdrawn theorem had claimed an exact obstruction for the
all-rank-three-pair stratum of a nonzero pure `P_4` restriction.
Suppose three exceptional pair edges form a star, every one has image
rank three, and every unique multiplication relation has
coefficient-matrix rank two.  Then no such plane tuple exists.

The proof uses tree gauge, the four-point classification of one
`2 x 4` row-pair, a matching on the parameter line of its adjugate
pencil, and one constant permanent on the balanced collision.  It
uses no elimination or component search.

The full star, mixed orientations, and lower pair-image-rank boundary
remain open; component exhaustiveness and the global Krenn--Gu
conjecture are not proved.

## Tree gauge makes a synchronization star

Let mode zero be the center and modes `1,2,3` the leaves.  In pure
factor bases `(y_i,x_i)`, the active-active coefficient of every
exceptional relation vanishes.  Since the relation matrix has rank
two, row scaling gives

```text
A_i y_0y_i+y_0x_i-x_0y_i=0.                                    (1)
```

The graph is a tree, so the three independent shifts

```text
x_i -> x_i+A_i y_i
```

kill all constants without holonomy.  Thus

```text
y_0x_i=x_0y_i,                    i=1,2,3.                       (2)
```

Every leaf row-pair is a synchronized partner of the center
row-pair.

## Zero and low-collision centers

Regard the center's four columns as labelled points of `P^1`, allowing
zero columns.

If one center column is zero, (2) and the nondegenerate alternating
form on `C^2` force the same leaf column to vanish for every leaf.
All four planes then lie in one coordinate hyperplane, so their
degree-four squarefree product is zero.

If the center has a `2+1+1` projective collision, normalize it to

```text
y_0=(1,1,0,1),
x_0=(0,0,1,1).
```

Every synchronized leaf has

```text
y_i=c_i y_0+d_i(0,0,1,-1),
x_i=c_i x_0.
```

Center-leaf rank three forces `c_i!=0`.  After row-pair rescaling, all
four active rows equal `x_0`, and the required pure coefficient
vanishes because `x_0` has support two:

```text
x_0x_1x_2x_3=x_0^4=0.                                           (3)
```

For a `1+3` split, every synchronized rank-two leaf spans the center
plane itself.  That plane squares into only
`span(y_0x_0,x_0^2)`, so the center-leaf pair image has rank at most
two.  A one-point configuration would make the center row-pair rank
one.

## The generic synchronizer pencil

Suppose the center has four nonzero distinct columns.  Normalize

```text
y=(1,0,1,1),
x=(0,1,1,lambda),                  lambda(lambda-1)!=0.            (4)
```

Every leaf lies on the projective adjugate pencil

```text
A(t)=A+tA^#,

y^#=(0,1,-1,-lambda),
x^#=(lambda,0,-lambda,-lambda).                                  (5)
```

The whole pencil is synchronized: any two members have the rank-two
relation

```text
y(t)x(u)=x(t)y(u).                                                (6)
```

Their pair image has rank below three precisely when at least two of

```text
R_1=lambda*t*u-1,
R_2=lambda*t*u-t-u+1,
R_3=lambda*t*u-lambda*t-lambda*u+1                               (7)
```

vanish.  The three alternatives are:

```text
R_1=R_2=0:      t,u are the roots of z^2-2z+1/lambda;
R_1=R_3=0:      t,u are the roots of z^2-(2/lambda)z+1/lambda;
R_2=R_3=0:      {t,u}={r,-r},       lambda*r^2=1.                 (8)
```

For `lambda!=0,1`, the three two-point sets in (8) are pairwise
disjoint and have no repeated point.  The rank-drop graph on the
affine parameter line is therefore a matching of three edges.
The projective point `t=infinity` has no rank-drop partner: the three
leading factors are

```text
lambda*u,       lambda*u-1,       lambda*(u-1),
```

and no two vanish together when `lambda!=1`.

Among three leaves, some pair therefore has image rank three.  Modes
zero and those two leaves form a flat triangle of three rank-three
pairs with rank-two relations.  But the complete flat-triangle
classification says that such a triangle must have a balanced
`2+2` center, contradicting (4).  Hence the four-distinct center is
impossible.

## The balanced collision has a constant forbidden coefficient

Only a `2+2` center remains.  Put

```text
a=(1,1,0,0),        a_bar=(1,-1,0,0),
b=(0,0,1,1),        b_bar=(0,0,1,-1),

(y_0,x_0)=(a,b).                                                    (9)
```

Every synchronized leaf is

```text
y_i=c_i a+beta_i b_bar,
x_i=c_i b+alpha_i a_bar.                                         (10)
```

Center-leaf rank three forces `c_i!=0`; rescale to `c_i=1`.
Now select the center kernel row, the first leaf kernel row, and the
other two leaf active rows.  Squarefree multiplication and

```text
a a_bar=0,                     b b_bar=0
```

give the parameter-free coefficient

```text
a(a+beta_1 b_bar)
 (b+alpha_2 a_bar)(b+alpha_3 a_bar)
 =a^2b^2
 =4X_0X_1X_2X_3.                                                 (11)
```

It contains kernel rows and must vanish in a pure tensor.  Equation
(11) is the final contradiction.

Thus no star of three rank-three pair images with rank-two unique
relations exists.

## Consequence for the component graph

When all six pair-image ranks are at least three, perfect pairing
forces at least one exceptional edge in each of the three perfect
matchings of `K_4`.  Three selected exceptional edges contain a star
or a triangle.

If all three selected relations have matrix rank two, the star is
excluded here and the triangle is lower-dimensional by the complete
triangle classification.  Hence a missing component on the
all-pair-rank-at-least-three locus must use a rank-one relation or a
mixed rank-one/rank-two selection.  This removes the
“predominantly rank-two” generic alternative in its pure form, but
does not yet classify all mixed selections.

## Verification

Run:

```text
python verify_p4_rank_two_relation_star_obstruction_withdrawn_overstrong.py
python audit_p4_rank_two_relation_star_obstruction_withdrawn_overstrong.py
```

These scripts replay the exact local identities but do not certify the
withdrawn global scope.  The primary verifier derives the three center synchronizer spaces,
checks the rank-drop matching (7)--(8), and replays the constant
coefficient (11).  The independent audit uses the crossed `2+2`
partition, resultant checks for the three matching edges, and a
separate dynamic-programming permanent.  Both are exact symbolic
proof replays, not searches.
