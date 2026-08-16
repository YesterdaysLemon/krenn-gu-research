# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective-involved-rows third-row-rank-two complete exclusion

## Status

**Exact characteristic-zero exclusion of the complete `(3,3,2)` row-profile
cell in the joint-rank-four, derivative-rank-eight three-root chart.**  Retain
the normalized, target-consistent physical `m=3` common-three-space
full-sensor hypotheses with singleton span dimension three, joint rank four,
all three root blocks nonzero, and shared-derivative rank eight.  Suppose

```text
rank rho=rank pi=3,                   rank theta=2.   (1)
```

Let `eta` generate `ker theta` and put `Q_3=pr_3 K=ker eta`.  The proof has
two exact stages.

First, a nonzero vertical subspace `K intersect A_3` is incompatible with
the projection ranks.  A support-one `eta` forces one split tangent lift,
leaving the involved shore represented by that tangent factor with rank at
most two.  A support-two `eta` forces both complementary split lifts; with a
vertical vector and the shared syzygy they fill `K`, but both involved
projections have rank two.

Second, when `K` has no vertical vector, the physical root box

```text
A_1 tensor A_2 tensor Q_3                            (2)
```

meets the singleton span only in zero.  The full target identity therefore
has unique representatives `F_0,F_1,F_2` in this box and becomes

```text
G_N=T_0 F_0+T_1 F_1+T_2 F_2.                        (3)
```

If all three `F_i` were nonzero, one root evaluation would give a concise
three-term source diagonal, contradicting `tensor-rank(P_3)=4`.  Hence a
target colour in the support of `eta` has `F_i=0`.  Its correction either
forces the residual block `C` into the forbidden derivative tangent plane,
or has zero third component and makes `w` that coordinate.

For support one, the last alternative leaves an exact binary diagonal frame
whose first or second plane equals the third-row plane, contradicting the
intersecting-plane binary obstruction.  For support two, permanent symmetry
on that equal plane reduces the remaining root coefficient to

```text
q_d sym(a,c) tensor e_t+c tensor n tensor c.         (4)
```

The mixed-factor lemma forces `q_d=0`.  If `e_d,n` are independent, (4)
is again an equal-plane binary diagonal frame.  If they are proportional,
one two-plane carries two fully transverse rank-one squares with zero mixed
map, contradicting the exact two-square lemma.

Thus `(3,3,2)` is empty for both possible kernel supports.  Together with
S2BX--S2CA, the only row profile left in the rank-four/rank-eight cell is
the fully injective `(3,3,3)` profile.  Joint-rank-three/rank-eight cells,
derivative-rank-seven cells, other components and pole strata, higher orders,
and all-rank drop remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Vertical directions are incompatible with the row ranks

Use the S2BR derivative normal form

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
ker D=span((x,y,0)),                                 (5)

