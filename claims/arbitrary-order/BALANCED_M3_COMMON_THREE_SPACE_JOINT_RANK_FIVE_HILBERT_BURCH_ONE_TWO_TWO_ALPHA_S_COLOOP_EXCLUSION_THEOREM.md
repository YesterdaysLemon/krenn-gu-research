# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` `alpha_s`-coloop exclusion

## Status

**Exact characteristic-zero exclusion of the distinguished first-root
coordinate coloop in the normalized, target-consistent physical `m=3`
common-three-space full-sensor stratum.**  Retain

```text
dim U=3,                         rank H=5,             (1)
```

and the S2AZ gauge

```text
ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2.                     (2)
```

Let `N=K^perp`, where `K=image H`.  The coordinate-coloop alternative

```text
N subset {alpha_s=0}                                  (3)
```

is impossible.

The proof uses the projective pencil of product faces on which the
Hilbert--Burch determinant vanishes.  Every pencil member supplies three
two-planes in one space of dimension at most three.  Unless a coordinate
projection degenerates, the complete target equation gives the forbidden
S2AN binary diagonal cube.  Vanishing of the product of the two projection
determinants on the whole projective line forces one of two exact linear
degeneracies.  A one-sided degeneracy is the S2AO same-third-row obstruction;
their intersection gives a new same-pair binary table, excluded below by a
complete plane-incidence argument.

This closes only the `alpha_s` coloop orientation.  The other seven
`(1,2,2)` coordinate coloops, joint rank at most four, other physical
component types, higher orders, and the global conjecture remain open.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The determinant-face pencil

Write

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_i=X_i tensor Y_i tensor Z_i. (4)
```

The gauge-fixed derivative transpose from S2AZ is

```text
D_B^T(alpha tensor beta tensor gamma)
 =((beta(y)gamma(w)-mu beta_t gamma(z))alpha,
   -lambda alpha_s gamma(w) beta,
    lambda mu alpha_s beta_t gamma).                 (5)
```

We first record that both

```text
pi:A_2^* -> image H^T,        theta:A_3^* -> image H^T (6)
```

are injective throughout the gauge (2), independently of which coloop is
selected.  Indeed, put

```text
L=(ker D_B)^perp,       E=image H^T,       V=H^T(L).
```

Then `dim E=5`, `dim V=3`, and the S2AZ quotient formulas are

```text
p(beta) congruent beta(y)A+mu beta_t B        mod V,
q(gamma) congruent gamma(z)A+gamma(w)B        mod V, (7)
```

where the classes of `A,B` form a basis of `E/V`.  Each quotient map has
rank two by the two independence assumptions in (2).  If

```text
0!=beta_0 in y^perp intersect e_t^perp
```

had `p(beta_0)=0`, contraction in the second root would kill the all-cross
term and every term of `D_B(K)=U`, while the target contraction
`sum_i (beta_0)_i T_i` is nonzero.  This contradicts the complete target
equation.  Thus `p(beta_0)!=0`, adding a third direction above (7).
The identical argument with

```text
0!=gamma_0 in z^perp intersect w^perp
```

proves that `theta` also has rank three.  This proves (6).

For a projective direction `delta=[h:k] in P^1`, define covector planes

```text
P_delta={beta:  k beta(y)-h mu beta_t=0},
Q_delta={gamma: k gamma(z)-h gamma(w)=0}.             (8)
```

The evaluation pairs

```text
(beta(y),mu beta_t),            (gamma(z),gamma(w))  (9)
```

of points in these planes lie on the same line `delta`.  Therefore, for
every `alpha_s=0`, `beta in P_delta`, and `gamma in Q_delta`, the determinant
in the first component of (5) vanishes.  The other two components vanish
because `alpha_s=0`.  The complete target equation is consequently

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i,
alpha_s=0,       beta in P_delta,       gamma in Q_delta. (10)
```

All three row planes in (10) lie in one space of dimension at most three.
To see this, put

```text
R=rho(e_s^perp),                         dim R=2.     (11)
```

The coloop (3) and S2AZ give

```text
H^T(L intersect {alpha_s=0})=R.                      (12)
```

The evaluation-kernel line of `P_delta` is
`y^perp intersect e_t^perp`; the corresponding pure second-root covectors
belong to the space in (12), so their `p` rows lie in `R`.  Similarly, the
evaluation-kernel rows of `Q_delta` lie in `R`.  Choose representatives
`beta_delta,gamma_delta` whose evaluation pairs in (9) are respectively
`(h,k)` and `(-h,-k)`.  Their sum as a root covector belongs to
`L intersect {alpha_s=0}`, hence

```text
p(beta_delta)+q(gamma_delta) in R.                  (13)
```

It follows that

```text
R, p(P_delta), q(Q_delta) subset
S_delta=R+span(p(beta_delta)),       dim S_delta<=3. (14)
```

