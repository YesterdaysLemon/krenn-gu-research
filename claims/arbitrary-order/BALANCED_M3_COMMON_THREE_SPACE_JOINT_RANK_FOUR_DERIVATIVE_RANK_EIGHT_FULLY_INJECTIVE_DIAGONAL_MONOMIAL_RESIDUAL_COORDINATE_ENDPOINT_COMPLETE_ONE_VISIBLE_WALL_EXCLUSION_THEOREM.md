# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective diagonal-monomial coordinate-endpoint complete one-visible-wall exclusion

## Status

**Exact characteristic-zero exclusion of the complete one-visible wall at
the surviving diagonal monomial coordinate endpoints.**  Retain the
normalized physical full-sensor hypotheses and notation of S2CF:

```text
C=lambda e_2 tensor e_2,             w=e_0,          lambda!=0,

D(a,b,c)=(a tensor y-x tensor b) tensor e_0+C tensor c,
ker D=span((x,y,0)) subset K,         dim K=4,

rank rho=rank pi=rank theta=3,
x not proportional e_2,              y not proportional e_2.       (1)
```

Let `Q=span(q_0,q_1,q_2)`.  S2CF gives, for
`alpha in x^perp` and `beta in y^perp`,

```text
M_(r_alpha,p_beta)(q_k)
 =alpha_k beta_k T_k+lambda alpha_2 beta_2 S_k,      (2)
```

where `M_(u,v)(q)=per(u,v,q)`.  Kernel incidence and full-sensor rank give

```text
Alt(Q)!=0.                                           (3)
```

Assume exactly one of `T_0,T_1` is visible outside the corrected cell in
the sense of S2CF's exact visibility census.  Then no physical point exists.

The proof exhausts all twenty ordered projective support masks on the
one-visible wall.  Two same-coordinate masks were excluded in S2CI.  Four
coordinate/two-support masks create a forbidden two-dimensional radical
shore.  The other fourteen masks admit two cross-zero pairs and S2CG's
split-three-source/common-split-plane dichotomy.  Seven `T_0`-only masks
contradict the retained face `P_111=T_1`; six `T_1`-only masks contradict the
unsliced target after exact source recovery; and the last
`supp(x)=supp(y)={0,2}` mask falls only after the whole unsliced root matrix
forces `H_2=0`; graph gauge then removes the first- and second-root entries
of the lift `k_2` while retaining its third entry `e_2`.

This theorem does not exclude the two-visible open cell and therefore does
not close either diagonal coordinate endpoint.  Every other nonmonomial
residual, lower-rank target cell, pair gate, component, pole stratum, higher
order, and all-rank-drop branch remains open.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. Exhaustive support atlas

For a nonzero coordinate vector, write its projective support as a subset of
`{0,1,2}`.  Since neither `x` nor `y` is proportional to `e_2`, the six
possible supports are

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

Direct Boolean intersection of (4)--(5) gives exactly the following twenty
ordered masks:

| visible target | prior same-coordinate | radical masks | cross-pair masks |
| --- | --- | --- | --- |
| `T_0` only | `({1},{1})` | `({1},{0,2})`, `({0,2},{1})` | `({1},{0,1})`, `({1},{1,2})`, `({1},{0,1,2})`, `({0,1},{1})`, `({1,2},{1})`, `({1,2},{1,2})`, `({0,1,2},{1})` |
| `T_1` only | `({0},{0})` | `({0},{1,2})`, `({1,2},{0})` | `({0},{0,1})`, `({0},{0,2})`, `({0},{0,1,2})`, `({0,1},{0})`, `({0,2},{0})`, `({0,1,2},{0})`, `({0,2},{0,2})` |

The two entries in the second column are empty by S2CI.  Sections 2--5
exclude the remaining eighteen.  Thus the table is a mathematical case
cover, not a count of solver inputs.

## 2. Four radical-shore masks

Consider `x=e_1` and `supp(y)={0,2}`.  Since `e_1 in y^perp`, injectivity
gives a nonzero row `p_1 in Q`.  Every `alpha in x^perp=span(e_0,e_2)`
satisfies

