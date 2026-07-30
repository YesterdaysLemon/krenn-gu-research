# Coordinate-normal reduction on the `b=0` boundary of `q4_211`

## Status

This note gives an exact characteristic-zero reduction on the boundary

```text
b=0,   a c != 0.                                    (1)
```

The first singleton row and its embedded-`P_4` normal coalesce:

```text
u_1=e_3,
h_1=-e_3.
```

That coordinate normal occurs in exactly two remaining row spaces.
Its two target covectors are, up to scale, `e_0^*` and `e_2^*`.
Relative to this fixed pair, the second singleton normal

```text
h_2=(c,0,0,0,-1)
```

can be neither exact disjoint nor exact parallel.  More sharply, it
must occur at the colour-two coordinate-normal mode `B` and at least
one of the other modes `C,D`.

This is a strict boundary reduction, not an exclusion of that adjacent
stratum, all normalized `q4_211`, `P_5 -> Delta_3`, or the global
Krenn--Gu conjecture.  The boundary `c=0,ab!=0` is target-colour
symmetric.

## Exactly two coordinate-normal incidences

The contraction by `u_1=e_3` is an embedded `P_4`, so the
decomposable-`P_4` rank-drop theorem puts `e_3` in at least two of the
four remaining row spaces.

If

```text
L_i^* alpha_i=e_3,
```

then

```text
(e_3,e_3) contract P_5=0
```

and diagonality with the distinguished target-colour-one row gives

```text
alpha_i[1]=0.                                       (2)
```

For any two such incidences, double contraction on the source is still
zero, while on the target it gives

```text
lambda_0 alpha_i[0]alpha_j[0] e_0^3
+lambda_2 alpha_i[2]alpha_j[2] e_2^3=0.             (3)
```

The two pure tensors are independent and both diagonal coefficients
are nonzero.  Since each `alpha_i` is a nonzero vector in
`span(e_0^*,e_2^*)`, equations (3) force the two projective rows to be

```text
{C e_0^*, C e_2^*}.                                 (4)
```

Three incidences are impossible: two of three rows would have the same
type in (4), violating (3).  Thus there are exactly two.  Label them
`A,B` so that

```text
L_A^*e_0^*=e_3,
L_B^*e_2^*=e_3                                      (5)
```

up to nonzero scale.

## The common ternary support

Put

```text
k=e_0+c e_4,
J=span(e_1,e_2,k).
```

Then

```text
J^perp=span(e_3,h_2),                               (6)
```

and

```text
(u_2,e_3) contract P_5=P_3(e_1,e_2,k).              (7)
```

Using (5), the same source tensor has two simultaneous target images:

```text
(L_A tensor L_C tensor L_D)P_3(e_1,e_2,k)
 =nonzero scalar * e_2^3,                           (8)
```

because the `e_3` row is used at `B`, while

```text
(L_B tensor L_C tensor L_D)P_3(e_1,e_2,k)=0,        (9)
```

because the `e_3` row is used at `A`.

## Excluding exact disjoint incidence

Suppose

```text
h_2 in R_C,R_D,
h_2 notin R_A,R_B.                                  (10)
```

The mixed contraction

```text
Q=(u_0,e_3,h_2) contract P_5
```

is, up to a nonzero common sign, the nondegenerate quadratic on

```text
H=span(e_1+e_2,e_1-e_2,e_0-c e_4)
```

with matrix

```text
M=[
 [ a/2,    0, 1 ],
 [   0, -a/2, 0 ],
 [   1,    0, 0 ]
],
det(M)=a/2.                                         (11)
```

Using the colour-zero `e_3` row at `A`, each complementary pair
`B,C` and `B,D` maps `Q` to a tensor of matrix rank at most one.
Using the colour-two `e_3` row at `B`, each pair `A,C` and `A,D`
maps `Q` to zero, since the distinguished `u_0` row has target colour
zero.

Exactness in (10) makes the restrictions at `C,D` have rank at least
two on `H`: rank one would put all of
`H^perp=span(e_3,u_2)` in the row space and add the forbidden `e_3`
incidence.  Sylvester's inequality applied to the two zero cross pairs
then forces

```text
rank(L_A|H)=1,
rank(L_C|H)=rank(L_D|H)=2.                          (12)
```

In particular `R_A` contains `span(e_3,u_2)`.

Let `L_A^* beta=u_2`.  Symmetry of `(u_2,e_3) contract P_5`, used once
with distinguished colour two and the colour-zero row in (5), and once
with distinguished colour one and `beta`, gives

```text
beta[1]=0.
```

Independence from the `e_3` row then gives `beta[2]!=0`.  Repeating
`u_2` at the distinguished mode and at `A` therefore yields

```text
(L_B tensor L_C tensor L_D)P_3(e_1,e_2,e_3)
 =nonzero scalar * e_2^3.                           (13)
```