C notin A_1 tensor y+x tensor A_2.                  (6)
```

Put

```text
V_3=K intersect (0 direct-sum 0 direct-sum A_3).    (7)
```

Since both involved projections have rank three, `dim V_3<=1`: two
vertical vectors would leave only two dimensions of `K` to generate either
three-dimensional involved projection.

Contract the complete target identity by `eta`.  Because `eta` annihilates
every third component of `K` and `eta(w)!=0`, each supported target colour
`i` supplies a vector `(a_i,b_i,c_i) in K` with

```text
a_i tensor y-x tensor b_i proportional e_i tensor e_i. (8)
```

The S2BR tangent-factor atlas says that `x` or `y` represents every such
colour.  Modulo the syzygy in (5), equation (8) gives

```text
x proportional e_i  implies a split (0,e_i,c_i),
y proportional e_i  implies a split (e_i,0,c_i).    (9)
```

Assume `dim V_3=1`.

If `eta` has support one, use (9) and complete a basis of `K` by one further
vector.  When `x` represents the support colour, the first projection is
spanned by `x` and the first component of that one remaining vector; it has
dimension at most two.  When `y` represents the colour, the second projection
has dimension at most two.  Both contradict (1).

If `eta` has support two, its colours are represented by `x,y` in one order,
on distinct coordinate lines.  The two tangent tensors in (8) are
independent, so their split classes are independent modulo the syzygy and
`V_3`.  Those four classes fill `K`.  Each involved projection is then
spanned by only the two represented coordinate lines and has rank two,
again contradicting (1).  Therefore

```text
V_3=0.                                               (10)
```

## 2. The direct root box and the `P_3` rank fork

Let

```text
L=A_1 tensor A_2 tensor Q_3.                        (11)
```

Every root coefficient of `G_N` lies in `L`.  If `D(a,b,c) in L` for a
vector of `K`, contraction by `eta` gives

```text
eta(w)(a tensor y-x tensor b)=0.                    (12)
```

Subtracting the derivative syzygy leaves `(0,0,c) in K`.  Equation (10)
then gives `c=0`, so the original vector lies in `ker D`.  Hence

```text
U intersect L=0.                                    (13)
```

For a colour `i` outside `support eta`, `e_i in Q_3`; set

```text
F_i=e_i tensor e_i tensor e_i.                      (14)
```

For `i in support eta`, equation (8) supplies a derivative correction whose
`eta` contraction matches that of the target cube.  Subtract the uniquely
scaled derivative image and call the resulting element of `L` by `F_i`.
The complete coefficientwise target equation and (13) then give exactly
(3).  In particular every non-target source coefficient of `G_N` is zero.

Every `F_i` outside `support eta` is nonzero by (13).  Suppose all three
`F_i` were nonzero.  Their three trilinear root polynomials have a common
nonvanishing point over the infinite characteristic-zero field.  Evaluation
of (3) there gives

```text
lambda_0 T_0+lambda_1 T_1+lambda_2 T_2,
lambda_0 lambda_1 lambda_2!=0.                      (15)
```

All one-mode flattenings of (15) have rank three.  The three local maps from
`P_3` are therefore invertible, but they would send the rank-four tensor
`P_3` to the rank-three tensor (15).  This is the exact S2R rank
contradiction.  Thus

```text
F_i=0 for at least one i in support eta.             (16)
```

Choose such an `i` and a correction preimage `k_i=(a_i,b_i,c_i)`.  Up to
nonzero scalars, `F_i=0` says

```text
C tensor c_i
 =e_i tensor e_i tensor (lambda e_i-mu w),
lambda mu!=0.                                       (17)
```

If `c_i!=0`, the rightmost factor in (17) is nonzero and equality across the
`(A_1 tensor A_2)|A_3` split forces

```text
C proportional e_i tensor e_i.                     (18)
```

But the represented-colour conclusion in (8) puts (18) in
`A_1 tensor y+x tensor A_2`, contradicting (6).  Therefore

```text
c_i=0,                       w proportional e_i.    (19)
```

The kernel of `pr_3|K` is now the span of the derivative syzygy and the
split lift in (9).

## 3. Support one gives an equal-plane binary frame

Suppose `support eta={i}`.  Then (16) applies to this unique colour.  Let
`j,k` be the complementary colours.  Equations (3), (14), and (19) give

```text
G_N=T_j e_j tensor e_j tensor e_j
   +T_k e_k tensor e_k tensor e_k.                  (20)
```

Assume first that `x proportional e_i`; the other case is root-exchanged.
The two vectors spanning `ker(pr_3|K)` have first components on the one line
`e_i`.  Consequently the annihilators in `K^*` of

```text
R=span(r_j,r_k),                  Q=image theta      (21)
```

are the same two-plane `ker(pr_3|K)`, and hence

```text
R=Q.                                                  (22)
```

The second binary plane `P=span(p_j,p_k)` has dimension two because `pi`
is injective.  Equation (20) is the exact two-colour diagonal table on
`R,P,Q`.  Choose any three-space containing the equal planes `R=Q`; the
two-plane `P` meets it nontrivially in the four-dimensional joint row space.
The S2BF intersecting-middle-plane binary obstruction excludes this table.
If `y` represents `e_i`, the same argument gives `P=Q` and root exchange
applies.  Thus the support-one cell is empty.

## 4. Support two reduces to binary or two-square obstruction

Let `support eta={s,t}` and call the complementary colour `d`.  Up to
exchanging the first two roots and exchanging `s,t`, take the zero in (16)
to be `F_s` and normalize

```text
x=e_s,                  y=e_t,                  w=e_s. (23)
```

The split lift for `s` has zero third component.  Exactly as in (21)--(22),

```text
R=span(r_d,r_t)=Q=image theta.                      (24)
```

The other supported coefficient `F_t` is nonzero: a second zero would, by
(17)--(19), force `w` onto the distinct line `e_t`.

Let `Q_3=pr_3 K`.  Projection of a vector of `K` to its first component
modulo `e_s` induces an isomorphism

```text
A:Q_3 -> A_1/span(e_s).                             (25)
```

Choose the `T_t` correction so that its tangent part is
`e_t tensor e_t`; write its third component as `c`.  Then

```text
c!=0,                         A(c)=e_t.             (26)
```

Indeed `c=0` would put this correction in `ker(pr_3|K)`.  Modulo the
syzygy, that kernel has only the split `e_s tensor e_s` tangent image, so it
cannot also contain the independent `e_t tensor e_t` image.

The nonzero representative has the form, up to nonzero scalars,

```text
F_t=e_t tensor e_t tensor q-C tensor c,
0!=q in Q_3.                                        (27)
```

Identify the first and third copies of the common row plane in (24) by
`A`.  Permanent symmetry says that every source coefficient of (3) is
symmetric in those two factors.  The pure coefficient

```text
F_d=e_d tensor e_d tensor e_d                      (28)
```

first forces `A(e_d)` to be proportional to `e_d`.  Thus `e_d,c` is a basis
of `Q_3`.  Write

```text
q=q_d e_d+q_c c,
(A^(-1) tensor id)(C mod e_s tensor A_2)
  =e_d tensor m_d+c tensor m_c.                    (29)
