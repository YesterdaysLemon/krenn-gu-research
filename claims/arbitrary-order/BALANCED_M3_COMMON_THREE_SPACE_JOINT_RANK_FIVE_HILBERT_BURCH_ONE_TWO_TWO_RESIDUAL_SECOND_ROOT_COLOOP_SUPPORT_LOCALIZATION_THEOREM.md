# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` residual second-root-coloop support localization

## Status

**Exact characteristic-zero support localization for both residual
second-root coordinate-coloop orientations in the normalized,
target-consistent physical `m=3` common-three-space full-sensor stratum.**
Retain

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
N subset {beta_j=0},                    j!=t.         (3)
```

Then

```text
w_t=0.                                                  (4)
```

The proof exposes a binary diagonal permanent table.  Two of its row planes
lie in the exact three-space `S=R direct-sum span(A)`, and one specified row
of the third plane lies in `S`; the other row may escape.  A new exact
four-dimensional obstruction excludes precisely this one-row escape.  Its
human incidence reduction leaves four endpoint incidences and seven nonzero
support masks.  All `4*7=28` normal forms have pinned rational
Nullstellensatz identities.

This is a localization, not an exclusion of either coloop in (3).  The
`w_t=0` residuals, all three third-root coloops, the two complementary
first-root coloops, joint rank at most four, other physical component types,
higher orders, and the global conjecture remain open.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. The residual coloop puts five needed rows in one three-space

Write

```text
r_i=rho(e_i^*),       p_i=pi(e_i^*),
q_i=theta(e_i^*),     T_i=X_i tensor Y_i tensor Z_i,

A=lambda^(-1)r_s,     B=mu^(-1)p_t,
R=rho(e_s^perp).                                      (5)
```

Let `L=(ker D_B)^perp`, `E=image H^T`, and `V=H^T(L)`.  S2AZ gives

```text
dim E=5,                   dim V=3,                  dim R=2,

E/V=span([A],[B]),         [A],[B] independent.      (6)
```

In particular `A` is not in `V`, while `R subset V`, so

```text
S=R direct-sum span(A),                 dim S=3.      (7)
```

All first-root rows lie in `S`, and `rho` is an isomorphism onto `S`: its
restriction to `e_s^perp` is injective by S2AZ, while `r_s=lambda A` is
outside `R`.

Let `k` be the third colour, so `{j,k,t}={0,1,2}`.  Under (3), S2AZ gives

```text
H^T(L intersect {beta_j=0})=R.                       (8)
```

The root covectors

```text
(-lambda^(-1)y_k e_s^*, e_k^*, 0),

(-lambda^(-1)z_m e_s^*,
 -mu^(-1)w_m e_t^*, e_m^*),             m=0,1,2,    (9)
```

belong to `L intersect {beta_j=0}`.  Here the gauge `y_t=0` is used in the
second line.  Applying (8) gives

```text
p_k-y_k A in R,
q_m-z_m A-w_m B in R,                    m=0,1,2.    (10)
```

Consequently

```text
p_k in S,                  q(w^perp) subset S.       (11)
```

No corresponding conclusion is available for `p_j`: this is the exact
one-row escape that distinguishes (3) from the already closed
distinguished `beta_t` coloop.

The gauge-fixed derivative transpose is

```text
D_B^T(alpha tensor beta tensor gamma)
 =((beta(y)gamma(w)-mu beta_t gamma(z))alpha,
   -lambda alpha_s gamma(w) beta,
    lambda mu alpha_s beta_t gamma).                 (12)
```

Thus the entire product face

```text
beta_t=0,                         gamma(w)=0          (13)
```

annihilates the derivative.  Since `U=D_B(K)`, the complete target equation
on this face is

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i.                  (14)
```

This is an identity on the complete displayed product of linear spaces,
not a finite sample or a generic-point statement.

## 2. If `w_t!=0`, a binary diagonal frame has one-row escape

