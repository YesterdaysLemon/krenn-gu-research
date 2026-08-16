# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight same-missing-colour third-row-support-one nonaligned source atlas and pair-pole exclusion

## Status

**Exact characteristic-zero source classification and complete graph-extension
exclusion of the nonaligned chart in S2BT's support-one split-lift atlas.**
Retain the normalized, target-consistent physical `m=3` common-three-space
full-sensor hypotheses with singleton span dimension three, joint rank four,
all three root blocks nonzero, and shared-derivative rank eight.  Let `d,s,t`
be the distinct target colours for which the first and second rows have
common kernel `e_d^*` and the third row has kernel `e_s^*`.

S2BT proves that the remaining nonaligned chart has

```text
D(a,b,c)=(a tensor y-e_s tensor b) tensor w+C tensor c,

C=kappa e_d tensor e_d+C_bar,       kappa!=0,
e_s^*(w)!=0,                                         (1)

K=span(k_0,k_1,k_2,k_3),
k_0=(e_s,y,0),
k_1=(0,0,e_d),
k_2=(0,-e_s,0),
k_3=(a,0,e_t),                                      (2)

span(e_s,y)=span(e_s,a)=span(e_s,e_t).              (3)
```

Every physical empty-target solution on (1)--(3) is forced into one exact
same-source two-plane family.  After source permutation and nonzero
rescaling, its four dual `K` rows have the form

```text
g_0=(1/2) z_t,
g_1=r,                       r in Z^*, r not proportional z_t,
g_2=b(1/2)z_t-mu(x_t-y_t),
g_3=x_t+y_t+c,               c in Z^*, mu!=0,       (4)
```

and the root data reduce to

```text
y=b e_s+e_t,              a=e_t,
C=e_d tensor e_d,         w=e_s.                    (5)
```

The family (4)--(5) genuinely satisfies the complete singleton/empty target
incidence and has generic sensor rank four.  It is therefore a sharp local
control, not an empty cell.  Its unique rational pair lift, however, has an
unavoidable prime-divisor pole on `x_t=0` or `y_t=0`.  The exact
Cramer--Euler pair-pole gate consequently excludes every graph extension of
the nonaligned chart.

Together with S2BU, this closes the complete same-missing-colour `(2,2,2)`
cell with coordinate third-row kernel.  It does not treat a noncoordinate
third-row kernel, third-row rank three, mixed or injective involved rows,
joint rank three, derivative rank seven, other components and pole strata,
higher orders, or all-rank drop.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The eight root coefficients

Write

```text
y=y_s e_s+y_t e_t,             a=a_s e_s+a_t e_t,
y_t a_t!=0.                                             (6)
```

Let `g_0,g_1,g_2,g_3` be the images under the injective transpose
`H^*:K^*->W^*` of the basis dual to (2).  Define

```text
u=g_0,                v=g_3,
h=g_0+a_s g_3,        q=y_s g_0-g_2,
r=g_1.                                                   (7)
```

The root rows are

```text
r_s=h,             r_t=a_t v,             r_d=0,
p_s=q,             p_t=y_t u,             p_d=0,
q_d=r,             q_s=0,                 q_t=v.        (8)
```

The change from `(g_0,g_1,g_2,g_3)` to `(u,r,q,v)` is invertible, so

```text
u,r,q,v are linearly independent.                       (9)
```

Put `P` for the six-term polarized source permanent.  As in S2BU, the root
box

```text
L=span(e_s,e_t) tensor span(e_s,e_t)
  tensor span(e_d,e_t)                                  (10)
```

meets `U` only in zero for every `C_bar` and every `w` nonzero on `e_s`:
the `dd d`, `dd t`, and then `ss s` coefficients successively kill the
three generators of `U`.

Write `w=w_d e_d+w_s e_s+w_t e_t`, with `w_s!=0`, and
`C_bar=sum c_ij e_i tensor e_j`.  The target representatives in `L` are

```text
ddd  congruent -kappa^(-1) C_bar tensor e_d,
sss  congruent -(w_d/w_s)ssd-(w_t/w_s)sst,
ttt  represented by ttt.                              (11)
```

