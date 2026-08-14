# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective diagonal-monomial coordinate-endpoint full-target reduction

## Status

**Exact characteristic-zero reduction of each remaining diagonal monomial
coordinate endpoint to two complete recovered source slices and one
gauge-free tangent-coset rank-one condition, with an exact corrected cube in
the third-row three-space as a consequence.**  Retain the
normalized, target-consistent physical `m=3` common-three-space full-sensor
hypotheses with singleton span dimension three, joint rank four, shared
derivative rank eight, and all three root rows injective.  At either diagonal
coordinate endpoint left by S2CC and S2CD, permute the complementary colours
and rescale the shared-factor presentation so that

```text
C=lambda e_2 tensor e_2,       w=e_0,       lambda!=0.       (1)
```

Write

```text
D(a,b,c)=(a tensor y-x tensor b) tensor e_0+C tensor c,
ker D=span((x,y,0)),                                    (2)

C notin A_1 tensor y+x tensor A_2,
x not proportional e_2,       y not proportional e_2. (3)
```

For graph lifts `k_c=(a_c,b_c,e_c)`, put

```text
P_ijk=per(r_i,p_j,q_k),
H_c=a_c tensor y-x tensor b_c.
```

Then the complete empty-target identity is equivalent to

```text
P^(0)-E_00 T_0=(C+H_0) S_0+H_1 S_1+H_2 S_2,
P^(1)-E_11 T_1=C S_1,
P^(2)-E_22 T_2=C S_2.                                (4)
```

The `(2,2)` entries of the last two slices determine `S_1,S_2`, but their
other sixteen root entries remain load-bearing.  After recovering the source
tensors, retain the complete face residuals

```text
F^(1)=P^(1)-E_11 T_1-C(lambda^(-1)P_221)=0,
F^(2)=P^(2)-E_22 T_2-C(lambda^(-1)(P_222-T_2))=0.    (4a)
```

After also subtracting their tangent contributions from the first slice, the
only remaining unsliced obligation is

```text
R=kappa tensor S_0,
kappa=C+H_0 in C+(A_1 tensor y+x tensor A_2),
kappa!=0.                                             (5)
```

Equivalently, all root/source flattening minors

```text
kappa_mn R_ij-kappa_ij R_mn=0                        (6)
```

vanish.  No divisor is hidden in (6): condition (3) makes `kappa` nonzero at
every admissible point, and (6) is imposed for every pair of root entries.

There is also a denominator-free consequence inside
`Q=span(q_0,q_1,q_2)`.  For `alpha in x^perp` and `beta in y^perp`,

```text
per(r_alpha,p_beta,q_k)
 =alpha_k beta_k T_k+lambda alpha_2 beta_2 S_k.      (7)
```

Both `r_alpha` and `p_beta` lie in `Q`.  Thus the endpoint contains an exact
`2 x 2 x 3` cube in one three-space, with only one corrected square.  The
cube does not replace the complete face residuals (4a): contraction forgets
their tangent-row and tangent-column slots.  The cube is sharp: Section 6
gives an exact split-form realization on a one-visible-target wall.
Therefore (7) alone cannot exclude the endpoint; every complete successor
must retain (4a) and couple the cube to (5).

This theorem is a reduction, not an endpoint exclusion.  Diagonal coordinate
endpoints and nonmonomial residuals remain open, as do the other lower-rank
cells, pair coupling, other components and pole strata, higher orders, and
all-rank drop.  It constructs neither a graph nor a counterexample.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The complete graph identity

Because the third row is injective and `dim K=4`, S2CC writes

```text
K=span((x,y,0))+span{k_0,k_1,k_2},
k_c=(a_c,b_c,e_c).                                  (8)
```

The derivative images

```text
U_c=D(k_c)=H_c tensor e_0+C tensor e_c              (9)
```

form a basis of `U=D(K)`.  Hence there are unique source tensors `S_c` with

```text
G_N-J=sum_c U_c S_c.                                (10)
```

At root coefficient `(i,j,k)`, (10) reads

