# Linear reduction of component twenty-five's ordinary finite-`D01` `A` branch

## Status

**Exact characteristic-zero supplemental reduction.**  On the ordinary
finite-`D01` residual branch `A=0`, one further Segre equation uniquely
determines `z_6` from the last free extension parameter `w`.

The remaining two Segre equations are not closed here.  Thus the `A` branch,
the parallel `B` branch, the remaining finite-`D23` branches, and the generic
weighted `H22` fibre remain **UNKNOWN**.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Input branch

Put

```text
P=ej+k^2,       Q=e+j,       R=1+ejs^2,
F=PR-Q^2.
```

Use the denominator-free finite-`D01` residual parameterization

```text
z_2=(lambda-1)w,       z_4=-(lambda+1)w.            (1)
```

On `lambda^2 != 1`, the four forced linear equations from the fixed-vertex
join solve `z_0,z_1,z_5,z_7` in terms of `w,z_3,z_6`.  The `A=0` factor from
the preceding factor cover sets

```text
z_3=-1/[2(lambda-1)(e^2-k^2)P].                    (2)
```

## The surviving `{1,3}` equation

Substitute (1)--(2) and the four linear solutions into

```text
C_0101 C_0000-C_0100 C_0001=0.                    (3)
```

Clear the substitution denominators and reduce the numerator exactly modulo
`F`.  Up to the nonzero factor `-Q^2/R^2`, the remainder is

```text
E_A=
  2kQ^2(e-j)(lambda-1)((lambda+1)w+z_6)+jR.        (4)
```

Hence every candidate on the ordinary `A` branch satisfies

```text
z_6=-(lambda+1)w
    -jR/[2kQ^2(e-j)(lambda-1)].                    (5)
```

The branch is therefore reduced to one extension parameter `w`; the two
remaining three-mode Segre equations decide whether it is empty or survives.

## Boundary and replay

This function-field chart treats

```text
P R k Q (e-j)(e^2-k^2)(lambda^2-1)
```

as nonzero.  Their special fibres and all projective component-boundary
fibres remain outside the claim.  The `B=0` branch is untouched.  A bounded
attempt to reduce the next Segre equation reached the 120-second cap; that
timeout is not theorem evidence.  No finite-field computation is used as
proof.

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a.py
```

The primary verifier reconstructs the certified component model, performs
the exact quotient reduction, and proves (4).  The audit imports no project
code, rebuilds the permanent tensor by subset dynamic programming, and
independently repeats the reduction.