Assume `w_t!=0`.  Coordinate restriction is then an isomorphism

```text
w^perp -> span(e_j,e_k)^*,
gamma |->(gamma_j,gamma_k).                          (15)
```

Choose its coordinate lifts `gamma^j,gamma^k` and put
`q'_a=q(gamma^a)`.  Substituting the coordinate first- and second-root
covectors into (14) gives the complete table

```text
per(r_a,p_b,q'_c)=delta_(a,b,c) T_c,
a,b,c in {j,k}.                                      (16)
```

The diagonal and crossed cells separately show that all three ordered row
families in (16) are two-planes.  By (7) and (11),

```text
span(r_j,r_k) subset S,
span(q'_j,q'_k) subset S,
p_k in S,                                            (17)
```

while `p_j` may lie outside `S`.  Relabel `j` as binary index zero and `k`
as binary index one.  The following lemma excludes exactly (16)--(17).

### Lemma 1 (binary diagonal frame with one middle-row escape)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field.  Let
`S subset W` be a three-space.  Let

```text
R=span(r_0,r_1),             Q=span(q_0,q_1) subset S
```

be two-planes, and let `P=span(p_0,p_1)` be a two-plane with `p_1 in S`.
There are no nonzero scalars `c_0,c_1` and fully transverse decomposable
tensors `T_0,T_1` satisfying

```text
per(r_a,p_b,q_c)=
  c_a T_a,                         a=b=c,
  0,                               otherwise,

a,b,c in {0,1}.                                      (18)
```

#### Proof: reduction to endpoint incidences

If `p_0 in S`, all three row planes lie in one three-space and S2AN's
binary-diagonal frame obstruction applies.  Assume `p_0` is outside `S` and
put

```text
S'=S direct-sum span(p_0),              dim S'=4.    (19)
```

If `R=Q`, write `q_c=sum_i L_(c,i)r_i` with `L` invertible.  Permanent
symmetry applied at `p_0` and `p_1` makes `L E_00` and `L E_11` symmetric,
so `L` is diagonal.  The crossed cells in (18) then give

```text
M_(r_0,r_1)|P=0,

M_(r_0,r_0)|P and M_(r_1,r_1)|P nonzero rank one
with images span(T_0), span(T_1).                    (20)
```

This is forbidden by S2AL Lemma 2 because the targets are fully transverse.
Hence assume `R!=Q`.  Their intersection in `S` is a line.  Choose a
nonzero representative

```text
ell=a_0r_0+a_1r_1=b_0q_0+b_1q_1.                    (21)
```

Equation (18) gives the exact square values

```text
M_(ell,ell)(p_0)=a_0b_0c_0T_0,
M_(ell,ell)(p_1)=a_1b_1c_1T_1.                      (22)
```

If both are nonzero, one square map contains two fully transverse
decomposable tensors, contradicting S2AL tangent-line separation.  Thus
`ell` is a coordinate line in at least one of the ordered planes `R,Q`.

Suppose it is coordinate in exactly one.  Exchanging the first and third
permanent arguments if necessary, and rescaling row representatives, write

```text
ell=r_a=q_0+q_1.                                     (23)
```

For `a=0`, the square map `M_(ell,ell)|P` has image `span(T_0)`, while
`M_(ell,r_1)|P` has image `span(T_1)`; both maps are nonzero and rank one.
For `a=1` the roles reverse.  S2AL mixed factor sharing says their
decomposable images share a source factor, contrary to full transversality.
Therefore `ell` is coordinate in both ordered planes:

```text
ell=r_a=q_b,                         (a,b) in {0,1}^2. (24)
```

This leaves four endpoint incidences.

#### Proof: the 28 endpoint normal forms

Fix `(a,b)` in (24).  Rescale row representatives and choose a basis of
`S'` so that

```text
r_a=q_b=e_0,       r_(1-a)=e_1,       q_(1-b)=e_2,
p_0=e_3.                                               (25)
```

