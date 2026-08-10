# Ternary-Segre obstruction for exact disjoint `a=0` incidence

## Status

This note exactly excludes the last open incidence type of normalized
`q4_211` over `C` on

```text
a=0,   b c != 0.                                    (1)
```

Assume exact disjoint singleton-normal incidence:

```text
h_1 in R_A,R_B only,
h_2 in R_C,R_D only.                                (2)
```

The third embedded `P_4` has a zero marked corner.  Rank-one
factorization makes one marked `P_3` slice vanish.  Three evaluations
of that slice force the other three restricted row spaces into one
coordinate hyperplane.  The surviving tensor is then an order-three
permanent.  Its exact decomposable-restriction theorem forces all three
spaces to be planes, and a binary Segre corner calculation contradicts
the absence assumptions in (2).

Thus exact disjoint incidence is empty on (1).  Combined with the
adjacent Grassmannian obstruction and the parallel-to-adjacent
reselection theorem, the entire `a=0` face is empty.

This theorem concerns normalized `q4_211`.  Its combination with the
generic and `b=0,c=0` theorems gives a complete normalized-`q4_211`
exclusion, but it does not by itself prove `P_5 -> Delta_3` impossible
or resolve the arbitrary-order Krenn--Gu conjecture.

## The third `P_4` and its marked rows

Put

```text
s=e_1+e_2,
J=span(e_0,s,e_3,e_4)=h_0^perp,
h_0=e_1-e_2.                                       (3)
```

At `a=0`,

```text
u_0 contract P_5=P_4(e_0,s,e_3,e_4),               (4)
```

and the four remaining maps send (4) to the nonzero pure tensor
`lambda_0 e_0^4`.

Rescale the singleton coordinates.  In dual coordinates

```text
(E,S,P,Q)
```

on `J`, the restrictions of the two singleton normals are

```text
f=E-P,   h=E-Q.                                     (5)
```

For each remaining mode set

```text
U_i=R_i restricted to J,   dim(U_i) in {2,3}.       (6)
```

The lower bound follows because restriction to a hyperplane drops the
rank-three ambient map by at most one.  Moreover,

```text
dim(U_i)=2 iff h_0 in R_i.                           (7)
```

The exact incidence (2) gives

```text
f in U_A,U_B,
h in U_C,U_D.                                       (8)
```

Let `T=P_4` on `J`.  Since its restricted image is nonzero and
decomposable, there are nonzero linear forms `alpha_i on U_i` and a
nonzero scalar `lambda` such that

```text
T(r_A,r_B,r_C,r_D)
 =lambda alpha_A(r_A)alpha_B(r_B)
         alpha_C(r_C)alpha_D(r_D).                  (9)
```

Direct permanent evaluation gives the zero marked corner

```text
T(f,f,h,h)=0.                                       (10)
```

Hence at least one of

```text
alpha_A(f), alpha_B(f), alpha_C(h), alpha_D(h)
```

vanishes.  Swapping `A,B`, swapping `C,D`, and interchanging the two
singleton coordinates reduce all cases to

```text
alpha_A(f)=0.                                       (11)
```

Therefore

```text
T(f,U_B,U_C,U_D)=0.                                 (12)
```

## The zero slice forces one coordinate hyperplane

For an arbitrary row `z=(z_E,z_S,z_P,z_Q)`, the same four-dimensional
permanent gives

```text
T(f,f,h,z)=2z_S,
T(f,h,f,z)=2z_S,
T(f,z,h,h)=2z_S.                                    (13)
```

Use the first identity with `f in U_B,h in U_C` and arbitrary
`z in U_D`.  Equation (12) gives `z_S=0`, so `U_D` is contained in
`S^perp`.  The other two placements give the same conclusion for
`U_C,U_B`:

```text
U_B,U_C,U_D subset X^*=span(E,P,Q).                 (14)
```

At least one row of `U_A` has nonzero `S` coordinate, or (4) would
have zero image.  Since all rows in (14) have zero `S` coordinate, the
permanent separates:

```text
T(r,b,c,d)
 =r_S P_3(b,c,d),                                   (15)
```

