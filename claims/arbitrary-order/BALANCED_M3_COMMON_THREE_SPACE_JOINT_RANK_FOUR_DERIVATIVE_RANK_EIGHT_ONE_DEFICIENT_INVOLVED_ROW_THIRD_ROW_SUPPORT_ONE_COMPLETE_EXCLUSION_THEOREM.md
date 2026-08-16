# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight one-deficient-involved-row third-row-support-one complete exclusion

## Status

**Exact characteristic-zero exclusion of every joint-rank-four,
derivative-rank-eight row profile having exactly one deficient involved row
and a rank-two third row whose kernel is one target coordinate.**  Retain the
normalized, target-consistent physical `m=3` common-three-space full-sensor
hypotheses with singleton span dimension three, joint rank four, all three
root blocks nonzero, and shared-derivative rank eight.  Up to exchanging the
first two roots, suppose

```text
rank rho=2,                 rank pi=3,
rank theta=2,               ker theta=span(e_s^*).       (1)
```

Let `d` be the missing colour of `rho` and `t` the third colour.  The
missing-colour target first forces the vertical lift `(0,0,e_d) in K`.  The
`T_s` target forces one split tangent lift.  The alternative split on the
first involved root would make `rank pi<=2`, so only the second-root split
can occur.  This gives one exact four-space normal form and a twelve-entry
root box disjoint from the singleton span.

Four coefficients in the third-`t` face then force two independent second
rows to span a resonant pair `u,v` satisfying

```text
P(u,u,v)=P(u,v,v)=0,             P(v,v,v) proportional T_t !=0. (2)
```

Thus, on the three source factor lines of `T_t`,

```text
v=x+y+z,
u=alpha x+beta y+gamma z,
alpha+beta+gamma=alpha beta+alpha gamma+beta gamma=0.   (3)
```

All three scalars are nonzero.  The two missing-colour coefficients put
both `P(v,u,r)` and `P(u,u,r)` in the line of the fully transverse `T_d`.
They also lie in the Segre tangent space at `T_t`, so both vanish.  The two
resulting scalar equations have common kernel exactly `span((1,1,1))`;
hence `r` is proportional to `v`.  But `r` and `v` are images of distinct
dual basis vectors under the injective physical transpose.  This is the
contradiction.

Together with S2BZ and S2BY, this closes every rank-four/rank-eight profile
having at least one deficient involved row.  Fully injective involved rows,
joint-rank-three/rank-eight cells, derivative-rank-seven cells, other
components and pole strata, higher orders, and all-rank drop remain open.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The vertical and split lifts

Use the S2BR normal form

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
ker D=span((x,y,0)),                                  (4)

x_d=0,
(e_d^* tensor id)C=kappa e_d,       kappa!=0.        (5)
```

Because the `T_d` correction has first-row contraction
`-e_d tensor e_d`, any preimage `(a_d,b_d,c_d) in K` satisfies

```text
c_d=-kappa^(-1)e_d.                                  (6)
```

The third-row kernel annihilates `pr_3 K`.  In particular, (6) gives
`s!=d`.  Contract the same correction by `e_s^*`.  Its target contribution
is zero, while `e_s^*(w)!=0` by S2BR, so

```text
a_d tensor y-x tensor b_d=0.                         (7)
```

The kernel of the tangent map in (7) is
`span((x,y))`.  Subtracting the derivative syzygy and rescaling proves

```text
(0,0,e_d) in K.                                     (8)
```

For the `T_s` correction, first-`d` contraction gives `c_s=0`, while
third-`s` contraction gives

```text
e_s^*(w)(a_s tensor y-x tensor b_s)
  =-e_s tensor e_s.                                  (9)
