# Pure `P_4` restrictions with a tangent rank-two pair

## Status

**Exact symbolic classification over `C`.**  Suppose a nonzero pure
restriction of `P_4` has a pair multiplication map of rank two whose kernel
line is tangent to the Segre quadric.  By the single-pair theorem, the two
planes on that edge have the form

```text
U_0=U_1=span(e,w),                                  (1)
```

where `e=X_0` and `w` uses at least two of `X_1,X_2,X_3`.

Let `A=U_2`, `B=U_3`.  This note classifies all possible opposite pairs.

1. If `w` has support three, one of `A,B` contains `e`.  After swapping them,
   `A=span(e,u)`.  The other plane is either an explicit graph over the
   ternary polar plane `u^perp`, or contains `e` as well.  Equations (10) and
   (11) below are necessary and sufficient for purity.
2. If `w` has support two, either a third plane lies in the same coordinate
   three-space, giving the known embedded-`P_3` suspension, or both opposite
   planes define orthogonal lines in a hyperbolic quotient and at least one
   meets the radical in the distinguished annihilator line.  This is the
   polar-flag family of (16).

Thus tangent kernels are not automatically empty and not all of them are
embedded `P_3`.  Their complete geometry is nevertheless controlled by
orthogonal complements and radical flags, without a permanent-ideal search.
Whether the non-embedded families are boundary strata of known components or
sit on further component closures remains open here.

## Purity becomes two bilinear forms

Use the bases `(e,w)` on the two tangent planes.  Their products are

```text
e^2=0,       ew=q,       w^2=r.                     (2)
```

For `a in A`, `b in B`, define

```text
Q_w(a,b)=[X_0X_1X_2X_3](q a b),
R_w(a,b)=[X_0X_1X_2X_3](r a b).                    (3)
```

The two-by-two slice on the tangent modes is

```text
[ 0          Q_w(a,b)]
[ Q_w(a,b)   R_w(a,b)].                             (4)
```

In a nonzero pure tensor, symmetry makes the two tangent-mode factors
proportional.  Since the upper-left coefficient is zero, both must select
the `w` row.  Therefore purity is equivalent to

```text
Q_w(A,B)=0,
rank(R_w restricted to A x B)=1.                   (5)
```

The second form must of course be nonzero.  Conversely, (5) makes the full
tensor the product of the two `w` coordinates with the rank-one opposite
form, so it is sufficient.

## Full support: a ternary orthogonal graph

Write

```text
w=w_1X_1+w_2X_2+w_3X_3,
W=span(X_1,X_2,X_3).                                (6)
```

On `W`, the first form has matrix

```text
       [  0   w_3 w_2]
Q_w = [ w_3   0   w_1],
       [ w_2 w_1   0  ]                             (7)
```

with determinant `2w_1w_2w_3`.  Its radical on all of `R_1` is exactly
`C e`.  The second form is the split star

```text
R_w(e,v)=ell_w(v),       R_w(W,W)=0,

ell_w(v)=2(w_2w_3v_1+w_1w_3v_2+w_1w_2v_3).         (8)
```

If neither `A` nor `B` contained `e`, their images in the nondegenerate
three-space `W` would both be two-dimensional and orthogonal, which is
impossible.  Swap the opposite modes and put

```text
A=span(e,u),       L=u^perp_Q subset W.             (9)
```

If `B` projects isomorphically onto `L`, it is the graph of a linear form
`phi:L->C`:

```text
B={phi(v)e+v:v in L}.
```

Then (5) is exactly

```text
ell_w|_L wedge (ell_w(u) phi)=0,
not both functionals zero.                          (10)
```

On the dense chart `ell_w(u)!=0` and `ell_w|_L!=0`, this says simply

```text
phi=t ell_w|_L.                                     (10a)
```

If `B` also contains `e`, write `B=span(e,v)` with `v in L`.  Its opposite
matrix is

```text
[      0       ell_w(v)]
[ ell_w(u)          0  ],
```

