# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` complementary first-root-coloop exclusion

## Status

**Exact characteristic-zero exclusion of both complementary first-root
coordinate coloops on the normalized, target-consistent physical `m=3`
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

Let `N=K^perp`, where `K=image H`.  For either colour `a!=s`, the
coordinate-coloop alternative

```text
N subset {alpha_a=0}                                 (3)
```

is impossible.

The proof extends the S2BC determinant-face pencil to the case where the
first row plane need only intersect the common three-space.  The S2BF
arbitrary-intersection binary-diagonal obstruction forces one of two exact
linear degeneracies.  If only one degeneracy holds, the S2BE one-row-escape
same-third-row obstruction applies.  At their common degeneration, the
selected coloop supplies a two-plane containing the inactive middle and
third rows, their active-row sum, and the in-space first row.  Equal partner
planes fail by the S2AL square-image lemma; otherwise five exact row-space
normal forms exhaust the residual, and each has a pinned rational
Nullstellensatz identity.

Together with S2BB, S2BC, S2BJ, and S2BK, this closes all nine S2AZ
coordinate-coloop orientations and therefore the complete joint-rank-five
Hilbert--Burch `(1,2,2)` profile.  Joint rank at most four, other physical
component types, pole strata, higher orders, and global resolution remain
open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The complementary coloop gives an intersecting pencil

Let `b` be the third colour, so

```text
{s,a,b}={0,1,2},                   a!=s.             (4)
```

Write

```text
r_i=rho(e_i^*),       p_i=pi(e_i^*),       q_i=theta(e_i^*),
T_i=X_i tensor Y_i tensor Z_i.                       (5)
```

Let

```text
L=(ker D_B)^perp,       E=image H^T,       V=H^T(L). (6)
```

S2AZ gives `dim E=5`, `dim V=3`, and a two-dimensional image for every
selected coordinate-coloop hyperplane.  Put

```text
C=H^T(L intersect {alpha_a=0}),             dim C=2. (7)
```

The target-contraction arguments used in S2BA--S2BC make `rho`, `pi`, and
`theta` injective.  For `rho`, S2AZ proves injectivity on `e_s^perp`, while
`r_s` has the nonzero quotient class `lambda A` outside the resulting
two-plane.  Thus all row planes below are genuine.

For a projective direction `delta=[h:kappa]`, define

```text
P_delta={beta: kappa beta(y)-h mu beta_t=0},
Q_delta={gamma:kappa gamma(z)-h gamma(w)=0}.          (8)
```

The gauge-fixed derivative transpose is

```text
D_B^T(alpha tensor beta tensor gamma)
 =((beta(y)gamma(w)-mu beta_tgamma(z))alpha,
   -lambda alpha_sgamma(w)beta,
    lambda mu alpha_sbeta_tgamma).                   (9)
```

If `alpha_s=0`, `beta in P_delta`, and `gamma in Q_delta`, the matched
evaluation pairs in (8) make the first component of (9) vanish, while the
other two components already contain `alpha_s`.  Direct substitution into
(9) therefore gives the complete target identity

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i,

alpha_s=0,       beta in P_delta,       gamma in Q_delta. (10)
```

For clarity, the determinant in the first component is

```text
beta(y)gamma(w)-mu beta_tgamma(z),                  (11)
```

and it vanishes on (8) without imposing the equations defining `L`.  No
sampled direction or generic identity is being asserted.

The row spaces in (10) have a stronger incidence than arbitrary planes.
The pure root covector `(e_b^*,0,0)` belongs to the space in (7), so

```text
r_b in C.                                            (12)
```

The evaluation-kernel lines of `P_delta` and `Q_delta` have zero evaluation
pairs.  Their pure second- and third-root covectors belong to (7), so their
row images lie in `C`.  Choose representatives `beta_delta,gamma_delta`
with opposite nonzero evaluation pairs.  Then

```text
(0,beta_delta,gamma_delta)
       in L intersect {alpha_a=0},

