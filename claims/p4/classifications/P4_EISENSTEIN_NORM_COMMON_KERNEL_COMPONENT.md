# A thirteenth pure `P_4` component from an Eisenstein norm quadric

## Status

**Exact algebraic-geometric component theorem over `C`.**  The pure
restriction locus of the order-four permanent has a five-dimensional
irreducible component arising from the active/active leaf orientation of a
common-kernel `(2,1,1)` triangle.  Its normalized moduli are a smooth
projective quadric, hence `P^1 x P^1` over `C`; the three-dimensional
diagonal source torus sweeps out the component.

On a dense open its pair-image profile, in edge order
`01,02,03,12,13,23`, is

```text
(4,4,4,3,3,3).                                      (1)
```

The triangle relation on `12` has coefficient rank two.  The relations on
`13,23` have coefficient rank one and are the same exact zero-divisor pair,
with the active leaf rows annihilating the common kernel row.  The graph is
shown in
[`research_figures/P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT_GRAPH.svg`](../../../research_figures/P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT_GRAPH.svg).

This raises the certified lower bound from twelve to thirteen symmetry-
inequivalent pure-`P_4` component orbits.  It is not component exhaustiveness
or a global proof of the Krenn--Gu conjecture.  Its generic marked `H31` and
weighted `H22` fibres were open at this checkpoint.  The generic `H31` fibre
is subsequently proved empty in
[`P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md`](../../p5/h31/eisenstein-norm/P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md).
The generic weighted `H22` fibre is subsequently proved empty in
[`P5_H22_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md`](../../p5/h22/eisenstein-norm/P5_H22_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md).
Special boundaries and the remaining support-one common-zero-divisor strata
remain open.

## The common-kernel normal form

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Put

```text
a=X_0+X_1,       c=X_0-X_1,
b=X_2+X_3,       b_bar=X_2-X_3,       ac=b*b_bar=0. (2)
```

For parameters `alpha,beta,r,gamma`, define

```text
m   =alpha*a+beta*c+b,
m_r =m+r*c,
d   =gamma*a+b,
x_0 =b-(alpha+gamma)*a-(2*beta+r)*c                 (3)
```

and the four marked planes, in row order `(y_i,x_i)`, by

```text
U_0=span(b_bar,x_0),
U_1=span(m,a),
U_2=span(m_r,a),
U_3=span(c,d).                                      (4)
```

The exceptional triangle relations are identically

```text
y_1x_2-x_1y_2=0,
x_1y_3=0,
x_2y_3=0.                                          (5)
```

Thus this is the `XX` leaf orientation left after the exact obstructions for
the `YY` and `YX` orientations.

## Three cubics collapse on one quadric

All seven kernel-containing triangle cubics span the same space as

```text
C_0=m*m_r*c,
C_1=m*m_r*d,
C_2=a*m*d.                                         (6)
```

In the degree-three basis indexed by the missing source coordinate, direct
squarefree multiplication gives the identity

```text
C_1=(2*beta+r)C_0+(2*alpha+gamma)C_2
    -2F*(0,0,1,1),                                 (7)
```

where

```text
F=alpha^2+alpha*gamma+gamma^2
  -3*beta^2-3*beta*r-r^2.                          (8)
```

The two rows of `U_0` annihilate `C_0,C_2`.  The first also annihilates the
all-active cubic `a^2d`, while the second pairs with it to `4`.  In fact the
entire four-mode restriction has only two possibly nonzero coefficients:

```text
T_1001=-4F,               T_1111=4.                (9)
```

Consequently `F=0` gives a nonzero pure tensor identically over the whole
parameter quadric.

## Across the mathematical fence: an Eisenstein norm torsor

Let

```text
N(x,y)=x^2+x*y+y^2.                                 (10)
```

This is the norm form of the Eisenstein quadratic extension, up to the
standard choice of generator.  Equation (8) is exactly

```text
N(alpha,gamma)=N(r+beta,beta).                      (11)
```

If `zeta^2+zeta+1=0`, put

```text
U=alpha-zeta*gamma,
V=alpha-zeta^2*gamma,
S=r+(1-zeta)*beta,
T=r+(1-zeta^2)*beta.                               (12)
```

Then (11) becomes the rank-one determinant

```text
U*V-S*T=0.                                         (13)
```

Thus the projectivized parameter surface is the Segre quadric
`P^1 x P^1`.  On the open set where the right norm is nonzero, (11) can also
be read as a norm-one torus equation for the ratio of two Eisenstein
numbers, the elementary Hilbert-90 shadow of the component.

This translation explains both the irreducibility and the otherwise
unexpected quadratic relation.  The permanent incidence is not being
solved by elimination here: it has become a rank-one matrix over the
quadratic splitting field.

## Five independent directions and a smooth incidence point

The Hessian determinant of `F` in `(alpha,beta,r,gamma)` is `9`, so the
projective quadric is smooth and irreducible.  Its two dimensions, together
with the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1),                                (14)
```

give five parameters.  The apparent affine radial direction of `F=0` is
already the block source scaling `t_0=t_1`; it is not a sixth family
direction.

At

```text
(alpha,beta,r,gamma)=(2,1,1,1),                    (15)
```

equation (8) holds, the pair profile is (1), and the relation ranks are
`(2,1,1)`.  In ordered Grassmann pivots

```text
(02),(01),(10),(01),                               (16)
```

the family tangent has rank five; one exact minor is

```text
1/864.                                             (17)
```

On the universal twenty-variable Segre incidence, the Jacobian has rank
fifteen at the same point.  One exact fifteen-by-fifteen minor is

```text
-2/81.                                             (18)
```

Hence the incidence is smooth of dimension five there.  The irreducible
quadric-torus family supplies all five local directions, so its closure is
an irreducible component.  A nonzero pure tensor has unique projective
factor lines; projection from the incidence to the plane tuple therefore
preserves this component.

## Why this is a new orbit

Dimension separates this fivefold from the three earlier sixfolds.  Among
the earlier fivefolds, the first apolar component is the only one with the
same exceptional triangle, pair profile, and relation-rank word `(2,1,1)`.
Its two rank-one zero-product labels are adjacent vertices of the support
octahedron `J(4,2)`; here both labels are the same vertex `{0,1}`.  Equality
versus adjacency of the two support labels is invariant under source and
mode permutations.

The equal-support eleventh component does have the same unmarked relation
support, but it is six-dimensional and has the opposite purity incidence:
its leaf factors are kernel rows and its common factor is active, whereas
in (5) the leaf factors are active and the common factor is the kernel row.
The transverse twelfth component has sorted pair profile
`(3,3,3,3,3,4)`, different from (1).  These invariants separate (4) from all
twelve previously certified component orbits.

## Verification

Run:

```text
uv run --with sympy python claims/p4/classifications/verify_p4_eisenstein_norm_common_kernel_component.py
python claims/p4/classifications/audit_p4_eisenstein_norm_common_kernel_component.py
```

The primary verifier checks (2)--(18) over characteristic zero.  The
independent audit works modulo `101`, uses Pluecker-ratio dual tangents rather
than the primary Grassmann chart, permutes and unequally scales the source
coordinates, and reconstructs the universal incidence derivatives directly.
It obtains family/incidence ranks `5/15` and a nonzero modular incidence
minor `86`.  Both are fixed-size exact replays, not searches.
