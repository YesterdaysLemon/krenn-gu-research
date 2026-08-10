# Component twenty-three `r=0` divisor-generic weighted-`H22` obstruction

## Status

**Exact characteristic-zero divisor-generic theorem.**  Work over

```text
K=Q(t)
```

on the normalized component-twenty-three divisor `r=0`.  Every finite weight,
including `lambda=0,1,-1`, and the projective weight is obstructed.  Hence the
complete weighted-`H22` fibre over the generic point of this component divisor
is empty.

This is not a pointwise theorem for every exceptional value of `t`.  The
normal-form boundary and special points of the `t`-line remain part of the
special/projective component analysis.  Other component-twenty-three divisors,
other components' remaining special fibres, and the global Krenn--Gu
conjecture remain **UNRESOLVED**.

## Divisor model

The normalized component basis is

```text
k=(1-rt)/(t-r),
alpha=(A, A+kD, A-C+B+rD, -(A+C)+B+tD),
beta =(B, B+C, C, C).
```

On `r=0` this gives `k=1/t`.  Thus `r=0` is a genuine divisor in the pure
all-pair chart over `Q(t)`, not a forced lower-pair collision.  Mark every row
by replacing

```text
beta_i -> beta_i+h_i alpha_i.
```

Use all eight extension entries and combine the fourteen mixed finite-`D01`
rows with the fourteen mixed finite-`D23` rows into a `28 x 8` matrix `M`.

## Ordinary finite weights

On this divisor,

```text
F=h3*t^2*(h0*(lambda+1)-2).                         (1)
```

Rows `0,1,3,7,8,9,11,12` give the divisor-specific exact minor

```text
-2048*h3*lambda*(lambda-1)^2*(lambda+1)^3
     *(h0*(lambda+1)-2).                            (1a)
```

Thus (1a) closes the ordinary open `F!=0` without specializing a generic
function-field unit.

Assume `lambda*(lambda-1)*(lambda+1)!=0` and `F=0`.  The verifier gives the
following exact minor cover.  Row sets refer to `M`, and every minor uses all
eight extension columns.

If `h3!=0`, substitute `h0=2/(lambda+1)`.  Rows

```text
0,1,3,4,7,8,9,11
```

have determinant

```text
-2048*h3*lambda*(lambda-1)^2*(lambda+1)^4,          (2)
```

so this branch is empty.

It remains to set `h3=0`.  Rows `1,3,4,5,7,8,9,11` give

```text
-2048*h2*lambda*(h1-1)*(lambda-1)^2*(lambda+1)^4.  (3)
```

Thus only `h2=0` or `h1=1` remains.

### The `h2=0` branch

Successive minors on rows

```text
1,3,4,7,8,9,11,12
1,3,4,7,8,9,11,13
1,3,4,7,8,9,11,14
```

have determinants

```text
 2048*lambda*(lambda-1)^3*(lambda+1)^3*(h0-h1-1),
-2048*lambda*(lambda-1)^3*(lambda+1)^3*(h1-1),
 1024*lambda*(lambda-1)^3*(lambda+1)^3
      *((lambda+1)t-2)/t,                           (4)
```

after imposing each preceding zero relation.  The terminal relation is
`lambda=2/t-1`; rows `1,3,4,7,8,9,11,16` then have determinant

```text
131072*(t-2)*(t-1)^3/t^9,                           (5)
```

a nonzero element of `Q(t)`.

### The `h1=1` branch

Rows `1,3,4,7,8,9,11,12` give

```text
-2048*lambda*(lambda-1)^2*(lambda+1)^3*G,           (6)

G=2*lambda*h2*(h0-1)-(lambda-1)*(h0-2).
```

On `G=0`, the case `h0=1` would force `lambda=1`; otherwise solve

```text
h2=(lambda-1)(h0-2)/(2lambda(h0-1)).                (7)
```

Rows `1,3,4,7,8,9,11,14` then give

```text
512*(lambda-1)^3*(lambda+1)^3
    *(h0*(lambda+1)-2)*((lambda+1)t-2)/t.           (8)
```

On the first factor branch, `h0=2/(lambda+1)` and (7) gives `h2=1`;
rows `1,3,4,7,8,9,11,17` have determinant

```text
-2048*lambda*(lambda-1)^3*(lambda+1)^3
     *(t-1)*(t+1)/t.                                (9)
```

On the second factor branch, `lambda=2/t-1`; the same rows split off

```text
h0*t-4*h0+2*t.                                      (10)
```

After its vanishing forces

```text
h0=-2t/(t-4),       h2=4(t-1)/(3t-4),              (11)
```

rows `1,3,4,7,8,9,11,16` have determinant

```text
131072*(t-2)*(t-1)^3/(t^8*(t-4)),                  (12)
```

again nonzero in `Q(t)`.  Equations (2)--(12) close every ordinary weight.

## Finite endpoints and projective weight

At `lambda=0`, rows `0,1,3,4,7,8,9,14` have determinant

```text
-256*h3*H0/t,
H0=2(t-1)(t+2)h3-t+2.                              (13)
```

Thus only `h3=0` or `H0=0` remains.  Exact module reductions over
`Q(t)[h]` give the full free rank-eight module on both loci.  A third full
module on `h2=0` is retained as an independent redundant check:

```text
h2=0,       h3=0,       h3=(t-2)/(2(t-1)(t+2)).    (14)
```

At `lambda=-1` the mixed-row module is also the full free module.  At
`lambda=1` it is exactly

```text
<e1,e2,e3,e4,e6,e7,e8>.                            (15)
```

The `D01` and `D23` all-alpha diagonals and the `D01` all-beta diagonal lie
in (15), so every mixed-kernel vector has a zero pure diagonal; no genuine
binary restriction survives.  Finally, at projective weight the mixed module
is again the full free rank-eight module.  This closes both weight charts.

## Boundary and failed routes

The proof is over the divisor function field `Q(t)`.  Factors such as
`t`, `t-1`, `t+1`, `t-2`, `t-4`, and `3t-4` are field units here; their
individual fibres are not silently claimed.  Some are endpoint or lower-pair
boundaries, while the remaining exceptional fibres require their own local
charts.  No arbitrary source-basis, ambient-basis, or omitted component chart
is covered by this package.

The determinant tree was used because a single monolithic saturated ideal is
substantially less transparent and was not needed.  No finite-field
calculation is used.

## Replay

```powershell
uv run --with sympy python verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement.py
uv run --with sympy python verify_p5_h22_common_center_kernel_star_component_r_zero_divisor_generic_obstruction.py
uv run --with sympy python audit_p5_h22_common_center_kernel_star_component_r_zero_divisor_generic_obstruction.py
```

The primary recomputes all twelve ordinary minors over `Q(t)`, the
`lambda=0` dense minor, and all six endpoint/projective row-module
certificates.  The no-import audit rebuilds the
permanent tensor independently at `(r,t)=(0,3)`, repeats the entire minor tree
and all modules over `Q`, and is explicitly an audit rather than the
divisor-generic proof.
