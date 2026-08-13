# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` residual second-root-coloop `s=t` endpoint exclusion

## Status

**Exact characteristic-zero exclusion of the `s=t` slice of every residual
second-root coordinate-coloop endpoint on the normalized, target-consistent
physical `m=3` common-three-space full-sensor stratum.**  Retain

```text
dim U=3,                         rank H=5,

ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2,                     (1)
```

and suppose the coordinate-coloop fork selects

```text
N=K^perp subset {beta_j=0},                   j!=t.  (2)
```

Let `k` be the third colour.  S2BE--S2BF give

```text
w is proportional to e_j or e_k,                    (3)
```

together with an exact support table.  Under either endpoint in (3),

```text
s=t                                               is impossible. (4)
```

Equivalently every surviving residual second-root-coloop endpoint satisfies

```text
s in {j,k}.                                          (5)
```

The proof strengthens S2BE's same-third-row obstruction.  Its middle-row
plane may now meet the common three-space in an arbitrary nonzero line; the
intersection need not be one of the two target-indexed rows.  The genuinely
non-coordinate case has 14 endpoint-support, five generic fixed-support, and
two polynomial one-parameter row-space families.  All 21 have pinned exact
rational Nullstellensatz identities.

This excludes only the `s=t` endpoint slice.  It does not exclude either
residual coloop, any endpoint with `s in {j,k}`, the three third-root
coloops, the two complementary first-root coloops, joint rank at most four,
other physical components, higher orders, or the global conjecture.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. An arbitrary middle-plane intersection still cannot carry a same-third-row table

### Lemma 1 (intersecting-middle-plane same-third-row obstruction)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field.  Let
`S subset W` be a three-space.  Suppose

```text
R=span(r_0,r_1),       Q=span(q_0,q_1) subset S
```

are two-planes and `P=span(p_0,p_1)` is a two-plane satisfying

```text
P intersect S !=0.                                  (6)
```

There are no nonzero scalars `c_0,c_1` and fully transverse decomposable
tensors `T_0,T_1` such that

```text
per(r_0,p_0,q_0)=c_0T_0,
per(r_1,p_1,q_0)=c_1T_1,                            (7)

per(r_a,p_b,q_c)=0                 at the other six binary cells. (8)
```

#### Proof: old coordinate intersections

If `P subset S`, S2AO's three-space same-third-row obstruction applies.  If
`P intersect S` is `span(p_0)` or `span(p_1)`, S2BE Lemma 1 applies after
interchanging binary labels if necessary.  It remains that

```text
P intersect S=span(a p_0+b p_1),          ab!=0.   (9)
```

Independent rescaling of the two target-indexed middle rows, with the
induced nonzero changes absorbed in `c_0,c_1`, normalizes (9) to

```text
P intersect S=span(p_0+p_1).                        (10)
```

#### Proof: first/third-plane incidence

The incidence reduction in S2BE Lemma 1 does not use which row of `P` lies
in `S`.  If `R=Q`, permanent symmetry at `p_0` and `p_1` makes the relevant
change matrix singular.  If `R!=Q`, choose

```text
ell=a_0r_0+a_1r_1=b_0q_0+b_1q_1
```

on their intersection line.  Equations (7)--(8) give

```text
M_(ell,ell)(p_0)=a_0b_0c_0T_0,
M_(ell,ell)(p_1)=a_1b_0c_1T_1.                     (11)
```

If `b_0a_0a_1!=0`, the square map contains two fully transverse targets,
contrary to S2AL tangent-line separation.  If `b_0!=0` and one `a_i`
vanishes, the square map on the coordinate row and its mixed map with the
other row have nonzero rank-one images on fully transverse targets,
contrary to S2AL mixed factor sharing.  Hence `b_0=0` and

```text
R intersect Q=span(q_1).                             (12)
```

Thus the zero third row is the plane-intersection line exactly as in S2BE.

#### Proof: the 21 generic-middle-line families

Choose a basis of `S'=S direct-sum span(p_0)` so that

```text
r_0=e_0,       r_1=e_1,       q_0=e_2,       p_0=e_3. (13)
```

By (12), write

```text
q_1=a e_0+b e_1,                    (a,b)!=(0,0).
```

The nonzero intersection vector `p_0+p_1` belongs to `S`, so write

```text
p_0+p_1=c e_0+d e_1+f e_2,         (c,d,f)!=(0,0,0).
                                                               (14)
```

The same diagonal row-space action used in S2BE classifies the ordered pair
in (14).  If `ab=0`, normalize `q_1` to `e_0` or `e_1`; the intersection
row has seven nonempty support masks.  This gives

```text
2*7=14 endpoint-support families.                  (15)
```

If `ab!=0`, normalize `q_1=e_0+e_1`.  When at most one of `c,d` is nonzero,
the possible fixed masks are

```text
1,2,4,5,6,                       five families.     (16)
```

When `cd!=0`, retain the genuine invariant parameter:

```text
p_0+p_1=e_0+tau e_1
                   or e_0+tau e_1+e_2,       tau!=0. (17)
```

These are two polynomial one-parameter families.  In every case, `p_1` is
the displayed intersection row minus `e_3`; no escaping coordinate is
dropped.