Comparing the eight root coordinates through (8), and suppressing only
nonzero scalars `a_t,y_t`, gives

```text
P(h,q,r)       in span(T_d,T_s),
P(h,u,r)       in span(T_d),
P(v,q,r)       in span(T_d),
P(v,u,r)       in span(T_d),                         (12)

P(h,q,v)       in span(T_s),
P(h,u,v)=0,
P(q,v,v)=0,
P(v,u,v)       in span(T_t)\{0}.                    (13)
```

The coefficients in (12) are respectively the `ss,st,ts,tt` entries of
`-kappa^(-1)C_bar`, with the `ss` coefficient also receiving the `w_d`
multiple of `T_s`.  The first line of (13) receives the `w_t` multiple of
`T_s`; its last line is exactly the nonzero `ttt` target.  Thus (12)--(13)
retain the complete target information needed below.

## 2. A deformed eight-product source atlas

### Lemma 1 (independent solutions have one same-source two-plane)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field, and
let `T_d,T_s,T_t` be three pure fully transverse tensors whose corresponding
factor lines are distinct in every source.  Suppose independent
`u,r,q,v in W` and a scalar `A` satisfy (12)--(13) with

```text
h=u+A v.                                             (14)
```

Then every tensor in (12) and the first tensor in (13) is zero, and, after
permuting sources and rescaling nonzero vectors,

```text
A=0,
u=z_t,
v=x_t+y_t+c,                 c in Z,
q=mu(x_t-y_t),               mu!=0,
r in Z,                      r not proportional z_t. (15)
```

#### Proof

The nonzero decomposable tensor `P(v,u,v)` shows that `v` uses at least two
source summands.

### 2.1 `v` uses exactly two sources

After permuting sources, write

```text
v=x+y,                    0!=x in X, 0!=y in Y.      (16)
```

The last equation in (13) makes the third component of `u` a nonzero vector
`z in Z`, and its target factor lines are `x,y,z`.  Write

```text
u=U_X+U_Y+z.                                        (17)
```

Expanding `P(u+A v,u,v)=0` and quotienting first by `x`, then by `y`, gives

```text
U_X=alpha x,             U_Y=beta y,
alpha+beta+A=0.                                      (18)
```

The equation `P(q,v,v)=0` first gives `q_Z=0`.  The tensor
`P(h,q,v)` contains two of the `t` factor lines, so it cannot be a nonzero
multiple of the fully transverse `T_s`; it vanishes.  Its `z` slice is

```text
q_X tensor y+x tensor q_Y=0,                        (19)
```

whence

```text
q=mu(x-y).                                          (20)
```

Independence makes `mu!=0`.

Every tensor in (12) likewise contains at least two `t` factor lines, so its
`T_d,T_s` coefficients and the tensor itself vanish.  From
`P(v,u,r)=0`, the off-line parts of `r_X,r_Y` vanish, and the off-line part
of `r_Z` vanishes unless `A=0`.  If `A!=0`, all four vectors lie in
`span(x,y,z)`, contradicting independence.  Thus `A=0` and `beta=-alpha`.

Now `h=u`.  The equation `P(u,u,r)=0` kills the off-line part of `r_Z`
unless `alpha=0`; that alternative again puts all four vectors in the same
three-space.  Hence `alpha=beta=0` and `u=z`.  The remaining equation
`P(v,u,r)=0` puts

```text
r_X=rho x,                 r_Y=-rho y.              (21)
```

Finally `P(u,q,r)=0` gives `2 mu rho=0`, so `rho=0` and `r in Z`.
Independence says `r` is not proportional to `z`.  This is (15) with
`c=0`.

### 2.2 `v` uses all three sources

Write

```text
v=x+y+z,                 xyz!=0.                    (22)
```

The tensor `P(u,v,v)` lies in the Segre tangent at `x tensor y tensor z`.
A nonzero decomposable tensor in that tangent shares at least two base
factor lines.  Permute sources so it has the form

```text
P(u,v,v)=xi tensor y tensor z.                      (23)
```

