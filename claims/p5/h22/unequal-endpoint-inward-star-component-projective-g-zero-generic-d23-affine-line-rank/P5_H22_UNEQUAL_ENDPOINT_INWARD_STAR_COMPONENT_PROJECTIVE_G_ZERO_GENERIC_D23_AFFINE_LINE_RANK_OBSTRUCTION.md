# Component twenty-five's `g=0` projective sheets: generic `D23` closure

## Status

**Exact characteristic-zero projective-sheet theorem.**  On both homogeneous
leaf sheets

```text
a=1,  g=0,  es=+1 or es=-1,
```

the generic finite-`D23` weighted-`H22` fibre is empty.  The complete
normalized binary incidence is an affine line, not a unit ideal.  Every point
of that line is nevertheless a false positive: two exact paired-`D01`
one-marked minors cover it and force rank four.

This theorem works over `Q(s,k,lambda)`.  Every special finite weight,
including `lambda=0,+1,-1`, weight infinity, special component-parameter
divisors such as `k=0`, the other projective leaf hyperplane and its
intersections, and arbitrary source/ambient/projective compactifications
remain separate and **UNKNOWN**.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Legal sign-sheet transfer

Simultaneously swap the ambient pairs `X0<->X1` and `X2<->X3`.  This fixes
`A,B`, sends `C,D` to `-C,-D`, and carries the `es=1` basis at `(-s,-k)` to
the `es=-1` basis at `(s,k)`, with source-row signs

```text
d=(1,1,-1,-1)                                      (1)
```

on the alpha rows.  Invert the homogeneous weight.  For every marked binary
word `w`, the verifier checks the exact identity

```text
d_w C_w^-(lambda)=lambda C_w^+(1/lambda),          (2)
```

where `d_w` is the product of the signs in (1) over the alpha positions.
The same ambient swap and target coordinate scaling identify the paired
`D01` one-marked maps up to invertible row/column operations.  Thus it is
enough to classify the `es=1` sheet.

## Complete normalized binary incidence

Use the adapted `es=1` basis from the preceding projective-`D01` theorem and
finite weight

```text
(x,e) -> (x0,x1,lambda*x2+x3,e).                   (3)
```

Let `C_w` be its sixteen canonical extension coefficients.  Normalize
`C_0000=1`.  The ten fixed-vertex Segre equations are

```text
C_w C_0000^(|w|-1)=product_{i in w} C_{e_i},
2 <= |w| <= 3.                                    (4)
```

Exact characteristic-zero Groebner reduction proves that (4), together with
the normalization, is precisely one affine line.  Put

```text
X=s+2(1-lambda)t.                                  (5)
```

Then every solution, and no others, is

```text
z0=X/[2s(lambda-1)],
z1=X[ks(lambda-1)+lambda+1]/[2s(lambda-1)(lambda+1)],
z2=1/[2(lambda-1)],
z3=X/[2(lambda+1)],
z4=0,
z5=kX/[2(lambda+1)],
z6=t/s-kX/[2(lambda+1)],
z7=t.                                               (6)
```

The forced marking is independent of `s,k,t`:

```text
h=(-1,-1,-1,-(lambda+1)/(lambda-1)).               (7)
```

After (7), all fourteen mixed `D23` coefficients vanish, the first diagonal
is one, and the opposite diagonal is

```text
-(lambda+1)[s+4(1-lambda)t]/[s(lambda-1)].         (8)
```

Thus the binary incidence is genuinely populated on a dense open subset.

## Paired rank obstruction

Project the same marked rows in the paired `D01` direction.  For mode three,
rows `(0,3,4,7)` of the one-marked map have determinant

```text
8k(lambda+1)^2 X/[s^6(lambda-1)^3].                (9)
```

Hence every point with `X!=0` has rank four.  The only residual point is

```text
t=s/[2(lambda-1)].                                 (10)
```

At (10), rows `(0,4,5,6)` of the mode-zero one-marked map have determinant

```text
k^2.                                                (11)
```

This is a unit over `Q(s,k,lambda)`.  Equations (9)--(11) cover the complete
affine line, including points where (8) vanishes, so no generic finite `D23`
binary incidence lifts to weighted `H22`.

## Independent audit and replay

The primary uses permutation permanents, a grevlex ideal comparison, and the
linear/rank cover (9)--(11).  The audit imports no project code, reconstructs
permanents by subset dynamic programming, compares the incidence ideal in
reverse-variable grevlex order, and replaces (9) by the independent mode-two minor

```text
-(lambda+1)X^2/[s^4(lambda-1)].                    (12)
```

It then independently repeats the residual minor (11).

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_projective_g_zero_generic_d23_affine_line_rank_obstruction.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_projective_g_zero_generic_d23_affine_line_rank_obstruction.py
```

Both calculations are exact in characteristic zero.  No finite-field output
is used as proof.
