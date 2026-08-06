# Weighted `H22` on the disjoint mixed-star component: working note

## Status

This is a superseded exploratory handoff, not a theorem.  The
determinantal route proposed below has now been completed over
characteristic zero in
[`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
The calculations here are retained as provenance for the modular
pattern and the failed broad elimination.

The eighth pure-`P_4` component is proved in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md),
and its generic marked `H31` incidence is excluded in
[`P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
Its generic weighted `H22` incidence is now closed on a dense open set
by the theorem linked above.
Subsequent exact boundary theorems close `r=+/-1`, twelve
parameter-pivot branches, the principal coupled slope divisor, and four
rational sheets `af=+/-1,a phi=+/-1`.  The last package also records an
intrinsic content factorization of all seven selected `D_23` maximal
minors:
[`P5_H22_DISJOINT_MIXED_STAR_AF_APHI_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_AF_APHI_BOUNDARY_OBSTRUCTION.md).
The compactified endpoint `r=0` is closed as well, together with an
intrinsic content ledger for the seven selected `D_01` maximal minors
and their rank pivot:
[`P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md).
A further coefficient normalization closes a new irreducible quadratic
component branch by full unsplit two-minor ideals in both directions:
[`P5_H22_DISJOINT_MIXED_STAR_COEFFICIENT_QUADRATIC_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COEFFICIENT_QUADRATIC_BOUNDARY_OBSTRUCTION.md).
Three rational slope graphs are subsequently closed by six unsplit
identities; one real mode-zero degeneration is repaired by the
mode-one `0457` minor:
[`P5_H22_DISJOINT_MIXED_STAR_LINEAR_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_LINEAR_SLOPE_BOUNDARY_OBSTRUCTION.md).
The exact source-torus quotient reduces the dense component base to the
slice `f=1`, and the remaining certificate factors and null calculations
are separated in the current frontier ledger:
[`P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md`](P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md),
[`P5_H22_DISJOINT_MIXED_STAR_CERTIFICATE_DIVISOR_FRONTIER.md`](P5_H22_DISJOINT_MIXED_STAR_CERTIFICATE_DIVISOR_FRONTIER.md).

No computation described below proves a statement over `C`.  In
particular, several direct characteristic-zero Groebner calculations
reached their time limits.  A timeout is recorded as a null result, not
as evidence that an ideal is or is not the unit ideal.

## Finite-field structure

Use the component family

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1 = 0
```

and mark the four plane bases by

```text
beta_i(t)=beta_i+t_i alpha_i.
```

For each weighted source direction `D_01^r` and `D_23^r`, the exploratory
script exhausts every affine marking and every genuine projective
binary-extension direction at one generic point in each of `F_11` and
`F_13`.  It uses exact modular permanent evaluation and row reduction.

At slope `r=2`, the results are:

| field | component point `(a,b,f,phi)` | `D_01` survivors | `D_23` survivors |
|---|---:|---:|---:|
| `F_11` | `(1,2,7,3)` | 5 | 10 |
| `F_13` | `(1,3,5,10)` | 5 | 12 |

Every surviving mixed coefficient matrix has rank seven and therefore
a single projective extension direction.  The marking loci have a
strikingly small form:

```text
D_01:  t_1 t_2 = 0,
D_23:  t_1 = t_2 = t_3 = 0.
```

For every survivor, the mode-zero one-marked contraction has rank four.
For `D_01`, at least one of the row minors `0137` and `0157` is nonzero;
for `D_23`, both are nonzero at the two tested points.

Run the two exact finite-field censuses with:

```text
python \
  explore_p5_h22_disjoint_mixed_star_modular.py 11 2

python \
  explore_p5_h22_disjoint_mixed_star_modular.py 13 2
```

These censuses are corroboration only.  Two fields and one slope do not
establish the generic characteristic-zero statement.

## Characteristic-zero attempt

The natural direct formulation is a Fitting incidence over

```text
K=C(a,b,f,r)[phi]/(Phi).
```

It imposes the fourteen mixed binary coefficients, normalizes the first
diagonal coefficient, inverts the second, and adds selected `4 x 4`
minors of the mode-zero one-marked map.  The unsplit ideals and most
marking-chart saturations were too expensive for the current Groebner
ordering and timed out.

Two smaller `D_23` subcalculations did reduce to the unit ideal: the
chart `t_3 != 0`, and the Fitting incidence on
`t_1=t_2=t_3=0`.  They do not cover the unresolved `t_1 != 0` and
`t_2 != 0` charts, so they are not a proof and have not been promoted
to theorem artifacts.

## Best next step

The modular loci suggest replacing broad elimination by symbolic linear
algebra on the `14 x 8` mixed coefficient matrix:

1. choose a generically nonzero `7 x 7` pivot;
2. express its kernel line by maximal minors or Cramer coordinates;
3. factor the remaining mixed equations modulo `Phi`;
4. derive `t_1 t_2=0` for `D_01` and
   `t_1=t_2=t_3=0` for `D_23`;
5. evaluate a small pair of mode-zero Fitting minors on those exact
   marking strata.

That would turn the observed finite-field collapse into a short
function-field argument and avoids a brute-force construction search.
Those identities are now derived and independently replayed in the
theorem package.  Special parameter/slope divisors, projective
boundaries, component exhaustiveness, and the global prize conjecture
remain open.
