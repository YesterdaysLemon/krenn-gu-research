# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` third-root-coloop exclusion

## Status

**Exact characteristic-zero exclusion of all three third-root coordinate
coloops on the normalized, target-consistent physical `m=3`
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

Let `N=K^perp`, where `K=image H`, and suppose the coordinate-coloop fork
selects

```text
N subset {gamma_k=0}                                  (3)
```

for any `k in {0,1,2}`.  Then (3) is impossible.

The proof uses no new finite search.  The complete derivative-zero face

```text
beta_t=0,                         gamma(w)=0           (4)
```

puts its first and second binary row planes in one exact three-space, while
the third plane has a nonzero intersection with that space.  If `w_t!=0`,
the face is the independently certified S2BF arbitrary-intersection binary
diagonal table.  If `w_t=0` and `w` has both complementary coordinates, it
is the independently certified S2BI common-active-row table.  If `w` is a
coordinate vector, exchanging roots two and three turns (3) into one of the
three second-root coloops already excluded by S2BB and S2BJ.

Together with S2BB, S2BC, and S2BJ, this closes seven of the nine
`(1,2,2)` coordinate-coloop orientations.  The two complementary first-root
coloops `alpha_a,alpha_b`, joint rank at most four, other physical component
types, pole strata, higher orders, and global resolution remain open.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The third-root coloop gives an intersecting face

Write

```text
r_i=rho(e_i^*),       p_i=pi(e_i^*),       q_i=theta(e_i^*),

A=lambda^(-1)r_s,     B=mu^(-1)p_t,
R=rho(e_s^perp),      S=R direct-sum span(A).        (5)
```

Let

```text
L=(ker D_B)^perp,       E=image H^T,       V=H^T(L). (6)
```

S2AZ and the target-contraction argument used in S2BC give

```text
dim E=5,             dim V=3,             dim R=2,
[A],[B] a basis of E/V,
rho, pi, theta injective.                              (7)
```

In particular `A` is not in `V`, so `S` in (5) has dimension three and
contains every first-root row.  Under (3), the S2AZ coloop fork says

```text
H^T(L intersect {gamma_k=0})=R.                     (8)
```

For every `beta in e_t^perp`, the covector

```text
(-lambda^(-1)beta(y)e_s^*, beta, 0)                 (9)
```

belongs to the space in (8).  Hence

```text
p(beta)-beta(y)A in R,             beta_t=0.        (10)
```

Likewise, for every

```text
gamma in w^perp intersect e_k^perp,                 (11)
```

the covector

```text
(-lambda^(-1)gamma(z)e_s^*,0,gamma)                 (12)
```

belongs to the space in (8), and therefore

```text
q(gamma)-gamma(z)A in R.                            (13)
```

The intersection in (11) is nonzero because it is the intersection of two
planes in a three-dimensional covector space.  Injectivity in (7) preserves
that nonzero row.  Consequently the three row planes

```text
R_t=rho(e_t^perp),       P_t=pi(e_t^perp),
Q_w=theta(w^perp)                                      (14)
```

are genuine two-planes and satisfy

```text
R_t subset S,             P_t subset S,
Q_w intersect S !=0.                                  (15)
```

No claim that `Q_w` itself lies in `S` is used.

## 2. The complete derivative-zero face

The gauge-fixed derivative transpose is

```text
D_B^T(alpha tensor beta tensor gamma)
 =((beta(y)gamma(w)-mu beta_tgamma(z))alpha,
   -lambda alpha_sgamma(w)beta,
    lambda mu alpha_sbeta_tgamma).                   (16)
```

Thus (4) annihilates the derivative without imposing the equations of `L`.
Since `U=D_B(K)`, the complete target equation on this whole product face is

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i,
 beta_t=0,                         gamma(w)=0.       (17)
```

This is a polynomial identity on the displayed linear spaces, not a sample
or a generic-point assertion.

### 2.1. The case `w_t!=0`

Let `{a,b}` be the two colours different from `t`.  Restriction to those
coordinates is an isomorphism

```text
w^perp -> span(e_a,e_b)^*.                           (18)
```

Its coordinate lifts are

```text
gamma^i=e_i^*-(w_i/w_t)e_t^*,          i in {a,b}.  (19)
```

Put `q'_i=q(gamma^i)`.  Substituting coordinate first- and second-root
covectors into (17) gives the complete binary diagonal frame

```text
per(r_i,p_j,q'_ell)=
  T_i,                         i=j=ell,
  0,                           otherwise,

i,j,ell in {a,b}.                                  (20)
```

By (14)--(15), its first and second row planes lie in the exact three-space
`S`, while its third row plane meets `S` in a nonzero line.  Permute the
second and third arguments of the permanent.  Equation (20) is precisely
S2BF Lemma 1, the arbitrary-intersection binary-diagonal obstruction.  Its
28 exact rational certificate cases exclude (20).  Therefore

