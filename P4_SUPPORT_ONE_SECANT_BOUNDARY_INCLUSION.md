# Support-one secants are boundaries of the disjoint-secant component

## Status

**Exact characteristic-zero boundary theorem.**  Suppose a nonzero pure
`P_4` restriction has an exact rank-two pair whose Segre-secant kernel
contains a support-one zero product.  Then, up to source and mode symmetry,
it lies in the closure of the disjoint-secant component proved in
[`P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md`](P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md).
It therefore creates no sixteenth component.

Together with the tangent, disjoint-support, and overlapping-support
classifications, this closes the last support degeneration for a **single**
exact-rank-two pair.  Compatibility among several rank-two pairs remains a
separate question.

## The other secant point must be disjoint

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

A support-one zero product is, after rescaling, `e tensor e` with `e=X_0`.
If the second point of the secant is also support one, the two pair planes
are the same coordinate two-plane and their product image is spanned by one
cross-product.  Its rank is one, not two.

Otherwise the second zero product has two-coordinate support and can be
written

```text
a=X_i+tX_j,       a_bar=X_i-tX_j,       t!=0.       (1)
```

If `0` belongs to `{i,j}`, then both pair planes are again the same
coordinate two-plane and their two cross-products are proportional.  Exact
rank two is impossible.  Consequently `{i,j}` is disjoint from `{0}`.  A
source permutation gives

```text
e=X_0,
a=X_1+tX_2,       a_bar=X_1-tX_2,
U_0=span(e,a),    U_1=span(e,a_bar).                 (2)
```

The pair image is spanned by `e*a_bar` and `a*e`, which are independent.

## The common-radical two-star problem

Let `Q,R` be the top-degree catalecticant forms of `e*a_bar` and `a*e`.
In the adapted basis

```text
c=e,       p=a_bar,       k=a,       z=X_3,          (3)
```

their only active entries, up to nonzero scalars, are

```text
Q(p,z)!=0,       R(k,z)!=0.                          (4)
```

Thus they are coordinate stars sharing the radical line `C*c`, exactly the
linear-algebra model appearing in the overlapping `1+3` secant
classification.  On the dense polar-line chart, put

```text
ell=p+lambda z,       ell_bar=p-lambda z,

A=span(c+m k, ell+u k),
B=span(c+n k, ell_bar+v k).                          (5)
```

The remaining restricted catalecticant has matrix

```text
[ 0                 -m lambda ]
[ n lambda    lambda(v-u)      ],                   (6)
```

so its determinant is `m*n*lambda^2`.  The two maximal branches `m=0` and
`n=0` are exchanged by swapping `A,B`.  It is enough to treat `m=0`:

```text
A=span(e, a_bar+lambda z+u a),
B=span(e+n a, a_bar-lambda z+v a).                  (7)
```

Direct squarefree permanent expansion leaves only

```text
T_1010= 2 lambda n t,
T_1011=-2 lambda t(u-v),                             (8)
```

and hence gives a pure tensor.  The dense nonzero part has
`t*lambda*n!=0`; the remaining nonzero points are in its parameter closure.

## A valuative arc from component fifteen

Introduce a formal parameter `epsilon` and split the singleton point into
the binary zero product

```text
g_plus =e+epsilon z,       g_minus=e-epsilon z.      (9)
```

For `epsilon!=0`, the two zero products

```text
g_plus*g_minus=0,       a*a_bar=0                   (10)
```

have disjoint two-coordinate supports.  Define

```text
L   = 2 epsilon/lambda,
M   =-2u epsilon/lambda,
N   = 1/n,
rho =-1+2v epsilon/(lambda n),                       (11)

U_0(epsilon)=span(g_plus,a),
U_1(epsilon)=span(g_minus,a_bar),

A(epsilon)=span(g_minus+M a, g_plus+L a_bar),
B(epsilon)=span(a+N g_minus,
                g_plus-L a_bar+rho g_minus).        (12)
```

Equations (9)--(12) are exactly the maximal flag chart of the disjoint
`2+2` component, with the two hyperbolic blocks
`span(g_plus,g_minus)` and `span(a,a_bar)`.  Thus every punctured point of
the arc lies in component fifteen.

The ordinary row limits of the last two planes lose rank, but their leading
Pluecker vectors do not.  With `pl` denoting the six Pluecker coordinates,
exact expansion gives

```text
lim_(epsilon->0) pl(A(epsilon))/epsilon
  =(2/lambda) pl(A),

lim_(epsilon->0) pl(B(epsilon))/epsilon
  =(-2/(lambda n)) pl(B),                            (13)
```

while `U_0(epsilon)` and `U_1(epsilon)` tend directly to the planes in
(2).  Therefore the Grassmannian limit is precisely (2),(7).

This proves containment on the dense `lambda*n!=0` branch.  Component
fifteen is closed, so parameter closure supplies `n=0` and the lower flag
strata; a mode swap supplies the other maximal branch.  Hence every
support-one exact-rank-two secant is already a boundary of component
fifteen.

The mechanism is valuative rather than eliminative: the limiting subspace
is stored in the leading exterior power after the row matrix itself drops
rank.  This is the same idea used by limit linear series and tropical
Grassmannian degenerations, here applied to the permanent-compression
variety.

## Exact replay

```text
uv run --with sympy python verify_p4_support_one_secant_boundary_inclusion.py
python audit_p4_support_one_secant_boundary_inclusion.py
```

The primary verifier checks the support dichotomy, star determinant, pure
family, exact component arc, Pluecker limits, and a rational pair profile.
The independent audit uses only rational Laurent arithmetic, a subset-DP
permanent, and exact Gaussian elimination.

No parameter search, numerical solve, Groebner basis, or component census is
used.
