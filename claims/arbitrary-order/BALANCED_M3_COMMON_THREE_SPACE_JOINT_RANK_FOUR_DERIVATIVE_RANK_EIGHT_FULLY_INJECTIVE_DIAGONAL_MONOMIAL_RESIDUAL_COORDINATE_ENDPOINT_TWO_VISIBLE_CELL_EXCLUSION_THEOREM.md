# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective diagonal-monomial coordinate-endpoint two-visible-cell exclusion

## Status

**Exact characteristic-zero exclusion of the complete two-visible cell at
the surviving diagonal monomial coordinate endpoints.**  Retain the
normalized physical full-sensor hypotheses and notation of S2CF:

```text
C=lambda e_2 tensor e_2,             w=e_0,          lambda!=0,

D(a,b,c)=(a tensor y-x tensor b) tensor e_0+C tensor c,
ker D=span((x,y,0)) subset K,         dim K=4,

rank rho=rank pi=rank theta=3,
x not proportional e_2,              y not proportional e_2.       (1)
```

Let `Q=span(q_0,q_1,q_2)`.  For `alpha in x^perp` and
`beta in y^perp`, S2CF gives

```text
M_(r_alpha,p_beta)(q_k)
 =alpha_k beta_k T_k+lambda alpha_2 beta_2 S_k,      (2)

M_(u,v)(q)=per(u,v,q),
Alt(Q)!=0.                                           (3)
```

Assume both `T_0` and `T_1` are visible outside the corrected cell in the
sense of S2CF's exact visibility census.  Then no physical point exists.

The two-visible support atlas has fourteen ordered masks.  Four central
masks are excluded by a new two-transverse mixed-map lemma.  Each of the
remaining ten masks has one structural zero pair and two correction-free
rank-one corners on the fully transverse target lines `T_0,T_1`.  S2CG's
zero-pair classification and a new zero-corner rectangle lemma exclude all
ten at once.

Together with S2CH and S2CJ, this closes both diagonal monomial coordinate
endpoints.  It does **not** reduce an arbitrary nonmonomial residual to a
monomial endpoint.  Every nonmonomial residual outside S2CG, every wider
lower-rank cell, pair gate, component, pole stratum, higher order, and the
all-rank-drop branch remains open.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. The exact fourteen-mask atlas

For a nonzero coordinate vector, write its projective support as a subset
of `{0,1,2}`.  Neither `x` nor `y` is proportional to `e_2`, so its support
is one of

```text
{0}, {1}, {0,1}, {0,2}, {1,2}, {0,1,2}.             (4)
```

S2CF's visibility conditions are

```text
T_0 visible iff x not proportional e_0, y not proportional e_0,
                   and (x_1,y_1)!=(0,0);

T_1 visible iff x not proportional e_1, y not proportional e_1,
                   and (x_0,y_0)!=(0,0).             (5)
```

Their simultaneous truth forces each support into

```text
{0,1}, {0,2}, {1,2}, {0,1,2},                       (6)
```

and excludes only the ordered pairs `({0,2},{0,2})` and
`({1,2},{1,2})`.  Thus there are exactly

```text
4*4-2=14                                             (7)
```

two-visible masks.  They split disjointly into

```text
central masks:
  {0,1} or {0,1,2}  by  {0,1} or {0,1,2};          4

boundary masks:
  every other pair in (6), except the two pairs above.             10
```

This is an exhaustive Boolean support cover, not a count of solver inputs.
All nonzero coordinate values remain arbitrary.

## 2. A mixed map cannot be a transverse secant

### Lemma 1 (two-transverse mixed-map obstruction)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field, let
`Q subset W` be a subspace, and let `u,v in Q`.  Let `T,S` be nonzero
decomposable tensors that are fully transverse in all three source factors.
Then

```text
M_(u,v)(Q) subset span(T,S)                          (8)
```

cannot contain both `T` and `S`.

#### Proof

Split `u` by its number of nonzero source components.

If `u` is pure, every nonzero mixed value containing it has its fixed
source factor.  Two such values cannot be fully transverse.

Suppose `u=x+y` has two nonzero source components.  Put

```text
L(q)=M_(u,v)(q).
```

Because `u,v in Q`, both `L(u)` and `L(v)` lie in the secant line in (8).
Direct expansion gives

