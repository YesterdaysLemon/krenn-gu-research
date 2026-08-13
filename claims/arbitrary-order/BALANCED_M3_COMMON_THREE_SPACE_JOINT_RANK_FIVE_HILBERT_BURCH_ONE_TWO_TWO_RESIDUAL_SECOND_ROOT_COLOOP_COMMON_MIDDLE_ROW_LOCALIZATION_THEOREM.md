# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` residual second-root-coloop common-middle-row localization

## Status

**Exact characteristic-zero localization of every surviving residual
second-root coordinate-coloop endpoint to one terminal aligned chart on the
normalized, target-consistent physical `m=3` common-three-space full-sensor
stratum.**  Retain

```text
dim U=3,                         rank H=5,

ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2,                     (1)
```

and suppose

```text
N=K^perp subset {beta_j=0},                   j!=t.  (2)
```

Let `k` be the third colour.  By S2BE--S2BH, every surviving endpoint has

```text
s in {j,k},
y proportional to e_u,          {s,u,t}={0,1,2},
w proportional to e_s or e_u.                         (3)
```

Absorb the nonzero endpoint scalar.  This theorem proves the sharper
localization

```text
w=e_u,                          z_s=0.               (4)
```

In particular `z_t!=0`, because `z,w` are independent and both lie in
`e_s^perp` under (4).

The new permanent lemma excludes a binary table in which the two fully
transverse targets share the active row of the only plane allowed to escape
the common three-space.  Its exact row-space cover has ten first/third-plane
incidence types, three positions of the escaping plane's intersection line,
and three affine patches for that line, for `10*3*3=90` cases.  Every case
has a pinned rational Nullstellensatz identity.

This is a localization, not an exclusion of either residual coloop or of
the terminal chart (4).  The three third-root coloops, two complementary
first-root coloops, joint rank at most four, other physical component and
pole strata, higher orders, and the global conjecture also remain open.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. A common active middle row cannot escape a three-space

### Lemma 1 (intersecting common-middle-row obstruction)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field.  Let
`S subset W` have dimension at most three.  Suppose

```text
R=span(r_0,r_1),       Q=span(q_0,q_1) subset S
```

are two-planes and `P=span(p_0,p_1)` is a two-plane satisfying

```text
P intersect S !=0.                                  (5)
```

There are no nonzero scalars `c_0,c_1` and fully transverse decomposable
tensors `T_0,T_1` such that

```text
per(r_0,p_0,q_0)=c_0T_0,
per(r_1,p_0,q_1)=c_1T_1,                            (6)

per(r_a,p_b,q_c)=0                 at the other six binary cells. (7)
```

#### The all-in-space and equal-plane cases

If `P subset S`, reorder the permanent arguments as `(R,Q,P)`.  Equations
(6)--(7) are the S2AO same-third-row table, with common third row `p_0`,
and are impossible.

Assume from now on that `P intersect S` is a line.  If `R=Q`, write

```text
q_c=sum_d L_(c,d)r_d,                    L in GL_2. (8)
```

At `p_0`, the coefficient matrix in the ordered `R,Q` bases is
`diag(c_0T_0,c_1T_1)`.  Converting the `Q` basis to the `R` basis must give
a symmetric matrix.  Since the two fully transverse targets are linearly
independent, both off-diagonal entries of `(L^T)^(-1)` vanish.  Thus `L` is
diagonal.  After rescaling,

```text
q_0=r_0,                         q_1=r_1.            (9)
```

This is the equal-plane normal form below.

#### The nine distinct-plane incidence types

If `R!=Q`, then `S=R+Q` has dimension three.  Put

```text
ell=R intersect Q
   =span(a_0r_0+a_1r_1)
   =span(b_0q_0+b_1q_1).                            (10)
```

Each ordered coefficient pair in (10) has support `{0}`, `{1}`, or
`{0,1}`.  Independent nonzero rescaling of the four indexed rows normalizes
every nonzero coefficient to one; the induced changes are absorbed in the
two arbitrary nonzero constants in (6).  Therefore (10) has exactly

```text
3*3=9                                                (11)
```

incidence types.  Choose a basis `(e_0,e_1,e_2)` of `S` with
`r_0=e_0,r_1=e_1`.  The intersection row is one of

```text
ell=e_0,                 ell=e_1,                 ell=e_0+e_1. (12)
```

For each choice in (12), the three normalized `Q` types are

```text
(q_0,q_1)=(ell,e_2),
            (e_2,ell),
            (e_2,ell-e_2).                          (13)
```

Together with the equal-plane form (9), equations (12)--(13) give ten
complete first/third-plane incidence types.

#### The escaping-plane line and its affine cover

Let `v` span `P intersect S`.  Relative to the ordered basis `(p_0,p_1)`,
the line is `p_0`, `p_1`, or has both coefficients nonzero.  Rescale the
two rows in the last case.  After adjoining an escaping basis vector `e_3`,
the three exact orientations are

```text
(p_0,p_1)=(e_3,v),
            (v,e_3),
            (e_3,v-e_3).                            (14)
```

Every nonzero projective `v in S` belongs to exactly the first applicable
affine patch

