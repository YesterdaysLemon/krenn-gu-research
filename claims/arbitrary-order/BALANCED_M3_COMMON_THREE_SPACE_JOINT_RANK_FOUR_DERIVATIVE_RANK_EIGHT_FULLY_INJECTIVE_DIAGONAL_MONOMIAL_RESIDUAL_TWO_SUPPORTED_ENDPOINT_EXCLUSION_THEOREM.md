# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective diagonal-monomial residual two-supported endpoint exclusion

## Status

**Exact characteristic-zero exclusion inside the diagonal endpoint left by
S2CC.**  Retain all hypotheses and notation of the fully-injective
monomial-residual endpoint localization.  In particular,

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
ker D=span((x,y,0)),
rank rho=rank pi=rank theta=3,
```

and suppose that the residual block is diagonal monomial:

```text
C=lambda e_d tensor e_d,                 lambda!=0.       (1)
```

S2CC proves `w_d=0`.  This theorem proves that `w` cannot have both
complementary coordinates nonzero.  Therefore

```text
C=lambda e_d tensor e_d
  implies w is proportional to e_a or e_b,
  where {a,b,d}={0,1,2}.                                (2)
```

The proof uses the complete target slice and both physical common rows.  The
two-supported case gives a same-third-row binary table in the four-dimensional
joint row space.  Shifts by the two common rows reduce all possible row-space
incidences to 29 exact polynomial charts.  Pinned rational Nullstellensatz
identities exclude every chart, and a separately implemented no-import audit
reconstructs every permanent and certificate product.

This is a localization, not closure of the `(3,3,3)` profile.  The two
coordinate endpoints in (2), every off-diagonal monomial endpoint, every
nonmonomial residual, wider lower-rank cells, other components and pole
strata, higher orders, and all-rank drop remain open.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. The complete diagonal endpoint face

Relabel the diagonal colour as `d=2` and its complementary colours as `0,1`.
Assume for contradiction that

```text
w=(w_0,w_1,0),                         w_0 w_1!=0.   (3)
```

The two covectors

```text
gamma_0=w_1 e_0^*-w_0 e_1^*,          gamma_1=e_2^* (4)
```

form a basis of `w^perp`.  Use the physical row notation

```text
r_i=rho(e_i^*),       p_i=pi(e_i^*),
q_k=theta(gamma_k),   T_i=X_i tensor Y_i tensor Z_i. (5)
```

S2CC's complete contracted target identity is

```text
per(r_i,p_j,q_gamma)-delta_(i=j) gamma_i T_i
  =C_(i,j) S_gamma.                                  (6)
```

Since every complementary row and column of (1) is zero, (6) gives

```text
per(r_0,p_0,q_0)= w_1 T_0,
per(r_1,p_1,q_0)=-w_0 T_1,                           (7)

per(r_i,p_j,q_k)=0 at the other six binary cells,    (8)

per(R,p_2,Q)=0,
per(r_2,P,Q)=0,                                      (9)
```

where

```text
R=span(r_0,r_1),       P=span(p_0,p_1),
Q=span(q_0,q_1).                                      (10)
```

All three planes lie in the four-dimensional joint row space `E`.  Full row
injectivity makes them genuine two-planes, and `u=r_2`, `v=p_2` in (9) are
nonzero.  Independent nonzero rescaling of the selected row and source-factor
representatives normalizes the two coefficients in (7) to one.  Hence the
abstract table used below is

```text
per(r_0,p_0,q_0)=T_0,
per(r_1,p_1,q_0)=T_1,
all other binary cells=0,                            (11)

