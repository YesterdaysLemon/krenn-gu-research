# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` residual second-root-coloop exclusion

## Status

**Exact characteristic-zero exclusion of both residual second-root coordinate
coloops on the normalized, target-consistent physical `m=3`
common-three-space full-sensor stratum.**  Retain

```text
dim U=3,                         rank H=5,

ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2.                     (1)
```

For either colour `j!=t`, the coordinate-coloop alternative

```text
N=K^perp subset {beta_j=0}                           (2)
```

is impossible.

S2BE--S2BI reduce (2) to one terminal chart.  If `k` is the third colour,
then for one `s in {j,k}` and the other colour `u`,

```text
{s,u,t}={0,1,2},
y=y_u e_u,                  y_u!=0,
w=e_u,
z=z_u e_u+z_t e_t,          z_t!=0.                 (3)
```

The final determinant face has two fully transverse targets sharing the
same active middle and third rows.  The residual-coloop quotient supplies
more than a bare plane intersection: according as `j=s` or `j=u`, either
the two active rows cancel modulo the first-row plane or the inactive middle
row already lies in that plane.  This reduces the actual row-space orbit to
`9+6=15` polynomial families.  Exact rational Nullstellensatz identities
exclude all 15; an equal-plane boundary is excluded directly by permanent
symmetry.

This closes only the two residual `beta_j` coloop orientations.  The three
third-root coloops, two complementary first-root coloops, joint rank at most
four, other physical component and pole strata, higher orders, and the
global conjecture remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The terminal same-pair determinant face

Normalize (3) and choose a projective direction `delta=[h:kappa]` avoiding

```text
h=0,                 kappa=0,                 h=kappa z_u. (4)
```

This is possible over every infinite characteristic-zero field.  The two
determinant-pencil planes from S2BF are

```text
P_delta={beta:kappa y_u beta_u-h mu beta_t=0},
Q_delta={gamma:kappa gamma(z)-h gamma(w)=0}.        (5)
```

They have the exact ordered bases

```text
P_delta=span(beta_*,e_s^*),
beta_*=h mu e_u^*+kappa y_u e_t^*,

Q_delta=span(gamma_*,e_s^*),
gamma_*=kappa z_t e_u^*+(h-kappa z_u)e_t^*.        (6)
```

Every displayed active coefficient is nonzero by (3)--(4).  On the complete
derivative-zero face

```text
alpha_s=0,                 beta in P_delta,
                            gamma in Q_delta,
```

the target equation gives

```text
per(r_u,p_*,q_*)=c_u T_u,
per(r_t,p_*,q_*)=c_t T_t,             c_u c_t!=0,  (7)

per(r_a,p_b,q_c)=0 at the other six binary cells, (8)
```

where

```text
r_a=rho(e_a^*),      p_*=pi(beta_*),     p_s=pi(e_s^*),
q_*=theta(gamma_*),  q_s=theta(e_s^*),

R=span(r_u,r_t),     P=span(p_*,p_s),
Q=span(q_*,q_s).                                    (9)
```

The tensors `T_u,T_t` are fully transverse.  S2BC makes `pi,theta`
injective, so every row plane and every row displayed in (9) is genuine.

Because `z,w` form a basis of `e_s^perp`, their common annihilator is
`span(e_s^*)`.  The S2BF pure-third-root row therefore gives

```text
q_s in R.                                           (10)
```

Thus `R` and `Q` lie in one space `S=R+Q` of dimension at most three.  If
`P subset S`, the S2BC same-pair obstruction applies after relabelling the
active rows and excludes (7)--(8).  It remains that `P intersect S` is one
line.

## 2. The equal first/third-plane boundary

Suppose `Q=R`.  Write

```text
q_c=sum_d L_(c,d)r_d,                    L in GL_2. (11)
```

For fixed `p_*`, let

```text
H_(a,d)=per(r_a,p_*,r_d),
F_(a,c)=per(r_a,p_*,q_c).                           (12)
```

Permanent symmetry makes `H` symmetric, while

```text
H=F (L^T)^(-1).                                    (13)
```

In the table (7)--(8), the `T_u` coefficient of `F` is a nonzero multiple
of `E_00`, and the `T_t` coefficient is a nonzero multiple of `E_10`.
Put `M=(L^T)^(-1)`.  Symmetry of `E_00 M` forces `M_01=0`; symmetry of
`E_10 M` then forces `M_00=0`.  The first row of `M` vanishes, contradicting
invertibility.  Hence

```text
Q!=R,                  dim S=3,
R intersect Q=span(q_s).                            (14)
```

## 3. The two residual-coloop orientations

There are two cases, according to which coordinate divisor is selected in
(2).

### Case A: the selected colour is `j=s`