p(beta_delta)+q(gamma_delta) in C.                  (13)
```

It follows that

```text
p(P_delta),q(Q_delta) subset
S_delta=C+span(p(beta_delta)),       dim S_delta<=3. (14)
```

The coordinate first-row plane of the derivative-zero face

```text
R=rho(e_s^perp)=span(r_a,r_b)                       (15)
```

meets `S_delta` nontrivially by (12), but need not be contained in it.  This
is the exact one-plane-intersection geometry used below.

## 2. The projective gate fork

Let `I={a,b}`, the two colours different from `s`.  The normal covectors in
(8) project isomorphically to their `I` coordinates exactly when their
`s` coordinates are nonzero.  The two gates are

```text
L_P(h,kappa)=kappa y_s-h mu delta_(s,t),
L_Q(h,kappa)=kappa z_s-h w_s.                       (16)
```

If both gates are nonzero at one projective direction, choose their
coordinate lifts `beta_i,gamma_i`, `i in I`.  Equation (10) gives

```text
per(r_i,p(beta_j),q(gamma_l))
 =delta_(i,j,l) T_i,                 i,j,l in I.     (17)
```

The middle and third row planes lie in `S_delta`, while the first plane
meets it by (12).  After permuting permanent arguments, (17) is exactly the
S2BF arbitrary-intersection binary-diagonal obstruction.  Its 28 rational
certificate cases exclude (17).  Hence

```text
L_P(h,kappa)L_Q(h,kappa)=0
                    for every [h:kappa] in P^1.     (18)
```

The field is infinite and the homogeneous quadratic in (18) vanishes
identically.  Since the polynomial ring is an integral domain, one linear
factor vanishes identically.  Thus one of

```text
A: s!=t and y_s=0,
B: z_s=w_s=0                                         (19)
```

must hold.  If `s=t`, the gauge makes `L_P=-h mu`, so only `B` can occur.

Neither alternative can hold alone.

Suppose `A` holds but `B` does not.  Since `s!=t`, `y_s=y_t=0` and the
independence of `y,e_t` makes `y` proportional to the third coordinate.
Choose a direction avoiding the coordinate directions and `L_Q=0`.  Then

```text
P_delta=span(e_s^*,beta_*),
Q_delta=span(gamma_a,gamma_b),                      (20)
```

where `beta_*` has both `I` coordinates nonzero and the gamma rows are
coordinate lifts.  The only nonzero cells of (10) are

```text
per(r_a,p(beta_*),q(gamma_a))=c_a T_a,
per(r_b,p(beta_*),q(gamma_b))=c_b T_b,
c_ac_b!=0.                                           (21)
```

The partner planes in (21) lie in `S_delta`, and `r_b` is the in-space row
of the possibly escaping first plane.  Permuting arguments turns (21) into
S2BE Lemma 1, the one-row-escape same-third-row obstruction.  Its complete
21-family rational certificate excludes (21).  Therefore

```text
A implies B.                                         (22)
```

If `B` holds but `A` does not, choose a direction for which `P_delta`
projects isomorphically and whose nonkernel row of `Q_delta` has both `I`
coordinates nonzero.  The identical table now shares the active third row;
another permutation gives S2BE Lemma 1.  Thus

```text
B implies A.                                         (23)
```

Only the common degeneration `A` and `B` remains.

## 3. The common degeneration

Assume both alternatives in (19).  Choose a projective direction away from
the finitely many coordinate directions.  Then

```text
P_delta=span(e_s^*,beta_*),
Q_delta=span(e_s^*,gamma_*),                        (24)
```

where the active rows have nonzero coordinates at both colours in `I`.
Choose their evaluation pairs oppositely as in (13).  Put

```text
p_0=p_s,       p_1=p(beta_*),
q_0=q_s,       q_1=q(gamma_*).                      (25)
```

The coloop plane gives the exact incidences

```text
r_b,p_0,q_0,p_1+q_1 in C.                           (26)
```

The complete binary table has only

```text
per(r_a,p_1,q_1)=d_a T_a,
per(r_b,p_1,q_1)=d_b T_b,             d_a d_b!=0,  (27)
```

with the other six cells zero.

### 3.1. Partner-plane and all-in-space boundaries

If `p_1 in C`, equation (26) also gives `q_1 in C`.  Injectivity makes both
partner planes equal `C`.  Write

```text
q_j=sum_l L_(j,l)p_l,                   L in GL_2. (28)
```

For either fixed first row, the `P x Q` permanent matrix in (27) is a
nonzero multiple of `E_11`.  Converting the `Q` basis to the `P` basis and
using permanent symmetry forces `q_0` to be proportional to `p_0`.  The
zero mixed cells then give

```text
per(r_i,p_0,p_1)=0,
per(r_i,p_1,p_1)=d'_i T_i,             i in I,       (29)
```

with both `d'_i` nonzero.  The square map
`per(-,p_1,p_1)|R` therefore contains two fully transverse decomposable
tensors, contrary to S2AL Lemma 1.  Hence

```text
p_1,q_1 notin C.                                      (30)
```

