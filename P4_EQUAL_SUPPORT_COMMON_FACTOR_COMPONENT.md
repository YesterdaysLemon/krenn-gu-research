# An eleventh pure `P_4` component from a shared exact zero divisor

## Status

**Exact algebraic-geometric component theorem over `C`.**  The locus of
ordered four-tuples of planes on which `P_4` restricts to a nonzero pure
tensor has a six-dimensional irreducible component with generic pair profile

```text
(4,4,4,3,3,3).                                      (1)
```

Its exceptional triangle has relation-rank pattern `(2,1,1)`.  Unlike the
first apolar component, the two rank-one edges use the same binary support
and the same active row at their common mode.  The new component is distinct
from the previously certified six-dimensional component, whose sorted pair
profile is `(2,3,3,4,4,4)`, and from every five-dimensional component.
Consequently the repository's certified lower bound rises from ten to
eleven symmetry-inequivalent pure-`P_4` component orbits.

This is a component construction and smoothness theorem, not a complete
classification of the common-factor Borel orientation.  Its generic marked
`H31` fibre is subsequently proved empty in
[`P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md).
Its weighted `H22` fibre, special-parameter/projective boundary, component
exhaustiveness, and the global Krenn--Gu conjecture remain open.

## The exact-zero-divisor normal form

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and put

```text
a=X_0+X_1,        a_bar=X_0-X_1,
b=X_2+X_3,        b_bar=X_2-X_3.                    (2)
```

Thus

```text
a a_bar=0,        b b_bar=0,
Ann_R1(a)=C a_bar.                                  (3)
```

For parameters `p,q,r`, define

```text
U_0=span(a+p b,       a_bar+q b),
U_1=span(a,           a_bar+b),
U_2=span(a,           r a_bar+b),
U_3=span(b_bar,       a_bar).                       (4)
```

In modes `1,2,3`, use the displayed row order `(y_i,x_i)`.  The exceptional
relations are

```text
y_1x_2-x_1y_2=0,       coefficient rank 2,
y_1x_3=0,               coefficient rank 1,
y_2x_3=0,               coefficient rank 1.         (5)
```

The last two relations are the same exact zero-divisor pair `a a_bar=0`.
They have equal support label `{0,1}` in the support octahedron from
[`P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md`](P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md).
This is the common-factor orbit that the crossed theorem deliberately did
not cover.

## Why the affine parameter `r` survives

Suppose two rank-one edges share a common row `z` and use kernel rows
`y_1,y_2` at their leaves.  The degree-one annihilator bound gives

```text
y_1 proportional to y_2 proportional to w,
wz=0.                                                 (6)
```

After scaling, the rank-two edge is

```text
w x_2=x_1 w.
```

Hence

```text
x_2-x_1 in Ann_R1(w)=Cz.                             (7)
```

Equation (7) is a synchronization law along the opposite zero-divisor line.
On the full binary-complement branch used below, diagonal source scaling gives

```text
w=a,       z=a_bar,
x_1=a_bar+b,       x_2=r a_bar+b.                   (8)
```

Unlike the crossed orientation, one relative translation parameter `r`
remains after the source torus is used.  The rank-one cubic branch constructed
below takes the common row to be the active row `x_3=a_bar` and its opposite
kernel row to be `y_3=b_bar`.  The theorem does not claim that these choices
classify every special common-factor boundary.

The homological shadow is a two-periodic exact-zero-divisor complex:

```text
... --a_bar--> R --a--> R --a_bar--> R --a--> ... .  (9)
```

Relation (7) says that the difference of the synchronized partners is a
cocycle valued in `Ann(a)=(a_bar)`.  Exact pairs and their totally reflexive
modules are studied, in a much broader setting, by Holm,
[Construction of totally reflexive modules from an exact pair of zero divisors](https://arxiv.org/abs/1002.0419),
and by Kustin--Striuli--Vraciu,
[Exact pairs of homogeneous zero divisors](https://arxiv.org/abs/1304.0411).
Those papers supply the neighboring homological language; they do not state
(4), its permanent, or the component theorem below.

## The apolar line and the pure tensor

Among the eight triple products of modes `1,2,3`, every kernel-containing
one is zero or proportional to

```text
C=a^2 b_bar.                                         (10)
```

Indeed, the only possibly nonzero second one is

```text
(a_bar+b)(r a_bar+b)b_bar=r a_bar^2b_bar,
```

and `a_bar^2=-a^2`.  Therefore

```text
Ann_R1(C)=span(a,a_bar,b).                           (11)
```

The plane `U_0` in (4) is a dense chart of

```text
Gr(2,Ann(C))=Gr(2,3)=P^2.                            (12)
```

The all-active cubic is

```text
X=(a_bar+b)(r a_bar+b)a_bar
  =-2(r+1)X_0X_1 b+2a_bar X_2X_3.                  (13)
```

Direct pairing with the two rows of `U_0` gives the only nonzero restricted
coefficients:

```text
T_0111=-4p(r+1),
T_1111=-4(1+q(r+1)).                                (14)
```

Thus (4) is a nonzero pure restriction whenever the vector in (14) is
nonzero.

## Exact exceptional graph

In edge order `01,02,03,12,13,23`, three exterior maximal minors are

```text
-8pq,       -8pq,       -8p.                        (15)
```

For the triangle, three rank-three minors are

```text
-4(r+1),       4,       4r^2.                       (16)
```

Consequently (1) holds, for example, on

```text
p q r(r+1)!=0.                                      (17)
```

The unique triangle relations are exactly (5), with coefficient ranks
`(2,1,1)`.  Notice that the common-factor support collision has increased
the normalized family dimension: the first crossed component had only its
apolar `P^2`, while (4) has that `P^2` plus `r`.

## Six independent family directions

Restore the projective diagonal source torus by applying

```text
D=diag(t_0,t_1,t_2,1)                               (18)
```

to every plane.  Use Grassmann pivot charts

```text
(01),(01),(01),(02)                                  (19)
```

for modes zero through three.  Row reduction gives

```text
N_0=((1,0, t_2(p+q)/(2t_0), (p+q)/(2t_0)),
     (0,1, t_2(p-q)/(2t_1), (p-q)/(2t_1))),

N_1=((1,0, t_2/(2t_0),  1/(2t_0)),
     (0,1,-t_2/(2t_1), -1/(2t_1))),

N_2=((1,0, t_2/(2rt_0),  1/(2rt_0)),
     (0,1,-t_2/(2rt_1), -1/(2rt_1))),

N_3=((1,-t_1/t_0,0,0),
     (0,0,1,-1/t_2)).                                (20)
```

Order each chart's four free entries rowwise and call the resulting sixteen
coordinates `g_0,...,g_15`.  At

```text
(p,q,r,t_0,t_1,t_2)=(1,2,2,1,1,1),                 (21)
```

the rows

```text
g_0,g_1,g_2,g_4,g_6,g_8
```

of the family Jacobian with respect to `(p,q,r,t_0,t_1,t_2)` have

```text
det=3/128.                                           (22)
```

The family image therefore has dimension six.

## Smooth component certificate

On the Grassmann charts (19), let `T_beta(g)` be the sixteen restricted
permanents.  In the target Segre chart at `alpha=0000`, introduce factor
ratios `z_0,...,z_3` and impose

```text
F_beta=T_beta-T_0000 product_(i: beta_i=1) z_i=0,
beta!=0000.                                         (23)
```

At (21), the normalized planes are

```text
N_0=((1,0, 3/2, 3/2),(0,1,-1/2,-1/2)),
N_1=((1,0, 1/2, 1/2),(0,1,-1/2,-1/2)),
N_2=((1,0, 1/4, 1/4),(0,1,-1/4,-1/4)),
N_3=((1,-1,0,0),(0,0,1,-1)),                       (24)
```

and

```text
T_0000=-5/2,       (z_0,z_1,z_2,z_3)=(-2/5,-1,-1,0). (25)
```

Take the fourteen Jacobian rows indexed by every `beta!=0000,1110` and the
fourteen columns

```text
g_0,g_1,g_2,g_4,g_5,g_6,g_8,g_9,g_10,
g_12,g_13,g_14,z_1,z_3.                             (26)
```

Their determinant is

```text
-9/2.                                                (27)
```

Hence the incidence tangent has codimension at least fourteen.  The six
independent family directions from (22) lift to the incidence, so the
tangent dimension is exactly six and the Jacobian rank exactly fourteen.
The incidence is smooth of dimension six at (21)--(25).

The parameter space is irreducible and its six-dimensional image lies in
the incidence by (14).  A smooth point has a unique local irreducible
component, so the family closure fills that component.  Since a nonzero
pure tensor has unique projective factors, the Segre incidence projects
isomorphically to the pure plane locus on this chart.  This proves the
component theorem.

## Why it is a new orbit

All ten previously certified component orbits are either five-dimensional
or belong to the six-dimensional component in
[`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](P4_SIX_DIMENSIONAL_PURE_COMPONENT.md).
That component has generic pair profile

