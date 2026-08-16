# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight one-deficient-involved-row third-row-support-two complete exclusion

## Status

**Exact characteristic-zero exclusion of every joint-rank-four,
derivative-rank-eight row profile having a rank-two involved row and a
rank-two third row whose kernel uses two target colours.**  Retain the
normalized, target-consistent physical `m=3` common-three-space full-sensor
hypotheses with singleton span dimension three, joint rank four, all three
root blocks nonzero, and shared-derivative rank eight.  Up to exchanging the
first two roots, suppose

```text
rank rho=2,                  rank theta=2,
rank pi in {2,3},                                      (1)
```

and the generator of `ker theta` has support two.

The missing involved row fixes the third component of **every** singleton
correction preimage.  All source coefficients except `T_d` consequently
come from the two-dimensional kernel of `pr_3|K`.  Modulo the contained
derivative syzygy, their root corrections lie on one nonzero tensor line
`K R tensor w`.  The missing-colour correction also puts `e_d` in the third
projection, so the third-row kernel is supported on the complementary
colours `s,t`.  Contracting the complete target identity by that kernel
would make the same `R` proportional both to `e_s tensor e_s` and to
`e_t tensor e_t`.  Since both kernel coefficients are nonzero, this is
impossible.

The same-colour `(2,2,2)` support-two case was already closed by S2BW.  The
new content is the complete mixed `(2,3,2)` support-two cell and its
`(3,2,2)` root-exchanged mate.  Together with S2BY, all mixed profiles with
third-row rank three and all support-two mixed profiles with third-row rank
two are closed.  Support-one mixed profiles, injective involved rows,
joint-rank-three/rank-eight cells, derivative-rank-seven cells, other
components and pole strata, higher orders, and all-rank drop remain open.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. Correction preimages collapse to one line

Let `d` be the missing colour of `rho`.  S2BR gives

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
ker D=span((x,y,0)),                                 (2)

x_d=0,
(e_d^* tensor id)C=kappa e_d,       kappa!=0.       (3)
```

Put

```text
L=ker(pr_3|K).                                      (4)
```

Since `dim K=4` and `rank theta=dim pr_3 K=2`,

```text
dim L=2.                                            (5)
```

The derivative syzygy in (2) lies in `L`.  Choose

```text
h=(a,b,0) in L\ker D.                               (6)
```

Then

```text
U_0=D(h)=R tensor w,
R=a tensor y-x tensor b !=0.                        (7)
```

The restriction of `D` to `L` has kernel exactly the syzygy line, hence

```text
D(L)=span(U_0).                                     (8)
```

Expand the complete target identity coefficientwise in any source tensor
basis containing `T_d,T_s,T_t`.  For a source coefficient `E`, choose a
preimage `(a_E,b_E,c_E) in K` of its root correction.  First-`d`
contraction kills the corresponding coefficient of `G_N` and gives

```text
kappa e_d tensor c_E
 =-delta_(E,T_d)e_d tensor e_d.                     (9)
```

Therefore

```text
c_E=-delta_(E,T_d)kappa^(-1)e_d.                   (10)
```

In particular, every correction with `E!=T_d` has its preimage in `L` and
therefore lies on the one root-tensor line (8).  Choose any `v_d in K` with
third component `e_d`, and put `U_d=D(v_d)`.  The possible `U_0` part of the
`T_d` preimage can be absorbed into one source tensor `S`.  The complete
identity has the exact form

```text
G_N-J=-kappa^(-1)T_d U_d+S U_0.                    (11)
```

Equation (10) also proves `e_d in pr_3 K`.  If `eta` spans `ker theta`, then

```text
eta_d=0.                                            (12)
```

By the support-two hypothesis, after naming the complementary colours,

```text
eta=eta_s e_s^*+eta_t e_t^*,
eta_s eta_t eta(w)!=0.                              (13)
```

The nonzero evaluation on `w` is the exact S2BR third-row-kernel conclusion.

## 2. The third contraction forces two different lines

Contract (11) in the third root by `eta`.  The left empty permanent
vanishes because `q_eta=0`.  Equation (12) removes the `C tensor e_d` part
of `U_d`.  Write

```text
R_d=a_d tensor y-x tensor b_d                       (14)
```

for the tangent part of the chosen lift `v_d`.  Equations (7), (11), and
(13) give, up to the fixed sign convention,

```text
eta(w) S R
 =-eta_s T_s e_s tensor e_s
  -eta_t T_t e_t tensor e_t
  +kappa^(-1)eta(w)T_d R_d.                         (15)
```

Compare the independent source-tensor coefficient `T_s`.  If `sigma_s` is
the `T_s` coefficient of `S`, then

```text
eta(w) sigma_s R=-eta_s e_s tensor e_s.             (16)
```

The right side is nonzero, so `sigma_s!=0` and

```text
R proportional e_s tensor e_s.                     (17)
```

The `T_t` coefficient likewise gives

```text
R proportional e_t tensor e_t.                     (18)
```

But the two displayed coordinate tensors are linearly independent, while
`R!=0` by (7).  This contradiction proves the exclusion.  No entry of the
second involved row and no pair-deck regularity is used.

## 3. Proof-topology consequence

Inside the rank-four/rank-eight cell,

```text
at least one deficient involved row:
  third row rank three:                 IMPOSSIBLE (S2BY);
  third row rank two, support two:      IMPOSSIBLE (this theorem);
  third row rank two, support one:
    same-colour involved rows:          IMPOSSIBLE (S2BU/S2BV);
    mixed involved rows:                OPEN;

fully injective involved rows:          OPEN.                     (19)
```

The remaining mixed branch is therefore the discrete support-one third-row
kernel cell.  This theorem does not claim that its correction line has the
support-two form (15).

## 4. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_two_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_two_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_two_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_two_complete_exclusion.py
```

The primary replay checks the first-contraction affine system, the
two-dimensional third-projection kernel and one-dimensional derivative
image, the support-two third contraction, and the two incompatible
coordinate lines with SymPy.  The independent no-import audit reverses
tensor indexing and reconstructs the correction line, exact ranks, both
source-coefficient equations, and all colour permutations with standard-
library `Fraction` arithmetic.  The arbitrary-coefficient comparison above
is the proof.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Same-colour support-two exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [Mixed injective-third-row exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_ONE_DEFICIENT_INVOLVED_ROW_THIRD_ROW_RANK_THREE_COMPLETE_EXCLUSION_THEOREM.md)

## Scope boundary

```text
one deficient involved row, third-kernel support two: IMPOSSIBLE;
mixed (2,3,2)/(3,2,2) support-two cells:              IMPOSSIBLE;
mixed support-one / injective involved-row cells:     OPEN;
other lower-rank cells / components / poles:          OPEN;
higher balanced orders / all-balanced rank-drop:      OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.     (20)
```
