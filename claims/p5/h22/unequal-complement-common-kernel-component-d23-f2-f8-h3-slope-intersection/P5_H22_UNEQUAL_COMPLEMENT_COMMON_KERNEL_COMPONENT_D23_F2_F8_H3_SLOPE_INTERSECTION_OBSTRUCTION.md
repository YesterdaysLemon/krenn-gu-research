# Component twenty-two: the `f2=f8=2h3+s=0` intersection is empty

## Status

**Exact characteristic-zero generic-component branch closure.**  Over
`K=Q(A,R,D)`, put `s=2*A+R` and consider component twenty-two's finite-`D23`
divisor

```text
H=2*A*h1+1=0,          rho*(rho+1)!=0.            (1)
```

With

```text
f2=s*h2+1,
f8=(A*D+A+R*D)*rho+A*D-A+R*D,                   (2)
```

the complete intersection

```text
H=f2=f8=2*h3+s=0                                  (3)
```

has mixed rank eight and is empty for weighted `H22`.  One exact maximal
minor forces a unique linear value of `h0`; a second maximal minor at that
value is a nonzero coefficient-field unit.

This closes only the displayed subintersection over `Q(A,R,D)`.  The rest of
`f2=f8=0`, the remaining `f2` residual, other special component-parameter
fibres, and all projective/source/ambient charts remain **UNKNOWN**.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.  No finite field or
numerical rank inference is used.

## Linear `h0` cofactor

On (3), solve

```text
h1=-1/(2*A),
h2=-1/s,
h3=-s/2,
rho=-(A*D-A+R*D)/(A*D+A+R*D).                   (4)
```

The determinant of the fourteen-by-eight mixed matrix on all columns and
rows

```text
(0,1,2,3,4,7,8,9)                                (5)
```

is a coefficient-field unit times

```text
Q8=2*A*D^2*h0-A*D^2-2*A*D*h0+2*A*D-A
   +2*D^2*R*h0-D^2*R-2*D*R*h0+2*D*R.            (6)
```

The exact unit multiplier is

```text
1024*A^6*D^4*R^2*(A+R)^2*s^5*(D-1)*(D+1)^3
 * (A*D-A+D*R)/(A*D+A+D*R)^7.                   (7)
```

Therefore rank drop forces

```text
h0=[A*(D-1)^2+D*(D-2)*R]/[2*D*(D-1)*(A+R)].      (8)
```

## Terminal unit

After (8), the determinant on rows

```text
(0,1,2,3,4,7,8,11)                               (9)
```

equals

```text
-256*A^4*D^4*R^2*(A+R)^2*s^4*(4*A+R)*(D-1)
 * (D+1)^3*(A*D-A+D*R)*T8/(A*D+A+D*R)^7,        (10)
```

where

```text
T8=2*A^3*D^2-2*A^3+4*A^2*D^2*R
   +3*A*D^2*R^2+A*R^2+D^2*R^3.                  (11)
```

Both `4*A+R` and `T8` are nonzero polynomials and hence units of
`K=Q(A,R,D)`.  Thus (10) is nonzero, contradicting mixed rank drop and
proving (3) empty.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-h3-slope-intersection/verify_p5_h22_unequal_complement_common_kernel_component_d23_f2_f8_h3_slope_intersection_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-h3-slope-intersection/audit_p5_h22_unequal_complement_common_kernel_component_d23_f2_f8_h3_slope_intersection_obstruction.py
```

The primary uses exact fraction-field `DomainMatrix` determinants.  The audit
rebuilds the component rows and projected permanents from the lower-level
model and evaluates both determinants by explicit rational Gaussian
elimination.
