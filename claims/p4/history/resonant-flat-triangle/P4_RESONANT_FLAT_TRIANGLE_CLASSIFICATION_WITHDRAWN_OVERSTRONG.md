# WITHDRAWN: overstrong classification of flat rank-two-relation triangles

## Status

**WITHDRAWN.**  The projective-column classification below used full
row `GL_2`, but purity fixes each kernel line and permits only Borel
row gauge.  The displayed balanced `2+2` family and the individual
normal-form identities remain exact; their claimed exhaustiveness and
dimension consequence do not.

The valid one-kernel-zero theorem is
[`P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md`](../../boundaries/rank-two-triangle/resonant/flat-kernel-zero-binary-cubic/P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md),
and the true full-support Borel chart is
[`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](../../boundaries/rank-two-triangle/resonant/flat-generic-binary-cubic/P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md).

The complete Borel classification has now been recovered by a different
support-stratified proof:
[`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](../../classifications/triangle-211/rank-two-relation-triangle-corrected/P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md).
Its survivor is the three-parameter marked family
`U_i=span(a,b+alpha_i*a_bar)` with nonzero sum of the `alpha_i`.  The family
displayed below is the exact `alpha_1=0` slice, not the whole Borel moduli
problem.  This file remains withdrawn as an audit record of the invalid
exhaustiveness argument.

