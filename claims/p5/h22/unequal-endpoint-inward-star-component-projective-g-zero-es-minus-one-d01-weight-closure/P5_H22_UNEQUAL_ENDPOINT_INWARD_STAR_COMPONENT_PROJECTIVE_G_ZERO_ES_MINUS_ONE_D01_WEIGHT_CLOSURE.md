# Component twenty-five's `g=0, es=-1` projective sheet: `D01` weight closure

## Status

**Exact characteristic-zero projective-sheet partial theorem.**  On the
homogeneous component-twenty-five sheet

```text
a=1,  g=0,  es=-1,
```

the generic finite-`D01` weighted-`H22` fibre is empty.  The finite weights
`lambda=0,+1,-1` and the weight-at-infinity endpoint are also empty, with all
four marking parameters retained polynomially.

This does **not** classify every parameter-dependent special finite weight.
It also does not treat either `D23` chart, intersections with the remaining
projective leaf hyperplane, or arbitrary source/ambient/projective
compactifications.  The full weighted fibre on this projective sheet remains
**UNKNOWN**, and the global Krenn--Gu conjecture remains **UNRESOLVED**.

## The opposite sign sheet

On `a=1,g=0`, the homogeneous component equation is

```text
j^2(e^2s^2-1)=0.
```

At its generic point `j!=0`, choose `es=-1` and scale away `j`.  With

```text
A=X0+X1,  C=X0-X1,  B=X2+X3,  D=X2-X3,
```

use

```text
alpha0=A+B/s,                 beta0=A,
alpha1=A+kD+B/s+C,            beta1=A+kD,
alpha2=C,                     beta2=A-B/s-kD,
alpha3=D,                     beta3=B-sC.          (1)
```

The only nonzero pure coefficient is

```text
T1111=-4/s.                                           (2)
```

At `s=1,k=2`, the pair profile is `(3,3,3,4,4,4)`, so the sheet contains a
genuine all-pair open set.

## Legal transfer of the generic finite weight

The ambient swap `X0<->X1` fixes `A,B,D` and sends `C` to `-C`.  Apply it to
the previously closed `es=1` sheet after

```text
s -> -s,
alpha2 -> -alpha2,
h2 -> -h2.                                          (3)
```

For finite `D01`, also invert the homogeneous weight:

```text
lambda -> 1/lambda.                                 (4)
```

The verifier checks all sixteen marked extension coefficients entry by
entry.  If `d=(1,1,-1,1)` and `d_w` is the product of `d_i` over the alpha
positions of a binary word `w`, then

```text
d_w C_w^-(lambda)=lambda C_w^+(1/lambda).          (5)
```

The factor `lambda`, the source-row signs, and the ambient coordinate swap
are units over `Q(s,k,lambda)`.  Thus the certified all-marking obstruction
on the `es=1` sheet transfers legally to the generic finite weight on the
`es=-1` sheet.  Equation (5) is not used at `lambda=0` or infinity.

## Exact endpoint modules

The four endpoints are checked directly in the opposite-sheet basis (1).
For each contraction, take the eight coefficient columns of the extension
variables and the fourteen mixed binary rows.  Exact standard-basis
membership over

```text
Q(s,k)[h0,h1,h2,h3]
```

gives

```text
weight             forced diagonal in mixed module
lambda=0           all-alpha
lambda=+1          all-alpha
lambda=-1          all-beta
lambda=infinity    all-alpha.                     (6)
```

Any genuine binary neighbour requires both diagonals to be nonzero, so each
line of (6) is an obstruction.  No marking parameter is inverted.

The primary proves the transfer (5), then uses term-over-position endpoint
modules.  The no-import audit reconstructs permanents by subset dynamic
programming, uses a polynomially rescaled source basis and position-over-term
modules, directly rechecks the generic finite module instead of relying on
the transfer, and independently repeats all four endpoint memberships.

## Replay

First replay the `es=1` prerequisite:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-projective-g-zero-es-one-d01-generic-weight/verify_p5_h22_unequal_endpoint_inward_star_component_projective_g_zero_es_one_d01_generic_weight_obstruction.py
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-projective-g-zero-es-one-d01-generic-weight/audit_p5_h22_unequal_endpoint_inward_star_component_projective_g_zero_es_one_d01_generic_weight_obstruction.py
```

Then run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-projective-g-zero-es-minus-one-d01-weight-closure/verify_p5_h22_unequal_endpoint_inward_star_component_projective_g_zero_es_minus_one_d01_weight_closure.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-projective-g-zero-es-minus-one-d01-weight-closure/audit_p5_h22_unequal_endpoint_inward_star_component_projective_g_zero_es_minus_one_d01_weight_closure.py
```

All calculations are exact in characteristic zero.  No finite-field output
is used as proof.
