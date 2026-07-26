# Three-colour blocker-union lemma

## Status

This is an arbitrary-order local obstruction in the deeper-blocker
branch.  It combines the multi-star lower bound across all three colours
with the tight two-blocker factorisation.

It proves that a fully supported zero-coupled root pair needs at least
four distinct outside blocker vertices.  It is not yet a global
contradiction.

## Theorem

Fix two root vertices `p,r` and vectors `x,y in C^3` satisfying

```text
B_pr(x,y) = 0,
x[d] y[d] != 0 for d=0,1,2.                            (1)
```

At every outside vertex `u`, put

```text
a_u(z) = B_pu(x,z),
b_u(z) = B_ru(y,z),
S_u = span(a_u,b_u) subset (C^3)*.
```

Let

```text
D_d = {u outside {p,r} : e_d^* belongs to S_u}
```

be the colour-`d` blocker set.  Then

```text
|D_0 union D_1 union D_2| >= 4.                        (2)
```

## Proof

The two-root instance of the multi-star blocker lemma gives

```text
|D_d| >= 2 for every d.                                (3)
```

No vertex belongs to all three blocker sets, because `S_u` is spanned
by only two covectors and cannot contain the three independent
coordinate functionals.

Suppose the union in (2) had at most three vertices.  The six
incidences forced by (3), together with the capacity of at most two per
vertex, imply equality everywhere.  After relabelling the three
outside vertices, their blocker types are exactly

```text
u_01 in D_0 intersect D_1,
u_02 in D_0 intersect D_2,
u_12 in D_1 intersect D_2.                             (4)
```

In particular,

```text
S_(u_01) = span(e_0^*,e_1^*),
S_(u_02) = span(e_0^*,e_2^*),                          (5)
```

and each displayed pair `(a_u,b_u)` is a basis of its coordinate
plane.

Colour 0 has exactly the two blockers `u_01,u_02`.  The tight
two-blocker factorisation says that its root--blocker tensor

```text
F(z_01,z_02)
  = a_01(z_01) b_02(z_02)
    + b_01(z_01) a_02(z_02)                            (6)
```

has no mixed-colour coefficient.

Restrict the coefficient matrix of (6) to row coordinates `(0,1)` and
column coordinates `(0,2)`.  If `U,V` are the two invertible
coefficient matrices of the bases in (5), this matrix is

```text
U [0 1; 1 0] transpose(V).                             (7)
```

It has nonzero determinant `-det(U)det(V)` and therefore rank two.
But a globally diagonal tensor on those two different coordinate
planes can use only their common diagonal position `(0,0)`, so its
restricted matrix has rank at most one.  This contradiction proves
(2).

## Tight blocker-pair span dichotomy

The same calculation gives a reusable matrix classification.  Suppose
colour `c` has exactly two blockers `u,v`.  Its tight root--blocker
coefficient matrix is diagonal and has a nonzero `(c,c)` entry.

If both `S_u` and `S_v` have dimension two, write the coefficient matrix
again as `U J V^T`, now with `U,V` of full column rank.  It has rank two,
its column space is `S_u`, and its row space is `S_v`.  A rank-two
diagonal `3 x 3` matrix with nonzero `(c,c)` entry has both spaces equal
to

```text
span(e_c^*,e_d^*)
```

for one common second colour `d`.

If either span has dimension one, blocker membership makes that span
exactly `span(e_c^*)`.  Therefore every exact blocker pair obeys:

1. one blocker is a pure coordinate-`c` blocker; or
2. both blocker spans are the same coordinate plane containing `e_c`.

## Consequences

Every rank-at-least-two edge block has a zero pair `(x,y)` satisfying
(1): its irreducible bilinear zero hypersurface is not contained in any
coordinate hyperplane.  Hence every such edge in a hypothetical witness
has at least four distinct outside double-star blocker vertices across
the three colours.

The conclusion also applies to any rank-one edge whose zero locus has a
component meeting the full coordinate torus.  Coordinate-monomial
rank-one edges are the exceptional case already isolated by the killer
and bridge reductions.

The new lower bound is sharp at the level of blocker-incidence patterns.
There is nevertheless a complete four-vertex boundary classification.
If a colour has exactly two blockers and both of them block a second
colour, those second colours must agree.  Otherwise their covector spans
are two different coordinate planes meeting only in `e_c`, and the same
rank-two versus rank-one argument used in (7) is a contradiction.

Enumerating the six nonempty blocker types of size at most two under
this rule leaves, up to a colour permutation, exactly three multisets:

```text
0, 0, 12, 12
0, 01, 12, 12
01, 01, 02, 02.                                        (8)
```

Thus every fully supported zero pair has either at least five blocker
vertices or one of the three explicit four-vertex incidence types in
(8).  In the first two types, the tight span dichotomy additionally
forces at least one of the singleton-type blockers to be the pure
coordinate line.  The next step is to intersect those patterns for
adjacent root edges or combine them with the exact diagonal
root--blocker tensors.

## Verification

Run:

```text
python verify_three_colour_blocker_union.py
python audit_three_colour_blocker_union.py
```

The primary verifier exhausts every blocker-incidence assignment on at
most four vertices, recovers the three orbits in (8), and checks the
determinant identity in (7) symbolically.  The independent audit
reconstructs the incidence census from bit masks and exhausts all
invertible `2 x 2` matrices over `F_3`, confirming that the restricted
tensor always has rank two while the permitted diagonal intersection
has rank at most one.  The written proof is over `C` and
arbitrary-order.