per(R,v,Q)=0,                per(u,P,Q)=0.           (12)
```

The tensors `T_0,T_1` are decomposable and fully transverse.

## 2. Plane separation and placement of the common rows

The S2BG arbitrary-middle-intersection same-third-row obstruction implies

```text
R intersect Q=0,                 P intersect Q=0.    (13)
```

Indeed, if `R intersect Q` were nonzero, the two planes would lie in a
three-space `S`; dimension forces `P intersect S` nonzero, exactly the S2BG
hypothesis.  Exchanging the first two roots gives the second equality.

The table also shows `v notin P`: a vector `a p_0+b p_1` satisfying the
first equation in (12) has `aT_0=bT_1=0`, hence is zero.  Thus

```text
B=P+span(v)                                      (dim B=3).
```

Dimension gives a nonzero vector in `Q intersect B`, say

```text
ell=a_0p_0+a_1p_1+c v.                              (14)
```

Here `c!=0` by (13).  If `(a_0,a_1)!=(0,0)`, choose `lambda_0,lambda_1`
with `a_0lambda_0+a_1lambda_1=c`.  The shifted plane

```text
P_lambda=span(p_0+lambda_0v,p_1+lambda_1v)          (15)
```

carries the same table by (12), but contains `ell` and meets `Q`, contrary
to (13) applied to the shifted table.  Therefore `a_0=a_1=0`, and

```text
v in Q.                                             (16)
```

Root exchange proves identically that

```text
u in Q.                                             (17)
```

No source-factor assertion is inferred from (16)--(17); they are statements
about physical row-space incidence only.

## 3. Coordinate intersections of the first two row planes

We need one second exact incidence consequence of (11).

### Lemma 1 (coordinate first--middle intersection)

For any frame carrying (11), every nonzero line in `R intersect P` is one
of the four ordered coordinate incidences

```text
span(r_i)=span(p_j),                    i,j in {0,1}. (18)
```

#### Proof

Write a nonzero intersection representative as

```text
ell=a_0r_0+a_1r_1=b_0p_0+b_1p_1.                    (19)
```

By trilinearity and (11), its square on the active third row is

```text
per(ell,ell,q_0)=a_0b_0T_0+a_1b_1T_1.              (20)
```

Every repeated-row permanent `per(ell,ell,q)` lies in the affine tangent
space to the binary Segre variety: in source-factor notation it is, up to a
nonzero scalar,

```text
x(q) tensor y(ell) tensor z(ell)
+x(ell) tensor y(q) tensor z(ell)
+x(ell) tensor y(ell) tensor z(q).                  (21)
```

Its Cayley hyperdeterminant is identically zero, including degenerate factor
values.  After choosing the transverse factor lines of `T_0,T_1` as binary
bases, the hyperdeterminant of `alpha T_0+beta T_1` is
`alpha^2 beta^2`.  Hence the two products in (20) cannot both be nonzero.

Suppose exactly one is nonzero, say `a_0b_0!=0`.  If `a_1!=0`, then
`b_1=0`, so `ell` is proportional to `p_0`; the square map on `Q` has image
`span(T_0)`, whereas the mixed map `per(ell,p_1,Q)` has nonzero image
`span(T_1)`.  The S2AL mixed-factor-sharing lemma says those two rank-one
decomposable images must share a source factor, contrary to full
transversality.  Thus `a_1=0`.  If `b_1!=0`, the root-exchanged argument,
using `per(r_1,ell,Q)`, gives the same contradiction.  Thus `b_1=0`.
The case `a_1b_1!=0` is symmetric.

Finally, if both diagonal products vanish, nonzero pairs `(a_0,a_1)` and
`(b_0,b_1)` must have opposite singleton supports.  Thus (19) is a cross
coordinate incidence.  These alternatives are exactly (18).  QED.

The primary verifier checks the tangent identity symbolically.  The audit
reconstructs the same identity with a reversed-variable sparse `Fraction`
implementation.

## 4. Common-row shifts force a coordinate graph column

By (13),

```text
E=R direct-sum Q,
P=span(A_0+l_0,A_1+l_1),                            (22)
```

where `A_0,A_1` form a basis of `R` and `l_0,l_1 in Q`.

Consider the three-space `R+span(v)`.  It meets `P` nontrivially.  If a
nonzero intersection vector has `P`-coordinates `(b_0,b_1)`, its `Q`
component says

```text
b_0l_0+b_1l_1 in span(v).                           (23)
```

Shift the two `P` rows independently along `v` so that this combination has
zero `Q` component.  Equation (12) preserves the whole table.  Lemma 1 then
says that `(b_0,b_1)` is a coordinate pair and that the corresponding
`A_j` is a coordinate row of `R`.  Consequently, for some `j`,

```text
A_j is proportional to r_i,          l_j in span(v). (24)
```

Apply the same argument to `P intersect (R+span(u))`, now shifting the `R`
rows along the common first row `u`.  It gives, possibly at the other middle
index,

```text
A_j is proportional to r_i,          l_j in span(u). (25)
```

Membership in (24)--(25) includes `l_j=0`.  This matters: a zero graph
component imposes no restriction on the common-row line.

After the simultaneous binary target swap if needed, one may take `A_0`
coordinate.  Independent diagonal rescaling leaves exactly four quotient
normal forms:

```text
D0: p_0=r_0+l_0,       p_1=r_1+l_1;
D1: p_0=r_0+l_0,       p_1=r_0+r_1+l_1;
X0: p_0=r_1+l_0,       p_1=r_0+l_1;
X1: p_0=r_1+l_0,       p_1=r_0+r_1+l_1.             (26)
```

Here `D/X` records same/cross incidence and `0/1` records zero/nonzero
shear.  The four quotient matrices have nonzero determinant, so no chart
has discarded the injectivity `P intersect Q=0`.

## 5. The complete 29-chart cover

Choose the four-space basis

```text
r_0=e_0,        r_1=e_1,        q_0=e_2,        q_1=e_3. (27)
```

The row changes preserving the ordered same-third table act on `Q` by

```text
q_0 -> a q_0+b q_1,          q_1 -> c q_1,       ac!=0. (28)
```

For `D0` and `X0`, both quotient columns are coordinate.  Conditions
(24)--(25), the target swap, row rescaling, and (28) give the seven complete
orbits

| orbit | `(l_0,l_1)` | extra common-row data when needed |
|---|---|---|
| `zero_zero` | `(0,0)` | none |
| `zero_q1` | `(0,q_1)` | none |
| `zero_q0` | `(0,q_0)` | none |
| `prop_q1` | `(q_1,tau q_1)` | `u=v=q_1` for `tau!=0` |
| `prop_q0` | `(q_0,tau q_0)` | none |
| `ind_q1_q0` | `(q_1,q_0)` | each of `u,v` is one of these two lines |
| `ind_affine` | `(q_0,q_0+q_1)` | each of `u,v` is one of these two lines |

The `tau=0` point of `prop_q1` is already `zero_q1` after the target swap.
The certificate identity is polynomial in `tau` and nevertheless holds at
zero too.  Each independent orbit has four ordered `u/v` assignments.

Some charts are already impossible from the 64 table equations alone, so
their redundant physical equations are not added.  The exact census is

```text
D0: 5 table-only + 1 proportional physical + 4 affine assignments = 10;
X0: 4 table-only + 1 proportional physical
                  + 4 q1/q0 assignments + 4 affine assignments = 13. (29)