```

The S2BR tangent-factor atlas says `x` or `y` is proportional to `e_s`.
Equation (9), modulo the syzygy, sharpens the two alternatives to

```text
x proportional e_s  implies (0,e_s,0) in K,
y proportional e_s  implies (e_s,0,0) in K.         (10)
```

If the second alternative held, the four-space `K` would be spanned by the
syzygy, `(e_s,0,0)`, `(0,0,e_d)`, and one vector over the remaining third
coordinate `e_t`.  Its second projection would be spanned by only `e_s` and
the second component of that last vector, and would have dimension at most
two.  This contradicts `rank pi=3`.  Therefore normalize

```text
x=e_s,                    (0,-e_s,0) in K.          (11)
```

## 2. The mixed four-space and its direct root box

The projection ranks in (1), together with (8) and (11), give the exact
basis

```text
k_0=(e_s,y,0),
k_1=(0,0,e_d),
k_2=(0,-e_s,0),
k_3=(lambda e_t,b,e_t),             lambda!=0,       (12)

span(e_s,y,b)=A_2.                                    (13)
```

Indeed, subtracting a multiple of `k_0` removes the `e_s` component of the
first entry of the fourth lift.  Its `e_t` component is nonzero because the
first projection has rank two.  Condition (13) is exactly the injectivity of
the second root row.

Put

```text
L=span(e_s,e_t) tensor A_2 tensor span(e_d,e_t).     (14)
```

Every root coefficient of the physical empty permanent lies in `L`.  Write

```text
C=kappa e_d tensor e_d+C_bar,
C_bar in span(e_s,e_t) tensor A_2.                   (15)
```

The three nonzero derivative images of (12) are

```text
D(k_1)=C tensor e_d,
D(k_2)=e_s tensor e_s tensor w,
D(k_3)=(lambda e_t tensor y-e_s tensor b) tensor w
       +C tensor e_t.                                (16)
```

A linear combination of (16) lying in `L` has successively zero
coefficients on `e_d e_d e_d`, `e_d e_d e_t`, and `e_s e_s e_s`.
The corresponding three combination coefficients vanish because
`kappa e_s^*(w)!=0`.  Hence

```text
U intersect L=0.                                    (17)
```

Writing `w=w_d e_d+w_s e_s+w_t e_t`, with `w_s!=0`, the three target
diagonals therefore have the unique representatives in `L`

```text
ddd congruent -kappa^(-1) C_bar tensor e_d,
sss congruent -(w_d/w_s)ssd-(w_t/w_s)sst,
ttt represented by ttt.                             (18)
```

No coordinate assumption on `w`, monomial assumption on `C`, or pair-deck
regularity enters (17)--(18).

## 3. Four third-`t` coefficients force resonance

Let `g_0,g_1,g_2,g_3 in W^*` be the images under the injective transpose
`H^*:K^*->W^*` of the basis dual to (12), and put

```text
u=g_0,                    r=g_1,                    v=g_3. (19)
```

These vectors, together with `g_2`, are independent.  The root rows are

```text
r_s=u,                    r_t=lambda v,             r_d=0,
p_i=y_i u-delta_(i,s)g_2+b_i v,
q_d=r,                    q_s=0,                    q_t=v. (20)
```

Since the second row has rank three, its `d,t` rows

```text
p_d=y_d u+b_d v,          p_t=y_t u+b_t v           (21)
```

are independent.  Equivalently,

```text
Delta=y_d b_t-y_t b_d!=0.                            (22)
```

Let `P` denote the six-term polarized permanent on the source direct sum.
The `sdt`, `stt`, `tdt`, and `ttt` coefficients of (18) give

```text
P(u,p_d,v)=0,               P(u,p_t,v)=0,
P(v,p_d,v)=0,               lambda P(v,p_t,v)=T_t. (23)
```

The first two equations and (22) imply

```text
P(u,u,v)=P(u,v,v)=0.                                (24)
```

The last two then imply

```text
b_d=0,               b_t!=0,               y_d!=0,
P(v,v,v)=(lambda b_t)^(-1)T_t!=0,
p_d=y_d u.                                           (25)
```

Write the three nonzero source components of `v` as `x,y,z`.  The pure
tensor identity in (25) identifies their factor lines with those of `T_t`.
The square-polarization kernel used in S2BU and (24) now give

```text
v=x+y+z,
u=alpha x+beta y+gamma z,
alpha+beta+gamma=0.                                  (26)
```

Expanding the other equation in (24) gives

```text
alpha beta+alpha gamma+beta gamma=0.                 (27)
```

None of `alpha,beta,gamma` is zero: if one vanished, (26)--(27) would make
all three vanish.  This is the exact cubic resonance frame.  No primitive
cube root is adjoined or chosen by the proof.

## 4. The missing-colour face collapses two dual rows

The `sdd` and `tdd` coefficients of (18), using (25), say

```text
P(u,u,r) in span(T_d),
P(v,u,r) in span(T_d).                              (28)
```

Both tensors on the left lie in the Segre tangent space at
`x tensor y tensor z`: every term has two of the three `t` factor lines.
The target `T_d` has a different factor line in every source.  Quotienting
all three source factors by the `t` lines shows

```text
span(T_d) intersect T_(x tensor y tensor z)=0.       (29)
```

Thus both tensors in (28) vanish.

Write `r=r_X+r_Y+r_Z`.  The off-line parts of `P(v,u,r)=0` have respective
nonzero coefficients

```text
beta+gamma=-alpha,
alpha+gamma=-beta,
alpha+beta=-gamma.                                  (30)
```

Hence `r_X,r_Y,r_Z` lie on the lines `x,y,z`; write

```text
r=r_x x+r_y y+r_z z.                                (31)
```

The two zero tensors in (28) reduce to

```text
alpha r_x+beta r_y+gamma r_z=0,
beta gamma r_x+alpha gamma r_y+alpha beta r_z=0.    (32)
```

The vector `(1,1,1)` lies in their common kernel by (26)--(27).  The two
rows in (32) are independent.  For if their first two-column minor vanished,

```text
gamma(alpha^2-beta^2)=0.                            (33)
```

Since `gamma!=0`, either `alpha=-beta`, forcing `gamma=0` in (26), or
`alpha=beta`, forcing `gamma=-2alpha` and then
`-3alpha^2=0` in (27).  Both contradict characteristic zero and the
nonzero coefficients.  Therefore the common kernel of (32) is exactly
`span((1,1,1))`, and

```text
r proportional v.                                  (34)
```

But `r=g_1` and `v=g_3` are images of distinct basis vectors under the
injective map `H^*`; they are independent.  This contradicts (34) and
excludes the mixed `(2,3,2)` support-one cell.  Exchanging the first two
roots excludes `(3,2,2)`.

## 5. Proof-topology consequence

Inside the rank-four/rank-eight cell,

```text
at least one deficient involved row:
  third row rank three:                 IMPOSSIBLE (S2BY);
  third row rank two, support two:      IMPOSSIBLE (S2BZ);
  third row rank two, support one:
    same-colour involved rows:          IMPOSSIBLE (S2BU/S2BV);
    mixed involved rows:                IMPOSSIBLE (this theorem);

