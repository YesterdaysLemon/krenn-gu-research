# Cyclic rank-one triangles are controlled by a gain graph

## Status

**Exact support-two classification theorem over `C`.**  Let three marked
planes of a nonzero pure `P_4` restriction form a triangle of rank-three pair
images whose unique relations have the cyclic rank-one orientation

```text
y_1x_2=0,       y_2x_3=0,       x_1y_3=0.          (1)
```

Assume every zero product in (1) has genuine two-coordinate support.  Then,
up to source-coordinate and mode symmetry, the tuple belongs to one of
exactly four already certified closures:

1. component sixteen, when the three distinct support labels form a source
   star;
2. component seventeen, when they form a source path;
3. the lower-pair/embedded-`P_3` union, when they form a source triangle;
4. component eight, when exactly two labels coincide and the third is
   disjoint.

The other repeated-label cases are zero, degenerate, or lower-pair.  Thus
this complete cyclic Borel orientation creates no component beyond sixteen
and seventeen.  Support-one zero products and other Borel orientations are
not asserted here.

## Exact pairs as a `C^*`-gain graph

In

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2),   (2)
```

a genuine binary zero product on support `{i,j}` has the form

```text
(X_i+lambda X_j)(X_i-lambda X_j)=0,       lambda!=0. (3)
```

Attach the gain `lambda` to the support edge `ij` of the source `K_4`.
Diagonal source scaling switches the gains at vertices.  Consequently all
gains on a forest can be normalized to one, while a support cycle retains
one multiplicative holonomy.

This is exactly the elementary switching mechanism of a gain graph.  The
general language originates in Zaslavsky's
[Biased graphs I: Bias, balance, and gains](https://doi.org/10.1016/0095-8956(89)90063-4):
a spanning forest can be switched to neutral gains, and products around
cycles are invariant.  That literature does not contain the permanent
purity consequences below; it supplies the right coordinate-free shape for
the normalization.

## Distinct labels: only three source graphs

Three distinct edges of `K_4` have exactly three isomorphism types:

```text
source star:       degree sequence (3,1,1,1),
source path:       degree sequence (2,2,1,1),
source triangle:   degree sequence (2,2,2,0).       (4)
```

The star and path are trees, so switching removes all three gains.  Their
normal forms are precisely the two apolar directed triangles in
[`P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md`](../../../../../P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md).
All three leaf-pair ranks are three; the kernel and active triple covectors
are independent; and the opposite apolar `P^2` produces components sixteen
and seventeen.

For the support triangle, normalize its three labels to `01,12,02` and
write their gains as `lambda,mu,nu`.  The marked planes are

```text
U_1=span(X_0+lambda X_1,       X_1+mu X_2),
U_2=span(X_0+nu X_2,           X_0-lambda X_1),
U_3=span(X_1-mu X_2,           X_0-nu X_2).         (5)
```

All six mixed cubics vanish by (1).  The remaining kernel and active cubic
covectors are

```text
C=(0,0,0, nu-lambda*mu),
D=(0,0,0,-nu-lambda*mu).                            (6)
```

Since `C,D` are proportional, a mode-zero plane cannot annihilate `C` while
detecting `D` unless

```text
nu=lambda*mu.                                      (7)
```

This is precisely neutral gain around the source triangle.  On (7), all
three pair images in (5) have rank two, with two independent rank-one
relations apiece.  The tuple is therefore already in the exhaustive
lower-pair union; conceptually, all three leaves also lie in one coordinate
three-space, so the nonzero restriction is an embedded-`P_3` suspension.

Thus the missing third simple support graph is not an eighteenth component.

## Exactly two equal labels

Put the repeated label at `01`, with gains `lambda,mu`, and let the third
gain be `nu`.

If the third support is adjacent, normalize it to `02`.  The two surviving
cubics are equal:

```text
C=D=(0,0,0,nu(lambda-mu)).                          (8)
```

Plane nondegeneracy requires `lambda!=mu`, so (8) is nonzero.  An opposite
plane that kills the kernel cubic automatically kills the active cubic.
Hence this branch has no nonzero pure restriction.

If the third support is disjoint, normalize it to `23`.  Now

```text
C=(0,0,nu(lambda-mu), lambda-mu),
D=(0,0,nu(lambda-mu),-lambda+mu).                   (9)
```

These are independent when the planes are nondegenerate.  After switching,
set `lambda=nu=1` and write `r=mu/lambda`.  An affine chart of the apolar
opposite plane and an exact one-parameter opening are

```text
U_0=span((1,0,p,-p),(0,1,q,-q)),
U_1=span((1,1,0,0),(1,r,0,0)),
U_2=span((0,0,1,1),(1,-1,0,0)),
U_3(k)=span((1,-r,0,0),(0,k,1,-1)).                (10)
```

For every `k`, direct expansion gives only

```text
T_0111=-2p(r-1),       T_1111=-2q(r-1).            (11)
```

At `k=0`, (10) is the repeated-disjoint cyclic triangle.  Its pair profile
is

```text
(3,4,4,3,3,3).                                     (12)
```

For `k!=0` on a dense open, the `23` triangle edge becomes full while the
exceptional graph becomes a three-edge star with profile

```text
(3,4,4,3,3,4).                                     (13)
```

Its support multiset is exactly `{01,01,23}` with the disjoint mixed-star
orientation.  The complete projective theorem
[`P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md`](../../../../../P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md)
places every punctured point of (10) in component eight.  Letting `k->0`
places the cyclic triangle in the same closure.  The apparent transverse
tangent is therefore an actual component-eight opening, not a new
component.

## All three labels equal

If all labels coincide, nondegeneracy makes every leaf plane the same
binary coordinate plane.  Every leaf-pair product image then has rank one.
The global rank-one-pair obstruction excludes a nonzero pure restriction.

## Consequence for the all-pair-rank frontier

Within the genuine support-two cyclic orientation (1), every nonzero pure
tuple is now assigned:

```text
distinct tree labels          -> component 16 or 17,
distinct cyclic labels        -> lower-pair / embedded P3,
repeated adjacent labels      -> zero,
repeated disjoint labels      -> component 8 boundary,
three equal labels            -> rank-one-pair obstruction.      (14)
```

This removes one complete all-pair-rank-at-least-three exceptional graph
from the component-exhaustiveness frontier.

## Exact replay

```text
uv run --with sympy python claims/p4/classifications/triangle-211/cyclic-rank-one-triangle-support/verify_p4_cyclic_rank_one_triangle_support_classification.py
python claims/p4/classifications/triangle-211/cyclic-rank-one-triangle-support/audit_p4_cyclic_rank_one_triangle_support_classification.py
```

The primary verifier checks the three source-graph types, every sign sheet,
the weighted holonomy formulas (6), the repeated-label formulas (8)--(9),
and the exact opening (10)--(13).  The independent audit uses integer
squarefree multiplication and rational row reduction.  The finite eight
sign sheets are a constant switching check, not a parameter or graph search.
