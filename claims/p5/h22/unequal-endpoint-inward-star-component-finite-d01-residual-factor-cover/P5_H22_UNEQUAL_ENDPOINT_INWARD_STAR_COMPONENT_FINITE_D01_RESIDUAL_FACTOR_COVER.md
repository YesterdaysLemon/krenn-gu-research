# Factor cover of component twenty-five's finite-`D01` residual

## Status

**Exact characteristic-zero supplemental reduction.**  This note refines the
finite-`D01` residual

```text
L_01=(lambda+1)z_2+(lambda-1)z_4=0
```

from
[`P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_PARTIAL.md`](../unequal-endpoint-inward-star/P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_PARTIAL.md).
The weight `lambda=1` is empty.  Away from `lambda=1,-1`, every remaining
candidate lies on one of two explicit linear factor branches.

Neither branch nor the endpoint `lambda=-1` is closed here.  Thus the full
finite-`D01` residual, finite `D23`, and the generic weighted `H22` fibre
remain **UNKNOWN**.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Denominator-free residual line

Put

```text
P=ej+k^2,       Q=e+j,
F=P(1+ejs^2)-Q^2.
```

Parametrize the residual without dividing by the weight:

```text
z_2=(lambda-1)w,       z_4=-(lambda+1)w.            (1)
```

This covers the line at both `lambda=1` and `lambda=-1`.  In the canonical
fixed-vertex coordinates it makes

```text
C_1000=C_1001=C_1100=C_1101=0.                     (2)
```

At `lambda=1`, it also makes `C_0000=0`.  The required all-kernel diagonal
therefore vanishes, so that finite weight is empty.

## Ordinary-weight linear reduction

Assume `lambda^2 != 1`.  Since the singleton `C_1000` vanishes, the
fixed-vertex Segre equations force

```text
C_1010=C_1011=C_1110=0.                            (3)
```

Normalize `C_0000=1`.  On the generic parameter chart

```text
kQ(k^2-e^2) != 0,
```

the four linear equations have a unique solution for
`z_0,z_1,z_5,z_7` in terms of `w,z_3,z_6`.  Substitution into the first
remaining three-mode Segre equation gives the exact identity

```text
C_0110 C_0000-C_0100 C_0010
  = (P/Q^2) A B,                                    (4)

A=1+2(lambda-1)(e^2-k^2)P z_3,

B=2P((lambda-1)sP-(lambda+1)Q)z_3-s.               (5)
```

The identity holds before reduction modulo `F`; in particular it is valid
over the component function field.  Since `P,Q` are units there, every
ordinary-weight candidate on `L_01=0` lies on

```text
A=0       or       B=0.                            (6)
```

This replaces the seven-variable residual by two explicit linear `z_3`
branches.  The other three-mode Segre equations on those branches remain to
be analyzed.

## Boundary ledger

The unresolved residual is now:

```text
lambda=-1,
lambda^2!=1 with A=0,
lambda^2!=1 with B=0,
and the entire finite-D23 pair orbit.               (7)
```

The component divisors `P=0`, `1+ejs^2=0`, `Q=0`, `k=0`, and
`k^2-e^2=0`, together with projective component-boundary fibres, remain
outside the generic chart.  No finite-field calculation is used as proof.
A bounded attempt to reduce the three remaining equations simultaneously on
both branches timed out after 120 seconds; that timeout is not theorem
evidence.

## Replay

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-residual/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_residual.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-residual/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_residual.py
```

The primary verifier uses the certified component basis and independently
checks (1)--(5).  The audit imports no project code, reconstructs every
permanent by subset dynamic programming, and repeats the symbolic
factorization from scratch.
