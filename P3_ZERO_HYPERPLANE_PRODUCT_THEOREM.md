# Zero restrictions of `P_3` to three planes

## Status

This is an exact tensor theorem over `C`.

Let `U_0,U_1,U_2` be subspaces of `C^3` of dimension at least two.  The
restriction of the order-three permanent tensor satisfies

```text
P_3 restricted to U_0 tensor U_1 tensor U_2 = 0        (1)
```

if and only if all three subspaces are the same coordinate plane:

```text
U_0=U_1=U_2=e_s^perp
```

for some source coordinate `s`.

The theorem classifies a zero `P_3` slice that arises when a rank-two
local map has three collinear source columns.  It is a structural input
for the shared rank-drop branch of `q5_311`; it does not by itself
exclude that branch or resolve the Krenn--Gu prize conjecture.

## Pair map

For `u,v in C^3`, define

```text
mu(u,v)=(
  u_1 v_2 + u_2 v_1,
  u_0 v_2 + u_2 v_0,
  u_0 v_1 + u_1 v_0
).                                                     (2)
```

Then

```text
P_3(u,v,w)=mu(u,v) dot w.
```

If (1) holds, `mu(U_0,U_1)` is contained in the annihilator of the
at-least-two-dimensional space `U_2`, so

```text
dim mu(U_0,U_1) <= 1.                                 (3)
```

## Classification of the pair image

Fix nonzero `v` and write `T_v(u)=mu(u,v)`.  Its matrix is

```text
[  0   v_2 v_1 ]
[ v_2   0  v_0 ]
[ v_1  v_0  0  ],
```

with determinant

```text
2 v_0 v_1 v_2.                                        (4)
```

Suppose two subspaces `U,V`, each of dimension at least two, satisfy
`dim mu(U,V)<=1`.

If `V` contained a vector with all three coordinates nonzero, (4) would
make `T_v` invertible.  Its restriction to `U` would then have rank at
least two, contradicting the pair-image bound.
Hence every vector of `V` has coordinate support at most two.

A subspace of dimension at least two with that property must be a
coordinate plane.  Indeed, if two basis vectors collectively used all three
coordinates, a generic linear combination would avoid the finitely many
coordinate cancellations and have support three.  Its dimension is
therefore exactly two and, after relabeling,

```text
V=span(e_p,e_q).
```

The kernel of `T_(e_p)` is the line `span(e_p)`.  Since its restriction
to `U` has rank at most one while `dim(U)>=2`, `U` has dimension two and
`e_p` lies in `U`.  The same
argument with `e_q` shows that `e_q` lies in `U`.  Therefore

```text
U=V=span(e_p,e_q).                                    (5)
```

The pair image in (5) is the line `span(e_s)`, where `s` is the
coordinate complementary to `{p,q}`.  A plane annihilates this line
exactly when it is `e_s^perp=span(e_p,e_q)`.  Applying this to `U_2`
proves the forward direction.  The converse follows immediately because
three vectors in the same two-coordinate plane cannot occupy all three
distinct source coordinates in a permanent term.

## Verification

Run:

```text
python verify_p3_zero_hyperplane_product.py
python audit_p3_zero_hyperplane_product.py
```

The primary verifier checks the determinant identity, the three
coordinate-plane pair images, and the resulting zero restrictions
symbolically.  The independent audit enumerates every triple of
rank-at-least-two subspaces over `F_3` and `F_5`; in each field exactly
the three common-coordinate-plane triples give zero.  The finite-field
census audits the boundary and the written proof above establishes the
theorem over `C`.
