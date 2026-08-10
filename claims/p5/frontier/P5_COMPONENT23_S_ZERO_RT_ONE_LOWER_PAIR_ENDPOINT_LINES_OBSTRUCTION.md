# Component twenty-three `s=0, rt=1` lower-pair endpoint-line obstructions

## Status

**Exact characteristic-zero normalized-line theorem.**  On component
twenty-three's projective parameter face

```text
s=0,       rt=1,
```

the two finite-`k` lower-pair endpoint lines

```text
r=t=+1, k arbitrary,       r=t=-1, k arbitrary
```

have empty complete affine-marked `H31` fibre and empty complete
homogeneous-weight `H22` fibre in the fixed normalized contraction order.
The calculation includes `k=0`, every finite weight, and projective weight.
Everything is over `Q`; no finite-field evidence is used.

This does not cover arbitrary ambient or source bases, other projective
component charts, arbitrary contraction order, or the local-to-global
reduction.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact tangent lower-pair placement

Put

```text
A=X0+X1,   C=X0-X1,   B=X2+X3,   D=X2-X3.
```

For `epsilon=+1,-1`, the endpoint rows are

```text
alpha=(A,A+kD,B+epsilon D,B+epsilon D),
beta =(B,B,   C,          C).                       (1)
```

Only `T_1111=-4` is nonzero.  For `k!=0`, the pair profile in edge
order `01,02,03,12,13,23` is

```text
(3,3,3,4,4,2).                                     (2)
```

At `k=0` it drops further to

```text
(3,3,3,3,3,2).                                     (3)
```

Unlike the `k=infinity` endpoint points, the rank-two edge here is tangent,
not secant.  Set

```text
e=(B+epsilon D)/2,   Z=(B-epsilon D)/2,
H=C,                 S=A.
```

After mode order `(2,3,0,1)`, the four planes are

```text
span(e,H),
span(e,H),
span(S,e+Z),
span(S+2 epsilon k e,e+Z).                          (4)
```

The kernel line on the first edge meets the Segre quadric in the double
support-one point `e tensor e`: in a kernel basis its determinant is a
nonzero square.  The opposite planes have the same isotropic quotient line,
and the first meets the radical in the distinguished annihilator `S`.
Thus (4) is the projective support-two tangent polar-flag boundary of the
known six-dimensional lower-pair component.  For `k!=0`, after the shear
`Z'=e+Z`, its other radical line is

```text
e+(2 epsilon k)^(-1)S;
```

`k=0` is the further projective endpoint of this same boundary line.

Replacing any `beta_i` by the omitted projective marking `alpha_i` makes
the inherited pure coefficient zero.  Since each displayed plane has rank
two, every genuine marked basis is therefore represented by

```text
beta_i -> beta_i+h_i alpha_i.                       (5)
```

## Complete marked `H31` fibre

For source-coordinate deletion `d`, let `M_d(h)` be the fourteen mixed
binary equations in the eight extension entries, and normalize the two
binary diagonals by `A_d=1`, `B_d!=0`.  Exact elimination over
`Q[k,h0,h1,h2,h3]` gives the unit ideal for seven of the eight signed
deletions.  The only nonunit projections are

```text
epsilon=+1, d=3:  <h0,h1,h2 h3>,
epsilon=-1, d=2:  <h0,h1,h2 h3>.                   (6)
```

Both inclusions are checked, so (6) has exactly two marking lines and no
hidden sheet.

### The punctured marking lines

On either line write its nonzero marking coordinate as `p`.  The mixed
matrix has rank four and nullity four.  In the exact nullspace basis used by
the verifiers, with extension `c0 K0+...+c3 K3`, the diagonals are

```text
A=4(c0 p-c3)/p,       B=-2(c1+c2).                  (7)
```

For mode `2` on `h2=0`, or mode `3` on `h3=0`, the four minors on rows

```text
0127, 0137, 0147, 0157
```

are the common genuine factor

```text
16(c1+c2)(c0 p-c3)                                  (8)
```

times

