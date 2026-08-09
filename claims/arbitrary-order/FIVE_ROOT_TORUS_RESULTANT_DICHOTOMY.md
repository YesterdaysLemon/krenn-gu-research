# Five-root torus-resultant dichotomy

## Status

This is an exact algebraic-geometric lemma over `C`.  For the ten
bilinear forms on five three-dimensional modes, it identifies fifteen
explicit resultant hypersurfaces that contain every coefficient tuple
whose common-zero scheme meets a coordinate boundary.  Away from their
union, the five-root intersection theorem therefore produces a fully
supported, pairwise zero-coupled root tuple.

The result is a genericity criterion and an arbitrary-order structural
dichotomy.  It does **not** show that the edge blocks of a hypothetical
Krenn--Gu witness avoid the resultants, exclude the blocker-surplus branch,
or prove the conjecture.

## Coefficient space and boundary incidence

Let `V_i=C^3` for `i=0,...,4`, put

```text
X = product_(i=0)^4 P(V_i),
E = {{i,j}:0<=i<j<=4},
P = product_(ij in E) P((V_i tensor V_j)^*).
```

Thus `P=(P^8)^10` parametrizes ten nonzero bilinear forms `B_ij`, and
`dim(P)=80`.  Write `h_i` for the hyperplane class from the `i`th factor
of `X`.

Fix a vertex `i` and a colour `c`.  The coordinate boundary

```text
Y_(i,c)={x_i[c]=0} subset X
```

is isomorphic to `P^1 x (P^2)^4` and has dimension nine.  Define the
projective incidence variety

```text
I_(i,c) = {(x,B) in Y_(i,c) x P:
           B_jk(x_j,x_k)=0 for every jk in E}.          (1)
```

For fixed `x`, each equation in (1) is one nonzero linear condition on
its own `P^8` coefficient block.  Hence the fibre over `x` is
`(P^7)^10`.  In particular, `I_(i,c)` is an irreducible projective bundle
over `Y_(i,c)` and

```text
dim I_(i,c)=9+10*7=79.                                  (2)
```

## Boundary resultant theorem

The image

```text
D_(i,c)=image(I_(i,c) -> P)                             (3)
```

is an irreducible hypersurface.  Equivalently, there is an irreducible
multihomogeneous polynomial, unique up to a nonzero scalar,

```text
Res_(i,c)((B_jk)_(jk in E)),                            (4)
```

such that

```text
Res_(i,c)(B)=0
  <=> the ten forms have a common projective zero with x_i[c]=0. (5)
```

Its degree in an edge-coefficient block is

```text
deg_(B_jk) Res_(i,c) = 12   if i belongs to {j,k},
                         10   if i does not belong to {j,k}.     (6)
```

Consequently its ordinary total degree is

```text
4*12+6*10=108.                                          (7)
```

### Proof that the image is a hypersurface

The projection in (3) is proper, so its image is closed and irreducible.
It remains to show that its dimension is 79 rather than smaller.

Fix an edge `e`, and choose general forms on the other nine edges.  Their
zero divisors on `Y_(i,c)` come from basepoint-free linear systems and
meet in a finite scheme.  Its length is the positive top intersection

```text
d_e = integral_(Y_(i,c)) product_(f in E minus {e})
                              (h_left(f)+h_right(f)).    (8)
```

For every point of this finite scheme, the remaining form `B_e` must lie
in one evaluation hyperplane in its coefficient `P^8`.  Thus, over a
dense open set of choices for the other nine blocks, the image in (3)
has a codimension-one fibre condition in the final block.  Together with
(2), this proves that `D_(i,c)` is a hypersurface.  Its defining equation
has degree `d_e` in the coefficients of `B_e`: for general choices the
finite intersection is reduced and its omitted-edge evaluation points are
distinct, so the resulting `d_e` evaluation hyperplanes are distinct.
Here is a dimension check for the parenthetical genericity.  If two distinct
roots give the same evaluation hyperplane for the omitted edge `e`, equality
of the two projective rank-one endpoint tensors forces both endpoints of `e`
to agree.  Let `S` be the vertex set on which the two roots agree, let `s` be
its size, and let `q` be the sum of the projective-factor dimensions outside
`S`.  Among the other nine blocks, exactly
`m=binomial(s,2)-1` pairs of evaluation conditions coincide.  The resulting
two-point incidence has dimension

