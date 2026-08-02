# Component twenty-five's sparse paired-`D23` two-minor cover

## Status

**Exact characteristic-zero necessary-divisor reduction.**  On component
twenty-five's normalized ordinary finite-`D01`, `B=0`, `N=0` exceptional
sheet, retain the genuine complement

```text
G != 0,  A_0 A_2 != 0,
```

and every standing, chart, and linear-solve nonvanishing assumption from the
full-field and opposite-diagonal packages.  If all four paired-`D23`
one-marked maps have rank at most three, then the point lies in the union

```text
w=0,
k=1,
Tbar=0 and A=0,                                    (1)
```

where, after normalizing `s=1` and writing `a=es`, `b=js`,

```text
Tbar=(1-b)lambda-(1+b),
A=a(lambda+1)-k(lambda-1).                         (2)
```

This is a necessary three-branch cover, not a classification of any branch
in (1).  The zero divisor `w=0`, the divisor `k=1`, and the residual algebraic
fibres described below remain **UNKNOWN**.  No claim about their intersection
with `G!=0` is made.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Removing the marking from the rank calculation

For a fixed marked mode, the other three binary row pairs enter the
one-marked coefficient map only through their eight binary choices.  Replacing

```text
beta_i -> beta_i+h_i alpha_i
```

in one of those modes applies the invertible triangular matrix

```text
[1 0]
[h 1]
```

to that binary row index.  The tensor product of the three such changes is
invertible.  Therefore the rank of the one-marked map is unchanged by the
`D01` marking.  The marked mode itself is occupied by the arbitrary test row,
so its marking does not enter.  This permits the paired-`D23` rank calculation
to use the original `alpha,beta` pairs.

Put

```text
P=ab+k^2=(a+b)^2/(1+ab),  Q=a+b,
D=(lambda-1)P-(lambda+1)Q,
z_3=1/(2PD).
```

Use the sparse pair bases

```text
(beta_0, alpha_0-Q beta_0),
(beta_1, alpha_1-Q beta_1),
(alpha_2,beta_2),
(alpha_3,beta_3).                                  (3)
```

Writing

```text
u_0=z_4,       v_0=z_0-Qz_4,
u_1=z_5,       v_1=z_1-Qz_5,
```

the certified branch extension gives

```text
z_2=(lambda-1)w,             u_0=-(lambda+1)w,
u_1=z_6-kz_3,

v_0=[P^2 z_3-1/(2(lambda-1))]/(Qk),
v_1=-P(lambda-1)w+aPz_3/k.                         (4)
```

These identities hold in the full quadratic component algebra; `w` is the
already-unique `K`-valued section coordinate and is not assumed to descend to
the base field.

## Two exact sparse minors

For mode `1`, hold `alpha_2` fixed and take the four corner choices in the
mode-`0` and mode-`3` pairs of (3).  Row differencing turns the resulting
`4 x 4` determinant into

```text
delta_1 = -8 b P z_2 (lambda-1)(lambda+1)
          (b u_0+z_2)
          (P(lambda+1)z_3-(lambda-1)v_0).
```

Substitution of (4) gives

```text
delta_1 = -8 b P^2 z_3/k
          (lambda-1)^2(lambda+1)^2 w^2(k-1) Tbar.  (5)
```

For mode `3`, hold `beta_0` fixed and take the four corner choices in the
mode-`1` and mode-`2` pairs.  The analogous determinant is

```text
delta_3 = 8 P u_0(lambda+1) A
          (aPz_2+a v_1+P u_1-Pz_6)
          (k(lambda-1)u_0+(lambda+1)z_2),
```

and (4) gives

```text
delta_3 = 8 P^2 z_3/k
          (lambda+1)^3(lambda-1) w^2(k-1)
          (a^2-k^2) A.                             (6)
```

Rank at most three forces every `4 x 4` minor to vanish, hence in particular
`delta_1=delta_3=0`.  On the retained open chart the numerical factor, `b`,
`P`, `z_3`, `k`, `lambda+/-1`, and `a^2-k^2` are nonzero.  Equations (5)--(6)
therefore imply exactly the necessary cover (1).

The factor `Tbar` is not the already-inverted solve factor
`T=(b-1)lambda-(b+1)`.  The new divisors `w=0` and `k=1` are also retained;
none is silently discarded.

## The `Tbar=A=0` residual

Away from the already-separated `b=0,1` factors, equations (2) give

```text
lambda=(1+b)/(1-b),       k=a/b.
```

After these substitutions the component equation `F=0` and exceptional
weight equation `N=0` have respective cleared numerators

```text
Phi_F = a^3b+a^2b^4-a^2b^2+a^2-ab^3-b^4,

Phi_N = 3a^3b^3-a^3b-a^2b^4+a^2b^2-a^2
        -ab^3-ab+b^4.
```

Their exact resultant is

```text
Res_a(Phi_F,Phi_N)
 = b^9(b-1)^3(b+1)^3
   (3b^6-3b^4-6b^2-2).                             (7)
```

Thus, away from `b=0,+/-1`, this residual branch can only lie over

```text
3b^6-3b^4-6b^2-2=0.                               (8)
```

Equation (8) is a further necessary restriction, not an obstruction: its
fibres, their genuineness condition `G!=0`, and all paired rank minors remain
**UNKNOWN**.

## Retained boundary and replay

The result assumes the normalized ordinary chart and retains all factors

```text
P R k Q (a-b)(a^2-k^2)(lambda^2-1),
H, a, b, lambda, T, A_0, A_2, G,
```

with `R=1+ab` and `H`/`T` as in the preceding packages.  Projective fibres,
the zero denominators used in (4), and all three branches in (1) are outside
the conclusion.

Run:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_d23_sparse_two_minor_cover.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_d23_sparse_two_minor_cover.py
```

The primary uses permutation permanents, exact `4 x 4` determinants, and
polynomial remainder in the quadratic component algebra.  The no-import audit
uses subset-dynamic-programming permanents, recursive cofactor determinants,
even/odd quadratic reduction, and an explicit `6 x 6` Sylvester determinant.
Both use exact characteristic-zero arithmetic.  No finite-field evidence is
used.