Choose source-coordinate bases whose first two factor lines are those of
`T_0,T_1`.  Restrict their six selected coordinate forms to `S'` and expand
the polarized permanent at all eight selected source triples and all eight
binary row triples.  Set the coefficient to one only at

```text
(source;row)=(000;000),              (111;110),      (18)
```

and to zero at the other 62 positions.  Every realization of (7)--(8)
would solve these 64 necessary cubic equations.

For all 21 families, the durable certificate gives an exact identity

```text
1=sum_(nu=1)^64 h_nu f_nu.                           (19)
```

The identities contain 44,806 sparse multiplier terms.  Their SHA-256 is

```text
ceb0c69b151523c43219d294806d50a1e1b2905bc7237c6a3709451fc868b9a0. (20)
```

The two parameter identities are polynomial in `tau`; they use no inverse,
saturation, or specialization, and hold at every parameter value over every
characteristic-zero field.  Both replay programs reconstruct all 64
generators in every family before checking (19).  The independent audit
reverses all 25 variables and uses a separate standard-library sparse
permanent expansion.  Thus (9) is impossible, completing Lemma 1.  QED.

## 2. The `s=t` endpoint pencil gives Lemma 1

Use the row notation

```text
r_i=rho(e_i^*),       p_i=pi(e_i^*),
q_i=theta(e_i^*),     T_i=X_i tensor Y_i tensor Z_i.
```

S2BF proves that for every determinant-pencil direction
`delta=[h:kappa]`, the row planes

```text
R=rho(e_s^perp),             q(Q_delta)
```

and a nonzero line of `p(P_delta)` lie in one space `S_delta` of dimension
at most three.  S2BC proves `pi` and `theta` injective, so all displayed
planes and the intersection line are genuine.  Enlarge `S_delta` to a
three-space if necessary.

Assume for contradiction that `s=t` and absorb the endpoint scalar in (3):

```text
w=e_l,                  {l,m}={j,k}.                (21)
```

S2BF gives `z_t=w_t=0`.  Independence of `z,w` therefore makes them a basis
of `e_t^perp`.  The pencil planes are

```text
P_delta={beta:kappa beta(y)-h mu beta_t=0},
Q_delta={gamma:kappa gamma(z)-h gamma(w)=0}.        (22)
```

Choose a projective direction satisfying

```text
h!=0,
Q_delta=span(e_t^*,gamma_*),
(gamma_*)_j (gamma_*)_k!=0.                         (23)
```

Such a direction exists.  The normals `kappa z-hw` run projectively through
every line of `e_t^perp`; their annihilator lines do the same.  Conditions
(23) remove only the direction `h=0` and the two coordinate annihilator
lines from the infinite projective line.

Because `s=t` and `y_t=0`, the first projection gate is

```text
L_P(h,kappa)=-h mu!=0.                              (24)
```

Thus `P_delta` has coordinate lifts `beta^j,beta^k` over the two colours
`j,k`.  The gauge-fixed derivative transpose vanishes on

```text
alpha_t=0,       beta in P_delta,       gamma in Q_delta,
```

so the complete target equation gives, for `a,b in {j,k}`,

```text
per(r_a,p(beta^b),q(gamma_*))
   =delta_(a,b) (gamma_*)_a T_a,

per(r_a,p(beta^b),q_t)=0.                           (25)
```

The two coefficients in the first line are nonzero by (23), and `T_j,T_k`
are fully transverse.  Equation (25) is exactly the same-third-row table
(7)--(8).  Its first- and third-row planes lie in `S_delta`, while S2BF
supplies the nonzero middle-plane intersection.  Lemma 1 contradicts (25).
Therefore `s=t` is impossible, proving (4)--(5).

## 3. Proof-topology consequence

The live `(1,2,2)` rank-five coloop frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);

beta_j coloop, j!=t:
  w=e_l, l in {j,k}, s=t:                          IMPOSSIBLE;
  w=e_l, l in {j,k}, s in {j,k},
    subject to the S2BF endpoint table:             OPEN;

three gamma_k coloops / two complementary alpha coloops
  / joint rank <=4 / other components / higher m:  OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.     (26)
```

No surviving endpoint is asserted to exist.  No finite-field scan,
numerical specialization, bounded parameter sample, generic-point promotion,
or unproved orbit cover enters the proof.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_exclusion.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_certificates.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_exclusion.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_certificates.py
```

The primary replay uses SymPy rational polynomials.  The independent audit
imports no repository module or third-party package.  Optional deterministic
certificate regeneration requires Singular 4.x and deliberately reuses the
predecessor's proved 21-family emitter with the exact row replacement
`p_1 -> p_1-e_3`:

```text
python claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_s_equal_t_endpoint_certificates.py
```

Singular is not needed for either replay.

## Dependencies

- [`(1,2,2)` residual second-root-coloop projective-pencil localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` residual second-root coordinate-line localization and same-third-row incidence](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COORDINATE_LINE_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` determinant-face pencil and `pi,theta` injectivity](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md)
- [Tangent-line and mixed-factor-sharing lemmas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#2-two-exact-two-plane-lemmas)