Injectivity in (6) makes all three displayed row spaces two-planes.
Whenever an inherited obstruction is stated for an ambient three-space and
`dim S_delta=2`, enlarge `S_delta` to any three-space containing it; the row
planes and their complete table are unchanged.

## 2. Two projection determinants and an exact projective fork

Let `I` be the two target colours different from `s`.  A covector plane
with normal `n` projects isomorphically to its two `I` coordinates exactly
when `n_s!=0`.  The normals in (8) therefore give the gates

```text
L_P(h,k)=k y_s-h mu delta_(s,t),
L_Q(h,k)=k z_s-h w_s.                               (15)
```

If both gates are nonzero for some `delta`, choose coordinate lifts
`beta_i in P_delta`, `gamma_i in Q_delta`, `i in I`.  With the basis
`(r_i)_(i in I)` of `R`, equation (10) becomes

```text
per(r_i,p(beta_j),q(gamma_l))
 =delta_(i,j,l) T_i,                 i,j,l in I.     (16)
```

This is the S2AN binary diagonal cube inside the at-most-three-space (14),
and is impossible.  If `S_delta` has dimension two, all three planes agree
and the equal-plane part of the same obstruction applies directly.

Hence, for every `[h:k] in P^1`,

```text
L_P(h,k)L_Q(h,k)=0.                                 (17)
```

The base field has characteristic zero and is infinite, so the homogeneous
quadratic in (17) vanishes identically.  Since the polynomial ring is an
integral domain, one linear factor vanishes identically.  Thus one of

```text
A: s!=t and y_s=0,
B: z_s=w_s=0                                         (18)
```

must hold.  Notice that if `s=t`, the gauge `y_t=0` makes
`L_P=-h mu`, so only `B` is possible.

The two alternatives cannot occur alone.

Suppose first that `A` holds but `B` does not.  Let `c` be the third colour,
different from `s,t`.  The independence of `y,e_t` and the gauge give

```text
y proportional to e_c.                              (19)
```

Choose a direction with `h k L_Q(h,k)!=0`.  Then `P_delta` has a basis

```text
(e_s^*,beta_*),              beta_*_t beta_*_c!=0,  (20)
```

while `Q_delta` projects isomorphically to the `{t,c}` coordinates.  After
choosing coordinate lifts there, (10) has exactly

```text
per(r_t,p(beta_*),q_t')=a_t T_t,
per(r_c,p(beta_*),q_c')=a_c T_c,
a_t a_c!=0,                                           (21)
```

with all other six binary cells zero.  Exchanging the second and third
permanent arguments turns (21) into the S2AO same-third-row binary table.
Its targets are fully transverse, so (21) is impossible.  Therefore

```text
A implies B.                                         (22)
```

Conversely suppose `B` holds but `A` does not.  Then `z,w` are an ordered
basis of `e_s^perp`.  Choose a projective direction for which `L_P!=0` and
whose nonzero normal `kz-hw` has both `I` coordinates nonzero.  This avoids
only finitely many directions.  Now `P_delta` has coordinate lifts, while

```text
Q_delta=span(e_s^*,gamma_*),
              product_(i in I) (gamma_*)_i !=0.     (23)
```

Equation (10) is the same S2AO table, this time with the common third row
`q(gamma_*)`.  It is impossible, proving

```text
B implies A.                                         (24)
```

Together, (18), (22), and (24) leave only `A` and `B` simultaneously.

## 3. A same-pair binary table is impossible

Under `A` and `B`, choose a direction avoiding the finitely many coordinate
directions in both pencils.  With `I={t,c}`, the three row planes in (14)
have bases

```text
R=(r_t,r_c),
P=(p_s,p_*),             Q=(q_s,q_*),                (25)
```

where both `p_*` and `q_*` have nonzero `t,c` coordinate evaluations.
The complete table (10) has exactly two nonzero cells:

```text
per(r_t,p_*,q_*)=b_t T_t,
per(r_c,p_*,q_*)=b_c T_c,             b_t b_c!=0,    (26)

per(r_i,p_j,q_l)=0                  at the other six cells. (27)
```

We isolate the incidence statement that excludes (26)--(27).

### Lemma 1 (same-pair binary obstruction)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field.  Let
`S subset W` have dimension at most three, and let `R,P,Q subset S` be
two-planes with ordered bases

```text
(r_0,r_1),             (p_0,p_1),             (q_0,q_1). (28)
```

There are no nonzero scalars `b_0,b_1` and fully transverse decomposable
tensors `T_0,T_1` such that

```text
per(r_0,p_1,q_1)=b_0 T_0,
per(r_1,p_1,q_1)=b_1 T_1,                           (29)
```

and all other six binary cells vanish.

#### Proof

If `dim S=2`, all three planes agree and the equal-plane argument below
applies.  Assume `dim S=3`.  Choose source-coordinate bases whose first two
lines are the factor lines of `T_0,T_1`; denote their restrictions to `S`
by

```text
xi_i, eta_j, zeta_k in S^*,              i,j,k in {0,1,2}. (30)
```