```text
c0+2c2,   2c2 p+c3,   c0+2c1,   2c1 p+c3.          (9)
```

If all four factors in (9) vanished, then `c0 p-c3=0`; hence `A=0`.
Every genuine binary extension therefore has a rank-four marked map and
cannot lift to `H31`.

### Their intersection for `k!=0`

At `h2=h3=0`, the diagonals become

```text
A=4(c0+c1),       B=-2(c2+c3).                     (10)
```

Four mode-zero minors are, up to their displayed nonzero scalar and powers
of `k`, the common factor `(c0+c1)(c2+c3)` times

```text
c0-2c2,   c1-2c2,   c0+2c3,   c1+2c3.              (11)
```

For `epsilon=+1` they are

```text
-16 k^2 AB' (c0-2c2),   -16 k^2 AB' (c1-2c2),
 16 k   AB' (c0+2c3),    16 k   AB' (c1+2c3),       (12)
```

where `AB'=(c0+c1)(c2+c3)`; the last two signs reverse for
`epsilon=-1`.  Vanishing of all four residual factors forces `c2+c3=0`,
contradicting `B!=0`.  This closes the intersection when `k!=0`.

### The `k=0` corner

This corner needs a structural argument rather than specialization of
(12).  Let `(u0,u1,uc,u4)` be a candidate pure-colour source row on the
three common source coordinates and the fifth coordinate.  On the genuine
open `(c0+c1)(c2+c3)!=0`, annihilating all alpha/beta coefficients first
forces

```text
u1=-u0.                                             (13)
```

If all three common coefficients `u0,u1,uc` are nonzero, the next two
coefficient rows force

```text
c0=c1=-(c2+c3).                                     (14)
```

Outside (14), a support-three `H31` row is already impossible.  On (14),
scale the fifth source coordinate so `c2+c3=1`, put `c2=tau`, and write the
only possible support-three row as

```text
(a,-a,b,-b/2),       a b!=0.                        (15)
```

At mode `2` for `epsilon=+1`, and mode `3` for `epsilon=-1`, the complete
one-gamma coefficient map has rank three.  Rows `027` and columns `023`
give respectively

```text
-16 a b^2,       +16 a b^2.                        (16)
```

The existing alpha and beta rows lie in its kernel and are independent.
Thus its two-dimensional kernel is exactly the marked plane: no third local
row can be independent.  This closes the final `k=0` corner and completes
the marked `H31` line theorem.

## Complete homogeneous weighted `H22` fibre

Use the two labelled contractions `D01` and `D23` with a shared extension.
The inherited pure coefficient is the all-beta word, so genuineness requires

```text
B01 B23 !=0,       and at least one of A01,A23 is nonzero.   (17)
```

On the finite weight chart `[lambda:1]`, exact module reduction over

```text
Q[k,h0,h1,h2,h3,lambda]
```

puts `A01` in the shared mixed-row module for both signs.  Therefore a
genuine point must have `A23!=0`.  Normalize `A23=1` and saturate by
`B01 B23`.  The ideal generated by all twenty-eight shared mixed equations,

```text
A23-1,       w B01 B23-1,                           (18)
```

is the unit ideal for each sign.  This closes every finite weight at once,
including `lambda=0,+1,-1`, with arbitrary `k` and marking.

On the projective weight chart, all four diagonals

```text
(A01,A23,B01,B23)
```

belong to the exact shared mixed module over `Q[k,h0,h1,h2,h3]` for both
signs.  Hence projective weight is empty as well.

## Replay

```powershell
uv run --with sympy python verify_p5_component23_s_zero_rt_one_lower_pair_endpoint_lines_obstruction.py
uv run --with sympy python audit_p5_component23_s_zero_rt_one_lower_pair_endpoint_lines_obstruction.py
```

The primary reconstructs the tangent placement, all eight exact `H31`
projections, every surviving rank certificate, and both homogeneous `H22`
charts.  The audit imports no project code and independently rebuilds the
permanents, contractions, elimination ideals, modules, and minors.  Neither
uses a finite field.