```

For `D1` and `X1`, only `p_0` has coordinate quotient.  Therefore
(24)--(25) force either `l_0=0`, or the two common rows lie on the same
nonzero line `span(l_0)`.  Under (28),

```text
l_0=0,       l_0=q_1 with u=v=q_1,       or l_0=q_0, (30)
```

while

```text
l_1=g q_0+h q_1                                      (31)
```

is arbitrary.  This gives three charts for each shear type, hence six more.
Equations (29)--(31) total

```text
10+13+3+3=29                                         (32)
```

charts.  No finite sampling of `tau,g,h` occurs.

## 6. Exact Nullstellensatz exclusion

Choose source-coordinate bases whose first two factor lines are those of
`T_0,T_1`.  Let their six selected coordinate forms on `E` have 24
independent coefficients.  For each chart, expand the polarized permanent
at every selected source triple and every binary row triple.  The coefficient
is one exactly at

```text
(source;row)=(000;000),              (111;110),      (33)
```

and zero at the other 62 positions.  Thus each chart has 64 necessary table
equations.  The 16 charts requiring physical data append the 32 coefficients
of `per(R,v,Q)=0` and the 32 coefficients of `per(u,P,Q)=0`, for 128
generators.

For every chart, the durable certificate supplies an exact identity

```text
1=sum_nu h_nu f_nu.                                  (34)
```

The 29 identities contain 2,972 sparse multiplier terms.  Their SHA-256 is

```text
e9414389e653a76770d8f105a086fcae6887d2dbe012f41e5d74f78686c72f52. (35)
```

All multipliers lie in the rational polynomial ring in the 24 form
coefficients and `tau,g,h`.  The identities contain no denominators,
saturation variables, localization, or solver-produced case assumptions.
They therefore exclude every chart over every characteristic-zero field.
This contradicts (3).

## 7. Proof-topology consequence

Combining this exclusion with S2CC gives

```text
fully injective (3,3,3), C=lambda e_d tensor e_e:
  d=e:
    support(w) has both complementary colours:      IMPOSSIBLE;
    w proportional to one complementary coordinate: OPEN;
  d!=e:
    w proportional to the third coordinate:         OPEN;
  C nonmonomial:                                     OPEN.

joint-rank-three / derivative-rank-seven cells:      OPEN;
other components and pole strata:                    OPEN;
higher balanced orders / all-rank-drop:               OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.     (36)
```

The coordinate alternatives are necessary endpoints.  This theorem does not
construct them and does not assert that they are physical incidences.

## 8. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_two_supported_endpoint_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_two_supported_endpoint_exclusion.py
python -m py_compile claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_two_supported_endpoint_certificates.py claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_two_supported_endpoint_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_two_supported_endpoint_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_two_supported_endpoint_certificates.py claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_two_supported_endpoint_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_two_supported_endpoint_exclusion.py
```

The generator needs Singular 4.x and is not needed for replay.  It computes a
reduced standard basis with `slimgb`, obtains the lift to the original ordered
generators, checks the unit identity inside Singular, and emits the sparse
multipliers.  The primary verifier reconstructs all generators with SymPy.
The independent audit reverses all 27 variables and uses only standard-library
`Fraction` sparse arithmetic.

## Dependencies

- [Fully-injective monomial-residual endpoint localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_MONOMIAL_RESIDUAL_ENDPOINT_LOCALIZATION_THEOREM.md)
- [Arbitrary-middle-intersection same-third-row obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_S_EQUAL_T_ENDPOINT_EXCLUSION_THEOREM.md#1-an-arbitrary-middle-plane-intersection-still-cannot-carry-a-same-third-row-table)
- [Tangent-line and mixed-factor-sharing lemmas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#2-two-exact-two-plane-lemmas)

## Scope boundary

```text
diagonal monomial with two-supported complementary w: IMPOSSIBLE;
diagonal monomial coordinate endpoints:               OPEN;
off-diagonal monomial endpoints:                       OPEN;
nonmonomial fully injective (3,3,3):                   OPEN;
other lower-rank cells / components / poles:           OPEN;
higher balanced orders / all-balanced rank-drop:       OPEN;
global Krenn--Gu conjecture:                            UNRESOLVED.   (37)
```
