# Generic marked `H31` obstruction on component twenty-four

## Status

**Exact characteristic-zero function-field theorem.**  The complete generic
marked `H31` fibre of the split-center mixed-star component (component
twenty-four) is empty.  One deletion is excluded by a row-module identity;
the other three project to four marking branches, and the same fixed
one-marked rank-four minor excludes every saturated extension on each branch.

This is a theorem over the generic point of the component.  Subsequent exact
work closes the generic weighted `H22` fibre and the remaining
star-`(2,1,1)` support strata.  Special/projective parameter fibres and the
arbitrary-order local-to-global step remain open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Generic pure basis

Use the `epsilon=1`, `h=1` chart of
[`P4_SPLIT_CENTER_MIXED_STAR_211_COMPONENT.md`](P4_SPLIT_CENTER_MIXED_STAR_211_COMPONENT.md)
over `K=C(k,s,t)`.  Put

```text
c=(t-ks)/(1-kst),

alpha=(A,
       A+kD,
       A+cC+kB-kD,
       D),

beta =(B,
       B+sC,
       C,
       tA+C-ktB).                                  (1)
```

The only nonzero pure coefficient is

```text
T_1111=4(kst-1).                                   (2)
```

Mark the active rows by

```text
beta_i -> beta_i+h_i alpha_i.                      (3)
```

For a distinguished source coordinate `q`, let `M_q` be the `14 x 8`
mixed-coefficient matrix of the projected binary extension, and let `d_0`
and `d_1` be its two diagonal rows.  Necessary binary incidence is the
saturation

```text
M_q z=0,       d_0 z=1,       u(d_1 z)=1.          (4)
```

## Exact marking projection

For `q=2`, exact row reduction over `K[h_0,h_1,h_2,h_3]` gives a standard
row module of size eight with

```text
d_0 in rowspan(M_2),       d_1 not in rowspan(M_2). (5)
```

Thus (4) is impossible for every marking in that deletion.

For the other three deletions, eliminate `z,u` from (4).  The exact projected
ideals are

```text
q=0: <h3-kt, h2,
      k(t+1)h1-2kst-t+1, h0>,

q=1: <h3-kt, h2,
      k(t-1)h1+2kst-t-1, h0>,                      (6)

q=3: <h3-kt,
      k(kst-1)h1+2t(k^2s^2-1)h2+kst-1,
      h0,
      2t(k^2s^2-1)h2^2+(k^2s^2t^2-1)h2>.
```

The first two ideals are prime marking points.  The last ideal is radical
and is exactly the intersection of

```text
P_3a=<h3-kt,h2,kh1+1,h0>,

P_3b=<h3-kt,
      2t(k^2s^2-1)h2+k^2s^2t^2-1,
      h1-st,h0>.                                   (7)
```

Therefore the full generic marking scheme consists of the four branches

```text
q0:  h=(0,(2kst+t-1)/(k(t+1)),0,kt),
q1:  h=(0,(t+1-2kst)/(k(t-1)),0,kt),
q3a: h=(0,-1/k,0,kt),
q3b: h=(0,st,-(k^2s^2t^2-1)/(2t(k^2s^2-1)),kt).   (8)
```

All denominators in (8) are nonzero elements of the generic coefficient
field.  No special divisor is silently claimed.

## Fixed-minor obstruction

Let `N_0` be the `8 x 4` one-marked ternary map in mode zero after inserting
the projected extension.  On each branch in (8), adjoin to (4) the fixed
minor

```text
det N_0[0,1,3,7].                                  (9)
```

Each of the four exact ideals over `K[z_0,...,z_7,u]` is the unit ideal.
Consequently every saturated binary extension makes (9) nonzero and has
one-marked rank four.  It cannot lift to a marked `H31` restriction.

Combining (5)--(9) excludes all four distinguished coordinates and proves
the theorem.

## Replay

```text
uv run --with sympy python verify_p5_h31_split_center_mixed_star_component_generic_obstruction.py
uv run --with sympy python audit_p5_h31_split_center_mixed_star_component_generic_obstruction.py
```

The primary verifier computes the function-field row module, all three exact
projections, the radical two-prime intersection, and all four unit ideals.
The independent audit rebuilds the permanent/extension matrices without
importing the primary and repeats the projections and unit ideals at two
rational parameter points.  Those specializations audit the exact generic
proof; they do not replace it.  No finite-field computation is used.
