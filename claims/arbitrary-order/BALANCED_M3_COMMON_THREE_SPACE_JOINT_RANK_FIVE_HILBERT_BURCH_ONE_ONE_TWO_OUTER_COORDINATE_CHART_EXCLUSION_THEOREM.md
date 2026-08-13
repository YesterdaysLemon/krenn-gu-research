# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,1,2)` outer-coordinate-chart exclusion

## Status

**Exact characteristic-zero exclusion of both genuinely outer coordinate-pair
charts of the `(1,1,2)` Hilbert--Burch boundary on the normalized,
target-consistent physical `m=3` common-three-space full-sensor stratum.**
Let `U` be the total singleton span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

Use the S2AG normal form

```text
ker D_B=span{(x,0,z),(0,y,w)},
dim span(z,w)=2.                                      (2)
```

Suppose first that the selected outer pair is coordinate:

```text
x=lambda e_s,                  w=nu e_t,
lambda nu!=0.                                        (3)
```

Then this chart is impossible.  If `y` is coordinate, it belongs to the
central chart already excluded by S2AX.  Otherwise an exact transpose
recovery identity forces `K` to contain a pure root-coordinate vector.  A
single binary exterior face excludes all nine possible coordinate coloops.
The proof uses the S2AL square/mixed lemma, the two endpoint lemmas of S2AX,
and two new exact source-support lemmas for the only support-degenerate
orientations.

Interchanging the first two roots and the two Hilbert--Burch generators sends
the other outer pair `(y,z)` to the form (3).  Hence both genuinely outer
coordinate-pair charts are impossible.

Together with S2AS--S2AX, this closes every coordinate-pair chart in the
`(1,1,2)` atlas.  Since the S2AG Boolean clauses say that every point of this
profile contains at least one of exactly those three coordinate pairs, the
complete `(1,1,2)` profile is impossible.  This theorem does **not** exclude
the `(1,2,2)` profile, joint ranks at most four, other physical component
types, higher orders, or a counterexample.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. Outer derivative, recovery, and the binary exterior face

The root--root blocks and derivative on (3) are

```text
B_23=-y tensor z,
B_13=-lambda nu e_s tensor e_t,
B_12= lambda e_s tensor y,

D_B(a,b,c)
 =-a tensor y tensor z
  -lambda nu e_s tensor b tensor e_t
  +lambda e_s tensor y tensor c.                    (4)
```

Write

```text
r(alpha)=rho(alpha),       p(beta)=pi(beta),
q(gamma)=theta(gamma),
T_i=X_i tensor Y_i tensor Z_i.                       (5)
```

The annihilator of the derivative kernel is

```text
L=(ker D_B)^perp
 ={(alpha,beta,gamma):
      lambda alpha_s+gamma(z)=0,
      beta(y)+nu gamma_t=0},            dim L=7.     (6)
```

For a product root functional, transpose of (4) is

```text
D_B^T(alpha tensor beta tensor gamma)
 =(-beta(y)gamma(z)alpha,
   -lambda nu alpha_s gamma_t beta,
    lambda alpha_s beta(y)gamma).                    (7)
```

Substitution of (6) gives the exact self-recovery identity

```text
D_B^T(alpha tensor beta tensor gamma)
 =nu gamma(z)gamma_t(alpha,beta,gamma),
                              (alpha,beta,gamma) in L. (8)
```

Put

```text
N=K^perp subset L,       dim N=4,
V=H^T(L),                dim V=3.                    (9)
```

Let

```text
E=e_s^perp subset A_1^*,          Y=y^perp subset A_2^*,
R=r(E),                           P=p(Y),
Q=image theta.                                         (10)
```

For `alpha in E` and `beta in Y`, every summand of (7) vanishes.
The complete target equation therefore gives the exact exterior face

```text
per(r(alpha),p(beta),q(gamma))
 =sum_(i!=s) alpha_i beta_i gamma_i T_i.              (11)
```

Let `a,b` be the two colours different from `s`.  Since `y` is not a target
coordinate, neither coordinate functional `beta_a,beta_b` vanishes
identically on `Y`.  Equation (11) makes `r|E` injective, so

```text
dim R=2.                                               (12)
```