```text
L(u)=2 x tensor y tensor v_Z.                       (9)
```

If `v_Z=0`, then

```text
L(q)=(x tensor v_Y+v_X tensor y) tensor q_Z.        (10)
```

Every nonzero decomposable value in (10) has the same first two factor
lines; if the displayed `X tensor Y` matrix is not decomposable, there is
no nonzero decomposable value at all.  Hence (10) cannot contain `T,S`.

If `v_Z!=0`, (9) is a nonzero decomposable point on the transverse secant.
The only decomposable points on that line are its two endpoints, so relabel
and scale it as `T=x tensor y tensor v_Z`.  Moreover

```text
L(v)=2(x tensor v_Y+v_X tensor y) tensor v_Z.       (11)
```

also lies on the secant.  Its fixed third factor forces it onto `span(T)`.
Projection modulo `span(x)` and `span(y)` in (11) gives
`v_X proportional x` and `v_Y proportional y`.  Every `L(q)` then lies in
the Segre tangent space at `T`; every decomposable point there shares at
least two factor lines with `T`.  The fully transverse endpoint `S` is not
in the image.

Finally let `u=x+y+z` have all three components.  The value

```text
L(u)=M_(u,u)(v)                                     (12)
```

lies in the Segre tangent space at `x tensor y tensor z`.  A tangent space
meets the line through two fully transverse Segre points only at zero or at
an endpoint.  One exact way to see this is to apply linear retractions of
the three source factors that fix the two endpoint-factor lines.  If all
three projected base components of `x,y,z` are nonzero, normalize them to
`e_0`.  The projected tangent then has support only at
`000,100,010,001`, so Cayley's `2 x 2 x 2` hyperdeterminant vanishes.  If
any projected base component is zero, the projected tangent is rank at most
one, or zero, and its hyperdeterminant again vanishes.  On `aT+bS`, by
contrast, the hyperdeterminant is a nonzero scalar multiple of `(ab)^2`.
Thus a point with `ab!=0` cannot occur.

If (12) is zero, projection modulo the factor lines of `u` gives

```text
v=(a x,b y,c z),                  a+b+c=0.           (13)
```

Consequently `L(Q)` lies in the same Segre tangent and cannot contain the
two transverse endpoints.  If (12) is one endpoint, the standard
decomposable-tangent classification makes it share two factor lines with
`x tensor y tensor z`.  After permuting sources, write that endpoint as
`T=xi tensor y tensor z`.  The membership

```text
v_X tensor y tensor z+x tensor v_Y tensor z+x tensor y tensor v_Z
  in span(xi tensor y tensor z)
```

and quotienting by `span(y)` and `span(z)` give
`v_Y in span(y)` and `v_Z in span(z)`.  Hence

```text
L(Q) subset X tensor span(y) tensor Z
             +X tensor Y tensor span(z).
```

Projection to `(Y/span(y)) tensor (Z/span(z))` shows that every
decomposable value shares `y` or `z`.  The other fully transverse endpoint
again cannot occur.  This exhausts the support of `u` and proves the
lemma.  QED.

### Application to the four central masks

Take the denominator-free covectors

```text
alpha=(x_1,-x_0,0) in x^perp,
beta =(y_1,-y_0,0) in y^perp.                       (14)
```

For all four central masks, `x_0x_1y_0y_1!=0`.  Put
`u=r_alpha`, `v=p_beta`.  Row injectivity makes `u,v` nonzero and (2)
gives

```text
M_(u,v)(q_0)= x_1y_1 T_0,
M_(u,v)(q_1)= x_0y_0 T_1,
M_(u,v)(q_2)=0.                                     (15)
```

The correction vanishes because `alpha_2=beta_2=0`.  Thus the image in
(15) is exactly the transverse secant `span(T_0,T_1)` and contains both
endpoints, contrary to Lemma 1.  All four central masks are empty.

## 3. A structural zero corner forbids two transverse corners

### Lemma 2 (zero-corner rectangle obstruction)

Let `Q subset W` be three-dimensional with `Alt(Q)!=0`.  Let
`A,c,B,d in Q` satisfy

```text
dim span(A,c)=dim span(B,d)=2,
M_(c,d)(Q)=0.                                       (16)
```

If two of the three maps

