# Component twenty-three's `s=1` triple-parameter infinity corner

## Status

**Exact characteristic-zero normalized-corner theorem.**  In the natural
multi-projective compactification of component twenty-three's `s=1` purity
surface, the simultaneous intersection

```text
k=infinity,       r=infinity,       t=infinity
```

is one smooth point, not an exceptional family of limiting directions.  At
that point the complete affine-marked `H31` fibre and complete homogeneous-
weight `H22` fibre are empty for the fixed normalized contraction order.

This concerns the displayed component chart and fixed source order only.  It
does not prove invariance under arbitrary ambient or source changes,
arbitrary contraction order, or the local-to-global reduction.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## The compactification point

Put

```text
A=(1,1,0,0),  C=(1,-1,0,0),
B=(0,0,1,1),  D=(0,0,1,-1).
```

On `s=1`, component twenty-three is given by

```text
1-r*t=k*(t-r).                                      (1)
```

In reciprocal coordinates

```text
q=1/k,       u=1/r,       v=1/t,
```

the exact closure of (1) is

```text
q*u*v-q-u+v=0.                                     (2)
```

The gradient of (2) at `(q,u,v)=(0,0,0)` is `(-1,-1,1)`.  Hence the triple
divisor intersection is a single smooth point of this compactification;
there is no blowup direction parameter hidden there.

After rescaling the first row of each diverging plane, the family extends
regularly as

```text
alpha=(A, q*A+D, u*(A-C+B)+D, v*(-A-C+B)+D),
beta =(B, B+C,   C,             C).                (3)
```

Every displayed plane remains two-dimensional at the origin, so (3) is a
regular Grassmannian chart there.  Its unique corner value is

```text
alpha=(A,D,D,D),        beta=(B,B+C,C,C).          (4)
```

Direct permanent expansion gives only `T1111=-4`.  In edge order
`01,02,03,12,13,23`, the pair profile is

```text
(3,2,2,3,3,3).                                    (5)
```

Thus (4) is a nonzero two-lower-pair intersection point in the closure of
component twenty-three.

## Complete marked-`H31` fibre

Every genuine marked basis is represented by

```text
beta_i -> beta_i+h_i*alpha_i.                      (6)
```

The omitted projective marking makes the two rows proportional and is not a
basis.  For source deletion `d`, normalize the first binary diagonal and
invert the second before eliminating the eight extension entries.  Exact
elimination gives

```text
d=0,1: <h0,h2*h3,h1*h3,h1*h2>,
d=2,3: <1>.                                        (7)
```

Consequently the complete survivor over either deletion zero or one is the
origin together with the three coordinate axes in `(h1,h2,h3)`.  The
verifiers treat the origin and each punctured axis separately; no division
by an axis parameter is used at the origin.

On every survivor the mixed binary matrix has rank six and a displayed
two-vector kernel frame.  Embed the pure and neighbouring one-marked maps in
their common five-dimensional source and stack them.  For target mode zero,
rows

```text
1,3,7,8,9                                             (8)
```

give determinant

```text
d=0: -32*A_d,             d=1: +32*A_d,             (9)
```

where `A_d` is the first binary diagonal evaluated on the extension.  A
genuine binary extension has `A_d!=0`; therefore the stacked map has rank
five and the third target row at mode zero must vanish globally.  It cannot
complete a rank-three local map.  Together with the unit ideals for
deletions two and three, this proves

```text
marked H31 fibre((4))=empty.                        (10)
```

## Complete weighted-`H22` fibre

For a common finite homogeneous weight `[lambda:1]`, combine the fourteen
mixed `D01` rows and fourteen mixed `D23` rows in their shared eight
extension variables.  Over `Q[h0,h1,h2,h3,lambda]`, the exact row module is

```text
< e1,e3,e4,
  (lambda+1)e2,(lambda-1)e5,
  (lambda+1)e6,(lambda+1)e7,(lambda+1)e8 >.         (11)
```

Both module inclusions are checked.  In diagonal order

```text
(A01,B01,A23,B23),
```

membership is

```text
(yes,no,yes,no).                                    (12)
```

Thus both alpha diagonals vanish on every common mixed-kernel vector.  A
genuine paired weighted lift requires both beta diagonals to be nonzero and
at least one alpha diagonal to be nonzero, so (12) obstructs every finite
weight, including `lambda=+1,-1`.

At projective weight the mixed module is the full coordinate module
`Q[h]^8`, so its common kernel is zero.  Therefore

```text
weighted H22 fibre((4))=empty.                      (13)
```

No finite-field calculation is used.

## Replay

```powershell
uv run --with sympy python verify_p5_component23_s_one_triple_parameter_infinity_corner_obstruction.py
uv run --with sympy python audit_p5_component23_s_one_triple_parameter_infinity_corner_obstruction.py
```

The primary uses the repository permanent and contraction builders.  The
audit imports no repository code: it independently reconstructs the
compactification, permanent tensors, pair matrices, saturated marked
projections, kernel frames, stacked maps, and weighted modules over
characteristic zero.