```text
alpha_k(e_1)_k=0 for k=0,1,2,
alpha_2(e_1)_2=0.                                  (6)
```

Equation (2) therefore makes the injective two-plane `r(x^perp)` a subset
of `Rad_Q(p_1)`.  S2CG Corollary 2 bounds the radical of every nonzero row in
an `Alt`-nonzero three-space by one dimension, contradicting (3).

Root exchange gives `({0,2},{1})`.  For the `T_1`-only orientation
`x=e_0,supp(y)={1,2}`, take the nonzero row `p_0 in Q`.  Every
`alpha in x^perp=span(e_1,e_2)` has zero coordinate products with `e_0`,
and the correction product also vanishes because `(e_0)_2=0`.  Thus
`r(x^perp) subset Rad_Q(p_0)`, the same contradiction.  Root exchange gives
`({1,2},{0})`.  Hence all four radical masks in the table are empty without
moving the normalized line `w=e_0`.

## 3. Cross-pair normal forms

Every remaining nonsame-coordinate mask has two bases of the perpendicular
planes for which one corner is the visible target and both cross corners
vanish identically in (2).

For the three `T_0`-only masks with `x=e_1` and `y_1!=0`, take

```text
alpha_A=e_0,                  alpha_Ap=e_2,
beta_B=y_1 e_0-y_0 e_1,      beta_Bp=y_2 e_1-y_1 e_2. (7)
```

In every displayed basis, write
`A=r_(alpha_A),A'=r_(alpha_Ap),B=p_(beta_B),B'=p_(beta_Bp)`.
Then

```text
M_(A,B')|Q=M_(A',B)|Q=0,
M_(A,B)(q_k)=y_1 delta_(k=0)T_0.                    (8)
```

The two covector pairs in (7) are bases.  Root exchange covers the other
three ordered masks.  For the seventh mask
`supp(x)=supp(y)={1,2}`, use

```text
alpha_A=beta_B=e_0,
alpha_Ap=x_2 e_1-x_1 e_2,
beta_Bp=y_2 e_1-y_1 e_2,                            (9)
```

which gives (8) with visible coefficient one.

For the three `T_1`-only masks with `x=e_0` and `y_0!=0`, take

```text
alpha_A=e_1,                  alpha_Ap=e_2,
beta_B=y_1 e_0-y_0 e_1,      beta_Bp=y_2 e_0-y_0 e_2. (10)
```

Now

```text
M_(A,B')|Q=M_(A',B)|Q=0,
M_(A,B)(q_k)=-y_0 delta_(k=1)T_1.                  (11)
```

Root exchange covers three more ordered masks.  The sole remaining mask is
`supp(x)=supp(y)={0,2}` and is treated in Section 5.

For every system (8) or (11), let

```text
R=span(A,A'),                P=span(B,B').           (12)
```

Both are two-planes by involved-row injectivity.  The two-cross-pair
dichotomy proved in S2CI from S2CG's zero-pair classification is exhaustive:

```text
(i) Q=span(x_s,y_s,z_s) is split across the three sources; or

(ii) R=P=H=span(x_s,y_s) is one split two-source plane. (13)
```

Dependent cross pairs are included: a dependent square-zero row is pure.
Distinct independent planes, or one independent plane plus a pure line in
its omitted source, give (i); equal planes and the remaining dependent cases
give (ii).  The nonzero visible map excludes a same-source collapse.  No
generic plane position is assumed.

## 4. The ordinary cross-pair masks

### 4.1 Every `T_0`-only mask

In fork (i), `Q` is spanned by the three pure rows defining the factor lines
of `T_0`.  Since `q_1 in Q` is a sum of those base rows, every summand of
`M_(r_1,p_1)(q_1)` contains one `T_0` factor.  Hence the triple quotient by
the three factor lines of `T_0` kills that permanent, even though `r_1,p_1`
need not lie in `Q`.

In fork (ii), the visible map in (8) has kernel `span(q_1,q_2)`.  Since
three rows in the two-source plane `H` have zero permanent,

```text
H subset ker(M_(A,B)|Q)=span(q_1,q_2),
```