It also makes every element of `ker(p|Y)` a multiple of `e_s^*`.  If
`y_s!=0`, this already proves injectivity.  Suppose `y_s=0`.  If `t!=s`,
the second exterior family

```text
beta in y^perp,            gamma_t=0                 (13)
```

and the complete target equation at colour `s` give
`per(r_s,p_s,q_s)=T_s`, so `p_s!=0`.  If `t=s` and `p_s=0`, every vector of
`K=image H` has second coordinate `b_s=0`.  At the root coefficient
`(s,s,s)`, the first and third summands of (4) vanish because `y_s=0`, the
second vanishes because `b_s=0`, and the all-cross term vanishes because
`p_s=0`.  This misses the nonzero target `T_s`, a contradiction.  Thus in
all cases

```text
dim P=2.                                               (14)
```

Finally choose `eta in A_2^*` with `eta(y)=1` and put

```text
A=lambda^(-1)r_s,       B=p(eta),
h(gamma)=q(gamma)-gamma(z)A-nu gamma_t B in V.        (15)
```

Modulo `V`,

```text
q(gamma) congruent gamma(z)A+nu gamma_tB.             (16)
```

The classes of `A,B` form a basis of the two-dimensional quotient of the
full row image by `V`, and `gamma(z),gamma_t` are independent because
`z` is not proportional to `e_t`.  If `0!=n` spans
`z^perp intersect e_t^perp`, then `q(n)=h(n) in V` is nonzero.  Otherwise
third-root contraction by `n` kills the all-cross term; it also kills
`D_B(K)` because `n(z)=n_t=0` and `q(n)=0` says `n(c)=0` on `K`.  The target
contraction `sum_i n_iT_i` is nonzero.  Therefore

```text
dim Q=3.                                               (17)
```

For a basis `v_0,v_1,v_2` of `V`, physical full-sensor rank gives

```text
Alt(v_0,v_1,v_2)
 =sum_(sigma in S_3) sign(sigma)
   (v_(sigma(1)))_X tensor
   (v_(sigma(2)))_Y tensor
   (v_(sigma(3)))_Z !=0.                              (18)
```

## 2. The nine-coordinate coloop fork

If an element of `N` has all nine target-coordinate evaluations nonzero,
then `gamma_t!=0` and, by (6), `gamma(z)=-lambda alpha_s!=0`.  Equation (8)
makes its product functional a fully supported annihilator of
`U=D_B(K)`, contrary to S2R.  Thus `N` is covered by the nine coordinate
hyperplanes

```text
alpha_i=0,             beta_j=0,             gamma_k=0,
0<=i,j,k<=2.                                        (19)
```

Over the infinite characteristic-zero field, a vector space is not a finite
union of proper subspaces.  Hence `N` is contained in one fixed hyperplane
in (19).  If `F subset L` is that six-dimensional hyperplane, then

```text
dim H^T(F)=dim F-dim N=2.                             (20)
```

We call this two-plane `S`.  The missing direction is a coloop of the
seven-row three-space `V`.

Two classes in (19) immediately force equal row planes.  If
`N subset {gamma_k=0}`, then `F` contains the independent copies of `E` and
`Y`, so `R,P subset S`.  If `N subset {alpha_s=0}`, equation (6) replaces
that condition by `gamma(z)=0`, and the same conclusion holds.  By
(12)--(14),

```text
R=P=S.                                                (21)
```

The next lemma excludes (21).

### Equal-plane binary-face lemma

Choose `beta in Y` with `beta_a beta_b!=0`, possible because `y` is not a
coordinate vector, and put `p=p(beta) in S`.  Write

```text
p=c r_a+d r_b,                  (c,d)!=(0,0),         (22)
```

where `r_i=r(e_i^*)`.  Equation (11) says

```text
M_(r_a,p)(q(gamma))=beta_a gamma_aT_a,
M_(r_b,p)(q(gamma))=beta_b gamma_bT_b,                (23)
```

with `M_(u,v)(q)=per(u,v,q)`.  Hence

```text
M_(p,p)(q(gamma))
 =c beta_a gamma_aT_a+d beta_b gamma_bT_b.            (24)
```

