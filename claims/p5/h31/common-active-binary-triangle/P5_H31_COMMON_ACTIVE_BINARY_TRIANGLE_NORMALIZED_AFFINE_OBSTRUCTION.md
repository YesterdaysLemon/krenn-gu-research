# Normalized affine `H31` exclusion for component twenty

## Status

**Exact characteristic-zero normalized-affine theorem.**  On the complete
finite normalized common-active binary-triangle sheet

```text
(p+q)(p-q+1) != 0,
```

the marked `H31` fibre is empty.  The statement includes every intersection
of the special divisors inside this open; it is stronger than closing only
their generic points.

The proof is a fixed exact saturation and determinantal calculation over
`Q`.  Finite-field calculations in the independent audit are regression
checks only and are not used to infer the characteristic-zero theorem.

This does not resolve weighted `H22`, projective or source-torus limits, component
exhaustiveness, the arbitrary-order local-to-global step, or the global
Krenn--Gu conjecture.

## Intrinsic bases on the normalized open

Put

```text
s=p-q+1,                         D=(p+q)s,
e=(1,0,0,0).
```

Use the intrinsic rows

```text
alpha0=(0,-p(p+1),q(q-1),s),
alpha1=e,
alpha2=e,
alpha3=(1,1,1,0),

beta0=(-s,-p-q,p+q,0)+h0 alpha0,
beta1=(0,p+1,q-1,1)+h1 alpha1,
beta2=(0,p,q,1)+h2 alpha2,
beta3=e+h3 alpha3.                                      (1)
```

The condition `D!=0` makes every displayed pair a basis of its local plane.
Direct permanent expansion over `Q[p,q,h0,h1,h2,h3]` gives

```text
T_w=0 for w!=1111,             T_1111=2D.              (2)
```

Thus `(h0,h1,h2,h3)` covers every affine marked basis over each point of the
normalized open, up to harmless nonzero row scalings.

## Global genuine-binary incidence

For a distinguished source coordinate `d`, delete `d`, append an extension
column, and write

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3)^T.
```

Let `M_d(h)` be the `14 x 8` coefficient matrix of the mixed permanent
coefficients, and let `A_d(h),B_d(h)` be the all-`alpha` and all-`beta`
diagonal rows.  With inverse variables `w,u`, the exact open incidence is

```text
I_d=<M_d(h)z,
     A_d(h)z-1,
     w B_d(h)z-1,
     u(p+q)(p-q+1)-1>.                                (3)
```

The first normalization is projectively harmless and the two inverse
equations retain exactly the genuine binary and normalized-sheet opens.

Eliminating `(z,w,u)` from (3) gives the following exact marking projections.
For `d=0` the result is `<1>`.  For the next two deletions:

```text
J1=<h0,h3,h1 h2,
    (2q-1)(q h1+(q-1)h2+q(q-1)),
    h2(h2+q)(q-1)(2q-1)>,                            (4)

J2=<h0,h3,h1 h2,
    (2p+1)(p h1+(p+1)h2+p(p+1)),
    h2(h2+p)(p+1)(2p+1)>.                            (5)
```

Both ideals are radical.  Their exact prime decompositions are

```text
J1 = <h0,h3,h2,h1+q-1>
   intersection <h0,h3,h2,q>
   intersection <h0,h3,h2,2q-1>
   intersection <h0,h3,h1,2q-1>
   intersection <h0,h3,h1,h2+q>
   intersection <h0,h3,h1,q-1>,                    (6)

J2 = <h0,h3,h2,h1+p+1>
   intersection <h0,h3,h2,p>
   intersection <h0,h3,h2,2p+1>
   intersection <h0,h3,h1,2p+1>
   intersection <h0,h3,h1,h2+p>
   intersection <h0,h3,h1,p+1>.                    (7)
```

The exact primary decomposition for deletion three is

```text
J3 = <q,h2,h1-p-1,h0,h3>
   intersection <q-1,h2-p,h1,h0,h3>
   intersection <p-q,h2-q,h1,h0,h3>
   intersection <p-q+2,h2,h1-q+1,h0,h3>
   intersection <2pq-p+q,h2^2,h1-h2,h0,h3>
   intersection <p,h2,h1-q+1,h0,h3>
   intersection <p+1,h2-q,h1,h0,h3>.                (8)
```

Only the `2pq-p+q` component in (8) is nonreduced.  Its geometric marking is
`h1=h2=0`, while its projected scheme retains the transverse nilpotent
`h2^2` with `h1=h2`.  Eliminating the markings from (8) gives exactly

```text
<p(p+1)q(q-1)(p-q)(p-q+2)(2pq-p+q)>.                (9)
```

Equations (4)--(9) include the generic markings, the axes at `q=1/2` and
`p=-1/2`, the three deletion-three divisors, all four `p,q` degenerations,
and all of their intersections that remain inside `D!=0`.

## Uniform all-minor certificate

Let `N_3(d,h,z)` be the neighbouring mode-three one-marked map.  It has eight
rows, indexed by the mode-`0,1,2` words, and four source columns.  Instead of
choosing a different pivot minor on each stratum, impose all of its maximal
minors.  Exact Singular reduction gives

```text
I_d + I_4(N_3) = <1>             for d=0,1,2,3.      (10)
```

There are respectively `6,68,68,68` nonzero generated minors.  Consequently
every genuine incidence point in (3), including every special intersection,
has `rank N_3=4`.

Let `P_3(h)` be the pure mode-three one-marked map.  Exact reduction also
gives

```text
I_d + <all entries of the deleted column of P_3> = <1>
                                      for d=0,1,2,3. (11)
```

In fact the following fixed entries already have no common zero on `D!=0`:

```text
d=0:  2D,

d=1:  pq,                 (p+1)(q-1),

d=2: -pq,                -(p+1)(q-1),

d=3: -pq(p-q+2),         -(p+1)(p-q)(q-1).          (12)
```

This last assertion is checked as a unit ideal after adjoining `uD-1`; it
does not require the incidence equations.

## The `H31` contradiction

In a hypothetical `H31` lift, let `G_3` be the third target-coordinate row in
mode three.  The coefficients containing one `G_3` vanish on the binary
neighbour.  Equation (10) makes `N_3` injective, so `G_3` vanishes on the
neighbouring hyperplane and can be supported only on the deleted pure source
coordinate.  Equation (11), or the smaller certificate (12), kills that final
coefficient.  Hence `G_3=0`, contradicting target rank three.

Therefore

```text
marked H31 fibre(component 20, finite normalized D!=0 sheet)=empty. (13)
```

## Exact replay

```text
uv run --with sympy python \
  verify_p5_h31_common_active_binary_triangle_normalized_affine_obstruction.py

uv run --with sympy python \
  audit_p5_h31_common_active_binary_triangle_normalized_affine_obstruction.py
```

The primary verifier reconstructs (1)--(3), proves the projected ideals and
their exact decompositions, checks the deletion-three base factor, and proves
the unit ideals (10)--(12) over characteristic zero.  The audit reconstructs
the coefficient matrices by independent three-row permanent formulas and
replays the characteristic-zero ideal equalities without importing the
primary.  Its small finite-field sweep is labelled audit-only and makes no
characteristic-zero inference.

## Scope boundary

The inverse `uD-1` deliberately excludes `p+q=0` and `p-q+1=0`.  The latter
requires a replacement intrinsic basis because the two mode-zero rows in (1)
become dependent.  Also excluded are parameter infinity, omitted
source-torus and projective limits, the singleton sheet, weighted `H22`, the
remaining pure-`P_4` cells, arbitrary-order gluing, and the global conjecture.
