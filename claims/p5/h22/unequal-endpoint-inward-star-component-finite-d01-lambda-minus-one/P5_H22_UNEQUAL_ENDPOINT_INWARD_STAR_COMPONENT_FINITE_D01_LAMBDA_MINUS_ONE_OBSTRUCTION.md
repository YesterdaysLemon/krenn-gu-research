# Component twenty-five's finite-`D01` weight `lambda=-1` is empty

## Status

**Exact characteristic-zero all-marking theorem.**  Over the generic point
of component twenty-five, the finite-`D01` weighted slice at `lambda=-1`
has no genuine binary neighbour.

This closes the endpoint left open in
[`P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_RESIDUAL_FACTOR_COVER.md`](../unequal-endpoint-inward-star-component-finite-d01-residual-factor-cover/P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_RESIDUAL_FACTOR_COVER.md).
The two ordinary finite-`D01` factor branches, the remaining finite-`D23`
branches, and the full generic weighted `H22` fibre remain **UNKNOWN**.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## The opposite-diagonal module obstruction

Work over

```text
K=C(e,j,s)[k]/(F),
F=(ej+k^2)(1+ejs^2)-(e+j)^2.
```

Use the intrinsic pure bases `alpha_i,beta_i`, with every marking represented
by

```text
beta_i(h)=beta_i+h_i alpha_i.                       (1)
```

At finite `D01` weight `lambda=-1`, the contraction is

```text
(x,e) -> (-x_0+x_1,x_2,x_3,e).                    (2)
```

Let `M(h)` be the `14 x 8` matrix of mixed binary coefficients in the eight
extension entries.  Let `a(h),b(h)` be the all-`alpha` and all-`beta(h)`
diagonal rows.  Exact quotient-ring row-module reduction over

```text
K[h_0,h_1,h_2,h_3]
```

gives

```text
size std(Row(M))=12,
NF_M(a) != 0,
NF_M(b)=0.                                         (3)
```

Thus the opposite diagonal from the earlier infinity and `lambda=1`
obstructions vanishes here: `b` belongs to the mixed row module for every
marking.  Any extension satisfying `M(h)z=0` has `b(h)z=0`, contradicting
the nonzero all-active diagonal required by a genuine binary `Delta_2`.
The complete endpoint is empty before any ternary-rank test.

## Remaining frontier and replay

The finite-`D01` residual now consists only of the two ordinary-weight
branches `A=0` and `B=0` with `lambda^2 != 1`.  The finite-`D23` cover still
has its `z_2=0`, `G23_endpoint`, and `G23_ordinary` residual branches.

The basis chart excludes `P=ej+k^2=0`; the quadratic-leading divisor
`1+ejs^2=0`, all special parameter fibres, and projective component-boundary
fibres remain outside the theorem.  No finite-field computation is used as
proof.

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-lambda-minus-one/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_lambda_minus_one.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-lambda-minus-one/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_lambda_minus_one.py
```

The primary verifier builds (1)--(2) from the certified component model and
performs the exact quotient-ring reduction (3).  The audit imports no
project code, reconstructs every permanent by subset dynamic programming,
and independently repeats the all-marking module calculation.
