# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` residual second-root-coloop projective-pencil localization

## Status

**Exact characteristic-zero projective-pencil and coordinate-endpoint
localization for both residual second-root coordinate-coloop orientations on
the normalized, target-consistent physical `m=3` common-three-space
full-sensor stratum.**  Retain

```text
dim U=3,                         rank H=5,

ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2,                     (1)
```

and suppose the S2AZ coordinate-coloop fork selects

```text
N=K^perp subset {beta_j=0},                   j!=t.  (2)
```

Let `k` be the third colour.  Then the determinant-face pencil forces

```text
s=t:       z_t=w_t=0;

s!=t:      y_s=0                 or
           z_s=w_s=0.                              (3)
```

There is also the exact incidence

```text
span(z,w) contains e_i for at least one i!=s.        (4)
```

S2BE proves that `w` is proportional to `e_j` or `e_k`.  Absorb the
nonzero endpoint scalar.  If `w=e_l`, where `l` is one of `j,k`, and `m`
is the other one, (3)--(4) give the complete support table

```text
s=l:       y is proportional to e_m,      z_m z_t=0;
s=m:       y_m z_m=0;
s=t:       z_t=0.                                   (5)
```

In addition, the selected canonical row is a genuine escape:

```text
p_j notin S=R direct-sum span(A).                    (6)
```

The key new permanent lemma strengthens S2BD's one-row-escape obstruction.
A binary diagonal frame is impossible whenever its middle-row plane has
*any* nonzero intersection with the three-space containing the first- and
third-row planes; the intersection line need not be one of the two
target-indexed middle rows.  The new generic-line case has four ordered
plane-intersection endpoints and seven nonempty support masks.  All 28 exact
normal forms have pinned rational Nullstellensatz identities.

This theorem is a localization, not an exclusion of a residual coloop or an
endpoint in (5).  The four ordered endpoints, the three third-root coloops,
the two complementary first-root coloops, joint rank at most four, other
physical component types, higher orders, and the global conjecture remain
open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Residual-coloop rows and the forced escape

Use the S2AZ notation

```text
r_i=rho(e_i^*),       p_i=pi(e_i^*),
q_i=theta(e_i^*),     T_i=X_i tensor Y_i tensor Z_i,

A=lambda^(-1)r_s,     B=mu^(-1)p_t,
R=rho(e_s^perp),      S=R direct-sum span(A).        (7)
```

Let `L=(ker D_B)^perp`, `E=image H^T`, and `V=H^T(L)`.  S2AZ and S2BD give

```text
dim R=2,              dim S=dim V=3,
E/V=span([A],[B]),    [A],[B] independent,

g_k=p_k-y_kA in R,
h_a=q_a-z_aA-w_aB in R,                  a=0,1,2.   (8)
```

The seven canonical rows spanning `V` are

```text
(r_i)_(i!=s),        g_j,g_k,        h_0,h_1,h_2.   (9)
```

Every row in (9) except `g_j` lies in the two-plane `R`.  Since the seven
rows span the three-space `V`,

```text
g_j notin R.                                         (10)
```

Also `V intersect S=R`, because `R subset V` and `A notin V`.  As

```text
p_j=y_jA+g_j,                                        (11)
```

membership of `p_j` in `S` would put `g_j` in `V intersect S=R`, contrary
to (10).  This proves (6).  The point is stronger than the earlier safe
statement that `p_j` may escape: under (2), it must escape.

S2BC's target-contraction argument, which uses only the S2AZ gauge, makes
both `pi` and `theta` injective.  We use this below to preserve every
two-plane and every nonzero intersection row.

## 2. A binary diagonal frame cannot have an arbitrary middle intersection

### Lemma 1 (intersecting-middle-plane binary obstruction)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field.  Let
`S subset W` be a three-space.  Suppose

```text
R=span(r_0,r_1),       Q=span(q_0,q_1) subset S
```

are two-planes and `P=span(p_0,p_1)` is a two-plane satisfying

```text
P intersect S !=0.                                  (12)
```

There are no nonzero scalars `c_0,c_1` and fully transverse decomposable
tensors `T_0,T_1` such that

```text
per(r_a,p_b,q_c)=
  c_a T_a,                         a=b=c,
  0,                               otherwise,

a,b,c in {0,1}.                                    (13)
```

#### Proof: reduction to the generic middle line

