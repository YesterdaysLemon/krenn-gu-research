# Balanced `m=3` common-three-space joint-rank-five support-one `(2,2)` complete exclusion

## Status

**Exact characteristic-zero exclusion of the last transverse
joint-rank-five support-one involved-row profile.**  Let `U` be the total
singleton span of a normalized, target-consistent physical `m=3` common
shore whose complete four-column sensor has full function-field rank.  Assume

```text
dim U=3,                         rank H=5.             (1)
```

Retain the transverse two-root branch of S2AG.  Thus the two nonzero
root--root blocks have disjoint derivative summands, the uninvolved third
root row has rank two, its one-dimensional kernel has target-coordinate
support exactly one, and both involved rows have rank two.  Then the physical
full-sensor conditions are inconsistent.

The two involved zero rows determine every coefficient of the singleton
correction.  Their missing colours must be distinct, and the relation
three-plane has one exact normal form.  The support-one colour is one of the
two missing colours.  In that normal form the complete target equation gives
a rank-one square onto the untouched third target and three mixed polarized
maps into the fully transverse plane spanned by the other two targets.  The
binary-diagonal-plane common-zero lemma of S2AK then kills the alternating
singleton determinant.

Together with the support-one higher-row-rank exclusion S2AL, this closes
the entire transverse two-root joint-rank-five branch.  This theorem does
**not** exclude the three Hilbert--Burch coordinate atlases, joint rank at
most four, another S2T/S2Q component type, a rank-one or pair-plane pole
stratum, a higher order, the all-rank-drop branch, or the global conjecture.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The two zero rows determine every correction

Use the transverse notation of S2AG.  After permuting roots,

```text
B_23=B!=0,                  B_13=C!=0,       B_12=0,

D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6.                                      (2)
```

There are a three-plane `P` and a two-plane `N_3` such that

```text
K=P direct-sum N_3,
P subset A_1 direct-sum A_2,
U=D_(B,C)(P).                                        (3)
```

Write the transposed root rows as

```text
rho:A_1^*->W^*,        pi:A_2^*->W^*,
theta:A_3^*->W^*,      W=X direct-sum Y direct-sum Z. (4)
```

The target-kernel argument for the two rank-two involved rows gives colours
`c,d` and nonzero scalars `kappa',kappa` with

```text
ker rho=span(e_c^*),       r_c=0,
C_(c,-)=kappa' e_c,

ker pi=span(e_d^*),        p_d=0,
B_(d,-)=kappa e_d.                                  (5)
```

Duality with `P` also gives

```text
pr_1(P) subset e_c^perp,              pr_2(P) subset e_d^perp. (6)
```

The restriction of `D_(B,C)` to `P` is injective.  Expand the complete
coefficientwise target identity in any basis of the three nonroot target
factors containing the three pure targets

```text
T_i=X_i tensor Y_i tensor Z_i.
```

For each coefficient tensor `E`, there is a unique
`w_E=(a_E,b_E) in P` whose singleton column supplies that coefficient.
Evaluate the identity on the complete root row with second coordinate `d`.
The all-cross permanent and every `C tensor b_E` term vanish by (5)--(6),
while `B_(d,-)=kappa e_d`.  Coefficientwise,

```text
a_E=-delta_(E,T_d) kappa^(-1)e_d.                   (7)
```

The complete root row with first coordinate `c` similarly gives

```text
b_E=-delta_(E,T_c) (kappa')^(-1)e_c.                (8)
```

If `c=d`, (7) contradicts the first containment in (6).  Hence

```text
c!=d.                                                (9)
```

Equations (7)--(9) give the only nonzero correction vectors:

```text
w_(T_d)=(-kappa^(-1)e_d,0),
w_(T_c)=(0,-(kappa')^(-1)e_c),
w_E=0 otherwise.                                   (10)
```

In particular, the full target equation is exactly

```text
G_N-J
 =-kappa^(-1)T_d D_(B,C)(e_d,0)
  -(kappa')^(-1)T_c D_(B,C)(0,e_c).                (11)
```

Let `j` be the third colour.  Both projections of `P` have dimension two.
The two vectors in (10), followed by subtraction in a third basis vector,
therefore put the whole relation plane in the normal form

```text
P=span{(e_d,0),(0,e_c),(e_j,tau e_j)},
tau!=0.                                             (12)
```

No entry of `B` or `C` outside the two forced rows in (5) has been
restricted.

## 2. The support colour is a missing involved colour

Relabel the support-one colour and rescale its kernel generator so that

```text
ker theta=span(e_2^*),                    q_2=0.     (13)
```

If `2` were different from both `c` and `d`, equations (7)--(8) would give
`w_(T_2)=0`.  The all-cross coefficient at the complete root row `(2,2,2)`
also vanishes by (13), leaving the nonzero target `T_2` with no correction.
Thus

```text
2 in {c,d}.                                         (14)
```

Exchange the two involved roots if necessary.  We may assume

```text
d=2,                     c in {0,1},
j={0,1,2}\{c,d}.                                    (15)
```

