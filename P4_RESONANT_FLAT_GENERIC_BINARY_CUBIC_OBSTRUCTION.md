# The generic flat binary-cubic triangle is impossible

## Status

This is an exact characteristic-zero obstruction for the dense
cross-ratio chart of the last triangle branch in
[`P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md`](P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md).
It uses projective normalization, a two-dimensional adjugate pencil,
and one compound-matrix identity.  It uses no component enumeration
or elimination.

Together with
[`P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md`](P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md),
this proves that a rank-two-relation triangle can survive only where
every row-pair has a zero or repeated projective column.  The
projective parameter sheets of the partner pencil are excluded below
as well.

The collision boundary has since been classified completely in
[`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION.md`](P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION.md).
It contains one balanced `2+2` family, but that family is too small to
be a pure-`P_4` component.  Pure-component exhaustiveness and the
global Krenn--Gu conjecture remain open.

## The flat synchronized problem

Work in the squarefree algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

The zero-holonomy theorem supplies three ordered row-pairs

```text
A_i=(y_i;x_i),                  i=1,2,3,
```

such that

```text
y_i x_j=x_i y_j                for i<j.                            (1)
```

Their triple products depend only on Hamming weight:

```text
Y=y_1y_2y_3,
K=x_1y_2y_3=y_1x_2y_3=y_1y_2x_3,
J=y_1x_2x_3=x_1y_2x_3=x_1x_2y_3,
X=x_1x_2x_3.                                                       (2)
```

Purity and the perfect `R_1 x R_3` pairing give the flag

```text
dim span(Y,K,J)<=2,             X notin span(Y,K,J).               (3)
```

In particular the full coefficient matrix

```text
C=[Y K J X]
```

must have rank at least three.

## Cross-ratio normalization

Suppose `A_1` has four nonzero, projectively distinct columns.
Row `GL_2` and the diagonal source torus put it in the form

```text
y=(1,0,1,1),
x=(0,1,1,lambda),               lambda(lambda-1)!=0.               (4)
```

Write a synchronized partner as

```text
y'=(a,b,c,d),
x'=(e,f,g,h).
```

The six coefficients of `yx'-xy'=0` give

```text
f=a,       e=lambda b,
c=a-b,     d=a-lambda b,
g=a-lambda b,   h=lambda(a-b).                                    (5)
```

Thus every partner lies in the two-dimensional pencil

```text
A(a,b)=aA+bA^#,

y^#=(0,1,-1,-lambda),
x^#=(lambda,0,-lambda,-lambda).                                   (6)
```

This is the useful matrix-pencil translation of the flat connection.
On the dense parameter chart `a_2a_3!=0`, rescale the second and third
row-pairs and write

```text
A_1=A,          A_2=A+tA^#,          A_3=A+uA^#.                   (7)
```

## The binary-cubic coefficient matrix

Use the basis of `R_3` indexed by the omitted source coordinate.
Direct squarefree multiplication gives

```text
C=2[
 -(lambda*t*u+t*u-t-u),
 -(lambda*t*u-1),
 -(lambda*t+lambda*u-lambda-1),
  lambda*(lambda*t*u-lambda*t-lambda*u-t-u+3);

  lambda*t*u-lambda*t-lambda*u-t-u+3,
 -(lambda*t+lambda*u-lambda-1),
 -lambda*(lambda*t*u-1),
 -lambda^2*(lambda*t*u+t*u-t-u);

 -(lambda*t*u-t-u),
  1,
  lambda,
 -lambda^2*(t*u-t-u);

 -(t*u-t-u),
  1,
  1,
 -lambda*(lambda*t*u-t-u)
].                                                                  (8)
```

The last two rows already reveal that `K,J` are independent:

```text
det C[{2,3},{K,J}]=-4(lambda-1) != 0.                              (9)
```

Consequently (3) forces

```text
rank[Y K J]=2.                                                     (10)
```

Define

```text
F =
 lambda^2*t^2*u^2-lambda*t^2-4lambda*t*u+2lambda*t
 -lambda*u^2+2lambda*u+2t+2u-3.                                  (11)
```

One compression minor is

```text
det C[{1,2,3},{Y,K,J}]=8(lambda-1)F.                              (12)
```

Thus (10) implies `F=0`.

## The compound-matrix collapse

