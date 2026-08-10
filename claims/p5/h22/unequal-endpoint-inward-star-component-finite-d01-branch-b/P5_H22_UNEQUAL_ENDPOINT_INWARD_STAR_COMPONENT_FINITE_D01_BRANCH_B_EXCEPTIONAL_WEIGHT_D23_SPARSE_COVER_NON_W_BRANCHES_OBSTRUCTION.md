# Component twenty-five's sparse `D23` cover: obstruction of the non-`w` branches

## Status

**Exact characteristic-zero finite-branch theorem.**  Retain the normalized
ordinary finite-`D01`, `B=0`, `N=0` sheet and the open conditions of the
component-twenty-five exceptional-weight packages.  The sparse paired-`D23`
two-minor theorem proves that simultaneous rank at most three requires

```text
w=0,
k=1,
or  Tbar=A=0,                                    (1)

Tbar=(1-b)lambda-(1+b),
A=a(lambda+1)-k(lambda-1).
```

This package closes the last two branches of (1):

- `k=1` lies entirely on the already-separated `a=+/-1` or `b=+/-1`
  boundaries;
- the complete retained `Tbar=A=0` branch has a genuine marked binary
  section, but an exact paired-`D23` one-marked map has rank four.

Consequently only the divisor `w=0` remains from the sparse two-minor cover
on the ordinary sheet.  This does not classify that divisor or any retained
standing/projective boundary.  It is not a counterexample.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## The `k=1` branch is old boundary

With `a=es`, `b=js`, and `s=1`, the component equation is

```text
F=(ab+k^2)(1+ab)-(a+b)^2=0.                      (2)
```

Direct factorization gives

```text
F|_{k=1}=(a-1)(a+1)(b-1)(b+1).                  (3)
```

These four parameter lines are precisely the linear factors already
separated in the certified `A_0=0` and `A_2=0` packages or their standing
boundaries.  Thus `k=1` contributes no new ordinary point away from those
packages.

## Elimination of the joint branch

On `Tbar=A=0`, away from `b=0,1`, one has

```text
lambda=(1+b)/(1-b),
k=a/b.                                           (4)
```

Substitution into (2) and the exceptional equation
`N=A_2 lambda^2+A_1 lambda+A_0=0` gives, up to the displayed invertible
factors,

```text
Phi_F = a^3b+a^2b^4-a^2b^2+a^2-ab^3-b^4,

Phi_N = 3a^3b^3-a^3b-a^2b^4+a^2b^2-a^2
        -ab^3-ab+b^4.                             (5)
```

More precisely, `F=Phi_F/b^2` and
`N=4(b+1)Phi_N/(b-1)`.  Exact elimination yields

```text
Res_a(Phi_F,Phi_N)
 =b^9(b-1)^3(b+1)^3 W,

W=3b^6-3b^4-6b^2-2.                              (6)
```

The sextic `W` is irreducible over `Q`.  The penultimate subresultant is
`b^4(b-1)(b+1)L`, where

```text
L=a(3b^8+12b^6-3b^4-2b^2+2)+9b^7+3b^5.          (7)
```

Its coefficient of `a` is coprime to `W`.  Reduction of (7) modulo `W`
therefore gives the unique retained parameterization

```text
a=b(3b^4-5b^2-4)/2.                              (8)
```

Thus the whole joint branch is computed in the exact degree-six field

```text
E=Q[b]/(W),

a=b(3b^4-5b^2-4)/2,
lambda=(1+b)/(1-b),
k=a/b.                                           (9)
```

The verifiers check in `E` that all retained component, weight, and
denominator factors are nonzero.

## Binary section and rank obstruction

The primary verifier independently solves the two finite-`D01` Segre
equations in `E`; the solution is

```text
w   =3(33b^5+123b^4-56b^3-200b^2-26b-126)/128,

z_6=-(969b^5+591b^4-1560b^3-936b^2-1002b-646)/128. (10)
```

It checks the third Segre equation, reconstructs and marks all sixteen binary
coefficients, and verifies that exactly the two diagonals survive and both
are nonzero.  Hence this is a genuine binary incidence, so the paired rank
test is required.

For the paired finite-`D23` mode-zero one-marked map, the coefficient rows
`000,001,010,011` give the exact minor

```text
delta_0=-2b(1023b^4-1223b^2-1950)/9.             (11)
```

Its field norm, computed as a resultant with `W`, is

```text
Norm_E/Q(delta_0)=-7912432945152 != 0.            (12)
```

Since `W` is irreducible in characteristic zero, (12) proves that this minor
is nonzero at every algebraic point of the joint branch.  The mode-zero map
therefore has rank four throughout (9), contradicting the rank-at-most-three
condition required by weighted `H22`.

The no-import audit uses subset-DP permanents, recursive cofactor
determinants, and the sparse row-pair basis from the prerequisite cover.  It
finds the independent rank-equivalent witness

```text
b(629739b^4-690248b^2-1332062)/1024,

Norm=-359006095368 != 0.                          (13)
```

Thus (11) is not being accepted merely through a duplicate implementation.

## Remaining boundary

Combining this theorem with the sparse two-minor cover reduces its retained
rank-drop alternatives to

```text
w=0.                                             (14)
```

The cleared polynomial geometry of (14), its intersections with the already
classified opposite-diagonal divisor, and all retained standing/projective
boundaries remain separate.  Equation (14) is a necessary residual branch,
not a claimed survivor.

## Replay

First replay the prerequisite sparse cover:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_d23_sparse_two_minor_cover.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_d23_sparse_two_minor_cover.py
```

Then run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_d23_sparse_cover_non_w_branches_obstruction.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_d23_sparse_cover_non_w_branches_obstruction.py
```

All four scripts use exact characteristic-zero arithmetic.  No finite-field
evidence is used.
