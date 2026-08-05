# `H31` exclusion on the intrinsic-basis boundary of component twenty

## Status

**Exact characteristic-zero divisor-generic boundary theorem.**  On the
finite normalized component-twenty divisor

```text
p-q+1=0,
```

the complete marked binary-neighbour incidence is empty over the generic
point.  Hence the marked `H31` fibre is empty there as well.

This is a divisor-generic statement.  It excludes `p=0,-1,-1/2`, where the
pure tensor vanishes or the normalized `U0` chart fails.  It does not cover
mixed source-torus/projective limits, parameter infinity, the singleton
sheet, weighted `H22`, component exhaustiveness, or the global Krenn--Gu
conjecture.

## Replacement intrinsic basis

Put `q=p+1`.  The intrinsic mode-zero row used by the generic theorem
collapses, so specializing that theorem's basis is invalid.  Return instead
to the two actual rows of the normalized `U0` plane:

```text
alpha0=r0=(0,-1,1,0),
beta0 =r1=(p(p+1)/(2p+1),-(2p+1),0,1).              (1)
```

For the other modes use

```text
alpha1=e,       beta1=((p+1)A+pB+C),
alpha2=e,       beta2=(pA+(p+1)B+C),
alpha3=e+A+B,   beta3=e.                             (2)
```

Exact permanent expansion leaves only

```text
T_1111=-2p(p+1).                                    (3)
```

Thus (1)--(2) is a valid pure orientation over `C(p)`.  Every marked basis of
the same four-plane point is `beta_i+h_i alpha_i` up to harmless nonzero row
scaling.

## Empty binary-neighbour projections

For each source deletion `d=0,1,2,3`, form the usual `14 x 8` mixed matrix
`M_d(h)` and binary diagonal rows `A_d(h),B_d(h)`.  Normalize and invert the
two required diagonal values:

```text
M_d(h)z=0,       A_d(h)z=1,       w B_d(h)z=1.       (4)
```

Exact characteristic-zero elimination over `C(p)` gives

```text
projection_h(4)=<1>       for d=0,1,2,3.             (5)
```

Each unit ideal is checked by bidirectional standard-basis reduction against
the expected ideal `<1>`.  Therefore no affine marking and no projective
extension direction produces even a genuine binary neighbour on the generic
point of this divisor.  A fortiori, no `H31` lift exists.

## Exact replay

```text
uv run --with sympy python \
  verify_p5_h31_common_active_binary_triangle_intrinsic_boundary_obstruction.py

uv run --with sympy python \
  audit_p5_h31_common_active_binary_triangle_intrinsic_boundary_obstruction.py
```

The primary verifier reconstructs the replacement basis, all sixteen pure
coefficients, and the four characteristic-zero projection certificates.  The
independent audit rebuilds the permanent maps without importing the primary
verifier and exhausts a finite-field marking sample only as a regression
check; it makes no characteristic-zero inference from that census.
