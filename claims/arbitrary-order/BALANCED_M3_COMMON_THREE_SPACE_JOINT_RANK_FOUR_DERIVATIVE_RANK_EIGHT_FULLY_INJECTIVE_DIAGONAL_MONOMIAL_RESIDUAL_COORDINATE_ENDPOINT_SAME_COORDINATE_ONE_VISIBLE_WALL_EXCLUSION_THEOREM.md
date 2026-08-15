# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective diagonal-monomial coordinate-endpoint same-coordinate one-visible-wall exclusion

## Status

**Exact characteristic-zero exclusion of the two same-coordinate
one-visible subcells at the surviving diagonal monomial coordinate
endpoints.**  Retain the normalized physical full-sensor hypotheses and
notation of S2CF:

```text
C=lambda e_2 tensor e_2,             w=e_0,          lambda!=0,

D(a,b,c)=(a tensor y-x tensor b) tensor e_0
          +C tensor c,

ker D=span((x,y,0)) subset K,         dim K=4,
rank rho=rank pi=rank theta=3,
x not proportional e_2,              y not proportional e_2.       (1)
```

Let `Q=span(q_0,q_1,q_2)`.  S2CF and the full-sensor quotient determinant
give

```text
per(r_alpha,p_beta,q_k)
 =alpha_k beta_k T_k+lambda alpha_2 beta_2 S_k,
alpha in x^perp,       beta in y^perp,               (2)

Alt(Q)!=0.                                                (3)
```

Then neither of the projective support cells

```text
x proportional y proportional e_1,
x proportional y proportional e_0                    (4)
```

contains a physical point.  The first cell is excluded by the two cross-zero
pairs in (2), the S2CG zero-pair classification, and the complete recovered
`k=1` face.  The second requires the same incidence dichotomy plus source
recovery and the unsliced tangent-coset equation; a triple quotient would
otherwise make the transverse targets `T_0,T_2` proportional.

This theorem does not exclude the other one-visible support cells or the
two-visible open cell.  It therefore does not close either diagonal
coordinate endpoint.  All other nonmonomial residuals, wider lower-rank
cells, pair gates, components, poles, higher orders, and all-rank drop remain
open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. A two-cross-pair incidence dichotomy

For rows `u,v,q` in
`W^*=X^* direct-sum Y^* direct-sum Z^*`, write

```text
M_(u,v)(q)=per(u,v,q).                                 (5)
```

We use the following consequence of S2CG.  Let

```text
R=span(A,C) subset Q,          P=span(B,D) subset Q   (6)
```

be two-planes, and assume

```text
M_(A,D)|Q=0,          M_(C,B)|Q=0,
M_(A,B)|Q!=0.                                         (7)
```

Then one of the following geometric alternatives holds:

```text
(i)  Q=span(x_s,y_s,z_s), where x_s,y_s,z_s are pure
     nonzero rows in the three distinct sources;

(ii) R=P=H=span(x_s,y_s), a split two-source plane.  (8)
```

Indeed, an independent zero pair is a conjugate pair spanning a split
two-source plane by S2CG Lemma 1.  A dependent zero pair is a nonzero
square-zero row, hence a pure source line by the square-zero branch of S2CG
Corollary 2.

If both cross pairs are independent, their split planes are either equal,
giving (ii), or distinct.  In the latter case S2CG Corollary 3 makes their
intersection a pure common-source line and their sum the three-source split
space in (i).  If one pair is dependent, its pure line either lies in the
other split plane, giving (ii), or supplies that plane's omitted source,
giving (i); a different line in either used source would make `Q` miss the
omitted source and contradict (3).  If both pairs are dependent, the two
pure lines are distinct because `R,P` have dimension two, and (7) forces
them into different sources.  Then `R=P` is the split plane in (ii).

Thus (8) is exhaustive.  No generic row, plane position, or cross-ratio is
assumed.

## 2. The complementary same-coordinate wall `x=y=e_1`

Normalize the first cell of (4) as `x=y=e_1` and put

```text
A=r_0,       C_0=r_2,       B=p_0,       D=p_2.
```

Taking the coordinate bases of `x^perp=y^perp=span(e_0,e_2)` in (2) gives

```text
M_(A,D)|Q=0,             M_(C_0,B)|Q=0,
M_(A,B)(q_k)=delta_(k=0)T_0.                         (9)
```

The involved-row injectivity makes both planes in (6) two-dimensional, so
Section 1 applies.

In alternative (i), every permanent of three rows in `Q` lies on the single
pure tensor line `x_s tensor y_s tensor z_s`.  The last equation in (9)
identifies this line with `span(T_0)`.  Let a bar denote the triple quotient

```text
(X^*/span(X_0)) tensor
(Y^*/span(Y_0)) tensor
(Z^*/span(Z_0)).                                    (10)
```

Because `q_1` is a sum of the three base pure rows, every term of
`M_(r_1,p_1)(q_1)` contains one base factor and dies in (10).  But the
complete recovered face (S2CF (15a)) says

```text
M_(r_1,p_1)(q_1)=T_1,                               (11)
```

whose triple quotient is nonzero.  This is a contradiction.

In alternative (ii), `H` uses only two sources.  Hence

```text
H subset ker(M_(A,B)|Q).
```

By (9), that kernel is `span(q_1,q_2)`, also a two-plane, so

```text
H=span(q_1,q_2).                                    (12)
```

The sixteen complete retained face equations include, for
`j in {0,2}` and `k in {1,2}`, and symmetrically for `i in {0,2}`,

```text
per(r_1,p_j,q_k)=0,             per(r_i,p_1,q_k)=0. (13)
```