```text
P_ijk-delta_(i=j=k) T_i
 =delta_(k=0) sum_c ((a_c)_i y_j-x_i (b_c)_j) S_c
   +lambda delta_(i=2) delta_(j=2) S_k.             (11)
```

If

```text
L_i=sum_c (a_c)_i S_c,       M_j=sum_c (b_c)_j S_c,
```

the tangent term is exactly

```text
delta_(k=0)(y_j L_i-x_i M_j).                       (12)
```

Thus its sign is `+y_j L_i-x_i M_j`, with no polarization factor.  Grouping
(11) by `k` gives (4).

The graph-lift gauge

```text
a_c -> a_c+t_c x,       b_c -> b_c+t_c y            (13)
```

leaves

```text
(a_c+t_c x) tensor y-x tensor (b_c+t_c y)=H_c       (14)
```

unchanged.  Hence (4)--(6) do not depend on a choice of lift.

## 2. Elimination of the source tensors

Since `C=lambda E_22`, the `(2,2)` entries of the last two equations in (4)
give

```text
S_1=lambda^(-1) P_221,
S_2=lambda^(-1)(P_222-T_2).                         (15)
```

Because `C=lambda E_22`, the two `(2,2)` equations become tautologies after
(15).  The exact remaining content of (4a) is the sixteen source-tensor
equations

```text
P_ijk-delta_(i=j=k)T_k=0,
k in {1,2},       (i,j)!=(2,2).                     (15a)
```

Define

```text
kappa=C+H_0,
R=P^(0)-E_00 T_0-H_1 S_1-H_2 S_2.                  (16)
```

The first equation in (4) is (5).  Moreover `kappa` cannot vanish, because
that would put `C=-H_0` in the tangent plane forbidden by (3).

Equation (5) implies every identity (6).  Conversely, assume (6) and choose
any nonzero entry `kappa_mn`.  The equations involving it give

```text
R_ij=kappa_ij (R_mn/kappa_mn)
```

for every `(i,j)`, proving (5) with `S_0=R_mn/kappa_mn`.  This is a pointwise
proof over the base field, not an inserted localization.  Computational
successors may use nine pivot charts; `kappa!=0` proves their union exhaustive.

Equations (15)--(16) therefore eliminate all three auxiliary source tensors:
`S_1,S_2` are read from the exceptional edge, their complete recovered face
residuals (4a) are retained, and existence of `S_0` is equivalent to the
ordinary polynomial minors (6).

## 3. The corrected cube in the third-row plane

Let `h,q_0,q_1,q_2` be the row vectors dual to the basis in (8).  Then

```text
r_i=x_i h+sum_c (a_c)_i q_c,
p_j=y_j h+sum_c (b_c)_j q_c.                        (17)
```

For `alpha in x^perp` and `beta in y^perp`, (17) gives

```text
r_alpha=sum_i alpha_i r_i in Q,
p_beta=sum_j beta_j p_j in Q.                       (18)
```

Contract (11) by `alpha_i beta_j`.  Both tangent summands vanish, while the
target diagonal and residual monomial give (7).

Because `x,y` are not proportional to `e_2`, choose bases

```text
alpha_0 in x^perp intersect e_2^perp,
alpha_1 in x^perp,       (alpha_1)_2=1,

beta_0 in y^perp intersect e_2^perp,
beta_1 in y^perp,        (beta_1)_2=1.              (19)
```

Put

```text
R_a=r_(alpha_a),       P_b=p_(beta_b),
A_ka=(alpha_a)_k,      B_kb=(beta_b)_k.             (20)
```

Then `R=span(R_0,R_1)` and `P=span(P_0,P_1)` are two-planes in `Q`, and

```text
A_2*=B_2*=(0,1),

per(R_a,P_b,q_k)
 =A_ka B_kb T_k+lambda delta_(a=1)delta_(b=1)S_k.   (21)
```

Only `(1,1)` is corrected.  The other three entries of each slice are

```text
A_k0 B_k0 T_k,       A_k0 B_k1 T_k,
A_k1 B_k0 T_k.                                      (22)
```

