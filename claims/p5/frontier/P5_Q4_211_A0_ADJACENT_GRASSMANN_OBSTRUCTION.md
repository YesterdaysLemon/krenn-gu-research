# Grassmannian obstruction on the adjacent `a=0` boundary

## Status

This note exactly excludes adjacent singleton-normal incidence in
normalized `q4_211` over `C` on

```text
a=0,   b c != 0.                                    (1)
```

The adjacent two-cross branch was already excluded.  In the remaining
one-cross branch, the third embedded `P_4` forces two rank-two row
planes.  A six-dimensional pair-contraction space turns their possible
incidence into a degeneracy locus on `Gr(2,4)`.  That locus consists of
five ordered pairs of planes in one complete quadrangle.  A
complementary flattening has a constant nonzero `2x2` minor at each of
the five points, contradicting the required rank-one target.

Together with the earlier `a=0` reduction, this proves that adjacent
incidence is empty on (1).  It does **not** exclude exact disjoint
incidence on (1), all normalized `q4_211`, the other local strata of
`P_5 -> Delta_3`, or the global Krenn--Gu conjecture.

## The four-dimensional support

Put

```text
s=e_1+e_2,
J=span(e_0,s,e_3,e_4)=h_0^perp,
h_0=e_1-e_2.                                       (2)
```

At `a=0`, contraction by the doubled-colour row is

```text
u_0 contract P_5=P_4(e_0,s,e_3,e_4).               (3)
```

Use the `q` orientation of the adjacent one-cross architecture:

- `A` contains `h_1,h_2`;
- `Y` contains the opposite pencil `span(h_1,n)`;
- `C` contains `h_2`; and
- `D` is the fourth mode.

The preceding `a=0` reduction and common-kernel obstruction give

```text
h_0 in R_C intersect R_D,
u_1 in R_C union R_D,
L_A(s) != 0,
L_Y(s) != 0.                                       (4)
```

The restrictions of `A,Y` to `J` have rank three.  Indeed, a rank drop
would put `h_0`, the annihilator of `J`, in the corresponding ambient
row space, contrary to the proof of (4).  The restrictions of `C,D`
have rank two: their three-dimensional ambient row spaces contain
`h_0`, and the restriction kernel on rows is exactly `C h_0`.

Rescale the two singleton coordinates, which changes (3) only by a
nonzero scalar.  In dual coordinates

```text
(E,S,P,Q)
```

on `J`, the relevant rows become

```text
h =E-Q,            u =E+P,
n =P+Q,            m =P-Q,
u+=E+Q,             h1=E-P.                         (5)
```

Here `h` represents `h_2`, `u` represents `u_1`, and `m` represents
`c u_1-b u_2`.

The common annihilator of `h_1,h_2` is
`span(S,k_+)`, where `k_+=(1,0,1,1)`.  The common annihilator of
`h_1,n` is `span(S,k_-)`, where `k_-=(1,0,1,-1)`.  Since neither
kernel is `S`, the two projective kernel lines have the forms

```text
kappa_A=(1,rho,1, 1),
kappa_Y=(1,sigma,1,-1)                              (6)
```

for arbitrary `rho,sigma in C`.  This parametrization includes
`rho=0` and `sigma=0`; no affine point at infinity is omitted.

Convenient bases of the two row hyperplanes are

```text
A:
  a0=(-rho,1,0,0),
  a1=(-1,0,1,0),
  a2=(-1,0,0,1);

Y:
  y0=(-sigma,1,0,0),
  y1=(-1,0,1,0),
  y2=(1,0,0,1).                                    (7)
```

## The pair-contraction space

Let `T=P_4` on `J`.  For two rows `r,z in J^*`, define

```text
mu(r,z)=T(r,z,-,-) in W,                            (8)
```

where `W` is the six-dimensional space of squarefree quadrics.  In the
ordered coordinates

```text
01,02,03,12,13,23,
```

the component indexed by `{i,j}` is

```text
mu(r,z)_ij=r_k z_l+r_l z_k,
{k,l}={0,1,2,3}\{i,j}.                              (9)
```

There is a nondegenerate complement pairing `B` on `W`, pairing each
coordinate with the complementary pair, such that

```text
T(r,z,c,d)=B(mu(r,z),mu(c,d)).                      (10)
```

Its matrix consists of three exchange blocks and has determinant
`-1`.

Let

```text
M(U,V)=span{mu(r,z):r in U,z in V}.                 (11)
```

Using (7), the matrix whose nine columns span `M(R_A|J,R_Y|J)` is

```text
[ 0           0      0       0       0  1       0  1  0 ]
[ 0           0      1       0       0  0       1  0  0 ]
[ 0           1      0       1       0  0       0  0  0 ]
[ 0           0   -rho       0       0 -1  -sigma -1  0 ]
[ 0        -rho      0  -sigma      -2  1       0 -1  0 ]
[-rho-sigma   -1      1      -1       0  0      -1  0  0 ].
                                                               (12)
```

The minor on rows `0,1,2,4,5` and columns `1,2,4,5,6` is the constant

```text
4.                                                    (13)
```

Thus

```text
dim M(R_A|J,R_Y|J) >= 5.                            (14)
```

The target image of (3) is a nonzero decomposable tensor, so its
`AY|CD` flattening has rank one.  By (10), the kernel of the induced
map from `M(R_C|J,R_D|J)` lies in the orthogonal complement of the
space in (14).  That orthogonal complement has dimension at most one.
A rank-one map has kernel of codimension at most one, hence

```text
dim M(R_C|J,R_D|J) <= 2.                            (15)
```

This is the key compression: (15) is a small Grassmannian incidence
condition, not a search over the four ambient maps.

