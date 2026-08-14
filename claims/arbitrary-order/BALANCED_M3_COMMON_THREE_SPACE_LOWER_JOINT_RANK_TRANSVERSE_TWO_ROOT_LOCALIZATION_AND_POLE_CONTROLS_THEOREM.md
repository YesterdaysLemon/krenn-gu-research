# Balanced `m=3` common-three-space lower-joint-rank transverse two-root localization and pole controls

## Status

**Exact characteristic-zero localization of every joint-rank-three or
joint-rank-four point in the transverse two-root-block part of the normalized,
target-consistent physical `m=3` common-three-space full-sensor stratum, plus
exact physical controls populating two of the resulting cells.**  Let `U` be
the total singleton span, put `K=image H`, and assume

```text
dim U=3,                    rank H=r in {3,4}.          (1)
```

Suppose exactly two root--root blocks are nonzero.  S2AG's rank-free
shared-factor exclusion makes their derivative transverse of rank six.  If
`q` is the rank of the uninvolved third-root row, then

```text
q in {1,2}.                                             (2)
```

Let `V` be the joint row space of the two involved roots and `Q` the row
space of the uninvolved root.  The four exact incidence types are

```text
(r,q)=(3,1): Q subset V;          (r,q)=(3,2): Q subset V;
(r,q)=(4,1): V intersect Q=0;     (r,q)=(4,2): dim(V intersect Q)=1. (3)
```

Every vector in the kernel of the uninvolved row has target-coordinate
support at most two.  Consequently, when `q=1` that kernel is one coordinate
plane.  If its missing colour is `s` and `{s,t,u}` are the three colours,
then, after exchanging the two involved roots if needed, the root blocks and
their three-dimensional preimage plane have the exact form

```text
B_23=lambda e_(2,t) tensor e_(3,t),
B_13=mu     e_(1,u) tensor e_(3,u),                   (4)

P=pr_(1,2)K
 =span{(e_t,0),(0,e_u),(e_s,tau e_s)},
lambda mu tau!=0.                                    (5)
```

After harmless row rescaling, the only surviving root-3 permanent cell is

```text
per(v,v,q_s)=T_s,
per(a,v,q_s)=per(v,b,q_s)=per(a,b,q_s)=0,             (6)
```

where `a=r_t`, `b=p_u`, and `r_s,p_s` are nonzero proportional copies of
`v`.  The rows `r_u,p_t,q_t,q_u` vanish.  At rank three `q_s` lies in
`span(a,b,v)`; at rank four it is independent of that three-plane.

Both alternatives in the last sentence are genuinely populated by exact
physical common-shore sensors.  The controls in Section 5 have full sensor
rank four over the function field, satisfy every singleton and empty
matching formula, and satisfy the complete GHZ target incidence.  Their
unique pair lifts have explicit coordinate-divisor poles, so they are not
six-vertex graphs and are not counterexamples.  They prove that lower joint
rank cannot be eliminated from the current local incidence equations alone.

This is a localization and sharpness theorem, not a lower-rank exclusion.
The `q=2` cells, the pole residues of the `q=1` controls, three-root lower-rank
derivatives, the other S2T/S2Q components and pole strata, higher orders, the
all-rank-drop branch, a witness, and a counterexample remain open.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The lower-rank derivative census

After permuting roots, write

```text
B_23=B!=0,                 B_13=C!=0,                 B_12=0. (7)
```

S2AB excludes one root block at every joint rank.  S2AG proves, also without
a joint-rank assumption, that two blocks cannot have the shared-factor
rank-five derivative.  Hence

```text
D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6,                 ker D_(B,C)=A_3.       (8)
```

Because `D_(B,C)(K)=U`, the projection

```text
P=pr_(1,2)K subset A_1 direct-sum A_2                 (9)
```

has dimension three, and the restriction of `D_(B,C)` to `P` is an
isomorphism onto `U`.  Therefore

```text
dim(K intersect A_3)=r-3.                             (10)
```

Transpose the three root rows as in S2AD:

```text
rho:A_1^*->K^*,       pi:A_2^*->K^*,
theta:A_3^*->K^*,
V=image rho+image pi, Q=image theta.                  (11)
```

Duality with (9) gives

```text
dim V=3,                 dim Q=q=dim pr_3 K,
V+Q=K^*.                                                (12)
```

The empty permanent would vanish identically if `q=0`.  Target consistency
would then put `J` in `U`; all four sensor columns would lie in the
three-space `U`, contradicting physical full-sensor rank four.  Thus `q>=1`.

If `q=3`, the relation-plane and beta-zero alternatives of S2AD depend only
on `dim P=dim V=3`.  S2AG records that the S2AE graph/square-pencil proof and
the S2AF coordinate-relation proof use only that `Q` is a three-plane, not
`V intersect Q=0`.  They exclude both alternatives.  Hence `q<=2`, proving
(2).  Finally