fully injective involved rows:          OPEN.                     (35)
```

The theorem is an empty-target exclusion, stronger than a pair-pole
obstruction.  It does not transfer without proof to joint rank three, where
the shared derivative syzygy is not contained in `K`, or to derivative rank
seven.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_one_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_one_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_one_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_one_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_one_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_one_deficient_involved_row_third_row_support_one_complete_exclusion.py
```

The primary replay checks the mixed four-space, derivative and projection
ranks, direct root quotient, root-row elimination, exact cubic resonance,
Segre-tangent separation, and one-dimensional common kernel with SymPy.  The
independent no-import audit uses a custom exact `Q(omega)` implementation,
reverse tensor indexing, separate Gaussian elimination, and all six colour
permutations to reconstruct the resonance and dual-row collapse.  The
arbitrary-covector and field-theoretic arguments above are the proof.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [One-deficient-row support-two exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_ONE_DEFICIENT_INVOLVED_ROW_THIRD_ROW_SUPPORT_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [Aligned split-lift Segre-tangent lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_ALIGNED_SPLIT_LIFT_EXCLUSION_THEOREM.md)

## Scope boundary

```text
mixed (2,3,2)/(3,2,2), support-one third kernel:    IMPOSSIBLE;
every profile with a deficient involved row:         IMPOSSIBLE;
fully injective involved-row rank-four/rank-eight:   OPEN;
other lower-rank cells / components / poles:         OPEN;
higher balanced orders / all-balanced rank-drop:     OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.     (36)
```
