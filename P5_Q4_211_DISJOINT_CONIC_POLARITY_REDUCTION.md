# Disjoint-incidence conic-polarity reduction for normalized `q4_211`

## Status

This note proves an exact projective-geometric reduction over `C` for
the generic disjoint singleton-normal incidence type in normalized
`q4_211`.

Assume

```text
a b c != 0
```

and label the remaining four modes so that

```text
h_1 in R_A,R_B,   h_1 notin R_C,R_D,
h_2 in R_C,R_D,   h_2 notin R_A,R_B,                (1)
```

where

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1).
```

Then all four maps have rank two on one explicit three-space, and one
of the two normal pairs has the same restricted kernel:

```text
ker(L_A|H)=ker(L_B|H)=span(e_1+e_2)
```

or

```text
ker(L_C|H)=ker(L_D|H)=span(e_1+e_2).                 (2)
```

Thus exact disjoint incidence lies on a common-kernel conic-polar
boundary.  A later kernel-propagation argument excludes that boundary
and therefore the whole exact disjoint type on `abc != 0`; see
[`P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md`](P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md).
This note alone does **not** exclude normalized `q4_211`,
`P_5 -> Delta_3`, or the arbitrary-order Krenn--Gu conjecture.

## The nondegenerate mixed contraction

Put

```text
s=e_1+e_2,
d=e_1-e_2,
w=e_0-b e_3-c e_4,
H=span(s,d,w).                                       (3)
```

Exact differentiation gives

```text
Q=(u_0,h_1,h_2) contract P_5
 =a x_1x_2+(x_1+x_2)(x_0-bx_3-cx_4).                (4)
```

Up to harmless nonzero normalization of symmetric tensors, the matrix
of `Q` in the basis `(s,d,w)` is

```text
M=[
 [ a/2,    0, 1 ],
 [   0, -a/2, 0 ],
 [   1,    0, 0 ]
].                                                    (5)
```

Its determinant is `a/2`, so it is nondegenerate.

Contract the target identity

```text
Phi(u_0)=lambda_0 e_0^4
```

at one mode from `{A,B}` by the pullback of `h_1` and at one mode from
`{C,D}` by the pullback of `h_2`.  The two complementary modes form
one of the four cross pairs

```text
AC, AD, BC, BD.
```

For every such pair `(i,j)`,

```text
(L_i tensor L_j)Q in span(e_0 tensor e_0),           (6)
```

possibly with zero scalar.  Hence every cross-pair matrix has rank at
most one.

## Exact disjointness forces four rank-two restrictions

Write

```text
r_i=rank(L_i|H).
```

Since `dim(H)=3`, the ambient rank-three condition gives `r_i>=1`.
In fact `r_i` cannot be one.

Suppose for example that `i` is one of `A,B`.  Its row space contains
`h_1`.  If `r_i=1`, then

```text
dim(R_i intersect H^perp)=2.
```

As `dim(H^perp)=2`, the whole annihilator `H^perp` lies in `R_i`.
But

```text
c h_1-b h_2 in H^perp,                               (7)
```

and `b != 0`, so `h_2 in R_i`, contradicting (1).  The same argument
with the two normals interchanged handles `C,D`.  Thus

```text
r_i>=2 for all i.                                    (8)
```

If some `r_i=3`, choose a cross-pair partner `j`.  Sylvester's rank
inequality applied to the invertible matrix (5) gives

```text
rank((L_i tensor L_j)Q)
 >= r_i+r_j-3
 >=2,
```

contradicting (6).  Therefore

```text
r_A=r_B=r_C=r_D=2.                                   (9)
```

Let `k_i` be the projective kernel line of `L_i|H`.  Both `h_1` and
`h_2` vanish on `span(s,d)` and are nonzero on `w`:

```text
h_1(w)=2b, h_2(w)=2c.
```

Since the applicable normal is in each row space, (9) implies

```text
k_i subset E=span(s,d) for every i.                  (10)
```

## The polarity on kernel lines

For two rank-two maps on the nondegenerate bilinear tensor `M`, the
image has rank one exactly when their kernel lines are polar:

```text
k_i^T M^(-1) k_j=0.                                  (11)
```

Indeed, choose row bases for the two annihilator planes
`k_i^perp,k_j^perp`.  Their `2 x 2` restricted matrix is singular
exactly when some row in `k_i^perp` is carried by `M` to the line
annihilating `k_j^perp`, which is equivalent to (11).  Its rank cannot
be zero by Sylvester's inequality, so (6) gives (11) on all four cross
edges.

The inverse of (5) is

```text
M^(-1)=[
 [ 0,    0,    1 ],
 [ 0, -2/a,    0 ],
 [ 1,    0, -a/2]
].                                                    (12)
```

Write a kernel line in (10) as

```text
k_i=sigma_i s+delta_i d.
```

Restricting (12) to `E` turns (11) into

```text
delta_i delta_j=0.                                   (13)
```

for each of the four edges of the complete bipartite graph
`{A,B}|{C,D}`.  Hence

```text
delta_A=delta_B=0
```

or

```text
delta_C=delta_D=0.
```

These are exactly the two alternatives in (2).

The distinguished line `span(s)` is the radical of the restricted
inverse-polarity form on `E`.  This explains why the result is a
common-kernel boundary rather than an immediate contradiction.

## Consequence and remaining boundary

Extra containments excluded in (1) can be reselected as adjacent or
parallel incidence types.  The genuinely disjoint generic type is
therefore reduced to the two colour-swapped alternatives (2).

The common kernel has since been combined with the two embedded `P_4`
tensors

```text
u_1 contract P_5=Sym(e_1,e_2,e_4,e_0+b e_3),
u_2 contract P_5=Sym(e_1,e_2,e_3,e_0+c e_4).
```

Repeated-normal contractions propagate `span(e_1+e_2)` to a third
mode and leave only kernel patterns `(s,s,s,s)` and `(s,s,d,s)`.
The second forces an incompatible `n` target row; the first kills the
required doubled-colour-zero coefficient.  Thus exact disjoint
incidence is empty on `abc != 0`.  The parameter boundary `a=0` is
excluded from the polarity argument because (5) becomes singular;
`b=0` and `c=0` are likewise separate normal-form boundaries.

## Verification

Run:

```text
python verify_p5_q4_211_disjoint_conic_polarity.py
python audit_p5_q4_211_disjoint_conic_polarity.py
```

The primary verifier differentiates (4), checks the determinant and
inverse in (5), (12), reconstructs `H^perp` and (7), and derives the
restricted polarity equation (13) symbolically.  The independent audit
rederives the contraction apolarly and enumerates only the projective
kernel lines over `F_3,F_5`, checking every `K_(2,2)` polarity pattern.
It does not enumerate ambient row spaces or local maps.  The
finite-field census audits the case split; the proof above is over
`C`.