```text
dim(V intersect Q)=3+q-r,                             (13)
```

which gives the four cells in (3).  Equation (10) also gives the necessary
lower bound `q>=r-3`.

## 2. Every uninvolved-row kernel vector is boundary-supported

Let `eta in ker theta` and contract the third root.  Put

```text
b_eta=(id tensor eta)(B) in A_2,
c_eta=(id tensor eta)(C) in A_1.                     (14)
```

Since `q_eta=0`, the same contraction kills the physical empty permanent.
Target consistency and (8)--(9) give

```text
eta(J) in eta(U)
 subset A_1 tensor b_eta+c_eta tensor A_2.            (15)
```

For every colour `i` in the coordinate support of `eta`, comparison of the
independent pure nonroot monomial `T_i` yields

```text
e_(1,i) tensor e_(2,i)
 in A_1 tensor b_eta+c_eta tensor A_2.                (16)
```

A nonzero decomposable tensor in the space on the right has first factor on
`c_eta` or second factor on `b_eta`: project to

```text
(A_1/span(c_eta)) tensor (A_2/span(b_eta)).           (17)
```

The two fixed lines can cover at most two distinct coordinate diagonals.
Thus every `eta in ker theta` has support at most two.

If `q=2`, this says that the kernel line has support one or two.  If `q=1`,
the kernel is a two-plane contained in the union of the three coordinate
hyperplanes.  Irreducibility of a linear plane over an infinite field puts
it in one fixed hyperplane, and equal dimensions give

```text
ker theta=e_s^perp,
q_t=q_u=0,                    q_s!=0.                 (18)
```

This proves the support assertions without sampling or a generic-point
promotion.

## 3. Two absorbed target diagonals force complementary monomial blocks

We use the following consequence of the exact S2AD beta-zero atlas.

### Lemma 1 (two-diagonal derivative forcing)

Suppose the transverse two-block derivative in (8) contains two distinct
target diagonals

```text
d_t=e_(1,t) tensor e_(2,t) tensor e_(3,t),
d_u=e_(1,u) tensor e_(2,u) tensor e_(3,u).            (19)
```

Then, after exchanging roots one and two,

```text
B proportional e_(2,t) tensor e_(3,t),
C proportional e_(1,u) tensor e_(3,u).               (20)
```

#### Proof

The S2AD beta-zero atlas is applicable because a simultaneous fully supported
zero of the two root blocks would annihilate `image D_(B,C)`, hence `U`, in
contradiction with S2R.  After exchanging blocks, its first case is

```text
B=e_i tensor e_j.                                    (21)
```

Choose `v in {t,u}` different from `j` and write

```text
d_v=a tensor B+C tensor b.                           (22)
```

Modulo `span(e_j)` in the third root, the first term vanishes.  The surviving
rank-one equality forces

```text
b proportional e_v,
C=lambda e_v tensor e_v+x tensor e_j,
lambda!=0.                                           (23)
```

If `j` were different from both `t,u`, applying this to both colours would
make the same quotient of `C` proportional to two distinct pure tensors.
Thus `j` is the other colour, say `w`.  In the equality for `d_w`, the
third-root `v` slice of (23) forces `b=0`, after which (21) forces `i=w`.
Returning to the equality for `d_v`, its third-root `w` slice forces `x=0`.
This gives (20).

In the second beta-zero-atlas case,

```text
B=e_i tensor z,
C=e_j tensor w+x tensor z,                           (24)
```

where `z,w` are independent and `ker z` meets the root torus.  In particular
`z` is not a target-coordinate vector.  Quotienting the third root by
`span(z)` in the equality for either `d_t` or `d_u` forces `e_j` to be that
target coordinate.  Applying it to both distinct colours is impossible.
This excludes (24) and proves the lemma.  QED.

Under (18), the root-3 contractions of the empty permanent at `t,u` vanish.
The `T_t,T_u` target coefficients therefore put `d_t,d_u` in `U`, so Lemma 1
applies.  Rescale (20) to (4).  Injectivity of the derivative on
`A_1 direct-sum A_2` makes the two preimages unique, hence

```text
(e_t,0),(0,e_u) in P.                                (25)
```

Choose a third generator of `P` and subtract multiples of (25).  The four
remaining root rows are all proportional to its dual functional `v`.
Because the root blocks in (4) have no third-root `s` slice, `s`-contraction
of `U` is zero.  Thus target consistency gives the exact one-cell grid

```text
per(r_a,p_b,q_s)=delta_(a,s)delta_(b,s)T_s.           (26)
```

The `(s,s)` cell makes `r_s,p_s` nonzero.  The `(u,s)` and `(s,t)` cells then
force `r_u=p_t=0`, yielding (5)--(6).  Equations (3) and (13) decide whether
`q_s` belongs to the involved three-plane.