Then

```text
u=U_X+beta y+gamma z,
xi=U_X+(beta+gamma)x.                               (24)
```

First suppose `U_X` is not proportional to `x`.  Expanding
`P(u+A v,u,v)=0` in the independent lines `U_X,x` gives

```text
beta+gamma+A=0,
beta gamma+A(beta+gamma)=0.                         (25)
```

The equation `P(q,v,v)=0` puts

```text
q=q_x x+q_y y+q_z z,             q_x+q_y+q_z=0.     (26)
```

As before, `P(h,q,v)` cannot equal a nonzero `T_s` tensor.  Its
`U_X` coefficient first gives `q_x=0`; its remaining coefficient gives
`q_y(gamma-beta)=0`.  Independence makes `q_y!=0`, so `beta=gamma`.
Equations (25) then give `3 beta^2=0`, hence

```text
beta=gamma=A=0,
u=U_X,                 q=mu(y-z).                   (27)
```

Now suppose `U_X=alpha x`.  Then `u` is a scaling vector on the three base
lines.  If every component of `r` lies on those lines, independence already
fails.  If, say, `r_X` has an off-line part, the off-line coefficients of

```text
P(v,u,r)=P(v,q,r)=P(h,u,r)=0                       (28)
```

successively give

```text
beta+gamma=0,             q_x=0,             2 beta gamma=0. (29)
```

Thus `beta=gamma=0`; the scalar equation
`P(u+A v,u,v)=0` and nonzero `alpha` give `A=0`, while (26) gives
`q=mu(y-z)`.  The root-exchanged cases are identical.  Hence every
independent scaling case also reduces to (27).

It remains to determine `r` in (27).  The zero `P(v,u,r)=0` gives

```text
r_Y=rho y,                 r_Z=-rho z.              (30)
```

The zero `P(u,q,r)=0` then gives `2 mu rho=0`, so `r_Y=r_Z=0` and
`r in X`.  Independence makes `r` independent of `u`.  Relabel this
distinguished source as `Z`; the unused component `x` of `v` in that source
becomes the arbitrary `c in Z` in (15).  This proves the lemma.  QED.

## 3. Application to the root chart

Lemma 1 applies to (12)--(13) because (9) gives independence.  Every target
coefficient in (12), and the `T_s` coefficient in (13), therefore vanishes.
Reading those coefficients through (11) yields

```text
C_bar=0,                   w_d=w_t=0.                (31)
```

Normalize `kappa=1` and `w=e_s`.  The scalar `A` in Lemma 1 is the
`e_s` component of the first factor `a` in (6), after harmless nonzero
rescaling; hence `a=e_t`.  Normalize the `e_t` component of `y` to one and
write `y=b e_s+e_t`.  Finally normalize the nonzero source factors in (15)
so that `P(v,u,v)=T_t`.  This gives exactly (4)--(5), with

```text
u=(1/2)z_t,
v=x_t+y_t+c,
q=mu(x_t-y_t),

g_0=u,             g_1=r,             g_2=b u-q,
g_3=v.                                                   (32)
```

Conversely, direct expansion of (32) gives

```text
P(v,u,v)=T_t,

P(h,q,r)=P(h,u,r)=P(v,q,r)=P(v,u,r)=0,
P(h,q,v)=P(h,u,v)=P(q,v,v)=0,                        (33)
```

with `h=u`.  Hence the empty companion is exactly

```text
G_N=e_t tensor e_t tensor e_t T_t.                  (34)
```

The vectors in (32) are independent because `u,r` span a two-plane in `Z`
and the projections of `v,q` to `X direct-sum Y` are independent.  Thus the
family is an exact, generically full local empty-target control.

## 4. The unique pair lift has a divisor pole

In the basis

```text
U_1=D(k_1)=ddd,
U_2=D(k_2)=sss,
U_3=D(k_3)=b tss+tts+ddt,                           (35)
```

the three singleton columns obtained from `D H` are

```text
G_x=(0,-mu x_t,x_t),
G_y=(0, mu y_t,y_t),
G_z=(r,(b/2)z_t,c).                                 (36)
```