If `cd!=0`, the square image contains both fully transverse decomposable
tensors `T_a,T_b`, contrary to the S2AL tangent-line separation lemma.  If
one coefficient vanishes, (23)--(24) give a nonzero rank-one square and a
nonzero rank-one mixed map containing its repeated row onto the two fully
transverse targets, contrary to the S2AL mixed factor-sharing lemma.  Thus
(21) is impossible.  This eliminates `alpha_s` and all three `gamma_k`
alternatives.

## 3. Two support-degenerate endpoint lemmas

The remaining first- and second-root coloops are generically the S2AX
coefficient fork.  We isolate the two exact lemmas needed when
`y_s=0` removes one column of that binary frame.  Work in
`W=X direct-sum Y direct-sum Z`, let `dim Q=3`, and retain the notation
`M_(u,v)(q)=per(u,v,q)`.

### Lemma 1 (square-zero radical bridge)

Suppose `a,b,v` form a basis of a three-plane and

```text
Alt(a,b,v)!=0,
M_(b,b)(Q)=M_(a,b)(Q)=0,                              (25)

M_(a,v)|Q and M_(b,v)|Q are nonzero rank-one maps     (26)
```

with fully transverse decomposable image tensors.  Then no such data exist.

#### Proof

If `b` has all three source components, the kernel of its square map is the
two-plane

```text
{(c_Xx,c_Yy,c_Zz):c_X+c_Y+c_Z=0},                    (27)
```

and cannot contain `Q`.

If `b=x+y` has exactly two source components, its square zero puts
`Q subset X direct-sum Y`.  The nonzero map containing `b` has the form

```text
M_(b,v)(q)=v_Z tensor(x tensor q_Y+q_X tensor y).     (28)
```

The parenthesized map has one-dimensional kernel `span(x-y)`, so its image
on the three-plane `Q` has dimension at least two, contrary to (26).

It remains that `b=x` is pure.  The mixed radical equation is

```text
a_Y tensor q_Z+q_Y tensor a_Z=0.                     (29)
```

If exactly one of `a_Y,a_Z` is nonzero, (29) removes the opposite source
from `Q`.  Rank one of `M_(b,v)|Q` then makes the remaining non-`X`
projection of `Q` one-dimensional.  Its kernel contains a two-plane of pure
`X` vectors.  On that two-plane,

```text
M_(a,v)(q)=q_X tensor
 (a_Y tensor v_Z+v_Y tensor a_Z),                    (30)
```

whose second factor is nonzero by `Alt(a,b,v)!=0`; the map has rank at
least two.

If both `a_Y,a_Z` are nonzero, (29) gives

```text
q_Y=tau(q)a_Y,                 q_Z=-tau(q)a_Z.        (31)
```

The kernel of `tau|Q` is again a two-plane of pure `X` vectors.  Unless the
parenthesized tensor in (30) is zero, the same rank contradiction applies.
If it is zero, then for some nonzero `c`

```text
v_Y=c a_Y,                     v_Z=-c a_Z.            (32)
```

Direct substitution into (26) shows that the two image tensors both have
the factor lines `span(a_Y),span(a_Z)`.  They are not fully transverse.
This exhausts the support of `b`.  QED.

### Lemma 2 (radical-plane two-target factor lemma)

Let `S=span(a,b)=span(v,d)` be a two-plane, let `p` complete it to a
three-plane `V`, and suppose

```text
0!=v in S,                       Alt(a,b,p)!=0,
M_(v,S)(Q)=0.                                          (33)
```

If `M_(a,p)|Q` and `M_(b,p)|Q` are nonzero rank-one maps with decomposable
images, their image tensors share a source factor line.

#### Proof

A full-support `v` is impossible by the square-kernel dimension in (27).
If `v=x+y`, square zero puts `Q subset X direct-sum Y`; the mixed zero with
`d` forces `d_Z=0`, because the map in parentheses in (28) has
one-dimensional kernel.  Thus `S,Q subset X direct-sum Y`, and every value
`M_(S,p,Q)` has the fixed third factor `p_Z`.  Nonvanishing of the
alternating tensor ensures `p_Z!=0`, so both image tensors share it.

Let `v=x` be pure.  The radical equation is