This is an equality in the whole source tensor space, not a selected-source
specialization.

It is not a converse to the face equations.  For example, take `x=y=e_1`
and add a nonzero source tensor `Z` to the `(1,1)` entry of `P^(1)`, leaving
every other displayed entry fixed.  Every `alpha in x^perp` and
`beta in y^perp` has `alpha_1=beta_1=0`, so all contractions (21) are
unchanged.  The recovery of `S_1` from `P_221` and the complete `k=0`
flattening are also unchanged.  But now

```text
F^(1)_11=Z!=0.                                       (21a)
```

Thus (4a) is logically indispensable; no endpoint exclusion may infer the
full two faces from the corrected cube.

## 4. Exact target-visibility census

Fix the denominator-free choices

```text
alpha_0=(x_1,-x_0,0),       beta_0=(y_1,-y_0,0).    (23)
```

Evaluation at colour `k` is nonzero on `x^perp` exactly when `x` is not
proportional to `e_k`, and similarly for `y^perp`.  The outer product of the
two evaluation vectors has a nonzero entry outside `(1,1)` exactly when both
vectors are nonzero and their zero-th coordinates do not both vanish.  Thus

```text
T_2: always confined to the corrected (1,1) cell;

T_0 visible in a nonexceptional cell iff
  x not proportional e_0,
  y not proportional e_0,
  (x_1,y_1)!=(0,0);

T_1 visible in a nonexceptional cell iff
  x not proportional e_1,
  y not proportional e_1,
  (x_0,y_0)!=(0,0).                                 (24)
```

Simultaneous two-target pressure occurs precisely on the intersection of the
two open conditions in (24).  Every one-visible and zero-visible support wall
is explicit.

## 5. A two-radical exclusion inside the quotient

The corrected cube already excludes one generic incidence subcase.

### Lemma 1 (two radicals cannot expose two transverse targets)

Let `Q=span(a,b,c)` be three-dimensional and put

```text
M_(u,v)(q)=per(u,v,q).
```

If

```text
M_(c,a)(Q)=M_(c,b)(Q)=0,                            (25)
```

then `M_(a,b)(Q)` cannot contain two nonzero decomposable tensors that are
fully transverse in all three source factors.

#### Proof

Split by the number of nonzero source components of `c`.

If `c=(x,y,z)` has all three components nonzero, the equations
`per(c,a,c)=per(c,b,c)=0`, projected successively modulo the three factor
lines of `c`, give

```text
a=(A x,B y,C z),       A+B+C=0,
b=(U x,V y,W z),       U+V+W=0.                    (26)
```

The equations at `a,b` and the mixed equation give

```text
AB+AC+BC=0,
UV+UW+VW=0,
AV+AW+UB+BW+UC+VC=0.                               (27)
```

On the plane `s+t+u=0`, the quadratic form

```text
st+su+tu=-s^2-st-t^2
```

has nondegenerate polar form of determinant `3`.  Since `a,b,c` are
independent, the two scaling triples in (26) form a basis of that plane.
Equations (27) would make its whole polar Gram matrix zero, a contradiction.

If `c` has two source components, `per(c,a,c)=per(c,b,c)=0` forces both
`a,b` to miss the third component.  Then all of `Q` misses it and
`M_(a,b)(Q)=0`.

If `c` is pure, `per(c,a,a)=per(c,b,b)=0` makes each of `a,b` miss at least
one of the other two sources.  If they miss the same source, the preceding
conclusion applies.  In the crossed case, `per(c,a,b)=0` forces one of
`a,b` to be pure in the source of `c`; every nonzero value of `M_(a,b)` then
has that fixed factor line.  Two outputs cannot be fully transverse.  QED.

Now assume

```text
x_2=y_2=0,
R!=P,
R intersect P=span(r_2)=span(p_2).                 (28)
```

Scale the common row to `c`.  Take

```text
a=r_(x_1,-x_0,0),       b=p_(y_1,-y_0,0).
```