```text
w_t!=0                                               IMPOSSIBLE. (21)
```

### 2.2. The case `w_t=0` with complementary support two

Now write

```text
w=w_a e_a+w_b e_b,                w_aw_b!=0.        (22)
```

The covectors

```text
n=w_b e_a^*-w_a e_b^*,              e_t^*           (23)
```

form a basis of `w^perp`.  Put `q'=q(n)`.  Equation (17) gives

```text
per(r_a,p_a,q')= w_b T_a,
per(r_b,p_b,q')=-w_a T_b,                            (24)

per(r_i,p_j,q')=0                         for i!=j,
per(r_i,p_j,q_t)=0                       for all i,j in {a,b}. (25)
```

Thus the two fully transverse targets share the active third row, and the
other six binary cells vanish.  The first and second row planes lie in `S`;
the third plane meets `S` by (15).  After permuting permanent arguments,
(24)--(25) are exactly S2BI Lemma 1.  That lemma includes all three possible
positions of the intersection line in the escaping ordered plane, so it
does not matter whether the in-space line is the active row, the zero row,
or their generic combination.  Its 90 exact rational certificate cases
exclude (24)--(25).  Hence

```text
w_t=0, w_aw_b!=0                                    IMPOSSIBLE. (26)
```

## 3. A coordinate `w` becomes a closed second-root coloop

The only remaining possibility has

```text
w=nu e_v,                    v!=t,       nu!=0.      (27)
```

Exchange roots two and three.  The derivative kernel becomes

```text
span{(lambda e_s,z,y),(0,nu e_v,mu e_t)}.           (28)
```

This is again the S2AZ `(1,2,2)` profile, now with

```text
y'=z,          z'=y,          c'=nu e_v,
w'=mu e_t.                                            (29)
```

The exact kernel-generator gauge replaces

```text
(lambda e_s,y',z')
 by
(lambda e_s,
 y'-(y'_v/nu)c',
 z'-(y'_v/nu)w'),                                    (30)
```

so the new `v` coordinate of `y'` is zero and all Hilbert--Burch blocks are
unchanged.  The two projected pairs remain independent.  Root exchange
preserves the target equation, full transversality, `dim U`, `rank H`, and
the relation kernel.  It sends

```text
N subset {gamma_k=0}
    to
N' subset {beta'_k=0}.                               (31)
```

If `k=v`, (31) is the distinguished second-root coloop excluded by S2BB.
If `k!=v`, it is one of the two residual second-root coloops excluded by
S2BJ.  Therefore (27) is impossible in every selected orientation.

Because `w!=0` by (2), the cases (21), (22), and (27) exhaust all `w`.
This proves that every coloop in (3) is impossible.  QED.

## 4. Proof-topology consequence

The live `(1,2,2)` rank-five coloop frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);
both residual beta_j coloops:                       IMPOSSIBLE (S2BJ);
all three gamma_k coloops:                          IMPOSSIBLE;

two complementary alpha coloops / joint rank <=4
  / other components / pole strata / higher m:     OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.   (32)
```

The theorem transfers two already proved permanent obstructions and the
already closed second-root orientations.  It does not infer a new
certificate, strengthen an intersection line to plane containment, or
claim anything about either complementary first-root coloop.

## Focused replay

Run from repository root:

```bash
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_third_root_coloop_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_third_root_coloop_exclusion.py

uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py

uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_localization.py

python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_third_root_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_third_root_coloop_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_third_root_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_third_root_coloop_exclusion.py
```

The new primary replay checks the derivative-zero face, the exact coloop
row-space transfer, both complete binary tables, the root-exchange gauge,
and the two dependency certificate pins.  The new independent audit imports
no repository module or third-party package; it reconstructs the canonical
five-dimensional row model and both target tables with `Fraction`
arithmetic, checks the root exchange separately, and recomputes the pins.

The inherited S2BF certificate contains 28 polynomial normal forms and has
SHA-256

```text
0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca.
```

The inherited S2BI certificate contains 90 polynomial normal forms and has
SHA-256

```text
a56242675744f848fc4f747045ce9b2a18c7b32ae2152ca800bd6c654d29e8d1.
```

Their own primary and independent replays remain the proof evidence for the
two computational lemmas; the new scripts audit the exact transfer into
those lemmas.

## Dependencies

- [`(1,2,2)` coordinate-coloop localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COORDINATE_COLOOP_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` `beta_t`-coloop coordinate-endpoint exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_BETA_T_COLOOP_COORDINATE_ENDPOINT_EXCLUSION_THEOREM.md)
- [`(1,2,2)` `alpha_s`-coloop exclusion and row injectivity](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md)
- [`(1,2,2)` residual second-root-coloop projective-pencil localization and arbitrary-intersection binary obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` residual second-root-coloop common-middle-row obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COMMON_MIDDLE_ROW_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` residual second-root-coloop exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_EXCLUSION_THEOREM.md)
