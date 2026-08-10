# Component twenty-five's exceptional `B`-weight leading divisor `A_2=0`

## Status

**Exact characteristic-zero special-divisor theorem.**  On component
twenty-five's normalized ordinary finite-`D01`, `B=0`, `N=0` sheet, the
leading-weight divisor

```text
A_2=0
```

supports no weighted `H22` lift.  The proof keeps the full quadratic
component algebra during the binary solve, treats its nonmonic parameter
boundary separately, and uses exact paired-`D23` rank minors.  No finite-field
evidence is used.

This closes only `A_2=0` inside the normalized ordinary finite sheet.  The
global opposite-diagonal and rank-norm divisors away from `A_2=0`, together
with standing and projective component boundaries, remain separate.  This is
not a counterexample.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Dimensionless factor cover

The preceding exact packages already remove `s=0`.  Use the homogeneous
rescaling to normalize `s=1`, and put

```text
a=es,  b=js.
```

Up to an invertible power of `s`, direct factorization gives

```text
A_2=(a+1)(b-1)C_2,

C_2=(3b^2+b-1)a^2-b(b+1)^2a+b^3.                 (1)
```

The two linear factors do not produce an ordinary point.  On `a=-1`, the
component equation gives

```text
P=1-b,  k^2=1,  e^2-k^2=0,                       (2)
```

so the entire factor is outside the normalized chart.  On `b=1`, the
exceptional weight equation specializes to

```text
N=-2(lambda-1)(a-1)^2(a+1).                      (3)
```

The ordinary condition `lambda^2!=1` therefore forces either `e-j=0` or the
boundary (2).  It remains to classify `C_2=0`.

## Generic `C_2` algebra

Write

```text
D=3b^2+b-1,
R=1+ab,  Q=a+b,  P=Q^2/R,  k^2=P-ab.
```

On `D!=0`, work in the full four-dimensional algebra

```text
E=Q(b)[a,k]/(C_2,k^2-P+ab),                      (4)
```

which is generically a field.  The verifier evaluates
`lambda=-A_0/A_1` inside (4), solves the two finite-`D01` Segre equations for
`w,z_6` in `E`, and checks the third equation directly.  It then reconstructs
and marks all sixteen binary coefficients.  Exactly the two diagonals remain,
with the first normalized to one.  No equation is split into coefficients of
`1,a,k,ak`.

The iterated norm to `Q(b)` of the opposite binary diagonal is nonzero.  After
cancellation, its exact signature

```text
(degree numerator, degree denominator,
 numerator at b=0, leading numerator coefficient)
  = (15,23,4,48).                                  (5)
```

Thus a zero of this norm is simply a failed binary incidence; away from its
zero divisor the section is genuinely binary and must also pass the paired
projection.

## Paired `D23` obstruction

For each marked mode `m`, take the fixed `4 x 4` minor of the one-marked
finite-`D23` ternary coefficient map whose other-mode rows are indexed by

```text
000, 001, 010, 011.
```

Let `nu_m(b)` be the iterated norm of this determinant.  Exact cancellation
gives the signatures

| marked mode | numerator degree | denominator degree | numerator at `b=0` | leading coefficient |
|---:|---:|---:|---:|---:|
| 0 | 86 | 80 | 1 | 9072 |
| 1 | 81 | 75 | -540 | 27 |
| 2 | 51 | 51 | -256 | 2160 |
| 3 | 58 | 54 | -1764 | 48 |

More strongly, the four cancelled numerators satisfy

```text
gcd_Q[b](numer(nu_0),...,numer(nu_3))=1.           (6)
```

Consequently, at every point where the rational section is defined, at least
one one-marked `D23` map has rank four.  A point where the opposite binary
diagonal vanishes already fails the binary requirement; every other point is
removed by (6).  Hence no point of this chart lifts to weighted `H22`.

## Denominators and the nonmonic boundary

The verifier factors every denominator appearing in (5)--(6).  Its complete
irreducible list, up to nonzero rational scalars, is

```text
b,  b-1,  b+1,  D,
b^2-8b+3,
b^3-b^2+3b-1,
b^3+3b^2+b+1,
b^4-8b^3+4b-1.                                   (7)
```

These factors introduce no omitted ordinary point:

- `b=0` is `j=0`, and `b=+/-1` reduces to the linear-factor or standing
  boundaries above;
- `b^2-8b+3=0` is the already-closed `H=0` intersection;
- `b^3-b^2+3b-1=0` is `R=0`;
- `b^3+3b^2+b+1=0` is `k=0`;
- `b^4-8b^3+4b-1=0` is `A_1=0`, while
  `Res_a(C_2,A_0)=16b^6(b-1)^3(b+1)^5`, so it has no `N=0` point away from
  the preceding factors;
- `D=0` is checked without division in a separate exact verifier.

For reference, the primary and audit also verify exact resultants locating
the `Q`, `R`, `e-j`, `e^2-k^2`, `H`, `T`, `A_0`, and `A_1` intersections.
They are boundary bookkeeping, not finite-field sampling.

On `D=0`, equation (1) is linear in `a` and gives

```text
a=b^2/(b+1)^2,  lambda=-3-6b,

E_D=Q(b)[k]/(3b^2+b-1,k^2-P+ab).                 (8)
```

The separate primary and no-import audit solve the binary section exactly in
`E_D`.  The opposite-diagonal norm is

```text
-7952112/18125,
```

and the four fixed `D23` minor norms are

```text
30155630569279962260615452611/409179521024000000000000,
-2996261580477497324383849919733/881852416000000000000,
-3507185203823023069968/5954345703125,
545235920497542050554260717/5954345703125.        (9)
```

All five values are nonzero, closing the nonmonic boundary.

## Replay

First replay the generic `C_2` calculation and its independent permanent and
determinant audit:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a2_zero_obstruction.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a2_zero_obstruction.py
```

Then replay the nonmonic boundary:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a2_zero_c2_leading_boundary_obstruction.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a2_zero_c2_leading_boundary_obstruction.py
```

The primary uses permutation permanents and direct Leibniz determinants.  The
no-import audit uses subset-DP permanents and recursive cofactor determinants.
All arithmetic is exact over characteristic zero.