## 4. Exact lower-rank row controls

Let the nonroot row space be

```text
W=X direct-sum Y direct-sum Z,                       (27)
```

and choose nonzero target-coordinate forms `x_s in X`, `y_s in Y`,
`z_s in Z`.  Put

```text
v=x_s+z_s,                   a=-x_s+z_s.              (28)
```

For joint rank four choose `x_* in X` independent of `x_s`; for joint rank
three put `x_*=x_s`.  Define

```text
b=-x_*+y_s,                 q=(x_*+y_s)/2,            (29)

r_s=p_s=v,                 r_t=a,       p_u=b,
q_s=q,
r_u=p_t=q_t=q_u=0.                                  (30)
```

Direct polarization gives

```text
per(v,v,q)=x_s tensor y_s tensor z_s,
per(a,v,q)=per(v,b,q)=per(a,b,q)=0.                  (31)
```

The rows `a,b,v,q` have rank four when `x_*` is independent of `x_s`.  When
`x_*=x_s`, they have rank three and

```text
q=(b+v-a)/2.                                         (32)
```

The three involved rows `a,b,v` still have a nonzero transversal determinant:

```text
det[(a|_X,a|_Y,a|_Z),
    (b|_X,b|_Y,b|_Z),
    (v|_X,v|_Y,v|_Z)]
=-2 x_s y_s z_s.                                    (33)
```

Thus the three singleton columns are generically independent in both ranks.

Take the root blocks in (4) with `lambda=mu=1` and `tau=1`.  Their singleton
span has the basis

```text
d_t,
d_u,
m=e_s tensor e_t tensor e_t+e_u tensor e_s tensor e_u. (34)
```

In this basis the three singleton columns are

```text
G_x=(-x_s,-x_*,x_s),
G_y=(0,y_s,0),
G_z=(z_s,0,z_s).                                    (35)
```

Equation (33) is exactly the determinant of (35).  Formula (31) makes the
physical empty companion

```text
G_N=d_s x_s y_s z_s.                                 (36)
```

Hence (34)--(36) satisfy the complete common-shore matching formulas and
leave precisely the two target terms `d_t T_t+d_u T_u` in `J-G_N`.

## 5. The unique pair lifts have coordinate poles

Write

```text
T_t=x_t y_t z_t,                  T_u=x_u y_u z_u.   (37)
```

Solving (35) for the residual target gives the unique rational pair
coefficients, in the singleton-column order `(G_x,G_y,G_z)`,

```text
C_x=-T_t/(2x_s),
C_z= T_t/(2z_s),
C_y= T_u/y_s-x_* T_t/(2x_s y_s).                    (38)
```

Indeed

```text
G_x C_x+G_y C_y+G_z C_z=(T_t,T_u,0).                 (39)
```

Their multidegrees are the required pair-deck degrees, but (38) exposes
prime-divisor poles on `x_s y_s z_s=0`.  This is consistent with the S2Q
common-three-space localization.  The controls are physical singleton/empty
shores and normalized target incidences, but the pair layer is not a global
collection of bilinear edge blocks.  They therefore do not contradict the
certified six-vertex exclusion and are not graph witnesses.

## 6. Proof-topology consequence

The transverse two-root lower-rank frontier is now

```text
joint rank 3 or 4, uninvolved-row rank q=3:            IMPOSSIBLE;
joint rank 3 or 4, q=2, kernel support at most two:    OPEN;
joint rank 3 or 4, q=1:
  complementary diagonal root blocks and one-cell
  permanent normal form (4)--(6):                     PROVED;
  exact normalized physical pole controls:            EXIST at both ranks;
  pole-residue / higher-deck exclusion:                OPEN;

three-root lower-rank derivatives / other components: OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.       (40)
```

The next honest step is to use residue or higher-deck information not present
in the local singleton/empty incidence equations, or to close the `q=2` and
three-root lower-rank cells.  The controls forbid silently treating full
sensor rank, target consistency, or the one-cell zero rectangle as an
exclusion.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_localization_and_pole_controls.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_localization_and_pole_controls.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_localization_and_pole_controls.py claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_localization_and_pole_controls.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_localization_and_pole_controls.py claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_localization_and_pole_controls.py
```

The primary verifier replays the derivative, all four `(r,q)` incidence
models, the support boundary, both physical row controls, the complete
singleton and empty matching formulas, target congruence, full-sensor rank,
and the rational Cramer identities.  The independent no-import audit rebuilds
the rows, permanents, singleton slices, exact ranks, and Laurent identities
with standard-library `Fraction` arithmetic.  The arbitrary-vector support
argument and Lemma 1 are the written characteristic-zero proof.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
