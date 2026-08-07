# Overlapping secant kernels recover the known lower-pair sixfold

## Status

**Exact characteristic-zero classification theorem.**  Suppose a nonzero
pure `P_4` restriction has an exact rank-two pair whose Segre-secant kernel
points are genuine two-coordinate zero products with supports meeting in one
coordinate.  Then its opposite planes lie in two mode-swapped polar-flag
branches.  Their closures exhaust this overlapping `1+3` secant stratum.

Each maximal branch has six parameters after restoring the two binary source
ratios.  Its closure is exactly the six-dimensional component already proved
in [`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](claims/p4/components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md),
not a sixteenth component.  The identification uses an explicit common
smooth point and source/mode transformation.

Together with the disjoint-secant component and the tangent classification,
this closes every genuine support-two exact-rank-two pair kernel.  The
support-one secants are subsequently placed in the disjoint-component
closure by
[`P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md`](P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md).
Compatibility of several lower-rank edges remains relevant to the closure
intersection poset, but no longer to exhaustiveness of the lower-pair locus.

## Two stars with intersecting radicals

Normalize the support pairs to `{0,1}` and `{0,2}`:

```text
a=X_0+sX_1,       a_bar=X_0-sX_1,
b=X_0+tX_2,       b_bar=X_0-tX_2.                  (1)
```

The rank-two secant edge is

```text
U_0=span(a,b),       U_1=span(a_bar,b_bar),         (2)
```

with zero products `a*a_bar=b*b_bar=0`.  Its cross-products are

```text
q=a*b_bar,       r=b*a_bar.                         (3)
```

Let `Q,R` be their top-degree catalecticant forms.  Put

```text
c=sX_1+tX_2,
P=span(a,b_bar),       K=span(a_bar,b).              (4)
```

Then

```text
rad(Q)=K,       rad(R)=P,
P intersection K=C c,
P+K=span(X_0,X_1,X_2).                              (5)
```

Choose `p=a`, `k=a_bar`, and `z=X_3`.  In the adapted basis `(c,p,k,z)`,
the only nonzero entries of the two forms are

```text
Q(p,z)!=0,       R(k,z)!=0.                         (6)
```

They are two rank-two stars sharing `z` and the common radical line `c`.

## The polar-flag classification

For opposite planes `A=U_2,B=U_3`, purity is, up to selecting the other
cross-product,

```text
Q(A,B)=0,
rank(R|A x B)=1 nonzero.                            (7)
```

On the dense chart, the `Q` projections of the two planes are polar lines

```text
ell=p+lambda z,       ell_bar=p-lambda z.           (8)
```

Write their radical-intersection lines and shears as

```text
A=span(c+m k, ell+u k),
B=span(c+n k, ell_bar+v k).                         (9)
```

In these bases, the `R` matrix is, up to a nonzero scalar,

```text
[ 0          -m lambda]
[ n lambda   lambda(v-u)].                          (10)
```

Its determinant is `mn lambda^2`.  Thus rank-one purity splits into

```text
m=0       or       n=0.                             (11)
```

The two branches are exchanged by swapping the opposite modes.  If a
`Q` projection drops, the corresponding plane moves into `rad(Q)` and is a
flag limit of (9); if both `R` projections are lines, it lies in the branch
intersection.  Hence the two closures in (11) exhaust the genuine
support-two overlapping-secant locus.

## A six-parameter branch

Take `m=0` and rename the six parameters

```text
(s,t,lambda,u,n,v).                                 (12)
```

The planes are

```text
U_0=span(a,b),
U_1=span(a_bar,b_bar),
U_2=span(c,a+lambda X_3+u a_bar),
U_3=span(c+n a_bar,a-lambda X_3+v a_bar).           (13)
```

Direct expansion leaves only

```text
T_1010=-2lambda nst,
T_1011= 2lambda st(u-v).                            (14)
```

Thus (13) is a nonzero pure family on a dense open set.

## Smooth six-dimensional certificate

All four planes lie in pivot-`01` charts near

```text
(s,t,lambda,u,n,v)=(1,1,-2,7,-1,3).                (15)
```

Their sixteen chart coordinates are

```text
(1,0,-1,0,  -1,0,-1,0,
 3/4,-1/4,1,0,  1/3,2/3,2/3,1/3).                 (16)
```

The family Jacobian has rank six; rows

```text
(0,2,8,9,12,14)                                    (17)
```

give determinant

```text
-1/13824.                                           (18)
```

In the target Segre chart anchored at `0100`, the target ratios are

```text
(-1,0,0,4/5).                                       (19)
```

The universal incidence Jacobian has rank fourteen.  Rows `0,...,13` and
columns `(0,...,11,17,18)` give the exact minor

```text
280/729.                                            (20)
```

Hence the branch closure is a smooth six-dimensional component at (15).

## Identification with the earlier sixfold

At the earlier sixfold certificate

```text
(a,c,d,b,e)=(1,2,4,1,2),                            (21)
```

its four planes are those of
[`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](claims/p4/components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md).
Transform an old source row by

```text
(E_0,E_1,E_2,E_3) -> (X_0,X_1,X_2,X_3)
                    =(E_3,-E_0,E_2,E_1),           (22)
```

and reorder the modes as

```text
(0,3,2,1).                                          (23)
```

The resulting four row spaces are exactly (13) at (15).  Explicitly, the
opposite parameters are

```text
lambda=-2,       u=7,       n=-1,       v=3.        (24)
```

The point is smooth of local dimension six by (20), so only one local
component passes through it.  The old sixfold and the six-dimensional family
(13) both pass through the point; their irreducible closures must coincide.

Thus (13) is a dense polar-flag presentation of the known overlapping
lower-pair component.  It also explains intrinsically why that component's
rank-two edge has a `1+3`, not `2+2`, secant center.

## Across the mathematical fence

The overlapping support geometry is a pencil of two degenerate quadratic
forms with intersecting radicals.  Passing to `(c,p,k,z)` turns the pencil
into two coordinate stars.  Purity then factors as the determinant
`mn lambda^2`, so the component branching is a pair of Schubert flag
conditions rather than a primary decomposition.

The common-smooth-point argument is the algebraic-geometric analogue of
recognizing two coordinate charts on the same manifold: once both
six-parameter charts meet at a smooth six-dimensional point, no second local
component is available.

## Verification

Run:

```text
uv run --with sympy python verify_p4_overlapping_secant_lower_pair_classification.py
python audit_p4_overlapping_secant_lower_pair_classification.py
```

The primary verifier derives (10), (14), both exact minors, the pair profile,
and the common-point row-space equality.  The independent audit uses
dual-number subset-DP permanents and rational row reduction.  Neither
performs a search.