so (5) becomes

```text
ell_w(u) ell_w(v)=0,
(ell_w(u),ell_w(v))!=(0,0).                         (11)
```

Equations (10)--(11) are exhaustive and sufficient.

## Support two: a radical hyperbolic quotient

After diagonal source scaling, put

```text
w=H=X_1+X_2,       S=X_1-X_2,       Z=X_3.          (12)
```

Now `Q_w` has radical

```text
K=span(e,S),                                       (13)
```

and the quotient `R_1/K=span(H,Z)` is a hyperbolic plane with
`Q_w(H,Z)!=0`.  Meanwhile `R_w` has only the hyperbolic pairing

```text
R_w(e,Z)!=0.                                       (14)
```

Let `pi:R_1->R_1/K`.  Orthogonality gives

```text
dim pi(A)+dim pi(B)<=2.                             (15)
```

If either image is zero, that plane equals `K`; three local planes then lie
in `span(X_0,X_1,X_2)`, and (5) is an embedded-`P_3` suspension.

Otherwise both images are orthogonal lines.  Put

```text
k_A=A intersection K,       k_B=B intersection K,
z_A=Z-coordinate of pi(A),  z_B=Z-coordinate of pi(B),
e_A=e-coordinate of k_A,    e_B=e-coordinate of k_B.
```

For arbitrary lifts of the quotient lines, the determinant of the opposite
`R_w` matrix is, up to one nonzero common scalar,

```text
-e_A e_B z_A z_B.                                  (16)
```

If `z_Az_B=0`, hyperbolic orthogonality forces both quotient lines to be
`C H`; again `A,B` lie in the coordinate three-space.  The non-embedded
case therefore has `z_Az_B!=0`, and (5) says

```text
k_A=C S or k_B=C S,                                (17)
```

with the remaining `R_w` entry nonzero.  This is the promised polar-flag
normal form.  It is both necessary and sufficient.

## Exact representatives

The dense full-support graph branch has the rational point

```text
e=(1,0,0,0),       w=(0,1,1,1),       u=(0,1,2,3),

A=span(e,u),
B=span((-2,4,-5,0),(-4,3,0,-5)).                   (18)
```

Its pair profile is

```text
(2,3,4,3,4,4),                                     (19)
```

and its four nonzero coefficients factor as

```text
-2 y_0 y_1 (x_2+12y_2)(x_3+2y_3).                 (20)
```

A non-embedded support-two polar flag is

```text
U_0=U_1=span(e,H),
U_2=span(e+S,H+Z),
U_3=span(S,e+H-Z).                                  (21)
```

Its profile is `(2,4,3,4,3,4)`, and its restriction is

```text
-2 y_0 y_1 (x_2-y_2)y_3.                           (22)
```

Both profiles sort to `(2,3,3,4,4,4)`, the same generic rank multiset as the
known six-dimensional lower-pair component.  Kernel tangency distinguishes
the displayed strata, but does not by itself decide component containment.

## Across the mathematical fence

The tangent-pair problem is a Witt-decomposition problem.  Full support
produces a nondegenerate ternary quadratic space, so dimension forces a
common radical vector and purity becomes proportionality of two functionals
on a polar plane.  Support two degenerates that form to a hyperbolic plane
with a two-dimensional radical; the survivor is exactly an incident polar
flag.

This is the same organization used for degenerate quadratic forms and
orthogonal Grassmannians.  It replaces sixteen permanent coefficients by
the rank and radical of two small bilinear forms.

## Verification

Run:

```text
uv run --with sympy python verify_p4_tangent_rank_two_pair_purity_classification.py
python audit_p4_tangent_rank_two_pair_purity_classification.py
```

The primary verifier derives (4), (7)--(8), (10)--(11), and (16), and checks
both rational representatives.  The independent audit source-permutes the
representatives and evaluates the permanent by subset dynamic programming.
Neither verifier searches for solutions.