Since `0!=p_1 in S`, independent diagonal rescaling of `e_0,e_1,e_2`
puts it in exactly one of the seven forms

```text
p_1=epsilon_0e_0+epsilon_1e_1+epsilon_2e_2,
(epsilon_0,epsilon_1,epsilon_2) in {0,1}^3 minus {(0,0,0)}. (26)
```

Rescaling the two target-factor representatives absorbs the two nonzero
constants in (18).  Extend their factor lines to source bases and denote the
restrictions of the first two source-coordinate forms to `S'` by

```text
xi_0,xi_1, eta_0,eta_1, zeta_0,zeta_1 in (S')^*.    (27)
```

Their 24 coefficients in the basis (25) are indeterminates.  For each of
the eight source triples `(u,v,w) in {0,1}^3` and eight row triples
`(i,l,h) in {0,1}^3`, expand

```text
sum_(sigma in S_3)
  xi_u(row_(sigma,1)) eta_v(row_(sigma,2))
  zeta_w(row_(sigma,3)).                              (28)
```

The 64 equations set (28) to one only for the paired triples

```text
(u,v,w;i,l,h)=(0,0,0;0,0,0),
                    (1,1,1;1,1,1),                  (29)
```

and to zero otherwise.  Every realization of (18) would solve this
restricted source-coordinate subsystem; coefficients involving the third
source-coordinate lines are not needed for the contradiction.

For all four choices in (24) and all seven masks in (26), the durable
certificate supplies an exact rational identity

```text
1=sum_(nu=1)^64 h_nu f_nu,                           (30)
```

where the `f_nu` are the equations (28)--(29).  The 28 identities contain
2,310 sparse multiplier terms in total.  Their SHA-256 is

```text
3ea2f9470d210d85f2b45dce6fd23126888701a37634f07a32dd6750b71e96d5. (31)
```

Both replay programs reconstruct the 64 generators from (25)--(29) before
checking (30); neither trusts a stored generator list.  The independent
audit reverses all 24 variables and uses a separate standard-library sparse
permanent expander.  Since (30) has rational coefficients, it remains a
unit-ideal identity after scalar extension to every characteristic-zero
field.  Thus none of the 28 cases exists.  This proves Lemma 1.  QED.

Applying Lemma 1 to (16)--(17) contradicts `w_t!=0`.  Therefore (4) holds.

## 3. Proof-topology consequence

Together with S2BB and S2BC, the live `(1,2,2)` rank-five coloop frontier is
now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);

beta_j coloop, j!=t:
  w_t!=0:                                           IMPOSSIBLE;
  w_t=0:                                            OPEN;

three gamma_k coloops / two complementary alpha coloops
  / joint rank <=4 / other components / higher m:  OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.     (32)
```

The theorem closes no complete coordinate-coloop orientation.  No finite
field scan, numerical specialization, bounded sample, generic-point
promotion, or unproved incidence cover enters the proof.  The only finite
case split follows from the proved plane-intersection fork (21)--(24) and
the complete nonzero support split (26); every leaf has an exact rational
identity (30).

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_support_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_support_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_support_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_support_localization.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_certificates.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_support_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_support_localization.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_certificates.py
```

The primary verifier uses SymPy rational polynomials.  The independent audit
imports no repository module or third-party package.  Regeneration is
optional and requires Singular 4.x, directly or through WSL:

```text
python claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_certificates.py
```

Singular is not needed to replay either pinned proof certificate.

## Dependencies

- [`(1,2,2)` coordinate-coloop localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COORDINATE_COLOOP_LOCALIZATION_THEOREM.md)
- [Tangent-line, mixed-factor, and two-square lemmas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#2-two-exact-two-plane-lemmas)
- [Three-plane binary-diagonal frame obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_LOCALIZATION_THEOREM.md#2-a-three-plane-cannot-carry-a-binary-diagonal-permanent-frame)
