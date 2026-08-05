# Component twenty-five's finite-`D23` weight `lambda=1` is empty

## Status

**Exact characteristic-zero all-marking theorem.**  Over the generic point
of component twenty-five, the finite-`D23` weighted slice at `lambda=1` has
no genuine binary neighbour.

This closes one divisor inside the `A23` branch of
[`P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D23_FACTOR_COVER.md`](P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D23_FACTOR_COVER.md).
The remaining finite-`D23` branches, the finite-`D01` residual, and the full
generic weighted `H22` fibre remain **UNKNOWN**.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## The all-marking row module

Work over

```text
K=C(e,j,s)[k]/(F),
F=(ej+k^2)(1+ejs^2)-(e+j)^2.
```

Use the intrinsic pure bases `alpha_i,beta_i` from the component's generic
`H31` theorem and mark every basis by

```text
beta_i(h)=beta_i+h_i alpha_i.                       (1)
```

At finite `D23` weight `lambda=1`, the contraction is

```text
(x,e) -> (x_0,x_1,x_2+x_3,e).                     (2)
```

In the canonical unmarked coordinates, the three sparse coefficients

```text
C_1000=C_0100=C_1100=0.                            (3)
```

For the complete marked family, let `M(h)` be the `14 x 8` matrix of mixed
binary coefficients in the eight extension entries, and let `a(h),b(h)` be
the all-`alpha` and all-`beta(h)` diagonal rows.  Exact quotient-ring module
reduction over

```text
K[h_0,h_1,h_2,h_3]
```

gives

```text
size std(Row(M))=7,
NF_M(a)=0,
NF_M(b) != 0.                                      (4)
```

Thus `a` belongs to the mixed row module for every marking.  Any extension
with `M(h)z=0` consequently has `a(h)z=0`, contradicting the nonzero
all-kernel diagonal required by a genuine binary `Delta_2`.  The slice is
empty before any ternary-rank test.

## Remaining frontier and replay

Inside the earlier finite-`D23` cover, the broad branch

```text
(lambda-1)z_2=0
```

now reduces away from `lambda=1` to `z_2=0`.  The `G23_endpoint` and
`G23_ordinary` branches are unchanged and remain open.

The basis chart excludes `P=ej+k^2=0`; the quadratic-leading divisor
`1+ejs^2=0`, all special parameter fibres, and projective component-boundary
fibres remain outside the theorem.  No finite-field computation is used as
proof.

Run:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d23_lambda_one.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d23_lambda_one.py
```

The primary verifier constructs (1)--(3) from the certified component model
and performs the exact quotient-ring reduction (4).  The audit imports no
project code, reconstructs every permanent by subset dynamic programming,
and independently repeats the same all-marking module calculation.
