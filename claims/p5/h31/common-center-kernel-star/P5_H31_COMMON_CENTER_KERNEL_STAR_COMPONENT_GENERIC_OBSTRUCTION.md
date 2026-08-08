# Generic marked-`H31` obstruction on component twenty-three

## Status

**Exact characteristic-zero theorem over the component function field.**  The
complete generic marked-`H31` fibre over the outward common-center-kernel star
component is empty.  The calculation covers every affine marking, all eight
extension entries, and all four source-coordinate deletions.

This is a generic-point theorem.  It does not close special/projective fibres,
weighted `H22`, the remaining inward/mixed star orientations, or the global
local-to-global step.  The Krenn--Gu conjecture remains **UNRESOLVED**.

## Normalized component basis

Over `K=C(r,t)`, put

```text
k=(1-rt)/(t-r)
```

and use the component-twenty-three basis

```text
alpha=(A, A+kD, A-C+B+rD, -(A+C)+B+tD),
beta =(B, B+C, C, C).                              (1)
```

Replace `beta_i` by `beta_i+h_i alpha_i` for arbitrary markings `h_i`.

## Two row-module deletions

For deleted coordinates `q=0,1`, let `M_q` be the `14 x 8` mixed coefficient
matrix and let `d_0,d_1` be its all-alpha and all-beta diagonal rows.  Exact
polynomial module reduction over `K[h_0,h_1,h_2,h_3]` gives

```text
d_0 in Row(M_q),    d_1 notin Row(M_q),
size(std(Row(M_q)))=10.                            (2)
```

Thus those two deletions have no genuine binary neighbour.

## The two survivor markings

For deleted coordinate two, exact denominator-cleared saturated projection is

```text
J_2=<h3,h2,(r+t-2)h1-r+t,h0>,                     (3)
```

and for deleted coordinate three it is

```text
J_3=<h3,h2,(r+t+2)h1-r+t,h0>.                     (4)
```

Both ideal equalities are checked in both directions.  Hence the only
markings are

```text
q=2: h=(0,(r-t)/(r+t-2),0,0),
q=3: h=(0,(r-t)/(r+t+2),0,0).                     (5)
```

The complete mixed kernel has dimension two.  For `q=2`, a basis is

```text
e0=(0,(rt-1)/(r-t),(r-1)^2/(r+t-2),(t-1)^2/(r+t-2);1,0,0,0),
e1=(0,0,1,1;0,1,0,0),                             (6)
```

while for `q=3` it is

```text
e0=(0,-(rt-1)/(r-t),-(r+1)^2/(r+t+2),-(t+1)^2/(r+t+2);1,0,0,0),
e1=(0,0,1,1;0,1,0,0).                             (7)
```

Write `z=p e0+w e1`.  The binary diagonals are

```text
q=2:
d0=2((rt+r+t-3)p-(r+t-2)w),
d1=2((r-1)(t-1)p/(r+t-2)-w),

q=3:
d0=2((rt-r-t-3)p+(r+t+2)w),
d1=-2((r+1)(t+1)p/(r+t+2)+w).                    (8)
```

## Uniform ternary obstruction

For one-marked mode zero, the determinant on rows `0347` is exactly

```text
q=2: -2(r-1)(t-1)(rt-1)/((r-t)(r+t-2)) d0 d1^2,
q=3: -2(r+1)(t+1)(rt-1)/((r-t)(r+t+2)) d0 d1^2.  (9)
```

Every prefactor in (9) is nonzero in `K`, and a genuine binary extension has
`d0*d1!=0`.  Therefore the one-marked map has rank four.  Its pure
mode-zero transverse entry, in tensor row `001` and deleted column `q`, is
respectively

```text
2(1-rt)/(r-t),       2(rt-1)/(r-t),               (10)
```

so the standard transverse-coordinate argument eliminates the remaining
target row.  This contradiction proves that the generic marked-`H31` fibre is
empty.

## Replay

```text
uv run --with sympy python claims/p5/h31/common-center-kernel-star/verify_p5_h31_common_center_kernel_star_component_generic_obstruction.py
uv run --with sympy python claims/p5/h31/common-center-kernel-star/audit_p5_h31_common_center_kernel_star_component_generic_obstruction.py
```

The primary replay performs the exact function-field row-module reductions,
bidirectional projections, kernel checks, and determinant identities.  The
audit rebuilds both surviving branches at two independent rational parameter
points without importing the primary verifier.  No finite-field computation
is used.