and equality follows by dimension.  Thus `q_1` lies in the two base factor
lines of `T_0`, so the same triple quotient again kills
`M_(r_1,p_1)(q_1)`.

The complete recovered face says

```text
M_(r_1,p_1)(q_1)=P_111=T_1,                         (14)
```

and the fully transverse `T_1` survives that quotient.  This contradiction
excludes all seven `T_0`-only cross-pair masks.

### 4.2 Six `T_1`-only masks with one coordinate shore

Take the orientation `x=e_0`, `y_0!=0` and the rows in (10).  In either fork
of (13), quotienting by the three factor lines of `T_1` kills

```text
M_(A',B')(q_k) for k=0,1,2,           and every P_ij0. (15)
```

For fork (i), this is because `Q` is the split space defining `T_1`.  For
fork (ii), `H=span(q_0,q_2)` is the kernel of the visible map; the `q_0,q_2`
permanents vanish and the `q_1` permanent lies on `T_1`.  In both forks,
`q_0` supplies a base factor to every `P_ij0`.

With `A'=r_2` and `B'=p_(y_2 e_0-y_0 e_2)`, the exact complete target gives

```text
M_(A',B')(q_0)=y_2 P_200-y_0 P_220=-y_0 lambda S_0,
M_(A',B')(q_1)=y_2 P_201-y_0 P_221=-y_0 lambda S_1,
M_(A',B')(q_2)=y_2 P_202-y_0 P_222=-y_0(T_2+lambda S_2). (16)
```

Here `P_201=P_202=0` are retained face equations.  The first identity follows
directly from the unsliced coefficient formula:

```text
P_200=y_0 sum_c (a_c)_2 S_c,
P_220=y_2 sum_c (a_c)_2 S_c+lambda S_0.             (17)
```

Since `y_0 lambda!=0`, (15)--(16) give in the `T_1` triple quotient

```text
bar(S_0)=bar(S_1)=0,
bar(S_2)=-lambda^(-1)bar(T_2).                      (18)
```

Apply the quotient to the `(0,0,0)` coefficient of

```text
P^(0)-E_00T_0=(C+H_0)S_0+H_1S_1+H_2S_2.           (19)
```

By (15), its left side is `-bar(T_0)`.  Equation (18) makes the right side a
scalar multiple of `bar(T_2)`.  These two quotient target classes are
nonzero and independent, a contradiction.  The root-exchanged calculation
can be kept equally explicit.  For `y=e_0,x_0!=0`, take
`A'=r_(x_2e_0-x_0e_2)` and `B'=p_2`.  Then

```text
M_(A',B')(q_0)=x_2 P_020-x_0 P_220=-x_0 lambda S_0,
M_(A',B')(q_1)=x_2 P_021-x_0 P_221=-x_0 lambda S_1,
M_(A',B')(q_2)=x_2 P_022-x_0 P_222=-x_0(T_2+lambda S_2). (19a)
```

Here `P_021=P_022=0` are retained faces, while the first identity follows
from the root-exchanged version of (17).  Thus the same quotient argument
applies without an unstated stabilizer, and all six masks covered by (10)
and root exchange are empty.

## 5. The final support cell `{0,2}` by `{0,2}`

Write

```text
x=(x_0,0,x_2),          y=(y_0,0,y_2),
x_0 x_2 y_0 y_2!=0,                                    (20)

A=r_1,                  B=p_1,
A'=r_(x_2,0,-x_0),      B'=p_(y_2,0,-y_0).            (21)
```

The cross cells vanish and

```text
M_(A,B)(q_k)=delta_(k=1)T_1.                         (22)
```

Thus (13) applies.  In either fork, the `T_1` triple quotient kills every
`P_ij0` and every `M_(A',B')(q_k)`, exactly as in (15).  Put

```text
eta=x_2 y_2/(x_0 y_0),          r=eta/lambda.        (23)
```

Equation (2) for the rows `A',B'` now gives

```text
bar(S_0)=-r bar(T_0),
bar(S_1)=0,
bar(S_2)=-lambda^(-1)bar(T_2).                       (24)
```

This time the whole root matrix in (19) is needed.  Since `bar(P^(0))=0`,
substitution of (24) yields

