# Proper cut supports cannot occur in a nonresonant triangle

## Status

This is an exact characteristic-zero boundary theorem for the
rank-two-relation triangle reduced to cuts in
[`P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md`](P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md).
It closes every proper bridge-support boundary by two coordinate
normal forms and one perfect-pairing inequality.  No elimination or
component search is used.

Combined with the full-support theorems

- [`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md),
- [`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md),

it proves:

```text
the complete nonresonant all-rank-two-relation triangle is empty.   (1)
```

Thus the all-rank-two-relation triangle frontier is now confined to
the resonant divisor where the multiplicative projective holonomy is
trivial.  Component exhaustiveness, the other lower-pair-rank strata,
and the global Krenn--Gu conjecture remain open.

## Why there are only two boundary supports

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

The cut theorem gives each nonzero bridge `Q_ij` one of two forms.

For a `1+3` cut it is supported on the three edges of a coordinate
triangle.  A proper nonzero support therefore has one or two edges.

For a `2+2` cut it is an outer product across a coordinate bipartition:

```text
q=(a_pX_p+a_qX_q)(b_rX_r+b_sX_s).                                 (2)
```

The support size is the product of the two factor support sizes, so it
is `4`, `2`, or `1`; a proper support again has at most two edges.

Two edges in either cut type necessarily share one coordinate.
Consequently every proper nonzero bridge is, up to source-coordinate
permutation and scaling, exactly one of:

```text
q=X_0X_1,                                                           (3)

q=X_0(alpha X_1+beta X_2),       alpha beta != 0.                  (4)
```

## The single-edge bridge

For (3),

```text
Ann_R1(q)=span(X_0,X_1)=:W.                                        (5)
```

Suppose a plane `V` has a rank-three product with `W` and the unique
kernel tensor has rank two.  Choose a basis `(v,w)` of `V` so that the
kernel relation is

```text
X_0v+X_1w=0.                                                        (6)
```

Comparing squarefree degree-two coefficients in (6) gives

```text
v_2=v_3=w_2=w_3=0,              v_1+w_0=0.                         (7)
```

Thus `V subset W`.  But then

```text
WV subset C X_0X_1,
```

so `dim(WV)<=1`, contradicting the assumed value three.

Hence a single-edge bridge cannot occur.

## The two-edge star

Normalize (4) to

```text
b=alpha X_1+beta X_2,
b_bar=alpha X_1-beta X_2,

q=X_0b.                                                             (8)
```

Then

```text
Ann_R1(q)=span(X_0,b_bar)=:W
          subset H_3={z_3=0}.                                      (9)
```

As before, let `V` be a rank-three partner of `W` with a unique
rank-two relation.  In a suitable basis `(v,w)` of `V`,

```text
X_0v+b_bar w=0.                                                     (10)
```

The `X_0X_3` coefficient in (10) is `v_3`.  The `X_1X_3` and
`X_2X_3` coefficients are respectively `alpha w_3` and
`-beta w_3`.  Since `alpha beta!=0`,

```text
v_3=w_3=0,
```

and therefore

```text
V subset H_3.                                                       (11)
```

Now take a triangle bridge `Q_12=q`.  The cut reduction gives
`U_3=W`.  Apply (11) to the rank-three pairs `(U_3,U_1)` and
`(U_3,U_2)`.  All three triangle planes lie in `H_3`.

Every surviving monomial of the nonzero pure `P_4` restriction must
take source coordinate three from the remaining mode zero.  Hence

```text
P_4|_(U_0,U_1,U_2,U_3)
 =(X_3|U_0) tensor P_3|_(U_1,U_2,U_3).                             (12)
```

The `P_3` restriction is nonzero and pure.  Multiplication in the
three-variable squarefree algebra is a perfect pairing

```text
R_2 tensor R_1 -> R_3=C.
```

If `r_ij=dim(U_iU_j)`, restricting this pairing to
`U_iU_j` and the opposite two-plane gives rank at least

```text
r_ij+2-3=r_ij-1.
```

Purity makes the flattening rank one, so

```text
r_ij<=2,                                                            (13)
```

contradicting the triangle hypothesis `r_ij=3`.

Thus a two-edge bridge cannot occur either, proving (1).

## Geometric interpretation

The support degeneration is a Schubert phenomenon.  A two-edge cut
selects a coordinate hyperplane, and the kernel relation transports
that hyperplane incidence to both neighboring planes.  The apparent
four-variable triangle is therefore a suspension from the
three-variable squarefree algebra.  Poincare duality there supplies
the rank obstruction (13).

This is adjacent to the use of Artinian Gorenstein pairings and
Lefschetz maps in Maeno--Watanabe,
[Lefschetz elements of Artinian Gorenstein algebras and Hessians of
homogeneous polynomials](https://arxiv.org/abs/0903.3581), and to the
study of exact zero divisors in Eddings--Vraciu,
[Rings for which general linear forms are exact zero
divisors](https://arxiv.org/abs/2407.16000).  Neither cited paper
states this triangle obstruction; equations (3)--(13) are its full
proof.

## Verification

Run:

```text
python verify_p4_nonresonant_degenerate_cut_triangle_obstruction.py
python audit_p4_nonresonant_degenerate_cut_triangle_obstruction.py
```

The primary verifier checks both catalecticants and annihilators,
solves the two kernel relations coefficient by coefficient, and
replays the three-variable pairing.  The independent audit uses a
different singleton and unequal star weights.  These are small exact
proof replays, not searches.