Under exactness, all three restrictions in (9) have rank two on `J`:
each row space meets (6) in exactly its selected normal line.  The
zero-`P_3` theorem applied to (9) says that `B,C,D` kill one common
coordinate of the basis `(e_1,e_2,k)`.  Equations (13) rule out
`e_1` and `e_2`, so

```text
L_B(k)=L_C(k)=L_D(k)=0.                             (14)
```

For `C,D`, restriction to `J` has rank two while (14) kills `k`.
Consequently both maps are injective on `E=span(e_1,e_2)`.

Now contract (13) at `B` by the target covector whose pullback is
`e_3`.  The remaining identity is

```text
(L_C tensor L_D)Sym(e_1,e_2)
 =nonzero scalar * e_2 tensor e_2.                 (15)
```

The binary permanent is a nondegenerate rank-two bilinear form.
Two injective maps on `E` preserve its matrix rank, so the left side
of (15) has rank two, while the right side has rank one.  This
contradiction excludes (10).

## Excluding exact parallel incidence

Suppose instead

```text
h_2 in R_A,R_B,
h_2 notin R_C,R_D.                                  (16)
```

Both `A,B` have rank one on `J`, while exactness makes `L_C|J,L_D|J`
rank-three isomorphisms.  At `A`, the target covectors of `e_3` and
`h_2` are `e_0^*` and `(r,p,0)` with `p!=0`; hence

```text
L_A(J)=C e_2.                                       (17)
```

Contract the nonzero pure identity (8) at `A` by `e_2^*`.  A nonzero
one-variable contraction of `P_3` remains a quadratic whose symmetric
matrix has zero diagonal.  Such a nonzero matrix has rank at least
two: its three principal `2 x 2` minors are the negatives of the
squares of its three off-diagonal entries.

The two isomorphisms `L_C|J,L_D|J` preserve that matrix rank, but the
target of the contracted (8) is the rank-one tensor
`e_2 tensor e_2`.  This contradiction excludes (16).

If the `h_2` containment set has any other placement, it meets
`{A,B}` but is not exactly `{A,B}`; selecting two incidences gives an
adjacent pair.

## The colour-two coordinate-normal mode is necessarily common

Suppose for a contradiction that `h_2 notin R_B`.  Since exact
disjoint and exact parallel incidence are excluded, `h_2` occurs at
`A` and at least one of `C,D`.

Now every restriction in the zero identity (9) has rank at least two
on `J`: the mode `B` contains only `e_3` from (6), while `C,D` may
contain `h_2` but cannot contain `e_3`.  The zero-`P_3` theorem makes
all three restrictions the same coordinate plane.  In particular,
both `C,D` have rank two on `J`, so both contain `h_2`, and all three
maps kill one common coordinate

```text
q in {e_1,e_2,k}.                                   (18)
```

The restriction at `A` has rank one on `J` because it contains both
rows in (6).  In the nonzero identity (8), the two maps at `C,D` kill
`q`.  Hence every surviving monomial assigns `q` to `A` and assigns
the other two coordinate factors to `C,D`.  Nonvanishing requires
`L_A(q)!=0`, and the remaining two-mode image is a nonzero pure tensor.

But each of `L_C,L_D` has rank two on `J` and kills exactly `q`, so it
is injective on the complementary coordinate two-plane.  The remaining
two-mode source tensor is the nondegenerate binary permanent on that
plane.  Two injective maps preserve its matrix rank two, contradicting
the pure target rank one.  Therefore

```text
h_2 in R_B.                                         (19)
```

Exact parallel incidence has already been excluded, so `h_2` also
occurs at `C` or `D`; interchange them and take

```text
h_2 in R_B,R_C.                                     (20)
```

There are only two remaining incidence architectures:

1. `h_2 in R_A` as well, with possible further containment at `D`; or
2. `h_2 notin R_A`.  Then the nonzero decomposable-`P_3` theorem
   applied to (8) forces `h_2 in R_D`, so the exact set is
   `{B,C,D}`.  Contracting the simultaneous zero tensor

   ```text
   (u_0,e_3) contract P_5
   ```

   at `C,D` by their `h_2` rows uses

   ```text
   (u_0,e_3,h_2,h_2) contract P_5=-2c(e_1+e_2)
   ```

   and forces

   ```text
   L_A(e_1+e_2)=0.                                  (21)
   ```

Thus the surviving boundary is a marked adjacent chart with a fixed
common mode `B`; if the other coordinate-normal mode is not common,
it lies on the explicit kernel (21).

## Verification

Run:

```text
python verify_p5_q4_211_b0_coordinate_normal.py
python audit_p5_q4_211_b0_coordinate_normal.py
```

The primary verifier differentiates (7), (11), (13), and (21), checks
the annihilators, and verifies the zero-diagonal and binary quadratic
rank bounds.  The
independent audit reconstructs the contractions and projective target
rows over `F_5,F_7`.  It enumerates no ambient maps or Grassmannians.
The finite-field calculations audit the formulas; the proof above is
over `C`.