```text
9+q+9*6+m = 63+q+m <= 70 < 72,                       (9)
```

where `72=9*dim(P^8)` is the parameter-space dimension of the nine fixed
blocks; the inequality is the four-case check `s=2,3,4` with one factor of
dimension one and four of dimension two.  Thus evaluation-hyperplane
coincidence is a proper closed condition.  A general point of one hyperplane
avoids all the others and therefore has a unique incidence preimage.  The
projection in (3) has generic degree one; no hidden projection degree divides
`d_e`.

### Exact multidegree

In the Chow ring of `Y_(i,c)`, the top exponent is one at vertex `i` and
two at every other vertex.  Expanding (8) assigns each of the nine edges
of `K_5-e` to one endpoint.  Therefore `d_e` counts orientations with

```text
indegree(i)=1,
indegree(j)=2 for j!=i.                                (10)
```

There are twelve such orientations when `e` is incident to `i`, and ten
when it is not.  This proves (6).  Positivity also supplies the finite
intersection used above.

## Torus-root criterion

Let

```text
R_boundary(B)=product_(i=0)^4 product_(c=0)^2 Res_(i,c)(B). (11)
```

If

```text
R_boundary(B) != 0,                                   (12)
```

then the common-zero scheme of the ten bilinear forms misses all fifteen
coordinate hyperplanes.  The five-root intersection theorem guarantees
that this scheme is nonempty.  Hence it contains a tuple

```text
([x_0],...,[x_4]) in ((C^*)^3/C^*)^5                  (12)
```

with every coordinate nonzero and every coupling `B_ij(x_i,x_j)=0`.

The condition (11) is a nonempty Zariski-open condition on `P`: each of
the fifteen factors defines a proper hypersurface, and `P` is
irreducible.  Intersecting it with the usual transverse open set shows
that a general ten-block system has exactly 24 distinct common zeros and
all 24 lie in the coordinate torus.

## Arbitrary-order blocker consequence

Evaluate the multihomogeneous resultants on affine representatives of the ten
blocks induced by any five vertices of a hypothetical even-order three-colour
witness.  If an induced block is zero, every resultant vanishes because (6)
has positive degree in every block.  Otherwise all ten blocks may be
projectivized and the theorem applies.  Exactly one of the following holds:

1. at least one of the fifteen boundary resultants vanishes; or
2. all fifteen boundary resultants are nonzero, there are five fully
   supported, pairwise zero-coupled roots, and then either their
   total blocker union has at least six vertices, or the tight-five-root
   extraction gives `P_5 -> Delta_3`.

Thus, conditional on excluding `P_5 -> Delta_3`, every induced `K_5` for
which no fully supported, pairwise zero-coupled root tuple has blocker union
of size at least six must lie on the fixed union of fifteen degree-108
boundary-resultant hypersurfaces.  This is a finite algebraic constraint on
the remaining boundary branch, not its exclusion.

## Exact replay

```text
python claims/arbitrary-order/verify_five_root_torus_resultant_dichotomy.py
python claims/arbitrary-order/audit_five_root_torus_resultant_dichotomy.py
```

The primary verifier expands the relevant Chow products directly and
checks the complete 15-by-10 multidegree table.  The independent audit
counts the endpoint orientations by a separate dynamic program and checks
the incidence dimensions and total degrees.  These computations verify
the discrete intersection numbers; projectivity, basepoint-freeness, and
the incidence argument above prove the theorem over `C`.
