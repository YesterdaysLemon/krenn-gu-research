# A second pure rank-two `P_4` component from diagonal quadrics

## Status

This is an exact algebraic-geometric theorem over `C`.

The all-rank-two plane locus on which `P_4` restricts to a nonzero
decomposable tensor has an irreducible component which is not in the
source/mode symmetry orbit of the component described in
[`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](P4_PURE_RANK_TWO_COMPONENT_THEOREM.md).
The new component has dimension five.  A dense three-parameter normal
form is an irreducible hypersurface in `P^2 x P^2`; its orbit under
diagonal source rescaling fills the component.

This corrects the previous frontier in a substantive way: additional
pure-compression components do exist.  The theorem is at plane level.
It does not classify the complete new component boundary or its marked
`H31` fibre, exclude `H31`, settle `H22`, or resolve the global prize
problem.

## Squarefree intersection algebra

Let

```text
A = C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).   (1)
```

The coefficient of `X_0 X_1 X_2 X_3` in a product of four linear forms
is their `P_4` permanent.  Thus `P_4` is the Frobenius intersection
form of the Artinian complete intersection (1).

For planes `U,V subset A_1`, the pair-image space used in the
flattening arguments is simply

```text
U V subset A_2.                                      (2)
```

If multiplication `U tensor V -> A_2` has a nonzero kernel, lift a
kernel relation to the ordinary polynomial ring.  Its squarefree
terms vanish, so

```text
u_0 v_0+u_1 v_1 = d_0 X_0^2+...+d_3 X_3^2.          (3)
```

When the relation has matrix rank two, the annihilator lines
`ell_U=P(U^perp)` and `ell_V=P(V^perp)` therefore lie on the same
diagonal quadric.  Conversely, for two skew lines, a diagonal quadric
through both gives (3).  This identifies the exceptional pair-image
incidence with the geometry of lines on diagonal quadrics, rather than
with an ambient coefficient search.

For one line `ell subset P^3`, put

```text
D(ell) = {
  (d_0,...,d_3) :
  sum d_i X_i^2 vanishes identically on ell
}.                                                    (4)
```

A general line has `dim D(ell)=1`.  The jump locus
`dim D(ell)>=2` consists of block lines: after partitioning the four
coordinates into two nonempty blocks, the line joins one point in
each coordinate block.  Indeed, the four coordinate forms restricted
to `ell=P^1` have squares on a Veronese conic; three distinct
directions span all binary quadrics, while at most two directions span
a plane.

## The radical-plane normal form

Use the following rows:

```text
y_1=(1,0,0,-1),                 y_2=(0,1,-1,0),
k_0=(1,0,0, 1),                 k_1=(0,1, 1,0),

x_1=(A,C+B,C-B,A),
x_2=(H+E,F,F,H-E),

u_0=(E,-F,-F,-E),
u_1=(A,-B, B, A).                                   (5)
```

Define four planes, with the displayed row order, by

```text
U_0=span(u_0,u_1),
U_1=span(y_1,x_1),
U_2=span(x_2,y_2),
U_3=span(k_0,k_1).                                  (6)
```

The geometry behind (5) is short.  Double contraction by `y_1,y_2`
gives the rank-two symmetric bilinear matrix

```text
  0  1 -1  0
  1  0  0 -1
 -1  0  0  1
  0 -1  1  0,
```

whose radical is exactly `U_3`.  Contraction by `y_1,x_2` on `U_3`
leaves the covector

```text
(-F,-E,-E,F),
```

while contraction by `x_1,y_2` leaves

```text
(-B,-A,A,-B).
```

Their common kernel is `U_0`, as displayed in (5).  Consequently every
restricted coefficient having the kernel row `y_1` or `y_2` vanishes.

The only possibly nonzero coefficients are

```text
T_0100 = -4 F (A F+C H),
T_0101 = -4 (A F H+C E^2),
T_1100 =  4 (A C F+B^2 H),
T_1101 =  4 A (A F+C H).                            (7)
```

They form a `2 x 2` matrix in modes zero and three.  Its determinant is

```text
-16 Psi,
```

where

```text
Psi =
  A^3 F^3 + A^2 C F^2 H
  - A B^2 F H^2
  - A C^2 E^2 F + A C^2 F H^2
  - B^2 C E^2 H.                                    (8)
```

Thus, on the open set where all four planes have rank two and (7) is
not the zero matrix,

```text
Psi=0                                               (9)
```

is equivalent to a nonzero pure restriction.

## Irreducibility and dimension

The polynomial `Psi` has bidegree `(3,3)` in

```text
(A:B:C) and (E:F:H).
```

It is irreducible.  To see this without factor enumeration, write

```text
Psi=P-B^2 Q,

