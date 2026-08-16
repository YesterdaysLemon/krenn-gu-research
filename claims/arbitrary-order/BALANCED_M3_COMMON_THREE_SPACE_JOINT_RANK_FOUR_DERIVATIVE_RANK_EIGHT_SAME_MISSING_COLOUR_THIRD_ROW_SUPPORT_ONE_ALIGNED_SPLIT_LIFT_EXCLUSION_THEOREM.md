# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight same-missing-colour third-row-support-one aligned split-lift exclusion

## Status

**Exact characteristic-zero exclusion of the complete aligned chart in the
S2BT support-one split-lift atlas.**  Retain the normalized,
target-consistent physical `m=3` common-three-space full-sensor hypotheses
with singleton span dimension three, joint rank four, all three root blocks
nonzero, and shared-derivative rank eight.  Let `d,s,t` be the distinct
target colours for which the first and second rows have common kernel
`e_d^*` and the third row has kernel `e_s^*`.

S2BT proves that the aligned chart has, after first/second root exchange and
nonzero rescaling, the exact form

```text
D(a,b,c)=(a tensor lambda e_s-e_s tensor b) tensor w+C tensor c,

C=kappa e_d tensor e_d+C_bar,       kappa!=0,
e_s^*(w)!=0,                                         (1)

K=span(k_0,k_1,k_2,k_3),
k_0=(e_s,lambda e_s,0),
k_1=(0,0,e_d),
k_2=(0,-e_s,0),
k_3=(alpha e_t,beta e_t,e_t),

lambda alpha beta!=0.                               (2)
```

No physical cross map onto this `K` can satisfy the complete empty-target
congruence.  The proof uses only four root coefficients.  The `ttt`
coefficient makes the fourth dual row fully supported.  The zero `stt` and
`tst` coefficients put two other dual rows in the two-dimensional kernel of
its Segre-tangent map.  The `ttd` coefficient lies in that tangent space but
would have to equal a multiple of the fully transverse `d` target, forcing
the final dual row into the same kernel.  Four dual rows then span at most
three dimensions, contradicting surjectivity of the physical cross map.

This excludes every value of `lambda,alpha,beta`, every complementary block
`C_bar` including zero, and every `w` with `e_s^*(w)!=0`; in particular it
includes the monomial-`C`, possibly noncoordinate-`w` branch.  The
nonaligned S2BT chart remains open away from the S2BS specialization, as do
other row profiles and all wider obligations.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. The root box is direct for arbitrary `w`

Put

```text
S=span(e_s,e_t),              T=span(e_d,e_t),
L=S tensor S tensor T.                                (3)
```

Every root coefficient of the physical empty permanent lies in `L`, because
the three projections of `K` are `S,S,T`.  The three nonzero derivative
images of the basis (2) are

```text
D(k_1)=C tensor e_d,
D(k_2)=e_s tensor e_s tensor w,
D(k_3)=(lambda alpha e_t tensor e_s
        -beta e_s tensor e_t) tensor w+C tensor e_t. (4)
```

They span `U`.  Suppose a linear combination of (4) lies in `L`.  Its
`e_d tensor e_d tensor e_d` coefficient first kills the coefficient of
`D(k_1)`.  Its `e_d tensor e_d tensor e_t` coefficient then kills that of
`D(k_3)`.  The remaining multiple of `D(k_2)` has nonzero
`e_s tensor e_s tensor e_s` coefficient because `e_s^*(w)!=0`, so it also
vanishes.  Hence

```text
U intersect L=0.                                    (5)
```

Write

```text
w=w_d e_d+w_s e_s+w_t e_t,          w_s!=0,
C_bar=sum_(i,j in {s,t}) c_ij e_i tensor e_j.       (6)
```

The three target diagonals have the unique representatives in `L`

```text
e_d e_d e_d  congruent -kappa^(-1) C_bar tensor e_d,

e_s e_s e_s  congruent
  -(w_d/w_s)e_s e_s e_d-(w_t/w_s)e_s e_s e_t,

e_t e_t e_t  represented by e_t e_t e_t.           (7)
```

The first relation is `D(k_1)=0` modulo `U`; the second is `D(k_2)=0`.
Uniqueness follows from (5).  Thus coefficient comparison inside `L` is
valid even when `C_bar=0` and `w` is noncoordinate.

## 2. Four forced source-permanent equations

Let `g_0,g_1,g_2,g_3 in W^*` be the images under the injective transpose
`H^*:K^*->W^*` of the basis dual to (2).  The root rows are read directly
from the three projections of the `k_i`:

```text
r_s=g_0,                  r_t=alpha g_3,       r_d=0,
p_s=lambda g_0-g_2,       p_t=beta g_3,        p_d=0,
q_d=g_1,                  q_s=0,               q_t=g_3. (8)
```

For source vectors `u,v,z`, write `P(u,v,z)` for their six-term polarized
permanent in `X^* tensor Y^* tensor Z^*`.  The root coefficient `ijt` of the
physical empty permanent is `P(r_i,p_j,q_t)`.