Let

```text
Res:Sym^3 S^* -> R^* tensor P^* tensor Q^*          (31)
```

be symmetric polarization restricted to `R x P x Q`.  Equations (29) and
the six zeros say that

```text
Res(xi_i eta_j zeta_k)=0                            (32)
```

for every source triple except `(0,0,0)` and `(1,1,1)`.  Those two
exceptions are nonzero.  This source-coordinate zero pattern is independent
of where the two values occur in the row table.

Suppose first that `R,P,Q` are pairwise distinct, with normals
`A,B,C`.  If the normals are independent, direct coefficient comparison
gives

```text
ker Res=span(A^3,B^3,C^3).                          (33)
```

The exact S2AN diagonal-divisor argument now applies.  The two nonzero split
cubics

```text
xi_0 eta_1 zeta_0,            xi_0 eta_1 zeta_1     (34)
```

belong to (33) and share a quadratic factor, so they are proportional and
`zeta_0` is proportional to `zeta_1`.  Applying the same argument to

```text
xi_0 eta_0 zeta_1, xi_0 eta_1 zeta_1,
xi_0 eta_0 zeta_1, xi_1 eta_0 zeta_1                (35)
```

makes `eta_0,eta_1` proportional and `xi_0,xi_1` proportional.  The
nonzero `(0,0,0)` product is then proportional to the zero `(0,0,1)`
product, a contradiction.

If the three distinct normals span a pencil, normalize them to
`A,B,A+B`.  Direct comparison instead gives

```text
ker Res=span(A^3,B^3,AB(A+B))
       subset Sym^3 span(A,B).                       (36)
```

For each nonzero coordinate form in (30), combine it with nonzero forms from
the two target products so that the resulting triple is not a target triple.
The split product belongs to (36), and unique factorization puts each linear
factor in `span(A,B)`.  Thus all source-coordinate forms belong to that
two-plane.  They jointly separate points of the embedded three-space `S`,
so they span `S^*`, a contradiction.

It remains that two planes agree.  If `R=P`, write

```text
p_b=sum_i L_(b,i) r_i,                    L in GL_2. (37)
```

For fixed `q`, let `F_(a,b)=per(r_a,p_b,q)`.  Permanent symmetry implies
that `L F` is symmetric.  At `q_1`, the two independent target coefficients
in (29) make `F` respectively `E_01` and `E_11`.  Symmetry of `L E_01`
forces `L_00=0`, while symmetry of `L E_11` forces `L_01=0`.  The first row
of `L` vanishes, contradicting invertibility.  The case `R=Q` is identical
after exchanging the last two permanent arguments.

Finally suppose `P=Q`, and write

```text
q_c=sum_j L_(c,j) p_j,                    L in GL_2. (38)
```

For each fixed `r_i`, the permanent matrix in the last two arguments is a
multiple of `E_11`.  Symmetry of its left product by `L` forces `L_01=0`,
so `q_0` is proportional to `p_0`.  The zero mixed cells then give

```text
per(r_i,p_1,q_1)=L_11 per(r_i,p_1,p_1),       i=0,1. (39)
```

Thus the square map `per(-,p_1,p_1)|R` contains both fully transverse
targets `T_0,T_1`.  This contradicts the S2AL tangent-line separation lemma.
The equal-plane and pairwise-distinct cases exhaust all plane incidences,
proving the lemma.  QED.

Equations (25)--(27) satisfy Lemma 1, the final contradiction.  Therefore
the coloop (3) is impossible.

## 4. Proof-topology consequence

The live `(1,2,2)` rank-five frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE;

other seven coordinate coloops / joint rank <=4
  / other components / higher m:                    OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.      (40)
```

No finite scan, numerical specialization, generic-point promotion, target
factor-sharing assumption, or unproved case cover enters the argument.  The
choices avoiding finitely many projective directions use only that every
characteristic-zero field is infinite.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_alpha_s_coloop_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_alpha_s_coloop_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_alpha_s_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_alpha_s_coloop_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_alpha_s_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_alpha_s_coloop_exclusion.py
```

The primary replay checks the determinant-face identity, both projection
gates, the homogeneous-polynomial fork, all four binary target tables, the
independent-normal and pencil-normal cubic kernels, and all three equal-plane
orientations.  The independent audit imports no repository module or
third-party package; it uses standard-library rational arithmetic, a reversed
cubic coefficient order, and separate exact elimination.  The scripts replay
the displayed identities; the arbitrary-field projective and incidence
arguments are the proof above.

## Dependencies

- [`(1,2,2)` coordinate-coloop localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COORDINATE_COLOOP_LOCALIZATION_THEOREM.md)
- [Support-one higher-row-rank exclusion and tangent-line separation](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
- [Repeated-coordinate binary-diagonal obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_LOCALIZATION_THEOREM.md)
- [Repeated-coordinate same-third-row obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_SUPPORT_LOCALIZATION_THEOREM.md)