If `P subset S`, S2AN's three-plane binary-diagonal obstruction applies.
If `P intersect S` is `span(p_0)` or `span(p_1)`, S2BD Lemma 1 applies,
after interchanging the binary labels if necessary.  It remains that

```text
P intersect S=span(a p_0+b p_1),          ab!=0.   (14)
```

Rescale the two target-indexed middle rows and absorb the induced nonzero
constants into `c_0,c_1`.  Thus the line in (14) is `span(p_0+p_1)`.

The plane-incidence part of S2BD Lemma 1 does not use which row of `P` lies
in `S`.  If `R=Q`, permanent symmetry gives the same singular change matrix
and the S2AL two-square contradiction.  If `R!=Q`, its intersection line
cannot be generic in both ordered planes by tangent-line separation and
cannot be coordinate in only one by mixed factor sharing.  Therefore

```text
R intersect Q=span(r_a)=span(q_b),
                                  (a,b) in {0,1}^2. (15)
```

This leaves four ordered endpoint incidences.

Choose a basis of `S'=S direct-sum span(p_0)` so that

```text
r_a=q_b=e_0,      r_(1-a)=e_1,      q_(1-b)=e_2,
p_0=e_3.                                             (16)
```

The nonzero vector `p_0+p_1` lies in `S`.  Independent diagonal rescaling
of `e_0,e_1,e_2` normalizes it to one of the seven nonempty support masks:

```text
p_1=epsilon_0e_0+epsilon_1e_1+epsilon_2e_2-e_3,
(epsilon_0,epsilon_1,epsilon_2) in {0,1}^3 minus {000}. (17)
```

The four choices in (15) and seven choices in (17) are an exhaustive 28-case
normal-form cover.

Choose source-coordinate bases whose first two factor lines are those of
`T_0,T_1`.  Restrict their six selected coordinate forms to `S'`.  As in
S2BD, expand the polarized permanent at all eight selected source triples
and all eight binary row triples.  Set the coefficient to one only at

```text
(source;row)=(000;000),              (111;111),      (18)
```

and to zero at the other 62 positions.  Every realization of (13) would
solve these 64 necessary cubic equations.

For all 28 normal forms, the durable certificate gives an exact rational
identity

```text
1=sum_(nu=1)^64 h_nu f_nu.                           (19)
```

The identities contain 20,582 sparse multiplier terms.  The compact
certificate has SHA-256

```text
0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca. (20)
```

Both replay programs reconstruct all 64 generators in every case before
checking (19).  The independent audit reverses all 24 variables and uses a
separate standard-library permanent expansion.  Since the identities have
rational coefficients, they remain unit-ideal identities after scalar
extension to every characteristic-zero field.  Thus (14) is also
impossible, proving Lemma 1.  QED.

## 3. The residual coloop puts every projective face in Lemma 1

The gauge-fixed derivative transpose is

```text
D_B^T(alpha tensor beta tensor gamma)
 =((beta(y)gamma(w)-mu beta_t gamma(z))alpha,
   -lambda alpha_s gamma(w) beta,
    lambda mu alpha_s beta_t gamma).                 (21)
```

For a projective direction `delta=[h:kappa] in P^1`, define

```text
P_delta={beta: kappa beta(y)-h mu beta_t=0},
Q_delta={gamma:kappa gamma(z)-h gamma(w)=0}.         (22)
```

When `alpha_s=0`, `beta in P_delta`, and `gamma in Q_delta`, matching
evaluation pairs make the determinant in (21) vanish.  The complete target
equation is

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i.                 (23)
```

Put `v=z^perp intersect w^perp`.  The pure root covector `(0,0,v)` belongs
to `L intersect {beta_j=0}`, so the residual coloop gives

```text
q(v) in R.                                           (24)
```

Fix `delta` and choose `0!=beta_*` in
`P_delta intersect {beta_j=0}`.  If its evaluation pair
`(beta_*(y),mu beta_*t)` is zero, then `p(beta_*) in R`; choosing any
nonkernel row of `Q_delta` puts `R`, `q(Q_delta)`, and `p(beta_*)` in one
space of dimension at most three.

If the pair is nonzero, choose `gamma_* in Q_delta` with opposite pair.
Then `(0,beta_*,gamma_*)` lies in `L intersect {beta_j=0}`, hence

```text
p(beta_*)+q(gamma_*) in R.                          (25)
```

Together with (24), equation (25) again puts

```text
R, q(Q_delta), p(beta_*) subset S_delta,
                                      dim S_delta<=3. (26)