Choose row forms `v_d,v_c,v_j` dual to the ordered basis in (12).  The
involved rows are exactly

```text
r_d=v_d,              r_c=0,              r_j=v_j,
p_d=0,                p_c=v_c,            p_j=tau v_j. (16)
```

Put

```text
V=span(v_d,v_c,v_j),                    Q=image theta. (17)
```

The S2AG row-space splitting and `rank H=5` give

```text
dim V=3,                 dim Q=2,                 V intersect Q=0. (18)
```

## 3. The complete target table has one square and one diagonal plane

For `u,v,q in W^*`, write

```text
M_(u,v)(q)=per(u,v,q) in X^* tensor Y^* tensor Z^*. (19)
```

Let `B_(a,k)` and `C_(a,k)` denote the coordinate entries of the two
root--root blocks.  Evaluating (11) at every root row gives the single exact
formula

```text
M_(r_a,p_b)(q_k)-delta_(a,b,k)T_k
 =-kappa^(-1)delta_(a,d)B_(b,k)T_d
  -(kappa')^(-1)C_(a,k)delta_(b,c)T_c.              (20)
```

Use (16) in the four root pairs `(j,j)`, `(d,j)`, `(j,c)`, and `(d,c)`.
For every `k`, equation (20) becomes

```text
tau M_(v_j,v_j)(q_k)=delta_(k,j)T_j,

tau M_(v_d,v_j)(q_k)=-kappa^(-1)B_(j,k)T_d,

M_(v_j,v_c)(q_k)=-(kappa')^(-1)C_(j,k)T_c,

M_(v_d,v_c)(q_k)
 =-kappa^(-1)B_(c,k)T_d-(kappa')^(-1)C_(d,k)T_c.   (21)
```

Because `q_0,q_1` span `Q`, the first line of (21) is a nonzero rank-one
square map with image `span(T_j)`.  Put

```text
D_cd=span(T_d,T_c).                                 (22)
```

The other three lines of (21) say

```text
M_(v_d,v_j)(Q) subset D_cd,
M_(v_c,v_j)(Q) subset D_cd,
M_(v_d,v_c)(Q) subset D_cd.                         (23)
```

This table retains every unrestricted entry of `B` and `C`; only its target
planes are used.

## 4. The alternating singleton determinant vanishes

The three tensors `T_d,T_c,T_j` are pairwise fully transverse.  Equations
(18), (21), and (23) are therefore exactly the hypotheses of the
binary-diagonal-plane common-zero lemma in S2AK, with

```text
(u_0,u_1,v)=(v_d,v_c,v_j),
D_01=D_cd,                    T_2=T_j.               (24)
```

That exact two-source/three-source atlas gives

```text
Alt_XYZ(v_d,v_c,v_j)=0.                             (25)
```

On the other hand, the three vectors in (12) are a basis of `P`,
`D_(B,C)|_P` is injective, and `tau!=0`.  The generic determinant of the
three separately linear physical singleton columns is the tensor in (25),
up to the nonzero determinant of this basis change.  Full sensor rank
requires

```text
Alt_XYZ(v_d,v_c,v_j)!=0,                            (26)
```

a contradiction.  Therefore

```text
rank H=5, transverse derivative rank 6,
rank theta=2 with support-one kernel,
involved rows (2,2):                                IMPOSSIBLE.       (27)
```

No finite scan, numerical specialization, generic-point promotion, or
unproved exhaustion is used.

## 5. Proof-topology consequence

The transverse joint-rank-five two-root branch now has

```text
third-row kernel support two, every involved profile: IMPOSSIBLE (S2AI--S2AK);

third-row kernel support one,
  involved rows (3,3), (3,2), or (2,3):             IMPOSSIBLE (S2AL);
  involved rows (2,2):                              IMPOSSIBLE (here);

two-root transverse joint-rank-five branch:         IMPOSSIBLE;

three-root Hilbert--Burch coordinate atlases:        OPEN;
joint rank at most four / other physical branches:   OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (28)
```

The next exact joint-rank-five obligations are the `(1,2,2)`, `(1,1,2)`,
and `(1,1,1)` Hilbert--Burch coordinate atlases of S2AG.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_one_two_by_two_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_one_two_by_two_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_one_two_by_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_one_two_by_two_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_one_two_by_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_one_two_by_two_complete_exclusion.py
```

The primary replay checks all ordered missing-colour pairs, the zero-row
correction system, the relation-plane normal form, support-colour forcing,
the complete arbitrary-block target table, and the inherited two-/three-
source common-zero atlas.  The independent no-import audit reconstructs the
same correction and target tables with standard-library `Fraction` sparse
tensors and a different coordinate convention.  The scripts replay the
displayed identities; the arbitrary-vector and inherited case-exhaustion
arguments are the proof above.

## Dependencies

- [Joint-rank-five derivative and torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [Support-two `(3,3)` exclusion and binary-diagonal-plane lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_THREE_BY_THREE_EXCLUSION_THEOREM.md)
- [Support-one higher-row-rank exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
