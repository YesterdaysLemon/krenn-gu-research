# Component twenty-five's exceptional `B`-weight `A_0=0` companion divisor

## Status

**Exact characteristic-zero special-divisor theorem.**  On component
twenty-five's normalized ordinary finite-`D01`, `B=0`, `N=0` sheet, the
nonzero-weight companion on the constant-weight divisor

```text
A_0=0
```

supports no weighted `H22` lift.  The generic companion is solved over the
full four-dimensional component algebra, its nonmonic parameter boundary is
handled separately, and a specialization-independent Bezout certificate
shows that the four paired-`D23` rank norms never vanish simultaneously.

Combined with the previously certified `lambda=0` theorem, this closes
`A_0=0` inside the normalized ordinary finite sheet.  The global
opposite-diagonal and rank-norm divisors away from `A_0A_2=0`, and the standing
and projective component boundaries, remain separate.  This is not a
counterexample.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Factor cover and reciprocal structure

As in the leading-divisor theorem, normalize the already-nonzero parameter
`s` to one and put

```text
a=es,  b=js.
```

Then

```text
A_0=(a-1)(b+1)C_0,

C_0=(3b^2-b-1)a^2-b(b-1)^2a-b^3.                (1)
```

The linear factor `a=1` lies identically on `e^2-k^2=0`.  On `b=-1`, the
exceptional equation is

```text
N=-2lambda(lambda-1)(a-1)(a+1)^2.                (2)
```

Thus an ordinary nonzero weight on this factor forces the endpoint
`lambda=1`, `e^2-k^2=0`, or `Q=0`.  Only `C_0=0` remains.

There is an exact reciprocal algebra identity

```text
C_0(a,b)=C_2(-a,-b),
N(a,b,lambda)=lambda^2 N(-a,-b,lambda^-1).        (3)
```

It predicts the mirror pattern found below, but the verifier and its
no-import audit reconstruct all rows and permanents independently; no graph
or coordinate symmetry not already certified is assumed.

## Generic `C_0` companion

On `C_0=0` and `lambda!=0`, the exceptional equation becomes

```text
A_2 lambda+A_1=0,
lambda=-A_1/A_2.                                  (4)
```

Write

```text
D=3b^2-b-1,
R=1+ab,  Q=a+b,  P=Q^2/R,  k^2=P-ab.
```

For `D!=0`, the computation takes place in

```text
E=Q(b)[a,k]/(C_0,k^2-P+ab).                      (5)
```

The primary and audit solve the two finite-`D01` Segre equations for `w,z_6`
in all of `E`, verify the third equation, reconstruct all sixteen marked
binary coefficients, and normalize the first diagonal to one.  No equation
is split into coefficients of `1,a,k,ak`.

The iterated norm of the opposite binary diagonal is nonzero, with cancelled
signature

```text
(degree numerator, degree denominator,
 numerator at b=0, leading numerator coefficient)
  = (15,23,-4,48).                                 (6)
```

For each marked mode, take the fixed `4 x 4` minor of the paired finite-`D23`
one-marked ternary map whose other-mode rows are `000,001,010,011`.  The four
iterated norm signatures are

| mode | numerator degree | denominator degree | numerator at `b=0` | leading coefficient |
|---:|---:|---:|---:|---:|
| 0 | 86 | 80 | 1 | 9072 |
| 1 | 81 | 75 | 540 | 27 |
| 2 | 51 | 51 | 256 | 2160 |
| 3 | 58 | 54 | -1764 | 48 |

Their cancelled numerators satisfy the specialization-independent identity

```text
gcd_Q[b](numer(nu_0),...,numer(nu_3))=1.           (7)
```

Hence at every defined parameter value at least one paired map has rank four.
If the opposite diagonal vanishes, the binary section is nongenuine; if it is
nonzero, (7) obstructs weighted `H22`.

## Denominator cover

The complete irreducible denominator list for the component parameters,
solved extension, marking, binary coefficients, paired rows, determinants,
and iterated norms is

```text
b,  b-1,  b+1,  D,
b^2+8b+3,
b^3+b^2+3b+1,
b^3-3b^2+b-1,
b^4+8b^3-4b-1.                                   (8)
```

Exact resultants identify them as follows:

- `b=0` is `j=0`, while `b=+/-1` reduces to (2) or standing boundaries;
- `b^2+8b+3=0` is the already-closed `H=0` intersection;
- `b^3+b^2+3b+1=0` is `R=0`;
- `b^3-3b^2+b-1=0` is `k=0`;
- `b^4+8b^3-4b-1=0` is `A_1=0`.  On the nonzero companion (4), this would
  also require `A_2=0`, but

  ```text
  Res_a(C_0,A_2)=16b^6(b-1)^5(b+1)^3,
  ```

  so there is no new ordinary point away from the preceding factors;
- `D=0` is computed directly below.

The same verifier also checks exact resultants for `Q`, `e-j`,
`e^2-k^2`, and `T`, keeping all standing and previously closed linear
boundaries explicit.

## Nonmonic boundary

On

```text
D=3b^2-b-1=0,
```

equation (1) becomes linear in `a` and gives

```text
a=-b^2/(b-1)^2,
lambda=1/9+(2/3)b.                                (9)
```

The companion weight in (9) is the reciprocal, modulo `D`, of the mirrored
leading-divisor weight in (3).  The separate primary and no-import audit work
directly in

```text
E_D=Q(b)[k]/(3b^2-b-1,k^2-P+ab).                 (10)
```

They solve the binary section exactly.  The opposite-diagonal norm is

```text
-7952112/18125,
```

and the four paired fixed-minor norms are

```text
30155630569279962260615452611/409179521024000000000000,
-2996261580477497324383849919733/881852416000000000000,
-3507185203823023069968/5954345703125,
545235920497542050554260717/5954345703125.        (11)
```

All five values are nonzero, closing the nonmonic boundary.

## Replay

Replay the generic companion and its independent audit:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a0_companion_divisor_obstruction.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a0_companion_divisor_obstruction.py
```

Then replay the nonmonic boundary:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a0_companion_c0_leading_boundary_obstruction.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a0_companion_c0_leading_boundary_obstruction.py
```

The primary uses permutation permanents and direct determinant expansions;
the no-import audit uses subset-DP permanents and recursive cofactor
determinants.  All arithmetic is exact over characteristic zero, and no
finite-field evidence is used.