```text
M_(A,d)|Q,              M_(c,B)|Q,              M_(A,B)|Q             (17)
```

are nonzero rank-one maps with decomposable images, their image tensors
cannot be fully transverse.

#### Proof: an independent zero pair

Suppose `c,d` are independent.  S2CG's zero-pair theorem gives, after a
source permutation and nonzero rescaling,

```text
c=x+y,                    d=x-y.                    (18)
```

Thus `x,y in Q`.  Since `dim Q=3`, the projection of `Q` to the omitted
source, say `Z`, has dimension at most one.  It is nonzero because
`Alt(Q)!=0`; write its line as `span(z)`.  Every permanent of three rows in
`Q` therefore has `Z` factor `z`.  In particular, every nonzero
decomposable value of all three maps in (17) has that same factor line.
Two of their image tensors cannot be fully transverse.

#### Proof: a dependent zero pair

Suppose `c,d` are dependent.  The square-zero branch of S2CG's theorem and
`Alt(Q)!=0` make their common row pure.  After rescaling, write

```text
c=d=x in X.                                         (19)
```

The first two maps in (17) have fixed `X` factor `x`, so their image
tensors are not fully transverse.  It remains, up to exchanging the first
two roots, to compare

```text
F=M_(A,x)|Q,                  H=M_(A,B)|Q.           (20)
```

Assume both are nonzero rank one and their decomposable image lines are
fully transverse.  The common trilinear value

```text
F(B)=M_(A,x)(B)=M_(A,B)(x)=H(x)                     (21)
```

belongs to both distinct image lines, and hence is zero.  Write

```text
A_Y=a,                         A_Z=b.                (22)
```

If `a,b` are nonzero, evaluating `F` at `A` shows that its image line is

```text
span(x tensor a tensor b).                          (23)
```

Equation (21) is

```text
a tensor B_Z+B_Y tensor b=0,                        (24)
```

so `B_Y=t a` and `B_Z=-t b` for some scalar `t`.  Direct expansion now
places the whole second image in

```text
H(Q) subset X tensor span(a) tensor Z
              +X tensor Y tensor span(b).           (25)
```

Every decomposable tensor in (25) has `Y` factor `a` or `Z` factor `b`.
It therefore shares a factor with (23), a contradiction.

If `a=0`, nonvanishing of `F` gives `b!=0`, and rank one says that the
projection of `Q` to `Y` is one line, say `span(y)`.  Equation (21) gives
`B_Y=0`.  Expansion then puts `H(Q)` in
`X tensor span(y) tensor Z`, so its decomposable image shares `y` with the
image of `F`.  The case `b=0` is analogous after exchanging the omitted
sources `Y,Z` and gives a common `Z` factor.  This proves the dependent
case and the lemma.  QED.

## 4. The ten boundary masks give Lemma 2

For a vector `v` with the named coordinates nonzero, put

```text
v_01=(v_1,-v_0,0),
v_02=(v_2,0,-v_0),
v_12=(0,v_2,-v_1).                                  (26)
```

Each displayed covector lies in `v^perp`.  The following table lists bases
`(c,A)` of `x^perp` and `(d,B)` of `y^perp`.  The last column lists the two
maps from (17) that (2) makes correction-free nonzero rank-one maps on the
fully transverse target lines `T_0,T_1`.

| `supp(x)` | `supp(y)` | `(c,A)` | `(d,B)` | correction-free target corners |
| --- | --- | --- | --- | --- |
| `01` | `02` | `(e_2,x_01)` | `(e_1,y_02)` | `Ad=T_1`, `AB=T_0` |
| `01` | `12` | `(e_2,x_01)` | `(e_0,y_12)` | `Ad=T_0`, `AB=T_1` |
| `02` | `01` | `(e_1,x_02)` | `(e_2,y_01)` | `cB=T_1`, `AB=T_0` |
| `12` | `01` | `(e_0,x_12)` | `(e_2,y_01)` | `cB=T_0`, `AB=T_1` |
| `02` | `12` | `(e_1,x_02)` | `(e_0,y_12)` | `Ad=T_0`, `cB=T_1` |
| `12` | `02` | `(e_0,x_12)` | `(e_1,y_02)` | `Ad=T_1`, `cB=T_0` |
| `02` | `012` | `(e_1,x_02)` | `(y_02,y_01)` | `cB=T_1`, `AB=T_0` |
| `12` | `012` | `(e_0,x_12)` | `(y_12,y_01)` | `cB=T_0`, `AB=T_1` |
| `012` | `02` | `(x_02,x_01)` | `(e_1,y_02)` | `Ad=T_1`, `AB=T_0` |
| `012` | `12` | `(x_12,x_01)` | `(e_0,y_12)` | `Ad=T_0`, `AB=T_1` |