Their determinant is

```text
-2 mu x_t y_t r!=0,                                 (37)
```

so the balanced sensor has generic rank four after adjoining the empty
column.  By (34), the residual target in the `U_i` basis is

```text
J-G_N=(T_d,T_s,0).                                  (38)
```

Put `ell=(b/2)z_t`.  Solving the unique Cramer system

```text
G_x C_x+G_y C_y+G_z C_z=(T_d,T_s,0)                 (39)
```

gives

```text
C_z=T_d/r,

C_x=[-T_s+(ell-mu c)T_d/r]/(2 mu x_t),
C_y=[ T_s-(ell+mu c)T_d/r]/(2 mu y_t).              (40)
```

At the prime divisor `x_t=0`, all factors in the numerator of `C_x` are
independent of `x_t`.  Pair regularity would therefore force

```text
r T_s=(ell-mu c)T_d.                                (41)
```

Likewise regularity at `y_t=0` would force

```text
r T_s=(ell+mu c)T_d.                                (42)
```

Subtracting (41)--(42) gives `2 mu c T_d=0`, hence `c=0`.  The common
identity then becomes

```text
r T_s=ell T_d.                                      (43)
```

But the left side has the nonzero `x_s y_s` source monomial and the right
side has the `x_d y_d` source monomial.  They are distinct basis monomials,
so (43) is impossible.  At least one of `C_x,C_y` therefore has valuation
`-1` on its displayed coordinate divisor.

The pair-pole condition in the exact Cramer--Euler globalization theorem is
necessary for any fixed shore to come from one graph.  Equations (37)--(43)
show that every nonaligned empty-target control fails it.  Hence the complete
nonaligned chart has no graph extension.

## 5. Proof-topology consequence

Combining S2BT, S2BU, and this theorem gives

```text
same-colour (2,2,2), coordinate third-row kernel:
  nonsplit missing-colour lifts:                    IMPOSSIBLE;
  aligned split-lift chart:                        IMPOSSIBLE;
  nonaligned empty-target solutions:               EXACT ATLAS (4)--(5);
  regular pair lift for every atlas point:          IMPOSSIBLE;
  complete coordinate-third-kernel graph cell:     IMPOSSIBLE.       (44)
```

The exact controls (4)--(5) explain why S2BS's empty-target obstruction could
not simply extend to every nonaligned parameter.  They are not graphs and
not counterexamples.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_nonaligned_source_atlas_and_pair_pole_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_nonaligned_source_atlas_and_pair_pole_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_nonaligned_source_atlas_and_pair_pole_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_nonaligned_source_atlas_and_pair_pole_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_nonaligned_source_atlas_and_pair_pole_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_nonaligned_source_atlas_and_pair_pole_exclusion.py
```

The primary replay checks the two-/three-source normal-form identities,
reconstructs the exact root and source control, verifies every root
coefficient, singleton column, rank determinant, rational pair solution, and
two divisor residues with SymPy.  The independent no-import audit uses
reverse tensor indexing, standard-library `Fraction` elimination, and a
separate sparse-polynomial representation to rebuild the control, pair lift,
and incompatible residues.  Lemma 1 is the exhaustive proof.

## Dependencies

- [Support-one split-lift atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_SPLIT_LIFT_ATLAS_THEOREM.md)
- [Aligned split-lift exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_ALIGNED_SPLIT_LIFT_EXCLUSION_THEOREM.md)
- [Cramer--Euler pair-pole gate](BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md)

## Scope boundary

```text
rank-free deformed eight-product source atlas:               PROVED;
nonaligned support-one empty-target controls:                CLASSIFIED;
regular pair lift on the complete nonaligned chart:          IMPOSSIBLE;
coordinate-third-kernel same-colour (2,2,2) graph cell:      IMPOSSIBLE;
noncoordinate third-kernel / other rank-eight row profiles:  OPEN;
lower-rank target cells / other components and poles:        OPEN;
higher balanced orders / all-balanced rank-drop:             OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED. (45)
```