## First Schubert calculation

Suppose `R_D|J` contains `u`.  Then write

```text
U=R_C|J=span(h,x),
V=R_D|J=span(u,y),

x=(0,x_s,x_p,x_q),
y=(0,y_s,y_p,y_q).                                 (16)
```

The first coordinates can be removed by adding multiples of `h,u`.
The `3x3` minors of the six-by-four matrix

```text
[mu(h,u),mu(h,y),mu(x,u),mu(x,y)]
```

have a Groebner basis containing

```text
x_s y_s,
y_s(x_p+x_q),
x_s(y_p+y_q),
x_q y_s^2,
x_s^2 y_q.                                         (17)
```

If `x_s` were nonzero, (17) would make `y=0`; if `y_s` were nonzero,
it would make `x=0`.  Both contradict (16), so

```text
x_s=y_s=0.                                         (18)
```

Put

```text
A=x_p+x_q,
B=y_p+y_q,
C=x_p y_q+x_q y_p,
D=x_p y_q-x_q y_p.
```

After (18), four minors are, up to signs,

```text
A B,   B C,   A C,   D C.                          (19)
```

If `C!=0`, then `A=B=D=0`, so both moving rows are `m`.
If `C=0`, then `AB=0`; nonzeroness of `x,y` gives either
`x=m,y=n` or `x=n,y=m`.  Therefore the only ordered pairs are

```text
(P_h,P),  (P_h,P_u),  (P,P_u),                     (20)
```

where

```text
P_h=span(h,m),
P  =span(h,u)=span(u,n),
P_u=span(u,m).                                     (21)
```

## The fixed-plane calculation

It remains possible that `u` occurs already at `C`.  Then

```text
R_C|J=P
```

and `R_D|J=V` is initially arbitrary.

Define the two linear operators

```text
H(v)=mu(h,v),   G(v)=mu(u,v).                       (22)
```

Both have rank three, with

```text
ker H=C u+,   ker G=C h1.                           (23)
```

If `V` contained neither kernel, `H|V` and `G|V` would both be
injective.  Condition (15) would force `H(V)=G(V)`.  Solving
`H(v)=G(w)` gives

```text
v_S=0,   v_E=v_P+v_Q.                              (24)
```

Thus `V` would equal `span(u,u+)=P_u`, which contains `u+`, contrary
to the assumed injectivity of `H|V`.  Hence `V` contains at least one
of the kernel lines in (23).

If `u+ in V`, write

```text
V=span(u+,(0,z_s,z_p,z_q)).
```

The `3x3` minors of

```text
[H(z),G(u+),G(z)]
```

give

```text
z_s^2=z_s z_p=z_s z_q=0,
(z_p-z_q)(z_p+z_q)=0.                              (25)
```

Over `C`, this yields `V=P_u` or

```text
P_0=span(n,u+).
```

The branch `h1 in V` has the same equations and yields
`V=P_h` or `P_0`.  Therefore

```text
(P,P_h), (P,P_u), (P,P_0)                          (26)
```

are the only fixed-plane pairs.

Combining (20) and (26), the complete degeneracy locus relevant here
is the five-point ordered set

```text
(P_h,P), (P_h,P_u), (P,P_h), (P,P_u), (P,P_0).     (27)
```

The four planes `P_h,P,P_u,P_0` are the sides through the marked
vertices of the complete quadrangle determined by the six rows in
(5).

## The complementary flattening excludes all five points

For each ordered pair `(U_C,U_D)` in (27), form the `9x4` matrix

```text
F_((i,j),(k,l))=T(a_i,y_j,c_k,d_l),                 (28)
```

using the bases in (7) and the displayed bases in (21), (25).  Rows
and columns in the following table are zero-indexed pairs of basis
indices.  Each indicated `2x2` determinant is independent of
`rho,sigma`:

| `(U_C,U_D)` | flattening rows | flattening columns | determinant |
| --- | --- | --- | ---: |
| `(P_h,P)` | `(0,1),(2,0)` | `(0,0),(0,1)` | `-4` |
| `(P_h,P_u)` | `(0,2),(2,0)` | `(0,0),(1,1)` | `4` |
| `(P,P_h)` | `(0,1),(2,0)` | `(0,0),(0,1)` | `-4` |
| `(P,P_u)` | `(0,2),(2,0)` | `(1,0),(1,1)` | `4` |
| `(P,P_0)` | `(0,1),(0,2)` | `(0,0),(1,0)` | `4` |

Thus every matrix (28) has rank at least two.  But it is precisely the
`AY|CD` flattening of the nonzero decomposable target image of (3),
which must have rank one.  This contradiction excludes all of (27).

The colour-swapped `p` orientation interchanges the two singleton
coordinates and gives the same quadrangle and the same obstruction.
Therefore adjacent incidence is empty on (1).

## Consequence

The remaining normalized `q4_211` frontier has now been reduced to
exact disjoint incidence on

```text
a=0,   b c != 0.
```

The generic stratum and the `b=0,c=0` boundary faces are already
excluded, while parallel incidence on `bc!=0` reselects as adjacent.

## Verification

Run:

```text
python verify_p5_q4_211_a0_adjacent_grassmann.py
python audit_p5_q4_211_a0_adjacent_grassmann.py
```

The primary verifier checks the complement pairing, the constant
five-by-five minor (13), both exact Grassmannian classifications, and
the five constant flattening minors.  The independent audit repeats
the classification over `F_5,F_7`, enumerating only the small
`Gr(2,4)` and the two projective kernel parameters.  It does not
enumerate ambient maps.  The finite-field calculation audits the
formulas and case split; the proof above is over `C`.