where the ternary permanent uses coordinates `(E,P,Q)`.

Take `r in U_A` with `r_S!=0`.  The corresponding slice of the
nonzero decomposable tensor (9) is a nonzero decomposable restriction
of `P_3` through `U_B,U_C,U_D`.  Every one of these spaces has
dimension at least two.  The exact theorem
[`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`](../../p3/restrictions/P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md)
therefore gives

```text
dim(U_B)=dim(U_C)=dim(U_D)=2.                        (16)
```

By (7), all three ambient row spaces contain `h_0`.

This makes the exact absences in (2) visible after restriction.  For
example, if `h in U_B`, some ambient row in `R_B` differs from `h` by
a multiple of `h_0`; since `h_0 in R_B`, this would put `h_2` itself
in `R_B`, contrary to (2).  Consequently

```text
h notin U_B,
f notin U_C,U_D.                                    (17)
```

## The binary Segre corner

Choose bases of the three planes in `(E,P,Q)` as

```text
U_B=span(f,b),   b=(0,b_P,b_Q),
U_C=span(h,c),   c=(0,c_P,c_Q),
U_D=span(h,d),   d=(0,d_P,d_Q).                     (18)
```

The first coordinate of each moving row is removed by its marked row.
The rows `b,c,d` are nonzero.  Conditions (17) are exactly

```text
b_P+b_Q != 0,
c_P+c_Q != 0,
d_P+d_Q != 0.                                      (19)
```

In the binary bases (18), the restricted `2x2x2` tensor has
coefficients

```text
Q_000=2,
Q_001=-(d_P+d_Q),
Q_010=-(c_P+c_Q),
Q_011=c_Pd_Q+c_Qd_P,

Q_100=-2b_P,
Q_101=b_Pd_Q+b_Qd_P,
Q_110=b_Pc_Q+b_Qc_P,
Q_111=0.                                           (20)
```

Because `Q_000!=0`, all three lower coordinates of a hypothetical
rank-one factorization are nonzero.  Since `Q_111=0`, one of its three
upper factor coordinates must vanish.

If the upper coordinate vanishes at `C`, the whole `C=1` slice
vanishes, in particular

```text
Q_010=-(c_P+c_Q)=0,
```

contrary to (19).  The `D` case is identical.

It remains to suppose that the upper coordinate vanishes at `B`.
Then the `B=1` slice of (20) is zero.  Successively,

```text
Q_100=0  => b_P=0,
Q_101=0  => b_Q d_P=0,
Q_110=0  => b_Q c_P=0.                              (21)
```

Equation (19) gives `b_Q!=0`, hence

```text
c_P=d_P=0,
c_Q d_Q != 0.                                      (22)
```

But the `B=0` matrix is now

```text
[ 2    -d_Q ]
[-c_Q    0  ],
```

whose determinant is `-c_Q d_Q!=0`.  It has rank two, contradicting
the assumed rank-one tensor.

All upper-coordinate cases are impossible.  This contradicts (9) and
proves that exact disjoint incidence cannot occur on (1).

## Consequence

On `a=0,bc!=0`, the two singleton-normal containment sets have only
the standard parallel, adjacent, and exact-disjoint selections.
Parallel incidence reselects as adjacent.  Adjacent incidence is
excluded by
[`P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md`](P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md),
and exact disjoint incidence is excluded here.  Hence the complete
`a=0` face is empty.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_a0_disjoint_p3.py
python claims/p5/frontier/audit_p5_q4_211_a0_disjoint_p3.py
```

The primary verifier reconstructs (10), (13), (15), all eight
coefficients in (20), and the final nonzero determinant.  It also pins
the exact ternary decomposable-restriction theorem used in (16).  The
independent audit checks the slice identities over `F_5,F_7` and
enumerates only the small ternary plane triples satisfying (18)--(19);
none has a nonzero rank-one permanent image.  It enumerates no ambient
maps or four-dimensional Grassmannians.  The finite-field calculation
audits the formulas and final Segre case split; the proof above is over
`C`.