```

Injectivity makes `p(P_delta)` and `q(Q_delta)` two-planes and makes the
displayed middle intersection nonzero.  Enlarge `S_delta` to a three-space
if needed.

Let `I` be the two colours different from `s`.  Projection of the two
covector planes in (22) to their `I` coordinates is invertible exactly when

```text
L_P(h,kappa)=kappa y_s-h mu delta_(s,t) !=0,
L_Q(h,kappa)=kappa z_s-h w_s !=0.                   (27)
```

If both gates are nonzero, choose their coordinate lifts over `I`.
Equation (23) is precisely the binary diagonal table (13) on the row planes
in (26), contradicting Lemma 1.  Therefore

```text
L_P(h,kappa)L_Q(h,kappa)=0
                    for every [h:kappa] in P^1.     (28)
```

Over the infinite characteristic-zero field, the homogeneous quadratic in
(28) vanishes identically.  The polynomial ring is an integral domain, so
one linear factor vanishes identically.  If `s=t`, the gauge `y_t=0` gives
`L_P=-h mu`, which is not the zero form; hence `z_t=w_t=0`.  If `s!=t`,
then `L_P=kappa y_s`, and the two possible zero factors are exactly the two
alternatives in (3).

## 4. Auxiliary incidence and endpoint table

For `alpha_s=0`, `gamma=v`, and arbitrary `beta`, all components of (21)
vanish.  The complete target equation gives

```text
per(r(alpha),p(beta),q(v))
 =sum_i alpha_i beta_i v_i T_i.                     (29)
```

The two rows `(r_i)_(i!=s)` are a basis of `R`, `q(v)` is a nonzero row in
`R` by injectivity, and `pi` is injective.  If both coordinates of `v`
outside `s` were nonzero, the S2BA coefficient fork would give either two
fully transverse targets in one square map or two nonzero mixed maps with
fully transverse images.  Both are forbidden by the S2AL tangent-line and
mixed-factor lemmas.  Thus some `v_i=0` with `i!=s`.  Since `v` is the
normal of `span(z,w)`, this is equivalent to (4).

Now use S2BE and write `w=e_l`, `l in {j,k}`.  If `s=t`, (3) gives
`z_t=0`.  If `s=l`, the second alternative in (3) is impossible because
`w_s!=0`; hence `y_s=0`.  Together with `y_t=0` and `y!=0`, this makes
`y` proportional to `e_m`.  Condition (4) says the plane
`span(z,e_l)` contains `e_m` or `e_t`, which is exactly `z_m z_t=0`.
Finally, if `s=m`, equation (3) is `y_m=0` or `z_m=0`, because `w_m=0`.
This proves (5).

## 5. Proof-topology consequence

The live `(1,2,2)` rank-five coloop frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);

beta_j coloop, j!=t:
  w=e_l, l in {j,k}, with the exact table (5):      OPEN;

three gamma_k coloops / two complementary alpha coloops
  / joint rank <=4 / other components / higher m:  OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.     (30)
```

No endpoint in (30) is asserted to exist.  No finite-field scan, numerical
specialization, bounded parameter sample, generic-point promotion, or
unproved incidence cover enters the proof.  The only finite split is the
proved four-endpoint/seven-support orbit cover in Lemma 1, and every leaf has
an exact rational identity.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_certificates.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_certificates.py
```

The primary replay uses SymPy rational polynomials.  The independent audit
imports no repository module or third-party package, reverses the variable
order, and expands every permanent independently.  Optional deterministic
certificate regeneration requires Singular 4.x, directly or through WSL:

```text
python claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_certificates.py
```

Singular is not needed for either replay.

## Dependencies

- [`(1,2,2)` residual second-root coordinate-line localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COORDINATE_LINE_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` residual second-root support localization and one-row-escape obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_SUPPORT_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` determinant-face pencil and `pi,theta` injectivity](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md)
- [Tangent-line and mixed-factor-sharing lemmas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#2-two-exact-two-plane-lemmas)
- [`beta_t`-coloop auxiliary coefficient fork](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_BETA_T_COLOOP_SUPPORT_LOCALIZATION_THEOREM.md#3-two-auxiliary-complete-faces)