Equation (21) gives both radical identities (25), while

```text
M_(a,b)(q_0)=x_1 y_1 T_0,
M_(a,b)(q_1)=x_0 y_0 T_1                         (29)
```

up to the harmless simultaneous signs from (23).  Lemma 1 therefore proves

```text
x_0 x_1 y_0 y_1=0                                  (30)
```

on the distinct-plane exceptional-intersection subcase (28).  Thus its
fully supported middle-plane orbit is already empty.

## 6. A sharp quotient control

The corrected cube is consistent.  Let `x=y=e_1` and work in

```text
Q=span(X_0,Y_0,Z_0) subset X^* direct-sum Y^* direct-sum Z^*.
```

Choose

```text
(R_0,R_1)=(Y_0,Z_0),
(P_0,P_1)=(Z_0,Y_0),
(q_0,q_1,q_2)=(X_0,Y_0,Z_0).                        (31)
```

The only nonzero displayed cells of the six-term polarization are

```text
per(R_0,P_0,q_0)=T_0,
per(R_1,P_1,q_0)=T_0.                               (32)
```

Therefore

```text
S_0=lambda^(-1)T_0,
S_1=0,
S_2=-lambda^(-1)T_2                                (33)
```

realizes (21) exactly.  Both row planes and the third row are injective in
`Q`.  This control does not choose the outside graph rows in (17), does not
satisfy (5), and is not a physical witness.  It proves that a valid exclusion
cannot discard the quotient cube alone.

## 7. Proof-topology consequence

After S2CD and S2CE, the monomial part of the fully-injective `(3,3,3)`
rank-four/rank-eight cell consists only of the two diagonal coordinate
endpoints.  For either endpoint, the complete target obligation is now

```text
complete recovered face residuals (4a),
corrected Q-cube (21),
support census (24),
two-radical exclusion (30),
nonzero tangent-coset rank-one flattening (5)--(6).  (34)
```

The finite successor is an incidence atlas for the two planes `R,P` in `Q`,
split by (24), retaining the complete recovered faces (4a), and coupled to
the nine ordinary pivot charts of `kappa`.  Atlas coverage and per-chart
certificates remain proof obligations.

```text
full diagonal coordinate-endpoint target reduction: PROVED;
diagonal coordinate-endpoint exclusion:              OPEN;
nonmonomial fully-injective residuals:                OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (35)
```

## 8. Focused replay

From repository root:

```bash
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_full_target_reduction.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_full_target_reduction.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_full_target_reduction.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_full_target_reduction.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_full_target_reduction.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_full_target_reduction.py
```

The primary replay checks (11), gauge invariance, all three slice equations,
source-tensor elimination with the sixteen retained face entries, the
flattening minors, contraction (7), the explicit omission control (21a), the
exhaustive support census, and the split-form control.  The no-import audit
reconstructs these interfaces with a separate sparse/Fraction representation.

## Dependencies

- [Fully-injective monomial-residual endpoint localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_MONOMIAL_RESIDUAL_ENDPOINT_LOCALIZATION_THEOREM.md)
- [Diagonal-monomial two-supported endpoint exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_TWO_SUPPORTED_ENDPOINT_EXCLUSION_THEOREM.md)
- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)

## Scope boundary

```text
characteristic-zero diagonal endpoint full-target reduction: PROVED;
ordinary polynomial flattening formulation:                  PROVED;
complete recovered `k=1,2` face residuals:                   PROVED;
corrected three-space cube and support census:                PROVED;
distinct-plane exceptional-intersection generic orbit:        IMPOSSIBLE;
quotient-only sharpness control:                              EXACT;
exhaustive plane-incidence/tangent-pivot atlas:               OPEN;
diagonal coordinate endpoint:                                OPEN;
nonmonomial rank-four/rank-eight residuals:                   OPEN;
other lower-rank target cells and pair coupling:              OPEN;
other components, pole strata, higher orders, all-rank drop: OPEN;
global Krenn--Gu conjecture:                                  UNRESOLVED.   (36)
```