```text
v=e_0+tau e_1+sigma e_2,
v=e_1+tau e_2,
v=e_2.                                               (15)
```

No parameter is sampled or inverted.  Equations (9), (12)--(15) give the
complete `10*3*3=90` row-space cover.

Choose source-coordinate bases whose first two factor lines are those of
`T_0,T_1`.  Restrict the six selected coordinate forms to the four-space
`S'=S+P`.  For all eight selected source triples and all eight binary row
triples, expand the polarized permanent.  Normalize the two nonzero target
coefficients to one.  The required values are one exactly at

```text
(source;row)=(000;000),              (111;101),      (16)
```

and zero at the other 62 positions.  Every realization of (6)--(7) would
therefore solve these 64 necessary cubic equations.

For all 90 normal forms, the durable certificate gives an exact rational
identity

```text
1=sum_(nu=1)^64 h_nu f_nu.                           (17)
```

The identities contain 31,591 sparse multiplier terms.  Their SHA-256 is

```text
a56242675744f848fc4f747045ce9b2a18c7b32ae2152ca800bd6c654d29e8d1. (18)
```

The identities on the first two patches are polynomial in `tau,sigma` or
`tau`; they use no localization, inverse, or specialization.  The primary
replay reconstructs every generator with SymPy.  The independent audit
reverses all 26 variables, imports no repository module or third-party
package, and expands every permanent separately with rational sparse
arithmetic.  Thus (17) holds after scalar extension to every
characteristic-zero field and excludes all 90 cases.  This proves Lemma 1.
QED.

## 2. Every nonterminal endpoint exposes Lemma 1

Normalize the surviving coordinates as

```text
(s,u,t)=(0,1,2),                 y=y_u e_u,         y_u!=0. (19)
```

For a projective direction `delta=[h:kappa]`, the determinant-pencil planes
are

```text
P_delta={beta:kappa y_u beta_u-h mu beta_t=0},
Q_delta={gamma:kappa gamma(z)-h gamma(w)=0}.        (20)
```

The first plane always has the exact basis

```text
P_delta=span(e_s^*,beta_*),
beta_*=h mu e_u^*+kappa y_u e_t^*.                 (21)
```

Its two active coordinates are nonzero when `h kappa!=0`.  The projection
of `Q_delta` to the `{u,t}` coordinates is invertible exactly when

```text
L_Q(h,kappa)=kappa z_s-h w_s !=0.                   (22)
```

Suppose the linear form in (22) is not identically zero.  Over the infinite
characteristic-zero field, choose a direction avoiding its one zero and the
two coordinate directions `h kappa=0`.  Let `gamma^u,gamma^t` be the exact
coordinate lifts in `Q_delta`.  On the complete derivative-zero face

```text
alpha_s=0,           beta in P_delta,       gamma in Q_delta,
```

the target equation gives, for `a,c in {u,t}`,

```text
per(r_a,p(beta_*),q(gamma^c))
  =delta_(a,c) (beta_*)_a T_a,

per(r_a,p_s,q(gamma^c))=0.                         (23)
```

Both active coefficients in (23) are nonzero.  S2BF puts
`R=rho(e_s^perp)`, the full plane `q(Q_delta)`, and a nonzero line of
`p(P_delta)` in one space of dimension at most three.  S2BC makes `pi` and
`theta` injective, so none of the displayed planes or the intersection line
collapses.  Equation (23) is exactly Lemma 1, with the common active middle
row `p(beta_*)`.  This contradiction proves

```text
L_Q(h,kappa) identically zero,
z_s=w_s=0.                                          (24)
```

S2BH leaves `w=e_s` or `w=e_u`.  The first has `w_s=1`, contrary to (24).
Hence `w=e_u`, and (24) gives `z_s=0`.  This proves (4).  Since
`z,w` are independent, `z_t` is nonzero as claimed.

## 3. Proof-topology consequence

The live `(1,2,2)` rank-five coloop frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);

beta_j coloop, j!=t:
  s=t:                                              IMPOSSIBLE (S2BG);
  s in {j,k}, y=e_u:
    w=e_s or z_s!=0:                               IMPOSSIBLE;
    w=e_u, z_s=0, z_t!=0:                          OPEN;

three gamma_k coloops / two complementary alpha coloops
  / joint rank <=4 / other components / higher m:  OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.     (25)
```

No terminal endpoint is asserted to exist.  No finite-field scan,
numerical specialization, bounded parameter sample, or unproved incidence
cover enters the proof.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_localization.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_certificates.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_localization.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_certificates.py
```

Optional deterministic certificate regeneration requires Singular 4.x,
directly or through WSL:

```text
python claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_common_middle_row_certificates.py
```

Singular is not needed for either replay.

## Dependencies

- [`(1,2,2)` residual second-root-coloop complementary-`y` localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COMPLEMENTARY_Y_COORDINATE_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` residual second-root-coloop projective-pencil geometry](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` determinant-face pencil and `pi,theta` injectivity](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md)
- [Three-space same-third-row obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_SUPPORT_LOCALIZATION_THEOREM.md#2-a-same-third-row-binary-diagonal-frame-is-impossible)
