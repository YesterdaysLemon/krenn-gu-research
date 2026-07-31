# Two rank-two edges cannot close with a rank-one triangle edge

## Status

This is an exact characteristic-zero obstruction on the
all-pair-rank-at-least-three pure `P_4` locus.

Suppose three exceptional edges form a triangle, every pair image has
rank three, two unique relations have coefficient-matrix rank two,
and the third has coefficient-matrix rank one.  Then no such plane
tuple exists.

The proof combines tree synchronization, the projective-column
classification of the common mode, and the degree-one annihilator of
a linear form in the squarefree algebra.  It uses no elimination or
component search.

Together with the pure rank-two star obstruction and complete
rank-two triangle classification, this leaves only mixed selections
with at most one rank-two edge, plus the lower pair-rank boundary.
It does not prove component exhaustiveness or the global Krenn--Gu
conjecture.

## Normalize the two rank-two edges

Let the rank-two relations be on edges `12` and `13`.  They form a
tree, so active-row shifts and scalings give

```text
y_1x_2=x_1y_2,
y_1x_3=x_1y_3.                                                    (1)
```

Thus the row-pairs of modes two and three are synchronized partners
of the mode-one row-pair.

The remaining edge `23` has image rank three and therefore a unique
relation.  By hypothesis that relation has matrix rank one.  Because
its active-active coefficient is zero, it must factor in one of the
two forms

```text
y_2 w_3=0,                 w_3 in U_3 nonzero,
w_2 y_3=0,                 w_2 in U_2 nonzero.                    (2)
```

## The easy projective-column types

If the common row-pair in mode one has a zero source column, (1)
propagates it to modes two and three.  The three planes lie in one
coordinate hyperplane.  A nonzero pure `P_4` restriction then
suspends a pure `P_3`, and perfect pairing forces their pair images
to have rank at most two.

For four nonzero distinct projective columns, every synchronized
partner lies on the adjugate pencil `A+tA^#`.  That pencil is totally
synchronized, so

```text
y_2x_3=x_2y_3.                                                    (3)
```

Since edge `23` has rank three, (3) spans its one-dimensional kernel
and has coefficient-matrix rank two, contradicting the rank-one
hypothesis.

For a `2+1+1` collision, every partner has the form

```text
y_i=c_i y+d_i z,
x_i=c_i x,

xz=0.
```

Center-leaf rank three forces `c_i!=0`; rescale to `c_i=1`.
Then the two leaves again obey (3), giving the same contradiction.

For a `1+3` split, every synchronized partner spans the common mode
plane, whose square has dimension two.  This contradicts either
center-leaf rank three.

## The balanced `2+2` center

It remains to use

```text
a=(1,1,0,0),        a_bar=(1,-1,0,0),
b=(0,0,1,1),        b_bar=(0,0,1,-1),

(y_1,x_1)=(a,b).                                                    (4)
```

Every synchronized rank-three partner is

```text
y_i=a+beta_i b_bar,
x_i=b+alpha_i a_bar.                                              (5)
```

The following elementary annihilator fact is decisive:

> A linear form supported on at least three source coordinates has
> zero degree-one annihilator in the squarefree algebra.  A
> two-supported form `a` has
> `Ann_R1(a)=C a_bar`.

If `beta_2!=0`, then `y_2` in (5) has support four, so the first
factorization in (2) is impossible.  If `beta_2=0`, then `y_2=a` and
it would force

```text
w_3 in C a_bar.                                                    (6)
```

But no nonzero combination of the rows of `U_3` is `a_bar`.  Indeed,

```text
A(a+beta_3 b_bar)+B(b+alpha_3 a_bar)=a_bar
```

has independent block coefficients

```text
A=0,                  B=0,                   B alpha_3=1,
```

which are inconsistent.

Thus `y_2w_3=0` is impossible.  Interchanging modes two and three
excludes `w_2y_3=0`.  This closes the last projective-column type and
proves the theorem.

## Consequence

On a rank-three exceptional triangle, a matrix-rank pattern

```text
(2,2,1)
```

cannot occur.  The all-rank-two pattern is already classified and
lower-dimensional.  Hence a generic mixed triangle not already
captured by the rank-one component classifications can have at most
one rank-two edge.

## Verification

Run:

```text
python verify_p4_mixed_two_rank_two_triangle_obstruction.py
python audit_p4_mixed_two_rank_two_triangle_obstruction.py
```

The primary verifier checks the totally synchronized generic and
collision pencils, the balanced synchronizer space, its annihilator
alternative, and the inconsistent containment (6).  The independent
audit uses the crossed coordinate partition and a direct coefficient
matrix for all possible row combinations.  Both are exact symbolic
proof replays, not searches.