```text
d_Y tensor q_Z+q_Y tensor d_Z=0,                     (34)
```

while full sensor gives

```text
d_Y tensor p_Z-p_Y tensor d_Z!=0.                    (35)
```

If exactly one of `d_Y,d_Z` is nonzero, (34) removes the opposite source
from `Q`, and all values `M_(S,p,Q)` share the remaining non-`X` factor of
`p`.  If both are nonzero, then

```text
q_Y=tau(q)d_Y,                  q_Z=-tau(q)d_Z.       (36)
```

On the two-plane `ker(tau|Q) subset X`, a vector
`s=A v+B d` satisfies

```text
M_(s,p)(q)=B q_X tensor
 (d_Y tensor p_Z+p_Y tensor d_Z).                    (37)
```

Because `a,b` form a basis and both maps in the lemma have rank one, the
parenthesized tensor must vanish.  Equation (35) then gives a nonzero `c`
with

```text
p_Y=c d_Y,                     p_Z=-c d_Z.            (38)
```

Substitution into (36) yields

```text
M_(s,p)(q)=-2c tau(q)s_X tensor d_Y tensor d_Z.       (39)
```

Both nonzero images share the last two factor lines.  If `tau` vanishes on
`Q`, (37) instead has rank zero or at least two, so two nonzero rank-one
maps cannot occur.  These cases prove the lemma.  QED.

## 4. Exclusion of the first-root coloops

Suppose `N subset {alpha_a=0}`; the `alpha_b` case is symmetric.  The
hyperplane image in (20) contains `P` and `r_b`, so

```text
S=P,                  r_b in S,       r_a notin S.    (40)
```

### 4.1 The case `y_s!=0`

Restriction `Y -> span(e_a^*,e_b^*)` is an isomorphism.  Choose
`beta^a,beta^b in Y` dual to the two displayed coordinates and write
`p_a=p(beta^a),p_b=p(beta^b)`.  Equation (11) is the complete binary table

```text
M_(r_a,p_a)(q(gamma))=gamma_aT_a,
M_(r_a,p_b)(Q)=M_(r_b,p_a)(Q)=0,
M_(r_b,p_b)(q(gamma))=gamma_bT_b.                     (41)
```

Write `r_b=c p_a+d p_b`.  This is exactly the S2AX coefficient fork.  If
`cd!=0`, (41) gives a rank-one square onto `T_b` and a rank-one mixed map
containing its repeated row onto `T_a`, contradicting S2AL.  At `d=0`, one
square-zero row carries two transverse rank-one mixed targets, contrary to
S2AX Lemma 1.  At `c=0`, a rank-one square has two mixed radical rows which,
by S2AX Lemma 2, kill the nonzero alternating tensor (18).  All cases are
impossible.

### 4.2 The case `y_s=0`

Now `y_a y_b!=0`.  Choose `beta^0 in Y` with

```text
beta^0_s=0,                    beta^0_a beta^0_b!=0,
p_0=p(beta^0).                                       (42)
```

Then `P=span(p_0,p_s)`.  Write

```text
r_b=c p_0+d p_s.                                     (43)
```

Equation (11) gives

```text
M_(r_a,p_0)|Q -> span(T_a) nonzero of rank one,
M_(r_b,p_0)|Q -> span(T_b) nonzero of rank one,
M_(R,p_s)(Q)=0.                                      (44)
```

If `c!=0`, (43)--(44) give a rank-one square of `r_b` onto `T_b` and a
rank-one mixed map `M_(r_a,r_b)` onto `T_a`, contradicting S2AL.  If
`c=0`, then `r_b` is proportional to `p_s`; (44) becomes

```text
M_(r_b,r_b)=M_(r_a,r_b)=0,                           (45)
```

while the two maps with `p_0` in (44) have the fully transverse images
`T_a,T_b`.  The vectors `r_a,r_b,p_0` form a basis of `V`, so (18) applies.
Lemma 1 excludes (44)--(45).

Thus both first-root coloop orientations are impossible.

## 5. Exclusion of the second-root coloops

Suppose `N subset {beta_j=0}`.  Its hyperplane image contains `R`, hence