```text
(4,3,2,4,4,3),       sorted (2,3,3,4,4,4).          (28)
```

The new profile (1) sorts to `(3,3,3,4,4,4)`.  Dimension and the pair-rank
multiset are invariant under source-coordinate permutations, diagonal
source scaling, and mode permutations.  Therefore the component in this
note is a new symmetry orbit, raising the certified lower bound to eleven.

The ambient algebra is a square-free monomial complete intersection.  Tran
and Skoldberg study the richer Hochschild-cohomology algebra of this class
([arXiv:1806.07802](https://arxiv.org/abs/1806.07802)); the component here
uses only its elementary Kunneth block split and Frobenius top pairing.  The
useful synthesis is:

```text
exact zero divisor -> affine synchronization parameter
                    -> one-dimensional cubic apolar space
                    -> P^2 opposite-plane fibre
                    -> six-dimensional smooth component.          (29)
```

## Verification

Run:

```text
uv run --with sympy python verify_p4_equal_support_common_factor_component.py
python audit_p4_equal_support_common_factor_component.py
```

The primary verifier checks (3)--(27) over `Q`, including the exact family
and incidence minors.  The independent audit permutes and unequally scales
the source coordinates, reconstructs the permanent by subset dynamic
programming, and recomputes both tangent ranks over `F_101` using forward
dual numbers.  These are fixed-size exact certificates, not searches.