Here, for example, `Ad=T_1` means that `M_(r_A,p_d)|Q` has image exactly
the nonzero line `span(T_1)`; the harmless displayed coefficient is a
product of coordinates nonzero on the named support mask.

In every row, the coordinate products of `c,d` vanish at all three colours
and `c_2d_2=0`.  Equation (2) therefore gives

```text
M_(r_c,p_d)(Q)=0.                                   (27)
```

The two covector pairs in the row are bases, so row injectivity gives the
two genuine planes required in Lemma 2.  The last column follows by direct
coordinate multiplication in (2).  Each named map has exactly one nonzero
target coefficient and has zero correction because at least one of its two
covectors has zero second coordinate.  Its image is therefore a nonzero
rank-one map on `T_0` or `T_1` exactly as displayed.

Lemma 2 says those two fully transverse target lines cannot coexist.  This
excludes every boundary row in the table.  The four central rows were
excluded in Section 2, so all fourteen masks in (7) are empty.

## 5. Proof-topology consequence

The visibility split at either diagonal monomial coordinate endpoint is
now

```text
zero-visible wall:                                  IMPOSSIBLE (S2CH);
one-visible wall:                                   IMPOSSIBLE (S2CJ);
two-visible cell:                                   IMPOSSIBLE;

diagonal monomial coordinate endpoints:             IMPOSSIBLE;
off-diagonal monomial coordinate endpoints:          IMPOSSIBLE (S2CE);

other nonmonomial residuals / wider cells:           OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.      (28)
```

No finite-field scan, numerical fit, solver certificate, support
specialization, saturation, limit, or unproved degeneration enters the
proof.  The support atlas is exact, and every division in the analytic
lemmas is only by a displayed nonzero vector or by the characteristic-zero
scalar `2`.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_two_visible_cell_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_two_visible_cell_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_two_visible_cell_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_two_visible_cell_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_two_visible_cell_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_two_visible_cell_exclusion.py
```

The primary SymPy replay exhausts the fourteen support masks and checks all
perpendicular bases, zero pairs, correction terms, and selected target
corners.  It also checks the exact tensor-coordinate interfaces used in the
mixed-map and zero-corner lemmas.

The independent audit imports neither the primary verifier nor SymPy.  It
uses standard-library `Fraction` arithmetic and reverses colour-mask,
source-coordinate-triple, permanent-summand, and chart traversal.  It has
separate permanent and rank routines and independent fixtures for the
support atlas and both analytic interfaces.
Both scripts leave the source-support classifications and the S2CG
zero-pair theorem to the written proof.

## Dependencies

- [Diagonal coordinate-endpoint full-target reduction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_FULL_TARGET_REDUCTION_THEOREM.md)
- [Canonical-binomial residual exclusion and general zero-pair classification](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_CANONICAL_BINOMIAL_RESIDUAL_EXCLUSION_THEOREM.md)
- [Complete diagonal one-visible-wall exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_COMPLETE_ONE_VISIBLE_WALL_EXCLUSION_THEOREM.md)
- [Tangent-line separation and mixed-factor sharing](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)

## Scope boundary

This theorem excludes exactly the two-visible cell at the two surviving
diagonal monomial coordinate endpoints in the fully-injective `(3,3,3)`,
joint-rank-four, derivative-rank-eight common-three-space full-sensor
stratum.  With S2CH and S2CJ it closes those endpoints, and with S2CE it
closes the monomial-residual branch of that stratum.

It neither classifies nor excludes an arbitrary nonmonomial residual.  It
does not close joint rank at most three, derivative rank seven, pair
coupling, another physical component or pole stratum, higher order, or the
all-balanced rank-drop branch.  No graph or counterexample is constructed.
Global Krenn--Gu remains **UNRESOLVED**.