```text
S=R.                                                  (46)
```

The line

```text
Y_j=Y intersect {beta_j=0}                           (47)
```

is one-dimensional because `y` is not a coordinate vector.  Choose
`0!=beta in Y_j` and put `v=p(beta) in S`; it is nonzero by (14).

If `beta_a beta_b!=0`, express `v=c r_a+d r_b`.  Equation (11) gives the two
rank-one maps onto `T_a,T_b`, and the equal-plane calculation
(22)--(24) excludes this case.

Suppose exactly one of `beta_a,beta_b` is nonzero, say
`beta_a!=0,beta_b=0`.  Then `y_s!=0`, so restriction of `Y` to the
`a,b` coordinates is an isomorphism.  Choose `beta' in Y` with
`beta'_a=0,beta'_b!=0` and put `p'=p(beta')`.  The vector `p'` lies outside
`S` and completes it to `V`.  The exterior table is

```text
M_(r_a,v)|Q -> span(T_a) nonzero of rank one,
M_(r_b,v)(Q)=M_(r_a,p')(Q)=0,
M_(r_b,p')|Q -> span(T_b) nonzero of rank one.        (48)
```

Writing `v=c r_a+d r_b` gives the S2AX coefficient fork with the first and
second row families interchanged.  For `cd!=0`, its square/mixed maps
contradict S2AL.  For `c=0`, S2AX Lemma 1 excludes a square-zero row with
two transverse targets.  For `d=0`, S2AX Lemma 2 makes the alternating
tensor of `v,r_b,p'` zero, contrary to (18).  The case with `a,b`
interchanged is identical.

It remains that

```text
beta_a=beta_b=0.                                     (49)
```

Then `beta` is proportional to `e_s^*`, so `y_s=0` and `v` is proportional
to the nonzero row `p_s`.  Equation (11) gives

```text
M_(v,S)(Q)=0.                                        (50)
```

Choose `beta^0` as in (42).  Its row `p_0` lies outside `S`, completes it to
`V`, and (11) gives nonzero rank-one maps

```text
M_(r_a,p_0)|Q -> span(T_a),
M_(r_b,p_0)|Q -> span(T_b).                           (51)
```

Lemma 2 says their decomposable images share a source factor, contrary to
the full transversality of `T_a,T_b`.  Thus every `beta_j` alternative is
impossible.

Sections 2, 4, and 5 exclude all nine hyperplanes in (19).  Therefore the
outer chart (3) does not occur.

## 6. Symmetry and proof-topology consequence

If the selected S2AG outer pair is `(y,z)`, interchange the first two roots
and then interchange the two kernel generators.  The new normal form is

```text
ker D_B=span{(y,0,w),(0,x,z)},                        (52)
```

so the coordinate pair `(y,z)` becomes the `(x',w')` pair treated above.
Hence both outer charts are impossible.

Combining this theorem with S2AS--S2AX gives

```text
Hilbert--Burch (1,1,2):
  central coordinate-pair charts:                   IMPOSSIBLE;
  outer coordinate-pair charts:                     IMPOSSIBLE;
  every coordinate-pair chart in the S2AG atlas:    IMPOSSIBLE;
  complete (1,1,2) profile:                          IMPOSSIBLE;

(1,2,2) / joint rank <=4 / other components
  / higher m:                                        OPEN.       (53)
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Focused replay

```bash
python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_outer_coordinate_chart_exclusion.py
python claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_outer_coordinate_chart_exclusion.py
```

The primary replay checks the outer derivative and kernel, recovery scalar,
exterior-face vanishing, quotient-rank calculation, support split, all
coefficient forks, and both endpoint source-support atlases exactly.  The
independent audit uses its own rational linear algebra and independently
reconstructs the derivative, coordinate-hyperplane fork, support cases, and
endpoint identities without importing the primary verifier.

## Dependencies

- [Joint-rank-five derivative and torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [Singleton-span torus-annihilator obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [Support-one higher-row-rank exclusion (square/mixed lemmas)](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
- [`(1,1,2)` same-colour central-chart exclusion (endpoint lemmas)](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_SAME_COLOUR_CENTRAL_CHART_EXCLUSION_THEOREM.md)
