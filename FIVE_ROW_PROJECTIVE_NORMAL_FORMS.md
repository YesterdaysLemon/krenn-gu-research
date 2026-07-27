# Five-row projective normal forms

## Status

This is an exact local theorem over `C`.  It strengthens the five-row
projective incidence lemma by classifying the hardest case, in which a
local map has exactly one singleton row.  It still does not by itself
exclude every hypothetical restriction

```text
P_5 -> Delta_3.
```

## The theorem

Let

```text
r_0,...,r_4 in C^3
```

span `C^3`, and suppose that for every distinct `p,q`,

```text
span(r_p,r_q) contains one of e_0,e_1,e_2.              (1)
```

Call a nonzero row **coordinate** if it is proportional to some `e_c`,
and otherwise call its projective point **non-coordinate**.

If a zero row occurs, every other nonzero row is coordinate.  Otherwise,
the non-coordinate projective points are distinct, there are at most
four of them, and they have the following complete classification.

1. Four non-coordinate points either all lie on one line containing a
   coordinate point, or no three are collinear and they form a complete
   quadrangle whose three diagonal points are exactly
   `E_0,E_1,E_2`.
2. Three non-coordinate points either lie on one line containing a
   coordinate point, or form a triangle whose three sides contain the
   three different coordinate points.
3. The line through two non-coordinate points contains a coordinate
   point.  Cases with at most one non-coordinate point need no further
   condition.

In the complete-quadrangle case, after reordering its four vertices and
applying an invertible diagonal change of the three coordinates, they
have the projective representatives

```text
( 1, 1, 1),
(-1, 1, 1),
( 1,-1, 1),
( 1, 1,-1).                                             (2)
```

Thus a spanning five-row configuration with exactly one coordinate row
has only two forms:

- **line type:** the other four rows lie on one coordinate-bearing
  projective line, and the coordinate row lies off that line;
- **quadrangle type:** the other four rows have the rigid sign pattern
  (2), up to the stated projective equivalences.

## Proof

A zero row paired with any other row makes (1) force that other row to
be coordinate.  Assume from now on that every row is nonzero.  Two
equal non-coordinate projective points are impossible, because their
one-dimensional span contains no coordinate point.  The earlier
five-row incidence lemma supplies at least one coordinate row, so there
are at most four non-coordinate points.

The assertions for zero, one, or two non-coordinate points are now
immediate.  For three points, if they are noncollinear, each side
contains a coordinate point by (1).  The same coordinate point cannot
lie on two sides, because those sides meet at a non-coordinate vertex.
The three sides therefore use `E_0,E_1,E_2` once each.

Consider four non-coordinate points.  If three lie on a line `L`, then
`L` contains at least one `E_c`.  Were the fourth point `Q` off `L`, the
three different lines from `Q` to those three points would have to use
three different coordinate points.  Any coordinate point already on
`L` is unavailable: its line to `Q` meets `L` at that coordinate point,
not at one of the three non-coordinate points.  Fewer than three
coordinate points remain, a contradiction.  Hence all four points lie
on `L`.

It remains that no three are collinear.  A side cannot contain two
coordinate points.  If, for example, `P_1P_2` contained `E_0,E_1`,
then each of `P_1P_3` and `P_2P_3` would have to contain `E_2`; their
intersection would make the non-coordinate point `P_3` equal to
`E_2`.  Thus every side contains a unique coordinate point.

Colour a side by that point.  Every triangle is rainbow.  On `K_4`
this forces opposite sides to have the same colour: after colouring
one triangle `0,1,2`, the colours of the three edges to its fourth
vertex are forced.  Consequently the intersections of the three pairs
of opposite sides are `E_0,E_1,E_2`.

Relabel the vertices so that

```text
E_0 = P_1P_2 intersect P_3P_4,
E_1 = P_1P_3 intersect P_2P_4,
E_2 = P_1P_4 intersect P_2P_3.                          (3)
```

No coordinate of `P_1=(a,b,c)` is zero.  For example, if `a=0`, the
line through `P_1` and `E_1` would also contain `E_2`, contrary to the
uniqueness of the coordinate point on a side.  Rescale the other
projective representatives along the three lines in (3) to write

```text
P_2=(x,b,c),  P_3=(a,y,c),  P_4=(a,b,z).
```

The other three incidences in (3) say

```text
yz=bc,  xz=ac,  xy=ab.
```

For `X=x/a`, `Y=y/b`, `Z=z/c`, these become

```text
YZ=XZ=XY=1.
```

Hence `X=Y=Z` and their common value squares to one.  The value `+1`
would repeat `P_1`, so it is `-1`.  Diagonal rescaling by
`diag(a^-1,b^-1,c^-1)` gives (2).

## Consequence for a hypothetical `P_5` restriction

For a local map

```text
phi_i : C^3 -> C^5,
```

the support-three contraction theorem gives condition (1) for its five
source-coordinate rows.  Therefore each local map lies in one of three
strata:

1. it has at least two coordinate rows;
2. it has exactly one coordinate row and is of line type;
3. it has exactly one coordinate row and is of quadrangle type.

The line type has an additional useful dual description.  Let `L` be
the two-dimensional vector space underlying its projective line.  Its
annihilator is a target vector `t`.  Since `L` contains some `e_a^*`,
the vector `t` has target support at most two.  It kills all four
non-coordinate rows, while the unique coordinate row, which lies off
`L`, does not kill it.  Thus

```text
phi_i(t) has source-coordinate support exactly one.     (4)
```

The quadrangle stratum is instead projectively rigid by (2).  These
three strata replace the unrestricted 68 singleton-placement orbits by
a geometric case split with one rigid exceptional shape.

## Verification

Run:

```text
python verify_five_row_projective_normal_forms.py
python audit_five_row_projective_normal_forms.py
```

The primary verifier exhausts the edge-colour constraints on `K_4`,
checks the opposite-edge rule, reconstructs the standard quadrangle,
and verifies the line-type annihilator consequence.  The independent
audit enumerates all spanning five-row multisets in `PG(2,F_5)` with an
optional zero row, checks (1), and independently places every retained
configuration in the stated stratum.

## Boundary

Projective row directions do not record their nonzero magnitudes.
Those magnitudes still enter the permanent cancellation equations.
The later
[`P5_COORDINATE_PLANE_PAIR_COVER.md`](P5_COORDINATE_PLANE_PAIR_COVER.md)
combines the local strata across all five modes and forces either a
multiple-coordinate-row map or an axial `4+1` line map.  Those branches
still require the mixed-row permanent identities; the theorem above is
a reduction, not a declaration that the prize conjecture is solved.
