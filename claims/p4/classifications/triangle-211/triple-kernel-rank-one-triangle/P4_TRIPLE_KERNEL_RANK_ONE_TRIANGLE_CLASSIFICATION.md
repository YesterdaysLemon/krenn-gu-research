# Fully kernel--kernel rank-one triangles lie in components sixteen or eighteen

## Status

**Exact characteristic-zero classification of one residual
`triangle-(1,1,1)` stratum.**  Work over `C` in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Let `U_i=span(y_i,x_i)` be four marked planes on which `P_4` restricts
to a nonzero pure tensor, with `y_i` the intrinsic kernel row.  Suppose
all six pair images have rank at least three and the selected exceptional
triangle on modes `1,2,3` has pair rank three and unique relations

```text
y_1 y_2=0,       y_1 y_3=0,       y_2 y_3=0.       (1)
```

Then the plane tuple belongs to one of two already certified component
closures:

1. if `U_0` contains the common singleton below, it belongs to component
   eighteen, the common-singleton component;
2. otherwise it belongs to component sixteen, the directed triangle whose
   source-support labels form a star.

Thus the fully doubly oriented part of the rank-one triangle cell creates no
nineteenth component.  The exactly-two-kernel stratum is now classified in
[`P4_TWO_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md`](../two-kernel-rank-one-triangle/P4_TWO_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md).
This theorem does **not** classify triangles with exactly one kernel--kernel
relation, either open star cell, special `P_5` fibres, or the global
Krenn--Gu conjecture.

## Three pairwise-zero kernel rows have one common singleton

For nonzero linear forms `u,v`, the equation `uv=0` says

```text
u_i v_j+u_j v_i=0       for every i<j.              (2)
```

The usual exact-zero-divisor argument shows that `u,v` have common support
of size at most two.  On genuine support two the annihilator of `u` in
degree one is the opposite binary direction; on support one it is the same
coordinate line.

Apply this to `y_1`.  Both `y_2` and `y_3` lie in its one-dimensional
degree-one annihilator, so they are proportional.  Equation `y_2y_3=0`
therefore says that the square of a nonzero linear form is zero.  In
characteristic zero this happens only for a coordinate form.  Hence, after
a source permutation and row scalings,

```text
y_1=y_2=y_3=e=X_2.                                  (3)
```

Put

```text
V=span(A,B,C)=span(X_0,X_1,X_3).
```

Borel-shift the three active rows to remove their `e` coordinates and write

```text
U_i=span(e,v_i),       v_i in V,       i=1,2,3.    (4)
```

If `T=P_3(v_1,v_2,v_3)`, the nonzero all-active coefficient is a nonzero
multiple of `T`; in particular `T!=0`.

## The branch containing `e` is component eighteen

If `e in U_0`, write

```text
U_0=span(ell,e),       ell in V.                    (5)
```

Every mixed coefficient containing `ell` and exactly one of the three
kernel rows is zero precisely when

```text
P_3(ell,v_i,v_j)=0       for i<j.                   (6)
```

Equations (4)--(6), together with `T!=0`, are exactly the intrinsic family
in [`P4_COMMON_SINGLETON_COMPONENT.md`](../../P4_COMMON_SINGLETON_COMPONENT.md).
This proves containment in component eighteen, including its special
orthogonal-flag boundary.

## The branch not containing `e` has a unique complementary-edge core

Assume now that `e` is not in `U_0`.  There are independent `y,w in V`
such that

```text
U_0=span(y,e+w).                                    (7)
```

Indeed, `U_0` cannot be contained in `V`: the product of its active row
with `v_1v_2v_3` would then have degree four in the three-variable
squarefree algebra on `A,B,C`, and hence would be zero.  Since `U_0` is
neither contained in `V` nor contains `e`, its intersection with `V` is a
line `span(y)` and a second row can be normalized to `e+w`; moreover `w`
cannot be proportional to `y`, because that would put `e` in `U_0`.

Let

```text
Q=span(v_1v_2,v_1v_3,v_2v_3) inside R_2(V).        (8)
```

Purity of every coefficient with exactly one triangle kernel says that
both `y` and `w` annihilate `Q` under the perfect pairing
`V x R_2(V) -> C`.  Since they are independent, `dim Q<=1`.  None of the
three products in (8) is zero, because multiplying it by the remaining
`v_i` gives `T!=0`.  Therefore

```text
dim Q=1.                                            (9)
```

The rows `v_1,v_2,v_3` are independent.  Otherwise relabel so that
`v_1,v_2` are independent and write `v_3=a v_1+b v_2`.  The selected
pair ranks are three, so no two `v_i` are proportional; hence `ab!=0`.
Equation (9) then gives

```text
v_1^2=alpha v_1v_2,       v_2^2=beta v_1v_2.
```

