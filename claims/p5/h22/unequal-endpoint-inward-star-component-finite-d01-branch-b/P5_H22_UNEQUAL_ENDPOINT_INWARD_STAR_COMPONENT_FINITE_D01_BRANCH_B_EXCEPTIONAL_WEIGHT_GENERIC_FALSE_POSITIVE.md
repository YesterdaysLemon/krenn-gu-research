# Generic false-positive classification on component twenty-five's exceptional `B`-weight divisor

## Status

**Exact characteristic-zero generic-divisor theorem.**  Retain the notation and
open chart of
[`P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_BRANCH_B_FULL_FIELD_GENERIC_WEIGHT_OBSTRUCTION.md`](P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_BRANCH_B_FULL_FIELD_GENERIC_WEIGHT_OBSTRUCTION.md).
On a nonempty Zariski-open subset of the exceptional divisor

```text
N=A_2 lambda^2+A_1 lambda+A_0=0,
```

the unique finite-`D01`, `B=0` section is a genuine shared binary incidence:
after marking, all fourteen mixed binary coefficients vanish and both diagonal
coefficients are nonzero.  It nevertheless is generically a **false positive**
for weighted `H22`.  For the paired finite-`D23` projection, every one-marked
ternary coefficient map has rank four, not rank at most three.

Thus the generic part of the quadratic exceptional-weight divisor does not
lift to weighted `H22`.  This does not classify lower-dimensional
intersections with the retained chart, determinant, diagonal, or rank-minor
divisors.  It is not a counterexample.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Generic binary section

Put

```text
F=(ej+k^2)(1+ejs^2)-(e+j)^2,
K=C(e,j,s)[k]/(F).
```

The preceding full-field calculation works in `K(lambda)` without splitting
an equation into its `1,k` coefficients.  On the open set where its displayed
denominators are nonzero, it solves `S_13=S_23=0` uniquely for `w,z_6` and gives

```text
S_123 =
 -k (lambda+1)(1+ejs^2) N
 /[(e+j)(lambda-1)D_0 T H].
```

Consequently all three remaining binary Segre equations vanish after imposing
`N=0`.  The resulting rational section lives in the full finite algebra

```text
A=C(e,j,s)[lambda,k]/(N,F),
```

with `A_2` inverted so that the `lambda` relation is monic.  The certificate
below proves, by an exact nonpoint specialization, that neither the opposite
binary diagonal nor the paired ternary rank minors vanish identically on this
section.  Their nonvanishing therefore holds on a nonempty open subset of
`N=0`.

## Exact one-parameter witness

Specialize only

```text
e=1,  j=2,
```

and retain `s` as a transcendental parameter.  Then

```text
Q=3,
R=1+2s^2,
P=9/(1+2s^2),
k^2=(7-4s^2)/(1+2s^2),
```

while the exceptional polynomial becomes

```text
N_s=A_2(s)lambda^2+A_1(s)lambda+A_0(s),

A_2=(s+1)(2s-1)(4s^2+2s-3),
A_1=-2(8s^4+16s^2-3),
A_0=(s-1)(2s+1)(4s^2-2s-3).
```

Its discriminant is

```text
disc_lambda(N_s)=4s^2(448s^4+16s^2-23).
```

The last factor is nonconstant and squarefree.  Hence `N_s` is irreducible
over `Q(s)`.  Its square class is represented by
`448s^4+16s^2-23`.  The numerator and denominator of

```text
k^2=(7-4s^2)/(1+2s^2)
```

are coprime to that squarefree polynomial and have simple roots.  Thus neither
`k^2` nor `k^2/disc_lambda(N_s)` is a square in `Q(s)`.  The standard
quadratic-extension square-class criterion shows that `k^2` does not become a
square after adjoining `lambda`.  In particular, this calculation takes place
over the full field

```text
E_s=Q(s)[lambda,k]
    /(N_s, k^2-(7-4s^2)/(1+2s^2)),
```

not at an algebraic point and not by coefficient splitting.

The verifiers reconstruct the branch equations in `E_s`, solve the two Segre
equations there, and check the third one is zero modulo `N_s`.  They normalize
the first `D01` diagonal to one, set

```text
h_i=-C_{0...010...0},
```

and directly recompute all sixteen marked binary coefficients.  Exactly the
two diagonal coefficients survive.  The iterated field norm of the opposite
diagonal is nonzero; after cancellation its numerator/denominator degree and
numerator endpoint data are

```text
(deg numerator, deg denominator, numerator at s=0, leading coefficient)
  = (24,28,0,12845056).
```

## Paired `D23` rank

For each marked mode `m`, use the coefficient rows indexed by

```text
000, 001, 010, 011
```

in the other three modes.  This gives a fixed `4 x 4` minor `delta_m` of the
one-marked ternary coefficient map.  The verifiers compute each determinant
inside `E_s` and then take its iterated norm to `Q(s)`.  The four exact
signatures are

| marked mode | numerator degree | denominator degree | numerator at `s=0` | leading coefficient |
|---:|---:|---:|---:|---:|
| 0 | 92 | 56 | 2559780258021441 | 1152921504606846976 |
| 1 | 102 | 66 | -70413806736 | 295147905179352825856 |
| 2 | 80 | 60 | 0 | 166020696663385964544 |
| 3 | 84 | 64 | 0 | 2594073385365405696 |

Each leading coefficient is nonzero, so every norm is a nonzero rational
function.  Therefore every `delta_m` is a unit over the generic point of this
slice and all four one-marked maps have rank four.

These are restrictions of the rational global norms on `A`.  All inverted
denominators remain nonzero rational functions after `e=1,j=2`.  If any global
norm vanished identically on `N=0`, its defined specialization would vanish in
`Q(s)`, contrary to the displayed exact signatures.  Thus the opposite binary
diagonal and all four rank minors are generically nonzero on the full
exceptional divisor.  This is a symbolic specialization argument for rational
functions, not finite-field interpolation.

## Relation to the known algebraic point

At `s=2`, the family has

```text
N_s=9(17lambda^2-42lambda+5),  k^2=-1,
```

which is the previously certified algebraic false positive.  That point is
retained as a regression example only.  The present generic conclusion uses
the nonzero polynomials in `Q(s)` above; it is not inferred from the value at
`s=2`.

## Retained boundary

The theorem localizes the standing affine factors

```text
P R k Q (e-j)(e^2-k^2)(lambda^2-1),
```

the `B`-chart and linear-solve factors

```text
H, e, j, s, lambda, T,
```

the leading coefficient `A_2`, the opposite binary diagonal, and the four
displayed rank-minor norms.  Their intersections with `N=0` are not classified
here.  In particular, this theorem closes the generic exceptional divisor,
not every special/projective fibre of component twenty-five.

## Replay

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_generic_false_positive.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_generic_false_positive.py
```

The primary verifier uses subset-dynamic-programming permanents and a direct
Leibniz determinant.  The no-import audit reconstructs the rows independently
with permutation permanents and recursive cofactor determinants.  Both work
over exact characteristic zero, solve over the full quadratic component
algebra, and use no finite-field evidence.
