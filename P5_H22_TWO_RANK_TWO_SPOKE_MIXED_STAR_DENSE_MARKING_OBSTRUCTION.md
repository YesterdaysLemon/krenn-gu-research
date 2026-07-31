# Dense-marking weighted `H22` obstruction on the tenth component

## Status

**Exact characteristic-zero partial theorem.**  On a dense open subset of

```text
(tenth component) x (weighted slope) x (marked-basis chart),
```

both weighted binary extension matrices have rank eight.  Thus neither
weighted direction has any nonzero mixed-zero extension there, and the
weighted `H22` incidence is empty on that dense total-space open.

At the rational component point `(s,t)=(2,3)`, the stronger statement holds:
both mixed row modules equal the full rank-eight extension module for every
slope and every marking.

This is not yet a complete marked-fibre theorem over the generic component
point.  Markings on the remaining determinantal divisors are open.  In
particular, this file does not claim that the tenth component's full generic
weighted `H22` fibre is empty, does not settle component exhaustiveness, and
does not resolve the global Krenn--Gu problem.

The later eleventh component is generically closed for weighted `H22` by the
independent exact-zero-divisor identity in
[`P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md).
Consequently the marking divisors left here are now the sole generic weighted
frontier among the eleven certified components.

![The tenth component's mixed-star graph](research_figures/p4_two_rank_two_spoke_mixed_star.png)

## Cayley coordinates reveal the torus

Put

```text
u=(s-1)/(s+1),       v=(t-1)/(t+1),
rho=(r-1)/(r+1).                                      (1)
```

The fourth-plane parameter satisfies

```text
d=(1+st)/(s+t)=(1+uv)/(1-uv).                        (2)
```

Write a source row by its coefficients in

```text
(a,a_bar,b,b_bar),
```

where `a=X0+X1`, `a_bar=X0-X1`, `b=X2+X3`, and
`b_bar=X2-X3`.  After multiplying both rows of modes `1,2,3` by their
Cayley denominators, the component becomes polynomial:

```text
alpha0=(1,0,1,0),
 beta0=(0,0,1,0),

alpha1=(1-u,-1-u,1-u,-1+u),
 beta1=(0,-1-u,1-u,0),

alpha2=(1-v,-1-v,1-v,1-v),
 beta2=(0,-1-v,1-v,0),

alpha3=(0,0,0,1-uv),
 beta3=(1-uv,-1-uv,-1+uv,0).                        (3)
```

The marked rows are `beta_i+h_i alpha_i`.  Pulling (3) back to the original
squarefree coordinates gives the single pure coefficient

```text
T_1111=4(u-1)(v-1)(uv-1).                            (4)
```

The pullback in the previous sentence is essential.  The squarefree
permanent is not invariant under the Hadamard change from
`(X0,X1,X2,X3)` to `(a,a_bar,b,b_bar)`.  Formula (3) is a coordinate aid,
not permission to replace the original Frobenius form by a new permanent.

## The two weighted projections

After harmless diagonal target scalings, the original weighted maps become

```text
D_01^rho(A,Abar,B,Bbar,e)
  =(A+rho Abar, B+Bbar, B-Bbar, e),

D_23^rho(A,Abar,B,Bbar,e)
  =(A+Abar, A-Abar, B+rho Bbar, e).                  (5)
```

For each direction let `M_ij(u,v,rho,h)` be the `14 x 8` matrix of mixed
binary extension coefficients.  Any binary neighbour lies in its kernel.

## Two exact canonical-marking pivots

At the canonical marking `h=0`, take the first eight mixed-word rows in
lexicographic order.  The corresponding determinants factor as follows:

```text
det M_01[0:8] =
 -2048 rho^2(rho-1)(rho+1)(u-1)^3(u-v)(v-1)^3(uv-1)^4
 * (2rho uv-2rho+uv-u-v+1)
 * (-2rho u^2v^2+2rho u^2v+2rho uv^2-2rho uv
    +u^3v^2+u^2v^3-4u^2v^2+4uv-u-v),               (6)

det M_23[0:8] =
 4096 rho^3 uv(rho-1)(rho+1)
 * (u-1)^2(u+1)^3(u+v)(v-1)^2(v+1)^3(uv-1)^4.      (7)
```

Neither polynomial is zero in `C[u,v,rho]`.  The same minors before setting
`h=0` are therefore nonzero polynomials in

```text
C[u,v,rho,h0,h1,h2,h3].                              (8)
```

Consequently both mixed matrices have full column rank eight on a nonempty
dense open subset of the whole parameter/marking space.  Their kernels are
zero there, which excludes a binary neighbour before any diagonal or ternary
condition is considered.

## A complete rational component fibre

The Cayley point

```text
(u,v)=(1/3,1/2)
```

is `(s,t)=(2,3)`.  Over

```text
C(rho)[h0,h1,h2,h3],
```

exact module normal form gives, independently for `01` and `23`,

```text
Row(M_ij)=S^8,

reduced basis=(e1,e2,e3,e4,e5,e6,e7,e8).             (9)
```

Thus the complete weighted marking fibre at that component point is empty in
both directions.  This is a full polynomial identity in the slope and four
marking parameters, not a finite evaluation.

## Cross-specialty interpretation

Equations (1)--(2) identify the component surface with multiplication on the
algebraic torus.  Equations (6)--(9) then turn the extension question into the
unimodularity of a presentation matrix over the coordinate ring of an affine
marking chart.  This is the Fitting-module viewpoint of the
[Stacks Project, Section 15.8](https://stacks.math.columbia.edu/tag/07Z6),
now expressed in the component's natural toric coordinates.

The useful lesson is also a warning about specialization boundaries:

```text
presymplectic normal form
 -> Cayley torus multiplication
 -> pull back the original squarefree Frobenius form
 -> study the extension module over the marking ring.              (10)
```

The torus chart simplifies the planes, while apolar/Frobenius duality tells us
which multilinear form must be retained.  Conflating those two coordinate
roles gives a false invariance; keeping them separate produces the compact
factors (6)--(7).

## Exact remaining frontier

Let `Delta_01(u,v,rho,h)` and `Delta_23(u,v,rho,h)` denote the same two
selected minors before specializing `h=0`.  A possible weighted lift over the
generic component point is now confined to

```text
V(Delta_01) union V(Delta_23).                       (11)
```

The all-marking module identities at `(2,3)` show that this union is not a
structural source of neighbours, but they do not exclude components of (11)
that dominate the `(u,v)` parameter surface.  Closing those exact marking
divisors—or finding a symmetry-compatible module identity there—is the next
symbolic task.

## Verification

Run:

```text
tmp/codex_verify_env/Scripts/python.exe \
  verify_p5_h22_two_rank_two_spoke_mixed_star_dense_marking_obstruction.py

tmp/codex_verify_env/Scripts/python.exe \
  audit_p5_h22_two_rank_two_spoke_mixed_star_dense_marking_obstruction.py
```

The primary verifier reconstructs the Cayley rows, pulls them back to the
original squarefree form, proves (4), factors (6)--(7), and verifies both
all-marking module identities (9).

The audit imports nothing from the primary verifier.  It reconstructs the
top coefficient by squarefree subset dynamic programming, checks the
canonical rank-eight pivots, and proves complete all-marking module identities
at the two further rational component points `(s,t)=(3,5)` and `(5,7)`.
Those extra fibres corroborate the geometry; the dense-open theorem itself is
the symbolic nonvanishing of (6)--(7).