The line `P_delta intersect {beta_s=0}` is `span(beta_*)`.  Its evaluation
pair is nonzero.  Scale `gamma_*` so its evaluation pair is opposite.  The
S2BF residual-coloop quotient identity gives

```text
p_*+q_* in R.                                       (15)
```

Thus the active middle row is the line `P intersect S`; the inactive row
`p_s` is the escaping row.

### Case B: the selected colour is `j=u`

For the generic direction (4),

```text
P_delta intersect {beta_u=0}=span(e_s^*).          (16)
```

This row has zero evaluation pair.  The zero-pair branch of the S2BF
residual-coloop quotient identity gives

```text
p_s in R.                                           (17)
```

Thus the inactive middle row is the line `P intersect S`; the active row
`p_*` is the escaping row.

These alternatives are exact consequences of which of the two residual
divisors is selected; they are not an additional genericity assumption.

## 4. The complete 15-family normal-form cover

Use (14) to choose a basis `(e_0,e_1,e_2)` of `S` with

```text
(r_u,r_t)=(e_0,e_1),                 q_*=e_2.       (18)
```

Independent nonzero row rescaling puts the intersection line `q_s` in one
of its three exact support types

```text
q_s=e_0,                q_s=e_1,                q_s=e_0+e_1. (19)
```

Adjoin an escaping row `e_3`.

In Case A, equation (15) gives three affine patches for the vector
`p_*+q_* in R`:

```text
(p_*,p_s)=(e_0+tau e_1-e_2,e_3),
            (e_1-e_2,e_3),
            (e_2,e_3).                              (20)
```

The last form represents the zero sum after harmless rescaling of the
active middle row; its induced nonzero target scalars are absorbed in
`c_u,c_t`.  Equations (19)--(20) give

```text
3*3=9                                                (21)
```

families.

In Case B, equation (17) gives the two affine patches for the nonzero line
`span(p_s) subset R`:

```text
(p_*,p_s)=(e_3,e_0+tau e_1),
            (e_3,e_1).                              (22)
```

Equations (19) and (22) give

```text
3*2=6                                                (23)
```

families.  The parameter identities below are polynomial in `tau` and
therefore include every endpoint value.  No parameter is sampled, inverted,
or promoted from a generic point.

## 5. Exact rational certificates

Choose source-coordinate bases whose first two factor lines are those of
`T_u,T_t`.  Restrict the six selected coordinate forms to the four-space
spanned by `(e_0,e_1,e_2,e_3)`.  For all eight selected source triples and
all eight binary row triples, expand the polarized permanent.  Rescale the
two nonzero target coefficients.  The required value is one exactly at

```text
(source;row)=(000;000),              (111;100),      (24)
```

and zero at the other 62 positions.  Every realization of (7)--(8) in one
of (19)--(22) would solve these 64 necessary cubic equations.

For all 15 families, the durable certificate supplies an exact identity

```text
1=sum_(nu=1)^64 h_nu f_nu.                           (25)
```

The identities contain 32,871 sparse multiplier terms.  Their SHA-256 is

```text
bc63359ece10e7d12237ab5821f64227de8391b5a9422091d9b5c0591484a7a0. (26)
```

The identities are rational polynomial identities, including in `tau`, so
they remain valid after scalar extension to every characteristic-zero
field.  The primary replay reconstructs every generator with SymPy.  The
independent audit imports no repository module or third-party package,
reverses all 26 certificate variables, and rebuilds all permanents with
standard-library rational sparse arithmetic.  Thus every case in
(21),(23) is impossible.

The equal-plane contradiction, the all-in-space S2BC lemma, and the 15
certified proper-intersection families exhaust the terminal chart.  This
contradicts (2) for both `j!=t` and proves the theorem.

## 6. Proof-topology consequence

The live `(1,2,2)` rank-five coloop frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);
both residual beta_j coloops, j!=t:                IMPOSSIBLE;

three gamma_k coloops / two complementary alpha coloops
  / joint rank <=4 / other components / higher m:  OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.     (27)
```

No exact counterexample is produced.  No finite-field computation,
numerical specialization, local monomial-order unit test, bounded parameter
sample, or unproved incidence cover enters the proof.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_exclusion.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_terminal_same_pair_certificates.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_exclusion.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_terminal_same_pair_certificates.py
```

Optional deterministic certificate regeneration requires Singular 4.x,
directly or through WSL:

```text
python claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_terminal_same_pair_certificates.py
```

Singular is not needed for either replay.

## Dependencies

- [`(1,2,2)` residual second-root-coloop terminal endpoint localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COMMON_MIDDLE_ROW_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` residual second-root-coloop projective-pencil geometry](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` determinant-face pencil, injectivity, and same-pair obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md)