The representatives (7) have no `stt` or `tst` coefficient, while their
`ttt` coefficient is exactly the physical target `T_t`.  Therefore (8)
gives

```text
beta P(g_0,g_3,g_3)=0,                              (9)

alpha lambda P(g_0,g_3,g_3)
  -alpha P(g_2,g_3,g_3)=0,                         (10)

alpha beta P(g_3,g_3,g_3)=T_t.                    (11)
```

The `ttd` coefficient receives only the `c_tt` part of the first relation
in (7); the `s` target representative has first two factors `ss`.  Hence

```text
alpha beta P(g_1,g_3,g_3)
  =-kappa^(-1)c_tt T_d.                            (12)
```

All displayed scalars except possibly `c_tt` are nonzero.

## 3. The Segre-tangent kernel

### Lemma 1 (square-polarization kernel)

Let `V=X direct-sum Y direct-sum Z` over a characteristic-zero field, and
let `v in V` satisfy

```text
P(v,v,v)=T!=0,                                     (13)
```

where `T` is decomposable and fully transverse.  Then the map

```text
Phi_v:V->X tensor Y tensor Z,       h |-> P(h,v,v) (14)
```

has a two-dimensional kernel.  Its image is the affine tangent space to the
Segre cone at `T`.  If `T'` is a pure tensor whose three factor lines all
differ from those of `T`, then

```text
span(T') intersect image(Phi_v)=0.                 (15)
```

#### Proof

Write `v=x+y+z` by source summands.  Equation (13) is

```text
6 x tensor y tensor z=T,                           (16)
```

so `x,y,z` are all nonzero and give the three factor lines of `T`.  For
`h=h_X+h_Y+h_Z`,

```text
Phi_v(h)=2(h_X tensor y tensor z
             +x tensor h_Y tensor z
             +x tensor y tensor h_Z).              (17)
```

Successively quotienting by the lines `x,y,z` shows that (17) vanishes only
when

```text
h_X=a x,             h_Y=b y,             h_Z=c z,
a+b+c=0.                                             (18)
```

This is a two-dimensional kernel.  Formula (17) is exactly the Segre tangent
space.  Quotient all three tensor factors by `x,y,z`: every tensor in (17)
maps to zero, whereas `T'` maps to a nonzero pure tensor because all three
of its factor lines differ.  This proves (15).  QED.

## 4. Exclusion of the aligned chart

Apply Lemma 1 with

```text
v=g_3,                 T=(alpha beta)^(-1)T_t.       (19)
```

Equation (11) supplies (13).  Since `beta,alpha` are nonzero, (9)--(10)
give

```text
g_0,g_2 in ker Phi_(g_3).                           (20)
```

The target tensors `T_d` and `T_t` have three distinct factor lines.
Equation (12) lies in `image Phi_(g_3)` on the left and on `span(T_d)` on
the right.  Lemma 1 therefore forces both sides to vanish, so

```text
c_tt=0,                g_1 in ker Phi_(g_3).        (21)
```

The three vectors `g_0,g_1,g_2` lie in one two-dimensional kernel, and
`g_3` adds at most one dimension.  Thus

```text
dim span(g_0,g_1,g_2,g_3)<=3.                       (22)
```

But `H:W->K` is onto, so `H^*:K^*->W^*` is injective and the four images of
a basis of `K^*` must be independent.  This contradicts (22).  The aligned
chart (1)--(2) is empty.

## 5. Proof-topology consequence

Combining S2BT and this theorem gives

```text
same-colour (2,2,2), coordinate third-row kernel:
  nonsplit missing-colour lifts:                    IMPOSSIBLE;
  aligned split-lift chart y proportional e_s:     IMPOSSIBLE;
  nonaligned split-lift chart:
    S2BS coordinate specialization:                 IMPOSSIBLE;
    remaining directions / C_bar / w parameters:   OPEN.             (23)
```

No pair-deck regularity, numerical search, generic specialization, or
finite-field inference enters the exclusion.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_aligned_split_lift_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_aligned_split_lift_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_aligned_split_lift_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_aligned_split_lift_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_aligned_split_lift_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_aligned_split_lift_exclusion.py
```

The primary replay checks the arbitrary-`w` direct quotient on exact
fixtures, reconstructs the four root-row coefficients, and verifies the
Segre-tangent image, kernel, and transverse target separation with SymPy.
The independent no-import audit reverses tensor indexing and rebuilds the
root quotient, row coefficients, tangent matrix, kernel rank, and target
separation with standard-library `Fraction` arithmetic.  Lemma 1 and the
coefficient comparison above are the proof.

## Dependencies

- [Support-one split-lift atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_SPLIT_LIFT_ATLAS_THEOREM.md)
- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)

## Scope boundary

```text
rank-free square-polarization tangent-kernel lemma:          PROVED;
complete aligned support-one split-lift chart:               IMPOSSIBLE;
remaining nonaligned support-one chart:                      OPEN;
other rank-eight row profiles / lower-rank target cells:     OPEN;
pair coupling / other components and poles:                  OPEN;
higher balanced orders / all-balanced rank-drop:             OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED. (24)
```
