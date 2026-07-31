# The mixed `(2,2,1)` triangle is empty

## Status

**Corrected exact theorem.**  On the nonzero pure `P_4` locus, suppose three
exceptional edges form a triangle, every pair image has rank three, two unique
relations have coefficient-matrix rank two, and the third has
coefficient-matrix rank one.  No such plane tuple exists.

The earlier version of this statement was withdrawn because it used an
unmarked `GL_2` row change where purity permits only Borel row changes.  The
proof below keeps the kernel rows marked.  Its only formerly missing Borel
chart is a four-minor calculation in a presymplectic plane.

This is a theorem about the indicated triangle stratum.  It is not component
exhaustiveness and does not prove the global Krenn--Gu conjecture.

## Turn the two rank-two edges into a synchronizer problem

Put the coefficient-rank-two relations on edges `12` and `13`.  Since those
edges form a tree, Borel-legal active-row shifts and scalings normalize them to

```text
y_1 x_2 = x_1 y_2,
y_1 x_3 = x_1 y_3.                                               (1)
```

Thus `U_2` and `U_3` are synchronized partners of the marked center `U_1`.
The projective-column classification of the center is already exhaustive.
It has the following consequences.

- A zero source column reduces to the pure `P_3` theorem, forcing a pair rank
  at most two.
- In every two-dimensional synchronizer pencil other than the exceptional
  balanced charts below, the synchronizer plane is totally isotropic: any two
  partners obey `y_2 x_3=x_2 y_3`.  If their pair image has rank three, its
  unique relation therefore has coefficient rank two, not one.
- A one-supported center already has center-leaf pair rank at most two.

This leaves exactly the support-two equal-ratio boundary and the full-support
`2+2` collision chart.

## The support-two equal-ratio boundary

Use

```text
a=(1,1,0,0),        a_bar=(1,-1,0,0),
b=(0,0,1,1),        b_bar=(0,0,1,-1).
```

In this marked chart a synchronized partner is

```text
y_i=a+beta_i b_bar,
x_i=b+alpha_i a_bar.                                             (2)
```

The squarefree degree-one annihilator of a linear form supported on at least
three coordinates is zero, while

```text
Ann_R1(a) = C a_bar.                                              (3)
```

A rank-one coefficient relation on edge `23` has zero active-active entry and
must factor as either `y_2 w_3=0` or `w_2 y_3=0`.  If the displayed `y` factor
has support at least three, (3) makes this impossible.  On the two-supported
boundary the other leaf would have to contain `a_bar`, but

```text
span(a+beta b_bar, b+alpha a_bar, a_bar)
```

has dimension three identically.  Hence neither factorization occurs.  This
argument uses the marked rows and no forbidden row swap.

## The full-support `2+2` chart is presymplectic

The last Borel chart has center

```text
(y_1,x_1)=(a+b,b)
```

and, after the permitted nonzero leaf rescalings, synchronized leaves

```text
y_i=a+b-r_i b_bar-s_i a_bar,
x_i=b-s_i a_bar.                                                 (4)
```

The synchronizer plane carries an alternating commutator form.  For the two
leaves its value is

```text
Delta = r_2 s_3-r_3 s_2,

y_2 x_3-x_2 y_3
  = Delta (0,1,-1,-1,1,0).                                      (5)
```

This is the presymplectic radical test hiding behind the graph relation.

Let `M_23` be the `6 x 4` matrix with columns
`y_2y_3,y_2x_3,x_2y_3,x_2x_3`.  Four of its maximal minors are, up to the
displayed nonzero constants,

```text
-8 Delta [s_2s_3(r_2+r_3)-(s_2+s_3)],
 8 Delta [s_2s_3(r_2+r_3)+(s_2+s_3)],
 8 Delta [r_2r_3(s_2+s_3)-(r_2+r_3)],
 8 Delta [r_2r_3(s_2+s_3)+(r_2+r_3)].                            (6)
```

Suppose the pair image has rank at most three.  If `Delta` were nonzero, all
four bracketed factors in (6) would vanish.  Subtracting the first pair gives
`s_2+s_3=0`; subtracting the second gives `r_2+r_3=0`.  But then

```text
Delta=r_2(-s_2)-(-r_2)s_2=0,
```

a contradiction.  Therefore pair rank at most three forces `Delta=0`.

Under the theorem's rank-three hypothesis, (5) is then the unique relation.
Its coefficient matrix in the two marked row bases is

```text
[ 0  1]
[-1  0],
```

which has determinant one and rank two.  The requested rank-one third edge
cannot occur.

## Consequence and proof boundary

The coefficient-rank pattern `(2,2,1)` is absent from rank-three exceptional
triangles.  Together with the corrected `(2,2,2)` triangle classification,
this sharply restricts the remaining graph shapes, but mixed triangles with
only one rank-two edge and lower pair-rank boundary strata remain outside this
theorem.

The star carrying the same relation-rank multiset is not empty; it is now
constructed and completely classified in
[`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md`](P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md)
and
[`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md`](P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md).

The proof is symbolic and constant-size.  It enumerates Borel normal-form
types, not graph instances or finite fields.

## Verification

Run:

```text
python verify_p4_mixed_two_rank_two_triangle_obstruction.py
python audit_p4_mixed_two_rank_two_triangle_obstruction.py
```

The primary verifier reconstructs the synchronizer identities, the
annihilator boundary, all fifteen maximal minors in the last chart, the four
decisive factors, and the alternating coefficient rank.  The audit permutes
the source partition to `{0,2}|{1,3}` and rebuilds the matrices independently.
Both use exact polynomial arithmetic and no search.
