# Component twenty-two: the `f2=f7=0` intersection is empty

## Status

**Exact characteristic-zero generic-component branch closure.**  Work over

```text
K=Q(A,R,D),              s=2*A+R,
```

on component twenty-two's finite-`D23` divisor

```text
H=2*A*h1+1=0,            rho*(rho+1)!=0.          (1)
```

Put

```text
f2=s*h2+1,
f7=(A*D+A+R)*rho+A*D-A-R.                        (2)
```

Then the complete intersection

```text
H=f2=f7=0                                             (3)
```

has mixed rank eight and is empty for weighted `H22`.  Three fixed maximal
minors give a triangular exact contradiction: the first forces one linear
value of `h0`, the second forces `2*h3+s=0`, and the third is a nonzero
element of the coefficient field.

This closes only the generic point over `Q(A,R,D)`.  Specializations of the
component parameters, the remaining `f2*f8*P=0` residual on `f2=0`, the
other `H=0` factors, and all other projective/source/ambient charts remain
**UNKNOWN**.  The global Krenn--Gu conjecture remains **UNRESOLVED**.  No
finite field or numerical rank calculation is used.

## First linear cofactor

On (3), solve

```text
h1=-1/(2*A),
h2=-1/s,
rho=-(A*D-A-R)/(A*D+A+R).                        (4)
```

For the fourteen-by-eight mixed matrix, the determinant on all columns and
rows

```text
(0,1,2,3,4,7,8,9)                                (5)
```

is a coefficient-field unit times

```text
Q0=4*A*D*h0-3*A*D+A+2*D*R*h0-D*R+R.             (6)
```

More precisely, the unit multiplier is

```text
-256*A^3*D^4*R^2*(A+R)^2*s^6*(D-1)*(D+1)^2
 * (A*D-A-R)^2/(A*D+A+R)^6.                      (7)
```

Hence rank drop forces

```text
h0=(3*A*D-A+D*R-R)/(2*D*s).                      (8)
```

## Second linear cofactor

After (8), the determinant on rows

```text
(0,1,2,3,4,7,8,10)                               (9)
```

is a coefficient-field unit times

```text
s+2*h3.                                          (10)
```

Its exact unit multiplier is

```text
256*A^3*D^4*R*(A+R)^3*s^7*(D-1)*(D+1)^3
 * (A*D-A-R)^2/(A*D+A+R)^6.                     (11)
```

Thus rank drop additionally forces `h3=-s/2`.

## Terminal unit

With (4), (8), and `h3=-s/2`, the determinant on rows

```text
(0,1,2,3,4,7,8,11)                               (12)
```

equals

```text
-128*A^2*D^4*R^2*(A+R)^3*s^5*(D+1)^2
 * (A*D-A-R)^2*T7/(A*D+A+R)^6,                  (13)
```

where

```text
T7=4*A^2*D^2-4*A^2+6*A*D^2*R+2*A*R
   +D^2*R^2+3*R^2.                               (14)
```

Equation (14) is a nonzero polynomial in `A,R,D`, hence a unit of
`K=Q(A,R,D)`.  Therefore (13) is nonzero, contradicting mixed rank drop.
This proves the branch empty.

## Replay

```powershell
uv run --with sympy python verify_p5_h22_unequal_complement_common_kernel_component_d23_f2_f7_intersection_obstruction.py
uv run --with sympy python audit_p5_h22_unequal_complement_common_kernel_component_d23_f2_f7_intersection_obstruction.py
```

The primary uses exact fraction-field `DomainMatrix` determinants.  The audit
rebuilds the component rows and projected permanents from the lower-level
model, then evaluates the same three determinants by explicit rational
Gaussian elimination.
