# Generic-weight obstruction on component twenty-five's finite-`D01` `A` branch

## Status

**Exact characteristic-zero generic-weight theorem.**  On the ordinary
finite-`D01` branch `A=0`, no binary candidate exists over the weight
function field `K(lambda)`.

This proves that no component of the `A`-branch incidence dominates the
ordinary weight line.  It does not identify or close the proper exceptional
weight divisor on which isolated candidates could remain.  Consequently the
complete `A` branch, the parallel `B` branch, the finite-`D01` residual, and
the generic weighted `H22` fibre remain **UNKNOWN**.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Exact terminal ideal

Put

```text
P=ej+k^2,       Q=e+j,       R=1+ejs^2,
F=PR-Q^2,
K=C(e,j,s)[k]/(F).
```

Use the residual parameterization and `A`-branch reduction from the preceding
certificates:

```text
z_2=(lambda-1)w,
z_4=-(lambda+1)w,
z_3=-1/[2(lambda-1)(e^2-k^2)P],

z_6=-(lambda+1)w
    -jR/[2kQ^2(e-j)(lambda-1)].                    (1)
```

Equivalently, retain the denominator-free equations defining (1), together
with the three forced mode-zero mixed coordinates and the normalization
`C_0000=1`.  Call their ideal `L` over

```text
K(lambda)[z_0,z_1,z_3,z_5,z_6,z_7,w].             (2)
```

Only two fixed-vertex Segre equations remain:

```text
S_23 =C_0011 C_0000-C_0010 C_0001,
S_123=C_0111 C_0000^2-C_0100 C_0010 C_0001.        (3)
```

Exact quotient-ring reduction first computes

```text
r_23 =NF_L(S_23),       r_123=NF_L(S_123),
```

and then gives

```text
std(L,r_23,r_123)=(1)                              (4)
```

over `K(lambda)`.  Thus the complete residual system has no solution at the
generic ordinary weight.

## Honest residual and replay

Statement (4) permits denominators in `lambda`.  It proves that any survivor
is supported on a proper algebraic divisor of the ordinary weight line, but
does not calculate that divisor.  A direct expanded reduction of `S_23`
reached the 120-second cap.  A retained-weight projection was then attempted,
but the WSL backend failed to start before Singular ran.  Neither event is
proof evidence, and no explicit exceptional-weight polynomial is claimed.

The chart also treats

```text
P R k Q (e-j)(e^2-k^2)(lambda^2-1)
```

as nonzero.  Their special fibres, the `B=0` branch, and projective
component-boundary fibres remain outside the theorem.  No finite-field
computation is used as proof.

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a-univariate/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_univariate.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a-univariate/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_univariate.py
```

The primary verifier reconstructs the certified component model and proves
(4) in the exact quotient ring.  The audit imports no project code, rebuilds
the permanent tensor by subset dynamic programming, and independently
repeats the same standard-basis calculation.
