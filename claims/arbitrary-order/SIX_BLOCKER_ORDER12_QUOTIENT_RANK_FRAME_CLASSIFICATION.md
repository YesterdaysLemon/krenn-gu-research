# Quotient-rank and frame classification of the order-twelve `P_6` family

## Status

**Exact characteristic-zero structural classification.**  For the
order-twelve maximal-overlap system of
[`SIX_BLOCKER_ORDER12_ISOTROPIC_P6_CURVE.md`](SIX_BLOCKER_ORDER12_ISOTROPIC_P6_CURVE.md),
reduce the four-dimensional bilinear permanent family modulo the
three-dimensional GHZ diagonal plane.  Its quotient map has exactly two
possibilities:

1. it is zero, in which case a Zariski-open part of the full
   `P(X_a) x P(X_b)` surface consists of concise diagonal `P_6` pullbacks;
2. it has rank one, in which case its diagonal locus is exactly the
   cross-form hyperplane, whose decomposable part is the previously found
   smooth conic or pair of rulings.

The target-frame divisor is classified as well.  After torus normalization,
its determinant is the affine collinearity determinant of three explicit
ratio points.  On that divisor the frame has rank two unless all three ratio
points coincide.  The rank-one subbranch is impossible when `delta=0`; when
`delta!=0`, it forces a `2+1` collision of two ratio pairs lying over the two
distinct roots of one quadratic.

This removes an unspecified ``frame-degenerate'' residual and replaces it by
an exact rank-one/rank-two ledger.  It does **not** exclude the quotient-zero
surface, the quotient-rank-one conic with frame rank two or three, or the
corresponding `P_6` restrictions.  The projected-Veronese/frame-orbit route
therefore remains structural exploration, not a global theorem.  Arbitrary
ambient order with residual vertices remains **UNKNOWN**, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

## The bilinear permanent family

Keep the notation

```text
X_a=span{x_a,z_a},       X_b=span{x_b,z_b},
beta=B_ab(x_a,x_b)!=0,   delta=B_ab(z_a,z_b),          (1)
```

with cross form

```text
q=B_ab|_(X_a x X_b)=diag(beta,delta).                  (2)
```

Let `mathcal T` be the six-blocker tensor space and

```text
mathcal D=span{e_0^6,e_1^6,e_2^6} subset mathcal T     (3)
```

its GHZ diagonal plane.  The six-row permanent pullback is a linear map

```text
Pi:X_a tensor X_b -> mathcal T.                        (4)
```

The exact matching partition from the preceding theorem is

```text
Pi(y_a tensor y_b)+q(y_a,y_b) C_I
 =D(h(y_a tensor y_b)),                                (5)
```

where `C_I` is the single four-root blocker--blocker cofactor,

```text
h(y_a tensor y_b)
 =d hadamard y_a hadamard y_b in C^3,
d_c=product_(i in I)x_i[c],

D(v)=sum_(c=0)^2 v_c product_(u in B)z_u[c].           (6)
```

Thus `D:C^3 -> mathcal D` is the coordinate diagonal embedding; in
particular the fixed six-blocker monomials are part of `D`, not omitted from
(5).  All entries of `d,x_a,z_a,x_b,z_b` are nonzero.

Let `rho:mathcal T -> mathcal T/mathcal D` and put bars over quotient
classes.  Applying `rho` to (5) gives the complete quotient identity

```text
bar(Pi)=-bar(C_I) tensor q.                            (7)
```

## The exact quotient dichotomy

Because `q` is nonzero (`q(x_a,x_b)=beta`), (7) has only two branches.

### Quotient-zero surface

If `bar(C_I)=0`, equivalently `C_I in mathcal D`, then

```text
bar(Pi)=0.                                             (8)
```

Thus every permanent pullback `Pi(y_a,y_b)` on the whole product of
exchanged planes is diagonal.  At the mixed point `(x_a,z_b)`, its three
coefficients are

```text
d_c x_a[c] z_b[c] !=0.                                (9)
```

The simultaneous nonvanishing of three bilinear coefficient forms is
Zariski open, so (9) supplies a nonempty open subset of
`P(X_a) x P(X_b)` on which the diagonal is concise.  Conciseness forces all
six local maps to have rank three.  Hence this branch contains a genuine
two-dimensional family of `P_6 -> Delta_3` restrictions.

No current theorem excludes `C_I in mathcal D`.

### Quotient-rank-one conic or rulings

If `bar(C_I)!=0`, then

```text
rank(bar(Pi))=1,       ker(bar(Pi))=ker(q).             (10)
```

Consequently a projective bilinear permanent `Pi(y_a,y_b)` is diagonal if
and only if `q(y_a,y_b)=0`.  Inside
`P(X_a tensor X_b)=P^3`, the decomposable points form the Segre quadric.
Their intersection with `P(ker q)` is

```text
delta!=0: a smooth (1,1) conic;
delta=0:  the two rulings y_a=z_a or y_b=z_b.           (11)
```

The torus points on (11) give precisely the concise restrictions in this
branch.  Thus the conic/rulings theorem is not merely one constructed
family: modulo the diagonal target, it is the complete decomposable
diagonal locus.

## The frame map on `ker q`

Use the tensor basis

```text
E_00=x_a tensor x_b,       E_01=x_a tensor z_b,
E_10=z_a tensor x_b,       E_11=z_a tensor z_b.
```

A basis of the three-space `ker q` is

```text
E_01,       E_10,       delta E_00-beta E_11.          (12)
```

