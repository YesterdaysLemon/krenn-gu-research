# Algebraic false positive on component twenty-five's exceptional finite-`D01` `B` divisor

## Status

**Exact characteristic-zero algebraic-point theorem.**  The exceptional
quadratic weight divisor `N(lambda)=0` retained by the corrected full-field
`B=0` reduction is populated by genuine normalized binary survivors.  At the
explicit algebraic component point below, however, all four paired finite-
`D23` one-marked maps have rank four.  The survivors therefore do not lift to
weighted `H22` restrictions and are not counterexamples.

This is a point theorem, not a generic closure of `N=0`.  Other points of the
exceptional divisor, the determinant divisors, and the standing affine-chart
boundary remain **UNKNOWN**.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Algebraic component point

Set

```text
(e,j,s)=(1,2,2),       k^2=-1,
17 lambda^2-42 lambda+5=0.                           (1)
```

Work in

```text
E=Q[lambda,k]/(17lambda^2-42lambda+5,k^2+1).
```

At this point

```text
P=ej+k^2=1,       Q=e+j=3,       R=1+ejs^2=9,
PR-Q^2=0,
N(lambda)=9(17lambda^2-42lambda+5)=0.                (2)
```

All standing factors are nonzero.  In particular,

```text
e-j=-1,       e^2-k^2=2,
lambda(lambda^2-1) != 0,
T=3lambda-5 != 0,       H=3lambda+15 != 0.           (3)
```

Thus this point is on the determinant-open part of the exceptional divisor,
not on one of the separately retained linear or chart boundaries.

## Exact `B` section and marking

Solving the two linear Segre equations over the full field `E`, without
splitting coefficients in the basis `1,k`, gives

```text
w   =-k(145+17lambda)/1280,
z_6 =-k(19+51lambda)/320.                            (4)
```

The complete extension is

```text
z_0= k(119+391lambda)/640,
z_1= k(61-51lambda)/160,
z_2= k(15-17lambda)/128,
z_3=(-127+17lambda)/640,
z_4= k(35+51lambda)/320,
z_5= k(89-119lambda)/640,
z_6=-k(19+51lambda)/320,
z_7= k(-21+51lambda)/160.                            (5)
```

The original `B` equation and all four forced extension equations vanish.
The third residual Segre equation vanishes modulo (1), as predicted by the
terminal factor `N`.

Normalize `C_0000=1`.  The four singleton equations uniquely force

```text
(h_0,h_1,h_2,h_3)
 =(0,-(33+17lambda)/160,-2,k(3-17lambda)/4).         (6)
```

After replacing every complete projected row by

```text
beta'_i -> beta'_i+h_i alpha'_i,
```

all fourteen mixed finite-`D01` coefficients vanish and the two pure
diagonals are

```text
(C_0000,C_1111)=(1,k(1+lambda)/10).                 (7)
```

The absolute field norm of the second value is

```text
Norm_E/Q(k(1+lambda)/10)=256/180625 != 0.            (8)
```

Hence this is a genuine binary survivor, not a diagonal-zero saturation
artefact.

## Exact paired ternary obstruction

Use the same completely marked lifted rows and project them through finite
`D23`.  For each marked mode `0,1,2,3`, form the `4 x 4` minor of the
one-marked map on the first four lexicographic binary words in the other
three modes,

```text
000,001,010,011.                                     (9)
```

The four determinant norms in mode order are

```text
3346477548867590625/321978368,
 242198579941179669/1710510080,
    371804801417254836/10440125,
   1123047541391554692/1305015625.                  (10)
```

Every number in (10) is nonzero, so every one-marked map has rank four.  A
weighted-`H22` lift would require rank at most three.  Equations (9)--(10)
therefore exclude both conjugate roots of (1), on both embeddings of
`k^2=-1`.

## Boundary and replay

This certificate establishes one exact algebraic false-positive fibre.  It
does not show that the determinants in (10) are uniformly nonzero over the
whole divisor `N=0`, nor does it classify intersections with

```text
e j s lambda T H P R k Q (e-j)(e^2-k^2)(lambda^2-1)=0.
```

Run:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_algebraic_false_positive.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_algebraic_false_positive.py
```

The primary reconstructs the tensor, solves the two linear minors in `E`,
and expands permanents by permutations.  The no-import audit starts from the
explicit section (4)--(6), verifies every defining equation, and evaluates
permanents by subset dynamic programming.  Both use exact characteristic-
zero arithmetic; no finite-field evidence is used.
