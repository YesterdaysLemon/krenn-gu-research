# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight one-deficient-involved-row third-row-rank-three complete exclusion

## Status

**Exact characteristic-zero exclusion of every joint-rank-four,
derivative-rank-eight row profile with an injective third row and at least one
rank-two involved row.**  Retain the normalized, target-consistent physical
`m=3` common-three-space full-sensor hypotheses with singleton span dimension
three, joint rank four, all three root blocks nonzero, and shared-derivative
rank eight.  Up to exchanging the first two roots, suppose

```text
rank rho=2,                  rank theta=3,
rank pi in {2,3}.                                      (1)
```

Then the physical empty-target equations are inconsistent.  The `rank pi=2`
case is already closed by S2BR and S2BX (distinct and equal missing colours,
respectively).  The new content is the complete mixed profile

```text
(rank rho,rank pi,rank theta)=(2,3,3),               (2)
```

and, by exchanging the involved roots, `(3,2,3)`.

Only the one deficient involved row is needed.  Its missing-coordinate
contraction reduces the complete singleton correction to one pure source
line because the third projection is injective modulo the derivative
syzygy.  The order-three permanent-rank obstruction removes that last line,
leaving the same exact binary diagonal table as S2BX on the two
complementary colours.  Restricting the injective second row to those two
colours supplies a binary row plane.  The third row's missing binary colour
is a common zero; arbitrary shifts along it and the exact S2BF
intersecting-plane obstruction give the same four-space contradiction as in
S2BX.

Consequently every rank-four/rank-eight profile with third-row rank three
and a deficient involved row is empty.  The sole third-row-rank-three row
profile left in this derivative cell is `(3,3,3)`.  Third-row-rank-two mixed
and injective profiles, joint-rank-three/rank-eight cells, derivative-rank-
seven cells, other components and pole strata, higher orders, and all-rank
drop remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. One missing row determines the complete correction

Let `d` be the kernel colour of `rho`, and let `s,t` be the other two
colours.  S2BR gives

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
ker D=span((x,y,0)),                                 (3)

x_d=0,
(e_d^* tensor id)C=kappa e_d,       kappa!=0.       (4)
```

Because `rank rho=2`, every first component of a vector in `K` lies in
`e_d^perp`.  Because `rank theta=3`,

```text
ker(pr_3|K)=ker D.                                  (5)
```

Choose graph lifts `k_c=(a_c,b_c,e_c)` for `c=d,s,t`.  Their images
`U_c=D(k_c)` form a basis of `U`.  Write the complete target identity as

```text
G_N-J=S_d U_d+S_s U_s+S_t U_t.                     (6)
```

First-`d` contraction kills `G_N` and gives

```text
(e_d^* tensor id tensor id)U_c
 =kappa e_d tensor e_c.                             (7)
```

Comparison with the `d` contraction of `J` therefore forces

```text
S_d=-kappa^(-1)T_d,                 S_s=S_t=0.      (8)
```

No row-kernel property of `pi` has entered.

Put

```text
F_d=e_d tensor e_d tensor e_d-kappa^(-1)U_d.       (9)
```

If `F_d` were nonzero, one root evaluation would make `G_N` a concise
three-term diagonal source tensor.  Its three flattening ranks force the
three local maps from `P_3` to be invertible, contradicting tensor ranks
four and three.  This is exactly the pointwise rank argument of S2BX and
gives

```text
F_d=0,
G_N=e_s tensor e_s tensor e_s T_s
   +e_t tensor e_t tensor e_t T_t.                 (10)
```

## 2. The mixed profile contains the same shifted binary frame

Let

```text
R=span(r_s,r_t),             P_0=span(p_s,p_t),
Q_0=span(q_s,q_t),           Q=span(q_d,q_s,q_t).   (11)
```

All three displayed binary spaces are two-planes: `rho` has kernel exactly
`e_d^*`, while `pi` and `theta` are injective in the mixed profile.  The
joint row space

```text
V=span(R,image pi,Q)                               (12)
```

has dimension four.  Equation (10), restricted to the indicated rows, is

```text
Perm(r_a,p_b,q_c)=delta_(a,b,c)T_c,
a,b,c in {s,t}.                                    (13)
```

Moreover the full third-row coefficient at colour `d` is zero:

```text
Perm(R,P_0,q_d)=0.                                  (14)
```

The S2BX four-space binary-frame lemma, which is a direct corollary of
S2BF's exact intersecting-middle-plane obstruction, gives

```text
R intersect P_0=R intersect Q_0=P_0 intersect Q_0=0. (15)
```

For arbitrary scalars `lambda_s,lambda_t`, the shifted plane

```text
Q_lambda=span(q_s+lambda_s q_d,
              q_t+lambda_t q_d)                    (16)
```

carries the same table by (14).  Hence

```text
R intersect Q_lambda=P_0 intersect Q_lambda=0
for every lambda.                                   (17)
```

Dimension makes `R intersect Q` a line.  Its nonzero representative has a
unique expression

```text
ell=a q_s+b q_t+c q_d,                  c!=0.       (18)
```

If `(a,b)!=(0,0)`, choose `lambda` with
`a lambda_s+b lambda_t=c`; then `ell in R intersect Q_lambda`, contrary to
(17).  Thus `ell` is proportional to `q_d` and

```text
q_d in R.                                           (19)
```

Repeating the argument with `P_0` gives `q_d in P_0`, contradicting the
first equality in (15).  Therefore the mixed profile (2) is impossible.
Root exchange proves the `(3,2,3)` mate.

## 3. Proof-topology consequence

Inside the joint-rank-four/rank-eight cell,

```text
third-row rank three:
  involved rows (2,2):              IMPOSSIBLE (S2BR/S2BX);
  involved rows (2,3)/(3,2):        IMPOSSIBLE (this theorem);
  involved rows (3,3):              OPEN;

at least one deficient involved row, q=3:           CLOSED.          (20)
```

The proof uses neither pair regularity nor any entry of the injective
involved row outside the two complementary colours.  It makes no inference
for third-row rank two, where the kernel of `pr_3|K` has an additional
non-syzygy direction and the correction need not collapse to one source
line.

## 4. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_rank_three_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_rank_three_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_rank_three_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_rank_three_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_rank_three_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_rank_three_complete_exclusion.py
```

The primary replay checks the one-row correction system, rank-three second
and third row restrictions, exact binary table, kernel shifts, and
four-space line trap with SymPy.  The independent no-import audit reverses
the abstract row order and reconstructs the correction, row ranks, all
binary entries, and every rational shift-support branch with standard-
library `Fraction` elimination.  S2BX supplies the already independently
audited `P_3` rank interface and S2BF supplies the exact binary-frame
incidence obstruction.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Same-colour third-row-rank-three exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_RANK_THREE_COMPLETE_EXCLUSION_THEOREM.md)
- [Intersecting-middle-plane binary obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md#2-a-binary-diagonal-frame-cannot-have-an-arbitrary-middle-intersection)

## Scope boundary

```text
rank-four/rank-eight one-deficient involved row, q=3: IMPOSSIBLE;
mixed (2,3,3)/(3,2,3) profiles:                      IMPOSSIBLE;
injective (3,3,3) profile:                           OPEN;
third-row-rank-two mixed/injective profiles:         OPEN;
other lower-rank cells / components / poles:         OPEN;
higher balanced orders / all-balanced rank-drop:     OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (21)
```
