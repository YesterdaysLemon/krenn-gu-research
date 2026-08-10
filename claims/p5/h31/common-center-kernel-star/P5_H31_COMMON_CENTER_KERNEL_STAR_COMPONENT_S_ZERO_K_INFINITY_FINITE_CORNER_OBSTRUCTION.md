# Marked-`H31` obstruction on component twenty-three's finite `s=0,k=infinity` corner

## Status

**Exact characteristic-zero normalized-corner theorem.**  On component
twenty-three, impose `s=0` and pass to the reciprocal `k` chart.  On the
corner `k=infinity`, every point with finite affine parameters `(r,t)` has
empty marked-`H31` fibre, for the fixed normalized source order used below.
The assertion covers every marked basis, all four source-coordinate
insertion positions, and every projective extension direction.

This is not a theorem on the whole projective `(r,t)` surface.  The charts
`r=infinity`, `t=infinity`, and `(r,t)=(infinity,infinity)` are not covered.
Arbitrary source or ambient changes, other source orders, arbitrary-order
gluing, and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Corner rows and pair strata

Put

```text
A=(1,1,0,0),   C=(1,-1,0,0),
B=(0,0,1,1),   D=(0,0,1,-1).
```

The finite corner rows are

```text
alpha=(A,D,B+rD,B+tD),
beta =(B,B,C,C).                                      (1)
```

All tensor coefficients vanish except `T1111=-4`.  In edge order
`01,02,03,12,13,23`, the generic pair profile is

```text
(3,3,3,3,3,4),                                      (2)
```

and the gcd of the nonzero maximal minors on edge `23` is

```text
8(r-t)(rt-1).                                       (3)
```

Away from their intersections, both divisors `r=t` and `rt=1` therefore
have all-rank-three profile `(3,3,3,3,3,3)`.  Their two common points
`(r,t)=(1,1),(-1,-1)` have lower-pair profile `(3,3,3,3,3,2)`.  The proof
below treats the generic surface, both divisors, their endpoints, the
coordinate lines, and the non-flat antidiagonal separately.

## Complete marking and exact incidence projection

Every marked basis whose first row is `alpha_i` has a unique affine form

```text
beta_i(h)=beta_i+h_i alpha_i.                        (4)
```

The omitted projective value makes the second row proportional to the first
and is not a basis.  For insertion position `d`, write
`z=(x0,x1,x2,x3;y0,y1,y2,y3)^T` for the extension column.  Let `M_d(h)` be
the fourteen mixed equations and let `a_d z,b_d z` be the two diagonal
coefficients.  A genuine binary neighbour satisfies

```text
M_d(h)z=0,             (a_d z)(b_d z)!=0.            (5)
```

Normalizing `a_d z=1` and inverting `b_d z` is complete on the projective
open (5).  Exact elimination gives `<1>` for `d=2,3` over the whole finite
`(r,t)` plane.  The projections for `d=0,1` are identical.

On `(r-t)(r+t)!=0`, their ideal is exactly the intersection of the following
seven branch ideals (the displayed equations omit the common localization):

```text
C:    h0=h2=h3=0,       (r+t)h1=rt+1;
B20:  r=0, h0=h3=0,     t h1=1;
B2+:  t=1, h0=h3=0,     h1=1;
B2-:  t=-1,h0=h3=0,     h1=-1;
B30:  t=0, h0=h2=0,     r h1=1;
B3+:  r=1, h0=h2=0,     h1=1;
B3-:  r=-1,h0=h2=0,     h1=-1.                      (6)
```

In particular, at `(r,t)=(0,2)` the complete incidence branch is
`h=(0,1/2,g,0)`; it is not a marked-`H31` survivor.

The remaining parameter strata are:

```text
t=-r, r!=0:                 unit ideal;
r=t, r(r^2-1)!=0:           Cdiag intersect B2diag intersect B3diag;
Cdiag:                       h0=h2=h3=0, h1 arbitrary;
B2diag:                      h0=h3=0, r h1=1;
B3diag:                      h0=h2=0, r h1=1;
r=t=0:                       unit ideal;
r=t=epsilon, epsilon=+/-1:  h0=0, h1=epsilon, h2 h3=0.             (7)
```

Every equality in (6)--(7) is checked in both ideal-containment directions.
The unit statement on the antidiagonal is essential: merely specializing
the closure of `C` would create false points at `(1,-1)` and `(-1,1)`.

## Uniform ternary obstruction

For every branch in (6)--(7), the primary replay supplies a complete frame
of `ker M_d`.  Away from the two lower-pair endpoints the mixed rank is six
and the kernel dimension is two.  At the endpoints it is five and the
kernel dimension is three.  Fixed maximal minors certify these ranks on the
stated localized bases; on `C` two minors cover the entire
`(r-t)(r+t)!=0` base.

Writing an extension in its displayed frame, the replay verifies a fixed
four-by-four minor of the neighbouring one-marked map.  On every branch it
is a unit multiple of either

```text
(a_d z)^2(b_d z)       or       (a_d z)(b_d z)^2.     (8)
```

Thus the one-marked map has rank four throughout the genuine-binary open
(5).  This includes the coordinate branch through `(0,2)`, where the exact
values are

```text
a_d z=2pt,
b_d z=+/-2(gp+2w),
minor=+/-8 p^2 t^2(gp+2w).                          (9)
```

At each endpoint the rank-five mixed kernel is handled directly, including
the central marking and both side branches `h2 h3=0`; its one-marked minor
is again a nonzero scalar multiple of (8).

Finally, a displayed entry of the pure mode-zero map is nonzero on every
surviving branch: it is one of `+/-2r`, `+/-2t`, or `+/-2` (and on the
diagonal `r` is a unit).  The standard transverse-coordinate argument first
forces the third target row to be supported only on the deleted source
coordinate and then forces its remaining entry to vanish.  This contradicts
the rank-three target map required by `H31`.  Consequently

```text
marked H31 fibre of (1), finite r,t=empty.           (10)
```

## Replay

```powershell
uv run --with sympy python verify_p5_h31_common_center_kernel_star_component_s_zero_k_infinity_finite_corner_obstruction.py
uv run --with sympy python audit_p5_h31_common_center_kernel_star_component_s_zero_k_infinity_finite_corner_obstruction.py
```

The primary verifier performs the characteristic-zero saturated
eliminations, both-way ideal comparisons, pair-rank checks, complete kernel
frames, rank certificates, diagonal identities, one-marked determinants,
and pure transverse checks.  The audit has no repository imports and
rebuilds the permanent tensors and all incidence matrices independently.  It
reverses the diagonal normalization in (5).  No finite-field calculation is
used.
