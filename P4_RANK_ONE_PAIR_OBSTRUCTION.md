# A nonzero pure `P_4` restriction has no rank-one pair image

## Status

**Exact characteristic-zero theorem.**  Let

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and let `U_0,...,U_3` be two-planes in `R_1`.  If the restriction of the
order-four permanent to `U_0 tensor ... tensor U_3` is nonzero and pure,
then

```text
dim(U_i U_j) >= 2                         for every i!=j.       (1)
```

More precisely, if two planes `U,V` have one-dimensional product image,
then for some distinct source coordinates `p,q`,

```text
U=V=span(X_p,X_q),
UV=C X_pX_q.                                           (2)
```

The multiplication form in (2) is nondegenerate of rank two.  This rank-two
binary slice prevents any nonzero four-mode restriction containing the pair
from being decomposable.

This closes pair-image ranks zero and one in the pure-`P_4` component
problem.  Exact rank two remains possible and sharp.

## The projective zero-product garden

For nonzero linear forms `u,v`, the relation `uv=0` says

```text
u_i v_j+u_j v_i=0                       for i<j.       (3)
```

If `u` has at least three nonzero coordinates, the ratios `v_i/u_i` would
have to be pairwise opposite; three indices force them all to vanish.  If
`u` has support two, `v` has the same support and is its opposite binary
direction.  Support one gives the repeated coordinate point.  Hence the
projectivized zero-product incidence is exactly

```text
Z=union_{p<q} C_pq,

C_pq={([aX_p+bX_q],[aX_p-bX_q]):[a:b] in P^1}.       (4)
```

Thus a seemingly four-variable annihilator variety is only six rational
curves.

## A rank-one image would sweep out one of the six curves

Suppose `dim(UV)=1`, and choose a generator `Q` of the product image.  There
is a bilinear form

```text
B:U x V -> C,                 uv=B(u,v)Q.             (5)
```

The form has no left radical.  Otherwise a nonzero `u` would annihilate the
whole two-plane `V`, contradicting

```text
dim Ann_R1(u) <= 1.                                  (6)
```

The same argument removes the right radical, so `B` is nondegenerate.  For
every `[u] in P(U)` there is therefore a unique `[v] in P(V)` with `uv=0`.
These pairs form the graph of a projective isomorphism

```text
Gamma_B isomorphic to P^1,       Gamma_B subset Z.    (7)
```

The curve `Gamma_B` is irreducible, while (4) is a finite union of closed
curves.  Consequently `Gamma_B` lies in one `C_pq`.  Its two projections
span `U` and `V`, so both planes equal `span(X_p,X_q)`.  This proves (2).

## The remaining binary form is not pure

In the coordinate bases `(X_p,X_q)`, multiplication in (2) is

```text
(aX_p+bX_q)(cX_p+dX_q)=(ad+bc)X_pX_q.               (8)
```

The coefficient matrix of `ad+bc` is

```text
[0 1]
[1 0],                                               (9)
```

which has rank two.  Let `{r,s}` be the complementary source coordinates.
For any other two planes `W,Z`, the four-mode Frobenius form factors as

```text
P_4(u,v,w,z)=(ad+bc) * coeff_{X_rX_s}(wz).           (10)
```

If (10) is nonzero, fixing `w,z` with nonzero second factor leaves the
rank-two binary slice (9).  A decomposable four-tensor has rank at most one
on every such slice.  Therefore (10) cannot be both nonzero and pure, proving
(1).

## Across the mathematical fence

The useful translation is from multiplication rank to the geometry of the
annihilator correspondence.  Rank one would create a complete projective
matching between two row pencils.  But the zero-product incidence of the
squarefree complete intersection is a reducible curve with only six
components, so irreducibility traps the matching in one coordinate block.
Frobenius--Kunneth separation then exposes the nonsplit binary form.

In algebraic-geometric language, (4) is a small reducible correspondence;
in linear-algebra language, (9) is a nondegenerate hyperbolic plane.  The
combination rules out the entire stratum without elimination or enumeration.

## Verification

Run:

```text
uv run --with sympy python verify_p4_rank_one_pair_obstruction.py
python audit_p4_rank_one_pair_obstruction.py
```

The primary verifier checks the six curve parameterizations, the general
annihilator equations on each support size, and the binary/Frobenius ranks.
The independent audit source-permutes all six coordinate blocks and checks
exact rational slices.  Neither performs a search.
