# Component twenty-three's two `s=1` parameter-infinity obstructions

## Status

**Exact characteristic-zero normalized-boundary theorem.**  On the `s=1`
chart of component twenty-three, the two replacement divisors obtained at
`r=infinity` and `t=infinity` have empty complete affine-marked `H31` fibre
and empty complete homogeneous-weight `H22` fibre for the fixed normalized
contraction order.  This holds at every finite value of the remaining
parameter, including `k=0,+1,-1`.

The simultaneous triple-parameter direction in which this remaining `k`
also tends to infinity is not a point of either replacement chart used here.
It requires an additional blowup chart and is not included.  Nor does this
theorem cover arbitrary source or ambient bases, arbitrary contraction order,
the local-to-global reduction, or the global Krenn--Gu conjecture, which
remains **UNRESOLVED**.

## The two pure curves

Put

```text
A=(1,1,0,0),  C=(1,-1,0,0),
B=(0,0,1,1),  D=(0,0,1,-1).
```

The `r=infinity` replacement curve `Dr` has rows

```text
alpha=(A,A+kD,D,-A-C+B+kD),
beta =(B,B+C,C,C),                                      (1r)
```

and the `t=infinity` replacement curve `Dt` has rows

```text
alpha=(A,A+kD,A-C+B-kD,D),
beta =(B,B+C,C,C).                                      (1t)
```

On both curves every permanent coefficient vanishes except
`T1111=-4`.  In edge order `01,02,03,12,13,23`, their generic pair profiles
are respectively

```text
Dr: (3,2,3,3,4,4),       Dt: (3,3,2,4,3,4).            (2)
```

The persistent rank-two edge has two decomposable kernel columns with
disjoint zero-product supports `{0,1}` and `{2,3}`.  Thus these are
disjoint-secant lower-pair curves.  On `Dr`, the gcd of the maximal minors
of edge `13` is `8k(k-1)(k+1)`; on `Dt` the same gcd occurs on edge `12`.
At each of `k=0,+1,-1`, the corresponding rank-four edge drops to rank
three, giving profiles

```text
Dr: (3,2,3,3,3,4),       Dt: (3,3,2,3,3,4).            (3)
```

These special intersections are retained in every calculation below.

## Exact involution

The source involution

```text
J(v0,v1,v2,v3)=(-v1,-v0,v3,v2)                        (4)
```

followed by the mode order `(0,1,3,2)` sends (1r) to (1t).  In the displayed
replacement bases, the alpha rows acquire factors `(-1,-1,+1,-1)` and the
beta rows acquire no factors.  Hence

```text
(h0,h1,h2,h3) -> (-h0,-h1,h3,-h2),
(d0,d1,d2,d3) -> (d1,d0,d3,d2).                       (5)
```

Both contracted source covectors transform exactly by

```text
[lambda:1] -> [1:lambda]                              (6)
```

for `D01` and `D23`; zero and projective weight are exchanged.  Equations
(4)--(6), including their row factors, are checked before the `Dr` marked
classification is transferred to `Dt`.  The weighted calculation below is
also replayed directly on both curves.

## Complete marked-`H31` classification on `Dr`

Every marked basis is represented uniquely up to the usual rescaling by

```text
beta_i -> beta_i+h_i alpha_i.                          (7)
```

The omitted projective point has second row proportional to `alpha_i` and
is not a basis.  For deletion `d`, normalize the first binary diagonal to
one and invert the second.  Eliminating the eight extension entries gives
the following exact projected ideals in `Q[k,h0,h1,h2,h3]`:

```text
d=0,1: <h3,h1-1,h0,(k^2-1)h2>,
d=2:   <h2-h3,h1-1,h0,h3(h3-1),h3(k-1)>,
d=3:   <h2+h3,h1-1,h0,h3(h3-1),h3(k+1)>.             (8)
```

Thus the complete survivor list is:

- the section `(h0,h1,h2,h3)=(0,1,0,0)` for all four deletions;
- at `k=+1` and `k=-1`, the families `(0,1,z,0)` for deletions zero and one;
- the extra point `(k,d,h)=(1,2,(0,1,1,1))`;
- the extra point `(k,d,h)=(-1,3,(0,1,-1,1))`.

There is one closure subtlety in (8).  At `k=0`, deletions zero and one have
no genuine binary extension at all: direct specialization before
elimination gives the unit ideal.  They appear in (8) only as non-proper
projection-limit points.  For the generic section, those two deletions are
therefore used only on `k!=0`; deletions two and three remain genuine at
`k=0`.

## Uniform global one-marked obstruction

For every actual branch in the list above, the mixed binary matrix has rank
six and the verifier supplies its complete two-vector kernel frame.  Let
`A_d` denote the normalized first binary diagonal.  Embed the pure
one-marked map and the neighbouring one-marked map in the common
five-dimensional source, and stack them.  For target mode one, rows

```text
0,6,7,8,14                                               (9)
```

give a five-by-five determinant equal to `+32 A_d` for deletion zero and
`-32 A_d` for deletions one, two, and three.  The same identity holds on
both nonzero-`z` marking families and at both isolated extra points.  Since
a genuine binary extension has `A_d!=0`, (9) has rank five.  The third row
at mode one must therefore vanish simultaneously on the pure and
neighbouring hyperplanes, hence globally.  It cannot complete a rank-three
local map.  This proves

```text
marked H31 fibre(Dr)=marked H31 fibre(Dt)=empty.       (10)
```

In particular, at `k=0` the surviving deletion-two and deletion-three
binary kernels really do have neighbour-only rank-three one-marked maps;
the stacked determinant (9), not a generic rank-four shortcut, is what
closes them.

## Every homogeneous `H22` weight

For each curve and marking (7), combine the fourteen mixed `D01` rows and
the fourteen mixed `D23` rows in their shared eight extension variables.
The primary and independent audit compare the exact row module with an
explicit normal form in every case below.  Diagonals are ordered

```text
(A01,B01,A23,B23).                                    (11)
```

On the finite chart, if `lambda^2!=1`, the mixed module is the full
coordinate module, uniformly in `k` and the markings.  At `lambda=1` and
`k!=0`, membership is

```text
(no,yes,yes,no),                                      (12)
```

while at `lambda=1,k=0` it is

```text
(yes,yes,yes,no).                                     (13)
```

At `lambda=-1`, for every `k`, membership is

```text
(yes,no,no,yes).                                      (14)
```

Finally, at projective weight the mixed module is the full coordinate
module.  A genuine weighted lift requires both beta diagonals `B01,B23` to
be nonzero.  Equations (12)--(14) put one of these required beta diagonals
in the mixed module, and the full-module cases kill the entire shared
kernel.  Therefore

```text
weighted H22 fibre(Dr)=weighted H22 fibre(Dt)=empty.  (15)
```

No weight, marking, or special `k` value is omitted, and no finite-field
calculation is used.

## Replay

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component23_s_one_parameter_infinity_curves_obstruction.py
uv run --with sympy python claims/p5/frontier/audit_p5_component23_s_one_parameter_infinity_curves_obstruction.py
```

The primary uses the repository permanent and contraction builders.  The
audit has no repository imports: it independently rebuilds the permanents,
pair matrices, marked binary projections, stacked one-marked maps, and
weighted contraction modules over characteristic zero.