Since `P=R=H=span(q_1,q_2)`, equations (13) say

```text
M_(r_1,H)(H)=0,                 M_(H,p_1)(H)=0.     (14)
```

Choose the two pure generators `x_s,y_s` of `H`.  Evaluating (14) on this
ordered pair forces the omitted-source components of both `r_1` and `p_1`
to vanish.  The row `q_1 in H` misses the same source, so its permanent with
`r_1,p_1` is zero.  This again contradicts (11).

Therefore the `x=y=e_1` one-visible cell is empty.  This exclusion uses the
complete recovered faces, not a converse inferred from the corrected cube.

## 3. The aligned same-coordinate wall `x=y=e_0`

Now normalize the second cell of (4) as `x=y=e_0` and put

```text
A=r_1,       C_1=r_2,       B=p_1,       D=p_2.
```

The corrected cube gives

```text
M_(A,D)|Q=0,             M_(C_1,B)|Q=0,
M_(A,B)(q_k)=delta_(k=1)T_1.                        (15)
```

Section 1 again gives alternatives (i) and (ii), now with the pure
three-source line in (i), or the missing-source completion of `H` in (ii),
identified with the factor lines of `T_1`.

Let a bar denote projection to

```text
(X^*/span(X_1)) tensor
(Y^*/span(Y_1)) tensor
(Z^*/span(Z_1)).                                    (16)
```

In alternative (i), `q_0 in Q` is a sum of the three base pure rows, so

```text
bar(M_(r_0,p_0)(q_0))=0.                            (17)
```

In alternative (ii), `H` is contained in the kernel of the last map in
(15), which is `span(q_0,q_2)`.  Equality follows by dimension, so `q_0 in H`
and (17) again holds.

The complete target is now essential.  S2CF writes it as

```text
P^(0)-E_00 T_0=(C+H_0)S_0+H_1S_1+H_2S_2,
P^(1)-E_11 T_1=C S_1,
P^(2)-E_22 T_2=C S_2,                               (18)
```

where `C=lambda E_22` and `H_c=a_c tensor y-x tensor b_c`.  Since
`x=y=e_0`, every `(H_c)_22` vanishes.  The `(2,2)` root entries of all three
slices therefore give

```text
S_0=lambda^(-1)M_(C_1,D)(q_0),
S_1=lambda^(-1)M_(C_1,D)(q_1),
S_2=lambda^(-1)(M_(C_1,D)(q_2)-T_2).                (19)
```

In alternative (i), all three permanent terms on the right lie in
`span(T_1)`.  In alternative (ii), the `q_0,q_2` terms vanish because all
three rows lie in the two-source plane `H`, while the `q_1` term lies in
`span(T_1)`.  Thus in both alternatives

```text
bar(S_0)=bar(S_1)=0,             bar(S_2)=-lambda^(-1)bar(T_2).  (20)
```

Take the `(0,0)` root entry of the first equation in (18) and apply (16).
Here `C_00=0`; equations (17) and (20) leave

```text
-bar(T_0)=-lambda^(-1)(H_2)_00 bar(T_2).            (21)
```

But `bar(T_0)` and `bar(T_2)` are nonzero and linearly independent: their
three factor lines remain distinct after quotienting by the factor lines of
the fully transverse tensor `T_1`.  Equation (21) is impossible.

Therefore the `x=y=e_0` one-visible cell is empty.  This second exclusion
genuinely uses source recovery and the unsliced tangent-coset equation.

## 4. Proof-topology consequence

Together with S2CH, the diagonal endpoint visibility split is now

```text
zero-visible wall:                                  IMPOSSIBLE;
same-coordinate one-visible cells x=y=e_0,e_1:      IMPOSSIBLE;
other one-visible support cells:                     OPEN;
two-visible open cell:                               OPEN;
complete diagonal coordinate endpoint:              OPEN;
other nonmonomial rank-eight residuals:              OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (22)
```

No target-stabilizer argument is claimed to reduce a general one-visible
support pair to (4).  The remaining non-same-coordinate support patterns
retain their evaluation parameters and complete face/flattening coupling.

## 5. Focused replay

From repository root:

```bash
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_same_coordinate_one_visible_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_same_coordinate_one_visible_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_same_coordinate_one_visible_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_same_coordinate_one_visible_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_same_coordinate_one_visible_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_same_coordinate_one_visible_exclusion.py
```

The primary replay checks the two normalized cube tables, the complete-face
indices, the split/equal-plane incidence interfaces, source recovery, and
the transverse quotient contradiction.  The independent no-import audit
uses a separate exact-arithmetic implementation and reversed traversal.
S2CG's written proof owns the zero-pair support theorem and its exhaustive
dependent/independent geometry.

## Dependencies

- [Diagonal coordinate-endpoint full-target reduction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_FULL_TARGET_REDUCTION_THEOREM.md)
- [Canonical-binomial residual exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_CANONICAL_BINOMIAL_RESIDUAL_EXCLUSION_THEOREM.md)
- [Diagonal zero-visible-wall exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_ZERO_VISIBLE_WALL_EXCLUSION_THEOREM.md)

## Scope boundary

```text
characteristic-zero same-coordinate subcell exclusion: PROVED;
two-cross-pair incidence dichotomy:                     PROVED;
complementary x=y=e_1 recovered-face contradiction:    PROVED;
aligned x=y=e_0 unsliced-quotient contradiction:        PROVED;
other one-visible and all two-visible cells:             OPEN;
complete diagonal endpoint exclusion:                    OPEN;
other nonmonomial residuals and wider branches:           OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED.    (23)
```
