# A fixed-vertex Segre join closes weighted `H22` on the tenth component

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
weighted marked-basis fibre over the generic point of the two-rank-two-spoke
mixed-star component is empty for `H22`.

It is enough to study the weighted `23` neighbour.  Instead of retaining the
four Borel marking parameters, project the possible binary tensor away from
its free all-active coordinate.  The other fifteen coordinates must lie in a
rank-one toric array with a fixed all-kernel vertex.  Six quadratic and four
cubic binomials cut out that array on the nonzero all-kernel chart.  After
substitution of the component's eight extension variables, their exact ideal
over `C(u,v,rho)` is the unit ideal.

Consequently all eleven currently certified pure-`P_4` component orbits are
now generically closed for both `H31` and weighted `H22`.

This is still not a proof of pure-`P_4` component exhaustiveness, does not
close every special parameter/projective boundary, and does not resolve the
global Krenn--Gu conjecture.

## The Cayley component and the weighted neighbour

Use Cayley component parameters `u,v` and weighted slope `rho`.  In
coefficients of

```text
(a,a_bar,b,b_bar),
```

take the intrinsic kernel rows

```text
alpha_0=(1,0,1,0),
alpha_1=(1-u,-1-u,1-u,-1+u),
alpha_2=(1-v,-1-v,1-v,1-v),
alpha_3=(0,0,0,1-uv),                               (1)
```

and active rows

```text
beta_0=(0,0,1,0),
beta_1=(0,-1-u,1-u,0),
beta_2=(0,-1-v,1-v,0),
beta_3=(1-uv,-1-uv,-1+uv,0).                       (2)
```

Pulling (1)--(2) back to the original squarefree coordinates leaves only

```text
T_1111=4(u-1)(v-1)(uv-1)                           (3)
```

in the pure `P_4` tensor.

For the weighted `23` neighbour, send a block row
`(A,Abar,B,Bbar)` with fifth entry `e` to

```text
(A+Abar, A-Abar, B+rho Bbar, e).                   (4)
```

Adjoin extensions

```text
z=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3)
```

to (1)--(2), and let `C_w(z)` be the resulting sixteen binary tensor
coordinates in the canonical `(alpha,beta)` bases.

## Eliminate markings by projecting a Segre join

Every compatible marked active row has the form

```text
beta_i'=beta_i+h_i alpha_i.                        (5)
```

Suppose the weighted neighbour were binary `Delta_2`, with nonzero
all-kernel coefficient `A` and all-active coefficient `B` in the marked
bases `(alpha_i,beta_i')`.  Since

```text
beta_i=beta_i'-h_i alpha_i,
```

its canonical coordinates satisfy, for every word `w!=1111`,

```text
C_w=A product_{i:w_i=1}(-h_i).                     (6)
```

Thus the fifteen coordinates other than `C_1111` form a rank-one Boolean
array.  Conversely, when `C_0000!=0`, this rank-one condition reconstructs
all four `h_i`; `C_1111` is free because it absorbs the second diagonal.

Normalize `C_0000=1`.  For a subset `S` of the four modes, write `C_S` for
the coordinate whose one-set is `S`, and put `c_i=C_{ {i} }`.  Equation (6)
is equivalent on this chart to the ten toric equations

```text
C_S C_empty^(|S|-1) = product_{i in S} c_i,

2 <= |S| <= 3.                                     (7)
```

There are six quadrics and four cubics.  They are simply the affine
fixed-vertex join of a point with the Segre variety; no marking variable
remains.

## A visible open-branch contradiction

Set

```text
K=x_3+rho(1-uv)y_0,
P=C_0000,
L=-2(u+1)(v+1),
M=-4(u+v).                                         (8)
```

Four extension coordinates factor as

```text
C_1000=M K,
C_1010=L K,
C_1100=L K,
C_1110=L K.                                       (9)
```

On `K!=0`, the toric equations for the one-sets `{0,1}`, `{0,2}`, and
`{0,1,2}` first give

```text
C_0100=(L/M)P,       C_0010=(L/M)P,                (10)
```

and then force `L=M`.  But

```text
M-L=2(u-1)(v-1),                                   (11)
```

which is a unit in the generic component field.  Hence the entire `K!=0`
branch is impossible by three binomials.

The divisor `K=0` is exactly where the visible cancellation (9) loses its
pivot.  Rather than reintroducing four markings there, retain the natural
full toric system (7).

## The boundary is also empty

Over

```text
K_0=C(u,v,rho),
```

substitute the sixteen linear forms `C_w(z)` into

```text
C_0000-1
```

and the ten equations (7).  Exact characteristic-zero reduction in

```text
K_0[x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3]              (12)
```

gives

```text
<C_0000-1, six quadrics, four cubics>=(1).          (13)
```

Thus no extension with nonzero all-kernel diagonal lies in the fixed-vertex
Segre join, including on `K=0`.  The weighted `23` neighbour cannot be binary
`Delta_2` in any marking.  A weighted `H22` lift requires both weighted
neighbours, so the generic component fibre is empty before any ternary-rank
test.

## The neighboring literature

The larger ambient object is the secant-line variety of
`Segre((P^1)^4)`.  Landsberg--Manivel study equations of Segre secants
([arXiv:math/0311388](https://arxiv.org/abs/math/0311388)), and Raicu proves
that secant-line ideals of Segre--Veronese varieties are generated by cubic
flattening minors ([arXiv:1011.5867](https://arxiv.org/abs/1011.5867)), a
circle motivated in part by algebraic statistics and phylogenetic
invariants.

The present incidence is smaller than the full secant: one Segre vertex is
fixed by the pure-`P_4` kernel rows.  Projecting away the opposite free
diagonal turns its join into the elementary toric model (7).  This translation
is what removes all four marking parameters and replaces a difficult
`14 x 8` polynomial row module by ten canonical binomials.

## Honest frontier

All eleven certified components are now generically closed for both marked
types.  The next symbolic front is no longer a generic fibre of a known
component.  It is pure-`P_4` component exhaustiveness and the special
parameter/projective boundaries needed to turn generic component theorems
into a complete `P_4` classification.  The global graph problem remains open.

## Verification

Run:

```text
uv run --with sympy python claims/p5/h22/two-rank-two-spoke-mixed-star/verify_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py
uv run --with sympy python claims/p5/h22/two-rank-two-spoke-mixed-star/audit_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(4), proves (3), builds all eleven
generators in (13), checks the factor pattern (8)--(11), and obtains the
reduced basis `{1}` over `C(u,v,rho)`.  The independent audit uses the
original `(s,t)` component rows rather than Cayley coordinates, reconstructs
permanents by subset dynamic programming, and obtains the same unit ideal
over `C(rho)` at `(s,t)=(2,3)` and `(3,5)`.  Those two fibres are
corroboration; the generic theorem is the primary function-field identity.
