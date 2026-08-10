# Component twenty-five's global exceptional-weight opposite-diagonal divisor

## Status

**Exact characteristic-zero divisor classification.**  On component
twenty-five's normalized ordinary finite-`D01`, `B=0`, `N=0` sheet, away from
the already-separated `A_0A_2=0`, standing, chart, and linear-solve
boundaries, the complete zero locus of the opposite marked binary diagonal is

```text
N(a,b,lambda)=G(a,b,lambda)=0.                   (1)
```

Its image in the dimensionless component-parameter plane is the single
irreducible hypersurface `U(a,b)=0` displayed below.  Every point of (1) has
zero opposite binary diagonal and therefore is not a genuine shared binary
incidence.  Thus the global opposite-diagonal divisor on this ordinary sheet
cannot lift to weighted `H22`.

This result does **not** classify simultaneous paired-`D23` rank-minor zeros
on the genuine complement `G!=0`.  It does not treat retained standing or
projective boundaries, and it is not a counterexample.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact opposite diagonal

Retain the notation and open chart of
[`P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_BRANCH_B_FULL_FIELD_GENERIC_WEIGHT_OBSTRUCTION.md`](P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_BRANCH_B_FULL_FIELD_GENERIC_WEIGHT_OBSTRUCTION.md).
Normalize the already-nonzero scale `s` and put

```text
a=es,  b=js.
```

The primary verifier works first over the unspecialized field

```text
K=C(e,j,s)[k]/((ej+k^2)(1+ejs^2)-(e+j)^2).       (2)
```

It solves the two finite-`D01` Segre equations for `w,z_6`, imposes the
quadratic exceptional-weight equation

```text
N=A_2 lambda^2+A_1 lambda+A_0=0,                 (3)
```

and reconstructs and marks the binary projection.  With its first diagonal
normalized to one, the opposite diagonal is purely `k`-odd.  After setting
`s=1`, its nonzero basis coefficient is

```text
-b(lambda+1)(1+ab)G
-----------------------------------------------,
 2lambda(a+b)^2(lambda-1)D_0 T H

D_0=a^2b^2-a^2-ab-b^2,
T=b lambda-b-lambda-1,
H=ab lambda+ab-a lambda+a-b lambda+b+lambda+1.  (4)
```

All factors in (4) other than `G` are inverted on the retained ordinary
chart.  Write

```text
G=g_4 lambda^4+g_3 lambda^3+g_2 lambda^2+g_1 lambda+g_0,
```

where

```text
g_4=a^3(b-1)^2+a^2(-b^3+3b-2)-a(b-1)^2+b^3-3b+2,

g_3=2a^3b^2-2a^3+2a^2b^3+4a^2b^2-6a^2b
    -6ab^2+8ab-2a-2b^3-2b+4,

g_2=-6a^3b^2+2a^3-2a^2b^3-2a^2b
    +6ab^2-2a+2b^3+2b,

g_1=2a^3b^2-2a^3+2a^2b^3-4a^2b^2-6a^2b
    -6ab^2-8ab-2a-2b^3-2b-4,

g_0=a^3(b+1)^2+a^2(-b^3+3b+2)-a(b+1)^2+b^3-3b-2.  (5)
```

The exact reciprocal identity

```text
G(a,b,lambda)=-lambda^4 G(-a,-b,lambda^-1)       (6)
```

agrees with the previously certified `A_0`/`A_2` reciprocity, but the primary
derives (5) directly from the marked permanent rather than assuming that
symmetry.

## Complete parameter resultant

Exact elimination of `lambda` gives

```text
Res_lambda(N,G)
 =64a(a-b)^3(a+b)^5(a-1)(a+1)(b-1)^2(b+1)^2 U, (7)
```

with

```text
U = 5a^6b^5-5a^6b^3+a^6b
    -4a^5b^6+12a^5b^4-10a^5b^2+2a^5
    -a^4b^7-a^4b^5-2a^4b^3+a^4b
    +8a^3b^6-14a^3b^4+6a^3b^2
    +2a^2b^7-2a^2b^5+3a^2b^3
    -4ab^6+4ab^4-b^7.                            (8)
```

The primary and independent audit both verify that `U` is irreducible in
`Q[a,b]`.  The other factors in (7) are already separated:

- `a=0`, `a-b=0`, and `a+b=0` are respectively `e=0`, `e-j=0`, and `Q=0`;
- `a=+/-1` and `b=+/-1` lie on the linear factors already handled in the
  `A_0=0` and `A_2=0` packages or on their standing boundaries.

Consequently, away from those factors, (7) proves that a common root of
`N` and `G` exists exactly over `U=0`.  This is a classification of the
opposite-diagonal failure locus, not a claim that both roots of `N` fail over
every point of `U`.

## Why this is an obstruction

On `N=0`, the finite-`D01` construction has all fourteen mixed marked binary
coefficients equal to zero.  A genuine shared binary incidence requires both
diagonals to be nonzero.  Equation (4) shows that every point of (1) has the
second diagonal equal to zero.  Such a point is therefore nongenuine before
any paired-`D23` rank test is needed.

The remaining component-twenty-five ordinary frontier is the simultaneous
rank-at-most-three locus of the four paired-`D23` one-marked maps on

```text
N=0,  G!=0,  A_0A_2!=0,                          (9)
```

plus the explicitly retained denominator and projective boundaries.

## Replay

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_opposite_diagonal_divisor.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_opposite_diagonal_divisor.py
```

The primary reconstructs the unspecialized full-quadratic-field section and
derives `G` from the marked permanent.  The no-import audit recomputes (7) as
the determinant of the explicit `6 x 6` Sylvester matrix, without calling a
resultant routine.  Both use exact characteristic-zero arithmetic.  No
finite-field evidence is used.