```text
-E_00 bar(T_0)
 =-r(C+H_0)bar(T_0)-lambda^(-1)H_2 bar(T_2).        (25)
```

The two quotient target classes are independent.  Coefficient comparison
therefore proves

```text
H_2=0,                  E_00=r(C+H_0).              (26)
```

The first identity is

```text
a_2 tensor y=x tensor b_2.
```

If one side vanishes then `a_2=b_2=0`, and put `t=0`.  Otherwise equality of
nonzero rank-one tensors gives `a_2=t x,b_2=t y` for one scalar `t`.  Replace
the graph lift by `k_2 -> k_2-t(x,y,0)`, namely use the gauge

```text
a_2 -> a_2-t x,             b_2 -> b_2-t y          (27)
```

This sets both vectors to zero without changing any `H_c` or the third entry
`e_2` of `k_2`.  Under this basis shear the dual rows `q_0,q_1,q_2` remain
fixed (only the complementary row `h` shifts).  S2CF's row formula

```text
r_i=x_i h+sum_c (a_c)_i q_c,
p_j=y_j h+sum_c (b_c)_j q_c                         (28)
```

then puts both perpendicular planes inside `span(q_0,q_1)`.  Injectivity
makes

```text
R=P=span(q_0,q_1).                                  (29)
```

Reapply the cross-pair classification inside this common plane.  An
independent zero pair spans it as a split two-source plane; if both pairs are
dependent, their distinct pure lines do the same.  Hence the common plane in
(29) is split across only two sources.  But `A,B,q_1` all lie in it, so

```text
M_(A,B)(q_1)=0,
```

contradicting (22).  This excludes the final mask.

The divisions in (23) use only `lambda,x_0,x_2,y_0,y_2`, all nonzero by the
named support cell and upstream endpoint hypothesis.  No hidden
localization, limit, or generic coefficient is used.

## 6. Proof-topology consequence

Together with S2CH and S2CI, the diagonal endpoint visibility split is now

```text
zero-visible wall:                                  IMPOSSIBLE;
complete one-visible wall:                          IMPOSSIBLE;
two-visible open cell:                              OPEN;
complete diagonal coordinate endpoint:              OPEN;
other nonmonomial rank-eight residuals:              OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (30)
```

The remaining two-visible cell still requires S2CF's sixteen retained face
equations and its nonzero tangent-coset root/source flattening.  This theorem
does not infer that an arbitrary nonmonomial residual degenerates or
normalizes to a monomial endpoint.

## 7. Focused replay

From repository root:

```bash
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_complete_one_visible_wall_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_complete_one_visible_wall_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_complete_one_visible_wall_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_complete_one_visible_wall_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_complete_one_visible_wall_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_complete_one_visible_wall_exclusion.py
```

The primary replay exhausts all twenty ordered support masks, checks the
four radical shores, every cross-pair covector basis and cube coefficient,
the retained face indices, source recovery identities, and final full-matrix
quotient/gauge interface.  The independent no-import audit uses a separate
standard-library exact-arithmetic implementation with reversed traversal.
S2CG's written proof owns the coordinate-free zero-pair classification and
radical theorem.

## Dependencies

- [Diagonal coordinate-endpoint full-target reduction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_FULL_TARGET_REDUCTION_THEOREM.md)
- [Canonical-binomial residual exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_CANONICAL_BINOMIAL_RESIDUAL_EXCLUSION_THEOREM.md)
- [Diagonal zero-visible-wall exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_ZERO_VISIBLE_WALL_EXCLUSION_THEOREM.md)
- [Same-coordinate one-visible-wall exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_SAME_COORDINATE_ONE_VISIBLE_WALL_EXCLUSION_THEOREM.md)

## Scope boundary

```text
characteristic-zero one-visible-wall exclusion:      PROVED;
twenty-mask support cover:                            PROVED;
four radical masks:                                   PROVED;
fourteen cross-pair masks:                            PROVED;
complete diagonal endpoint exclusion:                 OPEN;
two-visible diagonal cell:                            OPEN;
other nonmonomial residuals and wider branches:        OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (31)
```