```

Symmetry of (27) gives

```text
m_d proportional q_d e_t,                          (30)
```

with the fixed nonzero scale absorbed.  Hence, in the common outer-plane
coordinates,

```text
F_t=q_d(e_d tensor e_t tensor c+c tensor e_t tensor e_d)
    +c tensor n tensor c                            (31)
```

for one `n in A_2`.

Let `u,v` be the dual row basis of the common plane corresponding to
`e_d,c`.  On the full three-plane `image pi`, equation (28) makes

`M_(u,u)` a nonzero rank-one map onto `T_d`.  If `q_d!=0`, the cross map
`M_(u,v)` is a nonzero rank-one map onto the fully transverse `T_t`.
The S2AL mixed-factor-sharing lemma forbids this.  Therefore

```text
q_d=0,                     F_t=c tensor n tensor c,
n!=0.                                                (32)
```

If `e_d,n` are independent, take their dual middle rows.  Equations
(28),(32) give an exact binary diagonal table whose first and third planes
are the equal plane (24).  S2BF excludes it.

If `n` is proportional to `e_d`, choose one middle row nonzero on `e_d` and
one independent row annihilating `e_d`.  On their two-plane,

```text
M_(u,v)=0,
M_(u,u) and M_(v,v) are nonzero rank-one maps
onto the fully transverse lines T_d and T_t.         (33)
```

This is exactly the S2AL two-square obstruction.  Both alternatives are
impossible, completing the support-two exclusion.

## 5. Proof-topology consequence

Inside the joint-rank-four/rank-eight cell,

```text
at least one deficient involved row:                IMPOSSIBLE (S2BX--S2CA);
fully injective involved rows, third row rank two:  IMPOSSIBLE (this theorem);
fully injective involved rows, third row rank three: OPEN.             (34)
```

No pair-deck regularity is used.  The argument does not transfer without a
new incidence analysis to joint rank three, where the derivative syzygy is
not contained in `K`, or to derivative rank seven.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_involved_rows_third_row_rank_two_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_involved_rows_third_row_rank_two_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_involved_rows_third_row_rank_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_involved_rows_third_row_rank_two_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_involved_rows_third_row_rank_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_involved_rows_third_row_rank_two_complete_exclusion.py
```

The primary replay checks both vertical projection forks, exact derivative
and direct-box ranks, the three-representative rank fork, support-one plane
equality, the support-two symmetry reduction, and both terminal binary/two-
square tables with SymPy.  The independent no-import audit reverses tensor
indexing and uses separate `Fraction` elimination to reconstruct all colour
and root-exchange orientations.  The arbitrary-subspace arguments and the
already audited S2R, S2AL, and S2BF lemmas are the proof.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Order-three permanent rank obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [Tangent-line, mixed-factor, and two-square lemmas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
- [Intersecting-middle-plane binary obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md)

## Scope boundary

```text
fully injective involved rows, third-row rank two:  IMPOSSIBLE;
remaining rank-four/rank-eight profile (3,3,3):     OPEN;
other lower-rank cells / components / poles:        OPEN;
higher balanced orders / all-balanced rank-drop:    OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (35)
```