After omitting the fixed invertible diagonal scaling by `d`, the coefficient
map `h|_(ker q)` has frame columns

```text
v_01=x_a hadamard z_b,
v_10=z_a hadamard x_b,
v_m=delta(x_a hadamard x_b)-beta(z_a hadamard z_b).    (13)
```

Therefore

```text
rank(h|_(ker q))=rank(v_01,v_10,v_m),
Theta=det(v_01,v_10,v_m).                              (14)
```

The full-frame branch is exactly `Theta!=0`; there `h|_(ker q)` is an
isomorphism onto the GHZ coefficient space.  The frame divisor is exactly
`Theta=0`, with rank one or two as classified next.

## Ratio-point classification of `Theta=0`

Introduce the torus ratios

```text
r_c=z_a[c]/x_a[c],       s_c=x_b[c]/z_b[c],
p_c=x_a[c]z_b[c].                                      (15)
```

Row-scaling the frame in (13) by the nonzero `p_c` gives

```text
Theta
 =(p_0 p_1 p_2)
   det [1, r_c s_c, delta s_c-beta r_c]_(c=0,1,2).     (16)
```

Associate to each target colour the affine point

```text
P_c=(r_c s_c, delta s_c-beta r_c) in A^2.              (17)
```

Equation (16) gives the complete ledger:

```text
rank frame=3  <=> P_0,P_1,P_2 are not collinear;
rank frame=2  <=> they are collinear but not all equal;
rank frame=1  <=> P_0=P_1=P_2.                         (18)
```

If `delta=0`, equality of the second coordinates in the rank-one case gives
`r_0=r_1=r_2`.  Then `z_a` is proportional to `x_a`, contradicting
`dim X_a=2`.  Hence

```text
delta=0 and Theta=0  =>  rank frame=2.                 (19)
```

Suppose `delta!=0` and the frame has rank one.  There is a nonzero constant
`A` and a possibly zero constant `B` with

```text
r_c s_c=A,       delta s_c-beta r_c=B                 (20)
```

for all three colours.  Eliminating `s_c` gives

```text
beta r_c^2+B r_c-delta A=0.                            (21)
```

The ratios `r_c` cannot all agree because `x_a,z_a` are independent; the
ratios `s_c` cannot all agree because `x_b,z_b` are independent.  Thus (21)
has two distinct nonzero roots, and the three colours use them in a `2+1`
partition.  The corresponding `s_c=A/r_c` have the same partition.  This is
the complete frame-rank-one branch up to permuting colours.

This branch has an exact base-point description.  Along the isotropic
parametrization, the colour-`c` target factor is

```text
y_a(t)[c]y_b(t)[c]
 =p_c(1+r_c t)(delta s_c t-beta)
 =p_c(-beta+B t+delta A t^2).                         (22)
```

The quadratic in the last expression is independent of `c`.  Hence the
whole GHZ coefficient curve is one fixed torus vector, with coordinates
`d_c p_c`, times a common quadratic.  At either root of that quadratic the
target tensor is zero.  More precisely, if the two ratio solutions are
`(r,s)` and `(r',s')`, then

```text
-1/r=beta/(delta s'),       -1/r'=beta/(delta s).      (23)
```

At the first base point, `y_a` vanishes on the colour class carrying `r`
and `y_b` vanishes on its complementary class carrying `r'`; the roles swap
at the second base point.  Because the colour partition is `2+1`, each base
point has one exchanged vector of singleton support and the other of
complementary binary support.  These are exact zero-target boundary points,
not counterexamples.

On the rank-two divisor, the three points (17) lie on one affine line but are
not all equal.  Equivalently, there is a nonzero triple `(L_0,L_1,L_2)` such
that

```text
L_0+L_1 r_c s_c+L_2(delta s_c-beta r_c)=0             (24)
```

for `c=0,1,2`.  This exact `(1,1)` ratio relation is the remaining
frame-degenerate branch; no current permanent obstruction excludes it.

## What remains

The order-twelve maximal-overlap frontier is now partitioned without a
genericity gap:

```text
C_I in mathcal D:
  an open P1 x P1 surface of concise diagonal P_6 pullbacks;

C_I notin mathcal D, Theta!=0:
  the exact isotropic conic/rulings with full target frame;

C_I notin mathcal D, Theta=0, rank frame=2:
  the collinear but nonconstant ratio-point branch;

C_I notin mathcal D, rank frame=1:
  delta!=0, an exact 2+1 ratio-pair collision, and two complementary
  singleton/binary zero-target base points.
```

Excluding any of these branches requires genuinely new information about a
surface or synchronized curve of `P_6` restrictions sharing four fixed rows,
or about the image of the blocker cofactor `C_I`.  No completed `P_5` theorem
currently supplies that information.  The classification is replayable, but
it is not a proof or counterexample to Krenn--Gu.

## Replay

```text
uv run --with sympy python verify_six_blocker_order12_quotient_rank_frame_classification.py
uv run --with sympy python audit_six_blocker_order12_quotient_rank_frame_classification.py
```

The primary verifier checks the consequences of the quotient factorization,
the kernel and conic normal forms, the symbolic determinant identity, the
universal rank-one boundary identities, and exact examples of frame ranks
one, two, and three.  The no-import audit uses independent rational linear
algebra and a separate ratio reconstruction, including the valid `B=0`
rank-one case.  The underlying full matching partition is replayed in the
preceding order-twelve theorem.  No finite-field inference is used.
