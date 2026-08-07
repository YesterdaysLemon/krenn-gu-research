# Complete classification of the mixed-endpoint star `(1,1,1)` orientation

## Status

**Exact characteristic-zero orientation classification.**  Let a nonzero pure
`P_4` compression have all six pair-image ranks at least three, and suppose
the selected rank-one exceptional star is centered at mode three with

```text
x_1 y_3=0,       x_2 y_3=0,       y_0 x_3=0.       (1)
```

Here `y_i` is the pure-kernel row and `x_i` is active.  Thus two spokes use
the center kernel and the third uses a leaf kernel; no selected spoke is
kernel--kernel.  Every such tuple lies in an already certified component
closure.  Genuine binary overlapping supports are exhausted by the
projective mixed-orientation theorem, genuine binary disjoint supports are
exhausted by component eight, and the support-one boundary reduces to a
lower-pair point or an already classified rank-one triangle.

Consequently the complete endpoint-indegree signature `(2,1,0,0)` creates no
twenty-sixth component.  This does not classify the remaining endpoint
signature `(1,1,1,0)`, one- or two-double-spoke stars, or the global
Krenn--Gu conjecture, which remains **UNRESOLVED**.

## Support-two interior

For a nonzero degree-one zero divisor in the squarefree algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2),
```

the degree-one annihilator is one line and the common support has size at
most two.  The first two relations in (1) therefore have the same support
label.  If it is a singleton, then `x_1=x_2` is a coordinate row and
`x_1x_2=0`, contradicting the nonzero all-active coefficient.

Assume that common label is genuinely binary.  If the third label is the
same binary pair, then `x_1x_2x_3=0`; if it is a singleton on that pair, the
same cubic again vanishes.  For two distinct genuine binary labels there are
only two source-graph possibilities:

1. adjacent labels are the complete overlapping chart in
   [`P4_OVERLAPPING_MIXED_ORIENTATION_PROJECTIVE_EXHAUSTION.md`](../../../../../P4_OVERLAPPING_MIXED_ORIENTATION_PROJECTIVE_EXHAUSTION.md);
2. disjoint labels are the complete component-eight chart in
   [`P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md`](../disjoint-mixed-star-projective/P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md).

It remains only to classify a singleton third label outside the common
binary support.

## Normal form for the singleton boundary

Put

```text
A=X_0+X_1,       C=X_0-X_1,       E_2=X_2,       E_3=X_3.
```

Source scaling, row scaling, and legal Borel shifts give the complete form

```text
y_0=E_2,                 x_0=aA+bC+E_3,
y_1=cC+fE_2+gE_3,        x_1=A,
y_2=dC+hE_2+jE_3,        x_2=A,
y_3=C,                   x_3=E_2.                  (2)
```

The coefficient of the all-active word is the constant `2`.  The only
other possibly nonzero coefficients are

```text
T_0000=-2(cj+dg),
T_1000=-2(bfj+bgh+ch+df),
T_1001=-2(bcj+bdg+cd),
T_1011= 2ag,
T_1101= 2aj.                                       (3)
```

Thus purity is exactly the vanishing of the five expressions in (3).

## The exact branch split

If `a!=0`, equations (3) give `g=j=0`, followed by

```text
cd=0,       ch+df=0.                               (4)
```

Plane nondegeneracy leaves only `c=d=0`; then
`U_1=<E_2,A>` and `U_3=<C,E_2>` have product-image rank two.  Hence no
all-pair point occurs on `a!=0`.

Suppose `a=0`.  The first and third equations in (3) give

```text
cj+dg=0,       cd=0.                               (5)
```

After interchanging leaves one and two, take `c=0`.  If `d!=0`, then
`g=0` and plane nondegeneracy forces

```text
f!=0,       d=-bj.                                 (6)
```

Again `U_1=<E_2,A>` and `U_3=<C,E_2>` have rank-two product image.  Therefore
the all-pair locus has

```text
a=c=d=0,       b(fj+gh)=0.                         (7)
```

There are precisely two remaining branches.

### The branch `b=0`

Now

```text
U_0=<E_2,E_3>,
U_1=<fE_2+gE_3,A>,
U_3=<C,E_2>.                                      (8)
```

On modes `(0,1,3)` the three exact relations have support labels

```text
{2,23,01}:
E_2^2=0,
(gE_3-fE_2)(fE_2+gE_3)=0,
AC=0.                                             (9)
```

If any of these pair images has rank below three, the lower-pair theorem
applies.  Otherwise (9) is a cyclic rank-one triangle with a singleton
label, so the complete toric-boundary theorem
[`P4_CYCLIC_RANK_ONE_TRIANGLE_SUPPORT_ONE_BOUNDARY.md`](../../../../../P4_CYCLIC_RANK_ONE_TRIANGLE_SUPPORT_ONE_BOUNDARY.md)
places it in component sixteen or seventeen.

### The branch `b!=0`

Equation (7) becomes

```text
(fE_2+gE_3)(hE_2+jE_3)=0.                         (10)
```

Modes `(1,2,3)` therefore form a rank-one exceptional triangle with

```text
y_1y_2=0,       x_1y_3=0,       x_2y_3=0.         (11)
```

On the all-pair locus all three images have rank exactly three, and (11)
has exactly one kernel--kernel edge.  The complete exactly-one-kernel
triangle placement recorded in
[`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](../../../../../P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md)
puts every such point in an already certified component closure.

This exhausts the singleton boundary and hence the whole orientation (1).

## Replay

```text
uv run --with sympy python claims/p4/classifications/star/mixed-endpoint-star-111-complete/verify_p4_mixed_endpoint_star_111_complete_classification.py
uv run --with sympy python claims/p4/classifications/star/mixed-endpoint-star-111-complete/audit_p4_mixed_endpoint_star_111_complete_classification.py
```

The primary verifier reconstructs all coefficients in (3), both exact
branch relations, and symbolic pair-rank certificates.  The independent
audit uses a separate subset-DP permanent, unequal source scales, and a
source permutation.  Both use exact characteristic-zero arithmetic; no
finite-field inference or parameter search is used.
