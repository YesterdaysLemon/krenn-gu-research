# Component twenty-two finite-D23 h1-nonzero two-minor factor cover

## Status

**Exact characteristic-zero second-cofactor partial obstruction.**  Work
over `K=Q(A,R,D)`, put `s=2*A+R`, and consider the finite-`D23` divisor

```text
2*A*h1+1=0,       rho*(rho+1)!=0.                  (1)
```

A fixed maximal mixed minor gives the exact rank-drop cover

```text
h2*f2*f7*f8*U*V=0.                                (2)
```

where

```text
f2=s*h2+1,                  f3=2*h3-s,
f6=(D-1)*rho+D+1,
f7=(A*D+A+R)*rho+A*D-A-R,
f8=(A*D+A+R*D)*rho+A*D-A+R*D,
U=2*h0*f6+(3-D)*rho-(D+1),                        (3)
```

and

```text
V=(2*A^2*D^2+2*A^2*D+5*A*R*D^2-2*A*R*D-A*R
   +D^2*R^2-R^2)*h2*rho
 +(-2*A^2*D^2+2*A^2*D-5*A*R*D^2-2*A*R*D+A*R
   -D^2*R^2+R^2)*h2
 +(A*D+A+D^2*R-D*R+R)*rho
 +A*D-A-D^2*R-D*R-R.                              (4)
```

Outside (2), on the divisor (1), the fourteen-by-eight mixed matrix has rank
eight, so no binary extension and hence no weighted-`H22` lift exists.

The divisors in (2) remain **UNKNOWN**.  This package does not claim a
binary or one-marked closure of them.  The generic weighted-`H22` fibre,
special parameter fibres, arbitrary source order, and the global Krenn--Gu
conjecture remain **UNRESOLVED**.

## Context: the broader first-minor scout

Let `M` be the fourteen-by-eight mixed matrix.  The determinant using all
columns and rows

```text
(0,1,2,3,4,5,6,7)                                 (5)
```

was separately certified once through the pair-orbit package's exact
Singular associate helper to be associated over `K` to

```text
H*f2*f3*rho*(rho-1)*f6*f7*f8*(rho+1)^2.           (6)
```

That computation motivates the divisor (1), but it is not part of this
package's replayable theorem: after WSL became unavailable, a native
`DomainMatrix` reconstruction of (6) exceeded 900 seconds.  The timeout is
not theorem evidence.  Formula (6) should be treated as a separately logged
exact certificate until its own replay environment is restored.

## Maximal minor on H=0

On `H=0`, equivalently `h1=-1/(2*A)`, use all columns and rows

```text
(1,2,3,5,6,7,9,12).                               (7)
```

This determinant is associated over `K` to

```text
h2*f2*rho*(rho+1)^2*f7*f8*U*V.                    (8)
```

For a native exact certificate, multiply the specialized matrix in (7) by
`16*A` entrywise.  Its determinant divided by the right side of (8) is

```text
-2^33*A^8*D*s^3*(D+1),                            (9)
```

which is a unit in `K`.  Equation (8) alone gives exactly (2) on (1).

## Method and boundary

Identity (8) is checked natively by an exact polynomial-domain determinant
and exact quotient division.  No finite field, random sample,
or numerical rank calculation enters the proof.

A direct saturated binary-plus-one-marked standard-basis calculation on
`H=0` exceeded 300 seconds.  That timeout is not evidence for survival or
emptiness.  Exact characteristic-zero interpolation was used only to
discover (4); the theorem relies on the subsequent generic polynomial
identity (8)--(9), not on the interpolation fibres.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h1-nonzero-two-minor-factor-cover-partial/verify_p5_h22_unequal_complement_common_kernel_component_d23_h1_nonzero_two_minor_factor_cover_partial_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h1-nonzero-two-minor-factor-cover-partial/audit_p5_h22_unequal_complement_common_kernel_component_d23_h1_nonzero_two_minor_factor_cover_partial_obstruction.py
```

The audit imports no repository code and independently rebuilds the
component rows, projected permanents, mixed matrix, and determinant quotient.