Thus `v_1(v_1-alpha v_2)=0` and
`v_2(v_2-beta v_1)=0`.  The exact-zero-divisor support theorem puts
`v_1,v_2`, and hence `v_3`, in one coordinate two-plane (if `alpha` or
`beta` is zero, the corresponding row is a singleton and the same
conclusion follows).  This would force `T=0`, a contradiction.

Scale the `v_i` so that their three pair products are equal.  Associativity
then gives

```text
v_1(v_2-v_3)=0,
v_2(v_1-v_3)=0,
v_3(v_1-v_2)=0.                                    (10)
```

Each exact pair in (10) has genuine support two: support one would be a
linear dependence among the `v_i`.  The three support pairs are distinct,
since two equal labels would put all three rows in one binary coordinate
plane.  They are consequently the three edges of the coordinate triangle
on `A,B,C`.  Writing the three rows on those supports, the missing-coordinate
conditions in (10) force

```text
v_1=aB+bC,       v_2=cA+bC,       v_3=cA+aB,
abc!=0.                                               (11)
```

Diagonal source scaling, a mode swap, and row scalings give the convenient
signed representative

```text
v_1=B-C,       v_2=A-B,       v_3=A+C.              (12)
```

Its pair products satisfy

```text
v_1v_2=v_1v_3=-(v_2v_3)=q,
q=AB-AC+BC,       v_1v_2v_3=2ABC.                  (13)
```

The common annihilator of the pair products is

```text
W={aA+bB+cC : a-b+c=0}.                             (14)
```

Equations (7)--(9) say exactly that `y,w in W`.  Hence the opposite plane
is contained in the three-space

```text
H_0=span(e,W)={z : z_A-z_B+z_C=0},                 (15)
```

and is not contained in `W`.

## An explicit arc into component sixteen

For `epsilon!=0`, keep the active rows in (12) and replace the triangle
kernel rows by

```text
k_1=e+epsilon B,
k_2=e-epsilon A,
k_3=e-epsilon C.                                   (16)
```

These three planes are exactly the diagonal-source image, under
`e -> epsilon^(-1)e`, of the support-star triangle

```text
span(B+e,e+C),
span(A-e,B-e),
span(e-C,A+e)                                      (17)
```

from
[`P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md`](../../P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md).

For a row `z=z_A A+z_B B+z_e e+z_C C`, put

```text
g_epsilon(z)=z_A-z_B+z_C-epsilon z_e,
H_epsilon=ker(g_epsilon).                          (18)
```

A direct permanent expansion of `z` against one chosen row from each plane
in (16) gives, in binary order `000,...,111`,

```text
(-epsilon^2 g, epsilon g, epsilon g, -g,
 -epsilon g,       g,         g,       2 z_e).      (19)
```

Thus every plane in `Gr(2,H_epsilon)` that is not contained in
`{z_e=0}` is an allowed nonzero opposite plane for component sixteen.

Every target plane `U_0` from (15) has a canonical lift.  Define

```text
L_epsilon(z)=z+epsilon z_e A,
U_0(epsilon)=L_epsilon(U_0).                        (20)
```

Because `g_epsilon(L_epsilon(z))=0` for `z in H_0`, the lifted plane lies
in `H_epsilon`.  The map preserves `z_e`, so the all-active coefficient in
(19) stays nonzero.  Consequently the four planes

```text
U_0(epsilon),
span(k_1,v_1), span(k_2,v_2), span(k_3,v_3)         (21)
```

belong to component sixteen for every `epsilon!=0`, and their Grassmann
limit at `epsilon=0` is the original tuple.  This proves the second
containment and completes the stated stratum classification.

## What this closes and what remains

The tournament theorems already classify rank-one triangles with a unique
orientation on every edge.  The theorem above closes the opposite extreme,
where every edge is doubly oriented because its unique relation is
kernel--kernel.  Together with the exactly-two-kernel theorem cited above,
this leaves only the pattern with exactly one kernel--kernel edge inside
`triangle-(1,1,1)`; its finite residual normal forms are recorded in
[`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](../../P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md).
The other three coarse cells listed in
[`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](../../P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md)
also remain open.

## Exact replay

```text
uv run --with sympy python claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/verify_p4_triple_kernel_rank_one_triangle_classification.py
python claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/audit_p4_triple_kernel_rank_one_triangle_classification.py
```

The primary verifier checks the complementary-edge normal form, all eight
identities in (19), the lift (20), the component-sixteen row-span
identification, exact pair ranks, and the pure target tensor over a symbolic
characteristic-zero field.  The independent audit imports nothing from the
primary verifier: it uses rational permanent expansion and row reduction on
several opposite planes and several nonzero arc parameters.  The audit is
corroboration; the support and arc arguments above are the
characteristic-zero proof.