The withdrawn argument had claimed an exact classification of the
zero-additive-holonomy branch left by
[`P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md`](../../classifications/rank-two-triangle/resonant/affine-holonomy-reduction/P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md).
It combines the generic cross-ratio obstruction in
[`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](../../boundaries/rank-two-triangle/resonant/flat-generic-binary-cubic/P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md)
with a finite projective classification of its collision boundary.

The branch is not empty.  Up to source-coordinate permutation,
diagonal source scaling, mode permutation, and row-basis gauge, every
survivor is

```text
U_0=span(a_bar,b_bar),
U_1=span(a,b),
U_2=span(a,b+s a_bar),
U_3=span(a,b+t a_bar),                    s+t!=0,                  (1)
```

for the `2+2` block rows

```text
a=(1,1,0,0),       a_bar=(1,-1,0,0),
b=(0,0,1,1),       b_bar=(0,0,1,-1).                              (2)
```

With rows `(b_bar,a_bar)` on `U_0` and the displayed rows on the
other modes, the restricted permanent is

```text
-4(s+t) x_0 x_1 x_2 x_3.                                        (3)
```

The triangle locus has dimension at most four after restoring the
source torus, whereas every irreducible component of the nonzero pure
incidence has dimension at least five.  Therefore the
all-rank-two-relation triangle cannot be the generic exceptional graph
of a new pure-`P_4` component.

It does not complete the triangle alternative or component
exhaustiveness.

## Projective columns of a row-pair

On the flat branch there are ordered row-pairs

```text
A_i=(y_i;x_i),                  i=1,2,3,
```

obeying

```text
y_i x_j=x_i y_j.                                                (4)
```

Purity gives the binary-cubic flag

```text
dim span(Y,K,J)<=2,             X notin span(Y,K,J),              (5)
```

where `Y,K,J,X` are the four Hamming-weight products.

Regard the four columns of one `2 x 4` row-pair as labelled points of
`P^1`, allowing a zero column.  Row `GL_2` is only a simultaneous
basis gauge, while the diagonal source torus rescales the nonzero
columns.  Thus a rank-two row-pair has one of the following types:

1. a zero column;
2. four distinct nonzero projective columns;
3. three distinct nonzero columns, with multiplicities `2+1+1`;
4. two distinct nonzero columns, with multiplicities `1+3` or `2+2`.

One projective point would make the row-pair rank one.  This list is
the whole collision compactification needed here.

## Zero columns descend to `P_3`

Suppose column `r` of `A_1` is zero.  If `w_r` is the same column of a
synchronized partner, the three equations in (4) involving `r` say
that `w_r` is symplectically orthogonal to every nonzero column of
`A_1`.  Those columns span `C^2`, so `w_r=0`.

Consequently all three planes lie in the same coordinate hyperplane
`H_r`.  The nonzero pure restriction suspends a pure `P_3`
restriction.  Perfect pairing in the three-variable squarefree
algebra makes every triangle pair image have rank at most two,
contrary to the assumed rank three.

## Four distinct columns are impossible

Four nonzero distinct columns give the cross-ratio form

```text
y=(1,0,1,1),
x=(0,1,1,lambda),               lambda(lambda-1)!=0.
```

The generic binary-cubic theorem classifies every synchronized
partner, including both projective sheets of its adjugate pencil, and
derives a compound-matrix contradiction to (5).  Hence this type is
empty.

## A `2+1+1` collision kills the active cube

Three distinct projective columns have the normal form

```text
y=(1,1,0,1),
x=(0,0,1,1).                                                     (6)
```

Solving the six synchronization equations gives every partner as

```text
y'=c y+d(0,0,1,-1),
x'=c x.                                                          (7)
```

Row rank two forces `c!=0`.  Rescale each partner so that all three
active rows equal `x`.  Since `x` is supported on only two source
coordinates,

```text
X=x_1x_2x_3=x^3=0,
```

contradicting the escape condition in (5).

## A `1+3` split drops the pair rank

The two projective points can first occur as

```text
y=(1,0,0,0),
x=(0,1,1,1).                                                     (8)
```

Every synchronized rank-two partner is

```text
y'=c y,
x'=c x+d y,                    c!=0.                              (9)
```

It spans the same plane as `(y,x)`.  Moreover

```text
y^2=0,
```

so the common plane squares into `span(yx,x^2)`, of dimension at most
two.  This contradicts the triangle pair rank.  The `3+1`
orientation is equivalent by swapping the two projective points.

## The `2+2` synchronization space

Only the balanced split remains.  Normalize its base row-pair to

```text
A_1=(a;b)
```

with (2).  The annihilating block rows satisfy

```text
a a_bar=0,                    b b_bar=0.                          (10)
```

The six synchronization equations say that every partner is

```text
y_i=c_i a+beta_i b_bar,
x_i=c_i b+alpha_i a_bar.                                        (11)
```

If `c_i=0`, multiplication with `U_1` has rank at most two.  Hence
`c_2c_3!=0`, and row-pair rescaling makes both equal to one.

The remaining synchronization equation between modes two and three
is the single tetrad

```text
beta_2 alpha_3=alpha_2 beta_3.                                   (12)
```

Write

```text
(alpha_i,beta_i)=r_i(alpha,beta).
```

Put

```text
E_A=X_0X_1,                    E_B=X_2X_3,
u=E_A b,       u_bar=E_A b_bar,
v=a E_B,       v_bar=a_bar E_B.                                  (13)
```

These four vectors form a basis of `R_3`.  Direct multiplication,
using `a_bar^2=-a^2` and `b_bar^2=-b^2`, gives

```text
Y=2 beta(r_2+r_3)u_bar-2r_2r_3 beta^2 v,
K=2u,
J=2v,
X=2 alpha(r_2+r_3)v_bar-2r_2r_3 alpha^2 u.                       (14)
```

Because `K,J` are independent, the compression half of (5) forces

```text
beta(r_2+r_3)=0.
```

The escape half forces

```text
alpha(r_2+r_3)!=0.
```

Therefore `beta=0`.  Absorbing nonzero `alpha` into the `r_i` gives
the planes `U_1,U_2,U_3` in (1), with `s+t!=0`.

The annihilator of `span(u,v)` under the perfect `R_1 x R_3` pairing
is exactly

```text
U_0=span(a_bar,b_bar).                                            (15)
```

The row `b_bar` annihilates `X`, while

```text
a_bar X=-4(s+t)X_0X_1X_2X_3.
```

This proves (3).  Conversely, direct multiplication shows that all
three triangle pair images have rank three and their unique
relations are

```text
y_i x_j-x_i y_j=0,
```

of coefficient-matrix rank two.  Thus (1) is both necessary and
sufficient.

## Why this is not a new generic component

The normal form has two parameters.  Restoring the diagonal source
torus adds at most three dimensions, but the one-dimensional block
subtorus

```text
diag(rho,rho,1,1)
```

rescales `(s,t)` simultaneously and hence is already counted.
Therefore the plane locus swept out by (1) has dimension at most

```text
2+3-1=4.                                                         (16)
```

On a nonzero Segre chart, the pure incidence has twenty affine
variables—sixteen plane-chart coordinates and four target ratios—and
fifteen equations.  Krull's principal ideal theorem gives dimension
at least five for every irreducible component.  The pure target
factor is unique, so projection to the plane locus is locally an
isomorphism.

Hence the four-dimensional triangle locus cannot itself be an
irreducible component and cannot furnish the generic point of a
missing component.

## Verification

Run:

```text
python claims/p4/history/resonant-flat-triangle/verify_p4_resonant_flat_triangle_classification_withdrawn_overstrong.py
python claims/p4/history/resonant-flat-triangle/audit_p4_resonant_flat_triangle_classification_withdrawn_overstrong.py
```

These scripts replay the exact displayed normal forms but do not
certify the withdrawn exhaustiveness claim.  The primary verifier replays the collision normal forms, the `2+2`
synchronization space, (12)--(15), all sixteen permanent
coefficients, and the three triangle pair ranks.  The independent
audit uses the crossed block partition `{0,2}|{1,3}` and a separate
permanent implementation.  These are exact symbolic proof replays,
not searches.