The surprise is that the same scalar controls every `3 x 3` minor of
the full binary-cubic matrix.  Order row and column triples as

```text
012, 013, 023, 123.
```

Put

```text
P=lambda^2*t*u+2lambda*t*u-2lambda*t-2lambda*u-t-u+3,
Q=2lambda*t*u-lambda*t-lambda*u+t*u-2t-2u+3.
```

Then the third compound matrix factors exactly as

```text
C_3(C)=8F N,                                                       (13)
```

where

```text
N=[
 -(lambda*t-1)(lambda*u-1), -lambda*P, -lambda^2*Q,
 -lambda^3*(t-1)(u-1);

 -lambda*(t-1)(u-1), -lambda*Q, -lambda*P,
 -lambda*(lambda*t-1)(lambda*u-1);

 0, lambda*t*u*(lambda-1), lambda*(lambda-1)(t+u),
 lambda*(lambda-1);

 lambda-1, lambda*(lambda-1)(t+u),
 lambda^2*t*u*(lambda-1), 0
].                                                                  (14)
```

Equations (12)--(14) are a cofactor identity, not a radical or
set-theoretic computation.  Since purity forces `F=0`, all `3 x 3`
minors of `C` vanish:

```text
rank C<=2.                                                         (15)
```

But (3) says `X` escapes `span(Y,K,J)`, and (9)--(10) say that span
already has dimension two.  Hence `rank C=3`, contradicting (15).

Therefore the affine part of the generic cross-ratio chart (4), (7)
is empty.

## The projective pencil sheets

It remains to check that the affine parameterization (7) did not
discard a solution at infinity.  By symmetry, first take

```text
A_2=A^#,                 A_3=A+uA^#.
```

The coefficient matrix is the leading `t`-coefficient of (8):

```text
C_infinity=2[
 -(lambda*u+u-1), -lambda*u, -lambda,
 lambda*(lambda*u-lambda-1);

 lambda*u-lambda-1, -lambda, -lambda^2*u,
 -lambda^2*(lambda*u+u-1);

 -(lambda*u-1), 0, 0, -lambda^2*(u-1);

 -(u-1), 0, 0, -lambda*(lambda*u-1)
].                                                                  (16)
```

Two compression minors are

```text
-8lambda^2(lambda*u-1)(lambda*u^2-1),
-8lambda^2(u-1)(lambda*u^2-1).                                   (17)
```

Since `lambda!=1`, the factors `lambda*u-1` and `u-1`
cannot vanish together.  Purity therefore forces

```text
lambda*u^2=1.                                                      (18)
```

Every `3 x 3` minor of `C_infinity` is divisible by the
left side of (18), so (18) gives

```text
rank C_infinity<=2.                                                (19)
```

On the other hand,

```text
det C_infinity[{0,2},{Y,K}]
  =-4lambda*u(lambda*u-1).                                        (20)
```

It is nonzero under (18): `u=1` or `lambda*u=1` would each imply
`lambda=1`.  Hence `span(Y,K,J)` still has dimension two, and the
escape condition for `X` contradicts (19).

Finally, if both partners lie at infinity,

```text
A_2=A_3=A^#,
```

then one `3 x 3` compression minor is already

```text
det C[{0,1,2},{Y,K,J}]=-8lambda^4 != 0.                            (21)
```

Thus the projective pencil sheets are empty too.  Permuting the three
modes shows:

> In any surviving flat rank-two-relation triangle, none of the
> three ordered row-pairs can have four nonzero, projectively
> distinct source columns.

## What remains

The residual symbolic boundary consists only of row-pairs whose four
source columns include zero or repeated projective points, and their
intersections across the three modes.  These are lower-support and
collision strata in the moduli space of four points on `P^1`.  They
should be attacked by stable reduction of the four-point
configuration and its induced degeneration of the adjugate pencil,
rather than by a new ambient search.

## Verification

Run:

```text
python verify_p4_resonant_flat_generic_binary_cubic.py
python audit_p4_resonant_flat_generic_binary_cubic.py
```

The primary verifier derives the synchronization pencil, recomputes
the squarefree triple products, and checks (8)--(21) over rational
function fields.  The independent audit starts from the six linear
synchronization equations and the displayed coefficient matrices,
then checks the rank flags and compound divisibilities separately.
Both scripts are exact symbolic proof replays; neither searches for
solutions.