P=A F (A^2 F^2+A C F H-C^2 E^2+C^2 H^2),
Q=H(A F H+C E^2).                                  (10)
```

The polynomials `P,Q` are coprime.  Over the fraction field
`C(A,C,E,F,H)`, the quadratic in `B` could factor only if `P/Q` were a
square.  Its valuation at `A=0` is one, so it is not a square.
Gauss's lemma proves irreducibility.

Hence `V(Psi) subset P^2 x P^2` is an irreducible threefold.  Apply a
common diagonal source rescaling to the four planes.  At

```text
(A,B,C,E,F,H)=(1,1,0,2,1,1),                       (11)
```

use the affine charts `B=F=1`, solve (8) locally for `H`, and vary

```text
A,C,E,t_0,t_1.
```

In the all-`01` Grassmann chart, the rows

```text
U_0:a,b,c,d and U_1:c
```

of this five-parameter tangent matrix have determinant

```text
-24.                                                (12)
```

The diagonal-source orbit of (9) therefore has dimension at least
five.

## Exact component certificate

At (11), the four ordered row pairs are

```text
U_0=((2,-1,-1,-2),(1,-1,1,1)),
U_1=((1, 0, 0,-1),(1, 1,-1,1)),
U_2=((3, 1, 1,-1),(0, 1,-1,0)),
U_3=((1, 0, 0, 1),(0, 1, 1,0)).                    (13)
```

Their restriction is

```text
(-4 x_0+4 y_0) y_1 x_2 (x_3+y_3).                  (14)
```

All four `01` Pluecker coordinates are nonzero.  Row reduction gives
the sixteen plane-chart coordinates

```text
(-2,-3,-3,-4,
   0,-1,-1, 2,
 2/3,-1/3,-1,0,
   0, 1, 1,0).                                      (15)
```

Use the target Segre anchor `0100`, with ratios

```text
(z_0,z_1,z_2,z_3)=(3/2,0,0,1).                     (16)
```

The fifteen standard Segre-incidence equations have Jacobian rank
fourteen at (15)--(16).  A `14 x 14` minor has determinant

```text
1048576/243.                                        (17)
```

Thus the Zariski tangent space has dimension six.  The apparent sixth
direction is not an additional component direction.  In the variable
order consisting of the sixteen chart coordinates followed by the
four `z` coordinates, take

```text
v=(15,21,21,33, -11,11,15,-21, 4,0,0,0,
   0,0,0,0, 0,0,0,0).                              (18)
```

It is tangent and independent of the five family directions.  Order
the incidence equations lexicographically, omitting the anchor
`0100`, and take the Jacobian-cokernel vector

```text
lambda=(9,0,6,0,0,0,0,-6,0,-4,0,0,0,0,0).         (19)
```

The linear term of the combination in (19) vanishes.  Its quadratic
term evaluated on (18) is

```text
-132.                                               (20)
```

Therefore the tangent cone is contained in a nonzero quadric inside
the six-dimensional tangent space.  Its dimension is at most five.
The irreducible family already has dimension five by (12), so its
closure is an irreducible component of the incidence locus.  Since a
nonzero decomposable tensor has unique projective factors, projection
from the incidence chart to the plane locus is an isomorphism here.
This proves the component theorem.

## Distinctness from the known component

For the four annihilator lines of (13), the dimensions in (4) are

```text
(1,1,1,2).                                          (21)
```

Thus only one of the four planes is on the block-line jump locus.
For every point of the earlier component chart, three fixed modes have
`dim D(ell)>=2`; the same remains true on its closure because it is a
closed rank condition.  Source-coordinate permutations, diagonal
source rescalings, and mode permutations preserve the number of such
planes.  Consequently (13) is outside every symmetry translate of the
known component.

## Consequence for `H31`

The complete marked fibre of the first component remains validly
excluded.  It no longer exhausts the all-rank-two `H31` frontier:
the component proved here has its own marked-basis bundle and boundary,
which have not yet been classified.  Any global `H31` exclusion must
now handle this component and still prove whether further components
exist.

## Verification

Run:

```text
python verify_p4_diagonal_quadric_pure_component.py
python audit_p4_diagonal_quadric_pure_component.py
```

The primary verifier expands (5)--(8), checks irreducibility, derives
the rank-five family tangent, reconstructs the characteristic-zero
Jacobian minor, and verifies the exact quadratic tangent-cone
certificate (18)--(20).  The independent audit uses a separate
dynamic-programming permanent, modular dual numbers, truncated
second-order jets, and modular diagonal-quadric ranks.  Its finite-field
calculations audit the certificates; the displayed rational identities
and tangent-cone argument prove the theorem over `C`.