Put

```text
S=C direct-sum span(p_1),                 dim S=3.   (31)
```

Equation (26) gives `q_1 in S`, so both partner planes lie in `S`.  If
`r_a in S`, all three row planes lie in one three-space and the S2BC
same-pair lemma excludes (27).  It remains that

```text
r_a notin S,                  R intersect S=span(r_b). (32)
```

### 3.2. Five exact normal forms

Choose a basis of `S+span(r_a)` with

```text
C=span(e_0,e_1),        p_1=e_2,        r_a=e_3.    (33)
```

The inactive rows `p_0,q_0` are nonzero lines of `C`.  There are two exact
incidence types.

If their lines agree, normalize

```text
p_0=q_0=e_0.                                        (34)
```

The stabilizer of this line has two orbits on the nonzero line `span(r_b)`:

```text
r_b=e_0                         or        r_b=e_1.  (35)
```

If the inactive lines differ, normalize

```text
p_0=e_0,                         q_0=e_1.            (36)
```

The diagonal stabilizer leaves three support types:

```text
r_b=e_0,                  r_b=e_1,                  r_b=e_0+e_1. (37)
```

Finally (26) has the polynomial normal form

```text
q_1=-e_2+c_0e_0+c_1e_1,             c_0,c_1 arbitrary. (38)
```

Equations (34)--(38) give exactly

```text
2+3=5                                                    (39)
```

normal forms.  There is no nonzero parameter to invert, no sample, and no
missing coincidence boundary.

Choose source-coordinate bases whose first two factor lines are those of
`T_a,T_b`.  Restrict their six selected coordinate forms to the four-space
in (33).  For all eight selected source triples and all eight binary row
triples, expand the polarized permanent.  Normalize the two nonzero target
coefficients to one.  The required values are one exactly at

```text
(source;row)=(000;011),              (111;111),      (40)
```

and zero at the other 62 positions.

For all five normal forms, the durable certificate gives an exact rational
identity

```text
1=sum_(nu=1)^64 h_nu f_nu.                           (41)
```

The identities are polynomial in `c_0,c_1`, contain 5,928 sparse multiplier
terms, and have SHA-256

```text
10ce1216ed2360159eb4709140eabe4db1c51ad509f340ac137300a636583088. (42)
```

The primary verifier reconstructs all 64 cubic generators in every case
with SymPy.  The independent audit reverses all 26 certificate variables,
imports no repository module or third-party package, and rebuilds every
permanent with standard-library `Fraction` sparse arithmetic.  Thus (41)
remains a unit-ideal identity after scalar extension to every
characteristic-zero field and excludes all five cases.

This contradicts (3) for arbitrary `a!=s`, so both complementary first-root
coloops are impossible.  QED.

## 4. Proof-topology consequence

The complete `(1,2,2)` rank-five coloop frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);
both residual beta_j coloops:                       IMPOSSIBLE (S2BJ);
all three gamma_k coloops:                          IMPOSSIBLE (S2BK);
both complementary alpha_a,alpha_b coloops:         IMPOSSIBLE;

complete Hilbert--Burch (1,2,2) profile:            IMPOSSIBLE;

joint rank <=4 / other components / pole strata
  / higher m:                                       OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.   (43)
```

No claim is made about a lower-rank branch, another physical component,
another pole stratum, higher order, or global resolution.

## Focused replay

Run from repository root:

```bash
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_exclusion.py

uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_projective_pencil_localization.py

uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_coordinate_line_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_coordinate_line_localization.py

python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_exclusion.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_certificates.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_exclusion.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_certificates.py
```

The new primary replay checks the pencil and coloop-plane geometry, both
one-sided target tables, the complete five-case cover, the equal-plane
square boundary, every new rational certificate identity, and both inherited
certificate pins.  The independent audit reconstructs the five systems and
the two one-sided tables separately before replaying the identities.

The generator requires Singular 4.x.  Regeneration is optional for proof
replay:

```bash
python claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_complementary_first_root_coloop_certificates.py
```

## Dependencies

- [`(1,2,2)` coordinate-coloop localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COORDINATE_COLOOP_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` `alpha_s`-coloop exclusion and determinant pencil](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md)
- [`(1,2,2)` residual second-root-coloop arbitrary-intersection binary obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` residual second-root-coloop one-row-escape same-third-row obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COORDINATE_LINE_LOCALIZATION_THEOREM.md)
- [Tangent-line separation and square-image obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#2-two-exact-two-plane-lemmas)
