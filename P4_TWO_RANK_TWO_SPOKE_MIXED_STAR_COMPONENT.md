# A tenth pure `P_4` component from a `(2,2,1)` mixed star

## Status

**Exact characteristic-zero component theorem.**  The pure-compression locus
for four two-planes has a generically smooth, rational, five-dimensional
irreducible component whose exceptional graph is a star.  The unique
relations on its three spokes have coefficient-matrix ranks

```text
(2,2,1).                                                        (1)
```

All three leaf-pair images have full rank four.  This is the mixed-star shape
left open by the corrected triangle and rank-two-star theorems.  The relation
rank multiset separates it from the seven previously known five-dimensional
component orbits; dimension separates it from the two known six-dimensional
orbits.  The certified lower bound is therefore at least ten symmetry-
inequivalent pure-`P_4` component orbits.

This is a `P_4` plane-level component theorem, not a graph satisfying the
global Krenn--Gu prize conditions and not a proof of component exhaustiveness.

![Exceptional graph of the new mixed-star component](research_figures/p4_two_rank_two_spoke_mixed_star.png)

## Presymplectic construction

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Put

```text
a     =X_0+X_1,       a_bar=X_0-X_1,
b     =X_2+X_3,       b_bar=X_2-X_3.
```

For parameters `s,t`, define the four marked planes

```text
U_0=span(a+b, b),

U_1=span(a+b-b_bar-s a_bar, b-s a_bar),
U_2=span(a+b+b_bar-t a_bar, b-t a_bar),

U_3=span(
 b_bar,
 (s+t-1-st, s+t+1+st, -s-t, -s-t)).              (2)
```

The first three planes are the full-support `2+2` synchronizer chart.  Its
commutator is a degenerate alternating form; `U_0` is the radical, while the
two leaf parameters have symplectic determinant `s+t`.  Thus `s+t!=0` makes
the two synchronized leaves transverse rather than mutually exceptional.

The third spoke is the rank-one zero product

```text
b b_bar=0.                                                    (3)
```

This pins the last pure kernel to one binary block.  The squarefree permanent
then collapses to

```text
T_1111=-4(s+t),                                               (4)
```

with all other fifteen coefficients zero.  Hence (2) is a nonzero pure
restriction whenever `s+t!=0`.

## The hidden torus law

Before clearing denominators, the active row of `U_3` is determined by

```text
d=(1+st)/(s+t).                                               (5)
```

This is not an accidental rational expression.  Under the Cayley coordinate

```text
c(z)=(z-1)/(z+1),
```

one has exactly

```text
c(d)=c(s)c(t).                                                (6)
```

Thus purity is the multiplication graph of the algebraic torus `G_m` in
Cayley coordinates.  Equivalently, after scaling the last active row by
`(1+s)(1+t)`, it depends on the product `c(s)c(t)` through

```text
(-2c(s)c(t), 2, c(s)c(t)-1, c(s)c(t)-1).
```

This toric translation explains the two-dimensional survivor and gives a
natural route to its projective boundary without eliminating the original
plane equations.

## Exact exceptional graph

Order pair edges lexicographically as

```text
01,02,03,12,13,23.
```

On the dense open set

```text
st(s^2-1)(t^2-1)(s+t) != 0,
```

the pair-image profile is

```text
(3,3,3,4,4,4).                                               (7)
```

The relations on the three center spokes are respectively

```text
y_0x_1-x_0y_1=0,
y_0x_2-x_0y_2=0,
x_0y_3=0.                                                     (8)
```

Their coefficient matrices have ranks `2,2,1`.  Exact minors proving (7)
include

```text
4s,
4t,
4(s-1)(s+t)(t-1),
8(s+t)^2,
-8s(s-1)(s+1)(s+t)(t-1),
-8t(s-1)(s+t)(t-1)(t+1).                                    (9)
```

At the rational point `(s,t)=(2,3)`, all factors in (9) are nonzero.

## Five-dimensional component certificate

Apply the projective diagonal source torus

```text
diag(q_0,q_1,q_2,1)
```

and use the `(02)` Grassmann chart for all four planes.  At

```text
(s,t,q_0,q_1,q_2)=(2,3,1,1,1),                              (10)
```

the sixteen chart coordinates are

```text
(1,0,0,1,  -3,-2,-4,-3,  -1/2,-1/2,3/2,-1/2,  -6,5,0,-1).
```

Chart-coordinate rows `(0,3,4,5,8)` of the five-parameter Jacobian have
determinant

```text
-1/2.                                                        (11)
```

The irreducible family closure therefore has dimension five.

For the independent local upper bound, adjoin the unique Segre factor point
of the nonzero restricted tensor.  In the row-reduced chart, use anchor
`0100`; the four factor ratios are

```text
(-1,0,1,0).                                                  (12)
```

The fifteen universal Segre-incidence equations have a `15 x 15` Jacobian
minor on columns

```text
(0,1,2,3,4,5,6,7,8,9,10,11,14,17,19)
```

with determinant

```text
345600000.                                                   (13)
```

Hence the incidence locus is smooth of dimension five at (10).  The
five-dimensional irreducible family passes through that point, so its closure
is the unique local irreducible component.  A nonzero pure tensor has a unique
projective Segre factor point; forgetting it preserves the local component.

## Distinctness and proof boundary

The seven previously certified fivefolds have, on their rank-three
exceptional edges, either three coefficient-rank-one relations or two
rank-one relations and one rank-two relation.  The new multiset

```text
{1,2,2}
```

is invariant under mode/source symmetries and row-basis changes and is new.
The two other certified components are six-dimensional and have lower pair-
rank profiles.  Thus this is a tenth component orbit.

The result settles one mixed-star stratum by construction.  Stars with a
different number/orientation of rank-two spokes, triangles with exactly one
rank-two edge, special divisors of (2), and the rest of the lower pair-rank
boundary still require classification.  No global Krenn--Gu conclusion is
claimed.

## Verification

Run:

```text
uv run --with sympy python verify_p4_two_rank_two_spoke_mixed_star_component.py
uv run --with sympy python audit_p4_two_rank_two_spoke_mixed_star_component.py
```

The primary verifier checks (4)--(13) over the rationals.  The audit permutes
the source coordinates to `(1,0,3,2)`, uses the crossed `(13)` Grassmann
chart, and reconstructs the permanent by subset dynamic programming.  Both
are constant-size exact symbolic replays, not searches.
